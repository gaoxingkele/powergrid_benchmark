from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

import p4_boundary_experiments as boundary


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_profile_reconstructs_declared_problem() -> None:
    config = json.loads(boundary.CONFIG_PATH.read_text(encoding="utf-8"))
    stats = boundary.load_stats(ROOT / config["source_profile"])
    candidates = boundary.build_candidates(stats)
    assert len(stats) == 18
    assert len(candidates) == 72
    assert np.isclose(sum(item.load_mw for item in stats), 71348.898090)
    assert np.isclose(sum(item.res_mw for item in stats), 12234.935550)
    assert np.isclose(sum(item.line_length_km for item in stats), 34296.204782)


def test_der_draw_is_inactive_and_resilience_scale_is_load_bearing() -> None:
    config = json.loads(boundary.CONFIG_PATH.read_text(encoding="utf-8"))
    stats = boundary.load_stats(ROOT / config["source_profile"])
    candidates = boundary.build_candidates(stats)
    declared = config["settings"][0]
    reference = boundary.Setting(**{key: declared[key] for key in boundary.Setting.__dataclass_fields__})
    low = boundary.Setting("low", "test", 1.0, 16, 4, 0.75)
    scenarios = boundary.make_scenarios(config, reference, evaluation=True)
    changed_der = scenarios.copy()
    changed_der[:, 1] *= 3.0
    x = np.zeros(72)
    x[[1, 3, 5, 7]] = 1
    reference_problem = boundary.PlanningProblem(candidates, stats, reference, scenarios)
    low_problem = boundary.PlanningProblem(candidates, stats, low, scenarios)
    assert np.array_equal(reference_problem.objectives(x, scenarios), reference_problem.objectives(x, changed_der))
    ref_obj = reference_problem.objectives(x)[0]
    low_obj = low_problem.objectives(x)[0]
    assert np.array_equal(ref_obj[:4], low_obj[:4])
    assert ref_obj[4] != low_obj[4]


def test_hypervolume_helper_matches_known_two_dimensional_union() -> None:
    front = np.array([[0.2, 0.3], [0.4, 0.1]])
    assert np.isclose(boundary.exact_hv(front, 1.1, clip=False), 0.86)


def test_completed_run_has_one_bound_vector_per_setting() -> None:
    with boundary.RUNS_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1050
    assert all(row["run_status"] == "complete" for row in rows)
    for setting in {row["setting_id"] for row in rows}:
        assert len({row["bounds_sha256"] for row in rows if row["setting_id"] == setting}) == 1


def test_predeclared_comparator_directions_are_preserved_by_hv_audits() -> None:
    with boundary.GAPS_PATH.open(encoding="utf-8", newline="") as handle:
        gaps = list(csv.DictReader(handle))
    assert len(gaps) == 28
    assert all(row["gap_direction_consistent_across_hv_definitions"] == "True" for row in gaps)
    baseline = [row for row in gaps if row["opponent_role"] == "baseline"]
    assert len(baseline) == 7
    assert all(float(row["mean_gap_hv_clipped_ref_1p1"]) > 0 for row in baseline)
