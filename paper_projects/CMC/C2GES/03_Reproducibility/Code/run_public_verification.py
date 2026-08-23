#!/usr/bin/env python3
"""Run the portable C2GES checks that do not require redistributed source text."""

from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DATA = PROJECT / "03_Reproducibility" / "Data"
MANUSCRIPT = PROJECT / "01_Manuscript"
DEFAULT_REPORT = PROJECT / "02_Revision_and_QA" / "04_Build_Reports" / "C2GES_PUBLIC_VERIFICATION.json"


def run(label: str, command: list[str], cwd: Path) -> dict[str, object]:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, errors="replace")
    output = completed.stdout + completed.stderr
    skipped = sum(int(x) for x in re.findall(r"skipped=(\d+)", output))
    return {
        "label": label,
        "command": command,
        "cwd": cwd.relative_to(PROJECT).as_posix(),
        "returncode": completed.returncode,
        "skipped": skipped,
        "output": output,
    }


def run_sequence(label: str, commands: list[list[str]], cwd: Path) -> dict[str, object]:
    outputs: list[str] = []
    returncode = 0
    for command in commands:
        completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, errors="replace")
        outputs.append(f"$ {' '.join(command)}\n{completed.stdout}{completed.stderr}")
        if completed.returncode != 0:
            returncode = completed.returncode
            break
    output = "\n".join(outputs)
    return {
        "label": label,
        "command": commands,
        "cwd": cwd.relative_to(PROJECT).as_posix(),
        "returncode": returncode,
        "skipped": 0,
        "output": output,
    }


def run_latex_in_temporary_copy(label: str, source: Path, stem: str, use_bibtex: bool) -> dict[str, object]:
    """Compile a clean copy so the verification run never edits source files."""
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if not pdflatex or (use_bibtex and not bibtex):
        return {
            "label": label,
            "command": [],
            "cwd": "temporary_copy",
            "returncode": 127,
            "skipped": 0,
            "output": "pdflatex/bibtex is unavailable",
        }

    def ignore_source_build(directory: str, names: list[str]) -> set[str]:
        if Path(directory).resolve() != source.resolve():
            return set()
        return {name for name in names if name in {f"{stem}.aux", f"{stem}.bbl", f"{stem}.blg", f"{stem}.log", f"{stem}.out", f"{stem}.pdf"}}

    with tempfile.TemporaryDirectory(prefix=f"{label}_") as tmp:
        build = Path(tmp) / source.name
        shutil.copytree(source, build, ignore=ignore_source_build)
        commands: list[list[str]] = [[pdflatex, "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"]]
        if use_bibtex:
            commands.append([bibtex, stem])
        commands.extend([[pdflatex, "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"]] * 2)
        outputs: list[str] = []
        returncode = 0
        for command in commands:
            completed = subprocess.run(command, cwd=build, capture_output=True, text=True, errors="replace")
            outputs.append(f"$ {' '.join(command)}\n{completed.stdout}{completed.stderr}")
            if completed.returncode:
                returncode = completed.returncode
                break
        log_path = build / f"{stem}.log"
        log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.is_file() else ""
        if returncode == 0 and ("undefined references" in log.lower() or "undefined citations" in log.lower()):
            returncode = 1
            outputs.append("FAIL: undefined references or citations remain")
        pdf = build / f"{stem}.pdf"
        pages = re.search(r"Output written on .*\((\d+) pages?", log)
        if returncode == 0 and (not pdf.is_file() or pdf.stat().st_size == 0):
            returncode = 1
            outputs.append("FAIL: expected PDF was not generated")
        return {
            "label": label,
            "command": commands,
            "cwd": "temporary_copy",
            "returncode": returncode,
            "skipped": 0,
            "pages": int(pages.group(1)) if pages else -1,
            "pdf_bytes": pdf.stat().st_size if pdf.is_file() else 0,
            "output": "\n".join(outputs),
        }


