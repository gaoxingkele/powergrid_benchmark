#!/usr/bin/env python3
"""Read-only technical verification for the reorganized MA-SQLGrid package.

The default check is portable and does not require the restricted GridDB SQLite
snapshot.  ``--submission`` additionally enforces author/external release gates.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


METADATA = Path(__file__).resolve().parent
REPRO = METADATA.parent
PROJECT = REPRO.parent
CODE = REPRO / "Code"
DATA = REPRO / "Data"
MANUSCRIPT = PROJECT / "01_Manuscript" / "LaTeX"
DEFAULT_REPORT = PROJECT / "02_Revision_and_QA" / "04_Build_Reports" / "MA_SQLGRID_PUBLIC_VERIFICATION.json"


def require(path: Path) -> Path:
    if not path.is_file():
        raise AssertionError(f"missing required file: {path.relative_to(PROJECT)}")
    return path


def read_json(path: Path) -> dict:
    return json.loads(require(path).read_text(encoding="utf-8"))


def jsonl_count(path: Path) -> int:
    with require(path).open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def csv_rows(path: Path) -> list[dict[str, str]]:
    with require(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_manuscript() -> dict[str, int]:
    tex_path = require(MANUSCRIPT / "paper_applsci.tex")
    tex = tex_path.read_text(encoding="utf-8")
    bib_path = require(MANUSCRIPT / "references_verified.bib")
    bib = bib_path.read_text(encoding="utf-8")

    for token in ("76/180", "99/180", "100/180", "129/180", "40{,}320"):
        if token not in tex:
            raise AssertionError(f"manuscript is missing current result token: {token}")
    for obsolete in ("80/180 for C000", "101/180", "80/180 & 0.4444"):
        if obsolete in tex:
            raise AssertionError(f"obsolete historical-evaluator claim remains: {obsolete}")
    if re.search(r"citation\s+TODO|TODO\s+citation|\\cite\{TODO", tex, re.IGNORECASE):
        raise AssertionError("unresolved citation TODO remains in manuscript")
    for token in (
        "Bijing Liu",
        "Chenglong Sun",
        "Yong Yang",
        "yangyong1@sgepri.sgcc.com.cn",
        "cmc-2026-08-24-v2",
        "All authors have read and agreed",
        "ORCID: none declared",
    ):
        if token not in tex:
            raise AssertionError(f"manuscript is missing submission metadata token: {token}")
    for placeholder in ("email to be provided", "author-email-required@example.com", "[AUTHOR INPUT REQUIRED]"):
        if placeholder in tex:
            raise AssertionError(f"unresolved submission placeholder remains: {placeholder}")
    if "\\orcidauthor" in tex or "\\orcidA" in tex:
        raise AssertionError("ORCID command must be omitted when all authors declared NONE")
    abstract_match = re.search(r"\\abstract\{(.*?)\}\s*\\keyword", tex, flags=re.DOTALL)
    if abstract_match is None:
        raise AssertionError("abstract block not found")
    abstract_words = re.findall(
        r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",
        abstract_match.group(1).replace("\\masql{}", "MA-SQLGrid"),
    )
    if len(abstract_words) > 200:
        raise AssertionError(f"abstract exceeds 200 words: {len(abstract_words)}")

    cited: set[str] = set()
    for group in re.findall(r"\\cite\w*\{([^}]+)\}", tex):
        cited.update(key.strip() for key in group.split(",") if key.strip())
    available = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib))
    missing = sorted(cited - available)
    if missing:
        raise AssertionError(f"bibliography keys missing: {', '.join(missing)}")

    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex)
    for figure in figures:
        require(MANUSCRIPT / figure)
    return {
        "citation_keys": len(cited),
        "figures": len(figures),
        "tables": len(re.findall(r"\\begin\{table\*?\}", tex)),
        "abstract_words": len(abstract_words),
    }


def verify_data() -> dict[str, int]:
    canonical_n = jsonl_count(DATA / "canonical_v2" / "canonical_rows_v2.jsonl")
    atomic_n = jsonl_count(DATA / "constructed_state" / "atomic_scores.jsonl")
    historical_n = jsonl_count(DATA / "historical_pool" / "run_v3a" / "evaluation_ledger.jsonl")
    if (canonical_n, atomic_n, historical_n) != (1440, 25920, 540):
        raise AssertionError(
            f"core row-count mismatch: canonical={canonical_n}, atomic={atomic_n}, historical={historical_n}"
        )

    unified = read_json(DATA / "evaluator_audit" / "run_unified_v1b" / "unified_evaluator_results.json")
    unified_counts = {row["method"]: row["correct"] for row in unified["summary"]}
    expected = {
        "C000_fixed_order_equal_budget": 76,
        "validation_rank_equal_budget_no_cf": 99,
        "full_coordination_complete_metamorphic": 100,
        "qwen:F01_Full_WithShape": 129,
    }
    for method, correct in expected.items():
        if unified_counts.get(method) != correct:
            raise AssertionError(f"unified evaluator mismatch for {method}")
    if unified["evaluator"]["questions"] != 180 or unified["evaluator"]["executions"] != 1620:
        raise AssertionError("unified evaluator denominator mismatch")

    order = read_json(
        DATA / "evaluator_audit" / "order_sensitivity_unified_v1" / "order_sensitivity_summary.json"
    )
    for method in ("validation_only", "complete_witness"):
        record = order["methods"][method]
        if record["permutations"] != 40320 or (record["minimum_correct"], record["maximum_correct"]) != (95, 128):
            raise AssertionError(f"order-sensitivity mismatch for {method}")
    unique = order["normalized_unique_sql"]
    if unique["questions_with_any_duplicate_slot"] != 154:
        raise AssertionError("normalized unique-SQL duplicate count mismatch")
    if set(order["descriptive_tie_size_aurc"]) != {"definition", "validation_only", "complete_witness"}:
        raise AssertionError("descriptive tie-size AURC is incomplete")
    if len(csv_rows(DATA / "evaluator_audit" / "order_sensitivity_unified_v1" / "per_question_unique_sql.csv")) != 180:
        raise AssertionError("unique-SQL item ledger must contain 180 rows")

    role = read_json(DATA / "role_ablation" / "unified_v1" / "role_ablation_summary.json")
    role_expected = {
        "validation_original": 99,
        "validation_no_query_features": 76,
        "validation_no_order": 77,
        "complete_original": 100,
        "complete_no_constructed_state": 99,
        "complete_no_schema_grounding": 100,
    }
    for key, value in role_expected.items():
        if role["correct_counts"].get(key) != value:
            raise AssertionError(f"role-ablation mismatch for {key}")
    if role["cost"]["model_calls_in_historical_selector_study"] != 0:
        raise AssertionError("historical selector unexpectedly reports model calls")

    taxonomy = read_json(DATA / "error_taxonomy" / "unified_v1" / "error_taxonomy_summary.json")
    if taxonomy["expert_semantic_adjudication"] is not False:
        raise AssertionError("automated taxonomy must not claim expert adjudication")
    if (taxonomy["bounded_executions"], taxonomy["method_item_rows"]) != (1620, 1980):
        raise AssertionError("error-taxonomy denominator mismatch")
    taxonomy_rows = {row["method"]: row for row in csv_rows(
        DATA / "error_taxonomy" / "unified_v1" / "method_error_counts.csv"
    )}
    if int(taxonomy_rows["C000_fixed_order_equal_budget"]["correct"]) != 76:
        raise AssertionError("C000 taxonomy total mismatch")

    bird = csv_rows(DATA / "BIRD_aggregates" / "method_summary.csv")
    if len(bird) != 8 or any(int(row["n"]) != 500 for row in bird):
        raise AssertionError("BIRD aggregate denominator mismatch")

    restricted = list(PROJECT.rglob("database.sqlite")) + list(PROJECT.rglob("questions.jsonl"))
    if restricted:
        raise AssertionError("raw restricted GridDB assets unexpectedly included")
    return {
        "canonical_rows": canonical_n,
        "constructed_state_atomic_rows": atomic_n,
        "historical_pool_evaluation_rows": historical_n,
        "unified_executions": unified["evaluator"]["executions"],
        "order_permutations_per_selector": 40320,
        "taxonomy_method_item_rows": taxonomy["method_item_rows"],
        "bird_method_cells": len(bird),
    }


def run_unit_tests() -> dict[str, str]:
    suites = {
        "framework": (
            CODE / "framework",
            [
                sys.executable,
                "-m",
                "unittest",
                "tests/test_ma_sqlgrid_agents.py",
                "tests/test_sqlite_readonly_executor.py",
                "tests/test_replay_diagnostic.py",
            ],
        ),
        "final_executor": (
            CODE / "final_executor",
            [sys.executable, "-m", "unittest", "test_sqlite_readonly_executor_final.py"],
        ),
    }
    outcomes: dict[str, str] = {}
    for name, (cwd, command) in suites.items():
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(f"{name} unit tests failed:\n{result.stdout}\n{result.stderr}")
        match = re.search(r"Ran (\d+) tests?", result.stderr)
        outcomes[name] = f"PASS ({match.group(1) if match else 'unknown'} tests)"
    return outcomes


def compile_latex() -> dict[str, int | str]:
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if not pdflatex or not bibtex:
        raise AssertionError("pdflatex and bibtex are required for the portable build check")
    with tempfile.TemporaryDirectory(prefix="ma_sqlgrid_verify_") as tmp:
        build = Path(tmp) / "LaTeX"
        def ignore_source_build(directory: str, names: list[str]) -> set[str]:
            if Path(directory).resolve() != MANUSCRIPT.resolve():
                return set()
            return {
                name
                for name in names
                if name in {
                    "paper_applsci.aux",
                    "paper_applsci.bbl",
                    "paper_applsci.blg",
                    "paper_applsci.log",
                    "paper_applsci.out",
                    "paper_applsci.pdf",
                }
            }

        shutil.copytree(MANUSCRIPT, build, ignore=ignore_source_build)
        commands = [
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "paper_applsci.tex"],
            [bibtex, "paper_applsci"],
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "paper_applsci.tex"],
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "paper_applsci.tex"],
        ]
        for command in commands:
            result = subprocess.run(command, cwd=build, capture_output=True, text=True)
            if result.returncode:
                tail = "\n".join((result.stdout + "\n" + result.stderr).splitlines()[-60:])
                raise AssertionError(f"LaTeX build failed ({Path(command[0]).name}):\n{tail}")
        log = (build / "paper_applsci.log").read_text(encoding="utf-8", errors="replace")
        if "undefined references" in log.lower() or "undefined citations" in log.lower():
            raise AssertionError("LaTeX build contains undefined references or citations")
        pdf = require(build / "paper_applsci.pdf")
        pages_match = re.search(r"Output written on .*\((\d+) pages?", log)
        return {"status": "PASS", "pages": int(pages_match.group(1)) if pages_match else -1, "bytes": pdf.stat().st_size}


def external_gates() -> dict[str, str]:
    gates = {
        "author_metadata": "PROVIDED_0823_BASELINE_USER_DIRECTED_2026_08_24",
        "author_orcid": "NONE_DECLARED_ALL_AUTHORS",
        "corresponding_author_email": "PROVIDED_0823_SOURCE",
        "author_declarations": "PROVIDED_BY_PRIOR_AUTHOR_DEFAULT_AND_2026_08_24_DIRECTION",
        "author_code_license": "ALL_RIGHTS_RESERVED_NO_EXPLICIT_LICENSE",
        "rights_safe_public_release": "AUTHORIZED_GITHUB_SCOPE",
        "journal_portal_author_attestation": "MANUAL_AT_SUBMISSION_NOT_PACKAGE_GATE",
        "restricted_asset_release_permission": "NOT_REQUIRED_EXCLUDED_FROM_PUBLIC_RELEASE",
        "independent_power_system_and_database_expert_review": "CLAIM_UPGRADE_ONLY_ROUTE_B_C",
        "untouched_external_grid_evaluation": "CLAIM_UPGRADE_ONLY_ROUTE_B_C",
    }
    return gates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-latex", action="store_true", help="skip the temporary LaTeX build")
    parser.add_argument("--submission", action="store_true", help="fail unless every author/external gate is closed")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    result: dict[str, object] = {
        "schema_version": "ma-sqlgrid-portable-package-check-v2",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "manuscript": verify_manuscript(),
        "data": verify_data(),
        "unit_tests": run_unit_tests(),
        "latex": {"status": "SKIPPED"} if args.skip_latex else compile_latex(),
        "external_gates": external_gates(),
    }
    pending = [key for key, value in result["external_gates"].items() if value == "PENDING"]
    result["technical_status"] = "PASS"
    result["submission_ready"] = not pending
    result["status"] = "PASS" if not args.submission or not pending else "PENDING_EXTERNAL_GATES"
    report_path = args.report if args.report.is_absolute() else Path.cwd() / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "report": str(report_path), "submission_ready": result["submission_ready"]}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
