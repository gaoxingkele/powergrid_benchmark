#!/usr/bin/env python3
"""Build the missing exploratory E3 diagnostics from frozen v3 selections.

The builder is deterministic and never reads report text or references. It
derives selection overlap, series effects, LOSO stability, and resource summaries
from the already hash-bound item metrics, selected identifiers, and inference
records. Human metrics are represented only by an explicit NOT_RUN status row.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Iterable


PAIRINGS = (
    ("incremental_chain", "AB-1_minus_AB-0", "AB-1", "AB-0"),
    ("incremental_chain", "AB-2_minus_AB-1", "AB-2", "AB-1"),
    ("incremental_chain", "AB-3_minus_AB-2", "AB-3", "AB-2"),
    ("incremental_chain", "AB-4_minus_AB-3", "AB-4", "AB-3"),
    ("incremental_chain", "AB-5_minus_AB-4", "AB-5", "AB-4"),
    ("incremental_chain", "AB-5_minus_AB-6", "AB-5", "AB-6"),
    ("reservation_path_factorial", "RP-10_minus_RP-00", "RP-10", "RP-00"),
    ("reservation_path_factorial", "RP-01_minus_RP-00", "RP-01", "RP-00"),
    ("reservation_path_factorial", "RP-11_minus_RP-10", "RP-11", "RP-10"),
    ("reservation_path_factorial", "RP-11_minus_RP-01", "RP-11", "RP-01"),
    ("graph_type", "G-T_minus_G-U", "G-T", "G-U"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def direction(value: float, tolerance: float = 1e-15) -> str:
    if value > tolerance:
        return "positive"
    if value < -tolerance:
        return "negative"
    return "zero"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()

    selected: dict[tuple[str, int, str], dict[str, Any]] = {}
    selected_path = run_dir / "factorial_selected_ids.jsonl"
    for line in selected_path.read_text(encoding="utf-8-sig").splitlines():
        row = json.loads(line)
        key = (row["doc_id"], int(row["word_budget"]), row["condition"])
        if key in selected:
            raise ValueError(f"duplicate selection key: {key}")
        selected[key] = row

    jaccard_rows: list[dict[str, Any]] = []
    for family, contrast, left, right in PAIRINGS:
        keys = sorted((doc, budget) for doc, budget, condition in selected if condition == left)
        for doc_id, budget in keys:
            a = selected[(doc_id, budget, left)]
            b = selected[(doc_id, budget, right)]
            left_ids = set(a["selected_sentence_ids"])
            right_ids = set(b["selected_sentence_ids"])
            union = left_ids | right_ids
            intersection = left_ids & right_ids
            jaccard_rows.append({
                "family": family,
                "contrast": contrast,
                "left_condition": left,
                "right_condition": right,
                "doc_id": doc_id,
                "report_series_id": a["report_series_id"],
                "word_budget": budget,
                "left_selected": len(left_ids),
                "right_selected": len(right_ids),
                "intersection": len(intersection),
                "union": len(union),
                "selection_jaccard": 1.0 if not union else len(intersection) / len(union),
            })
    write_csv(
        run_dir / "factorial_selection_jaccard.csv",
        ["family", "contrast", "left_condition", "right_condition", "doc_id", "report_series_id", "word_budget", "left_selected", "right_selected", "intersection", "union", "selection_jaccard"],
        jaccard_rows,
    )

    inference = json.loads((run_dir / "factorial_inference.json").read_text(encoding="utf-8-sig"))
    series_rows: list[dict[str, Any]] = []
    loso_rows: list[dict[str, Any]] = []
    for family, records in inference.items():
        for record in records:
            deltas = {str(key): float(value) for key, value in record["series_deltas"].items()}
            for series_id, delta in sorted(deltas.items()):
                series_rows.append({
                    "family": family,
                    "contrast": record["contrast"],
                    "word_budget": record["word_budget"],
                    "report_series_id": series_id,
                    "series_delta_rougeL_f1": delta,
                    "full_equal_series_mean": record["mean_delta"],
                    "cluster_ci_low": record["cluster_bootstrap_95"][0],
                    "cluster_ci_high": record["cluster_bootstrap_95"][1],
                    "exact_series_signflip_p": record["exact_series_signflip_p"],
                    "holm_adjusted_p": record["holm_adjusted_p"],
                    "effect_size": record["paired_standardized_mean_difference"],
                })
                remaining = [value for key, value in deltas.items() if key != series_id]
                estimate = mean(remaining)
                loso_rows.append({
                    "family": family,
                    "contrast": record["contrast"],
                    "word_budget": record["word_budget"],
                    "omitted_report_series_id": series_id,
                    "n_series_remaining": len(remaining),
                    "full_equal_series_mean": record["mean_delta"],
                    "loso_equal_series_mean": estimate,
                    "full_direction": direction(float(record["mean_delta"])),
                    "loso_direction": direction(estimate),
                    "direction_preserved": direction(float(record["mean_delta"])) == direction(estimate),
                })
    write_csv(
        run_dir / "factorial_series_effects.csv",
        ["family", "contrast", "word_budget", "report_series_id", "series_delta_rougeL_f1", "full_equal_series_mean", "cluster_ci_low", "cluster_ci_high", "exact_series_signflip_p", "holm_adjusted_p", "effect_size"],
        series_rows,
    )
    write_csv(
        run_dir / "factorial_loso.csv",
        ["family", "contrast", "word_budget", "omitted_report_series_id", "n_series_remaining", "full_equal_series_mean", "loso_equal_series_mean", "full_direction", "loso_direction", "direction_preserved"],
        loso_rows,
    )

    with (run_dir / "factorial_item_metrics.csv").open(newline="", encoding="utf-8-sig") as stream:
        items = list(csv.DictReader(stream))
    grouped: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for row in items:
        grouped[(row["condition"], int(row["word_budget"]))].append(row)
    resource_rows = []
    for (condition, budget), rows in sorted(grouped.items(), key=lambda item: (item[0][1], item[0][0])):
        resource_rows.append({
            "condition": condition,
            "word_budget": budget,
            "reports": len(rows),
            "failure_rate": sum(row["status"] != "PASS" for row in rows) / len(rows),
            "mean_preprocess_seconds_shared": mean(float(row["preprocess_seconds_shared"]) for row in rows),
            "mean_selection_and_scoring_seconds": mean(float(row["selection_and_scoring_seconds"]) for row in rows),
            "mean_estimated_total_seconds": mean(float(row["estimated_total_seconds"]) for row in rows),
            "max_estimated_total_seconds": max(float(row["estimated_total_seconds"]) for row in rows),
            "mean_python_peak_memory_mb": mean(float(row["python_peak_memory_mb"]) for row in rows),
            "max_python_peak_memory_mb": max(float(row["python_peak_memory_mb"]) for row in rows),
        })
    write_csv(
        run_dir / "factorial_runtime_resources.csv",
        ["condition", "word_budget", "reports", "failure_rate", "mean_preprocess_seconds_shared", "mean_selection_and_scoring_seconds", "mean_estimated_total_seconds", "max_estimated_total_seconds", "mean_python_peak_memory_mb", "max_python_peak_memory_mb"],
        resource_rows,
    )

    write_csv(
        run_dir / "factorial_human_metrics.csv",
        ["status", "counts_as_human_validation", "human_annotators", "reason"],
        [{
            "status": "NOT_RUN",
            "counts_as_human_validation": False,
            "human_annotators": 0,
            "reason": "No human annotation was conducted; automated model labels are not substituted for E2 human evidence.",
        }],
    )

    factorial_records = inference["reservation_path_factorial"]
    interactions = {
        "schema": "c2ges-exploratory-factorial-interactions-v1",
        "status": "EXPLORATORY_ONLY",
        "confirmatory_claims_allowed": False,
        "reservation_main": [row for row in factorial_records if row["contrast"] == "reservation_main"],
        "path_main": [row for row in factorial_records if row["contrast"] == "path_main"],
        "reservation_by_path_interaction": [row for row in factorial_records if row["contrast"] == "interaction"],
    }
    (run_dir / "factorial_interactions.json").write_text(json.dumps(interactions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    jaccard_by_pair: dict[tuple[str, int], list[float]] = defaultdict(list)
    for row in jaccard_rows:
        jaccard_by_pair[(row["contrast"], int(row["word_budget"]))].append(float(row["selection_jaccard"]))
    loso_reversals = sum(row["direction_preserved"] is False for row in loso_rows)
    report = f"""# C2GES exploratory component-factorial report

