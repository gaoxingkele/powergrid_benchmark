"""Real-algorithm project-review benchmark for mintou p5 (TRACE-MOEA) and p6 (BiLo-NSGA).

v2 rewrite. The v1 pipeline was invalidated because methods were hand-parameterized
proxies and the evaluation consumed method-owned quality constants (circular).
This version enforces a strict separation:

- Problem definition (candidates, objectives, budget constraint) is computed only
  from public data (RTS-GMLC, SimBench, NERC/C2GES report metadata) and is
  identical for every method.
- Every method is a real algorithm operating on binary portfolio vectors:
  pymoo NSGA-II / NSGA-III / MOEA/D baselines, classic greedy / AHP-TOPSIS /
  weighted-sum / random-feasible baselines, and self-contained implementations
  of the proposed TRACE-MOEA (preference coevolution + budget repair + decision
  trace archive) and BiLo-NSGA (bidirectional local search + dependency-aware
  moves + feasibility recovery). Ablations toggle real mechanisms.
- Headline metric is the standard hypervolume of the feasible non-dominated
  front under fixed, method-independent normalization bounds and reference
  point. Trace/move statistics are descriptive secondary outputs only.
- 30 independent seeded runs per method per experiment; Mann-Whitney U tests
  (proposed vs. each baseline/ablation) with Holm correction.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu

ROOT = Path(__file__).resolve().parents[2]
RTS_SOURCE = ROOT / "data" / "public_datasets" / "production_cost" / "rts-gmlc" / "RTS_Data" / "SourceData"
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
NERC_ROOT = ROOT / "data" / "public_datasets" / "reliability_reports" / "c2ges_nerc_reports"
P5_ROOT = ROOT / "papers" / "mintou" / "mintou_p5_trace_moea_feasibility_review"
P6_ROOT = ROOT / "papers" / "mintou" / "mintou_p6_bilonsga_project_review"

STATUS = "public_rts_simbench_nerc_project_review_v2_real_algorithms"
N_SEEDS = 30
POP_SIZE = 40
N_GENERATIONS = 40


# ---------------------------------------------------------------------------
# Candidate construction (public-data-derived, method-independent)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Candidate:
    cid: str
    source: str
    zone: str
    kind: str
    cost: float
    reliability: float
    renewable: float
    load_support: float
    compliance: float
    schedule_risk: float
    implementation_risk: float
    evidence_score: float
    dependency_group: str


def parse_float(value: object, default: float = 0.0) -> float:
    try:
        if value in {"", "NA", "NULL", None}:
            return default
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def read_csv(path: Path, delimiter: str = ",") -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def load_nerc_evidence() -> dict[str, float]:
    manifest = NERC_ROOT / "metadata" / "c2ges_nerc_report_manifest.csv"
    rows = read_csv(manifest) if manifest.exists() else []
    downloaded = [row for row in rows if row.get("status") == "downloaded"]
    titles = " ".join(row.get("title", "").lower() for row in downloaded)
    return {
        "document_count": float(len(downloaded)),
        "event_reports": float(sum(1 for row in downloaded if "event" in row.get("source_page", ""))),
        "winter_mentions": float(titles.count("winter") + titles.count("arctic")),
        "ibr_mentions": float(titles.count("inverter") + titles.count("resource") + titles.count("solar")),
        "battery_mentions": float(titles.count("battery") + titles.count("storage")),
    }


def build_rts_candidates() -> list[Candidate]:
    gens = read_csv(RTS_SOURCE / "gen.csv")
    branches = read_csv(RTS_SOURCE / "branch.csv")
    buses = read_csv(RTS_SOURCE / "bus.csv")
    empty = lambda: {"load": 0.0, "bus_count": 0.0, "branch_rating": 0.0, "branch_outage": 0.0, "branch_count": 0.0, "gen_pmax": 0.0, "renewable_pmax": 0.0, "gen_for": 0.0, "gen_count": 0.0}
    by_zone: dict[str, dict[str, float]] = {}
    for row in buses:
        zone = row.get("Zone") or row.get("Area") or "unknown"
        data = by_zone.setdefault(zone, empty())
        data["load"] += parse_float(row.get("MW Load"))
        data["bus_count"] += 1
    for row in branches:
        from_bus = str(row.get("From Bus", ""))
        zone = from_bus[:1] if from_bus else "unknown"
        data = by_zone.setdefault(zone, empty())
        data["branch_rating"] += parse_float(row.get("Cont Rating"))
        data["branch_outage"] += parse_float(row.get("Perm OutRate"))
        data["branch_count"] += 1
    for row in gens:
        bus = str(row.get("Bus ID", ""))
        zone = bus[:1] if bus else "unknown"
        data = by_zone.setdefault(zone, empty())
        pmax = parse_float(row.get("PMax MW"))
        fuel = (row.get("Fuel") or row.get("Category") or "").lower()
        data["gen_pmax"] += pmax
        if any(token in fuel for token in ("wind", "solar", "pv", "hydro")):
            data["renewable_pmax"] += pmax
        data["gen_for"] += parse_float(row.get("FOR"))
        data["gen_count"] += 1
    candidates: list[Candidate] = []
    for zone, data in sorted(by_zone.items()):
        if data["load"] <= 0 and data["gen_pmax"] <= 0:
            continue
        reserve_margin = data["gen_pmax"] / max(1.0, data["load"])
        outage_pressure = data["branch_outage"] / max(1.0, data["branch_count"])
        renewable_gap = max(0.0, data["load"] * 0.28 - data["renewable_pmax"])
        candidates.extend(
            [
                Candidate(
                    cid=f"rts-zone-{zone}-transmission-reinforcement",
                    source="RTS-GMLC",
                    zone=f"rts-{zone}",
                    kind="transmission_reinforcement",
                    cost=95 + 0.018 * data["branch_rating"] + 0.030 * data["load"],
                    reliability=0.55 * outage_pressure + 0.018 * data["branch_count"],
                    renewable=0.016 * renewable_gap,
                    load_support=0.025 * data["load"] + 0.002 * data["branch_rating"],
                    compliance=0.66 + min(0.18, outage_pressure / 8),
                    schedule_risk=0.22 + min(0.24, data["branch_count"] / 120),
                    implementation_risk=0.26 + min(0.20, data["branch_rating"] / 6500),
                    evidence_score=0.74,
                    dependency_group=f"rts-grid-{zone}",
                ),
                Candidate(
                    cid=f"rts-zone-{zone}-reliability-automation",
                    source="RTS-GMLC",
                    zone=f"rts-{zone}",
                    kind="reliability_automation",
                    cost=62 + 1.9 * data["bus_count"] + 0.010 * data["branch_rating"],
                    reliability=0.12 * math.sqrt(data["branch_count"] + data["bus_count"] + 1) + 0.40 * outage_pressure,
                    renewable=0.006 * renewable_gap,
                    load_support=0.009 * data["load"],
                    compliance=0.80,
                    schedule_risk=0.14,
                    implementation_risk=0.16,
                    evidence_score=0.78,
                    dependency_group=f"rts-grid-{zone}",
                ),
                Candidate(
                    cid=f"rts-zone-{zone}-flexible-renewable-support",
                    source="RTS-GMLC",
                    zone=f"rts-{zone}",
                    kind="renewable_support",
                    cost=70 + 0.050 * renewable_gap + 4.0 * max(0.0, 1.15 - reserve_margin),
                    reliability=0.035 * math.sqrt(data["gen_count"] + 1),
                    renewable=0.090 * renewable_gap + 0.008 * data["load"],
                    load_support=0.010 * data["load"],
                    compliance=0.70,
                    schedule_risk=0.18,
                    implementation_risk=0.20,
                    evidence_score=0.72,
                    dependency_group=f"rts-renewable-{zone}",
                ),
            ]
        )
    return candidates


def build_simbench_candidates(limit: int = 16) -> list[Candidate]:
    loads = read_csv(SIMBENCH_NET / "Load.csv", delimiter=";")
    lines = read_csv(SIMBENCH_NET / "Line.csv", delimiter=";")
    res = read_csv(SIMBENCH_NET / "RES.csv", delimiter=";")
    empty = lambda: {"load": 0.0, "load_count": 0.0, "res": 0.0, "line_length": 0.0, "line_count": 0.0}
    by_subnet: dict[str, dict[str, float]] = {}
    for row in loads:
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["load"] += parse_float(row.get("pLoad"))
        data["load_count"] += 1
    for row in res:
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["res"] += parse_float(row.get("pRES"))
    for row in lines:
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["line_length"] += parse_float(row.get("length"))
        data["line_count"] += 1
    ranked = sorted(
        ((subnet, data) for subnet, data in by_subnet.items() if data["load"] > 0 and data["line_count"] > 0),
        key=lambda item: item[1]["load"] + 0.12 * item[1]["line_length"],
        reverse=True,
    )[:limit]
    candidates: list[Candidate] = []
    for subnet, data in ranked:
        der_gap = max(0.0, data["load"] * 0.55 - data["res"])
        stress = data["load"] / max(0.2, data["line_length"])
        candidates.extend(
            [
                Candidate(
                    cid=f"simbench-{subnet}-feeder-reinforcement",
                    source="SimBench",
                    zone=subnet,
                    kind="distribution_reinforcement",
                    cost=58 + 4.1 * data["line_length"] + 8.5 * data["load"],
                    reliability=0.025 * data["line_count"] + 0.08 * stress,
                    renewable=0.045 * der_gap,
                    load_support=0.110 * data["load"],
                    compliance=0.68,
                    schedule_risk=0.24 + min(0.20, data["line_count"] / 80),
                    implementation_risk=0.24 + min(0.18, data["line_length"] / 160),
                    evidence_score=0.82,
                    dependency_group=f"dist-{subnet}",
                ),
                Candidate(
                    cid=f"simbench-{subnet}-storage-flexibility",
                    source="SimBench",
                    zone=subnet,
                    kind="storage_flexibility",
                    cost=52 + 15 * math.sqrt(data["load"] + 1),
                    reliability=0.070 * math.sqrt(data["load_count"] + 1),
                    renewable=0.150 * der_gap + 0.065 * data["load"],
                    load_support=0.060 * data["load"],
                    compliance=0.74,
                    schedule_risk=0.16,
                    implementation_risk=0.19,
                    evidence_score=0.80,
                    dependency_group=f"flex-{subnet}",
                ),
                Candidate(
                    cid=f"simbench-{subnet}-protection-automation",
                    source="SimBench",
                    zone=subnet,
                    kind="protection_automation",
                    cost=36 + 2.1 * data["line_count"],
                    reliability=0.105 * math.sqrt(data["line_count"] + 1),
                    renewable=0.018 * der_gap,
                    load_support=0.020 * data["load"],
                    compliance=0.86,
                    schedule_risk=0.12,
                    implementation_risk=0.13,
                    evidence_score=0.84,
                    dependency_group=f"dist-{subnet}",
                ),
            ]
        )
    return candidates


def build_candidates() -> list[Candidate]:
    candidates = build_rts_candidates() + build_simbench_candidates()
    nerc = load_nerc_evidence()
    event_boost = min(0.16, nerc["event_reports"] / 180)
    ibr_boost = min(0.14, nerc["ibr_mentions"] / 95)
    battery_boost = min(0.10, nerc["battery_mentions"] / 80)
    adjusted: list[Candidate] = []
    for item in candidates:
        renewable = item.renewable
        if item.kind in {"renewable_support", "storage_flexibility"}:
            renewable += ibr_boost + battery_boost
        adjusted.append(
            Candidate(
                cid=item.cid,
                source=item.source,
                zone=item.zone,
                kind=item.kind,
                cost=item.cost,
                reliability=item.reliability + event_boost,
                renewable=renewable,
                load_support=item.load_support,
                compliance=item.compliance,
                schedule_risk=item.schedule_risk,
                implementation_risk=item.implementation_risk,
                evidence_score=min(0.98, item.evidence_score + min(0.10, nerc["document_count"] / 400)),
                dependency_group=item.dependency_group,
            )
        )
    return adjusted


# ---------------------------------------------------------------------------
# Problem definition (shared by every method)
# ---------------------------------------------------------------------------


class PortfolioProblem:
    """Multi-objective 0/1 portfolio selection under a budget constraint.

    Minimization objectives:
      p5 (5): cost, -reliability, -renewable, portfolio mean risk,
              -(portfolio mean of 0.5*compliance + 0.5*evidence)
      p6 (4): cost, -reliability, -renewable, portfolio mean risk

    Constraint: total cost <= budget (violation reported as (cost-B)/B).
    The evaluation depends only on candidate attributes; no method identity
    enters this class.
    """

    def __init__(self, candidates: list[Candidate], paper: str, budget: float):
        self.candidates = candidates
        self.paper = paper
        self.budget = budget
        self.n = len(candidates)
        self.cost = np.array([c.cost for c in candidates])
        self.reliability = np.array([c.reliability for c in candidates])
        self.renewable = np.array([c.renewable for c in candidates])
        self.load_support = np.array([c.load_support for c in candidates])
        self.compliance = np.array([c.compliance for c in candidates])
        self.evidence = np.array([c.evidence_score for c in candidates])
        self.risk = 0.58 * np.array([c.schedule_risk for c in candidates]) + 0.42 * np.array(
            [c.implementation_risk for c in candidates]
        )
        self.quality = 0.5 * self.compliance + 0.5 * self.evidence
        self.groups = [c.dependency_group for c in candidates]
        self.n_obj = 5 if paper == "p5" else 4

    def objectives(self, X: np.ndarray) -> np.ndarray:
        X = np.atleast_2d(X).astype(float)
        count = np.maximum(X.sum(axis=1), 1.0)
        cost = X @ self.cost
        rel = X @ self.reliability
        ren = X @ self.renewable
        risk_mean = (X @ self.risk) / count
        empty = X.sum(axis=1) == 0
        risk_mean[empty] = 1.0
        cols = [cost, -rel, -ren, risk_mean]
        if self.paper == "p5":
            quality_mean = (X @ self.quality) / count
            quality_mean[empty] = 0.0
            cols.append(-quality_mean)
        return np.column_stack(cols)

    def violation(self, X: np.ndarray) -> np.ndarray:
        X = np.atleast_2d(X).astype(float)
        return np.maximum(0.0, (X @ self.cost - self.budget) / self.budget)


def budget_for(experiment: str, paper: str) -> float:
    budget = 1160.0 if paper == "p5" else 1020.0
    if experiment in {"budget_ranking_stability", "budget_constrained_selection"}:
        budget *= 0.88
    if experiment == "budget_sensitivity":
        budget *= 0.75
    if experiment == "project_pool_scalability":
        budget *= 1.20
    return budget


RELIABILITY_KINDS = {"transmission_reinforcement", "reliability_automation", "protection_automation", "distribution_reinforcement"}
RENEWABLE_KINDS = {"renewable_support", "storage_flexibility"}


def experiment_pool(experiment: str, candidates: list[Candidate]) -> list[Candidate]:
    """Experiments modify the candidate pool / budget, never the evaluation."""
    if experiment in {"reliability_driven_review", "reliability_prioritized_review"}:
        return [c for c in candidates if c.kind in RELIABILITY_KINDS]
    if experiment == "renewable_accommodation_review":
        return [c for c in candidates if c.kind in RENEWABLE_KINDS or c.kind == "storage_flexibility"]
    if experiment == "distribution_project_review":
        return [c for c in candidates if c.source == "SimBench"]
    if experiment == "dependency_constrained_review":
        group_sizes: dict[str, int] = {}
        for c in candidates:
            group_sizes[c.dependency_group] = group_sizes.get(c.dependency_group, 0) + 1
        return [c for c in candidates if group_sizes[c.dependency_group] >= 2]
    return list(candidates)


def experiment_weights(experiment: str, paper: str) -> dict[str, float]:
    """Preference weights used ONLY by scalarizing baselines (greedy / AHP-TOPSIS /
    weighted sum) and as seed preferences for TRACE-MOEA's coevolved population.
    They never enter the evaluation metrics."""
    if paper == "p5":
        weights = {"reliability": 0.28, "renewable": 0.20, "load": 0.18, "compliance": 0.22, "evidence": 0.18, "risk": 0.30, "cost": 0.33}
        if "reliability" in experiment:
            weights["reliability"] += 0.22
        if "renewable" in experiment:
            weights["renewable"] += 0.24
        if "traceability" in experiment:
            weights["evidence"] += 0.28
            weights["compliance"] += 0.12
        if "preference" in experiment:
            weights["compliance"] += 0.16
        return weights
    weights = {"reliability": 0.26, "renewable": 0.18, "load": 0.20, "compliance": 0.14, "evidence": 0.12, "risk": 0.26, "cost": 0.38}
    if "budget" in experiment:
        weights["cost"] += 0.12
    if "dependency" in experiment:
        weights["reliability"] += 0.14
        weights["risk"] += 0.10
    if "local_move" in experiment:
        weights["cost"] += 0.06
        weights["risk"] += 0.06
    if "renewable" in experiment:
        weights["renewable"] += 0.24
    return weights


# ---------------------------------------------------------------------------
# Hypervolume with fixed, method-independent normalization
# ---------------------------------------------------------------------------


def normalization_bounds(problem: PortfolioProblem) -> tuple[np.ndarray, np.ndarray]:
    """Fixed per-problem bounds from a seeded reference set of random feasible
    portfolios plus single-item portfolios. Identical for every method."""
    rng = np.random.default_rng(20260713)
    samples = [np.zeros(problem.n)]
    for i in range(problem.n):
        row = np.zeros(problem.n)
        row[i] = 1.0
        samples.append(row)
    for _ in range(2048):
        density = rng.uniform(0.02, 0.25)
        row = (rng.random(problem.n) < density).astype(float)
        order = rng.permutation(problem.n)
        cost = 0.0
        selected = np.zeros(problem.n)
        for idx in order:
            if row[idx] and cost + problem.cost[idx] <= problem.budget:
                selected[idx] = 1.0
                cost += problem.cost[idx]
        samples.append(selected)
    F = problem.objectives(np.array(samples))
    lo = F.min(axis=0)
    hi = F.max(axis=0)
    span = np.maximum(hi - lo, 1e-9)
    return lo - 0.05 * span, hi + 0.05 * span


def hypervolume(front: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> float:
    """Standard hypervolume on normalized objectives, reference point 1.1^d.
    Uses pymoo's exact indicator."""
    from pymoo.indicators.hv import HV

    if front.size == 0:
        return 0.0
    norm = (front - lo) / np.maximum(hi - lo, 1e-9)
    norm = np.clip(norm, 0.0, 1.0)
    ref = np.full(front.shape[1], 1.1)
    return float(HV(ref_point=ref)(norm))


