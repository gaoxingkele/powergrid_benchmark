"""Create knowledge-base update files for a new work round."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPDATE_ROOT = ROOT / "knowledge_base" / "updates"

TEMPLATES = {
    "decision_log": """# Decision Log: {day}

## Decisions

- TODO

## Consequences

- TODO
""",
    "rationale_summary": """# Rationale Summary: {day}

## Evidence Used

- TODO

## Rationale Summary

- TODO
""",
    "paper_updates": """# Paper Updates: {day}

## Added

- TODO

## Revised

- TODO
""",
    "open_questions": """# Open Questions: {day}

1. TODO
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=date.today().isoformat(), help="Update date in YYYY-MM-DD format.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing update files.")
    args = parser.parse_args()

    created = 0
    for stream, template in TEMPLATES.items():
        path = UPDATE_ROOT / stream / f"{args.date}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and not args.force:
            print(f"exists: {path}")
            continue
        path.write_text(template.format(day=args.date), encoding="utf-8")
        created += 1
        print(f"created: {path}")

    print(f"update round ready: {args.date}; files created/overwritten: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