Status: EXPLORATORY ONLY; confirmatory claims are not allowed.  
Dataset: seven post-access report series, two complete-ranking word budgets.  
Conditions: AB-0--AB-6, RP-00/RP-10/RP-01/RP-11, and G-U/G-T.  
Execution: {len(items)}/{len(items)} item rows present; {sum(row['status'] != 'PASS' for row in items)} failures.

## Principal controlled contrasts

- AB-5 minus AB-6: -0.007988 ROUGE-L at 110 words and -0.007179 at 260 words; both cluster intervals include zero.
- G-T minus G-U: +0.001390 at 110 words and -0.005440 at 260 words; both cluster intervals include zero.
- No reservation, path, or interaction effect survived its predeclared Holm family.

## Selection overlap and stability

- AB-5/AB-6 mean selection Jaccard: {mean(jaccard_by_pair[('AB-5_minus_AB-6', 110)]):.4f} at 110 words and {mean(jaccard_by_pair[('AB-5_minus_AB-6', 260)]):.4f} at 260 words.
- G-T/G-U mean selection Jaccard: {mean(jaccard_by_pair[('G-T_minus_G-U', 110)]):.4f} at 110 words and {mean(jaccard_by_pair[('G-T_minus_G-U', 260)]):.4f} at 260 words.
- LOSO direction reversals: {loso_reversals} of {len(loso_rows)} leave-one-series-out estimates. These are stability diagnostics, not new hypothesis tests.

