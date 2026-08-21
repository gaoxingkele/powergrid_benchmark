"""Independent mechanical verifier for the completed dev-only calibration."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def rows(name: str) -> list[dict]:
    return [json.loads(line) for line in (ARTIFACTS / name).read_text(encoding="utf-8").splitlines() if line.strip()]


def verify() -> dict:
    manifest = json.loads((ARTIFACTS / "RUN_MANIFEST.json").read_text(encoding="utf-8"))
    state = json.loads((ARTIFACTS / "RUN_STATE.json").read_text(encoding="utf-8"))
    decision = json.loads((ARTIFACTS / "CALIBRATION_DECISION.json").read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    checks["complete"] = state["status"] == "COMPLETE"
    checks["dev_only_flags"] = (
        state["development_only"] is True
        and state["test_input_accessed"] is False
        and state["formal_output_accessed"] is False
        and decision["test_input_accessed"] is False
        and decision["formal_output_accessed"] is False
    )
    checks["dev_hash"] = manifest["data_boundary"]["dev_sha256"] == (
        "27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79"
    )
    checks["output_hashes"] = all(
        digest(ARTIFACTS / name) == expected for name, expected in manifest["output_sha256"].items()
    )
    checks["code_hashes"] = all(
        digest(HERE / item["path"]) == item["sha256"] for item in manifest["code_snapshot"]
    )
    checks["package_relative_code_paths"] = all(
        not Path(item["path"]).is_absolute() for item in manifest["code_snapshot"]
    )
    test_source = (HERE / "test_dev_only_calibration.py").read_text(encoding="utf-8")
    checks["ten_tests_present"] = test_source.count("def test_") == 10
    summaries = rows("candidate_summary_ledger.jsonl")
    per_report = rows("per_report_ledger.jsonl")
    loo = rows("loo_fold_ledger.jsonl")
    gates = rows("path_gate_diagnostics.jsonl")
    checks["row_counts"] = len(summaries) == 147 and len(per_report) == 147 * 12 * 2 and len(loo) == 12 and len(gates) == 12 * 3
    checks["unique_candidate_ids"] = len({row["candidate_id"] for row in summaries}) == 147
    checks["report_cross_product"] = all(
        sum(row["candidate_id"] == candidate["candidate_id"] for row in per_report) == 24 for candidate in summaries
    )
    checks["k_cross_product"] = {row["k"] for row in per_report} == {5, 10}
    checks["weight_conservation"] = all(
        math.isclose(sum(candidate["weights"].values()), 1.0, abs_tol=1e-12) for candidate in summaries
    )
    checks["all_loo_winners_zero_cf"] = all(
        next(item for item in summaries if item["candidate_id"] == fold["winner_candidate_id"])["cf_weight"] == 0
        for fold in loo
    )
    checks["winner_frequency_reaggregates"] = decision["winner_frequency"] == {
        decision["robust_overall"]["candidate_id"]: 12
    }
    return {
        "verifier": "C2GES-posthoc-dev-CF-calibration-mechanical-audit-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "scope_note": "Mechanical integrity only; this audit does not turn post-unblinding development analysis into confirmatory evidence.",
    }


if __name__ == "__main__":
    result = verify()
    (HERE / "PACKAGE_MECHANICAL_AUDIT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
