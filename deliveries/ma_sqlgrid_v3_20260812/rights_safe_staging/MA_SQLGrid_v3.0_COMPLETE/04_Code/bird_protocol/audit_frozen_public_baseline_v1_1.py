"""Independent technical audit of the additive protocol v1.1 freeze."""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FREEZE_PATH = ROOT / "BASELINE_PROTOCOL_FREEZE_v1_1.json"
BASE_PATH = ROOT / "BASELINE_PROTOCOL_FREEZE.json"
OUT = ROOT / "INDEPENDENT_TECHNICAL_FREEZE_AUDIT_v1_1.json"
PINNED_PYTHON = ROOT / "runtime_compat" / "python31011" / "python.exe"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pinned_eval(source: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(PINNED_PYTHON), "-c", source], cwd=ROOT, capture_output=True, text=True, timeout=timeout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auditor", required=True)
    args = parser.parse_args()
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    base = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["protocol_identity"] = freeze["protocol_id"] == "MA-PUBLIC-BIRD-MINIDEV-v1.1" and freeze["base_protocol_id"] == base["protocol_id"]
    checks["historical_base_freeze_identity"] = freeze["base_freeze_sha256"] == "29c780c63a2dc2baae221cfce52252c716d8720dbeecdc2f7a2fdd5756b42af5"
    checks["live_base_manifest_recorded_excluded"] = (
        freeze["live_workspace_base_manifest"]["observed_sha256"] == sha(BASE_PATH)
        and freeze["live_workspace_base_manifest"]["is_protocol_dependency"] is False
        and sha(BASE_PATH) != freeze["base_freeze_sha256"]
    )
    checks["frozen_not_run"] = freeze["status"] == "FROZEN_NOT_RUN" and freeze["formal_outputs"] == 0 and not freeze["formal_model_execution_authorized"]
    checks["all_declared_gates_true"] = all(freeze["gates"].values())
    checks["dataset_identity"] = freeze["dataset"]["name"] == "BIRD Mini-Dev SQLite" and freeze["dataset"]["items"] == 500 and freeze["dataset"]["databases"] == 11 and freeze["dataset"]["license"] == "CC-BY-SA-4.0"
    checks["methods_unchanged"] = freeze["methods"] == {
        "B0_DIRECT": {"calls": 1, "adapter": "full schema + evidence; SQL-only"},
        "B1_DECOMP": {"calls": 1, "adapter": "schema_links + clause_plan + final_sql JSON; final_sql scored"},
        "B2_SCHEMA_SELECT": {"calls": 1, "adapter": "deterministic BM25 table/column selection, keys and shortest-FK closure"},
        "B3_EXEC_REPAIR": {"calls": 2, "always_second_call": True, "feedback_vocabulary": ["SAFE_EXECUTED", "PARSE_ERROR", "UNKNOWN_TABLE", "UNKNOWN_COLUMN", "AMBIGUOUS_COLUMN", "TYPE_OR_FUNCTION_ERROR", "TIMEOUT", "OTHER_EXECUTION_ERROR"], "adapter": "candidate, safe execution class, mandatory final call"},
    }
    checks["models_identity"] = set(freeze["models"]) == {"qwen", "granite"} and freeze["models"]["qwen"]["sha256"] == "509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c" and freeze["models"]["granite"]["sha256"] == "77bcee066a76dcdd10d0d123c87e32c8ec2c74e31b6ffd87ebee49c9ac215dca"
    checks["claim_boundary_unchanged"] = freeze["claim_boundary"] == "Independent transparent public comparators on BIRD Mini-Dev; never DKASQL reproduction or sealed-domain validation."
    checks["planned_calls_unchanged"] = freeze["expected_future_generation_calls"] == 5000
    inherited_material = copy.deepcopy(freeze["prompt_materialization"])
    checks["prompt_inheritance_declared"] = inherited_material.pop("inherited_from_protocol_id", None) == base["protocol_id"]
    checks["prompt_materialization_unchanged"] = inherited_material == base["prompt_materialization"]
    checks["execution_base_fields_unchanged"] = all(freeze["execution"].get(k) == v for k, v in base["execution"].items())
    checks["pinned_runtime_declared"] = freeze["execution"]["required_formal_python"] == "3.10.11" and freeze["execution"]["required_formal_sqlite"] == "3.40.1"
    checks["change_whitelist_exact"] = freeze["change_control"]["unchanged"] == [
        "dataset", "materialized_prompts", "call_order", "models", "methods",
        "token_limits", "decoding", "zero_retry", "official_ex", "statistics_plan",
    ] and freeze["change_control"]["multi_statement_classification"] == "OTHER_EXECUTION_ERROR"
    checks["v1_0_module_snapshot_hash"] = (
        sha(ROOT / "freeze_public_baseline_v1_0_snapshot.py")
        == "d715d17f3d220fa5d17667ec2603c5290c0b2131ede8fc4ab674776455289d23"
    )
    checks["v1_0_test_snapshot_hash"] = (
        sha(ROOT / "test_public_baseline_freeze_v1_0_snapshot.py")
        == "ffc00d3cd004fd4f1f09de7b598c481b9eba366ac8edd33f4e70b67c39f91a01"
    )
    checks["live_v1_0_files_excluded"] = (
        freeze["change_control"]["live_v1_0_workspace_files_are_dependencies"] is False
        and sha(ROOT / "freeze_public_baseline.py") != "d715d17f3d220fa5d17667ec2603c5290c0b2131ede8fc4ab674776455289d23"
        and sha(ROOT / "test_public_baseline_freeze.py") != "ffc00d3cd004fd4f1f09de7b598c481b9eba366ac8edd33f4e70b67c39f91a01"
    )

    for section in (freeze["models"], freeze["dataset"]["database_manifest"]):
        for name, item in section.items():
            checks[f"hash_{name}"] = sha(Path(item["path"])) == item["sha256"] == item["expected_sha256"]
    for name, item in freeze["code"].items():
        checks[f"code_{name}"] = sha(Path(item["path"])) == item["sha256"]
    for name, item in freeze["documentation"].items():
        checks[f"documentation_{name}"] = sha(Path(item["path"])) == item["sha256"]

    order_path = ROOT / "DETERMINISTIC_CALL_ORDER.jsonl"
    order = [json.loads(line) for line in order_path.read_text(encoding="utf-8").splitlines()]
    material = freeze["prompt_materialization"]
    checks["call_order_hash_rows"] = len(order) == 2500 and sha(order_path) == material["call_order"]["sha256"] == base["prompt_materialization"]["call_order"]["sha256"]
    by_question = defaultdict(list)
    for row in order:
        by_question[row["question_id"]].append((row["method"], row["call"]))
    checks["500_items_five_calls"] = len(by_question) == 500 and all(len(v) == 5 for v in by_question.values())
    checks["mandatory_repair_second_call"] = all(v.count(("B3_EXEC_REPAIR", 1)) == 1 and v.count(("B3_EXEC_REPAIR", 2)) == 1 for v in by_question.values())
    for model in ("qwen", "granite"):
        manifest_path = ROOT / "materialized_prompts" / f"{model}_prompt_manifest.jsonl"
        content_path = ROOT / "materialized_prompts" / f"{model}_prompts.jsonl.gz"
        records = [json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines()]
        with gzip.open(content_path, "rt", encoding="utf-8") as handle:
            contents = [json.loads(line) for line in handle]
        checks[f"{model}_prompt_hashes_rows"] = (
            len(records) == len(contents) == 2500
            and sha(manifest_path) == material["prompt_manifests"][manifest_path.name]["sha256"]
            and sha(content_path) == material["prompt_manifests"][content_path.name]["sha256"]
        )
        checks[f"{model}_prompt_linkage"] = all(
            hashlib.sha256(c["rendered_prompt"].encode("utf-8")).hexdigest() == r["rendered_sha256"]
            and (c["question_id"], c["method"], c["call"]) == (r["question_id"], r["method"], r["call"])
            for c, r in zip(contents, records)
        )

    incidents = freeze["excluded_incidents"]
    incident_checks = []
    for key in ("attempt1_runtime_drift", "replacement1_sqlite_warning"):
        record = incidents[key]
        incident_checks.extend([
            sha(Path(record["call_ledger"]["path"])) == record["call_ledger"]["sha256"],
            sha(Path(record["final_scores"]["path"])) == record["final_scores"]["sha256"],
            record["eligible_for_scoring"] is False,
        ])
    checks["incidents_hash_bound_excluded"] = all(incident_checks)
    checks["physical_call_accounting"] = (
        incidents["physical_calls_completed"] == 2476
        and incidents["new_complete_calls_planned"] == 5000
        and incidents["maximum_physical_calls_after_completion"] == 7476
    )
    checks["no_v1_1_formal_output"] = not any((ROOT.parent / "formal_bird_runs").glob("MA_PUBLIC_BIRD_v1_1_*"))

    base_test_code = (
        "import sys,unittest; sys.path.insert(0,r'" + str(ROOT) + "'); "
        "import freeze_public_baseline_v1_0_snapshot as snap; sys.modules['freeze_public_baseline']=snap; "
        "suite=unittest.defaultTestLoader.loadTestsFromName('test_public_baseline_freeze_v1_0_snapshot'); "
        "r=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(0 if r.wasSuccessful() else 1)"
    )
    base_tests = pinned_eval(base_test_code)
    checks["base_tests_5"] = base_tests.returncode == 0 and "Ran 5 tests" in (base_tests.stdout + base_tests.stderr)
    test_code = (
        "import sys,unittest; sys.path.insert(0,r'" + str(ROOT) + "'); "
        "suite=unittest.defaultTestLoader.loadTestsFromName('test_public_baseline_freeze_v1_1'); "
        "r=unittest.TextTestRunner(verbosity=2).run(suite); raise SystemExit(0 if r.wasSuccessful() else 1)"
    )
    v11_tests = pinned_eval(test_code)
    checks["v1_1_pinned_regression_tests_3"] = v11_tests.returncode == 0 and "Ran 3 tests" in (v11_tests.stdout + v11_tests.stderr)
    diagnostic_code = (
        "import sys,json,time,sqlite3; sys.path.insert(0,r'" + str(ROOT) + "'); "
        "import freeze_public_baseline_v1_1 as f; "
        "row=next(x for x in f.load_rows() if x['question_id']==701); t=time.perf_counter(); "
        "s,rows=f.safe_execute(row['SQL'],f.db_path(row['db_id']),180.0); "
        "print(json.dumps({'python':sys.version.split()[0],'sqlite':sqlite3.sqlite_version,'status':s,'elapsed':time.perf_counter()-t,'rows':rows}))"
    )
    diagnostic = pinned_eval(diagnostic_code, timeout=30)
    try:
        diagnostic_json = json.loads(diagnostic.stdout.strip())
    except Exception:
        diagnostic_json = {}
    checks["question701_pinned_gold"] = (
        diagnostic.returncode == 0
        and diagnostic_json.get("python") == "3.10.11"
        and diagnostic_json.get("sqlite") == "3.40.1"
        and diagnostic_json.get("status") == "SAFE_EXECUTED"
        and diagnostic_json.get("rows") == [[0.6644518272425249]]
    )
    checks["official_ex_hash"] = sha(ROOT / "official_evaluator_b3d4bcb" / "evaluation_ex.py") == "da1bbcd4530be83692d7c650c814ea9704bb710d0c953eb75d02ccb38233cf89"

    report = {
        "schema_version": "ma-public-baseline-independent-audit-v1.1",
        "auditor_identity": args.auditor,
        "identity_type": "delegated_independent_technical_agent_not_human_signature",
        "protocol_id": freeze["protocol_id"],
        "freeze_sha256": sha(FREEZE_PATH),
        "base_freeze_sha256": sha(BASE_PATH),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "decision": "PASS" if all(checks.values()) else "BLOCK",
        "formal_model_calls_v1_1": 0,
        "excluded_incident_calls": 2476,
        "human_signature": None,
        "base_test_output": (base_tests.stdout + base_tests.stderr)[-4000:],
        "v1_1_test_output": (v11_tests.stdout + v11_tests.stderr)[-4000:],
        "question701_diagnostic": diagnostic_json,
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"decision": report["decision"], "passed": report["passed"], "total": report["total"], "auditor": args.auditor}))
    if report["decision"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
