"""Regenerate every BiLo-NSGA manuscript table and figure.

The accepted inputs are pinned by ``manuscript/RESULTS_ARTIFACT_MANIFEST.json``.
This script verifies each source byte count and SHA-256 digest before reading
data, writes the reader-facing derived CSV tables, and renders Figures 1--9 as
SVG, 300-DPI PNG, and PDF.  Legacy, matched-evaluation, matched-time,
sensitivity, and public-record scopes remain separate throughout.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[2]
ROOT = SCRIPT.parents[4]
MANUSCRIPT = PROJECT / "manuscript"
OUT = SCRIPT.parent
TABLES = MANUSCRIPT / "derived_tables"
MANIFEST_PATH = MANUSCRIPT / "RESULTS_ARTIFACT_MANIFEST.json"

BLUE = "#0077BB"
BLUE_DARK = "#005A8B"
CYAN = "#33BBEE"
TEAL = "#009988"
ORANGE = "#EE7733"
RED = "#CC3311"
MAGENTA = "#EE3377"
INK = "#222222"
INK_MUTED = "#666666"
GRAY_DARK = "#555555"
GRAY_MID = "#999999"
GRAY_LIGHT = "#D8D8D8"
GRAY_FILL = "#EFEFEF"
WHITE = "#FFFFFF"

matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "font.size": 8.0,
        "axes.labelsize": 8.5,
        "axes.titlesize": 9.0,
        "xtick.labelsize": 7.3,
        "ytick.labelsize": 7.3,
        "legend.fontsize": 7.2,
        "axes.edgecolor": GRAY_MID,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "axes.labelcolor": INK,
        "text.color": INK,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.facecolor": WHITE,
        "svg.hashsalt": "mintou-p6-results-v1",
    }
)

SCENARIOS = [
    "budget_constrained_selection",
    "reliability_prioritized_review",
    "renewable_accommodation_review",
    "dependency_constrained_review",
    "local_move_explainability",
    "ranking_robustness",
    "budget_sensitivity",
    "project_pool_scalability",
]

SCENARIO_LABELS = {
    "budget_constrained_selection": "Budget-constrained\nselection",
    "reliability_prioritized_review": "Reliability-prioritized\nreview",
    "renewable_accommodation_review": "Renewable-accommodation\nreview",
    "dependency_constrained_review": "Group-filtered\nreview",
    "local_move_explainability": "Local-move\nscenario",
    "ranking_robustness": "Ranking\nrobustness",
    "budget_sensitivity": "0.75x budget\nscenario",
    "project_pool_scalability": "1.20x large-pool\nscenario",
}

SCENARIO_CONTRACT = {
    "budget_constrained_selection": (0.88, "full pool"),
    "reliability_prioritized_review": (1.00, "reliability-related kinds only"),
    "renewable_accommodation_review": (1.00, "renewable/storage kinds only"),
    "dependency_constrained_review": (1.00, "repeated group labels; no co-selection constraint"),
    "local_move_explainability": (1.00, "full pool"),
    "ranking_robustness": (1.00, "full pool"),
    "budget_sensitivity": (0.75, "full pool"),
    "project_pool_scalability": (1.20, "full pool"),
}

MAIN_METHODS = [
    "BiLo-NSGA",
    "NSGA-II",
    "NSGA-III",
    "MOEA/D",
    "AHP-TOPSIS",
    "Greedy BCR",
]

ABLATIONS = [
    "Ablation-NoForwardSearch",
    "Ablation-NoBackwardSearch",
    "Ablation-LegacyDeletion",
    "Ablation-RandomMutationOnly",
    "Ablation-NoDependencyMoves",
    "Ablation-NoFeasibilityRecovery",
    "Ablation-WeightedRankingOnly",
    "Ablation-ShallowLocalSearch",
    "Ablation-LowDependencyDensity",
    "Ablation-LooseBudget",
]

METHOD_LABELS = {
    "BiLo-NSGA": "BiLo-NSGA",
    "NSGA-II": "NSGA-II",
    "NSGA-III": "NSGA-III",
    "MOEA/D": "MOEA/D",
    "AHP-TOPSIS": "AHP-TOPSIS",
    "Greedy BCR": "Greedy BCR",
    "Random Feasible": "Random Feasible",
    "Pareto Local Search": "Pareto Local Search",
    "Ablation-NoForwardSearch": "No forward insertion",
    "Ablation-NoBackwardSearch": "No atomic substitution",
    "Ablation-LegacyDeletion": "Legacy standalone deletion",
    "Ablation-RandomMutationOnly": "Random mutation only",
    "Ablation-NoDependencyMoves": "No group bonus",
    "Ablation-NoFeasibilityRecovery": "No feasibility recovery",
    "Ablation-WeightedRankingOnly": "Weighted ranking only",
    "Ablation-ShallowLocalSearch": "Local depth 2",
    "Ablation-LowDependencyDensity": "Isolated group labels",
    "Ablation-LooseBudget": "Loose search budget",
}

METHOD_DESCRIPTIONS = {
    "BiLo-NSGA": "custom constrained NDS with forward insertion, atomic substitution, heuristic group-order bonus, and deterministic repair",
    "NSGA-II": "legacy pymoo NSGA-II on the constrained binary problem; the matched study uses the separately disclosed stage-local implementation",
    "NSGA-III": "pymoo NSGA-III with 35 Das--Dennis directions and normalized budget violation",
    "MOEA/D": "pymoo MOEA/D with 35 directions and a budget-violation penalty",
    "Greedy BCR": "scenario-weighted benefit-cost order with affordable fill",
    "AHP-TOPSIS": "scenario-weighted TOPSIS order with affordable fill",
    "Random Feasible": "seeded random order with affordable fill",
    "Pareto Local Search": "40 repaired starts and feasible add/delete/swap moves under a 1600-neighbor legacy ceiling",
    "Ablation-NoForwardSearch": "forward insertion disabled",
    "Ablation-NoBackwardSearch": "atomic substitution disabled",
    "Ablation-LegacyDeletion": "atomic substitution replaced by standalone greedy deletion",
    "Ablation-RandomMutationOnly": "local search replaced by high-rate random mutation",
    "Ablation-NoDependencyMoves": "heuristic group-order bonus disabled",
    "Ablation-NoFeasibilityRecovery": "deterministic repair disabled; constraint dominance retained",
    "Ablation-WeightedRankingOnly": "weighted ranking without evolution",
    "Ablation-ShallowLocalSearch": "local-search depth reduced to 2",
    "Ablation-LowDependencyDensity": "every third candidate assigned an isolated group label",
    "Ablation-LooseBudget": "search at 1.2x budget and evaluation at the true budget",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_sources() -> tuple[dict, dict[str, Path], dict[str, object]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    paths: dict[str, Path] = {}
    data: dict[str, object] = {}
    for key, entry in manifest["sources"].items():
        path = ROOT / Path(entry["path"])
        if not path.is_file():
            raise FileNotFoundError(f"manifest source missing: {key}: {path}")
        actual_bytes = path.stat().st_size
        if actual_bytes != int(entry["bytes"]):
            raise RuntimeError(
                f"manifest byte-count mismatch for {key}: expected {entry['bytes']}, got {actual_bytes}"
            )
        actual_hash = sha256(path)
        if actual_hash != entry["sha256"]:
            raise RuntimeError(
                f"manifest hash mismatch for {key}: expected {entry['sha256']}, got {actual_hash}"
            )
        paths[key] = path
        if path.suffix.lower() == ".csv":
            data[key] = pd.read_csv(path)
        elif path.suffix.lower() == ".json":
            data[key] = json.loads(path.read_text(encoding="utf-8"))

    legacy_config = data["legacy_config"]
    matched_config = data["matched_config_snapshot"]
    validation = data["matched_validation"]
    legacy_runs = data["legacy_runs"]
    matched_results = data["matched_results"]
    if legacy_config["status"] != manifest["legacy_run_status"]:
        raise RuntimeError("legacy run status differs from the accepted manifest")
    if matched_config["status"] != manifest["matched_stage_status"]:
        raise RuntimeError("matched-stage status differs from the accepted manifest")
    if legacy_config["experiments"] != SCENARIOS or matched_config["scenarios"] != SCENARIOS:
        raise RuntimeError("scenario order differs from the accepted contract")
    if len(legacy_runs) != 18 * 8 * 30:
        raise RuntimeError(f"legacy run count is {len(legacy_runs)}, expected 4320")
    if len(matched_results) != 2 * 3 * 8 * 30:
        raise RuntimeError(f"matched run count is {len(matched_results)}, expected 1440")
    primary = matched_results[matched_results["protocol"] == "matched_evaluation"]
    timed = matched_results[matched_results["protocol"] == "matched_time"]
    if len(primary) != 720 or not (primary["total_evaluation_units"] == 3200).all():
        raise RuntimeError("primary matched rows do not all use exactly 3200 units")
    if len(timed) != 720 or not np.allclose(timed["target_search_runtime_s"], 0.2):
        raise RuntimeError("matched-time rows do not all use the 0.20-second target")
    required_flags = [
        "all_fronts_nonempty",
        "all_hypervolumes_finite",
        "all_matched_evaluation_rows_exact_budget",
        "p5_evidence_unchanged",
    ]
    if not all(bool(validation.get(flag)) for flag in required_flags):
        raise RuntimeError("matched validation record does not satisfy all accepted flags")
    return manifest, paths, data


def write_csv(frame: pd.DataFrame, name: str) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    frame.to_csv(TABLES / name, index=False, float_format="%.10g", lineterminator="\n")


def _ordered(frame: pd.DataFrame, column: str, values: list[str]) -> pd.DataFrame:
    out = frame.copy()
    out["_order"] = pd.Categorical(out[column], categories=values, ordered=True)
    return out.sort_values("_order").drop(columns="_order")


def generate_tables(data: dict[str, object]) -> dict[str, pd.DataFrame]:
    source = data["source_profile"].iloc[0]
    candidate_table = pd.DataFrame(
        [
            {
                "source": "RTS-GMLC",
                "public_artifact": "bus, branch, and generator source data with zone aggregates",
                "candidates": str(int(source["rts_candidate_count"])),
                "archetypes": "transmission reinforcement; reliability automation; renewable support",
            },
            {
                "source": "SimBench",
                "public_artifact": "complete mixed network; 16 highest-stress subnets",
                "candidates": str(int(source["simbench_candidate_count"])),
                "archetypes": "distribution reinforcement; storage flexibility; protection automation",
            },
            {
                "source": "NERC/C2GES report cache",
                "public_artifact": f"metadata for {int(source['nerc_document_count'])} reports ({int(source['nerc_event_reports'])} event reports)",
                "candidates": "attribute adjustment only",
                "archetypes": "not applicable",
            },
            {
                "source": "Total",
                "public_artifact": "",
                "candidates": str(int(source["candidate_count"])),
                "archetypes": "6 kinds",
            },
        ]
    )
    write_csv(candidate_table, "p6_candidate_pool_composition.csv")

    matched_results = data["matched_results"]
    scenario_rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        multiplier, description = SCENARIO_CONTRACT[scenario]
        counts = matched_results.loc[
            matched_results["scenario"] == scenario, "candidate_pool_size"
        ].drop_duplicates()
        if len(counts) != 1:
            raise RuntimeError(f"candidate-pool size is not unique for {scenario}")
        scenario_rows.append(
            {
                "scenario": scenario,
                "budget_multiplier": multiplier,
                "candidate_pool_size": int(counts.iloc[0]),
                "candidate_pool": description,
            }
        )
    scenario_table = pd.DataFrame(scenario_rows)
    write_csv(scenario_table, "p6_scenario_contract.csv")

    legacy_config = data["legacy_config"]
    legacy_runs = data["legacy_runs"].copy()
    roles = legacy_runs.groupby("method")["method_role"].first().to_dict()
    method_rows = []
    for method in legacy_config["methods"]:
        method_rows.append(
            {
                "method": method,
                "role": roles[method],
                "description": METHOD_DESCRIPTIONS[method],
            }
        )
    method_table = pd.DataFrame(method_rows)
    write_csv(method_table, "p6_method_contract.csv")

    leaderboard = (
        legacy_runs.groupby(["method", "method_role"], as_index=False)
        .agg(
            runs=("hypervolume", "size"),
            mean_hypervolume=("hypervolume", "mean"),
            std_hypervolume=("hypervolume", lambda x: x.std(ddof=1)),
            mean_runtime_s=("runtime_s", "mean"),
            mean_accepted_move_repair_events=("trace_event_count", "mean"),
            mean_position_cooccurrence=("decision_coverage", "mean"),
        )
        .sort_values("mean_hypervolume", ascending=False)
    )
    leaderboard["comparison_scope"] = "legacy fixed-generation pooled descriptive"
    write_csv(leaderboard, "p6_legacy_leaderboard.csv")

    search_audit = leaderboard[
        [
            "method",
            "method_role",
            "mean_hypervolume",
            "mean_runtime_s",
            "mean_accepted_move_repair_events",
            "mean_position_cooccurrence",
            "runs",
        ]
    ].rename(
        columns={
            "mean_hypervolume": "mean_hv",
            "mean_accepted_move_repair_events": "mean_trace_events",
            "mean_position_cooccurrence": "mean_coverage",
            "runs": "n",
        }
    )
    search_audit["mean_moves"] = search_audit["mean_trace_events"]
    search_audit = search_audit[
        [
            "method",
            "method_role",
            "mean_hv",
            "mean_runtime_s",
            "mean_moves",
            "mean_trace_events",
            "mean_coverage",
            "n",
        ]
    ]
    write_csv(search_audit, "p6_search_audit_efficiency.csv")

    inference = data["legacy_inference"].copy()
    nsga = inference[inference["opponent"] == "NSGA-II"].copy()
    nsga = _ordered(nsga, "experiment_id", SCENARIOS)
    nsga["multiplicity_family"] = "14 stochastic opponents within scenario"
    write_csv(nsga, "p6_legacy_nsga2_scenarios.csv")

    mtep = data["mtep_descriptive"].copy()
    mtep_methods = [
        "AHP-TOPSIS",
        "Ablation-NoFeasibilityRecovery",
        "Ablation-LowDependencyDensity",
        "BiLo-NSGA",
        "Pareto Local Search",
        "NSGA-III",
        "Greedy BCR",
        "NSGA-II",
        "Random Feasible",
    ]
    mtep_table = mtep[
        (mtep["experiment_id"] == "budget_constrained_selection")
        & mtep["method"].isin(mtep_methods)
    ].copy()
    mtep_table = _ordered(mtep_table, "method", mtep_methods)
    mtep_table["comparison_scope"] = (
        "descriptive public-record consistency; project-level dependence not preserved"
    )
    write_csv(mtep_table, "p6_mtep_outcome_summary.csv")

    trade_methods = [
        "BiLo-NSGA",
        "Ablation-NoBackwardSearch",
        "Ablation-LegacyDeletion",
        "Ablation-NoForwardSearch",
        "NSGA-II",
        "AHP-TOPSIS",
    ]
    trade = leaderboard[leaderboard["method"].isin(trade_methods)].copy()
    trade = _ordered(trade, "method", trade_methods)
    bilo = trade.loc[trade["method"] == "BiLo-NSGA"].iloc[0]
    nsga_row = trade.loc[trade["method"] == "NSGA-II"].iloc[0]
    trade["relative_hypervolume_vs_bilo_pct"] = 100 * (
        trade["mean_hypervolume"] - bilo["mean_hypervolume"]
    ) / bilo["mean_hypervolume"]
    trade["runtime_factor_vs_nsga2"] = trade["mean_runtime_s"] / nsga_row["mean_runtime_s"]
    implication = {
        "BiLo-NSGA": "1.12% higher legacy HV than NSGA-II at 2.74-times runtime; unmatched tradeoff",
        "Ablation-NoBackwardSearch": "0.61% higher pooled HV than full; all eight substitution contrasts unresolved",
        "Ablation-LegacyDeletion": "0.22% higher pooled HV than full; all eight contrasts unresolved",
        "Ablation-NoForwardSearch": "higher pooled HV; full resolves only in dependency-constrained review, local-move explainability, and project-pool scalability",
        "NSGA-II": "legacy comparator; matched-evaluation ordering reverses",
        "AHP-TOPSIS": "low runtime and lower proxy-objective hypervolume",
    }
    trade["evidence_implication"] = trade["method"].map(implication)
    write_csv(trade, "p6_quality_effort_tradeoff.csv")

    matched_summary = data["matched_summary"].copy()
    matched_inference = data["matched_inference"].copy()
    matched_tables: dict[str, pd.DataFrame] = {}
    for protocol, output_name in [
        ("matched_evaluation", "p6_matched_evaluation_summary.csv"),
        ("matched_time", "p6_matched_time_summary.csv"),
    ]:
        subset = matched_summary[matched_summary["protocol"] == protocol].copy()
        wide = subset.pivot(index="scenario", columns="method", values="mean_hypervolume")
        wide = wide.reindex(SCENARIOS).reset_index()
        inf = matched_inference[matched_inference["protocol"] == protocol]
        for comparator in ["NSGA-II", "Pareto Local Search"]:
            flags = inf[inf["comparator"] == comparator].set_index("scenario")
            label = comparator.lower().replace(" ", "_").replace("-", "")
            wide[f"bilo_vs_{label}_mean_difference"] = wide["scenario"].map(
                flags["mean_difference"]
            )
            wide[f"bilo_vs_{label}_holm_p"] = wide["scenario"].map(
                flags["holm_adjusted_p"]
            )
            wide[f"bilo_vs_{label}_holm_significant"] = wide["scenario"].map(
                flags["holm_significant_0p05"]
            )
        pooled = {
            "scenario": "pooled_descriptive_mean",
            "BiLo-NSGA": subset.loc[subset["method"] == "BiLo-NSGA", "mean_hypervolume"].mean(),
            "NSGA-II": subset.loc[subset["method"] == "NSGA-II", "mean_hypervolume"].mean(),
            "Pareto Local Search": subset.loc[
                subset["method"] == "Pareto Local Search", "mean_hypervolume"
            ].mean(),
        }
        wide = pd.concat([wide, pd.DataFrame([pooled])], ignore_index=True)
        wide["comparison_scope"] = (
            "primary 16-contrast paired family" if protocol == "matched_evaluation"
            else "separate secondary 16-contrast paired family"
        )
        write_csv(wide, output_name)
        matched_tables[protocol] = wide

    component_opponents = [
        "Ablation-NoForwardSearch",
        "Ablation-NoBackwardSearch",
        "Ablation-LegacyDeletion",
    ]
    component = inference[inference["opponent"].isin(component_opponents)].copy()
    component = component[
        [
            "experiment_id",
            "opponent",
            "mean_proposed",
            "mean_opponent",
            "mean_difference",
            "relative_difference_pct",
            "p_raw",
            "p_holm_stochastic_family",
            "significant_005_holm",
        ]
    ]
    component["resolution"] = np.where(
        component["significant_005_holm"] & (component["mean_difference"] > 0),
        "resolved_full_method_win",
        np.where(
            component["significant_005_holm"] & (component["mean_difference"] < 0),
            "resolved_full_method_loss",
            "unresolved",
        ),
    )
    component["multiplicity_family"] = "14 stochastic opponents within scenario"
    component["mechanism_scope"] = np.where(
        component["opponent"] == "Ablation-NoForwardSearch",
        "forward insertion",
        "atomic substitution",
    )
    component = _ordered(component, "experiment_id", SCENARIOS)
    write_csv(component, "p6_forward_substitution_resolution.csv")

    hv = data["hypervolume_sensitivity_summary"].copy()
    hv_pooled = (
        hv.groupby(["method", "scheme"], as_index=False)
        .agg(
            mean_hypervolume=("mean_hypervolume", "mean"),
            total_out_of_bounds_points=("total_out_of_bounds_points", "sum"),
            total_front_points=("total_front_points", "sum"),
        )
    )
    hv_pooled["comparison_scope"] = "descriptive normalization and reference sensitivity"
    write_csv(hv_pooled, "p6_hypervolume_sensitivity.csv")

    local_effects = data["local_sensitivity_effects"].copy()
    local_effects["comparison_scope"] = "descriptive one-factor scan; no p-values"
    write_csv(local_effects, "p6_local_sensitivity_effects.csv")

    return {
        "candidate": candidate_table,
        "scenarios": scenario_table,
        "methods": method_table,
        "runs": legacy_runs,
        "leaderboard": leaderboard,
        "inference": inference,
        "mtep": mtep,
        "trade": trade,
        "matched_results": matched_results,
        "matched_summary": matched_summary,
        "matched_inference": matched_inference,
        "component": component,
        "hv_sensitivity": hv_pooled,
        "local_effects": local_effects,
        "nerc": data["nerc_descriptive"].copy(),
    }


def save_figure(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.svg", metadata={"Date": None})
    fig.savefig(OUT / f"{stem}.png", dpi=300, metadata={"Software": "mintou-p6-results-v1"})
    fig.savefig(
        OUT / f"{stem}.pdf",
        metadata={"Creator": "mintou-p6-results-v1", "CreationDate": None, "ModDate": None},
    )
    plt.close(fig)


def _box(ax: plt.Axes, xy: tuple[float, float], width: float, height: float, text: str,
         *, color: str = WHITE, edge: str = GRAY_DARK, fontsize: float = 8.0) -> None:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        facecolor=color,
        edgecolor=edge,
        linewidth=1.1,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fontsize)


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], *, color: str = GRAY_DARK) -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11, linewidth=1.0, color=color))


def fig_architecture() -> None:
    fig, ax = plt.subplots(figsize=(7.1, 3.7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    _box(ax, (0.03, 0.62), 0.16, 0.17, "Population\n(binary portfolios)", color=GRAY_FILL, fontsize=7.0)
    _box(ax, (0.24, 0.62), 0.16, 0.17, "Global variation\n(crossover +\nmutation)", color=GRAY_FILL, fontsize=6.8)
    _box(ax, (0.45, 0.62), 0.15, 0.17, "Deterministic\nbudget repair", color=GRAY_FILL, fontsize=7.0)
    _box(ax, (0.65, 0.68), 0.14, 0.14, "Forward insertion\nunder slack", color="#DCEFFC", edge=BLUE_DARK, fontsize=7.0)
    _box(ax, (0.65, 0.48), 0.14, 0.14, "Atomic\nremove--insert\nsubstitution", color="#F7E5DA", edge=ORANGE, fontsize=6.5)
    _box(ax, (0.84, 0.58), 0.13, 0.22, "Constraint NDS\nselection", color=GRAY_FILL, fontsize=7.0)
    for start, end in [
        ((0.19, 0.705), (0.24, 0.705)),
        ((0.40, 0.705), (0.45, 0.705)),
        ((0.60, 0.705), (0.65, 0.75)),
        ((0.60, 0.68), (0.65, 0.55)),
        ((0.79, 0.75), (0.84, 0.71)),
        ((0.79, 0.55), (0.84, 0.64)),
    ]:
        _arrow(ax, start, end)
    _box(ax, (0.53, 0.25), 0.23, 0.11, "1.06 same-group multiplier\nproposal order only", color="#FFF4CC", edge="#A67C00", fontsize=7.6)
    _arrow(ax, (0.65, 0.36), (0.70, 0.48), color="#A67C00")
    _box(ax, (0.08, 0.18), 0.32, 0.13, "Accepted-event counters\ncounts + pool-position co-occurrence", color=WHITE, edge=GRAY_MID, fontsize=7.7)
    _arrow(ax, (0.67, 0.48), (0.40, 0.285), color=GRAY_MID)
    ax.text(
        0.50,
        0.06,
        "Evidence boundary: forward insertion resolves only in three legacy scenarios; atomic-substitution effects remain unresolved.",
        ha="center",
        va="center",
        fontsize=7.3,
        color=INK_MUTED,
    )
    save_figure(fig, "fig_architecture")


def fig_hv_boxplot(runs: pd.DataFrame) -> None:
    subset = runs[runs["method"].isin(MAIN_METHODS)]
    fig, axes = plt.subplots(2, 4, figsize=(7.2, 4.7), sharey=True)
    for ax, scenario in zip(axes.flat, SCENARIOS):
        cell = subset[subset["experiment_id"] == scenario]
        values = [cell.loc[cell["method"] == method, "hypervolume"].to_numpy() for method in MAIN_METHODS]
        box = ax.boxplot(
            values,
            positions=np.arange(len(MAIN_METHODS)),
            widths=0.60,
            patch_artist=True,
            showfliers=True,
            flierprops={"marker": "o", "markersize": 1.6, "markerfacecolor": GRAY_MID, "markeredgecolor": "none"},
            medianprops={"color": INK, "linewidth": 1.0},
            whiskerprops={"color": GRAY_DARK, "linewidth": 0.7},
            capprops={"color": GRAY_DARK, "linewidth": 0.7},
        )
        for patch, method in zip(box["boxes"], MAIN_METHODS):
            patch.set_facecolor(BLUE if method == "BiLo-NSGA" else GRAY_FILL)
            patch.set_edgecolor(BLUE_DARK if method == "BiLo-NSGA" else GRAY_DARK)
        ax.set_title(SCENARIO_LABELS[scenario], fontsize=7.5)
        ax.set_xticks(np.arange(len(MAIN_METHODS)))
        ax.set_xticklabels(MAIN_METHODS, rotation=48, ha="right", fontsize=6.2)
        ax.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)
    for ax in axes[:, 0]:
        ax.set_ylabel("Feasible-front hypervolume")
    fig.legend(
        [
            plt.Rectangle((0, 0), 1, 1, facecolor=BLUE, edgecolor=BLUE_DARK),
            plt.Rectangle((0, 0), 1, 1, facecolor=GRAY_FILL, edgecolor=GRAY_DARK),
        ],
        ["BiLo-NSGA", "Legacy comparators"],
        loc="upper center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, 1.02),
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96), h_pad=1.1, w_pad=0.5)
    save_figure(fig, "fig_hv_boxplot")


def fig_budget_sensitivity(runs: pd.DataFrame) -> None:
    budget_cells = [
        (0.75, ["budget_sensitivity"]),
        (0.88, ["budget_constrained_selection"]),
        (1.00, ["local_move_explainability", "ranking_robustness"]),
        (1.20, ["project_pool_scalability"]),
    ]
    styles = {
        "BiLo-NSGA": (BLUE, "-", "o"),
        "NSGA-II": (TEAL, "--", "s"),
        "NSGA-III": (GRAY_DARK, ":", "^"),
        "MOEA/D": (GRAY_MID, "-.", "x"),
        "AHP-TOPSIS": (ORANGE, "--", "D"),
        "Greedy BCR": (GRAY_MID, ":", "v"),
    }
    fig, ax = plt.subplots(figsize=(6.7, 3.7))
    for method in MAIN_METHODS:
        means, standard_deviations = [], []
        for _, scenarios in budget_cells:
            values = runs[
                (runs["method"] == method) & runs["experiment_id"].isin(scenarios)
            ]["hypervolume"]
            means.append(values.mean())
            standard_deviations.append(values.std(ddof=1))
        color, linestyle, marker = styles[method]
        ax.errorbar(
            [cell[0] for cell in budget_cells],
            means,
            yerr=standard_deviations,
            label=method,
            color=color,
            linestyle=linestyle,
            marker=marker,
            linewidth=1.3,
            markersize=4,
            capsize=2,
        )
    ax.set_xlabel("Budget multiplier (cross-scenario index)")
    ax.set_ylabel("Feasible-front hypervolume (mean ± SD)")
    ax.set_xticks([0.75, 0.88, 1.00, 1.20], ["0.75x", "0.88x", "1.00x", "1.20x"])
    ax.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
    ax.legend(ncol=3, frameon=False, loc="upper left")
    ax.text(
        0.02,
        0.03,
        "Pools, weights, and random streams are not all held fixed; this is not a budget-only intervention.",
        transform=ax.transAxes,
        fontsize=7.0,
        color=INK_MUTED,
    )
    fig.tight_layout()
    save_figure(fig, "fig_budget_sensitivity")


def fig_ablation(runs: pd.DataFrame) -> None:
    methods = ["BiLo-NSGA"] + ABLATIONS
    stats = runs[runs["method"].isin(methods)].groupby("method")["hypervolume"].agg(["mean", "std"])
    order = ["BiLo-NSGA"] + list(stats.loc[ABLATIONS].sort_values("mean", ascending=False).index)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    y = np.arange(len(order))[::-1]
    means = stats.loc[order, "mean"].to_numpy()
    stds = stats.loc[order, "std"].to_numpy()
    ax.barh(
        y,
        means,
        xerr=stds,
        height=0.62,
        color=[BLUE if method == "BiLo-NSGA" else GRAY_LIGHT for method in order],
        edgecolor=[BLUE_DARK if method == "BiLo-NSGA" else GRAY_MID for method in order],
        error_kw={"ecolor": GRAY_DARK, "elinewidth": 0.7, "capsize": 2},
    )
    full_mean = stats.loc["BiLo-NSGA", "mean"]
    ax.axvline(full_mean, color=BLUE_DARK, linestyle="--", linewidth=0.9)
    ax.set_yticks(y, ["BiLo-NSGA (full)"] + [METHOD_LABELS[m] for m in order[1:]])
    ax.set_xlabel("Legacy pooled hypervolume (mean ± SD; 8 scenarios × 30 runs)")
    ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    ax.set_axisbelow(True)
    for method in ["Ablation-NoForwardSearch", "Ablation-NoBackwardSearch", "Ablation-LegacyDeletion"]:
        index = order.index(method)
        delta = 100 * (stats.loc[method, "mean"] - full_mean) / full_mean
        ax.text(means[index] + stds[index] + 0.002, y[index], f"{delta:+.2f}%", va="center", fontsize=6.8)
    fig.tight_layout()
    save_figure(fig, "fig_ablation")


def fig_move_diagnostics(runs: pd.DataFrame) -> None:
    methods = [
        "BiLo-NSGA",
        "Ablation-NoForwardSearch",
        "Ablation-NoBackwardSearch",
        "Ablation-LegacyDeletion",
    ]
    labels = [METHOD_LABELS[m] for m in methods]
    subset = runs[runs["method"].isin(methods)]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.7))
    for ax, column, ylabel, title in [
        (axes[0], "trace_event_count", "Accepted-move/repair events per run", "Event production"),
        (axes[1], "hypervolume", "Feasible-front hypervolume", "Optimization quality"),
    ]:
        values = [subset.loc[subset["method"] == method, column].to_numpy() for method in methods]
        box = ax.boxplot(values, patch_artist=True, widths=0.58, showfliers=False)
        for index, patch in enumerate(box["boxes"]):
            patch.set_facecolor(BLUE if index == 0 else GRAY_LIGHT)
            patch.set_edgecolor(BLUE_DARK if index == 0 else GRAY_DARK)
        for median in box["medians"]:
            median.set_color(INK)
        ax.set_xticks(np.arange(1, len(methods) + 1), labels, rotation=30, ha="right")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
    fig.tight_layout()
    save_figure(fig, "fig_move_diagnostics")


def fig_nerc_backtest(nerc: pd.DataFrame) -> None:
    panels = [
        ("budget_constrained_selection", "Budget-constrained selection"),
        ("reliability_prioritized_review", "Reliability-prioritized review"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.8), sharex=True)
    for ax, (scenario, title) in zip(axes, panels):
        subset = nerc[(nerc["paper"] == "p6") & (nerc["experiment_id"] == scenario)].dropna(
            subset=["priority_capture_ratio"]
        )
        subset = subset.sort_values("priority_capture_ratio")
        y = np.arange(len(subset))
        colors = [BLUE if role == "proposed" else ORANGE if role == "baseline" else GRAY_LIGHT for role in subset["method_role"]]
        ax.barh(y, subset["priority_capture_ratio"], color=colors, edgecolor=GRAY_DARK, linewidth=0.5)
        ax.axvline(1.0, color=INK, linestyle="--", linewidth=0.9)
        ax.set_yticks(y, [METHOD_LABELS.get(method, method) for method in subset["method"]], fontsize=5.8)
        ax.set_xlabel("Priority-capture ratio")
        ax.set_title(title)
        ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    fig.legend(
        [
            plt.Rectangle((0, 0), 1, 1, color=BLUE),
            plt.Rectangle((0, 0), 1, 1, color=ORANGE),
            plt.Rectangle((0, 0), 1, 1, color=GRAY_LIGHT),
        ],
        ["BiLo-NSGA", "Baselines", "Ablations"],
        ncol=3,
        frameon=False,
        loc="upper center",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94), w_pad=1.0)
    save_figure(fig, "fig_nerc_backtest")


def fig_search_audit_efficiency(trade: pd.DataFrame) -> None:
    methods = [
        "BiLo-NSGA",
        "NSGA-II",
        "Ablation-NoForwardSearch",
        "Ablation-NoBackwardSearch",
        "Ablation-LegacyDeletion",
    ]
    subset = trade.set_index("method").reindex(methods).reset_index()
    labels = [METHOD_LABELS[m] for m in methods]
    metrics = [
        ("mean_hypervolume", "Legacy mean hypervolume", "Quality"),
        ("mean_runtime_s", "Mean runtime (s)", "Compute"),
        ("mean_accepted_move_repair_events", "Accepted-move/repair events", "Event output"),
        ("mean_position_cooccurrence", "Final-front/event position co-occurrence", "Set overlap"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.1))
    for ax, (column, ylabel, title) in zip(axes.flat, metrics):
        values = subset[column].fillna(0).to_numpy()
        x = np.arange(len(methods))
        ax.bar(
            x,
            values,
            color=[BLUE, TEAL, GRAY_LIGHT, GRAY_LIGHT, GRAY_LIGHT],
            edgecolor=[BLUE_DARK, TEAL, GRAY_DARK, GRAY_DARK, GRAY_DARK],
            linewidth=0.6,
        )
        ax.set_xticks(x, labels, rotation=32, ha="right", fontsize=6.3)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(axis="y", color=GRAY_FILL, linewidth=0.6)
        ax.set_axisbelow(True)
    axes[0, 0].text(0.5, 0.95, "+1.12% legacy HV", transform=axes[0, 0].transAxes, ha="center", va="top", color=BLUE_DARK, fontsize=7.4)
    axes[0, 1].text(0.5, 0.95, "2.74× legacy runtime", transform=axes[0, 1].transAxes, ha="center", va="top", color=BLUE_DARK, fontsize=7.4)
    axes[1, 0].text(1, 0, "not\ninstrumented", ha="center", va="bottom", fontsize=6.0, color=INK_MUTED)
    axes[1, 1].text(1, 0, "not\ninstrumented", ha="center", va="bottom", fontsize=6.0, color=INK_MUTED)
    fig.tight_layout(h_pad=1.2, w_pad=1.0)
    save_figure(fig, "fig_search_audit_efficiency")


def fig_mtep_outcome_backtest(mtep: pd.DataFrame) -> None:
    scenarios = [
        ("budget_constrained_selection", "Budget-constrained selection"),
        ("reliability_prioritized_review", "Reliability-prioritized review"),
    ]
    methods = [
        "AHP-TOPSIS",
        "BiLo-NSGA",
        "Pareto Local Search",
        "NSGA-III",
        "Greedy BCR",
        "NSGA-II",
        "MOEA/D",
        "Random Feasible",
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.0), sharey=True)
    width = 0.36
    for ax, (scenario, title) in zip(axes, scenarios):
        subset = mtep[(mtep["experiment_id"] == scenario) & mtep["method"].isin(methods)].set_index("method").reindex(methods)
        y = np.arange(len(methods))
        ax.barh(y - width / 2, subset["outcome_capture_broad"], height=width, color=BLUE, label="Broad")
        ax.barh(y + width / 2, subset["outcome_capture_strict"], height=width, color=ORANGE, label="Strict")
        ax.axvline(1.0, color=INK, linestyle="--", linewidth=0.9)
        ax.set_yticks(y, [METHOD_LABELS[m] for m in methods])
        ax.invert_yaxis()
        ax.set_xlabel("Outcome-capture ratio")
        ax.set_title(title)
        ax.grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, loc="upper center", ncol=2,
               bbox_to_anchor=(0.50, 1.01))
    fig.tight_layout(w_pad=1.0, rect=(0, 0, 1, 0.94))
    save_figure(fig, "fig_mtep_outcome_backtest")


def fig_atomic_substitution_controls(leaderboard: pd.DataFrame, inference: pd.DataFrame) -> None:
    methods = [
        "BiLo-NSGA",
        "Pareto Local Search",
        "Ablation-NoForwardSearch",
        "Ablation-NoBackwardSearch",
        "Ablation-LegacyDeletion",
    ]
    stats = leaderboard.set_index("method").reindex(methods)
    labels = [METHOD_LABELS[m] for m in methods]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.8), gridspec_kw={"width_ratios": [1.05, 1]})
    x = np.arange(len(methods))
    axes[0].bar(
        x,
        stats["mean_hypervolume"],
        yerr=stats["std_hypervolume"],
        color=[BLUE, ORANGE, GRAY_LIGHT, GRAY_LIGHT, GRAY_LIGHT],
        edgecolor=[BLUE_DARK, ORANGE, GRAY_DARK, GRAY_DARK, GRAY_DARK],
        error_kw={"elinewidth": 0.7, "capsize": 2, "ecolor": GRAY_DARK},
    )
    axes[0].set_xticks(x, labels, rotation=34, ha="right", fontsize=6.4)
    axes[0].set_ylabel("Legacy pooled hypervolume (mean ± SD)")
    axes[0].set_title("Pooled descriptive quality")
    axes[0].grid(axis="y", color=GRAY_FILL, linewidth=0.6)

    opponents = methods[1:]
    counts = []
    for opponent in opponents:
        rows = inference[inference["opponent"] == opponent]
        significant = rows["significant_005_holm"].astype(bool)
        wins = int((significant & (rows["mean_difference"] > 0)).sum())
        losses = int((significant & (rows["mean_difference"] < 0)).sum())
        counts.append((wins, losses, 8 - wins - losses))
    y = np.arange(len(opponents))
    wins = np.array([row[0] for row in counts])
    losses = np.array([row[1] for row in counts])
    unresolved = np.array([row[2] for row in counts])
    axes[1].barh(y, wins, color=TEAL, label="BiLo win")
    axes[1].barh(y, losses, left=wins, color=RED, label="BiLo loss")
    axes[1].barh(y, unresolved, left=wins + losses, color=GRAY_LIGHT, label="Unresolved")
    axes[1].set_yticks(y, [METHOD_LABELS[m] for m in opponents])
    axes[1].invert_yaxis()
    axes[1].set_xlim(0, 8)
    axes[1].set_xticks(range(0, 9, 2))
    axes[1].set_xlabel("Scenarios in legacy within-scenario family")
    axes[1].set_title("Multiplicity-adjusted resolution")
    axes[1].grid(axis="x", color=GRAY_FILL, linewidth=0.6)
    axes[1].legend(frameon=False, loc="lower right", fontsize=6.6)
    axes[1].text(
        0.02,
        -0.26,
        "Forward resolved only in dependency-constrained, local-move,\nand project-pool-scalability scenarios; substitution: 0/8.",
        transform=axes[1].transAxes,
        fontsize=6.5,
        color=INK_MUTED,
    )
    fig.tight_layout(w_pad=1.0)
    save_figure(fig, "fig_atomic_substitution_controls")


def main() -> None:
    manifest, _, data = load_sources()
    generated = generate_tables(data)
    fig_architecture()
    fig_hv_boxplot(generated["runs"])
    fig_budget_sensitivity(generated["runs"])
    fig_ablation(generated["runs"])
    fig_move_diagnostics(generated["runs"])
    fig_nerc_backtest(generated["nerc"])
    fig_search_audit_efficiency(generated["trade"])
    fig_mtep_outcome_backtest(generated["mtep"])
    fig_atomic_substitution_controls(generated["leaderboard"], generated["inference"])

    expected_tables = set(manifest["artifacts"]["tables"])
    written_tables = {path.name for path in TABLES.glob("p6_*.csv")}
    missing_tables = expected_tables - written_tables
    if missing_tables:
        raise RuntimeError(f"declared table artifacts were not written: {sorted(missing_tables)}")
    unexpected_tables = written_tables - expected_tables
    if unexpected_tables:
        raise RuntimeError(f"undeclared table artifacts remain: {sorted(unexpected_tables)}")
    for stem in manifest["artifacts"]["figures"]:
        for extension in manifest["artifacts"]["figure_formats"]:
            path = OUT / f"{stem}.{extension}"
            if not path.is_file() or path.stat().st_size == 0:
                raise RuntimeError(f"declared figure artifact missing: {path}")
    print(f"verified {len(manifest['sources'])} manifest sources")
    print(f"wrote {len(expected_tables)} derived tables and {len(manifest['artifacts']['figures'])} figures")


if __name__ == "__main__":
    main()
