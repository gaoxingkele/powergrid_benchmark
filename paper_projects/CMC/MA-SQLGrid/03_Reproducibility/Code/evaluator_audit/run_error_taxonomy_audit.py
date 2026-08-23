#!/usr/bin/env python3
"""Generate a nonverbatim, automated error decomposition under the unified evaluator."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from run_unified_evaluator_audit import (
    BACKBONES,
    CONDITIONS,
    SELECTORS,
    SQLiteReadOnlyExecutor,
    evaluate,
    load_jsonl,
    normalize_sql,
    sha256,
    sql_hash,
)


REPRO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPRO_ROOT / "Data" / "error_taxonomy" / "unified_v1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--qwen", type=Path, required=True)
    parser.add_argument("--granite", type=Path, required=True)
    parser.add_argument("--selection-inputs", type=Path, required=True)
    parser.add_argument("--selections", type=Path, required=True)
    parser.add_argument("--unified-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite output: {args.output}")
    args.output.mkdir(parents=True)

    selected_ids = {row["question_id"] for row in load_jsonl(args.selection_inputs)}
    questions = {row["question_id"]: row for row in load_jsonl(args.questions) if row["question_id"] in selected_ids}
    if len(questions) != 180:
        raise AssertionError("Expected the frozen 180-question universe")

    predictions: dict[str, dict[tuple[str, str], dict[str, Any]]] = {}
    for backbone, path in (("qwen", args.qwen), ("granite", args.granite)):
        rows = load_jsonl(path)
        predictions[backbone] = {(row["question_id"], row["condition"]): row for row in rows}
        if len(rows) != 720 or len(predictions[backbone]) != 720:
            raise AssertionError(f"{backbone}: prediction grid is not 180x4")

    selections = {(row["question_id"], row["method"]): row for row in load_jsonl(args.selections)}
    source_by_slot = {
        f"C{index:03d}": f"{backbone}:{condition}"
        for index, (backbone, condition) in enumerate((b, c) for b in BACKBONES for c in CONDITIONS)
    }
    slot_by_source = {source: slot for slot, source in source_by_slot.items()}

    trace_path = args.output / "execution_trace.jsonl"
    executor = SQLiteReadOnlyExecutor(
        args.db,
        timeout_seconds=2.0,
        max_opcodes=2_000_000,
        progress_step=1_000,
        max_rows=10_000,
        allow_metadata=False,
        trace_path=trace_path,
    )

    fixed_verdicts: dict[str, dict[str, dict[str, Any]]] = {}
    fixed_hashes: dict[tuple[str, str], str] = {}
    for qid in sorted(questions):
        record = questions[qid]
        gold = executor(normalize_sql(record["gold_sql"]))
        fixed_verdicts[qid] = {}
        for source in slot_by_source:
            backbone, condition = source.split(":", 1)
            sql = predictions[backbone][(qid, condition)]["predicted_sql"]
            result = executor(normalize_sql(sql))
            fixed_verdicts[qid][source] = evaluate(result, gold, record)
            fixed_hashes[(qid, source)] = sql_hash(sql)

    method_to_slot: dict[str, dict[str, str]] = {
        source: {qid: slot_by_source[source] for qid in questions} for source in slot_by_source
    }
    method_to_slot["C000_fixed_order_equal_budget"] = {qid: "C000" for qid in questions}
    for selector in SELECTORS:
        method_to_slot[selector] = {
            qid: selections[(qid, selector)]["selected_candidate_id"] for qid in questions
        }

    item_rows: list[dict[str, Any]] = []
    summary_counts: Counter[tuple[str, str]] = Counter()
    for method, selected in method_to_slot.items():
        for qid in sorted(questions):
            slot = selected[qid]
            source = source_by_slot[slot]
            verdict = fixed_verdicts[qid][source]
            record = questions[qid]
            error_type = verdict["error_type"]
            summary_counts[(method, error_type)] += 1
            item_rows.append(
                {
                    "question_id": qid,
                    "method": method,
                    "selected_slot": slot,
                    "selected_source": source,
                    "automatic_error_type": error_type,
                    "correct": int(verdict["correct"]),
                    "expected_columns": verdict["expected_columns"],
                    "candidate_columns": verdict["candidate_columns"],
                    "gold_columns": verdict["gold_columns"],
                    "candidate_rows": verdict["candidate_rows"],
                    "gold_rows": verdict["gold_rows"],
                    "difficulty": record["difficulty"],
                    "order_sensitive": int(bool(record["order_sensitive"])),
                    "tables": "|".join(sorted(record["tables"])),
                    "sql_feature_tags": "|".join(sorted(record["sql_feature_tags"])),
                    "candidate_sql_sha256": fixed_hashes[(qid, source)],
                    "gold_sql_sha256": sql_hash(record["gold_sql"]),
                }
            )

    if len(item_rows) != 1980:
        raise AssertionError(f"Expected 1,980 method-item rows, found {len(item_rows)}")
    unified = json.loads(args.unified_summary.read_text(encoding="utf-8"))
    expected_counts = {row["method"]: int(row["correct"]) for row in unified["summary"]}
    observed_counts = {
        method: summary_counts[(method, "correct")] for method in method_to_slot
    }
    if observed_counts != expected_counts:
        raise AssertionError(f"Unified counts do not reproduce: {observed_counts} != {expected_counts}")
    qwen_f00 = [row for row in item_rows if row["method"] == "qwen:F00_Full_NoShape"]
    c000 = [row for row in item_rows if row["method"] == "C000_fixed_order_equal_budget"]
    if [(r["question_id"], r["automatic_error_type"]) for r in qwen_f00] != [
        (r["question_id"], r["automatic_error_type"]) for r in c000
    ]:
        raise AssertionError("C000 and Qwen F00 item verdicts differ")

    categories = (
        "correct",
        "candidate_execution_error",
        "gold_execution_error",
        "candidate_shape_mismatch",
        "gold_shape_mismatch",
        "wrong_denotation",
    )
    summary_rows = [
        {
            "method": method,
            **{category: summary_counts[(method, category)] for category in categories},
            "n": 180,
        }
        for method in method_to_slot
    ]

    cross_counts: Counter[tuple[str, str, str, str]] = Counter()
    for row in item_rows:
        dimensions = [
            ("difficulty", row["difficulty"]),
            ("order_sensitive", str(row["order_sensitive"])),
        ]
        dimensions.extend(("table", value) for value in row["tables"].split("|") if value)
        dimensions.extend(("sql_feature_tag", value) for value in row["sql_feature_tags"].split("|") if value)
        for dimension, level in dimensions:
            cross_counts[(row["method"], dimension, level, row["automatic_error_type"])] += 1
    cross_rows = [
        {
            "method": method,
            "dimension": dimension,
            "level": level,
            "automatic_error_type": error_type,
            "count": count,
        }
        for (method, dimension, level, error_type), count in sorted(cross_counts.items())
    ]

    write_csv(args.output / "method_error_counts.csv", summary_rows)
    write_csv(args.output / "selected_item_errors.csv", item_rows)
    write_csv(args.output / "error_crosstabs.csv", cross_rows)
    report = {
        "protocol_id": "MA-SQLGrid-automated-error-taxonomy-unified-v1",
        "evaluator_id": unified["evaluator_id"],
        "post_review_automated_diagnostic": True,
        "expert_semantic_adjudication": False,
        "question_count": 180,
        "method_item_rows": len(item_rows),
        "bounded_executions": len(load_jsonl(trace_path)),
        "input_sha256": {
            "database": sha256(args.db),
            "questions": sha256(args.questions),
            "qwen_predictions": sha256(args.qwen),
            "granite_predictions": sha256(args.granite),
            "selections": sha256(args.selections),
            "unified_summary": sha256(args.unified_summary),
        },
        "correct_counts": observed_counts,
    }
    if report["bounded_executions"] != 1620:
        raise AssertionError("Execution trace does not contain 1,620 rows")
    (args.output / "error_taxonomy_summary.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    selectors = ["C000_fixed_order_equal_budget", *SELECTORS, "qwen:F01_Full_WithShape"]
    by_method = {row["method"]: row for row in summary_rows}
    lines = [
        "# Automated Error Taxonomy under the Unified Evaluator",
        "",
        "This is a post-review evaluator-state decomposition. It is not expert semantic adjudication and cannot identify business-meaning errors.",
        "",
        "| Method | Correct | Execution error | Shape mismatch | Wrong denotation |",
        "|---|---:|---:|---:|---:|",
    ]
    for method in selectors:
        row = by_method[method]
        lines.append(
            f"| {method} | {row['correct']} | {row['candidate_execution_error']} | "
            f"{row['candidate_shape_mismatch']} | {row['wrong_denotation']} |"
        )
    lines.extend(
        [
            "",
            "Gold execution and gold-shape errors were retained as fail-closed categories; their observed counts are available in `method_error_counts.csv`. The item ledger contains identifiers, labels, counts, and hashes only. Qualified review is still required to distinguish status, time, unit, topology, and operational-intent errors.",
            "",
        ]
    )
    (args.output / "AUTOMATED_ERROR_TAXONOMY_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
