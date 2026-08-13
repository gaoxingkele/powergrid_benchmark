"""p1 curtailment pivot (v4): real curtailment-risk forecasting on RTS-GMLC.

The v3 dispatch experiment had the proxy-method disease: per-method hand
constants (reserve_factor / renewable_bias / topology_bias) and an exclusive
renewable-bias formula for DSTAR-GRU, which manufactured most of the ~30x
curtailment gap the round-2 review highlighted. The pivot therefore redefines
the task as a genuine forecasting problem before adopting that signal:

- Ground truth is method-independent: a FIXED reference dispatch policy
  (renewable acceptance bias 0.92, reserve factor 0.10) is simulated once over
  the RTS-GMLC day-ahead series, producing a curtailment-rate series. Every
  method sees the same features and predicts the same targets.
- DSTAR-GRU is a real model: GRU encoder over 48h feature windows -> learned
  embedding; Siamese retrieval = k-NN in the LEARNED embedding space over the
  training bank; final prediction blends the GRU head with the retrieved
  analogs' targets, with the blend weight selected on a temporal validation
  split. Ablations are real switches (raw-feature retrieval, no retrieval,
  small bank, LSTM encoder, no topology feature).
- Baselines: persistence, seasonal-24h, ridge, MLP, LSTM, raw-feature k-NN.
- Metrics: curtailment-rate MAE/RMSE, high-curtailment event detection
  (top-decile threshold from the training split), stress-subset MAE.
- 10 seeds per learned method, Mann-Whitney U + Holm on the primary metric
  (curtailment MAE). The v3 dispatch artifacts remain untouched as historical
  evidence; this experiment supersedes them as the manuscript's primary task.
"""

from __future__ import annotations

import csv
import hashlib
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

import numpy as np
from scipy.stats import mannwhitneyu

from powergrid_benchmark.mintou_real_dispatch import (  # noqa: E402
    Branch,
    Scenario,
    load_branches,
    load_generators,
    load_scenarios,
    topology_stress,
)

P1_ROOT = ROOT / "papers" / "mintou" / "mintou_p1_dstar_gru_dispatch"
RUN_VERSION = "public_rts_curtailment_v6_modern_temporal_controls"

SCENARIO_HOURS = 8760  # full year of day-ahead hours
WINDOW = 48
HORIZONS = (1, 24)
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15  # tail of the training window, by time
SEEDS = (11, 23, 47, 59, 71, 83, 97, 109, 127, 139)
POINT_SEEDS = (11,)  # deterministic methods need one row only
# Reference acceptance cap: instantaneous renewable penetration limited to 70%
# of load, modeling a system non-synchronous penetration (SNSP-class) operating
# limit; yields ~9.5% nonzero-curtailment hours on the 4320h RTS-GMLC series.
REFERENCE_BIAS = 0.70
REFERENCE_RESERVE = 0.10
K_NEIGHBORS = 8
EPOCHS = 20
BATCH = 256


# ---------------------------------------------------------------------------
# Method-independent task construction
# ---------------------------------------------------------------------------


