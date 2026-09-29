"""Fetch a slice of the CNN/DailyMail test split (human-written highlights) for the
reference-type sensitivity layer.

Raw text stays outside the release scope; only derived numbers ship.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://datasets-server.huggingface.co/rows"
DATASET = "abisee/cnn_dailymail"
CONFIG = "3.0.0"
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
        except Exception as error:  # noqa: BLE001
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} after {type(error).__name__}: {error}")
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable")


def clean_article(text: str) -> str:
    lines = [line for line in text.split("\n") if not line.strip().startswith("@highlight")]
    body = " ".join(lines)
    for byline in ("(CNN)", "(Daily Mail)", "CNN", "Daily Mail"):
        body = body.replace(byline, " ")
    return " ".join(body.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--rows", type=int, default=2000)
    args = parser.parse_args()

    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for offset in range(0, args.rows, PAGE):
        payload = fetch_page(offset, PAGE)
        for item in payload["rows"]:
            row = item["row"]
            article = clean_article(row["article"])
            highlights = " ".join(row["highlights"].replace("@highlight", " ").split())
            records.append(
                {
                    "doc_id": f"cnndm_test_{item['row_idx']:05d}",
                    "article": article,
                    "highlights": highlights,
                    "article_chars": len(article),
                    "highlight_chars": len(highlights),
                }
            )
        print(f"  fetched {min(offset + PAGE, args.rows)} rows", flush=True)
    target.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    print(f"wrote {target} with {len(records)} rows")


if __name__ == "__main__":
    main()
