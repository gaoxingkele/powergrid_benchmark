"""Regenerate all quantitative P2 manuscript artifacts from accepted evidence.

The accepted rolling-origin namespace is authoritative for the matched-control
claim. Historical fixed-split and exact-hierarchy CSVs are retained as scoped
boundary evidence. Before reading the new results, this script verifies every
output hash recorded by the accepted run manifest. It then writes normalized,
version-free derived tables plus PNG/PDF/SVG figures.

The script intentionally uses only the Python standard library, Pillow, and
ReportLab so it can run in the preserved paper-harness runtime without a
Matplotlib installation.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas as pdfcanvas


FIG_DIR = Path(__file__).resolve().parent
MANUSCRIPT_DIR = FIG_DIR.parent
PROJECT_ROOT = MANUSCRIPT_DIR.parent
HARNESS_ROOT = PROJECT_ROOT.parents[1]
DERIVED_DIR = MANUSCRIPT_DIR / "derived_tables"

RUN_ROOT = PROJECT_ROOT / "experiments" / "p2_s3_identifiable_v1"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
RUN_TABLES = RUN_ROOT / "results"

HISTORICAL_ROOT = (
    HARNESS_ROOT
    / "papers"
    / "mintou"
    / "mintou_p2_hygraph_load_forecasting"
    / "evidence"
)
HIST_TABLES = HISTORICAL_ROOT / "tables"
HIST_RUNS = HISTORICAL_ROOT / "runs"

OPSD_LEADERBOARD = HIST_TABLES / "real_opsd_v7_leaderboard.csv"
SIMBENCH_LEADERBOARD = HIST_TABLES / "real_simbench_v7_leaderboard.csv"
FIXED_SIGNIFICANCE = HIST_TABLES / "real_p2_v7_significance.csv"
PAIRED_SENSITIVITY = HIST_TABLES / "real_p2_paired_sensitivity_v2.csv"
EXACT_RESULTS = HIST_RUNS / "real_ausgrid_exact_hierarchy_v8_results.csv"
EXACT_LEADERBOARD = HIST_TABLES / "real_ausgrid_exact_hierarchy_v8_leaderboard.csv"
EXACT_SIGNIFICANCE = HIST_TABLES / "real_ausgrid_exact_hierarchy_v8_significance.csv"

OPSD_RAW = [
    HIST_RUNS / "real_opsd_hyg_neural_results.csv",
    HIST_RUNS / "real_opsd_neural_results.csv",
    HIST_RUNS / "real_opsd_v7_extra_seed_results.csv",
]
SIMBENCH_RAW = [
    HIST_RUNS / "real_simbench_hyg_neural_results.csv",
    HIST_RUNS / "real_simbench_neural_results.csv",
    HIST_RUNS / "real_simbench_v7_extra_seed_results.csv",
]


METHOD_NAMES = {
    "HyG-LoadFormer (neural)": "CSA-LoadNet",
    "CSA-Poincare-Shared": "CSA-LoadNet",
    "TargetSelfContext-Matched": "Target-self context",
    "UniformCrossSeries-Matched": "Uniform cross-series",
    "CSA-Euclidean-Shared": "Euclidean weights",
    "CSA-FixedScale-Shared": "Fixed distance scale",
    "CSA-Poincare-IndependentEncoder": "Independent encoders",
    "Ablation-TemporalOnly (neural)": "TemporalOnly (smaller head)",
    "Ablation-EuclideanGraph (neural)": "Euclidean weights",
    "Ablation-EqualNeighbors (neural)": "Uniform/equal-weight neighbors",
    "Ablation-FixedCurvature (neural)": "Fixed distance scale",
    "Ablation-NoCalendar (neural)": "No sequence-phase features",
}

ROLE_NAMES = {
    "proposed": "proposed",
    "baseline": "external baseline",
    "ablation": "historical ablation",
    "capacity_compute_matched_control": "matched control",
    "informative_cross_series_control": "matched control",
    "weight_form_control": "weight-form control",
    "shared_encoder_control": "encoder control",
}


BLUE = "#2A78D6"
BLUE_DARK = "#174F93"
BLUE_LIGHT = "#B9D5F5"
ORANGE = "#E18B2D"
RED = "#C83E3A"
RED_LIGHT = "#F2C3C1"
TEAL = "#178B87"
PURPLE = "#7655A6"
GRAY_DARK = "#4D4D4A"
GRAY = "#858580"
GRAY_LIGHT = "#D8D8D3"
GRAY_FILL = "#EEEEEB"
INK = "#222222"
MUTED = "#666662"
WHITE = "#FFFFFF"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: Sequence[dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def f(value: str | float | int | None) -> float:
    if value in (None, ""):
        return math.nan
    return float(value)


def i(value: str | float | int | None) -> int:
    return int(float(value or 0))


def fmt(value: float, digits: int = 8) -> str:
    if math.isnan(value):
        return ""
    return f"{value:.{digits}f}"


def mean(values: Iterable[float]) -> float:
    vals = list(values)
    return statistics.fmean(vals)


def stdev(values: Iterable[float]) -> float:
    vals = list(values)
    return statistics.stdev(vals) if len(vals) > 1 else 0.0


def normalize_method(value: str) -> str:
    return METHOD_NAMES.get(value, value)


def rank_rows(rows: list[dict[str, object]], value_key: str, rank_key: str = "rank") -> None:
    ordered = sorted(rows, key=lambda row: float(row[value_key]))
    for rank, row in enumerate(ordered, start=1):
        row[rank_key] = rank


def verify_accepted_manifest() -> dict[str, object]:
    manifest = json.loads(RUN_MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "completed":
        raise RuntimeError(f"accepted run is not completed: {RUN_MANIFEST}")
    if manifest.get("run_namespace") != RUN_ROOT.name:
        raise RuntimeError("run namespace does not match accepted directory")

    for relative, record in manifest["outputs"].items():
        target = RUN_ROOT / relative
        if not target.is_file():
            raise FileNotFoundError(f"manifest output missing: {target}")
        observed = sha256(target)
        checkout_normalized = False
        if observed != record["sha256"] and target.suffix.lower() == ".md":
            payload = target.read_bytes()
            checkout_normalized = sha256_bytes(payload.replace(b"\r\n", b"\n")) == record["sha256"]
        if observed != record["sha256"] and not checkout_normalized:
            raise RuntimeError(
                f"manifest hash mismatch for {relative}: {observed} != {record['sha256']}"
            )

    for name, expected in manifest["row_counts"].items():
        path = RUN_TABLES / ("run_results.csv" if name == "run_results" else f"{name}.csv")
        observed = len(read_csv(path))
        if observed != expected:
            raise RuntimeError(f"row-count mismatch for {path.name}: {observed} != {expected}")
    return manifest


def required_historical_sources() -> list[Path]:
    sources = [
        OPSD_LEADERBOARD,
        SIMBENCH_LEADERBOARD,
        FIXED_SIGNIFICANCE,
        PAIRED_SENSITIVITY,
        EXACT_RESULTS,
        EXACT_LEADERBOARD,
        EXACT_SIGNIFICANCE,
        *OPSD_RAW,
        *SIMBENCH_RAW,
    ]
    missing = [path for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError("historical boundary evidence missing: " + ", ".join(map(str, missing)))
    return sources


def build_rolling_controls() -> list[dict[str, object]]:
    leaderboard = read_csv(RUN_TABLES / "leaderboard.csv")
    comparisons = read_csv(RUN_TABLES / "paired_comparisons.csv")
    config = json.loads((RUN_ROOT / "config.json").read_text(encoding="utf-8"))
    roles = {model["name"]: model["role"] for model in config["models"]}
    comparison_map = {
        (row["control"], row["metric"]): row
        for row in comparisons
    }
    rows: list[dict[str, object]] = []
    for source in leaderboard:
        method_key = source["method"]
        mape_cmp = comparison_map.get((method_key, "mape"))
        wape_cmp = comparison_map.get((method_key, "wape"))
        rows.append(
            {
                "scope": "OPSD lead 24 rolling origins",
                "method": normalize_method(method_key),
                "method_role": ROLE_NAMES.get(roles[method_key], roles[method_key]),
                "origin_count": i(source["origin_count"]),
                "seeds_per_origin": len(config["training"]["seeds"]),
                "mean_mape": fmt(f(source["mean_mape"]), 10),
                "std_mape_across_origin_means": fmt(f(source["std_mape"]), 10),
                "mean_wape": fmt(f(source["mean_wape"]), 10),
                "std_wape_across_origin_means": fmt(f(source["std_wape"]), 10),
                "mape_rank_within_six_arm_family": i(source["mape_rank"]),
                "proposed_minus_control_mape": "" if not mape_cmp else mape_cmp["mean_difference_proposed_minus_control"],
                "mape_bootstrap_95_ci_lower": "" if not mape_cmp else mape_cmp["bootstrap_95_ci_lower"],
                "mape_bootstrap_95_ci_upper": "" if not mape_cmp else mape_cmp["bootstrap_95_ci_upper"],
                "mape_holm_p": "" if not mape_cmp else mape_cmp["holm_p_primary_family"],
                "proposed_minus_control_wape": "" if not wape_cmp else wape_cmp["mean_difference_proposed_minus_control"],
                "wape_raw_p": "" if not wape_cmp else wape_cmp["exact_sign_flip_p"],
                "relative_reduction_proposed_vs_control_pct": "" if not mape_cmp else fmt(-f(mape_cmp["relative_difference_percent"]), 6),
                "percentage_denominator": "" if not mape_cmp else f"{normalize_method(method_key)} mean MAPE",
                "dispersion_scope": "SD across 8 origin means after averaging 5 matched seeds within each origin",
            }
        )
    return sorted(rows, key=lambda row: int(row["mape_rank_within_six_arm_family"]))


def fixed_significance_map() -> dict[tuple[str, int, str], dict[str, str]]:
    result: dict[tuple[str, int, str], dict[str, str]] = {}
    for row in read_csv(FIXED_SIGNIFICANCE):
        opponent = row["comparison"].split(" vs ", 1)[1]
        result[(row["dataset"].lower(), i(row["horizon_hours"]), opponent)] = row
    return result


def build_fixed_split_summary() -> list[dict[str, object]]:
    sig = fixed_significance_map()
    source_rows = [row for row in read_csv(OPSD_LEADERBOARD) if i(row["horizon_hours"]) == 24]
    proposed = next(row for row in source_rows if row["method_role"] == "proposed")
    proposed_mean = f(proposed["mean_mape"])
    rows: list[dict[str, object]] = []
    for rank, source in enumerate(sorted(source_rows, key=lambda row: f(row["mean_mape"])), start=1):
        stat = sig.get(("opsd", 24, source["method"]))
        control_mean = f(source["mean_mape"])
        relative = (control_mean - proposed_mean) / control_mean * 100.0
        verdict = "proposed"
        holm_p = ""
        if stat:
            holm_p = stat["p_holm"]
            significant = stat["significant_005_holm"].lower() == "true"
            better = stat["proposed_better"].lower() == "true"
            verdict = "significant win" if significant and better else "significant loss" if significant else "not separable"
        rows.append(
            {
                "scope": "OPSD lead 24 fixed split",
                "method": normalize_method(source["method"]),
                "method_role": ROLE_NAMES.get(source["method_role"], source["method_role"]),
                "fixed_split_count": 1,
                "seeds_on_split": i(source["n_seeds"]),
                "mean_mape": source["mean_mape"],
                "std_mape_across_seeds_conditional_on_split": source["std_mape"],
                "rank_within_seven_method_decision_set": rank,
                "holm_p_vs_proposed": holm_p,
                "verdict_for_proposed": verdict,
                "relative_reduction_proposed_vs_method_pct": "" if source["method_role"] == "proposed" else fmt(relative, 6),
                "percentage_denominator": "" if source["method_role"] == "proposed" else f"{normalize_method(source['method'])} mean MAPE",
                "dispersion_scope": "SD across optimization seeds conditional on one fixed temporal split",
            }
        )
    return rows


def build_reconciliation_summary() -> list[dict[str, object]]:
    source_rows = read_csv(EXACT_LEADERBOARD)
    by_reconciliation: dict[str, list[dict[str, object]]] = defaultdict(list)
    for source in source_rows:
        row: dict[str, object] = {
            "scope": "Ausgrid exact 12-leaf/4-region/system hierarchy, lead 24 fixed split",
            "method": normalize_method(source["method"]),
            "method_role": ROLE_NAMES.get(source["method_role"], source["method_role"]),
            "reconciliation": source["reconciliation"].replace("OLS-Reconciled", "OLS"),
            "fixed_split_count": 1,
            "seeds_on_split": i(source["runs"]),
            "mean_hierarchy_weighted_smape": source["mean_hierarchy_weighted_smape"],
            "std_hierarchy_weighted_smape_across_seeds_conditional_on_split": source["std_hierarchy_weighted_smape"],
            "mean_coherence_violation": source["mean_coherence_violation"],
            "mean_leaf_smape": source["mean_leaf_smape"],
            "mean_region_smape": source["mean_region_smape"],
            "mean_system_smape": source["mean_system_smape"],
            "dispersion_scope": "SD across optimization seeds conditional on one fixed temporal split",
        }
        by_reconciliation[str(row["reconciliation"])].append(row)
    result: list[dict[str, object]] = []
    order = {"Base": 0, "Bottom-Up": 1, "Top-Down": 2, "OLS": 3}
    for reconciliation, rows in by_reconciliation.items():
        rank_rows(rows, "mean_hierarchy_weighted_smape", "rank_within_reconciliation")
        result.extend(rows)
    return sorted(result, key=lambda row: (order[str(row["reconciliation"])], int(row["rank_within_reconciliation"])))


def build_rank_table(
    rolling: list[dict[str, object]],
    reconciliation: list[dict[str, object]],
) -> list[dict[str, object]]:
    settings: list[tuple[str, str, list[dict[str, str]], str, str, int, str]] = []
    opsd = read_csv(OPSD_LEADERBOARD)
    simbench = read_csv(SIMBENCH_LEADERBOARD)
    settings.extend(
        [
            ("OPSD lead 1 fixed split", "MAPE", [r for r in opsd if i(r["horizon_hours"]) == 1], "mean_mape", "method", 10, "seed means conditional on one fixed split"),
            ("OPSD lead 24 fixed split", "MAPE", [r for r in opsd if i(r["horizon_hours"]) == 24], "mean_mape", "method", 10, "seed means conditional on one fixed split"),
            ("SimBench lead 1 fixed split", "normalized MAE", [r for r in simbench if i(r["horizon_hours"]) == 1], "mean_normalized_mae", "method", 10, "seed means conditional on one fixed split"),
            ("SimBench lead 24 fixed split", "normalized MAE", [r for r in simbench if i(r["horizon_hours"]) == 24], "mean_normalized_mae", "method", 10, "seed means conditional on one fixed split"),
        ]
    )
    result: list[dict[str, object]] = []
    for setting, metric, source_rows, value_key, method_key, seed_count, uncertainty in settings:
        ordered = sorted(source_rows, key=lambda row: f(row[value_key]))
        denominator = len(ordered)
        for rank, row in enumerate(ordered, start=1):
            result.append(
                {
                    "setting": setting,
                    "metric": metric,
                    "method": normalize_method(row[method_key]),
                    "mean_error": row[value_key],
                    "rank": rank,
                    "rank_denominator": denominator,
                    "outer_analysis_units": 1,
                    "seeds_per_outer_unit": seed_count,
                    "uncertainty_scope": uncertainty,
                }
            )

    for row in rolling:
        result.append(
            {
                "setting": "OPSD lead 24 rolling origins",
                "metric": "MAPE",
                "method": row["method"],
                "mean_error": row["mean_mape"],
                "rank": row["mape_rank_within_six_arm_family"],
                "rank_denominator": 6,
                "outer_analysis_units": 8,
                "seeds_per_outer_unit": 5,
                "uncertainty_scope": "origin means after averaging matched seeds within origin",
            }
        )

    ols_rows = [row for row in reconciliation if row["reconciliation"] == "OLS"]
    for row in ols_rows:
        result.append(
            {
                "setting": "Ausgrid lead 24 exact hierarchy with OLS",
                "metric": "hierarchy-weighted sMAPE",
                "method": row["method"],
                "mean_error": row["mean_hierarchy_weighted_smape"],
                "rank": row["rank_within_reconciliation"],
                "rank_denominator": len(ols_rows),
                "outer_analysis_units": 1,
                "seeds_per_outer_unit": 10,
                "uncertainty_scope": "seed means conditional on one fixed split",
            }
        )
    setting_order = {
        "OPSD lead 1 fixed split": 0,
        "OPSD lead 24 fixed split": 1,
        "OPSD lead 24 rolling origins": 2,
        "SimBench lead 1 fixed split": 3,
        "SimBench lead 24 fixed split": 4,
        "Ausgrid lead 24 exact hierarchy with OLS": 5,
    }
    return sorted(result, key=lambda row: (setting_order[str(row["setting"])], int(row["rank"])))


def build_percentage_denominators(
    fixed: list[dict[str, object]],
    rolling: list[dict[str, object]],
    reconciliation: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(
        setting: str,
        comparator: str,
        proposed_error: float,
        comparator_error: float,
        analysis_unit: str,
        count: int,
        seeds: int,
        inference_scope: str,
    ) -> None:
        numerator = comparator_error - proposed_error
        rows.append(
            {
                "setting": setting,
                "comparison": f"CSA-LoadNet vs {comparator}",
                "percentage_definition": "100 * (comparator mean error - proposed mean error) / comparator mean error",
                "numerator_comparator_minus_proposed": fmt(numerator, 10),
                "denominator_comparator_mean_error": fmt(comparator_error, 10),
                "relative_reduction_percent_positive_favors_proposed": fmt(100.0 * numerator / comparator_error, 6),
                "analysis_unit": analysis_unit,
                "analysis_unit_count": count,
                "seeds_per_analysis_unit": seeds,
                "inference_scope": inference_scope,
            }
        )

    fixed_map = {str(row["method"]): row for row in fixed}
    fixed_prop = f(fixed_map["CSA-LoadNet"]["mean_mape"])
    for comparator in ["MLP", "TemporalOnly (smaller head)"]:
        add(
            "OPSD lead 24 fixed split",
            comparator,
            fixed_prop,
            f(fixed_map[comparator]["mean_mape"]),
            "fixed temporal split",
            1,
            10,
            "seed dispersion and seed-level tests are conditional on the fixed split",
        )

    rolling_map = {str(row["method"]): row for row in rolling}
    rolling_prop = f(rolling_map["CSA-LoadNet"]["mean_mape"])
    for comparator in [
        "Target-self context",
        "Uniform cross-series",
        "Euclidean weights",
        "Fixed distance scale",
        "Independent encoders",
    ]:
        add(
            "OPSD lead 24 rolling origins",
            comparator,
            rolling_prop,
            f(rolling_map[comparator]["mean_mape"]),
            "rolling temporal origin",
            8,
            5,
            "five matched seeds are averaged within each origin before origin-level inference",
        )

    ols_map = {str(row["method"]): row for row in reconciliation if row["reconciliation"] == "OLS"}
    add(
        "Ausgrid lead 24 exact hierarchy with OLS",
        "DLinear",
        f(ols_map["CSA-LoadNet"]["mean_hierarchy_weighted_smape"]),
        f(ols_map["DLinear"]["mean_hierarchy_weighted_smape"]),
        "fixed temporal split",
        1,
        10,
        "seed dispersion and seed-level tests are conditional on the fixed split",
    )
    return rows


def build_rolling_stability() -> list[dict[str, object]]:
    run_rows = read_csv(RUN_TABLES / "run_results.csv")
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    config = json.loads((RUN_ROOT / "config.json").read_text(encoding="utf-8"))
    origin_order = {
        timestamp: index
        for index, timestamp in enumerate(config["forecast"]["rolling_origin_timestamps_utc"])
    }
    for row in run_rows:
        grouped[(row["method"], row["rolling_origin"])].append(row)

    prepared: list[dict[str, object]] = []
    by_origin: dict[int, list[dict[str, object]]] = defaultdict(list)
    for (method_key, rolling_origin), rows in grouped.items():
        origin_index = origin_order[rolling_origin]
        mape_values = [f(row["mape"]) for row in rows]
        wape_values = [f(row["wape"]) for row in rows]
        item: dict[str, object] = {
            "rolling_origin_index": origin_index,
            "rolling_origin_utc": rolling_origin,
            "rolling_origin_processed_row_index": i(rows[0]["rolling_origin_index"]),
            "method": normalize_method(method_key),
            "seed_count": len(rows),
            "mean_mape_within_origin": fmt(mean(mape_values), 10),
            "std_mape_across_seeds_conditional_on_origin": fmt(stdev(mape_values), 10),
            "mean_wape_within_origin": fmt(mean(wape_values), 10),
            "std_wape_across_seeds_conditional_on_origin": fmt(stdev(wape_values), 10),
            "dispersion_scope": "SD across optimization seeds conditional on this rolling-origin split",
        }
        prepared.append(item)
        by_origin[origin_index].append(item)
    for rows in by_origin.values():
        rank_rows(rows, "mean_mape_within_origin", "mape_rank_within_origin")
    return sorted(prepared, key=lambda row: (int(row["rolling_origin_index"]), int(row["mape_rank_within_origin"])))


def deduplicated_raw(paths: Sequence[Path]) -> list[dict[str, str]]:
    records: dict[tuple[str, int, int], dict[str, str]] = {}
    for path in paths:
        for row in read_csv(path):
            key = (row["method"], i(row["horizon_hours"]), i(row["seed"]))
            records[key] = row
    return list(records.values())


def build_runtime_accuracy() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for dataset, paths, metric in [
        ("OPSD", OPSD_RAW, "mape"),
        ("SimBench", SIMBENCH_RAW, "normalized_mae"),
    ]:
        grouped: dict[tuple[int, str], list[dict[str, str]]] = defaultdict(list)
        for row in deduplicated_raw(paths):
            grouped[(i(row["horizon_hours"]), row["method"])].append(row)
        for (horizon, method_key), records in grouped.items():
            rows.append(
                {
                    "dataset": dataset,
                    "horizon_positions": horizon,
                    "method": normalize_method(method_key),
                    "method_role": ROLE_NAMES.get(records[0]["method_role"], records[0]["method_role"]),
                    "seed_count": len(records),
                    "mean_runtime_seconds": fmt(mean(f(row["runtime_s"]) for row in records), 6),
                    "primary_metric": "MAPE" if metric == "mape" else "normalized MAE",
                    "mean_primary_error": fmt(mean(f(row[metric]) for row in records), 10),
                    "runtime_scope": "within recorded dataset and execution environment only",
                }
            )

    exact_grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(EXACT_RESULTS):
        if row["reconciliation"] == "OLS-Reconciled":
            exact_grouped[row["method"]].append(row)
    for method_key, records in exact_grouped.items():
        rows.append(
            {
                "dataset": "Ausgrid exact hierarchy",
                "horizon_positions": 24,
                "method": normalize_method(method_key),
                "method_role": ROLE_NAMES.get(records[0]["method_role"], records[0]["method_role"]),
                "seed_count": len(records),
                "mean_runtime_seconds": fmt(mean(f(row["runtime_s"]) for row in records), 6),
                "primary_metric": "hierarchy-weighted sMAPE",
                "mean_primary_error": fmt(mean(f(row["hierarchy_weighted_smape"]) for row in records), 10),
                "runtime_scope": "within recorded dataset and execution environment only",
            }
        )
    return sorted(rows, key=lambda row: (str(row["dataset"]), int(row["horizon_positions"]), str(row["method"])))


def paired_values(
    records: Sequence[dict[str, str]],
    horizon: int,
    proposed_key: str,
    comparator_key: str,
    metric: str,
) -> list[float]:
    index = {
        (row["method"], i(row["horizon_hours"]), i(row["seed"])): f(row[metric])
        for row in records
    }
    seeds = sorted(
        seed for method, hz, seed in index
        if method == proposed_key and hz == horizon and (comparator_key, horizon, seed) in index
    )
    return [
        100.0 * (index[(comparator_key, horizon, seed)] - index[(proposed_key, horizon, seed)])
        / index[(comparator_key, horizon, seed)]
        for seed in seeds
    ]


def build_effect_summary(rolling_stability: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def append(setting: str, comparator: str, values: list[float], unit: str, scope: str) -> None:
        rows.append(
            {
                "setting": setting,
                "comparison": f"CSA-LoadNet vs {comparator}",
                "paired_relative_reduction_mean_pct": fmt(mean(values), 6),
                "paired_relative_reduction_std_pct": fmt(stdev(values), 6),
                "paired_unit_count": len(values),
                "paired_unit": unit,
                "percentage_denominator": "comparator error in the same paired unit",
                "uncertainty_scope": scope,
            }
        )

    opsd_records = deduplicated_raw(OPSD_RAW)
    simbench_records = deduplicated_raw(SIMBENCH_RAW)
    append(
        "OPSD lead 1 fixed split", "MLP",
        paired_values(opsd_records, 1, "HyG-LoadFormer (neural)", "MLP", "mape"),
        "seed", "seed variation conditional on one fixed split",
    )
    append(
        "OPSD lead 24 fixed split", "MLP",
        paired_values(opsd_records, 24, "HyG-LoadFormer (neural)", "MLP", "mape"),
        "seed", "seed variation conditional on one fixed split",
    )
    append(
        "SimBench lead 1 fixed split", "MLP",
        paired_values(simbench_records, 1, "HyG-LoadFormer (neural)", "MLP", "normalized_mae"),
        "seed", "seed variation conditional on one fixed split",
    )
    append(
        "SimBench lead 24 fixed split", "MLP",
        paired_values(simbench_records, 24, "HyG-LoadFormer (neural)", "MLP", "normalized_mae"),
        "seed", "seed variation conditional on one fixed split",
    )

    rolling_by_origin_method = {
        (i(row["rolling_origin_index"]), str(row["method"])): f(row["mean_mape_within_origin"])
        for row in rolling_stability
    }
    rolling_values = []
    for origin in range(8):
        proposed = rolling_by_origin_method[(origin, "CSA-LoadNet")]
        comparator = rolling_by_origin_method[(origin, "Target-self context")]
        rolling_values.append(100.0 * (comparator - proposed) / comparator)
    append(
        "OPSD lead 24 rolling origins", "Target-self context", rolling_values,
        "rolling origin after seed averaging", "variation across 8 origins; 5 matched seeds averaged within origin",
    )

    exact_rows = [row for row in read_csv(EXACT_RESULTS) if row["reconciliation"] == "OLS-Reconciled"]
    exact_index = {(row["method"], i(row["seed"])): f(row["hierarchy_weighted_smape"]) for row in exact_rows}
    exact_values = [
        100.0 * (exact_index[("DLinear", seed)] - exact_index[("HyG-LoadFormer (neural)", seed)])
        / exact_index[("DLinear", seed)]
        for seed in sorted(seed for method, seed in exact_index if method == "DLinear")
    ]
    append(
        "Ausgrid lead 24 exact hierarchy with OLS", "DLinear", exact_values,
        "seed", "seed variation conditional on one fixed split",
    )
    return rows


@dataclass
class Shape:
    kind: str
    values: tuple[object, ...]


class Chart:
    def __init__(self, width: int, height: int, background: str = WHITE) -> None:
        self.width = width
        self.height = height
        self.background = background
        self.shapes: list[Shape] = []

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str = "none", sw: float = 1) -> None:
        self.shapes.append(Shape("rect", (x, y, w, h, fill, stroke, sw)))

    def line(self, x1: float, y1: float, x2: float, y2: float, stroke: str = INK, sw: float = 2, dash: tuple[int, ...] | None = None) -> None:
        self.shapes.append(Shape("line", (x1, y1, x2, y2, stroke, sw, dash)))

    def circle(self, x: float, y: float, radius: float, fill: str, stroke: str = "none", sw: float = 1) -> None:
        self.shapes.append(Shape("circle", (x, y, radius, fill, stroke, sw)))

    def text(self, x: float, y: float, value: str, size: int = 28, fill: str = INK, anchor: str = "start", weight: str = "normal") -> None:
        self.shapes.append(Shape("text", (x, y, value, size, fill, anchor, weight)))

    @staticmethod
    def _font(size: int, weight: str) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        candidates = [
            Path("C:/Windows/Fonts/arialbd.ttf") if weight == "bold" else Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/calibrib.ttf") if weight == "bold" else Path("C:/Windows/Fonts/calibri.ttf"),
        ]
        for path in candidates:
            if path.is_file():
                return ImageFont.truetype(str(path), size=size)
        return ImageFont.load_default()

    def save_png(self, path: Path) -> None:
        image = Image.new("RGB", (self.width, self.height), self.background)
        draw = ImageDraw.Draw(image)
        for shape in self.shapes:
            if shape.kind == "rect":
                x, y, w, h, fill, stroke, sw = shape.values
                draw.rectangle((x, y, x + w, y + h), fill=fill, outline=None if stroke == "none" else stroke, width=max(1, int(sw)))
            elif shape.kind == "line":
                x1, y1, x2, y2, stroke, sw, dash = shape.values
                if dash:
                    length = math.hypot(x2 - x1, y2 - y1)
                    if length:
                        ux, uy = (x2 - x1) / length, (y2 - y1) / length
                        position = 0.0
                        draw_on = True
                        index = 0
                        while position < length:
                            step = min(float(dash[index % len(dash)]), length - position)
                            if draw_on:
                                draw.line((x1 + ux * position, y1 + uy * position, x1 + ux * (position + step), y1 + uy * (position + step)), fill=stroke, width=max(1, int(sw)))
                            position += step
                            draw_on = not draw_on
                            index += 1
                else:
                    draw.line((x1, y1, x2, y2), fill=stroke, width=max(1, int(sw)))
            elif shape.kind == "circle":
                x, y, radius, fill, stroke, sw = shape.values
                draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=fill, outline=None if stroke == "none" else stroke, width=max(1, int(sw)))
            elif shape.kind == "text":
                x, y, value, size, fill, anchor, weight = shape.values
                font = self._font(int(size), str(weight))
                lines = str(value).split("\n")
                line_height = int(size * 1.18)
                for line_index, line in enumerate(lines):
                    bbox = draw.textbbox((0, 0), line, font=font)
                    width = bbox[2] - bbox[0]
                    tx = float(x) - width / 2 if anchor == "middle" else float(x) - width if anchor == "end" else float(x)
                    draw.text((tx, float(y) + line_index * line_height), line, font=font, fill=fill)
        image.save(path, dpi=(300, 300), optimize=True)

    def save_svg(self, path: Path) -> None:
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
            f'<rect width="100%" height="100%" fill="{self.background}"/>',
        ]
        for shape in self.shapes:
            if shape.kind == "rect":
                x, y, w, h, fill, stroke, sw = shape.values
                parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
            elif shape.kind == "line":
                x1, y1, x2, y2, stroke, sw, dash = shape.values
                dash_attr = "" if not dash else f' stroke-dasharray="{",".join(map(str, dash))}"'
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{dash_attr}/>')
            elif shape.kind == "circle":
                x, y, radius, fill, stroke, sw = shape.values
                parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
            elif shape.kind == "text":
                x, y, value, size, fill, anchor, weight = shape.values
                escaped_lines = [html.escape(line) for line in str(value).split("\n")]
                parts.append(f'<text x="{x}" y="{float(y) + int(size)}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">')
                for index, line in enumerate(escaped_lines):
                    dy = 0 if index == 0 else int(size * 1.18)
                    parts.append(f'<tspan x="{x}" dy="{dy}">{line}</tspan>')
                parts.append("</text>")
        parts.append("</svg>")
        path.write_text("\n".join(parts) + "\n", encoding="utf-8")

    def save_pdf(self, path: Path) -> None:
        scale = 72.0 / 300.0
        pdf = pdfcanvas.Canvas(str(path), pagesize=(self.width * scale, self.height * scale), invariant=1, pageCompression=1)
        pdf.setFillColor(self.background)
        pdf.rect(0, 0, self.width * scale, self.height * scale, fill=1, stroke=0)

        def color(value: str) -> None:
            pdf.setFillColor(value)
            pdf.setStrokeColor(value)

        for shape in self.shapes:
            if shape.kind == "rect":
                x, y, w, h, fill, stroke, sw = shape.values
                pdf.setFillColor(fill)
                pdf.setStrokeColor(fill if stroke == "none" else stroke)
                pdf.setLineWidth(float(sw) * scale)
                pdf.rect(float(x) * scale, (self.height - float(y) - float(h)) * scale, float(w) * scale, float(h) * scale, fill=1, stroke=0 if stroke == "none" else 1)
            elif shape.kind == "line":
                x1, y1, x2, y2, stroke, sw, dash = shape.values
                pdf.setStrokeColor(stroke)
                pdf.setLineWidth(float(sw) * scale)
                pdf.setDash(list(dash) if dash else [])
                pdf.line(float(x1) * scale, (self.height - float(y1)) * scale, float(x2) * scale, (self.height - float(y2)) * scale)
                pdf.setDash([])
            elif shape.kind == "circle":
                x, y, radius, fill, stroke, sw = shape.values
                pdf.setFillColor(fill)
                pdf.setStrokeColor(fill if stroke == "none" else stroke)
                pdf.setLineWidth(float(sw) * scale)
                pdf.circle(float(x) * scale, (self.height - float(y)) * scale, float(radius) * scale, fill=1, stroke=0 if stroke == "none" else 1)
            elif shape.kind == "text":
                x, y, value, size, fill, anchor, weight = shape.values
                font_name = "Helvetica-Bold" if weight == "bold" else "Helvetica"
                pdf.setFont(font_name, float(size) * scale)
                pdf.setFillColor(fill)
                for line_index, line in enumerate(str(value).split("\n")):
                    width = pdf.stringWidth(line, font_name, float(size) * scale)
                    tx = float(x) * scale - width / 2 if anchor == "middle" else float(x) * scale - width if anchor == "end" else float(x) * scale
                    ty = (self.height - float(y) - float(size) - line_index * float(size) * 1.18) * scale
                    pdf.drawString(tx, ty, line)
        pdf.showPage()
        pdf.save()

    def save_all(self, stem: str) -> None:
        self.save_png(FIG_DIR / f"{stem}.png")
        self.save_svg(FIG_DIR / f"{stem}.svg")
        self.save_pdf(FIG_DIR / f"{stem}.pdf")


def draw_horizontal_bars(
    chart: Chart,
    rows: Sequence[dict[str, object]],
    x: int,
    y: int,
    width: int,
    height: int,
    value_key: str,
    error_key: str,
    title: str,
    xlabel: str,
    max_value: float,
    proposed_label: str = "CSA-LoadNet",
) -> None:
    label_width = int(width * 0.38)
    plot_x = x + label_width
    plot_width = width - label_width - 30
    chart.text(x + width / 2, y, title, size=31, anchor="middle", weight="bold")
    top = y + 62
    row_height = (height - 120) / max(1, len(rows))
    chart.line(plot_x, top, plot_x, y + height - 48, GRAY, 2)
    for tick in range(5):
        value = max_value * tick / 4
        tx = plot_x + plot_width * tick / 4
        chart.line(tx, top, tx, y + height - 48, GRAY_LIGHT, 1)
        chart.text(tx, y + height - 40, f"{value:.3f}", size=21, anchor="middle", fill=MUTED)
    for index, row in enumerate(rows):
        cy = top + index * row_height + row_height / 2
        method = str(row["method"])
        value = f(row[value_key])
        error = f(row[error_key])
        color = BLUE if method == proposed_label else GRAY
        edge = BLUE_DARK if method == proposed_label else GRAY_DARK
        bar_width = plot_width * value / max_value
        chart.text(plot_x - 16, cy - 14, method, size=23, anchor="end", weight="bold" if method == proposed_label else "normal")
        chart.rect(plot_x, cy - 17, bar_width, 34, color, edge, 2)
        err_width = plot_width * error / max_value
        chart.line(plot_x + bar_width - err_width, cy, plot_x + bar_width + err_width, cy, GRAY_DARK, 2)
        chart.line(plot_x + bar_width - err_width, cy - 8, plot_x + bar_width - err_width, cy + 8, GRAY_DARK, 2)
        chart.line(plot_x + bar_width + err_width, cy - 8, plot_x + bar_width + err_width, cy + 8, GRAY_DARK, 2)
        chart.text(min(plot_x + bar_width + err_width + 10, x + width - 10), cy - 13, f"{value:.5f}", size=20, fill=MUTED)
    chart.text(plot_x + plot_width / 2, y + height - 4, xlabel, size=24, anchor="middle")


def figure_leaderboards(fixed: list[dict[str, object]], rolling: list[dict[str, object]]) -> None:
    chart = Chart(2200, 1120)
    draw_horizontal_bars(
        chart, fixed, 40, 40, 1040, 930,
        "mean_mape", "std_mape_across_seeds_conditional_on_split",
        "(a) One fixed split", "MAPE; mean +/- seed SD conditional on split", 0.040,
    )
    draw_horizontal_bars(
        chart, rolling, 1120, 40, 1040, 930,
        "mean_mape", "std_mape_across_origin_means",
        "(b) Eight rolling origins", "MAPE; mean +/- SD across origin means", 0.050,
    )
    chart.text(
        1100, 1030,
        "Fixed split: 10 seeds per method. Rolling origins: 5 matched seeds averaged inside each of 8 origins.",
        size=27, anchor="middle", fill=MUTED,
    )
    chart.save_all("fig_leaderboard")


def verdict_cell(significant: bool, proposed_better: bool) -> tuple[str, str, str]:
    if significant and proposed_better:
        return "win", BLUE_LIGHT, BLUE_DARK
    if significant and not proposed_better:
        return "loss", RED_LIGHT, RED
    return "n.s.", GRAY_FILL, MUTED


def figure_component_matrix() -> None:
    historic = fixed_significance_map()
    rolling = {
        row["control"]: row
        for row in read_csv(RUN_TABLES / "paired_comparisons.csv")
        if row["metric"] == "mape"
    }
    exact = {
        row["comparison"].split(" vs ", 1)[1]: row
        for row in read_csv(EXACT_SIGNIFICANCE)
    }
    columns = [
        ("OPSD\nlead 1\nfixed", "fixed", "opsd", 1),
        ("OPSD\nlead 24\nfixed", "fixed", "opsd", 24),
        ("OPSD\nlead 24\nrolling", "rolling", "opsd", 24),
        ("SimBench\nlead 1\nfixed", "fixed", "simbench", 1),
        ("SimBench\nlead 24\nfixed", "fixed", "simbench", 24),
        ("Ausgrid\nlead 24\nOLS", "exact", "ausgrid", 24),
    ]
    opponents = [
        ("MLP", "MLP", "MLP"),
        ("Target-self context", None, "TargetSelfContext-Matched"),
        ("TemporalOnly (smaller head)", "Ablation-TemporalOnly (neural)", None),
        ("Uniform/equal-weight neighbors", "Ablation-EqualNeighbors (neural)", "UniformCrossSeries-Matched"),
        ("Euclidean weights", "Ablation-EuclideanGraph (neural)", "CSA-Euclidean-Shared"),
        ("Fixed distance scale", "Ablation-FixedCurvature (neural)", "CSA-FixedScale-Shared"),
    ]
    chart = Chart(2050, 1120)
    left, top, cell_w, cell_h = 530, 200, 240, 125
    chart.text(1025, 35, "Corrected proposed-versus-control decisions by evidence scope", size=36, anchor="middle", weight="bold")
    for col, (label, _, _, _) in enumerate(columns):
        chart.text(left + col * cell_w + cell_w / 2, 90, label, size=24, anchor="middle", weight="bold")
    for row_index, (label, historical_key, rolling_key) in enumerate(opponents):
        cy = top + row_index * cell_h
        chart.text(left - 24, cy + 39, label, size=25, anchor="end")
        for col, (_, kind, dataset, horizon) in enumerate(columns):
            record: dict[str, str] | None = None
            p_value = math.nan
            proposed_better = False
            significant = False
            if kind == "fixed" and historical_key:
                record = historic.get((dataset, horizon, historical_key))
                if record:
                    p_value = f(record["p_holm"])
                    proposed_better = record["proposed_better"].lower() == "true"
                    significant = record["significant_005_holm"].lower() == "true"
            elif kind == "rolling" and rolling_key:
                record = rolling.get(rolling_key)
                if record:
                    p_value = f(record["holm_p_primary_family"])
                    proposed_better = f(record["mean_difference_proposed_minus_control"]) < 0
                    significant = p_value < 0.05
            elif kind == "exact" and historical_key:
                record = exact.get(historical_key)
                if record:
                    p_value = f(record["p_holm"])
                    proposed_better = record["verdict"] == "win"
                    significant = record["significant_005_holm"].lower() == "true"

            x = left + col * cell_w
            if not record:
                chart.rect(x + 8, cy + 8, cell_w - 16, cell_h - 16, WHITE, GRAY_LIGHT, 2)
                chart.text(x + cell_w / 2, cy + 43, "not run", size=21, anchor="middle", fill=MUTED)
                continue
            verdict, fill, text_color = verdict_cell(significant, proposed_better)
            chart.rect(x + 8, cy + 8, cell_w - 16, cell_h - 16, fill, text_color, 3 if significant else 2)
            chart.text(x + cell_w / 2, cy + 24, verdict, size=27, anchor="middle", weight="bold" if significant else "normal", fill=text_color)
            p_text = "Holm p = 1" if p_value >= 0.9995 else f"Holm p = {p_value:.4g}"
            chart.text(x + cell_w / 2, cy + 65, p_text, size=20, anchor="middle", fill=MUTED)
    chart.text(1025, 1010, "Fixed-split cells use seed-level Mann-Whitney tests; rolling cells use exact sign-flip tests over 8 origin means.", size=24, anchor="middle", fill=MUTED)
    chart.save_all("fig_component")


def figure_ausgrid(reconciliation: list[dict[str, object]]) -> None:
    rows = sorted([row for row in reconciliation if row["reconciliation"] == "OLS"], key=lambda row: f(row["mean_hierarchy_weighted_smape"]), reverse=False)
    chart = Chart(1600, 1220)
    draw_horizontal_bars(
        chart, rows, 35, 30, 1530, 1080,
        "mean_hierarchy_weighted_smape",
        "std_hierarchy_weighted_smape_across_seeds_conditional_on_split",
        "Exact hierarchy under common OLS reconciliation",
        "Hierarchy-weighted sMAPE; mean +/- seed SD conditional on fixed split",
        0.34,
    )
    chart.text(800, 1155, "DLinear ranks first; CSA-LoadNet ranks sixth of 11 methods (Holm p = 0.000985, proposed method loses).", size=24, anchor="middle", fill=MUTED)
    chart.save_all("fig_ausgrid")


def figure_rolling_stability(rows: list[dict[str, object]]) -> None:
    selected = [
        "Fixed distance scale", "CSA-LoadNet", "Euclidean weights",
        "Uniform cross-series", "Target-self context", "Independent encoders",
    ]
    colors = [ORANGE, BLUE, TEAL, PURPLE, GRAY_DARK, RED]
    chart = Chart(1900, 1000)
    left, top, width, height = 170, 110, 1570, 700
    chart.text(950, 28, "Accepted rolling-origin OPSD lead-24 MAPE profiles", size=36, anchor="middle", weight="bold")
    y_min, y_max = 0.018, 0.060
    for tick in range(8):
        value = y_min + (y_max - y_min) * tick / 7
        py = top + height - height * (value - y_min) / (y_max - y_min)
        chart.line(left, py, left + width, py, GRAY_LIGHT, 1)
        chart.text(left - 18, py - 12, f"{value:.3f}", size=21, anchor="end", fill=MUTED)
    chart.line(left, top, left, top + height, GRAY, 2)
    chart.line(left, top + height, left + width, top + height, GRAY, 2)
    by_method: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_method[str(row["method"])].append(row)
    for method, color in zip(selected, colors):
        method_rows = sorted(by_method[method], key=lambda row: i(row["rolling_origin_index"]))
        previous: tuple[float, float] | None = None
        for row in method_rows:
            origin = i(row["rolling_origin_index"])
            value = f(row["mean_mape_within_origin"])
            px = left + width * origin / 7
            py = top + height - height * (value - y_min) / (y_max - y_min)
            if previous:
                chart.line(previous[0], previous[1], px, py, color, 4)
            chart.circle(px, py, 7, color, WHITE, 2)
            previous = (px, py)
        chart.line(left + 80 + selected.index(method) % 3 * 520, 865 + (selected.index(method) // 3) * 48, left + 125 + selected.index(method) % 3 * 520, 865 + (selected.index(method) // 3) * 48, color, 5)
        chart.text(left + 138 + selected.index(method) % 3 * 520, 850 + (selected.index(method) // 3) * 48, method, size=22)
    labels = ["2017-01", "2017-04", "2017-07", "2017-10", "2018-01", "2018-04", "2018-07", "2018-10"]
    for index, label in enumerate(labels):
        px = left + width * index / 7
        chart.text(px, top + height + 18, label, size=20, anchor="middle", fill=MUTED)
    chart.text(48, 440, "MAPE", size=26, weight="bold")
    chart.text(950, 960, "Each point averages five matched optimization seeds within that temporal origin.", size=23, anchor="middle", fill=MUTED)
    chart.save_all("fig_rolling_stability")


def figure_reconciliation(reconciliation: list[dict[str, object]]) -> None:
    methods = ["DLinear", "CSA-LoadNet"]
    regimes = ["Base", "Bottom-Up", "Top-Down", "OLS"]
    lookup = {(str(row["method"]), str(row["reconciliation"])): row for row in reconciliation}
    chart = Chart(2100, 1050)
    chart.text(1050, 30, "Accuracy and coherence under exact-hierarchy reconciliation", size=36, anchor="middle", weight="bold")
    panel_specs = [(90, "(a) Hierarchy-weighted sMAPE", 0.39, "mean_hierarchy_weighted_smape"), (1100, "(b) Mean structural violation", 0.05, "mean_coherence_violation")]
    for panel_x, title, max_value, key in panel_specs:
        left, top, width, height = panel_x + 80, 150, 820, 650
        chart.text(panel_x + 500, 92, title, size=29, anchor="middle", weight="bold")
        chart.line(left, top, left, top + height, GRAY, 2)
        chart.line(left, top + height, left + width, top + height, GRAY, 2)
        for tick in range(5):
            value = max_value * tick / 4
            py = top + height - height * value / max_value
            chart.line(left, py, left + width, py, GRAY_LIGHT, 1)
            chart.text(left - 14, py - 11, f"{value:.2f}", size=20, anchor="end", fill=MUTED)
        group_width = width / len(regimes)
        for regime_index, regime in enumerate(regimes):
            center = left + group_width * (regime_index + 0.5)
            for method_index, (method, color) in enumerate(zip(methods, [GRAY_DARK, BLUE])):
                row = lookup[(method, regime)]
                value = f(row[key])
                bar_width = 62
                bx = center + (method_index - 0.5) * 76 - bar_width / 2
                by = top + height - height * value / max_value
                chart.rect(bx, by, bar_width, top + height - by, color, BLUE_DARK if method == "CSA-LoadNet" else GRAY_DARK, 2)
                if key == "mean_hierarchy_weighted_smape":
                    error = f(row["std_hierarchy_weighted_smape_across_seeds_conditional_on_split"])
                    err = height * error / max_value
                    chart.line(bx + bar_width / 2, by - err, bx + bar_width / 2, by + err, INK, 2)
                    chart.line(bx + 20, by - err, bx + bar_width - 20, by - err, INK, 2)
                    chart.line(bx + 20, by + err, bx + bar_width - 20, by + err, INK, 2)
            chart.text(center, top + height + 18, regime, size=21, anchor="middle")
    chart.rect(780, 900, 34, 24, GRAY_DARK)
    chart.text(826, 895, "DLinear", size=23)
    chart.rect(1010, 900, 34, 24, BLUE)
    chart.text(1056, 895, "CSA-LoadNet", size=23)
    chart.text(1050, 980, "Means +/- seed SD are conditional on the same fixed split; all three reconciliation transforms are exactly coherent.", size=24, anchor="middle", fill=MUTED)
    chart.save_all("fig_exact_hierarchy_reconciliation")


def figure_effects(rows: list[dict[str, object]]) -> None:
    chart = Chart(1900, 1040)
    left, top, width, height = 520, 110, 1220, 730
    chart.text(950, 28, "Paired relative primary-error reduction", size=36, anchor="middle", weight="bold")
    x_min, x_max = -8.0, 8.0
    zero_x = left + width * (0 - x_min) / (x_max - x_min)
    chart.line(zero_x, top, zero_x, top + height, GRAY_DARK, 3)
    for tick in range(-8, 9, 2):
        px = left + width * (tick - x_min) / (x_max - x_min)
        chart.line(px, top, px, top + height, GRAY_LIGHT, 1)
        chart.text(px, top + height + 18, f"{tick}%", size=21, anchor="middle", fill=MUTED)
    row_height = height / len(rows)
    labels = {
        "OPSD lead 1 fixed split": "OPSD lead 1 fixed / MLP",
        "OPSD lead 24 fixed split": "OPSD lead 24 fixed / MLP",
        "OPSD lead 24 rolling origins": "OPSD lead 24 rolling / target-self",
        "SimBench lead 1 fixed split": "SimBench lead 1 fixed / MLP",
        "SimBench lead 24 fixed split": "SimBench lead 24 fixed / MLP",
        "Ausgrid lead 24 exact hierarchy with OLS": "Ausgrid OLS / DLinear",
    }
    for index, row in enumerate(rows):
        cy = top + row_height * (index + 0.5)
        value = f(row["paired_relative_reduction_mean_pct"])
        error = f(row["paired_relative_reduction_std_pct"])
        px = left + width * (value - x_min) / (x_max - x_min)
        low = left + width * (max(x_min, value - error) - x_min) / (x_max - x_min)
        high = left + width * (min(x_max, value + error) - x_min) / (x_max - x_min)
        color = BLUE if value > 0 else RED
        chart.text(left - 22, cy - 14, labels[str(row["setting"])], size=23, anchor="end")
        chart.line(low, cy, high, cy, GRAY_DARK, 3)
        chart.line(low, cy - 10, low, cy + 10, GRAY_DARK, 3)
        chart.line(high, cy - 10, high, cy + 10, GRAY_DARK, 3)
        chart.circle(px, cy, 12, color, WHITE, 2)
        chart.text(px + (18 if value >= 0 else -18), cy - 14, f"{value:+.2f}%", size=21, anchor="start" if value >= 0 else "end", fill=color, weight="bold")
    chart.text(1130, 900, "Positive values favor CSA-LoadNet; denominator = paired comparator error.", size=24, anchor="middle")
    chart.text(950, 946, "Fixed-split and hierarchy bars: seed mean +/- seed SD conditional on one split. Rolling bar: origin mean +/- origin SD after seed averaging.", size=22, anchor="middle", fill=MUTED)
    chart.save_all("fig_cross_dataset_effects")


def figure_ranks(rows: list[dict[str, object]]) -> None:
    settings = [
        "OPSD lead 1 fixed split",
        "OPSD lead 24 fixed split",
        "OPSD lead 24 rolling origins",
        "SimBench lead 1 fixed split",
        "SimBench lead 24 fixed split",
        "Ausgrid lead 24 exact hierarchy with OLS",
    ]
    short = ["OPSD\nlead 1\nfixed", "OPSD\nlead 24\nfixed", "OPSD\nlead 24\nrolling", "SimBench\nlead 1\nfixed", "SimBench\nlead 24\nfixed", "Ausgrid\nlead 24\nOLS"]
    methods = []
    preferred = [
        "DLinear", "PatchTST-lite", "MLP", "CSA-LoadNet", "Fixed distance scale",
        "Euclidean weights", "Uniform/equal-weight neighbors", "Uniform cross-series",
        "Target-self context", "Independent encoders", "TCN", "No sequence-phase features",
        "TemporalOnly (smaller head)", "LSTM",
    ]
    present = {str(row["method"]) for row in rows}
    for method in preferred + sorted(present - set(preferred)):
        if method in present and method not in methods:
            methods.append(method)
    lookup = {(str(row["setting"]), str(row["method"])): row for row in rows}
    chart = Chart(2150, 1380)
    left, top, cell_w, cell_h = 620, 190, 245, 72
    chart.text(1075, 25, "Ranks within each reported method roster", size=36, anchor="middle", weight="bold")
    for col, setting in enumerate(settings):
        denominator = max(i(row["rank_denominator"]) for row in rows if row["setting"] == setting)
        chart.text(left + col * cell_w + cell_w / 2, 78, short[col] + f"\n(n={denominator})", size=23, anchor="middle", weight="bold")
    for row_index, method in enumerate(methods):
        cy = top + row_index * cell_h
        chart.text(left - 22, cy + 18, method, size=23, anchor="end", weight="bold" if method == "CSA-LoadNet" else "normal")
        for col, setting in enumerate(settings):
            x = left + col * cell_w
            record = lookup.get((setting, method))
            if not record:
                chart.rect(x + 6, cy + 4, cell_w - 12, cell_h - 8, WHITE, GRAY_LIGHT, 1)
                chart.text(x + cell_w / 2, cy + 13, "-", size=25, anchor="middle", fill=MUTED)
                continue
            rank = i(record["rank"])
            denominator = i(record["rank_denominator"])
            intensity = (denominator - rank) / max(1, denominator - 1)
            fill = BLUE_LIGHT if rank == 1 else GRAY_FILL
            stroke = BLUE_DARK if method == "CSA-LoadNet" else GRAY_LIGHT
            chart.rect(x + 6, cy + 4, cell_w - 12, cell_h - 8, fill, stroke, 2)
            chart.text(x + cell_w / 2, cy + 11, f"{rank}/{denominator}", size=24, anchor="middle", weight="bold" if rank == 1 else "normal", fill=BLUE_DARK if rank == 1 else INK)
            _ = intensity
    chart.text(1075, 1295, "Ranks are local to each roster; missing methods are not imputed and no cross-metric average rank is formed.", size=24, anchor="middle", fill=MUTED)
    chart.save_all("fig_cross_setting_ranks")


def figure_compute_profile(runtime_rows: list[dict[str, object]]) -> None:
    proposed = [row for row in runtime_rows if row["method"] == "CSA-LoadNet"]
    labels = [f"{row['dataset']}\nlead {row['horizon_positions']}" for row in proposed]
    chart = Chart(1750, 920)
    left, top, width, height = 190, 130, 1370, 560
    chart.text(875, 28, "Recorded CSA-LoadNet runtime and dataset-specific primary error", size=34, anchor="middle", weight="bold")
    runtimes = [f(row["mean_runtime_seconds"]) for row in proposed]
    x_min, x_max = math.log10(min(runtimes) * 0.8), math.log10(max(runtimes) * 1.25)
    chart.line(left, top + height, left + width, top + height, GRAY, 2)
    for tick in [1, 2, 5, 10, 20]:
        if min(runtimes) * 0.8 <= tick <= max(runtimes) * 1.25:
            px = left + width * (math.log10(tick) - x_min) / (x_max - x_min)
            chart.line(px, top, px, top + height, GRAY_LIGHT, 1)
            chart.text(px, top + height + 16, f"{tick}s", size=21, anchor="middle", fill=MUTED)
    for index, row in enumerate(proposed):
        runtime = f(row["mean_runtime_seconds"])
        error = f(row["mean_primary_error"])
        px = left + width * (math.log10(runtime) - x_min) / (x_max - x_min)
        py = top + 70 + index * (height - 140) / max(1, len(proposed) - 1)
        chart.circle(px, py, 13, BLUE, WHITE, 2)
        chart.text(px + 20, py - 35, labels[index], size=20, fill=INK)
        chart.text(px + 20, py + 18, f"{row['primary_metric']}={error:.4f}", size=19, fill=MUTED)
    chart.text(875, 780, "Runtime axis is logarithmic. Primary-error values use different metrics and must not be compared vertically across datasets.", size=23, anchor="middle", fill=MUTED)
    chart.save_all("fig_compute_error_profile")


def write_tables(
    fixed: list[dict[str, object]],
    rolling: list[dict[str, object]],
    reconciliation: list[dict[str, object]],
    ranks: list[dict[str, object]],
    percentages: list[dict[str, object]],
    rolling_stability: list[dict[str, object]],
    runtime: list[dict[str, object]],
    effects: list[dict[str, object]],
) -> list[Path]:
    specs = [
        ("p2_fixed_split_summary.csv", fixed),
        ("p2_rolling_origin_controls.csv", rolling),
        ("p2_reconciliation_summary.csv", reconciliation),
        ("p2_cross_setting_ranks.csv", ranks),
        ("p2_percentage_denominators.csv", percentages),
        ("p2_rolling_stability.csv", rolling_stability),
        ("p2_runtime_accuracy.csv", runtime),
        ("p2_effect_summary.csv", effects),
    ]
    outputs: list[Path] = []
    for name, rows in specs:
        if not rows:
            raise RuntimeError(f"refusing to write empty derived table: {name}")
        path = DERIVED_DIR / name
        write_csv(path, rows, list(rows[0].keys()))
        outputs.append(path)
    return outputs


def write_artifact_manifest(
    accepted_manifest: dict[str, object],
    historical_sources: Sequence[Path],
    table_outputs: Sequence[Path],
) -> None:
    figure_outputs = sorted(
        path for path in FIG_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".png", ".pdf", ".svg"}
        and path.stem in {
            "fig_leaderboard", "fig_component", "fig_ausgrid", "fig_rolling_stability",
            "fig_exact_hierarchy_reconciliation", "fig_cross_dataset_effects",
            "fig_cross_setting_ranks", "fig_compute_error_profile",
        }
    )
    payload = {
        "artifact_namespace": "p2_s4_results_narrative",
        "accepted_run_namespace": accepted_manifest["run_namespace"],
        "accepted_run_manifest_sha256": sha256(RUN_MANIFEST),
        "accepted_run_status": accepted_manifest["status"],
        "source_scope": {
            "rolling_origin_controls": "accepted immutable run manifest and hashed outputs",
            "fixed_split_results": "historical fixed-split boundary evidence; seed uncertainty is conditional on one split",
            "exact_hierarchy_results": "historical exact-hierarchy boundary evidence under common reconciliation",
        },
        "percentage_definition": "100 * (comparator mean error - proposed mean error) / comparator mean error",
        "sources": {
            str(path.relative_to(HARNESS_ROOT)).replace("\\", "/"): sha256(path)
            for path in [RUN_MANIFEST, *historical_sources]
        },
        "outputs": {
            str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in sorted([*table_outputs, *figure_outputs])
        },
    }
    path = DERIVED_DIR / "p2_artifact_manifest.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    accepted_manifest = verify_accepted_manifest()
    historical_sources = required_historical_sources()
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)

    rolling = build_rolling_controls()
    fixed = build_fixed_split_summary()
    reconciliation = build_reconciliation_summary()
    ranks = build_rank_table(rolling, reconciliation)
    percentages = build_percentage_denominators(fixed, rolling, reconciliation)
    rolling_stability = build_rolling_stability()
    runtime = build_runtime_accuracy()
    effects = build_effect_summary(rolling_stability)

    table_outputs = write_tables(
        fixed, rolling, reconciliation, ranks, percentages,
        rolling_stability, runtime, effects,
    )
    figure_leaderboards(fixed, rolling)
    figure_component_matrix()
    figure_ausgrid(reconciliation)
    figure_rolling_stability(rolling_stability)
    figure_reconciliation(reconciliation)
    figure_effects(effects)
    figure_ranks(ranks)
    figure_compute_profile(runtime)
    write_artifact_manifest(accepted_manifest, historical_sources, table_outputs)

    print(f"verified accepted manifest: {RUN_MANIFEST}")
    for path in table_outputs:
        print(f"wrote {path}")
    print(f"wrote {DERIVED_DIR / 'p2_artifact_manifest.json'}")
    for stem in [
        "fig_leaderboard", "fig_component", "fig_ausgrid", "fig_rolling_stability",
        "fig_exact_hierarchy_reconciliation", "fig_cross_dataset_effects",
        "fig_cross_setting_ranks", "fig_compute_error_profile",
    ]:
        print(f"wrote {FIG_DIR / (stem + '.png/.pdf/.svg')}")


if __name__ == "__main__":
    main()