def require(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(path.relative_to(PROJECT).as_posix())
    return path


def data_checks() -> dict[str, object]:
    metadata_path = require(DATA / "rights_safe_metadata" / "rights_safe_report_metadata.csv")
    with metadata_path.open(newline="", encoding="utf-8-sig") as stream:
        metadata = list(csv.DictReader(stream))
    test = [row for row in metadata if row["analysis_split"] == "test"]
    included = [row for row in metadata if row["inclusion_status"] == "included"]

    length_path = require(DATA / "postrun_diagnostics" / "output_length_per_report.csv")
    with length_path.open(newline="", encoding="utf-8-sig") as stream:
        lengths = list(csv.DictReader(stream))

    signflip = json.loads(require(DATA / "postrun_sensitivity" / "exact_signflip_results.json").read_text(encoding="utf-8"))
    series = json.loads(require(DATA / "postrun_series_cluster" / "series_cluster_results.json").read_text(encoding="utf-8"))
    matched = json.loads(require(DATA / "postrun_matched_word" / "unified_v1" / "matched_word_results.json").read_text(encoding="utf-8"))
    embedding = json.loads(require(DATA / "postrun_embedding_audit" / "embedding_truncation_audit.json").read_text(encoding="utf-8"))
    ranking = json.loads(require(DATA / "postrun_embedding_ranking" / "minilm_v1" / "embedding_ranking_results.json").read_text(encoding="utf-8"))
    layout = json.loads(require(DATA / "postrun_layout_audit" / "pymupdf_blocks_v1" / "layout_unit_audit.json").read_text(encoding="utf-8"))
    clean = json.loads(require(DATA / "postrun_clean_ablation" / "normalized_v1" / "clean_ablation_results.json").read_text(encoding="utf-8"))
    balanced = json.loads(require(DATA / "dev_balanced_tuning" / "equal9_v1" / "BALANCED_TUNING_DECISION.json").read_text(encoding="utf-8"))
    required = [
        DATA / "rights_safe_metadata" / "rights_safe_report_metadata.json",
        DATA / "postrun_diagnostics" / "output_length_summary.csv",
        DATA / "postrun_diagnostics" / "selected_page_locator.csv",
        DATA / "audits" / "aggregate_metrics.json",
        DATA / "figure_inputs" / "paired_rougel_differences_nonverbatim.csv",
        DATA / "postrun_sensitivity" / "exact_signflip_results.csv",
        DATA / "POST_UNBLINDING_DEV_CALIBRATION_SUPPLEMENT.md",
        DATA / "formal_protocol" / "C2GES_REVISION_PROTOCOL_2026-08-23.md",
        DATA / "postrun_layout_audit" / "C2GES_LAYOUT_UNIT_PROTOCOL_2026-08-23.md",
        DATA / "postrun_matched_word" / "C2GES_MATCHED_WORD_PROTOCOL_2026-08-23.md",
        DATA / "postrun_embedding_ranking" / "C2GES_EMBEDDING_RANKING_PROTOCOL_2026-08-23.md",
        DATA / "postrun_clean_ablation" / "C2GES_CLEAN_PATH_ABLATION_PROTOCOL_2026-08-23.md",
        DATA / "dev_balanced_tuning" / "C2GES_BALANCED_TUNING_PROTOCOL_2026-08-23.md",
    ]
    for path in required:
        require(path)

    observed = {
        "sampling_frame_rows": len(metadata),
        "included_reports": len(included),
        "test_reports": len(test),
        "test_series": len({row["report_series_id"] for row in test}),
        "output_length_rows": len(lengths),
        "signflip_contrasts": len(signflip["results"]),
        "series_cluster_contrasts": len(series["results"]),
        "series_clusters": len(series["results"][0]["series"]),
        "matched_word_rows": matched["result_rows"],
        "matched_word_contrasts": len(matched["contrast_family"]),
        "embedding_candidates": embedding["overall"]["n_candidates"],
        "embedding_test_over_256": embedding["by_split"]["test"]["n_over_max_seq_length"],
        "embedding_ranking_contrasts": len(ranking["contrasts"]),
        "layout_reports": layout["reports"],
        "layout_table_detection_failures": layout["table_detection_failures"],
        "clean_ablation_contrasts": len(clean["contrasts"]),
        "balanced_methods": len(balanced["selected"]),
        "balanced_configurations_per_method": balanced["configuration_budget_per_method"],
        "machine_readable_files_checked": len(required) + 3,
    }
    expected = {
        "sampling_frame_rows": 40,
        "included_reports": 27,
        "test_reports": 15,
        "test_series": 10,
        "output_length_rows": 210,
        "signflip_contrasts": 6,
        "series_cluster_contrasts": 6,
        "series_clusters": 10,
        "matched_word_rows": 210,
        "matched_word_contrasts": 6,
        "embedding_candidates": 12924,
        "embedding_test_over_256": 29,
        "embedding_ranking_contrasts": 4,
        "layout_reports": 27,
        "layout_table_detection_failures": 0,
        "clean_ablation_contrasts": 2,
        "balanced_methods": 3,
        "balanced_configurations_per_method": 9,
    }
    mismatches = {key: {"expected": value, "observed": observed[key]}
                  for key, value in expected.items() if observed[key] != value}
    if matched["budgets"] != [110, 260]:
        mismatches["matched_word_budgets"] = {"expected": [110, 260], "observed": matched["budgets"]}
    if any(not (row["cluster_bootstrap_95_low"] <= 0 <= row["cluster_bootstrap_95_high"])
           for row in matched["contrast_family"]):
        mismatches["matched_word_interval_claim"] = {"expected": "all intervals include zero", "observed": "violation"}
    if any(row["holm_adjusted_p_four"] != 1.0 for row in ranking["contrasts"]):
        mismatches["embedding_ranking_holm"] = {"expected": "all 1.0", "observed": "violation"}
    if clean["archived_full_and_strict_selections_reproduced"] is not True:
        mismatches["clean_ablation_reproduction"] = {"expected": True, "observed": clean["archived_full_and_strict_selections_reproduced"]}
    if balanced["test_input_accessed"] is not False:
        mismatches["balanced_tuning_test_boundary"] = {"expected": False, "observed": balanced["test_input_accessed"]}
    if any(row["evaluated_configurations_for_method"] != 9 for row in balanced["selected"].values()):
        mismatches["balanced_tuning_equal_budget"] = {"expected": "9 each", "observed": balanced["selected"]}
    return {"status": "PASS" if not mismatches else "FAIL", "observed": observed, "mismatches": mismatches}


def manuscript_checks() -> dict[str, object]:
    tex = require(MANUSCRIPT / "LaTeX" / "paper_applsci.tex").read_text(encoding="utf-8")
    supplement = require(MANUSCRIPT / "Supplementary" / "supplementary_materials.tex").read_text(encoding="utf-8")
    required_claim_tokens = [
        "110- and 260-word caps",
        "10 frozen report-series clusters",
        "29 of 9504 candidates",
        "normalized-path",
        "exactly nine configurations",
        "future external-series",
    ]
    missing = [token for token in required_claim_tokens if token not in tex]
    if "test_input_accessed=false" not in supplement:
        missing.append("supplement test-input boundary")
    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex)
    missing_figures = [figure for figure in figures if not (MANUSCRIPT / "LaTeX" / figure).is_file()]
    return {
        "status": "PASS" if not missing and not missing_figures else "FAIL",
        "required_claim_tokens": len(required_claim_tokens),
        "figures": len(figures),
        "missing": missing,
        "missing_figures": missing_figures,
    }


