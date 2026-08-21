#!/usr/bin/env python3
"""Freeze MA-SQLGrid prospective E1/E2/E4 prompts without model execution."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import random
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = next(parent for parent in HERE.parents if (parent / "paper_projects").is_dir())
SOURCE = REPO / "paper_projects" / "2026_ma_sqlgrid_cmc" / "source"
EXPERIMENT = SOURCE / "code" / "experiment_final"
DATA = SOURCE / "data" / "griddb_maintenance_v2_v0_1"
MA = HERE.parent
CLUSTER_LEDGER = MA / "canonical_v2_reanalysis" / "canonical_rows_v2.jsonl"
os.environ["MA_SQLGRID_WORKSPACE"] = str(SOURCE)
sys.path.insert(0, str(EXPERIMENT))

import main as formal  # noqa: E402


SEED = 20260805
CONDITIONS = ("V0_NoValueEvidence", "V1_WithValueEvidence")
MODEL_MANIFESTS = {
    "qwen": MA / "local_model_artifact_manifest.json",
    "granite": MA / "granite33_local_model_artifact_manifest.json",
}
INPUTS = [
    DATA / "database.sqlite",
    DATA / "questions.jsonl",
    DATA / "splits.json",
    DATA / "schema.sql",
    EXPERIMENT / "main.py",
    EXPERIMENT / "applsci_factorial.py",
    SOURCE / "smoke" / "dev_chess_style_pilot.py",
    SOURCE / "smoke" / "minimal_text2sql_smoke.py",
    HERE / "build_freeze.py",
    HERE / "verify_freeze.py",
    HERE / "run_frozen.py",
    HERE / "offline_replay.py",
    HERE / "aggregate_results.py",
    HERE / "tests" / "test_aggregate_results.py",
    HERE / "tests" / "fixtures" / "synthetic_pairs.json",
    HERE / "EFFICIENCY_ATTESTATION.template.json",
    HERE / "STATISTICAL_ANALYSIS_PLAN.md",
    HERE / "STATISTICAL_IMPLEMENTATION_AUDIT.json",
    HERE / "current_status.py",
    CLUSTER_LEDGER,
    *MODEL_MANIFESTS.values(),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256_text(encoded)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def candidate_prompt(question_id: str, question: str, context: str, condition: str) -> str:
    return f"""You are a Text-to-SQL system for a synthetic SQLite power-grid maintenance database.

Return exactly three distinct read-only SQLite SELECT candidates as a numbered list (1., 2., 3.).
Do not include markdown fences or explanation. Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA,
ATTACH, or multiple statements in one candidate. Preserve the requested output columns, ordering,
aggregation, grouping, and literal predicates. Use only the provided database context.

Prospective condition: {condition}

{context}

