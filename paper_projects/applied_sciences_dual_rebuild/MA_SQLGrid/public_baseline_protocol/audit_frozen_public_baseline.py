"""Independent read-only technical audit of BASELINE_PROTOCOL_FREEZE.json."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auditor", required=True, help="Delegated technical auditor identity; not a human signature.")
    args = parser.parse_args()
    freeze = json.loads((ROOT / "BASELINE_PROTOCOL_FREEZE.json").read_text(encoding="utf-8"))
    checks = {}
    checks["frozen_not_run_status"] = freeze["status"] == "FROZEN_NOT_RUN"
    checks["all_declared_gates_true"] = all(freeze["gates"].values())
    checks["no_formal_outputs"] = freeze["formal_outputs"] == 0 and not freeze["formal_model_execution_authorized"]
    for section in (freeze["models"], freeze["dataset"]["database_manifest"]):
        for name, item in section.items():
            checks[f"hash_{name}"] = sha(Path(item["path"])) == item["sha256"] == item["expected_sha256"]
    for name, item in freeze["code"].items():
        checks[f"code_{name}"] = sha(Path(item["path"])) == item["sha256"]
    for name, item in freeze["documentation"].items():
        checks[f"documentation_{name}"] = sha(Path(item["path"])) == item["sha256"]
    material = freeze["prompt_materialization"]
    order = [json.loads(x) for x in (ROOT / "DETERMINISTIC_CALL_ORDER.jsonl").read_text(encoding="utf-8").splitlines()]
    checks["call_order_hash_and_rows"] = len(order) == 2500 and sha(ROOT / "DETERMINISTIC_CALL_ORDER.jsonl") == material["call_order"]["sha256"]
    by_question = defaultdict(list)
    for row in order:
        by_question[row["question_id"]].append((row["method"], row["call"]))
    checks["500_items_five_calls"] = len(by_question) == 500 and all(len(v) == 5 for v in by_question.values())
    checks["mandatory_b3_second_call"] = all(v.count(("B3_EXEC_REPAIR", 1)) == 1 and v.count(("B3_EXEC_REPAIR", 2)) == 1 for v in by_question.values())
    for model in ("qwen", "granite"):
        manifest_path = ROOT / "materialized_prompts" / f"{model}_prompt_manifest.jsonl"
        content_path = ROOT / "materialized_prompts" / f"{model}_prompts.jsonl.gz"
        records = [json.loads(x) for x in manifest_path.read_text(encoding="utf-8").splitlines()]
        with gzip.open(content_path, "rt", encoding="utf-8") as handle:
            contents = [json.loads(x) for x in handle]
        declared_manifest = material["prompt_manifests"][manifest_path.name]
        declared_content = material["prompt_manifests"][content_path.name]
        checks[f"{model}_manifest_hash_rows"] = len(records) == 2500 and sha(manifest_path) == declared_manifest["sha256"]
        checks[f"{model}_content_hash_rows"] = len(contents) == 2500 and sha(content_path) == declared_content["sha256"]
        aggregate = defaultdict(int)
        for r in records:
            aggregate[(r["question_id"], r["method"])] += r["token_upper_bound"]
        checks[f"{model}_token_caps"] = (
            max(r["token_upper_bound"] for r in records) == material["token_budget"][model]["maximum_call_upper_bound"]
            and max(aggregate.values()) == material["token_budget"][model]["maximum_item_method_aggregate_upper_bound"]
            and all(v <= 12000 for v in aggregate.values())
        )
        checks[f"{model}_prompt_hash_linkage"] = all(
            hashlib.sha256(c["rendered_prompt"].encode("utf-8")).hexdigest() == r["rendered_sha256"]
            and (c["question_id"], c["method"], c["call"]) == (r["question_id"], r["method"], r["call"])
            for c, r in zip(contents, records)
        )
        checks[f"{model}_dynamic_only_b3_call2"] = all(
            (r["dynamic_fields"] == ["first_candidate", "validator_feedback"]) == (r["method"] == "B3_EXEC_REPAIR" and r["call"] == 2)
            for r in records
        )
    # v1.0.1: the pinned embeddable runtime isolates sys.path (._pth), so
    # `-m unittest` cannot import the test module from cwd; wrap with an
    # explicit sys.path insertion while keeping subprocess isolation.
    _test_driver = (
        "import sys,unittest;"
        "sys.path.insert(0,'.');"
        "r=unittest.TextTestRunner(verbosity=2).run("
        "unittest.defaultTestLoader.loadTestsFromName('test_public_baseline_freeze'));"
        "sys.exit(0 if r.wasSuccessful() else 1)"
    )
    tests = subprocess.run([sys.executable, "-c", _test_driver], cwd=ROOT, capture_output=True, text=True)
    checks["unit_tests"] = tests.returncode == 0 and "Ran 6 tests" in (tests.stdout + tests.stderr)  # v1.0.1: 5 -> 6 (multi-statement regression test)
    checks["official_ex_hash"] = sha(ROOT / "official_evaluator_b3d4bcb" / "evaluation_ex.py") == "da1bbcd4530be83692d7c650c814ea9704bb710d0c953eb75d02ccb38233cf89"
    report = {
        "schema_version": "ma-public-baseline-independent-audit-v1",
        "auditor_identity": args.auditor,
        "identity_type": "delegated_independent_technical_agent_not_human_signature",
        "protocol_id": freeze["protocol_id"],
        "freeze_sha256": sha(ROOT / "BASELINE_PROTOCOL_FREEZE.json"),
        "checks": checks,
        "passed": sum(checks.values()), "total": len(checks),
        "decision": "PASS" if all(checks.values()) else "BLOCK",
        "formal_model_calls": 0,
        "dkasql_reproduction_claimed": False,
        "human_signature": None,
        "unit_test_output": (tests.stdout + tests.stderr)[-4000:],
    }
    (ROOT / "INDEPENDENT_TECHNICAL_FREEZE_AUDIT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"decision": report["decision"], "passed": report["passed"], "total": report["total"], "auditor": args.auditor}, ensure_ascii=False))
    if report["decision"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
