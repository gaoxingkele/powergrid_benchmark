#!/usr/bin/env python3
"""Recreate the compact Stage-6 submission payload and its hash manifest."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript" / "journal_submission"
RELEASE_ROOT = ROOT / "release_package"
PAYLOAD = RELEASE_ROOT / "manuscript"
MANIFEST = RELEASE_ROOT / "PACKAGE_MANIFEST.json"
SOURCE_DATE_EPOCH = "1787867025"
EXCLUDED_EXPLICITLY = {"body.generated.md", "paper_narrative_revision.pdf"}
EXCLUDED_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def excluded(path: Path) -> bool:
    relative = path.relative_to(SOURCE).as_posix()
    if relative in EXCLUDED_EXPLICITLY:
        return True
    return any(path.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)


def main() -> int:
    if not SOURCE.is_dir():
        raise SystemExit("journal-submission source directory is missing")
    source_files = sorted((path for path in SOURCE.rglob("*") if path.is_file() and not excluded(path)), key=lambda p: p.relative_to(SOURCE).as_posix())
    if len(source_files) != 87:
        raise SystemExit(f"fail-closed: compact payload must contain exactly 87 files, observed {len(source_files)}")

    resolved_root = ROOT.resolve()
    resolved_payload = PAYLOAD.resolve()
    if resolved_root not in resolved_payload.parents:
        raise SystemExit("refusing to rebuild payload outside the worktree")
    if PAYLOAD.exists():
        shutil.rmtree(PAYLOAD)
    PAYLOAD.mkdir(parents=True)

    entries: list[dict[str, object]] = []
    for source in source_files:
        relative = source.relative_to(SOURCE)
        destination = PAYLOAD / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        entries.append(
            {
                "path": (Path("manuscript") / relative).as_posix(),
                "source": source.relative_to(ROOT).as_posix(),
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )

    manifest = {
        "schema": "p1_stage6_compact_release_manifest",
        "schema_version": 1,
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "force_source_date": SOURCE_DATE_EPOCH,
        "payload_file_count": len(entries),
        "explicit_human_placeholders_retained": True,
        "built_in_pdf_integrity": "deferred because required human placeholders remain",
        "excluded_nonrelease_files": sorted(EXCLUDED_EXPLICITLY),
        "files": entries,
    }
    RELEASE_ROOT.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"release payload refreshed: files={len(entries)} manifest={MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
