#!/usr/bin/env python3
"""Executor-repaired MA-SQLGrid C1-C5 experiment runner.

The runner keeps the formal prediction path gold-free. Gold SQL and dataset
answer metadata are loaded only after predictions are written, for evaluator
scoring and diagnostics.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import sqlite3
import statistics
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


HYPERPARAMETERS = {
    "temperature": 0,
    "max_tokens": 700,
    "model_call_attempts": 4,
    "repair_attempts": 1,
    "c5_candidate_limit": 5,
    "formal_seed_count": 1,
    "smoke_seed_count": 3,
    "time_budget_sec": 7200,
}

FORMAL_SEEDS = [0]
SMOKE_SEEDS = [0, 1, 2]
FORMAL_SEED_POLICY = "single deterministic pass"
SMOKE_SEED_POLICY = "three-seed dev smoke for contract evidence only"
CONDITION_ORDER = [
    "C1_SchemaOnly_Direct",
    "C2_FullSchemaValues_Direct",
    "C3_CHESSLite_Generic",
    "C4_MASQLGrid_DomainContext",
    "C5_MASQLGrid_DomainContext_Validated",
]
FORBIDDEN_PREDICTION_FIELDS = {
    "gold_sql",
    "gold_result",
    "expected_result_hash",
    "execution_accuracy",
    "correct",
}
REQUIRED_PREDICTION_FIELDS = {
    "question_id",
    "condition",
    "model",
    "provider",
    "prompt_hash",
    "schema_context_hash",
    "input_contract_version",
    "predicted_sql",
    "candidate_sql",
    "selected_candidate_index",
    "intermediate_trace_path",
    "latency_ms",
    "token_input",
    "token_output",
    "retry_count",
    "error",
}

EXPERIMENT_DIR = Path(__file__).resolve().parent
STAGE10_DIR = EXPERIMENT_DIR.parent
FALLBACK_WORKSPACE = Path(
    "/media/lenovo/data2/cja/GridMind/references/AutoResearchClaw/"
    "paper_workspace/workspaces/ma-sqlgrid-value-grounded-restart"
)


def resolve_workspace() -> Path:
    env_workspace = os.environ.get("MA_SQLGRID_WORKSPACE")
    if env_workspace and Path(env_workspace).exists():
        return Path(env_workspace).resolve()
    for parent in [EXPERIMENT_DIR, *EXPERIMENT_DIR.parents]:
        if (parent / "data" / "griddb_maintenance_v2_v0_1" / "database.sqlite").exists():
            return parent.resolve()
    return FALLBACK_WORKSPACE.resolve()


WORKSPACE = resolve_workspace()
REPO_ROOT = WORKSPACE.parents[2]
DATA_DIR = WORKSPACE / "data" / "griddb_maintenance_v2_v0_1"
DB_PATH = DATA_DIR / "database.sqlite"
QUESTIONS_PATH = DATA_DIR / "questions.jsonl"
SCHEMA_PATH = DATA_DIR / "schema.sql"
OUT_DIR = Path(os.environ.get("MA_SQLGRID_OUTPUT_DIR", EXPERIMENT_DIR / "outputs")).resolve()
TRACE_DIR = OUT_DIR / "traces"
PREDICTIONS_PATH = OUT_DIR / "predictions.jsonl"
SCORES_PATH = OUT_DIR / "scores.jsonl"
CONTEXTS_PATH = OUT_DIR / "contexts.jsonl"
REPORT_PATH = OUT_DIR / "report.md"
RESULTS_PATH = OUT_DIR / "results.json"

sys.path.insert(0, str(WORKSPACE / "smoke"))
sys.path.insert(0, str(WORKSPACE / "evaluator"))
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(STAGE10_DIR / "agent_reference"))
sys.path.insert(0, str(EXPERIMENT_DIR))

from evaluator import (  # noqa: E402
    execute_sql,
    load_questions,
    score_prediction,
    validate_dataset,
    validate_read_only_select,
)
from experiment_harness import ExperimentHarness  # noqa: E402
from researchclaw.llm.client import LLMClient, LLMConfig  # noqa: E402

import dev_chess_style_pilot as chess  # noqa: E402
import minimal_text2sql_smoke as smoke  # noqa: E402


@dataclass
class ScoreRow:
    question_id: str
    condition: str
    seed: int
    safe_sql: bool
    evaluator_correct: bool
    evaluator_error_type: str
    evaluator_details: str
    contract_errors: list[str]
    answer_shape_ok: bool
    value_hint_coverage: float
    table_selection_recall: float | None
    column_selection_recall: float | None
    prompt_token_estimate: int
    latency_ms: int
    provider_error: bool


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def set_all_seeds(seed: int) -> None:
    random.seed(seed)


def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)


def clean_run_outputs() -> None:
    for path in [PREDICTIONS_PATH, SCORES_PATH, CONTEXTS_PATH, REPORT_PATH, RESULTS_PATH]:
        path.unlink(missing_ok=True)
    if TRACE_DIR.exists():
        for trace_path in TRACE_DIR.glob("*.json"):
            trace_path.unlink(missing_ok=True)


def relative_to_workspace(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(WORKSPACE))
    except ValueError:
        return str(path.resolve())


def llm_client() -> LLMClient:
    api_key = os.environ.get("KRILL_API_KEY")
    if not api_key:
        raise RuntimeError("KRILL_API_KEY is required for model-backed MA-SQLGrid runs")
    return LLMClient(
        LLMConfig(
            base_url=smoke.BASE_URL,
            api_key=api_key,
            primary_model=smoke.MODEL_NAME,
            fallback_models=[],
            max_tokens=int(HYPERPARAMETERS["max_tokens"]),
            temperature=float(HYPERPARAMETERS["temperature"]),
            timeout_sec=90,
            wire_api=smoke.WIRE_API,
        )
    )


def call_model_with_retries(client: LLMClient, prompt: str) -> tuple[str, str, int, int, int, int]:
    last_exc: Exception | None = None
    total_latency_ms = 0
    for attempt in range(int(HYPERPARAMETERS["model_call_attempts"])):
        start = time.monotonic()
        try:
            response = client.chat(
                [{"role": "user", "content": prompt}],
                max_tokens=int(HYPERPARAMETERS["max_tokens"]),
                temperature=float(HYPERPARAMETERS["temperature"]),
            )
            latency_ms = int((time.monotonic() - start) * 1000)
            total_latency_ms += latency_ms
            return (
                response.content,
                response.model or smoke.MODEL_NAME,
                total_latency_ms,
                int(response.prompt_tokens or 0),
                int(response.completion_tokens or 0),
                attempt,
            )
        except Exception as exc:
            last_exc = exc
            total_latency_ms += int((time.monotonic() - start) * 1000)
            time.sleep(min(8, 2 * (attempt + 1)))
    assert last_exc is not None
    raise last_exc


def load_split_records(mode: str) -> list[dict[str, Any]]:
    split_name = "dev" if mode == "smoke" else "test"
    splits = json.loads((DATA_DIR / "splits.json").read_text(encoding="utf-8"))
    split_ids = list(splits[split_name])
    requested_ids = [item.strip() for item in os.environ.get("MA_SQLGRID_QUESTION_IDS", "").split(",") if item.strip()]
    if requested_ids:
        allowed = set(split_ids)
        outside_split = [qid for qid in requested_ids if qid not in allowed]
        if outside_split:
            raise RuntimeError(f"MA_SQLGRID_QUESTION_IDS contains ids outside {split_name} split: {outside_split}")
        split_ids = requested_ids
    if mode == "smoke":
        limit = int(os.environ.get("MA_SQLGRID_SMOKE_QUESTIONS", "2"))
        if not requested_ids:
            split_ids = split_ids[: max(1, limit)]
    else:
        limit_env = os.environ.get("MA_SQLGRID_MAX_QUESTIONS")
        if limit_env and not requested_ids:
            split_ids = split_ids[: max(1, int(limit_env))]
    by_id = {record["question_id"]: record for record in load_questions(QUESTIONS_PATH)}
    records = [by_id[qid] for qid in split_ids]
    wrong_split = [record["question_id"] for record in records if record["split"] != split_name]
    if wrong_split:
        raise RuntimeError(f"records do not match requested {split_name} split: {wrong_split}")
    return records


def seeds_for_mode(mode: str) -> list[int]:
    return SMOKE_SEEDS if mode == "smoke" else FORMAL_SEEDS


def load_context_bundle(conn: sqlite3.Connection, record: dict[str, Any]) -> dict[str, Any]:
    schema_only_context = "\n".join(["SQLite schema:", SCHEMA_PATH.read_text(encoding="utf-8").strip()])
    full_schema_values_context = chess.render_full_schema_values(conn)
    generic = chess.generic_context(conn, record)
    domain = chess.infer_domain_context(conn, record)
    return {
        "schema_only_context": schema_only_context,
        "full_schema_values_context": full_schema_values_context,
        "generic": generic,
        "domain": domain,
        "generic_text": chess.render_selected_context(generic, domain=False),
        "domain_text": chess.render_selected_context(domain, domain=True),
    }


def direct_prompt(record: dict[str, Any], context_text: str, condition: str) -> str:
    return f"""You are a Text-to-SQL system for a synthetic SQLite power-grid maintenance database.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.