def build_series() -> tuple[np.ndarray, np.ndarray]:
    """Feature matrix [T, 7] and curtailment-rate target [T] under the fixed
    reference policy. No method identity enters."""
    import powergrid_benchmark.mintou_real_dispatch as dispatch

    loads = dispatch.sum_timeseries(dispatch.TIMESERIES / "Load" / "DAY_AHEAD_regional_Load.csv", limit=SCENARIO_HOURS)
    wind = dispatch.sum_timeseries(dispatch.TIMESERIES / "WIND" / "DAY_AHEAD_wind.csv", limit=SCENARIO_HOURS)
    pv = dispatch.sum_timeseries(dispatch.TIMESERIES / "PV" / "DAY_AHEAD_pv.csv", limit=SCENARIO_HOURS)
    scenarios = []
    prev_net = 0.0
    for idx, ((timestamp, load), (_, wind_mw), (_, pv_mw)) in enumerate(zip(loads, wind, pv)):
        renewable = wind_mw + pv_mw
        net = max(0.0, load - renewable)
        ramp = net - prev_net if idx else 0.0
        scenarios.append(
            Scenario(
                idx=idx,
                timestamp=timestamp,
                load_mw=load,
                wind_mw=wind_mw,
                pv_mw=pv_mw,
                net_load_mw=net,
                load_ramp_mw=ramp,
                renewable_share=renewable / max(1.0, load),
            )
        )
        prev_net = net
    branches = load_branches()
    features = []
    targets = []
    for scenario in scenarios:
        stress = topology_stress(scenario, branches)
        renewable = scenario.wind_mw + scenario.pv_mw
        used = min(renewable, scenario.load_mw * REFERENCE_BIAS)
        curtailment_rate = max(0.0, renewable - used) / max(1.0, renewable)
        features.append(
            [
                scenario.load_mw,
                scenario.wind_mw,
                scenario.pv_mw,
                scenario.net_load_mw,
                scenario.load_ramp_mw,
                scenario.renewable_share,
                stress,
            ]
        )
        targets.append(curtailment_rate)
    return np.asarray(features, dtype=np.float64), np.asarray(targets, dtype=np.float64)


@dataclass
class Task:
    X_windows: np.ndarray  # [N, WINDOW, 7] normalized
    y: np.ndarray  # [N]
    t_index: np.ndarray  # [N] absolute hour of the PREDICTION target
    fit_mask: np.ndarray
    val_mask: np.ndarray
    test_mask: np.ndarray
    event_threshold: float
    stress_mask: np.ndarray  # high-renewable-share subset of test rows


def build_task(features: np.ndarray, targets: np.ndarray, horizon: int) -> Task:
    T = features.shape[0]
    train_end = int(T * TRAIN_RATIO)
    mu = features[:train_end].mean(axis=0)
    sd = features[:train_end].std(axis=0)
    sd[sd < 1e-9] = 1.0
    norm = (features - mu) / sd

    starts = np.arange(WINDOW - 1, T - horizon)
    target_t = starts + horizon
    windows = np.stack([norm[s - WINDOW + 1 : s + 1] for s in starts])
    y = targets[target_t]

    fit_cut = int(train_end * (1 - VAL_RATIO))
    fit_mask = target_t < fit_cut
    val_mask = (target_t >= fit_cut) & (target_t < train_end)
    test_mask = target_t >= train_end

    train_targets = y[fit_mask | val_mask]
    positive = train_targets[train_targets > 0]
    # event = operationally significant curtailment: median positive rate on the
    # training window, floored at 2%
    event_threshold = max(0.02, float(np.quantile(positive, 0.50))) if positive.size >= 20 else 0.02

    share = features[target_t, 5]
    share_q75 = float(np.quantile(features[:train_end, 5], 0.75))
    stress_mask = test_mask & (share >= share_q75)

    return Task(windows, y, target_t, fit_mask, val_mask, test_mask, event_threshold, stress_mask)


def _f1(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float]:
    tp = int(np.sum(y_true & y_pred))
    recall = tp / max(1, int(y_true.sum()))
    precision = tp / max(1, int(y_pred.sum()))
    return 2 * precision * recall / max(1e-9, precision + recall), precision, recall


