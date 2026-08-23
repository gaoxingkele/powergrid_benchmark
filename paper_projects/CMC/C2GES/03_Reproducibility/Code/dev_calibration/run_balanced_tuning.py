#!/usr/bin/env python3
"""Equal nine-configuration development sweep for three tunable C2GES methods."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import sys
from pathlib import Path
from typing import Any

from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
R2 = PROJECT / "03_Reproducibility" / "Code" / "core" / "R2_v0_3"
CORE = R2.parent
sys.path.insert(0, str(R2))
sys.path.insert(0, str(CORE))
import run_formal_experiment as baselines  # noqa: E402
from run_test_v0_3_1 import semantic_embeddings, semantic_mmr_select  # noqa: E402
from v031_methods import build_graph_v03, constrained_select, redundancy, score_channels  # noqa: E402


DEFAULT_OUTPUT = PROJECT / "03_Reproducibility" / "Data" / "dev_balanced_tuning" / "equal9_v1"
MMR_GRID = tuple(round(value / 10.0, 2) for value in range(1, 10))
TEXTRANK_GRID = tuple(round(0.55 + 0.05 * index, 2) for index in range(9))
PATH_GRID = tuple(round(0.025 * index, 3) for index in range(9))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
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


def c2_weights(path_weight: float) -> dict[str, float]:
    remaining = 1.0 - path_weight
    return {
        "relevance": (0.40 / 0.85) * remaining,
        "role": (0.20 / 0.85) * remaining,
        "graph": (0.15 / 0.85) * remaining,
        "counterfactual": path_weight,
        "position": (0.10 / 0.85) * remaining,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite output: {args.output}")
    rows = load_jsonl(args.dev)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if len(rows) != 12 or any(row.get("split") != "dev" for row in rows):
        raise AssertionError("Requires the physical 12-report development split")
    if not (len(MMR_GRID) == len(TEXTRANK_GRID) == len(PATH_GRID) == 9):
        raise AssertionError("All grids must contain exactly nine configurations")

    model = SentenceTransformer(str(args.model_snapshot), device="cpu", local_files_only=True)
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    item_rows: list[dict[str, Any]] = []

    for report in rows:
        graph = build_graph_v03(report["candidate_sentences"], max_distance=int(config["max_distance"]))
        channels = score_channels(
            graph,
            path_min_edges=int(config["path_min_edges"]),
            path_max_edges=int(config["path_max_edges"]),
            path_max_paths=int(config["path_max_paths"]),
            path_max_expansions=int(config["path_max_expansions"]),
        )
        embeddings = semantic_embeddings(graph.nodes, model)
        for method, grid in (
            ("semantic_mmr", MMR_GRID),
            ("textrank", TEXTRANK_GRID),
            ("c2ges_normalized_path", PATH_GRID),
        ):
            for grid_index, value in enumerate(grid):
                for budget in (5, 10):
                    if method == "semantic_mmr":
                        selected, _ = semantic_mmr_select(graph.nodes, embeddings, budget, float(value))
                    elif method == "textrank":
                        scores, _ = baselines.textrank_scores(
                            graph.nodes,
                            {"alpha": float(value), "max_iter": 100, "tolerance": 1e-8, "fallback": "weighted_degree"},
                        )
                        selected = baselines.top_k(graph.nodes, scores, budget)
                    else:
                        selected, _ = constrained_select(
                            graph,
                            channels,
                            c2_weights(float(value)),
                            budget=budget,
                            redundancy_penalty=0.5,
                            remove_cf_only=False,
                        )
                    prediction = " ".join(node.text for node in selected)
                    scores = scorer.score(report["reference_summary"], prediction)
                    item_rows.append(
                        {
                            "doc_id": report["doc_id"],
                            "report_series_id": report["report_series_id"],
                            "method": method,
                            "grid_index": grid_index,
                            "parameter_value": value,
                            "budget": budget,
                            "selected_sentence_ids": "|".join(node.sid for node in selected),
                            "rouge1_f1": float(scores["rouge1"].fmeasure),
                            "rouge2_f1": float(scores["rouge2"].fmeasure),
                            "rougeL_f1": float(scores["rougeL"].fmeasure),
                            "redundancy": redundancy(selected),
                        }
                    )
    if len(item_rows) != 12 * 3 * 9 * 2:
        raise AssertionError(f"Unexpected item row count: {len(item_rows)}")

    aggregate_rows: list[dict[str, Any]] = []
    selections: dict[str, dict[str, Any]] = {}
    for method in ("semantic_mmr", "textrank", "c2ges_normalized_path"):
        method_aggregates: list[dict[str, Any]] = []
        for grid_index in range(9):
            subset = [row for row in item_rows if row["method"] == method and row["grid_index"] == grid_index]
            record = {
                "method": method,
                "grid_index": grid_index,
                "parameter_value": subset[0]["parameter_value"],
                "evaluated_configurations_for_method": 9,
                "report_budget_cells": len(subset),
                "mean_rouge1_f1": statistics.fmean(row["rouge1_f1"] for row in subset),
                "mean_rouge2_f1": statistics.fmean(row["rouge2_f1"] for row in subset),
                "mean_rougeL_f1": statistics.fmean(row["rougeL_f1"] for row in subset),
                "mean_redundancy": statistics.fmean(row["redundancy"] for row in subset),
                "mean_rougeL_k5": statistics.fmean(row["rougeL_f1"] for row in subset if row["budget"] == 5),
                "mean_rougeL_k10": statistics.fmean(row["rougeL_f1"] for row in subset if row["budget"] == 10),
            }
            aggregate_rows.append(record)
            method_aggregates.append(record)
        winner = max(
            method_aggregates,
            key=lambda row: (
                row["mean_rougeL_f1"],
                row["mean_rouge1_f1"],
                -row["mean_redundancy"],
                -row["grid_index"],
            ),
        )
        selections[method] = winner

    args.output.mkdir(parents=True)
    write_csv(args.output / "balanced_tuning_item_metrics.csv", item_rows)
    write_csv(args.output / "balanced_tuning_aggregate.csv", aggregate_rows)
    decision = {
        "analysis_id": "C2GES-balanced-development-tuning-equal9-v1",
        "status": "development_only_future_external_configuration",
        "test_input_accessed": False,
        "configuration_budget_per_method": 9,
        "selection_objective": [
            "highest mean ROUGE-L across K5/K10 and 12 reports",
            "highest mean ROUGE-1",
            "lowest mean redundancy",
            "earliest grid index",
        ],
        "inputs": {"dev_sha256": sha256(args.dev), "config_sha256": sha256(args.config)},
        "model": {"revision": args.model_snapshot.name},
        "selected": selections,
        "authorization": "Selected configurations are for a future preregistered external-series study only; do not apply to the retained test.",
        "privacy": "No candidate, reference, or prediction text is written to outputs.",
    }
    (args.output / "BALANCED_TUNING_DECISION.json").write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Balanced development tuning (equal nine configurations)",
        "",
        "Status: development-only configuration selection for a future unseen-series experiment. The retained test was not an input and must not be re-evaluated with these choices.",
        "",
        "| Method | Selected parameter | Grid index | Mean ROUGE-L | K=5 | K=10 | Mean redundancy |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for method, row in selections.items():
        lines.append(
            f"| {method} | {row['parameter_value']} | {row['grid_index']} | {row['mean_rougeL_f1']:.5f} | "
            f"{row['mean_rougeL_k5']:.5f} | {row['mean_rougeL_k10']:.5f} | {row['mean_redundancy']:.5f} |"
        )
    lines.extend(["", "Each method received exactly nine configurations under one ordered objective. This closes the development-budget asymmetry for the planned future comparison, not for the historical retained-test result.", ""])
    (args.output / "BALANCED_TUNING_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": "PASS", "selected": {method: row["parameter_value"] for method, row in selections.items()}, "output": str(args.output)}))


if __name__ == "__main__":
    main()
