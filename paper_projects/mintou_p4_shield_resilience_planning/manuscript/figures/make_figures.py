"""Compatibility entry point for the canonical p4 results-artifact build.

The stage-4 figure and table set is controlled by
``evidence/manifests/p4_s4_results_artifact_manifest_20260813.json`` and is
built by ``build_results_artifacts.ps1``.  The historical plotting functions
below are retained for source history, but ``main`` delegates to the
hash-checked canonical builder so this entry point cannot silently recreate
the superseded 72-case AC panel.

The historical implementation below read the real 30-seed evidence CSVs and
wrote three journal-ready PNG figures into this directory:

    fig_hv_boxplot.png      hypervolume boxplots, 8 archive labels x 6 main
                            methods, plus a pooled mean-vs-worst-envelope HV
                            robustness panel (single shared axis, no dual axes)
    fig_ablation.png        4 single-switch ablations vs the full method,
                            with relative-difference and significance callouts
    fig_ac_validation.png   pandapower AC validation: feasible rates
                            (all scenarios / stress-only) and mean max line
                            loading per method

``fig_sensitivity.png`` remains a separately produced parameter-sweep figure.

Style: matplotlib only; one accent hue (blue = SHIELD-MOEA) plus neutral
grays; recessive grid; identity is never carried by color alone (labels on
every bar/box position).
"""

from __future__ import annotations

from pathlib import Path
import subprocess


def canonical_builder_path() -> Path:
    """Resolve the controlling builder from the source or journal copy."""
    figure_dir = Path(__file__).resolve().parent
    if figure_dir.parent.name == "journal_submission":
        return figure_dir.parent.parent / "figures" / "build_results_artifacts.ps1"
    return figure_dir / "build_results_artifacts.ps1"


if __name__ == "__main__":
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-File", str(canonical_builder_path())],
        check=True,
    )
    raise SystemExit(0)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
FIG_DIR = Path(__file__).resolve().parent
PROJECT = "mintou_p4_shield_resilience_planning"


def find_repo_root(start: Path) -> Path:
    """Find the shared harness root from either figure-script copy."""
    for candidate in (start, *start.parents):
        evidence = candidate / "papers" / "mintou" / PROJECT / "evidence"
        if evidence.is_dir():
            return candidate
    raise FileNotFoundError("shared Mintou evidence tree not found above figure directory")


REPO_ROOT = find_repo_root(FIG_DIR)
EVIDENCE = REPO_ROOT / "papers" / "mintou" / PROJECT / "evidence"
RESULTS_CSV = EVIDENCE / "runs" / "real_simbench_planning_results.csv"
SIGNIFICANCE_CSV = EVIDENCE / "tables" / "real_simbench_planning_significance.csv"
AC_SUMMARY_CSV = EVIDENCE / "tables" / "real_ac_validation_summary.csv"

# ---------------------------------------------------------------------------
# Palette: one accent hue + neutral grays (validated categorical blue)
# ---------------------------------------------------------------------------
BLUE = "#2a78d6"
BLUE_DARK = "#1c5cab"
GRAY_DARK = "#4d4d4a"
GRAY_MID = "#8a8a86"
GRAY_LIGHT = "#c9c9c4"
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

PROPOSED = "SHIELD-MOEA"
MAIN_METHODS = [PROPOSED, "NSGA-II", "GA", "MOEA/D", "Weighted Sum", "Deterministic Planning"]
MAIN_LABELS = {
    "Deterministic Planning": "Deterministic",
    "Weighted Sum": "Weighted Sum",
}

EXPERIMENT_LABELS = {
    "deterministic_vs_scenario": "Deterministic vs.\nscenario",
    "der_uncertainty": "DER-factor label\n(inactive in p4 F)",
    "load_uncertainty": "Load\nuncertainty",
    "outage_contingency": "Outage\ncontingency",
    "restoration_aware_evaluation": "$L^e$ in search\nand evaluation",
    "scenario_screening_efficiency": "Scenario-screening\nefficiency",
    "pareto_quality": "Pareto\nquality",
    "unseen_stress_generalization": "Unseen-stress\ngeneralization",
}
EXPERIMENT_ORDER = list(EXPERIMENT_LABELS)

ABLATION_LABELS = {
    "Ablation-NoResilienceObj": "No survivability in environmental selection",
    "Ablation-NoScenarioScreen": "No scenario screening",
    "Ablation-NoOutage": "No outage in search",
    "Ablation-NoRepair": "No feasibility repair",
}


