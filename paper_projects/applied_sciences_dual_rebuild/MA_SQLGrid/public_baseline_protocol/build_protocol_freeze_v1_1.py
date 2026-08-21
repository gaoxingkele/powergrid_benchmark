"""Build the additive v1.1 freeze from immutable v1.0 assets."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_FREEZE = ROOT / "BASELINE_PROTOCOL_FREEZE.json"
OUT = ROOT / "BASELINE_PROTOCOL_FREEZE_v1_1.json"
HISTORICAL_BASE_FREEZE_SHA256 = "29c780c63a2dc2baae221cfce52252c716d8720dbeecdc2f7a2fdd5756b42af5"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def file_record(path: Path) -> dict:
    return {"path": str(path.resolve()), "bytes": path.stat().st_size, "sha256": sha(path)}


def main() -> None:
    base = json.loads(BASE_FREEZE.read_text(encoding="utf-8"))
    freeze = copy.deepcopy(base)
    freeze["schema_version"] = "ma-public-baseline-freeze-v1.1"
    freeze["protocol_id"] = "MA-PUBLIC-BIRD-MINIDEV-v1.1"
    freeze["base_protocol_id"] = base["protocol_id"]
    freeze["base_freeze_sha256"] = HISTORICAL_BASE_FREEZE_SHA256
    freeze["live_workspace_base_manifest"] = {
        "path": str(BASE_FREEZE.resolve()),
        "observed_sha256": sha(BASE_FREEZE),
        "is_protocol_dependency": False,
        "reason": "Concurrent shared-workspace regeneration after the historical v1.0 freeze; excluded from v1.1.",
    }
    freeze["date_local"] = "2026-08-07"
    freeze["status"] = "FROZEN_NOT_RUN"
    freeze["formal_model_execution_authorized"] = False
    freeze["formal_outputs"] = 0
    freeze["expected_future_generation_calls"] = 5000
    freeze["change_control"] = {
        "authorized_change": "Catch sqlite3.Warning alongside sqlite3.Error and route it through the existing frozen classifier.",
        "multi_statement_classification": "OTHER_EXECUTION_ERROR",
        "unchanged": [
            "dataset", "materialized_prompts", "call_order", "models", "methods",
            "token_limits", "decoding", "zero_retry", "official_ex", "statistics_plan",
        ],
        "change_control_document": file_record(ROOT / "PROTOCOL_V1_1_CHANGE_CONTROL.md"),
        "v1_0_code_snapshots": {
            "module": file_record(ROOT / "freeze_public_baseline_v1_0_snapshot.py"),
            "tests": file_record(ROOT / "test_public_baseline_freeze_v1_0_snapshot.py"),
        },
        "live_v1_0_workspace_files_are_dependencies": False,
    }
    freeze["prompt_materialization"]["inherited_from_protocol_id"] = base["protocol_id"]
    freeze["execution"]["required_formal_python"] = "3.10.11"
    freeze["execution"]["required_formal_sqlite"] = "3.40.1"
    freeze["execution"]["warning_policy_v1_1"] = "sqlite3.Warning -> existing classify_sqlite_error vocabulary"
    incident1 = ROOT.parent / "formal_bird_runs" / "MA_PUBLIC_BIRD_v1_qwen"
    incident2 = ROOT.parent / "formal_bird_runs" / "MA_PUBLIC_BIRD_v1_qwen_replacement1"
    freeze["excluded_incidents"] = {
        "attempt1_runtime_drift": {
            "calls": 341,
            "final_rows": 272,
            "call_ledger": file_record(incident1 / "call_ledger.jsonl"),
            "final_scores": file_record(incident1 / "final_scores.jsonl"),
            "eligible_for_scoring": False,
        },
        "replacement1_sqlite_warning": {
            "calls": 2135,
            "final_rows": 1707,
            "call_ledger": file_record(incident2 / "call_ledger.jsonl"),
            "final_scores": file_record(incident2 / "final_scores.jsonl"),
            "eligible_for_scoring": False,
        },
        "physical_calls_completed": 2476,
        "new_complete_calls_planned": 5000,
        "maximum_physical_calls_after_completion": 7476,
    }
    code_names = [
        "freeze_public_baseline_v1_0_snapshot.py",
        "freeze_public_baseline_v1_1.py",
        "test_public_baseline_freeze_v1_0_snapshot.py",
        "test_public_baseline_freeze_v1_1.py",
        "run_formal_public_baseline_v1_1.py",
        "audit_frozen_public_baseline_v1_1.py",
        "build_protocol_freeze_v1_1.py",
        "materialize_v1_0_code_snapshot.py",
    ]
    freeze["code"] = {name: file_record(ROOT / name) for name in code_names}
    freeze["documentation"] = {
        "change_control": file_record(ROOT / "PROTOCOL_V1_1_CHANGE_CONTROL.md"),
        "formal_runbook": file_record(ROOT / "FORMAL_RUNBOOK_v1_1.md"),
    }
    freeze["gates"]["v1_1_change_scope_only"] = True
    freeze["gates"]["v1_0_incidents_hash_bound_and_excluded"] = True
    freeze["gates"]["formal_runtime_python31011_sqlite3401"] = True
    freeze["gates"]["historical_v1_0_code_snapshot_hashes_recovered"] = True
    freeze["gates"]["live_workspace_v1_0_code_excluded"] = True
    freeze["independent_technical_audit"] = {
        "companion_required_before_run": "INDEPENDENT_TECHNICAL_FREEZE_AUDIT_v1_1.json",
        "must_match_protocol_id_and_freeze_sha256": True,
        "human_signature": None,
        "note": "Technical audit is not human launch authorization.",
    }
    freeze["human_author_launch_approval"] = {
        "status": "PENDING_EXTERNAL",
        "required_before_formal_generation": True,
        "must_acknowledge_maximum_physical_calls": 7476,
    }
    OUT.write_text(json.dumps(freeze, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"protocol_id": freeze["protocol_id"], "path": str(OUT), "sha256": sha(OUT)}))


if __name__ == "__main__":
    main()
