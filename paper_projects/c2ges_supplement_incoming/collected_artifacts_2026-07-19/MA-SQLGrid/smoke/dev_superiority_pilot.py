#!/usr/bin/env python3
"""Dev-only C1 vs C5 minimum superiority pilot.

This pilot is still pre-three-pack evidence. It uses only the dev split to
check whether the value-grounded rerank path shows any measurable advantage
over Strong Direct before the formal executor pipeline exists.
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
OUT_DIR = WORKSPACE / "smoke" / "dev_pilot"
PREDICTIONS_PATH = OUT_DIR / "predictions.jsonl"
SCORES_PATH = OUT_DIR / "scores.jsonl"
REPORT_PATH = OUT_DIR / "dev_pilot_report.md"
TRACE_DIR = OUT_DIR / "traces"

sys.path.insert(0, str(WORKSPACE / "smoke"))

import minimal_text2sql_smoke as smoke  # noqa: E402


def load_dev_questions() -> list[dict[str, Any]]:
    splits = json.loads((smoke.DATA_DIR / "splits.json").read_text(encoding="utf-8"))
    dev_ids = list(splits.get("dev", []))
    if len(dev_ids) != 20:
        raise RuntimeError(f"Expected exactly 20 dev questions, got {len(dev_ids)}")
    by_id = {record["question_id"]: record for record in smoke.load_questions(smoke.QUESTIONS_PATH)}
    missing = [qid for qid in dev_ids if qid not in by_id]
    if missing:
        raise RuntimeError(f"Missing dev question IDs: {missing}")
    records = [by_id[qid] for qid in dev_ids]
    non_dev = [record["question_id"] for record in records if record["split"] != "dev"]
    if non_dev:
        raise RuntimeError(f"Pilot must use dev questions only, got non-dev IDs: {non_dev}")
    return records


def run_condition_pair(
    conn: sqlite3.Connection,
    client: Any,
    schema_text: str,
    record: dict[str, Any],
) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []

    prompt = smoke.strong_direct_prompt(record, schema_text)
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
    except Exception as exc:  # Keep a record, but the pilot will fail if any error remains.
        error = f"{type(exc).__name__}: {exc}"
    trace_path = TRACE_DIR / f"{record['question_id']}_C1_StrongDirect.json"
    trace_path.write_text(json.dumps({"prompt": prompt, "raw_response": raw}, indent=2) + "\n", encoding="utf-8")
    predictions.append(
        smoke.prediction_record(
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

    prompt = smoke.vg_candidate_prompt(record, schema_text)
    error = None
    raw = ""
    model = smoke.MODEL_NAME
    latency_ms = 0
    input_tokens = 0
    output_tokens = 0
    candidates = ["SELECT 1;"]
    try:
        raw, model, latency_ms, input_tokens, output_tokens = smoke.call_model(client, prompt)
        candidates = smoke.extract_candidate_sql(raw)
        if not candidates:
            candidates = ["SELECT 1;"]
            error = "no SQL candidate extracted"
    except Exception as exc:  # Keep a record, but the pilot will fail if any error remains.
        error = f"{type(exc).__name__}: {exc}"
    selected_idx, rank_trace = smoke.rank_candidates(conn, record, candidates)
    trace_path = TRACE_DIR / f"{record['question_id']}_C5_VG_Rerank_Minimal.json"
    trace_path.write_text(
        json.dumps({"prompt": prompt, "raw_response": raw, "rank_trace": rank_trace}, indent=2) + "\n",
        encoding="utf-8",
    )
    predictions.append(
        smoke.prediction_record(
            question_id=record["question_id"],
            condition="C5_VG_Rerank_Minimal",
            model=model,
            prompt=prompt,
            schema_text=schema_text,
            predicted_sql=candidates[selected_idx],
            candidate_sql=candidates,
            selected_candidate_index=selected_idx,
            trace_path=str(trace_path.relative_to(WORKSPACE)),
            latency_ms=latency_ms,
            token_input=input_tokens,
            token_output=output_tokens,
            error=error,
        )
    )

    return predictions


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


def paired_summary(scores: list[smoke.SmokeScore]) -> dict[str, Any]:
    by_question: dict[str, dict[str, smoke.SmokeScore]] = {}
    for score in scores:
        by_question.setdefault(score.question_id, {})[score.condition] = score
    rows = []
    c5_wins = c1_wins = ties_correct = ties_wrong = 0
    for qid in sorted(by_question):
        c1 = by_question[qid]["C1_StrongDirect"]
        c5 = by_question[qid]["C5_VG_Rerank_Minimal"]
        if c5.evaluator_correct and not c1.evaluator_correct:
            outcome = "C5_win"
            c5_wins += 1
        elif c1.evaluator_correct and not c5.evaluator_correct:
            outcome = "C1_win"
            c1_wins += 1
        elif c1.evaluator_correct and c5.evaluator_correct:
            outcome = "tie_correct"
            ties_correct += 1
        else:
            outcome = "tie_wrong"
            ties_wrong += 1
        rows.append(
            {
                "question_id": qid,
                "c1_correct": c1.evaluator_correct,
                "c5_correct": c5.evaluator_correct,
                "c1_error": c1.evaluator_error_type,
                "c5_error": c5.evaluator_error_type,
                "outcome": outcome,
            }
        )
    return {
        "rows": rows,
        "c5_wins": c5_wins,
        "c1_wins": c1_wins,
        "ties_correct": ties_correct,
        "ties_wrong": ties_wrong,
        "measurable_advantage": c5_wins > c1_wins,
    }


def write_report(predictions: list[dict[str, Any]], scores: list[smoke.SmokeScore], summary: dict[str, Any]) -> None:
    condition_counts = Counter(prediction["condition"] for prediction in predictions)
    correct_by_condition = {
        condition: sum(score.evaluator_correct for score in scores if score.condition == condition)
        for condition in sorted(condition_counts)
    }
    error_by_condition = {
        condition: Counter(score.evaluator_error_type for score in scores if score.condition == condition and not score.evaluator_correct)
        for condition in sorted(condition_counts)
    }
    candidate_counts = Counter((prediction["condition"], len(prediction["candidate_sql"])) for prediction in predictions)
    lines = [
        "# Dev-Only C1 vs C5 Minimum Superiority Pilot",
        "",
        "## Scope",
        "",
        "- Purpose: check whether C5_VG_Rerank_Minimal shows any dev-set advantage over C1_StrongDirect before three-pack generation.",
        "- This is not a formal experiment and must not be used for paper claims.",
        "- Split: dev only, Q001-Q020. The test split Q021-Q200 is untouched.",
        f"- Model/provider: `{smoke.MODEL_NAME}` via `{smoke.PROVIDER}` `{smoke.BASE_URL}` with `wire_api={smoke.WIRE_API}` and temperature `{smoke.TEMPERATURE}`.",
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
        "- expected records: 40",
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
            "## Paired Superiority Diagnostic",
            "",
            f"- C5 wins: {summary['c5_wins']}",
            f"- C1 wins: {summary['c1_wins']}",
            f"- ties where both correct: {summary['ties_correct']}",
            f"- ties where both wrong: {summary['ties_wrong']}",
            f"- measurable dev advantage for C5: {summary['measurable_advantage']}",
            "",
            "| question_id | C1 correct | C5 correct | outcome | C1 error | C5 error |",
            "|---|---:|---:|---|---|---|",
        ]
    )
    for row in summary["rows"]:
        lines.append(
            f"| {row['question_id']} | {row['c1_correct']} | {row['c5_correct']} | "
            f"{row['outcome']} | {row['c1_error']} | {row['c5_error']} |"
        )
    lines.extend(
        [
            "",
            "## Gold-Leakage Check",
            "",
            "- Prompts include question text, schema, compact domain values, answer-shape metadata, order sensitivity, and required literal metadata.",
            "- Prompts do not include gold SQL, gold result rows, expected hashes, or test examples.",
            "- The C5 ranker uses only read-only execution status, answer-shape column count, required-literal presence, order cues, and candidate index.",
            "- Gold SQL is used only after prediction generation by `evaluator.score_prediction` to score this dev-only pilot.",
            "",
            "## Decision",
            "",
            (
                "C5 shows a measurable dev-set advantage over C1 under this pilot."
                if summary["measurable_advantage"]
                else "No measurable dev-set advantage for C5 over C1 appears under this pilot."
            ),
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    questions = load_dev_questions()
    client = smoke.llm_client()
    predictions: list[dict[str, Any]] = []
    conn = sqlite3.connect(smoke.DB_PATH)
    try:
        schema_text = smoke.schema_context(conn)
        for record in questions:
            predictions.extend(run_condition_pair(conn, client, schema_text, record))
        with PREDICTIONS_PATH.open("w", encoding="utf-8") as f:
            for prediction in predictions:
                f.write(json.dumps(prediction, sort_keys=True) + "\n")
        scores = score_predictions(conn, questions, predictions)
    finally:
        conn.close()

    with SCORES_PATH.open("w", encoding="utf-8") as f:
        for score in scores:
            f.write(json.dumps(asdict(score), sort_keys=True) + "\n")

    summary = paired_summary(scores)
    write_report(predictions, scores, summary)

    if len(predictions) != 40:
        print(f"FAIL: expected 40 prediction records, got {len(predictions)}")
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

    decision = (
        "C5 advantage observed"
        if summary["measurable_advantage"]
        else "no C5 advantage observed"
    )
    print(f"PASS: dev pilot completed; {decision}; report={REPORT_PATH.relative_to(WORKSPACE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