Use only the provided database context. When normalization hints or answer-shape hints are present, treat them as question-derived constraints. Match the requested projection count and include relevant literal predicates.

Condition: {condition}

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
"""


def candidate_prompt(record: dict[str, Any], context_text: str, condition: str) -> str:
    return f"""You are generating candidate SQLite SQL for CHESS-style MA-SQLGrid.

Return 3 distinct read-only SQLite SELECT queries as a numbered list. Do not include explanation.
Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.
Use only the selected context, normalization hints, and inferred output-form hints below. Candidate queries should differ in plausible joins/projections while respecting the inferred projection count and relevant literal predicates.

Condition: {condition}

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
"""


def repair_prompt(record: dict[str, Any], context_text: str, sql: str, validation: dict[str, Any]) -> str:
    return f"""Repair this SQLite SELECT query using only selected context and inferred hints.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
Previous SQL: {sql}
Reference-free validation result: {json.dumps(validation, sort_keys=True)}
"""


def prediction_record(
    *,
    question_id: str,
    condition: str,
    seed: int,
    model: str,
    prompt: str,
    context_text: str,
    predicted_sql: str,
    candidate_sql: list[str],
    selected_candidate_index: int,
    trace_path: Path,
    latency_ms: int,
    token_input: int,
    token_output: int,
    retry_count: int,
    error: str | None,
) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "condition": condition,
        "seed": seed,
        "model": model,
        "provider": smoke.PROVIDER,
        "prompt_hash": sha256_text(prompt),
        "schema_context_hash": sha256_text(context_text),
        "input_contract_version": "griddb-maintenance-v2-v0.1/no-gold-v1",
        "predicted_sql": predicted_sql,
        "candidate_sql": candidate_sql,
        "selected_candidate_index": selected_candidate_index,
        "intermediate_trace_path": relative_to_workspace(trace_path),
        "latency_ms": latency_ms,
        "token_input": token_input,
        "token_output": token_output,
        "retry_count": retry_count,
        "error": error,
    }


def validate_prediction_contract(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_PREDICTION_FIELDS - set(record)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    leaked = sorted(FORBIDDEN_PREDICTION_FIELDS & set(record))
    if leaked:
        errors.append(f"prediction record contains forbidden fields: {leaked}")
    if record.get("provider") != smoke.PROVIDER:
        errors.append(f"provider must be {smoke.PROVIDER}")
    if record.get("model") and not str(record["model"]).startswith(smoke.MODEL_NAME):
        errors.append(f"model must be {smoke.MODEL_NAME}-compatible")
    candidates = record.get("candidate_sql")
    if not isinstance(candidates, list) or not candidates:
        errors.append("candidate_sql must be a non-empty list")
    selected = record.get("selected_candidate_index")
    if not isinstance(selected, int):
        errors.append("selected_candidate_index must be an integer")
    elif isinstance(candidates, list) and not (0 <= selected < len(candidates)):
        errors.append("selected_candidate_index out of range")
    if not isinstance(record.get("predicted_sql"), str) or not record["predicted_sql"].strip():
        errors.append("predicted_sql must be a non-empty string")
    return errors


def write_trace(trace_path: Path, payload: dict[str, Any]) -> None:
    trace_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class SchemaOnlyDirect:
    name = "C1_SchemaOnly_Direct"

    def predict(self, client: LLMClient, conn: sqlite3.Connection, record: dict[str, Any], bundle: dict[str, Any], seed: int) -> dict[str, Any]:
        context_text = bundle["schema_only_context"]
        prompt = direct_prompt(record, context_text, self.name)
        raw = ""
        model = smoke.MODEL_NAME
        latency_ms = 0
        token_input = 0
        token_output = 0
        retry_count = 0
        error = None
        sql = "SELECT 1;"
        try:
            raw, model, latency_ms, token_input, token_output, retry_count = call_model_with_retries(client, prompt)
            sql = smoke.extract_sql(raw)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        if not sql.strip():
            sql = "SELECT 1;"
            error = error or "empty SQL extracted"
        trace_path = TRACE_DIR / f"{record['question_id']}_seed{seed}_{self.name}.json"
        write_trace(trace_path, {"prompt": prompt, "raw_response": raw})
        return prediction_record(
            question_id=record["question_id"],
            condition=self.name,
            seed=seed,
            model=model,
            prompt=prompt,
            context_text=context_text,
            predicted_sql=sql,
            candidate_sql=[sql],
            selected_candidate_index=0,
            trace_path=trace_path,
            latency_ms=latency_ms,
            token_input=token_input,
            token_output=token_output,
            retry_count=retry_count,
            error=error,
        )


class FullSchemaValuesDirect:
    name = "C2_FullSchemaValues_Direct"

    def predict(self, client: LLMClient, conn: sqlite3.Connection, record: dict[str, Any], bundle: dict[str, Any], seed: int) -> dict[str, Any]:
        context_text = bundle["full_schema_values_context"]
        prompt = direct_prompt(record, context_text, self.name)
        raw = ""
        model = smoke.MODEL_NAME
        latency_ms = 0
        token_input = 0
        token_output = 0
        retry_count = 0
        error = None
        sql = "SELECT 1;"
        try:
            raw, model, latency_ms, token_input, token_output, retry_count = call_model_with_retries(client, prompt)
            sql = smoke.extract_sql(raw)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        if not sql.strip():
            sql = "SELECT 1;"
            error = error or "empty SQL extracted"
        trace_path = TRACE_DIR / f"{record['question_id']}_seed{seed}_{self.name}.json"
        write_trace(trace_path, {"prompt": prompt, "raw_response": raw})
        return prediction_record(
            question_id=record["question_id"],
            condition=self.name,
            seed=seed,
            model=model,
            prompt=prompt,
            context_text=context_text,
            predicted_sql=sql,
            candidate_sql=[sql],
            selected_candidate_index=0,
            trace_path=trace_path,
            latency_ms=latency_ms,
            token_input=token_input,
            token_output=token_output,
            retry_count=retry_count,
            error=error,
        )


class ChessLiteGeneric:
    name = "C3_CHESSLite_Generic"

    def predict(self, client: LLMClient, conn: sqlite3.Connection, record: dict[str, Any], bundle: dict[str, Any], seed: int) -> dict[str, Any]:
        context_text = bundle["generic_text"]
        prompt = direct_prompt(record, context_text, self.name)
        raw = ""
        model = smoke.MODEL_NAME
        latency_ms = 0
        token_input = 0
        token_output = 0
        retry_count = 0
        error = None
        sql = "SELECT 1;"
        try:
            raw, model, latency_ms, token_input, token_output, retry_count = call_model_with_retries(client, prompt)
            sql = smoke.extract_sql(raw)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        if not sql.strip():
            sql = "SELECT 1;"
            error = error or "empty SQL extracted"
        trace_path = TRACE_DIR / f"{record['question_id']}_seed{seed}_{self.name}.json"
        write_trace(trace_path, {"prompt": prompt, "raw_response": raw, "context_mode": "generic"})
        return prediction_record(
            question_id=record["question_id"],
            condition=self.name,
            seed=seed,
            model=model,
            prompt=prompt,
            context_text=context_text,
            predicted_sql=sql,
            candidate_sql=[sql],
            selected_candidate_index=0,
            trace_path=trace_path,
            latency_ms=latency_ms,
            token_input=token_input,
            token_output=token_output,
            retry_count=retry_count,
            error=error,
        )


class MASQLGridDomainContext:
    name = "C4_MASQLGrid_DomainContext"

    def predict(self, client: LLMClient, conn: sqlite3.Connection, record: dict[str, Any], bundle: dict[str, Any], seed: int) -> dict[str, Any]:
        context_text = bundle["domain_text"]
        prompt = direct_prompt(record, context_text, self.name)
        raw = ""
        model = smoke.MODEL_NAME
        latency_ms = 0
        token_input = 0
        token_output = 0
        retry_count = 0
        error = None
        sql = "SELECT 1;"
        try:
            raw, model, latency_ms, token_input, token_output, retry_count = call_model_with_retries(client, prompt)
            sql = smoke.extract_sql(raw)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        if not sql.strip():
            sql = "SELECT 1;"
            error = error or "empty SQL extracted"
        trace_path = TRACE_DIR / f"{record['question_id']}_seed{seed}_{self.name}.json"
        write_trace(trace_path, {"prompt": prompt, "raw_response": raw, "context_mode": "domain"})
        return prediction_record(
            question_id=record["question_id"],
            condition=self.name,
            seed=seed,
            model=model,
            prompt=prompt,
            context_text=context_text,
            predicted_sql=sql,
            candidate_sql=[sql],
            selected_candidate_index=0,
            trace_path=trace_path,
            latency_ms=latency_ms,
            token_input=token_input,
            token_output=token_output,
            retry_count=retry_count,
            error=error,
        )


class MASQLGridValidated:
    name = "C5_MASQLGrid_DomainContext_Validated"

    def predict(self, client: LLMClient, conn: sqlite3.Connection, record: dict[str, Any], bundle: dict[str, Any], seed: int) -> dict[str, Any]:
        context = bundle["domain"]
        context_text = bundle["domain_text"]
        prompt = candidate_prompt(record, context_text, self.name)
        raw = ""
        repair_raw = ""
        model = smoke.MODEL_NAME
        latency_ms = 0
        token_input = 0
        token_output = 0
        retry_count = 0
        error = None
        candidates = ["SELECT 1;"]
        try:
            raw, model, latency_ms, token_input, token_output, retry_count = call_model_with_retries(client, prompt)
            candidates = smoke.extract_candidate_sql(raw)[: int(HYPERPARAMETERS["c5_candidate_limit"])]
            if not candidates:
                candidates = ["SELECT 1;"]
                error = "no SQL candidate extracted"
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        selected_idx, rank_trace = chess.rank_candidates(conn, context, candidates)
        predicted_sql = candidates[selected_idx]
        validation = rank_trace[selected_idx] if rank_trace else chess.reference_free_validation(conn, context, predicted_sql)
        repaired_sql = ""
        if not error and int(HYPERPARAMETERS["repair_attempts"]) > 0:
            needs_repair = (
                not validation["exec_ok"]
                or not validation["shape_ok"]
                or not validation["order_ok"]
                or bool(validation["missing_value_hints"])
            )
            if needs_repair:
                try:
                    prompt2 = repair_prompt(record, context_text, predicted_sql, validation)
                    repair_raw, model2, repair_latency, repair_in, repair_out, repair_retries = call_model_with_retries(client, prompt2)
                    repaired_sql = smoke.extract_sql(repair_raw)
                    repaired_validation = chess.reference_free_validation(conn, context, repaired_sql)
                    if repaired_validation["exec_ok"] and (
                        not validation["exec_ok"]
                        or int(repaired_validation["shape_ok"]) >= int(validation["shape_ok"])
                        or repaired_validation["value_hits"] >= validation["value_hits"]
                    ):
                        candidates.append(repaired_sql)
                        selected_idx = len(candidates) - 1
                        predicted_sql = repaired_sql
                        rank_trace.append(
                            {
                                "candidate_index": selected_idx,
                                "sql": repaired_sql,
                                "ranker_score": None,
                                **repaired_validation,
                            }
                        )
                    latency_ms += repair_latency
                    token_input += repair_in
                    token_output += repair_out
                    retry_count += repair_retries
                    model = model2
                except Exception as exc:
                    error = f"repair {type(exc).__name__}: {exc}"
        trace_path = TRACE_DIR / f"{record['question_id']}_seed{seed}_{self.name}.json"
        write_trace(
            trace_path,
            {
                "prompt": prompt,
                "raw_response": raw,
                "rank_trace": rank_trace,
                "repair_raw_response": repair_raw,
                "repaired_sql": repaired_sql,
            },
        )
        return prediction_record(
            question_id=record["question_id"],
            condition=self.name,
            seed=seed,
            model=model,
            prompt=prompt,
            context_text=context_text,
            predicted_sql=predicted_sql,
            candidate_sql=candidates,
            selected_candidate_index=selected_idx,
            trace_path=trace_path,
            latency_ms=latency_ms,
            token_input=token_input,
            token_output=token_output,
            retry_count=retry_count,
            error=error,
        )


def condition_instances() -> dict[str, Any]:
    return {
        "C1_SchemaOnly_Direct": SchemaOnlyDirect(),
        "C2_FullSchemaValues_Direct": FullSchemaValuesDirect(),
        "C3_CHESSLite_Generic": ChessLiteGeneric(),
        "C4_MASQLGrid_DomainContext": MASQLGridDomainContext(),
        "C5_MASQLGrid_DomainContext_Validated": MASQLGridValidated(),
    }


def context_recall(record: dict[str, Any], context: dict[str, Any]) -> tuple[float, float]:
    selected_tables = set(context.get("selected_tables") or [])
    gold_tables = set(record.get("tables") or [])
    selected_columns = {
        f"{table}.{column}"
        for table, columns in (context.get("selected_columns") or {}).items()
        for column in columns
    }
    gold_columns = set(record.get("columns") or [])
    table_recall = 1.0 if not gold_tables else len(gold_tables & selected_tables) / len(gold_tables)
    column_recall = 1.0 if not gold_columns else len(gold_columns & selected_columns) / len(gold_columns)
    return table_recall, column_recall


def infer_context_for_prediction(prediction: dict[str, Any], bundles: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    bundle = bundles[prediction["question_id"]]
    if prediction["condition"] in {"C4_MASQLGrid_DomainContext", "C5_MASQLGrid_DomainContext_Validated"}:
        return bundle["domain"]
    if prediction["condition"] == "C3_CHESSLite_Generic":
        return bundle["generic"]
    return None


def score_predictions(
    conn: sqlite3.Connection,
    records: list[dict[str, Any]],
    bundles: dict[str, dict[str, Any]],
    predictions: list[dict[str, Any]],
) -> list[ScoreRow]:
    by_id = {record["question_id"]: record for record in records}
    scores: list[ScoreRow] = []
    for prediction in predictions:
        record = by_id[prediction["question_id"]]
        contract_errors = validate_prediction_contract(prediction)
        safe, _, _ = validate_read_only_select(prediction["predicted_sql"])
        score = score_prediction(conn, record, prediction["predicted_sql"])
        context = infer_context_for_prediction(prediction, bundles)
        validation = chess.reference_free_validation(conn, context or {"inferred_shape": {}, "normalized_value_hints": []}, prediction["predicted_sql"])
        value_hint_count = int(validation.get("value_hint_count") or 0)
        value_hint_coverage = 1.0 if value_hint_count == 0 else float(validation.get("value_hits") or 0) / value_hint_count
        table_recall = None
        column_recall = None
        if context is not None:
            table_recall, column_recall = context_recall(record, context)
        trace_path = WORKSPACE / prediction["intermediate_trace_path"]
        prompt_token_estimate = 0
        if trace_path.exists():
            prompt = json.loads(trace_path.read_text(encoding="utf-8")).get("prompt", "")
            prompt_token_estimate = chess.estimate_tokens(prompt)
        scores.append(
            ScoreRow(
                question_id=prediction["question_id"],
                condition=prediction["condition"],
                seed=int(prediction["seed"]),
                safe_sql=safe,
                evaluator_correct=score.correct,
                evaluator_error_type=score.error_type,
                evaluator_details=score.details,
                contract_errors=contract_errors,
                answer_shape_ok=bool(validation.get("shape_ok")),
                value_hint_coverage=value_hint_coverage,
                table_selection_recall=table_recall,
                column_selection_recall=column_recall,
                prompt_token_estimate=prompt_token_estimate,
                latency_ms=int(prediction.get("latency_ms") or 0),
                provider_error=bool(prediction.get("error")),
            )
        )
    return scores


def mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def std(values: list[float]) -> float:
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def aggregate_scores(scores: list[ScoreRow]) -> dict[str, Any]:
    by_condition_seed: dict[tuple[str, int], list[ScoreRow]] = {}
    by_condition: dict[str, list[ScoreRow]] = {}
    for row in scores:
        by_condition_seed.setdefault((row.condition, row.seed), []).append(row)
        by_condition.setdefault(row.condition, []).append(row)
    seed_metrics = {
        f"{condition}|{seed}": mean([1.0 if row.evaluator_correct else 0.0 for row in rows])
        for (condition, seed), rows in sorted(by_condition_seed.items())
    }
    condition_metrics = {}
    for condition in CONDITION_ORDER:
        seed_values = [value for key, value in seed_metrics.items() if key.startswith(f"{condition}|")]
        rows = by_condition.get(condition, [])
        condition_metrics[condition] = {
            "execution_accuracy_mean": mean(seed_values),
            "execution_accuracy_std": std(seed_values),
            "valid_sql_rate": mean([1.0 if row.safe_sql else 0.0 for row in rows]),
            "answer_shape_accuracy": mean([1.0 if row.answer_shape_ok else 0.0 for row in rows]),
            "value_hint_coverage": mean([row.value_hint_coverage for row in rows]),
            "prompt_token_estimate": mean([float(row.prompt_token_estimate) for row in rows]),
            "latency_ms": mean([float(row.latency_ms) for row in rows]),
            "provider_failure_rate": mean([1.0 if row.provider_error else 0.0 for row in rows]),
            "unsafe_sql_rate": mean([0.0 if row.safe_sql else 1.0 for row in rows]),
            "contract_error_count": sum(1 for row in rows if row.contract_errors),
            "error_taxonomy": dict(Counter(row.evaluator_error_type for row in rows if not row.evaluator_correct)),
        }
    return {"seed_metrics": seed_metrics, "condition_metrics": condition_metrics}


def ablation_outputs_differ(predictions: list[dict[str, Any]]) -> bool:
    by_question_seed: dict[tuple[str, int], dict[str, str]] = {}
    for prediction in predictions:
        key = (prediction["question_id"], int(prediction["seed"]))
        by_question_seed.setdefault(key, {})[prediction["condition"]] = prediction["predicted_sql"]
    for row in by_question_seed.values():
        outputs = [row.get(condition, "") for condition in CONDITION_ORDER]
        if len(set(outputs)) > 1:
            return True
    return False


def leakage_scan() -> list[str]:
    forbidden_patterns = [
        "gold_sql",
        "gold_result",
        "expected_result_hash",
        "required_value_literals",
        "order_sensitive",
        '"answer_shape"',
    ]
    problems: list[str] = []
    for trace in TRACE_DIR.glob("*.json"):
        text = trace.read_text(encoding="utf-8")
        for pattern in forbidden_patterns:
            if pattern in text:
                problems.append(f"{trace.name}: contains forbidden prompt/trace token {pattern}")
    for prediction_line in PREDICTIONS_PATH.read_text(encoding="utf-8").splitlines() if PREDICTIONS_PATH.exists() else []:
        record = json.loads(prediction_line)
        leaked = sorted(FORBIDDEN_PREDICTION_FIELDS & set(record))
        if leaked:
            problems.append(f"{record.get('question_id')} {record.get('condition')}: leaked {leaked}")
    return problems


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_report(
    *,
    mode: str,
    seeds: list[int],
    records: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    scores: list[ScoreRow],
    aggregates: dict[str, Any],
    leakage_problems: list[str],
) -> None:
    condition_metrics = aggregates["condition_metrics"]
    lines = [
        "# MA-SQLGrid C1-C5 Experiment Report",
        "",
        "## Scope",
        "",
        f"- Run mode: `{mode}`.",
        f"- Records: {len(records)}.",
        f"- Seeds: {seeds}.",
        f"- Formal seed policy: `{FORMAL_SEED_POLICY}`.",
        f"- Dev smoke seed policy: `{SMOKE_SEED_POLICY}`.",
        f"- Model/provider: `{smoke.MODEL_NAME}` via `{smoke.PROVIDER}` `{smoke.BASE_URL}` with `wire_api={smoke.WIRE_API}` and temperature `{HYPERPARAMETERS['temperature']}`.",
        "- Dataset: controlled deterministic GridDB-Maintenance-v2 v0.1.",
        "",
        "## Conditions",
        "",
    ]
    lines.extend(f"- {condition}" for condition in CONDITION_ORDER)
    lines.extend(
        [
            "",
            "## Contract Checks",
            "",
            f"- Prediction records: {len(predictions)}.",
            f"- Contract-error records: {sum(1 for row in scores if row.contract_errors)}.",
            f"- Unsafe-SQL records: {sum(1 for row in scores if not row.safe_sql)}.",
            f"- Provider/model/extraction error records: {sum(1 for item in predictions if item.get('error'))}.",
            f"- Leakage scan problems: {len(leakage_problems)}.",
            "",
            "## Metrics",
            "",
            "| condition | execution accuracy mean | std | valid SQL | shape accuracy | value coverage | prompt tokens | latency ms | errors |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for condition in CONDITION_ORDER:
        metric = condition_metrics[condition]
        lines.append(
            f"| {condition} | {metric['execution_accuracy_mean']:.4f} | {metric['execution_accuracy_std']:.4f} | "
            f"{metric['valid_sql_rate']:.4f} | {metric['answer_shape_accuracy']:.4f} | "
            f"{metric['value_hint_coverage']:.4f} | {metric['prompt_token_estimate']:.1f} | "
            f"{metric['latency_ms']:.1f} | {metric['error_taxonomy'] or 'none'} |"
        )
    lines.extend(["", "## Leakage Scan", ""])
    if leakage_problems:
        lines.extend(f"- {problem}" for problem in leakage_problems)
    else:
        lines.append("- No forbidden prompt/trace or prediction-record tokens found.")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_results_json(
    *,
    mode: str,
    seeds: list[int],
    records: list[dict[str, Any]],
    predictions: list[dict[str, Any]],
    scores: list[ScoreRow],
    aggregates: dict[str, Any],
    leakage_problems: list[str],
    harness: ExperimentHarness,
) -> dict[str, Any]:
    results = {
        "hyperparameters": HYPERPARAMETERS,
        "mode": mode,
        "dataset": str(DATA_DIR.relative_to(WORKSPACE)),
        "question_count": len(records),
        "prediction_count": len(predictions),
        "conditions": CONDITION_ORDER,
        "seeds": seeds,
        "formal_seed_count": len(FORMAL_SEEDS),
        "formal_seed_policy": FORMAL_SEED_POLICY,
        "dev_smoke_seeds": SMOKE_SEEDS,
        "dev_smoke_seed_policy": SMOKE_SEED_POLICY,
        "metrics": aggregates["condition_metrics"],
        "seed_metrics": aggregates["seed_metrics"],
        "contract_error_count": sum(1 for row in scores if row.contract_errors),
        "unsafe_sql_count": sum(1 for row in scores if not row.safe_sql),
        "provider_error_count": sum(1 for prediction in predictions if prediction.get("error")),
        "leakage_scan": {"problem_count": len(leakage_problems), "problems": leakage_problems},
        "artifacts": {
            "predictions": relative_to_workspace(PREDICTIONS_PATH),
            "scores": relative_to_workspace(SCORES_PATH),
            "contexts": relative_to_workspace(CONTEXTS_PATH),
            "report": relative_to_workspace(REPORT_PATH),
        },
        "elapsed_sec": round(harness.elapsed, 2),
    }
    RESULTS_PATH.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path("results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return results


def print_startup(mode: str, records: list[dict[str, Any]], seeds: list[int]) -> None:
    print(f"REGISTERED_CONDITIONS: {', '.join(CONDITION_ORDER)}")
    print("METRIC_DEF: execution_accuracy | direction=higher | desc=validated denotation accuracy")
    print(f"SEED_COUNT: {len(seeds)}")
    if mode == "formal":
        print(f"FORMAL_SEED_POLICY: {FORMAL_SEED_POLICY}")
        print(f"FORMAL_SEED_COUNT: {len(seeds)}")
        print(f"DEV_SMOKE_SEEDS: {SMOKE_SEEDS} contract evidence only")
    else:
        print(f"SMOKE_SEED_POLICY: {SMOKE_SEED_POLICY}")
        print("SEED_WARNING: dev smoke uses 3 seeds for output-contract evidence only")
    estimated_calls = len(records) * len(CONDITION_ORDER) * len(seeds)
    print(f"TIME_ESTIMATE: model_calls~{estimated_calls} time_budget={HYPERPARAMETERS['time_budget_sec']}s")
    print(f"RUN_MODE: {mode} question_count={len(records)}")


def validate_foundation() -> None:
    dataset_result = validate_dataset(DB_PATH, QUESTIONS_PATH)
    if dataset_result["error_count"]:
        sample = dataset_result["errors"][:5]
        raise RuntimeError(f"dataset validation failed: {sample}")
    if not SCHEMA_PATH.exists() or not DB_PATH.exists():
        raise RuntimeError("missing local schema or SQLite database")


def run() -> int:
    mode = os.environ.get("MA_SQLGRID_RUN_MODE", "formal").strip().lower()
    if mode not in {"formal", "smoke"}:
        raise RuntimeError("MA_SQLGRID_RUN_MODE must be either formal or smoke")
    ensure_dirs()
    clean_run_outputs()
    validate_foundation()
    records = load_split_records(mode)
    seeds = seeds_for_mode(mode)
    print_startup(mode, records, seeds)

    harness = ExperimentHarness(time_budget=int(HYPERPARAMETERS["time_budget_sec"]))
    conditions = condition_instances()
    client = llm_client()
    predictions: list[dict[str, Any]] = []
    contexts: list[dict[str, Any]] = []
    bundles: dict[str, dict[str, Any]] = {}

    conn = sqlite3.connect(DB_PATH)
    try:
        for record in records:
            bundle = load_context_bundle(conn, record)
            bundles[record["question_id"]] = bundle
            contexts.append({"question_id": record["question_id"], **bundle["generic"]})
            contexts.append({"question_id": record["question_id"], **bundle["domain"]})

        for seed in seeds:
            set_all_seeds(seed)
            for condition_name in CONDITION_ORDER:
                condition = conditions[condition_name]
                condition_predictions: list[dict[str, Any]] = []
                for record in records:
                    if harness.should_stop():
                        print("TIME_GUARD: stopping before 80% budget is exceeded")
                        break
                    try:
                        prediction = condition.predict(client, conn, record, bundles[record["question_id"]], seed)
                    except Exception as exc:
                        print(f"CONDITION_FAILED: {condition_name} {type(exc).__name__}: {exc}")
                        continue
                    predictions.append(prediction)
                    condition_predictions.append(prediction)
                    harness.step()
                if condition_predictions:
                    write_jsonl(PREDICTIONS_PATH, predictions)
                if harness.should_stop():
                    break
            if harness.should_stop():
                break

        predictions.sort(key=lambda item: (item["question_id"], int(item["seed"]), CONDITION_ORDER.index(item["condition"])))
        write_jsonl(PREDICTIONS_PATH, predictions)
        write_jsonl(CONTEXTS_PATH, contexts)
        scores = score_predictions(conn, records, bundles, predictions)
    finally:
        conn.close()

    score_dicts = [asdict(row) for row in scores]
    write_jsonl(SCORES_PATH, score_dicts)
    aggregates = aggregate_scores(scores)
    leakage_problems = leakage_scan()
    write_report(
        mode=mode,
        seeds=seeds,
        records=records,
        predictions=predictions,
        scores=scores,
        aggregates=aggregates,
        leakage_problems=leakage_problems,
    )
    results = save_results_json(
        mode=mode,
        seeds=seeds,
        records=records,
        predictions=predictions,
        scores=scores,
        aggregates=aggregates,
        leakage_problems=leakage_problems,
        harness=harness,
    )

    for condition in CONDITION_ORDER:
        for seed in seeds:
            key = f"{condition}|{seed}"
            if key in aggregates["seed_metrics"]:
                value = aggregates["seed_metrics"][key]
                print(f"condition={condition} seed={seed} execution_accuracy: {value:.6f}")
        metric = aggregates["condition_metrics"][condition]
        mean_value = metric["execution_accuracy_mean"]
        std_value = metric["execution_accuracy_std"]
        print(f"condition={condition} execution_accuracy_mean: {mean_value:.6f} execution_accuracy_std: {std_value:.6f}")
        print(f"condition={condition} success_rate: {sum(1 for row in scores if row.condition == condition and row.evaluator_correct)}/{sum(1 for row in scores if row.condition == condition)}")
        print(f"SUMMARY condition={condition} metric=execution_accuracy mean={mean_value:.6f} std={std_value:.6f}")
        harness.report_metric(f"{condition}_execution_accuracy_mean", mean_value)

    summary_line = ", ".join(
        f"{condition}={results['metrics'][condition]['execution_accuracy_mean']:.6f}" for condition in CONDITION_ORDER
    )
    outputs_differ = ablation_outputs_differ(predictions)
    print(f"SUMMARY: {summary_line}")
    print(f"ABLATION_CHECK: C1-C5 outputs_differ={outputs_differ}")
    if not outputs_differ:
        print("WARNING: DEGENERATE_METRICS all condition outputs are identical")

    blocking = []
    if len(predictions) != len(records) * len(CONDITION_ORDER) * len(seeds):
        blocking.append(f"expected {len(records) * len(CONDITION_ORDER) * len(seeds)} predictions, got {len(predictions)}")
    if any(row.contract_errors for row in scores):
        blocking.append("prediction contract errors found")
    if any(not row.safe_sql for row in scores):
        blocking.append("unsafe SQL found")
    if leakage_problems:
        blocking.append("forbidden leakage scan tokens found")
    if any(prediction.get("error") for prediction in predictions):
        blocking.append("provider/model/extraction errors found")

    if blocking:
        for problem in blocking:
            print(f"FAIL: {problem}")
        harness.finalize()
        return 1

    harness.finalize()
    print(f"PASS: wrote {relative_to_workspace(RESULTS_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
