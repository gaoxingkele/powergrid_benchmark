"""Verify a semantic-release manifest beneath any supplied package root."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest["schema_version"] != "ma-sqlgrid-semantic-portable-release-v1":
        raise ValueError("Unsupported manifest schema")

    checked = 0
    for item in [manifest["root_marker"], *manifest["artifacts"]]:
        portable = PurePosixPath(item["path"])
        if portable.is_absolute() or ".." in portable.parts or ":" in item["path"]:
            raise ValueError(f"Non-portable path: {item['path']}")
        path = root.joinpath(*portable.parts).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"Path escapes package root: {item['path']}") from exc
        if not path.is_file() or path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise ValueError(f"Artifact identity mismatch: {item['path']}")
        checked += 1
    report = {
        "schema_version": "ma-sqlgrid-portable-clean-verification-v1",
        "status": "PASS",
        "manifest_sha256": sha256(args.manifest),
        "checked_files_including_root_marker": checked,
        "repo_root": str(root),
        "invariants": manifest["invariants"],
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PORTABLE_RELEASE_VERIFY PASS checked={checked}")


if __name__ == "__main__":
    main()
