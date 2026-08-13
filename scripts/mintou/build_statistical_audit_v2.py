"""Post-freeze statistical audit for the six Mintou manuscripts.

This script does not alter or rerun any frozen experiment.  It rebuilds the
inferential layer from the current run archives, removes deterministic-output
pseudo-replication from P3--P6, and adds effect estimates, confidence intervals,
and paired sensitivity analyses for the shared-seed P1/P2 designs.
"""

from __future__ import annotations

import csv
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu


ROOT = Path(__file__).resolve().parents[2]
PAPERS = ROOT / "papers" / "mintou"
OUT = ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "statistical_audit_v2"
RNG_SEED = 20260812
BOOTSTRAPS = 5000


def holm(pvalues: list[float]) -> list[float]:
    order = np.argsort(pvalues)
    adjusted = np.zeros(len(pvalues), dtype=float)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(pvalues) - rank) * pvalues[index]))
        adjusted[index] = running
    return adjusted.tolist()


def ci_mean_difference(a: np.ndarray, b: np.ndarray, *, paired: bool, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    if paired:
        delta = a - b
        samples = delta[rng.integers(0, len(delta), size=(BOOTSTRAPS, len(delta)))].mean(axis=1)
    else:
        left = a[rng.integers(0, len(a), size=(BOOTSTRAPS, len(a)))].mean(axis=1)
        right = b[rng.integers(0, len(b), size=(BOOTSTRAPS, len(b)))].mean(axis=1)
        samples = left - right
    return tuple(np.quantile(samples, [0.025, 0.975]).tolist())


def exact_signflip_p(delta: np.ndarray) -> float:
    """Exact two-sided randomization p-value from complete sign enumeration."""
    delta = np.asarray(delta, dtype=float)
    observed = abs(float(delta.mean()))
    means = []
    for signs in itertools.product((-1.0, 1.0), repeat=len(delta)):
        means.append(abs(float(np.mean(delta * np.asarray(signs)))))
    values = np.asarray(means)
    return float(np.count_nonzero(values >= observed - 1e-15) / len(values))


def paired_sign_balance(delta: np.ndarray) -> float:
    """Signed-pair balance (n_positive - n_negative) / n_nonzero.

    This is deliberately not labelled as Wilcoxon's matched-pairs
    rank-biserial correlation because it does not weight signs by ranks.
    """
    nonzero = delta[np.abs(delta) > 1e-15]
    if len(nonzero) == 0:
        return 0.0
    return float((np.count_nonzero(nonzero > 0) - np.count_nonzero(nonzero < 0)) / len(nonzero))


def write_frame(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, quoting=csv.QUOTE_MINIMAL)


def independent_audit() -> dict[str, dict[str, int]]:
    specs = {
        "p3": {
            "slug": "mintou_p3_samode_distribution_planning",
            "run": "real_simbench_planning_results.csv",
            "proposed": "CARS-MODE",
            "deterministic": {"Weighted Sum"},
            "critical": {"Ablation-FixedDE", "Ablation-NoRepair", "Ablation-NoDiversity"},
        },
        "p4": {
            "slug": "mintou_p4_shield_resilience_planning",
            "run": "real_simbench_planning_results.csv",
            "proposed": "SHIELD-MOEA",
            "deterministic": {"Deterministic Planning", "Weighted Sum"},
            "critical": {"Ablation-NoScenarioScreen", "Ablation-NoOutage", "Ablation-NoRepair"},
        },
        "p5": {
            "slug": "mintou_p5_trace_moea_feasibility_review",
            "run": "real_project_review_results.csv",
            "proposed": "TRACE-MOEA",
            "deterministic": {"AHP-TOPSIS", "Greedy BCR", "Weighted Sum"},
            "critical": {"Ablation-NoPreferenceRanking", "Ablation-NoScheduleRisk"},
        },
        "p6": {
            "slug": "mintou_p6_bilonsga_project_review",
            "run": "real_project_review_results.csv",
            "proposed": "BiLo-NSGA",
            "deterministic": {"AHP-TOPSIS", "Greedy BCR", "Ablation-WeightedRankingOnly"},
            "critical": {"Ablation-NoForwardSearch", "Ablation-NoBackwardSearch", "Ablation-LegacyDeletion"},
        },
    }
    summaries: dict[str, dict[str, int]] = {}
    for paper, spec in specs.items():
        root = PAPERS / spec["slug"]
        data = pd.read_csv(root / "evidence" / "runs" / spec["run"])
        rows: list[dict[str, object]] = []
        for experiment, block in data.groupby("experiment_id", sort=True):
            proposed = block.loc[block.method.eq(spec["proposed"]), "hypervolume"].to_numpy(float)
            eligible_indices: list[int] = []
            eligible_p: list[float] = []
            for offset, (method, group) in enumerate(block.loc[~block.method.eq(spec["proposed"])].groupby("method", sort=True)):
                other = group.hypervolume.to_numpy(float)
                role = str(group.method_role.iloc[0])
                deterministic = method in spec["deterministic"]
                row: dict[str, object] = {
                    "paper": paper,
                    "experiment_id": experiment,
                    "comparison": f"{spec['proposed']} vs {method}",
                    "opponent": method,
                    "opponent_role": role,
                    "inference_status": "descriptive_deterministic_n1" if deterministic else "inferential_stochastic",
                    "n_proposed": len(proposed),
                    "n_opponent_effective": 1 if deterministic else len(other),
                    "mean_proposed": proposed.mean(),
                    "mean_opponent": other.mean(),
                    "mean_difference": proposed.mean() - other.mean(),
                    "relative_difference_pct": (proposed.mean() / other.mean() - 1.0) * 100 if other.mean() else np.nan,
                }
                if deterministic:
                    row.update({"rank_biserial": np.nan, "mean_diff_ci_low": np.nan, "mean_diff_ci_high": np.nan, "p_raw": np.nan, "p_holm_stochastic_family": np.nan, "significant_005_holm": False})
                else:
                    u, p = mannwhitneyu(proposed, other, alternative="two-sided")
                    low, high = ci_mean_difference(proposed, other, paired=False, seed=RNG_SEED + len(rows))
                    row.update({
                        "rank_biserial": 2.0 * float(u) / (len(proposed) * len(other)) - 1.0,
                        "mean_diff_ci_low": low,
                        "mean_diff_ci_high": high,
                        "p_raw": float(p),
                        "p_holm_stochastic_family": np.nan,
                        "significant_005_holm": False,
                    })
                    eligible_indices.append(len(rows))
                    eligible_p.append(float(p))
                rows.append(row)
            for index, adjusted in zip(eligible_indices, holm(eligible_p)):
                rows[index]["p_holm_stochastic_family"] = adjusted
                rows[index]["significant_005_holm"] = adjusted < 0.05
        frame = pd.DataFrame(rows)
        write_frame(frame, OUT / f"{paper}_stochastic_only_inference.csv")
        write_frame(frame, root / "evidence" / "tables" / ("real_simbench_planning_inference_v2.csv" if paper in {"p3", "p4"} else "real_project_review_inference_v2.csv"))

        critical_rows: list[pd.DataFrame] = []
        for opponent in sorted(spec["critical"]):
            subset = frame[(frame.opponent == opponent) & (frame.inference_status == "inferential_stochastic")].copy()
            if subset.empty:
                continue
            subset["p_holm_across_scenarios"] = holm(subset.p_raw.astype(float).tolist())
            subset["significant_005_cross_scenario"] = subset.p_holm_across_scenarios < 0.05
            critical_rows.append(subset)
        if critical_rows:
            write_frame(pd.concat(critical_rows, ignore_index=True), OUT / f"{paper}_critical_ablation_cross_scenario.csv")

        baseline = frame[frame.opponent_role.eq("baseline")]
        inferential = baseline[baseline.inference_status.eq("inferential_stochastic")]
        descriptive = baseline[baseline.inference_status.eq("descriptive_deterministic_n1")]
        summaries[paper] = {
            "stochastic_baseline_comparisons": int(len(inferential)),
            "stochastic_significant_wins": int(((inferential.mean_difference > 0) & inferential.significant_005_holm).sum()),
            "stochastic_significant_losses": int(((inferential.mean_difference < 0) & inferential.significant_005_holm).sum()),
            "stochastic_positive_means": int((inferential.mean_difference > 0).sum()),
            "deterministic_descriptive_comparisons": int(len(descriptive)),
            "deterministic_positive_differences": int((descriptive.mean_difference > 0).sum()),
        }
    return summaries


def p1_paired_audit() -> pd.DataFrame:
    root = PAPERS / "mintou_p1_dstar_gru_dispatch"
    data = pd.read_csv(root / "evidence" / "runs" / "real_curtailment_results.csv")
    proposed_name = "DSTAR-GRU"
    metrics = ["curtailment_mae", "onset_mae", "onset_f1"]
    rows: list[dict[str, object]] = []
    for horizon, block in data.groupby("horizon_hours", sort=True):
        proposed_block = block[block.method.eq(proposed_name)]
        for method, group in block[~block.method.eq(proposed_name)].groupby("method", sort=True):
            common = sorted(set(proposed_block.seed).intersection(group.seed))
            if len(common) != 10:
                continue
            left = proposed_block.set_index("seed").loc[common]
            right = group.set_index("seed").loc[common]
            for metric in metrics:
                delta = left[metric].to_numpy(float) - right[metric].to_numpy(float)
                low, high = ci_mean_difference(left[metric].to_numpy(float), right[metric].to_numpy(float), paired=True, seed=RNG_SEED + len(rows))
                rows.append({
                    "horizon_hours": horizon,
                    "comparison": f"{proposed_name} vs {method}",
                    "metric": metric,
                    "n_pairs": len(common),
                    "mean_paired_difference": delta.mean(),
                    "median_paired_difference": np.median(delta),
                    "mean_diff_ci_low": low,
                    "mean_diff_ci_high": high,
                    "paired_sign_balance": paired_sign_balance(delta),
                    "exact_signflip_p": exact_signflip_p(delta),
                })
    frame = pd.DataFrame(rows)
    for (_, _), indices in frame.groupby(["horizon_hours", "metric"]).groups.items():
        frame.loc[indices, "p_holm_paired_sensitivity"] = holm(frame.loc[indices, "exact_signflip_p"].tolist())
    write_frame(frame, OUT / "p1_paired_sensitivity.csv")
    write_frame(frame, root / "evidence" / "tables" / "real_curtailment_paired_sensitivity_v2.csv")
    return frame


def p1_primary_audit() -> pd.DataFrame:
    root = PAPERS / "mintou_p1_dstar_gru_dispatch"
    data = pd.read_csv(root / "evidence" / "runs" / "real_curtailment_results.csv")
    primary = pd.read_csv(root / "evidence" / "tables" / "real_curtailment_significance.csv")
    rows: list[dict[str, object]] = []
    for index, record in primary.iterrows():
        opponent = str(record["comparison"]).split(" vs ", 1)[1]
        block = data[data.horizon_hours.eq(record["horizon_hours"])]
        left = block[block.method.eq("DSTAR-GRU")][record["metric"]].to_numpy(float)
        right = block[block.method.eq(opponent)][record["metric"]].to_numpy(float)
        if len(left) != 10 or len(right) != 10:
            continue
        low, high = ci_mean_difference(left, right, paired=False, seed=RNG_SEED + index)
        u = mannwhitneyu(left, right, alternative="two-sided").statistic
        row = record.to_dict()
        row.update({
            "mean_difference": float(left.mean() - right.mean()),
            "mean_diff_ci_low": low,
            "mean_diff_ci_high": high,
            "rank_biserial_proposed_greater": 2.0 * float(u) / (len(left) * len(right)) - 1.0,
            "ci_scope": "pointwise_multiplicity_unadjusted",
        })
        rows.append(row)
    frame = pd.DataFrame(rows)
    write_frame(frame, OUT / "p1_primary_inference.csv")
    write_frame(frame, root / "evidence" / "tables" / "real_curtailment_primary_inference_v2.csv")
    return frame


def p2_paired_audit() -> pd.DataFrame:
    root = PAPERS / "mintou_p2_hygraph_load_forecasting"
    run_root = root / "evidence" / "runs"
    rows: list[dict[str, object]] = []
    for dataset, metric in (("opsd", "mape"), ("simbench", "normalized_mae")):
        base = pd.concat([
            pd.read_csv(run_root / f"real_{dataset}_hyg_neural_results.csv"),
            pd.read_csv(run_root / f"real_{dataset}_v7_extra_seed_results.csv"),
            pd.read_csv(run_root / f"real_{dataset}_neural_results.csv").query("method == 'MLP'"),
        ], ignore_index=True)
        proposed_name = "HyG-LoadFormer (neural)"
        decision_methods = [m for m in sorted(base.method.unique()) if m == "MLP" or m.startswith("Ablation-")]
        for horizon, block in base.groupby("horizon_hours", sort=True):
            left_block = block[block.method.eq(proposed_name)]
            for method in decision_methods:
                right_block = block[block.method.eq(method)]
                common = sorted(set(left_block.seed).intersection(right_block.seed))
                if len(common) != 10:
                    continue
                left = left_block.set_index("seed").loc[common, metric].to_numpy(float)
                right = right_block.set_index("seed").loc[common, metric].to_numpy(float)
                delta = left - right
                low, high = ci_mean_difference(left, right, paired=True, seed=RNG_SEED + len(rows))
                rows.append({
                    "dataset": dataset.upper(),
                    "horizon_hours": horizon,
                    "reconciliation": "NA",
                    "comparison": f"{proposed_name} vs {method}",
                    "metric": metric,
                    "n_pairs": len(common),
                    "mean_paired_difference": delta.mean(),
                    "median_paired_difference": np.median(delta),
                    "mean_diff_ci_low": low,
                    "mean_diff_ci_high": high,
                    "paired_sign_balance": paired_sign_balance(delta),
                    "exact_signflip_p": exact_signflip_p(delta),
                })

    ausgrid = pd.read_csv(run_root / "real_ausgrid_exact_hierarchy_v8_results.csv")
    ausgrid = ausgrid[ausgrid.reconciliation.eq("OLS-Reconciled")]
    proposed_name = "HyG-LoadFormer (neural)"
    left_block = ausgrid[ausgrid.method.eq(proposed_name)]
    for method, right_block in ausgrid[~ausgrid.method.eq(proposed_name)].groupby("method", sort=True):
        common = sorted(set(left_block.seed).intersection(right_block.seed))
        left = left_block.set_index("seed").loc[common, "hierarchy_weighted_smape"].to_numpy(float)
        right = right_block.set_index("seed").loc[common, "hierarchy_weighted_smape"].to_numpy(float)
        delta = left - right
        low, high = ci_mean_difference(left, right, paired=True, seed=RNG_SEED + len(rows))
        rows.append({
            "dataset": "AUSGRID",
            "horizon_hours": 24,
            "reconciliation": "OLS-Reconciled",
            "comparison": f"{proposed_name} vs {method}",
            "metric": "hierarchy_weighted_smape",
            "n_pairs": len(common),
            "mean_paired_difference": delta.mean(),
            "median_paired_difference": np.median(delta),
            "mean_diff_ci_low": low,
            "mean_diff_ci_high": high,
            "paired_sign_balance": paired_sign_balance(delta),
            "exact_signflip_p": exact_signflip_p(delta),
        })
    frame = pd.DataFrame(rows)
    for (_, _, _), indices in frame.groupby(["dataset", "horizon_hours", "metric"]).groups.items():
        frame.loc[indices, "p_holm_paired_sensitivity"] = holm(frame.loc[indices, "exact_signflip_p"].tolist())
    write_frame(frame, OUT / "p2_paired_sensitivity.csv")
    write_frame(frame, root / "evidence" / "tables" / "real_p2_paired_sensitivity_v2.csv")
    return frame


def p2_primary_audit() -> pd.DataFrame:
    root = PAPERS / "mintou_p2_hygraph_load_forecasting"
    run_root = root / "evidence" / "runs"
    table_root = root / "evidence" / "tables"
    rows: list[dict[str, object]] = []

    current = pd.read_csv(table_root / "real_p2_v7_significance.csv")
    for dataset, metric in (("opsd", "mape"), ("simbench", "normalized_mae")):
        data = pd.concat([
            pd.read_csv(run_root / f"real_{dataset}_hyg_neural_results.csv"),
            pd.read_csv(run_root / f"real_{dataset}_v7_extra_seed_results.csv"),
            pd.read_csv(run_root / f"real_{dataset}_neural_results.csv").query("method == 'MLP'"),
        ], ignore_index=True)
        for index, record in current[current.dataset.eq(dataset)].iterrows():
            opponent = str(record["comparison"]).split(" vs ", 1)[1]
            block = data[data.horizon_hours.eq(record["horizon_hours"])]
            left = block[block.method.eq("HyG-LoadFormer (neural)")][metric].to_numpy(float)
            right = block[block.method.eq(opponent)][metric].to_numpy(float)
            if len(left) != 10 or len(right) != 10:
                continue
            low, high = ci_mean_difference(left, right, paired=False, seed=RNG_SEED + index)
            u = mannwhitneyu(left, right, alternative="two-sided").statistic
            row = record.to_dict()
            row.update({
                "mean_difference": float(left.mean() - right.mean()),
                "mean_diff_ci_low": low,
                "mean_diff_ci_high": high,
                "rank_biserial_proposed_greater": 2.0 * float(u) / (len(left) * len(right)) - 1.0,
                "ci_scope": "pointwise_multiplicity_unadjusted",
            })
            rows.append(row)

    ausgrid = pd.read_csv(run_root / "real_ausgrid_exact_hierarchy_v8_results.csv")
    ausgrid = ausgrid[ausgrid.reconciliation.eq("OLS-Reconciled")]
    primary_ausgrid = pd.read_csv(table_root / "real_ausgrid_exact_hierarchy_v8_significance.csv")
    for index, record in primary_ausgrid.iterrows():
        opponent = str(record["comparison"]).split(" vs ", 1)[1]
        left = ausgrid[ausgrid.method.eq("HyG-LoadFormer (neural)")]["hierarchy_weighted_smape"].to_numpy(float)
        right = ausgrid[ausgrid.method.eq(opponent)]["hierarchy_weighted_smape"].to_numpy(float)
        if len(left) != 10 or len(right) != 10:
            continue
        low, high = ci_mean_difference(left, right, paired=False, seed=RNG_SEED + 100 + index)
        u = mannwhitneyu(left, right, alternative="two-sided").statistic
        row = record.to_dict()
        row.update({
            "dataset": "ausgrid",
            "horizon_hours": 24,
            "metric": "hierarchy_weighted_smape",
            "mean_difference": float(left.mean() - right.mean()),
            "mean_diff_ci_low": low,
            "mean_diff_ci_high": high,
            "rank_biserial_proposed_greater": 2.0 * float(u) / (len(left) * len(right)) - 1.0,
            "ci_scope": "pointwise_multiplicity_unadjusted",
        })
        rows.append(row)
    frame = pd.DataFrame(rows)
    write_frame(frame, OUT / "p2_primary_inference.csv")
    write_frame(frame, root / "evidence" / "tables" / "real_p2_primary_inference_v2.csv")
    return frame


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summaries = independent_audit()
    p1_primary_audit()
    p1 = p1_paired_audit()
    p2_primary_audit()
    p2 = p2_paired_audit()
    lines = [
        "# Statistical Audit v2",
        "",
        "This post-freeze analysis preserves all run archives and excludes deterministic-output copies from seed-level inference.",
        f"Mean-difference intervals use {BOOTSTRAPS} bootstrap resamples with seed {RNG_SEED}; they are pointwise and multiplicity-unadjusted.",
        "P1/P2 exact sign-flip tests are paired sensitivity analyses; the frozen Mann--Whitney tests remain the prespecified primary analysis.",
        "Paired sign balance is the fraction difference between positive and negative nonzero paired differences; it is not a Wilcoxon rank-biserial effect.",
        "",
        "## Stochastic baseline counts",
        "",
        "| Paper | Eligible comparisons | Significant wins | Significant losses | Positive means | Deterministic descriptive gaps | Proposed higher in deterministic gaps |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for paper, summary in summaries.items():
        lines.append(
            f"| {paper.upper()} | {summary['stochastic_baseline_comparisons']} | {summary['stochastic_significant_wins']} | "
            f"{summary['stochastic_significant_losses']} | {summary['stochastic_positive_means']} | "
            f"{summary['deterministic_descriptive_comparisons']} | {summary['deterministic_positive_differences']} |"
        )
    lines.extend([
        "",
        "## Paired sensitivity",
        "",
        f"P1 contains {len(p1)} paired method--metric comparisons; P2 contains {len(p2)}. Detailed estimates and Holm-adjusted paired p-values are in the CSV files.",
        "",
        "## Interpretation boundary",
        "",
        "A non-significant comparison is reported as unresolved, not equivalent. Deterministic rules retain point estimates but have no seed-level p-value.",
    ])
    (OUT / "STATISTICAL_AUDIT_V2.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
