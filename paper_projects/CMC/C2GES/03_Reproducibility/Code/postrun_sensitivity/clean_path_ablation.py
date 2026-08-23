#!/usr/bin/env python3
"""Scale-preserving normalized no-path ablation from frozen candidate base scores."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from rouge_score import rouge_scorer


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
R2 = PROJECT / "03_Reproducibility" / "Code" / "core" / "R2_v0_3"
sys.path.insert(0, str(R2))
from v03_methods import ROLE_GROUPS, RedundancyCache, build_graph_v03, redundancy  # noqa: E402

DEFAULT_OUTPUT = PROJECT / "03_Reproducibility" / "Data" / "postrun_clean_ablation" / "normalized_v1"
BOOTSTRAP_SAMPLES = 10_000
SEED_BASE = 20_260_823


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def select_with_base(graph: Any, base: dict[str, float], budget: int, penalty: float = 0.5) -> list[Any]:
    nodes = list(graph.nodes)
    by_sid = {node.sid: node for node in nodes}
    selected: list[str] = []
    cache = RedundancyCache(nodes)
    if budget >= len(ROLE_GROUPS):
        for roles in ROLE_GROUPS.values():
            eligible = [node for node in nodes if node.sid not in selected and node.dominant_role in roles]
            if eligible:
                winner = max(eligible, key=lambda node: (base[node.sid], -node.position, node.sid))
                selected.append(winner.sid)
    while len(selected) < min(budget, len(nodes)):
        eligible = [node for node in nodes if node.sid not in selected]
        winner = max(
            eligible,
            key=lambda node: (
                base[node.sid] - penalty * max((cache.get(node.sid, prior) for prior in selected), default=0.0),
                -node.position,
                node.sid,
            ),
        )
        selected.append(winner.sid)
    return sorted((by_sid[sid] for sid in selected), key=lambda node: node.position)


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def exact_sign_flip(values: list[float]) -> float:
    observed = abs(statistics.fmean(values))
    extreme = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(values)):
        total += 1
        statistic = abs(statistics.fmean(sign * value for sign, value in zip(signs, values)))
        if statistic >= observed - 1e-15:
            extreme += 1
    return extreme / total


def holm(rows: list[dict[str, Any]]) -> None:
    order = sorted(range(len(rows)), key=lambda index: rows[index]["exact_series_signflip_p"])
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(rows) - rank) * rows[index]["exact_series_signflip_p"]))
        rows[index]["holm_adjusted_p_two"] = running


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite output: {args.output}")
    test_rows = load_jsonl(args.test)
    prediction_rows = [
        row for row in load_jsonl(args.predictions)
        if row["condition"] in {"c2ges_full", "graph_no_cf_strict"}
    ]
    if len(test_rows) != 15 or len(prediction_rows) != 60:
        raise AssertionError("Expected 15 reports and 60 Full/strict formal rows")
    frozen = {(row["doc_id"], row["condition"], int(row["budget"])): row for row in prediction_rows}
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    results: list[dict[str, Any]] = []
    series_by_doc: dict[str, str] = {}

    for report in test_rows:
        doc_id = report["doc_id"]
        series_by_doc[doc_id] = report["report_series_id"]
        graph = build_graph_v03(report["candidate_sentences"], max_distance=12)
        for budget in (5, 10):
            full_row = frozen[(doc_id, "c2ges_full", budget)]
            strict_row = frozen[(doc_id, "graph_no_cf_strict", budget)]
            full_base = {sid: float(score) for sid, score in full_row["selection_audit"]["base_scores"].items()}
            strict_base = {sid: float(score) for sid, score in strict_row["selection_audit"]["base_scores"].items()}
            variants = {
                "full": (full_base, full_row),
                "historical_strict_no_path": (strict_base, strict_row),
                "normalized_no_path": ({sid: score / 0.85 for sid, score in strict_base.items()}, None),
            }
            selected_by_variant: dict[str, list[Any]] = {}
            for variant, (base, archived) in variants.items():
                selected = select_with_base(graph, base, budget, penalty=0.5)
                selected_by_variant[variant] = selected
                selected_ids = [node.sid for node in selected]
                if archived is not None and selected_ids != list(archived["selected_sentence_ids"]):
                    raise AssertionError(f"{doc_id}/K={budget}/{variant}: archived selection does not reproduce")
                prediction = " ".join(node.text for node in selected)
                scores = scorer.score(report["reference_summary"], prediction)
                results.append(
                    {
                        "doc_id": doc_id,
                        "report_series_id": report["report_series_id"],
                        "budget": budget,
                        "variant": variant,
                        "selected_sentence_ids": "|".join(selected_ids),
                        "rouge1_f1": float(scores["rouge1"].fmeasure),
                        "rouge2_f1": float(scores["rouge2"].fmeasure),
                        "rougeL_f1": float(scores["rougeL"].fmeasure),
                        "redundancy": redundancy(selected),
                    }
                )
            full_ids = {node.sid for node in selected_by_variant["full"]}
            strict_ids = {node.sid for node in selected_by_variant["historical_strict_no_path"]}
            normalized_ids = {node.sid for node in selected_by_variant["normalized_no_path"]}
            for row in results[-3:]:
                chosen = set(row["selected_sentence_ids"].split("|"))
                row["overlap_with_full"] = len(chosen & full_ids) / budget
                row["overlap_with_historical_strict"] = len(chosen & strict_ids) / budget
                row["normalized_vs_strict_changed"] = int(normalized_ids != strict_ids)

    if len(results) != 90:
        raise AssertionError(f"Expected 90 result rows, found {len(results)}")
    metric = {(row["doc_id"], row["variant"], row["budget"]): row["rougeL_f1"] for row in results}
    reports_by_series: dict[str, list[str]] = defaultdict(list)
    for doc_id, series_id in series_by_doc.items():
        reports_by_series[series_id].append(doc_id)
    series_ids = sorted(reports_by_series)
    contrasts: list[dict[str, Any]] = []
    for budget in (5, 10):
        report_differences = {
            doc_id: metric[(doc_id, "full", budget)] - metric[(doc_id, "normalized_no_path", budget)]
            for doc_id in series_by_doc
        }
        series_differences = [
            statistics.fmean(report_differences[doc_id] for doc_id in reports_by_series[series_id])
            for series_id in series_ids
        ]
        rng = random.Random(SEED_BASE + budget)
        bootstrap = [statistics.fmean(rng.choice(series_differences) for _ in series_differences) for _ in range(BOOTSTRAP_SAMPLES)]
        changed = sum(
            next(row for row in results if row["doc_id"] == doc_id and row["budget"] == budget and row["variant"] == "normalized_no_path")["overlap_with_full"] < 1.0
            for doc_id in series_by_doc
        )
        strict_changed = sum(
            next(row for row in results if row["doc_id"] == doc_id and row["budget"] == budget and row["variant"] == "normalized_no_path")["normalized_vs_strict_changed"]
            for doc_id in series_by_doc
        )
        contrasts.append(
            {
                "budget": budget,
                "contrast": "full_minus_normalized_no_path",
                "full_vs_normalized_changed_reports": changed,
                "normalized_vs_historical_strict_changed_reports": strict_changed,
                "equal_series_mean_rougeL_difference": statistics.fmean(series_differences),
                "equal_report_mean_rougeL_difference": statistics.fmean(report_differences.values()),
                "cluster_bootstrap_95_low": percentile(bootstrap, 0.025),
                "cluster_bootstrap_95_high": percentile(bootstrap, 0.975),
                "exact_series_signflip_p": exact_sign_flip(series_differences),
                "holm_adjusted_p_two": 0.0,
                "bootstrap_samples": BOOTSTRAP_SAMPLES,
                "bootstrap_seed": SEED_BASE + budget,
            }
        )
    holm(contrasts)

    aggregate: list[dict[str, Any]] = []
    for budget in (5, 10):
        for variant in ("full", "historical_strict_no_path", "normalized_no_path"):
            subset = [row for row in results if row["budget"] == budget and row["variant"] == variant]
            aggregate.append(
                {
                    "budget": budget,
                    "variant": variant,
                    "mean_rouge1_f1": statistics.fmean(row["rouge1_f1"] for row in subset),
                    "mean_rouge2_f1": statistics.fmean(row["rouge2_f1"] for row in subset),
                    "mean_rougeL_f1": statistics.fmean(row["rougeL_f1"] for row in subset),
                    "mean_redundancy": statistics.fmean(row["redundancy"] for row in subset),
                }
            )

    args.output.mkdir(parents=True)
    write_csv(args.output / "clean_ablation_item_metrics.csv", results)
    write_csv(args.output / "clean_ablation_aggregate.csv", aggregate)
    write_csv(args.output / "clean_ablation_contrasts.csv", contrasts)
    summary = {
        "analysis_id": "C2GES-clean-normalized-path-ablation-v1",
        "status": "post_run_component_diagnostic_not_confirmatory",
        "weights": {
            "full": {"relevance": 0.4, "role": 0.2, "graph": 0.15, "counterfactual": 0.15, "position": 0.1},
            "normalized_no_path": {"relevance": 0.4/0.85, "role": 0.2/0.85, "graph": 0.15/0.85, "counterfactual": 0.0, "position": 0.1/0.85},
            "redundancy_penalty": 0.5,
        },
        "reports": 15,
        "series": 10,
        "archived_full_and_strict_selections_reproduced": True,
        "contrasts": contrasts,
        "privacy": "No candidate, reference, or prediction text is written to outputs.",
    }
    (args.output / "clean_ablation_results.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# C2GES clean normalized path ablation",
        "",
        "Status: post-run component diagnostic. Archived Full and historical strict selections were reproduced before the normalized variant was accepted.",
        "",
        "| K | Full - normalized no-path | Cluster-bootstrap 95% interval | Exact series p | Holm p | Full/normalized changed | Normalized/strict changed |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in contrasts:
        lines.append(
            f"| {row['budget']} | {row['equal_series_mean_rougeL_difference']:+.5f} | "
            f"[{row['cluster_bootstrap_95_low']:+.5f}, {row['cluster_bootstrap_95_high']:+.5f}] | "
            f"{row['exact_series_signflip_p']:.6f} | {row['holm_adjusted_p_two']:.6f} | "
            f"{row['full_vs_normalized_changed_reports']}/15 | {row['normalized_vs_historical_strict_changed_reports']}/15 |"
        )
    lines.extend(["", "The normalized contrast separates path removal from the historical positive-score scale change, but it remains a post-run same-corpus diagnostic.", ""])
    (args.output / "CLEAN_ABLATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(args.output), "contrasts": contrasts}))


if __name__ == "__main__":
    main()
