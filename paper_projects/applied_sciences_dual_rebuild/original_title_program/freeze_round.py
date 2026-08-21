"""Create a deterministic audit manifest for an original-title manuscript round."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


INCLUDED_SUFFIXES = {".tex", ".bib", ".pdf", ".svg", ".png", ".json", ".jsonl", ".csv", ".md", ".py"}
EXCLUDED_DIRS = {"build_r1_smoke", "__pycache__", ".pytest_cache"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest().upper()


def collect(round_dir: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(round_dir.rglob("*")):
        if not path.is_file() or path.name == "ROUND_AUDIT.json":
            continue
        relative = path.relative_to(round_dir)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.suffix.lower() not in INCLUDED_SUFFIXES:
            continue
        rows.append(
            {
                "path": relative.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("round_dir", type=Path)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    round_dir = args.round_dir.resolve(strict=True)
    files = collect(round_dir)
    required = {"paper_applsci.tex", "build/paper_applsci.pdf"}
    present = {str(row["path"]) for row in files}
    missing = sorted(required - present)
    payload = {
        "schema": "original-title-round-audit-v1",
        "label": args.label,
        "round_directory": round_dir.as_posix(),
        "status": "PASS" if not missing else "FAIL",
        "missing_required_files": missing,
        "file_count": len(files),
        "files": files,
    }
    output = round_dir / "ROUND_AUDIT.json"
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "file_count": len(files), "output": str(output)}))
    if missing:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
