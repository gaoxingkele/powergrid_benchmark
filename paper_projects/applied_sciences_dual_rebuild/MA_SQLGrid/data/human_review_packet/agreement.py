#!/usr/bin/env python3
"""Calculate categorical agreement for completed independent A/B reviews."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


FIELDS = ["decision", "semantic_alignment", "question_unambiguous", "units_correct", "sql_correct",
          "answer_useful", "query_class_reviewed", "difficulty_reviewed"]
CRITICAL_FIELDS = {"decision", "semantic_alignment", "question_unambiguous", "units_correct", "sql_correct"}


def read(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["blind_item_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate blind_item_id in {path}")
    return {row["blind_item_id"]: row for row in rows}


def cohen_kappa(left: list[str], right: list[str]) -> float | None:
    if not left:
        return None
    observed = sum(a == b for a, b in zip(left, right)) / len(left)
    left_counts, right_counts = Counter(left), Counter(right)
    categories = set(left_counts) | set(right_counts)
    expected = sum((left_counts[c] / len(left)) * (right_counts[c] / len(right)) for c in categories)
    if expected == 1:
        return 1.0 if observed == 1 else None
    return (observed - expected) / (1 - expected)


def calculate(a: dict[str, dict[str, str]], b: dict[str, dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    if set(a) != set(b):
        raise ValueError(f"Reviewer item sets differ: only A={sorted(set(a)-set(b))[:5]}, only B={sorted(set(b)-set(a))[:5]}")
    metrics = {}
    conflicts = []
    for field in FIELDS:
        complete = [(a[item][field].strip(), b[item][field].strip()) for item in sorted(a)
                    if a[item].get(field, "").strip() and b[item].get(field, "").strip()]
        left, right = [x[0] for x in complete], [x[1] for x in complete]
        agreements = sum(x == y for x, y in complete)
        metrics[field] = {
            "complete_pairs": len(complete), "coverage": len(complete) / len(a) if a else 0,
            "raw_agreement": agreements / len(complete) if complete else None,
            "cohen_kappa": cohen_kappa(left, right), "categories_a": dict(Counter(left)),
            "categories_b": dict(Counter(right)),
        }
    for item in sorted(a):
        disagree = [field for field in FIELDS if a[item].get(field, "").strip() and b[item].get(field, "").strip()
                    and a[item][field].strip() != b[item][field].strip()]
        missing = [field for field in CRITICAL_FIELDS if not a[item].get(field, "").strip() or not b[item].get(field, "").strip()]
        if disagree or missing:
            conflicts.append({
                "blind_item_id": item, "dataset": a[item].get("dataset", ""),
                "reviewer_a_decision": a[item].get("decision", ""), "reviewer_b_decision": b[item].get("decision", ""),
                "conflict_fields": "|".join(disagree), "missing_critical_fields": "|".join(sorted(missing)),
                "adjudicator_decision": "", "final_question": "", "final_sql": "", "change_reason": "",
                "reexecution_result_sha256": "", "adjudicator_qualification": "", "adjudicator_signature": "",
                "completed_at_utc": "",
            })
    return {"item_count": len(a), "fields": metrics, "conflict_count": len(conflicts),
            "all_critical_fields_complete": not any(row["missing_critical_fields"] for row in conflicts)}, conflicts


def markdown(report: dict[str, Any]) -> str:
    lines = ["# Independent-review agreement", "", "| Field | Complete pairs | Coverage | Raw agreement | Cohen kappa |",
             "|---|---:|---:|---:|---:|"]
    for field, value in report["fields"].items():
        raw = "n/a" if value["raw_agreement"] is None else f"{value['raw_agreement']:.4f}"
        kappa = "n/a" if value["cohen_kappa"] is None else f"{value['cohen_kappa']:.4f}"
        lines.append(f"| {field} | {value['complete_pairs']} | {value['coverage']:.1%} | {raw} | {kappa} |")
    lines.extend(["", f"Conflicts or incomplete critical records: **{report['conflict_count']}**.", "",
                  "Agreement measures reliability; they do not establish substantive correctness. All conflicts require independent adjudication.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewer-a", type=Path, required=True)
    parser.add_argument("--reviewer-b", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    parser.add_argument("--conflicts-out", type=Path, required=True)
    args = parser.parse_args()
    report, conflicts = calculate(read(args.reviewer_a), read(args.reviewer_b))
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_out.write_text(markdown(report), encoding="utf-8")
    fields = ["blind_item_id", "dataset", "reviewer_a_decision", "reviewer_b_decision", "conflict_fields",
              "missing_critical_fields", "adjudicator_decision", "final_question", "final_sql", "change_reason",
              "reexecution_result_sha256", "adjudicator_qualification", "adjudicator_signature", "completed_at_utc"]
    with args.conflicts_out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(conflicts)
    print(json.dumps({"item_count": report["item_count"], "conflict_count": report["conflict_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
