#!/usr/bin/env python3
"""Generate or verify the current-layout release checksum manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


METADATA = Path(__file__).resolve().parent
MARKER_NAME = "C2GES_RELEASE_MARKER.json"


def project_root(start: Path) -> Path:
    """Locate the release root by its marker.

    Walking up to the marker rather than taking a fixed parent keeps this working
    after the project is reached through a directory junction, where resolve()
    renames the root and a name-based test would pick the wrong verification file.
    """
    for candidate in (start, *start.parents):
        if (candidate / MARKER_NAME).is_file():
            return candidate
    raise RuntimeError(f"no {MARKER_NAME} above {start}")


PROJECT = project_root(METADATA)
PROJECT_NAME = json.loads((PROJECT / MARKER_NAME).read_text(encoding="utf-8-sig")).get("project", PROJECT.name)
CHECKSUMS = METADATA / "FILE_SHA256SUMS.txt"
MANIFEST = METADATA / "RELEASE_MANIFEST.json"
SCOPES = ("01_Manuscript", "02_Revision_and_QA", "03_Reproducibility")
EXCLUDED_SUFFIXES = {".aux", ".bbl", ".blg", ".log", ".out", ".pyc"}
EXCLUDED_NAMES = {"FILE_SHA256SUMS.txt", "RELEASE_MANIFEST.json"}
EXCLUDED_PARTS = {
    "__pycache__", "visual_qa", "source_pdfs_private", "derived_private",
    # Working copies that are not release content: a dated template backup, the
    # unpacked MDPI template, and the assets extracted for the Word rendering.
    "Definitions_20260623_backup", "_mdpi_template_acs", "_docx_assets",
}
EXCLUDED_FILE_SUFFIXES = ("_mdpi_template_acs.zip",)
# Verbatim third-party passages: the sealed RSI record keeps the selected and
# reference text so the run can be re-scored offline, and third-party
# redistribution permission has not been established.  Its rights-safe companion
# (identifiers, budgets, realised lengths and scores only) is shipped instead.
EXCLUDED_EXACT_PATHS = {("03_Reproducibility", "Data", "rsi_path_v1", "run", "SEALED_CHOICES.jsonl")}
BINARY_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".zip", ".docx", ".eps"}


def sha256(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() not in BINARY_SUFFIXES:
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest().upper()


def included_files() -> list[Path]:
    files: list[Path] = []
    for scope in SCOPES:
        root = PROJECT / scope
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(PROJECT)
            if path.name in EXCLUDED_NAMES or path.suffix.lower() in EXCLUDED_SUFFIXES:
                continue
            if path.name.endswith(EXCLUDED_FILE_SUFFIXES):
                continue
            if relative.parts in EXCLUDED_EXACT_PATHS:
                continue
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if relative.parts[:3] in {
                ("01_Manuscript", "LaTeX", "paper_applsci.pdf"),
                ("01_Manuscript", "Supplementary", "supplementary_materials.pdf"),
            }:
                continue
            files.append(relative)
    return sorted(files, key=lambda value: value.as_posix().lower())


def parse_checksums() -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in CHECKSUMS.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        if relative in rows:
            raise AssertionError(f"duplicate checksum path: {relative}")
        rows[relative] = expected
    return rows


def check() -> dict[str, object]:
    expected = parse_checksums()
    actual_paths = {path.as_posix() for path in included_files()}
    listed_paths = set(expected)
    missing = sorted(listed_paths - actual_paths)
    unlisted = sorted(actual_paths - listed_paths)
    mismatches = []
    for relative in sorted(listed_paths & actual_paths):
        if sha256(PROJECT / relative) != expected[relative]:
            mismatches.append(relative)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    checksum_hash_matches = manifest["checksum_list_sha256"] == sha256(CHECKSUMS)
    count_matches = manifest["file_count"] == len(expected)
    result = {
        "status": "PASS" if not missing and not unlisted and not mismatches and checksum_hash_matches and count_matches else "FAIL",
        "files_checked": len(expected),
        "missing": missing,
        "unlisted": unlisted,
        "hash_mismatches": mismatches,
        "checksum_hash_matches": checksum_hash_matches,
        "count_matches": count_matches,
    }
    return result


def generate(route: str = "diagnostic") -> None:
    files = included_files()
    lines = [f"{sha256(PROJECT / relative)}  {relative.as_posix()}" for relative in files]
    CHECKSUMS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if PROJECT_NAME == "C2GES" and route == "diagnostic":
        verification_name = "C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json"
    else:
        verification_name = "C2GES_PUBLIC_VERIFICATION.json" if PROJECT_NAME == "C2GES" else "MA_SQLGRID_PUBLIC_VERIFICATION.json"
    verification_path = PROJECT / "02_Revision_and_QA" / "04_Build_Reports" / verification_name
    verification = json.loads(verification_path.read_text(encoding="utf-8"))
    gates = verification.get("external_gates", {})
    manifest = {
        "schema_version": "cmc-current-layout-release-v1",
        "paper": PROJECT.name,
        "release_baseline": "2026-09-12 diagnostic submission v2" if route == "diagnostic" else "2026-08-23 revision",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "release_scopes": list(SCOPES),
        "file_count": len(files),
        "total_bytes": sum((PROJECT / relative).stat().st_size for relative in files),
        "checksum_list": str(CHECKSUMS.relative_to(PROJECT)).replace("\\", "/"),
        "checksum_list_sha256": sha256(CHECKSUMS),
        "hash_policy": "SHA-256 over exact binary bytes; text line endings normalized to LF",
        "technical_verification": {
            "report": str(verification_path.relative_to(PROJECT)).replace("\\", "/"),
            "status": verification.get("technical_status", verification.get("status")),
        },
        "submission_ready": verification.get("submission_ready", False),
        "external_gates": gates,
        "exclusions": [
            "90_Archive is outside the release scope",
            "LaTeX intermediates, Python bytecode, and rendered visual-QA page images",
            "the checksum list and release manifest themselves to avoid circular hashes",
            "restricted raw source assets identified in the data-rights notice",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result = check()
    if result["status"] != "PASS":
        raise AssertionError(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--route", choices=("confirmatory", "diagnostic"), default="diagnostic")
    args = parser.parse_args()
    if args.check:
        result = check()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        raise SystemExit(0 if result["status"] == "PASS" else 1)
    generate(args.route)


if __name__ == "__main__":
    main()
