#!/usr/bin/env python3
"""Fail-closed C2GES scientific-submission readiness gate.

Technical reproducibility and scientific submission readiness are deliberately
separate.  This gate accepts only a hash-bound, confirmatory E1/E2/E3 evidence
package and a manuscript that has been backfilled from those results.  It does
not execute experiments, infer missing values, or treat development pilots as
confirmatory evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


EXPECTED_EXTERNAL_MODE = "EXTERNAL_CONFIRMATORY_ONE_ATTEMPT"
PASS_STATES = {"PASS", "COMPLETE", "FROZEN", "APPROVED", "EXEMPT"}
PENDING_WORDS = re.compile(r"\b(?:pending|tbd|to be completed|not frozen)\b", re.I)

E1_FILES = (
    "rights_safe_external_metadata.csv",
    "layout_candidate_audit.csv",
    "balanced_tuning_grid.csv",
    "TUNING_DECISION.json",
    "external_item_metrics.csv",
    "external_aggregate_metrics.csv",
    "external_paired_contrasts.csv",
    "external_series_cluster_results.json",
    "external_loso.csv",
    "selected_page_locator.csv",
    "RUN_MANIFEST.json",
    "OUTPUT_SHA256SUMS.txt",
)
E2_FILES = (
    "annotator_a_blinded.csv",
    "annotator_b_blinded.csv",
    "pre_adjudication_agreement.json",
    "adjudication_log.csv",
    "human_structure_results.csv",
    "confusion_matrix_roles.csv",
    "edge_path_error_taxonomy.csv",
    "claim_gate_decisions.json",
    "ETHICS_OR_EXEMPTION_RECORD.md",
)
E3_FILES = (
    "factorial_item_metrics.csv",
    "factorial_series_effects.csv",
    "factorial_interactions.json",
    "factorial_selection_jaccard.csv",
    "factorial_human_metrics.csv",
    "factorial_runtime_resources.csv",
    "ablation_config_registry.json",
    "FACTORIAL_REPORT.md",
)

FINAL_LOCK = "03_Reproducibility/Data/submission_final/SUBMISSION_EVIDENCE_LOCK.json"
MANUSCRIPT = "01_Manuscript/LaTeX/paper_applsci.tex"
PUBLIC_REPORT = "02_Revision_and_QA/04_Build_Reports/C2GES_PUBLIC_VERIFICATION.json"
EXTERNAL_PROTOCOL = "03_Reproducibility/Data/prospective_external_v1/EXTERNAL_PROTOCOL_FREEZE.json"
FACTORIAL_PROTOCOL = "03_Reproducibility/Data/component_factorial_v1/FACTORIAL_PROTOCOL.json"

PROVISIONAL_MANUSCRIPT_PHRASES = (
    "those experiments remain unexecuted",
    "does not report their outcomes",
    "e1--e3 results will be inserted",
    "prospective human-annotation experiment has not been executed",
    "must be updated from measured e1--e3 results before submission",
    "a later submission-final tag is required",
)


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


def read_json(path: Path, findings: list[Finding], code: str) -> dict[str, Any] | None:
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


def require_files(root: Path, relative_dir: str, names: tuple[str, ...], prefix: str,
                  findings: list[Finding]) -> None:
    directory = root / relative_dir
    for name in names:
        path = directory / name
        if not path.is_file() or path.stat().st_size == 0:
            findings.append(Finding(f"{prefix}_FILE_MISSING", "required non-empty artifact is missing", path.relative_to(root).as_posix()))


def read_csv_rows(path: Path, findings: list[Finding], code: str) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    try:
        with path.open(newline="", encoding="utf-8-sig") as stream:
            rows = list(csv.DictReader(stream))
    except (UnicodeError, csv.Error) as exc:
        findings.append(Finding(code, f"invalid CSV: {exc}", path.as_posix()))
        return []
    if not rows:
        findings.append(Finding(code, "CSV contains no data rows", path.as_posix()))
    return rows


def check_protocol(path: Path, findings: list[Finding], prefix: str) -> dict[str, Any] | None:
    protocol = read_json(path, findings, f"{prefix}_PROTOCOL_MISSING_OR_INVALID")
    if protocol is None:
        return None
    if protocol.get("protocol_status") != "FROZEN":
        findings.append(Finding(f"{prefix}_PROTOCOL_NOT_FROZEN", "protocol_status must be FROZEN", path.as_posix()))
    if protocol.get("execution_allowed") is not True:
        findings.append(Finding(f"{prefix}_EXECUTION_NOT_ALLOWED", "execution_allowed must be true", path.as_posix()))
    return protocol


def check_e1(root: Path, findings: list[Finding]) -> None:
    rel = "03_Reproducibility/Data/prospective_external_v1"
    directory = root / rel
    require_files(root, rel, E1_FILES, "E1", findings)
    run = read_json(directory / "RUN_MANIFEST.json", findings, "E1_RUN_MANIFEST_INVALID")
    if run is not None:
        expectations = {
            "mode": EXPECTED_EXTERNAL_MODE,
            "status": "COMPLETE",
            "external_test_accessed": True,
            "confirmatory_claims_allowed": True,
            "failed_rows": 0,
        }
        for field, expected in expectations.items():
            if run.get(field) != expected:
                findings.append(Finding("E1_RUN_STATE_INVALID", f"{field} must equal {expected!r}", (directory / "RUN_MANIFEST.json").relative_to(root).as_posix()))
        if not isinstance(run.get("series"), int) or run.get("series", 0) < 8:
            findings.append(Finding("E1_SERIES_TOO_FEW", "formal external run must contain at least eight independent series", (directory / "RUN_MANIFEST.json").relative_to(root).as_posix()))
    rows = read_csv_rows(directory / "external_item_metrics.csv", findings, "E1_ITEM_METRICS_EMPTY")
    if rows and any(row.get("status") != "PASS" for row in rows):
        findings.append(Finding("E1_ITEM_FAILURE", "all formal item-metric rows must have status=PASS", f"{rel}/external_item_metrics.csv"))
    metadata = read_csv_rows(directory / "rights_safe_external_metadata.csv", findings, "E1_METADATA_EMPTY")
    if metadata:
        series = {row.get("report_series_id", "").strip() for row in metadata if row.get("report_series_id", "").strip()}
        if len(series) < 8:
            findings.append(Finding("E1_METADATA_SERIES_TOO_FEW", "rights-safe inventory must identify at least eight independent report series", f"{rel}/rights_safe_external_metadata.csv"))
        if any(row.get("rights_status", "").strip().upper() not in {"CLEARED", "PUBLIC_OFFICIAL", "AUTHORIZED"} for row in metadata):
            findings.append(Finding("E1_RIGHTS_UNRESOLVED", "every external report requires an explicit cleared rights_status", f"{rel}/rights_safe_external_metadata.csv"))

    checksums = directory / "OUTPUT_SHA256SUMS.txt"
    if checksums.is_file():
        for number, line in enumerate(checksums.read_text(encoding="utf-8-sig").splitlines(), 1):
            if not line.strip():
                continue
            match = re.fullmatch(r"([0-9A-Fa-f]{64})  (.+)", line)
            if match is None:
                findings.append(Finding("E1_OUTPUT_CHECKSUM_FORMAT", f"malformed checksum line {number}", f"{rel}/OUTPUT_SHA256SUMS.txt"))
                continue
            expected, relative = match.groups()
            artifact = directory / relative
            try:
                artifact.resolve().relative_to(directory.resolve())
            except ValueError:
                findings.append(Finding("E1_OUTPUT_CHECKSUM_ESCAPE", "checksum path escapes the E1 directory", f"{rel}/OUTPUT_SHA256SUMS.txt"))
                continue
            if not artifact.is_file() or sha256(artifact) != expected.upper():
                findings.append(Finding("E1_OUTPUT_CHECKSUM_MISMATCH", "formal output is missing or does not match its checksum", f"{rel}/{relative}"))


def check_e2(root: Path, findings: list[Finding]) -> None:
    rel = "03_Reproducibility/Data/human_structure_validation_v1"
    directory = root / rel
    require_files(root, rel, E2_FILES, "E2", findings)
    decisions = read_json(directory / "claim_gate_decisions.json", findings, "E2_DECISIONS_INVALID")
    if decisions is not None:
        if not decisions or any(value is not True for value in decisions.values()):
            findings.append(Finding("E2_CLAIM_GATE_FAILED", "every retained unconditional structure claim requires a true human-validation gate", f"{rel}/claim_gate_decisions.json"))
    ethics = directory / "ETHICS_OR_EXEMPTION_RECORD.md"
    if ethics.is_file():
        text = ethics.read_text(encoding="utf-8-sig")
        if PENDING_WORDS.search(text) or not re.search(r"\b(?:APPROVED|EXEMPT)\b", text, re.I):
            findings.append(Finding("E2_ETHICS_UNRESOLVED", "ethics record must state APPROVED or EXEMPT and contain no pending marker", f"{rel}/ETHICS_OR_EXEMPTION_RECORD.md"))
    for name in ("annotator_a_blinded.csv", "annotator_b_blinded.csv", "adjudication_log.csv", "human_structure_results.csv"):
        read_csv_rows(directory / name, findings, "E2_CSV_EMPTY")


def check_e3(root: Path, findings: list[Finding]) -> None:
    rel = "03_Reproducibility/Data/component_factorial_v1"
    directory = root / rel
    require_files(root, rel, E3_FILES, "E3", findings)
    for name in ("factorial_item_metrics.csv", "factorial_series_effects.csv", "factorial_selection_jaccard.csv", "factorial_runtime_resources.csv"):
        read_csv_rows(directory / name, findings, "E3_CSV_EMPTY")
    interactions = read_json(directory / "factorial_interactions.json", findings, "E3_INTERACTIONS_INVALID")
    if interactions is not None:
        required = {"reservation_main", "path_main", "reservation_by_path_interaction"}
        if not required.issubset(interactions):
            findings.append(Finding("E3_INTERACTIONS_INCOMPLETE", f"missing interaction estimates: {sorted(required - set(interactions))}", f"{rel}/factorial_interactions.json"))


def check_manuscript(root: Path, findings: list[Finding]) -> None:
    path = root / MANUSCRIPT
    if not path.is_file():
        findings.append(Finding("MANUSCRIPT_MISSING", "submission manuscript is missing", MANUSCRIPT))
        return
    text = path.read_text(encoding="utf-8-sig").lower()
    for phrase in PROVISIONAL_MANUSCRIPT_PHRASES:
        if phrase in text:
            findings.append(Finding("MANUSCRIPT_NOT_BACKFILLED", f"provisional phrase remains: {phrase}", MANUSCRIPT))


def check_public_report(root: Path, findings: list[Finding]) -> None:
    report = read_json(root / PUBLIC_REPORT, findings, "PUBLIC_REPORT_INVALID")
    if report is None:
        return
    if report.get("technical_status") != "PASS":
        findings.append(Finding("TECHNICAL_VERIFICATION_FAILED", "technical_status must be PASS", PUBLIC_REPORT))
    if report.get("submission_ready") is not True:
        findings.append(Finding("PUBLIC_REPORT_NOT_SUBMISSION_READY", "public verifier has not marked the package submission-ready", PUBLIC_REPORT))
    gates = report.get("external_gates")
    if not isinstance(gates, dict):
        findings.append(Finding("EXTERNAL_GATES_INVALID", "external_gates must be an object", PUBLIC_REPORT))
    else:
        for name in ("independent_power_system_expert_annotation", "untouched_external_series_evaluation", "controlled_component_factorial"):
            if str(gates.get(name, "")).upper() not in PASS_STATES:
                findings.append(Finding("EXTERNAL_GATE_OPEN", f"{name} is not closed", PUBLIC_REPORT))


def check_final_lock(root: Path, findings: list[Finding]) -> None:
    path = root / FINAL_LOCK
    lock = read_json(path, findings, "FINAL_EVIDENCE_LOCK_MISSING_OR_INVALID")
    if lock is None:
        return
    if lock.get("status") != "SUBMISSION_FINAL":
        findings.append(Finding("FINAL_EVIDENCE_LOCK_STATE", "lock status must be SUBMISSION_FINAL", FINAL_LOCK))
    hashes = lock.get("sha256")
    if not isinstance(hashes, dict) or not hashes:
        findings.append(Finding("FINAL_EVIDENCE_HASHES_MISSING", "lock must contain a non-empty sha256 mapping", FINAL_LOCK))
        return
    required = {MANUSCRIPT, PUBLIC_REPORT, EXTERNAL_PROTOCOL, FACTORIAL_PROTOCOL}
    required.update(f"03_Reproducibility/Data/prospective_external_v1/{name}" for name in E1_FILES)
    required.update(f"03_Reproducibility/Data/human_structure_validation_v1/{name}" for name in E2_FILES)
    required.update(f"03_Reproducibility/Data/component_factorial_v1/{name}" for name in E3_FILES)
    missing = required - set(hashes)
    if missing:
        findings.append(Finding("FINAL_EVIDENCE_HASHES_INCOMPLETE", f"required locked paths absent: {sorted(missing)}", FINAL_LOCK))
    for relative, expected in hashes.items():
        evidence = root / relative
        if not evidence.is_file():
            findings.append(Finding("FINAL_EVIDENCE_FILE_MISSING", "locked evidence file is missing", str(relative)))
        elif not isinstance(expected, str) or sha256(evidence) != expected.upper():
            findings.append(Finding("FINAL_EVIDENCE_HASH_MISMATCH", "locked SHA-256 does not match", str(relative)))
    locked_pdfs = [relative for relative in hashes if relative.startswith("01_Manuscript/PDF/") and relative.lower().endswith(".pdf")]
    if len(locked_pdfs) != 1:
        findings.append(Finding("FINAL_PDF_LOCK_INVALID", "exactly one submission-final manuscript PDF must be hash-locked", FINAL_LOCK))
    if not re.fullmatch(r"[0-9a-f]{40}", str(lock.get("git_commit", "")), re.I):
        findings.append(Finding("FINAL_COMMIT_INVALID", "git_commit must be a full 40-hex commit id", FINAL_LOCK))
    if not re.fullmatch(r"c2ges-.+-submission-final-v\d+", str(lock.get("git_tag", "")), re.I):
        findings.append(Finding("FINAL_TAG_INVALID", "git_tag must identify a c2ges submission-final version", FINAL_LOCK))


def evaluate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    findings: list[Finding] = []
    if not (root / "C2GES_RELEASE_MARKER.json").is_file():
        findings.append(Finding("PROJECT_MARKER_MISSING", "C2GES_RELEASE_MARKER.json not found", root.as_posix()))
    check_protocol(root / EXTERNAL_PROTOCOL, findings, "E1")
    check_protocol(root / FACTORIAL_PROTOCOL, findings, "E3")
    check_e1(root, findings)
    check_e2(root, findings)
    check_e3(root, findings)
    check_manuscript(root, findings)
    check_public_report(root, findings)
    check_final_lock(root, findings)
    return {
        "schema": "c2ges-submission-readiness-v1",
        "status": "READY" if not findings else "NOT_READY",
        "submission_ready": not findings,
        "finding_count": len(findings),
        "findings": [asdict(item) for item in findings],
    }


def discover_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "C2GES_RELEASE_MARKER.json").is_file():
            return candidate
    raise RuntimeError("C2GES release marker not found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--report", type=Path, help="optional output path outside a frozen release")
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
