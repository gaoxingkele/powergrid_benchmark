#!/usr/bin/env python3
"""Read-only validator and residual-error diagnostics for MA-SQLGrid.

This script consumes the repaired formal C1-C5 artifacts and trace files. It
does not generate SQL, change predictions, or expose gold answers to the model
or ranker. Gold data are used only offline to score alternative selections
already present in C5 traces.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPERIMENT_DIR = Path(__file__).resolve().parent
WORKSPACE = EXPERIMENT_DIR
for candidate in [EXPERIMENT_DIR, *EXPERIMENT_DIR.parents]:
    if (candidate / "data" / "griddb_maintenance_v2_v0_1" / "database.sqlite").exists():
        WORKSPACE = candidate.resolve()
        break

DATA_DIR = WORKSPACE / "data" / "griddb_maintenance_v2_v0_1"
DB_PATH = DATA_DIR / "database.sqlite"
QUESTIONS_PATH = DATA_DIR / "questions.jsonl"
OUT_DIR = EXPERIMENT_DIR / "outputs"
PREDICTIONS_PATH = OUT_DIR / "predictions.jsonl"
SCORES_PATH = OUT_DIR / "scores.jsonl"
DIAG_DIR = EXPERIMENT_DIR.parent / "validator_diagnostics"
RESULTS_PATH = DIAG_DIR / "validator_diagnostics.json"
REPORT_PATH = DIAG_DIR / "validator_diagnostics.md"

sys.path.insert(0, str(WORKSPACE / "evaluator"))

from evaluator import load_questions, score_prediction  # noqa: E402


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def default_score(validation: dict[str, Any], idx: int) -> int:
    score = 0
    score += 10 if validation["safe"] else -20
    score += 10 if validation["exec_ok"] else -15
    score += 6 if validation["shape_ok"] else -5
    score += 3 if validation["order_ok"] else -2
    score -= 2 if validation["empty_result"] else 0
    score += 4 * int(validation["value_hits"])
    score -= 3 * len(validation["missing_value_hints"])
    score -= idx
    return score


def variant_score(validation: dict[str, Any], idx: int, variant: str) -> int:
    if variant == "default_recomputed":
        return default_score(validation, idx)
    score = 0
    score += 10 if validation["safe"] else -20
    score += 10 if validation["exec_ok"] else -15
    if variant != "no_shape_term":
        score += 6 if validation["shape_ok"] else -5
    if variant != "no_order_empty_terms":
        score += 3 if validation["order_ok"] else -2
        score -= 2 if validation["empty_result"] else 0
    if variant != "no_value_terms":
        score += 4 * int(validation["value_hits"])
        score -= 3 * len(validation["missing_value_hints"])
    if variant == "exec_only":
        score = 0
        score += 10 if validation["safe"] else -20
        score += 10 if validation["exec_ok"] else -15
    score -= idx
    return score


def choose_variant(trace: list[dict[str, Any]], variant: str) -> int:
    best_idx = 0
    best_score = -10_000
    for entry in trace:
        idx = int(entry["candidate_index"])
        score = variant_score(entry, idx, variant)
        if score > best_score:
            best_idx = idx
            best_score = score
    return best_idx


def selected_entry(trace: list[dict[str, Any]], selected_idx: int) -> dict[str, Any]:
    for entry in trace:
        if int(entry["candidate_index"]) == selected_idx:
            return entry
    raise RuntimeError(f"selected index {selected_idx} missing from rank trace")


def error_prefix(details: str) -> str:
    if details.startswith("no such column:"):
        return details
    if details.startswith("ambiguous column name:"):
        return details
    return details.split(":", 1)[0]


def main() -> int:
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    predictions = load_jsonl(PREDICTIONS_PATH)
    scores = load_jsonl(SCORES_PATH)
    score_by_key = {(row["question_id"], row["condition"]): row for row in scores}
    records = {row["question_id"]: row for row in load_questions(QUESTIONS_PATH)}
    conn = sqlite3.connect(DB_PATH)

    c5_condition = "C5_MASQLGrid_DomainContext_Validated"
    c5_predictions = [row for row in predictions if row["condition"] == c5_condition]
    selected_stats: Counter[str] = Counter()
    selected_exec_errors: Counter[str] = Counter()
    variant_rows: dict[str, list[int]] = {
        "default_recomputed": [],
        "no_shape_term": [],
        "no_value_terms": [],
        "no_order_empty_terms": [],
        "exec_only": [],
    }
    variant_changed: Counter[str] = Counter()
    variant_correct: Counter[str] = Counter()

    try:
        for pred in c5_predictions:
            trace_path = WORKSPACE / pred["intermediate_trace_path"]
            trace_doc = json.loads(trace_path.read_text(encoding="utf-8"))
            rank_trace = trace_doc["rank_trace"]
            selected_idx = int(pred["selected_candidate_index"])
            selected = selected_entry(rank_trace, selected_idx)
            if selected_idx != 0:
                selected_stats["selected_non_first"] += 1
            if trace_doc.get("repaired_sql"):
                selected_stats["repair_response_nonempty"] += 1
            if trace_doc.get("repaired_sql") and selected.get("sql") == trace_doc.get("repaired_sql"):
                selected_stats["selected_repair"] += 1
            for key in ["safe", "exec_ok", "shape_ok", "order_ok"]:
                if selected.get(key):
                    selected_stats[f"selected_{key}"] += 1
            if selected.get("exec_error"):
                selected_exec_errors[error_prefix(str(selected["exec_error"]))] += 1

            for variant in variant_rows:
                chosen_idx = choose_variant(rank_trace, variant)
                variant_rows[variant].append(chosen_idx)
                if chosen_idx != selected_idx:
                    variant_changed[variant] += 1
                chosen_sql = selected_entry(rank_trace, chosen_idx)["sql"]
                score = score_prediction(conn, records[pred["question_id"]], chosen_sql)
                if score.correct:
                    variant_correct[variant] += 1
    finally:
        conn.close()

    residual_errors: dict[str, Any] = {}
    for condition in ["C4_MASQLGrid_DomainContext", c5_condition]:
        rows = [row for row in scores if row["condition"] == condition and not row["evaluator_correct"]]
        exec_rows = [row for row in rows if row["evaluator_error_type"] == "execution_error"]
        residual_errors[condition] = {
            "incorrect_count": len(rows),
            "execution_error_count": len(exec_rows),
            "wrong_denotation_count": sum(1 for row in rows if row["evaluator_error_type"] == "wrong_denotation"),
            "shape_mismatch_count": sum(1 for row in rows if row["evaluator_error_type"] == "shape_mismatch"),
            "execution_error_taxonomy": dict(Counter(error_prefix(row["evaluator_details"]) for row in exec_rows)),
            "execution_error_question_ids": [row["question_id"] for row in exec_rows],
        }

    result = {
        "task_id": "validator-diagnostics",
        "source_predictions": str(PREDICTIONS_PATH.relative_to(WORKSPACE)),
        "source_scores": str(SCORES_PATH.relative_to(WORKSPACE)),
        "c5_question_count": len(c5_predictions),
        "c5_selection": {
            "selected_non_first": selected_stats["selected_non_first"],
            "repair_response_nonempty": selected_stats["repair_response_nonempty"],
            "selected_repair": selected_stats["selected_repair"],
            "selected_safe": selected_stats["selected_safe"],
            "selected_executable": selected_stats["selected_exec_ok"],
            "selected_shape_ok": selected_stats["selected_shape_ok"],
            "selected_order_ok": selected_stats["selected_order_ok"],
            "selected_exec_error_taxonomy": dict(selected_exec_errors),
        },
        "offline_weight_sensitivity": {
            variant: {
                "changed_selection_count": variant_changed[variant],
                "execution_accuracy": variant_correct[variant] / len(c5_predictions),
                "correct": variant_correct[variant],
                "question_count": len(c5_predictions),
            }
            for variant in variant_rows
        },
        "residual_errors": residual_errors,
        "score_check": {
            "c4_execution_accuracy": sum(
                1 for row in scores if row["condition"] == "C4_MASQLGrid_DomainContext" and row["evaluator_correct"]
            )
            / 180,
            "c5_execution_accuracy": sum(1 for row in scores if row["condition"] == c5_condition and row["evaluator_correct"])
            / 180,
        },
    }

    RESULTS_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# MA-SQLGrid Validator Diagnostics",
        "",
        "## C5 Selection Behavior",
        "",
        f"- C5 traces: {result['c5_question_count']}",
        f"- Selected a non-first candidate: {result['c5_selection']['selected_non_first']}/{result['c5_question_count']}",
        f"- Nonempty repair response accepted: {result['c5_selection']['selected_repair']}/{result['c5_question_count']}",
        f"- Selected SQL executable: {result['c5_selection']['selected_executable']}/{result['c5_question_count']}",
        f"- Selected SQL shape-compatible: {result['c5_selection']['selected_shape_ok']}/{result['c5_question_count']}",
        f"- Selected SQL order-compatible: {result['c5_selection']['selected_order_ok']}/{result['c5_question_count']}",
        f"- Selected execution-error taxonomy: {result['c5_selection']['selected_exec_error_taxonomy']}",
        "",
        "## Offline Ranker-Weight Sensitivity",
        "",
        "| variant | changed selections | correct | execution accuracy |",
        "|---|---:|---:|---:|",
    ]
    for variant, row in result["offline_weight_sensitivity"].items():
        lines.append(
            f"| {variant} | {row['changed_selection_count']}/{row['question_count']} | "
            f"{row['correct']}/{row['question_count']} | {row['execution_accuracy']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Residual Execution Errors",
            "",
            "| condition | execution errors | taxonomy |",
            "|---|---:|---|",
        ]
    )
    for condition, row in result["residual_errors"].items():
        lines.append(f"| {condition} | {row['execution_error_count']} | {row['execution_error_taxonomy']} |")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        "VALIDATOR_DIAGNOSTICS "
        f"c5_non_first={result['c5_selection']['selected_non_first']} "
        f"c5_selected_repair={result['c5_selection']['selected_repair']} "
        f"c4_exec_errors={result['residual_errors']['C4_MASQLGrid_DomainContext']['execution_error_count']} "
        f"c5_exec_errors={result['residual_errors'][c5_condition]['execution_error_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
