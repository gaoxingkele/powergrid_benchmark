"""Generate evidence-bearing gap figures for the six Mintou manuscripts.

The script reads only frozen local result CSVs.  It does not simulate, resample,
or alter experimental observations.  Each figure is written as PNG, PDF, and
SVG so the manuscript can use a raster preview while the submission package
retains vector artwork.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "papers" / "mintou"
PROJECTS = ROOT / "paper_projects"

BLUE = "#0077BB"
CYAN = "#33BBEE"
TEAL = "#009988"
ORANGE = "#EE7733"
RED = "#CC3311"
GREY = "#BBBBBB"
BLACK = "#222222"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.dpi": 160,
        "savefig.dpi": 400,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def output_dir(slug: str) -> Path:
    path = PROJECTS / slug / "manuscript" / "figures"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save(fig: plt.Figure, slug: str, stem: str) -> None:
    out = output_dir(slug)
    for suffix in ("png", "pdf", "svg"):
        fig.savefig(out / f"{stem}.{suffix}", format=suffix)
    plt.close(fig)


def styled_boxplot(ax: plt.Axes, values: list[np.ndarray], labels: list[str], colors: list[str]) -> None:
    bp = ax.boxplot(
        values,
        tick_labels=labels,
        patch_artist=True,
        widths=0.62,
        showfliers=False,
        medianprops={"color": BLACK, "linewidth": 1.2},
        whiskerprops={"color": BLACK, "linewidth": 0.8},
        capprops={"color": BLACK, "linewidth": 0.8},
        boxprops={"edgecolor": BLACK, "linewidth": 0.7},
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.78)


def p1_seed_uncertainty() -> None:
    slug = "mintou_p1_dstar_gru_dispatch"
    path = EVIDENCE / slug / "evidence" / "runs" / "real_curtailment_results.csv"
    df = pd.read_csv(path)
    methods = ["DSTAR-GRU", "Ablation-NoRetrievalBank", "MLP"]
    labels = ["DSTAR-GRU", "No retrieval", "MLP"]
    colors = [BLUE, ORANGE, GREY]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.4), constrained_layout=True)
    for col, horizon in enumerate((1, 24)):
        sub = df[(df.horizon_hours == horizon) & df.method.isin(methods)]
        mae = [sub[sub.method == method].curtailment_mae.dropna().to_numpy() for method in methods]
        onset = [sub[sub.method == method].onset_mae.dropna().to_numpy() for method in methods]
        styled_boxplot(axes[0, col], mae, labels, colors)
        styled_boxplot(axes[1, col], onset, labels, colors)
        axes[0, col].set_title(f"{horizon} h horizon")
        axes[0, col].set_ylabel("Overall MAE" if col == 0 else "")
        axes[1, col].set_ylabel("Onset MAE" if col == 0 else "")
        axes[0, col].tick_params(axis="x", rotation=18)
        axes[1, col].tick_params(axis="x", rotation=18)
        axes[0, col].grid(axis="y", color="#DDDDDD", linewidth=0.5)
        axes[1, col].grid(axis="y", color="#DDDDDD", linewidth=0.5)
    axes[0, 0].text(-0.18, 1.05, "(a)", transform=axes[0, 0].transAxes, fontweight="bold")
    axes[1, 0].text(-0.18, 1.05, "(b)", transform=axes[1, 0].transAxes, fontweight="bold")
    save(fig, slug, "fig_seed_uncertainty")


def _p2_ten_seed(dataset: str) -> pd.DataFrame:
    slug = "mintou_p2_hygraph_load_forecasting"
    runs = EVIDENCE / slug / "evidence" / "runs"
    frames: list[pd.DataFrame] = []
    if dataset == "OPSD":
        frames.extend(
            [
                pd.read_csv(runs / "real_opsd_hyg_neural_results.csv"),
                pd.read_csv(runs / "real_opsd_neural_results.csv"),
                pd.read_csv(runs / "real_opsd_v7_extra_seed_results.csv"),
            ]
        )
    elif dataset == "SimBench":
        frames.extend(
            [
                pd.read_csv(runs / "real_simbench_hyg_neural_results.csv"),
                pd.read_csv(runs / "real_simbench_neural_results.csv"),
                pd.read_csv(runs / "real_simbench_v7_extra_seed_results.csv"),
            ]
        )
    else:
        frames.append(pd.read_csv(runs / "real_ausgrid_v7_results.csv"))
    return pd.concat(frames, ignore_index=True).drop_duplicates(
        subset=["dataset", "horizon_hours", "method", "seed"], keep="last"
    )


def p2_cross_dataset_effects() -> None:
    slug = "mintou_p2_hygraph_load_forecasting"
    specs = [
        ("OPSD 1 h", _p2_ten_seed("OPSD"), 1, "mape", "MLP"),
        ("OPSD 24 h", _p2_ten_seed("OPSD"), 24, "mape", "MLP"),
        ("SimBench 1 h", _p2_ten_seed("SimBench"), 1, "normalized_mae", "MLP"),
        ("SimBench 24 h", _p2_ten_seed("SimBench"), 24, "normalized_mae", "MLP"),
        ("Ausgrid 24 h", _p2_ten_seed("Ausgrid"), 24, "smape", "DLinear"),
    ]
    rows = []
    for label, df, horizon, metric, baseline in specs:
        sub = df[df.horizon_hours == horizon]
        full = sub[sub.method == "HyG-LoadFormer (neural)"][["seed", metric]].rename(columns={metric: "full"})
        base = sub[sub.method == baseline][["seed", metric]].rename(columns={metric: "base"})
        paired = full.merge(base, on="seed", how="inner").sort_values("seed")
        delta = 100.0 * (paired.base.to_numpy() - paired.full.to_numpy()) / paired.base.to_numpy()
        rows.append((label, delta.mean(), delta.std(ddof=1), len(delta), baseline))

    fig, ax = plt.subplots(figsize=(7.0, 3.6), constrained_layout=True)
    y = np.arange(len(rows))
    means = np.array([row[1] for row in rows])
    # The bars show seed-level standard deviation, not a confidence interval.
    stds = np.array([row[2] for row in rows])
    colors = [BLUE if value > 0 else RED for value in means]
    ax.barh(y, means, xerr=stds, color=colors, alpha=0.78, edgecolor=BLACK, linewidth=0.6, capsize=3)
    ax.axvline(0, color=BLACK, linewidth=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels([row[0] for row in rows])
    ax.invert_yaxis()
    ax.set_xlabel("Relative primary-error reduction versus named baseline (%)")
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.5)
    for idx, row in enumerate(rows):
        ax.text(
            0.99,
            idx - 0.26,
            f"n={row[3]}, vs {row[4]}",
            transform=ax.get_yaxis_transform(),
            ha="right",
            va="bottom",
            fontsize=7,
        )
    save(fig, slug, "fig_cross_dataset_effects")


def p3_portfolio_composition() -> None:
    slug = "mintou_p3_samode_distribution_planning"
    path = EVIDENCE / slug / "evidence" / "tables" / "real_simbench_planning_compromise_compositions.csv"
    df = pd.read_csv(path)
    methods = ["CARS-MODE", "NSGA-II", "NSGA-II+Repair", "Standard DE"]
    sub = df[df.method.isin(methods)].groupby("method")[["reinforcement", "storage", "der", "automation"]].mean()
    sub = sub.reindex(methods)
    fig, ax = plt.subplots(figsize=(7.0, 3.8), constrained_layout=True)
    left = np.zeros(len(sub))
    palette = [BLUE, TEAL, ORANGE, GREY]
    labels = ["Reinforcement", "Storage", "DER", "Automation"]
    for column, label, color in zip(sub.columns, labels, palette):
        values = sub[column].to_numpy()
        ax.barh(sub.index, values, left=left, label=label, color=color, edgecolor="white", linewidth=0.4)
        left += values
    ax.set_xlabel("Mean projects in the reported compromise portfolio")
    ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.01))
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.5)
    ax.invert_yaxis()
    save(fig, slug, "fig_portfolio_composition")


def p4_mechanism_controls() -> None:
    slug = "mintou_p4_shield_resilience_planning"
    runs = EVIDENCE / slug / "evidence" / "runs"
    full = pd.read_csv(runs / "real_simbench_planning_results.csv")
    full = full[full.method == "SHIELD-MOEA"].copy()
    controls = pd.read_csv(runs / "real_shield_mechanism_controls_20260810.csv")
    df = pd.concat([full, controls], ignore_index=True, sort=False)
    methods = ["SHIELD-MOEA", "Control-GAOnly", "Control-DEOnly", "Control-FixedWorstK"]
    labels = ["Full", "GA only", "DE only", "Fixed worst-K"]
    colors = [BLUE, ORANGE, TEAL, GREY]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), constrained_layout=True)
    for ax, metric, title in zip(
        axes,
        ["hypervolume", "hypervolume_worst_case"],
        ["Mean-front hypervolume", "Worst-case hypervolume"],
    ):
        values = [df[df.method == method][metric].dropna().to_numpy() for method in methods]
        styled_boxplot(ax, values, labels, colors)
        ax.set_title(title)
        ax.set_ylabel("Hypervolume")
        ax.tick_params(axis="x", rotation=20)
        ax.grid(axis="y", color="#DDDDDD", linewidth=0.5)
    axes[0].text(-0.18, 1.05, "(a)", transform=axes[0].transAxes, fontweight="bold")
    axes[1].text(-0.18, 1.05, "(b)", transform=axes[1].transAxes, fontweight="bold")
    save(fig, slug, "fig_mechanism_controls")


def p5_trace_diagnostics() -> None:
    slug = "mintou_p5_trace_moea_feasibility_review"
    path = EVIDENCE / slug / "evidence" / "runs" / "real_project_review_results.csv"
    df = pd.read_csv(path)
    methods = ["TRACE-MOEA", "Ablation-NoPreferenceRanking", "Ablation-NoFeasibilityRepair", "Ablation-NSGA2Only"]
    labels = ["Full", "No preference", "No repair", "NSGA-II kernel"]
    colors = [BLUE, ORANGE, RED, GREY]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), constrained_layout=True)
    coverage = [100 * df[df.method == method].decision_coverage.dropna().to_numpy() for method in methods]
    events = [df[df.method == method].trace_event_count.dropna().to_numpy() for method in methods]
    styled_boxplot(axes[0], coverage, labels, colors)
    styled_boxplot(axes[1], events, labels, colors)
    axes[0].set_ylabel("Decision coverage (%)")
    axes[1].set_ylabel("Logged events per run")
    axes[0].set_ylim(0, 105)
    for ax in axes:
        ax.tick_params(axis="x", rotation=20)
        ax.grid(axis="y", color="#DDDDDD", linewidth=0.5)
    axes[0].text(-0.18, 1.05, "(a)", transform=axes[0].transAxes, fontweight="bold")
    axes[1].text(-0.18, 1.05, "(b)", transform=axes[1].transAxes, fontweight="bold")
    save(fig, slug, "fig_trace_diagnostics")


def p6_move_diagnostics() -> None:
    slug = "mintou_p6_bilonsga_project_review"
    path = EVIDENCE / slug / "evidence" / "runs" / "real_project_review_results.csv"
    df = pd.read_csv(path)
    methods = ["BiLo-NSGA", "Ablation-NoForwardSearch", "Ablation-NoBackwardSearch", "Ablation-ShallowLocalSearch"]
    labels = ["Full", "No forward", "No backward", "Shallow search"]
    colors = [BLUE, ORANGE, TEAL, GREY]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), constrained_layout=True)
    moves = [df[df.method == method].local_move_count.dropna().to_numpy() for method in methods]
    hv = [df[df.method == method].hypervolume.dropna().to_numpy() for method in methods]
    styled_boxplot(axes[0], moves, labels, colors)
    styled_boxplot(axes[1], hv, labels, colors)
    axes[0].set_ylabel("Accepted/logged moves per run")
    axes[1].set_ylabel("Hypervolume")
    for ax in axes:
        ax.tick_params(axis="x", rotation=20)
        ax.grid(axis="y", color="#DDDDDD", linewidth=0.5)
    axes[0].text(-0.18, 1.05, "(a)", transform=axes[0].transAxes, fontweight="bold")
    axes[1].text(-0.18, 1.05, "(b)", transform=axes[1].transAxes, fontweight="bold")
    save(fig, slug, "fig_move_diagnostics")


def main() -> None:
    p1_seed_uncertainty()
    p2_cross_dataset_effects()
    p3_portfolio_composition()
    p4_mechanism_controls()
    p5_trace_diagnostics()
    p6_move_diagnostics()
    print("generated six evidence-gap figure packages")


if __name__ == "__main__":
    main()
