"""Apply the frozen energy-subset keyword rule of the transfer addendum."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

KEYWORDS = (
    "department of energy",
    "doe",
    "electric grid",
    "electrical grid",
    "power grid",
    "transmission",
    "distribution system",
    "power plant",
    "power system",
    "electricity",
    "electric utility",
    "utility grid",
    "renewable",
    "solar",
    "wind power",
    "nuclear",
    "natural gas",
    "hydropower",
    "coal",
    "energy storage",
    "battery storage",
    "grid reliability",
    "energy efficiency",
    "crude oil",
    "pipeline",
)
MIN_MATCHES = 3


def matches(report: str) -> list[str]:
    lowered = report.lower()
    return [word for word in KEYWORDS if word in lowered]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    kept = []
    with Path(args.corpus).open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            hits = matches(record["report"])
            if len(hits) >= MIN_MATCHES:
                record["energy_keyword_matches"] = hits
                kept.append(record)
    with Path(args.out).open("w", encoding="utf-8") as handle:
        for record in kept:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{len(kept)} of the test rows match >= {MIN_MATCHES} energy keywords -> {args.out}")


if __name__ == "__main__":
    main()
