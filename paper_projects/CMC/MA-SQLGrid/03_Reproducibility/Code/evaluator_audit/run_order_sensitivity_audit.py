#!/usr/bin/env python3
"""Exact candidate-order and descriptive risk--coverage audit.

The script consumes frozen pre-gold score ledgers and canonical-v2 item outcomes.
It never reads or emits SQL text and makes no model calls.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


REPRO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BLACKBOARDS = REPRO_ROOT / "Data" / "historical_pool" / "run_v3a" / "blackboards_sealed_before_gold.jsonl"
DEFAULT_CANONICAL = REPRO_ROOT / "Data" / "canonical_v2" / "canonical_rows_v2.jsonl"
DEFAULT_UNIFIED = REPRO_ROOT / "Data" / "evaluator_audit" / "run_unified_v1b" / "unified_evaluator_results.json"
DEFAULT_OUTPUT = REPRO_ROOT / "Data" / "evaluator_audit" / "order_sensitivity_unified_v1"

METHODS = {
    "validation_only": "decision:validation_rank_equal_budget_no_cf",
    "complete_witness": "decision:full_coordination_complete_metamorphic",
}
SLOT_TO_CELL = {
    "C000": ("qwen", "F00_Full_NoShape"),
    "C001": ("qwen", "F01_Full_WithShape"),
    "C002": ("qwen", "F10_Compact_NoShape"),
    "C003": ("qwen", "F11_Compact_WithShape"),
    "C004": ("granite", "F00_Full_NoShape"),
    "C005": ("granite", "F01_Full_WithShape"),
    "C006": ("granite", "F10_Compact_NoShape"),
    "C007": ("granite", "F11_Compact_WithShape"),
}
SLOTS = tuple(SLOT_TO_CELL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blackboards", type=Path, default=DEFAULT_BLACKBOARDS)
    parser.add_argument("--canonical", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--unified", type=Path, default=DEFAULT_UNIFIED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def normalize_sql(sql: str) -> str:
    """Match the unified evaluator's artifact-identity normalization."""
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL).strip()
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", sql, flags=re.IGNORECASE | re.DOTALL)
    return fenced.group(1).strip() if fenced else sql


def sql_hash(sql: str) -> str:
    return hashlib.sha256(normalize_sql(sql).encode("utf-8")).hexdigest().upper()


def nonordinal_key(score: dict[str, Any]) -> tuple[int, int, int]:
    total = int(score["counterfactual_total"])
    passes = int(score["counterfactual_passes"])
    cf_scaled = passes * 1_000_000 // total if total else -1
    return int(score["validation_points"]), cf_scaled, total


def extract_decision(board: dict[str, Any], kind: str) -> dict[str, Any]:
    matches = [message["payload"] for message in board["messages"] if message["kind"] == kind]
    if len(matches) != 1:
        raise AssertionError(f"{board['question_id']}: expected one {kind}, found {len(matches)}")
    return matches[0]


