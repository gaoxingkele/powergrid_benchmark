"""Assemble the immutable technical freeze manifest without model generation."""
from __future__ import annotations

import json
import platform
import sqlite3
import sys
from pathlib import Path

import freeze_public_baseline as f

ROOT = Path(__file__).resolve().parent


def artifact(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": f.sha256(path)}


def main() -> None:
    material = json.loads((ROOT / "PROMPT_MATERIALIZATION_AUDIT.json").read_text(encoding="utf-8"))
    gold = json.loads((ROOT / "BIRD_GOLD_PREFLIGHT.json").read_text(encoding="utf-8"))
    runtime = json.loads((ROOT / "SQLITE_RUNTIME_COMPATIBILITY.json").read_text(encoding="utf-8"))
    assert material["decision"] == "PASS" and material["generation_calls"] == 0
    assert gold["decision"] == "PASS" and gold["executed_successfully"] == 500
    expected_models = {
        "qwen": "509287f78cb4d4cf6b3843734733b914b2c158e43e22a7f4bf5e963800894d3c",
        "granite": "77bcee066a76dcdd10d0d123c87e32c8ec2c74e31b6ffd87ebee49c9ac215dca",
    }
    model_artifacts = {}
    for name, path in f.MODELS.items():
        entry = artifact(path)
        entry["expected_sha256"] = expected_models[name]
        entry["hash_match"] = entry["sha256"] == expected_models[name]
        model_artifacts[name] = entry
    db_manifest = {}
    for db_id, expected in gold["database_manifest"].items():
        path = ROOT / expected["relative_path"]
        actual = artifact(path)
        actual["expected_sha256"] = expected["sha256"]
        actual["hash_match"] = actual["sha256"] == expected["sha256"]
        db_manifest[db_id] = actual
    code_files = [
        ROOT / "freeze_public_baseline.py", ROOT / "test_public_baseline_freeze.py",
        ROOT / "preflight_bird_gold.py", ROOT / "finalize_freeze_manifest.py",
        ROOT / "audit_frozen_public_baseline.py",
        ROOT / "run_formal_public_baseline.py",
    ]
    evaluator = {
        "repository": "bird-bench/mini_dev",
        "commit": "b3d4bcbbae9a96934ad812551eb400c7a3b23c12",
        "archive": artifact(ROOT / "official_downloads" / "mini_dev_b3d4bcb.zip"),
        "evaluation_ex": artifact(ROOT / "official_evaluator_b3d4bcb" / "evaluation_ex.py"),
        "evaluation_utils": artifact(ROOT / "official_evaluator_b3d4bcb" / "evaluation_utils.py"),
        "boundary": "set(predicted_result_rows) == set(gold_result_rows); row order and duplicate multiplicity ignored, column order retained",
        "safety_wrapper_changes_metric_semantics": False,
        "safety_wrapper_rule": "unsafe/non-executable prediction receives EX=0; safe prediction and gold are compared with the pinned official set-of-row-tuples rule",
    }
    gates = {
        "all_500_questions_and_11_databases": gold["population"] == 500 and gold["databases_present"] == 11,
        "python31011_sqlite3401_gold_500_of_500": runtime["python_version"] == "3.10.11" and runtime["sqlite_version"] == "3.40.1" and gold["executed_successfully"] == 500,
        "official_ex_evaluator_pinned": evaluator["evaluation_ex"]["sha256"] == "da1bbcd4530be83692d7c650c814ea9704bb710d0c953eb75d02ccb38233cf89",
        "prompt_calls_2500_per_model": all(v["rows"] == 2500 for k, v in material["prompt_manifests"].items() if k.endswith("_prompt_manifest.jsonl")),
        "prompt_contents_materialized": all(v["rows"] == 2500 for k, v in material["prompt_manifests"].items() if k.endswith("_prompts.jsonl.gz")),
        "token_budget_pass_both_chat_templates": all(v["exact_counts_available"] and v["over_12000"] == 0 and v["over_context_minus_512"] == 0 for v in material["token_budget"].values()),
        "gold_difficulty_schema_leakage_audit_pass": not material["leakage_failures"],
        "deterministic_call_order_2500_per_model": material["call_order"]["rows"] == 2500,
        "model_hashes_match": all(v["hash_match"] for v in model_artifacts.values()),
        "database_hashes_match": all(v["hash_match"] for v in db_manifest.values()),
        "formal_outputs_zero": material["generation_calls"] == 0 and gold["model_calls"] == 0,
        "dkasql_reproduction_claim_disabled": True,
    }
    manifest = {
        "schema_version": "ma-public-baseline-freeze-v1",
        "protocol_id": f.PROTOCOL_ID,
        "date_local": "2026-08-05",
        "status": "FROZEN_NOT_RUN" if all(gates.values()) else "BLOCKED",
        "formal_model_execution_authorized": False,
        "formal_outputs": 0,
        "expected_future_generation_calls": 5000,
        "claim_boundary": "Independent transparent public comparators on BIRD Mini-Dev; never DKASQL reproduction or sealed-domain validation.",
        "dataset": {
            "name": "BIRD Mini-Dev SQLite", "items": 500, "databases": 11,
            "metadata": artifact(ROOT / "official_metadata" / "bird_mini_dev_sqlite.json"),
            "database_archive": artifact(ROOT / "official_downloads" / "bird_dev.zip"),
            "database_manifest": db_manifest,
            "license": "CC-BY-SA-4.0", "development_visible_not_sealed": True,
            "oracle_evidence_all_methods": True,
        },
        "methods": {
            "B0_DIRECT": {"calls": 1, "adapter": "full schema + evidence; SQL-only"},
            "B1_DECOMP": {"calls": 1, "adapter": "schema_links + clause_plan + final_sql JSON; final_sql scored"},
            "B2_SCHEMA_SELECT": {"calls": 1, "adapter": "deterministic BM25 table/column selection, keys and shortest-FK closure"},
            "B3_EXEC_REPAIR": {"calls": 2, "always_second_call": True, "feedback_vocabulary": list(f.FEEDBACK), "adapter": "candidate, safe execution class, mandatory final call"},
        },
        "selector_offline_audit": material["selector"],
        "prompt_materialization": material,
        "execution": {
            "read_only": "SQLite URI mode=ro + PRAGMA query_only + authorizer denial + progress timeout",
            "all_attempt_denominator": True, "retries": 0, "output_caps": {"one_call_methods": 800, "repair_call_1": 400, "repair_call_2": 400},
            "input_cap_per_item_method": 12000, "context": 16384, "safety_margin": 512,
            "model_order": ["qwen", "granite"], "item_order": "sha256(protocol_id|question_id)",
            "method_order": "cyclic rotation by deterministic item index; B3 calls remain adjacent",
            "evaluator": evaluator,
        },
        "models": model_artifacts,
        "runtime": {
            "llama_cpp_release": "b9637", "commit": "aedb2a5e9ca3d4064148bbb919e0ddc0c1b70ab3",
            "llama_server": artifact(f.SERVER), "llama_tokenize": artifact(f.TOKENIZER),
            "python_compat_archive": artifact(ROOT / "runtime_compat" / "python-3.10.11-embed-amd64.zip"),
            "gold_python": gold["python_version"], "gold_sqlite": gold["sqlite_version"],
            "manifest_builder_python": sys.version, "platform": platform.platform(),
            "hardware": "NVIDIA RTX 3090 24576 MiB; one formal server/slot at a time",
        },
        "code": {p.name: artifact(p) for p in code_files},
        "documentation": {
            "protocol_markdown": artifact(ROOT / "BASELINE_PROTOCOL_FREEZE.md"),
            "formal_runbook": artifact(ROOT / "FORMAL_RUNBOOK.md"),
        },
        "schema_catalog_cache": artifact(ROOT / "SCHEMA_CATALOG_CACHE.json"),
        "gates": gates,
        "independent_technical_audit": {
            "companion_required_before_run": "INDEPENDENT_TECHNICAL_FREEZE_AUDIT.json",
            "must_match_protocol_id_and_freeze_sha256": True,
            "human_signature": None,
            "note": "A delegated independent agent may audit technically; no agent may fabricate author/human approval. The runner verifies the external companion rather than mutating this immutable freeze after audit.",
        },
        "human_author_launch_approval": {"status": "PENDING_EXTERNAL", "required_before_formal_generation": True},
    }
    out = ROOT / "BASELINE_PROTOCOL_FREEZE.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "gates_passed": sum(gates.values()), "gates_total": len(gates), "formal_outputs": 0}, ensure_ascii=False))
    if manifest["status"] == "BLOCKED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
