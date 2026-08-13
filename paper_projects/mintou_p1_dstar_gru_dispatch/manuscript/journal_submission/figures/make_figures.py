"""Publication figures for mintou_p1 (IEEE Access framework/benchmark paper).

Regenerates all three manuscript figures at 300 dpi from primary sources:
  - fig_benchmark_overview.png : full-year curtailment-rate series, event
    sparsity, and onset-definition illustration. Series is RECOMPUTED from the
    benchmark pipeline (`src/powergrid_benchmark/mintou_real_curtailment.py`,
    build_series) so the figure is bound to the exact task definition.
  - fig_leaderboard.png        : per-horizon MAE and onset-F1 leaderboards from
    evidence/tables/real_curtailment_leaderboard.csv.
  - fig_scale_dependency.png   : scale-dependent utility of the retrieval
    component from evidence/tables/real_curtailment_significance.csv.

Also writes series_stats.json with the recomputed series statistics quoted in
the manuscript, so every number is checkable.

Usage:  python make_figures.py   (from anywhere; paths are absolute-safe)
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]  # D:\aicoding\powergrid_benchmark
sys.path.insert(0, str(REPO / "src"))

EVIDENCE = REPO / "papers" / "mintou" / "mintou_p1_dstar_gru_dispatch" / "evidence"
LEADERBOARD = EVIDENCE / "tables" / "real_curtailment_leaderboard.csv"
SIGNIFICANCE = EVIDENCE / "tables" / "real_curtailment_significance.csv"

DPI = 300

# ---- palette (validated placeholder palette, light mode) --------------------
BLUE = "#2a78d6"      # categorical slot 1 / proposed & "beneficial" pole
AQUA = "#1baf7a"      # categorical slot 2 / ablations
RED = "#e34948"       # diverging warm pole / "harmful"
INK = "#0b0b0b"       # primary text
INK2 = "#52514e"      # secondary text
MUTED = "#898781"     # axis labels / baseline methods
GRID = "#e1e0d9"      # hairline gridlines
AXIS = "#c3c2b7"      # axis spine
SURFACE = "#ffffff"   # print surface
NEUTRAL = "#c9c8c1"   # non-significant marks

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8.0,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK2,
        "axes.titlecolor": INK,
        "axes.titlesize": 8.5,
        "axes.titleweight": "semibold",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "legend.frameon": False,
        "legend.fontsize": 7.0,
    }
)


def style_axes(ax, grid_axis="y"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(True, axis=grid_axis, color=GRID, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)


# =============================================================================
# Figure 1: benchmark overview (recomputed series)
# =============================================================================


def fig_benchmark_overview() -> dict:
    from powergrid_benchmark.mintou_real_curtailment import (
        HORIZONS,
        TRAIN_RATIO,
        VAL_RATIO,
        build_series,
    )

    features, targets = build_series()
    T = targets.shape[0]
    train_end = int(T * TRAIN_RATIO)
    fit_cut = int(train_end * (1 - VAL_RATIO))
    thr = 0.02  # onset threshold (operationally significant curtailment)

    stats = {
        "hours": int(T),
        "train_end_hour": int(train_end),
        "fit_cut_hour": int(fit_cut),
        "nonzero_share": float((targets > 0).mean()),
        "share_ge_onset_thr": float((targets >= thr).mean()),
        "max_rate": float(targets.max()),
        "mean_rate": float(targets.mean()),
        "mean_positive_rate": float(targets[targets > 0].mean()),
        "median_positive_rate": float(np.median(targets[targets > 0])),
    }
    for h in HORIZONS:
        last = np.roll(targets, h)
        onset = (targets >= thr) & (last < thr)
        onset[:h] = False
        stats[f"onsets_total_h{h}"] = int(onset.sum())
        stats[f"onsets_test_h{h}"] = int(onset[train_end:].sum())

    fig = plt.figure(figsize=(7.16, 4.6))
    gs = fig.add_gridspec(
        2, 2, height_ratios=[1.35, 1.0], width_ratios=[1.0, 1.0],
        hspace=0.52, wspace=0.26, left=0.075, right=0.985, top=0.93, bottom=0.10,
    )

    # -- (a) full-year series with temporal splits ---------------------------
    ax = fig.add_subplot(gs[0, :])
    style_axes(ax)
    days = np.arange(T) / 24.0
    ax.fill_between(days, 0, targets, color=BLUE, alpha=0.25, linewidth=0, zorder=2)
    ax.plot(days, targets, color=BLUE, linewidth=0.5, zorder=3)
    ax.axhline(thr, color=RED, linewidth=0.9, linestyle=(0, (4, 3)), zorder=4)
    ax.text(176, thr + 0.012, "onset threshold = 0.02", color=RED, fontsize=6.8,
            va="bottom", ha="center")
    # split boundaries
    for x, label in ((fit_cut / 24, "fit | val"), (train_end / 24, "val | test")):
        ax.axvline(x, color=MUTED, linewidth=0.8, linestyle=":", zorder=4)
        ax.text(x + 1.5, 0.93, label, color=INK2, fontsize=6.8, va="top",
                transform=ax.get_xaxis_transform())
    ax.set_xlim(0, T / 24)
    ax.set_ylim(0, max(0.45, targets.max() * 1.06))
    ax.set_xlabel("Day of year (RTS-GMLC day-ahead series, 8760 h)")
    ax.set_ylabel("Curtailment rate")
    ax.set_title(
        f"(a) Reference-policy curtailment-rate series "
        f"({stats['nonzero_share']*100:.1f}% of hours nonzero)",
        loc="left",
    )

    # -- (b) event sparsity by month ------------------------------------------
    ax = fig.add_subplot(gs[1, 0])
    style_axes(ax)
    month_len = T / 12.0
    month_idx = np.minimum((np.arange(T) / month_len).astype(int), 11)
    frac_nonzero = [float((targets[month_idx == m] > 0).mean()) * 100 for m in range(12)]
    frac_event = [float((targets[month_idx == m] >= thr).mean()) * 100 for m in range(12)]
    x = np.arange(12)
    ax.bar(x - 0.21, frac_nonzero, width=0.38, color="#9ec5f4", zorder=2,
           label="curtailment > 0")
    ax.bar(x + 0.21, frac_event, width=0.38, color=BLUE, zorder=2,
           label="curtailment ≥ 0.02")
    ax.set_xticks(x)
    ax.set_xticklabels(["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    ax.set_xlabel("Month")
    ax.set_ylabel("Share of hours (%)")
    ax.set_title("(b) Event sparsity across the year", loc="left")
    ax.legend(loc="upper right", handlelength=1.0, handleheight=0.8)

    # -- (c) onset definition zoom --------------------------------------------
    ax = fig.add_subplot(gs[1, 1])
    style_axes(ax)
    h = 24
    last = np.roll(targets, h)
    onset = (targets >= thr) & (last < thr)
    onset[:h] = False
    # pick an illustrative test-window slice with a handful of onsets
    win = 24 * 8
    best_start = None
    for s in range(train_end, T - win, 24):
        c = int(onset[s : s + win].sum())
        if 3 <= c <= 6:
            best_start = s
            break
    if best_start is None:  # fallback: first window with any onset
        best_start = next(s for s in range(train_end, T - win, 24) if onset[s : s + win].any())
    sl = slice(best_start, best_start + win)
    tt = np.arange(best_start, best_start + win) / 24.0
    ax.fill_between(tt, 0, targets[sl], color=BLUE, alpha=0.25, linewidth=0, zorder=2)
    ax.plot(tt, targets[sl], color=BLUE, linewidth=1.1, zorder=3)
    ax.axhline(thr, color=RED, linewidth=0.9, linestyle=(0, (4, 3)), zorder=4)
    on_t = np.where(onset[sl])[0]
    ax.scatter(tt[on_t], targets[sl][on_t], s=26, color=RED, zorder=5,
               edgecolors=SURFACE, linewidths=1.0)
    # direct annotation instead of a legend (single series + one marker class)
    ax.annotate(
        "onset hours (h = 24)", xy=(tt[on_t[0]], targets[sl][on_t[0]]),
        xytext=(0.52, 0.86), textcoords="axes fraction", fontsize=6.8, color=INK2,
        arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.7},
    )
    ax.set_xlabel("Day of year (test-split excerpt)")
    ax.set_ylabel("Curtailment rate")
    ax.set_title("(c) Onset slice: $y_t \\geq 0.02$ and $y_{t-h} < 0.02$", loc="left")

    fig.savefig(HERE / "fig_benchmark_overview.png", dpi=DPI)
    plt.close(fig)
    return stats


# =============================================================================
# Figure 2: leaderboard (MAE + onset F1 at both horizons)
# =============================================================================

ROLE_COLOR = {"proposed": BLUE, "baseline": MUTED, "ablation": AQUA}
ROLE_LABEL = {"proposed": "framework (DSTAR-GRU)", "baseline": "baseline", "ablation": "ablation"}


def fig_leaderboard() -> None:
    with LEADERBOARD.open(encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["mae"] = float(r["mean_curtailment_mae"])
        r["mae_std"] = float(r["std_curtailment_mae"])
        r["onset_f1"] = float(r["mean_onset_f1"])

    fig, axes = plt.subplots(2, 2, figsize=(7.16, 5.4))
    fig.subplots_adjust(left=0.24, right=0.975, top=0.875, bottom=0.075,
                        hspace=0.52, wspace=0.56)

    panels = [
        ("1", "mae", "(a) 1 h horizon — MAE\n(lower is better)", True),
        ("1", "onset_f1", "(b) 1 h horizon — onset F1\n(higher is better)", False),
        ("24", "mae", "(c) 24 h horizon — MAE\n(lower is better)", True),
        ("24", "onset_f1", "(d) 24 h horizon — onset F1\n(higher is better)", False),
    ]
    for ax, (hz, key, title, lower_better) in zip(axes.flat, panels):
        sub = [r for r in rows if r["horizon_hours"] == hz]
        sub.sort(key=lambda r: r[key], reverse=lower_better)  # best at TOP after barh
        names = [r["method"] for r in sub]
        vals = [r[key] for r in sub]
        colors = [ROLE_COLOR[r["method_role"]] for r in sub]
        y = np.arange(len(sub))
        err = [r["mae_std"] if key == "mae" and int(r["n_seeds"]) > 1 else 0.0 for r in sub]
        ax.barh(y, vals, height=0.62, color=colors, zorder=2,
                xerr=err, error_kw={"ecolor": INK2, "elinewidth": 0.7, "capsize": 1.5})
        style_axes(ax, grid_axis="x")
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=6.6,
                           color=INK2)
        for label, r in zip(ax.get_yticklabels(), sub):
            if r["method_role"] == "proposed":
                label.set_fontweight("bold")
                label.set_color(INK)
        ax.set_title(title, loc="left", fontsize=8.0)
        ax.tick_params(axis="y", length=0)
        if key == "mae":
            ax.set_xlabel("Curtailment-rate MAE")
            ax.xaxis.set_major_formatter(lambda v, _: f"{v:.3f}")
        else:
            ax.set_xlabel("Onset F1 (validation-calibrated threshold)")
        ax.margins(x=0.02)

    handles = [plt.Rectangle((0, 0), 1, 1, color=ROLE_COLOR[k]) for k in ROLE_LABEL]
    fig.legend(handles, list(ROLE_LABEL.values()), loc="upper center", ncol=3,
               bbox_to_anchor=(0.5, 0.985), columnspacing=1.6, handlelength=1.1,
               handleheight=0.8)
    fig.savefig(HERE / "fig_leaderboard.png", dpi=DPI)
    plt.close(fig)


# =============================================================================
# Figure 3: scale-dependent utility of the retrieval component
# =============================================================================


def fig_scale_dependency() -> None:
    with SIGNIFICANCE.open(encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    def pick(horizon: str, metric: str) -> list[dict]:
        out = []
        for r in rows:
            if r["horizon_hours"] == horizon and r["metric"] == metric:
                out.append(
                    {
                        "opponent": r["comparison"].replace("DSTAR-GRU vs ", ""),
                        "proposed": float(r["mean_proposed"]),
                        "opponent_mean": float(r["mean_opponent"]),
                        "p_holm": float(r["p_holm"]),
                        "sig": r["significant_005_holm"] == "True",
                        "better": r["proposed_better"] == "True",
                    }
                )
        return out

    fig, axes = plt.subplots(1, 2, figsize=(7.16, 3.1))
    fig.subplots_adjust(left=0.21, right=0.975, top=0.82, bottom=0.16, wspace=0.52)

    # Panel A: 1h curtailment MAE — relative margin of the framework vs opponent
    # positive = retrieval framework better (blue); negative = worse (red)
    a_rows = pick("1", "curtailment_mae")
    a_rows.sort(key=lambda r: (r["opponent_mean"] - r["proposed"]) / r["opponent_mean"])
    ax = axes[0]
    style_axes(ax, grid_axis="x")
    y = np.arange(len(a_rows))
    vals = [100 * (r["opponent_mean"] - r["proposed"]) / r["opponent_mean"] for r in a_rows]
    colors = [(BLUE if v > 0 else RED) if r["sig"] else NEUTRAL for v, r in zip(vals, a_rows)]
    ax.barh(y, vals, height=0.6, color=colors, zorder=2)
    ax.axvline(0, color=AXIS, linewidth=0.8, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels([r["opponent"] for r in a_rows], fontsize=6.6, color=INK2)
    ax.tick_params(axis="y", length=0)
    for yi, (v, r) in enumerate(zip(vals, a_rows)):
        note = f"p={r['p_holm']:.3f}" if r["sig"] else "n.s."
        # label on the empty side of the zero line for negative bars
        xpos, halign = (v + 0.9, "left") if v >= 0 else (0.9, "left")
        ax.text(xpos, yi, note, fontsize=6.0, color=INK2, va="center", ha=halign)
    ax.set_xlabel("MAE margin of framework vs. opponent (%)")
    ax.set_title("(a) 1 h horizon:\nretrieval is beneficial (curtailment MAE)",
                 loc="left", fontsize=8.0)
    ax.margins(x=0.18)

    # Panel B: 24h onset F1 — absolute F1 difference (framework - opponent)
    b_rows = pick("24", "onset_f1")
    b_rows.sort(key=lambda r: r["proposed"] - r["opponent_mean"])
    ax = axes[1]
    style_axes(ax, grid_axis="x")
    y = np.arange(len(b_rows))
    vals = [100 * (r["proposed"] - r["opponent_mean"]) for r in b_rows]
    colors = [(BLUE if v > 0 else RED) if r["sig"] else NEUTRAL for v, r in zip(vals, b_rows)]
    ax.barh(y, vals, height=0.6, color=colors, zorder=2)
    ax.axvline(0, color=AXIS, linewidth=0.8, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels([r["opponent"] for r in b_rows], fontsize=6.6, color=INK2)
    ax.tick_params(axis="y", length=0)
    for yi, (v, r) in enumerate(zip(vals, b_rows)):
        note = f"p={r['p_holm']:.3f}" if r["sig"] else "n.s."
        # label on the empty side of the zero line for negative bars
        xpos, halign = (v + 0.25, "left") if v >= 0 else (0.25, "left")
        ax.text(xpos, yi, note, fontsize=6.0, color=INK2, va="center", ha=halign)
    ax.set_xlabel("Onset-F1 difference (points)")
    ax.set_title("(b) 24 h onset warning:\nretrieval is harmful (onset F1)",
                 loc="left", fontsize=8.0)
    ax.margins(x=0.18)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=BLUE),
        plt.Rectangle((0, 0), 1, 1, color=RED),
        plt.Rectangle((0, 0), 1, 1, color=NEUTRAL),
    ]
    fig.legend(
        handles,
        ["framework significantly better", "framework significantly worse",
         "not significant (Holm α = 0.05)"],
        loc="upper center", ncol=3, bbox_to_anchor=(0.5, 0.995),
        columnspacing=1.4, handlelength=1.1, handleheight=0.8,
    )
    fig.savefig(HERE / "fig_scale_dependency.png", dpi=DPI)
    plt.close(fig)


if __name__ == "__main__":
    stats = fig_benchmark_overview()
    (HERE / "series_stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))
    fig_leaderboard()
    fig_scale_dependency()
    print("figures written to", HERE)
