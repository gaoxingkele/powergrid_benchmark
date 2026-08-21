"""Build the semantic-completeness and exact-set supplement allowlist."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SUPPLEMENT = ROOT / "supplementary"
OUT = ROOT / "SUPPLEMENT_ALLOWLIST.json"

PROHIBITED_NAMES = {
    "nerc_full_pdf_benchmark_v0_3.jsonl",
    "nerc_full_pdf_dev_v0_3.jsonl",
    "nerc_full_pdf_test_v0_3.jsonl",
    "R2_TO_R3_RESPONSE_MATRIX_DRAFT.md",
}
REQUIRED_PATHS = {
    "supplementary/restricted_local_only/predictions.jsonl": "restricted immutable prediction ledger",
    "supplementary/transferable/FINAL_CITATION_CONTEXT_AUDIT.json": "23-item citation-context audit",
    "supplementary/transferable/development_calibration/run_dev_only_calibration.py": "portable calibration executable",
    "supplementary/transferable/development_calibration/test_dev_only_calibration.py": "portable 10-test suite",
    "supplementary/transferable/development_calibration/verify_calibration.py": "portable calibration verifier",
    "supplementary/transferable/development_calibration/RUN_STATE.json": "calibration state",
    "supplementary/transferable/development_calibration/RUN_MANIFEST.json": "relative calibration manifest",
    "supplementary/transferable/development_calibration/CALIBRATION_DECISION.json": "calibration decision",
    "supplementary/transferable/development_calibration/MECHANICAL_AUDIT.json": "original mechanical audit",
    "supplementary/transferable/development_calibration/PACKAGE_MECHANICAL_AUDIT.json": "package mechanical audit",
    "supplementary/transferable/development_calibration/candidate_summary_ledger.jsonl": "147-row candidate ledger",
    "supplementary/transferable/development_calibration/per_report_ledger.jsonl": "3528-row report ledger",
    "supplementary/transferable/development_calibration/loo_fold_ledger.jsonl": "12-row LOO ledger",
    "supplementary/transferable/development_calibration/path_gate_diagnostics.jsonl": "36-row path-gate ledger",
    "supplementary/transferable/development_calibration/original_frozen/run_dev_only_calibration.py": "original calibration executable",
    "supplementary/transferable/development_calibration/original_frozen/test_dev_only_calibration.py": "original 10-test snapshot",
    "supplementary/transferable/development_calibration/original_frozen/verify_calibration.py": "original verifier snapshot",
    "supplementary/transferable/development_calibration/code_snapshot/c2ges_offline.py": "core snapshot 1",
    "supplementary/transferable/development_calibration/code_snapshot/counterfactual_paths.py": "core snapshot 2",
    "supplementary/transferable/development_calibration/code_snapshot/v03_methods.py": "core snapshot 3",
    "supplementary/transferable/postrun_diagnostics/OUTPUT_LENGTH_AUDIT.json": "output-length audit",
    "supplementary/transferable/postrun_diagnostics/output_length_per_report.csv": "210-row length ledger",
    "supplementary/transferable/postrun_diagnostics/output_length_summary.csv": "14-group length summary",
    "supplementary/transferable/postrun_diagnostics/selected_page_locator.csv": "1575-row non-verbatim locator",
    "supplementary/transferable/postrun_diagnostics/SELECTED_PAGE_LOCATOR_AUDIT.json": "locator audit",
    "supplementary/transferable/figure_inputs/paired_rougel_differences_nonverbatim.csv": "90-row figure source",
    "supplementary/transferable/figure_inputs/RIGHTS_SAFE_FIGURE_INPUT_MANIFEST.json": "figure-source manifest",
    "supplementary/transferable/audits/aggregate_metrics.json": "frozen aggregate metrics",
    "supplementary/transferable/formal_protocol/formal_config_v0_3_1.json": "frozen formal configuration",
    "supplementary/transferable/rights_safe_metadata/rights_safe_report_metadata.json": "40-row rights-safe inventory",
}
EXPECTED_ROWS = {
    "supplementary/transferable/development_calibration/candidate_summary_ledger.jsonl": 147,
    "supplementary/transferable/development_calibration/per_report_ledger.jsonl": 3528,
    "supplementary/transferable/development_calibration/loo_fold_ledger.jsonl": 12,
    "supplementary/transferable/development_calibration/path_gate_diagnostics.jsonl": 36,
}
ORIGINAL_HASHES = {
    "supplementary/transferable/development_calibration/original_frozen/run_dev_only_calibration.py": "9C9AEE586E0B8FAAE483F275BE5D24D4553FA281B5CCB751C2904BF0FD3E418F",
    "supplementary/transferable/development_calibration/original_frozen/test_dev_only_calibration.py": "D723E459563808783BE2637FA137733EF5251202B76E8F987207B5783E60AB98",
    "supplementary/transferable/development_calibration/original_frozen/verify_calibration.py": "A470E5C4331456496B37B2A73F85746CBB850900840DC321EB2F17AF991BF611",
    "supplementary/transferable/development_calibration/code_snapshot/c2ges_offline.py": "77D89DBEB187A6EA89C5786584D5C1F55BCED5B88A949743F95546D39F5FC6DE",
    "supplementary/transferable/development_calibration/code_snapshot/counterfactual_paths.py": "73DD8BB7D6B362558E7DD9EA40F3A2FF8D4AB6CC5EDA493DD8A21701AD504E3C",
    "supplementary/transferable/development_calibration/code_snapshot/v03_methods.py": "6A7884C540690D052D6359481C511AA1170FF1C819627D67DA612897F0BA6216",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    failures: list[dict | str] = []
    paths = sorted((path for path in SUPPLEMENT.rglob("*") if path.is_file()), key=lambda path: path.as_posix())
    actual = {path.relative_to(ROOT).as_posix(): path for path in paths}
    for rel, role in REQUIRED_PATHS.items():
        if rel not in actual:
            failures.append({"missing_required_role": role, "path": rel})
    for rel in actual:
        path = actual[rel]
        if path.name in PROHIBITED_NAMES:
            failures.append({"prohibited_name": rel})
        if "__pycache__" in path.parts or path.suffix.lower() == ".pyc":
            failures.append({"python_cache_prohibited": rel})
        if path.suffix.lower() == ".pdf":
            failures.append({"source_or_other_pdf_prohibited_in_supplement": rel})
        if path.name == "predictions.jsonl" and "restricted_local_only" not in path.parts:
            failures.append({"prediction_ledger_outside_restricted": rel})
    for rel, expected in EXPECTED_ROWS.items():
        if rel in actual:
            observed = sum(bool(line.strip()) for line in actual[rel].read_text(encoding="utf-8").splitlines())
            if observed != expected:
                failures.append({"row_count_mismatch": rel, "expected": expected, "observed": observed})
    for rel, expected in ORIGINAL_HASHES.items():
        if rel in actual and digest(actual[rel]) != expected:
            failures.append({"original_hash_mismatch": rel, "expected": expected, "observed": digest(actual[rel])})
    prediction = actual.get("supplementary/restricted_local_only/predictions.jsonl")
    if prediction and digest(prediction) != "AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F":
        failures.append({"prediction_hash_mismatch": digest(prediction)})

    files = []
    for rel, path in actual.items():
        restricted = "restricted_local_only" in path.parts
        files.append(
            {
                "path": rel,
                "bytes": path.stat().st_size,
                "sha256": digest(path),
                "compartment": "restricted_local_only" if restricted else "transferable",
                "external_transfer_allowed": not restricted,
                "required_role": REQUIRED_PATHS.get(rel),
            }
        )
    manifest = {
        "schema": "c2ges-final-supplement-allowlist-v2",
        "status": "PASS" if not failures else "FAIL",
        "scientific_boundary": {
            "formal_predictions_immutable": True,
            "test_rerun": False,
            "test_tuning": False,
            "source_pdfs_packaged": False,
            "full_extracted_datasets_packaged": False,
            "prediction_transfer_requires_permission": True,
            "safe_editor_zip_excludes_restricted_compartment": True,
        },
        "required_role_count": len(REQUIRED_PATHS),
        "file_count": len(files),
        "files": files,
        "failures": failures,
    }
    OUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "files": len(files), "required_roles": len(REQUIRED_PATHS), "failures": failures}, indent=2))
    raise SystemExit(0 if manifest["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
