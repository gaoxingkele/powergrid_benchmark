"""Build six clean, independently verifiable Mintou submission bundles.

The current ``manuscript/journal_submission/paper.tex`` file is the canonical
source.  The legacy Markdown-to-LaTeX preview builder is intentionally not
invoked because its ``MANUSCRIPT.md`` inputs can lag the accepted narrative
revision.  Each PDF is compiled from the canonical TeX in an isolated temporary
directory, then packaged with figures, tables, experiment material, evidence,
code, review provenance, and per-file SHA-256 checksums.

This script verifies packaging and reproducibility material.  It does not fill
author-controlled metadata and does not convert a scientific evidence-contract
check into an acceptance guarantee.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import fitz


ROOT = Path(__file__).resolve().parents[2]
PROJECTS_ROOT = ROOT / "paper_projects"
COMPANIONS_ROOT = ROOT / "papers" / "mintou"
DEFAULT_OUT = ROOT / "deliverables" / "mintou_2026-08-25_latest_verified_packages"
REFERENCE_AUDIT = (
    ROOT
    / "reviews"
    / "mintou_2026-08-09_journal_fit_audit"
    / "reference_verification_summary.json"
)


@dataclass(frozen=True)
class PaperSpec:
    paper_id: str
    project: str
    target_journal: str
    documentclass_token: str


PAPERS = (
    PaperSpec("mintou_p1", "mintou_p1_dstar_gru_dispatch", "IEEE Access", "ieeeaccess"),
    PaperSpec("mintou_p2", "mintou_p2_hygraph_load_forecasting", "Electronics", "electronics"),
    PaperSpec("mintou_p3", "mintou_p3_samode_distribution_planning", "Energies", "energies"),
    PaperSpec("mintou_p4", "mintou_p4_shield_resilience_planning", "Energies", "energies"),
    PaperSpec("mintou_p5", "mintou_p5_trace_moea_feasibility_review", "Energies", "energies"),
    PaperSpec("mintou_p6", "mintou_p6_bilonsga_project_review", "Applied Sciences", "applsci"),
)

BUILD_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
    ".bbl",
    ".blg",
    ".lof",
    ".lot",
}
IGNORED_DIRS = {
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "worktrees",
}
IGNORED_NAMES = {
    "paper.pdf",
    "paper_narrative_revision.pdf",
    "body.generated.md",
    "body.generated.tex",
}
FIGURE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg", ".tif", ".tiff"}
TABLE_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls", ".tex", ".json"}
CODE_EXTENSIONS = {".py", ".ps1", ".sh", ".ipynb", ".toml", ".yaml", ".yml"}

COMMON_AUDIT_FILES = (
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round1_logic_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round1_statistics_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round1_theory_innovation_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round2_logic_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round2_statistics_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round2_theory_innovation_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round3_logic_final_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round3_statistics_final_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "round3_theory_innovation_final_p1_p6.md",
    ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds" / "FINAL_THREE_ROUND_CLOSURE_ZH.md",
    ROOT
    / "reviews"
    / "mintou_2026-08-10_comprehensive_latest_vs_10"
    / "COMPREHENSIVE_SIX_PAPER_VS_10_REPORT_ZH.md",
    ROOT
    / "reviews"
    / "mintou_2026-08-10_comprehensive_latest_vs_10"
    / "paper_vs_10_average.csv",
    REFERENCE_AUDIT,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def normalized_archive_name(value: str) -> str:
    name = value.replace("\\", "/").lstrip("/")
    if not name or name.startswith("../") or "/../" in name:
        raise ValueError(f"unsafe archive name: {value}")
    return name


def excluded_file(path: Path) -> bool:
    lower = path.name.lower()
    if lower in IGNORED_NAMES or lower.endswith(".zip"):
        return True
    return any(lower.endswith(suffix) for suffix in BUILD_SUFFIXES)


def iter_tree_files(root: Path, excluded_prefixes: Iterable[Path] = ()) -> Iterable[Path]:
    if not root.is_dir():
        return
    blocked = {prefix.resolve() for prefix in excluded_prefixes}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if name not in IGNORED_DIRS
            and not (current_path / name).is_symlink()
            and (current_path / name).resolve() not in blocked
        ]
        for name in sorted(files):
            source = current_path / name
            if source.is_symlink() or excluded_file(source):
                continue
            yield source


def load_portfolio_manifest() -> dict[str, dict[str, str]]:
    path = COMPANIONS_ROOT / "manifest.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["directory"]: row for row in csv.DictReader(handle)}


def extract_title(tex: str) -> str:
    match = re.search(r"\\(?:Title|title)\{([^\n]+?)\}", tex)
    if not match:
        raise ValueError("LaTeX title macro not found")
    return re.sub(r"\s+", " ", match.group(1)).strip()


def extract_abstract(tex: str) -> str:
    match = re.search(r"\\abstract\{(.*?)\}\s*\\keyword", tex, flags=re.DOTALL)
    if not match:
        match = re.search(
            r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, flags=re.DOTALL
        )
    if not match:
        raise ValueError("LaTeX abstract not found")
    return match.group(1)


def latex_plain_text(value: str) -> str:
    previous = None
    text = value
    while previous != text:
        previous = text
        text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[A-Za-z]+", " ", text)
    text = re.sub(r"[$~^{}]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def word_count(value: str) -> int:
    return len(re.findall(r"\b[\w][\w'’\-]*\b", latex_plain_text(value), flags=re.UNICODE))


def normalize_for_match(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).casefold()
    return "".join(char for char in normalized if char.isalnum())


def title_present_in_pdf(title: str, page_text: str) -> bool:
    title_normalized = normalize_for_match(latex_plain_text(title))
    page_normalized = normalize_for_match(page_text)
    if title_normalized and title_normalized in page_normalized:
        return True
    title_tokens = {
        token.casefold()
        for token in re.findall(r"[A-Za-z0-9]+", latex_plain_text(title))
        if len(token) >= 4
    }
    page_tokens = {token.casefold() for token in re.findall(r"[A-Za-z0-9]+", page_text)}
    return bool(title_tokens) and len(title_tokens & page_tokens) / len(title_tokens) >= 0.85


def resolve_graphics(latex_root: Path, tex: str) -> tuple[list[str], list[str]]:
    requested = re.findall(
        r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex, flags=re.MULTILINE
    )
    resolved: list[str] = []
    missing: list[str] = []
    for raw in requested:
        relative = Path(raw)
        candidates = [latex_root / relative]
        if not relative.suffix:
            candidates.extend(latex_root / f"{raw}{extension}" for extension in FIGURE_EXTENSIONS)
        found = next((candidate for candidate in candidates if candidate.is_file()), None)
        if found:
            resolved.append(found.relative_to(latex_root).as_posix())
        else:
            missing.append(raw)
    return sorted(set(resolved)), sorted(set(missing))


def tex_static_checks(spec: PaperSpec, tex_path: Path, manifest_row: dict[str, str]) -> dict[str, object]:
    tex = tex_path.read_text(encoding="utf-8")
    title = extract_title(tex)
    abstract_words = word_count(extract_abstract(tex))
    documentclass_line = next(
        (line.strip() for line in tex.splitlines() if line.strip().startswith("\\documentclass")),
        "",
    )
    graphics, missing_graphics = resolve_graphics(tex_path.parent, tex)
    labels = set(re.findall(r"\\label\{([^}]+)\}", tex))
    referenced_labels = set(
        re.findall(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}", tex)
    )
    bibitems = set(re.findall(r"\\bibitem\{([^}]+)\}", tex))
    citation_keys: set[str] = set()
    for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        citation_keys.update(key.strip() for key in group.split(",") if key.strip())
    author_gates = [
        {"line": index, "text": line.strip()}
        for index, line in enumerate(tex.splitlines(), start=1)
        if re.search(r"AUTHOR INPUT REQUIRED", line, flags=re.IGNORECASE)
    ]
    template_gates = []
    if "10.1109/ACCESS.XXXX.XXXXXXX" in tex:
        template_gates.append("IEEE Access DOI placeholder remains for publisher assignment")
    malformed_dois = [
        line.strip()
        for line in tex.splitlines()
        if re.search(r"\\url\{https://doi\.org/[^\n]*\}\)", line)
    ]
    raw_numeric_citations = re.findall(
        r"\{\[\}\d+(?:(?:\s*,\s*|\s*--\s*)\d+)*\{\]\}", tex
    )
    title_match = manifest_row.get("title", "").strip() == title
    journal_match = manifest_row.get("target_journal", "").strip() == spec.target_journal
    class_match = spec.documentclass_token.casefold() in documentclass_line.casefold()
    advisories: list[str] = []
    if spec.target_journal in {"Electronics", "Energies", "Applied Sciences"} and abstract_words > 200:
        advisories.append(
            f"Abstract is {abstract_words} words; MDPI profile recommends about 200 words."
        )
    if spec.target_journal == "IEEE Access" and not 150 <= abstract_words <= 250:
        advisories.append(
            f"Abstract is {abstract_words} words; re-check the live IEEE Access author guidance."
        )
    if bibitems - citation_keys:
        advisories.append(f"{len(bibitems - citation_keys)} bibliography entries are not cited in the TeX body.")

    hard_failures = []
    if not class_match:
        hard_failures.append(
            f"document class does not match {spec.target_journal}: {documentclass_line}"
        )
    if not title_match:
        hard_failures.append("portfolio manifest title differs from canonical TeX title")
    if not journal_match:
        hard_failures.append("portfolio manifest target journal differs from package specification")
    if missing_graphics:
        hard_failures.append("unresolved graphics: " + ", ".join(missing_graphics))
    if referenced_labels - labels:
        hard_failures.append(
            "unresolved LaTeX references: " + ", ".join(sorted(referenced_labels - labels))
        )
    if citation_keys - bibitems:
        hard_failures.append(
            "citation keys missing from bibliography: " + ", ".join(sorted(citation_keys - bibitems))
        )
    if malformed_dois:
        hard_failures.append("malformed DOI URL syntax remains")
    if raw_numeric_citations:
        hard_failures.append(
            f"{len(raw_numeric_citations)} static numeric citations remain instead of LaTeX citation commands"
        )

    return {
        "title": title,
        "target_journal": spec.target_journal,
        "documentclass": documentclass_line,
        "documentclass_match": class_match,
        "manifest_title_match": title_match,
        "manifest_journal_match": journal_match,
        "abstract_words": abstract_words,
        "graphics_inclusions": len(re.findall(r"\\includegraphics", tex)),
        "resolved_graphics": graphics,
        "missing_graphics": missing_graphics,
        "labels": len(labels),
        "referenced_labels": len(referenced_labels),
        "missing_labels": sorted(referenced_labels - labels),
        "bibliography_entries": len(bibitems),
        "citation_keys": len(citation_keys),
        "missing_bibliography_keys": sorted(citation_keys - bibitems),
        "uncited_bibliography_keys": sorted(bibitems - citation_keys),
        "author_input_gates": author_gates,
        "template_gates": template_gates,
        "malformed_dois": malformed_dois,
        "raw_numeric_citations": raw_numeric_citations,
        "advisories": advisories,
        "hard_failures": hard_failures,
    }


def run_command(command: list[str], cwd: Path, timeout: int = 300) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def compile_pdf(spec: PaperSpec, latex_root: Path, title: str, temp_root: Path) -> tuple[Path, dict[str, object]]:
    build_root = temp_root / spec.project
    shutil.copytree(
        latex_root,
        build_root,
        ignore=shutil.ignore_patterns(
            "paper.pdf",
            "paper_narrative_revision.pdf",
            "body.generated.md",
            "body.generated.tex",
            "*.aux",
            "*.log",
            "*.out",
            "*.toc",
            "*.fls",
            "*.fdb_latexmk",
            "*.synctex.gz",
        ),
    )
    engine = shutil.which("pdflatex")
    if not engine:
        raise RuntimeError("pdflatex was not found on PATH")
    runs = []
    for _ in range(2):
        result = run_command(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "paper.tex"],
            build_root,
        )
        runs.append(result)
        if result["returncode"] != 0:
            tail = (str(result["stdout"]) + str(result["stderr"]))[-8000:]
            raise RuntimeError(f"{spec.project} isolated LaTeX build failed:\n{tail}")
    pdf_path = build_root / "paper.pdf"
    log_path = build_root / "paper.log"
    if not pdf_path.is_file() or not log_path.is_file():
        raise RuntimeError(f"{spec.project} did not produce paper.pdf and paper.log")
    log = log_path.read_text(encoding="utf-8", errors="replace")
    blocking_warnings = []
    for pattern, label in (
        (r"There were undefined references", "undefined references"),
        (r"Citation [`'][^\n]+ undefined", "undefined citation"),
        (r"Reference [`'][^\n]+ undefined", "undefined reference"),
        (r"LaTeX Error: File [`'][^\n]+ not found", "missing LaTeX input"),
    ):
        if re.search(pattern, log, flags=re.IGNORECASE):
            blocking_warnings.append(label)
    if blocking_warnings:
        raise RuntimeError(
            f"{spec.project} LaTeX log contains blocking warnings: "
            + ", ".join(sorted(set(blocking_warnings)))
        )
    with fitz.open(pdf_path) as document:
        pages = document.page_count
        first_page = document.load_page(0).get_text("text") if pages else ""
    if pages < 1:
        raise RuntimeError(f"{spec.project} compiled PDF has no pages")
    if not title_present_in_pdf(title, first_page):
        raise RuntimeError(f"{spec.project} compiled PDF first page does not match TeX title")
    report = {
        "engine": engine,
        "runs": len(runs),
        "returncodes": [run["returncode"] for run in runs],
        "pages": pages,
        "pdf_bytes": pdf_path.stat().st_size,
        "pdf_sha256": sha256_file(pdf_path),
        "title_match": True,
        "undefined_reference_or_citation_warnings": 0,
        "overfull_hbox_warnings": len(re.findall(r"Overfull \\hbox", log)),
        "underfull_hbox_warnings": len(re.findall(r"Underfull \\hbox", log)),
    }
    return pdf_path, report


def run_scientific_contract(project: str) -> dict[str, object]:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "mintou" / "harness_scientific_acceptance.py"),
        "--project",
        project,
        "--phase",
        "narrative",
    ]
    result = run_command(command, ROOT)
    if result["returncode"] != 0:
        raise RuntimeError(
            f"{project} scientific evidence contract failed:\n"
            + (str(result["stdout"]) + str(result["stderr"]))[-8000:]
        )
    return {
        "status": "PASS",
        "scope": "claim-to-evidence narrative contract; not an acceptance guarantee",
        "command": " ".join(command),
        "output": str(result["stdout"]).strip(),
    }


def run_shared_regression_tests() -> dict[str, object]:
    pytest = shutil.which("pytest")
    if not pytest:
        raise RuntimeError("pytest executable was not found on PATH")
    command = [
        pytest,
        "-q",
        "-p",
        "no:cacheprovider",
        "tests/test_mintou_experiments.py",
    ]
    result = run_command(command, ROOT)
    if result["returncode"] != 0:
        raise RuntimeError(
            "shared Mintou regression tests failed:\n"
            + (str(result["stdout"]) + str(result["stderr"]))[-8000:]
        )
    return {
        "status": "PASS",
        "command": " ".join(command),
        "output": str(result["stdout"]).strip(),
    }


def verify_material_roots(spec: PaperSpec) -> dict[str, object]:
    project = PROJECTS_ROOT / spec.project
    companion = COMPANIONS_ROOT / spec.project
    required_dirs = {
        "latex": project / "manuscript" / "journal_submission",
        "source_figures": project / "manuscript" / "figures",
        "derived_tables": project / "manuscript" / "derived_tables",
        "evidence_runs": companion / "evidence" / "runs",
        "evidence_tables": companion / "evidence" / "tables",
        "evidence_source": companion / "evidence" / "source",
        "experiment_configs": companion / "src" / "configs",
    }
    counts = {}
    failures = []
    for name, path in required_dirs.items():
        count = sum(1 for item in iter_tree_files(path)) if path.is_dir() else 0
        counts[name] = {"path": path.relative_to(ROOT).as_posix(), "files": count}
        if count == 0:
            failures.append(f"required material directory is missing or empty: {path}")
    project_experiments = project / "experiments"
    counts["project_experiments"] = {
        "path": project_experiments.relative_to(ROOT).as_posix(),
        "files": sum(1 for item in iter_tree_files(project_experiments))
        if project_experiments.is_dir()
        else 0,
        "note": "P3 legitimately stores executed material in the evidence tree rather than this optional directory.",
    }
    if failures:
        raise RuntimeError("\n".join(failures))
    return {"status": "PASS", "roots": counts}


def collect_source_files(spec: PaperSpec) -> list[tuple[Path, str]]:
    project = PROJECTS_ROOT / spec.project
    companion = COMPANIONS_ROOT / spec.project
    latex_root = project / "manuscript" / "journal_submission"
    pairs: list[tuple[Path, str]] = []

    def add_tree(source_root: Path, archive_root: str, excluded_prefixes: Iterable[Path] = ()) -> None:
        for source in iter_tree_files(source_root, excluded_prefixes):
            relative = source.relative_to(source_root).as_posix()
            pairs.append((source, f"{archive_root}/{relative}"))

    add_tree(latex_root, "01_manuscript/latex")
    add_tree(project / "manuscript" / "figures", "02_figures_tables/source_figures")
    add_tree(project / "manuscript" / "derived_tables", "02_figures_tables/derived_tables")
    add_tree(project / "experiments", "03_experiments/project_experiments")
    add_tree(companion / "evidence", "04_evidence_data/evidence")
    add_tree(companion / "src", "05_code/paper_scaffold")

    shared_source = ROOT / "src" / "powergrid_benchmark"
    for source in sorted(shared_source.glob("mintou*.py")):
        pairs.append((source, f"05_code/shared_library/{source.name}"))
    for source in sorted((ROOT / "scripts" / "mintou").rglob("*.py")):
        pairs.append((source, f"05_code/workflow_scripts/{source.relative_to(ROOT / 'scripts' / 'mintou').as_posix()}"))
    for source in sorted((ROOT / "tests").glob("test_mintou*.py")):
        pairs.append((source, f"05_code/tests/{source.name}"))
    for name in ("pyproject.toml", "requirements.txt", "environment.yml"):
        source = ROOT / name
        if source.is_file():
            pairs.append((source, f"05_code/environment/{name}"))

    add_tree(
        project,
        "06_review_provenance/project_snapshot",
        excluded_prefixes=(
            project / "manuscript" / "journal_submission",
            project / "manuscript" / "submission_preview",
            project / "manuscript" / "figures",
            project / "manuscript" / "derived_tables",
            project / "experiments",
        ),
    )
    add_tree(
        companion,
        "06_review_provenance/companion_snapshot",
        excluded_prefixes=(companion / "evidence", companion / "src"),
    )
    for source in COMMON_AUDIT_FILES:
        if source.is_file():
            pairs.append((source, f"06_review_provenance/portfolio_audit/{source.name}"))

    seen: set[str] = set()
    clean_pairs: list[tuple[Path, str]] = []
    for source, arcname in pairs:
        normalized = normalized_archive_name(arcname)
        if normalized in seen:
            raise RuntimeError(f"duplicate archive path: {normalized}")
        seen.add(normalized)
        clean_pairs.append((source, normalized))
    return clean_pairs


def package_counts(names: Iterable[str]) -> dict[str, int]:
    counts = {
        "latex_files": 0,
        "pdf_files": 0,
        "figure_files": 0,
        "table_files": 0,
        "experiment_files": 0,
        "evidence_data_files": 0,
        "code_files": 0,
        "review_provenance_files": 0,
    }
    for name in names:
        path = Path(name)
        if name.startswith("01_manuscript/latex/"):
            counts["latex_files"] += 1
        if name.startswith("01_manuscript/pdf/"):
            counts["pdf_files"] += 1
        if name.startswith("02_figures_tables/source_figures/") and path.suffix.lower() in FIGURE_EXTENSIONS:
            counts["figure_files"] += 1
        if name.startswith("02_figures_tables/derived_tables/") and path.suffix.lower() in TABLE_EXTENSIONS:
            counts["table_files"] += 1
        if name.startswith("03_experiments/"):
            counts["experiment_files"] += 1
        if name.startswith("04_evidence_data/"):
            counts["evidence_data_files"] += 1
        if name.startswith("05_code/") and path.suffix.lower() in CODE_EXTENSIONS:
            counts["code_files"] += 1
        if name.startswith("06_review_provenance/"):
            counts["review_provenance_files"] += 1
    return counts


def git_provenance() -> dict[str, object]:
    head = run_command(["git", "rev-parse", "HEAD"], ROOT)
    status = run_command(["git", "status", "--short"], ROOT)
    return {
        "head": str(head["stdout"]).strip() if head["returncode"] == 0 else None,
        "worktree_clean": not bool(str(status["stdout"]).strip()),
        "note": "Package hashes, rather than worktree cleanliness, bind every included artifact.",
    }


def reference_audit_for(spec: PaperSpec) -> dict[str, object]:
    if not REFERENCE_AUDIT.is_file():
        return {"status": "UNAVAILABLE", "note": "historical reference audit file not found"}
    data = json.loads(REFERENCE_AUDIT.read_text(encoding="utf-8"))
    row = data.get(spec.project)
    if not row:
        return {"status": "UNAVAILABLE", "note": "paper absent from historical reference audit"}
    return {
        "status": "HISTORICAL_AUDIT_PRESENT",
        "source": REFERENCE_AUDIT.relative_to(ROOT).as_posix(),
        "counts": row,
        "note": "This preserved audit is not represented as a fresh live re-verification.",
    }


def generated_markdown_report(report: dict[str, object]) -> str:
    static = report["latex_static"]
    compilation = report["compilation"]
    counts = report["package_counts"]
    lines = [
        f"# Verification report: {report['project']}",
        "",
        f"- Target journal: {report['target_journal']}",
        f"- Canonical source: `{report['canonical_source']['path']}`",
        f"- Canonical source SHA-256: `{report['canonical_source']['sha256']}`",
        f"- Isolated LaTeX build: PASS ({compilation['pages']} pages; PDF SHA-256 `{compilation['pdf_sha256']}`)",
        f"- Scientific evidence-contract check: {report['scientific_contract']['status']}",
        f"- Shared regression tests: {report['shared_regression_tests']['status']}",
        f"- Package status: {report['package_status']}",
        f"- Submission ready: {str(report['submission_ready']).lower()}",
        "",
        "## Material counts",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in counts.items())
    lines.extend(["", "## LaTeX checks", ""])
    lines.extend(
        [
            f"- Abstract words: {static['abstract_words']}",
            f"- Figure inclusions resolved: {len(static['resolved_graphics'])}/{static['graphics_inclusions']}",
            f"- Missing labels: {len(static['missing_labels'])}",
            f"- Missing bibliography keys: {len(static['missing_bibliography_keys'])}",
            f"- Author-controlled gates: {len(static['author_input_gates'])}",
        ]
    )
    if static["advisories"]:
        lines.extend(["", "## Advisories", ""])
        lines.extend(f"- {item}" for item in static["advisories"])
    lines.extend(
        [
            "",
            "## Scope note",
            "",
            "This report verifies compilation, internal LaTeX references, material presence, evidence-contract scaffolding, and archive integrity. It does not make a final scientific judgment for the authors and does not replace live journal-policy checks, plagiarism screening, or author sign-off.",
            "",
        ]
    )
    return "\n".join(lines)


def generated_submission_gate(report: dict[str, object]) -> str:
    gates = report["latex_static"]["author_input_gates"]
    lines = [
        f"# Submission gate: {report['project']}",
        "",
        "Status: **AUTHOR SIGN-OFF REQUIRED BEFORE SUBMISSION**",
        "",
        "The archive is complete and mechanically verified, but it must not be uploaded until all author-controlled declarations are resolved. No author identity, affiliation, CRediT role, funding statement, conflict statement, ORCID, repository DOI, or AI-use disclosure has been guessed.",
        "",
        "## Unresolved author-controlled fields in canonical LaTeX",
        "",
    ]
    if gates:
        for gate in gates:
            text = re.sub(r"\s+", " ", gate["text"])
            lines.append(f"- Line {gate['line']}: {text}")
    else:
        lines.append("- No literal `AUTHOR INPUT REQUIRED` marker was found; a human submission-owner check is still required.")
    lines.extend(
        [
            "",
            "## Final manual actions",
            "",
            "- Confirm author list, affiliations, correspondence, CRediT roles, and author approval.",
            "- Confirm funding/APC funding, acknowledgments, conflicts of interest, ethics wording, and generative-AI disclosure.",
            "- Deposit the code/data supplement in a persistent archive where the manuscript requires a public URL or DOI.",
            "- Re-check the live target-journal instructions and upload fields immediately before submission.",
            "",
        ]
    )
    return "\n".join(lines)


def generated_readme(report: dict[str, object]) -> str:
    return f"""# {report['project']}: latest complete verified package

