#!/usr/bin/env python3
"""Run an explicitly exploratory E1 comparison on already-accessed reports."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import statistics
import time
from pathlib import Path
from typing import Any

import numpy as np
from rouge_score import rouge_scorer

from experiment import CONDITIONS, contrast_summary, holm, sha256, word_count
from external_confirmatory import (
    METHODS,
    load_embeddings,
    selection_metrics,
    system_select,
)
from v031_methods import RedundancyCache, build_graph_v03, score_channels


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(value for value in root.rglob("*") if value.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(bytes.fromhex(sha256(path)))
    return digest.hexdigest().upper()


def paired(rows: list[dict[str, Any]], budget: int, left: str, right: str) -> dict[str, float]:
    values = {(row["report_series_id"], row["method"]): float(row["rougeL_f1"])
              for row in rows if int(row["word_budget"]) == budget and row["method"] in {left, right}}
    series = sorted({key[0] for key in values})
    return {series_id: values[(series_id, left)] - values[(series_id, right)] for series_id in series}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.out_dir.exists():
        raise FileExistsError(f"refusing existing output directory: {args.out_dir}")
    args.out_dir.mkdir(parents=True)
    reports = load_jsonl(args.dataset)
    if len(reports) != 7 or any(row.get("split") != "exploratory_external" or row.get("synthetic") is not False
                                or row.get("confirmatory_claims_allowed") is not False for row in reports):
        raise RuntimeError("this runner accepts only the seven-row exploratory external corpus")
    config = {
        "base_positive_weights": {"relevance": 0.4, "role": 0.2, "graph": 0.15, "path": 0.15, "position": 0.1},
        "redundancy_penalty": 0.5,
        "semantic_mmr_lambda": 0.9,
        "textrank_alpha": 0.65,
        "pacsum": {"lambda_preceding": -1.0, "lambda_following": 1.0, "beta": 0.3},
    }
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    metrics: list[dict[str, Any]] = []
    selected_ids: list[dict[str, Any]] = []
    embedding_diagnostics: list[dict[str, Any]] = []
    for index, report in enumerate(reports, 1):
        print(f"[{index}/{len(reports)}] {report['doc_id']}")
        graph = build_graph_v03(report["candidate_sentences"], max_distance=12)
        channels0 = score_channels(graph, path_min_edges=2, path_max_edges=4, path_max_paths=250000, path_max_expansions=2000000)
        channels = {"relevance": channels0["relevance"], "role": channels0["role"], "graph": channels0["graph"],
                    "path": channels0["counterfactual"], "position": channels0["position"]}
        nodes = list(graph.nodes)
        embeddings, diagnostic = load_embeddings([node.text for node in nodes], args.model_snapshot, "chunk_mean_254")
        embedding_diagnostics.append({"doc_id": report["doc_id"], **diagnostic})
        cache = RedundancyCache(graph.nodes)
        page_by_sid = {str(row["sid"]): int(row["page"]) for row in report["candidate_sentences"]}
        for budget in (110, 260):
            for method in METHODS:
                started = time.perf_counter()
                selected, order = system_select(method, graph, channels, embeddings, config, budget)
                prediction = " ".join(node.text for node in selected)
                scores = scorer.score(report["reference_summary"], prediction)
                metrics.append({
                    "doc_id": report["doc_id"], "report_series_id": report["report_series_id"],
                    "word_budget": budget, "method": method, "status": "PASS",
                    "rouge1_f1": scores["rouge1"].fmeasure, "rouge2_f1": scores["rouge2"].fmeasure,
                    "rougeL_f1": scores["rougeL"].fmeasure, **selection_metrics(graph, selected, cache, budget),
                    "selection_scoring_seconds": time.perf_counter() - started,
                })
                selected_ids.append({
                    "doc_id": report["doc_id"], "report_series_id": report["report_series_id"],
                    "word_budget": budget, "method": method, "selection_order": order,
                    "selected_source_order": [node.sid for node in selected],
                    "selected_pages": [page_by_sid[node.sid] for node in selected],
                })
    write_csv(args.out_dir / "external_item_metrics.csv", metrics)
    aggregates: list[dict[str, Any]] = []
    for budget in (110, 260):
        for method in METHODS:
            subset = [row for row in metrics if row["word_budget"] == budget and row["method"] == method]
            aggregates.append({"word_budget": budget, "method": method, "reports": len(subset),
                               **{name: statistics.fmean(float(row[name]) for row in subset)
                                  for name in ("rouge1_f1", "rouge2_f1", "rougeL_f1", "redundancy", "role_coverage",
                                               "typed_edge_coverage", "actual_words", "budget_utilization", "selection_scoring_seconds")}})
    write_csv(args.out_dir / "external_aggregate_metrics.csv", aggregates)
    system_family: list[dict[str, Any]] = []
    path_family: list[dict[str, Any]] = []
    for budget in (110, 260):
        for offset, baseline in enumerate(("Semantic-MMR", "TextRank", "PacSum-MiniLM")):
            system_family.append({"word_budget": budget, "contrast": f"C2GES-NO-PATH_minus_{baseline}",
                                  **contrast_summary(paired(metrics, budget, "C2GES-NO-PATH", baseline), samples=10000,
                                                     seed=20260910 + budget * 100 + offset)})
        path_family.append({"word_budget": budget, "contrast": "C2GES-FULL_minus_C2GES-NO-PATH",
                            **contrast_summary(paired(metrics, budget, "C2GES-FULL", "C2GES-NO-PATH"), samples=10000,
                                               seed=20260910 + budget * 100 + 50)})
    holm(system_family); holm(path_family)
    inference = {"system_comparison_family": system_family, "path_mechanism_family": path_family}
    (args.out_dir / "external_series_cluster_results.json").write_text(json.dumps(inference, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    loso: list[dict[str, Any]] = []
    for record in system_family + path_family:
        deltas = record["series_deltas"]
        for omitted in sorted(deltas):
            kept = [float(value) for key, value in deltas.items() if key != omitted]
            loso.append({"word_budget": record["word_budget"], "contrast": record["contrast"],
                         "omitted_series": omitted, "remaining_mean_delta": statistics.fmean(kept)})
    write_csv(args.out_dir / "external_loso.csv", loso)
    with (args.out_dir / "selected_page_locator.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for row in selected_ids:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    (args.out_dir / "embedding_diagnostics.json").write_text(json.dumps(embedding_diagnostics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "schema": "c2ges-exploratory-system-comparison-v0", "status": "COMPLETE",
        "mode": "EXPLORATORY_EXTERNAL_NONCONFIRMATORY", "external_test_accessed": True,
        "confirmatory_claims_allowed": False, "reference_human_adjudicated": False,
        "reports": len(reports), "series": len({row["report_series_id"] for row in reports}),
        "methods": list(METHODS), "word_budgets": [110, 260], "failed_rows": 0,
        "fixed_untuned_parameters": config, "dataset_sha256": sha256(args.dataset),
        "runner_sha256": sha256(Path(__file__)), "model_revision": args.model_snapshot.name,
        "model_tree_sha256": tree_hash(args.model_snapshot), "python": platform.python_version(),
    }
    for name in ("external_item_metrics.csv", "external_aggregate_metrics.csv", "external_series_cluster_results.json",
                 "external_loso.csv", "selected_page_locator.jsonl", "embedding_diagnostics.json"):
        manifest.setdefault("artifacts", {})[name] = sha256(args.out_dir / name)
    (args.out_dir / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
