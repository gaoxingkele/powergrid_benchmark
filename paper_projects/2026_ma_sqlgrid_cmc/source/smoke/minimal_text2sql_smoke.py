#!/usr/bin/env python3
"""Pre-three-pack minimal Text-to-SQL smoke for MA-SQLGrid restart.

This is not a formal experiment. It only verifies that the provider, prompt
contracts, prediction JSONL shape, and semantic evaluator can form a local
closed loop on five dev questions.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
REPO_ROOT = WORKSPACE.parents[2]
DATA_DIR = WORKSPACE / "data" / "griddb_maintenance_v2_v0_1"
DB_PATH = DATA_DIR / "database.sqlite"
QUESTIONS_PATH = DATA_DIR / "questions.jsonl"
SCHEMA_PATH = DATA_DIR / "schema.sql"
OUT_DIR = WORKSPACE / "smoke" / "run"
PREDICTIONS_PATH = OUT_DIR / "predictions.jsonl"
SCORES_PATH = OUT_DIR / "scores.jsonl"
REPORT_PATH = OUT_DIR / "smoke_report.md"
TRACE_DIR = OUT_DIR / "traces"

MODEL_NAME = "gpt-5.4-mini"
PROVIDER = "krill"
BASE_URL = "https://api.krill-ai.com/codex/v1"
WIRE_API = "responses"
TEMPERATURE = 0
MAX_TOKENS = 700
QUESTION_IDS = ["Q001", "Q002", "Q003", "Q004", "Q005"]


sys.path.insert(0, str(WORKSPACE / "evaluator"))
sys.path.insert(0, str(REPO_ROOT))

from evaluator import execute_sql, load_questions, score_prediction, validate_read_only_select  # noqa: E402
from researchclaw.llm.client import LLMClient, LLMConfig  # noqa: E402


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


@dataclass
class SmokeScore:
    question_id: str
    condition: str
    predicted_sql: str
    safe_sql: bool
    evaluator_correct: bool
    evaluator_error_type: str
    evaluator_details: str
    contract_errors: list[str]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_smoke_questions() -> list[dict[str, Any]]:
    by_id = {record["question_id"]: record for record in load_questions(QUESTIONS_PATH)}
    missing = [qid for qid in QUESTION_IDS if qid not in by_id]
    if missing:
        raise RuntimeError(f"Missing smoke question IDs: {missing}")
    records = [by_id[qid] for qid in QUESTION_IDS]
    non_dev = [record["question_id"] for record in records if record["split"] != "dev"]
    if non_dev:
        raise RuntimeError(f"Smoke must use dev questions only, got non-dev IDs: {non_dev}")
    return records


def schema_context(conn: sqlite3.Connection) -> str:
    schema = SCHEMA_PATH.read_text(encoding="utf-8").strip()
    table_names = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]
    value_lines: list[str] = []
    value_columns = {
        "asset_types": ["type_name", "voltage_class", "manufacturer"],
        "locations": ["location_name", "region", "criticality"],
        "assets": ["asset_name", "status"],
        "technicians": ["technician_name", "specialty", "home_region"],
        "work_orders": ["priority", "status", "fault_code"],
        "maintenance_logs": ["action_type", "notes"],
        "sensor_readings": ["sensor_type", "unit", "alarm_flag"],
        "grid_topology": ["connection_type", "switch_status"],
    }
    for table in table_names:
        if table not in value_columns:
            continue
        for column in value_columns[table]:
            rows = conn.execute(f"SELECT DISTINCT {column} FROM {table} ORDER BY {column} LIMIT 20").fetchall()
            values = [str(row[0]) for row in rows]
            value_lines.append(f"- {table}.{column}: {', '.join(values)}")
    return "\n".join(
        [
            "SQLite schema:",
            schema,
            "",
            "Compact domain value dictionary:",
            *value_lines,
        ]
    )


def extract_sql(text: str) -> str:
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        text = fenced.group(1)
    text = text.strip()
    select_match = re.search(r"\b(with|select)\b", text, flags=re.IGNORECASE)
    if select_match:
        text = text[select_match.start() :]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return text
    sql = " ".join(lines)
    sql = re.sub(r"\s+", " ", sql).strip()
    if ";" in sql:
        sql = sql[: sql.find(";") + 1]
    elif sql:
        sql += ";"
    return sql


def extract_candidate_sql(text: str) -> list[str]:
    candidates: list[str] = []
    for fenced in re.findall(r"```(?:sql)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL):
        sql = extract_sql(fenced)
        if sql and sql not in candidates:
            candidates.append(sql)
    numbered_blocks = re.split(r"(?m)^\s*\d+[.)]\s*", text)
    for block in numbered_blocks:
        block = block.strip().strip("`").strip()
        if not block:
            continue
        if re.search(r"\b(select|with)\b", block, flags=re.IGNORECASE):
            sql = extract_sql(block)
            if sql and sql not in candidates:
                candidates.append(sql)
    for line in text.splitlines():
        line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
        if re.match(r"^(select|with)\b", line, flags=re.IGNORECASE):
            sql = extract_sql(line)
            if sql and sql not in candidates:
                candidates.append(sql)
    if not candidates:
        sql = extract_sql(text)
        if sql:
            candidates.append(sql)
    return candidates[:5]


def llm_client() -> LLMClient:
    if not os.environ.get("KRILL_API_KEY"):
        raise RuntimeError("KRILL_API_KEY is required for smoke runner")
    return LLMClient(
        LLMConfig(
            base_url=BASE_URL,
            api_key=os.environ["KRILL_API_KEY"],
            primary_model=MODEL_NAME,
            fallback_models=[],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            timeout_sec=90,
            wire_api=WIRE_API,
        )
    )


def call_model(client: LLMClient, prompt: str) -> tuple[str, str, int, int, int]:
    last_exc: Exception | None = None
    start = time.monotonic()
    for _ in range(2):
        try:
            response = client.chat(
                [{"role": "user", "content": prompt}],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            latency_ms = int((time.monotonic() - start) * 1000)
            input_tokens = int(response.prompt_tokens or 0)
            output_tokens = int(response.completion_tokens or 0)
            return response.content, response.model or MODEL_NAME, latency_ms, input_tokens, output_tokens
        except Exception as exc:
            last_exc = exc
            time.sleep(2)
    assert last_exc is not None
    raise last_exc


def strong_direct_prompt(record: dict[str, Any], schema_text: str) -> str:
    return f"""You are a Text-to-SQL system for a synthetic SQLite power-grid maintenance database.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Use only the schema and domain values below. Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.

