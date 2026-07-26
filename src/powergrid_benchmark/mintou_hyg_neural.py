"""Neural HyG-LoadFormer for mintou p2: the real implementation of the method.

The previous "HyG-LoadFormer" was a ridge regression over hand-built
hyperbolic-weighted features; the neural-baseline benchmark
(`mintou_neural_forecasting.py`) showed a plain MLP beats it in every setting,
so the method is upgraded to a genuine neural implementation whose components
match the ARA claims one-to-one:

- Shared temporal encoder phi: per-series window MLP 168 -> 96 -> 48 (kept at
  MLP-baseline-class parameter budget for a fair comparison).
- Hyperbolic graph attention: each series holds a learnable Poincare-ball
  embedding; the TARGET series holds a learnable adaptive curvature
  c_i = softplus(kappa_i) ("target-adaptive curvature"); attention from target
  i to neighbor j is softmax_j(-c_i * d_H(e_i, e_j)) over the Poincare distance
  d_H, and aggregates the neighbors' temporal encodings through a value map.
- Head: concat[phi(target window), graph aggregate, calendar] -> 64 -> 1.

Ablations are real mechanism switches on this model:
  Ablation-EuclideanGraph  : Euclidean embedding distance instead of Poincare
  Ablation-FixedCurvature  : c_i frozen at 1 (not learnable)
  Ablation-TemporalOnly    : graph aggregate removed from the head
  Ablation-NoCalendar      : calendar features removed from the head
  Ablation-EqualNeighbors  : uniform attention weights

Protocol is IDENTICAL to the neural baselines: same parse/splits/test sets
imported from `mintou_real_load_forecasting`, per-series z-normalization,
Adam 1e-3 / MSE, batch 512, train-sample stride 3 (test untouched), temporal
early stopping, 3 seeds with per-seed rows preserved and the median-MAPE seed
as headline. Outputs regenerate the combined leaderboards.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT / "src"))

from powergrid_benchmark.mintou_neural_forecasting import (  # noqa: E402
    BATCH_SIZE,
    SEEDS,
    TRAIN_STRIDE,
    WINDOW,
    SeriesTensors,
    build_tensors,
    denormalize,
)
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

HYG_RUN_VERSION = "public_data_benchmark_v6_hyg_neural"
EPOCHS = 15
ENCODER_DIM = 48
EMBED_DIM = 8

VARIANTS = (
    ("HyG-LoadFormer (neural)", "proposed", {}),
    ("Ablation-EuclideanGraph (neural)", "ablation", {"euclidean": True}),
    ("Ablation-FixedCurvature (neural)", "ablation", {"fixed_curvature": True}),
    ("Ablation-TemporalOnly (neural)", "ablation", {"no_graph": True}),
    ("Ablation-NoCalendar (neural)", "ablation", {"no_calendar": True}),
    ("Ablation-EqualNeighbors (neural)", "ablation", {"equal_neighbors": True}),
)


# ---------------------------------------------------------------------------
# Batched inputs: all-series windows per sample
# ---------------------------------------------------------------------------


def multi_series_tensors(samples: list[Sample], tensors: SeriesTensors, horizon: int):
    """All-series windows [N, S, WINDOW], calendar [N, 4], target index [N],
    normalized target [N]."""
    import torch

    index = {name: i for i, name in enumerate(tensors.names)}
    sidx = torch.tensor([index[s.country] for s in samples], dtype=torch.long)
    t_idx = torch.tensor([s.t for s in samples], dtype=torch.long)
    offsets = torch.arange(-WINDOW + 1, 1)
    gather_idx = t_idx[:, None] + offsets[None, :]  # [N, W]
    windows = tensors.norm[:, gather_idx].permute(1, 0, 2)  # [N, S, W]
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


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


def make_hyg_model(n_series: int, variant: dict):
    import torch
    from torch import nn

    class HyGLoadFormer(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.euclidean = bool(variant.get("euclidean"))
            self.fixed_curvature = bool(variant.get("fixed_curvature"))
            self.no_graph = bool(variant.get("no_graph"))
            self.no_calendar = bool(variant.get("no_calendar"))
            self.equal_neighbors = bool(variant.get("equal_neighbors"))
            self.encoder = nn.Sequential(
                nn.Linear(WINDOW, 96), nn.ReLU(), nn.Linear(96, ENCODER_DIM), nn.ReLU()
            )
            self.embed_raw = nn.Parameter(torch.randn(n_series, EMBED_DIM) * 0.2)
            self.kappa = nn.Parameter(torch.zeros(n_series))
            self.value = nn.Linear(ENCODER_DIM, ENCODER_DIM)
            head_in = ENCODER_DIM + (0 if self.no_graph else ENCODER_DIM) + (0 if self.no_calendar else 4)
            self.head = nn.Sequential(nn.Linear(head_in, 64), nn.ReLU(), nn.Linear(64, 1))

        def poincare_embed(self):
            # map raw parameters into the open unit ball (max norm 0.95)
            norm = self.embed_raw.norm(dim=1, keepdim=True).clamp_min(1e-6)
            return self.embed_raw / norm * 0.95 * torch.tanh(norm)

        def pairwise_distance(self):
            e = self.poincare_embed()  # [S, D]
            if self.euclidean:
                return torch.cdist(e, e)
            sq = torch.cdist(e, e).pow(2)
            denom = (1.0 - e.pow(2).sum(dim=1)).clamp_min(1e-6)
            arg = 1.0 + 2.0 * sq / (denom[:, None] * denom[None, :])
            return torch.acosh(arg.clamp_min(1.0 + 1e-7))

        def forward(self, windows, calendar, sidx):
            n, s, _ = windows.shape
            encoded = self.encoder(windows)  # [N, S, D]
            target_enc = encoded[torch.arange(n), sidx]  # [N, D]
            parts = [target_enc]
            if not self.no_graph:
                dist = self.pairwise_distance()  # [S, S]
                if self.fixed_curvature:
                    curvature = torch.ones_like(self.kappa)
                else:
                    curvature = torch.nn.functional.softplus(self.kappa) + 0.1
                scores = -curvature[:, None] * dist  # [S, S] row = target series
                eye = torch.eye(s, dtype=torch.bool, device=windows.device)
                scores = scores.masked_fill(eye, float("-inf"))
                if self.equal_neighbors:
                    attn = torch.full((s, s), 1.0 / max(1, s - 1), device=windows.device)
                    attn = attn.masked_fill(eye, 0.0)
                else:
                    attn = torch.softmax(scores, dim=1)  # [S, S]
                sample_attn = attn[sidx]  # [N, S]
                aggregate = torch.bmm(sample_attn.unsqueeze(1), self.value(encoded)).squeeze(1)
                parts.append(aggregate)
            if not self.no_calendar:
                parts.append(calendar)
            return self.head(torch.cat(parts, dim=1)).squeeze(-1)

    return HyGLoadFormer()


# ---------------------------------------------------------------------------
# Training (identical regime to the neural baselines)
# ---------------------------------------------------------------------------


def train_and_predict(
    variant: dict,
    seed: int,
    tensors: SeriesTensors,
    train: list[Sample],
    test: list[Sample],
    horizon: int,
) -> tuple[list[float], float]:
    import torch

    torch.manual_seed(seed)
    train_strided = train[::TRAIN_STRIDE]
    ts = sorted(s.t for s in train_strided)
    cutoff = ts[int(len(ts) * 0.85)]
    fit_samples = [s for s in train_strided if s.t < cutoff]
    val_samples = [s for s in train_strided if s.t >= cutoff]

    w_fit, c_fit, s_fit, y_fit = multi_series_tensors(fit_samples, tensors, horizon)
    w_val, c_val, s_val, y_val = multi_series_tensors(val_samples, tensors, horizon)
    w_test, c_test, s_test, _ = multi_series_tensors(test, tensors, horizon)

    model = make_hyg_model(len(tensors.names), variant)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.MSELoss()

    start = time.perf_counter()
    best_val = float("inf")
    best_state = {k: v.clone() for k, v in model.state_dict().items()}
    n_fit = w_fit.shape[0]
    for _ in range(EPOCHS):
        model.train()
        perm = torch.randperm(n_fit)
        for i in range(0, n_fit, BATCH_SIZE):
            idx = perm[i : i + BATCH_SIZE]
            optimizer.zero_grad()
            loss = loss_fn(model(w_fit[idx], c_fit[idx], s_fit[idx]), y_fit[idx])
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = 0.0
            for i in range(0, w_val.shape[0], 2048):
                pred = model(w_val[i : i + 2048], c_val[i : i + 2048], s_val[i : i + 2048])
                val_loss += loss_fn(pred, y_val[i : i + 2048]).item() * pred.shape[0]
            val_loss /= max(1, w_val.shape[0])
        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        preds = []
        for i in range(0, w_test.shape[0], 2048):
            batch = model(w_test[i : i + 2048], c_test[i : i + 2048], s_test[i : i + 2048])
            preds.append(denormalize(batch, s_test[i : i + 2048], tensors))
        preds_full = torch.cat(preds)
    return preds_full.tolist(), time.perf_counter() - start


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


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
        for name, role, variant in VARIANTS:
            for seed in SEEDS:
                preds, runtime = train_and_predict(variant, seed, tensors, train, test, horizon)
                metrics = evaluate_predictions(test, preds)
                rows.append(
                    {
                        "dataset": dataset_label,
                        "horizon_hours": str(horizon),
                        "method": name,
                        "method_role": role,
                        "seed": str(seed),
                        "epochs": str(EPOCHS),
                        "mae": f"{metrics['mae']:.8f}",
                        "rmse": f"{metrics['rmse']:.8f}",
                        "mape": f"{metrics['mape']:.8f}",
                        "smape": f"{metrics['smape']:.8f}",
                        "normalized_mae": f"{metrics['normalized_mae']:.8f}",
                        "peak_load_error": f"{metrics['peak_load_error']:.8f}",
                        "runtime_s": f"{runtime:.4f}",
                        "train_samples": str(len(train[::TRAIN_STRIDE])),
                        "test_samples": str(len(test)),
                        "source_status": HYG_RUN_VERSION,
                    }
                )
            done = [r for r in rows if r["method"] == name and r["horizon_hours"] == str(horizon)][-3:]
            print(f"[{dataset_key}] h{horizon} {name}: mape per seed = {', '.join(r['mape'] for r in done)}")
    return rows


def median_seed_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["dataset"], row["horizon_hours"], row["method"]), []).append(row)
    output = []
    for group in grouped.values():
        ordered = sorted(group, key=lambda r: float(r["mape"]))
        median = dict(ordered[len(ordered) // 2])
        mapes = [float(r["mape"]) for r in group]
        median["mape_seed_std"] = f"{statistics.stdev(mapes):.8f}" if len(mapes) > 1 else "0"
        output.append(median)
    return output


def rebuild_combined_leaderboard(dataset_key: str, hyg_median: list[dict[str, str]]) -> list[dict[str, str]]:
    """stdlib rows + neural-baseline median rows + neural HyG rows."""
    runs_dir = P2_ROOT / "evidence" / "runs"

    def read(path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    combined: list[dict[str, str]] = []
    for row in read(runs_dir / f"real_{dataset_key}_forecasting_results.csv"):
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
    neural_rows = read(runs_dir / f"real_{dataset_key}_neural_results.csv")
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in neural_rows:
        grouped.setdefault((row["horizon_hours"], row["method"]), []).append(row)
    for (_, _), group in grouped.items():
        ordered = sorted(group, key=lambda r: float(r["mape"]))
        median = ordered[len(ordered) // 2]
        mapes = [float(r["mape"]) for r in group]
        combined.append(
            {
                "horizon_hours": median["horizon_hours"],
                "method": median["method"],
                "method_role": "baseline",
                "family": "neural",
                "mape": median["mape"],
                "normalized_mae": median["normalized_mae"],
                "mae": median["mae"],
                "rmse": median["rmse"],
                "peak_load_error": median["peak_load_error"],
                "mape_seed_std": f"{statistics.stdev(mapes):.8f}" if len(mapes) > 1 else "0",
            }
        )
    for row in hyg_median:
        combined.append(
            {
                "horizon_hours": row["horizon_hours"],
                "method": row["method"],
                "method_role": row["method_role"],
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
        "# HyG-LoadFormer Neural Upgrade Analysis - P2",
        "",
        f"Status: `{HYG_RUN_VERSION}`. The proposed method is now a genuine neural",
        "implementation (Poincare-ball series embeddings, target-adaptive curvature",
        "hyperbolic graph attention, shared temporal MLP encoder at MLP-baseline",
        "parameter budget). Protocol identical to the neural baselines: same splits,",
        f"full test sets, Adam/MSE, temporal early stopping, {len(SEEDS)} seeds",
        "(median-MAPE seed reported; per-seed rows preserved in",
        "`real_*_hyg_neural_results.csv`). The five ablations are real mechanism",
        "switches on this model. The previous ridge implementation stays in the",
        "leaderboards as `HyG-LoadFormer` (stdlib family) for transparency.",
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
            proposed = next(r for r in group if r["method"] == "HyG-LoadFormer (neural)")
            rank = 1 + next(i for i, r in enumerate(group_sorted) if r["method"] == "HyG-LoadFormer (neural)")
            baselines = [r for r in group if r["method_role"] == "baseline"]
            best_baseline = min(baselines, key=lambda r: float(r[metric]))
            ablations = [r for r in group if "(neural)" in r["method"] and r["method_role"] == "ablation"]
            best_ablation = min(ablations, key=lambda r: float(r[metric])) if ablations else None
            gain_baseline = (float(best_baseline[metric]) / float(proposed[metric]) - 1.0) * 100
            verdict = "proposed_beats_all_baselines" if gain_baseline > 0 else "baseline_beats_proposed"
            lines.extend(
                [
                    f"### Horizon {horizon}h",
                    "",
                    f"- HyG-LoadFormer (neural) {metric_label}: `{proposed[metric]}` (rank {rank}/{len(group_sorted)}, seed-std MAPE `{proposed['mape_seed_std']}`)",
                    f"- Best baseline: `{best_baseline['method']}` ({best_baseline['family']}) with `{best_baseline[metric]}`",
                    f"- Margin over best baseline: `{gain_baseline:.2f}%` ({verdict})",
                ]
            )
            if best_ablation is not None:
                gain_ablation = (float(best_ablation[metric]) / float(proposed[metric]) - 1.0) * 100
                lines.append(
                    f"- Best neural ablation: `{best_ablation['method']}` with `{best_ablation[metric]}` (margin `{gain_ablation:.2f}%`)"
                )
            lines.extend(["", "| rank | method | family | MAPE | normalized MAE |", "|---|---|---|---|---|"])
            for i, row in enumerate(group_sorted[:12], start=1):
                lines.append(
                    f"| {i} | {row['method']} | {row['family']} | {row['mape']} | {row['normalized_mae']} |"
                )
            lines.append("")
    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "All neural models (proposed, ablations, baselines) share the same CPU training",
            "budget class, optimizer, early-stopping rule, and test sets, so rankings are",
            "internally fair; absolute numbers are not GPU-tuned SOTA. Per-seed variance is",
            "preserved. The ridge-based rows remain visible as the stdlib family.",
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
        write_csv(out_dir / f"real_{dataset_key}_hyg_neural_results.csv", rows)
        board = rebuild_combined_leaderboard(dataset_key, median_seed_rows(rows))
        write_csv(table_dir / f"real_{dataset_key}_combined_leaderboard.csv", board)
        boards[dataset_key] = board
    (out_dir / "real_hyg_neural_upgrade_analysis.md").write_text(analysis_markdown(boards), encoding="utf-8")
    import torch

    (config_dir / "real_hyg_neural_config.json").write_text(
        json.dumps(
            {
                "variants": {name: variant for name, _, variant in VARIANTS},
                "encoder": f"shared MLP {WINDOW}->96->{ENCODER_DIM}",
                "graph": "Poincare-ball embeddings dim 8, target-adaptive curvature softplus(kappa)+0.1, softmax(-c_i * d_H) attention, linear value map",
                "head": "concat[target_enc, graph_agg, calendar] -> 64 -> 1",
                "epochs": EPOCHS,
                "train_stride": TRAIN_STRIDE,
                "batch_size": BATCH_SIZE,
                "seeds": SEEDS,
                "optimizer": "Adam lr=1e-3, MSE on per-series z-normalized target",
                "early_stopping": "last 15% of training window by time, best-val state restored",
                "test_protocol": "identical splits and full test sets as stdlib and neural-baseline rows",
                "torch_version": torch.__version__,
                "device": "cpu",
                "status": HYG_RUN_VERSION,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("hyg neural upgrade complete")


if __name__ == "__main__":
    main()
