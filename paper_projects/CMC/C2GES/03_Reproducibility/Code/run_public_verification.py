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
    tex = require(MANUSCRIPT / "LaTeX" / "paper_information.tex").read_text(encoding="utf-8")
    supplement = require(MANUSCRIPT / "Supplementary" / "supplementary_materials.tex").read_text(encoding="utf-8")
    required_claim_tokens = [
        "0.0652/0.1044",
        "leading at 260 words but not at 110",
        "9774 of 19,008",
        "12,924 candidates",
        "tab:e2-gate",
        "not a demonstration of equivalence",
        "54--63\\%",
        "c2ges-2026-09-06-protocol-ready-v1",
        "Bijing Liu",
        "Yong Yang",
        "yangyong1@sgepri.sgcc.com.cn",
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


def diagnostic_evidence_checks() -> dict[str, object]:
    """Verify the post-access evidence used by the bounded diagnostic route."""
    base = DATA / "exploratory_external_v0"
    required = [
        base / "CURRENT_EXPLORATORY_VERSION.json",
        base / "EXPLORATORY_EXTERNAL_INVENTORY.csv",
        base / "layout_candidate_audit_v3.csv",
        base / "AUTOMATED_ANNOTATION_AGREEMENT_v3.json",
        base / "e1_system_comparison_exploratory_v3" / "RUN_MANIFEST.json",
        base / "e1_system_comparison_exploratory_v3" / "external_item_metrics.csv",
        base / "e1_system_comparison_exploratory_v3" / "external_aggregate_metrics.csv",
        base / "e1_system_comparison_exploratory_v3" / "external_series_cluster_results.json",
        base / "e1_system_comparison_exploratory_v3" / "external_loso.csv",
        base / "e1_system_comparison_exploratory_v3" / "selected_page_locator.jsonl",
        base / "e3_factorial_exploratory_v3" / "final_info.json",
        base / "e3_factorial_exploratory_v3" / "factorial_item_metrics.csv",
        base / "e3_factorial_exploratory_v3" / "factorial_aggregate_metrics.csv",
        base / "e3_factorial_exploratory_v3" / "factorial_inference.json",
        base / "e3_factorial_exploratory_v3" / "factorial_selected_ids.jsonl",
        base / "e3_factorial_exploratory_v3" / "factorial_selection_jaccard.csv",
        base / "e3_factorial_exploratory_v3" / "factorial_series_effects.csv",
        base / "e3_factorial_exploratory_v3" / "factorial_loso.csv",
        base / "e3_factorial_exploratory_v3" / "factorial_runtime_resources.csv",
        base / "e3_factorial_exploratory_v3" / "factorial_human_metrics.csv",
        base / "e3_factorial_exploratory_v3" / "factorial_interactions.json",
        base / "e3_factorial_exploratory_v3" / "FACTORIAL_REPORT.md",
        base / "e3_factorial_exploratory_v3" / "FACTORIAL_DIAGNOSTICS_MANIFEST.json",
    ]
    issues = [f"missing or empty: {path.relative_to(PROJECT).as_posix()}" for path in required if not path.is_file() or path.stat().st_size == 0]
    observed: dict[str, object] = {"required_artifacts": len(required)}
    if issues:
        return {"status": "FAIL", "observed": observed, "issues": issues}

    current = json.loads(required[0].read_text(encoding="utf-8-sig"))
    machine = json.loads((base / "AUTOMATED_ANNOTATION_AGREEMENT_v3.json").read_text(encoding="utf-8-sig"))
    e1 = json.loads((base / "e1_system_comparison_exploratory_v3" / "RUN_MANIFEST.json").read_text(encoding="utf-8-sig"))
    e3 = json.loads((base / "e3_factorial_exploratory_v3" / "final_info.json").read_text(encoding="utf-8-sig"))
    expected = {
        "current_status": (current.get("status"), "EXPLORATORY_ONLY"),
        "current_confirmatory": (current.get("confirmatory_claims_allowed"), False),
        "e1_mode": (e1.get("mode"), "EXPLORATORY_EXTERNAL_NONCONFIRMATORY"),
        "e1_status": (e1.get("status"), "COMPLETE"),
        "e1_confirmatory": (e1.get("confirmatory_claims_allowed"), False),
        "e1_failed_rows": (e1.get("failed_rows"), 0),
        "e1_reports": (e1.get("reports"), 7),
        "e1_series": (e1.get("series"), 7),
        "e3_mode": (e3.get("mode"), "EXPLORATORY_EXTERNAL_NONCONFIRMATORY"),
        "e3_status": (e3.get("status"), "COMPLETE"),
        "e3_confirmatory": (e3.get("confirmatory_claims_allowed"), False),
        "e3_failed_rows": (e3.get("failed_rows"), 0),
        "e3_rows": (e3.get("result_rows"), 182),
        "machine_status": (machine.get("status"), "AUTOMATED_PILOT_ONLY"),
        "machine_human_validation": (machine.get("counts_as_human_validation"), False),
        "machine_construct_validation": (machine.get("scientific_construct_validation_allowed"), False),
    }
    for name, (actual, wanted) in expected.items():
        if actual != wanted:
            issues.append(f"{name}: expected {wanted!r}, observed {actual!r}")
    with (base / "e1_system_comparison_exploratory_v3" / "external_item_metrics.csv").open(newline="", encoding="utf-8-sig") as stream:
        e1_rows = list(csv.DictReader(stream))
    with (base / "e3_factorial_exploratory_v3" / "factorial_item_metrics.csv").open(newline="", encoding="utf-8-sig") as stream:
        e3_rows = list(csv.DictReader(stream))
    diagnostic_row_expectations = {
        "factorial_selection_jaccard.csv": 154,
        "factorial_series_effects.csv": 140,
        "factorial_loso.csv": 140,
        "factorial_runtime_resources.csv": 26,
        "factorial_human_metrics.csv": 1,
    }
    diagnostic_counts: dict[str, int] = {}
    for filename, expected_count in diagnostic_row_expectations.items():
        with (base / "e3_factorial_exploratory_v3" / filename).open(newline="", encoding="utf-8-sig") as stream:
            rows = list(csv.DictReader(stream))
        diagnostic_counts[filename] = len(rows)
        if len(rows) != expected_count:
            issues.append(f"{filename}: expected {expected_count} data rows, observed {len(rows)}")
        if filename == "factorial_human_metrics.csv" and rows:
            if rows[0].get("status") != "NOT_RUN" or rows[0].get("counts_as_human_validation", "").upper() != "FALSE":
                issues.append("factorial_human_metrics.csv must explicitly record NOT_RUN and FALSE human-validation status")
    if len(e1_rows) != 112 or any(row.get("status") != "PASS" for row in e1_rows):
        issues.append(f"E1 item rows must be 112 PASS rows; observed {len(e1_rows)}")
    if len(e3_rows) != 182 or any(row.get("status") != "PASS" for row in e3_rows):
        issues.append(f"E3 item rows must be 182 PASS rows; observed {len(e3_rows)}")
    observed.update({"e1_item_rows": len(e1_rows), "e3_item_rows": len(e3_rows), "series": e1.get("series"), "machine_samples": machine.get("samples"), "factorial_diagnostic_rows": diagnostic_counts})
    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def revision_evidence_checks() -> dict[str, object]:
    """Verify the two evidence layers added for the Information revision.

    These layers are the held-out matched-budget path-utility revision (RSI) and the
    synthetic stress set v8. They were previously carried in the release without any
    public verification coverage, so the checks below bind the shipped artifacts to the
    numbers and boundaries the manuscript reports.
    """
    issues: list[str] = []
    observed: dict[str, object] = {}

    freeze_path = DATA / "rsi_path_v1" / "evolution" / "FREEZE.json"
    summary_path = DATA / "rsi_path_v1" / "run" / "SUMMARY.json"
    evaluation_path = DATA / "rsi_path_v1" / "run" / "EVALUATION.json"
    protocol_path = HERE / "rsi_path_v1" / "PROTOCOL.json"
    seen_check_path = HERE / "rsi_path_v1" / "SEEN_CHECK.json"
    for path in (freeze_path, summary_path, evaluation_path, protocol_path, seen_check_path):
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"missing or empty: {path.name}")
    if issues:
        return {"status": "FAIL", "observed": observed, "issues": issues}

    freeze = json.loads(freeze_path.read_text(encoding="utf-8-sig"))
    summary = json.loads(summary_path.read_text(encoding="utf-8-sig"))
    evaluation = json.loads(evaluation_path.read_text(encoding="utf-8-sig"))
    protocol = json.loads(protocol_path.read_text(encoding="utf-8-sig"))
    seen = json.loads(seen_check_path.read_text(encoding="utf-8-sig"))

    redesigned = summary["means"]["redesigned_path"]
    no_path = summary["means"]["no_path_c2ges"]
    textrank = summary["means"]["textrank"]
    observed["rsi"] = {
        "n_reports": summary["n"],
        "utility": summary["utility"],
        "path_weight": summary["path_weight"],
        "redesigned_110": round(redesigned["110"], 6),
        "redesigned_260": round(redesigned["260"], 6),
        "no_path_110": round(no_path["110"], 6),
        "no_path_260": round(no_path["260"], 6),
        "textrank_110": round(textrank["110"], 6),
        "textrank_260": round(textrank["260"], 6),
        "wins_both_vs_nopath": summary["wins_both_vs_nopath"],
        "dev_wins_both": freeze["wins_both_dev_budgets"],
        "result_rows": evaluation.get("n_rows"),
        "label": summary["label"],
    }

    def near(a: float, b: float, tol: float = 5e-5) -> bool:
        return abs(float(a) - float(b)) <= tol

    checks = {
        "rsi_dev_freeze_means": near(freeze["dev_mean_110"], 0.08541) and near(freeze["dev_mean_260"], 0.12532),
        "rsi_dev_no_path_means": near(freeze["no_path_dev_mean_110"], 0.08265) and near(freeze["no_path_dev_mean_260"], 0.12197),
        "rsi_dev_wins_both": freeze["wins_both_dev_budgets"] is True,
        "rsi_test_values": near(redesigned["110"], 0.0652) and near(redesigned["260"], 0.1044)
        and near(no_path["110"], 0.0654) and near(no_path["260"], 0.1020),
        "rsi_textrank_values": near(textrank["110"], 0.0675) and near(textrank["260"], 0.1031),
        "rsi_wins_260_only": redesigned["260"] > no_path["260"] and redesigned["110"] < no_path["110"],
        "rsi_not_both_budgets": summary["wins_both_vs_nopath"] is False,
        "rsi_label_held_out": summary["label"] == "held-out-for-this-revision",
        "rsi_protocol_not_unseen": protocol["evaluation"]["not_unseen_confirmatory"] is True,
        "rsi_protocol_budgets": protocol["evaluation"]["word_budgets"] == [110, 260],
        "rsi_protocol_forbidden_inputs": len(protocol["evolution"]["forbidden_inputs"]) >= 2,
        "rsi_no_unused_series": protocol["seen_exclusion"]["unused_lawful_public_series_available"] is False
        and seen["unused_lawful_public_series_available"] is False,
        "rsi_seen_registry_excluded": seen["all_excluded_from_confirmatory_external"] is True,
        "rsi_result_rows": evaluation.get("n_rows") == 90,
        "rsi_protocol_hash": freeze["protocol_sha256"] == protocol.get("protocol_sha256", freeze["protocol_sha256"])
        and freeze["protocol_sha256"] == evaluation["protocol_sha256"],
    }
    for name, ok in checks.items():
        if not ok:
            issues.append(f"{name} failed")

    synthetic_dir = DATA / "synthetic_stress_v1" / "run_20260918_heldout_v8"
    manifest_path = synthetic_dir / "SYNTHETIC_RUN_MANIFEST.json"
    final_info_path = synthetic_dir / "e3_factorial_pilot" / "final_info.json"
    inference_path = synthetic_dir / "e3_factorial_pilot" / "factorial_inference.json"
    for path in (manifest_path, final_info_path, inference_path):
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"missing or empty: {path.relative_to(DATA).as_posix()}")
    if inference_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        final_info = json.loads(final_info_path.read_text(encoding="utf-8-sig"))
        inference = json.loads(inference_path.read_text(encoding="utf-8-sig"))
        path_contrasts = [row for row in inference["incremental_chain"] if row.get("contrast") == "AB-5_minus_AB-6"]
        observed["synthetic"] = {
            "reports": final_info["reports"],
            "series": final_info["series"],
            "result_rows": final_info["result_rows"],
            "conditions": final_info["conditions"],
            "mode": final_info["mode"],
            "path_contrast_holm": [row.get("holm_adjusted_p") for row in path_contrasts],
        }
        synthetic_checks = {
            "synthetic_reports": manifest["reports"] == 8 and final_info["reports"] == 8,
            "synthetic_series": manifest["series"] == 4 and final_info["series"] == 4,
            "synthetic_fictional": manifest["synthetic"] is True and manifest["confirmatory_claims_allowed"] is False,
            "synthetic_external_not_accessed": manifest["external_test_accessed"] is False
            and final_info["external_test_accessed"] is False,
            "synthetic_status": final_info["status"] == "COMPLETE" and final_info["failed_rows"] == 0,
            "synthetic_budgets": final_info["word_budgets"] == [110, 260],
            "synthetic_path_holm_all_one": bool(path_contrasts)
            and all(row.get("holm_adjusted_p") == 1.0 for row in path_contrasts),
        }
        for name, ok in synthetic_checks.items():
            if not ok:
                issues.append(f"{name} failed")

    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def construct_audit_checks() -> dict[str, object]:
    """Verify the shipped adjacent-corpus construct audit of role and edge cues.

    The audit uses third-party human-annotated corpora that are not redistributed,
    so only the scripts and the aggregate result records ship. The checks below bind
    those aggregates to the numbers the manuscript reports.
    """
    base = DATA / "construct_audit_v1"
    required = [
        base / "audit_typed_edges_vs_human_rst.py",
        base / "audit_roles_vs_expert_pio.py",
        base / "typed_edge_construct_audit_v1.json",
        base / "role_construct_audit_ebm_v1.json",
    ]
    issues = [f"missing or empty: {p.name}" for p in required if not p.is_file() or p.stat().st_size == 0]
    if issues:
        return {"status": "FAIL", "observed": {}, "issues": issues}

    gum = json.loads(required[2].read_text(encoding="utf-8"))
    ebm = json.loads(required[3].read_text(encoding="utf-8"))
    observed = {
        "gum_edus": gum.get("edu_total"),
        "gum_unit_role_coverage": gum.get("unit_level", {}).get("unit_role_coverage"),
        "gum_relation_pairs": gum.get("human_relation_pairs"),
        "gum_pairs_with_role_evidence": gum.get("pairs_with_role_evidence_both_units"),
        "gum_predicted_edges": gum.get("predicted_edges"),
        "ebm_documents": ebm.get("documents_used"),
        "ebm_sentences": ebm.get("sentences"),
        "ebm_role_coverage": ebm.get("unit_role_coverage"),
        "ebm_intervention_precision": ebm["per_role"]["interventions->mitigation"]["precision"],
        "ebm_intervention_recall": ebm["per_role"]["interventions->mitigation"]["recall"],
        "ebm_outcome_precision": ebm["per_role"]["outcomes->impact"]["precision"],
        "ebm_outcome_recall": ebm["per_role"]["outcomes->impact"]["recall"],
    }
    checks = {
        "gum_edus": gum.get("edu_total") == 7678,
        "gum_role_coverage": abs(gum.get("unit_level", {}).get("unit_role_coverage", 0) - 0.0455) < 1e-4,
        "gum_relation_pairs": gum.get("human_relation_pairs") == 7285,
        "gum_pairs_with_role_evidence": gum.get("pairs_with_role_evidence_both_units") == 45,
        "gum_no_predicted_edges": gum.get("predicted_edges") == 0,
        "ebm_documents": ebm.get("documents_used") == 191,
        "ebm_sentences": ebm.get("sentences") == 2139,
        "ebm_intervention_metrics": abs(observed["ebm_intervention_precision"] - 0.6102) < 1e-3
        and abs(observed["ebm_intervention_recall"] - 0.0642) < 1e-3,
        "ebm_outcome_metrics": abs(observed["ebm_outcome_precision"] - 0.8072) < 1e-3
        and abs(observed["ebm_outcome_recall"] - 0.0604) < 1e-3,
        "corpora_not_redistributed": not any(
            (PROJECT / scope).exists() and list((PROJECT / scope).rglob("*.rels"))
            for scope in ("03_Reproducibility", "01_Manuscript", "02_Revision_and_QA")
        ),
    }
    for name, ok in checks.items():
        if not ok:
            issues.append(f"{name} failed")
    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def external_prospective_checks() -> dict[str, object]:
    """Verify the shipped external prospective evaluation (v2, Markdown extraction).

    Third-party incident-report PDFs and their verbatim Markdown never ship, so the
    checks bind the aggregate record to the numbers the manuscript reports and
    confirm that no corpus text entered the release scopes.
    """
    base = DATA / "external_prospective_v1"
    result_path = base / "external_prospective_v2.json"
    extension_path = base / "external_prospective_v2_expanded.json"
    arms_path = base / "external_arms_v3.json"
    protocol_path = base / "PROTOCOL_external_prospective_v1.md"
    scripts = [
        base / "run_external_prospective_v2.py",
        base / "convert_to_markdown.py",
        base / "fetch_with_snapshot_fallback.py",
        base / "run_external_arms_v3.py",
    ]
    required = [result_path, extension_path, arms_path, protocol_path, *scripts]
    issues = [f"missing or empty: {p.name}" for p in required if not p.is_file() or p.stat().st_size == 0]
    if issues:
        return {"status": "FAIL", "observed": {}, "issues": issues}

    payload = json.loads(result_path.read_text(encoding="utf-8"))
    extension = json.loads(extension_path.read_text(encoding="utf-8"))
    arms = json.loads(arms_path.read_text(encoding="utf-8"))
    contrasts = {(c["contrast"], c["budget"]): c for c in payload["contrasts"]}
    ext_contrasts = {(c["contrast"], c["budget"]): c for c in extension["contrasts"]}
    arm_contrasts = {(c["contrast"], c["budget"]): c for c in arms["contrasts"]}

    def arm(contrast: str, budget: str) -> dict:
        return arm_contrasts.get((contrast, budget), {})

    role_110 = arm("AB2 - AB0", "word:110")
    role_u10 = arm("AB2 - AB0", "unit:10")
    path = {b: arm("Full - no_path", b) for b in ("word:110", "word:260", "unit:5", "unit:10")}
    path_260 = path["word:260"]
    tr_110 = arm("TextRank - no_path", "word:110")
    tr_u5 = arm("TextRank - no_path", "unit:5")
    manuscript_text = (PROJECT / "01_Manuscript/LaTeX/paper_information.tex").read_text(encoding="utf-8")
    observed = {
        "documents": payload.get("reports_kept"),
        "families": sorted({d["family"] for d in payload["kept_documents"]}),
        "means": {k: v["mean"] for k, v in payload["by_condition"].items()},
        "holm": {f"{k[0]}@{k[1]}": v.get("holm_p") for k, v in contrasts.items()},
        "reference_words_min": min(d["reference_words"] for d in payload["kept_documents"]),
        "extension_documents": extension.get("reports_kept"),
        "extension_families": dict(
            __import__("collections").Counter(d["family"] for d in extension["kept_documents"])
        ),
        "extension_path_260": {
            "mean": ext_contrasts[("full_path_0.10 - no_path", 260)]["mean_difference"],
            "p": ext_contrasts[("full_path_0.10 - no_path", 260)]["exact_signflip_p"],
            "negative": ext_contrasts[("full_path_0.10 - no_path", 260)]["negative_documents"],
            "positive": ext_contrasts[("full_path_0.10 - no_path", 260)]["positive_documents"],
        },
        "arms_documents": arms.get("documents"),
        "arms_families": sorted(arms.get("families", [])),
        "role_layer_word110": {k: role_110.get(k) for k in ("mean", "negative", "positive", "zero", "p", "holm")},
        "role_layer_unit10": {k: role_u10.get(k) for k in ("mean", "negative", "positive", "zero", "p", "holm")},
        "path_layer_means": {b: c.get("mean") for b, c in path.items()},
        "path_layer_word260": {k: path_260.get(k) for k in ("mean", "negative", "positive", "zero", "p")},
        "textrank_flip": {"word110": tr_110.get("mean"), "unit5": tr_u5.get("mean")},
    }
    full260 = contrasts[("full_path_0.10 - no_path", 260)]
    tr260 = contrasts[("textrank - no_path", 260)]
    checks = {
        "documents": payload.get("reports_kept") == 19,
        "families": observed["families"] == ["entsoe_grid", "entsoe_market", "nerc"],
        "full_260_negative_and_corrected": abs(full260["mean_difference"] + 0.002906) < 1e-6
        and abs(full260["holm_p"] - 0.046875) < 1e-6
        and full260["negative_documents"] == 7
        and full260["positive_documents"] == 0,
        "textrank_260_positive_and_corrected": abs(tr260["mean_difference"] - 0.022940) < 1e-6
        and abs(tr260["holm_p"] - 0.032380) < 1e-6,
        "small_budget_not_significant": abs(contrasts[("full_path_0.10 - no_path", 110)]["holm_p"] - 0.317284) < 1e-6
        and abs(contrasts[("textrank - no_path", 110)]["holm_p"] - 0.317284) < 1e-6,
        "references_are_substantive": observed["reference_words_min"] >= 100,
        "claim_class_declared": "not author-attested unseen" in result_path.read_text(encoding="utf-8"),
        "extension_documents": extension.get("reports_kept") == 24,
        "extension_path_direction_stable": abs(
            ext_contrasts[("full_path_0.10 - no_path", 260)]["mean_difference"] + 0.006908
        )
        < 1e-5
        and ext_contrasts[("full_path_0.10 - no_path", 260)]["negative_documents"] == 10
        and ext_contrasts[("full_path_0.10 - no_path", 260)]["positive_documents"] == 1,
        "extension_mean_test_not_significant": abs(
            ext_contrasts[("full_path_0.10 - no_path", 260)]["exact_signflip_p"] - 0.444286
        )
        < 1e-3,
        "arms_documents_and_families": arms.get("documents") == 24
        and arms.get("schema") == "c2ges-external-arms-v3"
        and sorted(arms.get("families", [])) == ["entsoe_grid", "entsoe_market", "nerc", "other"],
        "role_layer_reverses_under_equal_word_budget": abs(role_110.get("mean", 0) + 0.035099) < 1e-5
        and role_110.get("negative") == 18
        and role_110.get("positive") == 4
        and role_110.get("zero") == 2
        and abs(role_110.get("p", 0) - 0.003870) < 1e-3
        and abs(role_110.get("holm", 0) - 0.0774) < 1e-3,
        "role_layer_only_positive_under_equal_unit_budget": abs(role_u10.get("mean", 0) - 0.010791) < 1e-5
        and role_u10.get("p", 0) > 0.05
        and role_u10.get("holm") == 1.0,
        "path_layer_stable_across_all_budgets": all(
            abs(c.get("mean", 1)) <= 0.007 and c.get("holm") == 1.0 for c in path.values()
        )
        and path_260.get("negative") == 10
        and path_260.get("positive") == 1
        and path_260.get("zero") == 13
        and abs(path_260.get("mean", 0) + 0.006908) < 1e-5
        and abs(path_260.get("p", 0) - 0.444286) < 1e-3,
        "baseline_ordering_flips_with_budget_type": tr_110.get("mean", 0) > 0.02 and tr_u5.get("mean", 0) < -0.015,
        "arm_numbers_bound_to_manuscript": all(
            token in manuscript_text for token in ("0.03510", "18 of 22", "0.0039", "0.0774", "0.01079")
        ),
        "no_corpus_text_in_release": not any(
            (PROJECT / scope).rglob("*") and any(
                p.suffix.lower() in {".md"} and "markdown" in p.parent.name.lower()
                for p in (PROJECT / scope).rglob("*") if p.is_file()
            )
            for scope in ("03_Reproducibility", "01_Manuscript", "02_Revision_and_QA")
        ),
    }
    for name, ok in checks.items():
        if not ok:
            issues.append(f"{name} failed")
    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def release_boundary_and_addenda_checks() -> dict[str, object]:
    """Guard the redistribution boundary and bind the second addendum round.

    Two distinct jobs:
      * no shipped data record may carry a long natural-language run, which is how
        verbatim third-party passages would enter the release;
      * the reviewer-requested addenda (equivalence bounds, budget curve, S14-S16
        sources) must exist with the row counts the supplement reports.
    """
    data_root = PROJECT / "03_Reproducibility" / "Data"
    sums_path = PROJECT / "03_Reproducibility" / "Package_Metadata" / "FILE_SHA256SUMS.txt"
    issues: list[str] = []
    observed: dict[str, object] = {}
    if not sums_path.is_file():
        return {"status": "FAIL", "observed": {}, "issues": [f"missing {sums_path.name}"]}

    shipped: list[str] = []
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            shipped.append(parts[1].strip())
    observed["shipped_files"] = len(shipped)
    observed["sealed_verbatim_shipped"] = any(path.endswith("SEALED_CHOICES.jsonl") for path in shipped)

    # A verbatim passage shows up as a long run that is mostly ordinary words.
    # Identifier lists ("u00001", "u00002", ...) and our own prose documents are
    # not scanned: only shipped data records are, and a run must carry at least
    # forty alphabetic words separated by spaces to count as a passage.
    run = re.compile(r"[A-Za-z][A-Za-z0-9 ,.;:'\"()\-/]{300,}")
    word = re.compile(r"[A-Za-z]{3,}")
    offenders: list[str] = []
    for relative in shipped:
        if not relative.startswith("03_Reproducibility/Data/"):
            continue
        if "synthetic_stress_v1" in relative:
            continue
        path = PROJECT / relative
        if not path.is_file() or path.suffix.lower() not in {".csv", ".json", ".jsonl", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(
            len(word.findall(match.group(0))) >= 40 and match.group(0).count(" ") >= 20
            for match in run.finditer(text)
        ):
            offenders.append(relative)
    observed["verbatim_like_records"] = offenders
    if offenders:
        issues.append(f"long prose runs in shipped data records: {offenders[:5]}")
    if observed["sealed_verbatim_shipped"]:
        issues.append("verbatim SEALED_CHOICES.jsonl is listed as shipped")

    expectations = {
        "03_Reproducibility/Data/rsi_path_v1/run/SEALED_CHOICES_rights_safe.jsonl": 90,
        "03_Reproducibility/Data/equivalence_bounds_v1/equivalence_bounds_v1.json": None,
        "03_Reproducibility/Data/external_prospective_v1/external_arms_curve_v4.json": None,
        "03_Reproducibility/Data/descriptive_addenda_v2/q5_reservation_path_effects.csv": 6,
        "03_Reproducibility/Data/descriptive_addenda_v2/q9_external_family_paired_contrasts.csv": 24,
        "03_Reproducibility/Data/descriptive_addenda_v2/q4_role_edge_coverage_per_report.csv": 14,
        "03_Reproducibility/Data/budget_curve_v1/figS5_source.csv": 54,
        "01_Manuscript/Supplementary/figures/figS5_budget_efficiency_curve.pdf": None,
    }
    counts: dict[str, int | None] = {}
    for relative, expected in expectations.items():
        path = PROJECT / relative
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"missing addendum artifact: {relative}")
            counts[relative] = None
            continue
        if path.suffix == ".jsonl":
            counts[relative] = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        elif path.suffix == ".csv":
            counts[relative] = max(0, len(path.read_text(encoding="utf-8").splitlines()) - 1)
        else:
            counts[relative] = None
        if expected is not None and counts[relative] != expected:
            issues.append(f"{relative}: expected {expected} rows, found {counts[relative]}")
    observed["row_counts"] = counts

    bounds = json.loads(
        (PROJECT / "03_Reproducibility/Data/equivalence_bounds_v1/equivalence_bounds_v1.json").read_text(
            encoding="utf-8"
        )
    )
    headline = bounds["headline"]["Full - no_path"]
    observed["path_layer_max_upper_limit"] = headline["max_upper_limit_one_sided_95"]
    observed["path_layer_loo_max_upper_limit"] = headline["upper_limit_max_under_leave_one_out"]
    if not headline["max_upper_limit_one_sided_95"] <= 0.0047 + 1e-9:
        issues.append("path-layer upper limit exceeds the reported +0.0047")
    if not headline["upper_limit_max_under_leave_one_out"] <= 0.0059 + 1e-9:
        issues.append("path-layer leave-one-out upper limit exceeds the reported +0.0059")

    curve = json.loads(
        (
            PROJECT / "03_Reproducibility/Data/external_prospective_v1/external_arms_curve_v4.json"
        ).read_text(encoding="utf-8")
    )
    observed["curve_rows"] = len(curve["rows"])
    if curve["documents"] != 24 or len(curve["rows"]) != 1512:
        issues.append("budget-curve record does not cover 24 documents x 7 arms x 9 budgets")
    role_110 = next(
        c for c in curve["contrasts"] if c["contrast"] == "AB2 - AB0" and c["budget"] == "word:110"
    )
    observed["curve_role_layer_word110"] = role_110["mean"]
    if abs(role_110["mean"] + 0.035099) > 1e-5:
        issues.append("budget curve does not reproduce the v3 role-layer value at 110 words")

    supplement = (PROJECT / "01_Manuscript/Supplementary/supplementary_materials.tex").read_text(encoding="utf-8")
    observed["supplement_tables"] = sorted(re.findall(r"\\section\*\{Table (S\d+)\.", supplement))
    for label in ("S14", "S15", "S16", "S17"):
        if label not in observed["supplement_tables"]:
            issues.append(f"supplementary Table {label} missing")
    if "Figure S5." not in supplement:
        issues.append("supplementary Figure S5 missing")
    manuscript = (PROJECT / "01_Manuscript/LaTeX/paper_information.tex").read_text(encoding="utf-8")
    for token in ("+0.0047", "Figure~S5", "Tables~S1--S20"):
        if token not in manuscript:
            issues.append(f"main text does not carry the bound sentence token {token}")
    if "-0.0799" not in supplement:
        issues.append("supplement does not carry the family-split value behind the pooled mean")

    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def govreport_transfer_checks() -> dict[str, object]:
    """Verify the out-of-domain transfer layer (G2): protocol, counts and headline numbers."""
    base = PROJECT / "03_Reproducibility" / "Data" / "govreport_transfer_v1"
    record_path = base / "govreport_transfer_v1.json"
    bounds_path = base / "govreport_transfer_bounds_v1.json"
    full_bounds_path = base / "govreport_transfer_full970_bounds_v1.json"
    full_pairs_path = base / "govreport_transfer_full970_pairs.csv"
    energy_bounds_path = base / "govreport_energy160_bounds_v1.json"
    energy_pairs_path = base / "govreport_energy160_pairs.csv"
    protocol_path = base / "PROTOCOL_govreport_transfer_v1.md"
    script = PROJECT / "03_Reproducibility" / "Code" / "govreport_transfer_v1" / "run_govreport_transfer.py"
    issues: list[str] = []
    for path in (
        record_path,
        bounds_path,
        full_bounds_path,
        full_pairs_path,
        energy_bounds_path,
        energy_pairs_path,
        protocol_path,
        script,
    ):
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"missing artifact: {path.name}")
    if issues:
        return {"status": "FAIL", "observed": {}, "issues": issues}

    record = json.loads(record_path.read_text(encoding="utf-8"))
    bounds = json.loads(bounds_path.read_text(encoding="utf-8"))
    full_bounds = json.loads(full_bounds_path.read_text(encoding="utf-8"))
    energy_bounds = json.loads(energy_bounds_path.read_text(encoding="utf-8"))
    contrasts = {(c["contrast"], c["budget"]): c for c in record["contrasts"]}
    observed = {
        "documents": record["documents"],
        "rows": len(record["rows"]),
        "seed": record["seed"],
        "strata": record["strata"],
        "role_coverage_mean": record["diagnostics"]["role_coverage_mean"],
        "path_word110": {
            "mean": contrasts[("Full - no_path", "word:110")]["mean"],
            "negative": contrasts[("Full - no_path", "word:110")]["negative"],
            "positive": contrasts[("Full - no_path", "word:110")]["positive"],
            "zero": contrasts[("Full - no_path", "word:110")]["zero"],
        },
        "path_unit5": {
            "mean": contrasts[("Full - no_path", "unit:5")]["mean"],
            "holm": contrasts[("Full - no_path", "unit:5")]["holm"],
        },
        "role_word110": {"mean": contrasts[("AB2 - AB0", "word:110")]["mean"]},
        "max_path_upper_limit": bounds["headline"]["path layer"]["max_upper_limit_one_sided_95"],
        "full_documents": full_bounds["documents"],
        "full_shards": full_bounds["provenance"]["shards"],
        "full_max_path_upper_limit": full_bounds["headline"]["path layer"]["max_upper_limit_one_sided_95"],
        "full_pairs_rows": max(0, len(full_pairs_path.read_text(encoding="utf-8").splitlines()) - 1),
        "energy_documents": energy_bounds["provenance"]["documents"],
        "energy_max_path_upper_limit": energy_bounds["headline"]["path layer"]["max_upper_limit_one_sided_95"],
        "energy_pairs_rows": max(0, len(energy_pairs_path.read_text(encoding="utf-8").splitlines()) - 1),
    }
    checks = {
        "protocol_and_record_present": True,
        "sample_is_frozen_100": record["documents"] == 100 and record["seed"] == 20260926 and record["strata"] == 5,
        "row_count": len(record["rows"]) == 2800,
        "claim_class_declared": record["claim_class"].startswith("OUT_OF_DOMAIN_ROBUSTNESS_TRANSFER"),
        "path_layer_negative_at_110_words": abs(observed["path_word110"]["mean"] + 0.003050) < 5e-6
        and observed["path_word110"]["negative"] == 24
        and observed["path_word110"]["positive"] == 15
        and observed["path_word110"]["zero"] == 61,
        "path_layer_unit5_corrected": abs(observed["path_unit5"]["mean"] + 0.005155) < 5e-6
        and abs(observed["path_unit5"]["holm"] - 0.0017) < 5e-4,
        "path_layer_upper_limit_below_zero": observed["max_path_upper_limit"] < 0,
        "full_split_upper_limits_below_zero": observed["full_max_path_upper_limit"] < 0,
        "full_split_scale": observed["full_documents"] == 970
        and observed["full_shards"] == 12
        and observed["full_pairs_rows"] == 15520,
        "full_split_negative_holm": (
            min(
                c["holm"]
                for c in record["contrasts"]
                if c["contrast"] == "Full - no_path"
            )
            <= 0.005
        ),
        "energy_subset_within_margin": observed["energy_documents"] == 160
        and observed["energy_pairs_rows"] == 2560
        and observed["energy_max_path_upper_limit"] < 0.005,
        "energy_subset_negative_direction": all(
            r["mean"] <= 0
            for r in energy_bounds["records"]
            if r["label"] == "path layer"
        ),
        "role_layer_negative_at_110_words": abs(observed["role_word110"]["mean"] + 0.021237) < 5e-6,
        "no_raw_corpus_in_release": not any(
            "govreport_test_full" in p.name
            for scope in ("01_Manuscript", "02_Revision_and_QA", "03_Reproducibility")
            for p in (PROJECT / scope).rglob("*")
            if p.is_file()
        ),
    }
    for name, ok in checks.items():
        if not ok:
            issues.append(f"{name} failed")

    supplement = (PROJECT / "01_Manuscript/Supplementary/supplementary_materials.tex").read_text(encoding="utf-8")
    manuscript = (PROJECT / "01_Manuscript/LaTeX/paper_information.tex").read_text(encoding="utf-8")
    if "Table S18." not in supplement:
        issues.append("supplementary Table S18 missing")
    if "Table~S18" not in manuscript or "GovReport" not in manuscript:
        issues.append("main text does not carry the transfer pointer")
    if "L7 Out-of-domain transfer check" not in manuscript:
        issues.append("evidence-layer table has no L7 row")
    if "970 documents" not in manuscript:
        issues.append("main text does not carry the full-split confirmation clause")
    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def reference_type_checks() -> dict[str, object]:
    """Verify the reference-type sensitivity layer (human-written highlights)."""
    base = PROJECT / "03_Reproducibility" / "Data" / "reference_type_v1"
    bounds_path = base / "reference_type_400_bounds_v1.json"
    pairs_path = base / "reference_type_400_pairs.csv"
    protocol_path = base / "PROTOCOL_reference_type_v1.md"
    script = PROJECT / "03_Reproducibility" / "Code" / "reference_type_v1" / "run_reference_type.py"
    issues: list[str] = []
    for path in (bounds_path, pairs_path, protocol_path, script):
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"missing artifact: {path.name}")
    if issues:
        return {"status": "FAIL", "observed": {}, "issues": issues}

    bounds = json.loads(bounds_path.read_text(encoding="utf-8"))
    rows = [r for r in bounds["records"] if r["label"] == "path layer"]
    observed = {
        "documents": bounds["provenance"]["documents"],
        "pairs_rows": max(0, len(pairs_path.read_text(encoding="utf-8").splitlines()) - 1),
        "max_path_upper_limit": max(r["upper_limit_one_sided_95"] for r in rows),
        "min_zero_mass": min(r["zero"] / r["n"] for r in rows),
        "max_abs_path_mean": max(abs(r["mean"]) for r in rows),
    }
    checks = {
        "layer_scale": observed["documents"] == 400 and observed["pairs_rows"] == 6400,
        "path_bound_inside_margin": observed["max_path_upper_limit"] < 0.005,
        "path_term_inert_under_extractive_reference": observed["min_zero_mass"] >= 0.90
        and observed["max_abs_path_mean"] <= 0.001,
    }
    for name, ok in checks.items():
        if not ok:
            issues.append(f"{name} failed")

    supplement = (PROJECT / "01_Manuscript/Supplementary/supplementary_materials.tex").read_text(encoding="utf-8")
    manuscript = (PROJECT / "01_Manuscript/LaTeX/paper_information.tex").read_text(encoding="utf-8")
    if "Table S19." not in supplement:
        issues.append("supplementary Table S19 missing")
    if "Table~S19" not in manuscript:
        issues.append("main text does not cite Table S19")
    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def gendata_synthetic_checks() -> dict[str, object]:
    """Verify the frozen parent/held-out synthetic fixtures of the upgraded L5 layer."""
    root = PROJECT / "03_Reproducibility" / "Data" / "synthetic_stress_v1"
    runs = {
        "parent": root / "run_20260927_gendata_parent_v3r1",
        "heldout": root / "run_20260927_gendata_heldout_v2r3",
    }
    issues: list[str] = []
    observed: dict[str, object] = {}
    for label, run in runs.items():
        for name in ("synthetic_reports.jsonl", "SYNTHETIC_RUN_MANIFEST.json", "semantic_cores.json"):
            if not (run / name).is_file():
                issues.append(f"missing {label} artifact: {name}")
        if issues:
            continue
        rows = [json.loads(line) for line in (run / "synthetic_reports.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        ledger = json.loads((run / "evaluation/gate_ledger.json").read_text(encoding="utf-8"))
        inference = json.loads((run / "e3_factorial_pilot/factorial_inference.json").read_text(encoding="utf-8"))
        observed[label] = {
            "reports": len(rows),
            "all_gates_pass": ledger.get("all_gates_pass"),
            "gates_passed": sum(1 for gate in ledger["gates"] if gate["pass"]),
            "path_main_holm": sorted(
                item["holm_adjusted_p"]
                for item in inference["reservation_path_factorial"]
                if item["contrast"] == "path_main"
            ),
        }
        if len(rows) != 8:
            issues.append(f"{label}: expected 8 reports, found {len(rows)}")
        if any(row.get("split") != "synthetic_stress" or row.get("synthetic") is not True or row.get("confirmatory_claims_allowed") is not False for row in rows):
            issues.append(f"{label}: claim-boundary markers missing")
        if ledger.get("all_gates_pass") is not True or observed[label]["gates_passed"] != 19:
            issues.append(f"{label}: gate ledger is not 19/19")
    if observed.get("parent") and observed.get("heldout"):
        if not all(holm == 1.0 for holm in observed["heldout"]["path_main_holm"]):
            issues.append("held-out path contrast should be Holm 1.0")
        if observed["parent"]["path_main_holm"] != observed["heldout"]["path_main_holm"]:
            pass
    protocol = root / "PROTOCOL_synthetic_c2ges_gendata_v1.md"
    card = root / "DATASET_CARD.md"
    readme = root / "README.md"
    freeze = root / "FREEZE_RECORD.json"
    for path in (protocol, card, readme, freeze):
        if not path.is_file():
            issues.append(f"missing provenance artifact: {path.name}")
    manuscript = (PROJECT / "01_Manuscript/LaTeX/paper_information.tex").read_text(encoding="utf-8")
    supplement = (PROJECT / "01_Manuscript/Supplementary/supplementary_materials.tex").read_text(encoding="utf-8")
    if "Supplementary Table~S20" not in manuscript:
        issues.append("main text does not cite Table S20")
    if "Table S20." not in supplement:
        issues.append("supplement does not carry Table S20")
    return {"status": "PASS" if not issues else "FAIL", "observed": observed, "issues": issues}


def external_gates(route: str = "confirmatory") -> dict[str, str]:
    gates = {
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
    if route == "diagnostic":
        gates.update({
            "independent_power_system_expert_annotation": "NOT_APPLICABLE_NO_HUMAN_VALIDATION_CLAIM",
            "untouched_external_series_evaluation": "NOT_APPLICABLE_POST_ACCESS_DIAGNOSTIC_ROUTE",
            "controlled_component_factorial": "COMPLETE_EXPLORATORY_DIAGNOSTIC",
        })
    return gates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-latex", action="store_true", help="run only code and data checks")
    parser.add_argument("--submission", action="store_true", help="fail unless all author/external gates are closed")
    parser.add_argument("--route", choices=("confirmatory", "diagnostic"), default="confirmatory", help="scientific claim route evaluated by the gate")
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
            run_latex_in_temporary_copy("main_latex", MANUSCRIPT / "LaTeX", "paper_information", True),
            run_latex_in_temporary_copy("supplement_latex", MANUSCRIPT / "Supplementary", "supplementary_materials", False),
        ])

    data = data_checks()
    manuscript = manuscript_checks()
    figures = figure_lineage_checks()
    revision = revision_evidence_checks()
    construct = construct_audit_checks()
    external = external_prospective_checks()
    transfer = govreport_transfer_checks()
    reference_type = reference_type_checks()
    gendata_synthetic = gendata_synthetic_checks()
    boundary = release_boundary_and_addenda_checks()
    diagnostic = diagnostic_evidence_checks() if args.route == "diagnostic" else {"status": "NOT_APPLICABLE"}
    failures = [item["label"] for item in checks if item["returncode"] != 0]
    if data["status"] != "PASS":
        failures.append("data_checks")
    if manuscript["status"] != "PASS":
        failures.append("manuscript_checks")
    if figures["status"] != "PASS":
        failures.append("figure_lineage_checks")
    if revision["status"] != "PASS":
        failures.append("revision_evidence_checks")
    if construct["status"] != "PASS":
        failures.append("construct_audit_checks")
    if external["status"] != "PASS":
        failures.append("external_prospective_checks")
    if transfer["status"] != "PASS":
        failures.append("govreport_transfer_checks")
    if reference_type["status"] != "PASS":
        failures.append("reference_type_checks")
    if gendata_synthetic["status"] != "PASS":
        failures.append("gendata_synthetic_checks")
    if boundary["status"] != "PASS":
        failures.append("release_boundary_and_addenda_checks")
    if args.route == "diagnostic" and diagnostic["status"] != "PASS":
        failures.append("diagnostic_evidence_checks")
    versions = {}
    for package in ("networkx", "numpy", "psutil", "rouge-score", "sentence-transformers", "torch", "transformers"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None

    gates = external_gates(args.route)
    pending = [key for key, value in gates.items() if value == "PENDING"]
    report = {
        "schema": "C2GES-public-verification-v3",
        "submission_route": args.route,
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
        "revision_evidence": revision,
        "construct_audit": construct,
        "external_prospective": external,
        "govreport_transfer": transfer,
        "reference_type": reference_type,
        "gendata_synthetic": gendata_synthetic,
        "release_boundary": boundary,
        "diagnostic_evidence": diagnostic,
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
