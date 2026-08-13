"""Render the post-audit enhancement figures for the six Mintou papers.

Every plotted value is read from the versioned experiment CSVs produced by
the 2026-08-11 frozen enhancement protocol.  Outputs are written as 300 dpi
PNG plus vector PDF/SVG companions.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "paper_projects"
EVIDENCE = ROOT / "papers" / "mintou"

BLUE = "#2F6690"
ORANGE = "#D97A2B"
GREEN = "#4C956C"
RED = "#B44C43"
GRAY = "#68737D"
LIGHT = "#EDF2F6"


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.5,
            "axes.titlesize": 9.5,
            "axes.labelsize": 8.5,
            "legend.fontsize": 7.5,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def save(fig: plt.Figure, directory: Path, stem: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(directory / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(directory / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(directory / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)


def p1() -> None:
    base = EVIDENCE / "mintou_p1_dstar_gru_dispatch" / "evidence"
    board = pd.read_csv(base / "tables" / "real_curtailment_leaderboard.csv")
    nrel = pd.read_csv(base / "tables" / "nrel118_transportability_summary.csv").iloc[0]
    chosen = ["DSTAR-GRU", "TCN", "DLinear"]
    colors = [BLUE, GREEN, ORANGE]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.65))
    x = np.arange(2)
    width = 0.24
    for offset, method, color in zip((-1, 0, 1), chosen, colors):
        vals = [
            board[(board.method == method) & (board.horizon_hours == horizon)]["mean_curtailment_mae"].iloc[0]
            for horizon in (1, 24)
        ]
        axes[0].bar(x + offset * width, vals, width=width, label=method, color=color)
    axes[0].set_xticks(x, ["1 h", "24 h"])
    axes[0].set_ylabel("Curtailment-rate MAE")
    axes[0].set_title("(a) Modern temporal controls")
    axes[0].legend(frameon=False, ncol=3, loc="upper left")

    labels = ["Mean", "95th percentile", "Maximum", "Frozen cap"]
    vals = [nrel.renewable_share_mean, nrel.renewable_share_q95, nrel.renewable_share_max, nrel.reference_acceptance_cap]
    axes[1].barh(labels, vals, color=[BLUE, BLUE, BLUE, RED])
    axes[1].set_xlim(0, 0.75)
    axes[1].set_xlabel("Renewable share")
    axes[1].set_title("(b) NREL-118 frozen-task applicability")
    axes[1].text(0.02, 0.04, "0 positive target hours", transform=axes[1].transAxes, color=RED, fontsize=8)
    fig.tight_layout()
    out = PROJECTS / "mintou_p1_dstar_gru_dispatch" / "manuscript" / "figures"
    save(fig, out, "fig_modern_baselines_transportability")


def p2_hierarchy() -> None:
    fig, ax = plt.subplots(figsize=(7.15, 3.25))
    ax.set_axis_off()
    leaf_y = np.linspace(0.05, 0.95, 12)
    group_y = np.asarray([leaf_y[i : i + 3].mean() for i in range(0, 12, 3)])
    total_y = 0.5

    def box(x: float, y: float, w: float, h: float, label: str, color: str, fs: float = 7.5) -> None:
        patch = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.012,rounding_size=0.012",
            linewidth=0.9, edgecolor=color, facecolor="white",
        )
        ax.add_patch(patch)
        ax.text(x, y, label, ha="center", va="center", fontsize=fs, color=color)

    for i, y in enumerate(leaf_y):
        box(0.14, y, 0.18, 0.052, f"Customer {i + 1}", BLUE, 6.8)
        gy = group_y[i // 3]
        ax.plot([0.23, 0.42], [y, gy], color=GRAY, lw=0.75)
    for i, y in enumerate(group_y):
        box(0.52, y, 0.18, 0.085, f"Region {i + 1}\n(sum of 3 leaves)", GREEN, 7.2)
        ax.plot([0.61, 0.79], [y, total_y], color=GRAY, lw=0.9)
    box(0.88, total_y, 0.17, 0.11, "System total\n(sum of 12 leaves)", ORANGE, 7.4)
    ax.text(0.14, 1.01, "12 exact leaf series", ha="center", va="bottom", weight="bold")
    ax.text(0.52, 1.01, "4 deterministic groups", ha="center", va="bottom", weight="bold")
    ax.text(0.88, 1.01, "1 root", ha="center", va="bottom", weight="bold")
    ax.text(0.5, -0.035, r"Exact identity at every hour:  $\mathbf{y}_t = \mathbf{S}\mathbf{b}_t$   with   $\mathbf{S}\in\{0,1\}^{17\times12}$", ha="center", va="top")
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.08, 1.07)
    fig.tight_layout()
    out = PROJECTS / "mintou_p2_hygraph_load_forecasting" / "manuscript" / "figures"
    save(fig, out, "fig_exact_hierarchy_design")


def p2_results() -> None:
    base = EVIDENCE / "mintou_p2_hygraph_load_forecasting" / "evidence"
    board = pd.read_csv(base / "tables" / "real_ausgrid_exact_hierarchy_v8_leaderboard.csv")
    methods = ["DLinear", "MLP", "PatchTST-lite", "HyG-LoadFormer (neural)", "TCN", "LSTM"]
    recs = ["Base", "Bottom-Up", "OLS-Reconciled"]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.8))
    x = np.arange(len(methods))
    for j, (rec, color) in enumerate(zip(recs, [GRAY, GREEN, BLUE])):
        vals = [board[(board.method == m) & (board.reconciliation == rec)].mean_hierarchy_weighted_smape.iloc[0] for m in methods]
        axes[0].plot(x, vals, marker="o", ms=4, lw=1.2, color=color, label=rec)
    axes[0].set_xticks(x, ["DLinear", "MLP", "PatchTST", "CSA-\nLoadNet", "TCN", "LSTM"], rotation=25, ha="right")
    axes[0].set_ylabel("Hierarchy-weighted sMAPE")
    axes[0].set_title("(a) Accuracy after reconciliation")
    axes[0].legend(frameon=False)

    selected = board[board.method.isin(methods) & board.reconciliation.isin(recs)]
    coh = selected.groupby("reconciliation").mean_coherence_violation.mean().reindex(recs)
    axes[1].bar(recs, coh.values, color=[GRAY, GREEN, BLUE])
    axes[1].set_ylabel("Mean coherence violation")
    axes[1].set_title("(b) Structural coherence")
    axes[1].tick_params(axis="x", rotation=25)
    axes[1].text(1.0, max(coh.max(), 1e-6) * 0.8, "exact", ha="center", color=GREEN)
    axes[1].text(2.0, max(coh.max(), 1e-6) * 0.8, "exact", ha="center", color=BLUE)
    fig.tight_layout()
    out = PROJECTS / "mintou_p2_hygraph_load_forecasting" / "manuscript" / "figures"
    save(fig, out, "fig_exact_hierarchy_reconciliation")


def p3() -> None:
    path = EVIDENCE / "mintou_p3_samode_distribution_planning" / "evidence" / "runs" / "real_simbench_planning_results.csv"
    df = pd.read_csv(path)
    chosen = ["CARS-MODE", "GDE3", "NSDE", "NSGA-II+Repair"]
    experiments = list(dict.fromkeys(df.experiment_id))
    labels = ["Base", "DER", "Storage", "Growth", "Pareto", "Repair", "Scale"]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.0))
    colors = [BLUE, ORANGE, GREEN, GRAY]
    x = np.arange(len(experiments))
    for method, color in zip(chosen, colors):
        g = df[df.method == method].groupby("experiment_id").hypervolume.agg(["mean", "std"]).reindex(experiments)
        axes[0].errorbar(x, g["mean"], yerr=g["std"], marker="o", ms=3.8, capsize=2, lw=1.1, label=method, color=color)
    axes[0].set_xticks(x, labels, rotation=30, ha="right")
    axes[0].set_ylabel("Feasible-front hypervolume")
    axes[0].set_title("(a) Direct multi-objective DE controls")
    axes[0].legend(frameon=False, ncol=2)

    proposed = df[df.method == "CARS-MODE"].groupby("experiment_id").hypervolume.mean()
    width = 0.34
    for j, (method, color) in enumerate(zip(["GDE3", "NSDE"], [ORANGE, GREEN])):
        other = df[df.method == method].groupby("experiment_id").hypervolume.mean()
        rel = 100 * (proposed / other - 1).reindex(experiments)
        axes[1].bar(x + (j - 0.5) * width, rel, width=width, color=color, label=method)
    axes[1].axhline(0, color="black", lw=0.8)
    axes[1].set_xticks(x, labels, rotation=30, ha="right")
    axes[1].set_ylabel("CARS-MODE HV advantage (%)")
    axes[1].set_title("(b) Relative advantage")
    axes[1].legend(frameon=False)
    fig.tight_layout()
    out = PROJECTS / "mintou_p3_samode_distribution_planning" / "manuscript" / "figures"
    save(fig, out, "fig_direct_de_controls")


def p4() -> None:
    path = EVIDENCE / "mintou_p4_shield_resilience_planning" / "evidence" / "runs" / "real_ac_validation_results.csv"
    df = pd.read_csv(path)
    methods = ["NoPlan", "NSGA-II+Repair", "SHIELD-MOEA"]
    families = ["SimBench MV", "CIGRE MV", "IEEE 33-bus"]
    colors = [GRAY, ORANGE, BLUE]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.75))
    x = np.arange(len(families))
    width = 0.24
    for j, (method, color) in enumerate(zip(methods, colors)):
        g = df[df.method == method].groupby("network_family")
        feas = g.ac_feasible.mean().reindex(families)
        min_voltage = g.min_vm_pu.mean().reindex(families)
        axes[0].bar(x + (j - 1) * width, feas, width, label=method, color=color)
        axes[1].bar(x + (j - 1) * width, min_voltage, width, label=method, color=color)
    axes[0].set_xticks(x, families, rotation=18, ha="right")
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel("AC-feasible rate")
    axes[0].set_title("(a) Cross-family feasibility")
    axes[0].legend(frameon=False, ncol=3, loc="upper center")
    axes[1].set_xticks(x, families, rotation=18, ha="right")
    axes[1].axhline(0.95, color=RED, lw=0.9, ls="--")
    axes[1].set_ylim(0.85, 1.01)
    axes[1].set_ylabel("Mean minimum voltage (pu)")
    axes[1].set_title("(b) Voltage support")
    fig.tight_layout()
    out = PROJECTS / "mintou_p4_shield_resilience_planning" / "manuscript" / "figures"
    save(fig, out, "fig_cross_family_ac")


def p5() -> None:
    path = EVIDENCE / "mintou_p5_trace_moea_feasibility_review" / "evidence" / "tables" / "real_preference_budget_v1_leaderboard.csv"
    df = pd.read_csv(path)
    methods = ["TRACE-MOEA", "R-NSGA-II", "NSGA-II"]
    colors = [BLUE, ORANGE, GRAY]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.65))
    for method, color in zip(methods, colors):
        g = df[df.method == method].sort_values("budget_multiplier")
        axes[0].errorbar(g.budget_multiplier, g.mean_hypervolume, yerr=g.std_hypervolume, marker="o", capsize=2, lw=1.2, color=color, label=method)
        axes[1].plot(g.budget_multiplier, g.mean_preference_achievement_distance, marker="o", lw=1.2, color=color, label=method)
    axes[0].set_xlabel("Budget multiplier")
    axes[0].set_ylabel("Hypervolume")
    axes[0].set_title("(a) Global front quality")
    axes[0].legend(frameon=False)
    axes[1].set_xlabel("Budget multiplier")
    axes[1].set_ylabel("Achievement distance (lower is better)")
    axes[1].set_title("(b) Preference-region quality")
    fig.tight_layout()
    out = PROJECTS / "mintou_p5_trace_moea_feasibility_review" / "manuscript" / "figures"
    save(fig, out, "fig_preference_budget_controls")


def p6() -> None:
    path = EVIDENCE / "mintou_p6_bilonsga_project_review" / "evidence" / "runs" / "real_project_review_results.csv"
    df = pd.read_csv(path)
    methods = ["BiLo-NSGA", "Ablation-NoBackwardSearch", "Ablation-LegacyDeletion", "NSGA-II", "Pareto Local Search"]
    labels = ["Revised full", "Forward-only", "Legacy deletion", "NSGA-II", "Pareto local search"]
    colors = [BLUE, GREEN, ORANGE, GRAY, RED]
    experiments = list(dict.fromkeys(df.experiment_id))
    short = ["Budget", "Reliability", "Renewable", "Dependency", "Explain.", "Ranking", "Sensitivity", "Scale"]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.0))
    x = np.arange(len(experiments))
    for method, label, color in zip(methods, labels, colors):
        g = df[df.method == method].groupby("experiment_id").hypervolume.mean().reindex(experiments)
        axes[0].plot(x, g, marker="o", ms=3.5, lw=1.05, label=label, color=color)
    axes[0].set_xticks(x, short, rotation=30, ha="right")
    axes[0].set_ylabel("Feasible-front hypervolume")
    axes[0].set_title("(a) Direct mechanism and local-search controls")
    axes[0].legend(frameon=False, ncol=2)

    proposed = df[df.method == "BiLo-NSGA"].groupby("experiment_id").hypervolume.mean()
    for method, label, color in zip(methods[1:], labels[1:], colors[1:]):
        other = df[df.method == method].groupby("experiment_id").hypervolume.mean()
        diff = (proposed - other).reindex(experiments)
        axes[1].plot(x, diff, marker="o", ms=3.5, lw=1.05, label=label, color=color)
    axes[1].axhline(0, color="black", lw=0.8)
    axes[1].set_xticks(x, short, rotation=30, ha="right")
    axes[1].set_ylabel("Revised full minus comparator HV")
    axes[1].set_title("(b) Effect direction by scenario")
    fig.tight_layout()
    out = PROJECTS / "mintou_p6_bilonsga_project_review" / "manuscript" / "figures"
    save(fig, out, "fig_atomic_substitution_controls")


def main() -> None:
    style()
    p1()
    p2_hierarchy()
    p2_results()
    p3()
    p4()
    p5()
    p6()
    print("Rendered seven enhancement figures for Mintou P1--P6.")


if __name__ == "__main__":
    main()
