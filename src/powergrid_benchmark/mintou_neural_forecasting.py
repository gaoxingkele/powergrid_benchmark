"""Neural baselines for mintou p2 (HyG-LoadFormer load forecasting).

Closes the P0 gap from the journal review: the public-data benchmark previously
contained only naive/ridge-level baselines, while the method manifest promised
LSTM/TCN/Transformer-class comparators. This module trains real neural
baselines on EXACTLY the same data, splits, and test samples as
`mintou_real_load_forecasting.py` (imported directly, so the protocol cannot
drift) and merges the results into a combined leaderboard:

- MLP            : lag window + calendar -> 128 -> 64 -> 1
- LSTM           : univariate 168h window, hidden 48, calendar-concat head
- TCN            : dilated causal Conv1d stack (k=3, dilations 1..64)
- DLinear        : moving-average trend/seasonal decomposition + two linears
- PatchTST-lite  : patch embedding (16/8) + 2-layer Transformer encoder

Training choices (identical for every neural model): global model across
series with per-series train-split z-normalization, Adam 1e-3, MSE on the
normalized target, batch 512, early stopping on the last 15% of the training
window (by time), training-sample stride 3 (test set NEVER strided or altered
so metrics are directly comparable with the existing stdlib rows). Three seeds
per model; the seed with median test MAPE provides the headline row and the
full per-seed table is preserved.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT / "src"))

from powergrid_benchmark.mintou_real_load_forecasting import (  # noqa: E402
    HORIZONS,
    P2_ROOT,
    Sample,
    evaluate_predictions,
    parse_opsd,
    parse_simbench,
    samples_for,
    write_csv,
)

WINDOW = 168
TRAIN_STRIDE = 3
BATCH_SIZE = 512
SEEDS = (11, 23, 47)
NEURAL_RUN_VERSION = "public_data_benchmark_v5_neural_baselines"

MODEL_SPECS = (
    ("MLP", "Feedforward 168-lag + calendar, 128-64-1.", 20),
    ("LSTM", "Univariate LSTM over the 168h window, hidden 48.", 6),
    ("TCN", "Dilated causal Conv1d stack, k=3, dilations 1..64.", 10),
    ("DLinear", "Moving-average decomposition + per-branch linear (Zeng et al. 2023).", 20),
    ("PatchTST-lite", "Patch embedding (16/8) + 2-layer Transformer encoder.", 8),
)


# ---------------------------------------------------------------------------
# Dataset assembly (identical samples to the stdlib pipeline)
# ---------------------------------------------------------------------------


@dataclass
class SeriesTensors:
    """Per-dataset tensors with per-series z-normalization from the train split."""

    names: list[str]
    values: "object"  # torch.Tensor [n_series, T]
    norm: "object"  # normalized values
    means: "object"
    stds: "object"


def build_tensors(series: dict[str, list[float]], train_end: int):
    import torch

    names = list(series)
    n = min(len(v) for v in series.values())
    values = torch.tensor([series[name][:n] for name in names], dtype=torch.float32)
    means = values[:, :train_end].mean(dim=1, keepdim=True)
    stds = values[:, :train_end].std(dim=1, keepdim=True).clamp_min(1e-6)
    norm = (values - means) / stds
    return SeriesTensors(names=names, values=values, norm=norm, means=means, stds=stds)


def sample_tensors(samples: list[Sample], tensors: SeriesTensors, horizon: int):
    """Windows [N, WINDOW], calendar [N, 4], series index [N], normalized target [N]."""
    import torch

    index = {name: i for i, name in enumerate(tensors.names)}
    sidx = torch.tensor([index[s.country] for s in samples], dtype=torch.long)
    t_idx = torch.tensor([s.t for s in samples], dtype=torch.long)
    offsets = torch.arange(-WINDOW + 1, 1)
    gather_idx = t_idx[:, None] + offsets[None, :]
    windows = tensors.norm[sidx[:, None], gather_idx]
    target_t = t_idx + horizon
    y = tensors.norm[sidx, target_t]
    hour = (target_t % 24).float()
    dow = ((target_t // 24) % 7).float()
    calendar = torch.stack(
        [
            torch.sin(2 * math.pi * hour / 24),
            torch.cos(2 * math.pi * hour / 24),
            torch.sin(2 * math.pi * dow / 7),
            torch.cos(2 * math.pi * dow / 7),
        ],
        dim=1,
    )
    return windows, calendar, sidx, y


def denormalize(preds, sidx, tensors: SeriesTensors):
    return preds * tensors.stds.squeeze(1)[sidx] + tensors.means.squeeze(1)[sidx]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def make_model(name: str):
    import torch
    from torch import nn

    if name == "MLP":

        class MLP(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.net = nn.Sequential(
                    nn.Linear(WINDOW + 4, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 1)
                )

            def forward(self, windows, calendar):
                return self.net(torch.cat([windows, calendar], dim=1)).squeeze(-1)

        return MLP()

    if name == "LSTM":

        class LSTMModel(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.lstm = nn.LSTM(input_size=1, hidden_size=48, num_layers=1, batch_first=True)
                self.head = nn.Linear(48 + 4, 1)

            def forward(self, windows, calendar):
                out, _ = self.lstm(windows.unsqueeze(-1))
                return self.head(torch.cat([out[:, -1], calendar], dim=1)).squeeze(-1)

        return LSTMModel()

    if name == "TCN":

        class CausalBlock(nn.Module):
            def __init__(self, c_in: int, c_out: int, dilation: int) -> None:
                super().__init__()
                self.pad = 2 * dilation
                self.conv = nn.Conv1d(c_in, c_out, kernel_size=3, dilation=dilation)
                self.relu = nn.ReLU()
                self.res = nn.Conv1d(c_in, c_out, kernel_size=1) if c_in != c_out else nn.Identity()

            def forward(self, x):
                out = self.conv(nn.functional.pad(x, (self.pad, 0)))
                return self.relu(out + self.res(x))

        class TCN(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                blocks = []
                c_in = 1
                for dilation in (1, 2, 4, 8, 16, 32, 64):
                    blocks.append(CausalBlock(c_in, 32, dilation))
                    c_in = 32
                self.blocks = nn.Sequential(*blocks)
                self.head = nn.Linear(32 + 4, 1)

            def forward(self, windows, calendar):
                feat = self.blocks(windows.unsqueeze(1))[:, :, -1]
                return self.head(torch.cat([feat, calendar], dim=1)).squeeze(-1)

        return TCN()

    if name == "DLinear":

        class DLinear(nn.Module):
            def __init__(self, kernel: int = 25) -> None:
                super().__init__()
                self.kernel = kernel
                self.trend = nn.Linear(WINDOW, 1)
                self.seasonal = nn.Linear(WINDOW, 1)

            def forward(self, windows, calendar):
                pad_front = windows[:, :1].expand(-1, (self.kernel - 1) // 2)
                pad_back = windows[:, -1:].expand(-1, (self.kernel - 1) // 2)
                padded = torch.cat([pad_front, windows, pad_back], dim=1)
                trend = nn.functional.avg_pool1d(padded.unsqueeze(1), self.kernel, stride=1).squeeze(1)
                seasonal = windows - trend
                return (self.trend(trend) + self.seasonal(seasonal)).squeeze(-1)

        return DLinear()

    if name == "PatchTST-lite":

        class PatchTST(nn.Module):
            def __init__(self, patch: int = 16, stride: int = 8, dim: int = 64) -> None:
                super().__init__()
                self.patch = patch
                self.stride = stride
                self.n_patches = (WINDOW - patch) // stride + 1
                self.embed = nn.Linear(patch, dim)
                self.pos = nn.Parameter(torch.zeros(1, self.n_patches, dim))
                layer = nn.TransformerEncoderLayer(
                    d_model=dim, nhead=4, dim_feedforward=128, dropout=0.1, batch_first=True
                )
                self.encoder = nn.TransformerEncoder(layer, num_layers=2)
                self.head = nn.Linear(dim * self.n_patches + 4, 1)

            def forward(self, windows, calendar):
                patches = windows.unfold(1, self.patch, self.stride)
                tokens = self.embed(patches) + self.pos
                encoded = self.encoder(tokens).flatten(1)
                return self.head(torch.cat([encoded, calendar], dim=1)).squeeze(-1)

        return PatchTST()

    raise KeyError(name)


# ---------------------------------------------------------------------------
# Training / evaluation
# ---------------------------------------------------------------------------


def train_and_predict(
    model_name: str,
    epochs: int,
    seed: int,
    tensors: SeriesTensors,
    train: list[Sample],
    test: list[Sample],
    horizon: int,
) -> tuple[list[float], float]:
    import torch

    torch.manual_seed(seed)
    device = torch.device("cpu")
    train_strided = train[::TRAIN_STRIDE]
    # temporal early-stopping split: last 15% of the training window by time
    ts = sorted(s.t for s in train_strided)
    cutoff = ts[int(len(ts) * 0.85)]
    fit_samples = [s for s in train_strided if s.t < cutoff]
    val_samples = [s for s in train_strided if s.t >= cutoff]

    w_fit, c_fit, s_fit, y_fit = sample_tensors(fit_samples, tensors, horizon)
    w_val, c_val, _, y_val = sample_tensors(val_samples, tensors, horizon)
    w_test, c_test, s_test, _ = sample_tensors(test, tensors, horizon)

    model = make_model(model_name).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.MSELoss()

    start = time.perf_counter()
    best_val = float("inf")
    best_state = {k: v.clone() for k, v in model.state_dict().items()}
    n_fit = w_fit.shape[0]
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(n_fit)
        for i in range(0, n_fit, BATCH_SIZE):
            idx = perm[i : i + BATCH_SIZE]
            optimizer.zero_grad()
            loss = loss_fn(model(w_fit[idx], c_fit[idx]), y_fit[idx])
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = 0.0
            for i in range(0, w_val.shape[0], 4096):
                pred = model(w_val[i : i + 4096], c_val[i : i + 4096])
                val_loss += loss_fn(pred, y_val[i : i + 4096]).item() * pred.shape[0]
            val_loss /= max(1, w_val.shape[0])
        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        preds = []
        for i in range(0, w_test.shape[0], 4096):
            batch = model(w_test[i : i + 4096], c_test[i : i + 4096])
            preds.append(denormalize(batch, s_test[i : i + 4096], tensors))
        preds_full = torch.cat(preds)
    return preds_full.tolist(), time.perf_counter() - start


def run_dataset(dataset_key: str) -> list[dict[str, str]]:
    if dataset_key == "opsd":
        timestamps, series = parse_opsd()
        dataset_label = "OPSD time_series_60min_singleindex"
    else:
        timestamps, series = parse_simbench()
        dataset_label = "SimBench 1-complete_data-mixed-all-0-sw LoadProfile hourly pload"
    n = len(timestamps)
    train_end = int(n * 0.70)
    tensors = build_tensors(series, train_end)

    rows: list[dict[str, str]] = []
    for horizon in HORIZONS:
        train, test = samples_for(series, horizon=horizon, train_end=train_end)
        for model_name, description, epochs in MODEL_SPECS:
            for seed in SEEDS:
                preds, runtime = train_and_predict(model_name, epochs, seed, tensors, train, test, horizon)
                metrics = evaluate_predictions(test, preds)
                rows.append(
                    {
                        "dataset": dataset_label,
                        "horizon_hours": str(horizon),
                        "method": model_name,
                        "method_role": "baseline",
                        "seed": str(seed),
                        "epochs": str(epochs),
                        "mae": f"{metrics['mae']:.8f}",
                        "rmse": f"{metrics['rmse']:.8f}",
                        "mape": f"{metrics['mape']:.8f}",
                        "smape": f"{metrics['smape']:.8f}",
                        "normalized_mae": f"{metrics['normalized_mae']:.8f}",
                        "peak_load_error": f"{metrics['peak_load_error']:.8f}",
                        "runtime_s": f"{runtime:.4f}",
                        "train_samples": str(len(train[::TRAIN_STRIDE])),
                        "test_samples": str(len(test)),
                        "source_status": NEURAL_RUN_VERSION,
                    }
                )
            done = [r for r in rows if r["method"] == model_name and r["horizon_hours"] == str(horizon)][-3:]
            mapes = ", ".join(r["mape"] for r in done)
            print(f"[{dataset_key}] h{horizon} {model_name}: mape per seed = {mapes}")
    return rows


def median_seed_rows(neural_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """One row per (dataset, horizon, method): the seed with median test MAPE."""
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in neural_rows:
        grouped.setdefault((row["dataset"], row["horizon_hours"], row["method"]), []).append(row)
    output = []
    for group in grouped.values():
        ordered = sorted(group, key=lambda r: float(r["mape"]))
        median = ordered[len(ordered) // 2]
        mapes = [float(r["mape"]) for r in group]
        row = dict(median)
        row["mape_seed_std"] = f"{statistics.stdev(mapes):.8f}" if len(mapes) > 1 else "0"
        output.append(row)
    return output


def combined_leaderboard(dataset_key: str, neural_median: list[dict[str, str]]) -> list[dict[str, str]]:
    """Merge existing stdlib results with the neural median rows."""
    existing_path = P2_ROOT / "evidence" / "runs" / f"real_{dataset_key}_forecasting_results.csv"
    with existing_path.open(encoding="utf-8-sig", newline="") as handle:
        existing = list(csv.DictReader(handle))
    combined = []
    for row in existing:
        combined.append(
            {
                "horizon_hours": row["horizon_hours"],
                "method": row["method"],
                "method_role": row["method_role"],
                "family": "stdlib",
                "mape": row["mape"],
                "normalized_mae": row["normalized_mae"],
                "mae": row["mae"],
                "rmse": row["rmse"],
                "peak_load_error": row["peak_load_error"],
                "mape_seed_std": "",
            }
        )
    for row in neural_median:
        combined.append(
            {
                "horizon_hours": row["horizon_hours"],
                "method": row["method"],
                "method_role": "baseline",
                "family": "neural",
                "mape": row["mape"],
                "normalized_mae": row["normalized_mae"],
                "mae": row["mae"],
                "rmse": row["rmse"],
                "peak_load_error": row["peak_load_error"],
                "mape_seed_std": row["mape_seed_std"],
            }
        )
    return sorted(combined, key=lambda r: (int(r["horizon_hours"]), float(r["mape"])))


def analysis_markdown(boards: dict[str, list[dict[str, str]]]) -> str:
    lines = [
        "# Neural Baseline Analysis - P2 HyG-LoadFormer",
        "",
        f"Status: `{NEURAL_RUN_VERSION}`. Real neural baselines (MLP, LSTM, TCN, DLinear,",
        "PatchTST-lite) trained on exactly the same data, 70% temporal split, and full",
        "test sets as the stdlib benchmark; per-series z-normalization, Adam/MSE,",
        f"temporal early stopping, train-sample stride {TRAIN_STRIDE} (test never strided),",
        f"{len(SEEDS)} seeds per model with the median-MAPE seed reported and per-seed",
        "variance preserved in `real_*_neural_results.csv`.",
        "",
    ]
    for dataset_key, board in boards.items():
        metric = "normalized_mae" if dataset_key == "simbench" else "mape"
        metric_label = "normalized MAE" if dataset_key == "simbench" else "MAPE"
        lines.append(f"## {dataset_key.upper()} (ranking metric: {metric_label})")
        lines.append("")
        for horizon in sorted({r["horizon_hours"] for r in board}, key=int):
            group = [r for r in board if r["horizon_hours"] == horizon]
            group_sorted = sorted(group, key=lambda r: float(r[metric]))
            proposed = next(r for r in group if r["method"] == "HyG-LoadFormer")
            neural = [r for r in group if r["family"] == "neural"]
            best_neural = min(neural, key=lambda r: float(r[metric]))
            proposed_rank = 1 + next(i for i, r in enumerate(group_sorted) if r["method"] == "HyG-LoadFormer")
            gain = (float(best_neural[metric]) / float(proposed[metric]) - 1.0) * 100
            verdict = "proposed_beats_all_neural" if gain > 0 else "neural_baseline_beats_proposed"
            lines.extend(
                [
                    f"### Horizon {horizon}h",
                    "",
                    f"- HyG-LoadFormer {metric_label}: `{proposed[metric]}` (rank {proposed_rank}/{len(group_sorted)})",
                    f"- Best neural baseline: `{best_neural['method']}` with `{best_neural[metric]}` (seed-std MAPE `{best_neural['mape_seed_std']}`)",
                    f"- HyG-LoadFormer margin over best neural baseline: `{gain:.2f}%` ({verdict})",
                    "",
                    "| rank | method | family | MAPE | normalized MAE |",
                    "|---|---|---|---|---|",
                ]
            )
            for i, row in enumerate(group_sorted[:10], start=1):
                lines.append(
                    f"| {i} | {row['method']} | {row['family']} | {row['mape']} | {row['normalized_mae']} |"
                )
            lines.append("")
    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "Neural baselines are compact CPU-trained models (bounded epochs, strided",
            "training samples); a GPU-tuned version of each could be somewhat stronger, and",
            "this is stated as a limitation rather than hidden. Test sets are identical to",
            "the stdlib benchmark rows, so the combined leaderboards are directly",
            "comparable. Rolling-split neural evidence is limited to what these budgets",
            "allow and remains an open extension.",
            "",
            "## Consequence for the manuscript claim",
            "",
            "If HyG-LoadFormer (currently a ridge-based implementation) does not beat the",
            "neural baselines on the 24h day-ahead task, the manuscript must either (a)",
            "upgrade the proposed method to a genuine neural implementation before claiming",
            "state-of-the-art-adjacent performance, or (b) reframe the contribution as an",
            "interpretable lightweight method and report the neural baselines honestly as",
            "an upper reference. Silent omission is not an option.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    out_dir = P2_ROOT / "evidence" / "runs"
    table_dir = P2_ROOT / "evidence" / "tables"
    config_dir = P2_ROOT / "src" / "configs"
    boards: dict[str, list[dict[str, str]]] = {}
    for dataset_key in ("opsd", "simbench"):
        rows = run_dataset(dataset_key)
        write_csv(out_dir / f"real_{dataset_key}_neural_results.csv", rows)
        median_rows = median_seed_rows(rows)
        board = combined_leaderboard(dataset_key, median_rows)
        write_csv(table_dir / f"real_{dataset_key}_combined_leaderboard.csv", board)
        boards[dataset_key] = board
    (out_dir / "real_neural_baselines_analysis.md").write_text(analysis_markdown(boards), encoding="utf-8")
    import torch

    (config_dir / "real_neural_config.json").write_text(
        json.dumps(
            {
                "models": {name: {"description": desc, "epochs": epochs} for name, desc, epochs in MODEL_SPECS},
                "window_hours": WINDOW,
                "train_stride": TRAIN_STRIDE,
                "batch_size": BATCH_SIZE,
                "seeds": SEEDS,
                "optimizer": "Adam lr=1e-3, MSE on per-series z-normalized target",
                "early_stopping": "last 15% of training window by time, best-val state restored",
                "test_protocol": "identical splits and full test sets as real_load_forecasting stdlib rows",
                "torch_version": torch.__version__,
                "device": "cpu",
                "status": NEURAL_RUN_VERSION,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("neural baselines complete")


if __name__ == "__main__":
    main()
