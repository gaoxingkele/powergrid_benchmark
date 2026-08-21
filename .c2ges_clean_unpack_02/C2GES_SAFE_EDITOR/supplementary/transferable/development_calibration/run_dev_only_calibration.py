"""Post-unblinding, development-only calibration of the C2GES CF channel.

This program is deliberately unable to accept an arbitrary input path.  It reads
only the SHA-256-pinned 12-report development JSONL and the prior development
decision.  It never reads the held-out test JSONL or any formal-run artifact.
Outputs are exploratory and cannot replace the frozen v0.3.1 result.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

HERE = Path(__file__).resolve().parent
CODE_SNAPSHOT = HERE / "code_snapshot"
DEV_PATH = HERE / "not_packaged_rights_restricted" / "nerc_full_pdf_dev_v0_3.jsonl"
RUN04_DECISION = HERE.parent / "formal_protocol" / "DEV_SELECTION_DECISION.json"
EXPECTED_DEV_SHA256 = "27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79"
OUTPUT_DIR = HERE / "artifacts"

# Import only the corrective-method implementation.  Its exact source hashes are
# recorded in RUN_MANIFEST.json so this run remains bound to a code snapshot.
sys.path.insert(0, str(CODE_SNAPSHOT))
from counterfactual_paths import (  # noqa: E402
    path_counterfactual_sensitivity,
    qualified_typed_paths,
    raw_path_counterfactual_loss,
)
from v03_methods import (  # noqa: E402
    RedundancyCache,
    build_graph_v03,
    constrained_select,
    redundancy,
    score_channels,
)
from rouge_score import rouge_scorer  # noqa: E402


CF_WEIGHTS = (0.0, 0.025, 0.05, 0.075, 0.10, 0.15, 0.20)
ALLOCATION_FAMILIES = ("relevance", "graph", "split")
PATH_MAXIMA = (3, 4, 5)
GATES = ("none", "coverage", "coverage_stability")
K_VALUES = (5, 10)
GATE_COVERAGE_THRESHOLD = 0.01
GATE_MIN_PATHS = 2
GATE_STABILITY_THRESHOLD = 0.75


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _read_allowed(path: Path) -> str:
    resolved = path.resolve()
    allowlist = {DEV_PATH.resolve(), RUN04_DECISION.resolve()}
    if resolved not in allowlist:
        raise PermissionError(f"development-only input guard rejected: {resolved}")
    return resolved.read_text(encoding="utf-8")


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def weights(cf_weight: float, allocation: str) -> dict[str, float]:
    """Move the difference from the formal 0.15 CF weight to fixed donors.

    At CF=0.15 all families equal the formal v0.3.1 coefficients.  At other
    weights, the 0.15-c difference is assigned to relevance, graph, or equally
    to both.  Role and position remain fixed; every full vector sums to one.
    """
    delta = 0.15 - cf_weight
    result = {
        "relevance": 0.40,
        "role": 0.20,
        "graph": 0.15,
        "counterfactual": cf_weight,
        "position": 0.10,
    }
    if allocation == "relevance":
        result["relevance"] += delta
    elif allocation == "graph":
        result["graph"] += delta
    elif allocation == "split":
        result["relevance"] += delta / 2.0
        result["graph"] += delta / 2.0
    else:
        raise ValueError(allocation)
    if any(value < 0 for value in result.values()) or not math.isclose(sum(result.values()), 1.0, abs_tol=1e-12):
        raise AssertionError(result)
    return {key: round(value, 12) for key, value in result.items()}


def normalized_no_cf_weights(full: Mapping[str, float], allocation: str) -> dict[str, float]:
    """Transfer all CF mass back to the prespecified donor(s), preserving sum 1."""
    result = dict(full)
    mass = result["counterfactual"]
    result["counterfactual"] = 0.0
    if allocation in {"shared_formal", "split"}:
        result["relevance"] += mass / 2.0
        result["graph"] += mass / 2.0
    elif allocation == "relevance":
        result["relevance"] += mass
    elif allocation == "graph":
        result["graph"] += mass
    else:
        raise ValueError(allocation)
    if not math.isclose(sum(result.values()), 1.0, abs_tol=1e-12):
        raise AssertionError(result)
    return result


def candidate_grid() -> list[dict[str, object]]:
    """Return a semantically deduplicated, fixed finite grid."""
    candidates: list[dict[str, object]] = []
    seen: set[str] = set()
    for cf_weight in CF_WEIGHTS:
        for allocation in ALLOCATION_FAMILIES:
            for path_max in PATH_MAXIMA:
                for gate in GATES:
                    # At c=0 path/gate have no effect; retain one per donor family.
                    if cf_weight == 0.0 and (path_max != 4 or gate != "none"):
                        continue
                    # At c=.15 all donor families produce the same full and strict-zero
                    # comparator. Retain one shared representative.
                    effective_allocation = "shared_formal" if cf_weight == 0.15 else allocation
                    if cf_weight == 0.15 and allocation != "split":
                        continue
                    full_weights = weights(cf_weight, "split" if effective_allocation == "shared_formal" else allocation)
                    record = {
                        "cf_weight": cf_weight,
                        "allocation": effective_allocation,
                        "path_min_edges": 2,
                        "path_max_edges": path_max,
                        "gate": gate,
                        "weights": full_weights,
                        "redundancy_penalty": 0.50,
                        "max_distance": 12,
                    }
                    key = json.dumps(record, sort_keys=True)
                    if key not in seen:
                        seen.add(key)
                        candidates.append(record)
    candidates.sort(key=lambda item: json.dumps(item, sort_keys=True))
    for index, item in enumerate(candidates):
        item["candidate_id"] = f"C{index:03d}"
    return candidates


def rankdata(values: Sequence[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: (values[i], i))
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and math.isclose(values[order[end]], values[order[start]], abs_tol=1e-15):
            end += 1
        rank = (start + 1 + end) / 2.0
        for pos in range(start, end):
            ranks[order[pos]] = rank
        start = end
    return ranks


def spearman(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("vectors must have equal positive length")
    a, b = rankdata(left), rankdata(right)
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((x - mb) ** 2 for x in b)
    if va <= 0 or vb <= 0:
        return 1.0 if all(math.isclose(x, y, abs_tol=1e-15) for x, y in zip(left, right)) else 0.0
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(va * vb)


def gate_diagnostic(graph, horizon: int) -> dict[str, object]:
    paths = qualified_typed_paths(graph, min_edges=2, max_edges=horizon)
    raw = raw_path_counterfactual_loss(graph, min_edges=2, max_edges=horizon)
    previous = path_counterfactual_sensitivity(graph, min_edges=2, max_edges=horizon - 1)
    current = path_counterfactual_sensitivity(graph, min_edges=2, max_edges=horizon)
    sids = [node.sid for node in graph.nodes]
    coverage = sum(raw[sid] > 0 for sid in sids) / len(sids) if sids else 0.0
    stability = spearman([previous[sid] for sid in sids], [current[sid] for sid in sids]) if sids else 0.0
    return {
        "qualified_path_count": len(paths),
        "node_coverage": coverage,
        "adjacent_horizon_spearman": stability,
        "coverage_pass": len(paths) >= GATE_MIN_PATHS and coverage >= GATE_COVERAGE_THRESHOLD,
        "stability_pass": stability >= GATE_STABILITY_THRESHOLD,
    }


def gate_enabled(mode: str, diagnostic: Mapping[str, object]) -> bool:
    if mode == "none":
        return True
    if mode == "coverage":
        return bool(diagnostic["coverage_pass"])
    if mode == "coverage_stability":
        return bool(diagnostic["coverage_pass"]) and bool(diagnostic["stability_pass"])
    raise ValueError(mode)


def metric_dict(scorer, reference: str, selected) -> dict[str, float]:
    result = scorer.score(reference, " ".join(node.text for node in selected))
    return {
        "rouge1": float(result["rouge1"].fmeasure),
        "rougeL": float(result["rougeL"].fmeasure),
        "redundancy": float(redundancy(selected)),
    }


def selection_jaccard(left, right) -> float:
    a, b = {node.sid for node in left}, {node.sid for node in right}
    return len(a & b) / len(a | b) if a or b else 1.0


def mean(records: Sequence[Mapping[str, object]], field: str) -> float:
    return statistics.fmean(float(record[field]) for record in records)


def percentile(values: Sequence[float], p: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    low = int(math.floor(position))
    high = int(math.ceil(position))
    if low == high:
        return ordered[low]
    return ordered[low] * (high - position) + ordered[high] * (position - low)


def bootstrap_ci(values: Sequence[float], *, seed: int = 20260808, draws: int = 20000) -> list[float]:
    rng = random.Random(seed)
    n = len(values)
    boot = [statistics.fmean(values[rng.randrange(n)] for _ in range(n)) for _ in range(draws)]
    return [percentile(boot, 0.025), percentile(boot, 0.975)]


def run() -> None:
    if OUTPUT_DIR.exists():
        raise FileExistsError(f"refusing to overwrite exploratory run: {OUTPUT_DIR}")
    OUTPUT_DIR.mkdir(parents=True)
    started = datetime.now(timezone.utc).isoformat()
    if sha256(DEV_PATH) != EXPECTED_DEV_SHA256:
        raise RuntimeError("development input hash mismatch")
    rows = [json.loads(line) for line in _read_allowed(DEV_PATH).splitlines() if line.strip()]
    if len(rows) != 12 or any(row.get("split") != "dev" for row in rows):
        raise RuntimeError("requires exactly 12 physically development-only reports")
    if len({row["doc_id"] for row in rows}) != 12:
        raise RuntimeError("duplicate development report id")
    prior = json.loads(_read_allowed(RUN04_DECISION))
    if prior.get("test_input_accessed") is not False or prior.get("candidate_count") != 144:
        raise RuntimeError("prior development decision does not match the audited run04 asset")

    state = {
        "status": "RUNNING",
        "started_utc": started,
        "development_only": True,
        "formal_result_already_unblinded_before_start": True,
        "test_input_accessed": False,
        "formal_output_accessed": False,
    }
    _write_json(OUTPUT_DIR / "RUN_STATE.json", state)
    scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)
    grid = candidate_grid()
    graphs = {}
    redundancy_caches = {}
    channel_cache = {}
    diagnostics = {}
    diagnostic_rows = []
    for row in rows:
        doc_id = row["doc_id"]
        graph = build_graph_v03(row["candidate_sentences"], max_distance=12)
        graphs[doc_id] = graph
        redundancy_caches[doc_id] = RedundancyCache(graph.nodes)
        for horizon in PATH_MAXIMA:
            channel_cache[(doc_id, horizon)] = score_channels(graph, path_max_edges=horizon)
            diagnostic = gate_diagnostic(graph, horizon)
            diagnostics[(doc_id, horizon)] = diagnostic
            diagnostic_rows.append({"doc_id": doc_id, "path_min_edges": 2, "path_max_edges": horizon, **diagnostic})

    per_report = []
    summaries = []
    for candidate in grid:
        cid = candidate["candidate_id"]
        candidate_rows = []
        for row in rows:
            doc_id = row["doc_id"]
            graph = graphs[doc_id]
            channels = {name: dict(values) for name, values in channel_cache[(doc_id, candidate["path_max_edges"])].items()}
            enabled = gate_enabled(candidate["gate"], diagnostics[(doc_id, candidate["path_max_edges"])])
            if not enabled:
                channels["counterfactual"] = {sid: 0.0 for sid in channels["counterfactual"]}
            normalized_weights = normalized_no_cf_weights(candidate["weights"], candidate["allocation"])
            for k in K_VALUES:
                full, _ = constrained_select(
                    graph, channels, candidate["weights"], budget=k,
                    redundancy_penalty=candidate["redundancy_penalty"], redundancy_cache=redundancy_caches[doc_id]
                )
                strict, _ = constrained_select(
                    graph, channels, candidate["weights"], budget=k,
                    redundancy_penalty=candidate["redundancy_penalty"], remove_cf_only=True,
                    redundancy_cache=redundancy_caches[doc_id]
                )
                normalized, _ = constrained_select(
                    graph, channels, normalized_weights, budget=k,
                    redundancy_penalty=candidate["redundancy_penalty"], redundancy_cache=redundancy_caches[doc_id]
                )
                full_m = metric_dict(scorer, row["reference_summary"], full)
                strict_m = metric_dict(scorer, row["reference_summary"], strict)
                norm_m = metric_dict(scorer, row["reference_summary"], normalized)
                record = {
                    "candidate_id": cid,
                    "doc_id": doc_id,
                    "k": k,
                    "gate_enabled": enabled,
                    "full_rouge1": full_m["rouge1"],
                    "full_rougeL": full_m["rougeL"],
                    "full_redundancy": full_m["redundancy"],
                    "strict_zero_rouge1": strict_m["rouge1"],
                    "strict_zero_rougeL": strict_m["rougeL"],
                    "strict_zero_redundancy": strict_m["redundancy"],
                    "normalized_no_cf_rouge1": norm_m["rouge1"],
                    "normalized_no_cf_rougeL": norm_m["rougeL"],
                    "normalized_no_cf_redundancy": norm_m["redundancy"],
                    "delta_strict_zero_rougeL": full_m["rougeL"] - strict_m["rougeL"],
                    "delta_normalized_no_cf_rougeL": full_m["rougeL"] - norm_m["rougeL"],
                    "jaccard_strict_zero": selection_jaccard(full, strict),
                    "jaccard_normalized_no_cf": selection_jaccard(full, normalized),
                    "changed_sentences_strict_zero": len({node.sid for node in full} ^ {node.sid for node in strict}),
                    "changed_sentences_normalized_no_cf": len({node.sid for node in full} ^ {node.sid for node in normalized}),
                }
                per_report.append(record)
                candidate_rows.append(record)
        summary = {**candidate}
        for k in K_VALUES:
            subset = [record for record in candidate_rows if record["k"] == k]
            for metric in ("rouge1", "rougeL", "redundancy"):
                summary[f"mean_full_{metric}_k{k}"] = mean(subset, f"full_{metric}")
            summary[f"mean_delta_strict_zero_rougeL_k{k}"] = mean(subset, "delta_strict_zero_rougeL")
            summary[f"mean_delta_normalized_no_cf_rougeL_k{k}"] = mean(subset, "delta_normalized_no_cf_rougeL")
            summary[f"mean_jaccard_strict_zero_k{k}"] = mean(subset, "jaccard_strict_zero")
            summary[f"mean_changed_sentences_strict_zero_k{k}"] = mean(subset, "changed_sentences_strict_zero")
            summary[f"gate_enabled_reports_k{k}"] = sum(bool(record["gate_enabled"]) for record in subset)
        summary["selection_objective"] = 0.5 * summary["mean_full_rougeL_k5"] + 0.5 * summary["mean_full_rougeL_k10"]
        summary["strict_delta_objective"] = 0.5 * summary["mean_delta_strict_zero_rougeL_k5"] + 0.5 * summary["mean_delta_strict_zero_rougeL_k10"]
        summary["mean_redundancy_objective"] = 0.5 * summary["mean_full_redundancy_k5"] + 0.5 * summary["mean_full_redundancy_k10"]
        summaries.append(summary)

    # Leave-one-report-out selection: each fold chooses only from the other 11
    # reports. This estimates configuration stability, not held-out confirmation.
    loo_rows = []
    winner_counts: Counter[str] = Counter()
    per_report_lookup = {(r["candidate_id"], r["doc_id"], r["k"]): r for r in per_report}
    for held_out in [row["doc_id"] for row in rows]:
        fold_records = []
        for candidate in grid:
            train_docs = [row["doc_id"] for row in rows if row["doc_id"] != held_out]
            r5 = [per_report_lookup[(candidate["candidate_id"], doc, 5)] for doc in train_docs]
            r10 = [per_report_lookup[(candidate["candidate_id"], doc, 10)] for doc in train_docs]
            objective = 0.5 * mean(r5, "full_rougeL") + 0.5 * mean(r10, "full_rougeL")
            strict_delta = 0.5 * mean(r5, "delta_strict_zero_rougeL") + 0.5 * mean(r10, "delta_strict_zero_rougeL")
            red = 0.5 * mean(r5, "full_redundancy") + 0.5 * mean(r10, "full_redundancy")
            fold_records.append((objective, strict_delta, -red, -float(candidate["cf_weight"]), candidate["candidate_id"]))
        winner_tuple = max(fold_records)
        winner = winner_tuple[-1]
        winner_counts[winner] += 1
        held5 = per_report_lookup[(winner, held_out, 5)]
        held10 = per_report_lookup[(winner, held_out, 10)]
        loo_rows.append({
            "held_out_doc_id": held_out,
            "winner_candidate_id": winner,
            "train_objective": winner_tuple[0],
            "train_strict_delta_objective": winner_tuple[1],
            "held_out_full_rougeL_k5": held5["full_rougeL"],
            "held_out_full_rougeL_k10": held10["full_rougeL"],
            "held_out_delta_strict_zero_rougeL_k5": held5["delta_strict_zero_rougeL"],
            "held_out_delta_strict_zero_rougeL_k10": held10["delta_strict_zero_rougeL"],
        })

    by_id = {item["candidate_id"]: item for item in summaries}
    # Robust candidate: modal LOO winner; ties use full-development objective,
    # lower redundancy, then lower CF weight and stable id.
    robust_id = max(
        by_id,
        key=lambda cid: (
            winner_counts[cid], by_id[cid]["selection_objective"],
            -by_id[cid]["mean_redundancy_objective"], -float(by_id[cid]["cf_weight"]), cid,
        ),
    )
    nonzero_ids = [cid for cid, item in by_id.items() if float(item["cf_weight"]) > 0]
    robust_nonzero_id = max(
        nonzero_ids,
        key=lambda cid: (
            winner_counts[cid], by_id[cid]["selection_objective"],
            by_id[cid]["strict_delta_objective"], -by_id[cid]["mean_redundancy_objective"],
            -float(by_id[cid]["cf_weight"]), cid,
        ),
    )
    formal_ids = [
        cid for cid, item in by_id.items()
        if math.isclose(float(item["cf_weight"]), 0.15) and item["path_max_edges"] == 4 and item["gate"] == "none"
    ]
    if len(formal_ids) != 1:
        raise AssertionError(formal_ids)

    for cid, item in by_id.items():
        item["loo_winner_count"] = winner_counts[cid]
    decision = {
        "status": "development_only_post_unblinding_exploration",
        "not_confirmatory": True,
        "does_not_replace_frozen_v0_3_1": True,
        "test_input_accessed": False,
        "formal_output_accessed": False,
        "candidate_count": len(grid),
        "selection_rule": "modal 12-fold report-LOO winner; ties full-dev objective, lower redundancy, lower CF weight, stable id",
        "robust_overall": by_id[robust_id],
        "robust_nonzero_cf": by_id[robust_nonzero_id],
        "formal_v0_3_1_dev_configuration": by_id[formal_ids[0]],
        "winner_frequency": dict(sorted(winner_counts.items(), key=lambda pair: (-pair[1], pair[0]))),
    }
    for label, cid in (("overall", robust_id), ("nonzero", robust_nonzero_id), ("formal", formal_ids[0])):
        selected_rows = [record for record in per_report if record["candidate_id"] == cid]
        for k in K_VALUES:
            subset = [record for record in selected_rows if record["k"] == k]
            decision[f"{label}_bootstrap_ci_delta_strict_zero_rougeL_k{k}"] = bootstrap_ci(
                [float(record["delta_strict_zero_rougeL"]) for record in subset], seed=20260808 + k
            )
            decision[f"{label}_bootstrap_ci_delta_normalized_no_cf_rougeL_k{k}"] = bootstrap_ci(
                [float(record["delta_normalized_no_cf_rougeL"]) for record in subset], seed=20260908 + k
            )

    _write_jsonl(OUTPUT_DIR / "path_gate_diagnostics.jsonl", diagnostic_rows)
    _write_jsonl(OUTPUT_DIR / "per_report_ledger.jsonl", per_report)
    _write_jsonl(OUTPUT_DIR / "candidate_summary_ledger.jsonl", summaries)
    _write_jsonl(OUTPUT_DIR / "loo_fold_ledger.jsonl", loo_rows)
    _write_json(OUTPUT_DIR / "CALIBRATION_DECISION.json", decision)
    completed = datetime.now(timezone.utc).isoformat()
    source_files = [
        Path(__file__).resolve(), R2_ROOT / "v03_methods.py", R2_ROOT / "counterfactual_paths.py",
        R2_ROOT.parent / "c2ges_offline.py",
    ]
    manifest = {
        "protocol": "C2GES-posthoc-dev-CF-calibration-v1",
        "started_utc": started,
        "completed_utc": completed,
        "timeline": [
            {"event": "formal_v0_3_1_results_unblinded", "time": "before_exploration_start", "source": "user-provided status; formal files were not read"},
            {"event": "posthoc_dev_only_exploration_started", "time": started},
            {"event": "posthoc_dev_only_exploration_completed", "time": completed},
        ],
        "data_boundary": {
            "allowed_inputs": [str(DEV_PATH.resolve()), str(RUN04_DECISION.resolve())],
            "dev_sha256": sha256(DEV_PATH),
            "forbidden_classes": ["test JSONL", "formal predictions", "formal aggregate", "formal contrasts"],
            "test_input_accessed": False,
            "formal_output_accessed": False,
        },
        "code_snapshot": [{"path": str(path), "sha256": sha256(path)} for path in source_files],
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "candidate_count": len(grid),
        "output_sha256": {},
    }
    for name in (
        "path_gate_diagnostics.jsonl", "per_report_ledger.jsonl", "candidate_summary_ledger.jsonl",
        "loo_fold_ledger.jsonl", "CALIBRATION_DECISION.json",
    ):
        manifest["output_sha256"][name] = sha256(OUTPUT_DIR / name)
    _write_json(OUTPUT_DIR / "RUN_MANIFEST.json", manifest)
    state.update({"status": "COMPLETE", "completed_utc": completed, "candidate_count": len(grid)})
    _write_json(OUTPUT_DIR / "RUN_STATE.json", state)


if __name__ == "__main__":
    run()
