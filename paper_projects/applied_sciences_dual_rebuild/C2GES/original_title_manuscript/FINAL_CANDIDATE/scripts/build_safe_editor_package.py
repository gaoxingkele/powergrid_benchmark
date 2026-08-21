"""Build and verify the deterministic C2GES safe-editor ZIP dry run."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PREFIX = "C2GES_SAFE_EDITOR"
PACKAGE_DIR = ROOT / "packages"
ZIP_PATH = PACKAGE_DIR / "C2GES_Applied_Sciences_SAFE_EDITOR_DRY_RUN.zip"
OUT = ROOT / "SAFE_EDITOR_PACKAGE_MANIFEST.json"
FIXED_ZIP_TIME = (2026, 8, 8, 0, 0, 0)


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def collect() -> dict[str, tuple[Path, str]]:
    selected: dict[str, tuple[Path, str]] = {}

    def add(path: Path, archive_rel: str, role: str) -> None:
        if not path.is_file():
            raise FileNotFoundError(path)
        if "__pycache__" in path.parts or path.suffix.lower() == ".pyc":
            raise RuntimeError(f"python cache refused: {path}")
        if archive_rel in selected:
            raise RuntimeError(f"duplicate archive path: {archive_rel}")
        selected[archive_rel] = (path, role)

    for name, role in {
        "paper_applsci.tex": "manuscript source",
        "references_cited_verified.bib": "cited bibliography",
        "build_original_title.ps1": "LaTeX build entry point",
        "COVER_LETTER_DRAFT.md": "editor cover-letter draft",
        "AUTHOR_METADATA_CONFIRMATION_2026-08-08.md": "author-metadata confirmation record",
        "FINAL_RESPONSE_MATRIX.md": "authoritative Round-3 response matrix",
        "SUBMISSION_HOLDS.md": "manual-hold register",
        "FINAL_CITATION_CONTEXT_AUDIT.json": "23-item citation-context audit",
        "FINAL_VISUAL_QA.md": "current-PDF page-by-page visual QA",
        "SUPPLEMENT_ALLOWLIST.json": "local two-compartment provenance allowlist",
    }.items():
        add(ROOT / name, name, role)
    add(ROOT / "build_r3" / "paper_applsci.pdf", "build_r3/paper_applsci.pdf", "compiled manuscript PDF")

    for directory, role in (("Definitions", "MDPI template dependency"), ("figures", "code-native figure/lineage"), ("scripts", "reproduction and package code")):
        for path in sorted((ROOT / directory).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix.lower() != ".pyc":
                add(path, path.relative_to(ROOT).as_posix(), role)

    transferable = ROOT / "supplementary" / "transferable"
    for path in sorted(transferable.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix.lower() != ".pyc":
            add(path, path.relative_to(ROOT).as_posix(), "transferable supplementary evidence")
    return selected


def main() -> None:
    selected = collect()
    failures = []
    for archive_rel, (path, _) in selected.items():
        lower = archive_rel.casefold()
        if "restricted_local_only" in lower or path.name == "predictions.jsonl":
            failures.append({"restricted_file_selected": archive_rel})
        if path.name in {"nerc_full_pdf_benchmark_v0_3.jsonl", "nerc_full_pdf_dev_v0_3.jsonl", "nerc_full_pdf_test_v0_3.jsonl"}:
            failures.append({"extracted_dataset_selected": archive_rel})
        if path.name == "R2_TO_R3_RESPONSE_MATRIX_DRAFT.md":
            failures.append({"obsolete_draft_selected": archive_rel})
        if path.suffix.lower() == ".pdf" and not (
            archive_rel == "build_r3/paper_applsci.pdf"
            or archive_rel.startswith("figures/")
            or archive_rel.startswith("Definitions/")
        ):
            failures.append({"unapproved_pdf_selected": archive_rel})
    if failures:
        raise SystemExit(json.dumps({"status": "FAIL", "failures": failures}, indent=2))

    records = []
    for archive_rel in sorted(selected):
        path, role = selected[archive_rel]
        records.append(
            {
                "path": archive_rel,
                "bytes": path.stat().st_size,
                "sha256": digest(path),
                "role": role,
            }
        )
    content_manifest = {
        "schema": "c2ges-safe-editor-package-content-v1",
        "status": "PASS",
        "manifest_self_excluded_from_file_inventory": True,
        "file_count": len(records),
        "files": records,
        "excluded": [
            "supplementary/restricted_local_only/** including predictions.jsonl",
            "source PDFs",
            "full extracted development/test/benchmark JSONL",
            "R2_TO_R3_RESPONSE_MATRIX_DRAFT.md",
            "__pycache__ and *.pyc",
        ],
        "manual_holds_remain": [
            "file-level rights decisions",
            "repository synchronization/license/tag/archive/fresh-clone receipt",
            "editorial decision on aspirational exact title",
            "qualified human power-grid validation and title-concordant external evidence for any stronger effectiveness or safety claim",
        ],
    }
    manifest_bytes = (json.dumps(content_manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for archive_rel in sorted(selected):
            path, _ = selected[archive_rel]
            info = zipfile.ZipInfo(f"{PREFIX}/{archive_rel}", FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        info = zipfile.ZipInfo(f"{PREFIX}/PACKAGE_CONTENT_MANIFEST.json", FIXED_ZIP_TIME)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, manifest_bytes, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = set(archive.namelist())
        expected_names = {f"{PREFIX}/{record['path']}" for record in records} | {f"{PREFIX}/PACKAGE_CONTENT_MANIFEST.json"}
        if names != expected_names:
            failures.append({"zip_exact_set_mismatch": {"missing": sorted(expected_names - names), "extra": sorted(names - expected_names)}})
        for record in records:
            data = archive.read(f"{PREFIX}/{record['path']}")
            if len(data) != record["bytes"] or digest_bytes(data) != record["sha256"]:
                failures.append({"zip_content_mismatch": record["path"]})
        if archive.read(f"{PREFIX}/PACKAGE_CONTENT_MANIFEST.json") != manifest_bytes:
            failures.append({"embedded_manifest_mismatch": True})
    status = "PASS" if not failures else "FAIL"
    report = {
        "schema": "c2ges-safe-editor-zip-dry-run-v1",
        "status": status,
        "zip_path": ZIP_PATH.relative_to(ROOT).as_posix(),
        "zip_bytes": ZIP_PATH.stat().st_size,
        "zip_sha256": digest(ZIP_PATH),
        "embedded_manifest_sha256": digest_bytes(manifest_bytes),
        "packaged_file_count_excluding_embedded_manifest": len(records),
        "zip_entry_count": len(records) + 1,
        "restricted_prediction_in_zip": False,
        "source_pdf_or_extracted_text_in_zip": False,
        "failures": failures,
    }
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
