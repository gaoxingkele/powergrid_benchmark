"""Execute the prospectively frozen P1 IEEE Access upgrade experiment.

The normative configuration is ``upgrade_contract.json``.  This runner writes
only inside its own namespace, records every expected key (including controlled
failures), and refuses to overwrite any manifest-bearing execution.
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
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
CONTRACT_PATH = HERE / "upgrade_contract.json"
RESULT_DIR = HERE / "results"
LOG_DIR = HERE / "logs"
RUN_NAMESPACE = "p1_ieee_access_upgrade_v2"
NULL = ""
METRIC_FIELDS = (
    "curtailment_mae",
    "curtailment_rmse",
    "event_f1",
    "event_precision",
    "event_recall",
    "onset_f1",
    "onset_precision",
    "onset_recall",
    "onset_mae",
    "stress_subset_mae",
)


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


def format_float(value: float | None, digits: int = 12) -> str:
    if value is None or not math.isfinite(value):
        return NULL
    return f"{value:.{digits}g}"


def write_json_atomic(path: Path, value: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_csv_atomic(path: Path, rows: list[dict[str, Any]], fieldnames: Iterable[str] | None = None) -> None:
    if not rows and fieldnames is None:
        raise ValueError(f"cannot infer columns for empty table: {path}")
    names = list(fieldnames or rows[0].keys())
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def write_npz_atomic(path: Path, arrays: dict[str, np.ndarray]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("wb") as handle:
        np.savez_compressed(handle, **arrays)
    tmp.replace(path)


class RunLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def emit(self, message: str) -> None:
        line = f"[{utc_now()}] {message}"
        print(line, flush=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def sync(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def sanitized_exception(exc: BaseException) -> tuple[str, str, str]:
    if isinstance(exc, (MemoryError, torch.cuda.OutOfMemoryError)):
        code = "resource_error"
        status = "failed_resource"
    elif isinstance(exc, (FloatingPointError, OverflowError)):
        code = "nonfinite_error"
        status = "failed_nonfinite"
    elif isinstance(exc, (FileNotFoundError, ValueError, AssertionError)):
        code = "integrity_error"
        status = "failed_integrity"
    else:
        code = "execution_exception"
        status = "failed_exception"
    return status, code, type(exc).__name__


def load_timeseries(path: Path, evaluated_rows: int) -> tuple[list[tuple[int, int, int, int]], np.ndarray, int]:
    keys: list[tuple[int, int, int, int]] = []
    totals: list[float] = []
    with path.open(encoding="utf-8", errors="strict", newline="") as handle:
        for row in csv.DictReader(handle):
            keys.append(tuple(int(row[name]) for name in ("Year", "Month", "Day", "Period")))
            totals.append(
                sum(parse_float(value) for name, value in row.items() if name not in {"Year", "Month", "Day", "Period"})
            )
    source_rows = len(keys)
    if source_rows != 8784 or source_rows < evaluated_rows:
        raise ValueError(f"unexpected source row count for {path.name}: {source_rows}")
    return keys[:evaluated_rows], np.asarray(totals[:evaluated_rows], dtype=np.float64), source_rows


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
    if not ratings:
        raise ValueError("branch table contains no positive contingency ratings")
    total_rating = float(sum(ratings))
    return total_rating, float(sum(weighted) / total_rating), len(ratings)


def load_features(rts_data: Path, contract: dict[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    scope = contract["scope"]
    evaluated_rows = int(scope["source_sequence"]["evaluated_rows"])
    paths = {name: rts_data / item["relative_path"] for name, item in scope["source_files"].items()}
    profile_files: dict[str, Any] = {}
    for name, path in paths.items():
        if not path.is_file():
            raise FileNotFoundError(f"missing frozen source: {name}")
        observed = sha256(path)
        expected = scope["source_files"][name]["sha256"]
        if observed != expected:
            raise ValueError(f"source hash mismatch: {name}")
        profile_files[name] = {"path": str(path.resolve()), "sha256": observed, "bytes": path.stat().st_size}

    load_keys, load, load_rows = load_timeseries(paths["load"], evaluated_rows)
    wind_keys, wind, wind_rows = load_timeseries(paths["wind"], evaluated_rows)
    pv_keys, pv, pv_rows = load_timeseries(paths["pv"], evaluated_rows)
    if load_keys != wind_keys or load_keys != pv_keys:
        raise ValueError("load/wind/PV delivery keys are not aligned")
    if load_keys[0] != (2020, 1, 1, 1) or load_keys[-1] != (2020, 12, 30, 24):
        raise ValueError("evaluated delivery-key boundary differs from contract")

    total_rating, weighted_outage, branch_count = load_branch_constants(paths["branch"])
    renewable = wind + pv
    net_load = np.maximum(0.0, load - renewable)
    ramp = np.zeros_like(net_load)
    ramp[1:] = np.diff(net_load)
    share = renewable / np.maximum(1.0, load)
    corridor_pressure = load / max(1.0, total_rating)
    ramp_pressure = np.abs(ramp) / np.maximum(1.0, load)
    stress = np.minimum(1.0, 0.55 * corridor_pressure + 0.25 * weighted_outage + 0.20 * ramp_pressure)
    features = np.column_stack((load, wind, pv, net_load, ramp, share, stress)).astype(np.float64)
    if not np.isfinite(features).all() or features.shape != (8760, 7):
        raise ValueError(f"invalid feature matrix: {features.shape}")
    return features, {
        "evaluated_rows": evaluated_rows,
        "source_rows": {"load": load_rows, "wind": wind_rows, "pv": pv_rows},
        "first_delivery_key": list(load_keys[0]),
        "last_delivery_key": list(load_keys[-1]),
        "branch_count": branch_count,
        "total_branch_rating": total_rating,
        "weighted_outage": weighted_outage,
        "source_files": profile_files,
    }


def build_targets(features: np.ndarray, cap: float) -> np.ndarray:
    load = features[:, 0]
    renewable = features[:, 1] + features[:, 2]
    accepted = np.minimum(renewable, cap * load)
    return np.maximum(0.0, renewable - accepted) / np.maximum(1.0, renewable)


@dataclass
class Task:
    windows: np.ndarray
    y: np.ndarray
    target_t: np.ndarray
    fit: np.ndarray
    selection: np.ndarray
    calibration: np.ndarray
    test: np.ndarray
    stress: np.ndarray
    event_threshold: float
    horizon: int


def build_task(features: np.ndarray, targets: np.ndarray, horizon: int, contract: dict[str, Any]) -> Task:
    temporal = contract["temporal_protocol"]
    per_horizon = temporal["per_horizon"][str(horizon)]
    window = int(temporal["query_window_rows"])
    mu = features[:4380].mean(axis=0)
    sd = features[:4380].std(axis=0)
    sd[sd < 1e-9] = 1.0
    normalized = (features - mu) / sd
    query_end = np.arange(window - 1, len(targets) - horizon, dtype=np.int64)
    target_t = query_end + horizon
    windows = np.stack([normalized[s - window + 1 : s + 1] for s in query_end]).astype(np.float32)

    def interval_mask(name: str) -> np.ndarray:
        start, end = (int(v) for v in per_horizon[name])
        return (target_t >= start) & (target_t < end)

    fit = interval_mask("fit")
    selection = interval_mask("selection")
    calibration = interval_mask("calibration")
    test = interval_mask("test")
    counts = per_horizon["counts"]
    actual = {name: int(mask.sum()) for name, mask in (("fit", fit), ("selection", selection), ("calibration", calibration), ("test", test))}
    for name in actual:
        if actual[name] != int(counts[name]):
            raise ValueError(f"phase count mismatch h={horizon} {name}: {actual[name]}")
    if np.any(fit & selection) or np.any(selection & calibration) or np.any(calibration & test):
        raise ValueError("temporal phase overlap")
    positive = targets[target_t][fit]
    positive = positive[positive > 0]
    event_threshold = max(0.02, float(np.quantile(positive, 0.5))) if positive.size >= 20 else 0.02
    share_q75 = float(np.quantile(features[:4380, 5], 0.75))
    stress = test & (features[target_t, 5] >= share_q75)
    return Task(windows, targets[target_t].astype(np.float64), target_t, fit, selection, calibration, test, stress, event_threshold, horizon)


def f1_score(truth: np.ndarray, predicted: np.ndarray) -> tuple[float, float, float]:
    truth = truth.astype(bool)
    predicted = predicted.astype(bool)
    tp = int(np.sum(truth & predicted))
    recall = tp / max(1, int(truth.sum()))
    precision = tp / max(1, int(predicted.sum()))
    f1 = 2.0 * precision * recall / max(1e-12, precision + recall)
    return float(f1), float(precision), float(recall)


def onset_mask(task: Task, targets: np.ndarray) -> np.ndarray:
    return (task.y >= 0.02) & (targets[task.target_t - task.horizon] < 0.02)


def choose_detection_threshold(
    predictions: np.ndarray, onsets: np.ndarray, mask: np.ndarray, contract: dict[str, Any]
) -> tuple[float, str]:
    protocol = contract["onset_protocol"]
    if int(onsets[mask].sum()) == 0:
        return float(protocol["zero_positive_fallback_threshold"]), protocol["zero_positive_status"]
    probabilities = np.linspace(
        float(protocol["quantile_probability_start"]),
        float(protocol["quantile_probability_end"]),
        int(protocol["calibration_quantiles"]),
    )
    grid = np.unique(np.quantile(predictions[mask], probabilities))
    best_threshold = float(grid[0])
    best_f1 = -1.0
    for threshold in grid:
        value, _, _ = f1_score(onsets[mask], predictions[mask] >= threshold)
        if value > best_f1 + 1e-15:
            best_f1 = value
            best_threshold = float(threshold)
    return best_threshold, "calibrated"


def selection_loss(
    task: Task, predictions: np.ndarray, targets: np.ndarray, objective: str, contract: dict[str, Any]
) -> float:
    if not np.isfinite(predictions[task.selection]).all():
        raise FloatingPointError("nonfinite selection predictions")
    if objective == "mae":
        return float(np.mean(np.abs(task.y[task.selection] - predictions[task.selection])))
    if objective == "onset_f1":
        onsets = onset_mask(task, targets)
        threshold, _ = choose_detection_threshold(predictions, onsets, task.selection, contract)
        value, _, _ = f1_score(onsets[task.selection], predictions[task.selection] >= threshold)
        return -value
    raise ValueError(f"unknown objective: {objective}")


def evaluate(task: Task, raw_predictions: np.ndarray, targets: np.ndarray, contract: dict[str, Any]) -> tuple[dict[str, Any], np.ndarray]:
    scored_mask = task.selection | task.calibration | task.test
    if not np.isfinite(raw_predictions[scored_mask]).all():
        raise FloatingPointError("nonfinite scored predictions")
    predictions = np.clip(raw_predictions.astype(np.float64), 0.0, 1.0)
    test = task.test
    y = task.y
    errors = np.abs(y[test] - predictions[test])
    events = y >= task.event_threshold
    event_f1, event_precision, event_recall = f1_score(events[test], predictions[test] >= task.event_threshold)
    onsets = onset_mask(task, targets)
    threshold, threshold_status = choose_detection_threshold(predictions, onsets, task.calibration, contract)
    onset_f1, onset_precision, onset_recall = f1_score(onsets[test], predictions[test] >= threshold)
    onset_rows = test & onsets
    onset_mae = float(np.mean(np.abs(y[onset_rows] - predictions[onset_rows]))) if onset_rows.any() else math.nan
    stress_errors = np.abs(y[task.stress] - predictions[task.stress])
    n_selection = int(onsets[task.selection].sum())
    n_calibration = int(onsets[task.calibration].sum())
    claim_valid = n_selection > 0 and n_calibration > 0
    metrics = {
        "curtailment_mae": float(errors.mean()),
        "curtailment_rmse": float(np.sqrt(np.mean((y[test] - predictions[test]) ** 2))),
        "event_f1": event_f1,
        "event_precision": event_precision,
        "event_recall": event_recall,
        "onset_f1": onset_f1,
        "onset_precision": onset_precision,
        "onset_recall": onset_recall,
        "onset_mae": onset_mae,
        "stress_subset_mae": float(stress_errors.mean()) if stress_errors.size else math.nan,
        "detection_threshold": threshold,
        "threshold_status": threshold_status,
        "onset_targeted_claim_valid": claim_valid,
        "scientific_support_status": "supported" if claim_valid else "onset_diagnostic_only_no_pretest_support",
        "n_fit": int(task.fit.sum()),
        "n_selection": int(task.selection.sum()),
        "n_calibration": int(task.calibration.sum()),
        "n_test": int(task.test.sum()),
        "n_onsets_selection": n_selection,
        "n_onsets_calibration": n_calibration,
        "n_onsets_test": int(onsets[test].sum()),
        "n_events_test": int(events[test].sum()),
    }
    return metrics, predictions[test].copy()


class GRURegressor(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.rnn = nn.GRU(7, 48, num_layers=1, batch_first=True, dropout=0.0, bidirectional=False)
        self.head = nn.Linear(48, 1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        output, _ = self.rnn(x)
        representation = output[:, -1, :]
        return self.head(representation).squeeze(-1), representation


class LSTMRegressor(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.rnn = nn.LSTM(7, 48, num_layers=1, batch_first=True, dropout=0.0, bidirectional=False)
        self.head = nn.Linear(48, 1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        output, _ = self.rnn(x)
        representation = output[:, -1, :]
        return self.head(representation).squeeze(-1), representation


class DLinearRegressor(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.trend_map = nn.Linear(48, 1)
        self.seasonal_map = nn.Linear(48, 1)
        self.head = nn.Linear(7, 1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        channels = x.transpose(1, 2)
        trend = F.avg_pool1d(F.pad(channels, (12, 12), mode="replicate"), kernel_size=25, stride=1)
        seasonal = channels - trend
        feature_forecast = self.trend_map(trend).squeeze(-1) + self.seasonal_map(seasonal).squeeze(-1)
        return self.head(feature_forecast).squeeze(-1), feature_forecast


class CausalConv(nn.Module):
    def __init__(self, dilation: int) -> None:
        super().__init__()
        self.left_pad = 2 * dilation
        self.conv = nn.Conv1d(48, 48, kernel_size=3, dilation=dilation, padding=0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(F.pad(x, (self.left_pad, 0)))


class ResidualTCNBlock(nn.Module):
    def __init__(self, dilation: int) -> None:
        super().__init__()
        self.conv1 = CausalConv(dilation)
        self.conv2 = CausalConv(dilation)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + F.relu(self.conv2(F.relu(self.conv1(x))))


class TCNRegressor(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.input_projection = nn.Conv1d(7, 48, kernel_size=1)
        self.block1 = ResidualTCNBlock(1)
        self.block2 = ResidualTCNBlock(2)
        self.head = nn.Linear(48, 1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        output = self.input_projection(x.transpose(1, 2))
        output = self.block2(self.block1(output))
        representation = output[:, :, -1]
        return self.head(representation).squeeze(-1), representation


ARCHITECTURES: dict[str, type[nn.Module]] = {
    "GRU": GRURegressor,
    "LSTM": LSTMRegressor,
    "DLinear": DLinearRegressor,
    "TCN": TCNRegressor,
}


def model_parameter_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    state = torch.random.get_rng_state()
    try:
        for name, model_type in ARCHITECTURES.items():
            torch.manual_seed(0)
            counts[name] = sum(parameter.numel() for parameter in model_type().parameters())
        torch.manual_seed(0)
        counts["randomized_GRU_encoder"] = sum(parameter.numel() for parameter in GRURegressor().rnn.parameters())
    finally:
        torch.random.set_rng_state(state)
    return counts


def initialize_model(model_type: type[nn.Module], seed: int, device: torch.device) -> nn.Module:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    return model_type().to(device)


def train_checkpoints(
    model_type: type[nn.Module],
    task: Task,
    seed: int,
    device: torch.device,
    contract: dict[str, Any],
    x_all: torch.Tensor,
    y_all: torch.Tensor,
) -> tuple[nn.Module, dict[int, dict[str, torch.Tensor]], float]:
    budget = contract["common_training_budget"]
    model = initialize_model(model_type, seed, device)
    parameters = list(model.parameters())
    first = [torch.zeros_like(parameter) for parameter in parameters]
    second = [torch.zeros_like(parameter) for parameter in parameters]
    fit_idx = np.flatnonzero(task.fit)
    generator = torch.Generator(device="cpu")
    generator.manual_seed(seed)
    checkpoints: dict[int, dict[str, torch.Tensor]] = {}
    checkpoint_epochs = {int(value) for value in budget["checkpoint_epochs"]}
    batch_size = int(budget["batch_size"])
    beta1 = float(budget["beta1"])
    beta2 = float(budget["beta2"])
    epsilon = float(budget["epsilon"])
    learning_rate = float(budget["learning_rate"])
    adam_step = 0
    sync(device)
    started = time.perf_counter()
    for epoch in range(1, int(budget["epochs"]) + 1):
        model.train()
        order = torch.randperm(len(fit_idx), generator=generator).numpy()
        for offset in range(0, len(order), batch_size):
            index = torch.as_tensor(fit_idx[order[offset : offset + batch_size]], dtype=torch.long, device=device)
            for parameter in parameters:
                parameter.grad = None
            prediction, _ = model(x_all[index])
            loss = torch.mean((prediction - y_all[index]) ** 2)
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite training loss")
            loss.backward()
            adam_step += 1
            with torch.no_grad():
                for parameter, moment1, moment2 in zip(parameters, first, second):
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
    sync(device)
    runtime = time.perf_counter() - started
    if set(checkpoints) != checkpoint_epochs:
        raise RuntimeError("not all frozen checkpoints were captured")
    return model, checkpoints, runtime


def infer(
    model: nn.Module,
    state: dict[str, torch.Tensor] | None,
    x_all: torch.Tensor,
    device: torch.device,
    indices: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    if state is not None:
        model.load_state_dict(state)
    model.eval()
    if indices is None:
        indices = np.arange(len(x_all), dtype=np.int64)
    predictions: list[np.ndarray] = []
    representations: list[np.ndarray] = []
    with torch.no_grad():
        for offset in range(0, len(indices), 1024):
            index = torch.as_tensor(indices[offset : offset + 1024], dtype=torch.long, device=device)
            prediction, representation = model(x_all[index])
            predictions.append(prediction.detach().cpu().numpy())
            representations.append(representation.detach().cpu().numpy())
    return np.concatenate(predictions).astype(np.float64), np.concatenate(representations).astype(np.float32)


def select_checkpoint(
    model: nn.Module,
    checkpoints: dict[int, dict[str, torch.Tensor]],
    task: Task,
    targets: np.ndarray,
    objective: str,
    contract: dict[str, Any],
    x_all: torch.Tensor,
    device: torch.device,
) -> tuple[int, float]:
    selection_idx = np.flatnonzero(task.selection)
    best_epoch = int(contract["common_training_budget"]["checkpoint_epochs"][0])
    best_loss = math.inf
    for value in contract["common_training_budget"]["checkpoint_epochs"]:
        epoch = int(value)
        selected, _ = infer(model, checkpoints[epoch], x_all, device, selection_idx)
        predictions = np.full(len(task.y), np.nan, dtype=np.float64)
        predictions[selection_idx] = selected
        value_loss = selection_loss(task, predictions, targets, objective, contract)
        if value_loss < best_loss - 1e-15:
            best_epoch, best_loss = epoch, value_loss
    return best_epoch, best_loss


def ridge_predictions(task: Task, targets: np.ndarray, objective: str, contract: dict[str, Any]) -> tuple[np.ndarray, float, float]:
    x = task.windows.reshape(len(task.windows), -1).astype(np.float64)
    fit_x = x[task.fit]
    fit_y = task.y[task.fit]
    xtx = fit_x.T @ fit_x
    xty = fit_x.T @ fit_y
    identity = np.eye(xtx.shape[0], dtype=np.float64)
    best_predictions: np.ndarray | None = None
    best_penalty = float(contract["baselines_and_controls"]["Ridge"]["penalties_order"][0])
    best_loss = math.inf
    for value in contract["baselines_and_controls"]["Ridge"]["penalties_order"]:
        penalty = float(value)
        coefficients = np.linalg.solve(xtx + penalty * identity, xty)
        predictions = x @ coefficients
        value_loss = selection_loss(task, predictions, targets, objective, contract)
        if value_loss < best_loss - 1e-15:
            best_predictions, best_penalty, best_loss = predictions, penalty, value_loss
    if best_predictions is None:
        raise RuntimeError("Ridge selection produced no candidate")
    return best_predictions, best_penalty, best_loss


def retrieval_predictions(
    task: Task, space: np.ndarray, device: torch.device, k_values: list[int]
) -> tuple[dict[int, np.ndarray], float]:
    fit_idx = np.flatnonzero(task.fit)
    query_idx = np.flatnonzero(task.selection | task.calibration | task.test)
    bank = torch.as_tensor(space[fit_idx], dtype=torch.float32, device=device)
    query_space = torch.as_tensor(space[query_idx], dtype=torch.float32, device=device)
    bank_y = torch.as_tensor(task.y[fit_idx], dtype=torch.float32, device=device)
    outputs = {k: np.full(len(task.y), np.nan, dtype=np.float64) for k in k_values}
    sync(device)
    started = time.perf_counter()
    with torch.no_grad():
        for offset in range(0, len(query_idx), 512):
            query = query_space[offset : offset + 512]
            distances = torch.cdist(query, bank, p=2.0)
            ordered_values = torch.topk(distances, k=max(k_values), largest=False, sorted=True).values
            for k in k_values:
                boundary = ordered_values[:, k - 1 : k]
                closer = distances < boundary
                tied = distances == boundary
                needed = k - closer.sum(dim=1, keepdim=True)
                tied_rank = torch.cumsum(tied.to(torch.int32), dim=1)
                chosen = closer | (tied & (tied_rank <= needed))
                counts = chosen.sum(dim=1)
                if not bool(torch.all(counts == k)):
                    raise RuntimeError(f"deterministic neighbor selection did not select k={k}")
                values = (chosen.to(bank_y.dtype) * bank_y.unsqueeze(0)).sum(dim=1) / float(k)
                outputs[k][query_idx[offset : offset + len(query)]] = values.detach().cpu().numpy()
    sync(device)
    runtime = time.perf_counter() - started
    for k, output in outputs.items():
        if not np.isfinite(output[query_idx]).all():
            raise FloatingPointError(f"nonfinite retrieval output k={k}")
    return outputs, runtime


def row_template(
    cap: float,
    task: Task,
    objective: str,
    condition_id: str,
    role: str,
    seed_index: int | str,
    seed: int | str,
    *,
    architecture: str = "",
    retrieval_space: str = "",
    k_neighbors: int | str = "",
    alpha_head: float | str = "",
    checkpoint_epoch: int | str = "",
    ridge_lambda: float | str = "",
    parameter_count: int = 0,
    rank_eligible: bool = True,
) -> dict[str, Any]:
    return {
        "run_namespace": RUN_NAMESPACE,
        "cap": f"{cap:.2f}",
        "horizon_hours": task.horizon,
        "selection_objective": objective,
        "condition_id": condition_id,
        "method_role": role,
        "architecture": architecture,
        "retrieval_space": retrieval_space,
        "k_neighbors": k_neighbors,
        "alpha_head": alpha_head,
        "checkpoint_epoch": checkpoint_epoch,
        "ridge_lambda": ridge_lambda,
        "seed_index": seed_index,
        "seed": seed,
        "execution_status": "",
        "scientific_support_status": "",
        "failure_code": "",
        "sanitized_exception_class": "",
        "parameter_count": parameter_count,
        "rank_eligible": rank_eligible,
        "training_runtime_s": "",
        "condition_runtime_s": "",
        "selection_loss": "",
        "detection_threshold": "",
        "threshold_status": "",
        "onset_targeted_claim_valid": "",
        **{name: "" for name in METRIC_FIELDS},
        "n_fit": int(task.fit.sum()),
        "n_selection": int(task.selection.sum()),
        "n_calibration": int(task.calibration.sum()),
        "n_test": int(task.test.sum()),
        "n_onsets_selection": "",
        "n_onsets_calibration": "",
        "n_onsets_test": "",
        "n_events_test": "",
    }


def complete_row(
    base: dict[str, Any],
    task: Task,
    predictions: np.ndarray,
    targets: np.ndarray,
    contract: dict[str, Any],
    *,
    training_runtime: float = 0.0,
    condition_runtime: float = 0.0,
    selected_loss: float | None = None,
) -> tuple[dict[str, Any], np.ndarray]:
    started = time.perf_counter()
    metrics, test_predictions = evaluate(task, predictions, targets, contract)
    elapsed = condition_runtime + (time.perf_counter() - started)
    row = dict(base)
    row["execution_status"] = "completed"
    row["training_runtime_s"] = format_float(training_runtime, 9)
    row["condition_runtime_s"] = format_float(elapsed, 9)
    row["selection_loss"] = format_float(selected_loss, 12)
    for name, value in metrics.items():
        if name in METRIC_FIELDS or name == "detection_threshold":
            row[name] = format_float(value, 12)
        elif isinstance(value, bool):
            row[name] = str(value).lower()
        else:
            row[name] = value
    return row, test_predictions


def failed_row(base: dict[str, Any], exc: BaseException) -> dict[str, Any]:
    status, code, exception_class = sanitized_exception(exc)
    row = dict(base)
    row["execution_status"] = status
    row["scientific_support_status"] = "not_evaluable_execution_failure"
    row["failure_code"] = code
    row["sanitized_exception_class"] = exception_class
    return row


def exact_sign_flip(differences: np.ndarray) -> float:
    observed = abs(float(np.mean(differences)))
    count = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(differences)):
        statistic = abs(float(np.mean(differences * np.asarray(signs, dtype=np.float64))))
        count += statistic >= observed - 1e-15
    return count / (2 ** len(differences))


def holm_adjust(pvalues: list[float]) -> list[float]:
    order = sorted(range(len(pvalues)), key=lambda index: (pvalues[index], index))
    adjusted = [math.nan] * len(pvalues)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(pvalues) - rank) * pvalues[index]))
        adjusted[index] = running
    return adjusted


def paired_effects(rows: list[dict[str, Any]], contract: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    primary = [row for row in rows if row["cap"] == "0.70"]
    for family in contract["statistics"]["families"]:
        objective = family["selection_objective"]
        metric = family["metric"]
        better = family["better_direction"]
        for horizon in contract["experimental_grid"]["horizons_hours"]:
            family_rows: list[dict[str, Any]] = []
            pvalues: list[float] = []
            family_complete = True
            for contrast in family["contrasts"]:
                record: dict[str, Any] = {
                    "run_namespace": RUN_NAMESPACE,
                    "family_id": family["family_id"],
                    "horizon_hours": horizon,
                    "selection_objective": objective,
                    "contrast_id": contrast["id"],
                    "treatment_condition_id": contrast["treatment"],
                    "control_condition_id": contrast["control"],
                    "metric": metric,
                    "better_direction": better,
                    "execution_status": "",
                    "n_pairs": 0,
                    "mean_treatment_minus_control": "",
                    "median_treatment_minus_control": "",
                    "sample_sd": "",
                    "dz": "",
                    "zero_variance": "",
                    "treatment_wins": "",
                    "ties": "",
                    "control_wins": "",
                    "p_exact_sign_flip": "",
                    "p_holm_within_family_horizon": "",
                    "holm_significant_005": "",
                    "seed_interval_low": "",
                    "seed_interval_high": "",
                    "mean_direction": "",
                }
                treatment = {
                    int(row["seed_index"]): float(row[metric])
                    for row in primary
                    if int(row["horizon_hours"]) == int(horizon)
                    and row["selection_objective"] == objective
                    and row["condition_id"] == contrast["treatment"]
                    and row["execution_status"] == "completed"
                }
                control = {
                    int(row["seed_index"]): float(row[metric])
                    for row in primary
                    if int(row["horizon_hours"]) == int(horizon)
                    and row["selection_objective"] == objective
                    and row["condition_id"] == contrast["control"]
                    and row["execution_status"] == "completed"
                }
                common = sorted(set(treatment) & set(control))
                record["n_pairs"] = len(common)
                if len(common) != int(contract["statistics"]["complete_pairs_required"]):
                    record["execution_status"] = "incomplete_missing_pairs"
                    family_complete = False
                    family_rows.append(record)
                    continue
                differences = np.asarray([treatment[index] - control[index] for index in common], dtype=np.float64)
                mean_difference = float(np.mean(differences))
                median_difference = float(np.median(differences))
                sample_sd = float(np.std(differences, ddof=1))
                zero_variance = sample_sd == 0.0
                pvalue = exact_sign_flip(differences)
                critical = float(contract["statistics"]["seed_conditional_interval"]["critical_value"])
                margin = 0.0 if zero_variance else critical * sample_sd / math.sqrt(len(differences))
                ties = np.abs(differences) <= 1e-15
                favorable = differences < -1e-15 if better == "lower" else differences > 1e-15
                adverse = (~ties) & (~favorable)
                if abs(mean_difference) <= 1e-15:
                    direction = "null"
                elif (mean_difference < 0 and better == "lower") or (mean_difference > 0 and better == "higher"):
                    direction = "favorable"
                else:
                    direction = "adverse"
                record.update(
                    {
                        "execution_status": "completed",
                        "mean_treatment_minus_control": format_float(mean_difference),
                        "median_treatment_minus_control": format_float(median_difference),
                        "sample_sd": format_float(sample_sd),
                        "dz": "" if zero_variance else format_float(mean_difference / sample_sd),
                        "zero_variance": str(zero_variance).lower(),
                        "treatment_wins": int(favorable.sum()),
                        "ties": int(ties.sum()),
                        "control_wins": int(adverse.sum()),
                        "p_exact_sign_flip": format_float(pvalue),
                        "seed_interval_low": format_float(mean_difference - margin),
                        "seed_interval_high": format_float(mean_difference + margin),
                        "mean_direction": direction,
                    }
                )
                family_rows.append(record)
                pvalues.append(pvalue)
            if family_complete and len(pvalues) == len(family_rows):
                for record, adjusted in zip(family_rows, holm_adjust(pvalues)):
                    record["p_holm_within_family_horizon"] = format_float(adjusted)
                    record["holm_significant_005"] = str(adjusted < 0.05).lower()
            output.extend(family_rows)
    return output


def aggregate_conditions(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = (
        "cap",
        "horizon_hours",
        "selection_objective",
        "condition_id",
        "method_role",
        "architecture",
        "retrieval_space",
        "k_neighbors",
        "rank_eligible",
    )
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row[field] for field in fields)].append(row)
    output: list[dict[str, Any]] = []
    for key, items in groups.items():
        completed = [row for row in items if row["execution_status"] == "completed"]
        record = dict(zip(fields, key))
        record.update(
            {
                "run_namespace": RUN_NAMESPACE,
                "n_expected_rows": len(items),
                "n_completed_rows": len(completed),
                "aggregation_status": "complete" if len(completed) == len(items) else "incomplete",
                "primary_cap": str(key[0]) == "0.70",
                "primary_k": key[7] in {"", 8, "8"},
                "scope": "primary" if str(key[0]) == "0.70" and key[7] in {"", 8, "8"} else "descriptive_sensitivity",
            }
        )
        for metric in METRIC_FIELDS:
            values = [float(row[metric]) for row in completed if row[metric] != ""]
            record[f"mean_{metric}"] = format_float(float(np.mean(values))) if values else ""
            record[f"sample_sd_{metric}"] = format_float(float(np.std(values, ddof=1))) if len(values) > 1 else ("0" if values else "")
        output.append(record)
    output.sort(key=lambda row: (float(row["cap"]), int(row["horizon_hours"]), row["selection_objective"], row["condition_id"]))
    return output


def moving_block_table(
    prediction_cache: dict[tuple[int, int, str], np.ndarray], contract: dict[str, Any]
) -> list[dict[str, Any]]:
    block = contract["supplementary_moving_block_analysis"]
    primary_family = {item["id"]: item for family in contract["statistics"]["families"] for item in family["contrasts"]}
    output: list[dict[str, Any]] = []
    for horizon in contract["experimental_grid"]["horizons_hours"]:
        expected_n = int(block["test_series_lengths"][str(horizon)])
        for contrast_id in block["scope"]["contrasts"]:
            contrast = primary_family[contrast_id]
            missing = [
                (seed_index, condition)
                for seed_index in range(10)
                for condition in (contrast["treatment"], contrast["control"])
                if (int(horizon), seed_index, condition) not in prediction_cache
            ]
            if missing:
                series = None
            else:
                per_seed = []
                for seed_index in range(10):
                    treatment = prediction_cache[(int(horizon), seed_index, contrast["treatment"])]
                    control = prediction_cache[(int(horizon), seed_index, contrast["control"])]
                    if len(treatment) != expected_n or len(control) != expected_n:
                        series = None
                        break
                    target_key = (int(horizon), -1, "target")
                    target = prediction_cache[target_key]
                    per_seed.append(np.abs(target - treatment) - np.abs(target - control))
                else:
                    series = np.mean(np.stack(per_seed), axis=0)
            for length in block["bootstrap"]["block_lengths"]:
                record = {
                    "run_namespace": RUN_NAMESPACE,
                    "cap": "0.70",
                    "horizon_hours": horizon,
                    "selection_objective": "mae",
                    "contrast_id": contrast_id,
                    "block_length": length,
                    "repetitions": int(block["bootstrap"]["repetitions"]),
                    "rng": block["bootstrap"]["rng"],
                    "rng_seed": int(block["bootstrap"]["rng_seeds"][f"h{horizon}_block{length}"]),
                    "n_test_targets": expected_n,
                    "execution_status": "",
                    "unresampled_mean": "",
                    "percentile_2_5": "",
                    "percentile_97_5": "",
                    "interval_label": "descriptive moving-block sensitivity on one observed sequence",
                }
                if series is None or len(series) != expected_n or not np.isfinite(series).all():
                    record["execution_status"] = "incomplete_missing_predictions"
                    output.append(record)
                    continue
                n = len(series)
                blocks_per_sample = math.ceil(n / int(length))
                rng = np.random.Generator(np.random.PCG64(record["rng_seed"]))
                bootstrap_means = np.empty(record["repetitions"], dtype=np.float64)
                offsets = np.arange(int(length), dtype=np.int64)
                for start in range(0, record["repetitions"], 250):
                    count = min(250, record["repetitions"] - start)
                    starts = rng.integers(0, n - int(length) + 1, size=(count, blocks_per_sample))
                    indices = (starts[:, :, None] + offsets[None, None, :]).reshape(count, -1)[:, :n]
                    bootstrap_means[start : start + count] = series[indices].mean(axis=1)
                low, high = np.quantile(bootstrap_means, [0.025, 0.975], method="linear")
                record.update(
                    {
                        "execution_status": "completed",
                        "unresampled_mean": format_float(float(series.mean())),
                        "percentile_2_5": format_float(float(low)),
                        "percentile_97_5": format_float(float(high)),
                    }
                )
                output.append(record)
    return output


def expected_keys(contract: dict[str, Any]) -> set[tuple[str, str, int, str, str, str]]:
    keys: set[tuple[str, str, int, str, str, str]] = set()
    catalog = [item["id"] for item in contract["seeded_condition_catalog"]]
    for cap in contract["experimental_grid"]["caps"]:
        cap_text = f"{float(cap):.2f}"
        for horizon in contract["experimental_grid"]["horizons_hours"]:
            for condition in contract["row_contract"]["objective_free_deterministic_ids"]:
                keys.add((RUN_NAMESPACE, cap_text, int(horizon), "not_applicable", condition, "deterministic"))
            for objective in contract["experimental_grid"]["selection_objectives"]:
                keys.add((RUN_NAMESPACE, cap_text, int(horizon), objective, "Ridge", "deterministic"))
                for seed_index in range(len(contract["experimental_grid"]["common_seeds"])):
                    for condition in catalog:
                        keys.add((RUN_NAMESPACE, cap_text, int(horizon), objective, condition, str(seed_index)))
    return keys


def row_key(row: dict[str, Any]) -> tuple[str, str, int, str, str, str]:
    return (
        str(row["run_namespace"]),
        str(row["cap"]),
        int(row["horizon_hours"]),
        str(row["selection_objective"]),
        str(row["condition_id"]),
        str(row["seed_index"]),
    )


def completeness_ledger(rows: list[dict[str, Any]], contract: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    expected = expected_keys(contract)
    observed_counts = Counter(row_key(row) for row in rows)
    row_index = {row_key(row): row for row in rows}
    ledger: list[dict[str, Any]] = []
    for key in sorted(expected, key=lambda item: (float(item[1]), item[2], item[3], item[4], item[5])):
        observed_count = observed_counts.get(key, 0)
        row = row_index.get(key)
        status = row["execution_status"] if row else "missing"
        comparable = observed_count == 1 and status == "completed" and row["condition_id"] != "DirectPolicyTransform-Privileged"
        ledger.append(
            {
                "run_namespace": key[0],
                "cap": key[1],
                "horizon_hours": key[2],
                "selection_objective": key[3],
                "condition_id": key[4],
                "seed_index": key[5],
                "expected_count": 1,
                "observed_count": observed_count,
                "execution_status": status,
                "scientific_support_status": "" if row is None else row["scientific_support_status"],
                "comparable_forecast_row": str(comparable).lower(),
                "ledger_status": "complete" if observed_count == 1 and status == "completed" else "incomplete",
            }
        )
    unexpected = set(observed_counts) - expected
    duplicates = [key for key, count in observed_counts.items() if count != 1]
    completed = sum(row["execution_status"] == "completed" for row in rows)
    summary = {
        "expected_rows": len(expected),
        "observed_rows": len(rows),
        "unique_observed_keys": len(observed_counts),
        "completed_rows": completed,
        "failed_rows": len(rows) - completed,
        "missing_keys": len(expected - set(observed_counts)),
        "unexpected_keys": len(unexpected),
        "duplicate_keys": len(duplicates),
    }
    return ledger, summary


def selections_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed = [row for row in rows if row["execution_status"] == "completed"]
    return {
        "checkpoint_epoch_counts": dict(sorted(Counter(str(row["checkpoint_epoch"]) for row in completed if row["checkpoint_epoch"] != "").items())),
        "selected_alpha_counts": dict(
            sorted(
                Counter(str(row["alpha_head"]) for row in completed if row["condition_id"] == "gru_learned_k8_selected_blend").items()
            )
        ),
        "ridge_lambda_counts": dict(sorted(Counter(str(row["ridge_lambda"]) for row in completed if row["condition_id"] == "Ridge").items())),
    }


def execute(args: argparse.Namespace) -> int:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if contract.get("run_namespace") != RUN_NAMESPACE:
        raise ValueError("contract namespace does not match runner namespace")
    features, source_profile = load_features(args.rts_data.resolve(), contract)
    counts = model_parameter_counts()
    expected_counts = {"GRU": 8257, "LSTM": 10993, "DLinear": 106, "TCN": 28273, "randomized_GRU_encoder": 8208}
    if counts != expected_counts:
        raise ValueError(f"architecture parameter-count mismatch: {counts}")
    for cap in contract["experimental_grid"]["caps"]:
        targets = build_targets(features, float(cap))
        for horizon in contract["experimental_grid"]["horizons_hours"]:
            build_task(features, targets, int(horizon), contract)
    if args.dry_run:
        print(
            f"OK dry-run: sources and temporal cells valid; expected_rows={contract['row_contract']['total_rows']}; "
            f"trajectories={contract['common_training_budget']['training_trajectories']}; parameters={counts}"
        )
        return 0

    manifest_path = HERE / "run_manifest.json"
    if manifest_path.exists():
        raise SystemExit("immutable namespace already contains run_manifest.json; refusing to overwrite")
    RESULT_DIR.mkdir(parents=True, exist_ok=False)
    LOG_DIR.mkdir(parents=True, exist_ok=False)
    log = RunLog(LOG_DIR / "run.log")
    device = torch.device("cuda" if args.device == "auto" and torch.cuda.is_available() else ("cpu" if args.device == "auto" else args.device))
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    torch.set_num_threads(int(args.cpu_threads))
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    total_started = time.perf_counter()
    manifest: dict[str, Any] = {
        "schema": "p1_ieee_access_upgrade_execution_manifest",
        "schema_version": 1,
        "run_namespace": RUN_NAMESPACE,
        "status": "running",
        "started_at": utc_now(),
        "command": [sys.executable, str(Path(__file__).resolve()), "--rts-data", str(args.rts_data.resolve()), "--device", args.device],
        "approved_stage": "p1v4_s2_fair_baselines_attribution",
        "contract": {"path": str(CONTRACT_PATH.relative_to(PROJECT_ROOT)), "sha256": sha256(CONTRACT_PATH)},
        "script": {"path": str(Path(__file__).resolve().relative_to(PROJECT_ROOT)), "sha256": sha256(Path(__file__))},
        "source_profile": source_profile,
        "parameter_counts": counts,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "torch": torch.__version__,
            "device": str(device),
            "cuda_version": torch.version.cuda,
            "cuda_device": torch.cuda.get_device_name(0) if device.type == "cuda" else "not_applicable",
            "cudnn_deterministic": True,
            "cudnn_benchmark": False,
            "global_deterministic_algorithms_enforced": False,
            "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
            "cpu_threads": int(args.cpu_threads),
        },
        "fixed_budgets": contract["common_training_budget"],
        "outputs": {},
    }
    write_json_atomic(manifest_path, manifest)
    log.emit(f"validated contract={manifest['contract']['sha256']} and four hashed RTS-GMLC sources")
    log.emit(f"device={device}; frozen trajectories=240; expected rows=2310")

    rows: list[dict[str, Any]] = []
    trajectories: list[dict[str, Any]] = []
    prediction_cache: dict[tuple[int, int, str], np.ndarray] = {}
    prediction_archive: dict[str, np.ndarray] = {}
    runtime_by_architecture: Counter[str] = Counter()
    retrieval_runtime: Counter[str] = Counter()
    seeds = [int(value) for value in contract["experimental_grid"]["common_seeds"]]
    k_values = [int(value) for value in contract["retrieval"]["k_values"]]
    objectives = list(contract["experimental_grid"]["selection_objectives"])
    try:
        for cap_value in contract["experimental_grid"]["cap_execution_order"]:
            cap = float(cap_value)
            targets = build_targets(features, cap)
            log.emit(f"cap={cap:.2f}; nonzero_target_share={float(np.mean(targets > 0)):.8f}")
            for horizon_value in contract["experimental_grid"]["horizons_hours"]:
                horizon = int(horizon_value)
                task = build_task(features, targets, horizon, contract)
                x_all = torch.as_tensor(task.windows, dtype=torch.float32, device=device)
                y_all = torch.as_tensor(task.y, dtype=torch.float32, device=device)
                log.emit(
                    f"cap={cap:.2f} h={horizon}; fit={task.fit.sum()} selection={task.selection.sum()} "
                    f"calibration={task.calibration.sum()} test={task.test.sum()}"
                )

                deterministic_specs = (
                    ("DirectPolicyTransform-Privileged", "privileged_audit", task.y.copy(), False),
                    ("Persistence", "naive_baseline", targets[task.target_t - horizon], True),
                    ("Seasonal-24h", "naive_baseline", targets[task.target_t - 24], True),
                )
                for condition, role, predictions, rank_eligible in deterministic_specs:
                    base = row_template(
                        cap, task, "not_applicable", condition, role, "deterministic", "deterministic", rank_eligible=rank_eligible
                    )
                    try:
                        row, _ = complete_row(base, task, predictions, targets, contract)
                    except Exception as exc:
                        row = failed_row(base, exc)
                    rows.append(row)

                for objective in objectives:
                    base = row_template(
                        cap,
                        task,
                        objective,
                        "Ridge",
                        "trained_baseline",
                        "deterministic",
                        "deterministic",
                        architecture="linear",
                        parameter_count=336,
                    )
                    try:
                        started = time.perf_counter()
                        predictions, penalty, loss = ridge_predictions(task, targets, objective, contract)
                        base["ridge_lambda"] = format_float(penalty)
                        row, _ = complete_row(
                            base, task, predictions, targets, contract, condition_runtime=time.perf_counter() - started, selected_loss=loss
                        )
                    except Exception as exc:
                        row = failed_row(base, exc)
                    rows.append(row)

                raw_error: BaseException | None = None
                raw_by_k: dict[int, np.ndarray] = {}
                raw_runtime = 0.0
                try:
                    raw_by_k, raw_runtime = retrieval_predictions(task, task.windows.reshape(len(task.windows), -1), device, k_values)
                    retrieval_runtime["raw"] += raw_runtime
                except Exception as exc:
                    raw_error = exc

                for seed_index, seed in enumerate(seeds):
                    random_error: BaseException | None = None
                    randomized_by_k: dict[int, np.ndarray] = {}
                    random_runtime = 0.0
                    try:
                        random_model = initialize_model(GRURegressor, seed, device)
                        _, random_space = infer(random_model, None, x_all, device)
                        randomized_by_k, random_runtime = retrieval_predictions(task, random_space, device, k_values)
                        retrieval_runtime["randomized"] += random_runtime
                    except Exception as exc:
                        random_error = exc

                    architecture_artifacts: dict[str, Any] = {}
                    for architecture, model_type in ARCHITECTURES.items():
                        trajectory = {
                            "run_namespace": RUN_NAMESPACE,
                            "cap": f"{cap:.2f}",
                            "horizon_hours": horizon,
                            "architecture": architecture,
                            "seed_index": seed_index,
                            "seed": seed,
                            "parameter_count": counts[architecture],
                            "epochs": 20,
                            "batch_size": 256,
                            "checkpoint_epochs": "5|10|15|20",
                            "execution_status": "",
                            "failure_code": "",
                            "sanitized_exception_class": "",
                            "training_runtime_s": "",
                        }
                        try:
                            model, checkpoints, runtime = train_checkpoints(
                                model_type, task, seed, device, contract, x_all, y_all
                            )
                            trajectory["execution_status"] = "completed"
                            trajectory["training_runtime_s"] = format_float(runtime, 9)
                            runtime_by_architecture[architecture] += runtime
                            architecture_artifacts[architecture] = (model, checkpoints, runtime)
                        except Exception as exc:
                            status, code, exception_class = sanitized_exception(exc)
                            trajectory.update(
                                {
                                    "execution_status": status,
                                    "failure_code": code,
                                    "sanitized_exception_class": exception_class,
                                }
                            )
                            architecture_artifacts[architecture] = exc
                        trajectories.append(trajectory)

                    objective_heads: dict[tuple[str, str], tuple[np.ndarray, np.ndarray, int, float, float] | BaseException] = {}
                    for objective in objectives:
                        for architecture in ARCHITECTURES:
                            artifact = architecture_artifacts[architecture]
                            condition = f"{architecture.lower()}_head"
                            base = row_template(
                                cap,
                                task,
                                objective,
                                condition,
                                "architecture_head",
                                seed_index,
                                seed,
                                architecture=architecture,
                                parameter_count=counts[architecture],
                            )
                            if isinstance(artifact, BaseException):
                                row = failed_row(base, artifact)
                                objective_heads[(architecture, objective)] = artifact
                            else:
                                model, checkpoints, training_runtime = artifact
                                try:
                                    epoch, selected_loss = select_checkpoint(
                                        model, checkpoints, task, targets, objective, contract, x_all, device
                                    )
                                    started = time.perf_counter()
                                    predictions, representation = infer(model, checkpoints[epoch], x_all, device)
                                    inference_runtime = time.perf_counter() - started
                                    base["checkpoint_epoch"] = epoch
                                    row, test_predictions = complete_row(
                                        base,
                                        task,
                                        predictions,
                                        targets,
                                        contract,
                                        training_runtime=training_runtime,
                                        condition_runtime=inference_runtime,
                                        selected_loss=selected_loss,
                                    )
                                    objective_heads[(architecture, objective)] = (
                                        predictions,
                                        representation,
                                        epoch,
                                        selected_loss,
                                        training_runtime,
                                    )
                                    if cap == 0.70 and objective == "mae":
                                        prediction_cache[(horizon, seed_index, condition)] = test_predictions
                                except Exception as exc:
                                    row = failed_row(base, exc)
                                    objective_heads[(architecture, objective)] = exc
                            rows.append(row)

                        for space_name, by_k, space_error, space_runtime, prefix, role, parameter_count in (
                            ("raw", raw_by_k, raw_error, raw_runtime, "raw", "attribution_control", 0),
                            (
                                "randomized",
                                randomized_by_k,
                                random_error,
                                random_runtime,
                                "gru_randomized",
                                "attribution_control",
                                counts["randomized_GRU_encoder"],
                            ),
                        ):
                            for k in k_values:
                                condition = f"{prefix}_k{k}_retrieval"
                                base = row_template(
                                    cap,
                                    task,
                                    objective,
                                    condition,
                                    role,
                                    seed_index,
                                    seed,
                                    architecture="GRU-untrained" if space_name == "randomized" else "none",
                                    retrieval_space=space_name,
                                    k_neighbors=k,
                                    alpha_head=0.0,
                                    parameter_count=parameter_count,
                                )
                                if space_error is not None:
                                    row = failed_row(base, space_error)
                                else:
                                    try:
                                        row, test_predictions = complete_row(
                                            base,
                                            task,
                                            by_k[k],
                                            targets,
                                            contract,
                                            condition_runtime=space_runtime,
                                        )
                                        if cap == 0.70 and objective == "mae" and k == 8:
                                            prediction_cache[(horizon, seed_index, condition)] = test_predictions
                                    except Exception as exc:
                                        row = failed_row(base, exc)
                                rows.append(row)

                        gru_artifact = objective_heads[("GRU", objective)]
                        learned_by_k: dict[int, np.ndarray] = {}
                        learned_error: BaseException | None = gru_artifact if isinstance(gru_artifact, BaseException) else None
                        learned_runtime = 0.0
                        if learned_error is None:
                            try:
                                head_predictions, learned_space, epoch, head_loss, training_runtime = gru_artifact
                                learned_by_k, learned_runtime = retrieval_predictions(task, learned_space, device, k_values)
                                retrieval_runtime["learned"] += learned_runtime
                            except Exception as exc:
                                learned_error = exc
                        for k in k_values:
                            condition = f"gru_learned_k{k}_retrieval"
                            base = row_template(
                                cap,
                                task,
                                objective,
                                condition,
                                "retrieval_only",
                                seed_index,
                                seed,
                                architecture="GRU",
                                retrieval_space="learned",
                                k_neighbors=k,
                                alpha_head=0.0,
                                checkpoint_epoch="" if isinstance(gru_artifact, BaseException) else gru_artifact[2],
                                parameter_count=counts["GRU"],
                            )
                            if learned_error is not None:
                                row = failed_row(base, learned_error)
                            else:
                                try:
                                    row, test_predictions = complete_row(
                                        base,
                                        task,
                                        learned_by_k[k],
                                        targets,
                                        contract,
                                        training_runtime=gru_artifact[4],
                                        condition_runtime=learned_runtime,
                                    )
                                    if cap == 0.70 and objective == "mae" and k == 8:
                                        prediction_cache[(horizon, seed_index, condition)] = test_predictions
                                except Exception as exc:
                                    row = failed_row(base, exc)
                            rows.append(row)

                        blend_specs: list[tuple[str, float | None, str]] = [
                            ("gru_learned_k8_selected_blend", None, "selected_blend"),
                            ("gru_learned_k8_fixed_0_5", 0.5, "mechanism_control"),
                            ("gru_learned_k8_fixed_1", 1.0, "mechanism_control"),
                        ]
                        selected_alpha = None
                        selected_blend_loss = None
                        if learned_error is None:
                            try:
                                head_predictions = gru_artifact[0]
                                retrieved = learned_by_k[8]
                                best_loss = math.inf
                                for alpha_value in contract["selection_and_scoring"]["blend_alpha_grid_order"]:
                                    alpha = float(alpha_value)
                                    blended = alpha * head_predictions + (1.0 - alpha) * retrieved
                                    value_loss = selection_loss(task, blended, targets, objective, contract)
                                    if value_loss < best_loss - 1e-15:
                                        selected_alpha, selected_blend_loss = alpha, value_loss
                                        best_loss = value_loss
                            except Exception as exc:
                                learned_error = exc
                        for condition, fixed_alpha, role in blend_specs:
                            alpha = selected_alpha if fixed_alpha is None else fixed_alpha
                            base = row_template(
                                cap,
                                task,
                                objective,
                                condition,
                                role,
                                seed_index,
                                seed,
                                architecture="GRU",
                                retrieval_space="learned",
                                k_neighbors=8,
                                alpha_head="" if alpha is None else alpha,
                                checkpoint_epoch="" if isinstance(gru_artifact, BaseException) else gru_artifact[2],
                                parameter_count=counts["GRU"],
                            )
                            if learned_error is not None or alpha is None:
                                row = failed_row(base, learned_error or RuntimeError("blend alpha unavailable"))
                            else:
                                try:
                                    blended = alpha * gru_artifact[0] + (1.0 - alpha) * learned_by_k[8]
                                    loss = selected_blend_loss if fixed_alpha is None else selection_loss(
                                        task, blended, targets, objective, contract
                                    )
                                    row, test_predictions = complete_row(
                                        base,
                                        task,
                                        blended,
                                        targets,
                                        contract,
                                        training_runtime=gru_artifact[4],
                                        condition_runtime=learned_runtime,
                                        selected_loss=loss,
                                    )
                                    if cap == 0.70 and objective == "mae":
                                        prediction_cache[(horizon, seed_index, condition)] = test_predictions
                                except Exception as exc:
                                    row = failed_row(base, exc)
                            rows.append(row)

                    if cap == 0.70:
                        prediction_cache[(horizon, -1, "target")] = task.y[task.test].copy()
                    write_csv_atomic(RESULT_DIR / "run_results.partial.csv", rows)
                    write_csv_atomic(RESULT_DIR / "trajectory_ledger.partial.csv", trajectories)
                    log.emit(f"cap={cap:.2f} h={horizon} seed_index={seed_index} seed={seed}; four trajectories recorded")
                del x_all, y_all
                if device.type == "cuda":
                    torch.cuda.empty_cache()

        ledger, completeness = completeness_ledger(rows, contract)
        paired = paired_effects(rows, contract)
        aggregate = aggregate_conditions(rows)
        moving = moving_block_table(prediction_cache, contract)
        for (horizon, seed_index, condition), values in prediction_cache.items():
            if seed_index >= 0:
                prediction_archive[f"h{horizon}_seed{seed_index}_{condition}"] = values
        for horizon in contract["experimental_grid"]["horizons_hours"]:
            prediction_archive[f"h{horizon}_target"] = prediction_cache[(int(horizon), -1, "target")]

        direct_rows = [row for row in rows if row["condition_id"] == "DirectPolicyTransform-Privileged"]
        seasonal_identity = []
        for cap in ("0.60", "0.70", "0.80"):
            p = next(row for row in rows if row["cap"] == cap and row["horizon_hours"] == 24 and row["condition_id"] == "Persistence")
            s = next(row for row in rows if row["cap"] == cap and row["horizon_hours"] == 24 and row["condition_id"] == "Seasonal-24h")
            seasonal_identity.append(abs(float(p["curtailment_mae"]) - float(s["curtailment_mae"])))
        checks = {
            "all_expected_rows_present_once": completeness["expected_rows"] == completeness["observed_rows"] == completeness["unique_observed_keys"] == 2310,
            "all_rows_completed": completeness["completed_rows"] == 2310,
            "all_240_trajectories_completed": len(trajectories) == 240 and all(row["execution_status"] == "completed" for row in trajectories),
            "all_30_paired_effect_cells_completed": len(paired) == 30 and all(row["execution_status"] == "completed" for row in paired),
            "all_36_moving_block_cells_completed": len(moving) == 36 and all(row["execution_status"] == "completed" for row in moving),
            "direct_privileged_zero_mae": len(direct_rows) == 6 and all(float(row["curtailment_mae"]) == 0.0 for row in direct_rows),
            "direct_privileged_excluded_from_rank": all(str(row["rank_eligible"]).lower() == "false" for row in direct_rows),
            "seasonal_24h_identity": max(seasonal_identity) == 0.0,
            "source_hashes_match_contract": all(
                source_profile["source_files"][name]["sha256"] == contract["scope"]["source_files"][name]["sha256"]
                for name in contract["scope"]["source_files"]
            ),
        }
        protocol_valid = all(checks.values())
        direction_counts = Counter(row["mean_direction"] for row in paired if row["execution_status"] == "completed")
        protocol = {
            "schema": "p1_ieee_access_upgrade_protocol_validity",
            "schema_version": 1,
            "run_namespace": RUN_NAMESPACE,
            "protocol_valid": protocol_valid,
            "effect_direction_is_not_validity_gate": True,
            "completeness": completeness,
            "checks": checks,
            "effect_direction_counts": dict(sorted(direction_counts.items())),
            "onset_targeted_claim_valid_rows": sum(row["onset_targeted_claim_valid"] == "true" for row in rows),
            "onset_diagnostic_only_rows": sum(row["scientific_support_status"] == "onset_diagnostic_only_no_pretest_support" for row in rows),
            "privileged_control_ranked_as_forecaster": False,
            "scope": {
                "proxy_not_observed_curtailment": True,
                "retrospective_lags_not_operational_forecasts": True,
                "single_truncated_sequence": True,
                "cross_cap_descriptive_only": True,
                "k_4_16_32_descriptive_only": True,
            },
        }

        write_csv_atomic(RESULT_DIR / "run_results.csv", rows)
        write_csv_atomic(RESULT_DIR / "trajectory_ledger.csv", trajectories)
        write_csv_atomic(RESULT_DIR / "paired_effects.csv", paired)
        write_csv_atomic(RESULT_DIR / "cap_k_sensitivity.csv", aggregate)
        write_csv_atomic(RESULT_DIR / "moving_block_supplement.csv", moving)
        write_csv_atomic(RESULT_DIR / "completeness_ledger.csv", ledger)
        failure_rows = [
            {
                "record_type": "failure" if row["execution_status"] != "completed" else "summary",
                "cap": row["cap"] if row["execution_status"] != "completed" else "",
                "horizon_hours": row["horizon_hours"] if row["execution_status"] != "completed" else "",
                "selection_objective": row["selection_objective"] if row["execution_status"] != "completed" else "",
                "condition_id": row["condition_id"] if row["execution_status"] != "completed" else "",
                "seed_index": row["seed_index"] if row["execution_status"] != "completed" else "",
                "execution_status": row["execution_status"] if row["execution_status"] != "completed" else "no_failures_recorded",
                "failure_code": row["failure_code"] if row["execution_status"] != "completed" else "",
                "sanitized_exception_class": row["sanitized_exception_class"] if row["execution_status"] != "completed" else "",
            }
            for row in rows
            if row["execution_status"] != "completed"
        ]
        if not failure_rows:
            failure_rows = [
                {
                    "record_type": "summary",
                    "cap": "",
                    "horizon_hours": "",
                    "selection_objective": "",
                    "condition_id": "",
                    "seed_index": "",
                    "execution_status": "no_failures_recorded",
                    "failure_code": "",
                    "sanitized_exception_class": "",
                }
            ]
        write_csv_atomic(RESULT_DIR / "failure_ledger.csv", failure_rows)
        write_json_atomic(RESULT_DIR / "protocol_validity.json", protocol)
        write_npz_atomic(RESULT_DIR / "test_predictions_primary_mae.npz", prediction_archive)

        for partial in (RESULT_DIR / "run_results.partial.csv", RESULT_DIR / "trajectory_ledger.partial.csv"):
            if partial.exists():
                partial.unlink()
        runtime_total = time.perf_counter() - total_started
        outputs: dict[str, Any] = {}
        for path in sorted(RESULT_DIR.iterdir()):
            if path.is_file():
                outputs[path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
        manifest.update(
            {
                "status": "completed" if protocol_valid else "failed_closed_incomplete_or_incomparable",
                "completed_at": utc_now(),
                "protocol_valid": protocol_valid,
                "row_counts": {
                    "run_results": len(rows),
                    "trajectory_ledger": len(trajectories),
                    "paired_effects": len(paired),
                    "cap_k_sensitivity": len(aggregate),
                    "moving_block_supplement": len(moving),
                    "completeness_ledger": len(ledger),
                },
                "runtimes_seconds": {
                    "total": runtime_total,
                    "unique_trajectory_sum": float(sum(float(row["training_runtime_s"]) for row in trajectories if row["training_runtime_s"])),
                    "by_architecture": {name: runtime_by_architecture[name] for name in ARCHITECTURES},
                    "retrieval_by_space": dict(retrieval_runtime),
                },
                "selections": selections_summary(rows),
                "completeness": completeness,
                "outputs": outputs,
            }
        )
        write_json_atomic(manifest_path, manifest)
        log.emit(
            f"execution sealed; status={manifest['status']} rows={len(rows)} trajectories={len(trajectories)} "
            f"runtime_s={runtime_total:.3f}"
        )
        return 0 if protocol_valid else 2
    except Exception as exc:
        manifest.update(
            {
                "status": "failed_preserved",
                "failed_at": utc_now(),
                "failure_code": sanitized_exception(exc)[1],
                "sanitized_exception_class": sanitized_exception(exc)[2],
                "preserved_rows": len(rows),
                "preserved_trajectories": len(trajectories),
            }
        )
        write_json_atomic(manifest_path, manifest)
        log.emit(f"FAILED and preserved; class={type(exc).__name__}; rows={len(rows)}; trajectories={len(trajectories)}")
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rts-data", type=Path, required=True)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--cpu-threads", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return execute(args)


if __name__ == "__main__":
    raise SystemExit(main())
