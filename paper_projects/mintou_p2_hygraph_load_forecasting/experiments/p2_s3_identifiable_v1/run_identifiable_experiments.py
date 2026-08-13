"""Run the frozen P2 S3 capacity-matched rolling-origin experiment once.

The namespace is append-only after completion.  The driver deliberately does
not import the historical training drivers: their fixed-split sampling and
smaller TemporalOnly head are the design limitations addressed here.
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
import random
import shutil
import statistics
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import torch
from torch import nn


SCRIPT = Path(__file__).resolve()
RUN_ROOT = SCRIPT.parent
CONFIG_PATH = RUN_ROOT / "config.json"
RESULTS_ROOT = RUN_ROOT / "results"
LOG_PATH = RUN_ROOT / "logs" / "run.log"
MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
REPO_ROOT = RUN_ROOT.parents[3]

COUNTRY_COLUMNS = {
    "DE": "DE_load_actual_entsoe_transparency",
    "FR": "FR_load_actual_entsoe_transparency",
    "IT": "IT_load_actual_entsoe_transparency",
    "ES": "ES_load_actual_entsoe_transparency",
    "NL": "NL_load_actual_entsoe_transparency",
    "PL": "PL_load_actual_entsoe_transparency",
}

MODEL_SPECS = (
    ("CSA-Poincare-Shared", "proposed", "learned", "shared"),
    ("TargetSelfContext-Matched", "capacity_compute_matched_control", "self", "shared"),
    ("UniformCrossSeries-Matched", "informative_cross_series_control", "uniform", "shared"),
    ("CSA-Euclidean-Shared", "weight_form_control", "euclidean", "shared"),
    ("CSA-FixedScale-Shared", "weight_form_control", "fixed", "shared"),
    ("CSA-Poincare-IndependentEncoder", "shared_encoder_control", "learned", "independent"),
)

METRICS = ("mape", "wape", "mae", "rmse", "smape")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(message: str, *, persist: bool = True) -> None:
    line = f"[{utc_now()}] {message}"
    print(line, flush=True)
    if persist:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def verify_frozen_inputs(config: dict) -> Path:
    if config["run_namespace"] != RUN_ROOT.name:
        raise RuntimeError("config namespace does not match directory name")
    if config["status"] != "frozen_before_execution":
        raise RuntimeError("config is not frozen_before_execution")
    source = Path(config["source_file"]["path"])
    if not source.is_file():
        raise FileNotFoundError(source)
    observed = sha256_file(source)
    expected = config["source_file"]["sha256"].lower()
    if observed != expected:
        raise RuntimeError(f"source SHA-256 mismatch: expected {expected}, observed {observed}")
    return source


def parse_opsd(source: Path, max_rows: int) -> tuple[list[str], dict[str, list[float]], dict[str, int]]:
    timestamps: list[str] = []
    series = {name: [] for name in COUNTRY_COLUMNS}
    scanned = 0
    discarded = 0
    with source.open(encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            scanned += 1
            values: dict[str, float] = {}
            valid = True
            for name, column in COUNTRY_COLUMNS.items():
                raw = row.get(column) or ""
                if not raw:
                    valid = False
                    break
                try:
                    values[name] = float(raw)
                except ValueError:
                    valid = False
                    break
            if not valid:
                discarded += 1
                continue
            timestamps.append(row["utc_timestamp"])
            for name, value in values.items():
                series[name].append(value)
            if len(timestamps) >= max_rows:
                break
    if len(timestamps) != max_rows:
        raise RuntimeError(f"expected {max_rows} retained OPSD rows, observed {len(timestamps)}")
    return timestamps, series, {
        "source_rows_scanned_before_stop": scanned,
        "retained_rows": len(timestamps),
        "discarded_rows_before_stop": discarded,
    }


def configure_determinism() -> dict:
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    deterministic_error = ""
    enforced = False
    try:
        torch.use_deterministic_algorithms(True)
        enforced = bool(torch.are_deterministic_algorithms_enabled())
    except Exception as exc:  # retained as environment evidence
        deterministic_error = f"{type(exc).__name__}: {exc}"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return {
        "device": str(device),
        "global_deterministic_algorithms_enforced": enforced,
        "deterministic_configuration_error": deterministic_error,
        "cudnn_deterministic": bool(torch.backends.cudnn.deterministic),
        "cudnn_benchmark": bool(torch.backends.cudnn.benchmark),
        "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG", ""),
    }


class IdentifiableCSA(nn.Module):
    """CSA model with a common 48-d context slot and 100-d prediction head."""

    def __init__(self, n_series: int, context_mode: str, encoder_mode: str) -> None:
        super().__init__()
        self.n_series = n_series
        self.context_mode = context_mode
        self.encoder_mode = encoder_mode
        if encoder_mode == "shared":
            self.encoder = nn.Sequential(
                nn.Linear(168, 96), nn.ReLU(), nn.Linear(96, 48), nn.ReLU()
            )
            self.independent_encoders = None
            self.series_calibration = None
            self.group_gain = None
        elif encoder_mode == "independent":
            widths = [16, 16, 16, 16, 15, 15]
            if n_series != len(widths):
                raise ValueError("capacity-matched independent encoder is frozen for six OPSD series")
            self.encoder = None
            self.independent_encoders = nn.ModuleList(
                nn.Sequential(nn.Linear(168, width), nn.ReLU(), nn.Linear(width, 48), nn.ReLU())
                for width in widths
            )
            # 186 series-specific plus eight shared channel-group calibration
            # parameters close the exact 194-parameter encoder-capacity gap.
            self.series_calibration = nn.Parameter(torch.zeros(n_series, 31))
            self.group_gain = nn.Parameter(torch.zeros(8))
        else:
            raise ValueError(encoder_mode)

        self.embed_raw = nn.Parameter(torch.randn(n_series, 8) * 0.2)
        self.kappa = nn.Parameter(torch.zeros(n_series))
        self.value = nn.Linear(48, 48)
        self.head = nn.Sequential(nn.Linear(100, 64), nn.ReLU(), nn.Linear(64, 1))

    def encode(self, windows: torch.Tensor) -> torch.Tensor:
        if self.encoder_mode == "shared":
            assert self.encoder is not None
            return self.encoder(windows)
        assert self.independent_encoders is not None
        assert self.series_calibration is not None
        assert self.group_gain is not None
        encoded = torch.stack(
            [module(windows[:, idx, :]) for idx, module in enumerate(self.independent_encoders)],
            dim=1,
        )
        calibration_index = torch.arange(48, device=windows.device) % 31
        calibration = self.series_calibration[:, calibration_index]
        gains = 1.0 + 0.01 * self.group_gain.repeat_interleave(6)
        return (encoded + calibration.unsqueeze(0)) * gains.view(1, 1, 48)

    def poincare_embed(self) -> torch.Tensor:
        norm = self.embed_raw.norm(dim=1, keepdim=True).clamp_min(1e-6)
        return self.embed_raw / norm * 0.95 * torch.tanh(norm)

    def pairwise_distance(self) -> torch.Tensor:
        embedded = self.poincare_embed()
        if self.context_mode == "euclidean":
            return torch.cdist(embedded, embedded)
        squared = torch.cdist(embedded, embedded).pow(2)
        denom = (1.0 - embedded.pow(2).sum(dim=1)).clamp_min(1e-6)
        argument = 1.0 + 2.0 * squared / (denom[:, None] * denom[None, :])
        return torch.acosh(argument.clamp_min(1.0 + 1e-7))

    def forward(self, windows: torch.Tensor, calendar: torch.Tensor, sidx: torch.Tensor) -> torch.Tensor:
        batch, series_count, _ = windows.shape
        encoded = self.encode(windows)
        target_encoded = encoded[torch.arange(batch, device=windows.device), sidx]

        distance = self.pairwise_distance()
        if self.context_mode == "fixed":
            scale = torch.ones_like(self.kappa) + 0.0 * self.kappa
        else:
            scale = torch.nn.functional.softplus(self.kappa) + 0.1
        scores = -scale[:, None] * distance
        diagonal = torch.eye(series_count, dtype=torch.bool, device=windows.device)
        scores = scores.masked_fill(diagonal, float("-inf"))
        learned_attention = torch.softmax(scores, dim=1)
        if self.context_mode == "uniform":
            uniform = torch.full_like(learned_attention, 1.0 / (series_count - 1))
            uniform = uniform.masked_fill(diagonal, 0.0)
            attention = uniform + 0.0 * learned_attention
        else:
            attention = learned_attention

        value_encoded = self.value(encoded)
        sample_attention = attention[sidx]
        cross_context = torch.bmm(sample_attention.unsqueeze(1), value_encoded).squeeze(1)
        if self.context_mode == "self":
            self_context = value_encoded[torch.arange(batch, device=windows.device), sidx]
            context = self_context + 0.0 * cross_context
        else:
            context = cross_context
        return self.head(torch.cat([target_encoded, context, calendar], dim=1)).squeeze(-1)


def count_parameters(module: nn.Module) -> int:
    return sum(parameter.numel() for parameter in module.parameters())


def model_audit_rows(n_series: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for name, role, context_mode, encoder_mode in MODEL_SPECS:
        torch.manual_seed(1)
        model = IdentifiableCSA(n_series, context_mode, encoder_mode)
        encoder_parameters = 0
        if encoder_mode == "shared":
            assert model.encoder is not None
            encoder_parameters = count_parameters(model.encoder)
            encoder_macs = n_series * (168 * 96 + 96 * 48)
        else:
            assert model.independent_encoders is not None
            encoder_parameters = (
                count_parameters(model.independent_encoders)
                + model.series_calibration.numel()
                + model.group_gain.numel()
            )
            encoder_macs = 168 * (16 * 4 + 15 * 2) + 48 * (16 * 4 + 15 * 2)
        rows.append(
            {
                "method": name,
                "role": role,
                "context_mode": context_mode,
                "encoder_mode": encoder_mode,
                "total_parameters": count_parameters(model),
                "encoder_parameters": encoder_parameters,
                "context_parameters": model.embed_raw.numel() + model.kappa.numel() + count_parameters(model.value),
                "head_parameters": count_parameters(model.head),
                "head_input_width": 100,
                "context_width": 48,
                "estimated_encoder_macs_per_unique_origin": encoder_macs,
                "attention_distance_path_executed": True,
                "exact_primary_match_contract": encoder_mode == "shared" and context_mode in {"learned", "self", "uniform"},
            }
        )
    totals = {int(row["total_parameters"]) for row in rows}
    if totals != {29815}:
        raise RuntimeError(f"parameter-match invariant failed: {totals}")
    return rows


def calendar_tensor(target_t: torch.Tensor) -> torch.Tensor:
    hour = (target_t % 24).float()
    day = ((target_t // 24) % 7).float()
    return torch.stack(
        [
            torch.sin(2 * math.pi * hour / 24),
            torch.cos(2 * math.pi * hour / 24),
            torch.sin(2 * math.pi * day / 7),
            torch.cos(2 * math.pi * day / 7),
        ],
        dim=1,
    )


def assemble_samples(
    normalized: torch.Tensor,
    values: torch.Tensor,
    origins: torch.Tensor,
    horizon: int,
) -> dict[str, torch.Tensor]:
    n_series = normalized.shape[0]
    expanded_t = origins.repeat_interleave(n_series)
    sidx = torch.arange(n_series).repeat(origins.numel())
    offsets = torch.arange(-167, 1)
    gather = expanded_t[:, None] + offsets[None, :]
    windows = normalized[:, gather].permute(1, 0, 2).contiguous()
    target_t = expanded_t + horizon
    target = normalized[sidx, target_t]
    actual = values[sidx, target_t]
    return {
        "windows": windows,
        "calendar": calendar_tensor(target_t),
        "sidx": sidx,
        "target": target,
        "actual": actual,
        "origin_t": expanded_t,
        "target_t": target_t,
    }


def prepare_origin_split(values: torch.Tensor, origin_index: int, config: dict) -> dict[str, object]:
    horizon = int(config["forecast"]["horizon_positions"])
    stride = int(config["forecast"]["training_origin_stride"])
    test_count = int(config["forecast"]["test_origin_positions_per_rolling_origin"])
    if origin_index + test_count + horizon > values.shape[1]:
        raise RuntimeError("rolling-origin test block exceeds retained data")

    means = values[:, :origin_index].mean(dim=1, keepdim=True)
    stds = values[:, :origin_index].std(dim=1, keepdim=True).clamp_min(1e-6)
    normalized = (values - means) / stds
    eligible = torch.arange(168, origin_index - horizon, stride)
    cutoff_index = int(eligible.numel() * 0.85)
    fit_origins = eligible[:cutoff_index]
    validation_origins = eligible[cutoff_index:]
    test_origins = torch.arange(origin_index, origin_index + test_count)
    if int(fit_origins[-1]) + horizon >= origin_index:
        raise RuntimeError("training-target embargo invariant failed")
    return {
        "fit": assemble_samples(normalized, values, fit_origins, horizon),
        "validation": assemble_samples(normalized, values, validation_origins, horizon),
        "test": assemble_samples(normalized, values, test_origins, horizon),
        "means": means,
        "stds": stds,
        "fit_unique_origins": fit_origins.numel(),
        "validation_unique_origins": validation_origins.numel(),
        "test_unique_origins": test_origins.numel(),
        "last_training_target_index": int(eligible[-1]) + horizon,
        "first_test_origin_index": origin_index,
    }


class ManualAdam:
    """Eager Adam used because torch.optim imports unavailable sympy here."""

    def __init__(self, parameters: Iterable[torch.nn.Parameter], learning_rate: float) -> None:
        self.parameters = [parameter for parameter in parameters if parameter.requires_grad]
        self.learning_rate = learning_rate
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.epsilon = 1e-8
        self.step_number = 0
        self.first = [torch.zeros_like(parameter) for parameter in self.parameters]
        self.second = [torch.zeros_like(parameter) for parameter in self.parameters]

    def zero_grad(self) -> None:
        for parameter in self.parameters:
            parameter.grad = None

    @torch.no_grad()
    def step(self) -> None:
        self.step_number += 1
        bias1 = 1.0 - self.beta1**self.step_number
        bias2 = 1.0 - self.beta2**self.step_number
        for parameter, first, second in zip(self.parameters, self.first, self.second):
            if parameter.grad is None:
                continue
            gradient = parameter.grad
            first.mul_(self.beta1).add_(gradient, alpha=1.0 - self.beta1)
            second.mul_(self.beta2).addcmul_(gradient, gradient, value=1.0 - self.beta2)
            denominator = second.sqrt().div_(math.sqrt(bias2)).add_(self.epsilon)
            parameter.addcdiv_(first, denominator, value=-self.learning_rate / bias1)


def batch_predictions(
    model: nn.Module,
    split: dict[str, torch.Tensor],
    device: torch.device,
    batch_size: int,
) -> torch.Tensor:
    predictions: list[torch.Tensor] = []
    model.eval()
    with torch.no_grad():
        for start in range(0, split["windows"].shape[0], batch_size):
            stop = start + batch_size
            predictions.append(
                model(
                    split["windows"][start:stop].to(device),
                    split["calendar"][start:stop].to(device),
                    split["sidx"][start:stop].to(device),
                ).cpu()
            )
    return torch.cat(predictions)


def train_and_predict(
    context_mode: str,
    encoder_mode: str,
    seed: int,
    split: dict[str, object],
    config: dict,
    device: torch.device,
) -> tuple[torch.Tensor, dict[str, object]]:
    torch.manual_seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
    model = IdentifiableCSA(6, context_mode, encoder_mode).to(device)
    if count_parameters(model) != 29815:
        raise RuntimeError("run-time parameter count drift")
    optimizer = ManualAdam(model.parameters(), float(config["training"]["learning_rate"]))
    loss_function = nn.MSELoss()
    epochs = int(config["training"]["epochs"])
    batch_size = int(config["training"]["batch_size"])
    fit = split["fit"]
    validation = split["validation"]
    assert isinstance(fit, dict) and isinstance(validation, dict)

    best_validation = float("inf")
    best_epoch = 0
    best_state = {name: tensor.detach().clone() for name, tensor in model.state_dict().items()}
    optimizer_steps = 0
    started = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        permutation = torch.randperm(fit["windows"].shape[0])
        for start in range(0, permutation.numel(), batch_size):
            indices = permutation[start : start + batch_size]
            optimizer.zero_grad()
            prediction = model(
                fit["windows"][indices].to(device),
                fit["calendar"][indices].to(device),
                fit["sidx"][indices].to(device),
            )
            loss = loss_function(prediction, fit["target"][indices].to(device))
            loss.backward()
            optimizer.step()
            optimizer_steps += 1

        normalized_predictions = batch_predictions(model, validation, device, 4096)
        validation_loss = loss_function(normalized_predictions, validation["target"]).item()
        if validation_loss < best_validation:
            best_validation = validation_loss
            best_epoch = epoch
            best_state = {name: tensor.detach().clone() for name, tensor in model.state_dict().items()}

    model.load_state_dict(best_state)
    normalized_test = batch_predictions(model, split["test"], device, 4096)
    test = split["test"]
    means = split["means"].squeeze(1)
    stds = split["stds"].squeeze(1)
    predictions = normalized_test * stds[test["sidx"]] + means[test["sidx"]]
    runtime = time.perf_counter() - started
    return predictions, {
        "runtime_s": runtime,
        "best_epoch": best_epoch,
        "best_validation_mse": best_validation,
        "optimizer_steps": optimizer_steps,
        "parameter_count": count_parameters(model),
    }


def metric_values(actual: torch.Tensor, prediction: torch.Tensor) -> dict[str, float]:
    actual = actual.double()
    prediction = prediction.double()
    absolute_error = (actual - prediction).abs()
    epsilon = 1e-6
    return {
        "mape": float((absolute_error / actual.abs().clamp_min(epsilon)).mean()),
        "wape": float(absolute_error.sum() / actual.abs().sum().clamp_min(epsilon)),
        "mae": float(absolute_error.mean()),
        "rmse": float(torch.sqrt(((actual - prediction) ** 2).mean())),
        "smape": float((2.0 * absolute_error / (actual.abs() + prediction.abs()).clamp_min(epsilon)).mean()),
    }


def day_metric_rows(
    method: str,
    origin_label: str,
    seed: int,
    timestamps: list[str],
    test: dict[str, torch.Tensor],
    predictions: torch.Tensor,
) -> list[dict[str, object]]:
    by_date: dict[str, list[int]] = defaultdict(list)
    for position, target_index in enumerate(test["target_t"].tolist()):
        by_date[timestamps[target_index][:10]].append(position)
    rows: list[dict[str, object]] = []
    for date, positions in sorted(by_date.items()):
        indices = torch.tensor(positions, dtype=torch.long)
        values = metric_values(test["actual"][indices], predictions[indices])
        rows.append(
            {
                "method": method,
                "rolling_origin": origin_label,
                "seed": seed,
                "forecast_target_date_utc": date,
                "target_count": len(positions),
                **{metric: f"{values[metric]:.10f}" for metric in METRICS},
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def mean(values: Iterable[float]) -> float:
    return statistics.fmean(values)


def exact_sign_flip_p(differences: list[float]) -> float:
    observed = abs(mean(differences))
    count = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(differences)):
        permuted = abs(mean(sign * value for sign, value in zip(signs, differences)))
        count += int(permuted >= observed - 1e-15)
        total += 1
    return count / total


def bootstrap_interval(differences: list[float], seed: int, resamples: int = 20000) -> tuple[float, float]:
    generator = random.Random(seed)
    estimates = []
    for _ in range(resamples):
        estimates.append(mean(generator.choice(differences) for _ in differences))
    estimates.sort()
    lower = estimates[int(0.025 * resamples)]
    upper = estimates[min(resamples - 1, int(0.975 * resamples))]
    return lower, upper


def holm_adjust(p_values: list[float]) -> list[float]:
    count = len(p_values)
    order = sorted(range(count), key=lambda index: p_values[index])
    adjusted = [1.0] * count
    running = 0.0
    for rank, index in enumerate(order):
        candidate = min(1.0, (count - rank) * p_values[index])
        running = max(running, candidate)
        adjusted[index] = running
    return adjusted


def derive_tables(run_rows: list[dict[str, object]], config: dict) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in run_rows:
        grouped[(str(row["method"]), str(row["rolling_origin"]))].append(row)

    origin_rows: list[dict[str, object]] = []
    for (method, origin), rows in sorted(grouped.items()):
        origin_rows.append(
            {
                "method": method,
                "rolling_origin": origin,
                "seed_count": len(rows),
                **{
                    metric: f"{mean(float(row[metric]) for row in rows):.10f}"
                    for metric in METRICS
                },
            }
        )

    by_method: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in origin_rows:
        by_method[str(row["method"])].append(row)
    leaderboard: list[dict[str, object]] = []
    for method, rows in by_method.items():
        record: dict[str, object] = {"method": method, "origin_count": len(rows)}
        for metric in METRICS:
            values = [float(row[metric]) for row in rows]
            record[f"mean_{metric}"] = f"{mean(values):.10f}"
            record[f"std_{metric}"] = f"{statistics.stdev(values):.10f}"
        leaderboard.append(record)
    leaderboard.sort(key=lambda row: float(row["mean_mape"]))
    for rank, row in enumerate(leaderboard, start=1):
        row["mape_rank"] = rank

    proposed = "CSA-Poincare-Shared"
    controls = [name for name, _, _, _ in MODEL_SPECS if name != proposed]
    lookup = {
        (str(row["method"]), str(row["rolling_origin"])): row
        for row in origin_rows
    }
    origin_labels = sorted({str(row["rolling_origin"]) for row in origin_rows})
    comparison_rows: list[dict[str, object]] = []
    primary_indices: list[int] = []
    primary_p_values: list[float] = []
    analysis_seed = int(config["statistics"]["analysis_seed"])
    for control_index, control in enumerate(controls):
        for metric_index, metric in enumerate(("mape", "wape")):
            differences = [
                float(lookup[(proposed, origin)][metric]) - float(lookup[(control, origin)][metric])
                for origin in origin_labels
            ]
            control_values = [float(lookup[(control, origin)][metric]) for origin in origin_labels]
            observed = mean(differences)
            ci_lower, ci_upper = bootstrap_interval(
                differences,
                analysis_seed + control_index * 17 + metric_index,
            )
            raw_p = exact_sign_flip_p(differences)
            row = {
                "proposed": proposed,
                "control": control,
                "metric": metric,
                "outer_unit": "rolling_origin",
                "n_outer_units": len(differences),
                "mean_difference_proposed_minus_control": f"{observed:.10f}",
                "relative_difference_percent": f"{100.0 * observed / max(abs(mean(control_values)), 1e-12):.6f}",
                "bootstrap_95_ci_lower": f"{ci_lower:.10f}",
                "bootstrap_95_ci_upper": f"{ci_upper:.10f}",
                "exact_sign_flip_p": f"{raw_p:.10f}",
                "holm_p_primary_family": "",
                "origins_favoring_proposed": sum(value < 0 for value in differences),
                "origins_favoring_control": sum(value > 0 for value in differences),
                "zero_difference_origins": sum(value == 0 for value in differences),
                "interpretation": "proposed_lower_error" if observed < 0 else "control_lower_error" if observed > 0 else "no_mean_difference",
            }
            comparison_rows.append(row)
            if metric == "mape":
                primary_indices.append(len(comparison_rows) - 1)
                primary_p_values.append(raw_p)
    adjusted = holm_adjust(primary_p_values)
    for index, value in zip(primary_indices, adjusted):
        comparison_rows[index]["holm_p_primary_family"] = f"{value:.10f}"
    return origin_rows, leaderboard, comparison_rows


def render_experiment_result(
    config: dict,
    leaderboard: list[dict[str, object]],
    comparisons: list[dict[str, object]],
    row_count: int,
    day_count: int,
    started_at: str,
) -> str:
    lead = {str(row["method"]): row for row in leaderboard}
    primary = [row for row in comparisons if row["metric"] == "mape"]
    self_row = next(row for row in primary if row["control"] == "TargetSelfContext-Matched")
    uniform_row = next(row for row in primary if row["control"] == "UniformCrossSeries-Matched")
    independent_row = next(row for row in primary if row["control"] == "CSA-Poincare-IndependentEncoder")
    weight_rows = [
        row for row in primary
        if row["control"] in {
            "UniformCrossSeries-Matched",
            "CSA-Euclidean-Shared",
            "CSA-FixedScale-Shared",
        }
    ]
    separated = [row for row in weight_rows if float(row["holm_p_primary_family"]) < 0.05]
    weight_statement = (
        "At least one frozen weighting-form contrast separated after Holm correction: "
        + ", ".join(str(row["control"]) for row in separated)
        if separated
        else "No frozen weighting-form contrast separated after Holm correction. This is not an equivalence result because no equivalence margin was specified."
    )
    return f"""## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run
