#!/usr/bin/env python3
"""Independent W3/W4 C2GES recomputation from run-level artifacts.

The official five_seed_aggregate.json is deliberately opened only after the
independent payload has been completely calculated from predictions.jsonl,
summary.json, and resource_usage.json.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats


SEEDS = (2026, 2027, 2028, 2029, 2030)
K_VALUES = (1, 3, 5, 10)
PROTOCOL_DIRS = {"oracle-label": "oracle", "predicted-label": "predicted", "label-blind": "label_blind"}
PROTOCOL_PAIRS = (
    ("oracle-label", "predicted-label"),
    ("oracle-label", "label-blind"),
    ("predicted-label", "label-blind"),
)
MODES = ("full", "query_only", "no_role", "no_graph", "tfidf", "bm25", "sbert", "lead_k", "lexcue")
EXPECTED_ROWS = len(K_VALUES) * len(MODES) * 1500
TOLERANCE = 1e-12
FAILURE_KEYS = (
    "malformed_json", "missing_required_fields", "duplicate_prediction_keys",
    "unexpected_mode_or_k", "invalid_metric_values", "incomplete_mode_k_cells",
    "unexpected_prediction_row_count", "summary_f1_mismatches",
    "summary_protocol_mismatch", "resource_run_failures",
    "nonidentical_bm25_cells", "cross_protocol_alignment_failures",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(values: list[float]) -> dict[str, Any]:
    mean = statistics.fmean(values)
    sample_std = statistics.stdev(values)
    sem = sample_std / math.sqrt(len(values))
    critical = float(stats.t.ppf(0.975, len(values) - 1))
    return {"values": values, "mean": mean, "sample_std": sample_std,
            "t_ci95": [mean - critical * sem, mean + critical * sem]}


def exact_sign_flip_p(values: list[float]) -> float:
    observed = abs(statistics.fmean(values))
    permuted = [abs(float(np.mean(np.asarray(values) * np.asarray(signs))))
                for signs in itertools.product((-1.0, 1.0), repeat=len(values))]
    return float(np.mean(np.asarray(permuted) >= observed - 1e-15))


def paired_seed_effect(left: list[float], right: list[float]) -> dict[str, Any]:
    deltas = [a - b for a, b in zip(left, right)]
    result = summarize(deltas)
    result.update({
        "left_values": left,
        "right_values": right,
        "positive_seed_count": sum(value > 0 for value in deltas),
        "negative_seed_count": sum(value < 0 for value in deltas),
        "paired_t_p_two_sided": float(stats.ttest_rel(left, right).pvalue),
        "exact_sign_flip_p_two_sided": exact_sign_flip_p(deltas),
    })
    return result


def hierarchical_bootstrap(delta_by_seed: dict[int, dict[str, list[float]]], samples: int, rng_seed: int) -> dict[str, Any]:
    """Resample training seeds, then document clusters within selected seed."""
    rng = np.random.default_rng(rng_seed)
    seed_ids = sorted(delta_by_seed)
    draws = []
    for _ in range(samples):
        selected_seeds = rng.choice(seed_ids, size=len(seed_ids), replace=True)
        values: list[float] = []
        for selected_seed in selected_seeds:
            clusters = delta_by_seed[int(selected_seed)]
            document_ids = list(clusters)
            selected_documents = rng.choice(document_ids, size=len(document_ids), replace=True)
            for document_id in selected_documents:
                values.extend(clusters[str(document_id)])
        draws.append(float(np.mean(values)))
    array = np.asarray(draws)
    return {
        "mean": float(array.mean()),
        "ci95": [float(np.quantile(array, 0.025)), float(np.quantile(array, 0.975))],
        "p_two_sided": float(min(1.0, 2 * min(np.mean(array <= 0), np.mean(array >= 0)))),
        "samples": samples,
        "outer_unit": "training_seed",
        "inner_unit": "underlying_wikipedia_document",
        "seed_count": len(seed_ids),
        "document_counts": {str(seed): len(clusters) for seed, clusters in delta_by_seed.items()},
    }


def run_directory(w3_root: Path, w4_root: Path, seed: int, protocol: str) -> Path:
    if seed == 2026:
        return w3_root / PROTOCOL_DIRS[protocol]
    return w4_root / f"seed_{seed}" / PROTOCOL_DIRS[protocol]


def scan_run(directory: Path, seed: int, protocol: str) -> dict[str, Any]:
    prediction_path = directory / "predictions.jsonl"
    summary_path = directory / "summary.json"
    resource_path = directory / "resource_usage.json"
    for path in (prediction_path, summary_path, resource_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    accumulators: dict[tuple[str, int], dict[str, float]] = defaultdict(lambda: {"n": 0, "precision": 0.0, "recall": 0.0, "f1": 0.0})
    full_rows: dict[tuple[int, str], dict[str, Any]] = {}
    bm25_rows: dict[tuple[int, str], dict[str, Any]] = {}
    failures = defaultdict(int)
    seen: set[tuple[str, int, str]] = set()
    row_count = 0
    with prediction_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            row_count += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                failures["malformed_json"] += 1
                raise ValueError(f"{prediction_path}:{line_number}: {exc}") from exc
            required = ("qid", "underlying_document_id", "mode", "k", "precision", "recall", "f1")
            if any(key not in row for key in required):
                failures["missing_required_fields"] += 1
                continue
            mode, k, qid = row["mode"], row["k"], row["qid"]
            key = (mode, k, qid)
            if key in seen:
                failures["duplicate_prediction_keys"] += 1
                continue
            seen.add(key)
            if mode not in MODES or k not in K_VALUES:
                failures["unexpected_mode_or_k"] += 1
                continue
            values = [float(row[name]) for name in ("precision", "recall", "f1")]
            if not all(math.isfinite(value) and 0 <= value <= 1 for value in values):
                failures["invalid_metric_values"] += 1
                continue
            accumulator = accumulators[(mode, k)]
            accumulator["n"] += 1
            for name, value in zip(("precision", "recall", "f1"), values):
                accumulator[name] += value
            compact = {"f1": values[2], "document_id": str(row["underlying_document_id"])}
            if mode == "full":
                full_rows[(k, qid)] = compact
            elif mode == "bm25":
                bm25_rows[(k, qid)] = compact

    metrics = {}
    for mode in MODES:
        metrics[mode] = {}
        for k in K_VALUES:
            item = accumulators[(mode, k)]
            n = int(item["n"])
            if n != 1500:
                failures["incomplete_mode_k_cells"] += 1
            metrics[mode][str(k)] = {
                "n": n,
                "evidence_precision": item["precision"] / n if n else None,
                "evidence_recall": item["recall"] / n if n else None,
                "evidence_f1": item["f1"] / n if n else None,
            }
    if row_count != EXPECTED_ROWS:
        failures["unexpected_prediction_row_count"] += 1

    # Summary is validation evidence only. Its numeric values never feed metrics/effects.
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary_mismatches = []
    for mode in MODES:
        for k in K_VALUES:
            found = metrics[mode][str(k)]["evidence_f1"]
            reported = summary.get("k_sensitivity", {}).get(str(k), {}).get("test", {}).get(mode, {}).get("evidence_f1")
            if reported is None or abs(found - float(reported)) > TOLERANCE:
                summary_mismatches.append({"mode": mode, "k": k, "recomputed": found, "summary": reported})
    failures["summary_f1_mismatches"] = len(summary_mismatches)
    if summary.get("protocol") != protocol:
        failures["summary_protocol_mismatch"] += 1

    resource = json.loads(resource_path.read_text(encoding="utf-8"))
    if resource.get("status") != "success" or resource.get("failure") is not None:
        failures["resource_run_failures"] += 1
    input_hashes = {path.name: sha256(path) for path in (prediction_path, summary_path, resource_path)}
    return {
        "seed": seed, "protocol": protocol, "directory": str(directory), "row_count": row_count,
        "metrics": metrics, "full_rows": full_rows, "bm25_rows": bm25_rows,
        "resource": resource, "failures": dict(failures), "summary_mismatches": summary_mismatches,
        "input_hashes": input_hashes,
    }


def independent_calculation(w3_root: Path, w4_root: Path, bootstrap_samples: int) -> tuple[dict[str, Any], dict[str, Any]]:
    runs: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
    all_failure_counts = {key: 0 for key in FAILURE_KEYS}
    input_manifest = []
    for seed in SEEDS:
        for protocol in PROTOCOL_DIRS:
            run = scan_run(run_directory(w3_root, w4_root, seed, protocol), seed, protocol)
            runs[seed][protocol] = run
            for name, count in run["failures"].items():
                all_failure_counts[name] = all_failure_counts.get(name, 0) + count
            input_manifest.append({"seed": seed, "protocol": protocol, "directory": run["directory"],
                                   "files": run["input_hashes"], "prediction_rows": run["row_count"]})

    # Pairing and deterministic-baseline audits.
    reference_bm25 = runs[2026]["oracle-label"]["bm25_rows"]
    for seed in SEEDS:
        for protocol in PROTOCOL_DIRS:
            current = runs[seed][protocol]["bm25_rows"]
            if current.keys() != reference_bm25.keys() or any(current[key]["f1"] != reference_bm25[key]["f1"] for key in reference_bm25):
                all_failure_counts["nonidentical_bm25_cells"] += 1
    for seed in SEEDS:
        reference_keys = runs[seed]["oracle-label"]["full_rows"].keys()
        for protocol in PROTOCOL_DIRS:
            if runs[seed][protocol]["full_rows"].keys() != reference_keys:
                all_failure_counts["cross_protocol_alignment_failures"] += 1

    metric_values = {
        protocol: {k: {seed: runs[seed][protocol]["metrics"]["full"][str(k)]["evidence_f1"] for seed in SEEDS}
                   for k in K_VALUES}
        for protocol in PROTOCOL_DIRS
    }
    metric_summary = {
        protocol: {str(k): summarize([metric_values[protocol][k][seed] for seed in SEEDS]) for k in K_VALUES}
        for protocol in PROTOCOL_DIRS
    }
    bm25 = {
        protocol: {str(k): summarize([runs[seed][protocol]["metrics"]["bm25"][str(k)]["evidence_f1"] for seed in SEEDS])
                   for k in K_VALUES}
        for protocol in PROTOCOL_DIRS
    }

    effects: dict[str, Any] = {}

    def add_effect(name: str, k: int, left_protocol: str, right_protocol: str | None) -> None:
        left = [metric_values[left_protocol][k][seed] for seed in SEEDS]
        if right_protocol is None:
            right = [runs[seed][left_protocol]["metrics"]["bm25"][str(k)]["evidence_f1"] for seed in SEEDS]
        else:
            right = [metric_values[right_protocol][k][seed] for seed in SEEDS]
        seed_effect = paired_seed_effect(left, right)
        delta_by_seed = {}
        for seed in SEEDS:
            left_rows = runs[seed][left_protocol]["full_rows"]
            right_rows = runs[seed][left_protocol]["bm25_rows"] if right_protocol is None else runs[seed][right_protocol]["full_rows"]
            clusters: dict[str, list[float]] = defaultdict(list)
            for (row_k, qid), left_row in left_rows.items():
                if row_k == k:
                    clusters[left_row["document_id"]].append(left_row["f1"] - right_rows[(row_k, qid)]["f1"])
            delta_by_seed[seed] = dict(clusters)
        hierarchical = hierarchical_bootstrap(delta_by_seed, bootstrap_samples, 50000 + k + len(effects) * 100)
        gate = bool(seed_effect["mean"] > 0 and seed_effect["t_ci95"][0] > 0 and hierarchical["ci95"][0] > 0)
        effects.setdefault(name, {})[str(k)] = {
            "seed_level": seed_effect, "hierarchical_bootstrap": hierarchical, "positive_effect_gate": gate,
        }

    for protocol in PROTOCOL_DIRS:
        for k in K_VALUES:
            add_effect(f"{protocol}_minus_bm25", k, protocol, None)
    for left, right in PROTOCOL_PAIRS:
        for k in K_VALUES:
            add_effect(f"{left}_minus_{right}", k, left, right)

    resources = {
        protocol: {
            "wall_seconds": summarize([runs[seed][protocol]["resource"]["wall_seconds"] for seed in SEEDS]),
            "peak_rss_gib": summarize([runs[seed][protocol]["resource"]["resource_sampling"]["peak_tree_rss_gib"] for seed in SEEDS]),
        }
        for protocol in PROTOCOL_DIRS
    }
    hard_failure_count = sum(all_failure_counts.values())
    projection = {
        "seeds": list(SEEDS), "k_values": list(K_VALUES), "metric": "macro mean instance-level evidence F1",
        "metric_summary": metric_summary, "effects": effects, "resources": resources,
    }
    payload = {
        "schema_version": "c2-independent-recompute-1.0",
        "calculation_input_policy": "official aggregate excluded until post-calculation diff",
        "projection_comparable_to_official": projection,
        "recomputed_by_protocol_k": {
            protocol: {str(k): {"full": metric_summary[protocol][str(k)], "bm25": bm25[protocol][str(k)]}
                       for k in K_VALUES}
            for protocol in PROTOCOL_DIRS
        },
        "per_seed_all_modes": {
            str(seed): {protocol: runs[seed][protocol]["metrics"] for protocol in PROTOCOL_DIRS} for seed in SEEDS
        },
        "failure_counts": {**dict(sorted(all_failure_counts.items())), "hard_failure_total": hard_failure_count,
                           "successful_resource_runs": sum(runs[s][p]["resource"].get("status") == "success" for s in SEEDS for p in PROTOCOL_DIRS),
                           "expected_resource_runs": len(SEEDS) * len(PROTOCOL_DIRS)},
        "input_manifest": input_manifest,
        "bootstrap": {"samples": bootstrap_samples, "outer_unit": "training_seed", "inner_unit": "underlying_wikipedia_document"},
    }
    return payload, projection


def compare_cells(independent: Any, official: Any, path: str = "$") -> list[dict[str, Any]]:
    cells = []
    if isinstance(independent, dict) and isinstance(official, dict):
        for key in sorted(set(independent) | set(official)):
            if key not in independent or key not in official:
                cells.append({"path": f"{path}.{key}", "independent": independent.get(key), "official": official.get(key), "match": False, "reason": "missing_key"})
            else:
                cells.extend(compare_cells(independent[key], official[key], f"{path}.{key}"))
    elif isinstance(independent, list) and isinstance(official, list):
        if len(independent) != len(official):
            cells.append({"path": path, "independent": len(independent), "official": len(official), "match": False, "reason": "list_length"})
        for index, (left, right) in enumerate(zip(independent, official)):
            cells.extend(compare_cells(left, right, f"{path}[{index}]"))
    else:
        numeric = isinstance(independent, (int, float)) and not isinstance(independent, bool) and isinstance(official, (int, float)) and not isinstance(official, bool)
        difference = abs(float(independent) - float(official)) if numeric else None
        match = difference <= TOLERANCE if numeric else independent == official
        cells.append({"path": path, "independent": independent, "official": official,
                      "absolute_difference": difference, "tolerance": TOLERANCE if numeric else None, "match": match})
    return cells


def write_markdown(payload: dict[str, Any], diff: dict[str, Any], output_path: Path) -> None:
    projection = payload["projection_comparable_to_official"]
    lines = [
        "# C2GES Independent Five-Seed Recompute", "",
        "The official aggregate was excluded from all calculations and opened only for the final cell-by-cell comparison.", "",
        f"- Diff status: **{'PASS' if diff['passed'] else 'FAIL'}** ({diff['matched_cells']}/{diff['cell_count']} comparable cells matched; max numeric difference `{diff['max_numeric_difference']:.3g}`).",
        f"- Hard artifact/row/resource failures: **{payload['failure_counts']['hard_failure_total']}**.",
        f"- Successful resource runs: **{payload['failure_counts']['successful_resource_runs']}/{payload['failure_counts']['expected_resource_runs']}**.", "",
        "## Recomputed full evidence F1", "",
        "| Protocol | K=1 | K=3 | K=5 | K=10 |", "|---|---:|---:|---:|---:|",
    ]
    for protocol in PROTOCOL_DIRS:
        cells = [projection["metric_summary"][protocol][str(k)] for k in K_VALUES]
        lines.append(f"| {protocol} | " + " | ".join(f"{cell['mean']:.6f} +/- {cell['sample_std']:.6f}" for cell in cells) + " |")
    lines += ["", "## Recomputed BM25 F1", "", "| Protocol | K=1 | K=3 | K=5 | K=10 |", "|---|---:|---:|---:|---:|"]
    for protocol in PROTOCOL_DIRS:
        cells = [payload["recomputed_by_protocol_k"][protocol][str(k)]["bm25"] for k in K_VALUES]
        lines.append(f"| {protocol} | " + " | ".join(f"{cell['mean']:.6f}" for cell in cells) + " |")
    lines += ["", "## Failure counts", "", "| Check | Count |", "|---|---:|"]
    for key, value in payload["failure_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines += ["", "## Reproducibility", "",
              "Input file hashes are embedded in `independent_recompute.json`; every compared leaf is recorded in `diff.json`.", ""]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    output_dir = Path(__file__).resolve().parent
    repo_root = Path(__file__).resolve().parents[5]
    w3_root = repo_root / "paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500"
    w4_root = repo_root / "paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed"
    official_path = w4_root / "five_seed_aggregate.json"

    payload, projection = independent_calculation(w3_root, w4_root, bootstrap_samples=2000)
    recompute_path = output_dir / "independent_recompute.json"
    recompute_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Deliberate phase boundary: official values are first read here, after output calculation.
    official = json.loads(official_path.read_text(encoding="utf-8"))
    official_projection = {key: official[key] for key in ("seeds", "k_values", "metric", "metric_summary", "effects", "resources")}
    cells = compare_cells(projection, official_projection)
    mismatches = [cell for cell in cells if not cell["match"]]
    numeric_differences = [cell["absolute_difference"] for cell in cells if cell.get("absolute_difference") is not None]
    diff = {
        "schema_version": "c2-independent-diff-1.0", "passed": not mismatches,
        "official_path": str(official_path), "official_sha256": sha256(official_path),
        "tolerance": TOLERANCE, "cell_count": len(cells), "matched_cells": len(cells) - len(mismatches),
        "mismatch_count": len(mismatches), "max_numeric_difference": max(numeric_differences, default=0.0),
        "mismatches": mismatches, "cells": cells,
        "official_failure_audit": {"passed": official.get("failure_audit", {}).get("passed"),
                                   "failure_count": official.get("failure_audit", {}).get("failure_count")},
    }
    diff_path = output_dir / "diff.json"
    diff_path.write_text(json.dumps(diff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = output_dir / "independent_recompute.md"
    write_markdown(payload, diff, report_path)
    manifest = {
        "schema_version": "c2-independent-recompute-manifest-1.0",
        "script": {"path": Path(__file__).name, "sha256": sha256(Path(__file__))},
        "tests": {"path": "test_recompute.py", "sha256": sha256(output_dir / "test_recompute.py")},
        "outputs": [{"path": path.name, "sha256": sha256(path), "bytes": path.stat().st_size}
                    for path in (recompute_path, report_path, diff_path)],
        "source_policy": payload["calculation_input_policy"],
    }
    (output_dir / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": diff["passed"], "cells": diff["cell_count"], "mismatches": diff["mismatch_count"],
                      "max_numeric_difference": diff["max_numeric_difference"], "hard_failures": payload["failure_counts"]["hard_failure_total"]}, indent=2))
    return 0 if diff["passed"] and payload["failure_counts"]["hard_failure_total"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
