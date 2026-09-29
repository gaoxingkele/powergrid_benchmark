"""Evidence-preserving P1 fair-data and retrieval-mechanism experiment.

This script writes only inside its own run namespace. It deliberately keeps
the direct policy transform as a privileged construction control and never
promotes it to an operational forecast baseline.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import platform
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import numpy as np
import torch
from torch import nn


RUN_DIR = Path(__file__).resolve().parent
RESULT_DIR = RUN_DIR / "results"
LOG_DIR = RUN_DIR / "logs"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_float(value: str | None, default: float = 0.0) -> float:
    try:
        if value in {None, "", "NA", "NULL"}:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def write_json_atomic(path: Path, value: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_csv_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table: {path}")
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


class RunLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def emit(self, message: str) -> None:
        line = f"[{utc_now()}] {message}"
        print(line, flush=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def load_timeseries(path: Path, evaluated_hours: int) -> tuple[list[tuple[int, int, int, int]], np.ndarray, int]:
    keys: list[tuple[int, int, int, int]] = []
    totals: list[float] = []
    with path.open(encoding="utf-8", errors="strict", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            key = tuple(int(row[name]) for name in ("Year", "Month", "Day", "Period"))
            total = sum(parse_float(value) for name, value in row.items() if name not in {"Year", "Month", "Day", "Period"})
            keys.append(key)
            totals.append(total)
    source_rows = len(keys)
    if source_rows < evaluated_hours:
        raise ValueError(f"{path} has {source_rows} rows, fewer than evaluated {evaluated_hours}")
    # Preserve the frozen v5/v6 construction, which evaluates the first 8,760
    # rows of the 8,784-row leap-year files.
    return keys[:evaluated_hours], np.asarray(totals[:evaluated_hours], dtype=np.float64), source_rows


def load_branch_constants(path: Path) -> tuple[float, float, int]:
    ratings: list[float] = []
    weighted: list[float] = []
    with path.open(encoding="utf-8", errors="strict", newline="") as handle:
        for row in csv.DictReader(handle):
            rating = parse_float(row.get("Cont Rating"))
            if rating <= 0:
                continue
            outage = parse_float(row.get("Perm OutRate")) + parse_float(row.get("Tran OutRate"))
            ratings.append(rating)
            weighted.append(rating * outage)
    total_rating = sum(ratings)
    weighted_outage = sum(weighted) / max(1.0, total_rating)
    return total_rating, weighted_outage, len(ratings)


def load_features(rts_data: Path, config: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    source_paths = {name: rts_data / item["relative_path"] for name, item in config["source_files"].items()}
    for name, path in source_paths.items():
        if not path.is_file():
            raise FileNotFoundError(f"missing {name} source: {path}")
        observed = sha256(path)
        expected = config["source_files"][name]["sha256"]
        if observed != expected:
            raise ValueError(f"source hash mismatch for {name}: {observed} != {expected}")

    expected_hours = int(config["hours"])
    load_keys, load, load_source_rows = load_timeseries(source_paths["load"], expected_hours)
    wind_keys, wind, wind_source_rows = load_timeseries(source_paths["wind"], expected_hours)
    pv_keys, pv, pv_source_rows = load_timeseries(source_paths["pv"], expected_hours)
    if load_keys != wind_keys or load_keys != pv_keys:
        raise ValueError("load/wind/PV delivery-row keys do not align")

    total_rating, weighted_outage, branch_count = load_branch_constants(source_paths["branch"])
    renewable = wind + pv
    net_load = np.maximum(0.0, load - renewable)
    ramp = np.zeros_like(net_load)
    ramp[1:] = np.diff(net_load)
    share = renewable / np.maximum(1.0, load)
    corridor_pressure = load / max(1.0, total_rating)
    ramp_pressure = np.abs(ramp) / np.maximum(1.0, load)
    stress = np.minimum(1.0, 0.55 * corridor_pressure + 0.25 * weighted_outage + 0.20 * ramp_pressure)
    features = np.column_stack((load, wind, pv, net_load, ramp, share, stress)).astype(np.float64)
    profile = {
        "hours": expected_hours,
        "source_rows": {"load": load_source_rows, "wind": wind_source_rows, "pv": pv_source_rows},
        "first_delivery_key": list(load_keys[0]),
        "last_delivery_key": list(load_keys[-1]),
        "branch_count": branch_count,
        "total_branch_rating": total_rating,
        "weighted_outage": weighted_outage,
        "source_files": {
            name: {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}
            for name, path in source_paths.items()
        },
    }
    return features, profile


def build_targets(features: np.ndarray, cap: float) -> np.ndarray:
    load = features[:, 0]
    renewable = features[:, 1] + features[:, 2]
    used = np.minimum(renewable, load * cap)
    return np.maximum(0.0, renewable - used) / np.maximum(1.0, renewable)


@dataclass
class Task:
    windows: np.ndarray
    y: np.ndarray
    target_t: np.ndarray
    fit: np.ndarray
    selection: np.ndarray
    calibration: np.ndarray
    test: np.ndarray
    event_threshold: float
    stress: np.ndarray
    horizon: int


def build_task(features: np.ndarray, targets: np.ndarray, horizon: int, config: dict[str, Any]) -> Task:
    total = len(targets)
    window = int(config["window"])
    parts = config["partitions"]
    fit_end = int(total * float(parts["fit_end_ratio"]))
    selection_end = int(total * float(parts["selection_end_ratio"]))
    calibration_end = int(total * float(parts["calibration_end_ratio"]))
    mu = features[:fit_end].mean(axis=0)
    sd = features[:fit_end].std(axis=0)
    sd[sd < 1e-9] = 1.0
    norm = (features - mu) / sd

    starts = np.arange(window - 1, total - horizon)
    target_t = starts + horizon
    windows = np.stack([norm[s - window + 1 : s + 1] for s in starts]).astype(np.float32)
    y = targets[target_t].astype(np.float32)
    fit = target_t < fit_end
    selection = (target_t >= fit_end + horizon) & (target_t < selection_end)
    calibration = (target_t >= selection_end + horizon) & (target_t < calibration_end)
    test = target_t >= calibration_end + horizon
    if not all(mask.any() for mask in (fit, selection, calibration, test)):
        raise ValueError(f"empty phase after embargo for horizon {horizon}")
    positive = y[fit][y[fit] > 0]
    event_threshold = max(0.02, float(np.quantile(positive, 0.50))) if positive.size >= 20 else 0.02
    share_q75 = float(np.quantile(features[:fit_end, 5], 0.75))
    stress = test & (features[target_t, 5] >= share_q75)
    return Task(windows, y, target_t, fit, selection, calibration, test, event_threshold, stress, horizon)


def f1_score(truth: np.ndarray, pred: np.ndarray) -> tuple[float, float, float]:
    truth = truth.astype(bool)
    pred = pred.astype(bool)
    tp = int(np.sum(truth & pred))
    recall = tp / max(1, int(truth.sum()))
    precision = tp / max(1, int(pred.sum()))
    f1 = 2 * precision * recall / max(1e-12, precision + recall)
    return float(f1), float(precision), float(recall)


def onset_mask(task: Task, targets_full: np.ndarray) -> np.ndarray:
    last_obs = targets_full[task.target_t - task.horizon]
    return (task.y >= 0.02) & (last_obs < 0.02)


def best_detection_threshold(preds: np.ndarray, events: np.ndarray, mask: np.ndarray, config: dict[str, Any]) -> tuple[float, str]:
    if int(events[mask].sum()) == 0:
        return 0.02, "fallback_no_positive_onsets"
    onset_cfg = config["onset"]
    quantiles = np.linspace(
        float(onset_cfg["detection_threshold_grid_start"]),
        float(onset_cfg["detection_threshold_grid_end"]),
        int(onset_cfg["detection_threshold_quantiles"]),
    )
    grid = np.unique(np.quantile(preds[mask], quantiles))
    best_threshold = float(grid[0])
    best_f1 = -1.0
    for threshold in grid:
        score, _, _ = f1_score(events[mask], preds[mask] >= threshold)
        if score > best_f1 + 1e-15:
            best_f1 = score
            best_threshold = float(threshold)
    return best_threshold, "calibrated"


def objective_loss(task: Task, preds: np.ndarray, targets_full: np.ndarray, objective: str, config: dict[str, Any]) -> float:
    mask = task.selection
    if objective == "mae":
        return float(np.mean(np.abs(task.y[mask] - preds[mask])))
    if objective == "onset_f1":
        events = onset_mask(task, targets_full)
        threshold, _ = best_detection_threshold(preds, events, mask, config)
        score, _, _ = f1_score(events[mask], preds[mask] >= threshold)
        return -score
    raise ValueError(f"unknown selection objective: {objective}")


def evaluate(task: Task, raw_preds: np.ndarray, targets_full: np.ndarray, config: dict[str, Any]) -> dict[str, Any]:
    preds = np.clip(raw_preds.astype(np.float64), 0.0, 1.0)
    test = task.test
    y = task.y.astype(np.float64)
    err = np.abs(y[test] - preds[test])
    events = y >= task.event_threshold
    event_f1, event_precision, event_recall = f1_score(events[test], preds[test] >= task.event_threshold)
    onsets = onset_mask(task, targets_full)
    detection_threshold, threshold_status = best_detection_threshold(preds, onsets, task.calibration, config)
    onset_f1, onset_precision, onset_recall = f1_score(onsets[test], preds[test] >= detection_threshold)
    onset_rows = test & onsets
    onset_mae = float(np.mean(np.abs(y[onset_rows] - preds[onset_rows]))) if onset_rows.any() else float("nan")
    stress_err = np.abs(y[task.stress] - preds[task.stress])
    return {
        "curtailment_mae": float(err.mean()),
        "curtailment_rmse": float(np.sqrt(np.mean((y[test] - preds[test]) ** 2))),
        "event_f1": event_f1,
        "event_precision": event_precision,
        "event_recall": event_recall,
        "onset_f1": onset_f1,
        "onset_precision": onset_precision,
        "onset_recall": onset_recall,
        "onset_mae": onset_mae,
        "stress_subset_mae": float(stress_err.mean()) if stress_err.size else float("nan"),
        "detection_threshold": detection_threshold,
        "threshold_status": threshold_status,
        "n_fit": int(task.fit.sum()),
        "n_selection": int(task.selection.sum()),
        "n_calibration": int(task.calibration.sum()),
        "n_test": int(task.test.sum()),
        "n_onsets_selection": int(onsets[task.selection].sum()),
        "n_onsets_calibration": int(onsets[task.calibration].sum()),
        "n_onsets_test": int(onsets[task.test].sum()),
        "n_events_test": int(events[task.test].sum()),
    }


def result_row(
    cap: float,
    task: Task,
    method: str,
    role: str,
    selection_objective: str,
    blend_mode: str,
    seed_index: int | str,
    seed: int | str,
    runtime_s: float,
    metrics: dict[str, Any],
    *,
    alpha: float | str = "NA",
    checkpoint_epoch: int | str = "NA",
    ridge_lambda: float | str = "NA",
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "run_namespace": "p1_s3_fair_v1",
        "cap": f"{cap:.2f}",
        "horizon_hours": task.horizon,
        "method": method,
        "method_role": role,
        "selection_objective": selection_objective,
        "blend_mode": blend_mode,
        "alpha_head": alpha,
        "checkpoint_epoch": checkpoint_epoch,
        "ridge_lambda": ridge_lambda,
        "seed_index": seed_index,
        "seed": seed,
        "runtime_s": f"{runtime_s:.6f}",
    }
    for key, value in metrics.items():
        if isinstance(value, float):
            row[key] = "nan" if math.isnan(value) else f"{value:.10f}"
        else:
            row[key] = value
    return row


def ridge_predictions(task: Task, targets_full: np.ndarray, objective: str, config: dict[str, Any]) -> tuple[np.ndarray, float]:
    x = task.windows.reshape(len(task.windows), -1).astype(np.float64)
    fit_x = x[task.fit]
    fit_y = task.y[task.fit].astype(np.float64)
    xtx = fit_x.T @ fit_x
    xty = fit_x.T @ fit_y
    identity = np.eye(xtx.shape[0], dtype=np.float64)
    best_preds: np.ndarray | None = None
    best_lambda = float(config["ridge_lambdas"][0])
    best_loss = float("inf")
    for value in config["ridge_lambdas"]:
        ridge_lambda = float(value)
        beta = np.linalg.solve(xtx + ridge_lambda * identity, xty)
        preds = x @ beta
        loss = objective_loss(task, preds, targets_full, objective, config)
        if loss < best_loss - 1e-15:
            best_loss = loss
            best_lambda = ridge_lambda
            best_preds = preds
    assert best_preds is not None
    return best_preds, best_lambda


class GRURegressor(nn.Module):
    def __init__(self, n_features: int, hidden_size: int) -> None:
        super().__init__()
        self.rnn = nn.GRU(input_size=n_features, hidden_size=hidden_size, num_layers=1, batch_first=True)
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        output, _ = self.rnn(x)
        embedding = output[:, -1]
        return self.head(embedding).squeeze(-1), embedding


def train_gru_checkpoints(task: Task, seed: int, device: torch.device, config: dict[str, Any]) -> tuple[GRURegressor, dict[int, dict[str, torch.Tensor]]]:
    gru_cfg = config["gru"]
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    model = GRURegressor(task.windows.shape[2], int(gru_cfg["hidden_size"])).to(device)
    loss_fn = nn.MSELoss()
    parameters = list(model.parameters())
    first_moment = [torch.zeros_like(parameter) for parameter in parameters]
    second_moment = [torch.zeros_like(parameter) for parameter in parameters]
    beta1, beta2, epsilon = 0.9, 0.999, 1e-8
    learning_rate = float(gru_cfg["learning_rate"])
    adam_step = 0
    x = torch.tensor(task.windows, dtype=torch.float32, device=device)
    y = torch.tensor(task.y, dtype=torch.float32, device=device)
    fit_idx = np.flatnonzero(task.fit)
    generator = torch.Generator(device="cpu")
    generator.manual_seed(seed)
    checkpoints: dict[int, dict[str, torch.Tensor]] = {}
    checkpoint_epochs = {int(v) for v in gru_cfg["checkpoint_epochs"]}
    batch_size = int(gru_cfg["batch_size"])
    for epoch in range(1, int(gru_cfg["epochs"]) + 1):
        model.train()
        order = torch.randperm(len(fit_idx), generator=generator).numpy()
        for offset in range(0, len(order), batch_size):
            idx = torch.tensor(fit_idx[order[offset : offset + batch_size]], dtype=torch.long, device=device)
            for parameter in parameters:
                parameter.grad = None
            pred, _ = model(x[idx])
            loss = loss_fn(pred, y[idx])
            loss.backward()
            adam_step += 1
            with torch.no_grad():
                for parameter, moment1, moment2 in zip(parameters, first_moment, second_moment):
                    if parameter.grad is None:
                        continue
                    gradient = parameter.grad
                    moment1.mul_(beta1).add_(gradient, alpha=1.0 - beta1)
                    moment2.mul_(beta2).addcmul_(gradient, gradient, value=1.0 - beta2)
                    bias1 = 1.0 - beta1**adam_step
                    bias2 = 1.0 - beta2**adam_step
                    denominator = moment2.sqrt().div_(math.sqrt(bias2)).add_(epsilon)
                    parameter.addcdiv_(moment1, denominator, value=-learning_rate / bias1)
        if epoch in checkpoint_epochs:
            checkpoints[epoch] = {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()}
    if set(checkpoints) != checkpoint_epochs:
        raise RuntimeError("not all frozen checkpoint epochs were captured")
    return model, checkpoints


def infer_model(
    model: GRURegressor,
    state: dict[str, torch.Tensor],
    windows: np.ndarray,
    device: torch.device,
    indices: np.ndarray | None = None,
    batch_size: int = 1024,
) -> tuple[np.ndarray, np.ndarray]:
    model.load_state_dict(state)
    model.eval()
    if indices is None:
        indices = np.arange(len(windows))
    pred_parts: list[np.ndarray] = []
    embedding_parts: list[np.ndarray] = []
    with torch.no_grad():
        for offset in range(0, len(indices), batch_size):
            idx = indices[offset : offset + batch_size]
            x = torch.tensor(windows[idx], dtype=torch.float32, device=device)
            pred, embedding = model(x)
            pred_parts.append(pred.cpu().numpy())
            embedding_parts.append(embedding.cpu().numpy())
    return np.concatenate(pred_parts), np.concatenate(embedding_parts)


def retrieval_predictions(task: Task, space: np.ndarray, device: torch.device, k: int) -> np.ndarray:
    fit_idx = np.flatnonzero(task.fit)
    query_mask = task.selection | task.calibration | task.test
    query_idx = np.flatnonzero(query_mask)
    bank = torch.tensor(space[fit_idx], dtype=torch.float32, device=device)
    bank_y = torch.tensor(task.y[fit_idx], dtype=torch.float32, device=device)
    output = np.full(len(task.y), np.nan, dtype=np.float64)
    batch_size = 1024
    with torch.no_grad():
        for offset in range(0, len(query_idx), batch_size):
            idx = query_idx[offset : offset + batch_size]
            query = torch.tensor(space[idx], dtype=torch.float32, device=device)
            distances = torch.cdist(query, bank)
            neighbors = torch.topk(distances, k=k, dim=1, largest=False).indices
            values = bank_y[neighbors].mean(dim=1).cpu().numpy()
            output[idx] = values
    if np.isnan(output[query_mask]).any():
        raise RuntimeError("retrieval prediction missing in a scored phase")
    return output


def run_gru_conditions(
    cap: float,
    task: Task,
    targets_full: np.ndarray,
    seed_index: int,
    seed: int,
    device: torch.device,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    start = time.perf_counter()
    model, checkpoints = train_gru_checkpoints(task, seed, device, config)
    selection_idx = np.flatnonzero(task.selection)
    selected_epochs: dict[str, int] = {}
    for objective in config["selection_objectives"]:
        best_epoch = int(config["gru"]["checkpoint_epochs"][0])
        best_loss = float("inf")
        for epoch in config["gru"]["checkpoint_epochs"]:
            selected_pred, _ = infer_model(model, checkpoints[int(epoch)], task.windows, device, selection_idx)
            preds = np.zeros(len(task.y), dtype=np.float64)
            preds[selection_idx] = selected_pred
            loss = objective_loss(task, preds, targets_full, objective, config)
            if loss < best_loss - 1e-15:
                best_loss = loss
                best_epoch = int(epoch)
        selected_epochs[objective] = best_epoch

    rows: list[dict[str, Any]] = []
    for objective in config["selection_objectives"]:
        epoch = selected_epochs[objective]
        head, embedding = infer_model(model, checkpoints[epoch], task.windows, device)
        retrieved = retrieval_predictions(task, embedding, device, int(config["retrieval"]["k_neighbors"]))
        best_alpha = float(config["retrieval"]["alpha_grid"][0])
        best_loss = float("inf")
        for alpha_value in config["retrieval"]["alpha_grid"]:
            alpha = float(alpha_value)
            blended = head.copy().astype(np.float64)
            mask = task.selection | task.calibration | task.test
            blended[mask] = alpha * head[mask] + (1.0 - alpha) * retrieved[mask]
            loss = objective_loss(task, blended, targets_full, objective, config)
            if loss < best_loss - 1e-15:
                best_loss = loss
                best_alpha = alpha

        controls: list[tuple[str, str, float]] = [("GRU-LSR", "selected", best_alpha)]
        controls.extend(
            (f"GRU-LSR-Fixed{alpha:g}", f"fixed_{alpha:g}", alpha)
            for alpha in (float(v) for v in config["retrieval"]["fixed_alpha_controls"])
        )
        elapsed = time.perf_counter() - start
        for method, blend_mode, alpha in controls:
            preds = head.copy().astype(np.float64)
            mask = task.selection | task.calibration | task.test
            preds[mask] = alpha * head[mask] + (1.0 - alpha) * retrieved[mask]
            metrics = evaluate(task, preds, targets_full, config)
            role = "proposed" if blend_mode == "selected" else "mechanism_control"
            rows.append(
                result_row(
                    cap,
                    task,
                    method,
                    role,
                    objective,
                    blend_mode,
                    seed_index,
                    seed,
                    elapsed,
                    metrics,
                    alpha=f"{alpha:.6f}",
                    checkpoint_epoch=epoch,
                )
            )
    return rows


def mean(values: Iterable[float]) -> float:
    vals = list(values)
    return float(sum(vals) / len(vals))


METRICS = ("curtailment_mae", "curtailment_rmse", "event_f1", "onset_f1", "onset_mae", "stress_subset_mae")


def aggregate_results(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    group_fields = ("cap", "horizon_hours", "method", "method_role", "selection_objective", "blend_mode")
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(tuple(row[field] for field in group_fields), []).append(row)
    board: list[dict[str, Any]] = []
    for key, items in groups.items():
        record = dict(zip(group_fields, key))
        record["n_seeds"] = len(items)
        alphas = [float(item["alpha_head"]) for item in items if item["alpha_head"] != "NA"]
        epochs = [float(item["checkpoint_epoch"]) for item in items if item["checkpoint_epoch"] != "NA"]
        lambdas = [float(item["ridge_lambda"]) for item in items if item["ridge_lambda"] != "NA"]
        record["mean_alpha_head"] = f"{mean(alphas):.8f}" if alphas else "NA"
        record["mean_checkpoint_epoch"] = f"{mean(epochs):.4f}" if epochs else "NA"
        record["mean_ridge_lambda"] = f"{mean(lambdas):.8g}" if lambdas else "NA"
        for metric in METRICS:
            values = [float(item[metric]) for item in items if item[metric] != "nan"]
            record[f"mean_{metric}"] = f"{mean(values):.10f}" if values else "nan"
            record[f"std_{metric}"] = f"{statistics.stdev(values):.10f}" if len(values) > 1 else "0.0000000000"
        board.append(record)
    board.sort(key=lambda row: (float(row["cap"]), int(row["horizon_hours"]), row["selection_objective"], row["method"], row["blend_mode"]))
    return board


def exact_sign_flip_pvalue(differences: np.ndarray) -> float:
    observed = abs(float(np.mean(differences)))
    count = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(differences)):
        statistic = abs(float(np.mean(differences * np.asarray(signs))))
        count += statistic >= observed - 1e-15
        total += 1
    return count / total


def holm(pvalues: list[float]) -> list[float]:
    order = np.argsort(pvalues)
    adjusted = [0.0] * len(pvalues)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (len(pvalues) - rank) * pvalues[int(idx)]))
        adjusted[int(idx)] = running
    return adjusted


def primary_paired_table(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary = [row for row in rows if row["cap"] == "0.70" and row["method"].startswith("GRU-LSR")]
    contrasts = [
        ("selected_retrieval_vs_head_mae", "mae", "selected", "fixed_1", "curtailment_mae", "lower"),
        ("selected_retrieval_vs_head_onset", "onset_f1", "selected", "fixed_1", "onset_f1", "higher"),
        ("fixed_half_vs_head_mae", "mae", "fixed_0.5", "fixed_1", "curtailment_mae", "lower"),
        ("fixed_half_vs_head_onset", "onset_f1", "fixed_0.5", "fixed_1", "onset_f1", "higher"),
        ("selected_vs_fixed_half_mae", "mae", "selected", "fixed_0.5", "curtailment_mae", "lower"),
        ("selected_vs_fixed_half_onset", "onset_f1", "selected", "fixed_0.5", "onset_f1", "higher"),
    ]
    output: list[dict[str, Any]] = []
    for horizon in (1, 24):
        horizon_rows: list[dict[str, Any]] = []
        pvalues: list[float] = []
        for contrast_id, objective, treatment_blend, control_blend, metric, better in contrasts:
            treatment = {
                int(row["seed_index"]): float(row[metric])
                for row in primary
                if int(row["horizon_hours"]) == horizon
                and row["selection_objective"] == objective
                and row["blend_mode"] == treatment_blend
            }
            control = {
                int(row["seed_index"]): float(row[metric])
                for row in primary
                if int(row["horizon_hours"]) == horizon
                and row["selection_objective"] == objective
                and row["blend_mode"] == control_blend
            }
            common = sorted(set(treatment) & set(control))
            if len(common) != 10:
                raise ValueError(f"paired primary contrast {contrast_id} has {len(common)} pairs")
            diffs = np.asarray([treatment[idx] - control[idx] for idx in common], dtype=np.float64)
            pvalue = exact_sign_flip_pvalue(diffs)
            pvalues.append(pvalue)
            favorable = diffs < 0 if better == "lower" else diffs > 0
            horizon_rows.append(
                {
                    "horizon_hours": horizon,
                    "contrast_id": contrast_id,
                    "selection_objective": objective,
                    "treatment_blend": treatment_blend,
                    "control_blend": control_blend,
                    "metric": metric,
                    "better_direction": better,
                    "n_pairs": len(common),
                    "mean_treatment_minus_control": f"{float(np.mean(diffs)):.10f}",
                    "median_treatment_minus_control": f"{float(np.median(diffs)):.10f}",
                    "treatment_wins": int(favorable.sum()),
                    "ties": int((np.abs(diffs) <= 1e-15).sum()),
                    "control_wins": int((~favorable & (np.abs(diffs) > 1e-15)).sum()),
                    "p_exact_sign_flip": f"{pvalue:.10f}",
                }
            )
        for record, adjusted in zip(horizon_rows, holm(pvalues)):
            record["p_holm_within_horizon"] = f"{adjusted:.10f}"
            record["holm_significant_005"] = str(adjusted < 0.05)
        output.extend(horizon_rows)
    return output


def cap_sensitivity_table(board: list[dict[str, Any]]) -> list[dict[str, Any]]:
    primary_index: dict[tuple[Any, ...], dict[str, Any]] = {}
    key_fields = ("horizon_hours", "method", "selection_objective", "blend_mode")
    for row in board:
        if row["cap"] == "0.70":
            primary_index[tuple(row[field] for field in key_fields)] = row
    output: list[dict[str, Any]] = []
    for row in board:
        key = tuple(row[field] for field in key_fields)
        reference = primary_index.get(key)
        if reference is None:
            continue
        record = {field: row[field] for field in ("cap",) + key_fields}
        record["n_seeds"] = row["n_seeds"]
        for metric in ("curtailment_mae", "onset_f1", "onset_mae"):
            value = float(row[f"mean_{metric}"])
            base = float(reference[f"mean_{metric}"])
            record[f"mean_{metric}"] = f"{value:.10f}"
            record[f"delta_vs_cap_0.70_{metric}"] = f"{value - base:.10f}"
        output.append(record)
    output.sort(key=lambda row: (int(row["horizon_hours"]), row["method"], row["selection_objective"], row["blend_mode"], float(row["cap"])))
    return output


def policy_audit_rows(config: dict[str, Any], profile: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    audit: list[dict[str, Any]] = []
    for name, source in profile["source_files"].items():
        audit.append(
            {
                "record_type": "source_file",
                "item": name,
                "value": source["path"],
                "sha256": source["sha256"],
                "scope": "delivery-row DAY_AHEAD input; issue time and vintage not recorded" if name in {"load", "wind", "pv"} else "static branch input",
            }
        )
    direct = [row for row in rows if row["method"] == "DirectPolicyTransform-Privileged"]
    for row in direct:
        audit.append(
            {
                "record_type": "direct_control_result",
                "item": f"cap={row['cap']};horizon={row['horizon_hours']}",
                "value": f"mae={row['curtailment_mae']};onset_f1={row['onset_f1']}",
                "sha256": "NA",
                "scope": config["direct_policy_transform"]["scope"],
            }
        )
    return audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=RUN_DIR / "config.json")
    parser.add_argument("--rts-data", type=Path, required=True)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = RUN_DIR / "run_manifest.json"
    if manifest_path.exists():
        prior = json.loads(manifest_path.read_text(encoding="utf-8"))
        if prior.get("status") == "completed":
            raise SystemExit("completed run namespace exists; refusing to overwrite")
        raise SystemExit("partial run namespace exists; preserve it and use a new namespace")

    config = json.loads(args.config.read_text(encoding="utf-8"))
    if config["run_namespace"] != RUN_DIR.name:
        raise ValueError("config namespace does not match directory")
    log = RunLog(LOG_DIR / "run.log")
    device = torch.device("cuda" if args.device == "auto" and torch.cuda.is_available() else ("cpu" if args.device == "auto" else args.device))
    torch.set_num_threads(4)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    # The preserved torch environment does not include sympy, which torch 2.13
    # imports when the global deterministic-algorithm switch is enabled.  The
    # exercised GRU path is instead constrained with fixed seeds, deterministic
    # cuDNN, disabled benchmarking, and CUBLAS_WORKSPACE_CONFIG.  Record this
    # exact boundary rather than claiming the unavailable global enforcement.
    log.emit(f"loading frozen configuration {sha256(args.config)}")
    features, source_profile = load_features(args.rts_data.resolve(), config)
    log.emit(f"validated {len(features)} aligned delivery rows and {source_profile['branch_count']} branches")
    if args.dry_run:
        log.emit("dry-run complete; no run namespace manifest or result table written")
        return 0

    command = [sys.executable, str(Path(__file__).resolve()), "--rts-data", str(args.rts_data.resolve()), "--device", args.device]
    manifest: dict[str, Any] = {
        "run_namespace": config["run_namespace"],
        "status": "running",
        "started_at": utc_now(),
        "command": command,
        "config_sha256": sha256(args.config),
        "script_sha256": sha256(Path(__file__)),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "torch": torch.__version__,
            "device": str(device),
            "cuda_version": torch.version.cuda,
            "cuda_device": torch.cuda.get_device_name(0) if device.type == "cuda" else "NA",
            "global_deterministic_algorithms_enforced": False,
            "cudnn_deterministic": True,
            "cudnn_benchmark": False,
            "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
        },
        "source_profile": source_profile,
        "evidence_boundary": {
            "primary_cap": config["primary_cap"],
            "paired_seed_primary": True,
            "direct_control_privileged": True,
            "operational_issue_time_available": False,
            "data_vintage_available": False,
            "cap_sensitivity_scope": "same system and weather year; descriptive method-level reruns",
        },
        "outputs": {},
    }
    write_json_atomic(manifest_path, manifest)

    rows: list[dict[str, Any]] = []
    try:
        for cap in (float(value) for value in config["caps"]):
            targets = build_targets(features, cap)
            log.emit(f"cap {cap:.2f}: nonzero target share={(targets > 0).mean():.6f}")
            for horizon in (int(value) for value in config["horizons"]):
                task = build_task(features, targets, horizon, config)
                log.emit(
                    f"cap {cap:.2f} h{horizon}: phase counts fit={task.fit.sum()} selection={task.selection.sum()} "
                    f"calibration={task.calibration.sum()} test={task.test.sum()}"
                )
                deterministic = [
                    ("DirectPolicyTransform-Privileged", "privileged_control", task.y.astype(np.float64)),
                    ("Persistence", "baseline", targets[task.target_t - horizon]),
                    ("Seasonal-24h", "baseline", targets[np.maximum(task.target_t - 24, 0)]),
                ]
                for method, role, preds in deterministic:
                    start = time.perf_counter()
                    metrics = evaluate(task, preds, targets, config)
                    rows.append(result_row(cap, task, method, role, "not_applicable", "not_applicable", 0, "deterministic", time.perf_counter() - start, metrics))
                for objective in config["selection_objectives"]:
                    start = time.perf_counter()
                    preds, ridge_lambda = ridge_predictions(task, targets, objective, config)
                    metrics = evaluate(task, preds, targets, config)
                    rows.append(
                        result_row(
                            cap,
                            task,
                            "Ridge",
                            "baseline",
                            objective,
                            "not_applicable",
                            0,
                            "deterministic",
                            time.perf_counter() - start,
                            metrics,
                            ridge_lambda=f"{ridge_lambda:.8g}",
                        )
                    )
                for seed_index, seed in enumerate(int(value) for value in config["gru"]["seeds"]):
                    seed_rows = run_gru_conditions(cap, task, targets, seed_index, seed, device, config)
                    rows.extend(seed_rows)
                    write_csv_atomic(RESULT_DIR / "run_results.partial.csv", rows)
                    log.emit(f"cap {cap:.2f} h{horizon}: GRU seed {seed_index} ({seed}) complete")

        write_csv_atomic(RESULT_DIR / "run_results.csv", rows)
        board = aggregate_results(rows)
        paired = primary_paired_table(rows)
        cap_table = cap_sensitivity_table(board)
        policy_audit = policy_audit_rows(config, source_profile, rows)
        write_csv_atomic(RESULT_DIR / "leaderboard.csv", board)
        write_csv_atomic(RESULT_DIR / "paired_primary.csv", paired)
        write_csv_atomic(RESULT_DIR / "cap_sensitivity.csv", cap_table)
        write_csv_atomic(RESULT_DIR / "policy_transform_audit.csv", policy_audit)
        partial = RESULT_DIR / "run_results.partial.csv"
        if partial.exists():
            partial.rename(RESULT_DIR / "run_results.completed_snapshot.csv")
        outputs = {}
        for path in sorted(RESULT_DIR.glob("*")):
            if path.is_file():
                outputs[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
        manifest["status"] = "completed"
        manifest["completed_at"] = utc_now()
        manifest["row_counts"] = {
            "run_results": len(rows),
            "leaderboard": len(board),
            "paired_primary": len(paired),
            "cap_sensitivity": len(cap_table),
            "policy_transform_audit": len(policy_audit),
        }
        manifest["outputs"] = outputs
        write_json_atomic(manifest_path, manifest)
        log.emit(f"completed namespace with {len(rows)} method-seed rows")
    except Exception as exc:
        manifest["status"] = "failed_preserved"
        manifest["failed_at"] = utc_now()
        manifest["failure_type"] = type(exc).__name__
        manifest["failure_message"] = str(exc)
        manifest["preserved_partial_rows"] = len(rows)
        write_json_atomic(manifest_path, manifest)
        log.emit(f"FAILED and preserved: {type(exc).__name__}: {exc}")
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
