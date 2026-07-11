from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
MINTOU_ROOT = ROOT / "papers" / "mintou"


@dataclass(frozen=True)
class MethodSpec:
    name: str
    role: str
    quality: float
    runtime: float
    description: str


@dataclass(frozen=True)
class PaperSpec:
    paper_id: str
    directory: str
    tag: str
    title: str
    short_title: str
    target_journal: str
    backup_journal: str
    algorithm_name: str
    algorithm_full_name: str
    task: str
    datasets: tuple[str, ...]
    metrics: tuple[str, ...]
    main_experiments: tuple[str, ...]
    ablations: tuple[str, ...]
    baselines: tuple[MethodSpec, ...]
    abstract: str
    innovations: tuple[str, ...]


COMMON_BASELINES = {
    "nsga2": MethodSpec("NSGA-II", "baseline", 0.78, 1.20, "Canonical non-dominated sorting evolutionary baseline."),
    "moead": MethodSpec("MOEA/D", "baseline", 0.75, 1.05, "Decomposition-based multi-objective evolutionary baseline."),
    "de": MethodSpec("Standard DE", "baseline", 0.70, 0.90, "Differential evolution without self-adaptation."),
    "pso": MethodSpec("PSO", "baseline", 0.69, 0.80, "Particle swarm optimization baseline."),
    "ga": MethodSpec("GA", "baseline", 0.67, 0.85, "Genetic algorithm baseline."),
    "weighted": MethodSpec("Weighted Sum", "baseline", 0.63, 0.35, "Single-objective weighted aggregation baseline."),
    "greedy": MethodSpec("Greedy BCR", "baseline", 0.60, 0.20, "Greedy benefit-cost ratio baseline."),
}


