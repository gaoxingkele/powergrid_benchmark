"""Publication figures for the TRACE-MOEA manuscript (mintou_p5, MDPI Energies).

Reads only the released evidence CSVs; every plotted number is reproducible from:
  papers/mintou/mintou_p5_trace_moea_feasibility_review/evidence/runs/real_project_review_results.csv
  papers/mintou/mintou_p5_trace_moea_feasibility_review/evidence/tables/real_nerc_rule_backtest.csv
  papers/mintou/mintou_p5_trace_moea_feasibility_review/evidence/tables/real_mtep_backtest.csv

Outputs 300 dpi PNGs next to this script:
  fig_hv_boxplot.png        hypervolume distributions, 7 experiments x 7 main methods
  fig_ablation.png          pooled ablation attribution with honest annotations
  fig_external_validity.png two-rung external-validity ladder (NERC + MTEP16)

Palette: dataviz reference categorical palette (validated, fixed slot order).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
EVID = ROOT / "papers" / "mintou" / "mintou_p5_trace_moea_feasibility_review" / "evidence"
OUT = Path(__file__).resolve().parent

# --- validated categorical palette (fixed order; do not cycle) -------------
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASE = "#c3c2b7"
SURFACE = "#ffffff"

METHOD_COLORS = {
    "TRACE-MOEA": "#2a78d6",      # slot 1 blue (proposed)
    "NSGA-II": "#1baf7a",         # slot 2 aqua
    "AHP-TOPSIS": "#eda100",      # slot 3 yellow
    "MOEA/D": "#008300",          # slot 4 green
    "Weighted Sum": "#4a3aa7",    # slot 5 violet
    "Greedy BCR": "#e87ba4",      # slot 7 magenta
    "Random Feasible": "#eb6834", # slot 8 orange
}
MAIN_METHODS = list(METHOD_COLORS)

EXP_LABELS = {
    "benchmark_portfolio_optimization": "benchmark\nportfolio",
    "distribution_project_review": "distribution\nreview",
    "reliability_driven_review": "reliability-\ndriven",
    "renewable_accommodation_review": "renewable\naccomm.",
    "budget_ranking_stability": "budget\nstability",
    "preference_aware_support": "preference-\naware",
    "traceability_evaluation": "traceability\nevaluation",
}
EXP_ORDER = list(EXP_LABELS)

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Segoe UI", "Arial"],
        "font.size": 8.5,
        "axes.edgecolor": BASE,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": INK2,
        "ytick.labelcolor": INK2,
        "axes.grid": False,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
    }
)


def _despine(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)


# ===========================================================================
# Figure 1: hypervolume boxplots, 7 experiments x 7 main methods
# ===========================================================================


DETERMINISTIC = {"AHP-TOPSIS", "Weighted Sum", "Greedy BCR"}


def fig_hv_boxplot(runs: pd.DataFrame) -> None:
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(figsize=(10.6, 4.4))
    n_m = len(MAIN_METHODS)
    group_w = 0.86
    box_w = group_w / n_m * 0.72
    for gi, exp in enumerate(EXP_ORDER):
        for mi, method in enumerate(MAIN_METHODS):
            vals = runs[(runs.experiment_id == exp) & (runs.method == method)].hypervolume.values
            pos = gi + (mi - (n_m - 1) / 2) * (group_w / n_m)
            color = METHOD_COLORS[method]
            if method in DETERMINISTIC:
                # weight-driven point methods are deterministic: one value per
                # experiment, drawn as a diamond instead of a degenerate box
                ax.scatter(
                    [pos], [vals[0]], marker="D", s=26, color=color,
                    edgecolors=SURFACE, linewidths=1.0, zorder=4,
                )
                continue
            bp = ax.boxplot(
                [vals],
                positions=[pos],
                widths=box_w,
                patch_artist=True,
                showfliers=False,
                whiskerprops=dict(color=color, linewidth=0.9),
                capprops=dict(color=color, linewidth=0.9),
                medianprops=dict(color=INK, linewidth=1.0),
                boxprops=dict(linewidth=0),
            )
            bp["boxes"][0].set_facecolor(color)
            bp["boxes"][0].set_alpha(0.85)
    ax.set_xticks(range(len(EXP_ORDER)))
    ax.set_xticklabels([EXP_LABELS[e] for e in EXP_ORDER])
    ax.set_ylabel("Hypervolume (30 seeds per box)")
    ax.set_ylim(0.0, 0.21)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    _despine(ax)
    for gi in range(len(EXP_ORDER) - 1):
        ax.axvline(gi + 0.5, color=GRID, linewidth=0.7)
    handles = []
    labels = []
    for m in MAIN_METHODS:
        if m in DETERMINISTIC:
            handles.append(
                Line2D([], [], marker="D", linestyle="none", markersize=5.5,
                       markerfacecolor=METHOD_COLORS[m], markeredgecolor="none")
            )
            labels.append(f"{m} (deterministic)")
        else:
            handles.append(
                plt.Rectangle((0, 0), 1, 1, facecolor=METHOD_COLORS[m], alpha=0.85, edgecolor="none")
            )
            labels.append(m)
    ax.legend(
        handles,
        labels,
        loc="lower left",
        ncol=4,
        frameon=False,
        fontsize=7.6,
        handlelength=1.2,
        handleheight=1.0,
        columnspacing=1.2,
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_hv_boxplot.png", dpi=300)
    plt.close(fig)


# ===========================================================================
# Figure 2: ablation attribution (pooled), honest annotations
# ===========================================================================

ABLATION_LABELS = {
    "TRACE-MOEA": "TRACE-MOEA (full)",
    "Ablation-NoScheduleRisk": "No schedule-risk objective",
    "Ablation-NoPreferenceRanking": "No preference adaptation",
    "Ablation-NoFeasibilityRepair": "No budget repair",
    "Ablation-NSGA2Only": "Bare kernel (no repair / pref. / trace)",
    "Ablation-NoRenewableFeatures": "No renewable objective",
    "Ablation-SingleObjective": "Scalarized single objective",
    "Ablation-NoReliabilityFeatures": "No reliability objective",
    "Ablation-SmallProjectPool": "One-third candidate pool",
}


def fig_ablation(runs: pd.DataFrame) -> None:
    sub = runs[runs.method.isin(ABLATION_LABELS)]
    agg = (
        sub.groupby("method")
        .hypervolume.agg(["mean", lambda s: s.std(ddof=1)])
        .rename(columns={"mean": "mean", "<lambda_0>": "std"})
        .reindex(ABLATION_LABELS)
        .sort_values("mean")
    )
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    y = np.arange(len(agg))
    colors = ["#2a78d6" if m == "TRACE-MOEA" else "#6da7ec" for m in agg.index]
    ax.barh(y, agg["mean"], height=0.62, color=colors, edgecolor="none", zorder=3)
    ax.errorbar(
        agg["mean"], y, xerr=agg["std"], fmt="none", ecolor=INK2, elinewidth=0.9, capsize=2.2, zorder=4
    )
    for yi, (m, row) in enumerate(agg.iterrows()):
        ax.text(
            row["mean"] + row["std"] + 0.004,
            yi,
            f"{row['mean']:.4f}",
            va="center",
            ha="left",
            fontsize=7.4,
            color=INK2,
        )
    ax.set_yticks(y)
    ax.set_yticklabels(
        [ABLATION_LABELS[m] for m in agg.index],
        fontsize=8.2,
        fontweight=["bold" if m == "TRACE-MOEA" else "normal" for m in agg.index][0],
    )
    for tick, m in zip(ax.get_yticklabels(), agg.index):
        tick.set_fontweight("bold" if m == "TRACE-MOEA" else "normal")
    ax.set_xlabel("Pooled mean hypervolume (7 experiments x 30 seeds; bar = mean, whisker = std)")
    ax.set_xlim(0.0, 0.35)
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    _despine(ax)
    # honest annotations, placed in the free right margin next to their rows
    y_nsr = list(agg.index).index("Ablation-NoScheduleRisk")
    ax.text(
        0.213,
        y_nsr,
        "-0.13% vs. full method (pooled, n.s.);\nsig. ahead in traceability evaluation\n(Holm p = 0.022)",
        fontsize=6.8,
        color=INK2,
        va="center",
        ha="left",
    )
    y_full = list(agg.index).index("TRACE-MOEA")
    ax.text(
        0.213,
        y_full,
        "best pooled mean: +0.89% over\nstrongest baseline (38/42 Holm wins)",
        fontsize=6.8,
        color=INK2,
        va="center",
        ha="left",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_ablation.png", dpi=300)
    plt.close(fig)


# ===========================================================================
# Figure 3: external-validity ladder — NERC rule backtest + MTEP16 outcomes
# ===========================================================================

EXP_DOT_COLORS = {
    "benchmark_portfolio_optimization": "#2a78d6",  # slot 1 blue
    "reliability_driven_review": "#eb6834",         # slot 8 orange
}
EXP_DOT_LABELS = {
    "benchmark_portfolio_optimization": "benchmark portfolio",
    "reliability_driven_review": "reliability-driven",
}


def _dot_panel(ax, df, value_col, title, xlabel, xlim):
    methods = MAIN_METHODS
    y = np.arange(len(methods))[::-1]
    ax.axvline(1.0, color=BASE, linewidth=1.0, zorder=2)
    for exp, color in EXP_DOT_COLORS.items():
        vals = []
        for m in methods:
            row = df[(df.experiment_id == exp) & (df.method == m)]
            vals.append(float(row[value_col].iloc[0]) if len(row) else np.nan)
        ax.scatter(
            vals,
            y,
            s=46,
            color=color,
            edgecolors=SURFACE,
            linewidths=1.4,
            zorder=4,
            label=EXP_DOT_LABELS[exp],
        )
    ax.set_yticks(y)
    ax.set_yticklabels(methods, fontsize=8.2)
    for tick, m in zip(ax.get_yticklabels(), methods):
        tick.set_fontweight("bold" if m == "TRACE-MOEA" else "normal")
    ax.set_xlim(*xlim)
    ax.set_ylim(-0.85, len(methods) - 0.4)
    ax.set_xlabel(xlabel, fontsize=8.2)
    ax.set_title(title, fontsize=9.2, color=INK, loc="left")
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    _despine(ax)
    ax.text(1.0, -0.62, "parity", fontsize=7.2, color=MUTED, ha="center", va="center",
            bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.0))


def fig_external_validity(nerc: pd.DataFrame, mtep: pd.DataFrame) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 3.7))
    _dot_panel(
        ax1,
        nerc,
        "priority_capture_ratio",
        "(a) Rung 1 - NERC rule backtest (consistency)",
        "Priority-capture ratio (>1 = oversamples documented-risk candidates)",
        (0.0, 2.55),
    )
    _dot_panel(
        ax2,
        mtep,
        "outcome_capture_broad",
        "(b) Rung 2 - MISO MTEP16 outcome backtest (weak form)",
        "Broad outcome-capture ratio (built vs. withdrawn/unresolved)",
        (0.95, 1.17),
    )
    # annotations
    nerc_ahp = float(
        nerc[(nerc.experiment_id == "benchmark_portfolio_optimization") & (nerc.method == "AHP-TOPSIS")][
            "priority_capture_ratio"
        ].iloc[0]
    )
    ax1.annotate(
        "AHP-TOPSIS: highest alignment by construction\n(directly weights reliability attributes;\nKendall tau 0.45/0.52, significant)",
        xy=(nerc_ahp, 4.0),
        xytext=(1.32, 2.15),
        fontsize=7.0,
        color=INK2,
        arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8, shrinkA=2, shrinkB=4),
    )
    mtep_tm = float(
        mtep[(mtep.experiment_id == "benchmark_portfolio_optimization") & (mtep.method == "TRACE-MOEA")][
            "outcome_capture_broad"
        ].iloc[0]
    )
    ax2.annotate(
        "TRACE-MOEA: capture 1.079,\npoint-biserial r = 0.169, p < 1e-7",
        xy=(mtep_tm, 6.0),
        xytext=(1.088, 4.6),
        fontsize=7.0,
        color=INK2,
        arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=0.8, shrinkA=2, shrinkB=4),
    )
    ax1.legend(loc="lower right", frameon=False, fontsize=7.6, handletextpad=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "fig_external_validity.png", dpi=300)
    plt.close(fig)


def main() -> None:
    runs = pd.read_csv(EVID / "runs" / "real_project_review_results.csv")
    nerc = pd.read_csv(EVID / "tables" / "real_nerc_rule_backtest.csv")
    mtep = pd.read_csv(EVID / "tables" / "real_mtep_backtest.csv")
    fig_hv_boxplot(runs)
    fig_ablation(runs)
    fig_external_validity(nerc, mtep)
    print("wrote:", ", ".join(p.name for p in sorted(OUT.glob("fig_*.png"))))


if __name__ == "__main__":
    main()
