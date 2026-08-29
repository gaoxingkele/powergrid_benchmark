#!/usr/bin/env python3
"""Fail-closed validator for the deterministic nine-page Stage-6 release."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "manuscript" / "journal_submission"
PACKAGE_ROOT = ROOT / "release_package"
PACKAGE = PACKAGE_ROOT / "manuscript"
MANIFEST_PATH = PACKAGE_ROOT / "PACKAGE_MANIFEST.json"
QA_PATH = ROOT / "manuscript" / "PDF_RENDER_QA.json"
EPOCH = "1787867025"


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def sha256(path: Path) -> str:
    require(path.is_file(), f"required file is missing: {path.relative_to(ROOT)}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required JSON is missing: {path.relative_to(ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover
        raise ValidationError(f"cannot parse {path.relative_to(ROOT)}: {exc}") from exc
    require(isinstance(value, dict), f"JSON root must be an object: {path.relative_to(ROOT)}")
    return value


def page_count(pdf: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(pdf)],
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    require(completed.returncode == 0, f"pdfinfo failed for {pdf.relative_to(ROOT)}: {completed.stdout.strip()}")
    match = re.search(r"^Pages:\s+(\d+)\s*$", completed.stdout, flags=re.MULTILINE)
    require(match is not None, f"page count missing for {pdf.relative_to(ROOT)}")
    return int(match.group(1))


def semantic_text(pdf: Path) -> bytes:
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(completed.returncode == 0, f"pdftotext failed for {pdf.relative_to(ROOT)}")
    text = completed.stdout.decode("utf-8", errors="strict").replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).strip() + "\n"
    return normalized.encode("utf-8")


def main() -> int:
    journal_pdf = JOURNAL / "paper.pdf"
    package_pdf = PACKAGE / "paper.pdf"
    journal_tex = JOURNAL / "paper.tex"
    package_tex = PACKAGE / "paper.tex"
    pdf_hash = sha256(journal_pdf)
    require(pdf_hash == sha256(package_pdf), "journal and package PDF bytes differ")
    tex_hash = sha256(journal_tex)
    require(tex_hash == sha256(package_tex), "journal and package TeX bytes differ")

    manifest = load_json(MANIFEST_PATH)
    require(manifest.get("schema") == "p1_stage6_compact_release_manifest", "package manifest schema changed")
    require(manifest.get("source_date_epoch") == EPOCH, "package SOURCE_DATE_EPOCH changed")
    require(manifest.get("force_source_date") == EPOCH, "package FORCE_SOURCE_DATE changed")
    require(manifest.get("payload_file_count") == 87, "release payload is not the compact 87-file style")
    require(manifest.get("explicit_human_placeholders_retained") is True, "package human-placeholder gate changed")
    require("deferred" in manifest.get("built_in_pdf_integrity", ""), "built-in pdf_integrity was not explicitly deferred")
    entries = manifest.get("files")
    require(isinstance(entries, list) and len(entries) == 87, "package manifest must index exactly 87 files")
    indexed_paths: set[str] = set()
    for entry in entries:
        require(isinstance(entry, dict), "package manifest contains a non-object file entry")
        relative = entry.get("path")
        require(isinstance(relative, str) and relative.startswith("manuscript/"), "invalid package-manifest path")
        require(relative not in indexed_paths, f"duplicate package-manifest path: {relative}")
        indexed_paths.add(relative)
        path = PACKAGE_ROOT / relative
        require(path.is_file(), f"manifested package file is missing: {relative}")
        require(entry.get("bytes") == path.stat().st_size, f"package size mismatch: {relative}")
        require(entry.get("sha256") == sha256(path), f"package hash mismatch: {relative}")
        source = entry.get("source")
        require(isinstance(source, str), f"source mapping missing: {relative}")
        source_path = ROOT / source
        require(source_path.is_file(), f"package source is missing: {source}")
        require(sha256(source_path) == sha256(path), f"package/source identity mismatch: {relative}")
    actual_payload = {path.relative_to(PACKAGE_ROOT).as_posix() for path in PACKAGE.rglob("*") if path.is_file()}
    require(actual_payload == indexed_paths, "package contains missing or unmanifested payload files")

    require(page_count(journal_pdf) == 9 and page_count(package_pdf) == 9, "nine-page identity failed")
    journal_text = semantic_text(journal_pdf)
    package_text = semantic_text(package_pdf)
    require(journal_text == package_text, "semantic extracted text differs")
    semantic_hash = hashlib.sha256(journal_text).hexdigest()

    qa = load_json(QA_PATH)
    require(qa.get("schema") == "p1_stage6_pdf_render_qa", "PDF QA schema changed")
    require(qa.get("source_date_epoch") == EPOCH and qa.get("force_source_date") == EPOCH, "PDF QA build constant changed")
    require(qa.get("pdf_sha256") == pdf_hash and qa.get("package_pdf_sha256") == pdf_hash, "PDF QA hash is stale")
    require(qa.get("raw_pdf_equality") is True, "PDF QA raw-equality gate failed")
    require(qa.get("page_count") == 9 and qa.get("package_page_count") == 9, "PDF QA page count changed")
    require(qa.get("semantic_extracted_text_sha256") == semantic_hash, "PDF QA semantic hash is stale")
    require(qa.get("package_semantic_extracted_text_sha256") == semantic_hash, "package semantic hash is stale")
    require(qa.get("semantic_extracted_text_equal") is True, "semantic-equality gate failed")
    compile_record = qa.get("compilation", {})
    require(compile_record.get("compile_hash_a") == pdf_hash, "first deterministic compile hash changed")
    require(compile_record.get("compile_hash_b") == pdf_hash, "second deterministic compile hash changed")
    require(compile_record.get("repeated_compiles_byte_identical") is True, "repeated compiles were not byte-identical")
    require(qa.get("inspection_status") == "PASS", "current-page visual inspection is not complete")
    require(qa.get("inspected_pages") == list(range(1, 10)), "not all nine current pages were visually inspected")
    renders = qa.get("renders")
    require(isinstance(renders, list) and len(renders) == 9, "PDF QA must index nine current renders")
    for page, render in enumerate(renders, start=1):
        require(render.get("page") == page, f"render page order changed at page {page}")
        require(render.get("visual_status") == "PASS", f"page {page} visual review did not pass")
        render_path = ROOT / render.get("path", "")
        require(render_path.is_file(), f"page {page} current render is missing")
        require(render.get("bytes") == render_path.stat().st_size, f"page {page} render size changed")
        require(render.get("sha256") == sha256(render_path), f"page {page} render hash changed")

    tex_text = journal_tex.read_text(encoding="utf-8", errors="strict")
    extracted = journal_text.decode("utf-8", errors="strict")
    require("AUTHOR INPUT REQUIRED" in tex_text and "AUTHOR INPUT REQUIRED" in extracted, "required human placeholders disappeared")
    require("deferred" in qa.get("built_in_pdf_integrity", ""), "PDF QA did not retain pdf_integrity deferral")

    print(
        json.dumps(
            {
                "status": "PASS",
                "pdf_sha256": pdf_hash,
                "tex_sha256": tex_hash,
                "semantic_sha256": semantic_hash,
                "pages": 9,
                "payload_files": 87,
                "package_manifest_hashes_verified": 87,
                "current_page_renders_verified": 9,
                "repeated_compiles_byte_identical": True,
                "built_in_pdf_integrity": "deferred: explicit human placeholders remain",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"STAGE6 DETERMINISTIC RELEASE INVALID: {exc}")
        raise SystemExit(1)
