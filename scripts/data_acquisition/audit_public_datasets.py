"""Audit local public-dataset cache against the manifest."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "public_datasets" / "manifests" / "public_dataset_manifest.csv"


def main() -> int:
    failures = 0
    rows = list(csv.DictReader(MANIFEST.open(newline="", encoding="utf-8")))
    print(f"manifest rows: {len(rows)}")
    for row in rows:
        dataset_id = row["dataset_id"]
        status = row["status"]
        local_path = row["local_path"]
        if not local_path:
            print(f"planned: {dataset_id} has no local path")
            continue
        path = ROOT / local_path
        exists = path.exists()
        if status in {"downloaded", "metadata-only"} and not exists:
            print(f"missing: {dataset_id} -> {path}")
            failures += 1
        else:
            print(f"{status}: {dataset_id} -> {path}")
    if failures:
        print(f"dataset audit failed: {failures} missing required path(s)")
        return 1
    print("dataset audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