Canonical manuscript source: `01_manuscript/latex/paper.tex`  
Fresh PDF compiled from that exact source: `01_manuscript/pdf/paper.pdf`

The package deliberately excludes the older `paper.pdf` and `paper_narrative_revision.pdf` files from the working tree. The only primary manuscript PDF is the fresh isolated build above. `06_review_provenance/project_snapshot/manuscript/MANUSCRIPT.md`, when present, is a legacy Markdown working snapshot and is **not** the canonical source.

Contents:

- `01_manuscript/`: canonical LaTeX, journal class/template dependencies, referenced figures, and the freshly compiled PDF.
- `02_figures_tables/`: source figures and derived tables.
- `03_experiments/`: project-local experiment scripts, configs, logs, and outputs when present.
- `04_evidence_data/`: evidence runs, source data, result tables, manifests, and provenance.
- `05_code/`: paper scaffold, shared Mintou implementation modules, workflow scripts, tests, and environment metadata.
- `06_review_provenance/`: revision records, trace/logic material, manuscript working snapshot, portfolio audits, and reference-audit summary.
- `VERIFICATION_REPORT.*`: compilation and completeness results.
- `SUBMISSION_GATE.md`: author-controlled items that still block upload.
- `SHA256SUMS.txt`: SHA-256 for every payload file except the checksum file itself.

