#!/usr/bin/env python3
"""Run the portable C2GES checks that do not require redistributed source text."""

from __future__ import annotations

import argparse
import csv
import hashlib
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


def discover_project_root(start: Path) -> Path:
    """Locate a portable C2GES release without relying on a Git checkout."""
    for candidate in (start, *start.parents):
        marker = candidate / "C2GES_RELEASE_MARKER.json"
        if marker.is_file() and (candidate / "01_Manuscript").is_dir() and (candidate / "03_Reproducibility").is_dir():
            return candidate
    raise RuntimeError("C2GES release marker not found above verification script")


PROJECT = discover_project_root(HERE)
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def figure_lineage_checks() -> dict[str, object]:
    registry_path = require(PROJECT / "03_Reproducibility" / "Figures" / "FIGURE_LINEAGE.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    if registry.get("schema") != "c2ges-figure-lineage-v3":
        issues.append(f"unexpected schema: {registry.get('schema')}")
    if registry.get("status") != "PASS":
        issues.append(f"registry status is {registry.get('status')}")
    artifacts = registry.get("artifacts", {})
    if registry.get("artifact_count") != 6 or len(artifacts) != 6:
        issues.append(f"expected six artifacts; recorded {registry.get('artifact_count')} / {len(artifacts)}")

    checked = 0
    manuscript_matches = 0
    project_root = PROJECT.resolve()
    for artifact_id, artifact in artifacts.items():
        records = list(artifact.get("inputs", []))
        script = artifact.get("script")
        if script:
            records.append(script)
        records.extend(artifact.get("outputs", {}).values())
        for record in records:
            relative = record.get("path")
            expected = record.get("sha256")
            if not relative or not expected:
                issues.append(f"{artifact_id}: incomplete lineage record")
                continue
            target = (PROJECT / relative).resolve()
            if not target.is_relative_to(project_root):
                issues.append(f"{artifact_id}: path escapes release root: {relative}")
                continue
            if not target.is_file():
                issues.append(f"{artifact_id}: missing {relative}")
                continue
            checked += 1
            observed = sha256(target)
            if observed != expected:
                issues.append(f"{artifact_id}: hash mismatch {relative}")

        pdf_record = artifact.get("outputs", {}).get("pdf")
        if pdf_record:
            source_pdf = PROJECT / pdf_record["path"]
            manuscript_pdf = MANUSCRIPT / "LaTeX" / "figures" / source_pdf.name
            if not manuscript_pdf.is_file():
                issues.append(f"{artifact_id}: manuscript copy missing: {manuscript_pdf.name}")
            elif sha256(source_pdf) != sha256(manuscript_pdf):
                issues.append(f"{artifact_id}: manuscript/reproducibility PDF mismatch")
            else:
                manuscript_matches += 1

    return {
        "status": "PASS" if not issues else "FAIL",
        "schema": registry.get("schema"),
        "artifacts": len(artifacts),
        "hash_records_checked": checked,
        "manuscript_pdf_matches": manuscript_matches,
        "issues": issues,
    }


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
    layout_pilot_dir = DATA / "prospective_external_v1" / "layout_dev_pilot_v2"
    human_validation_dir = DATA / "human_structure_validation_v1"
    layout_pilot = json.loads(require(layout_pilot_dir / "LAYOUT_DEV_PILOT_MANIFEST.json").read_text(encoding="utf-8"))
    with require(layout_pilot_dir / "layout_candidate_audit.csv").open(newline="", encoding="utf-8-sig") as stream:
        layout_pilot_rows = list(csv.DictReader(stream))
    with require(layout_pilot_dir / "layout_boundary_sample_blank.csv").open(newline="", encoding="utf-8-sig") as stream:
        layout_sample_rows = list(csv.DictReader(stream))
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
        DATA / "prospective_external_v1" / "LAYOUT_BOUNDARY_AUDIT_PROTOCOL.md",
        layout_pilot_dir / "LAYOUT_DEV_PILOT_REPORT.md",
        human_validation_dir / "ANNOTATION_PROTOCOL.md",
        human_validation_dir / "ANNOTATOR_QUALIFICATIONS.md",
        human_validation_dir / "ETHICS_OR_EXEMPTION_RECORD.md",
        human_validation_dir / "HUMAN_VALIDATION_EXECUTION.md",
        human_validation_dir / "annotation_schema.json",
        human_validation_dir / "annotation_form_blank.csv",
        human_validation_dir / "SAMPLING_MANIFEST_TEMPLATE.csv",
        human_validation_dir / "adjudication_log_template.csv",
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
        "layout_pilot_reports": len(layout_pilot_rows),
        "layout_pilot_candidates": layout_pilot["total_candidates"],
        "layout_pilot_sample_rows": len(layout_sample_rows),
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
        "layout_pilot_reports": 12,
        "layout_pilot_candidates": 3782,
        "layout_pilot_sample_rows": 244,
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
    forbidden_public_fields = {"text", "reference", "summary", "title", "url", "source_url"}
    layout_public_fields = ({key.lower() for row in layout_pilot_rows for key in row}
                            | {key.lower() for row in layout_sample_rows for key in row})
    if forbidden_public_fields & layout_public_fields:
        mismatches["layout_pilot_public_schema"] = {
            "expected": "no verbatim-capable fields",
            "observed": sorted(forbidden_public_fields & layout_public_fields),
        }
    if layout_pilot.get("external_test_accessed") is not False or layout_pilot.get("confirmatory_claims_allowed") is not False:
        mismatches["layout_pilot_evidence_boundary"] = {"expected": [False, False], "observed": [layout_pilot.get("external_test_accessed"), layout_pilot.get("confirmatory_claims_allowed")]}
    with (human_validation_dir / "annotation_form_blank.csv").open(newline="", encoding="utf-8-sig") as stream:
        annotation_reader = csv.DictReader(stream)
        annotation_fields = annotation_reader.fieldnames or []
        annotation_rows = list(annotation_reader)
    blinded_forbidden = {"system_condition", "automated_role_label", "confidence_stratum", "selection_agreement"}
    leaked = blinded_forbidden & set(annotation_fields)
    if leaked or annotation_rows:
        mismatches["human_annotation_blank_blinding"] = {
            "expected": "no condition/prediction fields and no label rows",
            "observed": {"leaked_fields": sorted(leaked), "rows": len(annotation_rows)},
        }
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
        "Bijing Liu",
        "Yong Yang",
        "yangyong1@sgepri.sgcc.com.cn",
        "c2ges-2026-09-06-protocol-ready-v1",
        "All authors have read and agreed",
        "ORCID: none declared",
    ]
    missing = [token for token in required_claim_tokens if token not in tex]
    for placeholder in ("email to be provided", "author-email-required@example.com", "[AUTHOR INPUT REQUIRED]"):
        if placeholder in tex:
            missing.append(f"unresolved placeholder: {placeholder}")
    if "\\orcidauthor" in tex or "\\orcidA" in tex:
        missing.append("ORCID command must be omitted when all authors declared NONE")
    abstract_match = re.search(r"\\abstract\{(.*?)\}\s*\\keyword", tex, flags=re.DOTALL)
    abstract_words = [] if abstract_match is None else re.findall(
        r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",
        abstract_match.group(1).replace("\\cges{}", "C2GES").replace("\\%", "%"),
    )
    if not abstract_words or len(abstract_words) > 200:
        missing.append(f"abstract word count must be 1--200; observed {len(abstract_words)}")
    if "test_input_accessed=false" not in supplement:
        missing.append("supplement test-input boundary")
    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex)
    missing_figures = [figure for figure in figures if not (MANUSCRIPT / "LaTeX" / figure).is_file()]
    return {
        "status": "PASS" if not missing and not missing_figures else "FAIL",
        "required_claim_tokens": len(required_claim_tokens),
        "figures": len(figures),
        "abstract_words": len(abstract_words),
        "missing": missing,
        "missing_figures": missing_figures,
    }


