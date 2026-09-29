#!/usr/bin/env python3
"""Build the complete, hash-manifested P1 Stage-7 submission-material ZIP."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _stage7_release_common import (
    BUILD_IDENTITY_PATH,
    MAX_SUBMISSION_FILE_BYTES,
    METADATA_PATH,
    PACKAGE_ROOT,
    QA_PATH,
    ROOT,
    SOURCE_DATE_EPOCH,
    atomic_write_json,
    forbidden_path_reason,
    load_json,
    main_error,
    require,
    require_environment,
    require_safe_tree,
    sha256,
)


REPO_ROOT = ROOT.parents[1]
DELIVERY_ROOT = ROOT / "final_delivery"
DEFAULT_ZIP = DELIVERY_ROOT / "P1_IEEE_ACCESS_STAGE7_COMPLETE.zip"
DEFAULT_SIDECAR = DELIVERY_ROOT / "P1_IEEE_ACCESS_STAGE7_COMPLETE.manifest.json"
TERMINAL_VALIDATOR = ROOT / "scripts" / "validate_stage7_release.py"
RUN_ROOTS = (
    ROOT / "experiments" / "p1_ieee_access_upgrade_v2",
    ROOT / "experiments" / "p1_ieee_access_upgrade_v2_stage6_attempt5",
)
RAW_DATA_NOTICE = REPO_ROOT / "data" / "public_datasets" / "production_cost" / "rts-gmlc" / "README.md"
RAW_DATA_FILES = {
    "RTS_Data/timeseries_data_files/Load/DAY_AHEAD_regional_Load.csv": "6efb6e3e06f7f1cee0d59eaf33768e06c33c737beb875676433850d8659943ee",
    "RTS_Data/timeseries_data_files/WIND/DAY_AHEAD_wind.csv": "b933f810511ce3d2128c490e4b230defcdc3c15ed4db0838c6fd4c62640e2208",
    "RTS_Data/timeseries_data_files/PV/DAY_AHEAD_pv.csv": "bfede6e558df5ea0f244b6326940a4ee0b95138643aa8a062897c67134c9c185",
    "RTS_Data/SourceData/branch.csv": "2f8f80f6f95ca46c2997646d56892436b50d7fb81163b680d06767bc3c1b179f",
}
RAW_DATA_ROOT = REPO_ROOT / "data" / "public_datasets" / "production_cost" / "rts-gmlc"
ROOT_REPORTS = (
    "P1_CITATION_VERIFICATION_V2.md",
    "P1_LITERATURE_GAP_V2.md",
    "STAGE7_HARNESSBANK_GATE_CARD.md",
    "CHECKPOINT_20260830.md",
)
MANUSCRIPT_RECORDS = (
    "MANUSCRIPT.md",
    "DEEP_REVISION_EVIDENCE.md",
    "STAGE6_METHOD_TO_EVIDENCE_AUDIT.md",
    "STAGE7_FINALIZER_FAILURE_PATH_EVIDENCE.json",
    "STAGE7_IEEE_ACCESS_OFFICIAL_POLICY_AUDIT_20260830.md",
    "STAGE7_HUMAN_METADATA.json",
    "STAGE7_BUILD_IDENTITY.json",
    "STAGE7_PDF_RENDER_QA.json",
    "SUPPLEMENTARY_METHODS_AND_AUDIT.md",
    "TABLE_TO_CONFIG_MANIFEST.md",
)


def run_terminal_gate() -> None:
    completed = subprocess.run(
        [sys.executable, "-B", str(TERMINAL_VALIDATOR)],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(completed.returncode == 0, f"terminal Stage-7 gate blocked bundle creation:\n{completed.stdout.rstrip()}")


def add_tree(rows: dict[str, Path], source_root: Path, archive_root: str) -> None:
    require_safe_tree(source_root)
    for source in sorted(source_root.rglob("*"), key=lambda item: item.relative_to(source_root).as_posix()):
        if not source.is_file():
            continue
        relative = source.relative_to(source_root).as_posix()
        reason = forbidden_path_reason(relative)
        if reason in {"cache path", "TeX auxiliary/log file"}:
            continue
        require(reason is None, f"forbidden bundle input ({reason}): {source}")
        archive_path = f"{archive_root.rstrip('/')}/{relative}"
        require(archive_path not in rows, f"duplicate bundle archive path: {archive_path}")
        rows[archive_path] = source


def collect_files() -> dict[str, Path]:
    rows: dict[str, Path] = {}
    add_tree(rows, PACKAGE_ROOT, "01_submission_package")
    for run_root in RUN_ROOTS:
        add_tree(rows, run_root, f"02_reproducibility/{run_root.name}")
    add_tree(rows, ROOT / "manuscript" / "derived_tables", "02_reproducibility/derived_tables")
    add_tree(rows, ROOT / "manuscript" / "figures", "02_reproducibility/figure_sources")
    add_tree(rows, ROOT / "scripts", "02_reproducibility/release_and_validation_scripts")

    for name in ROOT_REPORTS:
        source = ROOT / name
        require(source.is_file(), f"required project record is missing: {name}")
        rows[f"03_audit_records/{name}"] = source
    for name in MANUSCRIPT_RECORDS:
        source = ROOT / "manuscript" / name
        require(source.is_file(), f"required manuscript record is missing: {name}")
        rows[f"03_audit_records/manuscript/{name}"] = source

    require(RAW_DATA_NOTICE.is_file(), "RTS-GMLC data-use notice is missing")
    rows["04_input_data/RTS-GMLC/README_WITH_DATA_USE_NOTICE.md"] = RAW_DATA_NOTICE
    for relative, expected_hash in RAW_DATA_FILES.items():
        source = RAW_DATA_ROOT / Path(relative)
        require(source.is_file(), f"required RTS-GMLC input is missing: {relative}")
        require(sha256(source) == expected_hash, f"RTS-GMLC input hash changed: {relative}")
        rows[f"04_input_data/RTS-GMLC/{relative}"] = source
    return dict(sorted(rows.items()))


def zip_datetime() -> tuple[int, int, int, int, int, int]:
    instant = datetime.fromtimestamp(int(SOURCE_DATE_EPOCH), tz=timezone.utc)
    second = instant.second - instant.second % 2
    return instant.year, instant.month, instant.day, instant.hour, instant.minute, second


def manifest_rows(files: dict[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "path": archive_path,
            "source": source.relative_to(REPO_ROOT).as_posix(),
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
        }
        for archive_path, source in files.items()
    ]


def write_zip(destination: Path, files: dict[str, Path], payload_manifest: dict[str, Any]) -> None:
    timestamp = zip_datetime()
    with zipfile.ZipFile(destination, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for archive_path, source in files.items():
            info = zipfile.ZipInfo(archive_path, date_time=timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        info = zipfile.ZipInfo("BUNDLE_MANIFEST.json", date_time=timestamp)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        manifest_bytes = (json.dumps(payload_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        archive.writestr(info, manifest_bytes, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def publish_file(staged: Path, destination: Path, *, replace_existing: bool) -> Path | None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    resolved_parent = destination.parent.resolve()
    require(resolved_parent == DELIVERY_ROOT.resolve(), "bundle destination must remain in final_delivery")
    backup: Path | None = None
    if destination.exists():
        require(replace_existing, f"destination exists; use --replace-existing after inspecting it: {destination}")
        require(destination.is_file() and not destination.is_symlink(), "existing destination is not a regular file")
        backup = destination.with_name(f"{destination.name}.previous-{sha256(destination)[:12]}")
        require(not backup.exists(), f"bundle backup already exists: {backup}")
        destination.rename(backup)
    try:
        os.replace(staged, destination)
    except Exception:
        if backup is not None and backup.exists() and not destination.exists():
            backup.rename(destination)
        raise
    return backup


def execute() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replace-existing", action="store_true")
    args = parser.parse_args()
    require_environment()
    run_terminal_gate()
    files = collect_files()
    rows = manifest_rows(files)
    payload_manifest = {
        "schema": "p1_stage7_complete_submission_bundle_manifest",
        "schema_version": 1,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "manifest_covers_payload_excluding_itself": True,
        "payload_file_count": len(rows),
        "human_metadata_sha256": sha256(METADATA_PATH),
        "build_identity_sha256": sha256(BUILD_IDENTITY_PATH),
        "pdf_render_qa_sha256": sha256(QA_PATH),
        "stage7_package_manifest_sha256": sha256(PACKAGE_ROOT / "PACKAGE_MANIFEST.json"),
        "raw_input_notice_included": True,
        "files": rows,
    }

    DELIVERY_ROOT.mkdir(parents=True, exist_ok=True)
    for destination in (DEFAULT_ZIP, DEFAULT_SIDECAR):
        if destination.exists():
            require(args.replace_existing, f"destination exists; use --replace-existing after inspecting it: {destination}")
            require(destination.is_file() and not destination.is_symlink(), "existing destination is not a regular file")
            prospective_backup = destination.with_name(f"{destination.name}.previous-{sha256(destination)[:12]}")
            require(not prospective_backup.exists(), f"bundle backup already exists: {prospective_backup}")
    temporary_zip: Path | None = None
    temporary_sidecar: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=DELIVERY_ROOT, prefix=".p1-stage7-bundle-", suffix=".zip.tmp", delete=False) as handle:
            temporary_zip = Path(handle.name)
        write_zip(temporary_zip, files, payload_manifest)
        require(temporary_zip.stat().st_size < MAX_SUBMISSION_FILE_BYTES, "complete bundle reaches the 40 MB upload limit")
        with zipfile.ZipFile(temporary_zip, mode="r") as archive:
            require(archive.testzip() is None, "ZIP CRC validation failed")
            expected_names = [*files.keys(), "BUNDLE_MANIFEST.json"]
            require(archive.namelist() == expected_names, "ZIP file order or membership differs from the manifest")

        sidecar = {
            **payload_manifest,
            "zip_path": DEFAULT_ZIP.relative_to(ROOT).as_posix(),
            "zip_bytes": temporary_zip.stat().st_size,
            "zip_sha256": sha256(temporary_zip),
        }
        with tempfile.NamedTemporaryFile(dir=DELIVERY_ROOT, prefix=".p1-stage7-sidecar-", suffix=".json.tmp", delete=False) as handle:
            temporary_sidecar = Path(handle.name)
        atomic_write_json(temporary_sidecar, sidecar)
        zip_backup = publish_file(temporary_zip, DEFAULT_ZIP, replace_existing=args.replace_existing)
        temporary_zip = None
        sidecar_backup = publish_file(temporary_sidecar, DEFAULT_SIDECAR, replace_existing=args.replace_existing)
        temporary_sidecar = None
    finally:
        for temporary in (temporary_zip, temporary_sidecar):
            if temporary is not None and temporary.exists():
                temporary.unlink()

    print(
        "STAGE7 COMPLETE BUNDLE PASS "
        f"files={len(rows)} bytes={sidecar['zip_bytes']} zip_sha256={sidecar['zip_sha256']}"
    )
    if zip_backup or sidecar_backup:
        print("Prior deliverables were preserved as hash-suffixed backups.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_error("STAGE7 COMPLETE BUNDLE BLOCKED", execute))
