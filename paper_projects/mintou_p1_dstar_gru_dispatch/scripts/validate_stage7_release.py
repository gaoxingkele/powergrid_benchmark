#!/usr/bin/env python3
"""Read-only terminal validator for the human-complete P1 Stage-7 release."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from _stage7_release_common import (
    BUILD_COMMAND,
    BUILD_IDENTITY_PATH,
    EXPECTED_ENVIRONMENT,
    FORBIDDEN_SUFFIXES,
    JOURNAL,
    MARKDOWN_PATH,
    MAX_SUBMISSION_FILE_BYTES,
    METADATA_PATH,
    PACKAGE,
    PACKAGE_MANIFEST_PATH,
    PACKAGE_ROOT,
    QA_PATH,
    RENDER_DIR,
    ROOT,
    SAMPLE_PHOTO_SHA256,
    forbidden_path_reason,
    load_json,
    main_error,
    page_count,
    render_pngs,
    require,
    require_environment,
    require_no_placeholders,
    require_safe_tree,
    run_metadata_gate,
    semantic_sha256,
    semantic_text,
    sha256,
    tool_version,
    validate_build_identity,
)


EXCLUDED_EXPLICITLY = {"body.generated.md", "paper_narrative_revision.pdf"}
UNRESOLVED_LOG_PATTERNS = (
    re.compile(r"LaTeX Warning: There were undefined references", re.IGNORECASE),
    re.compile(r"LaTeX Warning: (?:Citation|Reference) .+ undefined", re.IGNORECASE),
    re.compile(r"There were undefined citations", re.IGNORECASE),
    re.compile(r"Rerun to get cross-references right", re.IGNORECASE),
)


def timezone_aware(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


def validate_house_style(identity: dict[str, Any]) -> None:
    tex = (JOURNAL / "paper.tex").read_text(encoding="utf-8", errors="strict")
    require(re.search(r"\\documentclass(?:\[[^]]*\])?\{ieeeaccess\}", tex) is not None, "dedicated IEEE Access class is not used")
    match = re.search(r"\\begin\{keywords\}(.*?)\\end\{keywords\}", tex, flags=re.DOTALL)
    require(match is not None, "IEEE Access keywords environment is missing")
    keywords = [item.strip() for item in match.group(1).split(",") if item.strip()] if match else []
    require(3 <= len(keywords) <= 10, f"IEEE Access requires 3-10 keywords; observed {len(keywords)}")

    pdf_text = normalized_text(semantic_text(JOURNAL / "paper.pdf").decode("utf-8", errors="strict"))
    for keyword in keywords:
        require(normalized_text(keyword) in pdf_text, f"keyword is absent from compiled PDF: {keyword}")
    metadata = load_json(METADATA_PATH)
    authors = metadata.get("authors")
    require(isinstance(authors, list) and bool(authors), "confirmed author list is missing")
    for index, author in enumerate(authors, start=1):
        require(isinstance(author, dict), f"author metadata record {index} is invalid")
        name = author.get("name")
        biography = author.get("biography")
        require(isinstance(name, str) and normalized_text(name) in pdf_text, f"author {index} is absent from compiled PDF")
        require(
            isinstance(biography, str) and normalized_text(biography) in pdf_text,
            f"author {index} biography is absent from compiled PDF",
        )
    correspondence = metadata.get("correspondence")
    require(isinstance(correspondence, dict), "correspondence metadata is missing")
    email = correspondence.get("email") if isinstance(correspondence, dict) else None
    require(isinstance(email, str) and normalized_text(email) in pdf_text, "corresponding e-mail is absent from compiled PDF")
    require(identity["page_count"] < 20, "a 20+ page paper requires an IEEE Access pre-submission inquiry")


def safe_relative(value: Any, prefix: str) -> Path:
    require(isinstance(value, str) and bool(value), f"manifest path is invalid: {value!r}")
    relative = Path(value)
    require(not relative.is_absolute() and ".." not in relative.parts, f"manifest path escapes package: {value}")
    require(relative.as_posix().startswith(prefix), f"manifest path has wrong prefix: {value}")
    return relative


def validate_manifest(identity: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    manifest = load_json(PACKAGE_MANIFEST_PATH)
    require(manifest.get("schema") == "p1_stage7_compact_release_manifest", "package manifest schema changed")
    require(manifest.get("schema_version") == 1, "package manifest version changed")
    require(manifest.get("source_date_epoch") == EXPECTED_ENVIRONMENT["SOURCE_DATE_EPOCH"], "manifest epoch changed")
    require(manifest.get("force_source_date") == EXPECTED_ENVIRONMENT["FORCE_SOURCE_DATE"], "manifest force-source-date changed")
    require(manifest.get("timezone") == EXPECTED_ENVIRONMENT["TZ"], "manifest timezone changed")
    require(manifest.get("build_command") == BUILD_COMMAND, "manifest build command changed")
    require(manifest.get("build_passes") == 3, "manifest build-pass count changed")
    require(
        manifest.get("max_submission_file_bytes") == MAX_SUBMISSION_FILE_BYTES,
        "manifest 40 MB file-size gate changed",
    )
    require(manifest.get("build_identity_sha256") == sha256(BUILD_IDENTITY_PATH), "manifest build identity hash is stale")
    require(manifest.get("human_metadata_sha256") == sha256(METADATA_PATH), "manifest human metadata hash is stale")
    require(manifest.get("pdf_sha256") == identity["pdf_sha256"], "manifest PDF hash differs from build identity")
    require((PACKAGE / "paper.pdf").is_file(), "packaged paper.pdf is missing")
    require(manifest.get("pdf_bytes") == (PACKAGE / "paper.pdf").stat().st_size, "manifest PDF bytes are stale")
    require(manifest.get("page_count") == identity["page_count"], "manifest page count differs from build identity")
    require(
        manifest.get("semantic_text_sha256") == identity["semantic_text_sha256"],
        "manifest semantic PDF hash differs from build identity",
    )
    require(manifest.get("tex_sha256") == identity["tex_sha256"], "manifest TeX hash differs from build identity")
    require(
        manifest.get("tex_canonical_sha256") == identity["tex_canonical_sha256"],
        "manifest canonical TeX hash differs from build identity",
    )
    require(manifest.get("explicit_human_placeholders_retained") is False, "manifest retains human placeholders")
    require(manifest.get("stage7_human_metadata_complete") is True, "manifest metadata-complete flag is false")
    require(manifest.get("built_in_pdf_integrity") == "pass", "manifest built-in PDF integrity did not pass")

    entries = manifest.get("files")
    require(isinstance(entries, list) and bool(entries), "manifest file index is empty or invalid")
    require(manifest.get("payload_file_count") == len(entries), "manifest payload count differs from file index")
    indexed: set[str] = set()
    indexed_sources: set[str] = set()
    for entry in entries:
        require(isinstance(entry, dict), "manifest contains a non-object file entry")
        relative = safe_relative(entry.get("path"), "manuscript/")
        relative_text = relative.as_posix()
        require(relative_text not in indexed, f"duplicate manifest path: {relative_text}")
        indexed.add(relative_text)
        require(forbidden_path_reason(relative_text) is None, f"forbidden package path: {relative_text}")
        package_path = PACKAGE_ROOT / relative
        require(package_path.is_file(), f"manifested package file is missing: {relative_text}")
        require(entry.get("bytes") == package_path.stat().st_size, f"package byte count differs: {relative_text}")
        require(package_path.stat().st_size < MAX_SUBMISSION_FILE_BYTES, f"package file reaches 40 MB: {relative_text}")
        require(entry.get("sha256") == sha256(package_path), f"package hash differs: {relative_text}")
        require(sha256(package_path) not in SAMPLE_PHOTO_SHA256, f"sample IEEE portrait is packaged: {relative_text}")

        source_relative = safe_relative(entry.get("source"), "manuscript/journal_submission/")
        source_text = source_relative.as_posix()
        require(source_text not in indexed_sources, f"duplicate manifest source: {source_text}")
        indexed_sources.add(source_text)
        source = ROOT / source_relative
        require(source.is_file(), f"manifested source is missing: {source_relative.as_posix()}")
        require(sha256(source) == sha256(package_path), f"source/package bytes differ: {relative_text}")

    actual = {
        path.relative_to(PACKAGE_ROOT).as_posix()
        for path in PACKAGE.rglob("*")
        if path.is_file()
    }
    require(actual == indexed, "package contains missing or unmanifested payload files")
    expected_sources: set[str] = set()
    for source in JOURNAL.rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(JOURNAL).as_posix()
        lowered = source.name.lower()
        if relative in EXCLUDED_EXPLICITLY:
            continue
        if any(lowered.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
            continue
        if sha256(source) in SAMPLE_PHOTO_SHA256:
            continue
        require(forbidden_path_reason(relative) is None, f"forbidden journal source path: {relative}")
        expected_sources.add(source.relative_to(ROOT).as_posix())
    require(indexed_sources == expected_sources, "manifest source index is incomplete or includes unexpected files")
    return manifest, sorted(indexed)


def recompile_package(identity: dict[str, Any]) -> list[str]:
    pdflatex, version = tool_version("pdflatex")
    require(pdflatex == identity.get("pdflatex_executable"), "current pdflatex executable differs from build identity")
    require(version == identity.get("pdflatex_version"), "current pdflatex version differs from build identity")
    with tempfile.TemporaryDirectory(prefix="p1_stage7_package_compile_") as temporary:
        compile_root = Path(temporary) / "manuscript"
        shutil.copytree(PACKAGE, compile_root)
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
                f"packaged pdflatex pass {pass_number} failed:\n{completed.stdout[-6000:]}",
            )
            hashes.append(sha256(compile_root / "paper.pdf"))
        log_path = compile_root / "paper.log"
        require(log_path.is_file(), "package recompile produced no paper.log")
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
        unresolved = [pattern.pattern for pattern in UNRESOLVED_LOG_PATTERNS if pattern.search(log_text)]
        require(not unresolved, f"package recompile retains unresolved LaTeX diagnostics: {unresolved}")
    require(len(set(hashes)) == 1, f"package recompile hashes differ: {hashes}")
    require(hashes[0] == identity["pdf_sha256"], "package recompile does not reproduce the accepted PDF")
    return hashes


def validate_qa(identity: dict[str, Any]) -> list[str]:
    qa = load_json(QA_PATH)
    require(qa.get("schema") == "p1_stage7_pdf_render_qa", "Stage-7 QA schema changed")
    require(qa.get("schema_version") == 1, "Stage-7 QA version changed")
    require(qa.get("inspection_status") == "PASS", "Stage-7 visual inspection is not PASS")
    require(qa.get("built_in_pdf_integrity") == "pass", "Stage-7 QA PDF integrity is not pass")
    require(qa.get("human_placeholders_retained") is False, "Stage-7 QA retains human placeholders")
    require(qa.get("pdf_sha256") == identity["pdf_sha256"], "QA journal PDF hash is stale")
    require(qa.get("package_pdf_sha256") == identity["pdf_sha256"], "QA package PDF hash is stale")
    require(qa.get("inspection_basis_pdf_sha256") == identity["pdf_sha256"], "visual review is bound to another PDF")
    require(qa.get("raw_pdf_equality") is True, "QA raw PDF equality is false")
    require(qa.get("page_count") == identity["page_count"], "QA page count is stale")
    require(qa.get("package_page_count") == identity["page_count"], "QA package page count is stale")
    require(qa.get("semantic_extracted_text_equal") is True, "QA semantic PDF equality is false")
    require(
        qa.get("semantic_extracted_text_sha256") == identity["semantic_text_sha256"],
        "QA semantic journal hash is stale",
    )
    require(
        qa.get("package_semantic_extracted_text_sha256") == identity["semantic_text_sha256"],
        "QA semantic package hash is stale",
    )
    require(isinstance(qa.get("inspected_by"), str) and qa["inspected_by"].strip(), "visual inspector is missing")
    require(timezone_aware(qa.get("inspected_at_utc")), "visual inspection timestamp is invalid")
    expected_pages = list(range(1, int(identity["page_count"]) + 1))
    require(qa.get("inspected_pages") == expected_pages, "visual review does not cover every page")
    compilation = qa.get("compilation")
    require(isinstance(compilation, dict), "QA compilation record is missing")
    require(compilation.get("compile_hashes") == identity["compile_pdf_sha256"], "QA compile hashes are stale")
    require(compilation.get("repeated_compiles_byte_identical") is True, "QA compile identity is not stable")

    records = qa.get("renders")
    require(isinstance(records, list) and len(records) == len(expected_pages), "QA render records are incomplete")
    recorded_hashes: list[str] = []
    indexed_paths: set[str] = set()
    for expected_page, record in zip(expected_pages, records, strict=True):
        require(isinstance(record, dict), f"QA page {expected_page} record is invalid")
        require(record.get("page") == expected_page, f"QA page order differs at {expected_page}")
        require(record.get("visual_status") == "PASS", f"QA visual status is not PASS on page {expected_page}")
        require(isinstance(record.get("finding"), str) and record["finding"].strip(), f"QA finding is missing on page {expected_page}")
        relative = safe_relative(record.get("path"), "manuscript/stage7_rendered_pages/")
        relative_text = relative.as_posix()
        require(relative_text not in indexed_paths, f"duplicate QA render path: {relative_text}")
        indexed_paths.add(relative_text)
        render = ROOT / relative
        require(render.is_file(), f"QA render is missing: {relative_text}")
        require(record.get("bytes") == render.stat().st_size, f"QA render bytes differ on page {expected_page}")
        require(record.get("sha256") == sha256(render), f"QA render hash differs on page {expected_page}")
        recorded_hashes.append(str(record["sha256"]))
    actual_renders = {
        path.relative_to(ROOT).as_posix()
        for path in RENDER_DIR.rglob("*")
        if path.is_file()
    }
    require(actual_renders == indexed_paths, "render directory contains missing or unindexed pages")
    return recorded_hashes


def execute() -> int:
    # Terminal validation is read-only and starts with the human-fact release gate.
    run_metadata_gate("release")
    require_environment()
    require(PACKAGE_ROOT != ROOT / "release_package", "Stage-7 package must not overwrite Stage 6")
    require_safe_tree(PACKAGE_ROOT)
    require_safe_tree(RENDER_DIR)
    identity = validate_build_identity()
    validate_house_style(identity)
    validate_manifest(identity)
    recorded_render_hashes = validate_qa(identity)
    recompile_package(identity)

    journal_pdf = JOURNAL / "paper.pdf"
    package_pdf = PACKAGE / "paper.pdf"
    journal_tex = JOURNAL / "paper.tex"
    package_tex = PACKAGE / "paper.tex"
    require(journal_pdf.read_bytes() == package_pdf.read_bytes(), "journal/package PDF bytes differ")
    require(journal_tex.read_bytes() == package_tex.read_bytes(), "journal/package TeX bytes differ")
    require(page_count(journal_pdf) == page_count(package_pdf) == identity["page_count"], "PDF page counts differ")
    require(semantic_text(journal_pdf) == semantic_text(package_pdf), "journal/package semantic PDF text differs")
    require(semantic_sha256(journal_pdf) == identity["semantic_text_sha256"], "semantic PDF identity differs")
    for path in (MARKDOWN_PATH, journal_tex, package_tex):
        require_no_placeholders(path)
    for path in (journal_pdf, package_pdf):
        require_no_placeholders(path, pdf=True)

    with tempfile.TemporaryDirectory(prefix="p1_stage7_terminal_render_") as temporary:
        temporary_root = Path(temporary)
        journal_pages = render_pngs(journal_pdf, temporary_root / "journal", dpi=144)
        package_pages = render_pngs(package_pdf, temporary_root / "package", dpi=144)
        journal_hashes = [sha256(path) for path in journal_pages]
        package_hashes = [sha256(path) for path in package_pages]
    require(journal_hashes == package_hashes, "independent journal/package render hashes differ")
    require(journal_hashes == recorded_render_hashes, "independent render hashes differ from inspected QA pages")

    print(
        "STAGE7 TERMINAL RELEASE PASS "
        f"files={load_json(PACKAGE_MANIFEST_PATH)['payload_file_count']} "
        f"pages={identity['page_count']} pdf_sha256={identity['pdf_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main_error("STAGE7 TERMINAL RELEASE BLOCKED", execute))