def load_results() -> pd.DataFrame:
    df = pd.read_csv(RESULTS_CSV)
    return df[df["paper"] == "p4"].copy()


# ---------------------------------------------------------------------------
# Figure 1: HV boxplots (8 archive labels x 6 main methods) + envelope panel
# ---------------------------------------------------------------------------
def fig_hv_boxplot(df: pd.DataFrame) -> None:
    d = df[df["method"].isin(MAIN_METHODS)]
    fig = plt.figure(figsize=(7.0, 6.6))
    gs = fig.add_gridspec(3, 4, height_ratios=[1.0, 1.0, 0.85], hspace=0.62, wspace=0.10)
    box_axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(4)]

    for ax, exp in zip(box_axes, EXPERIMENT_ORDER):
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
            medianprops=dict(color=INK, linewidth=1.0),
            whiskerprops=dict(color=GRAY_DARK, linewidth=0.8),
            capprops=dict(color=GRAY_DARK, linewidth=0.8),
            boxprops=dict(linewidth=0.8),
        )
        for patch, m in zip(bp["boxes"], MAIN_METHODS):
            if m == PROPOSED:
                patch.set_facecolor(BLUE)
                patch.set_edgecolor(BLUE_DARK)
                patch.set_alpha(0.85)
            else:
                patch.set_facecolor(GRAY_FILL)
                patch.set_edgecolor(GRAY_DARK)
        ax.set_title(EXPERIMENT_LABELS[exp], fontsize=7.3, pad=3)
        ax.set_xticks(np.arange(len(MAIN_METHODS)))
        ax.set_xticklabels([MAIN_LABELS.get(m, m) for m in MAIN_METHODS],
                           rotation=45, ha="right", fontsize=6.3)
        ax.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)
        ax.set_ylim(-0.015, 0.40)
        if ax not in (box_axes[0], box_axes[4]):
            ax.set_yticklabels([])
    box_axes[0].set_ylabel("Hypervolume")
    box_axes[4].set_ylabel("Hypervolume")

    # Robustness panel: pooled mean HV vs worst-case HV (same unit, one axis)
    axr = fig.add_subplot(gs[2, :])
    pooled = (
        d.groupby("method")[["hypervolume", "hypervolume_worst_case"]]
        .mean()
        .loc[MAIN_METHODS]
    )
    x = np.arange(len(MAIN_METHODS))
    dx = 0.14  # horizontal offset so the two nearly equal values stay legible
    for i, m in enumerate(MAIN_METHODS):
        mean_hv = pooled.loc[m, "hypervolume"]
        worst_hv = pooled.loc[m, "hypervolume_worst_case"]
        color = BLUE if m == PROPOSED else GRAY_DARK
        axr.plot([i - dx, i + dx], [mean_hv, worst_hv], color=color,
                 linewidth=1.2, zorder=2)
        axr.plot(i - dx, mean_hv, marker="o", markersize=6.0, markerfacecolor=color,
                 markeredgecolor="white", markeredgewidth=0.8, zorder=3)
        axr.plot(i + dx, worst_hv, marker="o", markersize=6.0, markerfacecolor="white",
                 markeredgecolor=color, markeredgewidth=1.3, zorder=3)
    axr.annotate(
        f"mean {pooled.loc[PROPOSED, 'hypervolume']:.3f} $\\rightarrow$ worst-envelope "
        f"{pooled.loc[PROPOSED, 'hypervolume_worst_case']:.3f}",
        (0 + dx, pooled.loc[PROPOSED, "hypervolume_worst_case"]), xytext=(-14, -30),
        textcoords="offset points", fontsize=6.8, color=BLUE_DARK,
        fontweight="bold", va="top", ha="left",
    )
    axr.set_xticks(x)
    axr.set_xticklabels([MAIN_LABELS.get(m, m) for m in MAIN_METHODS], fontsize=7.2)
    axr.set_ylabel("Hypervolume")
    axr.set_title("Pooled mean vs. sampled worst-envelope hypervolume (8 labels $\\times$ 30 seeds)",
                  fontsize=7.6, pad=4)
    axr.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
    axr.set_axisbelow(True)
    axr.tick_params(axis="x", length=0)
    axr.set_ylim(-0.015, 0.32)

    filled = plt.Line2D([], [], marker="o", linestyle="none", markersize=6,
                        markerfacecolor=GRAY_DARK, markeredgecolor="white")
    open_m = plt.Line2D([], [], marker="o", linestyle="none", markersize=6,
                        markerfacecolor="white", markeredgecolor=GRAY_DARK)
    blue_box = plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK, alpha=0.85)
    gray_box = plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_FILL, edgecolor=GRAY_DARK)
    fig.legend([blue_box, gray_box, filled, open_m],
               ["SHIELD-MOEA (proposed)", "Baselines",
                "Mean HV (bottom panel)", "Worst-envelope HV (bottom panel)"],
               loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.98))
    fig.subplots_adjust(top=0.90)
    fig.savefig(FIG_DIR / "fig_hv_boxplot.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: ablations vs full method
# ---------------------------------------------------------------------------
def fig_ablation(df: pd.DataFrame) -> None:
    sig = pd.read_csv(SIGNIFICANCE_CSV)
    methods = [PROPOSED] + list(ABLATION_LABELS)
    stats = (
        df[df["method"].isin(methods)]
        .groupby("method")["hypervolume"]
        .agg(["mean", "std"])
    )
    full_mean = stats.loc[PROPOSED, "mean"]
    order = [PROPOSED] + list(stats.loc[list(ABLATION_LABELS)]
                              .sort_values("mean", ascending=False).index)

    # Holm-significant label counts per ablation (out of 8)
    sig_counts = {}
    for m in ABLATION_LABELS:
        rows = sig[sig["comparison"] == f"{PROPOSED} vs {m}"]
        sig_counts[m] = int(rows["significant_005_holm"].sum())

    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    y = np.arange(len(order))[::-1]
    means = stats.loc[order, "mean"].to_numpy()
    stds = stats.loc[order, "std"].to_numpy()
    colors = [BLUE if m == PROPOSED else GRAY_LIGHT for m in order]
    edges = [BLUE_DARK if m == PROPOSED else GRAY_MID for m in order]

    ax.barh(y, means, xerr=stds, height=0.62, color=colors, edgecolor=edges,
            linewidth=0.8, error_kw=dict(ecolor=GRAY_DARK, elinewidth=0.8, capsize=2.0))
    ax.axvline(full_mean, color=BLUE_DARK, linestyle="--", linewidth=0.9, zorder=0)

    labels = []
    for m in order:
        labels.append("SHIELD-MOEA (full)" if m == PROPOSED else ABLATION_LABELS[m])
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Hypervolume (mean $\\pm$ std over 8 labels $\\times$ 30 seeds)")
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 0.345)

    for m in ABLATION_LABELS:
        delta = 100.0 * (stats.loc[m, "mean"] - full_mean) / full_mean
        idx = order.index(m)
        sig_txt = f"sig. {sig_counts[m]}/8" if sig_counts[m] else "n.s. 0/8"
        ax.annotate(
            f"{delta:+.2f}%  ({sig_txt})",
            (means[idx] + stds[idx], y[idx]),
            xytext=(6, 0), textcoords="offset points",
            va="center", fontsize=7.0, color=INK,
            fontweight="bold" if m == "Ablation-NoRepair" else "normal",
        )
    ax.annotate("full-method mean", (full_mean, y[0] + 0.55),
                xytext=(3, 2), textcoords="offset points",
                fontsize=6.8, color=BLUE_DARK, va="bottom")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_ablation.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: pandapower AC validation
