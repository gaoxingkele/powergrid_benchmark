#!/usr/bin/env python3
"""Bounded in-domain component ablations for MA-SQLGrid C4.

This addendum does not replace the repaired C1-C5 formal results. It runs two
generation-path ablations on the same held-out GridDB test split:

- C4_NoValueHints: domain-selected schema and answer-shape hints, but no exact
  matched values or normalized value hints rendered in the prompt.
- C4_NoShapeHints: domain-selected schema and value hints, but no answer-shape
  hints rendered in the prompt.

The script preserves the no-gold prediction contract used by the formal run.
Gold SQL/results and evaluator labels are used only after prediction for
scoring.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import Any

import main as formal


ADDENDUM_DIR = formal.EXPERIMENT_DIR.parent / "component_ablation_addendum"
PREDICTIONS_PATH = ADDENDUM_DIR / "predictions.jsonl"
SCORES_PATH = ADDENDUM_DIR / "scores.jsonl"
CONTEXTS_PATH = ADDENDUM_DIR / "contexts.jsonl"
RESULTS_PATH = ADDENDUM_DIR / "results.json"
REPORT_PATH = ADDENDUM_DIR / "report.md"
TRACE_DIR = ADDENDUM_DIR / "traces"

ABLATION_ORDER = [
    "C4_NoValueHints",
    "C4_NoShapeHints",
]


def ensure_addendum_dirs() -> None:
    ADDENDUM_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    for path in [PREDICTIONS_PATH, SCORES_PATH, CONTEXTS_PATH, RESULTS_PATH, REPORT_PATH]:
        if path.exists():
            path.unlink()
    for path in TRACE_DIR.glob("*.json"):
        path.unlink()


def clone_context(context: dict[str, Any], *, condition: str) -> dict[str, Any]:
    cloned = json.loads(json.dumps(context))
    cloned["mode"] = condition
    if condition == "C4_NoValueHints":
        cloned["matched_values"] = {}
        cloned["normalized_value_hints"] = []
    elif condition == "C4_NoShapeHints":
        cloned["inferred_shape"] = {}
    else:
        raise ValueError(f"unknown ablation condition: {condition}")
    return cloned


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def run_condition(
    *,
    client: Any,
    conn: sqlite3.Connection,
    record: dict[str, Any],
    condition: str,
    context: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    context_text = formal.chess.render_selected_context(context, domain=True)
    prompt = formal.direct_prompt(record, context_text, condition)
    raw = ""
    model = formal.smoke.MODEL_NAME
    latency_ms = 0
    token_input = 0
    token_output = 0
    retry_count = 0
    error = None
    sql = "SELECT 1;"
    try:
        raw, model, latency_ms, token_input, token_output, retry_count = formal.call_model_with_retries(client, prompt)
        sql = formal.smoke.extract_sql(raw)
    except Exception as exc:  # pragma: no cover - depends on external provider
        error = f"{type(exc).__name__}: {exc}"
    if not sql.strip():
        sql = "SELECT 1;"
        error = error or "empty SQL extracted"

    trace_path = TRACE_DIR / f"{record['question_id']}_seed{seed}_{condition}.json"
    formal.write_trace(
        trace_path,
        {
            "prompt": prompt,
            "raw_response": raw,
            "context_mode": condition,
            "ablation_note": (
                "value hints removed from prompt"
                if condition == "C4_NoValueHints"
                else "answer-shape hints removed from prompt"
            ),
        },
    )
    return formal.prediction_record(
        question_id=record["question_id"],
        condition=condition,
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


def score_ablation_predictions(
    conn: sqlite3.Connection,
    records: list[dict[str, Any]],
    contexts: dict[tuple[str, str], dict[str, Any]],
    predictions: list[dict[str, Any]],
) -> list[formal.ScoreRow]:
    by_id = {record["question_id"]: record for record in records}
    rows: list[formal.ScoreRow] = []
    for prediction in predictions:
        record = by_id[prediction["question_id"]]
        context = contexts[(prediction["question_id"], prediction["condition"])]
        contract_errors = formal.validate_prediction_contract(prediction)
        safe, _, _ = formal.validate_read_only_select(prediction["predicted_sql"])
        score = formal.score_prediction(conn, record, prediction["predicted_sql"])
        validation = formal.chess.reference_free_validation(conn, context, prediction["predicted_sql"])
        value_hint_count = int(validation.get("value_hint_count") or 0)
        value_hint_coverage = 1.0 if value_hint_count == 0 else float(validation.get("value_hits") or 0) / value_hint_count
        table_recall, column_recall = formal.context_recall(record, context)
        trace_path = formal.WORKSPACE / prediction["intermediate_trace_path"]
        prompt_token_estimate = 0
        if trace_path.exists():
            prompt = json.loads(trace_path.read_text(encoding="utf-8")).get("prompt", "")
            prompt_token_estimate = formal.chess.estimate_tokens(prompt)
        rows.append(
            formal.ScoreRow(
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
    return rows


def aggregate_ablation_scores(scores: list[formal.ScoreRow]) -> dict[str, Any]:
    by_condition: dict[str, list[formal.ScoreRow]] = {}
    for row in scores:
        by_condition.setdefault(row.condition, []).append(row)
    metrics: dict[str, Any] = {}
    for condition in ABLATION_ORDER:
        rows = by_condition.get(condition, [])
        metrics[condition] = {
            "question_count": len(rows),
            "correct": sum(1 for row in rows if row.evaluator_correct),
            "execution_accuracy": formal.mean([1.0 if row.evaluator_correct else 0.0 for row in rows]),
            "safe_sql_rate": formal.mean([1.0 if row.safe_sql else 0.0 for row in rows]),
            "answer_shape_accuracy": formal.mean([1.0 if row.answer_shape_ok else 0.0 for row in rows]),
            "value_hint_coverage": formal.mean([row.value_hint_coverage for row in rows]),
            "prompt_token_estimate": formal.mean([float(row.prompt_token_estimate) for row in rows]),
            "latency_ms": formal.mean([float(row.latency_ms) for row in rows]),
            "provider_failure_rate": formal.mean([1.0 if row.provider_error else 0.0 for row in rows]),
            "contract_error_count": sum(1 for row in rows if row.contract_errors),
            "error_taxonomy": dict(formal.Counter(row.evaluator_error_type for row in rows if not row.evaluator_correct)),
        }
    return metrics


def write_report(metrics: dict[str, Any]) -> None:
    lines = [
        "# MA-SQLGrid Component Ablation Addendum",
        "",
        "## Scope",
        "",
        "- Split: held-out GridDB-Maintenance-v2 v0.1 test questions Q021-Q200.",
        "- Generator/provider: same fixed provider contract as the repaired C1-C5 formal run.",
        "- Decoding: temperature 0; seed 0 is a deterministic pass label.",
        "- Contract: no gold SQL, gold denotation rows, evaluator correctness, required-literal metadata, answer-shape metadata, or order-sensitive metadata in prompts or prediction records.",
        "- Status: addendum only; it does not replace the repaired C1-C5 main results.",
        "",
        "## Conditions",
        "",
        "- C4_NoValueHints: uses the C4 domain-selected schema and answer-shape hints but removes exact matched values and normalized value hints from the prompt.",
        "- C4_NoShapeHints: uses the C4 domain-selected schema and value hints but removes answer-shape hints from the prompt.",
        "",
        "## Results",
        "",
        "| condition | correct | execution accuracy | safe SQL | answer-shape accuracy | prompt tokens | latency ms | error taxonomy |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for condition in ABLATION_ORDER:
        metric = metrics[condition]
        lines.append(
            f"| {condition} | {metric['correct']}/{metric['question_count']} | "
            f"{metric['execution_accuracy']:.4f} | {metric['safe_sql_rate']:.4f} | "
            f"{metric['answer_shape_accuracy']:.4f} | {metric['prompt_token_estimate']:.1f} | "
            f"{metric['latency_ms']:.1f} | {metric['error_taxonomy']} |"
        )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ensure_addendum_dirs()
    formal.validate_foundation()
    records = formal.load_split_records("formal")
    seed = formal.FORMAL_SEEDS[0]
    client = formal.llm_client()
    predictions: list[dict[str, Any]] = []
    context_rows: list[dict[str, Any]] = []
    contexts: dict[tuple[str, str], dict[str, Any]] = {}

    conn = sqlite3.connect(formal.DB_PATH)
    try:
        for record in records:
            base_context = formal.chess.infer_domain_context(conn, record)
            for condition in ABLATION_ORDER:
                context = clone_context(base_context, condition=condition)
                contexts[(record["question_id"], condition)] = context
                context_rows.append(context)
                prediction = run_condition(
                    client=client,
                    conn=conn,
                    record=record,
                    condition=condition,
                    context=context,
                    seed=seed,
                )
                predictions.append(prediction)
                print(f"ABLATION_PREDICTED question={record['question_id']} condition={condition}")
        scores = score_ablation_predictions(conn, records, contexts, predictions)
    finally:
        conn.close()

    score_dicts = [asdict(row) for row in scores]
    metrics = aggregate_ablation_scores(scores)
    result = {
        "task_id": "component-ablation-addendum",
        "mode": "formal_addendum",
        "dataset": formal.relative_to_workspace(formal.DATA_DIR),
        "question_count": len(records),
        "conditions": ABLATION_ORDER,
        "formal_seed_policy": "single deterministic pass",
        "seeds": [seed],
        "prediction_count": len(predictions),
        "score_count": len(score_dicts),
        "metrics": metrics,
        "artifacts": {
            "predictions": formal.relative_to_workspace(PREDICTIONS_PATH),
            "scores": formal.relative_to_workspace(SCORES_PATH),
            "contexts": formal.relative_to_workspace(CONTEXTS_PATH),
            "report": formal.relative_to_workspace(REPORT_PATH),
            "traces": formal.relative_to_workspace(TRACE_DIR),
        },
    }
    write_jsonl(PREDICTIONS_PATH, predictions)
    write_jsonl(SCORES_PATH, score_dicts)
    write_jsonl(CONTEXTS_PATH, context_rows)
    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(metrics)

    for condition in ABLATION_ORDER:
        metric = metrics[condition]
        print(
            "SUMMARY "
            f"condition={condition} metric=execution_accuracy "
            f"mean={metric['execution_accuracy']:.6f} correct={metric['correct']}/{metric['question_count']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
