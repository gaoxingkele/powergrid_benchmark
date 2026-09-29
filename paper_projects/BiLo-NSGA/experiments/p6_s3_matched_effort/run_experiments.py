"""Run the prespecified P6 matched-evaluation and matched-time stage.

The runner is deliberately stage-local. It imports the shared candidate and
problem definitions read-only, meters every search evaluation itself, and
writes only to a new immutable directory under this stage's ``runs`` folder.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np


STAGE_ROOT = Path(__file__).resolve().parent
HARNESS_ROOT = Path(__file__).resolve().parents[4]
SHARED_SRC = HARNESS_ROOT / "src"
P5_ROOT = HARNESS_ROOT / "papers" / "mintou" / "mintou_p5_trace_moea_feasibility_review"
SHARED_MODULE = SHARED_SRC / "powergrid_benchmark" / "mintou_real_project_review.py"


def _prepare_imports() -> str:
    """Use native SciPy if healthy, otherwise the narrow fail-closed shim."""

    try:
        from scipy.stats import mannwhitneyu as _unused  # noqa: F401

        scipy_mode = "native"
    except Exception:
        for name in list(sys.modules):
            if name == "scipy" or name.startswith("scipy."):
                del sys.modules[name]
        sys.path.insert(0, str(STAGE_ROOT / "runtime_compat"))
        scipy_mode = "p6_s3_import_only_compat"
    sys.path.insert(0, str(SHARED_SRC))
    return scipy_mode


SCIPY_MODE = _prepare_imports()

from powergrid_benchmark import mintou_real_project_review as core  # noqa: E402
from pymoo.vendor.hv import HyperVolume  # noqa: E402


METHODS = ("BiLo-NSGA", "NSGA-II", "Pareto Local Search")
COMPARATORS = ("NSGA-II", "Pareto Local Search")


def fmt(value: float) -> str:
    return f"{float(value):.10f}"


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mean(values: Iterable[float]) -> float:
    data = np.asarray(list(values), dtype=float)
    return float(np.mean(data))


def sample_sd(values: Iterable[float]) -> float:
    data = np.asarray(list(values), dtype=float)
    return float(np.std(data, ddof=1)) if data.size > 1 else 0.0


def median(values: Iterable[float]) -> float:
    return float(np.median(np.asarray(list(values), dtype=float)))


def configure_data_sources(config: dict) -> list[Path]:
    data_root = Path(config["input_data_root"])
    core.RTS_SOURCE = data_root / "production_cost" / "rts-gmlc" / "RTS_Data" / "SourceData"
    core.SIMBENCH_NET = (
        data_root
        / "grid_cases"
        / "simbench"
        / "simbench"
        / "networks"
        / "1-complete_data-mixed-all-0-sw"
    )
    core.NERC_ROOT = data_root / "reliability_reports" / "c2ges_nerc_reports"
    inputs = [
        core.RTS_SOURCE / "gen.csv",
        core.RTS_SOURCE / "branch.csv",
        core.RTS_SOURCE / "bus.csv",
        core.SIMBENCH_NET / "Load.csv",
        core.SIMBENCH_NET / "Line.csv",
        core.SIMBENCH_NET / "RES.csv",
        core.NERC_ROOT / "metadata" / "c2ges_nerc_report_manifest.csv",
    ]
    missing = [str(path) for path in inputs if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing registered public inputs: " + ", ".join(missing))
    return inputs


def p5_hashes(config: dict) -> dict[str, str]:
    return {
        relative: sha256_file(P5_ROOT / relative)
        for relative in config["source_contract"]["p5_evidence_sha256"]
    }


def validate_source_contract(config: dict) -> dict[str, str]:
    source_hash = sha256_file(SHARED_MODULE)
    expected_source = config["source_contract"]["shared_source_sha256"].lower()
    if source_hash != expected_source:
        raise RuntimeError(f"shared source hash changed: {source_hash} != {expected_source}")
    observed_p5 = p5_hashes(config)
    expected_p5 = {
        key: value.lower() for key, value in config["source_contract"]["p5_evidence_sha256"].items()
    }
    if observed_p5 != expected_p5:
        raise RuntimeError(f"P5 evidence hash mismatch: {observed_p5!r}")
    return observed_p5


@dataclass(frozen=True)
class LocalParameters:
    depth: int = 8
    penalty: float = 10.0
    group_bonus: float = 1.06


@dataclass
class EvaluationLedger:
    total_limit: int | None = None
    deadline: float | None = None
    population_evaluations: int = 0
    local_proposal_evaluations: int = 0

    @property
    def total(self) -> int:
        return self.population_evaluations + self.local_proposal_evaluations

    def can_evaluate(self) -> bool:
        if self.total_limit is not None and self.total >= self.total_limit:
            return False
        if self.deadline is not None and time.perf_counter() >= self.deadline:
            return False
        return True

    def charge(self, kind: str) -> None:
        if kind == "population":
            self.population_evaluations += 1
        elif kind == "local":
            self.local_proposal_evaluations += 1
        else:
            raise ValueError(f"unknown evaluation kind: {kind}")
        if self.total_limit is not None and self.total > self.total_limit:
            raise RuntimeError("evaluation budget exceeded")


@dataclass
class SearchResult:
    population: np.ndarray
    population_evaluations: int
    local_proposal_evaluations: int
    accepted_local_moves: int
    repair_drops: int
    generations_or_steps: int


def evaluate_candidate(
    problem: core.PortfolioProblem,
    x: np.ndarray,
    ledger: EvaluationLedger,
    kind: str,
) -> tuple[np.ndarray, float] | None:
    if not ledger.can_evaluate():
        return None
    f = problem.objectives(x[None, :])[0]
    violation = float(problem.violation(x[None, :])[0])
    ledger.charge(kind)
    return f, violation


def repair_to_budget(x: np.ndarray, problem: core.PortfolioProblem) -> int:
    benefit = problem.reliability + problem.renewable + problem.load_support + problem.quality
    score = benefit / np.maximum(problem.cost, 1.0)
    drops = 0
    while float(x @ problem.cost) > problem.budget and x.sum() > 0:
        selected = np.where(x > 0)[0]
        worst = int(selected[np.argmin(score[selected])])
        x[worst] = 0.0
        drops += 1
    return drops


def crowding_distance(f: np.ndarray) -> np.ndarray:
    return core._crowding_distance(f)  # type: ignore[attr-defined]


def reduce_population(
    x: np.ndarray,
    f: np.ndarray,
    violation: np.ndarray,
    limit: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    fronts = core._simple_nds(f, violation)  # type: ignore[attr-defined]
    selected: list[int] = []
    for front in fronts:
        if len(selected) + len(front) <= limit:
            selected.extend(int(idx) for idx in front)
        else:
            distance = crowding_distance(f[front])
            order = front[np.argsort(-distance, kind="stable")]
            selected.extend(int(idx) for idx in order[: limit - len(selected)])
            break
    indices = np.asarray(selected, dtype=int)
    return x[indices], f[indices], violation[indices]


def low_density_start(
    problem: core.PortfolioProblem,
    rng: np.random.Generator,
    ledger: EvaluationLedger,
    repair: bool,
    pop_size: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    xs: list[np.ndarray] = []
    fs: list[np.ndarray] = []
    violations: list[float] = []
    repair_drops = 0
    while len(xs) < pop_size and ledger.can_evaluate():
        density = float(rng.uniform(0.03, 0.15))
        x = (rng.random(problem.n) < density).astype(float)
        if repair:
            repair_drops += repair_to_budget(x, problem)
        result = evaluate_candidate(problem, x, ledger, "population")
        if result is None:
            break
        f, violation = result
        xs.append(x)
        fs.append(f)
        violations.append(violation)
    if not xs:
        raise RuntimeError("deadline expired before one initialization evaluation")
    return np.asarray(xs), np.asarray(fs), np.asarray(violations), repair_drops


def scalar_fitness(f: np.ndarray, violation: float, lo: np.ndarray, hi: np.ndarray, penalty: float) -> float:
    normalized = (f - lo) / np.maximum(hi - lo, 1e-12)
    return float(normalized.sum() + penalty * violation)


def local_improve(
    x: np.ndarray,
    current_f: np.ndarray,
    current_violation: float,
    problem: core.PortfolioProblem,
    parameters: LocalParameters,
    lo: np.ndarray,
    hi: np.ndarray,
    ledger: EvaluationLedger,
) -> tuple[np.ndarray, np.ndarray, float, int]:
    benefit = problem.reliability + problem.renewable + problem.load_support + problem.quality
    bcr = benefit / np.maximum(problem.cost, 1.0)
    accepted = 0

    for _ in range(parameters.depth):
        cost_now = float(x @ problem.cost)
        unselected = np.where((x < 1) & (problem.cost <= problem.budget - cost_now))[0]
        if unselected.size == 0 or not ledger.can_evaluate():
            break
        order_score = bcr[unselected].copy()
        selected_groups = {problem.groups[i] for i in np.where(x > 0)[0]}
        order_score *= np.array(
            [parameters.group_bonus if problem.groups[i] in selected_groups else 1.0 for i in unselected]
        )
        candidate_index = int(unselected[np.argmax(order_score)])
        proposal = x.copy()
        proposal[candidate_index] = 1.0
        result = evaluate_candidate(problem, proposal, ledger, "local")
        if result is None:
            break
        proposal_f, proposal_violation = result
        before = scalar_fitness(current_f, current_violation, lo, hi, parameters.penalty)
        after = scalar_fitness(proposal_f, proposal_violation, lo, hi, parameters.penalty)
        if after < before:
            x, current_f, current_violation = proposal, proposal_f, proposal_violation
            accepted += 1
        else:
            break

    for _ in range(max(2, parameters.depth // 2)):
        selected = np.where(x > 0)[0]
        if selected.size <= 2 or not ledger.can_evaluate():
            break
        weakest = int(selected[np.argmin(bcr[selected])])
        proposal = x.copy()
        proposal[weakest] = 0.0
        slack = problem.budget - float(proposal @ problem.cost)
        candidates = np.where((proposal < 1) & (problem.cost <= slack))[0]
        candidates = candidates[candidates != weakest]
        if candidates.size == 0:
            break
        proposal_score = bcr[candidates].copy()
        selected_groups = {problem.groups[i] for i in np.where(proposal > 0)[0]}
        proposal_score *= np.array(
            [parameters.group_bonus if problem.groups[i] in selected_groups else 1.0 for i in candidates]
        )
        replacement = int(candidates[np.argmax(proposal_score)])
        proposal[replacement] = 1.0
        result = evaluate_candidate(problem, proposal, ledger, "local")
        if result is None:
            break
        proposal_f, proposal_violation = result
        before = scalar_fitness(current_f, current_violation, lo, hi, parameters.penalty)
        after = scalar_fitness(proposal_f, proposal_violation, lo, hi, parameters.penalty)
        if after < before:
            x, current_f, current_violation = proposal, proposal_f, proposal_violation
            accepted += 1
        else:
            break
    return x, current_f, current_violation, accepted


def run_bilo(
    problem: core.PortfolioProblem,
    seed: int,
    ledger: EvaluationLedger,
    pop_size: int,
    parameters: LocalParameters,
) -> SearchResult:
    rng = np.random.default_rng(seed)
    pop_x, pop_f, pop_v, repair_drops = low_density_start(problem, rng, ledger, True, pop_size)
    accepted = 0
    generations = 0
    while ledger.can_evaluate():
        count = min(pop_size, ledger.total_limit - ledger.total) if ledger.total_limit is not None else pop_size
        if count <= 0:
            break
        idx_a = rng.integers(0, pop_x.shape[0], count)
        idx_b = rng.integers(0, pop_x.shape[0], count)
        mask = rng.random((count, problem.n)) < 0.5
        children_x = np.where(mask, pop_x[idx_a], pop_x[idx_b])
        flips = rng.random((count, problem.n)) < (1.0 / problem.n)
        children_x = np.abs(children_x - flips.astype(float))
        child_x_rows: list[np.ndarray] = []
        child_f_rows: list[np.ndarray] = []
        child_v_rows: list[float] = []
        for child in children_x:
            if not ledger.can_evaluate():
                break
            repair_drops += repair_to_budget(child, problem)
            evaluated = evaluate_candidate(problem, child, ledger, "population")
            if evaluated is None:
                break
            f, violation = evaluated
            child_x_rows.append(child.copy())
            child_f_rows.append(f)
            child_v_rows.append(violation)
        if not child_x_rows:
            break
        child_x = np.asarray(child_x_rows)
        child_f = np.asarray(child_f_rows)
        child_v = np.asarray(child_v_rows)
        generation_f = np.vstack([pop_f, child_f])
        lo_g = generation_f.min(axis=0)
        hi_g = generation_f.max(axis=0)
        for index in range(min(pop_size // 2, child_x.shape[0])):
            if not ledger.can_evaluate():
                break
            improved = local_improve(
                child_x[index].copy(),
                child_f[index].copy(),
                float(child_v[index]),
                problem,
                parameters,
                lo_g,
                hi_g,
                ledger,
            )
            child_x[index], child_f[index], child_v[index], moves = improved
            accepted += moves
        union_x = np.vstack([pop_x, child_x])
        union_f = np.vstack([pop_f, child_f])
        union_v = np.concatenate([pop_v, child_v])
        pop_x, pop_f, pop_v = reduce_population(union_x, union_f, union_v, pop_size)
        generations += 1
    return SearchResult(
        pop_x,
        ledger.population_evaluations,
        ledger.local_proposal_evaluations,
        accepted,
        repair_drops,
        generations,
    )


def rank_and_crowding(f: np.ndarray, violation: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    fronts = core._simple_nds(f, violation)  # type: ignore[attr-defined]
    rank = np.empty(f.shape[0], dtype=int)
    crowd = np.zeros(f.shape[0])
    for rank_index, front in enumerate(fronts):
        rank[front] = rank_index
        crowd[front] = crowding_distance(f[front])
    return rank, crowd


def tournament(
    rng: np.random.Generator,
    rank: np.ndarray,
    crowd: np.ndarray,
) -> int:
    left, right = (int(value) for value in rng.integers(0, rank.size, 2))
    if rank[left] != rank[right]:
        return left if rank[left] < rank[right] else right
    if crowd[left] != crowd[right]:
        return left if crowd[left] > crowd[right] else right
    return left if rng.random() < 0.5 else right


def nsga_child(
    pop_x: np.ndarray,
    rank: np.ndarray,
    crowd: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    first = pop_x[tournament(rng, rank, crowd)]
    second = pop_x[tournament(rng, rank, crowd)]
    child = first.copy()
    if child.size > 2 and rng.random() < 0.9:
        points = np.sort(rng.choice(np.arange(1, child.size), size=2, replace=False))
        child[points[0] : points[1]] = second[points[0] : points[1]]
    flips = rng.random(child.size) < (1.0 / child.size)
    return np.abs(child - flips.astype(float))


def run_nsga2(
    problem: core.PortfolioProblem,
    seed: int,
    ledger: EvaluationLedger,
    pop_size: int,
) -> SearchResult:
    rng = np.random.default_rng(seed)
    pop_x, pop_f, pop_v, _ = low_density_start(problem, rng, ledger, False, pop_size)
    generations = 0
    while ledger.can_evaluate():
        rank, crowd = rank_and_crowding(pop_f, pop_v)
        child_x_rows: list[np.ndarray] = []
        child_f_rows: list[np.ndarray] = []
        child_v_rows: list[float] = []
        while len(child_x_rows) < pop_size and ledger.can_evaluate():
            child = nsga_child(pop_x, rank, crowd, rng)
            evaluated = evaluate_candidate(problem, child, ledger, "population")
            if evaluated is None:
                break
            f, violation = evaluated
            child_x_rows.append(child)
            child_f_rows.append(f)
            child_v_rows.append(violation)
        if not child_x_rows:
            break
        child_x = np.asarray(child_x_rows)
        child_f = np.asarray(child_f_rows)
        child_v = np.asarray(child_v_rows)
        pop_x, pop_f, pop_v = reduce_population(
            np.vstack([pop_x, child_x]),
            np.vstack([pop_f, child_f]),
            np.concatenate([pop_v, child_v]),
            pop_size,
        )
        generations += 1
    return SearchResult(
        pop_x,
        ledger.population_evaluations,
        ledger.local_proposal_evaluations,
        0,
        0,
        generations,
    )


def pls_proposal(
    x: np.ndarray,
    step: int,
    problem: core.PortfolioProblem,
    bcr: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray | None:
    for offset in range(3):
        move = (step + offset) % 3
        selected = np.where(x > 0)[0]
        unselected = np.where(x < 1)[0]
        proposal = x.copy()
        if move == 0 and unselected.size:
            slack = problem.budget - float(x @ problem.cost)
            feasible_add = unselected[problem.cost[unselected] <= slack]
            if feasible_add.size:
                top = feasible_add[np.argsort(-bcr[feasible_add])[: min(8, feasible_add.size)]]
                proposal[int(rng.choice(top))] = 1.0
                return proposal
        elif move == 1 and selected.size > 1:
            bottom = selected[np.argsort(bcr[selected])[: min(8, selected.size)]]
            proposal[int(rng.choice(bottom))] = 0.0
            return proposal
        elif move == 2 and selected.size and unselected.size:
            bottom = selected[np.argsort(bcr[selected])[: min(8, selected.size)]]
            removed = int(rng.choice(bottom))
            proposal[removed] = 0.0
            slack = problem.budget - float(proposal @ problem.cost)
            feasible_add = unselected[problem.cost[unselected] <= slack]
            feasible_add = feasible_add[feasible_add != removed]
            if feasible_add.size:
                top = feasible_add[np.argsort(-bcr[feasible_add])[: min(8, feasible_add.size)]]
                proposal[int(rng.choice(top))] = 1.0
                return proposal
    return None


def reduce_pls_archive(
    archive_x: np.ndarray,
    archive_f: np.ndarray,
    problem: core.PortfolioProblem,
    limit: int,
) -> tuple[np.ndarray, np.ndarray]:
    unique_x, indices = np.unique(archive_x, axis=0, return_index=True)
    unique_f = archive_f[indices]
    feasible = problem.violation(unique_x) <= 1e-12
    unique_x, unique_f = unique_x[feasible], unique_f[feasible]
    if unique_x.shape[0] == 0:
        return np.zeros((0, problem.n)), np.zeros((0, problem.n_obj))
    keep = core.nondominated(unique_f)
    unique_x, unique_f = unique_x[keep], unique_f[keep]
    if unique_x.shape[0] > limit:
        order = np.argsort(-crowding_distance(unique_f), kind="stable")[:limit]
        unique_x, unique_f = unique_x[order], unique_f[order]
    return unique_x, unique_f


def update_pls_archive(
    archive_x: np.ndarray,
    archive_f: np.ndarray,
    proposal_x: np.ndarray,
    proposal_f: np.ndarray,
    limit: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Incrementally update a feasible non-dominated archive.

    PLS constructs feasible proposals, so this hot path needs only duplicate
    and dominance checks; it does not re-evaluate the full archive.
    """

    if np.any(np.all(archive_x == proposal_x, axis=1)):
        return archive_x, archive_f
    proposal_dominated = np.any(
        np.all(archive_f <= proposal_f, axis=1) & np.any(archive_f < proposal_f, axis=1)
    )
    if proposal_dominated:
        return archive_x, archive_f
    dominated = np.all(proposal_f <= archive_f, axis=1) & np.any(proposal_f < archive_f, axis=1)
    next_x = np.vstack([archive_x[~dominated], proposal_x])
    next_f = np.vstack([archive_f[~dominated], proposal_f])
    if next_x.shape[0] > limit:
        order = np.argsort(-crowding_distance(next_f), kind="stable")[:limit]
        next_x, next_f = next_x[order], next_f[order]
    return next_x, next_f


