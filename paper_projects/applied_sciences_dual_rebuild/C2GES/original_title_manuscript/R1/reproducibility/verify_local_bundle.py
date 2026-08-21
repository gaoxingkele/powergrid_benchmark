#!/usr/bin/env python3
"""Fail closed if any locally manifested C2GES artifact is missing or changed."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "paper_projects").is_dir())
MANIFEST = HERE.parent / "bundle_manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    seen = set()
    total = 0
    for item in manifest["artifacts"]:
        rel = item["path"]
        if rel in seen:
            errors.append(f"duplicate path: {rel}")
            continue
        seen.add(rel)
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing: {rel}")
            continue
        total += path.stat().st_size
        if path.stat().st_size != item["bytes"]:
            errors.append(f"size mismatch: {rel}")
        elif sha256(path) != item["sha256"]:
            errors.append(f"hash mismatch: {rel}")
    if len(seen) != manifest["artifact_count"]:
        errors.append("artifact count mismatch")
    if total != manifest["total_bytes"]:
        errors.append("total byte count mismatch")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {len(seen)} local artifacts, {total} bytes, all SHA-256 hashes verified.")
    if not manifest.get("public_doi"):
        print("HUMAN BLOCKER: permanent public DOI/URL and license review remain required before submission.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
