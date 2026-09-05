#!/usr/bin/env python3
"""Run the C2GES component factorial on development data as a non-confirmatory pilot.

The script implements the frozen AB/RP/G identities, complete-ranking word
budgets, series-level contrasts, cluster bootstrap intervals, exact sign flips,
Holm correction, effect sizes, and rights-safe selected-ID outputs.  It refuses
confirmatory mode; the external one-attempt runner will be a separate frozen
entry point after the external inventory and code revision are approved.
"""

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
import sys
import time
import tracemalloc
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from rouge_score import rouge_scorer


HERE = Path(__file__).resolve().parent


def find_project_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "C2GES_RELEASE_MARKER.json").is_file():
            return candidate
    raise RuntimeError("C2GES release marker not found")


def find_workspace_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("workspace root not found; set a portable dataset path before use")


PROJECT = find_project_root(HERE)
WORKSPACE = find_workspace_root(PROJECT)
CORE_ROOT = PROJECT / "03_Reproducibility/Code/core"
CORE = CORE_ROOT / "R2_v0_3"
for import_root in (CORE_ROOT, CORE):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

from c2ges_offline import CausalEdge, CausalEventGraph, _jaccard  # noqa: E402
from v031_methods import (  # noqa: E402
    RedundancyCache,
    build_graph_v03,
    score_channels,
)
from v03_methods import minmax  # noqa: E402


WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")
ROLE_GROUPS = {
    "cause_or_trigger": ("root_cause", "trigger_event"),
    "propagation_or_impact": ("propagation_or_response", "impact"),
    "mitigation": ("mitigation",),
}

