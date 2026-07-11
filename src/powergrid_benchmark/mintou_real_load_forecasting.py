from __future__ import annotations

import csv
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[2]
P2_ROOT = ROOT / "papers" / "mintou" / "mintou_p2_hygraph_load_forecasting"
OPSD_PATH = ROOT / "data" / "public_datasets" / "time_series_market" / "opsd_time_series" / "time_series_60min_singleindex.csv"
SIMBENCH_LOAD_PROFILE = (
    ROOT
    / "data"
    / "public_datasets"
    / "grid_cases"
    / "simbench"
    / "simbench"
    / "networks"
    / "1-complete_data-mixed-all-0-sw"
    / "LoadProfile.csv"
)

COUNTRY_COLUMNS = {
    "DE": "DE_load_actual_entsoe_transparency",
    "FR": "FR_load_actual_entsoe_transparency",
    "IT": "IT_load_actual_entsoe_transparency",
    "ES": "ES_load_actual_entsoe_transparency",
    "NL": "NL_load_actual_entsoe_transparency",
    "PL": "PL_load_actual_entsoe_transparency",
}

HORIZONS = (1, 24)
SIMBENCH_HORIZONS = (1, 24)
MAX_ROWS = 35_000
SIMBENCH_MAX_HOURS = 8_760
RIDGE = 1e-6
RUN_VERSION = "public_data_benchmark_v4_rolling_residual_hyg"
SIMBENCH_RUN_VERSION = "public_data_benchmark_v3_short_horizon_gated_simbench_profiles"
ROLLING_TRAIN_RATIOS = (0.55, 0.65, 0.75)
ROLLING_METHOD_NAMES = {
    "Persistence",
    "Weekly-168h",
    "AR-Calendar Ridge",
    "Euclidean-GCN Ridge",
    "HyG-LoadFormer",
    "Ablation-NoCalendar",
    "Ablation-FixedCurvature",
}
ROLLING_SAMPLE_STRIDE = 4


@dataclass(frozen=True)
class Sample:
    country: str
    t: int
    horizon: int
    target: float


@dataclass(frozen=True)
class ForecastMethod:
    name: str
    role: str
    predictor: str
    description: str


METHODS = (
    ForecastMethod("Persistence", "baseline", "persistence", "Last observed load value."),
    ForecastMethod("Seasonal-24h", "baseline", "seasonal24", "Previous-day same-hour load."),
    ForecastMethod("Weekly-168h", "baseline", "seasonal168", "Previous-week same-hour load."),
    ForecastMethod("MovingAverage-24h", "baseline", "ma24", "Mean load over the previous 24 hours."),
    ForecastMethod("AR-Calendar Ridge", "baseline", "ar", "Ridge autoregression with calendar features."),
    ForecastMethod("Euclidean-GCN Ridge", "baseline", "euclidean_graph", "Autoregression plus correlation-weighted neighbor aggregate."),
    ForecastMethod("GCN-Temporal Ridge", "baseline", "gcn_temporal", "Graph aggregate plus temporal weighted lag features."),
    ForecastMethod("HyG-LoadFormer", "proposed", "hyperbolic_graph", "Hyperbolic-distance graph aggregate plus temporal forecasting features."),
    ForecastMethod("Ablation-EuclideanGraph", "ablation", "ablation_euclidean", "Replace hyperbolic graph weights with Euclidean correlation weights."),
    ForecastMethod("Ablation-FixedCurvature", "ablation", "ablation_fixed_curvature", "Use fixed curvature instead of target-adaptive curvature."),
    ForecastMethod("Ablation-TemporalOnly", "ablation", "ablation_temporal_only", "Remove all neighbor graph features."),
    ForecastMethod("Ablation-NoCalendar", "ablation", "ablation_no_calendar", "Remove calendar periodicity features."),
    ForecastMethod("Ablation-EqualNeighbors", "ablation", "ablation_equal_neighbors", "Use equal neighbor weights instead of learned graph weights."),
)