def nondominated(F: np.ndarray) -> np.ndarray:
    """Boolean mask of non-dominated rows (minimization)."""
    n = F.shape[0]
    mask = np.ones(n, dtype=bool)
    for i in range(n):
        if not mask[i]:
            continue
        dominates = np.all(F <= F[i], axis=1) & np.any(F < F[i], axis=1)
        if np.any(dominates & mask):
            mask[i] = False
    return mask


def feasible_front(problem: PortfolioProblem, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
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


# ---------------------------------------------------------------------------
# Custom NSGA-II engine (shared by TRACE-MOEA / BiLo-NSGA and their ablations)
# ---------------------------------------------------------------------------


@dataclass
class EngineConfig:
    pop_size: int = POP_SIZE
    generations: int = N_GENERATIONS
    repair: bool = True
    coevolution: bool = False
    trace: bool = False
    forward_ls: bool = False
    backward_ls: bool = False
    dependency_moves: bool = False
    ls_depth: int = 8
    random_mutation_only: bool = False
    scalarize: bool = False
    search_obj_mask: tuple[int, ...] | None = None
    n_preferences: int = 8


@dataclass
class EngineResult:
    population: np.ndarray
    trace_events: list[dict] = field(default_factory=list)
    move_count: int = 0


def _norm_objs(F: np.ndarray) -> np.ndarray:
    lo = F.min(axis=0)
    span = np.maximum(F.max(axis=0) - lo, 1e-9)
    return (F - lo) / span


def _crowding_distance(F: np.ndarray) -> np.ndarray:
    n, d = F.shape
    dist = np.zeros(n)
    if n <= 2:
        return np.full(n, np.inf)
    for j in range(d):
        order = np.argsort(F[:, j])
        span = F[order[-1], j] - F[order[0], j]
        dist[order[0]] = dist[order[-1]] = np.inf
        if span <= 0:
            continue
        dist[order[1:-1]] += (F[order[2:], j] - F[order[:-2], j]) / span
    return dist


def _repair_to_budget(x: np.ndarray, problem: PortfolioProblem, events: list[dict] | None, gen: int) -> int:
    """Drop worst equal-weight benefit/cost items until within budget. Returns drops."""
    benefit = problem.reliability + problem.renewable + problem.load_support + problem.quality
    score = benefit / np.maximum(problem.cost, 1.0)
    drops = 0
    while x @ problem.cost > problem.budget and x.sum() > 0:
        selected = np.where(x > 0)[0]
        worst = selected[np.argmin(score[selected])]
        x[worst] = 0
        drops += 1
        if events is not None:
            events.append({"gen": gen, "event": "repair_drop", "item": int(worst)})
    return drops


def _scalar_fitness(x: np.ndarray, problem: PortfolioProblem, lo: np.ndarray, hi: np.ndarray) -> float:
    f = problem.objectives(x[None, :])[0]
    norm = (f - lo) / np.maximum(hi - lo, 1e-9)
    v = problem.violation(x[None, :])[0]
    return float(norm.sum() + 10.0 * v)


def _local_search(
    x: np.ndarray,
    problem: PortfolioProblem,
    cfg: EngineConfig,
    lo: np.ndarray,
    hi: np.ndarray,
    events: list[dict] | None,
    gen: int,
) -> int:
    """Bidirectional local search: forward insertion + backward deletion."""
    benefit = problem.reliability + problem.renewable + problem.load_support + problem.quality
    bcr = benefit / np.maximum(problem.cost, 1.0)
    moves = 0
    if cfg.forward_ls:
        for _ in range(cfg.ls_depth):
            cost_now = x @ problem.cost
            unselected = np.where((x < 1) & (problem.cost <= problem.budget - cost_now))[0]
            if unselected.size == 0:
                break
            order = bcr[unselected].copy()
            if cfg.dependency_moves:
                selected_groups = {problem.groups[i] for i in np.where(x > 0)[0]}
                bonus = np.array([1.06 if problem.groups[i] in selected_groups else 1.0 for i in unselected])
                order = order * bonus
            cand = unselected[np.argmax(order)]
            fit_before = _scalar_fitness(x, problem, lo, hi)
            x[cand] = 1
            if _scalar_fitness(x, problem, lo, hi) < fit_before:
                moves += 1
                if events is not None:
                    events.append({"gen": gen, "event": "forward_insert", "item": int(cand)})
            else:
                x[cand] = 0
                break
    if cfg.backward_ls:
        for _ in range(max(2, cfg.ls_depth // 2)):
            selected = np.where(x > 0)[0]
            if selected.size <= 2:
                break
            weakest = selected[np.argmin(bcr[selected])]
            fit_before = _scalar_fitness(x, problem, lo, hi)
            x[weakest] = 0
            if _scalar_fitness(x, problem, lo, hi) < fit_before:
                moves += 1
                if events is not None:
                    events.append({"gen": gen, "event": "backward_delete", "item": int(weakest)})
            else:
                x[weakest] = 1
                break
    return moves


def run_custom_ea(
    problem: PortfolioProblem,
    cfg: EngineConfig,
    seed: int,
    seed_weights: dict[str, float] | None = None,
) -> EngineResult:
    rng = np.random.default_rng(seed)
    n = problem.n
    events: list[dict] | None = [] if cfg.trace else None
    move_count = 0

    # --- init population ---
    pop = np.zeros((cfg.pop_size, n))
    for i in range(cfg.pop_size):
        density = rng.uniform(0.03, 0.15)
        pop[i] = (rng.random(n) < density).astype(float)
        if cfg.repair:
            move_count += _repair_to_budget(pop[i], problem, events, 0)

    # --- preference coevolution state (TRACE) ---
    n_search_obj = problem.n_obj if cfg.search_obj_mask is None else len(cfg.search_obj_mask)
    prefs = rng.dirichlet(np.ones(n_search_obj), size=cfg.n_preferences)
    if seed_weights is not None and problem.paper == "p5" and cfg.coevolution:
        # seed one preference vector from the experiment's stakeholder weights
        w = np.array([seed_weights["cost"], seed_weights["reliability"], seed_weights["renewable"], seed_weights["risk"], seed_weights["compliance"] + seed_weights["evidence"]])
        w = w[: n_search_obj]
        prefs[0] = w / w.sum()

    def search_objs(X: np.ndarray) -> np.ndarray:
        F = problem.objectives(X)
        if cfg.search_obj_mask is not None:
            F = F[:, list(cfg.search_obj_mask)]
        if cfg.scalarize:
            return _norm_objs(F).sum(axis=1, keepdims=True)
        return F

    for gen in range(1, cfg.generations + 1):
        # --- variation ---
        idx_a = rng.integers(0, cfg.pop_size, cfg.pop_size)
        idx_b = rng.integers(0, cfg.pop_size, cfg.pop_size)
        mask = rng.random((cfg.pop_size, n)) < 0.5
        children = np.where(mask, pop[idx_a], pop[idx_b])
        mut_rate = 3.0 / n if cfg.random_mutation_only else 1.0 / n
        flip = rng.random((cfg.pop_size, n)) < mut_rate
        children = np.abs(children - flip.astype(float))
        needs_ls = (cfg.forward_ls or cfg.backward_ls) and not cfg.random_mutation_only
        if needs_ls:
            F_gen = problem.objectives(np.vstack([pop, children]))
            lo_g, hi_g = F_gen.min(axis=0), F_gen.max(axis=0)
        for i in range(cfg.pop_size):
            if cfg.repair:
                move_count += _repair_to_budget(children[i], problem, events, gen)
            if needs_ls and i < cfg.pop_size // 2:
                move_count += _local_search(children[i], problem, cfg, lo_g, hi_g, events, gen)

        # --- environmental selection ---
        union = np.vstack([pop, children])
        F = search_objs(union)
        V = problem.violation(union)
        fronts = _simple_nds(F, V)
        selected: list[int] = []
        for front in fronts:
            if len(selected) + len(front) <= cfg.pop_size:
                selected.extend(front.tolist())
            else:
                dist = _crowding_distance(F[front])
                order = front[np.argsort(-dist)]
                selected.extend(order[: cfg.pop_size - len(selected)].tolist())
                break

        # --- preference elitism (TRACE coevolution) ---
        if cfg.coevolution:
            Fn = _norm_objs(F)
            for k, w in enumerate(prefs):
                w_full = w if Fn.shape[1] == w.shape[0] else np.resize(w, Fn.shape[1])
                scores = Fn @ w_full + 10.0 * V
                best = int(np.argmin(scores))
                if best not in selected:
                    selected[rng.integers(0, len(selected))] = best
                if events is not None:
                    items = [int(i) for i in np.where(union[best] > 0)[0]]
                    events.append({"gen": gen, "event": "preference_elite", "pref": k, "items": items})
            if gen % 5 == 0:
                # coevolve preferences: perturb, keep the K vectors whose best
                # responses are most spread in objective space
                perturbed = np.abs(prefs + rng.normal(0.0, 0.1, prefs.shape))
                perturbed = perturbed / perturbed.sum(axis=1, keepdims=True)
                pool = np.vstack([prefs, perturbed])
                responses = []
                for w in pool:
                    w_full = w if Fn.shape[1] == w.shape[0] else np.resize(w, Fn.shape[1])
                    responses.append(Fn[np.argmin(Fn @ w_full + 10.0 * V)])
                responses = np.array(responses)
                keep = [int(rng.integers(0, len(pool)))]
                while len(keep) < cfg.n_preferences:
                    dists = np.min(np.linalg.norm(responses[:, None, :] - responses[None, keep, :], axis=2), axis=1)
                    dists[keep] = -1.0
                    keep.append(int(np.argmax(dists)))
                prefs = pool[keep]

        pop = union[np.array(selected, dtype=int)]

    return EngineResult(population=pop, trace_events=events or [], move_count=move_count)


def _simple_nds(F: np.ndarray, violation: np.ndarray) -> list[np.ndarray]:
    """Constraint-domination NDS, straightforward O(n^2 d) implementation."""
    n = F.shape[0]
    feas = violation <= 1e-12
    dom = np.zeros((n, n), dtype=bool)
    for i in range(n):
        better_eq = np.all(F[i] <= F, axis=1)
        strictly = np.any(F[i] < F, axis=1)
        obj_dom = better_eq & strictly
        if feas[i]:
            dom[i] = obj_dom & feas
            dom[i] |= ~feas
        else:
            dom[i] = (~feas) & (violation[i] < violation)
        dom[i, i] = False
    counts = dom.sum(axis=0).astype(int)
    fronts: list[np.ndarray] = []
    assigned = np.zeros(n, dtype=bool)
    while not assigned.all():
        current = np.where((counts == 0) & ~assigned)[0]
        if current.size == 0:
            current = np.where(~assigned)[0]
        fronts.append(current)
        assigned[current] = True
        for i in current:
            counts -= dom[i].astype(int)
    return fronts


# ---------------------------------------------------------------------------
# pymoo baselines (NSGA-II / NSGA-III / MOEA/D)
# ---------------------------------------------------------------------------


def run_pymoo_baseline(problem: PortfolioProblem, algorithm_name: str, seed: int) -> np.ndarray:
    from pymoo.algorithms.moo.moead import MOEAD
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.algorithms.moo.nsga3 import NSGA3
    from pymoo.core.problem import Problem as PymooProblem
    from pymoo.core.sampling import Sampling
    from pymoo.operators.crossover.pntx import TwoPointCrossover
    from pymoo.operators.mutation.bitflip import BitflipMutation
    from pymoo.optimize import minimize
    from pymoo.util.ref_dirs import get_reference_directions

    class LowDensitySampling(Sampling):
        """Same budget-aware initialization density used by the custom engine
        (uniform 3-15% selection density), applied to every evolutionary method."""

        def _do(self, pymoo_problem, n_samples, **kwargs):
            rng = np.random.default_rng(seed)
            density = rng.uniform(0.03, 0.15, size=(n_samples, 1))
            return rng.random((n_samples, pymoo_problem.n_var)) < density

    constrained = algorithm_name != "MOEA/D"  # pymoo MOEA/D has no constraint handling

    class Wrapped(PymooProblem):
        def __init__(self) -> None:
            super().__init__(
                n_var=problem.n,
                n_obj=problem.n_obj,
                n_ieq_constr=1 if constrained else 0,
                xl=0,
                xu=1,
                vtype=bool,
            )

        def _evaluate(self, X: np.ndarray, out: dict, *args, **kwargs) -> None:
            Xf = X.astype(float)
            F = problem.objectives(Xf)
            V = problem.violation(Xf)
            if constrained:
                out["F"] = F
                out["G"] = V[:, None]
            else:
                # documented penalty handling for MOEA/D
                out["F"] = F + 1e4 * V[:, None]

    operators = dict(
        sampling=LowDensitySampling(),
        crossover=TwoPointCrossover(),
        mutation=BitflipMutation(),
    )
    if algorithm_name == "NSGA-II":
        algorithm = NSGA2(pop_size=POP_SIZE, **operators)
    elif algorithm_name == "NSGA-III":
        ref_dirs = get_reference_directions("das-dennis", problem.n_obj, n_partitions=4 if problem.n_obj == 4 else 3)
        algorithm = NSGA3(ref_dirs=ref_dirs, pop_size=max(POP_SIZE, len(ref_dirs)), **operators)
    else:
        ref_dirs = get_reference_directions("das-dennis", problem.n_obj, n_partitions=4 if problem.n_obj == 4 else 3)
        algorithm = MOEAD(ref_dirs=ref_dirs, n_neighbors=10, prob_neighbor_mating=0.7, **operators)
    result = minimize(Wrapped(), algorithm, ("n_gen", N_GENERATIONS), seed=seed, verbose=False)
    X = result.pop.get("X") if result.pop is not None else result.X
    if X is None:
        return np.zeros((0, problem.n))
    return np.atleast_2d(X).astype(float)


# ---------------------------------------------------------------------------
# Classic point baselines
# ---------------------------------------------------------------------------


def weighted_benefit(problem: PortfolioProblem, weights: dict[str, float]) -> np.ndarray:
    return (
        weights["reliability"] * problem.reliability
        + weights["renewable"] * problem.renewable
        + weights["load"] * problem.load_support
        + weights["compliance"] * problem.compliance
        + weights["evidence"] * problem.evidence
        - weights["risk"] * problem.risk
    )


def greedy_fill(problem: PortfolioProblem, order: np.ndarray) -> np.ndarray:
    x = np.zeros(problem.n)
    cost = 0.0
    for idx in order:
        if cost + problem.cost[idx] <= problem.budget:
            x[idx] = 1.0
            cost += problem.cost[idx]
    return x


def run_greedy_bcr(problem: PortfolioProblem, weights: dict[str, float]) -> np.ndarray:
    score = weighted_benefit(problem, weights) / np.maximum(problem.cost, 1.0)
    return greedy_fill(problem, np.argsort(-score))[None, :]


def run_weighted_sum(problem: PortfolioProblem, weights: dict[str, float]) -> np.ndarray:
    score = weighted_benefit(problem, weights)
    return greedy_fill(problem, np.argsort(-score))[None, :]


def run_ahp_topsis(problem: PortfolioProblem, weights: dict[str, float]) -> np.ndarray:
    """AHP (consistent pairwise matrix from the experiment weights) + TOPSIS."""
    criteria = np.array([weights["reliability"], weights["renewable"], weights["load"], weights["compliance"], weights["evidence"], weights["risk"], weights["cost"]])
    pairwise = criteria[:, None] / criteria[None, :]
    eigvals, eigvecs = np.linalg.eig(pairwise)
    w = np.abs(np.real(eigvecs[:, np.argmax(np.real(eigvals))]))
    w = w / w.sum()
    matrix = np.column_stack(
        [problem.reliability, problem.renewable, problem.load_support, problem.compliance, problem.evidence, problem.risk, problem.cost]
    )
    norm = matrix / np.maximum(np.linalg.norm(matrix, axis=0), 1e-9)
    weighted = norm * w
    benefit_cols = [0, 1, 2, 3, 4]
    cost_cols = [5, 6]
    ideal = np.empty(7)
    anti = np.empty(7)
    ideal[benefit_cols] = weighted[:, benefit_cols].max(axis=0)
    anti[benefit_cols] = weighted[:, benefit_cols].min(axis=0)
    ideal[cost_cols] = weighted[:, cost_cols].min(axis=0)
    anti[cost_cols] = weighted[:, cost_cols].max(axis=0)
    d_pos = np.linalg.norm(weighted - ideal, axis=1)
    d_neg = np.linalg.norm(weighted - anti, axis=1)
    closeness = d_neg / np.maximum(d_pos + d_neg, 1e-9)
    return greedy_fill(problem, np.argsort(-closeness))[None, :]


def run_random_feasible(problem: PortfolioProblem, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return greedy_fill(problem, rng.permutation(problem.n))[None, :]


# ---------------------------------------------------------------------------
# Method registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MethodSpec:
    name: str
    role: str
    runner: str  # 'custom' | 'pymoo' | 'point'
    description: str
    engine: EngineConfig | None = None
    pymoo_name: str = ""
    point_kind: str = ""
    pool_transform: str = ""  # 'small_pool' | 'low_dependency' | ''


def p5_methods() -> list[MethodSpec]:
    trace_cfg = EngineConfig(repair=True, coevolution=True, trace=True)
    return [
        MethodSpec("TRACE-MOEA", "proposed", "custom", "NSGA-II core + preference coevolution + budget repair + decision trace archive.", engine=trace_cfg),
        MethodSpec("NSGA-II", "baseline", "pymoo", "pymoo NSGA-II, binary encoding, constrained.", pymoo_name="NSGA-II"),
        MethodSpec("MOEA/D", "baseline", "pymoo", "pymoo MOEA/D, Tchebycheff decomposition, penalty for budget.", pymoo_name="MOEA/D"),
        MethodSpec("AHP-TOPSIS", "baseline", "point", "AHP-derived weights + TOPSIS closeness ranking + greedy fill.", point_kind="ahp_topsis"),
        MethodSpec("Weighted Sum", "baseline", "point", "Weighted-score ranking + greedy fill.", point_kind="weighted_sum"),
        MethodSpec("Greedy BCR", "baseline", "point", "Benefit-cost-ratio greedy under budget.", point_kind="greedy_bcr"),
        MethodSpec("Random Feasible", "baseline", "point", "Random permutation greedy fill (no penalties).", point_kind="random"),
        MethodSpec("Ablation-NoFeasibilityRepair", "ablation", "custom", "Repair operator disabled; constraint domination only.", engine=EngineConfig(repair=False, coevolution=True, trace=True)),
        MethodSpec("Ablation-NoPreferenceRanking", "ablation", "custom", "Preference coevolution disabled.", engine=EngineConfig(repair=True, coevolution=False, trace=True)),
        MethodSpec("Ablation-NoReliabilityFeatures", "ablation", "custom", "Reliability objective hidden from search (evaluation unchanged).", engine=EngineConfig(repair=True, coevolution=True, trace=True, search_obj_mask=(0, 2, 3, 4))),
        MethodSpec("Ablation-NoRenewableFeatures", "ablation", "custom", "Renewable objective hidden from search.", engine=EngineConfig(repair=True, coevolution=True, trace=True, search_obj_mask=(0, 1, 3, 4))),
        MethodSpec("Ablation-NoScheduleRisk", "ablation", "custom", "Risk objective hidden from search.", engine=EngineConfig(repair=True, coevolution=True, trace=True, search_obj_mask=(0, 1, 2, 4))),
        MethodSpec("Ablation-SingleObjective", "ablation", "custom", "Search on scalarized objective sum.", engine=EngineConfig(repair=True, coevolution=False, trace=True, scalarize=True)),
        MethodSpec("Ablation-NSGA2Only", "ablation", "custom", "Engine without repair, coevolution, and trace.", engine=EngineConfig(repair=False, coevolution=False, trace=False)),
        MethodSpec("Ablation-SmallProjectPool", "ablation", "custom", "Candidate pool restricted to one third.", engine=trace_cfg, pool_transform="small_pool"),
    ]


def p6_methods() -> list[MethodSpec]:
    bilo = EngineConfig(repair=True, forward_ls=True, backward_ls=True, dependency_moves=True, trace=True)
    return [
        MethodSpec("BiLo-NSGA", "proposed", "custom", "NSGA-II core + bidirectional local search + dependency moves + feasibility recovery.", engine=bilo),
        MethodSpec("NSGA-II", "baseline", "pymoo", "pymoo NSGA-II, binary encoding, constrained.", pymoo_name="NSGA-II"),
        MethodSpec("NSGA-III", "baseline", "pymoo", "pymoo NSGA-III with Das-Dennis reference directions.", pymoo_name="NSGA-III"),
        MethodSpec("MOEA/D", "baseline", "pymoo", "pymoo MOEA/D, penalty for budget.", pymoo_name="MOEA/D"),
        MethodSpec("Greedy BCR", "baseline", "point", "Benefit-cost-ratio greedy under budget.", point_kind="greedy_bcr"),
        MethodSpec("AHP-TOPSIS", "baseline", "point", "AHP-derived weights + TOPSIS ranking + greedy fill.", point_kind="ahp_topsis"),
        MethodSpec("Random Feasible", "baseline", "point", "Random permutation greedy fill (no penalties).", point_kind="random"),
        MethodSpec("Ablation-NoForwardSearch", "ablation", "custom", "Forward insertion disabled.", engine=EngineConfig(repair=True, forward_ls=False, backward_ls=True, dependency_moves=True, trace=True)),
        MethodSpec("Ablation-NoBackwardSearch", "ablation", "custom", "Backward deletion disabled.", engine=EngineConfig(repair=True, forward_ls=True, backward_ls=False, dependency_moves=True, trace=True)),
        MethodSpec("Ablation-RandomMutationOnly", "ablation", "custom", "Local search replaced by high-rate random mutation.", engine=EngineConfig(repair=True, forward_ls=False, backward_ls=False, random_mutation_only=True, trace=True)),
        MethodSpec("Ablation-NoDependencyMoves", "ablation", "custom", "Dependency-aware move bonus disabled.", engine=EngineConfig(repair=True, forward_ls=True, backward_ls=True, dependency_moves=False, trace=True)),
        MethodSpec("Ablation-NoFeasibilityRecovery", "ablation", "custom", "Budget repair disabled.", engine=EngineConfig(repair=False, forward_ls=True, backward_ls=True, dependency_moves=True, trace=True)),
        MethodSpec("Ablation-WeightedRankingOnly", "ablation", "point", "Weighted ranking without evolution.", point_kind="weighted_sum"),
        MethodSpec("Ablation-ShallowLocalSearch", "ablation", "custom", "Local-search depth reduced to 2.", engine=EngineConfig(repair=True, forward_ls=True, backward_ls=True, dependency_moves=True, trace=True, ls_depth=2)),
        MethodSpec("Ablation-LowDependencyDensity", "ablation", "custom", "Dependency graph thinned (every 3rd candidate isolated).", engine=bilo, pool_transform="low_dependency"),
        MethodSpec("Ablation-LooseBudget", "ablation", "custom", "Search at 1.2x budget, evaluated at the true budget.", engine=bilo, pool_transform="loose_budget"),
    ]


P5_EXPERIMENTS = (
    "benchmark_portfolio_optimization",
    "distribution_project_review",
    "reliability_driven_review",
    "renewable_accommodation_review",
    "budget_ranking_stability",
    "preference_aware_support",
    "traceability_evaluation",
)

P6_EXPERIMENTS = (
    "budget_constrained_selection",
    "reliability_prioritized_review",
    "renewable_accommodation_review",
    "dependency_constrained_review",
    "local_move_explainability",
    "ranking_robustness",
    "budget_sensitivity",
    "project_pool_scalability",
)


# ---------------------------------------------------------------------------
# Run orchestration
# ---------------------------------------------------------------------------


def apply_pool_transform(spec: MethodSpec, candidates: list[Candidate]) -> list[Candidate]:
    if spec.pool_transform == "small_pool":
        return candidates[: max(10, len(candidates) // 3)]
    if spec.pool_transform == "low_dependency":
        return [
            Candidate(**{**c.__dict__, "dependency_group": f"iso-{i}"}) if i % 3 == 0 else c
            for i, c in enumerate(candidates)
        ]
    return candidates


def run_method(
    spec: MethodSpec,
    candidates: list[Candidate],
    paper: str,
    experiment: str,
    seed: int,
) -> tuple[np.ndarray, PortfolioProblem, int, list[dict]]:
    budget = budget_for(experiment, paper)
    pool = apply_pool_transform(spec, candidates)
    search_budget = budget * 1.2 if spec.pool_transform == "loose_budget" else budget
    eval_problem = PortfolioProblem(pool, paper, budget)
    weights = experiment_weights(experiment, paper)
    move_count = 0
    events: list[dict] = []
    if spec.runner == "custom":
        search_problem = PortfolioProblem(pool, paper, search_budget)
        result = run_custom_ea(search_problem, spec.engine or EngineConfig(), seed, seed_weights=weights)
        X = result.population
        move_count = result.move_count
        events = result.trace_events
    elif spec.runner == "pymoo":
        X = run_pymoo_baseline(eval_problem, spec.pymoo_name, seed)
    else:
        if spec.point_kind == "greedy_bcr":
            X = run_greedy_bcr(eval_problem, weights)
        elif spec.point_kind == "weighted_sum":
            X = run_weighted_sum(eval_problem, weights)
        elif spec.point_kind == "ahp_topsis":
            X = run_ahp_topsis(eval_problem, weights)
        else:
            X = run_random_feasible(eval_problem, seed)
    return X, eval_problem, move_count, events


def compromise_metrics(problem: PortfolioProblem, front_X: np.ndarray, front_F: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> dict[str, float]:
    if front_X.shape[0] == 0:
        return {
            "compromise_cost_index": float("nan"),
            "compromise_reliability": 0.0,
            "compromise_renewable": 0.0,
            "compromise_risk": 1.0,
            "portfolio_size": 0.0,
        }
    norm = (front_F - lo) / np.maximum(hi - lo, 1e-9)
    best = int(np.argmin(norm.sum(axis=1)))
    x = front_X[best]
    count = max(1.0, x.sum())
    return {
        "compromise_cost_index": float(x @ problem.cost / problem.budget),
        "compromise_reliability": float(x @ problem.reliability),
        "compromise_renewable": float(x @ problem.renewable),
        "compromise_risk": float((x @ problem.risk) / count),
        "portfolio_size": float(x.sum()),
    }


def trace_metrics(events: list[dict], front_X: np.ndarray) -> dict[str, float]:
    """Descriptive-only trace statistics (never used for ranking)."""
    if not events or front_X.shape[0] == 0:
        return {"trace_event_count": float(len(events)), "decision_coverage": 0.0}
    traced_items: set[int] = set()
    for event in events:
        if "item" in event:
            traced_items.add(int(event["item"]))
        for item in event.get("items", []):
            traced_items.add(int(item))
    selected = {int(i) for i in np.where(front_X.sum(axis=0) > 0)[0]}
    coverage = len(selected & traced_items) / max(1, len(selected))
    return {"trace_event_count": float(len(events)), "decision_coverage": float(coverage)}


def run_paper(paper: str, root: Path, methods: list[MethodSpec], experiments: tuple[str, ...]) -> list[dict[str, str]]:
    all_candidates = build_candidates()
    rows: list[dict[str, str]] = []
    bounds_cache: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for experiment in experiments:
        pool = experiment_pool(experiment, all_candidates)
        budget = budget_for(experiment, paper)
        base_problem = PortfolioProblem(pool, paper, budget)
        lo, hi = normalization_bounds(base_problem)
        bounds_cache[experiment] = (lo, hi)
        for spec in methods:
            for seed_index in range(N_SEEDS):
                digest = hashlib.sha1(f"{paper}|{experiment}|{spec.name}".encode("utf-8")).hexdigest()
                seed = 100000 + seed_index * 7919 + int(digest[:6], 16) % 4096
                start = time.perf_counter()
                X, eval_problem, move_count, events = run_method(spec, pool, paper, experiment, seed)
                front_X, front_F = feasible_front(eval_problem, X)
                hv = hypervolume(front_F, lo, hi)
                comp = compromise_metrics(eval_problem, front_X, front_F, lo, hi)
                trace = trace_metrics(events, front_X)
                runtime = time.perf_counter() - start
                rows.append(
                    {
                        "paper": paper,
                        "experiment_id": experiment,
                        "method": spec.name,
                        "method_role": spec.role,
                        "seed": str(seed_index),
                        "hypervolume": f"{hv:.8f}",
                        "feasible_front_size": str(front_X.shape[0]),
                        "compromise_cost_index": f"{comp['compromise_cost_index']:.8f}",
                        "compromise_reliability": f"{comp['compromise_reliability']:.8f}",
                        "compromise_renewable": f"{comp['compromise_renewable']:.8f}",
                        "compromise_risk": f"{comp['compromise_risk']:.8f}",
                        "portfolio_size": f"{comp['portfolio_size']:.0f}",
                        "local_move_count": str(move_count),
                        "trace_event_count": f"{trace['trace_event_count']:.0f}",
                        "decision_coverage": f"{trace['decision_coverage']:.8f}",
                        "runtime_s": f"{runtime:.6f}",
                        "source_status": STATUS,
                    }
                )
        print(f"[{paper}] {experiment}: done ({len(methods)} methods x {N_SEEDS} seeds)")
    return rows


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
                "mean_feasible_front_size": f"{np.mean([float(r['feasible_front_size']) for r in group]):.4f}",
                "mean_compromise_cost_index": f"{np.nanmean([float(r['compromise_cost_index']) for r in group]):.8f}",
                "mean_portfolio_size": f"{np.mean([float(r['portfolio_size']) for r in group]):.4f}",
                "mean_local_move_count": f"{np.mean([float(r['local_move_count']) for r in group]):.4f}",
                "mean_decision_coverage": f"{np.mean([float(r['decision_coverage']) for r in group]):.8f}",
                "mean_runtime_s": f"{np.mean([float(r['runtime_s']) for r in group]):.6f}",
                "runs": str(len(group)),
            }
        )
    return sorted(board, key=lambda row: float(row["mean_hypervolume"]), reverse=True)


def holm_correction(pvalues: list[float]) -> list[float]:
    order = np.argsort(pvalues)
    m = len(pvalues)
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, idx in enumerate(order):
        adj = min(1.0, (m - rank) * pvalues[idx])
        running_max = max(running_max, adj)
        adjusted[idx] = running_max
    return adjusted


def statistics_table(rows: list[dict[str, str]], paper: str, proposed: str) -> list[dict[str, str]]:
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
    proposed_name = "TRACE-MOEA" if paper == "p5" else "BiLo-NSGA"
    proposed = next(row for row in board if row["method"] == proposed_name)
    baselines = [row for row in board if row["method_role"] == "baseline"]
    ablations = [row for row in board if row["method_role"] == "ablation"]
    best_baseline = max(baselines, key=lambda row: float(row["mean_hypervolume"]))
    best_ablation = max(ablations, key=lambda row: float(row["mean_hypervolume"]))
    proposed_hv = float(proposed["mean_hypervolume"])
    baseline_gain = (proposed_hv / max(1e-12, float(best_baseline["mean_hypervolume"])) - 1.0) * 100
    ablation_gain = (proposed_hv / max(1e-12, float(best_ablation["mean_hypervolume"])) - 1.0) * 100
    sig_baseline_wins = sum(
        1
        for s in stats
        if s["opponent_role"] == "baseline" and s["significant_005_holm"] == "True" and float(s["mean_diff"]) > 0
    )
    sig_baseline_total = sum(1 for s in stats if s["opponent_role"] == "baseline")
    sig_losses = sum(
        1 for s in stats if s["significant_005_holm"] == "True" and float(s["mean_diff"]) < 0
    )
    if baseline_gain > 0 and sig_baseline_wins > sig_baseline_total * 0.5 and sig_losses == 0:
        signal = "significant_public_signal"
    elif baseline_gain > 0:
        signal = "positive_but_partially_significant"
    else:
        signal = "no_advantage_over_baselines"
    title = "P5 TRACE-MOEA" if paper == "p5" else "P6 BiLo-NSGA"
    task = "traceable feasibility review" if paper == "p5" else "budget-constrained project review"
    lines = [
        f"# Real Project Review Analysis - {title} (v2, real algorithms)",
        "",
        f"Status: `{STATUS}`.",
        "",
        "## Why v2 exists",
        "",
        "The v1 experiment was **invalidated and deprecated**: methods were hand-parameterized",
        "proxies and the composite metric consumed method-owned constants (circular).",
        "v2 re-runs the task with real algorithm implementations (pymoo NSGA-II/NSGA-III/MOEA/D,",
        "classic AHP-TOPSIS/greedy/weighted-sum baselines, self-contained proposed methods),",
        "a method-independent evaluation (standard hypervolume, fixed normalization bounds),",
        f"{N_SEEDS} seeded runs per method/experiment, and Mann-Whitney U tests with Holm correction.",
        "Trace/move statistics are descriptive only and never enter the ranking.",
        "",
        f"Task: {task} over {'7' if paper == 'p5' else '8'} experiments on RTS-GMLC + SimBench + NERC-report-derived candidates.",
        "",
        "## Headline results (pooled across experiments and seeds)",
        "",
        f"- Proposed method: `{proposed_name}`",
        f"- Proposed mean hypervolume: `{proposed['mean_hypervolume']}` (std `{proposed['std_hypervolume']}`)",
        f"- Best baseline: `{best_baseline['method']}` with `{best_baseline['mean_hypervolume']}`",
        f"- Best ablation: `{best_ablation['method']}` with `{best_ablation['mean_hypervolume']}`",
        f"- Relative gain over best baseline: `{baseline_gain:.2f}%`",
        f"- Relative gain over best ablation: `{ablation_gain:.2f}%`",
        f"- Holm-significant wins vs baselines: `{sig_baseline_wins}/{sig_baseline_total}` (per-experiment comparisons)",
        f"- Holm-significant losses (any opponent): `{sig_losses}`",
        f"- Current value signal: `{signal}`",
        "",
        "## Leaderboard (mean hypervolume, descending)",
        "",
        "| method | role | mean HV | std | mean runtime (s) |",
        "|---|---|---|---|---|",
    ]
    for row in board:
        lines.append(
            f"| {row['method']} | {row['method_role']} | {row['mean_hypervolume']} | {row['std_hypervolume']} | {row['mean_runtime_s']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "Candidates are derived from public grid case statistics and public reliability-report",
            "metadata; portfolio objectives are engineering proxies. The experiment validates",
            "algorithmic performance on a reproducible public benchmark. It does not establish",
            "real-world review validity: expert-labeled outcomes and calibrated engineering",
            "economics remain open requirements before manuscript claims about actual utility",
            "project review. Trace/decision-coverage columns are explainability descriptors, not",
            "performance evidence.",
            "",
            "## Remaining Compliant Optimization Path",
            "",
            "- Add expert-labeled feasibility-review outcomes (or historical project outcome data,",
            "  e.g. LBNL Queued Up / EIA-860 retirements) as external ground truth.",
            "- Calibrate cost coefficients against published utility investment figures.",
            "- Keep v1 deprecated artifacts and all weak seeds in the evidence trail.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def deprecate_v1(root: Path) -> None:
    """Preserve v1 outputs under an explicit deprecated name instead of overwriting."""
    renames = [
        (root / "evidence" / "runs" / "real_project_review_results.csv", "real_project_review_results_v1_deprecated_circular.csv"),
        (root / "evidence" / "tables" / "real_project_review_leaderboard.csv", "real_project_review_leaderboard_v1_deprecated_circular.csv"),
        (root / "evidence" / "runs" / "real_project_review_analysis.md", "real_project_review_analysis_v1_deprecated_circular.md"),
        (root / "src" / "configs" / "real_project_review_methods.json", "real_project_review_methods_v1_deprecated_circular.json"),
    ]
    for src, new_name in renames:
        if src.exists():
            target = src.parent / new_name
            if not target.exists():
                src.rename(target)


def run_all(papers: tuple[str, ...] = ("p5", "p6")) -> None:
    jobs = {
        "p5": (P5_ROOT, p5_methods(), P5_EXPERIMENTS, "TRACE-MOEA"),
        "p6": (P6_ROOT, p6_methods(), P6_EXPERIMENTS, "BiLo-NSGA"),
    }
    for paper in papers:
        root, methods, experiments, proposed = jobs[paper]
        deprecate_v1(root)
        start = time.perf_counter()
        rows = run_paper(paper, root, methods, experiments)
        stats = statistics_table(rows, paper, proposed)
        write_csv_rows(root / "evidence" / "runs" / "real_project_review_results.csv", rows)
        write_csv_rows(root / "evidence" / "tables" / "real_project_review_leaderboard.csv", aggregate(rows, paper))
        write_csv_rows(root / "evidence" / "tables" / "real_project_review_significance.csv", stats)
        (root / "evidence" / "runs" / "real_project_review_analysis.md").write_text(
            analysis_markdown(rows, stats, paper), encoding="utf-8"
        )
        (root / "src" / "configs" / "real_project_review_config.json").write_text(
            json.dumps(
                {
                    "source_dirs": [
                        str(RTS_SOURCE.relative_to(ROOT)).replace("\\", "/"),
                        str(SIMBENCH_NET.relative_to(ROOT)).replace("\\", "/"),
                        str(NERC_ROOT.relative_to(ROOT)).replace("\\", "/"),
                    ],
                    "experiments": list(experiments),
                    "methods": [m.name for m in methods],
                    "method_descriptions": {m.name: m.description for m in methods},
                    "seeds_per_method_per_experiment": N_SEEDS,
                    "population_size": POP_SIZE,
                    "generations": N_GENERATIONS,
                    "evaluation": "standard hypervolume, fixed seeded normalization bounds, ref point 1.1^d; feasible non-dominated front only",
                    "statistics": "Mann-Whitney U two-sided, Holm correction per experiment",
                    "status": STATUS,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"[{paper}] complete in {time.perf_counter() - start:.1f}s")


if __name__ == "__main__":
    import sys

    selected = tuple(arg for arg in sys.argv[1:] if arg in {"p5", "p6"}) or ("p5", "p6")
    run_all(selected)
