"""Convert the frozen external corpus to structured Markdown (resumable).

Uses pymupdf4llm, which performs layout analysis and emits heading levels,
lists and tables, so that a summary section can be cut by heading structure
instead of by ad-hoc text-block heuristics.

Usage:
    python -B convert_to_markdown.py [--limit N] [--only SUBSTRING]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pymupdf4llm

HERE = Path(__file__).resolve().parent
OUT = HERE / "markdown"
SOURCES = (HERE / "source_pdfs_v2", HERE / "source_pdfs_entsoe", HERE / "source_pdfs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--only", default=None)
    args = parser.parse_args()

    OUT.mkdir(exist_ok=True)
    pdfs = [p for d in SOURCES for p in sorted(d.glob("*.pdf"))]
    if args.only:
        pdfs = [p for p in pdfs if args.only.lower() in p.name.lower()]
    done = 0
    for pdf in pdfs:
        target = OUT / f"{pdf.stem}.md"
        if target.is_file() and target.stat().st_size > 0:
            print(f"  skip (exists) {pdf.name[:60]}")
            continue
        try:
            md = pymupdf4llm.to_markdown(str(pdf))
        except Exception as exc:  # keep going; record the failure
            print(f"  FAIL {pdf.name[:60]}: {type(exc).__name__} {exc}"[:160])
            continue
        target.write_text(md, encoding="utf-8")
        heading = next((line for line in md.splitlines() if re.match(r"^#{1,4}\s+.*summary", line, re.I)), None)
        print(f"  wrote {target.name[:58]:60s} chars={len(md):8d} summary_heading={heading!r}"[:190])
        done += 1
        if args.limit and done >= args.limit:
            break


if __name__ == "__main__":
    main()