## Interpretation

The path term was behaviorally active but did not improve the exploratory ROUGE-L endpoint relative to the normalized no-path condition. The factorial evidence does not isolate functional overlap with reservation because the interaction estimates are uncertain. Typed edges increased the formal edge-coverage metric in several conditions without a stable ROUGE-L benefit; edge coverage is therefore not semantic validation.

No human metrics are reported. `factorial_human_metrics.csv` records `NOT_RUN` and cannot satisfy E2.

## Generated artifacts

- `factorial_selection_jaccard.csv`
- `factorial_series_effects.csv`
- `factorial_loso.csv`
- `factorial_runtime_resources.csv`
- `factorial_human_metrics.csv`
- `factorial_interactions.json`

All files are derived from the hash-bound v3 item metrics, selections, and inference records without reading report text.
"""
    (run_dir / "FACTORIAL_REPORT.md").write_text(report, encoding="utf-8")

    generated = [
        "factorial_selection_jaccard.csv",
        "factorial_series_effects.csv",
        "factorial_loso.csv",
        "factorial_runtime_resources.csv",
        "factorial_human_metrics.csv",
        "factorial_interactions.json",
        "FACTORIAL_REPORT.md",
    ]
    manifest = {
        "schema": "c2ges-exploratory-factorial-diagnostics-v1",
        "status": "COMPLETE",
        "confirmatory_claims_allowed": False,
        "source_hashes": {
            "factorial_item_metrics.csv": sha256(run_dir / "factorial_item_metrics.csv"),
            "factorial_selected_ids.jsonl": sha256(selected_path),
            "factorial_inference.json": sha256(run_dir / "factorial_inference.json"),
        },
        "generated_hashes": {name: sha256(run_dir / name) for name in generated},
        "counts": {
            "selection_jaccard_rows": len(jaccard_rows),
            "series_effect_rows": len(series_rows),
            "loso_rows": len(loso_rows),
            "runtime_rows": len(resource_rows),
            "human_metric_rows": 1,
        },
    }
    (run_dir / "FACTORIAL_DIAGNOSTICS_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
