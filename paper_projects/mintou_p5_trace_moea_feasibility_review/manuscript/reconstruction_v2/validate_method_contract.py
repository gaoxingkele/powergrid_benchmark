"""Validate the P1 method/data/implementation contract without running experiments.

This is an executable consistency oracle for the retrospective contract.  It is
not the archived optimizer and produces no scientific result.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTRACT = ROOT / "method_implementation_contract.json"
PROJECT = ROOT.parents[1]
ARCHIVED_ANALYSIS_CONFIG = PROJECT / "experiments" / "p5_s3_matched_sensitivity" / "config.json"
ARCHIVED_ANALYSIS_CODE = PROJECT / "experiments" / "p5_s3_matched_sensitivity" / "run_experiments.py"


def first_argmin(values: list[float]) -> int:
    return min(range(len(values)), key=values.__getitem__)


def objective(row: dict[str, float]) -> tuple[float, float, float, float, float]:
    count = row["count"]
    risk = row["risk_sum"] / count if count else 1.0
    quality = row["quality_sum"] / count if count else 0.0
    return row["cost"], -row["reliability"], -row["renewable"], risk, -quality


def violation(cost: float, budget: float) -> float:
    return max(0.0, (cost - budget) / budget)


def normalize(value: float, lower: float, upper: float, *, clip: bool) -> float:
    result = (value - lower) / (upper - lower)
    return min(1.0, max(0.0, result)) if clip else result


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    analysis_config = json.loads(ARCHIVED_ANALYSIS_CONFIG.read_text(encoding="utf-8"))
    analysis_code = ARCHIVED_ANALYSIS_CODE.read_text(encoding="utf-8")
    assert len(contract["objectives"]) == 5
    assert [item["sense"] for item in contract["objectives"]] == ["min"] * 5
    assert contract["budget"]["unit"] == contract["objectives"][0]["unit"]
    assert contract["budget"]["violation_unit"] == "dimensionless"
    assert contract["preference"]["count"] * contract["environmental_selection"]["generations"] == 320
    assert contract["normalization"]["preference_selection"]["clipping"] is False
    assert contract["normalization"]["reported_evaluation"]["reference_point"] == [1.1] * 5
    assert contract["evaluation_accounting"]["n_eval_archived"] is False
    assert set(contract["validation_usability"]) == {"traceable_cost", "ac_or_opf", "external_public_records"}
    assert contract["validation_usability"]["traceable_cost"]["decision"] == "NO_GO"
    assert contract["validation_usability"]["ac_or_opf"]["decision"] == "NO_GO"
    assert contract["validation_usability"]["external_public_records"]["decision"] == "GO_DESCRIPTIVE_ONLY"
    assert analysis_config["analysis_unit"] == contract["evaluation_accounting"]["analysis_unit"]
    assert analysis_config["clipping_incidence_tolerance"] == 1e-12
    expected_objective_tuple = '("cost", "negative_reliability", "negative_renewable", "risk", "negative_quality")'
    assert expected_objective_tuple in analysis_code
    assert "np.clip(normalized, 0.0, 1.0)" in analysis_code

    empty = objective({"count": 0, "cost": 0, "reliability": 0, "renewable": 0, "risk_sum": 0, "quality_sum": 0})
    assert empty == (0, 0, 0, 1.0, 0.0)
    assert math.isclose(violation(1276, 1160), 0.1)
    assert normalize(12, 0, 10, clip=False) == 1.2
    assert normalize(12, 0, 10, clip=True) == 1.0
    assert first_argmin([2.0, 1.0, 1.0]) == 1  # first exact tie

    print("OK: P1 method/data/implementation contract is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
