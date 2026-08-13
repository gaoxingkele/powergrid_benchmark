"""Run the prespecified P5 matched-output and normalization sensitivity stage.

The script is deliberately stage-local.  It imports the shared candidate and
optimizer implementation but never writes to the shared P5/P6 evidence tree.
"""

from __future__ import annotations

import argparse
import atexit
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Iterable

import numpy as np


STAGE_ROOT = Path(__file__).resolve().parent
HARNESS_ROOT = Path(__file__).resolve().parents[4]
SHARED_SRC = HARNESS_ROOT / "src"


def _prepare_imports() -> str:
    """Use native SciPy when valid; otherwise activate the narrow local shim."""

    try:
        from scipy.spatial.distance import cdist as _cdist  # noqa: F401

        scipy_mode = "native"
    except Exception:  # the host has a mismatched SciPy extension ABI
        for name in list(sys.modules):
            if name == "scipy" or name.startswith("scipy."):
                del sys.modules[name]
        sys.path.insert(0, str(STAGE_ROOT / "runtime_compat"))
        scipy_mode = "p5_s3_distance_only_compat"
    sys.path.insert(0, str(SHARED_SRC))
    return scipy_mode


SCIPY_MODE = _prepare_imports()

from powergrid_benchmark import mintou_real_project_review as core  # noqa: E402


OBJECTIVES = ("cost", "negative_reliability", "negative_renewable", "risk", "negative_quality")


class HypervolumeClient:
    """Persistent pure-Python Fonseca indicator process.

    The optimizer runtime is free-threaded CPython, while the cached ``moocore``
    wheel is a GIL-build ABI3 artifact.  The helper uses the already installed
    pure-Python pymoo 0.4.1 vendor implementation; the optimizer itself remains
    pymoo 0.6.2.  The legacy reproduction table checks indicator equivalence at
    the archived eight-decimal precision.
    """

    def __init__(self) -> None:
        helper_python = os.environ.get("P5_HV_HELPER_PYTHON")
        if not helper_python:
            candidate = Path(sys.executable).with_name("python.exe")
            helper_python = str(candidate if candidate.exists() else Path(sys.executable))
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        self.process = subprocess.Popen(
            [helper_python, str(STAGE_ROOT / "hv_helper.py")],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            env=environment,
        )
        if self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("failed to open hypervolume-helper pipes")

    def compute(self, front: np.ndarray, reference: np.ndarray) -> float:
        if self.process.poll() is not None:
            stderr = self.process.stderr.read() if self.process.stderr is not None else ""
            raise RuntimeError(f"hypervolume helper stopped early: {stderr}")
        payload = json.dumps({"front": front.tolist(), "reference": reference.tolist()}, separators=(",", ":"))
        assert self.process.stdin is not None
        assert self.process.stdout is not None
        self.process.stdin.write(payload + "\n")
        self.process.stdin.flush()
        response = self.process.stdout.readline()
        if not response:
            stderr = self.process.stderr.read() if self.process.stderr is not None else ""
            raise RuntimeError(f"hypervolume helper returned no result: {stderr}")
        result = json.loads(response)
        if "error" in result:
            raise RuntimeError(f"hypervolume helper error: {result['error']}")
        return float(result["hypervolume"])

    def close(self) -> None:
        if self.process.poll() is None and self.process.stdin is not None:
            self.process.stdin.write(json.dumps({"command": "close"}) + "\n")
            self.process.stdin.flush()
            self.process.wait(timeout=10)


HV_CLIENT = HypervolumeClient()
atexit.register(HV_CLIENT.close)


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


def mean(values: Iterable[float]) -> float:
    array = np.asarray(list(values), dtype=float)
    return float(np.mean(array))


def sample_sd(values: Iterable[float]) -> float:
    array = np.asarray(list(values), dtype=float)
    return float(np.std(array, ddof=1)) if array.size > 1 else 0.0


