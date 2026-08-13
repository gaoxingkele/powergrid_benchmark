"""Manuscript figures for mintou_p2 (CSA-LoadNet, MDPI Electronics).

Reads the v7 10-seed evidence CSVs and produces three journal-ready PNG
figures (300 dpi) in this directory:

    fig_leaderboard.png   OPSD 24h + SimBench 24h merged leaderboards
                          (mean +/- std over 10 seeds, primary metric per panel)
    fig_component.png     component-level significance summary matrix
                          (proposed vs each opponent, Holm-adjusted p,
                          5 dataset/horizon settings)
    fig_ausgrid.png       Ausgrid hierarchical 24h leaderboard, reported
                          honestly (DLinear significantly ahead of proposed)

Data sources (numbers in the manuscript are cross-checked against these):
    evidence/tables/real_opsd_v7_leaderboard.csv
    evidence/tables/real_simbench_v7_leaderboard.csv
    evidence/tables/real_ausgrid_exact_hierarchy_v8_leaderboard.csv
    evidence/tables/real_p2_v7_significance.csv

Style: matplotlib only; validated categorical palette (blue = proposed,
red reserved for "significant loss" polarity, neutral grays otherwise);
significance never encoded by color alone (cell text carries the verdict).
Evidence CSVs keep the method's pre-v7 working name "HyG-LoadFormer (neural)";
figures relabel it to the manuscript name CSA-LoadNet.
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
TABLES = REPO_ROOT / "papers" / "mintou" / "mintou_p2_hygraph_load_forecasting" / "evidence" / "tables"

OPSD_CSV = TABLES / "real_opsd_v7_leaderboard.csv"
SIMBENCH_CSV = TABLES / "real_simbench_v7_leaderboard.csv"
AUSGRID_CSV = TABLES / "real_ausgrid_exact_hierarchy_v8_leaderboard.csv"
SIG_CSV = TABLES / "real_p2_v7_significance.csv"
AUSGRID_SIG_CSV = TABLES / "real_ausgrid_exact_hierarchy_v8_significance.csv"

# ---------------------------------------------------------------------------
# Palette (validated defaults; blue = proposed, red = significant-loss pole,
# neutral grays for everything else; text always in ink, never series color)
# ---------------------------------------------------------------------------
BLUE = "#2a78d6"
BLUE_DARK = "#1c5cab"
BLUE_TINT = "#9ec5f4"
RED = "#e34948"
RED_TINT = "#f5b8b7"
GRAY_DARK = "#4d4d4a"
GRAY_MID = "#8a8a86"
GRAY_LIGHT = "#c9c9c4"
GRAY_FILL = "#e4e4e0"
NEUTRAL_CELL = "#f0efec"
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

# evidence-name -> manuscript-name
RENAME = {
    "HyG-LoadFormer (neural)": "CSA-LoadNet (proposed)",
    "Ablation-TemporalOnly (neural)": "TemporalOnly (no aggregation)",
    "Ablation-EuclideanGraph (neural)": "Euclidean weights",
    "Ablation-EqualNeighbors (neural)": "Equal-weight neighbors",
    "Ablation-FixedCurvature (neural)": "Fixed distance scale",
    "Ablation-NoCalendar (neural)": "No sequence-phase features",
    "MLP": "MLP",
    "DLinear": "DLinear",
    "TCN": "TCN",
    "PatchTST-lite": "PatchTST-lite",
    "LSTM": "LSTM",
}


def bar_style(role: str) -> tuple[str, str]:
    if role == "proposed":
        return BLUE, BLUE_DARK
    if role == "baseline":
        return GRAY_MID, GRAY_DARK
    return GRAY_FILL, GRAY_MID  # ablation


def draw_leaderboard_panel(ax, df, mean_col, std_col, xlabel):
    df = df.sort_values(mean_col, ascending=False).reset_index(drop=True)
    y = np.arange(len(df))
    colors, edges = zip(*(bar_style(r) for r in df["method_role"]))
    ax.barh(
        y, df[mean_col], xerr=df[std_col], height=0.62,
        color=list(colors), edgecolor=list(edges), linewidth=0.8,
        error_kw=dict(ecolor=GRAY_DARK, elinewidth=0.8, capsize=2.0),
    )
    labels = [
        f"{RENAME.get(m, m)}" + (f"  (n={n})" if n != 10 else "")
        for m, n in zip(df["method"], df["n_seeds"])
    ]
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7.2)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    # value labels at bar ends
    for yi, (mv, sv) in enumerate(zip(df[mean_col], df[std_col])):
        ax.annotate(f"{mv:.4f}", (mv + sv, yi), xytext=(4, 0),
                    textcoords="offset points", va="center",
                    fontsize=6.6, color=INK_MUTED)
    return df


# ---------------------------------------------------------------------------
# Figure 1: merged OPSD 24h + SimBench 24h leaderboards
# ---------------------------------------------------------------------------
def fig_leaderboard() -> None:
    opsd = pd.read_csv(OPSD_CSV)
    simb = pd.read_csv(SIMBENCH_CSV)
    opsd24 = opsd[opsd["horizon_hours"] == 24]
    simb24 = simb[simb["horizon_hours"] == 24]

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1))
    draw_leaderboard_panel(
        axes[0], opsd24, "mean_mape", "std_mape",
        "MAPE (10 seeds; lower is better)",
    )
    # honest significance verdicts live in the panel subtitles (no overlap
    # with bars) rather than floating annotations
    axes[0].set_title(
        "(a) OPSD, 24-hour-ahead point\nvs MLP: Holm p = 0.0085 (significant win)",
        fontsize=8.0, pad=5)
    axes[0].set_xlim(0, 0.043)

    draw_leaderboard_panel(
        axes[1], simb24, "mean_normalized_mae", "std_normalized_mae",
        "Normalized MAE (10 seeds; lower is better)",
    )
    axes[1].set_title(
        "(b) SimBench, 24-hour-ahead point\nvs MLP: p = 0.084 (not separable; MLP mean ahead)",
        fontsize=8.0, pad=5)
    axes[1].set_xlim(0, 0.078)

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_MID, edgecolor=GRAY_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_FILL, edgecolor=GRAY_MID),
    ]
    fig.legend(handles, ["CSA-LoadNet (proposed)", "External baseline", "Ablations"],
               loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, 1.06))
    fig.tight_layout(w_pad=2.4)
    fig.savefig(FIG_DIR / "fig_leaderboard.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: component significance summary (proposed vs opponents)
# ---------------------------------------------------------------------------
SETTINGS = [
    ("opsd", 1, "OPSD\n1 h"),
    ("opsd", 24, "OPSD\n24 h"),
    ("simbench", 1, "SimBench\n1 h"),
    ("simbench", 24, "SimBench\n24 h"),
    ("ausgrid", 24, "Ausgrid\n24 h"),
]
OPPONENT_ROWS = [
    ("MLP", "MLP (external baseline)"),
    ("Ablation-TemporalOnly (neural)", "TemporalOnly (no aggregation)"),
    ("Ablation-NoCalendar (neural)", "No sequence-phase features"),
    ("Ablation-EuclideanGraph (neural)", "Euclidean weights"),
    ("Ablation-EqualNeighbors (neural)", "Equal-weight neighbors"),
    ("Ablation-FixedCurvature (neural)", "Fixed distance scale"),
]
WEIGHT_FORM_ROWS = {3, 4, 5}  # indices of the weight-parameterization block


def fig_component() -> None:
    sig = pd.read_csv(SIG_CSV)
    # The v7 Ausgrid construction was superseded. Replace that column with
    # exact-hierarchy v8 comparisons under the common OLS reconciliation.
    sig = sig[~((sig["dataset"] == "ausgrid") & (sig["horizon_hours"] == 24))].copy()
    exact = pd.read_csv(AUSGRID_SIG_CSV)
    exact_rows = pd.DataFrame({
        "dataset": "ausgrid",
        "horizon_hours": 24,
        "comparison": exact["comparison"].str.replace(
            "CSA-LoadNet vs ", "HyG-LoadFormer (neural) vs ", regex=False),
        "p_holm": exact["p_holm"],
        "significant_005_holm": exact["significant_005_holm"],
        "proposed_better": exact["verdict"].eq("win"),
    })
    sig = pd.concat([sig, exact_rows], ignore_index=True, sort=False)
    sig["opponent"] = sig["comparison"].str.replace(
        "HyG-LoadFormer (neural) vs ", "", regex=False)

    n_rows, n_cols = len(OPPONENT_ROWS), len(SETTINGS)
    fig, ax = plt.subplots(figsize=(7.0, 3.3))

    for i, (opp_key, _) in enumerate(OPPONENT_ROWS):
        for j, (ds, hz, _) in enumerate(SETTINGS):
            row = sig[(sig["dataset"] == ds) & (sig["horizon_hours"] == hz)
                      & (sig["opponent"] == opp_key)]
            if row.empty:
                continue
            r = row.iloc[0]
            p = float(r["p_holm"])
            signif = str(r["significant_005_holm"]) == "True"
            better = str(r["proposed_better"]) == "True"
            if signif and better:
                face, edge, verdict, tcol = BLUE_TINT, BLUE_DARK, "win", BLUE_DARK
            elif signif and not better:
                face, edge, verdict, tcol = RED_TINT, RED, "loss", RED
            else:
                face, edge, verdict, tcol = NEUTRAL_CELL, GRAY_LIGHT, "n.s.", INK_MUTED
            ax.add_patch(plt.Rectangle(
                (j + 0.03, n_rows - 1 - i + 0.03), 0.94, 0.94,
                facecolor=face, edgecolor=edge,
                linewidth=1.3 if signif else 0.7))
            p_txt = "p $\\approx$ 1" if p >= 0.9995 else f"p = {p:.4g}"
            ax.text(j + 0.5, n_rows - 1 - i + 0.60, verdict,
                    ha="center", va="center", fontsize=7.6,
                    fontweight="bold" if signif else "normal", color=tcol)
            ax.text(j + 0.5, n_rows - 1 - i + 0.28, p_txt,
                    ha="center", va="center", fontsize=6.4, color=INK_MUTED)

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.set_xticks(np.arange(n_cols) + 0.5)
    ax.set_xticklabels([s[2] for s in SETTINGS], fontsize=7.6)
    ax.set_yticks(n_rows - 1 - np.arange(n_rows) + 0.5)
    ax.set_yticklabels([o[1] for o in OPPONENT_ROWS], fontsize=7.4)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "CSA-LoadNet vs opponent, Mann-Whitney U with Holm correction "
        "(10 seeds per cell)", fontsize=8.2, pad=8)

    # bracket for the weight-parameterization block
    y_top = n_rows - min(WEIGHT_FORM_ROWS)
    y_bot = n_rows - max(WEIGHT_FORM_ROWS) - 1
    ax.annotate(
        "", xy=(n_cols + 0.08, y_bot + 0.06), xytext=(n_cols + 0.08, y_top - 0.06),
        arrowprops=dict(arrowstyle="-", color=INK_MUTED, linewidth=1.0),
        annotation_clip=False)
    ax.text(n_cols + 0.18, (y_top + y_bot) / 2,
            "aggregation-weight form:\nnot separable in any setting",
            fontsize=6.9, color=INK_MUTED, va="center", ha="left")

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE_TINT, edgecolor=BLUE_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=RED_TINT, edgecolor=RED),
        plt.Rectangle((0, 0), 1, 1, facecolor=NEUTRAL_CELL, edgecolor=GRAY_LIGHT),
    ]
    fig.legend(handles,
               ["significant win (proposed better)",
                "significant loss (opponent better)",
                "not separable (Holm p $\\geq$ 0.05)"],
               loc="lower center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_component.png")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: Ausgrid hierarchical 24h leaderboard (honest negative result)
# ---------------------------------------------------------------------------
def fig_ausgrid() -> None:
    aus = pd.read_csv(AUSGRID_CSV)
    aus24 = aus[aus["reconciliation"] == "OLS-Reconciled"].copy()
    aus24["n_seeds"] = aus24["runs"]

    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    df = draw_leaderboard_panel(
        ax, aus24, "mean_hierarchy_weighted_smape", "std_hierarchy_weighted_smape",
        "Hierarchy-weighted sMAPE (mean $\\pm$ std; lower is better)",
    )
    # honest verdict carried in the subtitle (kept clear of the bars):
    # DLinear is significantly ahead of the proposed method here.
    ax.set_title(
        "Ausgrid solar-home hierarchy (17 series), 24-hour-ahead point\n"
        "DLinear vs CSA-LoadNet under OLS: Holm p = 0.000985 (proposed method loses)",
        fontsize=8.0, pad=5)
    ax.set_xlim(0, 0.34)
    _ = df

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_MID, edgecolor=GRAY_DARK),
        plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_FILL, edgecolor=GRAY_MID),
    ]
    fig.legend(handles, ["CSA-LoadNet (proposed)", "External baselines", "Ablations"],
               loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, 1.05))
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_ausgrid.png")
    plt.close(fig)


def main() -> None:
    fig_leaderboard()
    fig_component()
    fig_ausgrid()
    for name in ["fig_leaderboard", "fig_component", "fig_ausgrid"]:
        print(f"wrote {FIG_DIR / (name + '.png')}")


if __name__ == "__main__":
    main()