- Origin Date: {started_at}
- Verification Status: UNVERIFIED
- Version Label: p2_s3_identifiable_v1_exp_result_v1
- Upstream Dependencies: hashed OPSD source; frozen local configuration and driver

# Experiment Result

- **ID:** `p2_s3_identifiable_v1`
- **Type:** neural training and rolling-origin component controls
- **Status:** COMPLETED
- **Run rows:** {row_count}
- **Forecast-day audit rows:** {day_count}
- **Outer analysis unit:** eight rolling temporal origins; five seed runs averaged within each origin
- **Metrics:** MAPE primary, WAPE secondary; MAE, RMSE, and sMAPE descriptive

## Capacity-matched cross-series result

`CSA-Poincare-Shared` has mean origin-level MAPE {lead['CSA-Poincare-Shared']['mean_mape']};
`TargetSelfContext-Matched` has {lead['TargetSelfContext-Matched']['mean_mape']}.
The proposed-minus-control MAPE difference is {self_row['mean_difference_proposed_minus_control']}
(pointwise origin bootstrap 95% interval [{self_row['bootstrap_95_ci_lower']},
{self_row['bootstrap_95_ci_upper']}], exact sign-flip p={self_row['exact_sign_flip_p']},
Holm p={self_row['holm_p_primary_family']}). Negative differences favor the proposed arm.
Both arms have 29,815 instantiated parameters, the same 100-to-64-to-1 head,
the same optimizer, batches, epochs, seeds, and the same executed attention path.

