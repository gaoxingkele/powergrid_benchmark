#!/usr/bin/env python3
"""Independent, read-only release audit for the v3 offline study."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
RELEASE = HERE / "prospective_from_freeze_offline_study_v3"
OUTPUT = RELEASE / "INDEPENDENT_AUDIT_V3.json"
METHODS = [
    "fixed_order_equal_budget",
    "validation_rank_equal_budget_no_cf",
    "full_coordination_complete_metamorphic",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(f"audit output exists: {OUTPUT}")
    checks: dict[str, bool] = {}
    freeze = load_json(RELEASE / "freeze_manifest.json")
    freeze_hash = freeze.pop("freeze_content_sha256")
    checks["freeze_content_hash"] = canonical_hash(freeze) == freeze_hash
    freeze["freeze_content_sha256"] = freeze_hash
    checks["all_21_frozen_files_match"] = len(freeze["files"]) == 21 and all(
        (ROOT / item["path"]).stat().st_size == item["bytes"] and sha(ROOT / item["path"]) == item["sha256"]
        for item in freeze["files"].values()
    )
    checks["freeze_timestamp_content_bound"] = bool(datetime.fromisoformat(freeze["created_at_utc"]))
    checks["freeze_declares_before_selection"] = freeze["status"] == "FROZEN_BEFORE_V3_SELECTION_AND_GOLD_EVALUATION"
    checks["builder_and_all_tests_frozen"] = "witness_builder" in freeze["files"] and len([key for key in freeze["files"] if key.startswith("test:")]) == 4
    pretest = load_json(RELEASE / "prefreeze_test_result.json")
    checks["prefreeze_tests_passed"] = pretest["passed"] is True and pretest["returncode"] == 0

    witness = load_json(HERE / "metamorphic_witnesses_v3" / "WITNESS_MANIFEST.json")
    witness_hash = witness.pop("manifest_content_sha256")
    checks["witness_manifest_content_hash"] = canonical_hash(witness) == witness_hash == freeze["witness_manifest_content_sha256"]
    witness["manifest_content_sha256"] = witness_hash
    builder_path = ROOT / freeze["files"]["witness_builder"]["path"]
    checks["witness_builder_bound_twice"] = witness["builder"]["sha256"] == sha(builder_path) == freeze["files"]["witness_builder"]["sha256"]
    hashes = {witness["base"]["sha256"], *(row["sha256"] for row in witness["states"])}
    checks["four_distinct_database_hashes"] = len(hashes) == 4
    checks["witness_integrity_checks_ok"] = all(row["integrity_check"] == "ok" for row in witness["states"])

    canonical_files = ["selection_ledger_pre_gold.jsonl", "evaluation_ledger.jsonl", "sensitivity_evaluation.jsonl", "summary.json"]
    run_details: dict[str, Any] = {}
    for run_name in ["run_v3a", "run_v3b"]:
        run = RELEASE / run_name
        release_manifest = load_json(run / "run_release_manifest_v3.json")
        run_hash = release_manifest.pop("run_manifest_content_sha256")
        checks[f"{run_name}_manifest_content_hash"] = canonical_hash(release_manifest) == run_hash
        checks[f"{run_name}_after_freeze"] = datetime.fromisoformat(release_manifest["created_at_utc"]) >= datetime.fromisoformat(freeze["created_at_utc"])
        checks[f"{run_name}_freeze_binding"] = release_manifest["freeze_content_sha256"] == freeze_hash
        attempts = load_jsonl(run / "candidate_execution_attempts.jsonl")
        boards = load_jsonl(run / "blackboards_sealed_before_gold.jsonl")
        selections = load_jsonl(run / "selection_ledger_pre_gold.jsonl")
        evaluations = load_jsonl(run / "evaluation_ledger.jsonl")
        checks[f"{run_name}_topology"] = len(attempts) == 5760 and len(boards) == 180 and len(selections) == 540 and len(evaluations) == 540
        checks[f"{run_name}_all_boards_sealed"] = all(row["sealed"] for row in boards)
        checks[f"{run_name}_postseal_evaluation"] = all(row["gold_access_phase"] == "after_all_blackboards_sealed" for row in evaluations)
        validation_messages = [
            message["payload"]
            for board in boards
            for message in board["messages"]
            if message["kind"] == "decision:validation_rank_equal_budget_no_cf"
        ]
        checks[f"{run_name}_validation_empty_cf"] = len(validation_messages) == 180 and all(
            all(score["counterfactual_total"] == 0 and score["counterfactual_passes"] == 0 for score in decision["scores"])
            for decision in validation_messages
        )
        summary = load_json(run / "summary.json")
        recomputed = {}
        for method in METHODS:
            rows = [row for row in evaluations if row["method"] == method]
            recomputed[method] = {
                "correct": sum(row["correct"] for row in rows),
                "covered": sum(row["covered"] for row in rows),
                "invariant": sum(row["robust_invariance"] for row in rows),
            }
        checks[f"{run_name}_summary_recomputed"] = all(
            recomputed[method]["correct"] == summary["methods"][method]["correct"]
            and recomputed[method]["covered"] == summary["methods"][method]["covered"]
            and recomputed[method]["invariant"] == summary["methods"][method]["robust_invariance_selected"]
            for method in METHODS
        )
        selection_index = {(row["question_id"], row["method"]): row for row in selections}
        differences = [qid for qid in sorted({row["question_id"] for row in selections}) if selection_index[(qid, METHODS[1])]["selected_candidate_id"] != selection_index[(qid, METHODS[2])]["selected_candidate_id"]]
        checks[f"{run_name}_difference_is_narrow_projection_case"] = len(differences) == 1 and all(
            "*" in selection_index[(qid, METHODS[1])]["selected_sql"] and "*" not in selection_index[(qid, METHODS[2])]["selected_sql"]
            for qid in differences
        )
        run_details[run_name] = {"summary": recomputed, "selection_differences": differences, "retained_failures": sum(not row["executable"] for row in attempts)}

    comparison = load_json(RELEASE / "INDEPENDENT_REPRODUCTION_CHECK_V3.json")
    checks["dual_canonical_outputs_identical"] = comparison["all_canonical_outputs_identical"] and all(
        sha(RELEASE / "run_v3a" / name) == sha(RELEASE / "run_v3b" / name) for name in canonical_files
    )
    result = {
        "schema_version": "ma-sqlgrid-offline-release-v3-independent-audit-v1",
        "decision": "PASS" if all(checks.values()) else "FAIL",
        "freeze_content_sha256": freeze_hash,
        "passed": sum(checks.values()),
        "total": len(checks),
        "checks": checks,
        "run_details": run_details,
        "claim_boundary": "Shared precomputed evidence over a historical pool; the one-selection difference is a narrow M3 nullable-schema-extension projection-stability case, not a general multi-agent or counterfactual gain.",
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"decision": result["decision"], "passed": result["passed"], "total": result["total"]}, sort_keys=True))
    return 0 if result["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
