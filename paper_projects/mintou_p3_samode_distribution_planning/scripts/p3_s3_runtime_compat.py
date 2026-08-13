"""Local compatibility layer for the isolated P3 validation rerun.

The archived planning source was written against pymoo 0.6.2.  The isolated
runner has a readable cached source distribution for that version, but its
system Python contains mutually incompatible GIL/free-threaded SciPy wheels.
This module supplies only the small, deterministic subset of SciPy/moocore
used by the configured P3 algorithms.  It does not change the shared planning
source or either paper's evidence tree.
"""

from __future__ import annotations

import math
import sys
import types
import ctypes
from contextlib import AbstractContextManager
from pathlib import Path

import numpy as np


_C_HV_FUNCTION = None


def configure_moocore_pyd(path: Path) -> None:
    """Use the vendored moocore ABI3 hypervolume kernel through ``ctypes``."""
    global _C_HV_FUNCTION
    library = ctypes.CDLL(str(path))
    function = library.fpli_hv
    function.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t,
        ctypes.c_uint8,
        ctypes.POINTER(ctypes.c_double),
    ]
    function.restype = ctypes.c_double
    # Keep the library alive through the function object's owning DLL handle.
    _C_HV_FUNCTION = function


def cdist(a: np.ndarray, b: np.ndarray, metric: str = "euclidean") -> np.ndarray:
    """NumPy implementation of the SciPy distance subset used by pymoo."""
    left = np.asarray(a, dtype=float)
    right = np.asarray(b, dtype=float)
    delta = left[:, None, :] - right[None, :, :]
    squared = np.sum(delta * delta, axis=2)
    if metric == "sqeuclidean":
        return squared
    if metric != "euclidean":
        raise ValueError(f"unsupported compatibility distance metric: {metric}")
    return np.sqrt(squared)


def pdist(a: np.ndarray, metric: str = "euclidean") -> np.ndarray:
    matrix = cdist(a, a, metric=metric)
    return matrix[np.triu_indices(matrix.shape[0], 1)]


def squareform(values: np.ndarray) -> np.ndarray:
    condensed = np.asarray(values, dtype=float)
    n = int((1 + math.sqrt(1 + 8 * len(condensed))) / 2)
    if n * (n - 1) // 2 != len(condensed):
        raise ValueError("invalid condensed distance vector")
    matrix = np.zeros((n, n), dtype=float)
    upper = np.triu_indices(n, 1)
    matrix[upper] = condensed
    matrix += matrix.T
    return matrix


def is_nondominated(front: np.ndarray, keep_weakly: bool = True) -> np.ndarray:
    """Return the weak non-dominance mask for minimization objectives."""
    values = np.asarray(front, dtype=float)
    if values.shape[0] == 0:
        return np.zeros(0, dtype=bool)
    dominates = np.all(values[:, None, :] <= values[None, :, :], axis=2)
    dominates &= np.any(values[:, None, :] < values[None, :, :], axis=2)
    mask = ~dominates.any(axis=0)
    if keep_weakly:
        return mask
    # moocore's non-weak mode keeps one representative of duplicate rows.
    result = mask.copy()
    seen: set[tuple[float, ...]] = set()
    for index in np.where(mask)[0]:
        key = tuple(values[index].tolist())
        if key in seen:
            result[index] = False
        else:
            seen.add(key)
    return result


def pareto_rank(front: np.ndarray) -> np.ndarray:
    """Straightforward Pareto ranks, matching the ordering contract needed by pymoo."""
    values = np.asarray(front, dtype=float)
    n = values.shape[0]
    if n == 0:
        return np.zeros(0, dtype=int)
    dominates = np.all(values[:, None, :] <= values[None, :, :], axis=2)
    dominates &= np.any(values[:, None, :] < values[None, :, :], axis=2)
    counts = dominates.sum(axis=0).astype(int)
    ranks = np.full(n, -1, dtype=int)
    rank = 0
    while np.any(ranks < 0):
        current = np.where((ranks < 0) & (counts == 0))[0]
        if current.size == 0:
            current = np.where(ranks < 0)[0]
        ranks[current] = rank
        for index in current:
            counts -= dominates[index].astype(int)
        rank += 1
    return ranks


