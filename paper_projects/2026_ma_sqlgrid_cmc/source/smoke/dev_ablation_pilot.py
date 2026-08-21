#!/usr/bin/env python3
"""Dev-only prompt/context ablation pilot.

Compares:
- C1_LiteSchemaOnly: question + schema only.
- C1_StrongDirect: schema + value dictionary + answer-shape metadata.
- C5_VG_Rerank_Minimal: multi-candidate value-grounded rerank path.

The pilot uses only the dev split and is not formal experiment evidence.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
OUT_DIR = WORKSPACE / "smoke" / "dev_ablation"
PREDICTIONS_PATH = OUT_DIR / "predictions.jsonl"
SCORES_PATH = OUT_DIR / "scores.jsonl"
REPORT_PATH = OUT_DIR / "dev_ablation_report.md"
TRACE_DIR = OUT_DIR / "traces"

sys.path.insert(0, str(WORKSPACE / "smoke"))

import minimal_text2sql_smoke as smoke  # noqa: E402
import dev_superiority_pilot as dev_pilot  # noqa: E402


def lite_schema_context() -> str:
    return "\n".join(["SQLite schema:", smoke.SCHEMA_PATH.read_text(encoding="utf-8").strip()])


def lite_prompt(record: dict[str, Any], schema_text: str) -> str:
    return f"""You are a Text-to-SQL system for a synthetic SQLite power-grid maintenance database.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Use only the schema below. Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.

{schema_text}

