#!/usr/bin/env python3
"""Mechanism diagnostics for the MA-SQLGrid C4/C5 context path.

This script does not generate predictions and does not expose gold SQL/results
to prompts, rankers, or repairs. Dataset answer-shape metadata is used only as
an offline diagnostic target.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPERIMENT_DIR = Path(__file__).resolve().parent
FALLBACK_WORKSPACE = Path(
    "/media/lenovo/data2/cja/GridMind/references/AutoResearchClaw/"
    "paper_workspace/workspaces/ma-sqlgrid-value-grounded-restart"
)


def resolve_workspace() -> Path:
    for candidate in [EXPERIMENT_DIR, *EXPERIMENT_DIR.parents]:
        if (candidate / "data" / "griddb_maintenance_v2_v0_1" / "database.sqlite").exists():
            return candidate.resolve()
    return FALLBACK_WORKSPACE.resolve()


WORKSPACE = resolve_workspace()
DATA_DIR = WORKSPACE / "data" / "griddb_maintenance_v2_v0_1"
DB_PATH = DATA_DIR / "database.sqlite"
QUESTIONS_PATH = DATA_DIR / "questions.jsonl"
DEFAULT_OUT_DIR = EXPERIMENT_DIR.parent / "mechanism_diagnostics"

sys.path.insert(0, str(WORKSPACE / "smoke"))

import dev_chess_style_pilot as chess  # noqa: E402


PATTERN_FIXTURES = [
    ("Find assets installed before 2018 in the North region.", 2, ["assets.install_date < '2018-01-01'"]),
    ("Which technicians are assigned to high-priority work orders?", 1, ["work_orders.priority = 'high'"]),
    ("Show the latest voltage reading for asset LN-003.", 3, ["sensor_readings.sensor_type = 'voltage'"]),
    ("Which asset has the highest recorded temperature alarm?", 2, ["sensor_readings.sensor_type = 'temperature'", "sensor_readings.alarm_flag = 1"]),
    ("Show assets in critical locations with their region.", 2, ["locations.criticality = 'critical'"]),
    ("What type, location, and status are recorded for asset TX-001?", 3, []),
    ("Show the latest sensor reading recorded for asset TX-001.", 4, []),
    ("List topology edges that originate from upstream asset TX-001.", 4, []),
    ("List work orders with fault code TEMP.", 4, []),
    ("Which work orders have fault code TEMP?", 3, []),
    ("Which asset type has the most alarmed sensor readings?", 2, ["sensor_readings.alarm_flag = 1"]),
]


def load_questions() -> list[dict[str, Any]]:
    return [json.loads(line) for line in QUESTIONS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def shape_metadata_audit(conn: sqlite3.Connection, split: str) -> dict[str, Any]:
    rows = [record for record in load_questions() if record["split"] == split]
    mismatches = []
    inferred_dist: Counter[int] = Counter()
    metadata_dist: Counter[int] = Counter()
    value_hint_records = 0
    for record in rows:
        context = chess.infer_domain_context(conn, record)
        inferred_count = int(context["inferred_shape"]["column_count"])
        metadata_count = int(record["answer_shape"]["column_count"])
        inferred_dist[inferred_count] += 1
        metadata_dist[metadata_count] += 1
        if context["normalized_value_hints"]:
            value_hint_records += 1
        if inferred_count != metadata_count:
            mismatches.append(
                {
                    "question_id": record["question_id"],
                    "question": record["question"],
                    "inferred_column_count": inferred_count,
                    "metadata_column_count": metadata_count,
                    "inferred_hints": context["inferred_shape"]["hints"],
                }
            )
    return {
        "split": split,
        "question_count": len(rows),
        "column_count_mismatch_count": len(mismatches),
        "inferred_column_count_distribution": dict(sorted(inferred_dist.items())),
        "metadata_column_count_distribution": dict(sorted(metadata_dist.items())),
        "value_hint_record_count": value_hint_records,
        "mismatches": mismatches,
    }


def pattern_fixture_audit(conn: sqlite3.Connection) -> dict[str, Any]:
    failures = []
    rows = []
    for idx, (question, expected_columns, required_hints) in enumerate(PATTERN_FIXTURES, start=1):
        record = {"question_id": f"PATTERN_{idx:03d}", "question": question}
        context = chess.infer_domain_context(conn, record)
        inferred_count = int(context["inferred_shape"]["column_count"])
        hint_text = "\n".join(context["normalized_value_hints"])
        missing_hints = [hint for hint in required_hints if hint not in hint_text]
        row = {
            "question": question,
            "expected_column_count": expected_columns,
            "inferred_column_count": inferred_count,
            "missing_required_hints": missing_hints,
            "normalized_value_hints": context["normalized_value_hints"],
            "selected_tables": context["selected_tables"],
            "selected_columns": context["selected_columns"],
            "inferred_hints": context["inferred_shape"]["hints"],
        }
        rows.append(row)
        if inferred_count != expected_columns or missing_hints:
            failures.append(row)
    return {"fixture_count": len(rows), "failure_count": len(failures), "failures": failures, "rows": rows}


def write_outputs(out_dir: Path, result: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "mechanism_diagnostics.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# MA-SQLGrid Mechanism Diagnostics",
        "",
        f"- Metadata split: `{result['metadata_audit']['split']}`",
        f"- Metadata questions: {result['metadata_audit']['question_count']}",
        f"- Column-count mismatches: {result['metadata_audit']['column_count_mismatch_count']}",
        f"- Pattern fixture failures: {result['pattern_audit']['failure_count']}",
        f"- Value-hint records: {result['metadata_audit']['value_hint_record_count']}",
        "",
        "## Distributions",
        "",
        f"- Inferred: {result['metadata_audit']['inferred_column_count_distribution']}",
        f"- Metadata: {result['metadata_audit']['metadata_column_count_distribution']}",
    ]
    if result["metadata_audit"]["mismatches"]:
        lines.extend(["", "## Metadata Mismatches", ""])
        for row in result["metadata_audit"]["mismatches"][:25]:
            lines.append(f"- {row['question_id']}: inferred {row['inferred_column_count']} vs metadata {row['metadata_column_count']} -- {row['question']}")
    if result["pattern_audit"]["failures"]:
        lines.extend(["", "## Pattern Fixture Failures", ""])
        for row in result["pattern_audit"]["failures"]:
            lines.append(f"- inferred {row['inferred_column_count']} vs expected {row['expected_column_count']} -- {row['question']}")
    (out_dir / "mechanism_diagnostics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    try:
        result = {
            "metadata_audit": shape_metadata_audit(conn, args.split),
            "pattern_audit": pattern_fixture_audit(conn),
        }
    finally:
        conn.close()

    write_outputs(args.out_dir, result)
    print(f"MECHANISM_DIAGNOSTICS split={args.split} column_count_mismatches={result['metadata_audit']['column_count_mismatch_count']} pattern_failures={result['pattern_audit']['failure_count']}")
    if result["metadata_audit"]["column_count_mismatch_count"] or result["pattern_audit"]["failure_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