CONDITIONS: dict[str, dict[str, Any]] = {
    "AB-0": {"components": ("relevance", "position"), "reservation": False, "graph": "none", "path": False, "redundancy": False},
    "AB-1": {"components": ("relevance", "role", "position"), "reservation": False, "graph": "none", "path": False, "redundancy": False},
    "AB-2": {"components": ("relevance", "role", "position"), "reservation": True, "graph": "none", "path": False, "redundancy": False},
    "AB-3": {"components": ("relevance", "role", "graph", "position"), "reservation": True, "graph": "typed", "path": False, "redundancy": False},
    "AB-4": {"components": ("relevance", "role", "graph", "path", "position"), "reservation": True, "graph": "typed", "path": True, "redundancy": False},
    "AB-5": {"components": ("relevance", "role", "graph", "path", "position"), "reservation": True, "graph": "typed", "path": True, "redundancy": True},
    "AB-6": {"components": ("relevance", "role", "graph", "position"), "reservation": True, "graph": "typed", "path": False, "redundancy": True},
    "RP-00": {"components": ("relevance", "role", "graph", "position"), "reservation": False, "graph": "typed", "path": False, "redundancy": True},
    "RP-10": {"components": ("relevance", "role", "graph", "position"), "reservation": True, "graph": "typed", "path": False, "redundancy": True},
    "RP-01": {"components": ("relevance", "role", "graph", "path", "position"), "reservation": False, "graph": "typed", "path": True, "redundancy": True},
    "RP-11": {"components": ("relevance", "role", "graph", "path", "position"), "reservation": True, "graph": "typed", "path": True, "redundancy": True},
    "G-U": {"components": ("relevance", "role", "graph", "position"), "reservation": True, "graph": "untyped", "path": False, "redundancy": True},
    "G-T": {"components": ("relevance", "role", "graph", "position"), "reservation": True, "graph": "typed", "path": False, "redundancy": True},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def normalized_weights(base: Mapping[str, float], components: Sequence[str]) -> dict[str, float]:
    total = sum(float(base[name]) for name in components)
    if total <= 0:
        raise ValueError("positive component weights must have positive total")
    return {name: (float(base[name]) / total if name in components else 0.0) for name in base}


def untyped_graph_signal(typed_graph: CausalEventGraph, max_distance: int) -> dict[str, float]:
    """Match typed-graph weights while removing the role-transition gate.

    Lexical overlap is deliberately shared with the typed graph; otherwise the
    G-U/G-T contrast would confound edge typing with tokenization.
    """
    edges: list[CausalEdge] = []
    nodes = list(typed_graph.nodes)
    for left_index, source in enumerate(nodes):
        for target in nodes[left_index + 1 :]:
            distance = abs(source.position - target.position)
            if distance > max_distance:
                continue
            overlap = _jaccard(source.text, target.text)
            confidence = min(max(dict(source.role_scores).values()), max(dict(target.role_scores).values()))
            weight = 0.45 * math.exp(-distance / 5.0) + 0.30 * overlap + 0.25 * confidence
            edges.append(CausalEdge(source.sid, target.sid, "untyped_local_link", round(weight, 12)))
    return CausalEventGraph(nodes, edges).graph_signal()


def select_word_budget(
    graph: CausalEventGraph,
    channels: Mapping[str, Mapping[str, float]],
    condition: Mapping[str, Any],
    base_weights: Mapping[str, float],
    word_budget: int,
    redundancy_penalty: float,
) -> tuple[list[Any], dict[str, Any]]:
    components = tuple(condition["components"])
    weights = normalized_weights(base_weights, components)
    nodes = list(graph.nodes)
    by_sid = {node.sid: node for node in nodes}
    base_scores = {
        node.sid: sum(weights[name] * float(channels[name][node.sid]) for name in weights)
        for node in nodes
    }
    cache = RedundancyCache(nodes)
    selected: list[str] = []
    reasons: dict[str, str] = {}
    used_words = 0

    def fitting(candidates: Iterable[Any]) -> list[Any]:
        return [node for node in candidates if word_count(node.text) <= word_budget - used_words]

    def choose(candidates: Sequence[Any], apply_redundancy: bool) -> Any:
        def adjusted(node: Any) -> float:
            penalty = 0.0
            if apply_redundancy and selected:
                penalty = redundancy_penalty * max(cache.get(node.sid, prior) for prior in selected)
            return base_scores[node.sid] - penalty
        return sorted(candidates, key=lambda node: (-adjusted(node), node.position, node.sid))[0]

    if condition["reservation"]:
        for group, roles in ROLE_GROUPS.items():
            eligible = fitting(node for node in nodes if node.sid not in selected and node.dominant_role in roles)
            if eligible:
                winner = choose(eligible, False)
                selected.append(winner.sid)
                used_words += word_count(winner.text)
                reasons[winner.sid] = f"required_role_group:{group}"

    while True:
        eligible = fitting(node for node in nodes if node.sid not in selected)
        if not eligible:
            break
        winner = choose(eligible, bool(condition["redundancy"]))
        selected.append(winner.sid)
        used_words += word_count(winner.text)
        reasons[winner.sid] = "highest_adjusted_score"

    ordered = sorted((by_sid[sid] for sid in selected), key=lambda node: node.position)
    return ordered, {
        "selection_order": selected,
        "selection_reasons": reasons,
        "weights": weights,
        "actual_words": used_words,
        "unused_words": word_budget - used_words,
    }


def role_coverage(selected: Sequence[Any]) -> float:
    covered = sum(any(node.dominant_role in roles for node in selected) for roles in ROLE_GROUPS.values())
    return covered / len(ROLE_GROUPS)


def typed_edge_coverage(graph: CausalEventGraph, selected: Sequence[Any]) -> float:
    selected_ids = {node.sid for node in selected}
    incident = {edge.source for edge in graph.edges} | {edge.target for edge in graph.edges}
    return len(selected_ids & incident) / len(selected_ids) if selected_ids else 0.0


def redundancy(selected: Sequence[Any], cache: RedundancyCache) -> float:
    values = [cache.get(left.sid, right.sid) for index, left in enumerate(selected) for right in selected[index + 1 :]]
    return statistics.fmean(values) if values else 0.0


def percentile(sorted_values: Sequence[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("cannot take percentile of an empty sequence")
    position = probability * (len(sorted_values) - 1)
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    fraction = position - lower
    return float(sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction)


def contrast_summary(deltas: Mapping[str, float], *, samples: int, seed: int) -> dict[str, Any]:
    series = sorted(deltas)
    values = [float(deltas[key]) for key in series]
    observed = statistics.fmean(values)
    rng = random.Random(seed)
    draws = sorted(statistics.fmean(values[rng.randrange(len(values))] for _ in values) for _ in range(samples))
    if len(values) <= 20:
        threshold = abs(observed) - 1e-15
        total = 1 << len(values)
        extreme = 0
        for mask in range(total):
            value = statistics.fmean(delta if mask & (1 << idx) else -delta for idx, delta in enumerate(values))
            extreme += abs(value) >= threshold
        exact_p = extreme / total
    else:
        exact_p = None
    if len(values) > 1:
        spread = statistics.stdev(values)
        effect = observed / spread if spread > 0 else (math.inf if observed else 0.0)
    else:
        effect = None
    return {
        "n_series": len(values),
        "mean_delta": observed,
        "cluster_bootstrap_95": [percentile(draws, 0.025), percentile(draws, 0.975)],
        "exact_series_signflip_p": exact_p,
        "paired_standardized_mean_difference": effect,
        "series_deltas": {key: deltas[key] for key in series},
        "bootstrap_samples": samples,
        "bootstrap_seed": seed,
    }


def holm(records: list[dict[str, Any]]) -> None:
    eligible = [index for index, row in enumerate(records) if row["exact_series_signflip_p"] is not None]
    ordered = sorted(eligible, key=lambda index: records[index]["exact_series_signflip_p"])
    running = 0.0
    for rank, index in enumerate(ordered):
        adjusted = min(1.0, (len(ordered) - rank) * records[index]["exact_series_signflip_p"])
        running = max(running, adjusted)
        records[index]["holm_adjusted_p"] = running
        records[index]["holm_family_size"] = len(ordered)


def per_series_means(rows: Sequence[Mapping[str, Any]], metric: str) -> dict[tuple[int, str, str], float]:
    grouped: dict[tuple[int, str, str], list[float]] = defaultdict(list)
    for row in rows:
        if row["status"] == "PASS":
            grouped[(int(row["word_budget"]), str(row["condition"]), str(row["report_series_id"]))].append(float(row[metric]))
    return {key: statistics.fmean(values) for key, values in grouped.items()}


def paired_deltas(means: Mapping[tuple[int, str, str], float], budget: int, left: str, right: str) -> dict[str, float]:
    series = sorted({key[2] for key in means if key[0] == budget and key[1] in (left, right)})
    return {sid: means[(budget, left, sid)] - means[(budget, right, sid)] for sid in series}


def factorial_deltas(means: Mapping[tuple[int, str, str], float], budget: int, effect: str) -> dict[str, float]:
    series = sorted({key[2] for key in means if key[0] == budget and key[1].startswith("RP-")})
    output = {}
    for sid in series:
        value = lambda condition: means[(budget, condition, sid)]
        if effect == "reservation_main":
            output[sid] = ((value("RP-10") - value("RP-00")) + (value("RP-11") - value("RP-01"))) / 2
        elif effect == "path_main":
            output[sid] = ((value("RP-01") - value("RP-00")) + (value("RP-11") - value("RP-10"))) / 2
        elif effect == "interaction":
            output[sid] = (value("RP-11") - value("RP-10")) - (value("RP-01") - value("RP-00"))
        else:
            raise ValueError(effect)
    return output


def analyze(rows: Sequence[Mapping[str, Any]], config: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    means = per_series_means(rows, "rougeL_f1")
    chain_pairs = [("AB-1", "AB-0"), ("AB-2", "AB-1"), ("AB-3", "AB-2"), ("AB-4", "AB-3"), ("AB-5", "AB-4"), ("AB-5", "AB-6")]
    families: dict[str, list[dict[str, Any]]] = {"incremental_chain": [], "reservation_path_factorial": [], "graph_type": []}
    seed = int(config["bootstrap_seed"])
    for budget in config["word_budgets"]:
        for index, (left, right) in enumerate(chain_pairs):
            row = {"word_budget": budget, "contrast": f"{left}_minus_{right}", **contrast_summary(paired_deltas(means, budget, left, right), samples=int(config["bootstrap_samples"]), seed=seed + budget * 100 + index)}
            families["incremental_chain"].append(row)
        for index, effect in enumerate(("reservation_main", "path_main", "interaction")):
            row = {"word_budget": budget, "contrast": effect, **contrast_summary(factorial_deltas(means, budget, effect), samples=int(config["bootstrap_samples"]), seed=seed + budget * 100 + 20 + index)}
            families["reservation_path_factorial"].append(row)
        row = {"word_budget": budget, "contrast": "G-T_minus_G-U", **contrast_summary(paired_deltas(means, budget, "G-T", "G-U"), samples=int(config["bootstrap_samples"]), seed=seed + budget * 100 + 30)}
        families["graph_type"].append(row)
    for records in families.values():
        holm(records)
    return families


def run(config_path: Path, out_dir: Path) -> dict[str, Any]:
    print("This run tests implementation and mechanism diagnostics on development reports; it cannot support confirmatory manuscript claims.")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("mode") != "DEV_PILOT_NONCONFIRMATORY" or config.get("confirmatory_claims_allowed") is not False:
        raise RuntimeError("this entry point is restricted to non-confirmatory development pilots")
    if config.get("external_test_accessed") is not False:
        raise RuntimeError("external-test access flag must remain false")
    dataset = (WORKSPACE / config["dataset_relative_to_workspace"]).resolve()
    dataset.relative_to(WORKSPACE.resolve())
    if not dataset.is_file():
        raise FileNotFoundError(dataset)
    reports = jsonl(dataset)
    if len(reports) != int(config["expected_reports"]) or any(row.get("split") != "dev" for row in reports):
        raise RuntimeError("pilot requires the declared development-only dataset")
    if out_dir.exists():
        raise FileExistsError(f"refusing existing output directory: {out_dir}")
    out_dir.mkdir(parents=True)
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    result_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []

    for report_index, report in enumerate(reports, start=1):
        print(f"[{report_index}/{len(reports)}] Building controlled channels for {report['doc_id']}")
        graph_started = time.perf_counter()
        graph = build_graph_v03(report["candidate_sentences"], max_distance=int(config["max_distance"]))
        channels = score_channels(
            graph,
            path_min_edges=int(config["path_min_edges"]),
            path_max_edges=int(config["path_max_edges"]),
            path_max_paths=int(config["path_max_paths"]),
            path_max_expansions=int(config["path_max_expansions"]),
        )
        channels = {
            "relevance": channels["relevance"],
            "role": channels["role"],
            "graph": channels["graph"],
            "path": channels["counterfactual"],
            "position": channels["position"],
        }
        typed_preprocess_seconds = time.perf_counter() - graph_started
        untyped_started = time.perf_counter()
        untyped_signal = untyped_graph_signal(graph, int(config["max_distance"]))
        untyped_preprocess_seconds = time.perf_counter() - untyped_started
        cache = RedundancyCache(graph.nodes)

        for budget in config["word_budgets"]:
            for condition_name, condition in CONDITIONS.items():
                condition_channels = dict(channels)
                if condition["graph"] == "untyped":
                    condition_channels["graph"] = untyped_signal
                tracemalloc.start()
                started = time.perf_counter()
                try:
                    selected, audit = select_word_budget(
                        graph,
                        condition_channels,
                        condition,
                        config["base_positive_weights"],
                        int(budget),
                        float(config["redundancy_penalty"]),
                    )
                    prediction = " ".join(node.text for node in selected)
                    scores = scorer.score(report["reference_summary"], prediction)
                    elapsed = time.perf_counter() - started
                    _, peak = tracemalloc.get_traced_memory()
                    preprocess = typed_preprocess_seconds + (untyped_preprocess_seconds if condition["graph"] == "untyped" else 0.0)
                    result_rows.append({
                        "doc_id": report["doc_id"],
                        "report_series_id": report["report_series_id"],
                        "word_budget": int(budget),
                        "condition": condition_name,
                        "status": "PASS",
                        "rouge1_f1": float(scores["rouge1"].fmeasure),
                        "rouge2_f1": float(scores["rouge2"].fmeasure),
                        "rougeL_f1": float(scores["rougeL"].fmeasure),
                        "redundancy": redundancy(selected, cache),
                        "role_coverage": role_coverage(selected),
                        "typed_edge_coverage": typed_edge_coverage(graph, selected),
                        "actual_words": audit["actual_words"],
                        "budget_utilization": audit["actual_words"] / int(budget),
                        "selected_units": len(selected),
                        "preprocess_seconds_shared": preprocess,
                        "selection_and_scoring_seconds": elapsed,
                        "estimated_total_seconds": preprocess + elapsed,
                        "python_peak_memory_mb": peak / (1024 * 1024),
                    })
                    selected_rows.append({
                        "doc_id": report["doc_id"],
                        "report_series_id": report["report_series_id"],
                        "word_budget": int(budget),
                        "condition": condition_name,
                        "selected_sentence_ids": [node.sid for node in selected],
                        "selection_order": audit["selection_order"],
                        "actual_words": audit["actual_words"],
                    })
                except Exception as exc:
                    elapsed = time.perf_counter() - started
                    _, peak = tracemalloc.get_traced_memory()
                    result_rows.append({
                        "doc_id": report["doc_id"], "report_series_id": report["report_series_id"],
                        "word_budget": int(budget), "condition": condition_name, "status": "FAIL",
                        "error_type": type(exc).__name__, "error": str(exc),
                        "selection_and_scoring_seconds": elapsed, "python_peak_memory_mb": peak / (1024 * 1024),
                    })
                finally:
                    tracemalloc.stop()

    fieldnames = sorted({key for row in result_rows for key in row})
    with (out_dir / "factorial_item_metrics.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result_rows)
    with (out_dir / "factorial_selected_ids.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for row in selected_rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    families = analyze(result_rows, config)
    write_json(out_dir / "factorial_inference.json", families)

    aggregates: list[dict[str, Any]] = []
    for budget in config["word_budgets"]:
        for condition in CONDITIONS:
            subset = [row for row in result_rows if row["status"] == "PASS" and row["word_budget"] == budget and row["condition"] == condition]
            aggregates.append({
                "word_budget": budget,
                "condition": condition,
                "reports": len(subset),
                "failure_rate": 1.0 - len(subset) / len(reports),
                **{metric: statistics.fmean(float(row[metric]) for row in subset) for metric in ("rougeL_f1", "redundancy", "role_coverage", "typed_edge_coverage", "actual_words", "budget_utilization", "estimated_total_seconds", "python_peak_memory_mb")},
            })
    with (out_dir / "factorial_aggregate_metrics.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(aggregates[0]))
        writer.writeheader()
        writer.writerows(aggregates)

    final = {
        "status": "COMPLETE" if all(row["status"] == "PASS" for row in result_rows) else "COMPLETE_WITH_FAILURES",
        "mode": config["mode"],
        "confirmatory_claims_allowed": False,
        "external_test_accessed": False,
        "dataset_sha256": sha256(dataset),
        "config_sha256": sha256(config_path),
        "code_sha256": sha256(Path(__file__)),
        "reports": len(reports),
        "series": len({row["report_series_id"] for row in reports}),
        "conditions": len(CONDITIONS),
        "word_budgets": config["word_budgets"],
        "result_rows": len(result_rows),
        "failed_rows": sum(row["status"] != "PASS" for row in result_rows),
        "artifacts": {},
    }
    for name in ("factorial_item_metrics.csv", "factorial_selected_ids.jsonl", "factorial_inference.json", "factorial_aggregate_metrics.csv"):
        final["artifacts"][name] = sha256(out_dir / name)
    write_json(out_dir / "final_info.json", final)
    print(json.dumps(final, ensure_ascii=False, indent=2))
    return final


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=HERE / "experiment_config.json")
    args = parser.parse_args()
    run(args.config.resolve(), args.out_dir.resolve())


if __name__ == "__main__":
    main()