def run_pls(
    problem: core.PortfolioProblem,
    seed: int,
    ledger: EvaluationLedger,
    pop_size: int,
) -> SearchResult:
    rng = np.random.default_rng(seed)
    start_x, start_f, _, repair_drops = low_density_start(problem, rng, ledger, True, pop_size)
    archive_x, archive_f = reduce_pls_archive(start_x, start_f, problem, pop_size)
    benefit = problem.reliability + problem.renewable + problem.load_support + problem.quality
    bcr = benefit / np.maximum(problem.cost, 1.0)
    step = 0
    while ledger.can_evaluate():
        if archive_x.shape[0] == 0:
            raise RuntimeError("PLS archive unexpectedly became empty")
        parent = archive_x[int(rng.integers(0, archive_x.shape[0]))]
        proposal = pls_proposal(parent, step, problem, bcr, rng)
        if proposal is None:
            raise RuntimeError("PLS could not construct an add, delete, or swap proposal")
        evaluated = evaluate_candidate(problem, proposal, ledger, "local")
        if evaluated is None:
            break
        proposal_f, _ = evaluated
        archive_x, archive_f = update_pls_archive(
            archive_x, archive_f, proposal, proposal_f, pop_size
        )
        step += 1
    return SearchResult(
        archive_x,
        ledger.population_evaluations,
        ledger.local_proposal_evaluations,
        0,
        repair_drops,
        step,
    )


