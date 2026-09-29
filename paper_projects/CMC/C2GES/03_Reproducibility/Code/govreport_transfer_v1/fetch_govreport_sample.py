"""Fetch the GovReport test split from the HuggingFace datasets-server API.

GovReport is CC BY 4.0 (CRS and GAO reports, human-written summaries).  The raw
text is kept outside the release scope; only derived numbers are shipped.  The
script pulls all 973 test rows in pages so that the stratified sample can be
drawn with knowledge of the full length distribution.

Usage:
    python -B fetch_govreport_sample.py --out <dir>
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://datasets-server.huggingface.co/rows"
DATASET = "ccdv/govreport-summarization"
CONFIG = "document"
SPLIT = "test"
PAGE = 100


def fetch_page(offset: int, length: int) -> dict:
    query = urllib.parse.urlencode(
        {"dataset": DATASET, "config": CONFIG, "split": SPLIT, "offset": offset, "length": length}
    )
    url = f"{API}?{query}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                return json.load(response)
        except Exception as error:  # noqa: BLE001 - retry on any transport error
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} after {type(error).__name__}: {error}")
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="directory for the fetched JSONL")
    args = parser.parse_args()

    target = Path(args.out)
    target.mkdir(parents=True, exist_ok=True)
    out_path = target / "govreport_test_full.jsonl"

    first = fetch_page(0, 1)
    total = first["num_rows_total"]
    print(f"test split rows: {total}")

    rows: list[dict] = []
    for offset in range(0, total, PAGE):
        payload = fetch_page(offset, PAGE)
        for item in payload["rows"]:
            row = item["row"]
            rows.append(
                {
                    "doc_id": f"govreport_test_{item['row_idx']:04d}",
                    "report": row["report"],
                    "summary": row["summary"],
                    "report_chars": len(row["report"]),
                    "summary_chars": len(row["summary"]),
                }
            )
        print(f"  fetched {min(offset + PAGE, total)}/{total}", flush=True)

    with out_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {out_path} with {len(rows)} rows")


if __name__ == "__main__":
    main()
