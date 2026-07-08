"""Download official NERC PDFs mapped to the C2GES report ids."""

from __future__ import annotations

import csv
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data" / "public_datasets" / "reliability_reports" / "c2ges_nerc_reports"
MANIFEST = DATASET / "metadata" / "c2ges_nerc_report_manifest.csv"


def main() -> int:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8", newline="")))
    downloaded = 0
    for row in rows:
        out = DATASET / row["local_pdf"]
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and out.stat().st_size > 1024:
            print(f"exists: {row['doc_id']} -> {out}")
            downloaded += 1
            continue
        print(f"download: {row['doc_id']} <- {row['url']}")
        request = urllib.request.Request(row["url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=180) as response, out.open("wb") as handle:
            handle.write(response.read())
        if out.stat().st_size <= 1024:
            print(f"failed: {row['doc_id']} produced a tiny file")
            return 1
        downloaded += 1
    print(f"C2GES NERC reports ready: {downloaded}/{len(rows)} PDFs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