Question ID: {question_id}
Question: {question}
"""


def prompt_record(conn: Any, original: dict[str, Any], condition: str) -> dict[str, Any]:
    # A whitelist is stricter than subtracting known gold keys: evaluator-only
    # fields such as required literals, tables, columns, and answer shape can
    # never enter the context builder.
    clean = {"question_id": original["question_id"], "question": original["question"]}
    domain = formal.load_context_bundle(conn, clean)["domain"]
    intervention = copy.deepcopy(domain)
    if condition == CONDITIONS[0]:
        intervention["matched_values"] = {}
        intervention["normalized_value_hints"] = []
    elif condition != CONDITIONS[1]:
        raise ValueError(condition)
    context = formal.chess.render_selected_context(intervention, domain=True)
    prompt = candidate_prompt(original["question_id"], original["question"], context, condition)
    gold_sql = str(original.get("gold_sql") or "").strip()
    if gold_sql and gold_sql in prompt:
        raise RuntimeError(f"gold SQL leaked for {original['question_id']} {condition}")
    return {
        "question_id": original["question_id"],
        "question": original["question"],
        "condition": condition,
        "prompt": prompt,
        "context": context,
        "prompt_sha256": sha256_text(prompt),
        "context_sha256": sha256_text(context),
        "selected_tables_sha256": canonical_hash(domain["selected_tables"]),
        "selected_columns_sha256": canonical_hash(domain["selected_columns"]),
        "inferred_shape_sha256": canonical_hash(domain["inferred_shape"]),
        "matched_value_field_count": len(domain["matched_values"]),
        "normalization_hint_count": len(domain["normalized_value_hints"]),
    }


def make_order(question_ids: list[str], eligible: set[str], model: str) -> list[dict[str, Any]]:
    rng = random.Random(SEED + (101 if model == "qwen" else 202))
    qids = question_ids[:]
    rng.shuffle(qids)
    rows: list[dict[str, Any]] = []
    call_index = 0
    for qid in qids:
        pair = list(CONDITIONS)
        if int(sha256_text(f"{model}|{qid}|{SEED}")[-1], 16) % 2:
            pair.reverse()
        if qid not in eligible:
            pair = [CONDITIONS[1]]
        for condition in pair:
            rows.append({"call_index": call_index, "question_id": qid, "condition": condition, "scored": True})
            call_index += 1
    return rows


def main() -> int:
    run_artifacts = [path for path in (HERE / "runs").glob("**/*") if path.is_file()] if (HERE / "runs").exists() else []
    if run_artifacts:
        raise RuntimeError("refusing to rebuild the freeze after any formal run artifact exists")
    analysis_artifacts = [path for path in (HERE / "analysis").glob("**/*") if path.is_file()] if (HERE / "analysis").exists() else []
    if analysis_artifacts:
        raise RuntimeError("refusing to rebuild the freeze after formal analysis artifacts exist")
    formal.validate_foundation()
    formal_records = formal.load_split_records("formal")
    dev_records = formal.load_split_records("smoke")
    if len(formal_records) != 180:
        raise RuntimeError(f"expected 180 frozen test records, found {len(formal_records)}")

    import sqlite3

    prompt_rows: list[dict[str, Any]] = []
    warmup_rows: list[dict[str, Any]] = []
    conn = sqlite3.connect(formal.DB_PATH)
    try:
        for record in formal_records:
            prompt_rows.extend(prompt_record(conn, record, condition) for condition in CONDITIONS)
        for record in dev_records[:2]:
            warmup_rows.extend(prompt_record(conn, record, condition) for condition in CONDITIONS)
    finally:
        conn.close()

    by_key = {(row["question_id"], row["condition"]): row for row in prompt_rows}
    eligible = {
        record["question_id"]
        for record in formal_records
        if by_key[(record["question_id"], CONDITIONS[0])]["context_sha256"]
        != by_key[(record["question_id"], CONDITIONS[1])]["context_sha256"]
    }
    for record in formal_records:
        qid = record["question_id"]
        v0 = by_key[(qid, CONDITIONS[0])]
        v1 = by_key[(qid, CONDITIONS[1])]
        for field in ("selected_tables_sha256", "selected_columns_sha256", "inferred_shape_sha256"):
            if v0[field] != v1[field]:
                raise RuntimeError(f"non-value field differs for {qid}: {field}")
        if "Exact database values matched from the question:" in v0["context"]:
            raise RuntimeError(f"V0 retained matched-value block for {qid}")
        if "Power-grid domain normalization hints" in v0["context"]:
            raise RuntimeError(f"V0 retained normalization block for {qid}")

    orders = {model: make_order([r["question_id"] for r in formal_records], eligible, model) for model in MODEL_MANIFESTS}
    cluster_rows = [json.loads(line) for line in CLUSTER_LEDGER.read_text(encoding="utf-8").splitlines() if line.strip()]
    cluster_by_question = {row["question_id"]: row["template_cluster"] for row in cluster_rows}
    if set(cluster_by_question) != {record["question_id"] for record in formal_records}:
        raise RuntimeError("frozen cluster ledger does not map exactly the 180 test questions")
    input_hashes = {
        str(path.relative_to(REPO)).replace("\\", "/"): {"sha256": sha256_file(path), "bytes": path.stat().st_size}
        for path in INPUTS
    }
    model_specs = {}
    for model, path in MODEL_MANIFESTS.items():
        item = json.loads(path.read_text(encoding="utf-8"))
        model_specs[model] = {
            "served_model_id": item["served_model_id"],
            "model_sha256": item["model_sha256"],
            "model_bytes": item["model_bytes"],
            "model_revision": item["model_revision"],
            "backend": item["backend"],
            "backend_revision": item["backend_revision"],
            "license": item["license"],
        }

    write_jsonl(HERE / "frozen_prompts.jsonl", sorted(prompt_rows, key=lambda x: (x["question_id"], x["condition"])))
    write_jsonl(HERE / "warmup_prompts.jsonl", sorted(warmup_rows, key=lambda x: (x["question_id"], x["condition"])))
    for model, rows in orders.items():
        write_jsonl(HERE / f"call_order_{model}.jsonl", rows)
    freeze = {
        "schema_version": "ma-sqlgrid-prospective-components-freeze-v1.1",
        "freeze_revision": "v1.1-statistical-aggregator-and-synthetic-tests-added-before-run",
        "freeze_date": "2026-08-05",
        "status": "protocol_and_prompts_frozen_not_executed",
        "formal_model_execution_started": False,
        "seed": SEED,
        "dataset": "GridDB-Maintenance-v2 v0.1 frozen test split",
        "question_count": 180,
        "conditions": list(CONDITIONS),
        "eligible_value_intervention_questions": len(eligible),
        "ineligible_identical_context_questions": 180 - len(eligible),
        "template_cluster_count": len(set(cluster_by_question.values())),
        "eligible_template_cluster_count": len({cluster_by_question[qid] for qid in eligible}),
        "e1_primary_population": "questions whose frozen V0 and V1 contexts differ before execution",
        "e2_primary_population": "all 180 V1 candidate sets with at least two safely parsed candidates; failures remain denominator failures",
        "e4_primary_population": "same E1 eligible paired calls, within backbone",
        "candidate_count_requested": 3,
        "generation": {"temperature": 0.0, "seed": SEED, "max_tokens": 600, "retries": 2, "timeout_sec": 90},
        "models": model_specs,
        "formal_calls_per_model": {model: len(rows) for model, rows in orders.items()},
        "warmup_calls_per_model": len(warmup_rows),
        "total_formal_calls": sum(len(rows) for rows in orders.values()),
        "total_warmup_calls": len(warmup_rows) * len(MODEL_MANIFESTS),
        "prompt_ledger_sha256": sha256_file(HERE / "frozen_prompts.jsonl"),
        "warmup_ledger_sha256": sha256_file(HERE / "warmup_prompts.jsonl"),
        "call_order_sha256": {model: sha256_file(HERE / f"call_order_{model}.jsonl") for model in MODEL_MANIFESTS},
        "eligible_question_ids_sha256": canonical_hash(sorted(eligible)),
        "input_hashes": input_hashes,
        "intervention_invariance": ["selected_tables", "selected_columns", "join_paths", "inferred_shape", "question", "candidate_prompt"],
        "intervention_removed_in_v0": ["matched_values presentation", "normalized_value_hints presentation"],
        "gold_policy": "gold fields are absent from prompt ledgers; gold SQL/results are loaded only after immutable predictions are persisted",
    }
    write_json(HERE / "PROTOCOL_FREEZE.json", freeze)
    print(json.dumps({key: freeze[key] for key in ("status", "eligible_value_intervention_questions", "total_formal_calls", "total_warmup_calls")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