# ---------------------------------------------------------------------------
AC_ORDER = [
    "SHIELD-MOEA", "GA", "NSGA-II", "Deterministic Planning", "MOEA/D",
    "Weighted Sum", "Ablation-NoResilienceObj", "Ablation-NoScenarioScreen",
    "Ablation-NoOutage", "Ablation-NoRepair", "NoPlan",
]
AC_LABELS = {
    "Deterministic Planning": "Deterministic",
    "Ablation-NoResilienceObj": "No $S$ in selection",
    "Ablation-NoScenarioScreen": "No scenario screen",
    "Ablation-NoOutage": "No outage in search",
    "Ablation-NoRepair": "No repair",
    "NoPlan": "No plan (reference)",
}


def fig_ac_validation() -> None:
    ac = pd.read_csv(AC_SUMMARY_CSV)
    ac = ac[ac["paper"] == "p4"].set_index("method").loc[AC_ORDER]
    noplan_rate = ac.loc["NoPlan", "ac_feasible_rate"]

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.6), sharey=True)
    y = np.arange(len(AC_ORDER))[::-1]

    def style(m):
        if m == PROPOSED:
            return BLUE, BLUE_DARK
        if m == "NoPlan":
            return "white", GRAY_DARK
        if m.startswith("Ablation"):
            return GRAY_LIGHT, GRAY_MID
        return GRAY_MID, GRAY_DARK

    # Panel (a): AC-feasible rate, all scenarios and stress-only
    ax = axes[0]
    for i, m in enumerate(AC_ORDER):
        face, edge = style(m)
        ax.barh(y[i] + 0.19, ac.loc[m, "ac_feasible_rate"], height=0.36,
                color=face, edgecolor=edge, linewidth=0.8)
        ax.barh(y[i] - 0.19, ac.loc[m, "stress_ac_feasible_rate"], height=0.36,
                color=face, edgecolor=edge, linewidth=0.8, alpha=0.45)
    ax.axvline(noplan_rate, color=INK, linestyle="--", linewidth=0.9, zorder=3)
    ax.annotate("no-plan\nreference (0.50)", (noplan_rate, y[-1] - 0.35),
                xytext=(3, 0), textcoords="offset points",
                fontsize=6.4, color=INK_MUTED, va="bottom")
    ax.annotate("0.708 (tied highest)",
                (ac.loc[PROPOSED, "ac_feasible_rate"], y[0] + 0.19),
                xytext=(4, 0), textcoords="offset points", va="center",
                fontsize=6.8, color=BLUE_DARK, fontweight="bold")
    noout_y = y[AC_ORDER.index("Ablation-NoOutage")]
    ax.annotate("0.625", (ac.loc["Ablation-NoOutage", "ac_feasible_rate"], noout_y + 0.19),
                xytext=(4, 0), textcoords="offset points", va="center",
                fontsize=6.8, color=INK, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels([AC_LABELS.get(m, m) for m in AC_ORDER], fontsize=7.0)
    ax.set_xlabel("AC-feasible rate (72 network $\\times$ scenario cases)")
    ax.set_xlim(0, 1.0)
    ax.set_title("(a) AC feasibility (solid: all scenarios; faded: stress-only)",
                 fontsize=7.6, pad=4)
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)

    # Panel (b): mean max line loading
    ax = axes[1]
    for i, m in enumerate(AC_ORDER):
        face, edge = style(m)
        ax.barh(y[i], ac.loc[m, "mean_max_line_loading_pct"], height=0.62,
                color=face, edgecolor=edge, linewidth=0.8)
    ax.axvline(100.0, color=INK, linestyle="--", linewidth=0.9, zorder=3)
    ax.annotate("loading limit (100%)", (100.0, y[0] + 0.55),
                xytext=(4, 0), textcoords="offset points",
                fontsize=6.4, color=INK_MUTED, ha="left", va="bottom")
    for m in [PROPOSED, "Ablation-NoOutage", "NoPlan"]:
        idx = AC_ORDER.index(m)
        val = ac.loc[m, "mean_max_line_loading_pct"]
        ax.annotate(f"{val:.1f}%", (val, y[idx]),
                    xytext=(4, 0), textcoords="offset points", va="center",
                    fontsize=6.8,
                    color=BLUE_DARK if m == PROPOSED else INK,
                    fontweight="bold" if m in (PROPOSED, "Ablation-NoOutage") else "normal")
    ax.set_xlabel("Mean max line loading (%)")
    ax.set_xlim(0, 125)
    ax.set_title("(b) Mean maximum line loading", fontsize=7.6, pad=4)
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_MID, edgecolor=GRAY_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_LIGHT, edgecolor=GRAY_MID),
        plt.Rectangle((0, 0), 1, 1, facecolor="white", edgecolor=GRAY_DARK),
    ]
    fig.legend(handles, ["SHIELD-MOEA (proposed)", "Baselines", "Ablations", "No-plan reference"],
               loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(w_pad=1.6)
    fig.savefig(FIG_DIR / "fig_ac_validation.png")
    plt.close(fig)


def main() -> None:
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-File", str(canonical_builder_path())],
        check=True,
    )


if __name__ == "__main__":
    main()