def analytic_bounds(problem: core.PortfolioProblem) -> tuple[np.ndarray, np.ndarray]:
    for name in ("cost", "reliability", "renewable", "risk"):
        values = np.asarray(getattr(problem, name), dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError(f"non-finite candidate values in {name}")
    if np.any(problem.cost < 0) or np.any(problem.reliability < 0) or np.any(problem.renewable < 0):
        raise ValueError("analytic bounds require non-negative cost and additive benefit attributes")
    lo = np.array(
        [
            0.0,
            -float(problem.reliability.sum()),
            -float(problem.renewable.sum()),
            min(float(problem.risk.min()), 1.0),
        ]
    )
    hi = np.array(
        [
            float(problem.budget),
            0.0,
            0.0,
            max(float(problem.risk.max()), 1.0),
        ]
    )
    if np.any(hi <= lo):
        raise ValueError("invalid analytic bounds")
    return lo, hi


def expanded_bounds(lo: np.ndarray, hi: np.ndarray, fraction: float = 0.25) -> tuple[np.ndarray, np.ndarray]:
    span = hi - lo
    return lo - fraction * span, hi + fraction * span


def normalize(front: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
    return (front - lo) / np.maximum(hi - lo, 1e-12)


def hypervolume(front: np.ndarray, lo: np.ndarray, hi: np.ndarray, reference: float, clip: bool) -> float:
    if front.size == 0:
        return 0.0
    normalized = normalize(front, lo, hi)
    if clip:
        normalized = np.clip(normalized, 0.0, 1.0)
    ref = np.full(front.shape[1], reference, dtype=float)
    normalized = normalized[np.all(normalized <= ref, axis=1)]
    if normalized.shape[0] == 0:
        return 0.0
    return float(HyperVolume(ref).compute(normalized.tolist()))


def clipping_counts(front: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> tuple[int, int, int]:
    if front.size == 0:
        return 0, 0, 0
    normalized = normalize(front, lo, hi)
    lower = normalized < -1e-12
    upper = normalized > 1.0 + 1e-12
    return int(lower.sum()), int(upper.sum()), int(np.any(lower | upper, axis=1).sum())


def front_hash(front: np.ndarray) -> str:
    if front.size == 0:
        return hashlib.sha256(b"").hexdigest()
    keys = tuple(front[:, index] for index in reversed(range(front.shape[1])))
    ordered = front[np.lexsort(keys)]
    return hashlib.sha256(np.round(ordered, 12).astype("<f8").tobytes()).hexdigest()


def scenario_seed(scenario: str, seed_index: int) -> int:
    digest = hashlib.sha1(f"p6_s3|{scenario}".encode("utf-8")).hexdigest()
    return 900000 + 7919 * seed_index + int(digest[:6], 16) % 4096


def protocol_ledger(protocol: str, config: dict, search_start: float) -> EvaluationLedger:
    if protocol == "matched_evaluation":
        return EvaluationLedger(total_limit=int(config["protocols"][protocol]["total_evaluation_units"]))
    if protocol == "matched_time":
        target = float(config["protocols"][protocol]["search_time_limit_seconds"])
        return EvaluationLedger(deadline=search_start + target)
    raise ValueError(f"unknown protocol: {protocol}")


def execute_search(
    method: str,
    problem: core.PortfolioProblem,
    seed: int,
    protocol: str,
    config: dict,
    parameters: LocalParameters | None = None,
) -> tuple[SearchResult, float]:
    search_start = time.perf_counter()
    ledger = protocol_ledger(protocol, config, search_start)
    pop_size = int(config["population_size"])
    if method == "BiLo-NSGA":
        result = run_bilo(problem, seed, ledger, pop_size, parameters or LocalParameters())
    elif method == "NSGA-II":
        result = run_nsga2(problem, seed, ledger, pop_size)
    elif method == "Pareto Local Search":
        result = run_pls(problem, seed, ledger, pop_size)
    else:
        raise ValueError(f"unknown method: {method}")
    search_runtime = time.perf_counter() - search_start
    if protocol == "matched_evaluation" and result.population_evaluations + result.local_proposal_evaluations != ledger.total_limit:
        raise RuntimeError(f"{method} did not consume the exact evaluation budget")
    return result, search_runtime


def scenario_context(
    scenario: str,
    candidates: list[core.Candidate],
) -> tuple[list[core.Candidate], core.PortfolioProblem, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    pool = core.experiment_pool(scenario, candidates)
    problem = core.PortfolioProblem(pool, "p6", core.budget_for(scenario, "p6"))
    empirical_lo, empirical_hi = core.normalization_bounds(problem)
    analytic_lo, analytic_hi = analytic_bounds(problem)
    return pool, problem, empirical_lo, empirical_hi, analytic_lo, analytic_hi


def execute_cell(
    protocol: str,
    scenario: str,
    method: str,
    seed_index: int,
    sequence_order: int,
    context: tuple[list[core.Candidate], core.PortfolioProblem, np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    config: dict,
    parameters: LocalParameters | None = None,
) -> tuple[dict[str, str], np.ndarray, np.ndarray]:
    pool, problem, empirical_lo, empirical_hi, _, _ = context
    seed = scenario_seed(scenario, seed_index)
    run_start = time.perf_counter()
    result, search_runtime = execute_search(method, problem, seed, protocol, config, parameters)
    front_x, front_f = core.feasible_front(problem, result.population)
    reported_hv = hypervolume(front_f, empirical_lo, empirical_hi, 1.1, True)
    total_runtime = time.perf_counter() - run_start
    feasibility = problem.violation(result.population) <= 1e-12
    time_target = (
        float(config["protocols"]["matched_time"]["search_time_limit_seconds"])
        if protocol == "matched_time"
        else float("nan")
    )
    row = {
        "protocol": protocol,
        "scenario": scenario,
        "method": method,
        "seed_index": str(seed_index),
        "seed_value": str(seed),
        "execution_order_within_seed": str(sequence_order),
        "candidate_pool_size": str(len(pool)),
        "budget": fmt(problem.budget),
        "hypervolume": fmt(reported_hv),
        "search_runtime_s": fmt(search_runtime),
        "total_run_runtime_s": fmt(total_runtime),
        "target_search_runtime_s": fmt(time_target),
        "deadline_overshoot_s": fmt(search_runtime - time_target) if protocol == "matched_time" else "nan",
        "population_objective_evaluations": str(result.population_evaluations),
        "local_proposal_evaluations": str(result.local_proposal_evaluations),
        "total_evaluation_units": str(result.population_evaluations + result.local_proposal_evaluations),
        "accepted_local_moves": str(result.accepted_local_moves),
        "repair_drops": str(result.repair_drops),
        "generations_or_steps": str(result.generations_or_steps),
        "final_population_size": str(result.population.shape[0]),
        "final_population_feasibility_rate": fmt(float(np.mean(feasibility))),
        "feasible_front_nonempty": "1" if front_f.shape[0] else "0",
        "feasible_front_size": str(front_f.shape[0]),
        "front_objectives_sha256": front_hash(front_f),
    }
    return row, front_x, front_f


def hypervolume_scheme_rows(
    main_row: dict[str, str],
    front: np.ndarray,
    context: tuple[list[core.Candidate], core.PortfolioProblem, np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    config: dict,
) -> list[dict[str, str]]:
    _, _, empirical_lo, empirical_hi, analytic_lo, analytic_hi = context
    expanded_lo, expanded_hi = expanded_bounds(empirical_lo, empirical_hi)
    bounds = {
        "reported_empirical_ref1p1_clipped": (empirical_lo, empirical_hi),
        "reported_empirical_ref1p1_unclipped": (empirical_lo, empirical_hi),
        "expanded_empirical_ref1p1_unclipped": (expanded_lo, expanded_hi),
        "analytic_ref1p05_unclipped": (analytic_lo, analytic_hi),
        "analytic_ref1p1_unclipped": (analytic_lo, analytic_hi),
        "analytic_ref1p2_unclipped": (analytic_lo, analytic_hi),
    }
    rows: list[dict[str, str]] = []
    for scheme in config["hypervolume_schemes"]:
        lo, hi = bounds[scheme["id"]]
        low, high, points = clipping_counts(front, lo, hi)
        rows.append(
            {
                "protocol": main_row["protocol"],
                "scenario": main_row["scenario"],
                "method": main_row["method"],
                "seed_index": main_row["seed_index"],
                "scheme": scheme["id"],
                "reference_point": fmt(float(scheme["reference_point"])),
                "clip": "1" if scheme["clip"] else "0",
                "hypervolume": fmt(
                    hypervolume(front, lo, hi, float(scheme["reference_point"]), bool(scheme["clip"]))
                ),
                "below_zero_coordinates": str(low),
                "above_one_coordinates": str(high),
                "out_of_bounds_points": str(points),
                "front_size": str(front.shape[0]),
                "front_objectives_sha256": main_row["front_objectives_sha256"],
            }
        )
    return rows


def summarize_main(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["protocol"], row["scenario"], row["method"])].append(row)
    summary: list[dict[str, str]] = []
    for (protocol, scenario, method), values in sorted(grouped.items()):
        summary.append(
            {
                "protocol": protocol,
                "scenario": scenario,
                "method": method,
                "n_runs": str(len(values)),
                "mean_hypervolume": fmt(mean(float(row["hypervolume"]) for row in values)),
                "sd_hypervolume": fmt(sample_sd(float(row["hypervolume"]) for row in values)),
                "median_hypervolume": fmt(median(float(row["hypervolume"]) for row in values)),
                "mean_search_runtime_s": fmt(mean(float(row["search_runtime_s"]) for row in values)),
                "mean_total_runtime_s": fmt(mean(float(row["total_run_runtime_s"]) for row in values)),
                "mean_population_objective_evaluations": fmt(
                    mean(int(row["population_objective_evaluations"]) for row in values)
                ),
                "mean_local_proposal_evaluations": fmt(
                    mean(int(row["local_proposal_evaluations"]) for row in values)
                ),
                "mean_total_evaluation_units": fmt(mean(int(row["total_evaluation_units"]) for row in values)),
                "mean_final_population_feasibility_rate": fmt(
                    mean(float(row["final_population_feasibility_rate"]) for row in values)
                ),
                "nonempty_feasible_front_rate": fmt(
                    mean(int(row["feasible_front_nonempty"]) for row in values)
                ),
                "mean_feasible_front_size": fmt(mean(int(row["feasible_front_size"]) for row in values)),
            }
        )
    return summary


def exact_two_sided_sign_p(differences: list[float]) -> tuple[float, int, int, int]:
    positive = sum(value > 0 for value in differences)
    negative = sum(value < 0 for value in differences)
    n = positive + negative
    if n == 0:
        return 1.0, positive, negative, n
    tail = min(positive, negative)
    probability = 2.0 * sum(math.comb(n, index) for index in range(tail + 1)) / (2**n)
    return min(1.0, probability), positive, negative, n


def holm_adjust(pvalues: list[float]) -> list[float]:
    order = sorted(range(len(pvalues)), key=pvalues.__getitem__)
    adjusted = [1.0] * len(pvalues)
    running = 0.0
    total = len(pvalues)
    for rank, index in enumerate(order):
        value = min(1.0, (total - rank) * pvalues[index])
        running = max(running, value)
        adjusted[index] = running
    return adjusted


def inference_rows(rows: list[dict[str, str]], config: dict) -> list[dict[str, str]]:
    index = {
        (row["protocol"], row["scenario"], row["method"], int(row["seed_index"])): float(row["hypervolume"])
        for row in rows
    }
    output: list[dict[str, str]] = []
    for protocol, family in (
        ("matched_evaluation", "primary_matched_evaluation_16"),
        ("matched_time", "secondary_matched_time_16"),
    ):
        family_rows: list[dict[str, str]] = []
        raw_pvalues: list[float] = []
        for scenario in config["scenarios"]:
            proposed = [index[(protocol, scenario, "BiLo-NSGA", seed)] for seed in range(30)]
            for comparator in COMPARATORS:
                baseline = [index[(protocol, scenario, comparator, seed)] for seed in range(30)]
                differences = [left - right for left, right in zip(proposed, baseline)]
                pvalue, positive, negative, nonzero = exact_two_sided_sign_p(differences)
                raw_pvalues.append(pvalue)
                family_rows.append(
                    {
                        "family": family,
                        "family_size": "16",
                        "protocol": protocol,
                        "scenario": scenario,
                        "proposed": "BiLo-NSGA",
                        "comparator": comparator,
                        "n_pairs": "30",
                        "n_nonzero_pairs": str(nonzero),
                        "positive_pairs": str(positive),
                        "negative_pairs": str(negative),
                        "mean_difference": fmt(mean(differences)),
                        "median_difference": fmt(median(differences)),
                        "raw_sign_test_p": fmt(pvalue),
                        "holm_adjusted_p": "",
                        "holm_significant_0p05": "",
                        "test": config["multiplicity"]["test"],
                    }
                )
        adjusted = holm_adjust(raw_pvalues)
        for row, value in zip(family_rows, adjusted):
            row["holm_adjusted_p"] = fmt(value)
            row["holm_significant_0p05"] = "1" if value < 0.05 else "0"
        output.extend(family_rows)
    return output


def summarize_hv_sensitivity(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["scenario"], row["method"], row["scheme"])].append(row)
    output: list[dict[str, str]] = []
    for (scenario, method, scheme), values in sorted(grouped.items()):
        output.append(
            {
                "scenario": scenario,
                "method": method,
                "scheme": scheme,
                "n_runs": str(len(values)),
                "mean_hypervolume": fmt(mean(float(row["hypervolume"]) for row in values)),
                "sd_hypervolume": fmt(sample_sd(float(row["hypervolume"]) for row in values)),
                "total_out_of_bounds_points": str(sum(int(row["out_of_bounds_points"]) for row in values)),
                "total_front_points": str(sum(int(row["front_size"]) for row in values)),
            }
        )
    return output


def run_local_sensitivity(
    main_rows: list[dict[str, str]],
    contexts: dict[str, tuple[list[core.Candidate], core.PortfolioProblem, np.ndarray, np.ndarray, np.ndarray, np.ndarray]],
    config: dict,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    registered = {
        (row["scenario"], int(row["seed_index"])): row
        for row in main_rows
        if row["protocol"] == "matched_evaluation"
        and row["method"] == "BiLo-NSGA"
        and int(row["seed_index"]) < int(config["local_sensitivity"]["seeds_per_cell"])
    }
    results: list[dict[str, str]] = []
    for cell in config["local_sensitivity"]["cells"]:
        parameters = LocalParameters(
            int(cell["local_depth"]),
            float(cell["local_violation_penalty"]),
            float(cell["dependency_group_order_bonus"]),
        )
        for scenario in config["scenarios"]:
            context = contexts[scenario]
            if cell["id"] == "registered":
                for seed_index in range(int(config["local_sensitivity"]["seeds_per_cell"])):
                    source = registered[(scenario, seed_index)]
                    results.append(
                        {
                            "cell": cell["id"],
                            "factor": cell["factor"],
                            "scenario": scenario,
                            "seed_index": str(seed_index),
                            "seed_value": source["seed_value"],
                            "local_depth": str(parameters.depth),
                            "local_violation_penalty": fmt(parameters.penalty),
                            "dependency_group_order_bonus": fmt(parameters.group_bonus),
                            "hypervolume": source["hypervolume"],
                            "search_runtime_s": source["search_runtime_s"],
                            "population_objective_evaluations": source["population_objective_evaluations"],
                            "local_proposal_evaluations": source["local_proposal_evaluations"],
                            "total_evaluation_units": source["total_evaluation_units"],
                            "final_population_feasibility_rate": source["final_population_feasibility_rate"],
                            "feasible_front_size": source["feasible_front_size"],
                            "source": "reused_primary_matched_evaluation_run",
                        }
                    )
            else:
                for seed_index in range(int(config["local_sensitivity"]["seeds_per_cell"])):
                    row, _, _ = execute_cell(
                        "matched_evaluation",
                        scenario,
                        "BiLo-NSGA",
                        seed_index,
                        0,
                        context,
                        config,
                        parameters,
                    )
                    results.append(
                        {
                            "cell": cell["id"],
                            "factor": cell["factor"],
                            "scenario": scenario,
                            "seed_index": str(seed_index),
                            "seed_value": row["seed_value"],
                            "local_depth": str(parameters.depth),
                            "local_violation_penalty": fmt(parameters.penalty),
                            "dependency_group_order_bonus": fmt(parameters.group_bonus),
                            "hypervolume": row["hypervolume"],
                            "search_runtime_s": row["search_runtime_s"],
                            "population_objective_evaluations": row["population_objective_evaluations"],
                            "local_proposal_evaluations": row["local_proposal_evaluations"],
                            "total_evaluation_units": row["total_evaluation_units"],
                            "final_population_feasibility_rate": row["final_population_feasibility_rate"],
                            "feasible_front_size": row["feasible_front_size"],
                            "source": "new_stage_local_run",
                        }
                    )
            print(f"[local sensitivity] {cell['id']} | {scenario}: done", flush=True)
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in results:
        grouped[(row["cell"], row["scenario"])].append(row)
    summary: list[dict[str, str]] = []
    for (cell, scenario), values in sorted(grouped.items()):
        summary.append(
            {
                "cell": cell,
                "scenario": scenario,
                "n_runs": str(len(values)),
                "mean_hypervolume": fmt(mean(float(row["hypervolume"]) for row in values)),
                "sd_hypervolume": fmt(sample_sd(float(row["hypervolume"]) for row in values)),
                "mean_search_runtime_s": fmt(mean(float(row["search_runtime_s"]) for row in values)),
                "mean_local_proposal_evaluations": fmt(
                    mean(int(row["local_proposal_evaluations"]) for row in values)
                ),
                "mean_final_population_feasibility_rate": fmt(
                    mean(float(row["final_population_feasibility_rate"]) for row in values)
                ),
            }
        )
    overall: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in results:
        overall[row["cell"]].append(row)
    reference_mean = mean(float(row["hypervolume"]) for row in overall["registered"])
    effects: list[dict[str, str]] = []
    cell_index = {cell["id"]: cell for cell in config["local_sensitivity"]["cells"]}
    for cell, values in sorted(overall.items()):
        value = mean(float(row["hypervolume"]) for row in values)
        effects.append(
            {
                "cell": cell,
                "factor": cell_index[cell]["factor"],
                "n_runs": str(len(values)),
                "scenario_balanced_mean_hypervolume": fmt(value),
                "difference_from_registered": fmt(value - reference_mean),
                "relative_difference_percent": fmt(100.0 * (value / reference_mean - 1.0)),
                "inference": "descriptive_no_p_values",
            }
        )
    return results, summary, effects


def environment_record() -> dict[str, object]:
    def version(name: str) -> str:
        try:
            return importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            return "not-installed"

    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=HARNESS_ROOT, text=True, encoding="utf-8"
        ).strip()
    except Exception:
        commit = "unavailable"
    return {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "numpy": np.__version__,
        "scipy_distribution": version("scipy"),
        "scipy_runtime_mode": SCIPY_MODE,
        "pymoo": version("pymoo"),
        "pymoo_usage": "pure-Python pymoo 0.4.1 HyperVolume indicator only; no pymoo optimizer",
        "git_commit": commit,
        "shared_source_sha256": sha256_file(SHARED_MODULE),
        "runner_sha256": sha256_file(Path(__file__)),
        "cpu_count": os.cpu_count(),
    }


def analysis_markdown(
    summary: list[dict[str, str]],
    inference: list[dict[str, str]],
    hv_summary: list[dict[str, str]],
    local_effects: list[dict[str, str]],
) -> str:
    pooled: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in summary:
        pooled[(row["protocol"], row["method"])].append(row)

    lines = [
        "# P6 S3 Matched-Effort Analysis",
        "",
        "## Protocol",
        "",
        "Each matched-evaluation run consumed exactly 3,200 search-evaluation units. "
        "Each matched-time run used the same 0.20-second search deadline; realized times and "
        "deadline overshoot are retained per run. Hypervolume uses only the final feasible "
        "non-dominated front.",
        "",
        "## Scenario-balanced descriptive means",
        "",
        "| Protocol | Method | Mean HV | Mean search runtime (s) | Mean feasibility rate |",
        "|---|---|---:|---:|---:|",
    ]
    for protocol in ("matched_evaluation", "matched_time"):
        for method in METHODS:
            values = pooled[(protocol, method)]
            lines.append(
                f"| {protocol} | {method} | "
                f"{mean(float(row['mean_hypervolume']) for row in values):.6f} | "
                f"{mean(float(row['mean_search_runtime_s']) for row in values):.6f} | "
                f"{mean(float(row['mean_final_population_feasibility_rate']) for row in values):.6f} |"
            )
    lines.extend(
        [
            "",
            "## Declared multiplicity families",
            "",
            "The primary family is the 16 matched-evaluation BiLo-NSGA contrasts (two "
            "comparators by eight scenarios). The matched-time protocol is a separate "
            "16-contrast secondary family. Both use exact paired sign tests and Holm "
            "correction. Sensitivity outputs are descriptive.",
            "",
            "| Family | Significant contrasts | Positive mean differences | Total |",
            "|---|---:|---:|---:|",
        ]
    )
    for family in ("primary_matched_evaluation_16", "secondary_matched_time_16"):
        values = [row for row in inference if row["family"] == family]
        lines.append(
            f"| {family} | {sum(row['holm_significant_0p05'] == '1' for row in values)} | "
            f"{sum(float(row['mean_difference']) > 0 for row in values)} | {len(values)} |"
        )
    registered_hv = [
        row for row in hv_summary if row["scheme"] == "reported_empirical_ref1p1_clipped"
    ]
    analytic_hv = [row for row in hv_summary if row["scheme"] == "analytic_ref1p1_unclipped"]
    lines.extend(
        [
            "",
            "## Hypervolume and local-parameter sensitivity",
            "",
            f"The registered scheme's scenario/method cells have an unweighted mean HV of "
            f"{mean(float(row['mean_hypervolume']) for row in registered_hv):.6f}; the "
            f"analytic-bound reference-1.1 scheme has {mean(float(row['mean_hypervolume']) for row in analytic_hv):.6f}. "
            "These scales are not interchangeable. The CSVs retain per-run clipping incidence "
            "and the reference-point alternatives.",
            "",
            "The one-factor local scan retains every registered and adverse/null setting. "
            "Scenario-balanced descriptive differences from the registered cell are:",
            "",
            "| Cell | Difference in mean HV | Relative difference (%) |",
            "|---|---:|---:|",
        ]
    )
    for row in local_effects:
        lines.append(
            f"| {row['cell']} | {float(row['difference_from_registered']):+.6f} | "
            f"{float(row['relative_difference_percent']):+.3f} |"
        )
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "The NSGA-II search is the fully specified stage-local implementation recorded in "
            "the config, not a silent substitution for the unavailable recorded pymoo 0.6.2 "
            "runtime. Wall-clock results are machine-specific. PLS evidence applies to this "
            "bounded add/delete/swap implementation. No result establishes deployment, expert "
            "agreement, calibrated economics, or electrical feasibility.",
        ]
    )
    return "\n".join(lines)


def execute(config_path: Path, output_root: Path) -> None:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("stage") != "p6_s3_matched_effort":
        raise ValueError("wrong stage config")
    allowed_root = (STAGE_ROOT / "runs").resolve()
    resolved_output = output_root.resolve()
    if not resolved_output.is_relative_to(allowed_root):
        raise ValueError(f"output root must be beneath {allowed_root}")
    if output_root.exists():
        raise FileExistsError(f"immutable output root already exists: {output_root}")

    p5_before = validate_source_contract(config)
    inputs = configure_data_sources(config)
    started = datetime.now(timezone.utc)
    output_root.mkdir(parents=True, exist_ok=False)
    write_json(output_root / "config_snapshot.json", config)
    write_json(output_root / "environment.json", environment_record())
    passport = [
        {
            "path": path.as_posix(),
            "bytes": str(path.stat().st_size),
            "sha256": sha256_file(path),
        }
        for path in inputs
    ]
    write_csv(output_root / "input_material_passport.csv", passport)

    candidates = core.build_candidates()
    contexts = {scenario: scenario_context(scenario, candidates) for scenario in config["scenarios"]}
    main_rows: list[dict[str, str]] = []
    hv_rows: list[dict[str, str]] = []
    for protocol in ("matched_evaluation", "matched_time"):
        for scenario in config["scenarios"]:
            context = contexts[scenario]
            for seed_index in range(int(config["seeds_per_method_scenario"])):
                offset = seed_index % len(METHODS)
                order = METHODS[offset:] + METHODS[:offset]
                for sequence_order, method in enumerate(order):
                    row, _, front_f = execute_cell(
                        protocol,
                        scenario,
                        method,
                        seed_index,
                        sequence_order,
                        context,
                        config,
                    )
                    main_rows.append(row)
                    if protocol == "matched_evaluation":
                        hv_rows.extend(hypervolume_scheme_rows(row, front_f, context, config))
            print(f"[{protocol}] {scenario}: 3 methods x 30 seeds done", flush=True)

    summary = summarize_main(main_rows)
    inference = inference_rows(main_rows, config)
    hv_summary = summarize_hv_sensitivity(hv_rows)
    local_rows, local_summary, local_effects = run_local_sensitivity(main_rows, contexts, config)

    write_csv(output_root / "matched_results.csv", main_rows)
    write_csv(output_root / "matched_summary.csv", summary)
    write_csv(output_root / "matched_inference.csv", inference)
    write_csv(output_root / "hypervolume_sensitivity_results.csv", hv_rows)
    write_csv(output_root / "hypervolume_sensitivity_summary.csv", hv_summary)
    write_csv(output_root / "local_sensitivity_results.csv", local_rows)
    write_csv(output_root / "local_sensitivity_summary.csv", local_summary)
    write_csv(output_root / "local_sensitivity_effects.csv", local_effects)
    write_text(output_root / "analysis.md", analysis_markdown(summary, inference, hv_summary, local_effects))

    evaluation_rows = [row for row in main_rows if row["protocol"] == "matched_evaluation"]
    time_rows = [row for row in main_rows if row["protocol"] == "matched_time"]
    expected_units = int(config["protocols"]["matched_evaluation"]["total_evaluation_units"])
    p5_after = p5_hashes(config)
    checks = {
        "candidate_count": len(candidates),
        "main_row_count": len(main_rows),
        "matched_evaluation_row_count": len(evaluation_rows),
        "matched_time_row_count": len(time_rows),
        "hypervolume_sensitivity_row_count": len(hv_rows),
        "local_sensitivity_row_count": len(local_rows),
        "all_matched_evaluation_rows_exact_budget": all(
            int(row["total_evaluation_units"]) == expected_units for row in evaluation_rows
        ),
        "all_fronts_nonempty": all(row["feasible_front_nonempty"] == "1" for row in main_rows),
        "all_hypervolumes_finite": all(math.isfinite(float(row["hypervolume"])) for row in main_rows),
        "time_target_minimum_realized_s": min(float(row["search_runtime_s"]) for row in time_rows),
        "time_target_maximum_realized_s": max(float(row["search_runtime_s"]) for row in time_rows),
        "p5_hashes_before": p5_before,
        "p5_hashes_after": p5_after,
        "p5_evidence_unchanged": p5_before == p5_after,
        "shared_source_sha256": sha256_file(SHARED_MODULE),
        "runner_sha256": sha256_file(Path(__file__)),
    }
    if not checks["all_matched_evaluation_rows_exact_budget"]:
        raise RuntimeError("one or more matched-evaluation rows missed the exact budget")
    if not checks["all_hypervolumes_finite"]:
        raise RuntimeError("non-finite hypervolume detected")
    if not checks["p5_evidence_unchanged"]:
        raise RuntimeError("P5 evidence changed during the stage run")
    write_json(output_root / "validation.json", checks)
    completed = datetime.now(timezone.utc)
    write_text(
        output_root / "EXECUTION.md",
        "\n".join(
            [
                "# Execution Record",
                "",
                "- ID: p6_s3_matched_effort_primary_v1",
                f"- Started UTC: {started.isoformat()}",
                f"- Completed UTC: {completed.isoformat()}",
                f"- Duration seconds: {(completed - started).total_seconds():.3f}",
                f"- Config SHA256: {sha256_file(config_path)}",
                f"- Runner SHA256: {sha256_file(Path(__file__))}",
                f"- Shared source SHA256: {sha256_file(SHARED_MODULE)}",
                f"- Output root: {output_root.as_posix()}",
                "- Status: completed without filtering, failed-seed replacement, or result-dependent retuning",
            ]
        ),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    execute(args.config, args.output_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