def external_gates() -> dict[str, str]:
    return {
        "author_metadata": "PROVIDED_0823_BASELINE_USER_DIRECTED_2026_08_24",
        "author_orcid": "NONE_DECLARED_ALL_AUTHORS",
        "corresponding_author_email": "PROVIDED_0823_SOURCE",
        "author_declarations": "PROVIDED_BY_PRIOR_AUTHOR_DEFAULT_AND_2026_08_24_DIRECTION",
        "author_code_license": "ALL_RIGHTS_RESERVED_NO_EXPLICIT_LICENSE",
        "rights_safe_public_release": "AUTHORIZED_GITHUB_SCOPE",
        "journal_portal_author_attestation": "MANUAL_AT_SUBMISSION_NOT_PACKAGE_GATE",
        "third_party_redistribution_permission": "NOT_REQUIRED_EXCLUDED_FROM_PUBLIC_RELEASE",
        "independent_power_system_expert_annotation": "PENDING",
        "untouched_external_series_evaluation": "PENDING",
        "controlled_component_factorial": "PENDING",
        "operational_maintenance_record_validation": "CLAIM_UPGRADE_ONLY_EXPANDED_SCOPE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-latex", action="store_true", help="run only code and data checks")
    parser.add_argument("--submission", action="store_true", help="fail unless all author/external gates are closed")
    parser.add_argument("--report", type=Path, default=None, help="explicit report path; omitted writes only to the system temporary directory")
    parser.add_argument("--check", action="store_true", help="run non-mutating checks and do not write a report")
    args = parser.parse_args()

    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(f"Python 3.12 required; found {platform.python_version()}")

    checks = [
        run("core_tests", [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py", "-v"], HERE / "core" / "R2_v0_3"),
        run("development_tests", [sys.executable, "-m", "unittest", "-v", "test_dev_only_calibration"], HERE / "dev_calibration"),
        run("postrun_tests", [sys.executable, "-m", "unittest", "-v", "test_exact_signflip_sensitivity", "test_rights_safe_metadata", "test_series_cluster_sensitivity"], HERE / "postrun_sensitivity"),
        run("prospective_tests", [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_*.py", "-v"], HERE / "prospective_v1"),
        run("development_pilot_integrity", [sys.executable, "validate_run.py", "run_2"], HERE / "prospective_v1"),
    ]
    if not args.skip_latex:
        checks.extend([
            run_latex_in_temporary_copy("main_latex", MANUSCRIPT / "LaTeX", "paper_applsci", True),
            run_latex_in_temporary_copy("supplement_latex", MANUSCRIPT / "Supplementary", "supplementary_materials", False),
        ])

    data = data_checks()
    manuscript = manuscript_checks()
    figures = figure_lineage_checks()
    failures = [item["label"] for item in checks if item["returncode"] != 0]
    if data["status"] != "PASS":
        failures.append("data_checks")
    if manuscript["status"] != "PASS":
        failures.append("manuscript_checks")
    if figures["status"] != "PASS":
        failures.append("figure_lineage_checks")
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
        "figure_lineage": figures,
        "commands": checks,
    }
    if args.check:
        report_path = None
    elif args.report is not None:
        report_path = args.report if args.report.is_absolute() else (Path.cwd() / args.report)
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        report_path = Path(tempfile.gettempdir()) / f"C2GES_PUBLIC_VERIFICATION_{stamp}.json"

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": None if report_path is None else str(report_path), "non_mutating": args.check, "failures": failures}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else (2 if report["status"] == "PENDING_EXTERNAL_GATES" else 1)


if __name__ == "__main__":
    raise SystemExit(main())
