#!/usr/bin/env python3
"""Render the current nine-page paper and refresh PDF_RENDER_QA.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "manuscript" / "journal_submission" / "paper.pdf"
PACKAGE_PDF = ROOT / "release_package" / "manuscript" / "paper.pdf"
RENDER_DIR = ROOT / "manuscript" / "rendered_pages"
QA_PATH = ROOT / "manuscript" / "PDF_RENDER_QA.json"
SOURCE_DATE_EPOCH = "1787867025"
EXPECTED_PDF_SHA256 = "bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def semantic_text(pdf: Path) -> bytes:
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    text = completed.stdout.decode("utf-8", errors="strict").replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).strip() + "\n"
    return normalized.encode("utf-8")


def pages(pdf: Path) -> int:
    completed = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE)
    match = re.search(r"^Pages:\s+(\d+)\s*$", completed.stdout, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("pdfinfo did not report a page count")
    return int(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compile-hash-a", required=True)
    parser.add_argument("--compile-hash-b", required=True)
    parser.add_argument("--confirm-visual-review", action="store_true")
    args = parser.parse_args()
    if not PDF.is_file() or not PACKAGE_PDF.is_file():
        raise SystemExit("paper PDF or package PDF is missing")
    expected_environment = {
        "SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH,
        "FORCE_SOURCE_DATE": "1",
        "TZ": "UTC",
    }
    actual_environment = {key: os.environ.get(key) for key in expected_environment}
    if actual_environment != expected_environment:
        raise SystemExit(
            f"deterministic build environment mismatch: expected {expected_environment}, "
            f"observed {actual_environment}"
        )
    current_hash = sha256(PDF)
    if current_hash != EXPECTED_PDF_SHA256:
        raise SystemExit("current PDF is not the visually inspected deterministic build")
    if current_hash != sha256(PACKAGE_PDF):
        raise SystemExit("paper and package PDFs are not byte-identical")
    if current_hash.lower() not in {args.compile_hash_a.lower()} or args.compile_hash_a.lower() != args.compile_hash_b.lower():
        raise SystemExit("repeated compile hashes are not identical to the current PDF")
    if pages(PDF) != 9 or pages(PACKAGE_PDF) != 9:
        raise SystemExit("paper and package must each contain exactly nine pages")

    if RENDER_DIR.exists():
        resolved_root = ROOT.resolve()
        resolved_render = RENDER_DIR.resolve()
        if resolved_root not in resolved_render.parents:
            raise SystemExit("refusing to refresh render directory outside the worktree")
        shutil.rmtree(RENDER_DIR)
    RENDER_DIR.mkdir(parents=True)
    subprocess.run(["pdftoppm", "-r", "144", "-png", str(PDF), str(RENDER_DIR / "page")], check=True)
    renders = sorted(RENDER_DIR.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
    if len(renders) != 9:
        raise SystemExit(f"expected nine page renders, observed {len(renders)}")

    semantic = semantic_text(PDF)
    package_semantic = semantic_text(PACKAGE_PDF)
    if semantic != package_semantic:
        raise SystemExit("semantic extracted text differs between journal and package PDFs")
    render_rows = []
    for page_number, render in enumerate(renders, start=1):
        render_rows.append(
            {
                "page": page_number,
                "path": render.relative_to(ROOT).as_posix(),
                "bytes": render.stat().st_size,
                "sha256": sha256(render),
                "visual_status": "PASS" if args.confirm_visual_review else "PENDING",
                "finding": (
                    "Current-page visual review found no clipped or overlapping text, broken figure/table, unreadable glyph, or page-number defect."
                    if args.confirm_visual_review
                    else "Manual visual review required."
                ),
            }
        )
    record = {
        "schema": "p1_stage6_pdf_render_qa",
        "schema_version": 1,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "force_source_date": "1",
        "timezone": "UTC",
        "pdf_path": PDF.relative_to(ROOT).as_posix(),
        "package_pdf_path": PACKAGE_PDF.relative_to(ROOT).as_posix(),
        "pdf_sha256": current_hash,
        "package_pdf_sha256": sha256(PACKAGE_PDF),
        "raw_pdf_equality": True,
        "page_count": 9,
        "package_page_count": 9,
        "semantic_extracted_text_sha256": hashlib.sha256(semantic).hexdigest(),
        "package_semantic_extracted_text_sha256": hashlib.sha256(package_semantic).hexdigest(),
        "semantic_extracted_text_equal": True,
        "compilation": {
            "compile_hash_a": args.compile_hash_a.lower(),
            "compile_hash_b": args.compile_hash_b.lower(),
            "repeated_compiles_byte_identical": args.compile_hash_a.lower() == args.compile_hash_b.lower(),
        },
        "inspection_mode": (
            "manual visual review bound to exact PDF SHA-256 on 2026-08-29"
            if args.confirm_visual_review
            else "pending manual visual review"
        ),
        "inspection_basis_pdf_sha256": EXPECTED_PDF_SHA256 if args.confirm_visual_review else None,
        "inspected_by": "Codex independent nine-page visual QA" if args.confirm_visual_review else None,
        "inspection_status": "PASS" if args.confirm_visual_review else "PENDING",
        "inspected_pages": list(range(1, 10)) if args.confirm_visual_review else [],
        "renders": render_rows,
        "human_placeholders_retained": True,
        "built_in_pdf_integrity": "deferred because required human placeholders remain",
    }
    QA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"PDF render QA refreshed: status={record['inspection_status']} pages=9 hash={current_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
