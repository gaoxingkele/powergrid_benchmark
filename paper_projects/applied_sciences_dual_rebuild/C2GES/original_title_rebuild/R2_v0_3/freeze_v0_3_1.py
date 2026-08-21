"""Create the unauthorized v0.3.1 successor freeze without parsing test data."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[5]
PREFIX = "paper_projects/applied_sciences_dual_rebuild/C2GES/original_title_rebuild/R2_v0_3"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def entry(relative: str) -> dict[str, object]:
    path = REPO / relative
    return {"path": relative, "sha256": sha256(path), "bytes": path.stat().st_size}


def p(name: str) -> str:
    return f"{PREFIX}/{name}"


def main() -> None:
    config_path = p("formal_config_v0_3_1.json")
    test_path = p("diagnostic_build_08/nerc_full_pdf_test_v0_3.jsonl")
    dependency_lock = p("OUTPUT_DEPENDENCY_LOCK_v0_3_1.json")
    bound_names = (
        "diagnostic_build_08/build_manifest.json",
        "diagnostic_build_08/nerc_full_pdf_benchmark_v0_3.jsonl",
        "diagnostic_build_08/nerc_full_pdf_dev_v0_3.jsonl",
        "diagnostic_build_08/nerc_full_pdf_test_v0_3.jsonl",
        "dev_selection_run04/DEV_SELECTION_DECISION.json",
        "dev_selection_run04/dev_search_ledger.jsonl",
        "dev_selection_run04/run_state.json",
        "INDEPENDENT_STAGE1_REAUDIT_08.md",
        "TEST_FREEZE_MANIFEST_v0_3.json",
        "INDEPENDENT_PRETEST_AUDIT_v0_3.md",
        "CORRECTIVE_HISTORY_v0_3_1.md",
        "PRETEST_REPAIR_RESPONSE.md",
        "OUTPUT_DEPENDENCY_LOCK_v0_3_1.json",
        "formal_config_v0_3_1.json",
    )
    code_names = (
        "run_test_v0_3_1.py",
        "v031_methods.py",
        "counterfactual_paths_v031.py",
        "v03_methods.py",
        "counterfactual_paths.py",
        "generate_dependency_lock_v0_3_1.py",
        "freeze_v0_3_1.py",
    )
    external_code = (
        "paper_projects/applied_sciences_dual_rebuild/C2GES/original_title_rebuild/run_formal_experiment.py",
        "paper_projects/applied_sciences_dual_rebuild/C2GES/original_title_rebuild/c2ges_offline.py",
    )
    test_names = (
        "test_full_pdf_builder.py",
        "test_v03_methods.py",
        "test_counterfactual_paths.py",
        "test_formal_runner_v0_3.py",
        "test_v031_repair.py",
    )
    old_freeze = json.loads((HERE / "TEST_FREEZE_MANIFEST_v0_3.json").read_text(encoding="utf-8"))
    decision = json.loads((HERE / "dev_selection_run04/DEV_SELECTION_DECISION.json").read_text(encoding="utf-8"))
    payload = {
        "freeze_id": "C2GES-NERC-FORMAL-v0.3.1-PRETEST-20260808",
        "created_date": date.today().isoformat(),
        "status": "PRETEST_FROZEN_UNAUTHORIZED_AWAITING_FRESH_INDEPENDENT_AUDIT",
        "evaluation_status": "post_audit_corrective_descriptive_not_fresh_confirmatory",
        "test_execution_authorized": False,
        "path_resolution": "repository_root",
        "repository_root_identity": "powergrid_benchmark",
        "predecessor": {
            "freeze_path": p("TEST_FREEZE_MANIFEST_v0_3.json"),
            "freeze_sha256": sha256(HERE / "TEST_FREEZE_MANIFEST_v0_3.json"),
            "audit_path": p("INDEPENDENT_PRETEST_AUDIT_v0_3.md"),
            "audit_sha256": sha256(HERE / "INDEPENDENT_PRETEST_AUDIT_v0_3.md"),
            "verdict": "FAIL_DO_NOT_AUTHORIZE",
            "formal_test_executed": False,
        },
        "datasets": {
            "combined_path": p("diagnostic_build_08/nerc_full_pdf_benchmark_v0_3.jsonl"),
            "combined_sha256": old_freeze["datasets"]["combined_sha256"],
            "dev_path": p("diagnostic_build_08/nerc_full_pdf_dev_v0_3.jsonl"),
            "dev_sha256": old_freeze["datasets"]["dev_sha256"],
            "test_path": test_path,
            "test_sha256": old_freeze["datasets"]["test_sha256"],
            "included_reports": 27,
            "development_reports": 12,
            "test_reports": 15,
            "test_content_status_during_repair": "not decoded or parsed",
        },
        "development": {
            "decision_path": p("dev_selection_run04/DEV_SELECTION_DECISION.json"),
            "decision_sha256": sha256(HERE / "dev_selection_run04/DEV_SELECTION_DECISION.json"),
            "ledger_path": p("dev_selection_run04/dev_search_ledger.jsonl"),
            "ledger_sha256": sha256(HERE / "dev_selection_run04/dev_search_ledger.jsonl"),
            "registered_grid_records": 144,
            "selected_grid_index": decision["selected"]["grid_index"],
            "selected_config": decision["selected"],
            "test_input_accessed": False,
            "semantic_mmr_lambda": 0.5,
            "semantic_mmr_lambda_selection": "fixed symmetric balance; neither development-optimized nor test-informed",
        },
        "method": {
            "conditions": ["lead", "centroid", "textrank", "semantic_mmr", "role", "graph_no_cf_strict", "c2ges_full"],
            "budgets": [5, 10],
            "semantic_mmr": "0.5*MiniLM centroid cosine - 0.5*maximum selected-sentence MiniLM cosine",
            "counterfactual_parameters": {"path_min_edges": 2, "path_max_edges": 4, "path_max_paths": 250000, "path_max_expansions": 2000000},
            "counterfactual_failure_policy": "fail closed and retain registered failed attempt",
        },
        "statistics": {
            "primary_metric": "ROUGE-L F1",
            "primary_contrasts": ["c2ges_full_minus_graph_no_cf_strict", "c2ges_full_minus_semantic_mmr", "c2ges_full_minus_textrank"],
            "budgets": [5, 10],
            "primary_family_size": 6,
            "paired_bootstrap_samples": 10000,
            "bootstrap_seed_base": 20260808,
            "multiplicity": "Holm step-down across six tests",
        },
        "semantic_model_snapshot": old_freeze["semantic_model_snapshot"],
        "artifacts": {
            "config_path": config_path,
            "config_sha256": sha256(REPO / config_path),
            "repair_response_path": p("PRETEST_REPAIR_RESPONSE.md"),
            "repair_response_sha256": sha256(HERE / "PRETEST_REPAIR_RESPONSE.md"),
            "tests": {"command": "python -m unittest discover -s . -p test_*.py -q", "result": "29 passed, 0 failed, 0 errors"},
        },
        "bound_files": [entry(p(name)) for name in bound_names],
        "code_files": [entry(p(name)) for name in code_names] + [entry(name) for name in external_code],
        "test_files": [entry(p(name)) for name in test_names],
        "runtime": {
            "dependency_lock_path": dependency_lock,
            "dependency_lock_sha256": sha256(REPO / dependency_lock),
            "lock_scope": "recursive installed output-relevant Requires-Dist closure",
            "offline_only": True,
        },
        "authorization": {
            "required": True,
            "status_at_freeze": "unauthorized",
            "artifact_path": p("FORMAL_TEST_AUTHORIZATION_v0_3_1.json"),
            "artifact_exists_at_freeze": False,
            "required_bindings": ["freeze_sha256", "audit_decision_path", "audit_decision_sha256", "run_id", "output_path", "approver", "approved_at", "authorized=true"],
        },
        "run_control": {
            "registry_path": p("formal_run_registry_v0_3_1"),
            "registry_exists_at_freeze": False,
            "canonical_output_root": p("formal_runs_v0_3_1"),
            "permitted_physical_attempts": 1,
            "reservation": "atomic registry-directory creation before test content decoding",
            "second_attempt_policy": "forbidden after CLAIMED, FAILED, COMPLETE, or crash placeholder; requires a new freeze and authorization",
            "failure_policy": "retain registry and entire output; never resume, overwrite, delete, or retry",
        },
        "next_gate": {
            "required": "fresh independent pretest audit",
            "decision_artifact_schema": {"verdict": "PASS", "freeze_sha256": "exact successor freeze hash"},
            "formal_test_before_gate": "forbidden",
        },
    }
    output = HERE / "TEST_FREEZE_MANIFEST_v0_3_1.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(sha256(output))


if __name__ == "__main__":
    main()
