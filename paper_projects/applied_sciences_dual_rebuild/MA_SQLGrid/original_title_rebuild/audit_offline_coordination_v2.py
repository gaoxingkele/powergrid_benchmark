#!/usr/bin/env python3
"""Independent, read-only audit of the frozen offline-coordination v2 release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent / "prospective_from_freeze_offline_study_v2"
WITNESS = Path(__file__).resolve().parent / "metamorphic_witnesses_v2" / "WITNESS_MANIFEST.json"
METHODS = {
    "fixed_order_equal_budget": (80, 180, 0, 177),
    "validation_rank_equal_budget_no_cf": (100, 180, 0, 179),
    "full_coordination_complete_metamorphic": (101, 180, 0, 180),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    checks: dict[str, bool] = {}
    freeze = json.loads((BASE / "freeze_manifest.json").read_text(encoding="utf-8"))
    expected = freeze.pop("freeze_content_sha256")
    checks["freeze_content_hash"] = canonical(freeze) == expected == "31eea8af71ad24be31df91091724d58a160eb230636a093c78e8eabf53b732cb"
    checks["all_frozen_files_match"] = all(
        (ROOT / item["path"]).is_file()
        and (ROOT / item["path"]).stat().st_size == item["bytes"]
        and sha(ROOT / item["path"]) == item["sha256"]
        for item in freeze["files"].values()
    )
    checks["gold_not_a_frozen_opened_file"] = not any("questions_with_gold" in key or "gold" in key for key in freeze["files"])
    selection = rows(BASE / "selection_inputs.jsonl")
    checks["selection_view_180_question_only"] = len(selection) == 180 and all(set(row) == {"question_id", "question"} for row in selection)

    witness = json.loads(WITNESS.read_text(encoding="utf-8"))
    witness_hashes = [row["sha256"] for row in witness["states"]]
    checks["three_unique_witness_hashes"] = len(witness_hashes) == len(set(witness_hashes)) == 3
    checks["witnesses_distinct_from_t0"] = witness["base"]["sha256"] not in witness_hashes
    checks["witness_builder_query_blind"] = all(not value for value in witness["forbidden_inputs_accessed"].values())
    checks["witness_files_match"] = all(sha(WITNESS.parent / row["path"]) == row["sha256"] for row in witness["states"])

    run_details = {}
    for run_name in ("run_v2a", "run_v2b"):
        run = BASE / run_name
        boards = rows(run / "blackboards_sealed_before_gold.jsonl")
        selections = rows(run / "selection_ledger_pre_gold.jsonl")
        evaluations = rows(run / "evaluation_ledger.jsonl")
        attempts = rows(run / "candidate_execution_attempts.jsonl")
        summary = json.loads((run / "summary.json").read_text(encoding="utf-8"))
        checks[f"{run_name}_180_sealed_boards"] = len(boards) == 180 and all(row["sealed"] for row in boards)
        checks[f"{run_name}_equal_operation_attempts"] = len(attempts) == 5760
        checks[f"{run_name}_all_method_rows"] = len(selections) == len(evaluations) == 540 and {row["method"] for row in selections} == set(METHODS)
        checks[f"{run_name}_fixed_order_is_c000"] = all(row["selected_candidate_id"] == "C000" for row in selections if row["method"] == "fixed_order_equal_budget")
        validation_messages = [
            message for board in boards for message in board["messages"]
            if message["kind"] == "decision:validation_rank_equal_budget_no_cf"
        ]
        checks[f"{run_name}_validation_has_empty_cf_scores"] = len(validation_messages) == 180 and all(
            all(score["counterfactual_total"] == 0 for score in message["payload"]["scores"])
            for message in validation_messages
        )
        checks[f"{run_name}_summary_values"] = all(
            (summary["methods"][method]["correct"], summary["methods"][method]["covered"], summary["methods"][method]["abstained"], summary["methods"][method]["robust_invariance_selected"]) == expected_values
            for method, expected_values in METHODS.items()
        )
        run_details[run_name] = {
            "candidate_state_attempts": len(attempts),
            "failed_attempts": sum(not row["executable"] for row in attempts),
            "selection_sha256": sha(run / "selection_ledger_pre_gold.jsonl"),
            "evaluation_sha256": sha(run / "evaluation_ledger.jsonl"),
            "summary_sha256": sha(run / "summary.json"),
        }
    reproduction = json.loads((BASE / "INDEPENDENT_REPRODUCTION_CHECK_v2.json").read_text(encoding="utf-8"))
    checks["canonical_outputs_identical"] = reproduction["all_canonical_outputs_identical"]
    report = {
        "schema_version": "ma-sqlgrid-offline-v2-independent-audit-v1",
        "decision": "PASS" if all(checks.values()) else "FAIL",
        "freeze_content_sha256": expected,
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "run_details": run_details,
        "claim_boundary": "Supports only deterministic offline selection over a historical eight-slot pool. Schema grounding is trace-only; no five-role end-to-end or new-generation gain is estimated. The full-vs-validation increment is 1/180 and descriptive.",
    }
    output = BASE / "INDEPENDENT_AUDIT_v2.json"
    if output.exists():
        raise FileExistsError(f"audit output exists: {output}")
    output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"decision": report["decision"], "passed": report["passed"], "total": report["total"], "failed": [key for key, value in checks.items() if not value]}, sort_keys=True))
    return 0 if report["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
