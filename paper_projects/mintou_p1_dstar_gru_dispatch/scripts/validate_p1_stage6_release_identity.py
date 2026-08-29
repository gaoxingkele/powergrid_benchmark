"""Read-only terminal validator for the P1 Stage-6 release identity.

The validator writes only to an operating-system temporary directory while
independently rendering the two PDFs. It never modifies the worktree.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "manuscript" / "journal_submission"
RELEASE = ROOT / "manuscript" / "release_package"
EXPECTED_PDF_SHA256 = "bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c"
EXPECTED_PAGES = 9
EXPECTED_SOURCE_DATE_EPOCH = "1787867025"
EXPECTED_ABSTRACT_SHA256 = "c86963d625f30e7f1c709f0b2ea55a6913c01a51d88835f3053fb42c37f176f6"
EXPECTED_RUNNER_SHA256 = "d4f0e14dd010e4f429e2d61771d781b169a673b73156dac5236113f0e3f34e28"
EXPECTED_CONTRACT_SHA256 = "3d99dc96aeb9ac51974f76e5c0f544083f4dc41a4f5de5998b7b3e7f2ec78878"

AUXILIARY_SUFFIXES = {
    ".aux",
    ".out",
    ".toc",
    ".bbl",
    ".blg",
    ".fls",
    ".fdb_latexmk",
    ".synctex",
    ".synctex.gz",
}
CACHE_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "cache",
}
RUNTIME_FILENAMES = {
    "pdflatex.exe",
    "pdftex.exe",
    "miktex.exe",
    "miktex-pdflatex.exe",
    "initexmf.exe",
    "mpm.exe",
    "mpm_mfc.exe",
    "miktexsetup.exe",
}


def fail(message: str) -> None:
    raise SystemExit(f"STAGE6 RELEASE IDENTITY INVALID: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required JSON missing: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.relative_to(ROOT)}: {exc}")
    require(isinstance(value, dict), f"JSON root is not an object: {path.relative_to(ROOT)}")
    return value


def semantic_text(path: Path) -> tuple[int, str]:
    try:
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except (OSError, ValueError) as exc:
        fail(f"cannot extract PDF text from {path.relative_to(ROOT)}: {exc}")
    normalized = re.sub(r"\s+", " ", text).strip()
    return len(reader.pages), normalized


def render_hashes(path: Path, output_parent: Path, label: str) -> list[str]:
    output_parent.mkdir(parents=True, exist_ok=False)
    prefix = output_parent / "page"
    completed = subprocess.run(
        ["pdftoppm", "-png", "-r", "150", str(path), str(prefix)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    require(completed.returncode == 0, f"{label} pdftoppm render failed: {completed.stderr.strip()}")
    pages = sorted(output_parent.glob("page-*.png"))
    require(len(pages) == EXPECTED_PAGES, f"{label} rendered page count is {len(pages)}")
    return [sha256(page) for page in pages]


def has_auxiliary_suffix(path: str) -> bool:
    lowered = path.lower()
    return any(lowered.endswith(suffix) for suffix in AUXILIARY_SUFFIXES)


def forbidden_path_reason(path: str) -> str | None:
    normalized = path.replace("\\", "/")
    parts = [part.lower() for part in normalized.split("/") if part]
    if any(part.startswith(".miktex") for part in parts):
        return ".miktex path"
    if has_auxiliary_suffix(normalized):
        return "TeX auxiliary/log file"
    if normalized.lower().endswith(".log") and "manuscript/" in normalized.lower():
        return "TeX auxiliary/log file"
    if any(part in CACHE_PARTS for part in parts):
        return "cache path"
    filename = parts[-1] if parts else ""
    if filename in RUNTIME_FILENAMES:
        return "alternative TeX runtime executable"
    if any(part in {"texmf", "texmf-local", "texmflocal", "miktex-portable"} for part in parts):
        return "packaged TeX runtime tree"
    return None


def validate_no_tracked_or_packaged_runtime_debris() -> None:
    completed = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=False, capture_output=True, text=True
    )
    require(completed.returncode == 0, f"git ls-files failed: {completed.stderr.strip()}")
    tracked = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    violations: list[str] = []
    for path in tracked:
        reason = forbidden_path_reason(path)
        if reason:
            violations.append(f"tracked {reason}: {path}")
    require(RELEASE.is_dir(), "release package directory is missing")
    for path in RELEASE.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        reason = forbidden_path_reason(relative)
        if reason:
            violations.append(f"packaged {reason}: {relative}")
    require(not violations, "; ".join(violations))


def validate_science_preservation() -> None:
    rerun = ROOT / "experiments" / "p1_ieee_access_upgrade_v2_stage6_attempt5"
    comparison = load_json(rerun / "STAGE6_RERUN_COMPARISON.json")
    require(comparison.get("status") == "scientific_content_exact_timing_disclosed", "rerun comparison status changed")
    require(comparison.get("supports_new_claim") is False, "rerun comparison supports a new claim")
    identity = comparison.get("identity", {})
    require(identity.get("runner_sha256") == EXPECTED_RUNNER_SHA256, "rerun comparison runner hash changed")
    require(identity.get("contract_sha256") == EXPECTED_CONTRACT_SHA256, "rerun comparison contract hash changed")
    require(identity.get("source_file_hashes_exact") is True, "rerun input identity is not exact")
    require(
        comparison.get("scientific_outputs", {}).get("all_non_timing_content_exact") is True,
        "rerun non-timing scientific content is not exact",
    )
    derived = comparison.get("derived_tables", {})
    require(len(derived) == 5, "rerun comparison does not cover five derived tables")
    require(
        all(record.get("canonical_scientific_bytes_equal") is True for record in derived.values()),
        "a rerun-derived paper table is not exact",
    )
    narrative = comparison.get("accepted_narrative_and_human_placeholders", {})
    require(narrative.get("word_count") == 236, "accepted narrative is not 236 words")
    require(narrative.get("sha256") == EXPECTED_ABSTRACT_SHA256, "accepted narrative hash changed")
    require(narrative.get("markdown_author_input_required_count") == 11, "Markdown placeholders changed")
    require(narrative.get("tex_author_input_required_count") == 9, "TeX placeholders changed")


def main() -> int:
    validate_science_preservation()
    validate_no_tracked_or_packaged_runtime_debris()

    journal_pdf = JOURNAL / "paper.pdf"
    journal_tex = JOURNAL / "paper.tex"
    package_pdf = RELEASE / "paper.pdf"
    package_tex = RELEASE / "paper.tex"
    for path in (journal_pdf, journal_tex, package_pdf, package_tex):
        require(path.is_file(), f"required release artifact missing: {path.relative_to(ROOT)}")
    qa = load_json(RELEASE / "PDF_RENDER_QA.json")
    manifest = load_json(RELEASE / "PACKAGE_MANIFEST.json")

    journal_pdf_sha = sha256(journal_pdf)
    package_pdf_sha = sha256(package_pdf)
    qa_source_sha = qa.get("source_pdf", {}).get("sha256")
    qa_package_sha = qa.get("packaged_pdf", {}).get("sha256")
    manifest_pdf_sha = manifest.get("paper_pdf", {}).get("sha256")
    require(journal_pdf_sha == EXPECTED_PDF_SHA256, "journal PDF raw SHA-256 is not the frozen expected value")
    require(
        journal_pdf_sha == package_pdf_sha == qa_source_sha == qa_package_sha == manifest_pdf_sha,
        "journal/package/QA/manifest PDF hashes are not identical",
    )
    require(journal_pdf.read_bytes() == package_pdf.read_bytes(), "journal and packaged PDF bytes differ")
    require(manifest.get("paper_pdf", {}).get("bytes") == journal_pdf.stat().st_size, "manifest PDF byte count differs")
    require(qa.get("source_pdf", {}).get("bytes") == journal_pdf.stat().st_size, "QA source-PDF byte count differs")
    require(qa.get("packaged_pdf", {}).get("bytes") == package_pdf.stat().st_size, "QA package-PDF byte count differs")

    journal_tex_sha = sha256(journal_tex)
    package_tex_sha = sha256(package_tex)
    manifest_tex_sha = manifest.get("paper_tex", {}).get("sha256")
    require(journal_tex_sha == package_tex_sha == manifest_tex_sha, "journal/package/manifest TeX hashes differ")
    require(journal_tex.read_bytes() == package_tex.read_bytes(), "journal and packaged TeX bytes differ")
    require(manifest.get("paper_tex", {}).get("bytes") == journal_tex.stat().st_size, "manifest TeX byte count differs")

    build = manifest.get("build_contract", {})
    require(build.get("executable") == "inherited default-PATH pdflatex", "manifest build executable changed")
    require(build.get("command") == ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], "manifest command changed")
    require(build.get("passes") == 3, "manifest does not record three LaTeX passes")
    require(build.get("bibliography_step_required") is False, "unexpected bibliography step recorded")
    require(
        build.get("environment")
        == {"SOURCE_DATE_EPOCH": EXPECTED_SOURCE_DATE_EPOCH, "FORCE_SOURCE_DATE": "1", "TZ": "UTC"},
        "manifest deterministic build environment changed",
    )
    for field in (
        "custom_or_local_miktex_or_texmf_runtime",
        "miktex_or_texmf_override",
        "alternate_pdflatex_binary",
        "output_directory",
        "container",
    ):
        require(build.get(field) is False, f"prohibited build mechanism recorded: {field}")

    journal_pages, journal_text = semantic_text(journal_pdf)
    package_pages, package_text = semantic_text(package_pdf)
    require(journal_pages == package_pages == EXPECTED_PAGES, "journal/package page counts are not both nine")
    require(manifest.get("paper_pdf", {}).get("page_count") == EXPECTED_PAGES, "manifest page count is not nine")
    require(qa.get("render", {}).get("page_count") == EXPECTED_PAGES, "QA page count is not nine")
    require(qa.get("packaged_pdf", {}).get("page_count") == EXPECTED_PAGES, "QA packaged-PDF page count is not nine")
    require(journal_text == package_text, "semantically extracted journal/package text differs")
    for token in ("Persistence", "GRU", "2310", "AUTHOR INPUT REQUIRED"):
        require(token.lower() in journal_text.lower(), f"semantic PDF text missing required token: {token}")

    with tempfile.TemporaryDirectory(prefix="p1_stage6_terminal_render_") as temporary:
        temporary_root = Path(temporary)
        journal_render_hashes = render_hashes(journal_pdf, temporary_root / "journal", "journal PDF")
        package_render_hashes = render_hashes(package_pdf, temporary_root / "package", "package PDF")
    require(journal_render_hashes == package_render_hashes, "journal/package per-page render hashes differ")

    page_records = qa.get("render", {}).get("pages", [])
    require(isinstance(page_records, list) and len(page_records) == EXPECTED_PAGES, "QA lacks nine page records")
    recorded_render_hashes: list[str] = []
    for expected_page, record in enumerate(page_records, start=1):
        require(record.get("page") == expected_page, f"QA page order mismatch at page {expected_page}")
        render_file = RELEASE / str(record.get("file", ""))
        require(render_file.is_file(), f"QA render missing for page {expected_page}")
        recorded_sha = record.get("sha256")
        require(recorded_sha == sha256(render_file), f"QA stored render hash differs on page {expected_page}")
        require(record.get("bytes") == render_file.stat().st_size, f"QA stored render bytes differ on page {expected_page}")
        recorded_render_hashes.append(str(recorded_sha))
        inspection = record.get("visual_inspection", {})
        require(inspection.get("status") == "pass", f"visual inspection not passed for page {expected_page}")
        require(isinstance(inspection.get("inspected_by"), str) and inspection["inspected_by"].strip(), f"visual inspector missing for page {expected_page}")
        checks = inspection.get("checks", {})
        expected_checks = {
            "no_clipping",
            "no_overlap",
            "tables_figures_legible",
            "fonts_glyphs_rendered",
            "headers_footers_page_numbering_consistent",
        }
        require(set(checks) == expected_checks, f"visual check set differs on page {expected_page}")
        require(all(value is True for value in checks.values()), f"visual check failed on page {expected_page}")
        require(isinstance(inspection.get("notes"), str) and inspection["notes"].strip(), f"visual notes missing for page {expected_page}")
    require(recorded_render_hashes == journal_render_hashes, "QA-recorded and independently rendered page hashes differ")
    require(qa.get("visual_inspection_complete") is True, "QA visual-inspection completion flag is false")
    require(qa.get("complete_page_records") == EXPECTED_PAGES, "QA complete-page record count is not nine")
    require(qa.get("expected_page_records") == EXPECTED_PAGES, "QA expected-page record count is not nine")
    require(qa.get("scientific_claim_change") is False, "QA records a scientific claim change")
    require(manifest.get("scientific_claim_change") is False, "manifest records a scientific claim change")
    require(manifest.get("stage7_human_placeholders_retained") is True, "manifest does not retain Stage 7 placeholders")

    expected_package_files = {
        "paper.pdf",
        "paper.tex",
        "PACKAGE_MANIFEST.json",
        "PDF_RENDER_QA.json",
        *(f"rendered_pages/page-{page:02d}.png" for page in range(1, EXPECTED_PAGES + 1)),
    }
    actual_package_files = {
        path.relative_to(RELEASE).as_posix() for path in RELEASE.rglob("*") if path.is_file()
    }
    require(actual_package_files == expected_package_files, f"unexpected package file set: {sorted(actual_package_files ^ expected_package_files)}")

    print(
        "OK Stage 6 release identity: expected PDF hash; journal/package/QA/manifest identity; "
        "matching TeX; identical semantic text; nine identical renders; nine visual passes; no runtime debris"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