def analytic_bounds(problem: core.PortfolioProblem) -> tuple[np.ndarray, np.ndarray]:
    """Definition-derived conservative bounds for every feasible P5 portfolio."""

    for name in ("cost", "reliability", "renewable", "risk", "quality"):
        values = np.asarray(getattr(problem, name), dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError(f"non-finite values in {name}")
    if np.any(problem.cost < 0) or np.any(problem.reliability < 0) or np.any(problem.renewable < 0):
        raise ValueError("analytic bounds require non-negative costs and additive benefits")
    lo = np.array(
        [
            0.0,
            -float(problem.reliability.sum()),
            -float(problem.renewable.sum()),
            min(float(problem.risk.min()), 1.0),
            -float(problem.quality.max()),
        ]
    )
    hi = np.array(
        [
            float(problem.budget),
            0.0,
            0.0,
            max(float(problem.risk.max()), 1.0),
            0.0,
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


def hv(front: np.ndarray, lo: np.ndarray, hi: np.ndarray, reference: float, clip: bool) -> float:
    if front.size == 0:
        return 0.0
    normalized = normalize(front, lo, hi)
    if clip:
        normalized = np.clip(normalized, 0.0, 1.0)
    ref = np.full(front.shape[1], reference, dtype=float)
    return HV_CLIENT.compute(normalized, ref)


def clipping_counts(
    front: np.ndarray, lo: np.ndarray, hi: np.ndarray, tolerance: float = 1e-12
) -> tuple[int, int, int]:
    if front.size == 0:
        return 0, 0, 0
    normalized = normalize(front, lo, hi)
    lower = normalized < -tolerance
    upper = normalized > 1.0 + tolerance
    any_point = np.any(lower | upper, axis=1)
    return int(lower.sum()), int(upper.sum()), int(any_point.sum())


def select_compromise(
    front_x: np.ndarray,
    front_f: np.ndarray,
    lo: np.ndarray,
    hi: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    if front_x.shape[0] == 0:
        raise ValueError("matched compromise rule requires a non-empty feasible front")
    normalized = normalize(front_f, lo, hi)
    if np.any(normalized < -1e-9) or np.any(normalized > 1.0 + 1e-9):
        raise ValueError("analytic bounds failed to contain a returned feasible front")
    max_score = normalized.max(axis=1)
    sum_score = normalized.sum(axis=1)
    best = min(range(front_x.shape[0]), key=lambda idx: (max_score[idx], sum_score[idx], idx))
    return front_x[best], front_f[best], float(max_score[best]), float(sum_score[best])


def selected_identity(problem: core.PortfolioProblem, x: np.ndarray) -> tuple[str, str]:
    identifiers = [candidate.cid for candidate, chosen in zip(problem.candidates, x) if chosen > 0.5]
    joined = ";".join(identifiers)
    digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return joined, digest


def main_seed(scenario: str, method: str, seed_index: int) -> int:
    digest = hashlib.sha1(f"p5|{scenario}|{method}".encode("utf-8")).hexdigest()
    return 100000 + seed_index * 7919 + int(digest[:6], 16) % 4096


def read_legacy_rows() -> list[dict[str, str]]:
    path = (
        HARNESS_ROOT
        / "papers"
        / "mintou"
        / "mintou_p5_trace_moea_feasibility_review"
        / "evidence"
        / "runs"
        / "real_project_review_results.csv"
    )
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def legacy_hv_index(rows: list[dict[str, str]]) -> dict[tuple[str, str, int], str]:
    return {
        (row["experiment_id"], row["method"], int(row["seed"])): row["hypervolume"]
        for row in rows
    }


def scheme_values(
    front: np.ndarray,
    empirical_lo: np.ndarray,
    empirical_hi: np.ndarray,
    expanded_lo: np.ndarray,
    expanded_hi: np.ndarray,
    analytic_lo: np.ndarray,
    analytic_hi: np.ndarray,
) -> dict[str, float]:
    return {
        "hv_reported_empirical_ref1p1_clipped": hv(front, empirical_lo, empirical_hi, 1.1, True),
        "hv_reported_empirical_ref1p1_unclipped": hv(front, empirical_lo, empirical_hi, 1.1, False),
        "hv_expanded_empirical_ref1p1_unclipped": hv(front, expanded_lo, expanded_hi, 1.1, False),
        "hv_analytic_ref1p1_unclipped": hv(front, analytic_lo, analytic_hi, 1.1, False),
        "hv_analytic_ref1p2_unclipped": hv(front, analytic_lo, analytic_hi, 1.2, False),
    }


def summarize_matched(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["scenario"], row["method"])].append(row)
    scenario_rows: list[dict[str, str]] = []
    for (scenario, method), values in sorted(groups.items()):
        scenario_rows.append(
            {
                "scenario": scenario,
                "method": method,
                "method_type": values[0]["method_type"],
                "unique_runs": str(len(values)),
                "mean_compromise_cost_index": fmt(mean(float(row["compromise_cost_index"]) for row in values)),
                "mean_compromise_reliability": fmt(mean(float(row["compromise_reliability"]) for row in values)),
                "mean_compromise_renewable": fmt(mean(float(row["compromise_renewable"]) for row in values)),
                "mean_compromise_risk": fmt(mean(float(row["compromise_risk"]) for row in values)),
                "mean_portfolio_size": fmt(mean(float(row["portfolio_size"]) for row in values)),
                "mean_full_front_hypervolume_context": fmt(
                    mean(float(row["full_front_hypervolume_context"]) for row in values)
                ),
            }
        )
    by_method: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in scenario_rows:
        by_method[row["method"]].append(row)
    overall: list[dict[str, str]] = []
    for method, values in sorted(by_method.items()):
        overall.append(
            {
                "method": method,
                "method_type": values[0]["method_type"],
                "scenarios": str(len(values)),
                "scenario_balanced_mean_compromise_cost_index": fmt(
                    mean(float(row["mean_compromise_cost_index"]) for row in values)
                ),
                "scenario_balanced_mean_compromise_reliability": fmt(
                    mean(float(row["mean_compromise_reliability"]) for row in values)
                ),
                "scenario_balanced_mean_compromise_renewable": fmt(
                    mean(float(row["mean_compromise_renewable"]) for row in values)
                ),
                "scenario_balanced_mean_compromise_risk": fmt(
                    mean(float(row["mean_compromise_risk"]) for row in values)
                ),
                "scenario_balanced_mean_portfolio_size": fmt(
                    mean(float(row["mean_portfolio_size"]) for row in values)
                ),
                "scenario_balanced_mean_full_front_hypervolume_context": fmt(
                    mean(float(row["mean_full_front_hypervolume_context"]) for row in values)
                ),
            }
        )
    overall.sort(key=lambda row: row["method"])
    return scenario_rows, overall


def summarize_normalization(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["scenario"], row["method"])].append(row)
    summary: list[dict[str, str]] = []
    clip_summary: list[dict[str, str]] = []
    hv_columns = [name for name in rows[0] if name.startswith("hv_")]
    for (scenario, method), values in sorted(groups.items()):
        row = {
            "scenario": scenario,
            "method": method,
            "method_type": values[0]["method_type"],
            "unique_runs": str(len(values)),
        }
        for column in hv_columns:
            row[f"mean_{column}"] = fmt(mean(float(value[column]) for value in values))
        row["mean_unclipped_minus_clipped_reported_hv"] = fmt(
            mean(
                float(value["hv_reported_empirical_ref1p1_unclipped"])
                - float(value["hv_reported_empirical_ref1p1_clipped"])
                for value in values
            )
        )
        summary.append(row)

        front_points = sum(int(value["front_points"]) for value in values)
        coordinates = front_points * len(OBJECTIVES)
        clip_row = {
            "scenario": scenario,
            "method": method,
            "method_type": values[0]["method_type"],
            "unique_runs": str(len(values)),
            "front_points": str(front_points),
        }
        for prefix in ("reported", "expanded", "analytic"):
            low = sum(int(value[f"{prefix}_below_zero_coordinates"]) for value in values)
            high = sum(int(value[f"{prefix}_above_one_coordinates"]) for value in values)
            points = sum(int(value[f"{prefix}_clipped_points"]) for value in values)
            clip_row[f"{prefix}_clipped_coordinates"] = str(low + high)
            clip_row[f"{prefix}_coordinate_clip_rate"] = fmt((low + high) / max(1, coordinates))
            clip_row[f"{prefix}_clipped_points"] = str(points)
            clip_row[f"{prefix}_point_clip_rate"] = fmt(points / max(1, front_points))
        clip_summary.append(clip_row)
    return summary, clip_summary


def matched_analysis(overall: list[dict[str, str]]) -> str:
    lines = [
        "## Material Passport",
        "",
        "- Origin Skill: experiment-agent",
        "- Origin Mode: run",
        "- Verification Status: UNVERIFIED",
        "- Version Label: p5_s3_matched_compromise_v1",
        "",
        "## Matched-compromise result",
        "",
        "This analysis consumes the compromise already selected in every preserved main-run row "
        "by the shared normalized-objective-sum rule. Deterministic rules contribute one unique "
        "output per scenario; their repeated provenance rows are not treated as independent runs.",
        "",
        "| Method | Type | Cost index | Reliability | Renewable | Risk | Size |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in overall:
        lines.append(
            f"| {row['method']} | {row['method_type']} | "
            f"{row['scenario_balanced_mean_compromise_cost_index']} | "
            f"{row['scenario_balanced_mean_compromise_reliability']} | "
            f"{row['scenario_balanced_mean_compromise_renewable']} | "
            f"{row['scenario_balanced_mean_compromise_risk']} | "
            f"{row['scenario_balanced_mean_portfolio_size']} |"
        )
    lines.extend(
        [
            "",
            "The objectives trade off, so this table does not declare a universal winner. Full-front "
            "hypervolume is retained in the CSV only as context and is not a matched-cardinality "
            "metric. A deterministic method's single output does not create a sampling distribution, "
            "and no p-value is computed against repeated stochastic runs.",
        ]
    )
    return "\n".join(lines)


def normalization_analysis(
    summary: list[dict[str, str]], clip_summary: list[dict[str, str]], legacy_matches: int, legacy_total: int
) -> str:
    total_points = sum(int(row["front_points"]) for row in clip_summary)
    total_reported_clipped = sum(int(row["reported_clipped_points"]) for row in clip_summary)
    total_expanded_clipped = sum(int(row["expanded_clipped_points"]) for row in clip_summary)
    total_analytic_clipped = sum(int(row["analytic_clipped_points"]) for row in clip_summary)
    mean_delta = mean(float(row["mean_unclipped_minus_clipped_reported_hv"]) for row in summary)
    return "\n".join(
        [
            "## Material Passport",
            "",
            "- Origin Skill: experiment-agent",
            "- Origin Mode: validate",
            "- Verification Status: ANALYZED",
            "- Version Label: p5_s3_normalization_v1",
            "",
            "## Hypervolume-bound and clipping result",
            "",
            f"Across {total_points} returned non-dominated points, the reported empirical bounds "
            f"place {total_reported_clipped} points outside at least one normalized [0,1] coordinate. "
            f"The 25%-expanded bounds leave {total_expanded_clipped}, and the conservative analytic "
            f"bounds leave {total_analytic_clipped}.",
            "",
            f"The mean method-scenario difference (unclipped minus clipped) under the reported "
            f"bounds is {mean_delta:.10f}. Hypervolume is also recomputed with analytic bounds at "
            "reference points 1.1 and 1.2; these are sensitivity readouts, not replacements selected "
            "because they improve a preferred method's ranking.",
            "",
            f"The rerun matched {legacy_matches}/{legacy_total} preserved primary hypervolume cells "
            "at the archived eight-decimal precision. Any non-match remains listed in "
            "`legacy_reproduction.csv`.",
        ]
    )


class SensitivityProblem(core.PortfolioProblem):
    """Stage-local formulation variants; shared P5/P6 source remains untouched."""

    def __init__(
        self,
        candidates: list[core.Candidate],
        budget: float,
        risk_aggregation: str,
        quality_compliance_share: float,
    ) -> None:
        super().__init__(candidates, "p5", budget)
        self.risk_aggregation = risk_aggregation
        self.quality_compliance_share = quality_compliance_share
        self.quality = (
            quality_compliance_share * self.compliance
            + (1.0 - quality_compliance_share) * self.evidence
        )

    def objectives(self, x: np.ndarray) -> np.ndarray:
        values = np.atleast_2d(x).astype(float)
        count = np.maximum(values.sum(axis=1), 1.0)
        empty = values.sum(axis=1) == 0
        cost = values @ self.cost
        reliability = values @ self.reliability
        renewable = values @ self.renewable
        if self.risk_aggregation == "mean":
            risk = (values @ self.risk) / count
        elif self.risk_aggregation == "max":
            selected_risk = np.where(values > 0.5, self.risk[None, :], -np.inf)
            risk = selected_risk.max(axis=1)
        else:
            raise ValueError(f"unsupported risk aggregation: {self.risk_aggregation}")
        risk[empty] = 1.0
        quality = (values @ self.quality) / count
        quality[empty] = 0.0
        return np.column_stack((cost, -reliability, -renewable, risk, -quality))


def profile_weights(profile: str) -> dict[str, float]:
    scenarios = {
        "balanced": "benchmark_portfolio_optimization",
        "reliability": "reliability_driven_review",
        "renewable": "renewable_accommodation_review",
        "traceability": "traceability_evaluation",
    }
    return core.experiment_weights(scenarios[profile], "p5")


def summarize_sensitivity(
    rows: list[dict[str, str]], config: dict
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["cell_id"], row["method"])].append(row)
    summary: list[dict[str, str]] = []
    for (cell_id, method), values in sorted(groups.items()):
        summary.append(
            {
                "cell_id": cell_id,
                "factor": values[0]["factor"],
                "method": method,
                "risk_aggregation": values[0]["risk_aggregation"],
                "quality_compliance_share": values[0]["quality_compliance_share"],
                "n_preferences": values[0]["n_preferences"],
                "preference_profile": values[0]["preference_profile"],
                "runs": str(len(values)),
                "mean_hv_analytic_ref1p2": fmt(mean(float(row["hv_analytic_ref1p2"]) for row in values)),
                "sd_hv_analytic_ref1p2": fmt(sample_sd(float(row["hv_analytic_ref1p2"]) for row in values)),
                "mean_matched_single_hv_analytic_ref1p2": fmt(
                    mean(float(row["matched_single_hv_analytic_ref1p2"]) for row in values)
                ),
                "mean_full_front_size": fmt(mean(float(row["full_front_size"]) for row in values)),
                "mean_trace_event_count": fmt(mean(float(row["trace_event_count"]) for row in values)),
            }
        )
    index = {(row["cell_id"], row["method"]): row for row in summary}
    baseline = index[("registered", "TRACE-MOEA")]
    baseline_hv = float(baseline["mean_hv_analytic_ref1p2"])
    baseline_single = float(baseline["mean_matched_single_hv_analytic_ref1p2"])
    raw_by_key = groups
    effects: list[dict[str, str]] = []
    for cell in config["sensitivity"]["cells"]:
        cell_id = cell["id"]
        trace = index[(cell_id, "TRACE-MOEA")]
        trace_hv = float(trace["mean_hv_analytic_ref1p2"])
        trace_single = float(trace["mean_matched_single_hv_analytic_ref1p2"])
        comparator_cell = cell_id if (cell_id, "NoPreferenceRanking-MOEA") in index else "registered"
        comparator = index[(comparator_cell, "NoPreferenceRanking-MOEA")]
        paired = [
            float(row["hv_analytic_ref1p2"])
            for row in raw_by_key[(cell_id, "TRACE-MOEA")]
        ]
        base_paired = [
            float(row["hv_analytic_ref1p2"])
            for row in raw_by_key[("registered", "TRACE-MOEA")]
        ]
        differences = np.asarray(paired) - np.asarray(base_paired)
        delta = trace_hv - baseline_hv
        effects.append(
            {
                "cell_id": cell_id,
                "factor": cell["factor"],
                "delta_mean_hv_vs_registered": fmt(delta),
                "percent_delta_mean_hv_vs_registered": fmt(100.0 * delta / max(abs(baseline_hv), 1e-12)),
                "delta_mean_matched_single_hv_vs_registered": fmt(trace_single - baseline_single),
                "positive_seed_fraction_vs_registered": fmt(float(np.mean(differences > 0))),
                "negative_seed_fraction_vs_registered": fmt(float(np.mean(differences < 0))),
                "no_preference_comparator_cell": comparator_cell,
                "trace_minus_no_preference_mean_hv": fmt(
                    trace_hv - float(comparator["mean_hv_analytic_ref1p2"])
                ),
            }
        )
    return summary, effects


def sensitivity_analysis(summary: list[dict[str, str]], effects: list[dict[str, str]]) -> str:
    baseline = next(row for row in summary if row["cell_id"] == "registered" and row["method"] == "TRACE-MOEA")
    lines = [
        "## Material Passport",
        "",
        "- Origin Skill: experiment-agent",
        "- Origin Mode: validate",
        "- Verification Status: ANALYZED",
        "- Version Label: p5_s3_formulation_preference_sensitivity_v1",
        "",
        "## Prespecified compact sensitivity result",
        "",
        f"The registered TRACE-MOEA cell has mean analytic-bound HV "
        f"{baseline['mean_hv_analytic_ref1p2']} at reference point 1.2. The scan changes one "
        "formulation or preference factor at a time; it is descriptive and emits no p-values.",
        "",
        "| Cell | Factor | Mean-HV change | Percent change | Positive-seed fraction | TRACE minus no-preference MOEA |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in effects:
        lines.append(
            f"| {row['cell_id']} | {row['factor']} | {row['delta_mean_hv_vs_registered']} | "
            f"{row['percent_delta_mean_hv_vs_registered']}% | "
            f"{row['positive_seed_fraction_vs_registered']} | "
            f"{row['trace_minus_no_preference_mean_hv']} |"
        )
    nonpositive = [row["cell_id"] for row in effects if float(row["delta_mean_hv_vs_registered"]) <= 0.0]
    near_null = [
        row["cell_id"]
        for row in effects
        if abs(float(row["percent_delta_mean_hv_vs_registered"])) <= 0.1
    ]
    lines.extend(
        [
            "",
            "Non-positive changes relative to the registered cell: "
            + (", ".join(nonpositive) if nonpositive else "none")
            + ".",
            "Near-null changes within 0.1% in absolute mean HV: "
            + (", ".join(near_null) if near_null else "none")
            + ".",
            "",
            "The scan does not isolate a causal component effect and does not alter the existing "
            "negative finding that adaptive preference elitism's direct contribution is unresolved.",
        ]
    )
    return "\n".join(lines)


def run_matched_and_normalization(config: dict, output_root: Path) -> None:
    candidates = core.build_candidates()
    if len(candidates) != 120:
        raise ValueError(f"expected the registered 120-candidate pool, found {len(candidates)}")
    methods = {spec.name: spec for spec in core.p5_methods()}
    preserved_rows = read_legacy_rows()
    legacy = legacy_hv_index(preserved_rows)
    matched_rows: list[dict[str, str]] = []
    matched_subset_rows: list[dict[str, str]] = []
    normalization_rows: list[dict[str, str]] = []
    bounds_rows: list[dict[str, str]] = []
    legacy_rows: list[dict[str, str]] = []

    matched_methods = set(config["stochastic_methods"] + config["deterministic_methods"])
    deterministic_methods = set(config["deterministic_methods"])
    for source in preserved_rows:
        method = source["method"]
        if source["experiment_id"] not in config["scenarios"] or method not in matched_methods:
            continue
        deterministic = method in deterministic_methods
        if deterministic and source["seed"] != "0":
            continue
        matched_rows.append(
            {
                "scenario": source["experiment_id"],
                "method": method,
                "method_type": "deterministic" if deterministic else "stochastic_moea",
                "seed_index": "unique" if deterministic else source["seed"],
                "matched_output_cardinality": "1",
                "compromise_rule": "shared_minimum_normalized_objective_sum",
                "compromise_cost_index": source["compromise_cost_index"],
                "compromise_reliability": source["compromise_reliability"],
                "compromise_renewable": source["compromise_renewable"],
                "compromise_risk": source["compromise_risk"],
                "portfolio_size": source["portfolio_size"],
                "full_front_hypervolume_context": source["hypervolume"],
                "full_front_size_context": source["feasible_front_size"],
                "source_status": source["source_status"],
            }
        )

    expected_matched = (
        len(config["scenarios"])
        * len(config["stochastic_methods"])
        * config["seeds_per_stochastic_cell"]
        + len(config["scenarios"]) * len(config["deterministic_methods"])
    )
    if len(matched_rows) != expected_matched:
        raise ValueError(f"expected {expected_matched} matched rows, found {len(matched_rows)}")

    selected_methods = config["normalization_rerun_methods"]

    for scenario in config["scenarios"]:
        pool = core.experiment_pool(scenario, candidates)
        problem = core.PortfolioProblem(pool, "p5", core.budget_for(scenario, "p5"))
        empirical_lo, empirical_hi = core.normalization_bounds(problem)
        expanded_lo, expanded_hi = expanded_bounds(empirical_lo, empirical_hi)
        analytic_lo, analytic_hi = analytic_bounds(problem)
        schemes = {
            "reported_empirical": (empirical_lo, empirical_hi),
            "expanded_empirical": (expanded_lo, expanded_hi),
            "analytic": (analytic_lo, analytic_hi),
        }
        for scheme, (lo, hi) in schemes.items():
            for objective, lower, upper in zip(OBJECTIVES, lo, hi):
                bounds_rows.append(
                    {
                        "scenario": scenario,
                        "candidate_count": str(problem.n),
                        "budget": fmt(problem.budget),
                        "scheme": scheme,
                        "objective": objective,
                        "lower_bound": fmt(lower),
                        "upper_bound": fmt(upper),
                    }
                )

        for method in selected_methods:
            spec = methods[method]
            deterministic = method in deterministic_methods
            seed_indices = [0] if deterministic else list(range(config["seeds_per_stochastic_cell"]))
            for seed_index in seed_indices:
                seed = 0 if deterministic else main_seed(scenario, method, seed_index)
                x, eval_problem, _moves, _events = core.run_method(spec, pool, "p5", scenario, seed)
                front_x, front_f = core.feasible_front(eval_problem, x)
                if [candidate.cid for candidate in eval_problem.candidates] != [candidate.cid for candidate in problem.candidates]:
                    raise ValueError(f"unexpected method-owned pool change for {method}")
                compromise_x, compromise_f, max_score, sum_score = select_compromise(
                    front_x, front_f, analytic_lo, analytic_hi
                )
                selected_ids, selected_hash = selected_identity(eval_problem, compromise_x)
                single_hv = hv(compromise_f[None, :], analytic_lo, analytic_hi, 1.2, False)
                matched_subset_rows.append(
                    {
                        "scenario": scenario,
                        "method": method,
                        "method_type": "deterministic" if deterministic else "shared_custom_moea",
                        "seed_index": "unique" if deterministic else str(seed_index),
                        "seed_value": "not_applicable" if deterministic else str(seed),
                        "full_front_size": str(front_f.shape[0]),
                        "matched_output_cardinality": "1",
                        "matched_single_hv_analytic_ref1p2": fmt(single_hv),
                        "compromise_max_score": fmt(max_score),
                        "compromise_sum_tiebreak": fmt(sum_score),
                        "objective_cost": fmt(compromise_f[0]),
                        "objective_negative_reliability": fmt(compromise_f[1]),
                        "objective_negative_renewable": fmt(compromise_f[2]),
                        "objective_risk": fmt(compromise_f[3]),
                        "objective_negative_quality": fmt(compromise_f[4]),
                        "portfolio_size": str(int(compromise_x.sum())),
                        "selected_candidate_ids": selected_ids,
                        "selected_set_sha256": selected_hash,
                    }
                )
                values = scheme_values(
                    front_f,
                    empirical_lo,
                    empirical_hi,
                    expanded_lo,
                    expanded_hi,
                    analytic_lo,
                    analytic_hi,
                )
                reported_low, reported_high, reported_points = clipping_counts(front_f, empirical_lo, empirical_hi)
                expanded_low, expanded_high, expanded_points = clipping_counts(front_f, expanded_lo, expanded_hi)
                analytic_low, analytic_high, analytic_points = clipping_counts(front_f, analytic_lo, analytic_hi)
                normalization_rows.append(
                    {
                        "scenario": scenario,
                        "method": method,
                        "method_type": "deterministic" if deterministic else "shared_custom_moea",
                        "seed_index": "unique" if deterministic else str(seed_index),
                        "front_points": str(front_f.shape[0]),
                        **{key: fmt(value) for key, value in values.items()},
                        "reported_below_zero_coordinates": str(reported_low),
                        "reported_above_one_coordinates": str(reported_high),
                        "reported_clipped_points": str(reported_points),
                        "expanded_below_zero_coordinates": str(expanded_low),
                        "expanded_above_one_coordinates": str(expanded_high),
                        "expanded_clipped_points": str(expanded_points),
                        "analytic_below_zero_coordinates": str(analytic_low),
                        "analytic_above_one_coordinates": str(analytic_high),
                        "analytic_clipped_points": str(analytic_points),
                    }
                )
                legacy_value = legacy[(scenario, method, seed_index)]
                rerun_value = f"{values['hv_reported_empirical_ref1p1_clipped']:.8f}"
                legacy_rows.append(
                    {
                        "scenario": scenario,
                        "method": method,
                        "seed_index": str(seed_index),
                        "legacy_hypervolume": legacy_value,
                        "rerun_hypervolume": rerun_value,
                        "exact_at_archived_precision": str(rerun_value == legacy_value),
                    }
                )
            print(f"[normalization] {scenario} | {method} | {len(seed_indices)} unique run(s)", flush=True)

    matched_summary, matched_overall = summarize_matched(matched_rows)
    normalization_summary, clip_summary = summarize_normalization(normalization_rows)
    legacy_matches = sum(row["exact_at_archived_precision"] == "True" for row in legacy_rows)

    matched_root = output_root / "matched_compromise"
    write_csv(matched_root / "matched_results.csv", matched_rows)
    write_csv(matched_root / "matched_summary_by_scenario.csv", matched_summary)
    write_csv(matched_root / "matched_overall_summary.csv", matched_overall)
    write_text(matched_root / "analysis.md", matched_analysis(matched_overall))

    normalization_root = output_root / "normalization"
    write_csv(normalization_root / "bounds.csv", bounds_rows)
    write_csv(normalization_root / "matched_subset_results.csv", matched_subset_rows)
    write_csv(normalization_root / "normalization_results.csv", normalization_rows)
    write_csv(normalization_root / "normalization_summary.csv", normalization_summary)
    write_csv(normalization_root / "clipping_summary.csv", clip_summary)
    write_csv(normalization_root / "legacy_reproduction.csv", legacy_rows)
    write_text(
        normalization_root / "analysis.md",
        normalization_analysis(normalization_summary, clip_summary, legacy_matches, len(legacy_rows)),
    )


def run_sensitivity(config: dict, output_root: Path) -> None:
    candidates = core.build_candidates()
    scenario = config["sensitivity"]["scenario"]
    budget = core.budget_for(scenario, "p5")
    trace_spec = next(spec for spec in core.p5_methods() if spec.name == "TRACE-MOEA")
    rows: list[dict[str, str]] = []
    cells = config["sensitivity"]["cells"]

    def execute(cell: dict, method: str) -> None:
        problem = SensitivityProblem(
            candidates,
            budget,
            cell["risk_aggregation"],
            float(cell["quality_compliance_share"]),
        )
        weights = profile_weights(cell["preference_profile"])
        empirical_lo, empirical_hi = core.normalization_bounds(problem)
        analytic_lo, analytic_hi = analytic_bounds(problem)
        for seed_index in range(config["sensitivity"]["seeds_per_cell"]):
            seed = 700000 + 7919 * seed_index
            if method == "TRACE-MOEA":
                engine = replace(trace_spec.engine or core.EngineConfig(), n_preferences=int(cell["n_preferences"]))
                result = core.run_custom_ea(problem, engine, seed, seed_weights=weights)
                x = result.population
                trace_count = len(result.trace_events)
            elif method == "NoPreferenceRanking-MOEA":
                control = core.EngineConfig(repair=True, coevolution=False, trace=False)
                result = core.run_custom_ea(problem, control, seed, seed_weights=weights)
                x = result.population
                trace_count = 0
            else:
                raise ValueError(method)
            front_x, front_f = core.feasible_front(problem, x)
            compromise_x, compromise_f, max_score, _sum_score = select_compromise(
                front_x, front_f, analytic_lo, analytic_hi
            )
            rows.append(
                {
                    "cell_id": cell["id"],
                    "factor": cell["factor"],
                    "method": method,
                    "risk_aggregation": cell["risk_aggregation"],
                    "quality_compliance_share": fmt(float(cell["quality_compliance_share"])),
                    "n_preferences": str(cell["n_preferences"]) if method == "TRACE-MOEA" else "not_applicable",
                    "preference_profile": cell["preference_profile"] if method == "TRACE-MOEA" else "not_applicable",
                    "seed_index": str(seed_index),
                    "seed_value": str(seed),
                    "hv_reported_empirical_ref1p1_clipped": fmt(
                        hv(front_f, empirical_lo, empirical_hi, 1.1, True)
                    ),
                    "hv_analytic_ref1p2": fmt(hv(front_f, analytic_lo, analytic_hi, 1.2, False)),
                    "matched_single_hv_analytic_ref1p2": fmt(
                        hv(compromise_f[None, :], analytic_lo, analytic_hi, 1.2, False)
                    ),
                    "compromise_max_score": fmt(max_score),
                    "full_front_size": str(front_f.shape[0]),
                    "portfolio_size": str(int(compromise_x.sum())),
                    "trace_event_count": str(trace_count),
                }
            )
        print(f"[sensitivity] {cell['id']} | {method} | 30 runs", flush=True)

    for cell in cells:
        execute(cell, "TRACE-MOEA")
    for cell in cells:
        if cell["factor"] in {"reference", "formulation"}:
            execute(cell, "NoPreferenceRanking-MOEA")

    summary, effects = summarize_sensitivity(rows, config)
    sensitivity_root = output_root / "sensitivity"
    write_csv(sensitivity_root / "sensitivity_results.csv", rows)
    write_csv(sensitivity_root / "sensitivity_summary.csv", summary)
    write_csv(sensitivity_root / "sensitivity_effects.csv", effects)
    write_text(sensitivity_root / "analysis.md", sensitivity_analysis(summary, effects))


def environment_record() -> dict[str, object]:
    return {
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "optimizer_runtime": "shared custom TRACE/NoPreferenceRanking engines; preserved pymoo 0.6.2 rows for other MOEAs",
        "hypervolume_engine": "pymoo 0.4.1 vendor Fonseca dimension sweep in isolated helper process",
        "scipy_mode": SCIPY_MODE,
        "shared_core": str(Path(core.__file__).resolve()),
        "shared_status": core.STATUS,
        "rts_source": str(core.RTS_SOURCE),
        "simbench_source": str(core.SIMBENCH_NET),
        "nerc_source": str(core.NERC_ROOT),
    }


def configure_data_sources(config: dict) -> None:
    """Bind the documented read-only public cache without editing shared code."""

    public_root = Path(config["input_data_root"])
    core.RTS_SOURCE = public_root / "production_cost" / "rts-gmlc" / "RTS_Data" / "SourceData"
    core.SIMBENCH_NET = (
        public_root
        / "grid_cases"
        / "simbench"
        / "simbench"
        / "networks"
        / "1-complete_data-mixed-all-0-sw"
    )
    core.NERC_ROOT = public_root / "reliability_reports" / "c2ges_nerc_reports"
    required = [core.RTS_SOURCE / "gen.csv", core.SIMBENCH_NET, core.NERC_ROOT]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("documented public-data cache inputs are missing: " + ", ".join(missing))


def execute(config_path: Path, output_root: Path) -> None:
    if output_root.exists():
        raise FileExistsError(f"output root already exists: {output_root}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config["status"] != "prespecified_before_execution":
        raise ValueError("configuration is not marked prespecified_before_execution")
    configure_data_sources(config)
    output_root.mkdir(parents=True)
    write_json(output_root / "config_snapshot.json", config)
    write_json(output_root / "environment.json", environment_record())
    run_matched_and_normalization(config, output_root)
    run_sensitivity(config, output_root)
    write_text(
        output_root / "EXECUTION.md",
        "\n".join(
            [
                "## Material Passport",
                "",
                "- Origin Skill: experiment-agent",
                "- Origin Mode: run",
                "- Verification Status: UNVERIFIED",
                "- Version Label: p5_s3_execution_v1",
                "",
                "## Experiment Result",
                "",
                "- ID: p5_s3_matched_sensitivity",
                "- Type: analysis",
                "- Status: completed",
                f"- Configuration: {config_path}",
                f"- Output root: {output_root}",
                "- Anomalies: "
                + (
                    "none; ABI-matched native SciPy was active."
                    if SCIPY_MODE == "native"
                    else "native SciPy was unavailable; the distance-only compatibility mode was active and statistical calls were disabled."
                ),
                "",
                "Public-record backtests were not rerun and retain their descriptive scope.",
            ]
        ),
    )
    print(f"[complete] {output_root}", flush=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=STAGE_ROOT / "config.json")
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    execute(args.config.resolve(), args.output_root.resolve())
