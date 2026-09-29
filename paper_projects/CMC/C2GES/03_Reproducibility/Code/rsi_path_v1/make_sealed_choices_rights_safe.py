"""Derive a rights-safe companion for the sealed RSI choices record.

`SEALED_CHOICES.jsonl` stores the selected and reference passages verbatim so the
sealed run can be re-scored offline.  Third-party redistribution permission has
not been established, so the verbatim record stays out of the release and this
script writes the shippable companion: identical identifiers, budgets, realised
lengths and scores with the two passage fields removed.

Usage:
    python -B make_sealed_choices_rights_safe.py
"""

from __future__ import annotations

import json
from pathlib import Path

RUN = Path(
    r"F:\aicoding\powergrid_benchmark\paper_projects\C2GES\Workspace"
    r"\03_Reproducibility\Data\rsi_path_v1\run"
)
SOURCE = RUN / "SEALED_CHOICES.jsonl"
TARGET = RUN / "SEALED_CHOICES_rights_safe.jsonl"
STRIP = ("selected_text", "reference_text")


def main() -> None:
    rows = []
    with SOURCE.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            safe = {key: value for key, value in record.items() if key not in STRIP}
            safe["text_fields_removed"] = list(STRIP)
            rows.append(safe)
    with TARGET.open("w", encoding="utf-8") as handle:
        for record in rows:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    longest = max(
        len(json.dumps(record, ensure_ascii=False)) for record in rows
    )
    print(f"wrote {TARGET.name}: {len(rows)} rows, longest row {longest} chars")


if __name__ == "__main__":
    main()