## Informative context and weighting-form controls

The uniform cross-series control has mean MAPE {lead['UniformCrossSeries-Matched']['mean_mape']}.
Its proposed-minus-control difference is {uniform_row['mean_difference_proposed_minus_control']}
(Holm p={uniform_row['holm_p_primary_family']}). {weight_statement}

The weighting block is combined evidence only for that bounded joint statement;
it does not identify a best form when contrasts do not separate and it does not
upgrade non-significance to equivalence.

## Shared-versus-independent encoder control

The capacity-matched independent-encoder arm has mean MAPE
{lead['CSA-Poincare-IndependentEncoder']['mean_mape']}; its proposed-minus-control
difference is {independent_row['mean_difference_proposed_minus_control']}
(Holm p={independent_row['holm_p_primary_family']}). Although total parameters
and the downstream head are matched, independent encoders use narrower hidden
layers and less encoder arithmetic. This result cannot isolate sharing from
width allocation and does not license a general claim that sharing helps or hurts.

## Evidence boundary

This run narrows confirmation to OPSD lead 24 and does not equalize or rerun the
historical external architecture roster. It does not broaden claims to OPSD
lead 1, SimBench, Ausgrid, other years, exogenous weather, hierarchical
coherence, dispatch, or deployment. Processed positions can skip UTC hours
because the frozen parser drops a row when any selected series is missing.
No independent rerun was performed, so the artifact remains `UNVERIFIED`.
"""


def render_validation_report(comparisons: list[dict[str, object]], source_profile: dict[str, int], started_at: str) -> str:
    primary = [row for row in comparisons if row["metric"] == "mape"]
    findings = "\n".join(
        f"| CSA-Poincare-Shared vs {row['control']} | exact paired sign-flip over origins | "
        f"diff={row['mean_difference_proposed_minus_control']}, raw p={row['exact_sign_flip_p']}, Holm p={row['holm_p_primary_family']} | "
        f"origin bootstrap [{row['bootstrap_95_ci_lower']}, {row['bootstrap_95_ci_upper']}] | CAUTION |"
        for row in primary
    )
    return f"""## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: validate
