#!/usr/bin/env python3
"""Create a metadata-bound, dynamic Stage-7 release without touching Stage 6."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from _stage7_release_common import (
    BUILD_COMMAND,
    BUILD_IDENTITY_PATH,
    EXPECTED_ENVIRONMENT,
    FORBIDDEN_SUFFIXES,
    JOURNAL,
    MAX_SUBMISSION_FILE_BYTES,
    METADATA_PATH,
    PACKAGE_ROOT,
    ROOT,
    SAMPLE_PHOTO_SHA256,
    atomic_write_json,
    canonical_text_sha256,
    forbidden_path_reason,
    main_error,
    page_count,
    publish_directory,
    require,
    require_environment,
    require_no_placeholders,
    require_safe_tree,
    run_metadata_gate,
    semantic_sha256,
    sha256,
    validate_build_identity,
)


EXCLUDED_EXPLICITLY = {"body.generated.md", "paper_narrative_revision.pdf"}


def excluded(path: Path) -> tuple[bool, str | None]:
    relative = path.relative_to(JOURNAL).as_posix()
    if relative in EXCLUDED_EXPLICITLY:
        return True, "nonrelease manuscript derivative"
    lowered = path.name.lower()
    if any(lowered.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
        return True, "TeX auxiliary/log output"
    if sha256(path) in SAMPLE_PHOTO_SHA256:
        return True, "bundled IEEE sample portrait"
    return False, None


def collect_source_files() -> tuple[list[Path], list[dict[str, str]]]:
    require_safe_tree(JOURNAL)
    files: list[Path] = []
    exclusions: list[dict[str, str]] = []
    for path in sorted(JOURNAL.rglob("*"), key=lambda item: item.relative_to(JOURNAL).as_posix()):
        if not path.is_file():
            continue
        skip, reason = excluded(path)
        if skip:
            exclusions.append({"path": path.relative_to(JOURNAL).as_posix(), "reason": str(reason)})
            continue
        relative = path.relative_to(JOURNAL).as_posix()
        require(forbidden_path_reason(relative) is None, f"forbidden release source path: {relative}")
        files.append(path)
    require(files, "no release source files were selected")
    return files, exclusions


def execute() -> int:
    # The package cannot be created until author-supplied facts pass independently.
    run_metadata_gate("prebuild")
    require_environment()
    identity = validate_build_identity()
    source_files, exclusions = collect_source_files()

    staging = Path(tempfile.mkdtemp(prefix=".stage7-release-staging-", dir=ROOT))
    staging_payload = staging / "manuscript"
    try:
        staging_payload.mkdir(parents=True)
        entries: list[dict[str, object]] = []
        for source in source_files:
            relative = source.relative_to(JOURNAL)
            destination = staging_payload / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            require(sha256(source) == sha256(destination), f"source/package copy differs: {relative.as_posix()}")
            require(
                destination.stat().st_size < MAX_SUBMISSION_FILE_BYTES,
                f"release file reaches the 40 MB submission limit: {relative.as_posix()}",
            )
            entries.append(
                {
                    "path": (Path("manuscript") / relative).as_posix(),
                    "source": source.relative_to(ROOT).as_posix(),
                    "bytes": destination.stat().st_size,
                    "sha256": sha256(destination),
                }
            )

        staged_pdf = staging_payload / "paper.pdf"
        staged_tex = staging_payload / "paper.tex"
        require(identity["pdf_sha256"] == sha256(staged_pdf), "packaged PDF differs from build identity")
        require(identity["tex_sha256"] == sha256(staged_tex), "packaged TeX differs from build identity")
        require(identity["page_count"] == page_count(staged_pdf), "packaged PDF page count differs")
        require(identity["semantic_text_sha256"] == semantic_sha256(staged_pdf), "packaged PDF semantic hash differs")
        require_no_placeholders(staged_pdf, pdf=True)
        require_no_placeholders(staged_tex)

        manifest = {
            "schema": "p1_stage7_compact_release_manifest",
            "schema_version": 1,
            "source_date_epoch": EXPECTED_ENVIRONMENT["SOURCE_DATE_EPOCH"],
            "force_source_date": EXPECTED_ENVIRONMENT["FORCE_SOURCE_DATE"],
            "timezone": EXPECTED_ENVIRONMENT["TZ"],
            "build_command": BUILD_COMMAND,
            "build_passes": 3,
            "build_identity_path": BUILD_IDENTITY_PATH.relative_to(ROOT).as_posix(),
            "build_identity_sha256": sha256(BUILD_IDENTITY_PATH),
            "human_metadata_path": METADATA_PATH.relative_to(ROOT).as_posix(),
            "human_metadata_sha256": sha256(METADATA_PATH),
            "pdf_sha256": identity["pdf_sha256"],
            "pdf_bytes": staged_pdf.stat().st_size,
            "page_count": identity["page_count"],
            "semantic_text_sha256": identity["semantic_text_sha256"],
            "tex_sha256": identity["tex_sha256"],
            "tex_canonical_sha256": canonical_text_sha256(staged_tex),
            "payload_file_count": len(entries),
            "max_submission_file_bytes": MAX_SUBMISSION_FILE_BYTES,
            "explicit_human_placeholders_retained": False,
            "stage7_human_metadata_complete": True,
            "built_in_pdf_integrity": "pass",
            "excluded_nonrelease_files": exclusions,
            "files": entries,
        }
        atomic_write_json(staging / "PACKAGE_MANIFEST.json", manifest)
        require_safe_tree(staging)
        backup = publish_directory(staging, PACKAGE_ROOT)
        staging = Path()
    finally:
        if staging != Path() and staging.exists():
            resolved = staging.resolve()
            if resolved.parent == ROOT.resolve() and staging.name.startswith(".stage7-release-staging-"):
                shutil.rmtree(staging)

    backup_note = f" prior_package_preserved={backup.relative_to(ROOT).as_posix()}" if backup else ""
    print(
        "STAGE7 RELEASE BUILD PASS "
        f"files={manifest['payload_file_count']} pdf_sha256={manifest['pdf_sha256']}" + backup_note
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main_error("STAGE7 RELEASE BUILD BLOCKED", execute))