def exact_hypervolume(front: np.ndarray, ref: np.ndarray) -> float:
    """Exact union-of-boxes hypervolume for small minimization fronts.

    The recursion slices on the first coordinate and is exact for the P3
    fronts (at most 40 returned points in five dimensions).  Points not
    strictly dominated by ``ref`` do not define a positive box and are
    excluded, matching the mathematical hypervolume definition.
    """
    values = np.asarray(front, dtype=float)
    reference = np.asarray(ref, dtype=float)
    if values.size == 0:
        return 0.0
    values = values[np.all(values < reference, axis=1)]
    if values.shape[0] == 0:
        return 0.0
    values = np.ascontiguousarray(
        np.unique(values[is_nondominated(values)], axis=0), dtype=np.float64
    )
    reference = np.ascontiguousarray(reference, dtype=np.float64)

    if _C_HV_FUNCTION is not None:
        result = _C_HV_FUNCTION(
            values.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            values.shape[0],
            values.shape[1],
            reference.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        )
        if result < 0:
            raise MemoryError("moocore hypervolume kernel reported an allocation failure")
        return float(result)

    def recurse(points: np.ndarray, point_ref: np.ndarray) -> float:
        if points.shape[0] == 0:
            return 0.0
        if points.shape[1] == 1:
            return max(0.0, float(point_ref[0] - points[:, 0].min()))
        coordinates = np.unique(points[:, 0])
        volume = 0.0
        for position, coordinate in enumerate(coordinates):
            next_coordinate = (
                coordinates[position + 1]
                if position + 1 < len(coordinates)
                else point_ref[0]
            )
            width = float(next_coordinate - coordinate)
            if width <= 0:
                continue
            active = points[points[:, 0] <= coordinate, 1:]
            volume += width * recurse(active, point_ref[1:])
        return volume

    return float(recurse(values, reference))


def igd(front: np.ndarray, ref: np.ndarray) -> float:
    values = np.asarray(front, dtype=float)
    reference = np.asarray(ref, dtype=float)
    if values.shape[0] == 0:
        return float("inf")
    return float(np.mean(np.min(cdist(reference, values), axis=1)))


def igd_plus(front: np.ndarray, ref: np.ndarray) -> float:
    """IGD+ from a common reference set to an approximation set."""
    values = np.asarray(front, dtype=float)
    reference = np.asarray(ref, dtype=float)
    if values.shape[0] == 0:
        return float("inf")
    delta = np.maximum(values[None, :, :] - reference[:, None, :], 0.0)
    distances = np.sqrt(np.sum(delta * delta, axis=2))
    return float(np.mean(np.min(distances, axis=1)))


def epsilon_additive(front: np.ndarray, ref: np.ndarray) -> float:
    values = np.asarray(front, dtype=float)
    reference = np.asarray(ref, dtype=float)
    if values.shape[0] == 0:
        return float("inf")
    pairwise = np.max(values[None, :, :] - reference[:, None, :], axis=2)
    return float(np.max(np.min(pairwise, axis=1)))


def epsilon_mult(front: np.ndarray, ref: np.ndarray) -> float:
    values = np.asarray(front, dtype=float)
    reference = np.asarray(ref, dtype=float)
    if np.any(values <= 0) or np.any(reference <= 0):
        return epsilon_additive(values, reference)
    pairwise = np.max(values[None, :, :] / reference[:, None, :], axis=2)
    return float(np.max(np.min(pairwise, axis=1)))


def hv_contributions(front: np.ndarray, ref: np.ndarray) -> np.ndarray:
    values = np.asarray(front, dtype=float)
    total = exact_hypervolume(values, ref)
    return np.array(
        [total - exact_hypervolume(np.delete(values, i, axis=0), ref) for i in range(len(values))],
        dtype=float,
    )


def _average_ranks(values: np.ndarray) -> tuple[np.ndarray, list[int]]:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    tie_sizes: list[int] = []
    start = 0
    while start < len(values):
        stop = start + 1
        while stop < len(values) and values[order[stop]] == values[order[start]]:
            stop += 1
        ranks[order[start:stop]] = 0.5 * (start + 1 + stop)
        tie_sizes.append(stop - start)
        start = stop
    return ranks, tie_sizes


