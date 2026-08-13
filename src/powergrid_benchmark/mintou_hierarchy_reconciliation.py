"""Exact-hierarchy Ausgrid benchmark and reconciliation controls for P2.

This v8 extension does not overwrite the v7 all-customer aggregate evidence.
It rebuilds an exact 12-leaf hierarchy and evaluates independent, bottom-up,
top-down, and OLS projection reconciliation for every trained model/seed.
"""

from __future__ import annotations

import csv
import json
import math
import time
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from powergrid_benchmark.mintou_hyg_neural import VARIANTS
from powergrid_benchmark.mintou_hyg_significance import (
    ALL_SEEDS,
    AUSGRID_HYG_EPOCHS,
    AUSGRID_TRAIN_STRIDE,
    AUSGRID_YEAR_FILES,
    AUSGRID_ZIP,
    hyg_train_and_predict_lazy,
)
from powergrid_benchmark.mintou_neural_forecasting import (
    build_tensors,
    train_and_predict as baseline_train_and_predict,
)
from powergrid_benchmark.mintou_real_load_forecasting import P2_ROOT, samples_for

STATUS = "public_ausgrid_exact_hierarchy_v8_reconciliation"
CACHE = AUSGRID_ZIP.parent / "processed_hourly_gc_exact_12leaf_hierarchy.json"
HORIZON = 24

BASELINE_SPECS = (
    ("MLP", 20),
    ("DLinear", 20),
    ("TCN", 10),
    ("PatchTST-lite", 8),
    ("LSTM", 6),
)


