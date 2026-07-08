"""Restore public dataset archives created by archive_public_datasets.py."""

from __future__ import annotations

import csv
import tarfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_ROOT = ROOT / "data" / "public_dataset_archives"
ARCHIVE_MANIFEST = ARCHIVE_ROOT / "archives_manifest.csv"


def main() -> int:
    rows = list(csv.DictReader(ARCHIVE_MANIFEST.open(encoding="utf-8", newline="")))
    by_dataset: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_dataset[row["dataset_id"]].append(row)

    for dataset_id, dataset_rows in sorted(by_dataset.items()):
        dataset_rows.sort(key=lambda row: row["archive_part"])
        first_part = ROOT / dataset_rows[0]["archive_part"]
        if first_part.name.endswith(".part001"):
            tar_path = ARCHIVE_ROOT / f"{dataset_id}.tar.gz"
            with tar_path.open("wb") as out:
                for row in dataset_rows:
                    out.write((ROOT / row["archive_part"]).read_bytes())
        else:
            tar_path = first_part

        print(f"restore {dataset_id}: {tar_path}")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(ROOT)

        if tar_path.parent == ARCHIVE_ROOT and tar_path.name == f"{dataset_id}.tar.gz" and first_part != tar_path:
            tar_path.unlink()

    print("restore complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
