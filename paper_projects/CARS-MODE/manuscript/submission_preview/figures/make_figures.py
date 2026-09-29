"""Manuscript figures for mintou_p3 (CARS-MODE, MDPI Energies).

Reads the real 30-seed evidence CSVs and produces three journal-ready PNG
figures (>= 300 dpi) in this directory:

    fig_hv_boxplot.png       hypervolume boxplots, 7 experiments x 7 main methods
    fig_ablation.png         4 ablations vs full CARS-MODE, mean HV bars
                             (FixedDE micro-advantage annotated)
    fig_ac_validation.png    pandapower AC-feasible rates per method vs No-Plan
                             (CARS-MODE mid-pack, FixedDE lower - the HV/AC
                             reversal that the paper discusses honestly)

fig_sensitivity.png is produced separately by
src/powergrid_benchmark/mintou_planning_sensitivity.py and is not rebuilt here.

Style: matplotlib only, no seaborn; <= 2 main hues (blue = proposed method,
neutral grays = everything else); DejaVu Sans; recessive grids and spines.

Data sources (all numbers traceable):
    evidence/runs/real_simbench_planning_results.csv    (per-seed HV, 30 seeds)
    evidence/tables/real_simbench_planning_leaderboard.csv
    evidence/tables/real_simbench_planning_significance.csv
    evidence/tables/real_ac_validation_summary.csv      (72 AC cases per method)
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
PAPER_ROOT = FIG_DIR.parents[1]
EVIDENCE = PAPER_ROOT / "evidence"
RESULTS_CSV = EVIDENCE / "runs" / "real_simbench_planning_results.csv"
SIGNIFICANCE_CSV = EVIDENCE / "tables" / "real_simbench_planning_significance.csv"
AC_SUMMARY_CSV = EVIDENCE / "tables" / "real_ac_validation_summary.csv"

# ---------------------------------------------------------------------------
# Palette (validated categorical slot 1 blue + neutral grays; <= 2 main hues)
# ---------------------------------------------------------------------------
BLUE = "#2a78d6"        # proposed method (CARS-MODE)
BLUE_DARK = "#1c5cab"
BLUE_LIGHT = "#9dc1ec"
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

MAIN_METHODS = ["CARS-MODE", "NSGA-II", "Standard DE", "GA", "PSO", "Weighted Sum", "MOEA/D"]

EXPERIMENT_LABELS = {
    "base_distribution_planning": "Base distribution\nplanning",
    "der_siting_sizing": "DER siting\nand sizing",
    "storage_allocation": "Storage\nallocation",
    "load_growth_expansion": "Load-growth\nexpansion (1.3x)",
    "pareto_quality": "Pareto-quality\nreplicate",
    "constraint_repair": "Tight budget\n(0.82x)",
    "runtime_scalability": "Loose budget\n(1.20x)",
}
EXPERIMENT_ORDER = list(EXPERIMENT_LABELS)

ABLATION_LABELS = {
    "Ablation-FixedDE": "Fixed F/CR, single strategy",
    "Ablation-NoDER": "No DER/storage candidates",
    "Ablation-NoRepair": "No budget repair",
    "Ablation-NoDiversity": "No crowding diversity",
}


def load_results() -> pd.DataFrame:
    df = pd.read_csv(RESULTS_CSV)
    return df[df["paper"] == "p3"].copy()


# ---------------------------------------------------------------------------
# Figure 1: hypervolume boxplots, 7 experiments x 7 main methods
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
            if m == "CARS-MODE":
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

    # 8th panel is unused (7 experiments): hide it and reuse the space
    axes.flat[-1].axis("off")

    for ax in axes[:, 0]:
        ax.set_ylabel("Hypervolume")

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK, alpha=0.85),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_FILL, edgecolor=GRAY_DARK),
    ]
    fig.legend(handles, ["CARS-MODE (proposed)", "Baseline methods"],
               loc="upper center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, 1.035))
    fig.tight_layout(h_pad=1.2, w_pad=0.6)
    fig.savefig(FIG_DIR / "fig_hv_boxplot.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: 4 ablations vs full method, mean HV over 7 experiments x 30 seeds
# ---------------------------------------------------------------------------
def fig_ablation(df: pd.DataFrame) -> None:
    methods = ["CARS-MODE"] + list(ABLATION_LABELS)
    stats = (
        df[df["method"].isin(methods)]
        .groupby("method")["hypervolume"]
        .agg(["mean", "std"])
    )
    full_mean = stats.loc["CARS-MODE", "mean"]

    # full method first, then ablations sorted by descending mean HV
    abl_sorted = stats.loc[list(ABLATION_LABELS)].sort_values("mean", ascending=False)
    order = ["CARS-MODE"] + list(abl_sorted.index)

    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    y = np.arange(len(order))[::-1]  # full method on top
    means = stats.loc[order, "mean"].to_numpy()
    stds = stats.loc[order, "std"].to_numpy()
    colors = [BLUE if m == "CARS-MODE" else GRAY_LIGHT for m in order]
    edges = [BLUE_DARK if m == "CARS-MODE" else GRAY_MID for m in order]

    ax.barh(y, means, xerr=stds, height=0.62, color=colors, edgecolor=edges,
            linewidth=0.8, error_kw=dict(ecolor=GRAY_DARK, elinewidth=0.8, capsize=2.0))
    ax.axvline(full_mean, color=BLUE_DARK, linestyle="--", linewidth=0.9, zorder=0)
    ax.annotate("full-method mean", (full_mean, y[0] + 0.55),
                xytext=(3, 0), textcoords="offset points",
                fontsize=6.8, color=BLUE_DARK, va="center")

    labels = ["CARS-MODE (full)"] + [ABLATION_LABELS[m] for m in order[1:]]
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Hypervolume (mean $\\pm$ std over 7 experiments $\\times$ 30 seeds)")
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 0.062)

    # relative-difference annotations for every ablation
    for m in ABLATION_LABELS:
        delta = 100.0 * (stats.loc[m, "mean"] - full_mean) / full_mean
        idx = order.index(m)
        note = f"{delta:+.2f}%"
        if m == "Ablation-FixedDE":
            note += " (n.s. in all 7 experiments;\nAC-feasible rate drops, Fig. 3)"
        ax.annotate(
            note,
            (means[idx] + stds[idx], y[idx]),
            xytext=(6, 0), textcoords="offset points",
            va="center", fontsize=7.0, color=INK, fontweight="bold",
        )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_ablation.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: pandapower AC-feasible rates (72 cases per method) vs No-Plan
# ---------------------------------------------------------------------------
def fig_ac_validation() -> None:
    ac = pd.read_csv(AC_SUMMARY_CSV)
    ac = ac[ac["paper"] == "p3"].copy()
    ac = ac.sort_values("ac_feasible_rate", ascending=True).reset_index(drop=True)

    noplan_rate = float(ac.loc[ac["method"] == "NoPlan", "ac_feasible_rate"].iloc[0])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    y = np.arange(len(ac))
    bar_h = 0.36

    colors, edges = [], []
    for m, role in zip(ac["method"], ac["method_role"]):
        if role == "proposed":
            colors.append(BLUE)
            edges.append(BLUE_DARK)
        elif role == "reference":
            colors.append("white")
            edges.append(GRAY_DARK)
        elif role == "baseline":
            colors.append(GRAY_MID)
            edges.append(GRAY_DARK)
        else:  # ablation
            colors.append(GRAY_LIGHT)
            edges.append(GRAY_MID)

    ax.barh(y + bar_h / 2, ac["ac_feasible_rate"], height=bar_h,
            color=colors, edgecolor=edges, linewidth=0.8)
    stress_colors = [BLUE_LIGHT if r == "proposed" else GRAY_FILL for r in ac["method_role"]]
    ax.barh(y - bar_h / 2, ac["stress_ac_feasible_rate"], height=bar_h,
            color=stress_colors, edgecolor=edges, linewidth=0.6)

    ax.axvline(noplan_rate, color=INK, linestyle="--", linewidth=0.9, zorder=3)
    ax.annotate("No-Plan reference\n(all scenarios, 0.50)", (noplan_rate, 1.0),
                xytext=(5, 0), textcoords="offset points",
                fontsize=6.6, color=INK_MUTED, va="center")

    labels = [m if m != "NoPlan" else "No-Plan (reference)" for m in ac["method"]]
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.2)
    ax.set_xlabel("AC-feasible rate over 72 pandapower load-flow cases")
    ax.set_xlim(0, 0.88)
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)

    # honest callouts: CARS-MODE mid-pack; FixedDE lower than the full method
    for method, text in [
        ("CARS-MODE", "proposed: 0.611, mid-pack\n(best plan mix: Standard DE, 0.681)"),
        ("Ablation-FixedDE", "FixedDE ablation: 0.569\n(higher proxy HV, lower AC rate)"),
    ]:
        idx = int(ac.index[ac["method"] == method][0])
        rate = float(ac.loc[idx, "ac_feasible_rate"])
        ax.annotate(text, (rate, idx + bar_h / 2),
                    xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=6.8, color=INK, fontweight="bold")

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_MID, edgecolor=GRAY_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_LIGHT, edgecolor=GRAY_MID),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_FILL, edgecolor=GRAY_MID),
    ]
    fig.legend(handles,
               ["CARS-MODE (proposed)", "Baselines", "Ablations",
                "Stress-only scenarios (lower bar)"],
               loc="upper center", ncol=4, frameon=False,
               bbox_to_anchor=(0.5, 1.05))
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_ac_validation.png")
    plt.close(fig)


def main() -> None:
    df = load_results()
    fig_hv_boxplot(df)
    fig_ablation(df)
    fig_ac_validation()
    for name in ["fig_hv_boxplot", "fig_ablation", "fig_ac_validation"]:
        print(f"wrote {FIG_DIR / (name + '.png')}")


if __name__ == "__main__":
    main()
