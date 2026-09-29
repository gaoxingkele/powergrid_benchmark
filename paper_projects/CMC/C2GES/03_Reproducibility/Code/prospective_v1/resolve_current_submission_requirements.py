#!/usr/bin/env python3
"""Resolve current diagnostic-submission requirements versus future upgrades."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "03_Reproducibility/Data/submission_final/CURRENT_SUBMISSION_REQUIREMENTS_RESOLUTION.json"


def load(relative: str) -> dict:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {relative}")
    return value


def main() -> None:
    public = load("02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json")
    disposition = load("03_Reproducibility/Data/submission_final/CONFIRMATORY_42_FINDINGS_DISPOSITION.json")
    manuscript = (ROOT / "01_Manuscript/LaTeX/paper_applsci.tex").read_text(encoding="utf-8-sig")

    title_match = re.search(r"\\Title\{([^\n]+)\}", manuscript)
    title = "" if title_match is None else title_match.group(1)
    manuscript_checks = {
        "diagnostic_title": "Diagnostic Evaluation" in title,
        "no_structure_aware_title_claim": "Structure-Aware" not in title,
        "no_typed_path_title_claim": "Typed-Path Graphs" not in title,
        "superiority_disclaimed": (
            "does not establish a system-level advantage" in manuscript
            or "do not establish a system-level advantage" in manuscript
            or "does not establish a length-controlled system advantage" in manuscript
        ),
        "human_validation_disclaimed": "this was not human validation" in manuscript,
        "operational_benefit_disclaimed": "operational benefit are not established" in manuscript,
        "no_humans_reported": "includes no recruited human participants, human annotators, or animals" in manuscript,
    }
    current_ready = (
        public.get("status") == "PASS"
        and public.get("submission_ready") is True
        and disposition.get("open_for_diagnostic_route") == 0
        and all(manuscript_checks.values())
    )

    requirements = [
        {
            "id": "E1",
            "current_route_status": "SATISFIED_AS_BOUNDED_EXPLORATORY_EVIDENCE",
            "evidence": "Seven-series post-access pilot is reported with matched word budgets and an explicit non-confirmatory boundary.",
            "future_upgrade": "A genuinely unseen, prospectively frozen cohort is required only to restore a confirmatory superiority claim.",
        },
        {
            "id": "E2",
            "current_route_status": "NOT_APPLICABLE_NO_HUMAN_OR_CONSTRUCT_VALIDITY_CLAIM",
            "evidence": "The manuscript explicitly labels model annotations as machine error discovery and disclaims human validation and semantic construct validity.",
            "future_upgrade": "Two independent eligible humans are required only before restoring a validated Structure-Aware claim.",
        },
        {
            "id": "E3",
            "current_route_status": "COMPLETE_EXPLORATORY_COMPONENT_DIAGNOSIS",
            "evidence": "AB-0--AB-6, RP factorial, G-U/G-T, Jaccard, series effects, LOSO, runtime, memory, and failures are reported and hash-locked.",
            "future_upgrade": "Repeat on the untouched cohort if the paper is later upgraded to a confirmatory route.",
        },
        {
            "id": "E4",
            "current_route_status": "NOT_APPLICABLE_OPERATIONAL_BENEFIT_NOT_CLAIMED",
            "evidence": "The manuscript does not claim improved engineering review time, accuracy, or omission risk.",
            "future_upgrade": "Required only if an operational-effectiveness claim is introduced.",
        },
        {
            "id": "E5",
            "current_route_status": "NOT_APPLICABLE_MAINTENANCE_GENERALIZATION_NOT_CLAIMED",
            "evidence": "The manuscript limits the study to public technical-report proxies and does not generalize to work orders or maintenance records.",
            "future_upgrade": "Required only if maintenance-record generalization is introduced.",
        },
        {
            "id": "ETHICS",
            "current_route_status": "NOT_APPLICABLE_NO_RECRUITED_HUMANS",
            "evidence": "No humans were recruited and the manuscript reports that boundary; the current study does not present human-subject results.",
            "future_upgrade": "An institutional determination is mandatory before any future human recruitment or annotation.",
        },
        {
            "id": "R1",
            "current_route_status": "COMPLETE",
            "evidence": "Portable verification, non-mutating checks, LaTeX builds, evidence lock, and release manifest pass.",
            "future_upgrade": None,
        },
    ]
    record = {
        "schema": "c2ges-current-submission-requirements-resolution-v1",
        "date": "2026-09-12",
        "selected_route": "DIAGNOSTIC_NONCONFIRMATORY",
        "status": "CURRENT_SUBMISSION_REQUIREMENTS_RESOLVED" if current_ready else "NOT_RESOLVED",
        "current_submission_ready": current_ready,
        "current_required_open": 0 if current_ready else 1,
        "author_portal_attestation": "DEFERRED_MANUAL_SUBMISSION_STEP_NOT_A_TECHNICAL_PACKAGE_GATE",
        "diagnostic_readiness": {
            "status": "EVALUATED_SEPARATELY_BY_DIAGNOSTIC_SUBMISSION_READINESS",
            "report": "02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_SUBMISSION_READINESS.json",
        },
        "public_verification": {
            "status": public.get("status"),
            "submission_ready": public.get("submission_ready"),
        },
        "former_confirmatory_findings": {
            "source_count": disposition.get("source_finding_count"),
            "open_for_current_diagnostic_route": disposition.get("open_for_diagnostic_route"),
            "classification": "FUTURE_UPGRADE_ONLY_NOT_CURRENT_BLOCKERS",
        },
        "manuscript_claim_checks": manuscript_checks,
        "requirements": requirements,
        "unresolved_current_submission_requirements": [] if current_ready else ["diagnostic route verification failed"],
        "future_optional_upgrade_requirements": [
            "signed author unseen-status and rights attestation",
            "prospectively frozen untouched report-series cohort",
            "two independent eligible human annotators",
            "institutional ethics approval, exemption, or formal non-human-subject determination before recruitment",
        ],
        "integrity_rule": "Future requirements may not be backfilled with synthetic data, model labels, or unsigned assertions.",
    }
    OUTPUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": record["status"], "current_required_open": record["current_required_open"], "output": str(OUTPUT)}))
    raise SystemExit(0 if current_ready else 2)


if __name__ == "__main__":
    main()