Package status: **{report['package_status']}**. This is an internal complete package, not an editorial acceptance guarantee. Read `SUBMISSION_GATE.md` before any upload.
"""


def add_bytes(
    archive: zipfile.ZipFile,
    name: str,
    data: bytes,
    hashes: dict[str, str],
) -> None:
    normalized = normalized_archive_name(name)
    if normalized in hashes:
        raise RuntimeError(f"duplicate generated archive path: {normalized}")
    archive.writestr(normalized, data)
    hashes[normalized] = sha256_bytes(data)


def verify_zip(
    archive_path: Path,
    expected_tex_sha256: str,
    expected_pdf_sha256: str,
) -> dict[str, object]:
    with zipfile.ZipFile(archive_path, "r") as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise RuntimeError(f"ZIP CRC failure: {corrupt}")
        names = archive.namelist()
        if names.count("01_manuscript/latex/paper.tex") != 1:
            raise RuntimeError("archive must contain exactly one canonical paper.tex")
        primary_pdfs = [name for name in names if name.startswith("01_manuscript/pdf/") and name.endswith(".pdf")]
        if primary_pdfs != ["01_manuscript/pdf/paper.pdf"]:
            raise RuntimeError(f"archive has ambiguous primary PDFs: {primary_pdfs}")
        if sha256_bytes(archive.read("01_manuscript/latex/paper.tex")) != expected_tex_sha256:
            raise RuntimeError("packaged paper.tex differs from canonical source")
        if sha256_bytes(archive.read("01_manuscript/pdf/paper.pdf")) != expected_pdf_sha256:
            raise RuntimeError("packaged paper.pdf differs from isolated build")
        sums_text = archive.read("SHA256SUMS.txt").decode("utf-8")
        checksum_rows = {}
        for line in sums_text.splitlines():
            digest, name = line.split("  ", 1)
            checksum_rows[name] = digest
        payload_names = set(names) - {"SHA256SUMS.txt"}
        if set(checksum_rows) != payload_names:
            raise RuntimeError("SHA256SUMS payload list differs from ZIP payload")
        for name, expected in checksum_rows.items():
            actual = sha256_bytes(archive.read(name))
            if actual != expected:
                raise RuntimeError(f"checksum mismatch inside ZIP: {name}")
        required_prefixes = (
            "01_manuscript/latex/",
            "01_manuscript/pdf/",
            "02_figures_tables/source_figures/",
            "02_figures_tables/derived_tables/",
            "04_evidence_data/",
            "05_code/",
            "06_review_provenance/",
        )
        missing_prefixes = [prefix for prefix in required_prefixes if not any(name.startswith(prefix) for name in names)]
        if missing_prefixes:
            raise RuntimeError("archive missing required sections: " + ", ".join(missing_prefixes))
    return {
        "crc": "PASS",
        "checksums": "PASS",
        "canonical_tex": "PASS",
        "canonical_pdf": "PASS",
        "files": len(names),
    }


def build_package(
    spec: PaperSpec,
    out_dir: Path,
    manifest_row: dict[str, str],
    shared_tests: dict[str, object],
    git_info: dict[str, object],
    overwrite: bool,
) -> dict[str, object]:
    project = PROJECTS_ROOT / spec.project
    tex_path = project / "manuscript" / "journal_submission" / "paper.tex"
    if not tex_path.is_file():
        raise FileNotFoundError(tex_path)
    static = tex_static_checks(spec, tex_path, manifest_row)
    if static["hard_failures"]:
        raise RuntimeError(f"{spec.project} static LaTeX checks failed: {static['hard_failures']}")
    materials = verify_material_roots(spec)
    scientific = run_scientific_contract(spec.project)
    canonical_tex_sha256 = sha256_file(tex_path)

    archive_path = out_dir / f"{spec.project}_latest_complete_verified.zip"
    if archive_path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing archive: {archive_path}")

    with tempfile.TemporaryDirectory(prefix="mintou_latest_package_") as temp:
        temp_root = Path(temp)
        compiled_pdf, compilation = compile_pdf(
            spec,
            tex_path.parent,
            str(static["title"]),
            temp_root,
        )
        source_pairs = collect_source_files(spec)
        source_names = [arcname for _, arcname in source_pairs]
        counts = package_counts(source_names + ["01_manuscript/pdf/paper.pdf"])
        for key in ("latex_files", "pdf_files", "figure_files", "table_files", "evidence_data_files", "code_files"):
            if counts[key] <= 0:
                raise RuntimeError(f"{spec.project} package category is empty: {key}")
        report: dict[str, object] = {
            "schema": "mintou-latest-verified-package-v1",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "paper_id": spec.paper_id,
            "project": spec.project,
            "target_journal": spec.target_journal,
            "canonical_source": {
                "path": tex_path.relative_to(ROOT).as_posix(),
                "sha256": canonical_tex_sha256,
                "policy": "paper.tex is canonical; legacy MANUSCRIPT.md is provenance only",
            },
            "latex_static": static,
            "compilation": compilation,
            "material_roots": materials,
            "scientific_contract": scientific,
            "shared_regression_tests": shared_tests,
            "reference_audit": reference_audit_for(spec),
            "git": git_info,
            "package_counts": counts,
            "package_status": "PASS_WITH_AUTHOR_GATES" if static["author_input_gates"] else "PASS",
            "submission_ready": False,
            "submission_note": "A complete ZIP is not upload-ready until SUBMISSION_GATE.md is cleared by the authors.",
        }
        generated = {
            "PACKAGE_README.md": generated_readme(report).encode("utf-8"),
            "SUBMISSION_GATE.md": generated_submission_gate(report).encode("utf-8"),
            "VERIFICATION_REPORT.json": (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
            "VERIFICATION_REPORT.md": generated_markdown_report(report).encode("utf-8"),
        }

        hashes: dict[str, str] = {}
        with zipfile.ZipFile(
            archive_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            allowZip64=True,
        ) as archive:
            for name, data in generated.items():
                add_bytes(archive, name, data, hashes)
            for source, arcname in source_pairs:
                data = source.read_bytes()
                add_bytes(archive, arcname, data, hashes)
            add_bytes(
                archive,
                "01_manuscript/pdf/paper.pdf",
                compiled_pdf.read_bytes(),
                hashes,
            )
            sums = "".join(f"{digest}  {name}\n" for name, digest in sorted(hashes.items()))
            archive.writestr("SHA256SUMS.txt", sums.encode("utf-8"))

        zip_verification = verify_zip(
            archive_path,
            expected_tex_sha256=canonical_tex_sha256,
            expected_pdf_sha256=str(compilation["pdf_sha256"]),
        )

    return {
        "paper_id": spec.paper_id,
        "project": spec.project,
        "title": static["title"],
        "target_journal": spec.target_journal,
        "archive": archive_path.relative_to(ROOT).as_posix(),
        "bytes": archive_path.stat().st_size,
        "sha256": sha256_file(archive_path),
        "payload_files": zip_verification["files"] - 1,
        "pdf_pages": compilation["pages"],
        "canonical_tex_sha256": canonical_tex_sha256,
        "compiled_pdf_sha256": compilation["pdf_sha256"],
        "package_status": report["package_status"],
        "submission_ready": False,
        "zip_verification": zip_verification,
        "package_counts": counts,
    }


def write_index(out_dir: Path, rows: list[dict[str, object]]) -> None:
    index_json = out_dir / "PACKAGE_INDEX.json"
    index_md = out_dir / "PACKAGE_INDEX.md"
    index_json.write_text(
        json.dumps(
            {
                "schema": "mintou-six-package-index-v1",
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "packages": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Mintou six-paper latest verified packages",
        "",
        "All six archives passed isolated LaTeX compilation, source/PDF binding, material-presence checks, internal SHA-256 verification, and ZIP CRC verification. Every package remains subject to its author-controlled `SUBMISSION_GATE.md`.",
        "",
        "| Paper | Journal | Pages | ZIP bytes | SHA-256 |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['project']} | {row['target_journal']} | {row['pdf_pages']} | {row['bytes']} | `{row['sha256']}` |"
        )
    lines.append("")
    index_md.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--project",
        choices=[spec.project for spec in PAPERS],
        help="Build one package; omitted builds all six.",
    )
    args = parser.parse_args(argv)
    out_dir = args.output.resolve()
    expected_parent = (ROOT / "deliverables").resolve()
    if out_dir != expected_parent and expected_parent not in out_dir.parents:
        raise SystemExit(f"output must stay under {expected_parent}: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    portfolio = load_portfolio_manifest()
    missing = [spec.project for spec in PAPERS if spec.project not in portfolio]
    if missing:
        raise SystemExit("portfolio manifest is missing: " + ", ".join(missing))

    selected = [spec for spec in PAPERS if not args.project or spec.project == args.project]
    shared_tests = run_shared_regression_tests()
    git_info = git_provenance()
    rows = []
    for spec in selected:
        row = build_package(
            spec,
            out_dir,
            portfolio[spec.project],
            shared_tests,
            git_info,
            args.overwrite,
        )
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False))
    write_index(out_dir, rows)
    print(f"index={out_dir.relative_to(ROOT).as_posix()}/PACKAGE_INDEX.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
