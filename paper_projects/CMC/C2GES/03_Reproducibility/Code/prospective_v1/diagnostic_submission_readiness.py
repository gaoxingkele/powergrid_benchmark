#!/usr/bin/env python3
"""Fail-closed readiness gate for the bounded C2GES diagnostic route.

This route never treats post-access reports as unseen and never treats model
labels as human validation.  The confirmatory gate in submission_readiness.py
remains unchanged and is expected to reject the current evidence package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PUBLIC_REPORT = "02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json"
MANUSCRIPT_TEX = "01_Manuscript/LaTeX/paper_applsci.tex"
MANUSCRIPT_PDF = "01_Manuscript/PDF/C2GES_Applied_Sciences_2026-09-12_diagnostic_submission.pdf"
SUPPLEMENTARY_PDF = "01_Manuscript/PDF/C2GES_Supplementary_2026-09-12_diagnostic_submission.pdf"
FINAL_LOCK = "03_Reproducibility/Data/submission_final/DIAGNOSTIC_SUBMISSION_EVIDENCE_LOCK.json"
DISPOSITION = "03_Reproducibility/Data/submission_final/CONFIRMATORY_42_FINDINGS_DISPOSITION.json"
CURRENT_RESOLUTION = "03_Reproducibility/Data/submission_final/CURRENT_SUBMISSION_REQUIREMENTS_RESOLUTION.json"


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: str | None = None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_json(path: Path, findings: list[Finding], code: str) -> dict[str, Any] | None:
    if not path.is_file():
        findings.append(Finding(code, "required JSON file is missing", path.as_posix()))
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        findings.append(Finding(code, f"invalid JSON: {exc}", path.as_posix()))
        return None
    if not isinstance(value, dict):
        findings.append(Finding(code, "JSON root must be an object", path.as_posix()))
        return None
    return value


def evaluate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    findings: list[Finding] = []
    tex_path = root / MANUSCRIPT_TEX
    pdf_path = root / MANUSCRIPT_PDF
    supplement_pdf_path = root / SUPPLEMENTARY_PDF
    if not tex_path.is_file():
        findings.append(Finding("MANUSCRIPT_MISSING", "diagnostic manuscript TeX is missing", MANUSCRIPT_TEX))
    else:
        tex = tex_path.read_text(encoding="utf-8-sig")
        title = re.search(r"\\Title\{([^\n]+)\}", tex)
        title_text = "" if title is None else title.group(1)
        if "Diagnostic Evaluation" not in title_text or "Structure-Aware" in title_text or "Typed-Path Graphs" in title_text:
            findings.append(Finding("TITLE_ROUTE_MISMATCH", "title must identify a diagnostic evaluation without an unvalidated structure-aware claim", MANUSCRIPT_TEX))
        required_boundaries = (
            "post-access exploratory",
            "this was not human validation",
            "not establish a length-controlled system advantage",
            "System superiority, semantic validity of the structural proxies, and operational benefit are not established",
            "includes no recruited human participants, human annotators, or animals",
        )
        lowered = tex.lower()
        for phrase in required_boundaries:
            if phrase.lower() not in lowered:
                findings.append(Finding("CLAIM_BOUNDARY_MISSING", f"required diagnostic boundary is absent: {phrase}", MANUSCRIPT_TEX))
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        findings.append(Finding("MANUSCRIPT_PDF_MISSING", "compiled diagnostic manuscript PDF is missing", MANUSCRIPT_PDF))
    if not supplement_pdf_path.is_file() or supplement_pdf_path.stat().st_size == 0:
        findings.append(Finding("SUPPLEMENTARY_PDF_MISSING", "compiled diagnostic supplementary PDF is missing", SUPPLEMENTARY_PDF))

    public = load_json(root / PUBLIC_REPORT, findings, "PUBLIC_REPORT_INVALID")
    if public is not None:
        if public.get("submission_route") != "diagnostic" or public.get("status") != "PASS" or public.get("submission_ready") is not True:
            findings.append(Finding("PUBLIC_REPORT_NOT_READY", "diagnostic public verification must be PASS and submission_ready=true", PUBLIC_REPORT))
        diagnostic = public.get("diagnostic_evidence")
        if not isinstance(diagnostic, dict) or diagnostic.get("status") != "PASS":
            findings.append(Finding("DIAGNOSTIC_EVIDENCE_FAILED", "public report must pass diagnostic evidence checks", PUBLIC_REPORT))

    disposition = load_json(root / DISPOSITION, findings, "DISPOSITION_INVALID")
    if disposition is not None:
        if disposition.get("source_finding_count") != 42 or disposition.get("open_for_diagnostic_route") != 0:
            findings.append(Finding("DISPOSITION_INCOMPLETE", "all 42 original findings require an explicit diagnostic-route disposition", DISPOSITION))
        entries = disposition.get("findings")
        if not isinstance(entries, list) or len(entries) != 42:
            findings.append(Finding("DISPOSITION_COUNT_INVALID", "disposition must contain exactly 42 finding records", DISPOSITION))

    resolution = load_json(root / CURRENT_RESOLUTION, findings, "CURRENT_RESOLUTION_INVALID")
    if resolution is not None:
        if (
            resolution.get("selected_route") != "DIAGNOSTIC_NONCONFIRMATORY"
            or resolution.get("status") != "CURRENT_SUBMISSION_REQUIREMENTS_RESOLVED"
            or resolution.get("current_submission_ready") is not True
            or resolution.get("current_required_open") != 0
            or resolution.get("unresolved_current_submission_requirements") != []
        ):
            findings.append(Finding("CURRENT_RESOLUTION_NOT_READY", "current diagnostic requirements must be explicitly resolved with zero open items", CURRENT_RESOLUTION))

    lock = load_json(root / FINAL_LOCK, findings, "FINAL_LOCK_INVALID")
    if lock is not None:
        if lock.get("status") != "DIAGNOSTIC_SUBMISSION_FINAL" or lock.get("submission_route") != "diagnostic":
            findings.append(Finding("FINAL_LOCK_STATE", "diagnostic evidence lock has the wrong state or route", FINAL_LOCK))
        hashes = lock.get("sha256")
        if not isinstance(hashes, dict) or not hashes:
            findings.append(Finding("FINAL_LOCK_EMPTY", "diagnostic evidence lock requires hashes", FINAL_LOCK))
        else:
            required = {MANUSCRIPT_TEX, MANUSCRIPT_PDF, SUPPLEMENTARY_PDF, PUBLIC_REPORT, DISPOSITION, CURRENT_RESOLUTION}
            missing = required - set(hashes)
            if missing:
                findings.append(Finding("FINAL_LOCK_INCOMPLETE", f"required paths absent from lock: {sorted(missing)}", FINAL_LOCK))
            for relative, expected in hashes.items():
                path = root / relative
                if not path.is_file():
                    findings.append(Finding("LOCKED_FILE_MISSING", "hash-locked file is missing", relative))
                elif not isinstance(expected, str) or sha256(path) != expected.upper():
                    findings.append(Finding("LOCKED_HASH_MISMATCH", "hash-locked file does not match", relative))

    return {
        "schema": "c2ges-diagnostic-submission-readiness-v1",
        "submission_route": "diagnostic",
        "status": "READY" if not findings else "NOT_READY",
        "submission_ready": not findings,
        "finding_count": len(findings),
        "findings": [asdict(item) for item in findings],
        "confirmatory_route_status": "NOT_READY_BY_DESIGN_DO_NOT_RELABEL_POST_ACCESS_EVIDENCE",
    }


def discover_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "C2GES_RELEASE_MARKER.json").is_file():
            return candidate
    raise RuntimeError("C2GES release marker not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.project_root.resolve() if args.project_root else discover_root(Path(__file__).resolve())
    result = evaluate(root)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if result["submission_ready"] else 2)


if __name__ == "__main__":
    main()
