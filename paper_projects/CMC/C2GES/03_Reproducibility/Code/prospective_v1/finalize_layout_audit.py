#!/usr/bin/env python3
"""Finalize the two-reviewer C2GES layout-boundary audit without source text."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from external_confirmatory import sha256, utc_now


LABELS = {
    "valid_standalone", "valid_with_adjacent_context", "fragment_or_truncated",
    "fused_unrelated_content", "header_footer_contamination", "table_body_fusion",
    "incorrect_unit_type", "duplicate", "cannot_judge",
}
VALID = {"valid_standalone", "valid_with_adjacent_context"}
KEY = ("doc_id", "candidate_id", "normalized_sha256")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        result = list(csv.DictReader(stream))
    if not result or not set(KEY).issubset(result[0]):
        raise ValueError(f"layout audit is empty or missing identity columns: {path}")
    return result


def index(values: list[dict[str, str]], label_field: str) -> dict[tuple[str, ...], str]:
    result: dict[tuple[str, ...], str] = {}
    for row in values:
        key = tuple(row[field].strip() for field in KEY)
        label = row.get(label_field, "").strip()
        if not all(key) or key in result:
            raise ValueError(f"invalid or duplicate layout sample identity: {key}")
        if label not in LABELS:
            raise ValueError(f"invalid or missing {label_field}: {key}={label!r}")
        result[key] = label
    return result


def nominal_kappa(a: list[str], b: list[str]) -> float | None:
    observed = sum(left == right for left, right in zip(a, b, strict=True)) / len(a)
    ca, cb = Counter(a), Counter(b)
    expected = sum((ca[label] / len(a)) * (cb[label] / len(b)) for label in LABELS)
    return None if expected == 1.0 else (observed - expected) / (1.0 - expected)


def finalize(
    reviewer_a: Path, reviewer_b: Path, adjudicated: Path, output: Path,
    reviewer_a_id: str, reviewer_b_id: str,
) -> dict[str, object]:
    if output.exists():
        raise FileExistsError(f"refusing existing output: {output}")
    if not reviewer_a_id.strip() or not reviewer_b_id.strip() or reviewer_a_id == reviewer_b_id:
        raise ValueError("two distinct coded reviewer identifiers are required")
    a = index(rows(reviewer_a), "reviewer_a_validity")
    b = index(rows(reviewer_b), "reviewer_b_validity")
    final = index(rows(adjudicated), "adjudication")
    if set(a) != set(b) or set(a) != set(final):
        raise ValueError("reviewer and adjudication files do not contain identical samples")
    ordered = sorted(a)
    labels_a = [a[key] for key in ordered]
    labels_b = [b[key] for key in ordered]
    labels_final = [final[key] for key in ordered]
    auditable = [label for label in labels_final if label != "cannot_judge"]
    if not auditable:
        raise ValueError("layout audit has no auditable adjudicated samples")
    validity_rate = sum(label in VALID for label in auditable) / len(auditable)
    fusion_rate = sum(label == "table_body_fusion" for label in auditable) / len(auditable)
    result: dict[str, object] = {
        "schema": "c2ges-layout-boundary-audit-summary-v1",
        "status": "PASS" if validity_rate >= 0.90 and fusion_rate <= 0.05 else "FAIL",
        "completed_at": utc_now(), "independent_reviewers": 2,
        "reviewer_ids": [reviewer_a_id, reviewer_b_id],
        "sample_count": len(ordered), "auditable_sample_count": len(auditable),
        "cannot_judge_count": len(ordered) - len(auditable),
        "candidate_validity_rate": validity_rate,
        "table_body_fusion_rate": fusion_rate,
        "header_footer_contamination_rate": sum(label == "header_footer_contamination" for label in auditable) / len(auditable),
        "pre_adjudication_raw_agreement": sum(left == right for left, right in zip(labels_a, labels_b, strict=True)) / len(ordered),
        "pre_adjudication_cohen_kappa": nominal_kappa(labels_a, labels_b),
        "adjudicated_label_counts": dict(sorted(Counter(labels_final).items())),
        "thresholds": {"candidate_validity_rate_min": 0.90, "table_body_fusion_rate_max": 0.05},
        "input_sha256": {"reviewer_a": sha256(reviewer_a), "reviewer_b": sha256(reviewer_b), "adjudicated": sha256(adjudicated)},
        "source_text_in_output": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewer-a", type=Path, required=True)
    parser.add_argument("--reviewer-b", type=Path, required=True)
    parser.add_argument("--adjudicated", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reviewer-a-id", required=True)
    parser.add_argument("--reviewer-b-id", required=True)
    args = parser.parse_args()
    result = finalize(args.reviewer_a, args.reviewer_b, args.adjudicated, args.output, args.reviewer_a_id, args.reviewer_b_id)
    print(json.dumps({"status": result["status"], "sample_count": result["sample_count"], "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
