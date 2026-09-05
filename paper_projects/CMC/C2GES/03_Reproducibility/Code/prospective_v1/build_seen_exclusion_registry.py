#!/usr/bin/env python3
"""Build the rights-safe registry of reports ineligible for external testing."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


URL_RE = re.compile(r"`(https://[^`]+)`")


def build(historical: Path, access_log: Path) -> list[dict[str, str]]:
    with historical.open(newline="", encoding="utf-8-sig") as stream:
        source_rows = list(csv.DictReader(stream))
    rows = [
        {
            "exposure_class": "historical_corpus",
            "doc_id": row["doc_id"],
            "report_series_id": row["report_series_id"],
            "source_url": row["source_url"],
            "source_pdf_sha256": row["pdf_sha256"],
            "disposition": "EXCLUDE_FROM_CONFIRMATORY_EXTERNAL",
        }
        for row in source_rows
    ]
    known_urls = {row["source_url"] for row in rows}
    for url in URL_RE.findall(access_log.read_text(encoding="utf-8-sig")):
        if url not in known_urls:
            rows.append({
                "exposure_class": "prefreeze_content_exposure",
                "doc_id": "",
                "report_series_id": "",
                "source_url": url,
                "source_pdf_sha256": "",
                "disposition": "EXCLUDE_FROM_CONFIRMATORY_EXTERNAL",
            })
            known_urls.add(url)
    return sorted(rows, key=lambda row: (row["exposure_class"], row["source_url"], row["doc_id"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--historical", type=Path, required=True)
    parser.add_argument("--access-log", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing existing output: {args.output}")
    rows = build(args.historical, args.access_log)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"rows={len(rows)} historical={sum(row['exposure_class']=='historical_corpus' for row in rows)} prefreeze={sum(row['exposure_class']=='prefreeze_content_exposure' for row in rows)}")


if __name__ == "__main__":
    main()