- Origin Date: {started_at}
- Verification Status: ANALYZED
- Version Label: p2_s3_identifiable_v1_validation_v1

# Validation Report

- **Source:** `p2_s3_identifiable_v1`
- **Overall Confidence:** CAUTION
- **Outer unit:** eight rolling origins; seeds averaged before inference
- **Fallacy coverage:** 11/11 checked

## Statistical Findings

| Contrast | Test | MAPE result | Effect interval | Confidence |
|---|---|---|---|---|
{findings}

WAPE is retained in `paired_comparisons.csv` as the frozen secondary metric.
Its p-values are descriptive and are not inserted into the primary Holm family.
Intervals are pointwise percentile bootstrap intervals over eight origins;
they are not simultaneous intervals and do not make adjacent origin blocks independent.

## Assumptions and warnings

- Exact sign-flip inference assumes origin-level differences are exchangeable
  under the null. Quarterly blocks reduce overlap, but all origins come from
  one dataset and adjacent weather years; full independence is not established.
- The parser scanned {source_profile['source_rows_scanned_before_stop']} rows,
  retained {source_profile['retained_rows']}, and discarded
  {source_profile['discarded_rows_before_stop']} before reaching the frozen
  35,000-row cap. A 24-position lead is therefore not guaranteed to equal 24
  elapsed UTC hours at every location of a dropped row.