def external_gates() -> dict[str, str]:
    return {
        "author_metadata_and_approval": "PENDING",
        "author_code_license_and_release_approval": "PENDING",
        "third_party_redistribution_permission": "NOT_REQUIRED_EXCLUDED_FROM_PUBLIC_RELEASE",
        "independent_power_system_expert_annotation": "CLAIM_UPGRADE_ONLY_EXPANDED_SCOPE",
        "untouched_external_series_evaluation": "CLAIM_UPGRADE_ONLY_EXPANDED_SCOPE",
        "operational_maintenance_record_validation": "CLAIM_UPGRADE_ONLY_EXPANDED_SCOPE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-latex", action="store_true", help="run only code and data checks")
    parser.add_argument("--submission", action="store_true", help="fail unless all author/external gates are closed")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(f"Python 3.12 required; found {platform.python_version()}")

    checks = [
        run("core_tests", [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py", "-v"], HERE / "core" / "R2_v0_3"),
        run("development_tests", [sys.executable, "-m", "unittest", "-v", "test_dev_only_calibration"], HERE / "dev_calibration"),
        run("postrun_tests", [sys.executable, "-m", "unittest", "-v", "test_exact_signflip_sensitivity", "test_rights_safe_metadata", "test_series_cluster_sensitivity"], HERE / "postrun_sensitivity"),
    ]
    if not args.skip_latex:
        checks.extend([
            run_latex_in_temporary_copy("main_latex", MANUSCRIPT / "LaTeX", "paper_applsci", True),
            run_latex_in_temporary_copy("supplement_latex", MANUSCRIPT / "Supplementary", "supplementary_materials", False),
        ])

    data = data_checks()
    manuscript = manuscript_checks()
    failures = [item["label"] for item in checks if item["returncode"] != 0]
    if data["status"] != "PASS":
        failures.append("data_checks")
    if manuscript["status"] != "PASS":
        failures.append("manuscript_checks")
    versions = {}
    for package in ("networkx", "numpy", "rouge-score", "sentence-transformers", "torch"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None

    gates = external_gates()
    pending = [key for key, value in gates.items() if value == "PENDING"]
    report = {
        "schema": "C2GES-public-verification-v2",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "package_versions": versions,
        "technical_status": "PASS" if not failures else "FAIL",
        "submission_ready": not failures and not pending,
        "status": "PASS" if not failures and (not args.submission or not pending) else ("PENDING_EXTERNAL_GATES" if not failures else "FAIL"),
        "failures": failures,
        "external_gates": gates,
        "restricted_boundaries": [
            "source PDFs and verbatim extraction JSONL are not redistributed",
            "formal one-attempt generation is not rerun by this public verifier",
            "tests that require excluded raw ledgers report explicit skips",
        ],
        "data": data,
        "manuscript": manuscript,
        "commands": checks,
    }
    report_path = args.report if args.report.is_absolute() else (Path.cwd() / args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(report_path), "failures": failures}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else (2 if report["status"] == "PENDING_EXTERNAL_GATES" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
