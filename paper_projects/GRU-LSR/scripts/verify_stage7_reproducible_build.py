#!/usr/bin/env python3
"""Build the human-complete P1 manuscript reproducibly without in-place trial writes."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from _stage7_release_common import (
    BUILD_COMMAND,
    BUILD_IDENTITY_PATH,
    EXPECTED_ENVIRONMENT,
    JOURNAL,
    MARKDOWN_PATH,
    METADATA_PATH,
    atomic_write_json,
    canonical_text_sha256,
    main_error,
    page_count,
    require,
    require_environment,
    require_no_placeholders,
    require_safe_tree,
    run_metadata_gate,
    semantic_sha256,
    sha256,
    tool_version,
)


TEMP_EXCLUDED_NAMES = {"paper.pdf", "paper_narrative_revision.pdf"}
TEMP_EXCLUDED_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".bbl",
    ".blg",
    ".fls",
    ".fdb_latexmk",
    ".synctex",
    ".synctex.gz",
}
UNRESOLVED_LOG_PATTERNS = (
    re.compile(r"LaTeX Warning: There were undefined references", re.IGNORECASE),
    re.compile(r"LaTeX Warning: (?:Citation|Reference) .+ undefined", re.IGNORECASE),
    re.compile(r"There were undefined citations", re.IGNORECASE),
    re.compile(r"Rerun to get cross-references right", re.IGNORECASE),
)


def excluded_from_compile_copy(path: Path) -> bool:
    if path.name in TEMP_EXCLUDED_NAMES:
        return True
    lowered = path.name.lower()
    return any(lowered.endswith(suffix) for suffix in TEMP_EXCLUDED_SUFFIXES)


def copy_compile_tree(destination: Path) -> None:
    require_safe_tree(JOURNAL)
    destination.mkdir(parents=True)
    for source in sorted(JOURNAL.rglob("*"), key=lambda item: item.relative_to(JOURNAL).as_posix()):
        relative = source.relative_to(JOURNAL)
        target = destination / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif source.is_file() and not excluded_from_compile_copy(source):
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def compile_three_passes(compile_root: Path, pdflatex: str) -> list[str]:
    hashes: list[str] = []
    for pass_number in range(1, 4):
        completed = subprocess.run(
            [pdflatex, *BUILD_COMMAND[1:]],
            cwd=compile_root,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=os.environ.copy(),
        )
        require(
            completed.returncode == 0,
            f"pdflatex pass {pass_number} failed:\n{completed.stdout[-6000:]}",
        )
        output_pdf = compile_root / "paper.pdf"
        require(output_pdf.is_file(), f"pdflatex pass {pass_number} produced no paper.pdf")
        hashes.append(sha256(output_pdf))
    return hashes


def publish_pdf(source_pdf: Path) -> None:
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=JOURNAL,
            prefix=".stage7-paper.",
            suffix=".pdf.tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
        shutil.copyfile(source_pdf, temporary)
        require(sha256(temporary) == sha256(source_pdf), "staged PDF copy is not byte-identical")
        os.replace(temporary, JOURNAL / "paper.pdf")
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def execute() -> int:
    # This must be first: incomplete human facts cannot trigger compilation or writes.
    run_metadata_gate("prebuild")
    require_environment()
    pdflatex, pdflatex_version = tool_version("pdflatex")
    tool_version("pdfinfo", ["-v"])
    tool_version("pdftotext", ["-v"])
    require_no_placeholders(MARKDOWN_PATH)
    require_no_placeholders(JOURNAL / "paper.tex")

    with tempfile.TemporaryDirectory(prefix="p1_stage7_compile_") as temporary:
        compile_root = Path(temporary) / "journal_submission"
        copy_compile_tree(compile_root)
        compile_hashes = compile_three_passes(compile_root, pdflatex)
        require(len(set(compile_hashes)) == 1, f"three compile hashes differ: {compile_hashes}")

        log_path = compile_root / "paper.log"
        require(log_path.is_file(), "pdflatex did not produce paper.log")
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
        unresolved = [pattern.pattern for pattern in UNRESOLVED_LOG_PATTERNS if pattern.search(log_text)]
        require(not unresolved, f"unresolved LaTeX diagnostics remain after three passes: {unresolved}")

        pdf = compile_root / "paper.pdf"
        pages = page_count(pdf)
        require(0 < pages < 20, f"compiled paper must contain 1-19 pages, observed {pages}")
        require_no_placeholders(pdf, pdf=True)
        identity = {
            "schema": "p1_stage7_build_identity",
            "schema_version": 1,
            "environment": EXPECTED_ENVIRONMENT,
            "build_command": BUILD_COMMAND,
            "build_passes": 3,
            "pdflatex_executable": pdflatex,
            "pdflatex_version": pdflatex_version,
            "compile_pdf_sha256": compile_hashes,
            "pdf_sha256": sha256(pdf),
            "pdf_bytes": pdf.stat().st_size,
            "page_count": pages,
            "semantic_text_sha256": semantic_sha256(pdf),
            "tex_sha256": sha256(JOURNAL / "paper.tex"),
            "tex_canonical_sha256": canonical_text_sha256(JOURNAL / "paper.tex"),
            "metadata_sha256": sha256(METADATA_PATH),
            "markdown_sha256": sha256(MARKDOWN_PATH),
            "unresolved_latex_diagnostics": [],
            "human_placeholders_retained": False,
        }
        require(identity["pdf_sha256"] == compile_hashes[-1], "final compile hash bookkeeping differs")
        publish_pdf(pdf)
        require(sha256(JOURNAL / "paper.pdf") == identity["pdf_sha256"], "published journal PDF hash differs")
        atomic_write_json(BUILD_IDENTITY_PATH, identity)

    print(
        "STAGE7 REPRODUCIBLE BUILD PASS "
        f"pages={identity['page_count']} pdf_sha256={identity['pdf_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main_error("STAGE7 REPRODUCIBLE BUILD BLOCKED", execute))