def mannwhitneyu(x: np.ndarray, y: np.ndarray, alternative: str = "two-sided") -> tuple[float, float]:
    """Asymptotic Mann--Whitney U with tie and continuity correction.

    This matches SciPy's default large-sample branch for the 30-by-30 P3
    comparisons.  It is supplied for the new robustness tables; the archived
    p-values remain untouched.
    """
    left = np.asarray(x, dtype=float)
    right = np.asarray(y, dtype=float)
    combined = np.concatenate([left, right])
    ranks, tie_sizes = _average_ranks(combined)
    n1, n2 = len(left), len(right)
    u1 = float(ranks[:n1].sum() - n1 * (n1 + 1) / 2)
    mean = n1 * n2 / 2
    total = n1 + n2
    tie_term = sum(size**3 - size for size in tie_sizes)
    variance = n1 * n2 / 12 * (
        total + 1 - tie_term / max(total * (total - 1), 1)
    )
    if variance <= 0:
        return u1, 1.0
    if alternative == "two-sided":
        z = max(0.0, abs(u1 - mean) - 0.5) / math.sqrt(variance)
        p_value = math.erfc(z / math.sqrt(2.0))
    elif alternative == "greater":
        z = (u1 - mean - 0.5) / math.sqrt(variance)
        p_value = 0.5 * math.erfc(z / math.sqrt(2.0))
    elif alternative == "less":
        z = (mean - u1 - 0.5) / math.sqrt(variance)
        p_value = 0.5 * math.erfc(z / math.sqrt(2.0))
    else:
        raise ValueError(f"unsupported Mann--Whitney alternative: {alternative}")
    return u1, min(1.0, max(0.0, float(p_value)))


def _simple_nds(front: np.ndarray, violation: np.ndarray) -> list[np.ndarray]:
    """Constraint-domination sorting used verbatim by the planning engines."""
    values = np.asarray(front, dtype=float)
    violations = np.asarray(violation, dtype=float)
    n = values.shape[0]
    feasible = violations <= 1e-12
    objective_domination = np.all(values[:, None, :] <= values[None, :, :], axis=2)
    objective_domination &= np.any(values[:, None, :] < values[None, :, :], axis=2)
    feasible_pair = feasible[:, None] & feasible[None, :]
    feasible_over_infeasible = feasible[:, None] & ~feasible[None, :]
    infeasible_pair = ~feasible[:, None] & ~feasible[None, :]
    lower_violation = violations[:, None] < violations[None, :]
    dominates = (objective_domination & feasible_pair) | feasible_over_infeasible
    dominates |= infeasible_pair & lower_violation
    np.fill_diagonal(dominates, False)
    counts = dominates.sum(axis=0).astype(int)
    fronts: list[np.ndarray] = []
    assigned = np.zeros(n, dtype=bool)
    while not assigned.all():
        current = np.where((counts == 0) & ~assigned)[0]
        if current.size == 0:
            current = np.where(~assigned)[0]
        fronts.append(current)
        assigned[current] = True
        for index in current:
            counts -= dominates[index].astype(int)
    return fronts


def _crowding_distance(front: np.ndarray) -> np.ndarray:
    values = np.asarray(front, dtype=float)
    n, dimensions = values.shape
    distance_values = np.zeros(n)
    if n <= 2:
        return np.full(n, np.inf)
    for dimension in range(dimensions):
        order = np.argsort(values[:, dimension])
        span = values[order[-1], dimension] - values[order[0], dimension]
        distance_values[order[0]] = distance_values[order[-1]] = np.inf
        if span <= 0:
            continue
        distance_values[order[1:-1]] += (
            values[order[2:], dimension] - values[order[:-2], dimension]
        ) / span
    return distance_values


def _holm(pvalues: list[float]) -> list[float]:
    order = np.argsort(pvalues)
    adjusted = [0.0] * len(pvalues)
    running = 0.0
    for rank, index in enumerate(order):
        value = min(1.0, (len(pvalues) - rank) * pvalues[int(index)])
        running = max(running, value)
        adjusted[int(index)] = running
    return adjusted


class _SilentAliveBar(AbstractContextManager):
    def __enter__(self):
        return lambda *args, **kwargs: None

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return False


