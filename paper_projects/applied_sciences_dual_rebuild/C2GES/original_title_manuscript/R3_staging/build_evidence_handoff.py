#!/usr/bin/env python3
"""Freeze hashes and key counts for the R3 evidence handoff."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
R2 = HERE.parents[1] / "original_title_rebuild" / "R2_v0_3"
SENS = R2 / "postrun_sensitivity"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    files = [
        HERE / "REGISTERED_BOOTSTRAP_INTERPRETATION.md",
        HERE / "POST_UNBLINDING_DEV_CALIBRATION_SUPPLEMENT.md",
        HERE / "RIGHTS_SAFE_INDEX_AND_SIGN_COUNTS.md",
        HERE / "R2_TO_R3_RESPONSE_MATRIX_DRAFT.md",
        SENS / "exact_signflip_sensitivity.py",
        SENS / "test_exact_signflip_sensitivity.py",
        SENS / "build_rights_safe_metadata.py",
        SENS / "test_rights_safe_metadata.py",
        SENS / "verify_postrun_package.py",
        SENS / "artifacts/exact_signflip_results.json",
        SENS / "artifacts/exact_signflip_results.csv",
        SENS / "artifacts/EXACT_SIGNFLIP_REPORT.md",
        SENS / "artifacts/OUTPUT_MANIFEST.json",
        SENS / "rights_safe_metadata/rights_safe_report_metadata.json",
        SENS / "rights_safe_metadata/rights_safe_report_metadata.csv",
        SENS / "rights_safe_metadata/RIGHTS_SAFE_METADATA_MANIFEST.json",
        SENS / "INDEPENDENT_MECHANICAL_VERIFY.json",
    ]
    missing = [str(p) for p in files if not p.is_file()]
    if missing:
        raise SystemExit("missing handoff files: " + ", ".join(missing))
    results = json.loads((SENS / "artifacts/exact_signflip_results.json").read_text(encoding="utf-8"))
    meta = json.loads((SENS / "rights_safe_metadata/rights_safe_report_metadata.json").read_text(encoding="utf-8"))
    calibration = json.loads((R2 / "posthoc_dev_cf_calibration/artifacts/CALIBRATION_DECISION.json").read_text(encoding="utf-8"))
    handoff = {
        "handoff_id": "C2GES-R2-to-R3-evidence-fixes-v1",
        "formal_test_modified_or_rerun": False,
        "external_data_read": False,
        "test_hyperparameter_tuning": False,
        "formal_predictions_sha256": results["input"]["sha256"],
        "signflip": {
            "status": results["status"],
            "contrasts": len(results["results"]),
            "assignments_per_contrast": 32768,
            "raw_p": [r["exact_two_sided_signflip_p"] for r in results["results"]],
            "holm_six": [r["holm_adjusted_p_six_tests"] for r in results["results"]],
            "sign_counts": [r["sign_counts"] for r in results["results"]],
            "assumption": results["method"]["assumption"],
        },
        "metadata": {
            "rows": len(meta),
            "included": sum(r["inclusion_status"] == "included" for r in meta),
            "excluded": sum(r["inclusion_status"] == "excluded" for r in meta),
            "rights_resolved": False,
        },
        "post_unblinding_development_calibration": {
            "candidate_count": calibration["candidate_count"],
            "loo_zero_cf_winner_count": calibration["robust_overall"]["loo_winner_count"],
            "winner_frequency": calibration["winner_frequency"],
            "test_input_accessed": calibration["test_input_accessed"],
            "formal_output_accessed": calibration["formal_output_accessed"],
            "does_not_replace_frozen_v0_3_1": calibration["does_not_replace_frozen_v0_3_1"],
        },
        "files": {str(p.relative_to(HERE.parents[4])).replace("\\", "/"): sha(p) for p in files},
        "manual_open_gates": [
            "qualified power-grid human validation/adjudication",
            "file-by-file rights and terms determination",
            "corresponding-author and author/funder/COI/AI-use verification",
            "repository synchronization, release/tag/archive, and fresh-clone verification",
            "new untouched title-concordant maintenance corpus for effectiveness claims",
        ],
    }
    out = HERE / "EVIDENCE_HANDOFF.json"
    out.write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(out), "sha256": sha(out)}, indent=2))


if __name__ == "__main__":
    main()