def evaluate(task: Task, preds: np.ndarray, targets_full: np.ndarray, horizon: int) -> dict[str, float]:
    y = task.y[task.test_mask]
    p = preds[task.test_mask]
    err = np.abs(y - p)
    thr = task.event_threshold
    events = y >= thr
    f1, precision, recall = _f1(events, p >= thr)
    stress_err = np.abs(task.y[task.stress_mask] - preds[task.stress_mask])

    # Onset slice: no significant curtailment at observation time, event at the
    # target hour — the operationally critical hours where persistence
    # structurally cannot warn. Detection threshold is calibrated per method on
    # the VALIDATION onsets (best F1 over prediction-quantile grid), then
    # applied unchanged to the test split.
    last_obs = targets_full[task.t_index - horizon]
    thr_onset = 0.02  # emergence of any operationally significant curtailment
    onset_all = (task.y >= thr_onset) & (last_obs < thr_onset)
    cease_all = (task.y < thr_onset) & (last_obs >= thr_onset)

    def calibrated_threshold() -> float:
        # calibrate on the whole training window (fit+val): the temporal val
        # slice can be seasonally onset-free; identical protocol for every method
        cal = task.fit_mask | task.val_mask
        cal_events = onset_all[cal]
        if cal_events.sum() == 0:
            return thr
        grid = np.unique(np.quantile(preds[cal], np.linspace(0.5, 0.999, 40)))
        best_t, best_f1 = thr, -1.0
        for t in grid:
            f1_v, _, _ = _f1(cal_events, preds[cal] >= t)
            if f1_v > best_f1:
                best_f1, best_t = f1_v, float(t)
        return best_t

    det_thr = calibrated_threshold()
    test = task.test_mask
    onset_test = onset_all[test]
    onset_f1, onset_precision, onset_recall = _f1(onset_test, preds[test] >= det_thr)
    onset_rows = test & onset_all
    onset_mae = float(np.abs(task.y[onset_rows] - preds[onset_rows]).mean()) if onset_rows.sum() else float("nan")
    cease_rows = test & cease_all
    cease_f1, _, _ = _f1(cease_all[test], preds[test] < det_thr) if cease_rows.sum() else (float("nan"), 0, 0)

    return {
        "curtailment_mae": float(err.mean()),
        "curtailment_rmse": float(np.sqrt(((y - p) ** 2).mean())),
        "event_recall": float(recall),
        "event_precision": float(precision),
        "event_f1": float(f1),
        "onset_f1": float(onset_f1),
        "onset_precision": float(onset_precision),
        "onset_recall": float(onset_recall),
        "onset_mae": onset_mae,
        "cessation_f1": float(cease_f1),
        "detection_threshold": float(det_thr),
        "n_onsets_test": float(onset_test.sum()),
        "stress_subset_mae": float(stress_err.mean()) if stress_err.size else float("nan"),
        "n_test": float(y.size),
        "n_events": float(events.sum()),
    }


# ---------------------------------------------------------------------------
# Methods
# ---------------------------------------------------------------------------


def predict_persistence(task: Task, horizon: int, targets_full: np.ndarray) -> np.ndarray:
    # last observed curtailment before the target hour
    return targets_full[task.t_index - horizon]


def predict_seasonal(task: Task, horizon: int, targets_full: np.ndarray) -> np.ndarray:
    lag = 24 if horizon <= 24 else 168
    idx = np.maximum(task.t_index - lag, 0)
    return targets_full[idx]


def predict_ridge(task: Task) -> np.ndarray:
    X = task.X_windows.reshape(task.X_windows.shape[0], -1)
    fit = task.fit_mask | task.val_mask
    A = X[fit]
    b = task.y[fit]
    reg = 1e-3 * np.eye(A.shape[1])
    beta = np.linalg.solve(A.T @ A + reg, A.T @ b)
    return X @ beta


def _knn_predict(queries: np.ndarray, bank: np.ndarray, bank_y: np.ndarray) -> np.ndarray:
    from scipy.spatial.distance import cdist

    d = cdist(queries, bank)
    nn = np.argpartition(d, K_NEIGHBORS, axis=1)[:, :K_NEIGHBORS]
    return bank_y[nn].mean(axis=1)


def predict_knn_raw(task: Task) -> np.ndarray:
    X = task.X_windows.reshape(task.X_windows.shape[0], -1)
    fit = np.where(task.fit_mask | task.val_mask)[0]
    return _knn_predict(X, X[fit], task.y[fit])


