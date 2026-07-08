"""Archive downloaded public datasets for GitHub-friendly storage.

Raw dataset folders stay ignored. This script creates tar.gz archives from the
manifest and splits any archive larger than the configured part size. The
default is 20 MB to keep pushes reliable on unstable connections.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "public_datasets" / "manifests" / "public_dataset_manifest.csv"
ARCHIVE_ROOT = ROOT / "data" / "public_dataset_archives"
PART_SIZE = 20 * 1024 * 1024


def should_skip(path: Path) -> bool:
    return any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts)


def add_path(tar: tarfile.TarFile, source: Path, arcname: Path) -> None:
    if source.is_file():
        if not should_skip(source):
            tar.add(source, arcname=str(arcname))
        return
    for item in source.rglob("*"):
        if should_skip(item):
            continue
        rel = item.relative_to(source)
        tar.add(item, arcname=str(arcname / rel))


def split_file(path: Path, part_size: int) -> list[Path]:
    if path.stat().st_size <= part_size:
        return [path]
    parts: list[Path] = []
    with path.open("rb") as src:
        idx = 1
        while True:
            chunk = src.read(part_size)
            if not chunk:
                break
            part = path.with_name(f"{path.name}.part{idx:03d}")
            part.write_bytes(chunk)
            parts.append(part)
            idx += 1
    path.unlink()
    return parts


def archive_dataset(row: dict[str, str], archive_root: Path, part_size: int) -> list[dict[str, str]]:
    dataset_id = row["dataset_id"]
    local_path = row["local_path"]
    source = ROOT / local_path
    if not source.exists():
        raise FileNotFoundError(f"{dataset_id}: missing {source}")

    archive_root.mkdir(parents=True, exist_ok=True)
    archive_path = archive_root / f"{dataset_id}.tar.gz"
    if archive_path.exists():
        archive_path.unlink()
    for old_part in archive_root.glob(f"{dataset_id}.tar.gz.part*"):
        old_part.unlink()

    with tarfile.open(archive_path, "w:gz") as tar:
        add_path(tar, source, Path(local_path))

    parts = split_file(archive_path, part_size)
    return [
        {
            "dataset_id": dataset_id,
            "archive_part": str(part.relative_to(ROOT)).replace("\\", "/"),
            "bytes": str(part.stat().st_size),
            "source_path": local_path,
        }
        for part in parts
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", action="append", default=[], help="Dataset id to archive. Repeatable.")
    parser.add_argument("--clean", action="store_true", help="Delete existing archive directory before archiving.")
    parser.add_argument("--part-size-mb", type=int, default=20)
    args = parser.parse_args()

    if args.clean and ARCHIVE_ROOT.exists():
        shutil.rmtree(ARCHIVE_ROOT)
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8", newline="")))
    dataset_filter = set(args.dataset)
    archive_rows: list[dict[str, str]] = []
    for row in rows:
        if row["status"] != "downloaded":
            continue
        if dataset_filter and row["dataset_id"] not in dataset_filter:
            continue
        print(f"archive {row['dataset_id']} <- {row['local_path']}")
        archive_rows.extend(archive_dataset(row, ARCHIVE_ROOT, args.part_size_mb * 1024 * 1024))

    archive_manifest = ARCHIVE_ROOT / "archives_manifest.csv"
    with archive_manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["dataset_id", "archive_part", "bytes", "source_path"])
        writer.writeheader()
        writer.writerows(archive_rows)

    print(f"archive parts: {len(archive_rows)}")
    print(f"manifest: {archive_manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