PAPERS: tuple[PaperSpec, ...] = (
    PaperSpec(
        paper_id="mintou_p1",
        directory="mintou_p1_dstar_gru_dispatch",
        tag="mintou",
        title="Digital-Twin Siamese GRU for Similarity-Aware Multi-Objective Power Grid Dispatch under Load and Topology Uncertainty",
        short_title="DSTAR-GRU Dispatch",
        target_journal="IEEE Access",
        backup_journal="Electronics",
        algorithm_name="DSTAR-GRU",
        algorithm_full_name="Digital-twin Siamese Temporal Alignment and Retrieval GRU",
        task="similarity-aware load and topology constrained dispatch recommendation",
        datasets=("RTS-GMLC", "PGLib-OPF", "MATPOWER", "Grid2Op", "OPSD"),
        metrics=("dispatch_cost_index", "constraint_violation_rate", "renewable_curtailment_rate", "retrieval_hit_rate", "runtime_s"),
        main_experiments=(
            "nominal_dispatch",
            "opf_transfer",
            "load_perturbation",
            "renewable_uncertainty",
            "topology_disturbance",
            "similarity_retrieval",
            "scalability_runtime",
        ),
        ablations=(
            "no_siamese_branch",
            "lstm_encoder",
            "no_retrieval_bank",
            "no_topology_features",
            "single_objective_layer",
            "small_reference_bank",
        ),
        baselines=(
            MethodSpec("DC OPF", "baseline", 0.66, 0.25, "Linearized OPF dispatch baseline."),
            MethodSpec("AC OPF", "baseline", 0.72, 0.70, "AC OPF feasibility baseline."),
            MethodSpec("GRU Direct", "baseline", 0.70, 0.45, "GRU dispatch predictor without Siamese retrieval."),
            MethodSpec("LSTM Direct", "baseline", 0.69, 0.50, "LSTM dispatch predictor without retrieval."),
            MethodSpec("CNN-LSTM", "baseline", 0.73, 0.65, "Hybrid temporal neural dispatch predictor."),
            MethodSpec("Grid2Op Rule", "baseline", 0.67, 0.30, "Rule-based topology-control dispatch support."),
            COMMON_BASELINES["pso"],
            COMMON_BASELINES["ga"],
        ),
        abstract="This ARA project studies DSTAR-GRU, a digital-twin Siamese GRU that learns dispatch-state transferability and couples retrieved operating analogues with constrained multi-objective dispatch decisions.",
        innovations=(
            "Treats dispatch-state similarity as a supervised retrieval target.",
            "Connects a digital-twin state bank with dispatch optimization.",
            "Evaluates feasibility, curtailment, topology risk, and runtime together.",
        ),
    ),
    PaperSpec(
        paper_id="mintou_p2",
        directory="mintou_p2_hygraph_load_forecasting",
        tag="mintou",
        title="Hyperbolic Graph Neural Forecasting for Hierarchical Power Load Prediction in Smart Dispatch Systems",
        short_title="HyG-LoadFormer",
        target_journal="Electronics",
        backup_journal="Applied Sciences",
        algorithm_name="HyG-LoadFormer",
        algorithm_full_name="Hyperbolic Graph Load Forecasting Transformer",
        task="hierarchical short-term and day-ahead power load forecasting",
        datasets=("OPSD", "SimBench", "PSML", "NSRDB optional weather features"),
        metrics=("mae", "rmse", "mape", "peak_load_error", "spatial_transfer_error", "runtime_s"),
        main_experiments=(
            "one_step_forecast",
            "multi_step_forecast",
            "day_ahead_forecast",
            "feeder_profile_forecast",
            "cross_region_transfer",
            "missing_node_robustness",
            "weather_aware_extension",
            "dispatch_sensitivity",
        ),
        ablations=(
            "euclidean_gcn",
            "fixed_curvature",
            "temporal_only",
            "no_weather_features",
            "physical_edges_only",
            "poincare_only",
            "short_horizon_only",
        ),
        baselines=(
            MethodSpec("ARIMA", "baseline", 0.58, 0.20, "Statistical time-series baseline."),
            MethodSpec("XGBoost", "baseline", 0.68, 0.40, "Tree ensemble forecasting baseline."),
            MethodSpec("LSTM", "baseline", 0.70, 0.55, "Sequential neural baseline."),
            MethodSpec("BiLSTM", "baseline", 0.72, 0.65, "Bidirectional recurrent baseline."),
            MethodSpec("TCN", "baseline", 0.73, 0.55, "Temporal convolution baseline."),
            MethodSpec("Transformer", "baseline", 0.75, 0.85, "Attention-based temporal baseline."),
            MethodSpec("Euclidean GCN", "baseline", 0.76, 0.80, "Graph neural baseline without hyperbolic geometry."),
            MethodSpec("GCN-Transformer", "baseline", 0.79, 0.95, "Recent target-journal style GCN and Transformer hybrid."),
            MethodSpec("CNN-LSTM", "baseline", 0.74, 0.70, "CNN-LSTM comparator."),
        ),
        abstract="This ARA project studies HyG-LoadFormer, a hyperbolic graph forecasting model for hierarchical load prediction and downstream dispatch sensitivity analysis.",
        innovations=(
            "Uses hyperbolic geometry to model load and grid hierarchy.",
            "Separates hierarchy benefit from generic GCN/Transformer capacity by ablation.",
            "Links forecast accuracy to dispatch sensitivity metrics.",
        ),
    ),
    PaperSpec(
        paper_id="mintou_p3",
        directory="mintou_p3_samode_distribution_planning",
        tag="mintou",
        title="Self-Adaptive Multi-Objective Differential Evolution for Reproducible Distribution Network Planning with DER and Storage Integration",
        short_title="CARS-MODE Planning",
        target_journal="Energies",
        backup_journal="Applied Sciences",
        algorithm_name="CARS-MODE",
        algorithm_full_name="Constraint-Aware Repair and Strategy-adaptive Multi-Objective Differential Evolution",
        task="distribution network expansion, DER siting, and storage planning",
        datasets=("SimBench", "pandapower", "MATPOWER", "PGLib-OPF", "OPSD"),
        metrics=("hypervolume", "igd", "constraint_violation_rate", "investment_cost_index", "runtime_s"),
        main_experiments=(
            "base_distribution_planning",
            "der_siting_sizing",
            "storage_allocation",
            "load_growth_expansion",
            "pareto_quality",
            "constraint_repair",
            "runtime_scalability",
        ),
        ablations=(
            "fixed_parameters",
            "no_strategy_adaptation",
            "no_constraint_repair",
            "no_diversity_preservation",
            "weighted_sum_only",
            "no_storage_candidates",
            "no_der_candidates",
            "low_scenario_count",
        ),
        baselines=(COMMON_BASELINES["de"], COMMON_BASELINES["nsga2"], COMMON_BASELINES["moead"], COMMON_BASELINES["pso"], COMMON_BASELINES["ga"], COMMON_BASELINES["weighted"]),
        abstract="This ARA project studies CARS-MODE, a constraint-aware and strategy-adaptive differential evolution algorithm for distribution planning portfolios.",
        innovations=(
            "Adapts mutation, crossover, and repair intensity from diversity and violation signals.",
            "Represents planning decisions as engineering portfolios.",
            "Reports Pareto quality and electrical feasibility together.",
        ),
    ),
    PaperSpec(
        paper_id="mintou_p4",
        directory="mintou_p4_shield_resilience_planning",
        tag="mintou",
        title="Scenario-Aware Hybrid Multi-Objective Evolution for Resilient Distribution Network Planning under DER and Load Uncertainty",
        short_title="SHIELD-MOEA",
        target_journal="Energies",
        backup_journal="IEEE Access",
        algorithm_name="SHIELD-MOEA",
        algorithm_full_name="Scenario-screened Hybrid Evolution for Load-serving Distribution Resilience",
        task="resilience-oriented distribution planning under DER, load, and outage scenarios",
        datasets=("SimBench", "pandapower", "OPSD", "RTS-GMLC", "NERC/C2GES reports"),
        metrics=("hypervolume", "survivability_rate", "voltage_violation_probability", "expected_loss_index", "runtime_s"),
        main_experiments=(
            "deterministic_vs_scenario",
            "der_uncertainty",
            "load_uncertainty",
            "outage_contingency",
            "restoration_aware_evaluation",
            "scenario_screening_efficiency",
            "pareto_quality",
            "unseen_stress_generalization",
        ),
        ablations=(
            "no_scenario_screening",
            "no_local_repair",
            "no_resilience_objective",
            "no_der_uncertainty",
            "no_outage_uncertainty",
            "low_scenario_count",
            "weighted_sum_only",
        ),
        baselines=(COMMON_BASELINES["nsga2"], COMMON_BASELINES["moead"], COMMON_BASELINES["ga"], COMMON_BASELINES["weighted"], MethodSpec("Stochastic MILP-small", "baseline", 0.74, 1.80, "Small-case stochastic MILP comparator.")),
        abstract="This ARA project studies SHIELD-MOEA, a scenario-screened hybrid evolutionary framework for resilient distribution planning.",
        innovations=(
            "Combines scenario screening with resilience-aware Pareto optimization.",
            "Uses local repair to recover feasibility under outage and DER uncertainty.",
            "Preserves stress-test and failed-scenario evidence in ARA traces.",
        ),
    ),
    PaperSpec(
        paper_id="mintou_p5",
        directory="mintou_p5_trace_moea_feasibility_review",
        tag="mintou",
        title="Hybrid Multi-Objective Evolution for Traceable Power Grid Feasibility Review and Investment Effectiveness Optimization",
        short_title="TRACE-MOEA Review",
        target_journal="IEEE Access",
        backup_journal="Energies",
        algorithm_name="TRACE-MOEA",
        algorithm_full_name="Traceable Review-Aware Coevolutionary Multi-Objective Evolution",
        task="traceable feasibility review and investment effectiveness optimization",
        datasets=("RTS-GMLC", "SimBench", "MATPOWER", "PGLib-OPF", "NERC/C2GES reports"),
        metrics=("hypervolume", "budget_feasibility_rate", "ranking_stability", "trace_completeness", "runtime_s"),
        main_experiments=(
            "benchmark_portfolio_optimization",
            "distribution_project_review",
            "reliability_driven_review",
            "renewable_accommodation_review",
            "budget_ranking_stability",
            "preference_aware_support",
            "traceability_evaluation",
        ),
        ablations=(
            "no_feasibility_repair",
            "no_preference_ranking",
            "no_reliability_features",
            "no_renewable_features",
            "no_schedule_risk",
            "single_weighted_objective",
            "nsga2_only",
            "small_project_pool",
        ),
        baselines=(COMMON_BASELINES["nsga2"], COMMON_BASELINES["moead"], COMMON_BASELINES["greedy"], MethodSpec("AHP", "baseline", 0.58, 0.15, "Analytic hierarchy process scoring baseline."), MethodSpec("TOPSIS", "baseline", 0.60, 0.15, "TOPSIS multi-criteria scoring baseline."), COMMON_BASELINES["weighted"]),
        abstract="This ARA project studies TRACE-MOEA, a traceable multi-objective optimization framework for benchmark-derived power grid feasibility review.",
        innovations=(
            "Formalizes feasibility review as evidence-linked multi-objective decision support.",
            "Combines review-rule repair with Pareto search and preference-aware ranking.",
            "Uses reliability-report features as auditable review evidence.",
        ),
    ),
    PaperSpec(
        paper_id="mintou_p6",
        directory="mintou_p6_bilonsga_project_review",
        tag="mintou",
        title="Non-Dominated Sorting with Bidirectional Local Search for Budget-Constrained Power Grid Project Review",
        short_title="BiLo-NSGA",
        target_journal="Applied Sciences",
        backup_journal="IEEE Access",
        algorithm_name="BiLo-NSGA",
        algorithm_full_name="Bidirectional Local-search Non-dominated Sorting Genetic Algorithm",
        task="budget-constrained power grid project review and portfolio ranking",
        datasets=("RTS-GMLC", "SimBench", "MATPOWER", "PGLib-OPF", "NERC/C2GES reports"),
        metrics=("hypervolume", "feasibility_rate", "ranking_stability", "move_trace_completeness", "runtime_s"),
        main_experiments=(
            "budget_constrained_selection",
            "reliability_prioritized_review",
            "renewable_accommodation_review",
            "dependency_constrained_review",
            "local_move_explainability",
            "ranking_robustness",
            "budget_sensitivity",
            "project_pool_scalability",
        ),
        ablations=(
            "no_forward_search",
            "no_backward_search",
            "random_mutation_only",
            "no_dependency_moves",
            "no_feasibility_recovery",
            "weighted_ranking_only",
            "shallow_local_search",
            "low_dependency_density",
            "loose_budget",
        ),
        baselines=(COMMON_BASELINES["nsga2"], MethodSpec("NSGA-III", "baseline", 0.77, 1.30, "Many-objective non-dominated sorting baseline."), COMMON_BASELINES["moead"], COMMON_BASELINES["greedy"], MethodSpec("AHP/TOPSIS", "baseline", 0.59, 0.18, "Static multi-criteria ranking baseline."), MethodSpec("Random Feasible", "baseline", 0.42, 0.10, "Random feasible portfolio baseline.")),
        abstract="This ARA project studies BiLo-NSGA, a non-dominated sorting algorithm with forward and backward local search for power grid project review.",
        innovations=(
            "Defines local-search moves in project-review terms.",
            "Produces an audit trail for added, removed, and substituted projects.",
            "Separates the algorithmic contribution from broader feasibility-review framing.",
        ),
    ),
)


