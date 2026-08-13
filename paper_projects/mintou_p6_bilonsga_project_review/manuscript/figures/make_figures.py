"""Manuscript figures for mintou_p6 (BiLo-NSGA, MDPI Applied Sciences).

Reads the real 30-seed evidence CSVs and produces four journal-ready PNG
figures (>= 300 dpi) in this directory:

    fig_hv_boxplot.png          hypervolume boxplots, 8 experiments x 6 main methods
    fig_budget_sensitivity.png  mean HV +/- std across 4 budget levels
    fig_ablation.png            9 ablations vs full BiLo-NSGA, mean HV bars
    fig_nerc_backtest.png       NERC rule-backtest priority-capture ratios

Style: matplotlib only, no seaborn; <= 2 main hues (blue = proposed method,
neutral grays = everything else); DejaVu Sans; recessive grids and spines.

Budget-level mapping used in fig_budget_sensitivity (from
src/powergrid_benchmark/mintou_real_project_review.py::budget_for):
    0.75x -> budget_sensitivity
    0.88x -> budget_constrained_selection
    1.00x -> local_move_explainability + ranking_robustness pooled
             (the two full-pool experiments run at the nominal budget)
    1.20x -> project_pool_scalability
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
FIG_DIR = Path(__file__).resolve().parent
REPO_ROOT = FIG_DIR.parents[3]
EVIDENCE = REPO_ROOT / "papers" / "mintou" / "mintou_p6_bilonsga_project_review" / "evidence"
RESULTS_CSV = EVIDENCE / "runs" / "real_project_review_results.csv"
NERC_CSV = EVIDENCE / "tables" / "real_nerc_rule_backtest.csv"

# ---------------------------------------------------------------------------
# Palette (validated categorical slot 1 blue + neutral grays; <= 2 main hues)
# ---------------------------------------------------------------------------
BLUE = "#2a78d6"        # proposed method (BiLo-NSGA)
BLUE_DARK = "#1c5cab"
GRAY_DARK = "#4d4d4a"   # baseline emphasis / ink
GRAY_MID = "#8a8a86"    # baselines
GRAY_LIGHT = "#c9c9c4"  # ablations / de-emphasised fills
GRAY_FILL = "#e4e4e0"
INK = "#262625"
INK_MUTED = "#6e6e6a"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 8.0,
    "axes.labelsize": 8.5,
    "axes.titlesize": 8.5,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.edgecolor": GRAY_MID,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": INK_MUTED,
    "ytick.color": INK_MUTED,
    "axes.labelcolor": INK,
    "text.color": INK,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})

MAIN_METHODS = ["BiLo-NSGA", "NSGA-II", "NSGA-III", "MOEA/D", "AHP-TOPSIS", "Greedy BCR"]

EXPERIMENT_LABELS = {
    "budget_constrained_selection": "Budget-constrained\nselection (0.88x)",
    "reliability_prioritized_review": "Reliability-prioritized\nreview",
    "renewable_accommodation_review": "Renewable-accommodation\nreview",
    "dependency_constrained_review": "Dependency-constrained\nreview",
    "local_move_explainability": "Local-move\nexplainability",
    "ranking_robustness": "Ranking\nrobustness",
    "budget_sensitivity": "Budget\nsensitivity (0.75x)",
    "project_pool_scalability": "Project-pool\nscalability (1.20x)",
}
EXPERIMENT_ORDER = list(EXPERIMENT_LABELS)

ABLATION_LABELS = {
    "Ablation-NoBackwardSearch": "No backward search",
    "Ablation-LowDependencyDensity": "Low dependency density",
    "Ablation-ShallowLocalSearch": "Shallow local search",
    "Ablation-NoDependencyMoves": "No dependency moves",
    "Ablation-RandomMutationOnly": "Random mutation only",
    "Ablation-NoForwardSearch": "No forward search",
    "Ablation-NoFeasibilityRecovery": "No feasibility recovery",
    "Ablation-LooseBudget": "Loose budget (1.2x search)",
    "Ablation-WeightedRankingOnly": "Weighted ranking only",
}


def load_results() -> pd.DataFrame:
    df = pd.read_csv(RESULTS_CSV)
    return df[df["paper"] == "p6"].copy()


# ---------------------------------------------------------------------------
# Figure 1: hypervolume boxplots, 8 experiments x 6 main methods
# ---------------------------------------------------------------------------
def fig_hv_boxplot(df: pd.DataFrame) -> None:
    d = df[df["method"].isin(MAIN_METHODS)]
    fig, axes = plt.subplots(2, 4, figsize=(7.0, 4.6), sharey=True, sharex=True)

    for ax, exp in zip(axes.flat, EXPERIMENT_ORDER):
        sub = d[d["experiment_id"] == exp]
        data = [sub.loc[sub["method"] == m, "hypervolume"].to_numpy() for m in MAIN_METHODS]
        bp = ax.boxplot(
            data,
            positions=np.arange(len(MAIN_METHODS)),
            widths=0.62,
            patch_artist=True,
            showfliers=True,
            flierprops=dict(marker="o", markersize=1.8, markerfacecolor=GRAY_MID,
                            markeredgecolor="none", alpha=0.7),
            medianprops=dict(color=INK, linewidth=1.1),
            whiskerprops=dict(color=GRAY_DARK, linewidth=0.8),
            capprops=dict(color=GRAY_DARK, linewidth=0.8),
            boxprops=dict(linewidth=0.8),
        )
        for patch, m in zip(bp["boxes"], MAIN_METHODS):
            if m == "BiLo-NSGA":
                patch.set_facecolor(BLUE)
                patch.set_edgecolor(BLUE_DARK)
                patch.set_alpha(0.85)
            else:
                patch.set_facecolor(GRAY_FILL)
                patch.set_edgecolor(GRAY_DARK)
        ax.set_title(EXPERIMENT_LABELS[exp], fontsize=7.5, pad=3)
        ax.set_xticks(np.arange(len(MAIN_METHODS)))
        ax.set_xticklabels(MAIN_METHODS, rotation=45, ha="right", fontsize=6.6)
        ax.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)

    for ax in axes[:, 0]:
        ax.set_ylabel("Hypervolume")

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK, alpha=0.85),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_FILL, edgecolor=GRAY_DARK),
    ]
    fig.legend(handles, ["BiLo-NSGA (proposed)", "Baseline methods"],
               loc="upper center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, 1.035))
    fig.tight_layout(h_pad=1.2, w_pad=0.6)
    fig.savefig(FIG_DIR / "fig_hv_boxplot.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: mean HV +/- std across the 4 budget levels
# ---------------------------------------------------------------------------
BUDGET_LEVELS = [
    (0.75, ["budget_sensitivity"]),
    (0.88, ["budget_constrained_selection"]),
    (1.00, ["local_move_explainability", "ranking_robustness"]),
    (1.20, ["project_pool_scalability"]),
]

# style per method: (color, linestyle, marker)
LINE_STYLES = {
    "BiLo-NSGA": (BLUE, "-", "o"),
    "NSGA-II": (GRAY_DARK, "--", "s"),
    "NSGA-III": (GRAY_DARK, ":", "^"),
    "AHP-TOPSIS": (GRAY_MID, "-.", "D"),
    "Greedy BCR": (GRAY_MID, "--", "v"),
    "MOEA/D": (GRAY_LIGHT, ":", "x"),
}


def fig_budget_sensitivity(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    xs = [lvl for lvl, _ in BUDGET_LEVELS]
    offsets = dict(zip(MAIN_METHODS, np.linspace(-0.008, 0.008, len(MAIN_METHODS))))

    for m in MAIN_METHODS:
        means, stds = [], []
        for _, exps in BUDGET_LEVELS:
            v = df[(df["method"] == m) & (df["experiment_id"].isin(exps))]["hypervolume"]
            means.append(v.mean())
            stds.append(v.std())
        color, ls, marker = LINE_STYLES[m]
        x = np.asarray(xs) + offsets[m]
        ax.errorbar(
            x, means, yerr=stds,
            color=color, linestyle=ls, marker=marker,
            linewidth=1.4, markersize=4.0,
            markerfacecolor="white" if marker != "x" else color,
            markeredgecolor=color, markeredgewidth=1.0,
            capsize=2.2, elinewidth=0.8, zorder=3 if m == "BiLo-NSGA" else 2,
        )
        # direct label at the right end
        ax.annotate(
            m, (x[-1], means[-1]), xytext=(7, 0), textcoords="offset points",
            va="center", fontsize=7.0,
            color=BLUE_DARK if m == "BiLo-NSGA" else INK_MUTED,
            fontweight="bold" if m == "BiLo-NSGA" else "normal",
        )

    ax.set_xlabel("Budget multiplier (relative to nominal review budget)")
    ax.set_ylabel("Hypervolume (mean $\\pm$ std across seeds)")
    ax.set_xticks(xs)
    ax.set_xticklabels(["0.75x", "0.88x", "1.00x", "1.20x"])
    ax.set_xlim(0.68, 1.36)
    ax.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_budget_sensitivity.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: ablations vs full method, mean HV over all 8 experiments
# ---------------------------------------------------------------------------
def fig_ablation(df: pd.DataFrame) -> None:
    methods = ["BiLo-NSGA"] + list(ABLATION_LABELS)
    stats = (
        df[df["method"].isin(methods)]
        .groupby("method")["hypervolume"]
        .agg(["mean", "std"])
    )
    full_mean = stats.loc["BiLo-NSGA", "mean"]

    # full method first, then ablations sorted by descending mean HV
    abl_sorted = stats.loc[list(ABLATION_LABELS)].sort_values("mean", ascending=False)
    order = ["BiLo-NSGA"] + list(abl_sorted.index)

    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    y = np.arange(len(order))[::-1]  # full method on top
    means = stats.loc[order, "mean"].to_numpy()
    stds = stats.loc[order, "std"].to_numpy()
    colors = [BLUE if m == "BiLo-NSGA" else GRAY_LIGHT for m in order]
    edges = [BLUE_DARK if m == "BiLo-NSGA" else GRAY_MID for m in order]

    ax.barh(y, means, xerr=stds, height=0.62, color=colors, edgecolor=edges,
            linewidth=0.8, error_kw=dict(ecolor=GRAY_DARK, elinewidth=0.8, capsize=2.0))
    ax.axvline(full_mean, color=BLUE_DARK, linestyle="--", linewidth=0.9, zorder=0)
    ax.annotate("full-method mean", (full_mean, y[0] + 0.62),
                xytext=(3, 0), textcoords="offset points",
                fontsize=6.8, color=BLUE_DARK, va="center")

    labels = ["BiLo-NSGA (full)"] + [ABLATION_LABELS[m] for m in order[1:]]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Hypervolume (mean $\\pm$ std over 8 experiments $\\times$ 30 seeds)")
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 0.215)

    # relative-difference annotations for the named ablations
    callouts = {
        "Ablation-NoBackwardSearch": None,
        "Ablation-NoFeasibilityRecovery": None,
        "Ablation-LooseBudget": None,
        "Ablation-WeightedRankingOnly": None,
    }
    for m in callouts:
        delta = 100.0 * (stats.loc[m, "mean"] - full_mean) / full_mean
        idx = order.index(m)
        ax.annotate(
            f"{delta:+.1f}%",
            (means[idx] + stds[idx], y[idx]),
            xytext=(6, 0), textcoords="offset points",
            va="center", fontsize=7.0, color=INK, fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_ablation.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4: NERC rule-backtest priority-capture ratios
# ---------------------------------------------------------------------------
NERC_PANELS = [
    ("budget_constrained_selection", "Budget-constrained selection"),
    ("reliability_prioritized_review", "Reliability-prioritized review"),
]


def fig_nerc_backtest() -> None:
    nerc = pd.read_csv(NERC_CSV)
    nerc = nerc[nerc["paper"] == "p6"]

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.9), sharex=True)
    for ax, (exp, title) in zip(axes, NERC_PANELS):
        sub = nerc[nerc["experiment_id"] == exp].dropna(subset=["priority_capture_ratio"])
        sub = sub.sort_values("priority_capture_ratio", ascending=True)
        labels = [ABLATION_LABELS.get(m, m) for m in sub["method"]]
        y = np.arange(len(sub))
        colors, edges = [], []
        for m, role in zip(sub["method"], sub["method_role"]):
            if role == "proposed":
                colors.append(BLUE)
                edges.append(BLUE_DARK)
            elif role == "baseline":
                colors.append(GRAY_MID)
                edges.append(GRAY_DARK)
            else:  # ablation
                colors.append(GRAY_LIGHT)
                edges.append(GRAY_MID)
        ax.barh(y, sub["priority_capture_ratio"], height=0.66,
                color=colors, edgecolor=edges, linewidth=0.7)
        ax.axvline(1.0, color=INK, linestyle="--", linewidth=0.9, zorder=3)
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=6.8)
        ax.set_title(title, fontsize=8.0, pad=4)
        ax.set_xlabel("Priority-capture ratio")
        ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)

    # reference-line label on the left panel only, in the empty region right
    # of the parity line next to the lowest bars
    axes[0].annotate("parity with random\nselection (= 1)", (1.06, 0.5),
                     fontsize=6.6, color=INK_MUTED, ha="left", va="center")
    # note the method missing from the reliability panel (no feasible portfolio)
    missing = set(nerc[nerc["experiment_id"] == NERC_PANELS[0][0]]["method"]) - set(
        nerc[(nerc["experiment_id"] == NERC_PANELS[1][0])
             & nerc["priority_capture_ratio"].notna()]["method"])
    if missing:
        axes[1].annotate(f"{', '.join(sorted(missing))}: no feasible\nportfolio (not shown)",
                         xy=(0.98, 0.03), xycoords="axes fraction",
                         ha="right", va="bottom", fontsize=6.6, color=INK_MUTED)

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_MID, edgecolor=GRAY_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_LIGHT, edgecolor=GRAY_MID),
    ]
    fig.legend(handles, ["BiLo-NSGA (proposed)", "Baselines", "Ablations"],
               loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(w_pad=2.0)
    fig.savefig(FIG_DIR / "fig_nerc_backtest.png")
    plt.close(fig)


def main() -> None:
    df = load_results()
    fig_hv_boxplot(df)
    fig_budget_sensitivity(df)
    fig_ablation(df)
    fig_nerc_backtest()
    for name in ["fig_hv_boxplot", "fig_budget_sensitivity", "fig_ablation", "fig_nerc_backtest"]:
        print(f"wrote {FIG_DIR / (name + '.png')}")


if __name__ == "__main__":
    main()