{schema_text}

Question ID: {record['question_id']}
Question: {record['question']}
Expected answer shape: {json.dumps(record['answer_shape'], sort_keys=True)}
Order-sensitive answer: {record['order_sensitive']}
Required domain literals mentioned by metadata: {json.dumps(record['required_value_literals'])}
"""


def vg_candidate_prompt(record: dict[str, Any], schema_text: str) -> str:
    return f"""You are generating candidate SQL for a value-grounded Text-to-SQL smoke test.

Return 3 distinct read-only SQLite SELECT queries as a numbered list. Do not include explanation.
Each candidate must use only the schema and domain values below.
Prefer exact domain literals from the question/metadata and preserve expected answer shape.

{schema_text}

Question ID: {record['question_id']}
Question: {record['question']}
Expected answer shape: {json.dumps(record['answer_shape'], sort_keys=True)}
Order-sensitive answer: {record['order_sensitive']}
Required domain literals mentioned by metadata: {json.dumps(record['required_value_literals'])}
"""


def rank_candidates(
    conn: sqlite3.Connection,
    record: dict[str, Any],
    candidates: list[str],
) -> tuple[int, list[dict[str, Any]]]:
    expected_cols = int(record["answer_shape"]["column_count"])
    required_values = [str(value) for value in record.get("required_value_literals", [])]
    trace: list[dict[str, Any]] = []
    best_idx = 0
    best_score = -10_000
    for idx, sql in enumerate(candidates):
        result = execute_sql(conn, sql)
        safe, _, safety_error = validate_read_only_select(sql)
        shape_ok = result.ok and len(result.columns) == expected_cols
        values_present = sum(1 for value in required_values if value == "" or value in sql)
        order_bonus = 1 if (not record["order_sensitive"] or "order by" in sql.lower() or "limit" in sql.lower()) else 0
        score = 0
        score += 5 if safe else -5
        score += 5 if result.ok else -5
        score += 4 if shape_ok else -3
        score += values_present
        score += order_bonus
        score -= idx
        entry = {
            "candidate_index": idx,
            "sql": sql,
            "safe": safe,
            "safety_error": safety_error,
            "exec_ok": result.ok,
            "exec_error": result.error,
            "column_count": len(result.columns),
            "expected_column_count": expected_cols,
            "shape_ok": bool(shape_ok),
            "required_value_hits": values_present,
            "ranker_score": score,
        }
        trace.append(entry)
        if score > best_score:
            best_idx = idx
            best_score = score
    return best_idx, trace


def prediction_record(
    *,
    question_id: str,
    condition: str,
    model: str,
    prompt: str,
    schema_text: str,
    predicted_sql: str,
    candidate_sql: list[str],
    selected_candidate_index: int,
    trace_path: str | None,
    latency_ms: int,
    token_input: int,
    token_output: int,
    error: str | None,
) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "condition": condition,
        "model": model,
        "provider": PROVIDER,
        "prompt_hash": sha256_text(prompt),
        "schema_context_hash": sha256_text(schema_text),
        "input_contract_version": "griddb-maintenance-v2-v0.1",
        "predicted_sql": predicted_sql,
        "candidate_sql": candidate_sql,
        "selected_candidate_index": selected_candidate_index,
        "intermediate_trace_path": trace_path,
        "latency_ms": latency_ms,
        "token_input": token_input,
        "token_output": token_output,
        "retry_count": 0,
        "error": error,
    }


def validate_prediction_contract(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_PREDICTION_FIELDS - set(record)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    if not isinstance(record.get("candidate_sql"), list) or not record.get("candidate_sql"):
        errors.append("candidate_sql must be a non-empty list")
    if not isinstance(record.get("selected_candidate_index"), int):
        errors.append("selected_candidate_index must be an integer")
    elif isinstance(record.get("candidate_sql"), list) and not (0 <= record["selected_candidate_index"] < len(record["candidate_sql"])):
        errors.append("selected_candidate_index out of range")
    if not isinstance(record.get("predicted_sql"), str) or not record["predicted_sql"].strip():
        errors.append("predicted_sql must be a non-empty string")
    forbidden_score_fields = {"correct", "execution_accuracy", "gold_sql", "gold_result", "expected_result_hash"}
    leaked = sorted(forbidden_score_fields & set(record))
    if leaked:
        errors.append(f"prediction record contains forbidden gold/score fields: {leaked}")
    return errors


def run() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    records = load_smoke_questions()
    client = llm_client()
    conn = sqlite3.connect(DB_PATH)
    predictions: list[dict[str, Any]] = []
    scores: list[SmokeScore] = []
    try:
        schema_text = schema_context(conn)
        for record in records:
            prompt = strong_direct_prompt(record, schema_text)
            error = None
            try:
                raw, model, latency_ms, input_tokens, output_tokens = call_model(client, prompt)
                sql = extract_sql(raw)
            except Exception as exc:  # pragma: no cover - smoke should preserve failure records.
                raw = ""
                model = MODEL_NAME
                latency_ms = 0
                input_tokens = 0
                output_tokens = 0
                sql = "SELECT 1;"
                error = f"{type(exc).__name__}: {exc}"
            trace_path = TRACE_DIR / f"{record['question_id']}_C1_StrongDirect.json"
            trace_path.write_text(json.dumps({"prompt": prompt, "raw_response": raw}, indent=2) + "\n", encoding="utf-8")
            predictions.append(
                prediction_record(
                    question_id=record["question_id"],
                    condition="C1_StrongDirect",
                    model=model,
                    prompt=prompt,
                    schema_text=schema_text,
                    predicted_sql=sql,
                    candidate_sql=[sql],
                    selected_candidate_index=0,
                    trace_path=str(trace_path.relative_to(WORKSPACE)),
                    latency_ms=latency_ms,
                    token_input=input_tokens,
                    token_output=output_tokens,
                    error=error,
                )
            )

            prompt = vg_candidate_prompt(record, schema_text)
            error = None
            try:
                raw, model, latency_ms, input_tokens, output_tokens = call_model(client, prompt)
                candidates = extract_candidate_sql(raw)
                if not candidates:
                    candidates = ["SELECT 1;"]
                    error = "no SQL candidate extracted"
            except Exception as exc:  # pragma: no cover - smoke should preserve failure records.
                raw = ""
                model = MODEL_NAME
                latency_ms = 0
                input_tokens = 0
                output_tokens = 0
                candidates = ["SELECT 1;"]
                error = f"{type(exc).__name__}: {exc}"
            selected_idx, rank_trace = rank_candidates(conn, record, candidates)
            predicted = candidates[selected_idx]
            trace_path = TRACE_DIR / f"{record['question_id']}_C5_VG_Rerank_Minimal.json"
            trace_path.write_text(
                json.dumps({"prompt": prompt, "raw_response": raw, "rank_trace": rank_trace}, indent=2) + "\n",
                encoding="utf-8",
            )
            predictions.append(
                prediction_record(
                    question_id=record["question_id"],
                    condition="C5_VG_Rerank_Minimal",
                    model=model,
                    prompt=prompt,
                    schema_text=schema_text,
                    predicted_sql=predicted,
                    candidate_sql=candidates,
                    selected_candidate_index=selected_idx,
                    trace_path=str(trace_path.relative_to(WORKSPACE)),
                    latency_ms=latency_ms,
                    token_input=input_tokens,
                    token_output=output_tokens,
                    error=error,
                )
            )

        with PREDICTIONS_PATH.open("w", encoding="utf-8") as f:
            for prediction in predictions:
                f.write(json.dumps(prediction, sort_keys=True) + "\n")

        by_id = {record["question_id"]: record for record in records}
        for prediction in predictions:
            question = by_id[prediction["question_id"]]
            contract_errors = validate_prediction_contract(prediction)
            score = score_prediction(conn, question, prediction["predicted_sql"])
            safe, _, _ = validate_read_only_select(prediction["predicted_sql"])
            scores.append(
                SmokeScore(
                    question_id=prediction["question_id"],
                    condition=prediction["condition"],
                    predicted_sql=prediction["predicted_sql"],
                    safe_sql=safe,
                    evaluator_correct=score.correct,
                    evaluator_error_type=score.error_type,
                    evaluator_details=score.details,
                    contract_errors=contract_errors,
                )
            )
    finally:
        conn.close()

    with SCORES_PATH.open("w", encoding="utf-8") as f:
        for score in scores:
            f.write(json.dumps(asdict(score), sort_keys=True) + "\n")

    write_report(predictions, scores)
    blocking = [
        score
        for score in scores
        if score.contract_errors or not score.predicted_sql.strip() or not score.safe_sql
    ]
    model_errors = [prediction for prediction in predictions if prediction.get("error")]
    if len(predictions) != len(QUESTION_IDS) * 2:
        print(f"FAIL: expected {len(QUESTION_IDS) * 2} predictions, got {len(predictions)}")
        return 1
    if model_errors:
        print(f"FAIL: {len(model_errors)} prediction records have model/extraction errors")
        return 1
    if blocking:
        print(f"FAIL: {len(blocking)} prediction records failed contract/safety smoke checks")
        return 1
    print(f"PASS: wrote {PREDICTIONS_PATH.relative_to(WORKSPACE)} and {REPORT_PATH.relative_to(WORKSPACE)}")
    return 0


def write_report(predictions: list[dict[str, Any]], scores: list[SmokeScore]) -> None:
    by_condition: dict[str, list[SmokeScore]] = {}
    for score in scores:
        by_condition.setdefault(score.condition, []).append(score)
    lines = [
        "# Pre-Three-Pack Minimal Text-to-SQL Smoke Report",
        "",
        "## Scope",
        "",
        "- Purpose: verify provider, baseline/method prediction contracts, and evaluator scoring before three-pack generation.",
        "- This is not a formal experiment and must not be used for paper claims.",
        f"- Questions: {', '.join(QUESTION_IDS)} from the dev split only.",
        f"- Model/provider: `{MODEL_NAME}` via `{PROVIDER}` `{BASE_URL}` with `wire_api={WIRE_API}` and temperature `{TEMPERATURE}`.",
        "",
        "## Artifacts",
        "",
        f"- predictions: `{PREDICTIONS_PATH.relative_to(WORKSPACE)}`",
        f"- scores: `{SCORES_PATH.relative_to(WORKSPACE)}`",
        f"- traces: `{TRACE_DIR.relative_to(WORKSPACE)}/`",
        "",
        "## Contract Summary",
        "",
        f"- prediction records written: {len(predictions)}",
        f"- expected records: {len(QUESTION_IDS) * 2}",
        f"- records with contract errors: {sum(1 for score in scores if score.contract_errors)}",
        f"- records with unsafe SQL: {sum(1 for score in scores if not score.safe_sql)}",
        f"- records with model/extraction errors: {sum(1 for prediction in predictions if prediction.get('error'))}",
        "",
        "## Condition Diagnostic Scores",
        "",
        "| condition | records | evaluator_correct | evaluator_errors |",
        "|---|---:|---:|---|",
    ]
    for condition, condition_scores in sorted(by_condition.items()):
        errors = sorted({score.evaluator_error_type for score in condition_scores if not score.evaluator_correct})
        lines.append(
            f"| {condition} | {len(condition_scores)} | "
            f"{sum(1 for score in condition_scores if score.evaluator_correct)} | "
            f"{', '.join(errors) if errors else 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Per-Question Results",
            "",
            "| question_id | condition | safe_sql | evaluator_correct | error_type | contract_errors |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    for score in scores:
        lines.append(
            f"| {score.question_id} | {score.condition} | {score.safe_sql} | {score.evaluator_correct} | "
            f"{score.evaluator_error_type} | {'; '.join(score.contract_errors) if score.contract_errors else 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Gold-Leakage Check",
            "",
            "- Prompts include question text, schema, compact domain values, answer-shape metadata, order sensitivity, and required literal metadata.",
            "- Prompts do not include gold SQL, gold result rows, expected hashes, or test examples.",
            "- The C5 ranker uses only read-only execution status, answer-shape column count, required-literal presence, order cues, and candidate index.",
            "- Gold SQL is used only after prediction generation by `evaluator.score_prediction` to score this smoke.",
            "",
            "## Decision Rule",
            "",
            "This smoke passes only if all 10 prediction records exist, satisfy the JSONL contract, contain read-only SQL, and can be scored by the evaluator without crashing. Accuracy is diagnostic only.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(run())
