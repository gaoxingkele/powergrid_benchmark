"""Immutable p4 boundary experiment for stage p4_s3_boundary_experiments.

The runner is intentionally local to the manuscript worktree.  It freezes the
minimal SimBench subnet statistics needed by the reconciled equations, then
runs a predeclared one-at-a-time matrix without modifying the shared p3/p4
planning implementation or either paper's historical archives.

The installed Python environment has a usable NumPy and pymoo 0.4.1 but an
unusable SciPy binary.  Only NSGA-II's duplicate-distance helper needs SciPy in
that pymoo release, so ``_install_pymoo_scipy_compat`` provides the exact
Euclidean distance operation with NumPy.  No statistical routine is replaced:
the boundary report predeclares fixed-seed percentile bootstrap intervals.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import sys
import tempfile
import time
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "experiments" / "p4_s3_boundary_predeclared.json"
RUNS_PATH = PROJECT_ROOT / "evidence" / "runs" / "p4_s3_boundary_runs_20260813.csv"
ANALYSIS_PATH = PROJECT_ROOT / "evidence" / "runs" / "p4_s3_boundary_analysis_20260813.md"
SUMMARY_PATH = PROJECT_ROOT / "evidence" / "tables" / "p4_s3_boundary_summary_20260813.csv"
GAPS_PATH = PROJECT_ROOT / "evidence" / "tables" / "p4_s3_boundary_gaps_20260813.csv"
BOUNDS_PATH = PROJECT_ROOT / "evidence" / "tables" / "p4_s3_hv_bounds_20260813.csv"
MANIFEST_PATH = PROJECT_ROOT / "evidence" / "manifests" / "p4_s3_boundary_manifest_20260813.json"


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


@dataclass(frozen=True)
class Setting:
    setting_id: str
    axis: str
    budget_factor: float
    scenario_count: int
    screen_k: int
    survivability_action_scale: float


@dataclass(frozen=True)
class Method:
    name: str
    role: str
    variation_mode: str = "hybrid"
    screen_dynamic: bool = True
    nsga2_repair: bool = False


METHODS = (
    Method("SHIELD-MOEA", "proposed"),
    Method("NSGA-II+Repair", "baseline", nsga2_repair=True),
    Method("Control-GAOnly", "mechanism_control", variation_mode="ga"),
    Method("Control-DEOnly", "mechanism_control", variation_mode="de"),
    Method("Control-FixedWorstK", "mechanism_control", screen_dynamic=False),
)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False, dir=path.parent) as handle:
        handle.write(text)
        temp = Path(handle.name)
    temp.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False, dir=path.parent) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        temp = Path(handle.name)
    temp.replace(path)


def read_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _parse_float(value: str | None, default: float = 0.0) -> float:
    try:
        if value in {"", "NULL", None}:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_semicolon(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", errors="ignore", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def snapshot_source(raw_dir: Path) -> None:
    """Freeze the exact 18-subnet input sufficient for candidate reconstruction."""
    config = read_config()
    target = PROJECT_ROOT / config["source_profile"]
    if target.exists():
        raise SystemExit(f"immutable source profile already exists: {target}")
    expected = config["raw_source"]["files"]
    for name, digest in expected.items():
        path = raw_dir / name
        if not path.is_file():
            raise SystemExit(f"raw source file missing: {path}")
        actual = sha256_path(path)
        if actual != digest:
            raise SystemExit(f"raw source hash mismatch for {name}: {actual}")

    empty = lambda: {
        "load_mw": 0.0,
        "qload_mvar": 0.0,
        "load_count": 0.0,
        "res_mw": 0.0,
        "line_length_km": 0.0,
        "line_count": 0.0,
        "loading_sum": 0.0,
    }
    by_subnet: dict[str, dict[str, float]] = {}
    for row in _read_semicolon(raw_dir / "Load.csv"):
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["load_mw"] += _parse_float(row.get("pLoad"))
        data["qload_mvar"] += _parse_float(row.get("qLoad"))
        data["load_count"] += 1
    for row in _read_semicolon(raw_dir / "RES.csv"):
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["res_mw"] += _parse_float(row.get("pRES"))
    for row in _read_semicolon(raw_dir / "Line.csv"):
        data = by_subnet.setdefault(row.get("subnet") or "unknown", empty())
        data["line_length_km"] += _parse_float(row.get("length"))
        data["line_count"] += 1
        data["loading_sum"] += _parse_float(row.get("loadingMax"), 100.0)
    ranked = sorted(
        ((subnet, data) for subnet, data in by_subnet.items() if data["load_mw"] > 0 and data["line_count"] > 0),
        key=lambda item: item[1]["load_mw"] + 0.2 * item[1]["line_length_km"],
        reverse=True,
    )[:18]
    rows: list[dict[str, Any]] = []
    for subnet, data in ranked:
        rows.append(
            {
                "subnet": subnet,
                "load_mw": format(data["load_mw"], ".17g"),
                "qload_mvar": format(data["qload_mvar"], ".17g"),
                "load_count": str(int(data["load_count"])),
                "res_mw": format(data["res_mw"], ".17g"),
                "line_length_km": format(data["line_length_km"], ".17g"),
                "line_count": str(int(data["line_count"])),
                "avg_loading_max": format(data["loading_sum"] / max(1.0, data["line_count"]), ".17g"),
            }
        )
    if len(rows) != 18:
        raise SystemExit(f"expected 18 ranked subnets, found {len(rows)}")
    expected_names = {
        "EHV1", "HV1", "HV2", "LV3.101", "LV3.102", "LV3.103", "LV3.104", "LV3.105",
        "LV3.106", "LV3.107", "LV3.201", "LV3.202", "LV3.203", "LV3.204", "LV3.205",
        "LV3.206", "LV3.207", "LV3.208",
    }
    if {row["subnet"] for row in rows} != expected_names:
        raise SystemExit("ranked subnet identity differs from the archived source profile")
    write_csv(target, rows)
    print(f"snapshotted {len(rows)} subnets to {target.relative_to(PROJECT_ROOT)}")


def load_stats(path: Path) -> list[SubnetStats]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    stats = [
        SubnetStats(
            subnet=row["subnet"],
            load_mw=float(row["load_mw"]),
            qload_mvar=float(row["qload_mvar"]),
            load_count=int(row["load_count"]),
            res_mw=float(row["res_mw"]),
            line_length_km=float(row["line_length_km"]),
            line_count=int(row["line_count"]),
            avg_loading_max=float(row["avg_loading_max"]),
        )
        for row in rows
    ]
    if len(stats) != 18:
        raise ValueError(f"source profile must contain 18 subnets, found {len(stats)}")
    return stats


def build_candidates(stats: list[SubnetStats]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for item in stats:
        stress = item.load_mw / max(0.2, item.line_length_km)
        der_gap = max(0.0, item.load_mw * 0.55 - item.res_mw)
        candidates.extend(
            [
                Candidate(
                    f"{item.subnet}::reinforcement", item.subnet, "reinforcement",
                    60 + 4.5 * item.line_length_km + 7 * item.load_mw,
                    0.012 * item.line_length_km + 0.020 * stress,
                    0.020 + 0.006 * stress, 0.06 * der_gap,
                    0.018 * item.line_count, 0.016 * item.line_count, 0.20,
                ),
                Candidate(
                    f"{item.subnet}::storage", item.subnet, "storage",
                    50 + 16 * math.sqrt(item.load_mw + 1),
                    0.025 * math.sqrt(item.load_mw + 1),
                    0.018 * math.sqrt(stress + 1), 0.12 * der_gap + 0.08 * item.load_mw,
                    0.055 * math.sqrt(item.load_count + 1),
                    0.070 * math.sqrt(item.load_count + 1), 0.80,
                ),
                Candidate(
                    f"{item.subnet}::der", item.subnet, "der",
                    45 + 10 * math.sqrt(item.load_mw + 1),
                    0.018 * math.sqrt(item.load_mw + 1), 0.012,
                    0.18 * der_gap + 0.10 * item.load_mw,
                    0.020 * math.sqrt(item.load_count + 1),
                    0.028 * math.sqrt(item.load_count + 1), 1.00,
                ),
                Candidate(
                    f"{item.subnet}::automation", item.subnet, "automation",
                    38 + 1.8 * item.line_count, 0.006 * item.line_count,
                    0.010 * math.sqrt(stress + 1), 0.025 * der_gap,
                    0.085 * math.sqrt(item.line_count + 1),
                    0.115 * math.sqrt(item.line_count + 1), 0.35,
                ),
            ]
        )
    if len(candidates) != 72:
        raise ValueError(f"expected 72 candidates, found {len(candidates)}")
    return candidates


class PlanningProblem:
    def __init__(self, candidates: list[Candidate], stats: list[SubnetStats], setting: Setting, scenarios: np.ndarray):
        self.candidates = candidates
        self.setting = setting
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
        self.hosting_denom = total_load * 0.45
        self.budget = 920.0 * setting.budget_factor
        self._norm_bounds_cache: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    def components(self, X: np.ndarray, scenarios: np.ndarray | None = None) -> dict[str, np.ndarray]:
        X = np.atleast_2d(X).astype(float)
        S = self.scenarios if scenarios is None else scenarios
        loadf = S[:, 0][None, :]
        derf = S[:, 1][None, :]
        sev = S[:, 2][None, :]
        cost = (X @ self.cost)[:, None] * np.ones_like(loadf)
        loss = np.maximum(0.015, self.base_loss * loadf - (X @ self.loss_red)[:, None] / 120)
        voltage = np.maximum(0.005, self.base_voltage * loadf - (X @ self.volt_red)[:, None] / 10)
        hosting = np.minimum(1.0, (X @ self.hosting_gain)[:, None] / np.maximum(1.0, self.hosting_denom * derf))
        reliability = np.minimum(1.0, 0.35 + (X @ self.rel_gain)[:, None] / 28)
        survivability = np.minimum(
            1.0,
            0.42 * (1.0 - sev)
            + self.setting.survivability_action_scale * (X @ self.res_gain)[:, None] / 24,
        )
        count = np.maximum(1.0, X.sum(axis=1))[:, None]
        return {
            "cost": cost,
            "loss": loss,
            "voltage": voltage,
            "hosting": hosting,
            "reliability": reliability,
            "survivability": survivability,
            "der_readiness": np.minimum(1.0, (X @ self.der_support)[:, None] / (count * 0.62)),
        }

    def objectives(self, X: np.ndarray, scenarios: np.ndarray | None = None) -> np.ndarray:
        comp = self.components(X, scenarios)
        cols = [comp["cost"], comp["loss"], comp["voltage"], -comp["reliability"], -comp["survivability"]]
        return np.stack([col.mean(axis=1) for col in cols], axis=1)

    def violation(self, X: np.ndarray) -> np.ndarray:
        X = np.atleast_2d(X).astype(float)
        return np.maximum(0.0, (X @ self.cost - self.budget) / self.budget)


def make_scenarios(config: dict[str, Any], setting: Setting, evaluation: bool) -> np.ndarray:
    protocol = config["scenario_protocol"]
    rng = np.random.default_rng(protocol["evaluation_seed"] if evaluation else protocol["search_seed"])
    ranges = [protocol["load_range"], protocol["der_range_inactive_for_p4"], protocol["outage_range"]]
    return np.column_stack([rng.uniform(bounds[0], bounds[1], setting.scenario_count) for bounds in ranges])


def nondominated(F: np.ndarray) -> np.ndarray:
    mask = np.ones(F.shape[0], dtype=bool)
    for i in range(F.shape[0]):
        if not mask[i]:
            continue
        dominates = np.all(F <= F[i], axis=1) & np.any(F < F[i], axis=1)
        if np.any(dominates & mask):
            mask[i] = False
    return mask


def simple_nds(F: np.ndarray, violation: np.ndarray) -> list[np.ndarray]:
    n = F.shape[0]
    feasible = violation <= 1e-12
    dom = np.zeros((n, n), dtype=bool)
    for i in range(n):
        better_eq = np.all(F[i] <= F, axis=1)
        strictly = np.any(F[i] < F, axis=1)
        obj_dom = better_eq & strictly
        if feasible[i]:
            dom[i] = obj_dom & feasible
            dom[i] |= ~feasible
        else:
            dom[i] = (~feasible) & (violation[i] < violation)
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


def crowding_distance(F: np.ndarray) -> np.ndarray:
    n, d = F.shape
    dist = np.zeros(n)
    if n <= 2:
        return np.full(n, np.inf)
    for j in range(d):
        order = np.argsort(F[:, j])
        span = F[order[-1], j] - F[order[0], j]
        dist[order[0]] = dist[order[-1]] = np.inf
        if span > 0:
            dist[order[1:-1]] += (F[order[2:], j] - F[order[:-2], j]) / span
    return dist


def environmental_select(union: np.ndarray, F: np.ndarray, V: np.ndarray, pop_size: int, rng: np.random.Generator) -> np.ndarray:
    selected: list[int] = []
    for front in simple_nds(F, V):
        if len(selected) + len(front) <= pop_size:
            selected.extend(front.tolist())
        else:
            remaining = pop_size - len(selected)
            order = front[np.argsort(-crowding_distance(F[front]))]
            selected.extend(order[:remaining].tolist())
            break
    return union[np.asarray(selected, dtype=int)]


def normalization_bounds(problem: PlanningProblem, seed: int) -> tuple[np.ndarray, np.ndarray]:
    cache_key = str(seed)
    if cache_key in problem._norm_bounds_cache:
        return problem._norm_bounds_cache[cache_key]
    rng = np.random.default_rng(seed)
    samples = [np.zeros(problem.n)]
    for i in range(problem.n):
        row = np.zeros(problem.n)
        row[i] = 1.0
        samples.append(row)
    for _ in range(2048):
        density = rng.uniform(0.02, 0.30)
        proposed = (rng.random(problem.n) < density).astype(float)
        order = rng.permutation(problem.n)
        cost = 0.0
        selected = np.zeros(problem.n)
        for idx in order:
            if proposed[idx] and cost + problem.cost[idx] <= problem.budget:
                selected[idx] = 1.0
                cost += problem.cost[idx]
        samples.append(selected)
    F = problem.objectives(np.asarray(samples))
    lo, hi = F.min(axis=0), F.max(axis=0)
    span = np.maximum(hi - lo, 1e-9)
    bounds = (lo - 0.05 * span, hi + 0.05 * span)
    problem._norm_bounds_cache[cache_key] = bounds
    return bounds


def repair_to_budget(x: np.ndarray, problem: PlanningProblem) -> int:
    benefit = (
        problem.loss_red / 0.12 + problem.volt_red / 0.02 + problem.hosting_gain / 5
        + problem.rel_gain / 2 + problem.res_gain / 2
    )
    score = benefit / np.maximum(problem.cost, 1.0)
    drops = 0
    while x @ problem.cost > problem.budget and x.sum() > 0:
        selected = np.where(x > 0)[0]
        x[selected[np.argmin(score[selected])]] = 0
        drops += 1
    return drops


def scalar_score(problem: PlanningProblem, X: np.ndarray, lo: np.ndarray, hi: np.ndarray, scenarios: np.ndarray) -> np.ndarray:
    F = problem.objectives(X, scenarios)
    norm = (F - lo) / np.maximum(hi - lo, 1e-9)
    return norm.sum(axis=1) + 10.0 * problem.violation(X)


def run_shield(problem: PlanningProblem, method: Method, seed: int, protocol: dict[str, Any]) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = problem.n
    pop_size = int(protocol["population_size"])
    generations = int(protocol["generations"])
    pop = np.zeros((pop_size, n))
    for i in range(pop_size):
        density = rng.uniform(0.03, 0.18)
        pop[i] = (rng.random(n) < density).astype(float)
        repair_to_budget(pop[i], problem)
    search_scenarios = problem.scenarios
    active = search_scenarios
    lo, hi = normalization_bounds(problem, 20260713)
    for gen in range(1, generations + 1):
        screen_due = gen == 1 or (method.screen_dynamic and gen % int(protocol["screen_every"]) == 1)
        if screen_due:
            scores = np.array(
                [scalar_score(problem, pop, lo, hi, search_scenarios[s : s + 1]).mean() for s in range(len(search_scenarios))]
            )
            active = search_scenarios[np.argsort(-scores)[: problem.setting.screen_k]]
        idx_a = rng.integers(0, pop_size, pop_size)
        idx_b = rng.integers(0, pop_size, pop_size)
        mask = rng.random((pop_size, n)) < 0.5
        ga_children = np.where(mask, pop[idx_a], pop[idx_b])
        flip = rng.random((pop_size, n)) < 1.0 / n
        ga_children = np.abs(ga_children - flip.astype(float))
        de_idx = rng.integers(0, pop_size, (pop_size, 3))
        de_trial = np.clip(pop[de_idx[:, 0]] + 0.5 * (pop[de_idx[:, 1]] - pop[de_idx[:, 2]]), 0.0, 1.0)
        de_children = (rng.random((pop_size, n)) < np.where(de_trial > 0.5, 0.9, 0.08)).astype(float)
        if method.variation_mode == "ga":
            children = ga_children
        elif method.variation_mode == "de":
            children = de_children
        else:
            half = pop_size // 2
            children = np.vstack([ga_children[:half], de_children[half:]])
        for row in children:
            repair_to_budget(row, problem)
        union = np.vstack([pop, children])
        pop = environmental_select(union, problem.objectives(union, active), problem.violation(union), pop_size, rng)
    return pop


def _install_pymoo_scipy_compat() -> None:
    """Supply only scipy.spatial.distance.cdist for old pymoo duplicate checks."""
    scipy = types.ModuleType("scipy")
    spatial = types.ModuleType("scipy.spatial")
    distance = types.ModuleType("scipy.spatial.distance")

    def cdist(a: np.ndarray, b: np.ndarray, **_: Any) -> np.ndarray:
        a_float = np.asarray(a, dtype=float)
        b_float = np.asarray(b, dtype=float)
        return np.sqrt(((a_float[:, None, :] - b_float[None, :, :]) ** 2).sum(axis=2))

    distance.cdist = cdist  # type: ignore[attr-defined]
    spatial.distance = distance  # type: ignore[attr-defined]
    scipy.spatial = spatial  # type: ignore[attr-defined]
    sys.modules["scipy"] = scipy
    sys.modules["scipy.spatial"] = spatial
    sys.modules["scipy.spatial.distance"] = distance


def run_nsga2_repair(problem: PlanningProblem, seed: int, protocol: dict[str, Any]) -> np.ndarray:
    # pymoo 0.4.1 predates NumPy's removal of these scalar aliases.
    np.int = int  # type: ignore[attr-defined]
    np.float = float  # type: ignore[attr-defined]
    np.bool = bool  # type: ignore[attr-defined]
    np.object = object  # type: ignore[attr-defined]
    _install_pymoo_scipy_compat()
    from pymoo.algorithms.nsga2 import NSGA2
    from pymoo.configuration import Configuration
    from pymoo.model.problem import Problem
    from pymoo.model.sampling import Sampling
    from pymoo.operators.crossover.point_crossover import PointCrossover
    from pymoo.operators.mutation.bitflip_mutation import BinaryBitflipMutation
    from pymoo.optimize import minimize

    Configuration.show_compile_hint = False

    class LowDensitySampling(Sampling):
        def _do(self, pymoo_problem: Any, n_samples: int, **_: Any) -> np.ndarray:
            rng = np.random.default_rng(seed)
            density = rng.uniform(0.03, 0.18, size=(n_samples, 1))
            return rng.random((n_samples, pymoo_problem.n_var)) < density

    class Wrapped(Problem):
        def __init__(self) -> None:
            super().__init__(n_var=problem.n, n_obj=problem.n_obj, n_constr=1, xl=0, xu=1, type_var=np.bool)

        def _evaluate(self, X: np.ndarray, out: dict[str, np.ndarray], *args: Any, **kwargs: Any) -> None:
            Xf = X.astype(float)
            out["F"] = problem.objectives(Xf)
            out["G"] = problem.violation(Xf)[:, None]

    algorithm = NSGA2(
        pop_size=int(protocol["population_size"]),
        sampling=LowDensitySampling(),
        crossover=PointCrossover(2),
        mutation=BinaryBitflipMutation(),
    )
    result = minimize(Wrapped(), algorithm, ("n_gen", int(protocol["generations"])), seed=seed, verbose=False)
    X = np.atleast_2d(result.pop.get("X")).astype(float)
    for row in X:
        repair_to_budget(row, problem)
    return X


def feasible_front(problem: PlanningProblem, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X = np.atleast_2d(X)
    X = X[problem.violation(X) <= 1e-9]
    if not len(X):
        return np.empty((0, problem.n)), np.empty((0, problem.n_obj))
    X = np.unique(X, axis=0)
    F = problem.objectives(X)
    keep = nondominated(F)
    return X[keep], F[keep]


def exact_hv(normalized_front: np.ndarray, reference_value: float, clip: bool) -> float:
    np.float = float  # type: ignore[attr-defined]
    np.int = int  # type: ignore[attr-defined]
    from pymoo.vendor.hv import HyperVolume

    if not normalized_front.size:
        return 0.0
    points = np.clip(normalized_front, 0.0, 1.0) if clip else normalized_front.copy()
    ref = np.full(points.shape[1], reference_value)
    points = points[np.all(points <= ref, axis=1)]
    if not len(points):
        return 0.0
    points = points[nondominated(points)]
    return float(HyperVolume(ref).compute(points))


def bounds_hash(lo: np.ndarray, hi: np.ndarray) -> str:
    payload = "|".join(format(float(value), ".17g") for value in np.concatenate([lo, hi]))
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def optimizer_seed(run_id: str, setting_id: str, method: str, seed_index: int) -> int:
    digest = hashlib.sha1(f"{run_id}|{setting_id}|{method}".encode("utf-8")).hexdigest()
    return 310000 + seed_index * 7919 + int(digest[:6], 16) % 4096


def mean_sd(values: Iterable[float]) -> tuple[float, float]:
    array = np.asarray(list(values), dtype=float)
    return float(array.mean()), float(array.std(ddof=1))


def bootstrap_gap(a: np.ndarray, b: np.ndarray, seed: int, n_boot: int = 5000) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    batch = 500
    draws: list[np.ndarray] = []
    for start in range(0, n_boot, batch):
        size = min(batch, n_boot - start)
        a_mean = a[rng.integers(0, len(a), (size, len(a)))].mean(axis=1)
        b_mean = b[rng.integers(0, len(b), (size, len(b)))].mean(axis=1)
        draws.append(a_mean - b_mean)
    values = np.concatenate(draws)
    return float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))


def aggregate_outputs(rows: list[dict[str, Any]], config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summary: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    metrics = ("hv_clipped_ref_1p1", "hv_unclipped_ref_1p1", "hv_clipped_ref_1p2")
    for setting in config["settings"]:
        setting_id = setting["setting_id"]
        setting_rows = [row for row in rows if row["setting_id"] == setting_id]
        for method in METHODS:
            group = [row for row in setting_rows if row["method"] == method.name]
            item: dict[str, Any] = {
                "run_id": config["run_id"],
                "setting_id": setting_id,
                "axis": setting["axis"],
                "method": method.name,
                "method_role": method.role,
                "n": len(group),
            }
            for metric in metrics:
                mean, sd = mean_sd(float(row[metric]) for row in group)
                item[f"mean_{metric}"] = f"{mean:.10f}"
                item[f"sd_{metric}"] = f"{sd:.10f}"
            item["runs_with_any_clipping"] = sum(int(row["clipped_point_count"]) > 0 for row in group)
            item["mean_clipped_component_count"] = f"{np.mean([int(row['clipped_component_count']) for row in group]):.6f}"
            item["mean_front_size"] = f"{np.mean([int(row['feasible_front_size']) for row in group]):.6f}"
            summary.append(item)

        proposed = [row for row in setting_rows if row["method"] == "SHIELD-MOEA"]
        for opponent in [method for method in METHODS if method.name != "SHIELD-MOEA"]:
            other = [row for row in setting_rows if row["method"] == opponent.name]
            item = {
                "run_id": config["run_id"],
                "setting_id": setting_id,
                "axis": setting["axis"],
                "comparison": f"SHIELD-MOEA minus {opponent.name}",
                "opponent_role": opponent.role,
                "n_per_method": len(proposed),
            }
            signs: list[int] = []
            for metric in metrics:
                a = np.array([float(row[metric]) for row in proposed])
                b = np.array([float(row[metric]) for row in other])
                gap = float(a.mean() - b.mean())
                seed_text = f"{config['run_id']}|{setting_id}|{opponent.name}|{metric}"
                boot_seed = int(hashlib.sha1(seed_text.encode("utf-8")).hexdigest()[:8], 16)
                low, high = bootstrap_gap(a, b, boot_seed)
                item[f"mean_gap_{metric}"] = f"{gap:.10f}"
                item[f"relative_gap_pct_{metric}"] = f"{100.0 * gap / max(abs(float(b.mean())), 1e-12):.6f}"
                item[f"bootstrap95_low_{metric}"] = f"{low:.10f}"
                item[f"bootstrap95_high_{metric}"] = f"{high:.10f}"
                signs.append(int(np.sign(gap)))
            item["gap_direction_consistent_across_hv_definitions"] = str(len(set(signs)) == 1)
            gaps.append(item)
    return summary, gaps


def render_analysis(rows: list[dict[str, Any]], summary: list[dict[str, Any]], gaps: list[dict[str, Any]], config: dict[str, Any]) -> str:
    primary = "hv_clipped_ref_1p1"
    lines = [
        "# P4 Boundary Experiment Analysis",
        "",
        f"Run: `{config['run_id']}`. This is a predeclared exploratory boundary study and does not replace the main archive.",
        "",
        "## Hypervolume Audit",
        "",
    ]
    clipped_runs = sum(int(row["clipped_point_count"]) > 0 for row in rows)
    clipped_components = sum(int(row["clipped_component_count"]) for row in rows)
    lines.append(
        f"All settings use one bounds vector computed before method execution from the declared reference-plan sample. "
        f"Across {len(rows)} run fronts, {clipped_runs} required clipping ({clipped_components} objective components)."
    )
    lines.extend(
        [
            "The primary score clips affine values to [0,1] at reference point 1.1. The same raw fronts were also scored without clipping and with the predeclared alternative reference point 1.2.",
            "",
            "## SHIELD minus NSGA-II+Repair",
            "",
            "| Setting | Primary mean gap | Relative gap | 95% bootstrap interval | Gap sign stable across clipping/reference audits? |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for gap in [item for item in gaps if item["opponent_role"] == "baseline"]:
        lines.append(
            f"| {gap['setting_id']} | {float(gap[f'mean_gap_{primary}']):.5f} | "
            f"{float(gap[f'relative_gap_pct_{primary}']):.2f}% | "
            f"[{float(gap[f'bootstrap95_low_{primary}']):.5f}, {float(gap[f'bootstrap95_high_{primary}']):.5f}] | "
            f"{gap['gap_direction_consistent_across_hv_definitions']} |"
        )
    lines.extend(
        [
            "",
            "## Mechanism Gaps",
            "",
            "Positive values favor the full hybrid/dynamic SHIELD configuration. Intervals are pointwise and multiplicity-unadjusted; overlap with zero is not an equivalence result.",
            "",
            "| Setting | Opponent | Primary mean gap | 95% bootstrap interval |",
            "|---|---|---:|---:|",
        ]
    )
    for gap in [item for item in gaps if item["opponent_role"] == "mechanism_control"]:
        opponent = gap["comparison"].replace("SHIELD-MOEA minus ", "")
        lines.append(
            f"| {gap['setting_id']} | {opponent} | {float(gap[f'mean_gap_{primary}']):.5f} | "
            f"[{float(gap[f'bootstrap95_low_{primary}']):.5f}, {float(gap[f'bootstrap95_high_{primary}']):.5f}] |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "Budget factor, scenario count, and the action-gain coefficient in the survivability equation are varied one at a time. The DER-output multiplier remains inactive. Scenario-count settings scale K at one quarter of the search draw and change both the search and disjoint evaluation sample sizes. The resilience coefficient changes the proxy formulation and its method-independent bounds, but not the fixed repair heuristic. These are proxy-benchmark reruns, not AC, deployment, tail-bound, or monetary-calibration evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def run_experiment() -> None:
    outputs = [RUNS_PATH, ANALYSIS_PATH, SUMMARY_PATH, GAPS_PATH, BOUNDS_PATH, MANIFEST_PATH]
    existing = [path for path in outputs if path.exists()]
    if existing:
        raise SystemExit("immutable run output already exists: " + ", ".join(str(path) for path in existing))
    config = read_config()
    source_profile = PROJECT_ROOT / config["source_profile"]
    if not source_profile.is_file():
        raise SystemExit(f"source profile missing; run snapshot first: {source_profile}")
    stats = load_stats(source_profile)
    candidates = build_candidates(stats)
    protocol = config["optimizer_protocol"]
    bounds_seed = int(config["hypervolume_protocol"]["bounds_seed"])
    rows: list[dict[str, Any]] = []
    bounds_rows: list[dict[str, Any]] = []
    for declared in config["settings"]:
        setting = Setting(**{key: declared[key] for key in Setting.__dataclass_fields__})
        search_problem = PlanningProblem(candidates, stats, setting, make_scenarios(config, setting, evaluation=False))
        eval_problem = PlanningProblem(candidates, stats, setting, make_scenarios(config, setting, evaluation=True))
        lo, hi = normalization_bounds(eval_problem, bounds_seed)
        bound_digest = bounds_hash(lo, hi)
        bound_row: dict[str, Any] = {
            "run_id": config["run_id"],
            "setting_id": setting.setting_id,
            "axis": setting.axis,
            "reference_plan_count": 1 + eval_problem.n + 2048,
            "bounds_sha256": bound_digest,
        }
        for j in range(eval_problem.n_obj):
            bound_row[f"lo_{j + 1}"] = format(float(lo[j]), ".17g")
            bound_row[f"hi_{j + 1}"] = format(float(hi[j]), ".17g")
        bounds_rows.append(bound_row)
        for method in METHODS:
            for seed_index in range(int(protocol["seeds_per_method_setting"])):
                seed = optimizer_seed(config["run_id"], setting.setting_id, method.name, seed_index)
                start = time.perf_counter()
                if method.nsga2_repair:
                    X = run_nsga2_repair(search_problem, seed, protocol)
                else:
                    X = run_shield(search_problem, method, seed, protocol)
                front_X, front_F = feasible_front(eval_problem, X)
                normalized = (front_F - lo) / np.maximum(hi - lo, 1e-9)
                low_count = int((normalized < 0.0).sum())
                high_count = int((normalized > 1.0).sum())
                point_count = int(np.any((normalized < 0.0) | (normalized > 1.0), axis=1).sum()) if len(normalized) else 0
                rows.append(
                    {
                        "run_id": config["run_id"],
                        "setting_id": setting.setting_id,
                        "axis": setting.axis,
                        "budget_factor": setting.budget_factor,
                        "scenario_count": setting.scenario_count,
                        "screen_k": setting.screen_k,
                        "survivability_action_scale": setting.survivability_action_scale,
                        "method": method.name,
                        "method_role": method.role,
                        "seed_index": seed_index,
                        "optimizer_seed": seed,
                        "bounds_sha256": bound_digest,
                        "feasible_front_size": len(front_X),
                        "clipped_low_component_count": low_count,
                        "clipped_high_component_count": high_count,
                        "clipped_component_count": low_count + high_count,
                        "clipped_point_count": point_count,
                        "hv_clipped_ref_1p1": f"{exact_hv(normalized, 1.1, clip=True):.10f}",
                        "hv_unclipped_ref_1p1": f"{exact_hv(normalized, 1.1, clip=False):.10f}",
                        "hv_clipped_ref_1p2": f"{exact_hv(normalized, 1.2, clip=True):.10f}",
                        "runtime_s": f"{time.perf_counter() - start:.6f}",
                        "run_status": "complete",
                    }
                )
            print(f"{setting.setting_id}: {method.name} complete", flush=True)

    summary, gaps = aggregate_outputs(rows, config)
    analysis = render_analysis(rows, summary, gaps, config)
    write_csv(RUNS_PATH, rows)
    write_csv(SUMMARY_PATH, summary)
    write_csv(GAPS_PATH, gaps)
    write_csv(BOUNDS_PATH, bounds_rows)
    _atomic_text(ANALYSIS_PATH, analysis)

    import pymoo

    assets = [CONFIG_PATH, Path(__file__).resolve(), source_profile, RUNS_PATH, SUMMARY_PATH, GAPS_PATH, BOUNDS_PATH, ANALYSIS_PATH]
    manifest = {
        "run_id": config["run_id"],
        "stage": config["stage"],
        "completed_date": "2026-08-13",
        "immutable_policy": "The runner refuses to overwrite any run output or this manifest.",
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pymoo": pymoo.__version__,
            "scipy_used": False,
            "pymoo_compatibility": "NumPy Euclidean cdist shim used only for pymoo 0.4.1 duplicate elimination; no statistical SciPy routine used.",
        },
        "counts": {
            "settings": len(config["settings"]),
            "methods": len(METHODS),
            "seeds_per_method_setting": int(protocol["seeds_per_method_setting"]),
            "run_rows": len(rows),
        },
        "assets": {str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"): sha256_path(path) for path in assets},
    }
    _atomic_text(MANIFEST_PATH, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"wrote immutable manifest {MANIFEST_PATH.relative_to(PROJECT_ROOT)}")


def verify() -> None:
    if not MANIFEST_PATH.is_file():
        raise SystemExit(f"manifest missing: {MANIFEST_PATH}")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []
    for relative, expected in manifest["assets"].items():
        path = PROJECT_ROOT / relative
        if not path.is_file():
            failures.append(f"missing {relative}")
        elif sha256_path(path) != expected:
            failures.append(f"hash mismatch {relative}")
    if failures:
        raise SystemExit("manifest verification failed: " + "; ".join(failures))
    with RUNS_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected_rows = int(manifest["counts"]["settings"]) * int(manifest["counts"]["methods"]) * int(manifest["counts"]["seeds_per_method_setting"])
    if len(rows) != expected_rows or any(row["run_status"] != "complete" for row in rows):
        raise SystemExit(f"run completeness failed: {len(rows)} rows, expected {expected_rows}")
    for setting in {row["setting_id"] for row in rows}:
        digests = {row["bounds_sha256"] for row in rows if row["setting_id"] == setting}
        if len(digests) != 1:
            raise SystemExit(f"method-dependent bounds detected for {setting}")
    print(f"verified {len(rows)} complete rows and method-independent bounds in {len(manifest['assets'])} hashed assets")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    snapshot = sub.add_parser("snapshot", help="freeze the minimal SimBench subnet profile")
    snapshot.add_argument("--raw-dir", required=True, type=Path)
    sub.add_parser("run", help="execute the predeclared immutable boundary matrix")
    sub.add_parser("verify", help="verify hashes, row completeness, and bound sharing")
    args = parser.parse_args(argv)
    if args.command == "snapshot":
        snapshot_source(args.raw_dir)
    elif args.command == "run":
        run_experiment()
    else:
        verify()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
