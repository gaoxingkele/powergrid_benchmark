"""Append a structured event to the independent research wiki log."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "research_wiki" / "logs"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--title", required=True)
    parser.add_argument("--observation", default="")
    parser.add_argument("--action", default="")
    parser.add_argument("--rationale", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--impact", default="")
    parser.add_argument("--next", default="")
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    path = LOG_DIR / f"{args.date}.md"
    if not path.exists():
        path.write_text(f"# Research Log: {args.date}\n", encoding="utf-8")

    now = datetime.now().strftime("%H:%M")
    entry = f"""

## {now} - {args.title}

- Observation: {args.observation}
- Action: {args.action}
- Rationale Summary: {args.rationale}
- Evidence: {args.evidence}
- Impact on Methodology: {args.impact}
- Next: {args.next}
"""
    with path.open("a", encoding="utf-8") as handle:
        handle.write(entry)
    print(f"appended: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