- Five neural seeds improve optimization coverage but are averaged within
  origin and are not treated as data replications.
- No equivalence margin was specified; null weighting-form results remain
  unresolved differences rather than equivalence.
- The independent-encoder control matches total parameters but changes hidden
  width allocation and encoder arithmetic, so it is not a clean causal test of
  parameter sharing.

## Fallacy Scan

| # | Fallacy | Severity | Check result |
|---|---|---|---|
| 1 | Simpson's paradox | NOTE | Origin-specific paired values are preserved; inference is not based only on a pooled target table. Direction counts are reported per contrast. |
| 2 | Ecological fallacy | NOTE | The outer unit is a temporal origin and no claim about individual consumers is made from country-level series. |
| 3 | Berkson's paradox | CAUTION | The six-series complete-row filter selects timestamps where all named country values are present; generalization to discarded timestamps is unsupported. |
| 4 | Collider bias | NOTE | No post-treatment covariate or model-performance collider is adjusted for in the paired analysis. |
| 5 | Base-rate neglect | NOTE | Not applicable: this is continuous-error forecasting, not classification or screening. |
| 6 | Regression to the mean | NOTE | Quarterly origins were frozen by calendar date rather than selected for extreme historical model error. |
| 7 | Survivorship bias | CAUTION | Rows missing any selected series are excluded. Exact discarded-row counts before the retained cap are reported, but performance on those timestamps is unobserved. |
| 8 | Look-elsewhere effect | NOTE | One primary metric and five contrasts were frozen; Holm correction covers that primary family. Secondary WAPE remains descriptive. |
| 9 | Garden of forking paths | CAUTION | The local configuration was frozen before execution, but the study was not externally preregistered and follows earlier fixed-split evidence. |
| 10 | Correlation is not causation | NOTE | Results concern predictive error under code-level component interventions; no physical or behavioral causal mechanism is claimed. |
| 11 | Reverse causality | NOTE | Histories precede target positions, but forecasting precedence is not used to claim a causal load mechanism. |

