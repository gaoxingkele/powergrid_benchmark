"""Derive non-verbatim output-length diagnostics from the frozen prediction ledger.

This is a read-only, post-run descriptive audit.  It never performs selection,
changes a prediction, or computes a new ROUGE result.  Word counts use Python's
Unicode-aware whitespace tokenization (``text.split()``); character counts use
the number of Unicode code points in each selected extraction unit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path


EXPECTED_PREDICTION_SHA256 = (
    "AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def percentile(values: list[int], q: float) -> float:
    """Linear-interpolated percentile, independent of optional packages."""
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty percentile input")
    position = (len(ordered) - 1) * q
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def derive(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    per_report: list[dict] = []
    units: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for row in rows:
        selected = row["selected_sentences"]
        if len(selected) != row["budget"] or len(selected) != len(row["selected_sentence_ids"]):
            raise AssertionError(f"selection cardinality mismatch: {row['doc_id']} {row['condition']}")
        unit_rows = []
        for sentence_id, text in zip(row["selected_sentence_ids"], selected):
            item = {
                "condition": row["condition"],
                "budget": int(row["budget"]),
                "doc_id": row["doc_id"],
                "sentence_id": sentence_id,
                "word_count": len(text.split()),
                "character_count": len(text),
                "table_marker": "Table" in text,
            }
            unit_rows.append(item)
            units[(item["condition"], item["budget"])].append(item)
        per_report.append(
            {
                "condition": row["condition"],
                "budget": int(row["budget"]),
                "doc_id": row["doc_id"],
                "output_word_count": sum(item["word_count"] for item in unit_rows),
                "output_character_count": sum(item["character_count"] for item in unit_rows),
                "units_over_100_words": sum(item["word_count"] > 100 for item in unit_rows),
                "table_marker_units": sum(item["table_marker"] for item in unit_rows),
                "maximum_unit_words": max(item["word_count"] for item in unit_rows),
            }
        )

    grouped_reports: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for row in per_report:
        grouped_reports[(row["condition"], row["budget"])].append(row)

    summary = []
    for key in sorted(grouped_reports):
        condition, budget = key
        report_group = grouped_reports[key]
        unit_group = units[key]
        word_totals = [row["output_word_count"] for row in report_group]
        char_totals = [row["output_character_count"] for row in report_group]
        unit_words = [row["word_count"] for row in unit_group]
        summary.append(
            {
                "condition": condition,
                "budget": budget,
                "reports": len(report_group),
                "selected_unit_instances": len(unit_group),
                "mean_output_words": statistics.fmean(word_totals),
                "median_output_words": statistics.median(word_totals),
                "min_output_words": min(word_totals),
                "max_output_words": max(word_totals),
                "mean_output_characters": statistics.fmean(char_totals),
                "median_output_characters": statistics.median(char_totals),
                "mean_unit_words": statistics.fmean(unit_words),
                "median_unit_words": statistics.median(unit_words),
                "p90_unit_words": percentile(unit_words, 0.90),
                "maximum_unit_words": max(unit_words),
                "units_over_100_words": sum(value > 100 for value in unit_words),
                "table_marker_units": sum(row["table_marker"] for row in unit_group),
            }
        )
    return per_report, summary


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    actual_hash = digest(args.predictions)
    if actual_hash != EXPECTED_PREDICTION_SHA256:
        raise SystemExit(f"refused: prediction hash {actual_hash} != frozen hash")
    rows = load_jsonl(args.predictions)
    if len(rows) != 210:
        raise SystemExit(f"refused: expected 210 prediction rows, observed {len(rows)}")

    per_report, summary = derive(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "output_length_per_report.csv", per_report)
    write_csv(args.output_dir / "output_length_summary.csv", summary)
    payload = {
        "schema": "c2ges-frozen-output-length-audit-v1",
        "status": "PASS",
        "evidence_class": "post-run descriptive diagnostic",
        "selection_rerun": False,
        "prediction_sha256": actual_hash,
        "prediction_rows": len(rows),
        "word_definition": "number of nonempty Unicode whitespace-delimited tokens from text.split()",
        "character_definition": "number of Unicode code points in each selected extraction unit",
        "table_marker_definition": "case-sensitive substring 'Table' in the selected extraction unit",
        "summary": summary,
    }
    (args.output_dir / "OUTPUT_LENGTH_AUDIT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "PASS", "rows": len(rows), "groups": len(summary)}, indent=2))


if __name__ == "__main__":
    main()
