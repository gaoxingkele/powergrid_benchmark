"""Generate additional evidence-bearing diagnostics for the six Mintou papers.

Every panel is derived from an already frozen CSV.  The script does not run,
filter, or tune an experiment.  It also writes the plotted aggregates so that
figure values can be checked without digitising the graphics.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PAPER_ROOT = ROOT / "paper_projects"
EVIDENCE_ROOT = ROOT / "papers" / "mintou"

SLUGS = {
    "P1": "mintou_p1_dstar_gru_dispatch",
    "P2": "mintou_p2_hygraph_load_forecasting",
    "P3": "mintou_p3_samode_distribution_planning",
    "P4": "mintou_p4_shield_resilience_planning",
    "P5": "mintou_p5_trace_moea_feasibility_review",
    "P6": "mintou_p6_bilonsga_project_review",
}

BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
RED = "#D55E00"
GREY = "#8A8A8A"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        "font.size": 8.5,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7.5,
        "figure.dpi": 150,
        "savefig.dpi": 400,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def paths(paper: str) -> tuple[Path, Path]:
    slug = SLUGS[paper]
    fig = PAPER_ROOT / slug / "manuscript" / "figures"
    tab = PAPER_ROOT / slug / "manuscript" / "derived_tables"
    fig.mkdir(parents=True, exist_ok=True)
    tab.mkdir(parents=True, exist_ok=True)
    return fig, tab


def save(fig: plt.Figure, out: Path) -> None:
    for ext in ("pdf", "svg", "png"):
        fig.savefig(out.with_suffix(f".{ext}"), facecolor="white")
    plt.close(fig)


def short(name: str) -> str:
    return (
        name.replace("Ablation-", "Abl.-")
        .replace("HyG-LoadFormer", "CSA-LoadNet")
        .replace("Feasibility", "Feas.")
        .replace("Reliability", "Reliab.")
        .replace("Renewable", "Renew.")
    )


def p1() -> None:
    fig_dir, tab_dir = paths("P1")
    src = EVIDENCE_ROOT / SLUGS["P1"] / "evidence" / "runs" / "real_curtailment_results.csv"
    d = pd.read_csv(src)
    agg = (
        d.groupby(["horizon_hours", "method", "method_role"], as_index=False)
        .agg(
            curtailment_mae=("curtailment_mae", "mean"),
            onset_mae=("onset_mae", "mean"),
            event_f1=("event_f1", "mean"),
            onset_f1=("onset_f1", "mean"),
            stress_subset_mae=("stress_subset_mae", "mean"),
            runtime_s=("runtime_s", "mean"),
            n=("seed", "count"),
        )
    )
    agg.to_csv(tab_dir / "p1_method_diagnostics.csv", index=False)

    metrics = ["curtailment_mae", "onset_mae", "stress_subset_mae", "event_f1", "onset_f1"]
    labels = ["MAE", "Onset MAE", "Stress MAE", "Event F1", "Onset F1"]
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.4), constrained_layout=True)
    for ax, horizon in zip(axes, (1, 24)):
        x = agg[agg.horizon_hours == horizon].copy()
        x["mean_rank"] = 0.0
        ranks = []
        for metric in metrics:
            ascending = not metric.endswith("f1")
            r = x[metric].rank(method="average", ascending=ascending)
            ranks.append(r.to_numpy())
        matrix = np.column_stack(ranks)
        x["mean_rank"] = matrix.mean(axis=1)
        keep = x.sort_values("mean_rank").head(9).copy()
        order = keep.index.to_numpy()
        plot_matrix = matrix[[np.where(x.index.to_numpy() == idx)[0][0] for idx in order], :]
        im = ax.imshow(plot_matrix, cmap="cividis_r", aspect="auto", vmin=1, vmax=len(x))
        ax.set_xticks(range(len(labels)), labels, rotation=28, ha="right")
        ax.set_yticks(range(len(keep)), [short(v) for v in keep.method])
        ax.set_title(f"({chr(96+horizon//23+1)}) {horizon} h: within-task metric ranks")
        for i in range(plot_matrix.shape[0]):
            for j in range(plot_matrix.shape[1]):
                ax.text(j, i, f"{plot_matrix[i,j]:.0f}", ha="center", va="center", fontsize=6.5)
    cbar = fig.colorbar(im, ax=axes, shrink=0.83, pad=0.02)
    cbar.set_label("Rank (1 = best)")
    save(fig, fig_dir / "fig_metric_rank_profile")

    learned = agg[agg.runtime_s > 0.02].copy()
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.0), constrained_layout=True)
    for ax, horizon in zip(axes, (1, 24)):
        x = learned[learned.horizon_hours == horizon]
        for _, row in x.iterrows():
            color = BLUE if row.method == "DSTAR-GRU" else (ORANGE if row.method_role == "baseline" else GREY)
            ax.scatter(row.runtime_s, row.curtailment_mae, c=color, s=35, marker="o" if row.method_role != "ablation" else "s")
            ax.annotate(short(row.method), (row.runtime_s, row.curtailment_mae), xytext=(3, 2), textcoords="offset points", fontsize=6.2)
        ax.set_xlabel("Mean run time (s)")
        ax.set_ylabel("Curtailment MAE")
        ax.set_title(f"{horizon} h horizon")
        ax.grid(axis="both", color="#E6E6E6", linewidth=0.5)
    save(fig, fig_dir / "fig_runtime_error_tradeoff")


def p2() -> None:
    fig_dir, tab_dir = paths("P2")
    frames = []
    for dataset in ("opsd", "simbench"):
        src = EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / f"real_{dataset}_rolling_results.csv"
        x = pd.read_csv(src)
        metric = "mape" if dataset == "opsd" else "normalized_mae"
        for (split_id, horizon), g in x.groupby(["split_id", "horizon_hours"]):
            prop = g[g.method_role == "proposed"].iloc[0]
            best = g[g.method_role == "baseline"].sort_values(metric).iloc[0]
            frames.append(
                {
                    "dataset": dataset.upper(),
                    "split_id": split_id,
                    "horizon_hours": horizon,
                    "metric": metric,
                    "proposed": prop[metric],
                    "best_baseline": best[metric],
                    "baseline_method": best.method,
                    "relative_change_pct": 100.0 * (best[metric] - prop[metric]) / best[metric],
                }
            )
    roll = pd.DataFrame(frames)
    roll.to_csv(tab_dir / "p2_rolling_stability.csv", index=False)
    fig, axes = plt.subplots(2, 2, figsize=(7.1, 4.7), sharey=False, constrained_layout=True)
    for ax, ((dataset, horizon), g) in zip(axes.flat, roll.groupby(["dataset", "horizon_hours"])):
        g = g.sort_values("split_id")
        ax.axhline(0, color="black", linewidth=0.7)
        ax.plot(g.split_id, g.relative_change_pct, color=BLUE, marker="o", linewidth=1.4)
        ax.fill_between(np.arange(len(g)), 0, g.relative_change_pct.to_numpy(), color=BLUE, alpha=0.12)
        ax.set_title(f"{dataset}, {int(horizon)} h")
        ax.set_ylabel("Error reduction vs. best baseline (%)")
        ax.tick_params(axis="x", rotation=20)
        ax.grid(axis="y", color="#E6E6E6", linewidth=0.5)
    save(fig, fig_dir / "fig_rolling_stability")

    srcs = [
        EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / "real_opsd_neural_results.csv",
        EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / "real_opsd_hyg_neural_results.csv",
        EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / "real_opsd_v7_extra_seed_results.csv",
        EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / "real_simbench_neural_results.csv",
        EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / "real_simbench_hyg_neural_results.csv",
        EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / "real_simbench_v7_extra_seed_results.csv",
        EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "runs" / "real_ausgrid_v7_results.csv",
    ]
    all_rows = pd.concat([pd.read_csv(p) for p in srcs], ignore_index=True, sort=False)
    all_rows["dataset_short"] = all_rows.dataset.str.split().str[0]
    agg = all_rows.groupby(["dataset_short", "horizon_hours", "method", "method_role"], as_index=False).agg(runtime_s=("runtime_s", "mean"), mae=("mae", "mean"), mape=("mape", "mean"), normalized_mae=("normalized_mae", "mean"), smape=("smape", "mean"))
    agg.to_csv(tab_dir / "p2_runtime_accuracy.csv", index=False)
    proposed = agg[agg.method.str.contains("HyG|CSA", case=False, regex=True)].copy()
    fig, ax = plt.subplots(figsize=(7.1, 3.2), constrained_layout=True)
    for _, row in proposed.iterrows():
        metric = row.mape if str(row.dataset_short).upper().startswith("OPSD") else (row.smape if str(row.dataset_short).lower().startswith("aus") else row.normalized_mae)
        ax.scatter(row.runtime_s, metric, s=55, c=BLUE if row.horizon_hours == 24 else ORANGE, marker="o" if row.horizon_hours == 24 else "s")
        ax.annotate(f"{row.dataset_short}, {int(row.horizon_hours)} h", (row.runtime_s, metric), xytext=(4, 3), textcoords="offset points", fontsize=7)
    ax.set_xscale("log")
    ax.set_xlabel("Mean run time (s, log scale)")
    ax.set_ylabel("Dataset-specific primary error")
    ax.set_title("CSA-LoadNet compute--error profile (metrics are not cross-dataset comparable)")
    ax.grid(axis="both", color="#E6E6E6", linewidth=0.5)
    save(fig, fig_dir / "fig_compute_error_profile")

    leaderboards = []
    specs = [
        ("OPSD", "real_opsd_v7_leaderboard.csv", "mean_mape"),
        ("SimBench", "real_simbench_v7_leaderboard.csv", "mean_normalized_mae"),
        ("Ausgrid", "real_ausgrid_exact_hierarchy_v8_leaderboard.csv", "mean_hierarchy_weighted_smape"),
    ]
    for dataset, filename, metric in specs:
        x = pd.read_csv(EVIDENCE_ROOT / SLUGS["P2"] / "evidence" / "tables" / filename)
        if dataset == "Ausgrid":
            x = x[x.reconciliation.eq("OLS-Reconciled")].copy()
            x["horizon_hours"] = 24
        x["setting"] = x.horizon_hours.map(lambda h: f"{dataset}\n{int(h)} h")
        x["rank"] = x.groupby("setting")[metric].rank(method="min", ascending=True)
        x["method_short"] = x.method.map(short).str.replace(" (neural)", "", regex=False)
        leaderboards.append(x[["setting", "method_short", "rank"]])
    ranks = pd.concat(leaderboards, ignore_index=True)
    matrix = ranks.pivot_table(index="method_short", columns="setting", values="rank", aggfunc="min")
    settings = ["OPSD\n1 h", "OPSD\n24 h", "SimBench\n1 h", "SimBench\n24 h", "Ausgrid\n24 h"]
    matrix = matrix.reindex(columns=settings)
    matrix["mean"] = matrix.mean(axis=1, skipna=True)
    matrix = matrix.sort_values("mean").drop(columns="mean").head(11)
    matrix.to_csv(tab_dir / "p2_cross_setting_ranks.csv")
    masked = np.ma.masked_invalid(matrix.to_numpy(dtype=float))
    cmap = mpl.colormaps["cividis_r"].copy()
    cmap.set_bad("#F3F3F3")
    fig, ax = plt.subplots(figsize=(7.1, 4.0), constrained_layout=True)
    im = ax.imshow(masked, cmap=cmap, aspect="auto", vmin=1, vmax=max(10, np.nanmax(masked)))
    ax.set_xticks(range(len(settings)), settings)
    ax.set_yticks(range(len(matrix)), matrix.index.tolist())
    ax.set_title("Method ranks where reported across five primary dataset--horizon settings")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix.iloc[i, j]
            ax.text(j, i, "--" if pd.isna(value) else f"{value:.0f}", ha="center", va="center", fontsize=6.5)
    cbar = fig.colorbar(im, ax=ax, shrink=.8)
    cbar.set_label("Rank (1 = lowest primary error)")
    save(fig, fig_dir / "fig_cross_setting_ranks")


def pooled_efficiency(paper: str, proposed_name: str, src_name: str = "real_simbench_planning_results.csv") -> pd.DataFrame:
    fig_dir, tab_dir = paths(paper)
    src = EVIDENCE_ROOT / SLUGS[paper] / "evidence" / "runs" / src_name
    d = pd.read_csv(src)
    agg = d.groupby(["method", "method_role"], as_index=False).agg(mean_hv=("hypervolume", "mean"), sd_hv=("hypervolume", "std"), mean_runtime_s=("runtime_s", "mean"), mean_front=("feasible_front_size", "mean"), n=("seed", "count"))
    agg.to_csv(tab_dir / f"{paper.lower()}_pooled_efficiency.csv", index=False)
    fig, ax = plt.subplots(figsize=(7.1, 3.6), constrained_layout=True)
    for _, row in agg.iterrows():
        color = BLUE if row.method == proposed_name else (ORANGE if row.method_role == "baseline" else GREY)
        ax.scatter(row.mean_runtime_s, row.mean_hv, s=24 + 1.2 * row.mean_front, c=color, alpha=0.88, marker="o" if row.method_role != "ablation" else "s")
        if row.method == proposed_name or row.method_role == "baseline":
            offsets = {
                "CARS-MODE": (4, 9), "FixedDE": (4, -11),
                "SHIELD-MOEA": (4, 9), "NSGA-II": (4, -13),
                "NSGA-II+Repair": (4, -3), "Deterministic Planning": (4, 8),
                "Weighted Sum": (4, -9),
            }
            dx, dy = offsets.get(row.method, (3, 2))
            ax.annotate(short(row.method), (row.mean_runtime_s, row.mean_hv), xytext=(dx, dy), textcoords="offset points", fontsize=6.5)
    ax.set_xlabel("Mean run time (s)")
    ax.set_ylabel("Pooled mean hypervolume")
    ax.set_title("Quality--cost diagnostic; marker area reflects feasible-front size")
    ax.grid(axis="both", color="#E6E6E6", linewidth=0.5)
    save(fig, fig_dir / "fig_quality_cost_tradeoff")
    return d


def p3() -> None:
    d = pooled_efficiency("P3", "CARS-MODE")
    fig_dir, tab_dir = paths("P3")
    ac = pd.read_csv(EVIDENCE_ROOT / SLUGS["P3"] / "evidence" / "runs" / "real_ac_validation_results.csv")
    agg = ac.groupby("method", as_index=False).agg(ac_feasible_rate=("ac_feasible", "mean"), median_max_line_loading=("max_line_loading_pct", "median"), p95_max_line_loading=("max_line_loading_pct", lambda s: s.quantile(.95)), min_voltage=("min_vm_pu", "min"), max_voltage=("max_vm_pu", "max"), n=("ac_feasible", "size"))
    agg.to_csv(tab_dir / "p3_ac_margin_diagnostics.csv", index=False)
    keep = agg.sort_values("ac_feasible_rate", ascending=False)
    fig, ax = plt.subplots(figsize=(7.1, 3.4), constrained_layout=True)
    colors = [BLUE if x == "CARS-MODE" else (GREEN if x == "NoPlan" else GREY) for x in keep.method]
    ax.bar(np.arange(len(keep)) - .18, keep.median_max_line_loading, .36, color=colors, label="Median")
    ax.bar(np.arange(len(keep)) + .18, keep.p95_max_line_loading, .36, color=colors, alpha=.55, hatch="//", label="95th percentile")
    ax.axhline(100, color=RED, linestyle="--", linewidth=1, label="Thermal limit")
    ax.set_xticks(np.arange(len(keep)), [short(x) for x in keep.method], rotation=28, ha="right")
    ax.set_ylabel("Maximum line loading (%)")
    ax.set_title("AC operating-margin distribution across 72 validation cases per method")
    ax.legend(ncol=3, frameon=False)
    save(fig, fig_dir / "fig_ac_margin_distribution")


def p4() -> None:
    d = pooled_efficiency("P4", "SHIELD-MOEA")
    fig_dir, tab_dir = paths("P4")
    agg = d.groupby(["method", "method_role"], as_index=False).agg(reliability=("compromise_reliability", "mean"), survivability=("compromise_survivability", "mean"), worst_hv=("hypervolume_worst_case", "mean"), runtime_s=("runtime_s", "mean"))
    agg.to_csv(tab_dir / "p4_resilience_tradeoff.csv", index=False)
    fig, ax = plt.subplots(figsize=(7.1, 3.5), constrained_layout=True)
    for _, row in agg.iterrows():
        color = BLUE if row.method == "SHIELD-MOEA" else (ORANGE if row.method_role == "baseline" else GREY)
        ax.scatter(row.reliability, row.survivability, s=35 + 300 * max(row.worst_hv, 0), c=color, alpha=.85)
        label_offsets = {
            "SHIELD-MOEA": (5, 10), "NSGA-II": (5, -13),
            "Ablation-NoScenarioScreen": (-82, -12),
            "Ablation-NoResilienceObj": (-82, 10),
        }
        if row.method in label_offsets:
            dx, dy = label_offsets[row.method]
            ax.annotate(short(row.method), (row.reliability, row.survivability), xytext=(dx, dy), textcoords="offset points", fontsize=6.2)
    ax.set_xlabel("Mean compromise reliability proxy")
    ax.set_ylabel("Mean compromise survivability proxy")
    ax.set_title("Reliability--survivability composition; marker area reflects worst-case HV")
    ax.grid(axis="both", color="#E6E6E6", linewidth=.5)
    save(fig, fig_dir / "fig_resilience_tradeoff")


def portfolio_diagnostics(paper: str, proposed_name: str) -> None:
    fig_dir, tab_dir = paths(paper)
    base = EVIDENCE_ROOT / SLUGS[paper] / "evidence"
    d = pd.read_csv(base / "runs" / "real_project_review_results.csv")
    agg = d.groupby(["method", "method_role"], as_index=False).agg(mean_hv=("hypervolume", "mean"), mean_runtime_s=("runtime_s", "mean"), mean_moves=("local_move_count", "mean"), mean_trace_events=("trace_event_count", "mean"), mean_coverage=("decision_coverage", "mean"), n=("seed", "count"))
    agg.to_csv(tab_dir / f"{paper.lower()}_search_audit_efficiency.csv", index=False)
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.3), constrained_layout=True)
    for _, row in agg.iterrows():
        color = BLUE if row.method == proposed_name else (ORANGE if row.method_role == "baseline" else GREY)
        marker = "o" if row.method_role != "ablation" else "s"
        axes[0].scatter(row.mean_runtime_s, row.mean_hv, c=color, marker=marker, s=35)
        axes[1].scatter(row.mean_trace_events, row.mean_coverage, c=color, marker=marker, s=35)
        if row.method in {proposed_name, "NSGA-II", "AHP-TOPSIS"}:
            offsets = {proposed_name: (3, 4), "NSGA-II": (3, -10), "AHP-TOPSIS": (3, 3)}
            axes[0].annotate(short(row.method), (row.mean_runtime_s, row.mean_hv), xytext=offsets[row.method], textcoords="offset points", fontsize=6.1)
        if row.method == proposed_name:
            axes[1].annotate(short(row.method), (row.mean_trace_events, row.mean_coverage), xytext=(3, 3), textcoords="offset points", fontsize=6.1)
    axes[0].set_xlabel("Mean run time (s)")
    axes[0].set_ylabel("Pooled mean hypervolume")
    axes[0].set_title("(a) Search quality and run time")
    axes[1].set_xlabel("Mean trace events per run")
    axes[1].set_ylabel("Mean decision coverage")
    axes[1].set_title("(b) Audit volume and coverage")
    axes[1].annotate("baselines: no trace", (0, 0), xytext=(6, 6), textcoords="offset points", fontsize=6.0, color="#555555")
    for ax in axes:
        ax.grid(axis="both", color="#E6E6E6", linewidth=.5)
    save(fig, fig_dir / "fig_search_audit_efficiency")

    m = pd.read_csv(base / "tables" / "real_mtep_backtest.csv")
    key = m[(m.method == proposed_name) | (m.method_role == "baseline")].copy()
    key.to_csv(tab_dir / f"{paper.lower()}_mtep_outcome_summary.csv", index=False)
    scenarios = list(key.experiment_id.drop_duplicates())
    baseline_order = (key[key.method_role == "baseline"].groupby("method").outcome_capture_broad.mean().sort_values(ascending=False).head(5).index.tolist())
    method_order = list(reversed([proposed_name] + baseline_order))
    fig, axes = plt.subplots(1, len(scenarios), figsize=(7.1, 3.6), sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    for ax, scenario in zip(axes, scenarios):
        x = key[(key.experiment_id == scenario) & key.method.isin(method_order)].copy()
        x["method"] = pd.Categorical(x.method, categories=method_order, ordered=True)
        x = x.sort_values("method").reset_index(drop=True)
        y = np.arange(len(x))
        for i, row in x.iterrows():
            color = BLUE if row.method == proposed_name else GREY
            ax.barh(i - .17, row.outcome_capture_strict, .34, color=color, label="Strict" if i == 0 else None)
            ax.barh(i + .17, row.outcome_capture_broad, .34, color=color, alpha=.45, edgecolor="none", label="Broad" if i == 0 else None)
        ax.axvline(1.0, color=RED, linestyle="--", linewidth=.8)
        ax.set_yticks(y, [short(v) for v in x.method.tolist()])
        ax.set_xlabel("Outcome-capture ratio")
        ax.set_title(scenario.replace("_", " "))
    axes[0].legend(frameon=False, ncol=2)
    save(fig, fig_dir / "fig_mtep_outcome_backtest")


def main() -> None:
    p1()
    p2()
    p3()
    p4()
    portfolio_diagnostics("P5", "TRACE-MOEA")
    portfolio_diagnostics("P6", "BiLo-NSGA")
    print("Generated 12 diagnostics (PDF/SVG/PNG) and auditable aggregate CSVs.")


if __name__ == "__main__":
    main()
