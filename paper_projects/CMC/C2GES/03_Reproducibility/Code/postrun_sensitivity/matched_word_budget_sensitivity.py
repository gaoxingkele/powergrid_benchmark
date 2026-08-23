#!/usr/bin/env python3
"""Re-budget frozen top-10 C2GES selections under development-chosen word caps."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from rouge_score import rouge_scorer


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_OUTPUT = PROJECT / "03_Reproducibility" / "Data" / "postrun_matched_word" / "unified_v1"
CONDITIONS = (
    "lead",
    "centroid",
    "textrank",
    "semantic_mmr",
    "role",
    "graph_no_cf_strict",
    "c2ges_full",
)
BASELINES = ("graph_no_cf_strict", "semantic_mmr", "textrank")
WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)
BOOTSTRAP_SAMPLES = 10_000
SEED_BASE = 20_260_823


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
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


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def derive_budgets(dev_rows: list[dict[str, Any]]) -> tuple[dict[int, list[int]], tuple[int, int]]:
    lengths: dict[int, list[int]] = {}
    budgets: list[int] = []
    for k in (5, 10):
        values = [sum(word_count(item["text"]) for item in row["candidate_sentences"][:k]) for row in dev_rows]
        lengths[k] = values
        budgets.append(int(round(statistics.median(values) / 10.0) * 10))
    return lengths, (budgets[0], budgets[1])


def ranking(row: dict[str, Any], positions: dict[str, int]) -> list[str]:
    selected = list(row["selected_sentence_ids"])
    condition = row["condition"]
    audit = row["selection_audit"]
    if condition == "lead":
        return sorted(selected, key=lambda sid: (positions[sid], sid))
    if condition in {"semantic_mmr", "graph_no_cf_strict", "c2ges_full"}:
        order = list(audit["selection_order"])
        if set(order) != set(selected) or len(order) != len(selected):
            raise AssertionError(f"{condition}: stored dynamic order does not match selected top 10")
        return order
    scores = audit["scores"]
    return sorted(selected, key=lambda sid: (-float(scores[sid]), positions[sid], sid))


def greedy_word_cap(order: list[str], text_by_sid: dict[str, str], budget: int) -> tuple[list[str], int]:
    selected: list[str] = []
    used = 0
    for sid in order:
        words = word_count(text_by_sid[sid])
        if used + words <= budget:
            selected.append(sid)
            used += words
    return selected, used


def exact_sign_flip(series_differences: list[float]) -> float:
    observed = abs(statistics.fmean(series_differences))
    extreme = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(series_differences)):
        total += 1
        statistic = abs(statistics.fmean(sign * value for sign, value in zip(signs, series_differences)))
        if statistic >= observed - 1e-15:
            extreme += 1
    return extreme / total


def holm(rows: list[dict[str, Any]]) -> None:
    order = sorted(range(len(rows)), key=lambda index: rows[index]["exact_series_signflip_p"])
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(rows) - rank) * rows[index]["exact_series_signflip_p"]))
        rows[index]["holm_adjusted_p_six"] = running


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite output: {args.output}")
    dev_rows = load_jsonl(args.dev)
    test_rows = load_jsonl(args.test)
    prediction_rows = load_jsonl(args.predictions)
    if len(dev_rows) != 12 or len(test_rows) != 15:
        raise AssertionError("Expected 12 development and 15 retained test reports")
    if any(row.get("split") != "dev" for row in dev_rows) or any(row.get("split") != "test" for row in test_rows):
        raise AssertionError("Physical split labels do not match")

    dev_lengths, budgets = derive_budgets(dev_rows)
    if budgets != (110, 260):
        raise AssertionError(f"Development budget rule changed: {budgets}")

    top10 = {
        (row["doc_id"], row["condition"]): row
        for row in prediction_rows
        if int(row["budget"]) == 10
    }
    if len(top10) != 15 * len(CONDITIONS):
        raise AssertionError(f"Expected 105 frozen top-10 rows, found {len(top10)}")

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    result_rows: list[dict[str, Any]] = []
    series_by_doc: dict[str, str] = {}
    for report in test_rows:
        doc_id = report["doc_id"]
        series_by_doc[doc_id] = report["report_series_id"]
        text_by_sid = {item["sid"]: item["text"] for item in report["candidate_sentences"]}
        positions = {item["sid"]: index for index, item in enumerate(report["candidate_sentences"])}
        for condition in CONDITIONS:
            frozen = top10[(doc_id, condition)]
            order = ranking(frozen, positions)
            for budget in budgets:
                selected, used = greedy_word_cap(order, text_by_sid, budget)
                document_order = sorted(selected, key=lambda sid: (positions[sid], sid))
                prediction = " ".join(text_by_sid[sid] for sid in document_order)
                scores = scorer.score(report["reference_summary"], prediction)
                result_rows.append(
                    {
                        "doc_id": doc_id,
                        "report_series_id": report["report_series_id"],
                        "condition": condition,
                        "word_budget": budget,
                        "selected_sentence_count": len(selected),
                        "used_words": used,
                        "unused_words": budget - used,
                        "selected_sentence_ids": "|".join(document_order),
                        "rouge1_f1": float(scores["rouge1"].fmeasure),
                        "rouge2_f1": float(scores["rouge2"].fmeasure),
                        "rougeL_f1": float(scores["rougeL"].fmeasure),
                    }
                )
    if len(result_rows) != 210 or any(row["used_words"] > row["word_budget"] for row in result_rows):
        raise AssertionError("Matched-word result cardinality or budget compliance failed")

    metric = {(row["doc_id"], row["condition"], row["word_budget"]): row["rougeL_f1"] for row in result_rows}
    series_ids = sorted(set(series_by_doc.values()))
    if len(series_ids) != 10:
        raise AssertionError(f"Expected 10 series, found {len(series_ids)}")
    reports_by_series: dict[str, list[str]] = defaultdict(list)
    for doc_id, series_id in series_by_doc.items():
        reports_by_series[series_id].append(doc_id)

    contrast_rows: list[dict[str, Any]] = []
    for budget in budgets:
        for contrast_index, baseline in enumerate(BASELINES):
            report_differences = {
                doc_id: metric[(doc_id, "c2ges_full", budget)] - metric[(doc_id, baseline, budget)]
                for doc_id in series_by_doc
            }
            series_differences = [
                statistics.fmean(report_differences[doc_id] for doc_id in reports_by_series[series_id])
                for series_id in series_ids
            ]
            rng = random.Random(SEED_BASE + budget * 100 + contrast_index)
            bootstrap = [
                statistics.fmean(rng.choice(series_differences) for _ in series_differences)
                for _ in range(BOOTSTRAP_SAMPLES)
            ]
            contrast_rows.append(
                {
                    "word_budget": budget,
                    "contrast": f"c2ges_full_minus_{baseline}",
                    "n_reports": 15,
                    "n_series": 10,
                    "equal_series_mean_difference": statistics.fmean(series_differences),
                    "equal_report_mean_difference": statistics.fmean(report_differences.values()),
                    "cluster_bootstrap_95_low": percentile(bootstrap, 0.025),
                    "cluster_bootstrap_95_high": percentile(bootstrap, 0.975),
                    "exact_series_signflip_p": exact_sign_flip(series_differences),
                    "holm_adjusted_p_six": 0.0,
                    "bootstrap_samples": BOOTSTRAP_SAMPLES,
                    "bootstrap_seed": SEED_BASE + budget * 100 + contrast_index,
                }
            )
    holm(contrast_rows)

    aggregate_rows: list[dict[str, Any]] = []
    for budget in budgets:
        for condition in CONDITIONS:
            subset = [row for row in result_rows if row["word_budget"] == budget and row["condition"] == condition]
            aggregate_rows.append(
                {
                    "word_budget": budget,
                    "condition": condition,
                    "n_reports": len(subset),
                    "mean_used_words": statistics.fmean(row["used_words"] for row in subset),
                    "mean_selected_sentences": statistics.fmean(row["selected_sentence_count"] for row in subset),
                    "equal_report_mean_rougeL_f1": statistics.fmean(row["rougeL_f1"] for row in subset),
                    "reports_with_unused_capacity": sum(row["unused_words"] > 0 for row in subset),
                }
            )

    args.output.mkdir(parents=True)
    write_csv(args.output / "matched_word_item_metrics.csv", result_rows)
    write_csv(args.output / "matched_word_aggregate.csv", aggregate_rows)
    write_csv(args.output / "matched_word_contrasts.csv", contrast_rows)
    payload = {
        "analysis_id": "C2GES-postrun-matched-word-top10-v1",
        "status": "post_run_sensitivity_not_confirmatory",
        "budgets": list(budgets),
        "development_rule": {
            "first_5_word_totals": dev_lengths[5],
            "first_10_word_totals": dev_lengths[10],
            "median_first_5": statistics.median(dev_lengths[5]),
            "median_first_10": statistics.median(dev_lengths[10]),
            "rounding": "nearest 10 using Python half-to-even",
        },
        "inputs": {
            "dev_sha256": sha256(args.dev),
            "test_sha256": sha256(args.test),
            "formal_predictions_sha256": sha256(args.predictions),
        },
        "reports": 15,
        "series": 10,
        "result_rows": len(result_rows),
        "contrast_family": contrast_rows,
        "privacy": "No candidate, prediction, or reference text is written to public outputs.",
        "limitation": "Word caps are enforced only within each frozen top-10 ranking.",
    }
    (args.output / "matched_word_results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# C2GES matched-word-budget sensitivity",
        "",
        "Status: post-run sensitivity; the retained test outcomes were already visible. Budgets were mechanically derived from development candidate lengths, and no text was truncated after selection.",
        "",
        "| Budget | Contrast | Equal-series difference | Cluster-bootstrap 95% interval | Exact series p | Holm p |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for row in contrast_rows:
        lines.append(
            f"| {row['word_budget']} | {row['contrast']} | {row['equal_series_mean_difference']:+.4f} | "
            f"[{row['cluster_bootstrap_95_low']:+.4f}, {row['cluster_bootstrap_95_high']:+.4f}] | "
            f"{row['exact_series_signflip_p']:.6f} | {row['holm_adjusted_p_six']:.6f} |"
        )
    lines.extend(
        [
            "",
            "The audit constrains complete sentences within the frozen top-10 rankings. It does not search lower-ranked candidates, retune a method, or provide unseen-series confirmation.",
            "",
        ]
    )
    (args.output / "MATCHED_WORD_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": "PASS", "budgets": budgets, "output": str(args.output)}))


if __name__ == "__main__":
    main()