Question ID: {record['question_id']}
Question: {record['question']}
"""


def run_lite_condition(client: Any, schema_text: str, record: dict[str, Any]) -> dict[str, Any]:
    prompt = lite_prompt(record, schema_text)
    error = None
    raw = ""
    model = smoke.MODEL_NAME
    latency_ms = 0
    input_tokens = 0
    output_tokens = 0
    sql = "SELECT 1;"
    try:
        raw, model, latency_ms, input_tokens, output_tokens = smoke.call_model(client, prompt)
        sql = smoke.extract_sql(raw)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    trace_path = TRACE_DIR / f"{record['question_id']}_C1_LiteSchemaOnly.json"
    trace_path.write_text(json.dumps({"prompt": prompt, "raw_response": raw}, indent=2) + "\n", encoding="utf-8")
    return smoke.prediction_record(
        question_id=record["question_id"],
        condition="C1_LiteSchemaOnly",
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


def score_predictions(conn: sqlite3.Connection, questions: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> list[smoke.SmokeScore]:
    by_id = {record["question_id"]: record for record in questions}
    scores: list[smoke.SmokeScore] = []
    for prediction in predictions:
        question = by_id[prediction["question_id"]]
        contract_errors = smoke.validate_prediction_contract(prediction)
        score = smoke.score_prediction(conn, question, prediction["predicted_sql"])
        safe, _, _ = smoke.validate_read_only_select(prediction["predicted_sql"])
        scores.append(
            smoke.SmokeScore(
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
    return scores


def paired_rows(scores: list[smoke.SmokeScore]) -> list[dict[str, Any]]:
    by_question: dict[str, dict[str, smoke.SmokeScore]] = {}
    for score in scores:
        by_question.setdefault(score.question_id, {})[score.condition] = score
    rows = []
    for qid in sorted(by_question):
        item = by_question[qid]
        rows.append(
            {
                "question_id": qid,
                "lite": item["C1_LiteSchemaOnly"].evaluator_correct,
                "strong": item["C1_StrongDirect"].evaluator_correct,
                "c5": item["C5_VG_Rerank_Minimal"].evaluator_correct,
                "lite_error": item["C1_LiteSchemaOnly"].evaluator_error_type,
                "strong_error": item["C1_StrongDirect"].evaluator_error_type,
                "c5_error": item["C5_VG_Rerank_Minimal"].evaluator_error_type,
            }
        )
    return rows


def write_report(predictions: list[dict[str, Any]], scores: list[smoke.SmokeScore]) -> None:
    condition_counts = Counter(prediction["condition"] for prediction in predictions)
    correct_by_condition = {
        condition: sum(score.evaluator_correct for score in scores if score.condition == condition)
        for condition in sorted(condition_counts)
    }
    error_by_condition = {
        condition: Counter(score.evaluator_error_type for score in scores if score.condition == condition and not score.evaluator_correct)
        for condition in sorted(condition_counts)
    }
    rows = paired_rows(scores)
    c5_over_lite = sum(row["c5"] and not row["lite"] for row in rows)
    strong_over_lite = sum(row["strong"] and not row["lite"] for row in rows)
    c5_over_strong = sum(row["c5"] and not row["strong"] for row in rows)
    strong_over_c5 = sum(row["strong"] and not row["c5"] for row in rows)
    candidate_counts = Counter((prediction["condition"], len(prediction["candidate_sql"])) for prediction in predictions)

    lines = [
        "# Dev-Only Prompt/Context Ablation Pilot",
        "",
        "## Scope",
        "",
        "- Purpose: identify whether C5's apparent value comes from value/shape context, reranking, or neither.",
        "- This is not a formal experiment and must not be used for paper claims.",
        "- Split: dev only, Q001-Q020. The test split Q021-Q200 is untouched.",
        f"- Model/provider: `{smoke.MODEL_NAME}` via `{smoke.PROVIDER}` `{smoke.BASE_URL}` with `wire_api={smoke.WIRE_API}` and temperature `{smoke.TEMPERATURE}`.",
        "",
        "## Conditions",
        "",
        "- C1_LiteSchemaOnly: question plus schema only.",
        "- C1_StrongDirect: question plus schema, compact values, answer shape, order sensitivity, and required literals.",
        "- C5_VG_Rerank_Minimal: value-grounded candidate generation plus reference-free execution-aware reranking.",
        "",
        "## Artifacts",
        "",
        f"- predictions: `{PREDICTIONS_PATH.relative_to(WORKSPACE)}`",
        f"- scores: `{SCORES_PATH.relative_to(WORKSPACE)}`",
        f"- traces: `{TRACE_DIR.relative_to(WORKSPACE)}/`",
        "",
        "## Contract And Runtime Checks",
        "",
        f"- prediction records written: {len(predictions)}",
        "- expected records: 60",
        f"- records with contract errors: {sum(1 for score in scores if score.contract_errors)}",
        f"- records with unsafe SQL: {sum(1 for score in scores if not score.safe_sql)}",
        f"- records with model/extraction errors: {sum(1 for prediction in predictions if prediction.get('error'))}",
        f"- candidate count distribution: {dict(candidate_counts)}",
        "",
        "## Accuracy Diagnostics",
        "",
        "| condition | records | evaluator_correct | accuracy | evaluator_errors |",
        "|---|---:|---:|---:|---|",
    ]
    for condition in sorted(condition_counts):
        records = condition_counts[condition]
        correct = correct_by_condition[condition]
        errors = error_by_condition[condition]
        lines.append(
            f"| {condition} | {records} | {correct} | {correct / records:.3f} | "
            f"{dict(errors) if errors else 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Paired Diagnostics",
            "",
            f"- C5 correct while lite is wrong: {c5_over_lite}",
            f"- strong correct while lite is wrong: {strong_over_lite}",
            f"- C5 correct while strong is wrong: {c5_over_strong}",
            f"- strong correct while C5 is wrong: {strong_over_c5}",
            "",
            "| question_id | lite | strong | C5 | lite error | strong error | C5 error |",
            "|---|---:|---:|---:|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['question_id']} | {row['lite']} | {row['strong']} | {row['c5']} | "
            f"{row['lite_error']} | {row['strong_error']} | {row['c5_error']} |"
        )
    lines.extend(
        [
            "",
            "## Gold-Leakage Check",
            "",
            "- C1_LiteSchemaOnly receives only schema and question.",
            "- C1_StrongDirect and C5 receive answer-shape metadata and required literals, but not gold SQL, gold result rows, expected hashes, or test examples.",
            "- The C5 ranker uses only read-only execution status, answer-shape column count, required-literal presence, order cues, and candidate index.",
            "- Gold SQL is used only after prediction generation by `evaluator.score_prediction` to score this dev-only pilot.",
            "",
            "## Decision",
            "",
        ]
    )
    if c5_over_strong > strong_over_c5:
        lines.append("C5 shows a dev-set advantage over C1_StrongDirect in this ablation.")
    elif c5_over_lite > 0 and c5_over_strong == 0:
        lines.append("C5 improves over schema-only prompting, but not over C1_StrongDirect. The likely contribution is value/shape context rather than reranking superiority.")
    else:
        lines.append("No C5 advantage appears over the tested baselines in this ablation.")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    questions = dev_pilot.load_dev_questions()
    client = smoke.llm_client()
    predictions: list[dict[str, Any]] = []
    conn = sqlite3.connect(smoke.DB_PATH)
    try:
        lite_context = lite_schema_context()
        strong_context = smoke.schema_context(conn)
        for record in questions:
            predictions.append(run_lite_condition(client, lite_context, record))
            predictions.extend(dev_pilot.run_condition_pair(conn, client, strong_context, record))
        with PREDICTIONS_PATH.open("w", encoding="utf-8") as f:
            for prediction in predictions:
                f.write(json.dumps(prediction, sort_keys=True) + "\n")
        scores = score_predictions(conn, questions, predictions)
    finally:
        conn.close()

    with SCORES_PATH.open("w", encoding="utf-8") as f:
        for score in scores:
            f.write(json.dumps(asdict(score), sort_keys=True) + "\n")

    write_report(predictions, scores)

    if len(predictions) != 60:
        print(f"FAIL: expected 60 prediction records, got {len(predictions)}")
        return 1
    if any(prediction.get("error") for prediction in predictions):
        print("FAIL: at least one prediction has a model/extraction error")
        return 1
    if any(score.contract_errors for score in scores):
        print("FAIL: at least one prediction has contract errors")
        return 1
    if any(not score.safe_sql for score in scores):
        print("FAIL: at least one prediction has unsafe SQL")
        return 1
    print(f"PASS: dev ablation pilot completed; report={REPORT_PATH.relative_to(WORKSPACE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
