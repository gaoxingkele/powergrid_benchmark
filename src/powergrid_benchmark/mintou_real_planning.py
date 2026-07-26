"""Real-MOEA planning benchmark for mintou p3 (CARS-MODE) and p4 (SHIELD-MOEA).

v2 rewrite. The v1 pipeline scored hand-shaped ranking heuristics per method
(quality constants, method-name-conditional weights). The portfolio evaluation
itself was already method-independent, but the "algorithms" were proxies with
no variance across repeats. This version follows the same discipline as the
p5/p6 project-review rewrite:

- Problem definition (SimBench-derived candidates, objectives, budget and
  planning-target constraints, stochastic load/DER/outage scenarios) is
  identical for every method and computed only from candidate attributes.
- Every method is a real algorithm on binary plan vectors:
  * CARS-MODE: multi-objective binary Differential Evolution with jDE-style
    self-adaptive F/CR, a SaDE-style two-strategy pool with success-based
    selection, constraint-aware budget repair, and crowding-distance diversity.
  * SHIELD-MOEA: NSGA-II core with hybrid GA/DE variation, adaptive worst-K
    scenario screening during search (final evaluation always on the full
    scenario set), and local feasibility repair.
  * Baselines: pymoo NSGA-II / MOEA/D; scalarized single-objective GA, binary
    PSO, and standard DE; weighted-sum and cost-first greedy point methods.
  * Ablations toggle single real mechanisms (repair, adaptation, diversity,
    screening, objective masks, scenario stress).
- Headline metric: standard hypervolume of the feasible non-dominated front
  under fixed, method-independent normalization bounds (mean-over-scenarios
  objectives). 30 seeded runs per method/experiment; Mann-Whitney U with Holm
  correction. Compromise-plan compositions are exported for the pandapower AC
  validation stage.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu

ROOT = Path(__file__).resolve().parents[2]
SIMBENCH_NET = (
    ROOT
    / "data"
    / "public_datasets"
    / "grid_cases"
    / "simbench"
    / "simbench"
    / "networks"
    / "1-complete_data-mixed-all-0-sw"
)
P3_ROOT = ROOT / "papers" / "mintou" / "mintou_p3_samode_distribution_planning"
P4_ROOT = ROOT / "papers" / "mintou" / "mintou_p4_shield_resilience_planning"

P3_STATUS = "public_simbench_planning_v6_real_moea"
P4_STATUS = "public_simbench_planning_v2_real_moea"
N_SEEDS = 30
POP_SIZE = 40
N_GENERATIONS = 40
N_SCENARIOS = 16


# ---------------------------------------------------------------------------
# SimBench-derived candidates (unchanged data engineering, method-independent)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SubnetStats:
    subnet: str
    load_mw: float
    qload_mvar: float
    load_count: int
    res_mw: float
    line_length_km: float
    line_count: int
    avg_loading_max: float


@dataclass(frozen=True)
class Candidate:
    cid: str
    subnet: str
    kind: str
    cost: float
    loss_reduction: float
    voltage_reduction: float
    hosting_gain: float
    reliability_gain: float
    resilience_gain: float
    der_support: float


def read_semicolon_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def parse_float(value: str, default: float = 0.0) -> float:
    try:
        if value in {"", "NULL", None}:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_subnet_stats(limit: int = 18) -> list[SubnetStats]:
    loads = read_semicolon_csv(SIMBENCH_NET / "Load.csv")
    lines = read_semicolon_csv(SIMBENCH_NET / "Line.csv")
    res = read_semicolon_csv(SIMBENCH_NET / "RES.csv")
    empty = lambda: {"load_mw": 0.0, "qload_mvar": 0.0, "load_count": 0.0, "res_mw": 0.0, "line_length_km": 0.0, "line_count": 0.0, "loading_sum": 0.0}
    by_subnet: dict[str, dict[str, float]] = {}
    for row in loads:
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["load_mw"] += parse_float(row.get("pLoad", "0"))
        data["qload_mvar"] += parse_float(row.get("qLoad", "0"))
        data["load_count"] += 1
    for row in res:
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["res_mw"] += parse_float(row.get("pRES", "0"))
    for row in lines:
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["line_length_km"] += parse_float(row.get("length", "0"))
        data["line_count"] += 1
        data["loading_sum"] += parse_float(row.get("loadingMax", "100"), 100.0)
    stats = []
    for subnet, data in by_subnet.items():
        if data["load_mw"] <= 0 or data["line_count"] <= 0:
            continue
        stats.append(
            SubnetStats(
                subnet=subnet,
                load_mw=data["load_mw"],
                qload_mvar=data["qload_mvar"],
                load_count=int(data["load_count"]),
                res_mw=data["res_mw"],
                line_length_km=data["line_length_km"],
                line_count=int(data["line_count"]),
                avg_loading_max=data["loading_sum"] / max(1.0, data["line_count"]),
            )
        )
    return sorted(stats, key=lambda item: item.load_mw + 0.2 * item.line_length_km, reverse=True)[:limit]


def build_candidates(stats: list[SubnetStats]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for item in stats:
        stress = item.load_mw / max(0.2, item.line_length_km)
        der_gap = max(0.0, item.load_mw * 0.55 - item.res_mw)
        candidates.extend(
            [
                Candidate(
                    cid=f"{item.subnet}::reinforcement",
                    subnet=item.subnet,
                    kind="reinforcement",
                    cost=60 + 4.5 * item.line_length_km + 7 * item.load_mw,
                    loss_reduction=0.012 * item.line_length_km + 0.020 * stress,
                    voltage_reduction=0.020 + 0.006 * stress,
                    hosting_gain=0.06 * der_gap,
                    reliability_gain=0.018 * item.line_count,
                    resilience_gain=0.016 * item.line_count,
                    der_support=0.20,
                ),
                Candidate(
                    cid=f"{item.subnet}::storage",
                    subnet=item.subnet,
                    kind="storage",
                    cost=50 + 16 * math.sqrt(item.load_mw + 1),
                    loss_reduction=0.025 * math.sqrt(item.load_mw + 1),
                    voltage_reduction=0.018 * math.sqrt(stress + 1),
                    hosting_gain=0.12 * der_gap + 0.08 * item.load_mw,
                    reliability_gain=0.055 * math.sqrt(item.load_count + 1),
                    resilience_gain=0.070 * math.sqrt(item.load_count + 1),
                    der_support=0.80,
                ),
                Candidate(
                    cid=f"{item.subnet}::der",
                    subnet=item.subnet,
                    kind="der",
                    cost=45 + 10 * math.sqrt(item.load_mw + 1),
                    loss_reduction=0.018 * math.sqrt(item.load_mw + 1),
                    voltage_reduction=0.012,
                    hosting_gain=0.18 * der_gap + 0.10 * item.load_mw,
                    reliability_gain=0.020 * math.sqrt(item.load_count + 1),
                    resilience_gain=0.028 * math.sqrt(item.load_count + 1),
                    der_support=1.00,
                ),
                Candidate(
                    cid=f"{item.subnet}::automation",
                    subnet=item.subnet,
                    kind="automation",
                    cost=38 + 1.8 * item.line_count,
                    loss_reduction=0.006 * item.line_count,
                    voltage_reduction=0.010 * math.sqrt(stress + 1),
                    hosting_gain=0.025 * der_gap,
                    reliability_gain=0.085 * math.sqrt(item.line_count + 1),
                    resilience_gain=0.115 * math.sqrt(item.line_count + 1),
                    der_support=0.35,
                ),
            ]
        )
    return candidates


# ---------------------------------------------------------------------------
# Problem definition (method-independent, scenario-aware)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExperimentSetup:
    """Method-independent problem variant. Scenario multipliers and planning
    targets are the ONLY experiment knobs; no method identity enters."""

    budget_factor: float = 1.0
    load_factor: float = 1.0
    kind_excluded: str = ""
    hosting_target: float = 0.018
    der_target: float = 0.48
    load_range: tuple[float, float] = (0.95, 1.25)
    der_range: tuple[float, float] = (0.7, 1.3)
    outage_range: tuple[float, float] = (0.0, 0.25)
    use_expected_loss: bool = False
    eval_load_range: tuple[float, float] | None = None
    eval_der_range: tuple[float, float] | None = None
    eval_outage_range: tuple[float, float] | None = None


P3_EXPERIMENTS: dict[str, ExperimentSetup] = {
    "base_distribution_planning": ExperimentSetup(),
    "der_siting_sizing": ExperimentSetup(kind_excluded="storage", hosting_target=0.025, der_target=0.56),
    "storage_allocation": ExperimentSetup(kind_excluded="der", hosting_target=0.025, der_target=0.56),
    "load_growth_expansion": ExperimentSetup(load_factor=1.3, hosting_target=0.025),
    "pareto_quality": ExperimentSetup(),
    "constraint_repair": ExperimentSetup(budget_factor=0.82),
    "runtime_scalability": ExperimentSetup(budget_factor=1.2),
}

P4_EXPERIMENTS: dict[str, ExperimentSetup] = {
    "deterministic_vs_scenario": ExperimentSetup(),
    "der_uncertainty": ExperimentSetup(der_range=(0.4, 1.7)),
    "load_uncertainty": ExperimentSetup(load_range=(0.85, 1.45)),
    "outage_contingency": ExperimentSetup(outage_range=(0.1, 0.55)),
    "restoration_aware_evaluation": ExperimentSetup(outage_range=(0.1, 0.55), use_expected_loss=True),
    "scenario_screening_efficiency": ExperimentSetup(),
    "pareto_quality": ExperimentSetup(),
    "unseen_stress_generalization": ExperimentSetup(
        eval_load_range=(1.3, 1.6), eval_der_range=(1.4, 1.9), eval_outage_range=(0.4, 0.7)
    ),
}


def make_scenarios(setup: ExperimentSetup, paper: str, evaluation: bool) -> np.ndarray:
    """Fixed seeded scenario matrix [load_factor, der_factor, outage_severity].
    p3 is a deterministic planning study: single nominal scenario."""
    if paper == "p3":
        return np.array([[setup.load_factor, 1.0, 0.0]])
    load_range = setup.eval_load_range if evaluation and setup.eval_load_range else setup.load_range
    der_range = setup.eval_der_range if evaluation and setup.eval_der_range else setup.der_range
    outage_range = setup.eval_outage_range if evaluation and setup.eval_outage_range else setup.outage_range
    rng = np.random.default_rng(20260713 if not evaluation else 20260714)
    return np.column_stack(
        [
            rng.uniform(load_range[0], load_range[1], N_SCENARIOS),
            rng.uniform(der_range[0], der_range[1], N_SCENARIOS),
            rng.uniform(outage_range[0], outage_range[1], N_SCENARIOS),
        ]
    )


class PlanningProblem:
    """Multi-objective 0/1 planning under budget + planning-target constraints.

    Minimization objectives (mean over the scenario set):
      p3 (5): cost, loss_index, voltage_risk, -hosting_capacity, -reliability
      p4 (5): cost, loss_index, voltage_risk, -reliability, -survivability
    """

    def __init__(
        self,
        candidates: list[Candidate],
        stats: list[SubnetStats],
        paper: str,
        setup: ExperimentSetup,
        scenarios: np.ndarray,
    ):
        self.candidates = candidates
        self.paper = paper
        self.setup = setup
        self.scenarios = scenarios
        self.n = len(candidates)
        self.n_obj = 5
        self.cost = np.array([c.cost for c in candidates])
        self.loss_red = np.array([c.loss_reduction for c in candidates])
        self.volt_red = np.array([c.voltage_reduction for c in candidates])
        self.hosting_gain = np.array([c.hosting_gain for c in candidates])
        self.rel_gain = np.array([c.reliability_gain for c in candidates])
        self.res_gain = np.array([c.resilience_gain for c in candidates])
        self.der_support = np.array([c.der_support for c in candidates])
        total_load = sum(item.load_mw for item in stats)
        total_line = sum(item.line_length_km for item in stats)
        self.base_loss = 0.12 + total_line / max(1.0, total_load) * 0.015
        self.base_voltage = 0.18 + total_load / max(1.0, total_line) * 0.010
        self.hosting_denom = total_load * (0.08 if paper == "p3" else 0.45)
        self.budget = (980.0 if paper == "p3" else 920.0) * setup.budget_factor

    def _components(self, X: np.ndarray, scenarios: np.ndarray) -> dict[str, np.ndarray]:
        """Scenario-resolved raw components; every quantity depends only on the
        plan vector, the candidate attributes, and the scenario multipliers."""
        X = np.atleast_2d(X).astype(float)
        S = scenarios
        loadf = S[:, 0][None, :]
        derf = S[:, 1][None, :]
        sev = S[:, 2][None, :]
        cost = (X @ self.cost)[:, None] * np.ones_like(loadf)
        loss = np.maximum(0.015, self.base_loss * loadf - (X @ self.loss_red)[:, None] / 120)
        voltage = np.maximum(0.005, self.base_voltage * loadf - (X @ self.volt_red)[:, None] / 10)
        hosting = np.minimum(1.0, (X @ self.hosting_gain)[:, None] / np.maximum(1.0, self.hosting_denom * derf))
        reliability = np.minimum(1.0, 0.35 + (X @ self.rel_gain)[:, None] / 28)
        survivability = np.minimum(1.0, 0.42 * (1.0 - sev) + (X @ self.res_gain)[:, None] / 24)
        expected_loss = loss * (1.0 + 0.30 * sev * (1.0 - survivability))
        count = np.maximum(1.0, X.sum(axis=1))[:, None]
        der_readiness = np.minimum(1.0, (X @ self.der_support)[:, None] / (count * 0.62))
        return {
            "cost": cost,
            "loss": loss,
            "voltage": voltage,
            "hosting": hosting,
            "reliability": reliability,
            "survivability": survivability,
            "expected_loss": expected_loss,
            "der_readiness": der_readiness,
        }

    def objectives(self, X: np.ndarray, scenarios: np.ndarray | None = None, aggregate: str = "mean") -> np.ndarray:
        """aggregate='mean': expectation over scenarios (headline).
        aggregate='worst': per-objective worst case over scenarios (robustness
        readout, method-independent)."""
        S = self.scenarios if scenarios is None else scenarios
        comp = self._components(X, S)
        loss = comp["expected_loss"] if self.setup.use_expected_loss else comp["loss"]
        if self.paper == "p3":
            cols = [comp["cost"], loss, comp["voltage"], -comp["hosting"], -comp["reliability"]]
        else:
            cols = [comp["cost"], loss, comp["voltage"], -comp["reliability"], -comp["survivability"]]
        if aggregate == "worst":
            return np.stack([c.max(axis=1) for c in cols], axis=1)
        return np.stack([c.mean(axis=1) for c in cols], axis=1)

    def violation(self, X: np.ndarray, scenarios: np.ndarray | None = None) -> np.ndarray:
        """Budget is the only hard constraint. Voltage risk and hosting capacity
        are already objectives; planning-target shortfalls are reported as
        descriptive compromise metrics, not feasibility gates (the v1 pipeline's
        voltage/hosting 'constraints' were unsatisfiable within budget and were
        silently soft-penalized)."""
        X = np.atleast_2d(X).astype(float)
        cost = X @ self.cost
        return np.maximum(0.0, (cost - self.budget) / self.budget)


# ---------------------------------------------------------------------------
# Shared evaluation helpers (hypervolume etc. reused from the p5/p6 module)
# ---------------------------------------------------------------------------


def _hv_helpers():
    from powergrid_benchmark.mintou_real_project_review import (
        holm_correction,
        hypervolume,
        nondominated,
    )

    return hypervolume, nondominated, holm_correction


def normalization_bounds(problem: PlanningProblem, aggregate: str = "mean") -> tuple[np.ndarray, np.ndarray]:
    cache = getattr(problem, "_norm_bounds_cache", None)
    if cache is None:
        cache = {}
        problem._norm_bounds_cache = cache
    if aggregate in cache:
        return cache[aggregate]
    rng = np.random.default_rng(20260713)
    samples = [np.zeros(problem.n)]
    for i in range(problem.n):
        row = np.zeros(problem.n)
        row[i] = 1.0
        samples.append(row)
    for _ in range(2048):
        density = rng.uniform(0.02, 0.30)
        row = (rng.random(problem.n) < density).astype(float)
        order = rng.permutation(problem.n)
        cost = 0.0
        selected = np.zeros(problem.n)
        for idx in order:
            if row[idx] and cost + problem.cost[idx] <= problem.budget:
                selected[idx] = 1.0
                cost += problem.cost[idx]
        samples.append(selected)
    F = problem.objectives(np.array(samples), aggregate=aggregate)
    lo = F.min(axis=0)
    hi = F.max(axis=0)
    span = np.maximum(hi - lo, 1e-9)
    bounds = (lo - 0.05 * span, hi + 0.05 * span)
    cache[aggregate] = bounds
    return bounds


def feasible_front(problem: PlanningProblem, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    _, nondominated, _ = _hv_helpers()
    X = np.atleast_2d(X)
    if X.size == 0:
        return np.empty((0, problem.n)), np.empty((0, problem.n_obj))
    feasible = problem.violation(X) <= 1e-9
    X = X[feasible]
    if X.shape[0] == 0:
        return np.empty((0, problem.n)), np.empty((0, problem.n_obj))
    X = np.unique(X, axis=0)
    F = problem.objectives(X)
    mask = nondominated(F)
    return X[mask], F[mask]


def _repair_to_budget(x: np.ndarray, problem: PlanningProblem) -> int:
    benefit = problem.loss_red / 0.12 + problem.volt_red / 0.02 + problem.hosting_gain / 5 + problem.rel_gain / 2 + problem.res_gain / 2
    score = benefit / np.maximum(problem.cost, 1.0)
    drops = 0
    while x @ problem.cost > problem.budget and x.sum() > 0:
        selected = np.where(x > 0)[0]
        worst = selected[np.argmin(score[selected])]
        x[worst] = 0
        drops += 1
    return drops


def _scalar_score(problem: PlanningProblem, X: np.ndarray, lo: np.ndarray, hi: np.ndarray, scenarios: np.ndarray | None = None) -> np.ndarray:
    F = problem.objectives(X, scenarios)
    norm = (F - lo) / np.maximum(hi - lo, 1e-9)
    return norm.sum(axis=1) + 10.0 * problem.violation(X, scenarios)


# ---------------------------------------------------------------------------
# NSGA-II-style environmental selection (shared by custom methods)
# ---------------------------------------------------------------------------


def _environmental_select(
    union: np.ndarray,
    F: np.ndarray,
    V: np.ndarray,
    pop_size: int,
    use_crowding: bool,
    rng: np.random.Generator,
) -> np.ndarray:
    from powergrid_benchmark.mintou_real_project_review import _crowding_distance, _simple_nds

    fronts = _simple_nds(F, V)
    selected: list[int] = []
    for front in fronts:
        if len(selected) + len(front) <= pop_size:
            selected.extend(front.tolist())
        else:
            remaining = pop_size - len(selected)
            if use_crowding:
                dist = _crowding_distance(F[front])
                order = front[np.argsort(-dist)]
            else:
                order = front[rng.permutation(len(front))]
            selected.extend(order[:remaining].tolist())
            break
    return union[np.array(selected, dtype=int)]


# ---------------------------------------------------------------------------
# CARS-MODE: strategy-adaptive multi-objective binary DE (p3 proposed)
# ---------------------------------------------------------------------------


@dataclass
class CarsConfig:
    repair: bool = True
    strategy_adaptive: bool = True
    diversity: bool = True
    # jDE-style probability of resampling F/CR each generation (default 0.1
    # reproduces the original hardcoded behaviour; exposed for the parameter
    # sensitivity study in mintou_planning_sensitivity.py).
    resample_prob: float = 0.1


def run_cars_mode(problem: PlanningProblem, cfg: CarsConfig, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n, pop_size = problem.n, POP_SIZE
    genome = rng.uniform(0.0, 0.45, (pop_size, n))
    genome[rng.random((pop_size, n)) < 0.08] = 0.75  # sparse initial plans
    F_param = np.full(pop_size, 0.5)
    CR_param = np.full(pop_size, 0.9)
    strategy_success = np.array([1.0, 1.0])  # rand/1, best/1

    def decode(g: np.ndarray) -> np.ndarray:
        x = (g > 0.5).astype(float)
        if cfg.repair:
            for row in x:
                _repair_to_budget(row, problem)
        return x

    pop_x = decode(genome)

    for _ in range(N_GENERATIONS):
        F_obj = problem.objectives(pop_x)
        V = problem.violation(pop_x)
        # current "best" pool = feasible-first non-dominated members
        from powergrid_benchmark.mintou_real_project_review import _simple_nds

        first_front = _simple_nds(F_obj, V)[0]
        trial_genome = np.empty_like(genome)
        strat_used = np.zeros(pop_size, dtype=int)
        p_best = strategy_success[1] / strategy_success.sum() if cfg.strategy_adaptive else 0.0
        for i in range(pop_size):
            if cfg.strategy_adaptive and rng.random() < cfg.resample_prob:
                F_param[i] = rng.uniform(0.1, 0.9)
                CR_param[i] = rng.uniform(0.0, 1.0)
            f_i = F_param[i] if cfg.strategy_adaptive else 0.5
            cr_i = CR_param[i] if cfg.strategy_adaptive else 0.9
            idx = rng.choice(pop_size, 3, replace=False)
            use_best = cfg.strategy_adaptive and rng.random() < p_best
            strat_used[i] = 1 if use_best else 0
            if use_best:
                base = genome[int(rng.choice(first_front))]
            else:
                base = genome[idx[0]]
            mutant = base + f_i * (genome[idx[1]] - genome[idx[2]])
            cross = rng.random(n) < cr_i
            cross[rng.integers(0, n)] = True
            trial_genome[i] = np.clip(np.where(cross, mutant, genome[i]), 0.0, 1.0)
        trial_x = decode(trial_genome)

        union_g = np.vstack([genome, trial_genome])
        union_x = np.vstack([pop_x, trial_x])
        F_union = problem.objectives(union_x)
        V_union = problem.violation(union_x)
        # strategy success accounting: trial i succeeded if it Pareto-improves parent i
        if cfg.strategy_adaptive:
            for i in range(pop_size):
                parent_f, trial_f = F_union[i], F_union[pop_size + i]
                parent_v, trial_v = V_union[i], V_union[pop_size + i]
                better = (trial_v < parent_v - 1e-12) or (
                    trial_v <= parent_v + 1e-12 and np.all(trial_f <= parent_f) and np.any(trial_f < parent_f)
                )
                if better:
                    strategy_success[strat_used[i]] += 1.0
            strategy_success *= 0.95  # decay
            strategy_success = np.maximum(strategy_success, 0.2)

        selected = _environmental_select(
            np.arange(2 * pop_size)[:, None], F_union, V_union, pop_size, cfg.diversity, rng
        ).ravel().astype(int)
        genome = union_g[selected]
        pop_x = union_x[selected]

    return pop_x


# ---------------------------------------------------------------------------
# SHIELD-MOEA: scenario-screened hybrid NSGA-II (p4 proposed)
# ---------------------------------------------------------------------------


@dataclass
class ShieldConfig:
    repair: bool = True
    scenario_screen: bool = True
    screen_k: int = 4
    screen_every: int = 5
    resilience_in_search: bool = True
    outage_in_search: bool = True


def run_shield_moea(problem: PlanningProblem, cfg: ShieldConfig, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n, pop_size = problem.n, POP_SIZE
    pop = np.zeros((pop_size, n))
    for i in range(pop_size):
        density = rng.uniform(0.03, 0.18)
        pop[i] = (rng.random(n) < density).astype(float)
        if cfg.repair:
            _repair_to_budget(pop[i], problem)

    full_scenarios = problem.scenarios
    search_scenarios = full_scenarios
    if not cfg.outage_in_search:
        search_scenarios = full_scenarios.copy()
        search_scenarios[:, 2] = 0.0
    lo, hi = normalization_bounds(problem)

    def search_objs(X: np.ndarray, scen: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        F = problem.objectives(X, scen)
        if not cfg.resilience_in_search:
            F = F[:, :4]  # drop the survivability column from search guidance
        return F, problem.violation(X, scen)

    active = search_scenarios
    for gen in range(1, N_GENERATIONS + 1):
        if cfg.scenario_screen and gen % cfg.screen_every == 1 and problem.paper == "p4":
            # screen: keep the K scenarios where the current population performs worst
            scores = np.empty(search_scenarios.shape[0])
            for s in range(search_scenarios.shape[0]):
                scen = search_scenarios[s : s + 1]
                scores[s] = _scalar_score(problem, pop, lo, hi, scen).mean()
            worst = np.argsort(-scores)[: cfg.screen_k]
            active = search_scenarios[worst]
        elif not cfg.scenario_screen:
            active = search_scenarios

        # hybrid variation: half GA (uniform crossover + bitflip), half binary DE
        idx_a = rng.integers(0, pop_size, pop_size)
        idx_b = rng.integers(0, pop_size, pop_size)
        mask = rng.random((pop_size, n)) < 0.5
        ga_children = np.where(mask, pop[idx_a], pop[idx_b])
        flip = rng.random((pop_size, n)) < 1.0 / n
        ga_children = np.abs(ga_children - flip.astype(float))
        de_idx = rng.integers(0, pop_size, (pop_size, 3))
        de_trial = np.clip(pop[de_idx[:, 0]] + 0.5 * (pop[de_idx[:, 1]] - pop[de_idx[:, 2]]), 0.0, 1.0)
        de_children = (rng.random((pop_size, n)) < np.where(de_trial > 0.5, 0.9, 0.08)).astype(float)
        half = pop_size // 2
        children = np.vstack([ga_children[:half], de_children[half:]])
        if cfg.repair:
            for row in children:
                _repair_to_budget(row, problem)

        union = np.vstack([pop, children])
        F, V = search_objs(union, active)
        pop = _environmental_select(union, F, V, pop_size, True, rng)

    return pop


# ---------------------------------------------------------------------------
# Scalarized single-objective baselines (real GA / binary PSO / standard DE)
# ---------------------------------------------------------------------------


def run_scalar_ga(problem: PlanningProblem, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n, pop_size = problem.n, POP_SIZE
    lo, hi = normalization_bounds(problem)
    pop = (rng.random((pop_size, n)) < rng.uniform(0.03, 0.18, (pop_size, 1))).astype(float)
    fit = _scalar_score(problem, pop, lo, hi)
    for _ in range(N_GENERATIONS):
        contenders = rng.integers(0, pop_size, (pop_size, 2))
        parents = np.where((fit[contenders[:, 0]] < fit[contenders[:, 1]])[:, None], pop[contenders[:, 0]], pop[contenders[:, 1]])
        pairs = rng.permutation(pop_size)
        mask = rng.random((pop_size, n)) < 0.5
        children = np.where(mask, parents, parents[pairs])
        flip = rng.random((pop_size, n)) < 1.5 / n
        children = np.abs(children - flip.astype(float))
        child_fit = _scalar_score(problem, children, lo, hi)
        union = np.vstack([pop, children])
        union_fit = np.concatenate([fit, child_fit])
        keep = np.argsort(union_fit)[:pop_size]
        pop, fit = union[keep], union_fit[keep]
    return pop[np.argmin(fit)][None, :]


def run_binary_pso(problem: PlanningProblem, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n, pop_size = problem.n, POP_SIZE
    lo, hi = normalization_bounds(problem)
    pos = (rng.random((pop_size, n)) < rng.uniform(0.03, 0.18, (pop_size, 1))).astype(float)
    vel = rng.normal(0.0, 0.1, (pop_size, n))
    pbest, pbest_fit = pos.copy(), _scalar_score(problem, pos, lo, hi)
    gbest = pbest[np.argmin(pbest_fit)].copy()
    gbest_fit = pbest_fit.min()
    for _ in range(N_GENERATIONS):
        r1, r2 = rng.random((pop_size, n)), rng.random((pop_size, n))
        vel = 0.72 * vel + 1.49 * r1 * (pbest - pos) + 1.49 * r2 * (gbest[None, :] - pos)
        prob = 1.0 / (1.0 + np.exp(-np.clip(vel, -6, 6)))
        pos = (rng.random((pop_size, n)) < prob).astype(float)
        fit = _scalar_score(problem, pos, lo, hi)
        improved = fit < pbest_fit
        pbest[improved], pbest_fit[improved] = pos[improved], fit[improved]
        if pbest_fit.min() < gbest_fit:
            gbest, gbest_fit = pbest[np.argmin(pbest_fit)].copy(), pbest_fit.min()
    return gbest[None, :]


def run_standard_de(problem: PlanningProblem, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n, pop_size = problem.n, POP_SIZE
    lo, hi = normalization_bounds(problem)
    genome = rng.uniform(0.0, 0.45, (pop_size, n))
    genome[rng.random((pop_size, n)) < 0.08] = 0.75
    decode = lambda g: (g > 0.5).astype(float)
    fit = _scalar_score(problem, decode(genome), lo, hi)
    for _ in range(N_GENERATIONS):
        idx = np.array([rng.choice(pop_size, 3, replace=False) for _ in range(pop_size)])
        mutant = genome[idx[:, 0]] + 0.5 * (genome[idx[:, 1]] - genome[idx[:, 2]])
        cross = rng.random((pop_size, n)) < 0.9
        cross[np.arange(pop_size), rng.integers(0, n, pop_size)] = True
        trial = np.clip(np.where(cross, mutant, genome), 0.0, 1.0)
        trial_fit = _scalar_score(problem, decode(trial), lo, hi)
        improved = trial_fit < fit
        genome[improved], fit[improved] = trial[improved], trial_fit[improved]
    return decode(genome[np.argmin(fit)])[None, :]


def run_weighted_sum(problem: PlanningProblem) -> np.ndarray:
    benefit = problem.loss_red / 0.12 + problem.volt_red / 0.02 + problem.hosting_gain / 5 + problem.rel_gain / 2 + problem.res_gain / 2
    order = np.argsort(-benefit)
    x = np.zeros(problem.n)
    cost = 0.0
    for idx in order:
        if cost + problem.cost[idx] <= problem.budget:
            x[idx] = 1.0
            cost += problem.cost[idx]
    return x[None, :]


def run_cost_first(problem: PlanningProblem) -> np.ndarray:
    order = np.argsort(problem.cost)
    x = np.zeros(problem.n)
    cost = 0.0
    for idx in order:
        if cost + problem.cost[idx] <= problem.budget:
            x[idx] = 1.0
            cost += problem.cost[idx]
    return x[None, :]


def run_pymoo(problem: PlanningProblem, algorithm_name: str, seed: int) -> np.ndarray:
    from pymoo.algorithms.moo.moead import MOEAD
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem as PymooProblem
    from pymoo.core.sampling import Sampling
    from pymoo.operators.crossover.pntx import TwoPointCrossover
    from pymoo.operators.mutation.bitflip import BitflipMutation
    from pymoo.optimize import minimize
    from pymoo.util.ref_dirs import get_reference_directions

    constrained = algorithm_name != "MOEA/D"

    class LowDensitySampling(Sampling):
        def _do(self, pymoo_problem, n_samples, **kwargs):
            rng = np.random.default_rng(seed)
            density = rng.uniform(0.03, 0.18, size=(n_samples, 1))
            return rng.random((n_samples, pymoo_problem.n_var)) < density

    class Wrapped(PymooProblem):
        def __init__(self) -> None:
            super().__init__(n_var=problem.n, n_obj=problem.n_obj, n_ieq_constr=1 if constrained else 0, xl=0, xu=1, vtype=bool)

        def _evaluate(self, X: np.ndarray, out: dict, *args, **kwargs) -> None:
            Xf = X.astype(float)
            F = problem.objectives(Xf)
            V = problem.violation(Xf)
            if constrained:
                out["F"] = F
                out["G"] = V[:, None]
            else:
                out["F"] = F + 1e4 * V[:, None]

    operators = dict(sampling=LowDensitySampling(), crossover=TwoPointCrossover(), mutation=BitflipMutation())
    if algorithm_name == "NSGA-II":
        algorithm = NSGA2(pop_size=POP_SIZE, **operators)
    else:
        ref_dirs = get_reference_directions("das-dennis", problem.n_obj, n_partitions=3)
        algorithm = MOEAD(ref_dirs=ref_dirs, n_neighbors=10, prob_neighbor_mating=0.7, **operators)
    result = minimize(Wrapped(), algorithm, ("n_gen", N_GENERATIONS), seed=seed, verbose=False)
    X = result.pop.get("X") if result.pop is not None else result.X
    if X is None:
        return np.zeros((0, problem.n))
    return np.atleast_2d(X).astype(float)


# ---------------------------------------------------------------------------
# Method registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MethodSpec:
    name: str
    role: str
    runner: str  # cars | shield | pymoo | scalar_ga | pso | de | point_ws | point_cost
    description: str
    cars: CarsConfig | None = None
    shield: ShieldConfig | None = None
    pymoo_name: str = ""
    kind_excluded: str = ""


def p3_methods() -> list[MethodSpec]:
    return [
        MethodSpec("CARS-MODE", "proposed", "cars", "Binary MODE: jDE self-adaptive F/CR + SaDE strategy pool + budget repair + crowding diversity.", cars=CarsConfig()),
        MethodSpec("NSGA-II", "baseline", "pymoo", "pymoo NSGA-II, binary, constrained.", pymoo_name="NSGA-II"),
        MethodSpec("NSGA-II+Repair", "baseline", "pymoo_repair", "NSGA-II with budget repair applied to returned population.", pymoo_name="NSGA-II"),
        MethodSpec("MOEA/D", "baseline", "pymoo", "pymoo MOEA/D, penalty for constraints.", pymoo_name="MOEA/D"),
        MethodSpec("Standard DE", "baseline", "de", "Binary DE/rand/1/bin, F=0.5 CR=0.9, scalarized objective.", ),
        MethodSpec("PSO", "baseline", "pso", "Binary PSO (sigmoid velocity), scalarized objective."),
        MethodSpec("GA", "baseline", "scalar_ga", "Single-objective GA, tournament + uniform crossover, scalarized."),
        MethodSpec("Weighted Sum", "baseline", "point_ws", "Weighted-benefit greedy fill under budget."),
        MethodSpec("Ablation-NoRepair", "ablation", "cars", "Budget repair disabled.", cars=CarsConfig(repair=False)),
        MethodSpec("Ablation-FixedDE", "ablation", "cars", "F=0.5 CR=0.9 fixed, single rand/1 strategy.", cars=CarsConfig(strategy_adaptive=False)),
        MethodSpec("Ablation-NoDiversity", "ablation", "cars", "Crowding distance replaced by random tie-break.", cars=CarsConfig(diversity=False)),
        MethodSpec("Ablation-NoDER", "ablation", "cars", "der/storage candidates removed from the pool.", cars=CarsConfig(), kind_excluded="der+storage"),
    ]


def p4_methods() -> list[MethodSpec]:
    return [
        MethodSpec("SHIELD-MOEA", "proposed", "shield", "NSGA-II core + hybrid GA/DE variation + adaptive worst-K scenario screening + repair.", shield=ShieldConfig()),
        MethodSpec("NSGA-II", "baseline", "pymoo", "pymoo NSGA-II, binary, constrained (full scenario set).", pymoo_name="NSGA-II"),
        MethodSpec("NSGA-II+Repair", "baseline", "pymoo_repair", "NSGA-II with budget repair applied to returned population.", pymoo_name="NSGA-II"),
        MethodSpec("MOEA/D", "baseline", "pymoo", "pymoo MOEA/D, penalty for constraints.", pymoo_name="MOEA/D"),
        MethodSpec("GA", "baseline", "scalar_ga", "Single-objective GA, scalarized."),
        MethodSpec("Weighted Sum", "baseline", "point_ws", "Weighted-benefit greedy fill."),
        MethodSpec("Deterministic Planning", "baseline", "point_cost", "Cost-first greedy fill."),
        MethodSpec("Ablation-NoScenarioScreen", "ablation", "shield", "Search on all scenarios (no screening).", shield=ShieldConfig(scenario_screen=False)),
        MethodSpec("Ablation-NoRepair", "ablation", "shield", "Budget repair disabled.", shield=ShieldConfig(repair=False)),
        MethodSpec("Ablation-NoResilienceObj", "ablation", "shield", "Survivability objective hidden from search.", shield=ShieldConfig(resilience_in_search=False)),
        MethodSpec("Ablation-NoOutage", "ablation", "shield", "Outage severity zeroed during search (final eval unchanged).", shield=ShieldConfig(outage_in_search=False)),
    ]


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def experiment_pool(candidates: list[Candidate], setup: ExperimentSetup) -> list[Candidate]:
    if setup.kind_excluded:
        return [c for c in candidates if c.kind != setup.kind_excluded]
    return list(candidates)


def method_search_mask(pool: list[Candidate], spec: MethodSpec) -> np.ndarray:
    """Columns of the experiment pool the method may select. Pool-restricted
    ablations search a subspace but are evaluated (and normalized) in the full
    experiment space so hypervolumes stay comparable."""
    if spec.kind_excluded == "der+storage":
        return np.array([c.kind not in {"der", "storage"} for c in pool])
    return np.ones(len(pool), dtype=bool)


def run_method(spec: MethodSpec, problem: PlanningProblem, seed: int, search_mask: np.ndarray | None = None) -> np.ndarray:
    if spec.runner == "cars":
        X = run_cars_mode(problem, spec.cars or CarsConfig(), seed)
    elif spec.runner == "shield":
        X = run_shield_moea(problem, spec.shield or ShieldConfig(), seed)
    elif spec.runner == "pymoo":
        X = run_pymoo(problem, spec.pymoo_name, seed)
    elif spec.runner == "pymoo_repair":
        X = run_pymoo(problem, spec.pymoo_name, seed)
        for row in X:
            _repair_to_budget(row, problem)
    elif spec.runner == "scalar_ga":
        X = run_scalar_ga(problem, seed)
    elif spec.runner == "pso":
        X = run_binary_pso(problem, seed)
    elif spec.runner == "de":
        X = run_standard_de(problem, seed)
    elif spec.runner == "point_ws":
        X = run_weighted_sum(problem)
    else:
        X = run_cost_first(problem)
    if spec.runner in {"scalar_ga", "pso", "de"}:
        for row in X:
            _repair_to_budget(row, problem)
    if search_mask is not None and not search_mask.all():
        X = X * search_mask[None, :].astype(float)
    return X


def compromise_solution(problem: PlanningProblem, front_X: np.ndarray, front_F: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> np.ndarray | None:
    if front_X.shape[0] == 0:
        return None
    norm = (front_F - lo) / np.maximum(hi - lo, 1e-9)
    return front_X[int(np.argmin(norm.sum(axis=1)))]


def composition_counts(problem: PlanningProblem, x: np.ndarray | None) -> dict[str, int]:
    counts = {"reinforcement": 0, "storage": 0, "der": 0, "automation": 0}
    if x is None:
        return counts
    for i in np.where(x > 0)[0]:
        counts[problem.candidates[int(i)].kind] += 1
    return counts


def run_paper(paper: str) -> None:
    hypervolume, _, holm_correction = _hv_helpers()
    root = P3_ROOT if paper == "p3" else P4_ROOT
    methods = p3_methods() if paper == "p3" else p4_methods()
    experiments = P3_EXPERIMENTS if paper == "p3" else P4_EXPERIMENTS
    status = P3_STATUS if paper == "p3" else P4_STATUS
    proposed_name = "CARS-MODE" if paper == "p3" else "SHIELD-MOEA"

    stats = load_subnet_stats()
    all_candidates = build_candidates(stats)
    rows: list[dict[str, str]] = []
    compositions: list[dict[str, str]] = []

    for experiment, setup in experiments.items():
        eval_scenarios = make_scenarios(setup, paper, evaluation=True)
        search_scenarios = make_scenarios(setup, paper, evaluation=False)
        pool = experiment_pool(all_candidates, setup)
        eval_problem = PlanningProblem(pool, stats, paper, setup, eval_scenarios)
        lo, hi = normalization_bounds(eval_problem)
        for spec in methods:
            mask = method_search_mask(pool, spec)
            if mask.all():
                search_pool = pool
            else:
                # pool-restricted ablation: excluded candidates get prohibitive
                # cost in the SEARCH problem only; evaluation stays in the full
                # experiment space so hypervolumes remain comparable
                search_pool = [
                    c if keep else Candidate(**{**c.__dict__, "cost": 1e9})
                    for c, keep in zip(pool, mask)
                ]
            search_problem = PlanningProblem(search_pool, stats, paper, setup, search_scenarios)
            for seed_index in range(N_SEEDS):
                digest = hashlib.sha1(f"{paper}|{experiment}|{spec.name}".encode("utf-8")).hexdigest()
                seed = 200000 + seed_index * 7919 + int(digest[:6], 16) % 4096
                start = time.perf_counter()
                X = run_method(spec, search_problem, seed, search_mask=mask)
                front_X, front_F = feasible_front(eval_problem, X)
                hv = hypervolume(front_F, lo, hi)
                if front_X.shape[0] > 0:
                    lo_w, hi_w = normalization_bounds(eval_problem, aggregate="worst")
                    F_worst = eval_problem.objectives(front_X, aggregate="worst")
                    hv_worst = hypervolume(F_worst, lo_w, hi_w)
                else:
                    hv_worst = 0.0
                comp_x = compromise_solution(eval_problem, front_X, front_F, lo, hi)
                runtime = time.perf_counter() - start
                comp_metrics: dict[str, float] = {}
                if comp_x is not None:
                    comp = eval_problem._components(comp_x[None, :], eval_scenarios)
                    comp_metrics = {
                        "cost_index": float(comp_x @ eval_problem.cost / eval_problem.budget),
                        "loss_index": float(comp["loss"].mean()),
                        "voltage_risk": float(comp["voltage"].mean()),
                        "hosting_capacity": float(comp["hosting"].mean()),
                        "reliability_proxy": float(comp["reliability"].mean()),
                        "survivability_rate": float(comp["survivability"].mean()),
                        "portfolio_size": float(comp_x.sum()),
                        "hosting_shortfall": max(0.0, setup.hosting_target - float(comp["hosting"].mean())),
                        "der_readiness_shortfall": max(0.0, setup.der_target - float(comp["der_readiness"].mean())),
                    }
                rows.append(
                    {
                        "paper": paper,
                        "experiment_id": experiment,
                        "method": spec.name,
                        "method_role": spec.role,
                        "seed": str(seed_index),
                        "hypervolume": f"{hv:.8f}",
                        "hypervolume_worst_case": f"{hv_worst:.8f}",
                        "feasible_front_size": str(front_X.shape[0]),
                        "compromise_cost_index": f"{comp_metrics.get('cost_index', float('nan')):.8f}",
                        "compromise_loss_index": f"{comp_metrics.get('loss_index', float('nan')):.8f}",
                        "compromise_voltage_risk": f"{comp_metrics.get('voltage_risk', float('nan')):.8f}",
                        "compromise_hosting_capacity": f"{comp_metrics.get('hosting_capacity', float('nan')):.8f}",
                        "compromise_reliability": f"{comp_metrics.get('reliability_proxy', float('nan')):.8f}",
                        "compromise_survivability": f"{comp_metrics.get('survivability_rate', float('nan')):.8f}",
                        "portfolio_size": f"{comp_metrics.get('portfolio_size', 0):.0f}",
                        "hosting_shortfall": f"{comp_metrics.get('hosting_shortfall', float('nan')):.8f}",
                        "der_readiness_shortfall": f"{comp_metrics.get('der_readiness_shortfall', float('nan')):.8f}",
                        "runtime_s": f"{runtime:.6f}",
                        "source_status": status,
                    }
                )
                if seed_index == 0:
                    counts = composition_counts(eval_problem, comp_x)
                    compositions.append(
                        {
                            "paper": paper,
                            "experiment_id": experiment,
                            "method": spec.name,
                            "method_role": spec.role,
                            "reinforcement": str(counts["reinforcement"]),
                            "storage": str(counts["storage"]),
                            "der": str(counts["der"]),
                            "automation": str(counts["automation"]),
                            "source_status": status,
                        }
                    )
        print(f"[{paper}] {experiment}: done ({len(methods)} methods x {N_SEEDS} seeds)")

    stats_rows = statistics_table(rows, paper, proposed_name, holm_correction)
    deprecate_v1(root)
    write_csv_rows(root / "evidence" / "runs" / "real_simbench_planning_results.csv", rows)
    write_csv_rows(root / "evidence" / "tables" / "real_simbench_planning_leaderboard.csv", aggregate(rows, paper))
    write_csv_rows(root / "evidence" / "tables" / "real_simbench_planning_significance.csv", stats_rows)
    write_csv_rows(root / "evidence" / "tables" / "real_simbench_planning_compromise_compositions.csv", compositions)
    (root / "evidence" / "runs" / "real_simbench_planning_analysis.md").write_text(
        analysis_markdown(rows, stats_rows, paper), encoding="utf-8"
    )
    (root / "src" / "configs" / "real_simbench_planning_config.json").write_text(
        json.dumps(
            {
                "source_dir": str(SIMBENCH_NET.relative_to(ROOT)).replace("\\", "/"),
                "experiments": {name: setup.__dict__ for name, setup in experiments.items()},
                "methods": {m.name: m.description for m in methods},
                "seeds_per_method_per_experiment": N_SEEDS,
                "population_size": POP_SIZE,
                "generations": N_GENERATIONS,
                "scenarios_per_experiment": N_SCENARIOS if paper == "p4" else 1,
                "evaluation": "standard hypervolume on mean-over-scenario objectives; fixed seeded normalization bounds; feasible non-dominated front only; search and final-evaluation scenario sets are disjoint seeds",
                "statistics": "Mann-Whitney U two-sided, Holm correction per experiment",
                "status": status,
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[{paper}] complete")


def aggregate(rows: list[dict[str, str]], paper: str) -> list[dict[str, str]]:
    by_method: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_method.setdefault(row["method"], []).append(row)
    board = []
    for method, group in by_method.items():
        hv = np.array([float(r["hypervolume"]) for r in group])
        board.append(
            {
                "paper": paper,
                "method": method,
                "method_role": group[0]["method_role"],
                "mean_hypervolume": f"{hv.mean():.8f}",
                "std_hypervolume": f"{hv.std(ddof=1):.8f}",
                "mean_hypervolume_worst_case": f"{np.mean([float(r['hypervolume_worst_case']) for r in group]):.8f}",
                "mean_feasible_front_size": f"{np.mean([float(r['feasible_front_size']) for r in group]):.4f}",
                "mean_compromise_cost_index": f"{np.nanmean([float(r['compromise_cost_index']) for r in group]):.8f}",
                "mean_portfolio_size": f"{np.mean([float(r['portfolio_size']) for r in group]):.4f}",
                "mean_runtime_s": f"{np.mean([float(r['runtime_s']) for r in group]):.6f}",
                "runs": str(len(group)),
            }
        )
    return sorted(board, key=lambda row: float(row["mean_hypervolume"]), reverse=True)


def statistics_table(rows: list[dict[str, str]], paper: str, proposed: str, holm_correction) -> list[dict[str, str]]:
    stats: list[dict[str, str]] = []
    experiments = sorted({r["experiment_id"] for r in rows})
    for experiment in experiments:
        exp_rows = [r for r in rows if r["experiment_id"] == experiment]
        proposed_hv = [float(r["hypervolume"]) for r in exp_rows if r["method"] == proposed]
        others = sorted({r["method"] for r in exp_rows if r["method"] != proposed})
        pvals: list[float] = []
        entries: list[dict[str, str]] = []
        for other in others:
            other_hv = [float(r["hypervolume"]) for r in exp_rows if r["method"] == other]
            if np.allclose(proposed_hv, other_hv):
                u_stat, p_value = float("nan"), 1.0
            else:
                try:
                    u_stat, p_value = mannwhitneyu(proposed_hv, other_hv, alternative="two-sided")
                except ValueError:
                    u_stat, p_value = float("nan"), 1.0
            pvals.append(float(p_value))
            role = next(r["method_role"] for r in exp_rows if r["method"] == other)
            entries.append(
                {
                    "paper": paper,
                    "experiment_id": experiment,
                    "comparison": f"{proposed} vs {other}",
                    "opponent_role": role,
                    "n_per_group": str(len(proposed_hv)),
                    "mean_proposed": f"{np.mean(proposed_hv):.8f}",
                    "mean_opponent": f"{np.mean(other_hv):.8f}",
                    "mean_diff": f"{np.mean(proposed_hv) - np.mean(other_hv):.8f}",
                    "u_statistic": f"{u_stat:.2f}" if not math.isnan(u_stat) else "NA",
                    "p_value": f"{p_value:.6g}",
                }
            )
        for entry, p_holm in zip(entries, holm_correction(pvals)):
            entry["p_holm"] = f"{p_holm:.6g}"
            entry["significant_005_holm"] = str(p_holm < 0.05 and float(entry["mean_diff"]) != 0.0)
        stats.extend(entries)
    return stats


def analysis_markdown(rows: list[dict[str, str]], stats: list[dict[str, str]], paper: str) -> str:
    board = aggregate(rows, paper)
    proposed_name = "CARS-MODE" if paper == "p3" else "SHIELD-MOEA"
    status = P3_STATUS if paper == "p3" else P4_STATUS
    proposed = next(row for row in board if row["method"] == proposed_name)
    baselines = [row for row in board if row["method_role"] == "baseline"]
    ablations = [row for row in board if row["method_role"] == "ablation"]
    best_baseline = max(baselines, key=lambda row: float(row["mean_hypervolume"]))
    best_ablation = max(ablations, key=lambda row: float(row["mean_hypervolume"]))
    proposed_hv = float(proposed["mean_hypervolume"])
    baseline_gain = (proposed_hv / max(1e-12, float(best_baseline["mean_hypervolume"])) - 1.0) * 100
    ablation_gain = (proposed_hv / max(1e-12, float(best_ablation["mean_hypervolume"])) - 1.0) * 100
    sig_wins = sum(1 for s in stats if s["opponent_role"] == "baseline" and s["significant_005_holm"] == "True" and float(s["mean_diff"]) > 0)
    sig_total = sum(1 for s in stats if s["opponent_role"] == "baseline")
    sig_losses = sum(1 for s in stats if s["significant_005_holm"] == "True" and float(s["mean_diff"]) < 0)
    if baseline_gain > 0 and sig_wins > sig_total * 0.5 and sig_losses == 0:
        signal = "significant_public_signal"
    elif baseline_gain > 0:
        signal = "positive_but_partially_significant"
    else:
        signal = "no_advantage_over_baselines"
    title = "P3 CARS-MODE" if paper == "p3" else "P4 SHIELD-MOEA"
    lines = [
        f"# Real SimBench Planning Analysis - {title} (real MOEA rewrite)",
        "",
        f"Status: `{status}`.",
        "",
        "## Why this version exists",
        "",
        "The previous pipeline scored hand-shaped ranking heuristics per method (quality",
        "constants, method-name-conditional weights) with deterministic repeats. It is",
        "preserved as `*_proxy_methods_deprecated.*`. This version implements every method",
        "as a real algorithm (pymoo NSGA-II/MOEA/D; real scalarized GA/PSO/DE; the proposed",
        "method as a genuine self-contained MOEA), keeps the evaluation method-independent,",
        f"and runs {N_SEEDS} seeds per method/experiment with Mann-Whitney U + Holm tests.",
    ]
    if paper == "p4":
        lines.extend(
            [
                "Scenario uncertainty is now a real mechanism: each experiment carries a fixed",
                f"seeded set of {N_SCENARIOS} (load, DER, outage) scenarios; SHIELD-MOEA screens the",
                "worst-K scenarios during search, while the final evaluation always uses a",
                "disjoint-seed full scenario set (so screening cannot leak into scoring).",
            ]
        )
    lines.extend(
        [
            "",
            "## Headline results (pooled across experiments and seeds)",
            "",
            f"- Proposed method: `{proposed_name}`",
            f"- Proposed mean hypervolume: `{proposed['mean_hypervolume']}` (std `{proposed['std_hypervolume']}`)",
            f"- Best baseline: `{best_baseline['method']}` with `{best_baseline['mean_hypervolume']}`",
            f"- Best ablation: `{best_ablation['method']}` with `{best_ablation['mean_hypervolume']}`",
            f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
            f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
            f"- Holm-significant wins vs baselines: `{sig_wins}/{sig_total}` (per-experiment comparisons)",
            f"- Holm-significant losses (any opponent): `{sig_losses}`",
            f"- Current value signal: `{signal}`",
            "",
            "## Leaderboard (mean hypervolume, descending; worst-case HV = robustness readout)",
            "",
            "| method | role | mean HV | std | worst-case HV | mean runtime (s) |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in board:
        lines.append(
            f"| {row['method']} | {row['method_role']} | {row['mean_hypervolume']} | {row['std_hypervolume']} | {row['mean_hypervolume_worst_case']} | {row['mean_runtime_s']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "Objectives are engineering proxies computed from SimBench subnet statistics;",
            "electrical claims are backed separately by the pandapower AC validation stage",
            "(`real_ac_validation_*`), which should be re-run against the compromise",
            "compositions exported by this pipeline",
            "(`tables/real_simbench_planning_compromise_compositions.csv`).",
            "",
            "## Remaining Compliant Optimization Path",
            "",
            "- Nodal siting/sizing experiments on concrete pandapower networks for method",
            "  differentiation at the electrical level.",
            "- Monetary calibration of cost coefficients.",
            "- Keep deprecated proxy-method artifacts and all weak seeds in the evidence trail.",
        ]
    )
    return "\n".join(lines) + "\n"


def deprecate_v1(root: Path) -> None:
    renames = [
        (root / "evidence" / "runs" / "real_simbench_planning_results.csv", "real_simbench_planning_results_proxy_methods_deprecated.csv"),
        (root / "evidence" / "tables" / "real_simbench_planning_leaderboard.csv", "real_simbench_planning_leaderboard_proxy_methods_deprecated.csv"),
        (root / "evidence" / "runs" / "real_simbench_planning_analysis.md", "real_simbench_planning_analysis_proxy_methods_deprecated.md"),
    ]
    for src, new_name in renames:
        if src.exists():
            target = src.parent / new_name
            if not target.exists():
                src.rename(target)


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(ROOT / "src"))
    selected = tuple(arg for arg in sys.argv[1:] if arg in {"p3", "p4"}) or ("p3", "p4")
    for paper in selected:
        run_paper(paper)