def _day_key(raw: str) -> datetime:
    for fmt in ("%d-%b-%y", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognized Ausgrid date: {raw!r}")


def build_exact_hierarchy() -> tuple[list[str], dict[str, list[float]], np.ndarray, dict[str, object]]:
    if CACHE.exists():
        payload = json.loads(CACHE.read_text(encoding="utf-8"))
        return (
            payload["timestamps"],
            payload["series"],
            np.asarray(payload["summing_matrix"], dtype=float),
            payload["metadata"],
        )

    per_customer: dict[int, dict[str, list[float]]] = {}
    postcode: dict[int, str] = {}
    for name in AUSGRID_YEAR_FILES:
        with zipfile.ZipFile(AUSGRID_ZIP).open(name) as handle:
            text = (line.decode("utf-8", errors="ignore") for line in handle)
            reader = csv.reader(text)
            next(reader)
            header = next(reader)
            date_col = header.index("date")
            first_val = date_col + 1
            for row in reader:
                if len(row) <= first_val or row[3] != "GC":
                    continue
                try:
                    customer = int(row[0])
                except ValueError:
                    continue
                postcode[customer] = row[2]
                values: list[float] = []
                try:
                    for hour in range(24):
                        values.append(float(row[first_val + 2 * hour] or 0) + float(row[first_val + 2 * hour + 1] or 0))
                except (ValueError, IndexError):
                    continue
                per_customer.setdefault(customer, {})[row[date_col]] = values

    max_days = max(len(days) for days in per_customer.values())
    complete = {customer: days for customer, days in per_customer.items() if len(days) == max_days}
    totals = {customer: sum(sum(values) for values in days.values()) for customer, days in complete.items()}
    leaves = sorted(complete, key=lambda customer: -totals[customer])[:12]
    ordered_for_groups = sorted(leaves, key=lambda customer: (postcode[customer], customer))
    groups = [ordered_for_groups[index : index + 3] for index in range(0, 12, 3)]
    group_of = {customer: group_index for group_index, group in enumerate(groups) for customer in group}

    dates = sorted(next(iter(complete.values())), key=_day_key)
    for first, second in zip(dates, dates[1:]):
        if _day_key(second) - _day_key(first) != timedelta(days=1):
            raise RuntimeError(f"date gap between {first} and {second}")

    leaf_names = [f"customer{customer}" for customer in leaves]
    series: dict[str, list[float]] = {name: [] for name in leaf_names}
    for group_index in range(4):
        series[f"region{group_index + 1}"] = []
    series["system_total"] = []
    timestamps: list[str] = []
    for date in dates:
        for hour in range(24):
            timestamps.append(f"{_day_key(date).date()}T{hour:02d}:00")
            leaf_values = []
            for customer in leaves:
                value = complete[customer][date][hour]
                series[f"customer{customer}"].append(value)
                leaf_values.append(value)
            group_values = [0.0] * 4
            for customer, value in zip(leaves, leaf_values):
                group_values[group_of[customer]] += value
            for group_index, value in enumerate(group_values):
                series[f"region{group_index + 1}"].append(value)
            series["system_total"].append(sum(leaf_values))

    summing = np.zeros((17, 12), dtype=float)
    summing[:12] = np.eye(12)
    for leaf_index, customer in enumerate(leaves):
        summing[12 + group_of[customer], leaf_index] = 1.0
    summing[16] = 1.0
    metadata: dict[str, object] = {
        "leaf_customers": leaves,
        "groups": groups,
        "postcodes": {str(customer): postcode[customer] for customer in leaves},
        "n_complete_customers_available": len(complete),
        "status": STATUS,
    }
    CACHE.write_text(
        json.dumps(
            {
                "timestamps": timestamps,
                "series": series,
                "summing_matrix": summing.tolist(),
                "metadata": metadata,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return timestamps, series, summing, metadata


def _matrix_from_samples(samples, values: list[float], names: list[str]) -> np.ndarray:
    index = {name: position for position, name in enumerate(names)}
    times = sorted({sample.t for sample in samples})
    time_index = {value: position for position, value in enumerate(times)}
    matrix = np.zeros((len(names), len(times)), dtype=float)
    for sample, value in zip(samples, values):
        matrix[index[sample.country], time_index[sample.t]] = value
    return matrix


def reconcile(base: np.ndarray, summing: np.ndarray, proportions: np.ndarray) -> dict[str, np.ndarray]:
    bottom = summing @ base[:12]
    top = summing @ (proportions[:, None] * base[16][None, :])
    projection = summing @ np.linalg.solve(summing.T @ summing, summing.T)
    ols = projection @ base
    return {"Base": base, "Bottom-Up": bottom, "Top-Down": top, "OLS-Reconciled": ols}


def metrics(pred: np.ndarray, truth: np.ndarray, summing: np.ndarray) -> dict[str, float]:
    denom = np.maximum(np.abs(pred) + np.abs(truth), 1e-6)
    node_smape = np.mean(2.0 * np.abs(pred - truth) / denom, axis=1)
    node_mae = np.mean(np.abs(pred - truth), axis=1)
    hierarchy_weighted_smape = float((node_smape[:12].mean() + node_smape[12:16].mean() + node_smape[16]) / 3.0)
    residual = pred[12:] - (summing @ pred[:12])[12:]
    scale = np.maximum(np.mean(np.abs(truth[12:]), axis=1, keepdims=True), 1e-6)
    coherence = float(np.mean(np.abs(residual) / scale))
    return {
        "hierarchy_weighted_smape": hierarchy_weighted_smape,
        "leaf_smape": float(node_smape[:12].mean()),
        "region_smape": float(node_smape[12:16].mean()),
        "system_smape": float(node_smape[16]),
        "leaf_mae": float(node_mae[:12].mean()),
        "region_mae": float(node_mae[12:16].mean()),
        "system_mae": float(node_mae[16]),
        "coherence_violation": coherence,
    }


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    import torch

    torch.set_num_threads(4)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
    print(f"[p2-v8] execution device: {device}")
    timestamps, series, summing, metadata = build_exact_hierarchy()
    names = list(series)
    n = len(timestamps)
    train_end = int(n * 0.70)
    tensors = build_tensors(series, train_end)
    train, test = samples_for(series, horizon=HORIZON, train_end=train_end)
    truth = _matrix_from_samples(test, [sample.target for sample in test], names)
    leaf_energy = np.asarray([sum(series[name][:train_end]) for name in names[:12]], dtype=float)
    proportions = leaf_energy / max(float(leaf_energy.sum()), 1e-9)
    rows: list[dict[str, str]] = []
    out = P2_ROOT / "evidence" / "runs"

    model_specs = [
        (name, role, variant, "hyg", AUSGRID_HYG_EPOCHS)
        for name, role, variant in VARIANTS
    ]
    model_specs += [(name, "baseline", {}, "baseline", epochs) for name, epochs in BASELINE_SPECS]
    for name, role, variant, family, epochs in model_specs:
        for seed in ALL_SEEDS:
            start = time.perf_counter()
            if family == "hyg":
                predictions, _ = hyg_train_and_predict_lazy(
                    variant,
                    seed,
                    tensors,
                    train,
                    test,
                    HORIZON,
                    epochs,
                    AUSGRID_TRAIN_STRIDE,
                    device_name=device.type,
                )
            else:
                predictions, _ = baseline_train_and_predict(
                    name,
                    epochs,
                    seed,
                    tensors,
                    train,
                    test,
                    HORIZON,
                    device_name=device.type,
                )
            base = _matrix_from_samples(test, predictions, names)
            runtime = time.perf_counter() - start
            for reconciliation, pred in reconcile(base, summing, proportions).items():
                values = metrics(pred, truth, summing)
                rows.append(
                    {
                        "dataset": "Ausgrid exact 12-leaf/4-region/system hierarchy",
                        "horizon_hours": str(HORIZON),
                        "method": name,
                        "method_role": role,
                        "seed": str(seed),
                        "reconciliation": reconciliation,
                        **{key: f"{value:.8f}" for key, value in values.items()},
                        "runtime_s": f"{runtime:.4f}",
                        "train_samples": str(len(train[::AUSGRID_TRAIN_STRIDE])),
                        "test_samples": str(len(test)),
                        "source_status": STATUS,
                    }
                )
            _write_csv(out / "real_ausgrid_exact_hierarchy_v8_partial.csv", rows)
            print(f"[p2-v8] {name} seed {seed}: done")

    tables = P2_ROOT / "evidence" / "tables"
    configs = P2_ROOT / "src" / "configs"
    _write_csv(out / "real_ausgrid_exact_hierarchy_v8_results.csv", rows)
    board: list[dict[str, str]] = []
    keys = sorted({(row["method"], row["method_role"], row["reconciliation"]) for row in rows})
    for method, role, reconciliation_name in keys:
        group = [row for row in rows if row["method"] == method and row["reconciliation"] == reconciliation_name]
        board.append(
            {
                "method": method,
                "method_role": role,
                "reconciliation": reconciliation_name,
                "mean_hierarchy_weighted_smape": f"{np.mean([float(row['hierarchy_weighted_smape']) for row in group]):.8f}",
                "std_hierarchy_weighted_smape": f"{np.std([float(row['hierarchy_weighted_smape']) for row in group], ddof=1):.8f}",
                "mean_coherence_violation": f"{np.mean([float(row['coherence_violation']) for row in group]):.8f}",
                "mean_leaf_smape": f"{np.mean([float(row['leaf_smape']) for row in group]):.8f}",
                "mean_region_smape": f"{np.mean([float(row['region_smape']) for row in group]):.8f}",
                "mean_system_smape": f"{np.mean([float(row['system_smape']) for row in group]):.8f}",
                "runs": str(len(group)),
            }
        )
    board.sort(key=lambda row: float(row["mean_hierarchy_weighted_smape"]))
    _write_csv(tables / "real_ausgrid_exact_hierarchy_v8_leaderboard.csv", board)
    configs.mkdir(parents=True, exist_ok=True)
    (configs / "real_ausgrid_exact_hierarchy_v8_config.json").write_text(
        json.dumps(
            {
                **metadata,
                "horizon": HORIZON,
                "seeds": list(ALL_SEEDS),
                "models": [spec[0] for spec in model_specs],
                "reconciliation": ["Base", "Bottom-Up", "Top-Down", "OLS-Reconciled"],
                "primary_metric": "hierarchy-weighted sMAPE",
                "execution_device": str(device),
                "status": STATUS,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[p2-v8] complete: {len(rows)} metric rows")


if __name__ == "__main__":
    main()