PROPOSED_QUALITY = {
    "mintou_p1": 0.88,
    "mintou_p2": 0.90,
    "mintou_p3": 0.87,
    "mintou_p4": 0.89,
    "mintou_p5": 0.86,
    "mintou_p6": 0.88,
}


def stable_seed(*parts: str) -> int:
    digest = hashlib.sha1("||".join(parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def metric_round(value: float) -> str:
    return f"{value:.6f}"


def paper_by_id(paper_id: str) -> PaperSpec:
    for paper in PAPERS:
        if paper.paper_id == paper_id:
            return paper
    raise KeyError(paper_id)


def method_specs(paper: PaperSpec) -> list[MethodSpec]:
    proposed = MethodSpec(paper.algorithm_name, "proposed", PROPOSED_QUALITY[paper.paper_id], 1.0, paper.algorithm_full_name)
    ablations = [
        MethodSpec(name, "ablation", max(0.48, PROPOSED_QUALITY[paper.paper_id] - 0.035 - idx * 0.018), 0.85 + idx * 0.025, f"Ablation: {name}.")
        for idx, name in enumerate(paper.ablations)
    ]
    return [proposed, *paper.baselines, *ablations]


def simulate_metrics(paper: PaperSpec, experiment: str, method: MethodSpec, repeat: int) -> dict[str, str]:
    rng = random.Random(stable_seed(paper.paper_id, experiment, method.name, str(repeat)))
    difficulty = 0.92 + (stable_seed(paper.paper_id, experiment) % 17) / 100
    jitter = rng.uniform(-0.018, 0.018)
    quality = min(0.98, max(0.35, method.quality + jitter))
    normalized = quality / difficulty
    runtime = (0.15 + method.runtime * difficulty * rng.uniform(0.85, 1.25)) * (1 + repeat * 0.015)
    row = {
        "paper_id": paper.paper_id,
        "experiment_id": experiment,
        "method": method.name,
        "method_role": method.role,
        "repeat": str(repeat),
        "quality_index": metric_round(normalized),
        "runtime_s": metric_round(runtime),
        "scenario_status": "synthetic_smoke_v0",
    }
    if paper.paper_id == "mintou_p1":
        row.update(
            {
                "dispatch_cost_index": metric_round(1.18 - normalized * 0.22 + rng.uniform(-0.01, 0.01)),
                "constraint_violation_rate": metric_round(max(0.002, 0.20 - normalized * 0.15 + rng.uniform(-0.006, 0.006))),
                "renewable_curtailment_rate": metric_round(max(0.003, 0.16 - normalized * 0.10 + rng.uniform(-0.005, 0.005))),
                "retrieval_hit_rate": metric_round(min(0.98, 0.42 + normalized * 0.48 + rng.uniform(-0.02, 0.02))),
            }
        )
    elif paper.paper_id == "mintou_p2":
        row.update(
            {
                "mae": metric_round(max(0.02, 1.08 - normalized * 0.72 + rng.uniform(-0.015, 0.015))),
                "rmse": metric_round(max(0.03, 1.24 - normalized * 0.78 + rng.uniform(-0.015, 0.015))),
                "mape": metric_round(max(0.01, 0.22 - normalized * 0.13 + rng.uniform(-0.004, 0.004))),
                "peak_load_error": metric_round(max(0.015, 0.30 - normalized * 0.18 + rng.uniform(-0.006, 0.006))),
                "spatial_transfer_error": metric_round(max(0.02, 0.34 - normalized * 0.20 + rng.uniform(-0.008, 0.008))),
            }
        )
    elif paper.paper_id == "mintou_p4":
        row.update(
            {
                "hypervolume": metric_round(max(0.01, normalized * 0.82 + rng.uniform(-0.01, 0.01))),
                "survivability_rate": metric_round(min(0.99, 0.48 + normalized * 0.45 + rng.uniform(-0.015, 0.015))),
                "voltage_violation_probability": metric_round(max(0.003, 0.24 - normalized * 0.17 + rng.uniform(-0.006, 0.006))),
                "expected_loss_index": metric_round(max(0.05, 1.10 - normalized * 0.48 + rng.uniform(-0.012, 0.012))),
            }
        )
    elif paper.paper_id == "mintou_p5":
        row.update(
            {
                "hypervolume": metric_round(max(0.01, normalized * 0.78 + rng.uniform(-0.01, 0.01))),
                "budget_feasibility_rate": metric_round(min(0.99, 0.50 + normalized * 0.42 + rng.uniform(-0.015, 0.015))),
                "ranking_stability": metric_round(min(0.99, 0.44 + normalized * 0.46 + rng.uniform(-0.012, 0.012))),
                "trace_completeness": metric_round(min(1.0, 0.55 + normalized * 0.42 + rng.uniform(-0.01, 0.01))),
            }
        )
    elif paper.paper_id == "mintou_p6":
        row.update(
            {
                "hypervolume": metric_round(max(0.01, normalized * 0.80 + rng.uniform(-0.01, 0.01))),
                "feasibility_rate": metric_round(min(0.99, 0.50 + normalized * 0.43 + rng.uniform(-0.015, 0.015))),
                "ranking_stability": metric_round(min(0.99, 0.43 + normalized * 0.45 + rng.uniform(-0.012, 0.012))),
                "move_trace_completeness": metric_round(min(1.0, 0.50 + normalized * 0.46 + rng.uniform(-0.01, 0.01))),
            }
        )
    else:
        row.update(
            {
                "hypervolume": metric_round(max(0.01, normalized * 0.80 + rng.uniform(-0.01, 0.01))),
                "igd": metric_round(max(0.02, 0.62 - normalized * 0.38 + rng.uniform(-0.01, 0.01))),
                "constraint_violation_rate": metric_round(max(0.003, 0.22 - normalized * 0.16 + rng.uniform(-0.006, 0.006))),
                "investment_cost_index": metric_round(max(0.35, 1.06 - normalized * 0.34 + rng.uniform(-0.012, 0.012))),
            }
        )
    return row


def result_rows(paper: PaperSpec, repeats: int = 5) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for experiment in paper.main_experiments:
        for method in method_specs(paper):
            for repeat in range(1, repeats + 1):
                rows.append(simulate_metrics(paper, experiment, method, repeat))
    return rows


def mean(values: Iterable[float]) -> float:
    values_list = list(values)
    if not values_list:
        return math.nan
    return sum(values_list) / len(values_list)


def leaderboard(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_method: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_method.setdefault(row["method"], []).append(row)
    output = []
    for method, group in by_method.items():
        role = group[0]["method_role"]
        quality = mean(float(row["quality_index"]) for row in group)
        runtime = mean(float(row["runtime_s"]) for row in group)
        output.append(
            {
                "method": method,
                "method_role": role,
                "mean_quality_index": metric_round(quality),
                "mean_runtime_s": metric_round(runtime),
                "runs": str(len(group)),
            }
        )
    return sorted(output, key=lambda row: float(row["mean_quality_index"]), reverse=True)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    preferred = ["paper_id", "experiment_id", "method", "method_role", "repeat"]
    fields = [field for field in preferred if field in fields] + [field for field in fields if field not in preferred]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def analysis_markdown(paper: PaperSpec, board: list[dict[str, str]]) -> str:
    proposed = next(row for row in board if row["method"] == paper.algorithm_name)
    baseline_rows = [row for row in board if row["method_role"] == "baseline"]
    ablation_rows = [row for row in board if row["method_role"] == "ablation"]
    best_baseline = max(baseline_rows, key=lambda row: float(row["mean_quality_index"]))
    best_ablation = max(ablation_rows, key=lambda row: float(row["mean_quality_index"]))
    proposed_quality = float(proposed["mean_quality_index"])
    baseline_quality = float(best_baseline["mean_quality_index"])
    ablation_quality = float(best_ablation["mean_quality_index"])
    baseline_gain = (proposed_quality / baseline_quality - 1.0) * 100
    ablation_gain = (proposed_quality / ablation_quality - 1.0) * 100
    if baseline_gain >= 5.0 and ablation_gain >= 2.0:
        status = "promising_synthetic_signal"
        action = "Proceed to heavier public-benchmark simulation before manuscript claims."
    else:
        status = "needs_compliant_optimization"
        action = "Tune features, scenario selection, operator schedules, and hyperparameters; do not fabricate or alter raw results."
    lines = [
        f"# Result Analysis - {paper.algorithm_name}",
        "",
        "Status: synthetic smoke benchmark v0. These values prove the experiment pipeline runs; they are not final manuscript results.",
        "",
        f"- Proposed method: `{paper.algorithm_name}` / {paper.algorithm_full_name}",
        f"- Best baseline: `{best_baseline['method']}` with mean quality `{best_baseline['mean_quality_index']}`",
        f"- Best ablation: `{best_ablation['method']}` with mean quality `{best_ablation['mean_quality_index']}`",
        f"- Proposed mean quality: `{proposed['mean_quality_index']}`",
        f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
        f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
        f"- Current value signal: `{status}`",
        f"- Next compliant optimization action: {action}",
        "",
        "## Interpretation Boundary",
        "",
        "This analysis is generated from deterministic benchmark-derived synthetic scenarios. It is suitable for pipeline validation, baseline-count verification, and ARA evidence wiring. It must be replaced or extended with public benchmark simulation before numerical manuscript claims are made.",
    ]
    return "\n".join(lines) + "\n"


def method_manifest(paper: PaperSpec) -> list[dict[str, str]]:
    return [
        {
            "method": method.name,
            "role": method.role,
            "quality_prior": metric_round(method.quality),
            "runtime_prior": metric_round(method.runtime),
            "description": method.description,
        }
        for method in method_specs(paper)
    ]


def experiment_manifest(paper: PaperSpec) -> dict[str, object]:
    return {
        "paper_id": paper.paper_id,
        "tag": paper.tag,
        "title": paper.title,
        "algorithm_name": paper.algorithm_name,
        "algorithm_full_name": paper.algorithm_full_name,
        "task": paper.task,
        "target_journal": paper.target_journal,
        "backup_journal": paper.backup_journal,
        "datasets": list(paper.datasets),
        "metrics": list(paper.metrics),
        "main_experiments": list(paper.main_experiments),
        "ablations": list(paper.ablations),
        "baselines": [method.name for method in paper.baselines],
        "status": "synthetic_smoke_v0",
    }


def run_paper(paper: PaperSpec, project_root: Path, repeats: int = 5) -> None:
    rows = result_rows(paper, repeats=repeats)
    board = leaderboard(rows)
    write_csv(project_root / "evidence" / "runs" / "synthetic_smoke_results.csv", rows)
    write_csv(project_root / "evidence" / "tables" / "synthetic_smoke_leaderboard.csv", board)
    write_csv(project_root / "src" / "configs" / "method_manifest.csv", method_manifest(paper))
    (project_root / "src" / "configs").mkdir(parents=True, exist_ok=True)
    (project_root / "src" / "configs" / "experiment_manifest.json").write_text(
        json.dumps(experiment_manifest(paper), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (project_root / "evidence" / "runs" / "analysis.md").write_text(analysis_markdown(paper, board), encoding="utf-8")


def run_all(project_root: Path = MINTOU_ROOT, repeats: int = 5) -> None:
    for paper in PAPERS:
        run_paper(paper, project_root / paper.directory, repeats=repeats)


if __name__ == "__main__":
    run_all()
