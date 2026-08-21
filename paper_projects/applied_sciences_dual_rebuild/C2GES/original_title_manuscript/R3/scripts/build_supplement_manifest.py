"""Build and verify the exact R3 supplementary allowlist.

The manifest is deliberately outside the inventoried directories so its own
hash does not create a recursive dependency. Source PDFs and full extracted
datasets are prohibited. The immutable prediction ledger is allowed only in
the restricted-local compartment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3 = HERE.parent
SUPP = R3 / "supplementary"
OUT = R3 / "SUPPLEMENT_ALLOWLIST.json"

PROHIBITED_SUFFIXES = {".pdf"}
PROHIBITED_NAMES = {
    "nerc_full_pdf_benchmark_v0_3.jsonl",
    "nerc_full_pdf_dev_v0_3.jsonl",
    "nerc_full_pdf_test_v0_3.jsonl",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    files = []
    failures = []
    for path in sorted((p for p in SUPP.rglob("*") if p.is_file()), key=lambda p: p.as_posix()):
        rel = path.relative_to(R3).as_posix()
        compartment = "restricted_local_only" if "restricted_local_only" in path.parts else "transferable"
        if path.suffix.lower() in PROHIBITED_SUFFIXES or path.name in PROHIBITED_NAMES:
            failures.append(f"prohibited artifact: {rel}")
        if path.name == "predictions.jsonl" and compartment != "restricted_local_only":
            failures.append(f"prediction ledger outside restricted compartment: {rel}")
        files.append({
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "compartment": compartment,
            "external_transfer_allowed": compartment == "transferable",
        })

    required_names = {
        "predictions.jsonl",
        "TEST_FREEZE_MANIFEST_v0_3_1.json",
        "FORMAL_TEST_AUTHORIZATION_v0_3_1.json",
        "OUTPUT_DEPENDENCY_LOCK_v0_3_1.json",
        "rights_safe_report_metadata.csv",
        "exact_signflip_results.json",
        "DEV_ONLY_EXPLORATORY_REPORT.md",
        "REGRESSION_TEST_EVIDENCE.md",
        "INCIDENT_REGISTER.md",
        "INDEPENDENT_PRETEST_AUDIT_v0_3_1.md",
        "INDEPENDENT_POSTRUN_AUDIT_v0_3_1.md",
    }
    present = {Path(item["path"]).name for item in files}
    missing = sorted(required_names - present)
    failures.extend(f"missing required allowlist item: {name}" for name in missing)

    manifest = {
        "schema": "c2ges-r3-supplement-allowlist-v1",
        "status": "PASS" if not failures else "FAIL",
        "scientific_boundary": {
            "formal_predictions_immutable": True,
            "test_rerun": False,
            "test_tuning": False,
            "source_pdfs_packaged": False,
            "full_extracted_datasets_packaged": False,
            "prediction_transfer_requires_permission": True,
        },
        "file_count": len(files),
        "files": files,
        "failures": failures,
    }
    OUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "file_count": len(files), "failures": failures}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()