class _CompatKDTree:
    def __init__(self, data: np.ndarray):
        self.data = np.asarray(data, dtype=float)

    def query(self, points: np.ndarray, k: int = 1):
        distances = cdist(np.atleast_2d(points), self.data)
        order = np.argsort(distances, axis=1)[:, :k]
        selected = np.take_along_axis(distances, order, axis=1)
        if k == 1:
            return selected[:, 0], order[:, 0]
        return selected, order


def install_runtime_stubs() -> None:
    """Install deterministic compatibility modules before importing pymoo."""
    scipy = types.ModuleType("scipy")
    special = types.ModuleType("scipy.special")
    special.binom = lambda n, k: float(math.comb(int(n), int(k)))

    spatial = types.ModuleType("scipy.spatial")
    distance = types.ModuleType("scipy.spatial.distance")
    distance.cdist = cdist
    distance.pdist = pdist
    distance.squareform = squareform
    ckdtree = types.ModuleType("scipy.spatial.ckdtree")
    ckdtree.cKDTree = _CompatKDTree
    spatial.distance = distance
    spatial.cKDTree = _CompatKDTree

    stats = types.ModuleType("scipy.stats")
    stats.mannwhitneyu = mannwhitneyu

    scipy.special = special
    scipy.spatial = spatial
    scipy.stats = stats
    for name, module in (
        ("scipy", scipy),
        ("scipy.special", special),
        ("scipy.spatial", spatial),
        ("scipy.spatial.distance", distance),
        ("scipy.spatial.ckdtree", ckdtree),
        ("scipy.stats", stats),
    ):
        sys.modules[name] = module

    moocore = types.ModuleType("moocore")
    moocore.hypervolume = exact_hypervolume
    moocore.hv_approx = exact_hypervolume
    moocore.hv_contributions = hv_contributions
    moocore.igd = igd
    moocore.igd_plus = igd_plus
    moocore.epsilon_additive = epsilon_additive
    moocore.epsilon_mult = epsilon_mult
    moocore.pareto_rank = pareto_rank
    moocore.is_nondominated = is_nondominated
    sys.modules["moocore"] = moocore

    alive_progress = types.ModuleType("alive_progress")
    alive_progress.alive_bar = lambda *args, **kwargs: _SilentAliveBar()
    sys.modules["alive_progress"] = alive_progress

    planning_helpers = types.ModuleType("powergrid_benchmark.mintou_real_project_review")
    planning_helpers._simple_nds = _simple_nds
    planning_helpers._crowding_distance = _crowding_distance
    planning_helpers.nondominated = is_nondominated
    planning_helpers.holm_correction = lambda pvalues: _holm(pvalues)

    def planning_hypervolume(front, lower, upper):
        values = np.asarray(front, dtype=float)
        if values.size == 0:
            return 0.0
        normalized = (values - lower) / np.maximum(upper - lower, 1e-9)
        return exact_hypervolume(np.clip(normalized, 0.0, 1.0), np.full(values.shape[1], 1.1))

    planning_helpers.hypervolume = planning_hypervolume
    sys.modules["powergrid_benchmark.mintou_real_project_review"] = planning_helpers


def assert_self_tests() -> None:
    """Fail closed if the compatibility math violates simple exact cases."""
    two_dimensional = np.array([[0.2, 0.8], [0.8, 0.2]])
    observed = exact_hypervolume(two_dimensional, np.ones(2))
    if not math.isclose(observed, 0.28, rel_tol=0.0, abs_tol=1e-12):
        raise AssertionError(f"hypervolume self-test failed: {observed}")
    ranks = pareto_rank(np.array([[0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]))
    if not np.array_equal(ranks, np.array([0, 0, 1])):
        raise AssertionError(f"Pareto-rank self-test failed: {ranks.tolist()}")
    if not math.isclose(igd_plus(np.array([[0.5, 0.5]]), np.array([[0.4, 0.4]])), math.sqrt(0.02)):
        raise AssertionError("IGD+ self-test failed")


def verify_pymoo_source(source_root: Path) -> None:
    version_file = source_root / "pymoo" / "version.py"
    if not version_file.exists():
        raise FileNotFoundError(f"pymoo source tree missing version file: {version_file}")
    version_text = version_file.read_text(encoding="utf-8")
    if "0.6.2" not in version_text:
        raise RuntimeError("the validation rerun requires the archived pymoo 0.6.2 source")