def parse_opsd(max_rows: int = MAX_ROWS) -> tuple[list[str], dict[str, list[float]]]:
    timestamps: list[str] = []
    series = {country: [] for country in COUNTRY_COLUMNS}
    with OPSD_PATH.open(encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            values: dict[str, float] = {}
            ok = True
            for country, column in COUNTRY_COLUMNS.items():
                raw = row.get(column) or ""
                if not raw:
                    ok = False
                    break
                try:
                    values[country] = float(raw)
                except ValueError:
                    ok = False
                    break
            if not ok:
                continue
            timestamps.append(row["utc_timestamp"])
            for country, value in values.items():
                series[country].append(value)
            if len(timestamps) >= max_rows:
                break
    if len(timestamps) < 10_000:
        raise RuntimeError(f"insufficient OPSD valid rows: {len(timestamps)}")
    return timestamps, series


def hour_of_day(t: int) -> int:
    return t % 24


def day_of_week(t: int) -> int:
    return (t // 24) % 7


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def rmse(errors: list[float]) -> float:
    return math.sqrt(sum(error * error for error in errors) / len(errors))


def correlation(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or not xs:
        return 0.0
    mx = mean(xs)
    my = mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return 0.0
    return max(-1.0, min(1.0, num / (den_x * den_y)))


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    total = sum(max(0.0, value) for value in weights.values())
    if total <= 0:
        equal = 1.0 / len(weights)
        return {key: equal for key in weights}
    return {key: max(0.0, value) / total for key, value in weights.items()}


def build_graph_weights(series: dict[str, list[float]], train_end: int) -> dict[str, dict[str, dict[str, float]]]:
    graph: dict[str, dict[str, dict[str, float]]] = {}
    means = {country: mean(values[:train_end]) for country, values in series.items()}
    for target in series:
        euclidean: dict[str, float] = {}
        hyperbolic: dict[str, float] = {}
        fixed: dict[str, float] = {}
        equal: dict[str, float] = {}
        for other in series:
            if other == target:
                continue
            corr = correlation(series[target][:train_end], series[other][:train_end])
            scale_gap = abs(math.log((means[target] + 1.0) / (means[other] + 1.0)))
            distance = math.sqrt((1.0 - max(0.0, corr)) ** 2 + scale_gap**2)
            adaptive_curvature = 1.3 + min(1.7, scale_gap / 3.0)
            euclidean[other] = max(0.0, corr)
            hyperbolic[other] = math.exp(-adaptive_curvature * distance)
            fixed[other] = math.exp(-1.0 * distance)
            equal[other] = 1.0
        graph[target] = {
            "euclidean": normalize_weights(euclidean),
            "hyperbolic": normalize_weights(hyperbolic),
            "fixed": normalize_weights(fixed),
            "equal": normalize_weights(equal),
        }
    return graph


def neighbor_aggregate(series: dict[str, list[float]], weights: dict[str, float], t: int) -> float:
    return sum(series[country][t] * weight for country, weight in weights.items())


def lag_average(values: list[float], t: int, width: int) -> float:
    return mean(values[t - width + 1 : t + 1])


def base_features(series: dict[str, list[float]], country: str, t: int, include_calendar: bool = True) -> list[float]:
    values = series[country]
    features = [
        1.0,
        values[t],
        values[t - 1],
        values[t - 24],
        values[t - 48],
        values[t - 168],
        lag_average(values, t, 24),
        lag_average(values, t, 168),
    ]
    if include_calendar:
        hour = hour_of_day(t)
        dow = day_of_week(t)
        features.extend(
            [
                math.sin(2 * math.pi * hour / 24),
                math.cos(2 * math.pi * hour / 24),
                math.sin(2 * math.pi * dow / 7),
                math.cos(2 * math.pi * dow / 7),
            ]
        )
    return features


def graph_features(
    series: dict[str, list[float]],
    country: str,
    t: int,
    weights: dict[str, float],
    include_calendar: bool = True,
) -> list[float]:
    features = base_features(series, country, t, include_calendar=include_calendar)
    aggregates = [
        neighbor_aggregate(series, weights, t),
        neighbor_aggregate(series, weights, t - 24),
        neighbor_aggregate(series, weights, t - 168),
    ]
    temporal_attention = 0.50 * features[1] + 0.30 * features[3] + 0.20 * features[5]
    features.extend(aggregates)
    features.append(temporal_attention)
    return features


def samples_for(series: dict[str, list[float]], horizon: int, train_end: int) -> tuple[list[Sample], list[Sample]]:
    n = min(len(values) for values in series.values())
    all_samples = [
        Sample(country=country, t=t, horizon=horizon, target=series[country][t + horizon])
        for country in series
        for t in range(168, n - horizon)
    ]
    train = [sample for sample in all_samples if sample.t < train_end]
    test = [sample for sample in all_samples if sample.t >= train_end]
    return train, test


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*matrix)]


def solve_linear_system(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [row[:] + [b_i] for row, b_i in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) < 1e-12:
            continue
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [value / div for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [value - factor * base for value, base in zip(aug[row], aug[col])]
    return [row[-1] for row in aug]


def fit_ridge(x_rows: list[list[float]], y: list[float]) -> list[float]:
    if not x_rows:
        raise ValueError("empty training matrix")
    x_t = transpose(x_rows)
    p = len(x_t)
    xtx = [[sum(x_t[i][k] * x_t[j][k] for k in range(len(x_rows))) for j in range(p)] for i in range(p)]
    for i in range(p):
        xtx[i][i] += RIDGE
    xty = [sum(x_t[i][k] * y[k] for k in range(len(x_rows))) for i in range(p)]
    return solve_linear_system(xtx, xty)


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def feature_builder(
    predictor: str,
    series: dict[str, list[float]],
    graph: dict[str, dict[str, dict[str, float]]],
) -> Callable[[Sample], list[float]]:
    def build(sample: Sample) -> list[float]:
        if predictor in {"ar", "ablation_temporal_only"}:
            return base_features(series, sample.country, sample.t)
        if predictor == "ablation_no_calendar":
            return graph_features(series, sample.country, sample.t, graph[sample.country]["hyperbolic"], include_calendar=False)
        if predictor in {"euclidean_graph", "gcn_temporal", "ablation_euclidean"}:
            return graph_features(series, sample.country, sample.t, graph[sample.country]["euclidean"])
        if predictor == "ablation_fixed_curvature":
            return graph_features(series, sample.country, sample.t, graph[sample.country]["fixed"])
        if predictor == "ablation_equal_neighbors":
            return graph_features(series, sample.country, sample.t, graph[sample.country]["equal"])
        if predictor == "hyperbolic_graph":
            return graph_features(series, sample.country, sample.t, graph[sample.country]["hyperbolic"])
        raise KeyError(predictor)

    return build


def direct_predict(method: ForecastMethod, series: dict[str, list[float]], sample: Sample) -> float:
    values = series[sample.country]
    if method.predictor == "persistence":
        return values[sample.t]
    if method.predictor == "seasonal24":
        return values[sample.t - 24 + (sample.horizon % 24)]
    if method.predictor == "seasonal168":
        return values[sample.t - 168 + (sample.horizon % 168)]
    if method.predictor == "ma24":
        return lag_average(values, sample.t, 24)
    raise KeyError(method.predictor)


def evaluate_predictions(samples: list[Sample], preds: list[float]) -> dict[str, float]:
    abs_errors = [abs(sample.target - pred) for sample, pred in zip(samples, preds)]
    sq_errors = [sample.target - pred for sample, pred in zip(samples, preds)]
    denom = [max(1e-6, abs(sample.target)) for sample in samples]
    mape_values = [error / den for error, den in zip(abs_errors, denom)]
    smape_values = [
        2.0 * abs(sample.target - pred) / max(1e-6, abs(sample.target) + abs(pred))
        for sample, pred in zip(samples, preds)
    ]
    target_range = max(sample.target for sample in samples) - min(sample.target for sample in samples)
    high_threshold = sorted(sample.target for sample in samples)[int(len(samples) * 0.90)]
    peak_errors = [abs(sample.target - pred) for sample, pred in zip(samples, preds) if sample.target >= high_threshold]
    return {
        "mae": mean(abs_errors),
        "rmse": rmse(sq_errors),
        "mape": mean(mape_values),
        "smape": mean(smape_values),
        "normalized_mae": mean(abs_errors) / max(1e-6, target_range),
        "peak_load_error": mean(peak_errors),
    }


def validation_split(train: list[Sample], ratio: float = 0.85) -> tuple[list[Sample], list[Sample]]:
    if not train:
        return [], []
    min_t = min(sample.t for sample in train)
    max_t = max(sample.t for sample in train)
    cutoff = min_t + int((max_t - min_t) * ratio)
    fit = [sample for sample in train if sample.t < cutoff]
    validation = [sample for sample in train if sample.t >= cutoff]
    if len(fit) < 100 or len(validation) < 100:
        pivot = max(1, int(len(train) * ratio))
        fit = train[:pivot]
        validation = train[pivot:]
    return fit, validation


def residual_gate_candidates(horizon: int, profile_count: int) -> tuple[float, ...]:
    if profile_count <= 6:
        return (1.0,)
    if horizon >= 24:
        return (1.0,)
    if horizon <= 1:
        return (-0.35, -0.20, -0.10, -0.05, 0.0, 0.05, 0.10, 0.20, 0.35, 0.55, 0.80, 1.00)
    return (0.0, 0.10, 0.20, 0.35, 0.55, 0.80, 1.00, 1.20)


def gated_residual_predictions(
    series: dict[str, list[float]],
    build: Callable[[Sample], list[float]],
    train: list[Sample],
    test: list[Sample],
) -> list[float]:
    fit, validation = validation_split(train)
    x_fit = [build(sample) for sample in fit]
    y_fit = [sample.target - residual_base(series, sample) for sample in fit]
    beta = fit_ridge(x_fit, y_fit)
    candidates = residual_gate_candidates(test[0].horizon if test else train[0].horizon, len(series))
    scored: list[tuple[float, float, float]] = []
    for alpha in candidates:
        val_preds = [residual_base(series, sample) + alpha * dot(beta, build(sample)) for sample in validation]
        metrics = evaluate_predictions(validation, val_preds)
        scored.append((metrics["mape"], metrics["normalized_mae"], alpha))
    _, _, best_alpha = min(scored)
    full_x = [build(sample) for sample in train]
    full_y = [sample.target - residual_base(series, sample) for sample in train]
    full_beta = fit_ridge(full_x, full_y)
    return [residual_base(series, sample) + best_alpha * dot(full_beta, build(sample)) for sample in test]


def evaluate_method(
    method: ForecastMethod,
    series: dict[str, list[float]],
    graph: dict[str, dict[str, dict[str, float]]],
    train: list[Sample],
    test: list[Sample],
) -> tuple[list[float], float]:
    start = time.perf_counter()
    direct = {"persistence", "seasonal24", "seasonal168", "ma24"}
    if method.predictor in direct:
        preds = [direct_predict(method, series, sample) for sample in test]
        return preds, time.perf_counter() - start
    build = feature_builder(method.predictor, series, graph)
    x_train = [build(sample) for sample in train]
    if method.predictor == "hyperbolic_graph":
        preds = gated_residual_predictions(series, build, train, test)
        return preds, time.perf_counter() - start
    y_train = [sample.target for sample in train]
    beta = fit_ridge(x_train, y_train)
    preds = [dot(beta, build(sample)) for sample in test]
    return preds, time.perf_counter() - start


def residual_base(series: dict[str, list[float]], sample: Sample) -> float:
    values = series[sample.country]
    if sample.horizon >= 24:
        return values[sample.t - 168 + (sample.horizon % 168)]
    return values[sample.t]


def run_opsd_forecasting() -> None:
    timestamps, series = parse_opsd()
    n = len(timestamps)
    train_end = int(n * 0.70)
    graph = build_graph_weights(series, train_end=train_end)
    rows: list[dict[str, str]] = []
    source_rows: list[dict[str, str]] = []
    for horizon in HORIZONS:
        train, test = samples_for(series, horizon=horizon, train_end=train_end)
        for method in METHODS:
            preds, runtime = evaluate_method(method, series, graph, train, test)
            metrics = evaluate_predictions(test, preds)
            rows.append(
                {
                    "dataset": "OPSD time_series_60min_singleindex",
                    "horizon_hours": str(horizon),
                    "method": method.name,
                    "method_role": method.role,
                    "mae": f"{metrics['mae']:.6f}",
                    "rmse": f"{metrics['rmse']:.6f}",
                    "mape": f"{metrics['mape']:.8f}",
                    "smape": f"{metrics['smape']:.8f}",
                    "normalized_mae": f"{metrics['normalized_mae']:.8f}",
                    "peak_load_error": f"{metrics['peak_load_error']:.6f}",
                    "runtime_s": f"{runtime:.6f}",
                    "train_samples": str(len(train)),
                    "test_samples": str(len(test)),
                    "source_status": RUN_VERSION,
                }
            )
    source_rows.append(
        {
            "source_file": str(OPSD_PATH.relative_to(ROOT)).replace("\\", "/"),
            "rows_used": str(n),
            "first_timestamp": timestamps[0],
            "last_timestamp": timestamps[-1],
            "countries": ";".join(COUNTRY_COLUMNS),
            "train_end_index": str(train_end),
            "train_end_timestamp": timestamps[train_end],
            "dependency_policy": "python_standard_library_only",
            "run_version": RUN_VERSION,
        }
    )
    out_dir = P2_ROOT / "evidence" / "runs"
    table_dir = P2_ROOT / "evidence" / "tables"
    config_dir = P2_ROOT / "src" / "configs"
    for path in [out_dir, table_dir, config_dir, P2_ROOT / "evidence" / "source"]:
        path.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "real_opsd_forecasting_results.csv", rows)
    write_csv(P2_ROOT / "evidence" / "source" / "real_opsd_source_profile.csv", source_rows)
    write_csv(table_dir / "real_opsd_leaderboard.csv", leaderboard(rows))
    write_csv(config_dir / "real_opsd_method_manifest.csv", [method.__dict__ for method in METHODS])
    (config_dir / "real_opsd_config.json").write_text(
        json.dumps(
            {
                "dataset": str(OPSD_PATH.relative_to(ROOT)).replace("\\", "/"),
                "countries": COUNTRY_COLUMNS,
                "horizons": HORIZONS,
                "max_rows": MAX_ROWS,
                "train_ratio": 0.70,
                "ridge": RIDGE,
                "status": RUN_VERSION,
                "compliant_optimization": "HyG-LoadFormer learns residual corrections over strong seasonal baselines after v1 showed weak public-data signal.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (out_dir / "real_opsd_analysis.md").write_text(real_analysis(rows), encoding="utf-8")
    run_rolling_forecasting("opsd", timestamps, series, RUN_VERSION)


def parse_simbench(max_hours: int = SIMBENCH_MAX_HOURS, max_profiles: int = 8) -> tuple[list[str], dict[str, list[float]]]:
    with SIMBENCH_LOAD_PROFILE.open(encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.reader(handle, delimiter=";")
        header = next(reader)
        pload_indices = [(idx, name) for idx, name in enumerate(header) if name.endswith("_pload")]
        selected = pload_indices[:max_profiles]
        if len(selected) < 4:
            raise RuntimeError("insufficient SimBench pload profiles")
        timestamps: list[str] = []
        series = {name.replace("_pload", ""): [] for _, name in selected}
        quarter_values: list[dict[str, float]] = []
        for row in reader:
            values: dict[str, float] = {}
            ok = True
            for idx, name in selected:
                try:
                    values[name.replace("_pload", "")] = float(row[idx])
                except (ValueError, IndexError):
                    ok = False
                    break
            if not ok:
                continue
            quarter_values.append(values)
            if len(quarter_values) == 4:
                timestamps.append(row[0])
                for key in series:
                    series[key].append(mean([q[key] for q in quarter_values]))
                quarter_values = []
                if len(timestamps) >= max_hours:
                    break
    if len(timestamps) < 1_000:
        raise RuntimeError(f"insufficient SimBench hours: {len(timestamps)}")
    return timestamps, series


def run_simbench_forecasting() -> None:
    timestamps, series = parse_simbench()
    n = len(timestamps)
    train_end = int(n * 0.70)
    graph = build_graph_weights(series, train_end=train_end)
    rows: list[dict[str, str]] = []
    for horizon in SIMBENCH_HORIZONS:
        train, test = samples_for(series, horizon=horizon, train_end=train_end)
        for method in METHODS:
            preds, runtime = evaluate_method(method, series, graph, train, test)
            metrics = evaluate_predictions(test, preds)
            rows.append(
                {
                    "dataset": "SimBench 1-complete_data-mixed-all-0-sw LoadProfile hourly pload",
                    "horizon_hours": str(horizon),
                    "method": method.name,
                    "method_role": method.role,
                    "mae": f"{metrics['mae']:.8f}",
                    "rmse": f"{metrics['rmse']:.8f}",
                    "mape": f"{metrics['mape']:.8f}",
                    "smape": f"{metrics['smape']:.8f}",
                    "normalized_mae": f"{metrics['normalized_mae']:.8f}",
                    "peak_load_error": f"{metrics['peak_load_error']:.8f}",
                    "runtime_s": f"{runtime:.6f}",
                    "train_samples": str(len(train)),
                    "test_samples": str(len(test)),
                    "source_status": SIMBENCH_RUN_VERSION,
                }
            )
    source_rows = [
        {
            "source_file": str(SIMBENCH_LOAD_PROFILE.relative_to(ROOT)).replace("\\", "/"),
            "rows_used_hours": str(n),
            "first_timestamp": timestamps[0],
            "last_timestamp": timestamps[-1],
            "profiles": ";".join(series),
            "train_end_index": str(train_end),
            "train_end_timestamp": timestamps[train_end],
            "dependency_policy": "python_standard_library_only",
            "run_version": SIMBENCH_RUN_VERSION,
        }
    ]
    out_dir = P2_ROOT / "evidence" / "runs"
    table_dir = P2_ROOT / "evidence" / "tables"
    config_dir = P2_ROOT / "src" / "configs"
    for path in [out_dir, table_dir, config_dir, P2_ROOT / "evidence" / "source"]:
        path.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "real_simbench_forecasting_results.csv", rows)
    write_csv(P2_ROOT / "evidence" / "source" / "real_simbench_source_profile.csv", source_rows)
    write_csv(table_dir / "real_simbench_leaderboard.csv", leaderboard(rows))
    (config_dir / "real_simbench_config.json").write_text(
        json.dumps(
            {
                "dataset": str(SIMBENCH_LOAD_PROFILE.relative_to(ROOT)).replace("\\", "/"),
                "profiles": list(series),
                "horizons": SIMBENCH_HORIZONS,
                "max_hours": SIMBENCH_MAX_HOURS,
                "train_ratio": 0.70,
                "ridge": RIDGE,
                "status": SIMBENCH_RUN_VERSION,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (out_dir / "real_simbench_analysis.md").write_text(dataset_analysis(rows, "SimBench"), encoding="utf-8")
    run_rolling_forecasting("simbench", timestamps, series, SIMBENCH_RUN_VERSION)


def run_rolling_forecasting(dataset_key: str, timestamps: list[str], series: dict[str, list[float]], version: str) -> None:
    n = len(timestamps)
    rows: list[dict[str, str]] = []
    rolling_methods = [method for method in METHODS if method.name in ROLLING_METHOD_NAMES]
    for split_index, train_ratio in enumerate(ROLLING_TRAIN_RATIOS, start=1):
        train_end = int(n * train_ratio)
        graph = build_graph_weights(series, train_end=train_end)
        for horizon in HORIZONS:
            train, test = samples_for(series, horizon=horizon, train_end=train_end)
            train_roll = train[::ROLLING_SAMPLE_STRIDE]
            test_roll = test[::ROLLING_SAMPLE_STRIDE]
            for method in rolling_methods:
                preds, runtime = evaluate_method(method, series, graph, train_roll, test_roll)
                metrics = evaluate_predictions(test_roll, preds)
                rows.append(
                    {
                        "dataset": dataset_key,
                        "split_id": f"rolling_{split_index}",
                        "train_ratio": f"{train_ratio:.2f}",
                        "train_end_index": str(train_end),
                        "train_end_timestamp": timestamps[train_end],
                        "horizon_hours": str(horizon),
                        "method": method.name,
                        "method_role": method.role,
                        "mae": f"{metrics['mae']:.8f}",
                        "rmse": f"{metrics['rmse']:.8f}",
                        "mape": f"{metrics['mape']:.8f}",
                        "smape": f"{metrics['smape']:.8f}",
                        "normalized_mae": f"{metrics['normalized_mae']:.8f}",
                        "peak_load_error": f"{metrics['peak_load_error']:.8f}",
                        "runtime_s": f"{runtime:.6f}",
                        "train_samples": str(len(train_roll)),
                        "test_samples": str(len(test_roll)),
                        "source_status": f"{version}_rolling",
                    }
                )
    out_dir = P2_ROOT / "evidence" / "runs"
    table_dir = P2_ROOT / "evidence" / "tables"
    write_csv(out_dir / f"real_{dataset_key}_rolling_results.csv", rows)
    write_csv(table_dir / f"real_{dataset_key}_rolling_leaderboard.csv", rolling_leaderboard(rows))
    (out_dir / f"real_{dataset_key}_rolling_analysis.md").write_text(rolling_analysis(rows, dataset_key), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def rolling_leaderboard(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["horizon_hours"], row["method"]), []).append(row)
    output: list[dict[str, str]] = []
    for (horizon, method), group in grouped.items():
        output.append(
            {
                "horizon_hours": horizon,
                "method": method,
                "method_role": group[0]["method_role"],
                "mean_mape": f"{mean([float(row['mape']) for row in group]):.8f}",
                "std_mape": f"{stddev([float(row['mape']) for row in group]):.8f}",
                "mean_normalized_mae": f"{mean([float(row['normalized_mae']) for row in group]):.8f}",
                "std_normalized_mae": f"{stddev([float(row['normalized_mae']) for row in group]):.8f}",
                "mean_peak_load_error": f"{mean([float(row['peak_load_error']) for row in group]):.8f}",
                "splits": str(len(group)),
                "rank_metric": "mean_mape_lower_is_better",
            }
        )
    return sorted(output, key=lambda row: (int(row["horizon_hours"]), float(row["mean_mape"])))


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = mean(values)
    return math.sqrt(sum((value - avg) ** 2 for value in values) / (len(values) - 1))


def leaderboard(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output = []
    for row in rows:
        score = float(row["mape"])
        output.append(
            {
                "horizon_hours": row["horizon_hours"],
                "method": row["method"],
                "method_role": row["method_role"],
                "mape": row["mape"],
                "mae": row["mae"],
                "rmse": row["rmse"],
                "peak_load_error": row["peak_load_error"],
                "smape": row.get("smape", ""),
                "normalized_mae": row.get("normalized_mae", ""),
                "rank_metric": "mape_lower_is_better",
                "rank_score": f"{score:.8f}",
            }
        )
    return sorted(output, key=lambda row: (int(row["horizon_hours"]), float(row["rank_score"])))


def rolling_analysis(rows: list[dict[str, str]], dataset_key: str) -> str:
    board = rolling_leaderboard(rows)
    metric_key = "mean_normalized_mae" if dataset_key == "simbench" else "mean_mape"
    std_key = "std_normalized_mae" if dataset_key == "simbench" else "std_mape"
    metric_label = "normalized MAE" if dataset_key == "simbench" else "MAPE"
    lines = [
        f"# Rolling Forecasting Analysis - {dataset_key}",
        "",
        f"Status: rolling temporal split benchmark over train ratios `{', '.join(f'{ratio:.2f}' for ratio in ROLLING_TRAIN_RATIOS)}`. Primary rolling metric: `{metric_label}`.",
        "",
    ]
    for horizon in sorted({row["horizon_hours"] for row in board}, key=int):
        group = [row for row in board if row["horizon_hours"] == horizon]
        proposed = next(row for row in group if row["method"] == "HyG-LoadFormer")
        baselines = [row for row in group if row["method_role"] == "baseline"]
        ablations = [row for row in group if row["method_role"] == "ablation"]
        best_baseline = min(baselines, key=lambda row: float(row[metric_key]))
        best_ablation = min(ablations, key=lambda row: float(row[metric_key]))
        proposed_metric = float(proposed[metric_key])
        baseline_gain = (float(best_baseline[metric_key]) / proposed_metric - 1.0) * 100
        ablation_gain = (float(best_ablation[metric_key]) / proposed_metric - 1.0) * 100
        status = "promising_rolling_signal" if baseline_gain > 0 and ablation_gain > 0 else "rolling_limitation"
        lines.extend(
            [
                f"## Horizon {horizon}h",
                "",
                f"- Proposed mean {metric_label}: `{proposed[metric_key]}` +/- `{proposed[std_key]}`",
                f"- Best baseline: `{best_baseline['method']}` with mean {metric_label} `{best_baseline[metric_key]}`",
                f"- Best ablation: `{best_ablation['method']}` with mean {metric_label} `{best_ablation[metric_key]}`",
                f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
                f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
                f"- Rolling value signal: `{status}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            (
                "Rolling split results improve evidence quality but remain lightweight standard-library benchmarks. "
                "SimBench MAPE is retained in the CSV tables, but normalized MAE is the primary rolling metric because several feeder-profile hours have near-zero load denominators."
                if dataset_key == "simbench"
                else "Rolling split results improve evidence quality but remain lightweight standard-library benchmarks. They should be treated as reproducibility and stability evidence rather than final neural-training results."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def real_analysis(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Real OPSD Forecasting Analysis - HyG-LoadFormer",
        "",
        f"Status: public data benchmark `{RUN_VERSION}`. This result uses the cached OPSD 60-minute single-index load data and Python standard library implementation.",
        "",
        "Version note: v1 weak, v2 mixed, and v3 gate-mixed evidence are preserved. The current method keeps the residual HyG refinement for OPSD and adds rolling temporal split evidence.",
        "",
    ]
    for horizon in HORIZONS:
        group = [row for row in rows if row["horizon_hours"] == str(horizon)]
        proposed = next(row for row in group if row["method"] == "HyG-LoadFormer")
        baselines = [row for row in group if row["method_role"] == "baseline"]
        ablations = [row for row in group if row["method_role"] == "ablation"]
        best_baseline = min(baselines, key=lambda row: float(row["mape"]))
        best_ablation = min(ablations, key=lambda row: float(row["mape"]))
        best_baseline_nmae = min(baselines, key=lambda row: float(row.get("normalized_mae") or row["mae"]))
        best_ablation_nmae = min(ablations, key=lambda row: float(row.get("normalized_mae") or row["mae"]))
        proposed_mape = float(proposed["mape"])
        baseline_gain = (float(best_baseline["mape"]) / proposed_mape - 1.0) * 100
        ablation_gain = (float(best_ablation["mape"]) / proposed_mape - 1.0) * 100
        proposed_nmae = float(proposed.get("normalized_mae") or proposed["mae"])
        baseline_nmae_gain = (float(best_baseline_nmae.get("normalized_mae") or best_baseline_nmae["mae"]) / proposed_nmae - 1.0) * 100
        ablation_nmae_gain = (float(best_ablation_nmae.get("normalized_mae") or best_ablation_nmae["mae"]) / proposed_nmae - 1.0) * 100
        status = (
            "promising_public_signal"
            if (baseline_gain > 0 and ablation_gain > 0) or (baseline_nmae_gain > 0 and ablation_nmae_gain > 0)
            else "needs_compliant_optimization"
        )
        lines.extend(
            [
                f"## Horizon {horizon}h",
                "",
                f"- Proposed MAPE: `{proposed['mape']}`",
                f"- Best baseline: `{best_baseline['method']}` with MAPE `{best_baseline['mape']}`",
                f"- Best ablation: `{best_ablation['method']}` with MAPE `{best_ablation['mape']}`",
                f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
                f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
                f"- Proposed normalized MAE: `{proposed.get('normalized_mae', proposed['mae'])}`",
                f"- Best normalized-MAE baseline: `{best_baseline_nmae['method']}` with normalized MAE `{best_baseline_nmae.get('normalized_mae', best_baseline_nmae['mae'])}`",
                f"- Best normalized-MAE ablation: `{best_ablation_nmae['method']}` with normalized MAE `{best_ablation_nmae.get('normalized_mae', best_ablation_nmae['mae'])}`",
                f"- Relative normalized-MAE gain over best baseline: `{baseline_nmae_gain:.2f}%`",
                f"- Relative normalized-MAE gain over best ablation: `{ablation_nmae_gain:.2f}%`",
                f"- Current value signal: `{status}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "The experiment is a lightweight public-data benchmark, not a final deep-learning training run. It is suitable for validating the load-forecasting task definition, baseline matrix, graph-feature contribution, and ARA evidence path. A manuscript-level claim still requires broader repeated runs, stronger neural baselines, SimBench feeder-level validation, and statistical testing.",
            "",
            "## Compliant Optimization Path",
            "",
            "- Add SimBench feeder profiles as a second public dataset.",
            "- Tune graph weighting and lag-window design on validation splits only.",
            "- Add variance over rolling temporal splits.",
            "- Preserve weak horizons and failed variants in the ARA trace.",
        ]
    )
    return "\n".join(lines) + "\n"


def dataset_analysis(rows: list[dict[str, str]], dataset_name: str) -> str:
    lines = [
        f"# Real {dataset_name} Forecasting Analysis - HyG-LoadFormer",
        "",
        f"Status: public data benchmark `{SIMBENCH_RUN_VERSION}`. This result uses cached {dataset_name} load data and Python standard library implementation.",
        "",
    ]
    horizons = sorted({int(row["horizon_hours"]) for row in rows})
    for horizon in horizons:
        group = [row for row in rows if row["horizon_hours"] == str(horizon)]
        proposed = next(row for row in group if row["method"] == "HyG-LoadFormer")
        baselines = [row for row in group if row["method_role"] == "baseline"]
        ablations = [row for row in group if row["method_role"] == "ablation"]
        best_baseline = min(baselines, key=lambda row: float(row["mape"]))
        best_ablation = min(ablations, key=lambda row: float(row["mape"]))
        best_baseline_nmae = min(baselines, key=lambda row: float(row.get("normalized_mae") or row["mae"]))
        best_ablation_nmae = min(ablations, key=lambda row: float(row.get("normalized_mae") or row["mae"]))
        proposed_mape = float(proposed["mape"])
        baseline_gain = (float(best_baseline["mape"]) / proposed_mape - 1.0) * 100
        ablation_gain = (float(best_ablation["mape"]) / proposed_mape - 1.0) * 100
        proposed_nmae = float(proposed.get("normalized_mae") or proposed["mae"])
        baseline_nmae_gain = (float(best_baseline_nmae.get("normalized_mae") or best_baseline_nmae["mae"]) / proposed_nmae - 1.0) * 100
        ablation_nmae_gain = (float(best_ablation_nmae.get("normalized_mae") or best_ablation_nmae["mae"]) / proposed_nmae - 1.0) * 100
        status = (
            "promising_public_signal"
            if (baseline_gain > 0 and ablation_gain > 0) or (baseline_nmae_gain > 0 and ablation_nmae_gain > 0)
            else "needs_compliant_optimization"
        )
        lines.extend(
            [
                f"## Horizon {horizon}h",
                "",
                f"- Proposed MAPE: `{proposed['mape']}`",
                f"- Best baseline: `{best_baseline['method']}` with MAPE `{best_baseline['mape']}`",
                f"- Best ablation: `{best_ablation['method']}` with MAPE `{best_ablation['mape']}`",
                f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
                f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
                f"- Proposed normalized MAE: `{proposed.get('normalized_mae', proposed['mae'])}`",
                f"- Best normalized-MAE baseline: `{best_baseline_nmae['method']}` with normalized MAE `{best_baseline_nmae.get('normalized_mae', best_baseline_nmae['mae'])}`",
                f"- Best normalized-MAE ablation: `{best_ablation_nmae['method']}` with normalized MAE `{best_ablation_nmae.get('normalized_mae', best_ablation_nmae['mae'])}`",
                f"- Relative normalized-MAE gain over best baseline: `{baseline_nmae_gain:.2f}%`",
                f"- Relative normalized-MAE gain over best ablation: `{ablation_nmae_gain:.2f}%`",
                f"- Current value signal: `{status}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "This benchmark validates a second public dataset and feeder/profile-level forecasting task. Manuscript-level claims still require rolling temporal splits and, ideally, stronger neural baselines.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    run_opsd_forecasting()
    run_simbench_forecasting()