## Reproducibility

- **Method:** not rerun
- **Verdict:** CANNOT_VERIFY
- The completed manifest records the configuration, driver, input, environment,
  and output hashes. A separate immutable rerun is required for `VERIFIED` status.
"""


def preflight(config: dict) -> None:
    source = verify_frozen_inputs(config)
    timestamps, series, profile = parse_opsd(source, int(config["source_file"]["max_retained_rows"]))
    origin_lookup = {timestamp: index for index, timestamp in enumerate(timestamps)}
    missing = [timestamp for timestamp in config["forecast"]["rolling_origin_timestamps_utc"] if timestamp not in origin_lookup]
    if missing:
        raise RuntimeError(f"missing rolling-origin timestamps: {missing}")
    audits = model_audit_rows(len(series))
    environment = configure_determinism()
    device = torch.device(environment["device"])
    torch.manual_seed(11)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(11)
    windows = torch.randn(12, 6, 168, device=device)
    calendar = torch.randn(12, 4, device=device)
    sidx = torch.arange(6, device=device).repeat(2)
    for _, _, context_mode, encoder_mode in MODEL_SPECS:
        model = IdentifiableCSA(6, context_mode, encoder_mode).to(device)
        prediction = model(windows, calendar, sidx)
        prediction.square().mean().backward()
        optimizer = ManualAdam(model.parameters(), 0.001)
        optimizer.step()
    log(
        f"PREFLIGHT OK retained={profile['retained_rows']} discarded={profile['discarded_rows_before_stop']} "
        f"origins={[origin_lookup[t] for t in config['forecast']['rolling_origin_timestamps_utc']]} "
        f"parameters={sorted({row['total_parameters'] for row in audits})} device={device}",
        persist=False,
    )


def run() -> None:
    if MANIFEST_PATH.exists():
        raise RuntimeError(f"completed or attempted namespace already has {MANIFEST_PATH}")
    if LOG_PATH.exists() or (RESULTS_ROOT.exists() and any(RESULTS_ROOT.iterdir())):
        raise RuntimeError("namespace already contains run outputs; automatic retry is prohibited")

    config = load_config()
    started_at = utc_now()
    log("START p2_s3_identifiable_v1")
    source = verify_frozen_inputs(config)
    environment = configure_determinism()
    device = torch.device(environment["device"])
    log(f"ENVIRONMENT python={sys.version.split()[0]} torch={torch.__version__} device={device}")
    timestamps, series, source_profile = parse_opsd(
        source,
        int(config["source_file"]["max_retained_rows"]),
    )
    names = list(config["source_file"]["series"])
    values = torch.tensor([series[name] for name in names], dtype=torch.float32)
    origin_lookup = {timestamp: index for index, timestamp in enumerate(timestamps)}
    origins = [(label, origin_lookup[label]) for label in config["forecast"]["rolling_origin_timestamps_utc"]]
    audits = model_audit_rows(len(names))
    write_csv(RESULTS_ROOT / "model_audit.csv", audits)
    log(
        f"DATA retained={source_profile['retained_rows']} discarded={source_profile['discarded_rows_before_stop']} "
        f"origin_indices={[index for _, index in origins]}"
    )

    run_rows: list[dict[str, object]] = []
    day_rows: list[dict[str, object]] = []
    seeds = [int(seed) for seed in config["training"]["seeds"]]
    total_runs = len(origins) * len(MODEL_SPECS) * len(seeds)
    completed_runs = 0
    for origin_label, origin_index in origins:
        split = prepare_origin_split(values, origin_index, config)
        log(
            f"ORIGIN {origin_label} index={origin_index} fit_origins={split['fit_unique_origins']} "
            f"validation_origins={split['validation_unique_origins']} test_origins={split['test_unique_origins']} "
            f"last_training_target={split['last_training_target_index']}"
        )
        test = split["test"]
        assert isinstance(test, dict)
        for method, role, context_mode, encoder_mode in MODEL_SPECS:
            for seed in seeds:
                predictions, training = train_and_predict(
                    context_mode,
                    encoder_mode,
                    seed,
                    split,
                    config,
                    device,
                )
                metric = metric_values(test["actual"], predictions)
                completed_runs += 1
                run_rows.append(
                    {
                        "dataset": "OPSD time_series_60min_singleindex",
                        "horizon_positions": 24,
                        "rolling_origin": origin_label,
                        "rolling_origin_index": origin_index,
                        "method": method,
                        "method_role": role,
                        "seed": seed,
                        "epochs_completed": int(config["training"]["epochs"]),
                        "best_epoch": training["best_epoch"],
                        "best_validation_mse": f"{float(training['best_validation_mse']):.10f}",
                        "optimizer_steps": training["optimizer_steps"],
                        "parameter_count": training["parameter_count"],
                        "fit_unique_origins": split["fit_unique_origins"],
                        "validation_unique_origins": split["validation_unique_origins"],
                        "test_unique_origins": split["test_unique_origins"],
                        "test_target_count": test["actual"].numel(),
                        **{key: f"{metric[key]:.10f}" for key in METRICS},
                        "runtime_s": f"{float(training['runtime_s']):.4f}",
                    }
                )
                day_rows.extend(
                    day_metric_rows(method, origin_label, seed, timestamps, test, predictions)
                )
                write_csv(RESULTS_ROOT / "run_results.csv", run_rows)
                write_csv(RESULTS_ROOT / "day_metrics.csv", day_rows)
                log(
                    f"RUN {completed_runs}/{total_runs} origin={origin_label} method={method} seed={seed} "
                    f"mape={metric['mape']:.8f} wape={metric['wape']:.8f} runtime_s={float(training['runtime_s']):.2f}"
                )
        del split
        if device.type == "cuda":
            torch.cuda.empty_cache()

    shutil.copyfile(RESULTS_ROOT / "run_results.csv", RESULTS_ROOT / "run_results.completed_snapshot.csv")
    origin_rows, leaderboard, comparisons = derive_tables(run_rows, config)
    write_csv(RESULTS_ROOT / "origin_metrics.csv", origin_rows)
    write_csv(RESULTS_ROOT / "leaderboard.csv", leaderboard)
    write_csv(RESULTS_ROOT / "paired_comparisons.csv", comparisons)

    result_text = render_experiment_result(
        config,
        leaderboard,
        comparisons,
        len(run_rows),
        len(day_rows),
        started_at,
    )
    validation_text = render_validation_report(comparisons, source_profile, started_at)
    (RUN_ROOT / "EXPERIMENT_RESULT.md").write_text(result_text, encoding="utf-8", newline="\n")
    (RUN_ROOT / "VALIDATION_REPORT.md").write_text(validation_text, encoding="utf-8", newline="\n")

    log(
        f"OUTPUT run_rows={len(run_rows)} day_rows={len(day_rows)} origin_rows={len(origin_rows)} "
        f"comparisons={len(comparisons)}"
    )
    log("COMPLETED p2_s3_identifiable_v1")

    output_paths = [
        RESULTS_ROOT / "model_audit.csv",
        RESULTS_ROOT / "run_results.csv",
        RESULTS_ROOT / "run_results.completed_snapshot.csv",
        RESULTS_ROOT / "day_metrics.csv",
        RESULTS_ROOT / "origin_metrics.csv",
        RESULTS_ROOT / "leaderboard.csv",
        RESULTS_ROOT / "paired_comparisons.csv",
        RUN_ROOT / "EXPERIMENT_RESULT.md",
        RUN_ROOT / "VALIDATION_REPORT.md",
    ]
    upstream_paths = [
        REPO_ROOT / "src" / "powergrid_benchmark" / "mintou_real_load_forecasting.py",
        REPO_ROOT / "src" / "powergrid_benchmark" / "mintou_hyg_neural.py",
        REPO_ROOT / "src" / "powergrid_benchmark" / "mintou_neural_forecasting.py",
    ]
    manifest = {
        "run_namespace": config["run_namespace"],
        "status": "completed",
        "started_at": started_at,
        "completed_at": utc_now(),
        "command": [sys.executable, str(SCRIPT)],
        "config_sha256": sha256_file(CONFIG_PATH),
        "script_sha256": sha256_file(SCRIPT),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "torch": torch.__version__,
            "cuda_version": torch.version.cuda,
            "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "pythonpath": os.environ.get("PYTHONPATH", ""),
            **environment,
        },
        "source_profile": {
            **source_profile,
            "first_timestamp": timestamps[0],
            "last_timestamp": timestamps[-1],
            "series": names,
            "source_file": {
                "path": str(source),
                "bytes": source.stat().st_size,
                "sha256": sha256_file(source),
            },
        },
        "upstream_source_hashes": {
            str(path.relative_to(REPO_ROOT)).replace("\\", "/"): sha256_file(path)
            for path in upstream_paths
            if path.is_file()
        },
        "analysis_contract": config["statistics"],
        "comparison_budget": config["comparison_budget"],
        "row_counts": {
            "run_results": len(run_rows),
            "day_metrics": len(day_rows),
            "origin_metrics": len(origin_rows),
            "leaderboard": len(leaderboard),
            "paired_comparisons": len(comparisons),
            "model_audit": len(audits),
        },
        "outputs": {
            str(path.relative_to(RUN_ROOT)).replace("\\", "/"): {
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in output_paths
        },
        "verification_status": "UNVERIFIED",
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="validate data, hashes, model counts, CUDA backward, and manual Adam without writing outputs",
    )
    args = parser.parse_args()
    config = load_config()
    if args.preflight:
        preflight(config)
        return 0
    try:
        run()
    except Exception as exc:
        log(f"FAILED {type(exc).__name__}: {exc}", persist=LOG_PATH.exists())
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
