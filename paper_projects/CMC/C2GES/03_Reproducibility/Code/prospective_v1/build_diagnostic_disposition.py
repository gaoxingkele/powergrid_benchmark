#!/usr/bin/env python3
"""Map every finding from the confirmatory-only gate to the diagnostic route."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def disposition(code: str) -> tuple[str, str, str]:
    if code == "MANUSCRIPT_NOT_BACKFILLED":
        return (
            "RESOLVED",
            "The manuscript was rewritten as a bounded diagnostic study and no longer presents an unexecuted human study as a submission requirement.",
            "01_Manuscript/LaTeX/paper_applsci.tex",
        )
    if code == "PUBLIC_REPORT_NOT_SUBMISSION_READY":
        return (
            "RESOLVED_BY_ROUTE_SPECIFIC_VERIFICATION",
            "The diagnostic public verifier checks the exploratory evidence boundary and closes only gates relevant to the diagnostic claim set.",
            "02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json",
        )
    if code == "FINAL_EVIDENCE_LOCK_MISSING_OR_INVALID":
        return (
            "RESOLVED_BY_ROUTE_SPECIFIC_LOCK",
            "A separate evidence lock binds the diagnostic manuscript, public verification, disposition, and exploratory evidence.",
            "03_Reproducibility/Data/submission_final/DIAGNOSTIC_SUBMISSION_EVIDENCE_LOCK.json",
        )
    if code.startswith("E1_"):
        return (
            "NOT_APPLICABLE_DIAGNOSTIC_ROUTE",
            "E1 requires a genuinely unseen one-attempt confirmatory corpus. The available reports were accessed before freezing and are reported only as a post-access exploratory pilot.",
            "03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/RUN_MANIFEST.json",
        )
    if code.startswith("E2_"):
        return (
            "NOT_APPLICABLE_NO_HUMAN_VALIDATION_CLAIM",
            "No human study was conducted and no human-validation claim is retained. Machine labels are explicitly non-human and cannot populate E2 artifacts or an ethics decision.",
            "03_Reproducibility/Data/exploratory_external_v0/AUTOMATED_ANNOTATION_AGREEMENT_v3.json",
        )
    if code.startswith("E3_"):
        return (
            "SUPERSEDED_BY_EXPLORATORY_DIAGNOSTIC_E3",
            "The AB/RP/G experiment was completed on the disclosed post-access pilot and is used only for exploratory negative component diagnosis, not confirmatory inference.",
            "03_Reproducibility/Data/exploratory_external_v0/e3_factorial_exploratory_v3/final_info.json",
        )
    if code == "EXTERNAL_GATE_OPEN":
        return (
            "DISPOSED_BY_BOUNDED_CLAIM_SET",
            "The route-specific public report distinguishes not-applicable human/unseen gates from the completed exploratory factorial gate.",
            "02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json",
        )
    raise ValueError(f"unmapped finding code: {code}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = json.loads(args.source.read_text(encoding="utf-8-sig"))
    rows = []
    for index, finding in enumerate(source["findings"], 1):
        state, rationale, evidence = disposition(finding["code"])
        rows.append({
            "source_index": index,
            "code": finding["code"],
            "source_message": finding["message"],
            "source_path": finding.get("path"),
            "diagnostic_disposition": state,
            "rationale": rationale,
            "evidence": evidence,
        })
    output = {
        "schema": "c2ges-confirmatory-findings-diagnostic-disposition-v1",
        "created_on": "2026-09-11",
        "submission_route": "diagnostic",
        "source_report": args.source.as_posix(),
        "source_finding_count": source["finding_count"],
        "disposition_count": len(rows),
        "open_for_diagnostic_route": 0,
        "confirmatory_route_closed": False,
        "confirmatory_route_note": "The confirmatory route remains fail-closed; these dispositions do not convert post-access or machine-generated evidence into confirmatory or human evidence.",
        "findings": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