def select_from_top(top_slots: tuple[str, ...], order: tuple[str, ...]) -> str:
    top = set(top_slots)
    return next(slot for slot in order if slot in top)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    boards = load_jsonl(args.blackboards)
    canonical = load_jsonl(args.canonical)
    unified = json.loads(args.unified.read_text(encoding="utf-8"))

    if len(boards) != 180 or len({row["question_id"] for row in boards}) != 180:
        raise AssertionError("Expected 180 unique sealed blackboards")
    if len(canonical) != 1440:
        raise AssertionError(f"Expected 1,440 canonical rows, found {len(canonical)}")

    correctness: dict[tuple[str, str], bool] = {}
    for row in canonical:
        slot = next(
            candidate_id
            for candidate_id, cell in SLOT_TO_CELL.items()
            if cell == (row["backbone"], row["condition"])
        )
        key = (row["question_id"], slot)
        if key in correctness:
            raise AssertionError(f"Duplicate canonical outcome: {key}")
        correctness[key] = bool(row["execution"])
    if len(correctness) != 1440:
        raise AssertionError("Canonical outcome matrix is incomplete")

    recorded_summary = {row["method"]: row for row in unified["summary"]}
    if int(recorded_summary["C000_fixed_order_equal_budget"]["correct"]) != 76:
        raise AssertionError("Unified evaluator input does not record C000=76")

    board_by_qid = {board["question_id"]: board for board in boards}
    qids = tuple(sorted(board_by_qid))
    original_order = SLOTS
    reverse_order = tuple(reversed(SLOTS))
    top_sets: dict[str, dict[str, tuple[str, ...]]] = {method: {} for method in METHODS}
    recorded_choices: dict[str, dict[str, str]] = {method: {} for method in METHODS}
    sql_hashes: dict[str, dict[str, str]] = {}

    for qid in qids:
        board = board_by_qid[qid]
        pools = [message["payload"] for message in board["messages"] if message["kind"] == "eight_slot_candidate_pool"]
        if len(pools) != 1 or len(pools[0]["candidates"]) != 8:
            raise AssertionError(f"{qid}: expected one complete eight-slot candidate pool")
        sql_hashes[qid] = {row["candidate_id"]: sql_hash(row["sql"]) for row in pools[0]["candidates"]}
        for method, kind in METHODS.items():
            decision = extract_decision(board, kind)
            eligible = [score for score in decision["scores"] if score["eligible"]]
            if not eligible:
                raise AssertionError(f"{qid}/{method}: no eligible candidate")
            best_key = max(nonordinal_key(score) for score in eligible)
            top = tuple(score["candidate_id"] for score in eligible if nonordinal_key(score) == best_key)
            reconstructed = select_from_top(top, original_order)
            recorded = decision["selected_candidate_id"]
            if reconstructed != recorded:
                raise AssertionError(f"{qid}/{method}: reconstructed {reconstructed}, recorded {recorded}")
            top_sets[method][qid] = top
            recorded_choices[method][qid] = recorded

    original_counts = {
        method: sum(correctness[(qid, recorded_choices[method][qid])] for qid in qids)
        for method in METHODS
    }
    if original_counts != {"validation_only": 99, "complete_witness": 100}:
        raise AssertionError(f"Unexpected unified original-order counts: {original_counts}")
    c000_count = sum(correctness[(qid, "C000")] for qid in qids)
    if c000_count != 76:
        raise AssertionError(f"Unexpected C000 count: {c000_count}")

    histograms: dict[str, Counter[int]] = {method: Counter() for method in METHODS}
    reverse_counts: dict[str, int] = {}
    for method in METHODS:
        reverse_counts[method] = sum(
            correctness[(qid, select_from_top(top_sets[method][qid], reverse_order))] for qid in qids
        )

    permutation_count = 0
    for permutation in itertools.permutations(SLOTS):
        permutation_count += 1
        for method in METHODS:
            correct = sum(
                correctness[(qid, select_from_top(top_sets[method][qid], permutation))] for qid in qids
            )
            histograms[method][correct] += 1
    if permutation_count != 40_320:
        raise AssertionError(f"Expected 40,320 permutations, found {permutation_count}")

    permutation_rows: list[dict[str, Any]] = []
    method_summaries: dict[str, dict[str, Any]] = {}
    for method, histogram in histograms.items():
        if sum(histogram.values()) != 40_320:
            raise AssertionError(f"{method}: incomplete histogram")
        expanded = [score for score, frequency in sorted(histogram.items()) for _ in range(frequency)]
        tied_questions = sum(len(top_sets[method][qid]) > 1 for qid in qids)
        method_summaries[method] = {
            "original_order_correct": original_counts[method],
            "reverse_order_correct": reverse_counts[method],
            "permutations": 40_320,
            "minimum_correct": min(expanded),
            "median_correct": statistics.median(expanded),
            "mean_correct": statistics.fmean(expanded),
            "maximum_correct": max(expanded),
            "top_tie_questions": tied_questions,
            "mean_top_tie_size_all_questions": statistics.fmean(len(top_sets[method][qid]) for qid in qids),
            "mean_top_tie_size_tied_questions": statistics.fmean(
                len(top_sets[method][qid]) for qid in qids if len(top_sets[method][qid]) > 1
            ),
        }
        for correct, frequency in sorted(histogram.items()):
            permutation_rows.append(
                {"method": method, "correct_count": correct, "permutation_frequency": frequency}
            )

    item_rows: list[dict[str, Any]] = []
    for qid in qids:
        row: dict[str, Any] = {"question_id": qid}
        for method in METHODS:
            top = top_sets[method][qid]
            selected = recorded_choices[method][qid]
            row[f"{method}_top_tie_size"] = len(top)
            row[f"{method}_top_slots"] = "|".join(top)
            row[f"{method}_original_slot"] = selected
            row[f"{method}_original_correct"] = int(correctness[(qid, selected)])
            row[f"{method}_any_top_correct"] = int(any(correctness[(qid, slot)] for slot in top))
            row[f"{method}_all_top_correct"] = int(all(correctness[(qid, slot)] for slot in top))
        item_rows.append(row)

    risk_rows: list[dict[str, Any]] = []
    risk_areas: dict[str, float] = {}
    for method in METHODS:
        previous_coverage = 0.0
        area = 0.0
        for maximum_tie_size in range(1, 9):
            covered = [qid for qid in qids if len(top_sets[method][qid]) <= maximum_tie_size]
            correct = sum(correctness[(qid, recorded_choices[method][qid])] for qid in covered)
            risk_rows.append(
                {
                    "method": method,
                    "maximum_top_tie_size": maximum_tie_size,
                    "covered_questions": len(covered),
                    "coverage": len(covered) / len(qids),
                    "correct_covered": correct,
                    "covered_accuracy": correct / len(covered) if covered else "",
                    "overall_correct_yield": correct / len(qids),
                }
            )
            coverage = len(covered) / len(qids)
            selective_risk = 1 - (correct / len(covered)) if covered else 0.0
            area += (coverage - previous_coverage) * selective_risk
            previous_coverage = coverage
        risk_areas[method] = area

    unique_rows: list[dict[str, Any]] = []
    for qid in qids:
        hashes = sql_hashes[qid]
        row: dict[str, Any] = {
            "question_id": qid,
            "slot_count": 8,
            "unique_normalized_sql": len(set(hashes.values())),
            "duplicate_slots": 8 - len(set(hashes.values())),
        }
        for method in METHODS:
            top = top_sets[method][qid]
            row[f"{method}_top_slots"] = len(top)
            row[f"{method}_unique_top_sql"] = len({hashes[slot] for slot in top})
            row[f"{method}_duplicate_top_slots"] = len(top) - row[f"{method}_unique_top_sql"]
        unique_rows.append(row)

    args.output.mkdir(parents=True, exist_ok=True)
    write_csv(
        args.output / "permutation_histogram.csv",
        ["method", "correct_count", "permutation_frequency"],
        permutation_rows,
    )
    write_csv(args.output / "risk_coverage.csv", list(risk_rows[0]), risk_rows)
    write_csv(args.output / "per_question_ties.csv", list(item_rows[0]), item_rows)
    write_csv(args.output / "per_question_unique_sql.csv", list(unique_rows[0]), unique_rows)

    summary = {
        "protocol_id": "MA-SQLGrid-order-sensitivity-unified-v1",
        "evaluator_id": "MA-SQLGrid-GridDB-T0-shape-denotation-v1",
        "post_review_diagnostic": True,
        "question_count": len(qids),
        "candidate_slots": list(SLOTS),
        "fixed_c000_correct": c000_count,
        "inputs": {
            "blackboards": {"path": str(args.blackboards), "sha256": sha256(args.blackboards)},
            "canonical": {"path": str(args.canonical), "sha256": sha256(args.canonical)},
            "unified": {"path": str(args.unified), "sha256": sha256(args.unified)},
        },
        "methods": method_summaries,
        "normalized_unique_sql": {
            "normalization": "unified evaluator comment/fence removal followed by SHA-256; no SQL text emitted",
            "questions_with_any_duplicate_slot": sum(row["duplicate_slots"] > 0 for row in unique_rows),
            "mean_unique_sql_per_question": statistics.fmean(row["unique_normalized_sql"] for row in unique_rows),
            "minimum_unique_sql_per_question": min(row["unique_normalized_sql"] for row in unique_rows),
            "maximum_unique_sql_per_question": max(row["unique_normalized_sql"] for row in unique_rows),
            "methods": {
                method: {
                    "questions_with_duplicate_top_slots": sum(row[f"{method}_duplicate_top_slots"] > 0 for row in unique_rows),
                    "mean_unique_top_sql": statistics.fmean(row[f"{method}_unique_top_sql"] for row in unique_rows),
                    "mean_top_slots": statistics.fmean(row[f"{method}_top_slots"] for row in unique_rows),
                }
                for method in METHODS
            },
        },
        "descriptive_tie_size_aurc": {
            "definition": "right-step area under selective risk versus coverage across maximum top-tie-size thresholds 1..8",
            **risk_areas,
        },
    }
    (args.output / "order_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    strict_rows = {
        row["method"]: row for row in risk_rows if row["maximum_top_tie_size"] == 1
    }
    report_lines = [
        "# Unified-Evaluator Candidate-Order Audit",
        "",
        "This is a post-review descriptive diagnostic. It does not define a preferred policy or a confirmatory comparison.",
        "",
        f"- Questions: {len(qids)}; fixed slots per question: 8.",
        f"- Exact global candidate orders enumerated: {permutation_count:,}.",
        f"- C000 under the unified evaluator: {c000_count}/180.",
        "",
        "| Selector | Original | Reverse | Exact min | Median | Mean | Exact max | Top ties |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method in METHODS:
        result = method_summaries[method]
        report_lines.append(
            f"| {method} | {result['original_order_correct']}/180 | {result['reverse_order_correct']}/180 | "
            f"{result['minimum_correct']}/180 | {result['median_correct']:.1f}/180 | "
            f"{result['mean_correct']:.3f}/180 | {result['maximum_correct']}/180 | "
            f"{result['top_tie_questions']}/180 |"
        )
    report_lines.extend(
        [
            "",
            "## Strict no-tie abstention diagnostic",
            "",
            "| Selector | Covered | Correct when covered | Covered accuracy | Overall correct yield |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for method in METHODS:
        row = strict_rows[method]
        report_lines.append(
            f"| {method} | {row['covered_questions']}/180 | {row['correct_covered']} | "
            f"{float(row['covered_accuracy']):.4f} | {float(row['overall_correct_yield']):.4f} |"
        )
    report_lines.extend(
        [
            "",
            "The permutation range measures how much the frozen evidence leaves to the arbitrary final tie breaker. "
            "The risk--coverage table is outcome-aware and descriptive; it requires independent calibration and evaluation before operational use.",
            "",
            "## Normalized unique-SQL audit",
            "",
            f"- Questions with at least one duplicate normalized SQL slot: {summary['normalized_unique_sql']['questions_with_any_duplicate_slot']}/180.",
            f"- Mean unique SQL strings per eight-slot pool: {summary['normalized_unique_sql']['mean_unique_sql_per_question']:.3f}.",
            f"- Descriptive right-step tie-size AURC: validation {risk_areas['validation_only']:.4f}; complete witness {risk_areas['complete_witness']:.4f}.",
            "- Deduplication changes the reported tie multiplicity when duplicate slots share one normalized SQL; it does not create a deployable tie rule. No SQL text is emitted.",
            "",
        ]
    )
    (args.output / "ORDER_SENSITIVITY_REPORT.md").write_text("\n".join(report_lines), encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
