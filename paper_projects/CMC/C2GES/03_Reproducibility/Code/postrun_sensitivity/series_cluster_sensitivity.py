#!/usr/bin/env python3
"""Series-cluster sensitivity analysis from distributed non-verbatim deltas."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import random
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DATA = PROJECT / "03_Reproducibility" / "Data"
DEFAULT_INPUT = DATA / "postrun_sensitivity" / "exact_signflip_results.json"
DEFAULT_METADATA = DATA / "rights_safe_metadata" / "rights_safe_report_metadata.csv"
DEFAULT_OUTPUT = DATA / "postrun_series_cluster"
BOOTSTRAP_SAMPLES = 10_000
BOOTSTRAP_SEED = 20_260_823


def exact_signflip(values: list[float]) -> tuple[float, int, int]:
    observed = abs(sum(values))
    total = 2 ** len(values)
    extreme = sum(
        abs(sum(sign * value for sign, value in zip(signs, values))) + 1e-15 >= observed
        for signs in itertools.product((-1.0, 1.0), repeat=len(values))
    )
    return extreme / total, extreme, total


def holm(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    adjusted = [0.0] * len(values)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(values) - rank) * values[index]))
        adjusted[index] = running
    return adjusted


def percentile(sorted_values: list[float], probability: float) -> float:
    position = probability * (len(sorted_values) - 1)
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return sorted_values[lower] * (1.0 - fraction) + sorted_values[upper] * fraction


def bootstrap_interval(values: list[float], seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    n = len(values)
    draws = sorted(sum(rng.choice(values) for _ in range(n)) / n for _ in range(BOOTSTRAP_SAMPLES))
    return percentile(draws, 0.025), percentile(draws, 0.975)


def load_series(metadata_path: Path) -> dict[str, str]:
    with metadata_path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    mapping = {row["doc_id"]: row["report_series_id"] for row in rows if row["analysis_split"] == "test"}
    if len(mapping) != 15 or len(set(mapping.values())) != 10:
        raise ValueError("expected 15 retained test reports in 10 series")
    return mapping


def analyze(payload: dict, series_by_doc: dict[str, str]) -> list[dict]:
    results = []
    for index, item in enumerate(payload["results"]):
        grouped: dict[str, list[float]] = defaultdict(list)
        for row in item["report_deltas"]:
            grouped[series_by_doc[row["doc_id"]]].append(float(row["delta"]))
        if set(series_by_doc.values()) != set(grouped):
            raise ValueError(f"series coverage mismatch for {item['contrast']} K={item['budget']}")
        series_rows = [
            {
                "report_series_id": series,
                "n_reports": len(values),
                "mean_delta": sum(values) / len(values),
            }
            for series, values in sorted(grouped.items())
        ]
        values = [row["mean_delta"] for row in series_rows]
        p_value, extreme, total = exact_signflip(values)
        lower, upper = bootstrap_interval(values, BOOTSTRAP_SEED + index)
        loso = []
        for excluded in sorted(grouped):
            kept = [row["mean_delta"] for row in series_rows if row["report_series_id"] != excluded]
            loso.append({"excluded_series": excluded, "mean_delta": sum(kept) / len(kept)})
        results.append({
            "budget": int(item["budget"]),
            "contrast": item["contrast"],
            "n_reports": len(item["report_deltas"]),
            "n_series": len(values),
            "report_equal_mean_delta": sum(float(row["delta"]) for row in item["report_deltas"]) / len(item["report_deltas"]),
            "series_equal_mean_delta": sum(values) / len(values),
            "cluster_bootstrap_95_percentile": [lower, upper],
            "exact_series_signflip_p": p_value,
            "extreme_assignments": extreme,
            "enumerated_assignments": total,
            "series": series_rows,
            "leave_one_series_out": loso,
            "loso_min": min(row["mean_delta"] for row in loso),
            "loso_max": max(row["mean_delta"] for row in loso),
        })
    adjusted = holm([row["exact_series_signflip_p"] for row in results])
    for row, value in zip(results, adjusted):
        row["holm_adjusted_p_six_tests"] = value
    return results


def write_outputs(output: Path, results: list[dict], input_path: Path, metadata_path: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    payload = {
        "analysis_id": "C2GES-v0.3.1-postrun-series-cluster-sensitivity-v1",
        "status": "post_run_sensitivity_not_confirmatory",
        "inputs": [input_path.relative_to(PROJECT).as_posix(), metadata_path.relative_to(PROJECT).as_posix()],
        "method": {
            "primary_sensitivity_estimand": "equal weight per report_series_id after within-series mean",
            "secondary_estimand": "equal weight per report",
            "cluster_bootstrap_samples": BOOTSTRAP_SAMPLES,
            "cluster_bootstrap_seed_base": BOOTSTRAP_SEED,
            "series_signflip": "all 2^10 assignments, two-sided inclusive absolute-mean rule",
            "multiplicity": "Holm step-down over six contrasts",
            "leave_one_series_out": True,
        },
        "results": results,
    }
    (output / "series_cluster_results.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with (output / "series_cluster_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["budget", "contrast", "n_reports", "n_series", "report_equal_mean_delta", "series_equal_mean_delta", "bootstrap_95_low", "bootstrap_95_high", "exact_series_signflip_p", "holm_adjusted_p", "loso_min", "loso_max"])
        for row in results:
            writer.writerow([row["budget"], row["contrast"], row["n_reports"], row["n_series"], row["report_equal_mean_delta"], row["series_equal_mean_delta"], *row["cluster_bootstrap_95_percentile"], row["exact_series_signflip_p"], row["holm_adjusted_p_six_tests"], row["loso_min"], row["loso_max"]])
    with (output / "series_cluster_loso.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["budget", "contrast", "excluded_series", "mean_delta"])
        for row in results:
            for item in row["leave_one_series_out"]:
                writer.writerow([row["budget"], row["contrast"], item["excluded_series"], item["mean_delta"]])

    lines = [
        "# C2GES series-cluster sensitivity report",
        "",
        "Status: post-run sensitivity analysis; not a fresh confirmatory test.",
        "",
        "The 15 retained reports form 10 frozen `report_series_id` clusters. Each series first contributes its within-series mean delta; the series-equal estimand then assigns equal weight to the 10 series. The interval is a deterministic 10,000-draw cluster bootstrap. Exact sign flips enumerate all 1,024 series-level assignments, followed by Holm adjustment across the six contrasts.",
        "",
        "| K | Contrast | Report-equal delta | Series-equal delta | Cluster bootstrap 95% | Exact p | Holm p | LOSO range |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        low, high = row["cluster_bootstrap_95_percentile"]
        lines.append(f"| {row['budget']} | {row['contrast']} | {row['report_equal_mean_delta']:.6f} | {row['series_equal_mean_delta']:.6f} | [{low:.6f}, {high:.6f}] | {row['exact_series_signflip_p']:.6f} | {row['holm_adjusted_p_six_tests']:.6f} | [{row['loso_min']:.6f}, {row['loso_max']:.6f}] |")
    lines.extend(["", "These values describe robustness to the recorded series clustering. They do not repair unequal output length, tuning asymmetry, extraction-unit contamination, embedding truncation, or the absence of expert semantic validation.", ""])
    (output / "SERIES_CLUSTER_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    results = analyze(payload, load_series(args.metadata))
    write_outputs(args.output, results, args.input, args.metadata)
    print(json.dumps({"status": "PASS", "contrasts": len(results), "output": str(args.output)}))


if __name__ == "__main__":
    main()
