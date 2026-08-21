"""Development-only registered grid selection for the v0.3 C2GES component."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

from rouge_score import rouge_scorer

from build_full_pdf_dataset import sha256
from v03_methods import RedundancyCache, build_graph_v03, constrained_select, redundancy, score_channels


def candidates() -> list[dict]:
    rows = []
    for relevance, role, graph, counterfactual in itertools.product(
        (0.30, 0.40), (0.15, 0.20), (0.15, 0.20), (0.15, 0.25)
    ):
        position = round(1.0 - relevance - role - graph - counterfactual, 12)
        if not 0.05 <= position <= 0.20:
            continue
        for redundancy_penalty, max_distance, path_max_edges in itertools.product(
            (0.20, 0.35, 0.50), (8, 12), (3, 4)
        ):
            rows.append(
                {
                    "weights": {
                        "relevance": relevance,
                        "role": role,
                        "graph": graph,
                        "counterfactual": counterfactual,
                        "position": position,
                    },
                    "redundancy_penalty": redundancy_penalty,
                    "max_distance": max_distance,
                    "path_min_edges": 2,
                    "path_max_edges": path_max_edges,
                }
            )
    rows.sort(key=lambda item: json.dumps(item, sort_keys=True))
    return rows


def run(dev_path: Path, output: Path) -> dict:
    if output.exists():
        raise FileExistsError(f"Refusing existing output directory: {output}")
    output.mkdir(parents=True)
    state_path = output / "run_state.json"
    state_path.write_text(
        json.dumps({"status": "RUNNING", "started_utc": datetime.now(timezone.utc).isoformat()}, indent=2) + "\n",
        encoding="utf-8",
    )
    rows = [json.loads(line) for line in dev_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 12 or any(row.get("split") != "dev" for row in rows):
        raise RuntimeError("development selection requires the physically dev-only 12-report file")
    scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)
    grid = candidates()
    graph_cache = {}
    channel_cache = {}
    redundancy_caches = {}
    for row in rows:
        for max_distance in sorted({item["max_distance"] for item in grid}):
            graph = build_graph_v03(row["candidate_sentences"], max_distance=max_distance)
            graph_cache[(row["doc_id"], max_distance)] = graph
            redundancy_caches[(row["doc_id"], max_distance)] = RedundancyCache(graph.nodes)
            for path_max_edges in sorted({item["path_max_edges"] for item in grid}):
                channel_cache[(row["doc_id"], max_distance, path_max_edges)] = score_channels(
                    graph, path_max_edges=path_max_edges
                )

    ledger = []
    for index, config in enumerate(grid):
        full_rl, full_r1, no_cf_rl, redundancies, nonidentity = [], [], [], [], []
        for row in rows:
            graph = graph_cache[(row["doc_id"], config["max_distance"])]
            channels = channel_cache[(row["doc_id"], config["max_distance"], config["path_max_edges"])]
            similarity = redundancy_caches[(row["doc_id"], config["max_distance"])]
            full, _ = constrained_select(
                graph,
                channels,
                config["weights"],
                budget=5,
                redundancy_penalty=config["redundancy_penalty"],
                redundancy_cache=similarity,
            )
            no_cf, _ = constrained_select(
                graph,
                channels,
                config["weights"],
                budget=5,
                redundancy_penalty=config["redundancy_penalty"],
                remove_cf_only=True,
                redundancy_cache=similarity,
            )
            full_metrics = scorer.score(row["reference_summary"], " ".join(node.text for node in full))
            no_cf_metrics = scorer.score(row["reference_summary"], " ".join(node.text for node in no_cf))
            full_rl.append(float(full_metrics["rougeL"].fmeasure))
            full_r1.append(float(full_metrics["rouge1"].fmeasure))
            no_cf_rl.append(float(no_cf_metrics["rougeL"].fmeasure))
            redundancies.append(redundancy(full))
            nonidentity.append(
                max(abs(channels["graph"][sid] - channels["counterfactual"][sid]) for sid in channels["graph"])
            )
        record = {
            "grid_index": index,
            **config,
            "dev_n_reports": len(rows),
            "objective_mean_rougeL_k5": statistics.fmean(full_rl),
            "tie_mean_rouge1_k5": statistics.fmean(full_r1),
            "tie_negative_redundancy_k5": -statistics.fmean(redundancies),
            "dev_full_minus_no_cf_rougeL_k5": statistics.fmean(a - b for a, b in zip(full_rl, no_cf_rl)),
            "min_report_max_abs_cf_minus_graph": min(nonidentity),
        }
        ledger.append(record)
        if (index + 1) % 12 == 0 or index + 1 == len(grid):
            state_path.write_text(
                json.dumps(
                    {
                        "status": "RUNNING",
                        "completed_grid_records": index + 1,
                        "total_grid_records": len(grid),
                        "test_input_accessed": False,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    # Registered order: primary mean R-L, then R-1, then lower redundancy,
    # then the lexicographically earliest fully specified candidate.
    selected = max(
        ledger,
        key=lambda item: (
            item["objective_mean_rougeL_k5"],
            item["tie_mean_rouge1_k5"],
            item["tie_negative_redundancy_k5"],
            -item["grid_index"],
        ),
    )
    with (output / "dev_search_ledger.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for record in ledger:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    decision = {
        "protocol": "C2GES-NERC-v0.3-dev-selection-v1",
        "evaluation_status": "development_only_for_post_audit_corrective_evaluation",
        "dev_input": str(dev_path),
        "dev_input_sha256": sha256(dev_path),
        "test_input_accessed": False,
        "candidate_count": len(grid),
        "selection_objective": [
            "maximize mean ROUGE-L F1 at K=5 on 12 dev reports",
            "tie: maximize mean ROUGE-1 F1",
            "tie: minimize mean redundancy",
            "tie: earliest lexicographic grid record",
        ],
        "selected": selected,
        "cf_development_gate": {
            "signal_nonidentity_required": True,
            "min_report_max_abs_cf_minus_graph": selected["min_report_max_abs_cf_minus_graph"],
            "full_minus_no_cf_rougeL_k5": selected["dev_full_minus_no_cf_rougeL_k5"],
            "note": "A positive dev difference is not test evidence and is not guaranteed by selection eligibility.",
        },
        "script_sha256": sha256(Path(__file__)),
    }
    decision_path = output / "DEV_SELECTION_DECISION.json"
    decision_path.write_text(json.dumps(decision, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state_path.write_text(
        json.dumps(
            {
                "status": "COMPLETE",
                "completed_grid_records": len(grid),
                "total_grid_records": len(grid),
                "test_input_accessed": False,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return decision


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.dev.resolve(), args.output.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