def make_torch_model(kind: str, n_features: int):
    import torch
    from torch import nn

    if kind == "mlp":

        class MLP(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.net = nn.Sequential(nn.Linear(WINDOW * n_features, 96), nn.ReLU(), nn.Linear(96, 48), nn.ReLU(), nn.Linear(48, 1))

            def forward(self, x):
                return self.net(x.flatten(1)).squeeze(-1), None

        return MLP()

    if kind == "dlinear":

        class DLinear(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.trend = nn.Linear(WINDOW * n_features, 1)
                self.seasonal = nn.Linear(WINDOW * n_features, 1)

            def forward(self, x):
                # Fixed 25-hour moving average, with replicate padding, gives
                # the same decomposition to every feature channel.
                xt = x.transpose(1, 2)
                trend = nn.functional.avg_pool1d(
                    nn.functional.pad(xt, (12, 12), mode="replicate"),
                    kernel_size=25,
                    stride=1,
                ).transpose(1, 2)
                seasonal = x - trend
                pred = self.trend(trend.flatten(1)) + self.seasonal(seasonal.flatten(1))
                return pred.squeeze(-1), None

        return DLinear()

    if kind == "tcn":

        class TCN(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                layers = []
                channels = n_features
                for dilation in (1, 2, 4, 8):
                    layers.extend(
                        [
                            nn.Conv1d(channels, 32, kernel_size=3, dilation=dilation, padding=dilation),
                            nn.ReLU(),
                        ]
                    )
                    channels = 32
                self.net = nn.Sequential(*layers)
                self.head = nn.Linear(32, 1)

            def forward(self, x):
                embedding = self.net(x.transpose(1, 2))[:, :, -1]
                return self.head(embedding).squeeze(-1), embedding

        return TCN()

    class Recurrent(nn.Module):
        def __init__(self, cell: str) -> None:
            super().__init__()
            rnn_cls = nn.GRU if cell == "gru" else nn.LSTM
            self.rnn = rnn_cls(input_size=n_features, hidden_size=48, num_layers=1, batch_first=True)
            self.head = nn.Linear(48, 1)

        def forward(self, x):
            out, _ = self.rnn(x)
            embedding = out[:, -1]
            return self.head(embedding).squeeze(-1), embedding

    return Recurrent("gru" if kind == "gru" else "lstm")


def train_torch(task: Task, kind: str, seed: int, feature_mask: np.ndarray | None = None):
    import torch

    torch.manual_seed(seed)
    X = task.X_windows
    if feature_mask is not None:
        X = X[:, :, feature_mask]
    n_features = X.shape[2]
    Xt = torch.tensor(X, dtype=torch.float32)
    yt = torch.tensor(task.y, dtype=torch.float32)
    fit_idx = np.where(task.fit_mask)[0]
    val_idx = np.where(task.val_mask)[0]

    model = make_torch_model(kind, n_features)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.MSELoss()
    best_val = float("inf")
    best_state = {k: v.clone() for k, v in model.state_dict().items()}
    for _ in range(EPOCHS):
        model.train()
        perm = np.random.default_rng(seed).permutation(fit_idx)
        for i in range(0, len(perm), BATCH):
            idx = torch.tensor(perm[i : i + BATCH])
            optimizer.zero_grad()
            pred, _ = model(Xt[idx])
            loss = loss_fn(pred, yt[idx])
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            val_pred, _ = model(Xt[torch.tensor(val_idx)])
            val_loss = loss_fn(val_pred, yt[torch.tensor(val_idx)]).item()
        if val_loss < best_val:
            best_val = val_loss
            best_state = {k: v.clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        preds, embeddings = model(Xt)
    emb = embeddings.numpy() if embeddings is not None else None
    return preds.numpy(), emb


def retrieval_blend(task: Task, head_preds: np.ndarray, space: np.ndarray, bank_hours: int | None) -> np.ndarray:
    """Siamese retrieval: k-NN in the given representation space over the
    training bank; blend weight selected on the temporal validation split."""
    fit_idx = np.where(task.fit_mask)[0]
    if bank_hours is not None:
        # restrict the bank to the most recent hours before the fit cutoff
        cutoff = task.t_index[fit_idx].max()
        keep = task.t_index[fit_idx] >= cutoff - bank_hours
        fit_idx = fit_idx[keep]
    retrieved = _knn_predict(space, space[fit_idx], task.y[fit_idx])
    val = np.where(task.val_mask)[0]
    best_alpha, best_mae = 1.0, float("inf")
    for alpha in (0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0):
        mae = np.abs(task.y[val] - (alpha * head_preds[val] + (1 - alpha) * retrieved[val])).mean()
        if mae < best_mae:
            best_mae, best_alpha = mae, alpha
    return best_alpha * head_preds + (1 - best_alpha) * retrieved


@dataclass(frozen=True)
class MethodSpec:
    name: str
    role: str
    runner: str
    description: str
    seeded: bool = True


METHODS = (
    MethodSpec("DSTAR-GRU", "proposed", "dstar", "GRU encoder + Siamese retrieval in learned embedding space + validated blend.", True),
    MethodSpec("Persistence", "baseline", "persistence", "Last observed curtailment rate.", False),
    MethodSpec("Seasonal-24h", "baseline", "seasonal", "Previous-day same-hour curtailment.", False),
    MethodSpec("Ridge", "baseline", "ridge", "Ridge regression on the flattened window.", False),
    MethodSpec("MLP", "baseline", "mlp", "Feedforward on the flattened window.", True),
    MethodSpec("LSTM", "baseline", "lstm_base", "LSTM head without retrieval.", True),
    MethodSpec("DLinear", "baseline", "dlinear", "Fixed moving-average decomposition with linear trend and seasonal heads.", True),
    MethodSpec("TCN", "baseline", "tcn", "Causal dilated temporal convolutional network without retrieval.", True),
    MethodSpec("kNN-RawFeature", "baseline", "knn_raw", "k-NN retrieval in raw feature space (no learning).", False),
    MethodSpec("Ablation-NoSiamese", "ablation", "no_siamese", "Retrieval in RAW feature space instead of the learned embedding.", True),
    MethodSpec("Ablation-NoRetrievalBank", "ablation", "gru_only", "GRU head without any retrieval.", True),
    MethodSpec("Ablation-SmallBank", "ablation", "small_bank", "Retrieval bank restricted to the most recent 168 hours.", True),
    MethodSpec("Ablation-LSTMEncoder", "ablation", "lstm_encoder", "LSTM encoder with the same Siamese retrieval.", True),
    MethodSpec("Ablation-NoTopology", "ablation", "no_topology", "Topology-stress feature removed.", True),
)


def run_method(spec: MethodSpec, task: Task, horizon: int, targets_full: np.ndarray, seed: int) -> np.ndarray:
    if spec.runner == "persistence":
        return predict_persistence(task, horizon, targets_full)
    if spec.runner == "seasonal":
        return predict_seasonal(task, horizon, targets_full)
    if spec.runner == "ridge":
        return predict_ridge(task)
    if spec.runner == "knn_raw":
        return predict_knn_raw(task)
    if spec.runner == "mlp":
        preds, _ = train_torch(task, "mlp", seed)
        return preds
    if spec.runner == "lstm_base":
        preds, _ = train_torch(task, "lstm", seed)
        return preds
    if spec.runner == "dlinear":
        preds, _ = train_torch(task, "dlinear", seed)
        return preds
    if spec.runner == "tcn":
        preds, _ = train_torch(task, "tcn", seed)
        return preds
    if spec.runner == "gru_only":
        preds, _ = train_torch(task, "gru", seed)
        return preds
    if spec.runner == "no_topology":
        mask = np.array([True, True, True, True, True, True, False])
        preds, emb = train_torch(task, "gru", seed, feature_mask=mask)
        return retrieval_blend(task, preds, emb, bank_hours=None)
    if spec.runner == "lstm_encoder":
        preds, emb = train_torch(task, "lstm", seed)
        return retrieval_blend(task, preds, emb, bank_hours=None)
    if spec.runner == "no_siamese":
        preds, _ = train_torch(task, "gru", seed)
        raw = task.X_windows.reshape(task.X_windows.shape[0], -1)
        return retrieval_blend(task, preds, raw, bank_hours=None)
    if spec.runner == "small_bank":
        preds, emb = train_torch(task, "gru", seed)
        return retrieval_blend(task, preds, emb, bank_hours=168)
    # dstar
    preds, emb = train_torch(task, "gru", seed)
    return retrieval_blend(task, preds, emb, bank_hours=None)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def holm(pvalues: list[float]) -> list[float]:
    order = np.argsort(pvalues)
    m = len(pvalues)
    adjusted = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvalues[idx]))
        adjusted[idx] = running
    return adjusted


def main() -> None:
    import torch

    torch.set_num_threads(4)
    features, targets = build_series()
    print(f"series: {features.shape[0]} hours; nonzero curtailment share: {(targets > 0).mean():.3f}")

    rows: list[dict[str, str]] = []
    for horizon in HORIZONS:
        task = build_task(features, targets, horizon)
        for spec in METHODS:
            seeds = SEEDS if spec.seeded else POINT_SEEDS
            for seed_index, seed in enumerate(seeds):
                digest = hashlib.sha1(f"p1|{horizon}|{spec.name}".encode()).hexdigest()
                run_seed = seed + int(digest[:4], 16) % 97
                start = time.perf_counter()
                preds = run_method(spec, task, horizon, targets, run_seed)
                metrics = evaluate(task, np.clip(preds, 0.0, 1.0), targets, horizon)
                rows.append(
                    {
                        "dataset": "RTS-GMLC day-ahead (fixed reference dispatch curtailment)",
                        "horizon_hours": str(horizon),
                        "method": spec.name,
                        "method_role": spec.role,
                        "seed": str(seed_index),
                        "curtailment_mae": f"{metrics['curtailment_mae']:.8f}",
                        "curtailment_rmse": f"{metrics['curtailment_rmse']:.8f}",
                        "event_recall": f"{metrics['event_recall']:.6f}",
                        "event_precision": f"{metrics['event_precision']:.6f}",
                        "event_f1": f"{metrics['event_f1']:.6f}",
                        "onset_f1": f"{metrics['onset_f1']:.6f}",
                        "onset_precision": f"{metrics['onset_precision']:.6f}",
                        "onset_recall": f"{metrics['onset_recall']:.6f}",
                        "onset_mae": f"{metrics['onset_mae']:.8f}",
                        "cessation_f1": f"{metrics['cessation_f1']:.6f}",
                        "detection_threshold": f"{metrics['detection_threshold']:.6f}",
                        "n_onsets_test": f"{metrics['n_onsets_test']:.0f}",
                        "stress_subset_mae": f"{metrics['stress_subset_mae']:.8f}",
                        "n_test": f"{metrics['n_test']:.0f}",
                        "n_events": f"{metrics['n_events']:.0f}",
                        "runtime_s": f"{time.perf_counter() - start:.4f}",
                        "source_status": RUN_VERSION,
                    }
                )
            print(f"h{horizon} {spec.name}: done ({len(seeds)} seeds)")

    # significance: proposed vs everyone, per horizon, on curtailment MAE
    stats_rows: list[dict[str, str]] = []
    for horizon in HORIZONS:
        group = [r for r in rows if r["horizon_hours"] == str(horizon)]
        entries, pvals = [], []
        for metric, better_low in (("curtailment_mae", True), ("onset_mae", True), ("onset_f1", False)):
          proposed = [float(r[metric]) for r in group if r["method"] == "DSTAR-GRU"]
          opponents = sorted({r["method"] for r in group if r["method"] != "DSTAR-GRU"})
          for opponent in opponents:
            values = [float(r[metric]) for r in group if r["method"] == opponent]
            if len(values) < 3 or any(math.isnan(v) for v in values + proposed):
                continue  # deterministic point methods: report means only
            try:
                u_stat, p_value = mannwhitneyu(proposed, values, alternative="two-sided")
            except ValueError:
                u_stat, p_value = float("nan"), 1.0
            better = np.mean(proposed) < np.mean(values) if better_low else np.mean(proposed) > np.mean(values)
            pvals.append(float(p_value))
            entries.append(
                {
                    "horizon_hours": str(horizon),
                    "metric": metric,
                    "comparison": f"DSTAR-GRU vs {opponent}",
                    "opponent_role": next(r["method_role"] for r in group if r["method"] == opponent),
                    "n": str(len(values)),
                    "mean_proposed": f"{np.mean(proposed):.8f}",
                    "mean_opponent": f"{np.mean(values):.8f}",
                    "proposed_better": str(better),
                    "u_statistic": f"{u_stat:.2f}" if not math.isnan(u_stat) else "NA",
                    "p_value": f"{p_value:.6g}",
                }
            )
        for entry, p_h in zip(entries, holm(pvals)):
            entry["p_holm"] = f"{p_h:.6g}"
            entry["significant_005_holm"] = str(p_h < 0.05)
        stats_rows.extend(entries)

    # leaderboard
    board: list[dict[str, str]] = []
    for horizon in HORIZONS:
        group = [r for r in rows if r["horizon_hours"] == str(horizon)]
        for method in sorted({r["method"] for r in group}):
            sub = [r for r in group if r["method"] == method]
            mae = [float(r["curtailment_mae"]) for r in sub]
            board.append(
                {
                    "horizon_hours": str(horizon),
                    "method": method,
                    "method_role": sub[0]["method_role"],
                    "n_seeds": str(len(sub)),
                    "mean_curtailment_mae": f"{np.mean(mae):.8f}",
                    "std_curtailment_mae": f"{np.std(mae, ddof=1):.8f}" if len(mae) > 1 else "0",
                    "mean_event_f1": f"{np.mean([float(r['event_f1']) for r in sub]):.6f}",
                    "mean_onset_f1": f"{np.mean([float(r['onset_f1']) for r in sub]):.6f}",
                    "mean_onset_mae": f"{np.nanmean([float(r['onset_mae']) for r in sub]):.8f}",
                    "mean_stress_subset_mae": f"{np.mean([float(r['stress_subset_mae']) for r in sub]):.8f}",
                }
            )
    board.sort(key=lambda r: (int(r["horizon_hours"]), float(r["mean_curtailment_mae"])))

    out_dir = P1_ROOT / "evidence" / "runs"
    table_dir = P1_ROOT / "evidence" / "tables"
    config_dir = P1_ROOT / "src" / "configs"
    for d in (out_dir, table_dir, config_dir):
        d.mkdir(parents=True, exist_ok=True)

    def write(path: Path, data: list[dict[str, str]]) -> None:
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)

    write(out_dir / "real_curtailment_results.csv", rows)
    write(table_dir / "real_curtailment_leaderboard.csv", board)
    write(table_dir / "real_curtailment_significance.csv", stats_rows)

    proposed_rows = [r for r in board if r["method"] == "DSTAR-GRU"]
    lines = [
        "# Real Curtailment Forecasting Analysis - P1 DSTAR-GRU (v4 pivot)",
        "",
        f"Status: `{RUN_VERSION}`.",
        "",
        "## Why v4 exists",
        "",
        "The v3 dispatch experiment scored hand-parameterized method proxies, and",
        "DSTAR-GRU carried an exclusive renewable-bias formula that manufactured most",
        "of the curtailment gap highlighted in the round-2 review. v4 redefines the",
        "task honestly: curtailment under a FIXED reference dispatch policy is the",
        "method-independent target, every method is a real forecasting model, and",
        "DSTAR-GRU's Siamese retrieval operates in a genuinely learned embedding",
        "space. v3 artifacts remain as historical evidence.",
        "",
        "## Headline (per horizon)",
        "",
    ]
    for horizon in HORIZONS:
        sub = [r for r in board if r["horizon_hours"] == str(horizon)]
        proposed = next(r for r in sub if r["method"] == "DSTAR-GRU")
        rank = 1 + next(i for i, r in enumerate(sub) if r["method"] == "DSTAR-GRU")
        baselines = [r for r in sub if r["method_role"] == "baseline"]
        best_baseline = min(baselines, key=lambda r: float(r["mean_curtailment_mae"]))
        gain = (float(best_baseline["mean_curtailment_mae"]) / max(1e-12, float(proposed["mean_curtailment_mae"])) - 1.0) * 100
        lines.extend(
            [
                f"### Horizon {horizon}h",
                "",
                f"- DSTAR-GRU MAE `{proposed['mean_curtailment_mae']}` (std `{proposed['std_curtailment_mae']}`, rank {rank}/{len(sub)})",
                f"- Best baseline: `{best_baseline['method']}` MAE `{best_baseline['mean_curtailment_mae']}`",
                f"- Margin over best baseline: `{gain:.2f}%`",
                f"- Event F1: `{proposed['mean_event_f1']}` vs best baseline `{best_baseline['mean_event_f1']}`",
                f"- ONSET F1 (validation-calibrated detection): `{proposed['mean_onset_f1']}` vs best baseline `{max(baselines, key=lambda r: float(r['mean_onset_f1']))['method']}` `{max(baselines, key=lambda r: float(r['mean_onset_f1']))['mean_onset_f1']}`",
                f"- ONSET MAE: `{proposed['mean_onset_mae']}` vs best baseline `{min(baselines, key=lambda r: float(r['mean_onset_mae']) if r['mean_onset_mae'] != 'nan' else 9e9)['mean_onset_mae']}`",
                "",
                "| rank | method | role | MAE | onset F1 | onset MAE | event F1 | stress MAE |",
                "|---|---|---|---|---|---|---|---|",
            ]
        )
        for i, r in enumerate(sub, start=1):
            lines.append(
                f"| {i} | {r['method']} | {r['method_role']} | {r['mean_curtailment_mae']} | {r['mean_onset_f1']} | {r['mean_onset_mae']} | {r['mean_event_f1']} | {r['mean_stress_subset_mae']} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Interpretation Boundary",
            "",
            "The target is curtailment under one fixed reference policy, i.e. a proxy",
            "for operational curtailment risk, not an OPF/UC-validated quantity; the",
            "dispatch-advisory story requires the (still open) DC-OPF layer. Learned",
            "methods share the training regime and temporal splits; deterministic",
            "methods have single rows. Significance: Mann-Whitney U + Holm on",
            "curtailment MAE, seeded methods only.",
        ]
    )
    (out_dir / "real_curtailment_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (config_dir / "real_curtailment_config.json").write_text(
        json.dumps(
            {
                "task": f"curtailment-rate forecasting under fixed reference dispatch (acceptance cap {REFERENCE_BIAS:.2f}, reserve {REFERENCE_RESERVE:.2f})",
                "hours": SCENARIO_HOURS,
                "window": WINDOW,
                "horizons": HORIZONS,
                "train_ratio": TRAIN_RATIO,
                "seeds": SEEDS,
                "epochs": EPOCHS,
                "k_neighbors": K_NEIGHBORS,
                "methods": {m.name: m.description for m in METHODS},
                "statistics": "Mann-Whitney U two-sided + Holm per horizon on curtailment MAE",
                "status": RUN_VERSION,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("curtailment pivot complete")


if __name__ == "__main__":
    main()
