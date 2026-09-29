#!/usr/bin/env python3
"""Render every Stage-7 page and bind an explicit visual review to exact bytes."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

from _stage7_release_common import (
    BUILD_IDENTITY_PATH,
    JOURNAL,
    PACKAGE,
    PACKAGE_MANIFEST_PATH,
    QA_PATH,
    RENDER_DIR,
    ROOT,
    atomic_write_json,
    load_json,
    main_error,
    page_count,
    render_pngs,
    require,
    require_environment,
    require_safe_tree,
    run_metadata_gate,
    semantic_sha256,
    semantic_text,
    sha256,
    tool_version,
    validate_build_identity,
)


def timezone_aware(value: str | None) -> bool:
    if not value:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def publish_renders(staging: Path, pdf_hash: str) -> Path | None:
    require_safe_tree(staging)
    require(staging.resolve().parent.parent == RENDER_DIR.parent.resolve(), "render staging location is invalid")
    backup: Path | None = None
    if RENDER_DIR.exists():
        require_safe_tree(RENDER_DIR)
        backup = RENDER_DIR.with_name(f"{RENDER_DIR.name}.previous-{pdf_hash[:12]}")
        require(not backup.exists(), f"prior render backup already exists; inspect it first: {backup}")
        RENDER_DIR.rename(backup)
    try:
        staging.rename(RENDER_DIR)
    except Exception:
        if backup is not None and backup.exists() and not RENDER_DIR.exists():
            backup.rename(RENDER_DIR)
        raise
    return backup


def execute() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm-visual-review", action="store_true")
    parser.add_argument("--inspected-by")
    parser.add_argument("--inspected-at-utc")
    parser.add_argument("--inspection-notes", default="")
    args = parser.parse_args()
    if args.confirm_visual_review:
        require(bool(args.inspected_by and args.inspected_by.strip()), "--inspected-by is required for PASS")
        require(timezone_aware(args.inspected_at_utc), "--inspected-at-utc must be timezone-aware for PASS")

    # Release metadata and manifest must exist before any render files are changed.
    run_metadata_gate("release")
    require_environment()
    identity = validate_build_identity()
    manifest = load_json(PACKAGE_MANIFEST_PATH)
    require(manifest.get("schema") == "p1_stage7_compact_release_manifest", "Stage-7 package schema changed")
    require(manifest.get("build_identity_sha256") == sha256(BUILD_IDENTITY_PATH), "package build identity hash is stale")
    require(manifest.get("pdf_sha256") == identity["pdf_sha256"], "package PDF identity is stale")

    journal_pdf = JOURNAL / "paper.pdf"
    package_pdf = PACKAGE / "paper.pdf"
    pdf_hash = sha256(journal_pdf)
    require(pdf_hash == sha256(package_pdf) == identity["pdf_sha256"], "journal/package/build PDF hashes differ")
    pages = page_count(journal_pdf)
    require(pages == page_count(package_pdf) == identity["page_count"], "journal/package/build page counts differ")
    require(semantic_text(journal_pdf) == semantic_text(package_pdf), "journal/package semantic PDF text differs")

    pdftoppm, pdftoppm_version = tool_version("pdftoppm", ["-v"])
    temporary_root = Path(tempfile.mkdtemp(prefix=".stage7-render-staging-", dir=RENDER_DIR.parent))
    staging_pages = temporary_root / "pages"
    backup: Path | None = None
    try:
        renders = render_pngs(journal_pdf, staging_pages, dpi=144)
        require(len(renders) == pages, "all pages were not rendered")
        rows: list[dict[str, object]] = []
        status = "PASS" if args.confirm_visual_review else "PENDING"
        for page_number, render in enumerate(renders, start=1):
            rows.append(
                {
                    "page": page_number,
                    "path": (RENDER_DIR / render.name).relative_to(ROOT).as_posix(),
                    "bytes": render.stat().st_size,
                    "sha256": sha256(render),
                    "visual_status": status,
                    "finding": (
                        "No clipped or overlapping text, broken figure/table, unreadable glyph, or page-number defect was found."
                        if args.confirm_visual_review
                        else "Independent visual inspection is required."
                    ),
                }
            )
        backup = publish_renders(staging_pages, pdf_hash)
        record = {
            "schema": "p1_stage7_pdf_render_qa",
            "schema_version": 1,
            "pdf_path": journal_pdf.relative_to(ROOT).as_posix(),
            "package_pdf_path": package_pdf.relative_to(ROOT).as_posix(),
            "pdf_sha256": pdf_hash,
            "package_pdf_sha256": sha256(package_pdf),
            "raw_pdf_equality": journal_pdf.read_bytes() == package_pdf.read_bytes(),
            "page_count": pages,
            "package_page_count": page_count(package_pdf),
            "semantic_extracted_text_sha256": semantic_sha256(journal_pdf),
            "package_semantic_extracted_text_sha256": semantic_sha256(package_pdf),
            "semantic_extracted_text_equal": semantic_text(journal_pdf) == semantic_text(package_pdf),
            "compilation": {
                "compile_hashes": identity["compile_pdf_sha256"],
                "repeated_compiles_byte_identical": len(set(identity["compile_pdf_sha256"])) == 1,
            },
            "render": {
                "executable": pdftoppm,
                "version": pdftoppm_version,
                "dpi": 144,
                "format": "PNG",
            },
            "inspection_status": status,
            "inspection_basis_pdf_sha256": pdf_hash if args.confirm_visual_review else None,
            "inspected_by": args.inspected_by.strip() if args.confirm_visual_review else None,
            "inspected_at_utc": args.inspected_at_utc if args.confirm_visual_review else None,
            "inspection_notes": args.inspection_notes.strip() if args.confirm_visual_review else None,
            "inspected_pages": list(range(1, pages + 1)) if args.confirm_visual_review else [],
            "renders": rows,
            "human_placeholders_retained": False,
            "built_in_pdf_integrity": "pass" if args.confirm_visual_review else "pending_visual_review",
        }
        atomic_write_json(QA_PATH, record)
    finally:
        if temporary_root.exists():
            resolved = temporary_root.resolve()
            if resolved.parent == RENDER_DIR.parent.resolve() and temporary_root.name.startswith(".stage7-render-staging-"):
                shutil.rmtree(temporary_root)

    backup_note = f" prior_renders_preserved={backup.relative_to(ROOT).as_posix()}" if backup else ""
    print(f"STAGE7 PDF RENDER QA {record['inspection_status']} pages={pages} pdf_sha256={pdf_hash}" + backup_note)
    return 0
if __name__ == "__main__":
    raise SystemExit(main_error("STAGE7 PDF RENDER QA BLOCKED", execute))
