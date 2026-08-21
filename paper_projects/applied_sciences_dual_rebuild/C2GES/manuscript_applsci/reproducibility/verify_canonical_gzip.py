#!/usr/bin/env python3
"""Verify the currently bound canonical gzip and its decompressed payload."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve()
MANUSCRIPT = HERE.parent.parent
ROOT = next(p for p in HERE.parents if (p / "paper_projects").is_dir())
RECORD = MANUSCRIPT / "evidence/canonical_gzip_transition.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    artifact = ROOT / record["artifact_path"]
    compressed = artifact.read_bytes()
    payload = gzip.decompress(compressed)
    checks = {
        "compressed_sha256": digest(compressed) == record["current_compressed_sha256"],
        "compressed_bytes": len(compressed) == record["current_compressed_bytes"],
        "decompressed_sha256": digest(payload) == record["current_decompressed_sha256"],
        "decompressed_bytes": len(payload) == record["current_decompressed_bytes"],
        "decompressed_lines": payload.count(b"\n") == record["current_decompressed_line_count"],
    }
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
