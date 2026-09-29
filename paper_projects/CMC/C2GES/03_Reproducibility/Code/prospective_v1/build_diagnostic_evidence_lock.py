#!/usr/bin/env python3
"""Regenerate the bounded diagnostic-route evidence lock deterministically."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "03_Reproducibility/Data/submission_final/DIAGNOSTIC_SUBMISSION_EVIDENCE_LOCK.json"
LOCKED_PATHS = (
    "00_Status_and_Index/CURRENT_BASELINE.md",
    "00_Status_and_Index/E1_E2_E3_EXECUTION_STATUS_2026-09-12.md",
    "01_Manuscript/LaTeX/paper_applsci.tex",
    "01_Manuscript/Supplementary/supplementary_materials.tex",
    "01_Manuscript/Supplementary/figures/figS4_reservation_path_interaction.pdf",
    "01_Manuscript/PDF/C2GES_Applied_Sciences_2026-09-12_diagnostic_submission.pdf",
    "01_Manuscript/PDF/C2GES_Supplementary_2026-09-12_diagnostic_submission.pdf",
    "02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json",
    "03_Reproducibility/Data/submission_final/CONFIRMATORY_42_FINDINGS_DISPOSITION.json",
    "03_Reproducibility/Data/submission_final/DIAGNOSTIC_ROUTE_DECISION.md",
    "03_Reproducibility/Data/submission_final/CURRENT_SUBMISSION_REQUIREMENTS_RESOLUTION.json",
    "03_Reproducibility/Data/submission_final/README.md",
    "03_Reproducibility/Data/exploratory_external_v0/CURRENT_EXPLORATORY_VERSION.json",
    "03_Reproducibility/Data/exploratory_external_v0/EXPLORATORY_EXTERNAL_INVENTORY.csv",
    "03_Reproducibility/Data/exploratory_external_v0/layout_candidate_audit_v3.csv",
    "03_Reproducibility/Data/exploratory_external_v0/AUTOMATED_ANNOTATION_AGREEMENT_v3.json",
    "03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/RUN_MANIFEST.json",
    "03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/external_item_metrics.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/external_aggregate_metrics.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/external_series_cluster_results.json",
    "03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/external_loso.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/selected_page_locator.jsonl",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/final_info.json",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_item_metrics.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_aggregate_metrics.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_inference.json",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_selected_ids.jsonl",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_selection_jaccard.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_series_effects.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_loso.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_runtime_resources.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_human_metrics.csv",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/factorial_interactions.json",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/FACTORIAL_REPORT.md",
    "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/FACTORIAL_DIAGNOSTICS_MANIFEST.json",
    "03_Reproducibility/Data/prospective_external_v1/PRE_FREEZE_ACCESS_LOG.md",
    "03_Reproducibility/Data/prospective_external_v1/SEEN_EXCLUSION_REGISTRY.csv",
    "03_Reproducibility/Data/prospective_external_v1/E1_AUTHOR_UNSEEN_AND_RIGHTS_ATTESTATION.md",
    "03_Reproducibility/Data/human_structure_validation_v1/ETHICS_REVIEW_REQUEST_PACKET.md",
    "03_Reproducibility/Data/human_structure_validation_v1/ETHICS_OR_EXEMPTION_RECORD.md",
    "03_Reproducibility/Data/human_structure_validation_v1/E2_RECRUITMENT_TEXT.md",
    "03_Reproducibility/Data/human_structure_validation_v1/E2_ANNOTATOR_INFORMATION_AND_CONSENT.md",
    "03_Reproducibility/Data/human_structure_validation_v1/E2_DATA_MANAGEMENT_PLAN.md",
    "03_Reproducibility/Code/run_public_verification.py",
    "03_Reproducibility/Code/prospective_v1/build_factorial_diagnostics.py",
    "03_Reproducibility/Code/prospective_v1/generate_factorial_interaction_figure.py",
    "03_Reproducibility/Code/prospective_v1/test_factorial_diagnostics.py",
    "03_Reproducibility/Code/prospective_v1/diagnostic_submission_readiness.py",
    "03_Reproducibility/Code/prospective_v1/build_diagnostic_evidence_lock.py",
    "03_Reproducibility/Code/prospective_v1/resolve_current_submission_requirements.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main() -> None:
    missing = [relative for relative in LOCKED_PATHS if not (ROOT / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"cannot lock missing files: {missing}")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    record = {
        "schema": "c2ges-diagnostic-submission-evidence-lock-v2",
        "status": "DIAGNOSTIC_SUBMISSION_FINAL",
        "submission_route": "diagnostic",
        "created_on": "2026-09-12",
        "base_git_commit": commit,
        "planned_git_tag": "c2ges-2026-09-12-diagnostic-submission-v2",
        "claim_boundary": {
            "external_pilot": "POST_ACCESS_EXPLORATORY_NOT_CONFIRMATORY",
            "machine_labels": "AUTOMATED_ERROR_DISCOVERY_NOT_HUMAN_VALIDATION",
            "factorial": "COMPLETE_EXPLORATORY_MECHANISM_DIAGNOSIS",
            "system_superiority_claimed": False,
            "structural_construct_validity_claimed": False,
            "operational_benefit_claimed": False,
        },
        "sha256": {relative: sha256(ROOT / relative) for relative in LOCKED_PATHS},
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "locked_files": len(LOCKED_PATHS), "output": str(OUTPUT)}))


if __name__ == "__main__":
    main()
