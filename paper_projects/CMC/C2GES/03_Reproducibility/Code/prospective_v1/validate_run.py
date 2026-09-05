#!/usr/bin/env python3
"""Validate a completed development-pilot run without changing its artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


SAFE_SELECTED_KEYS = {
    "doc_id", "report_series_id", "word_budget", "condition",
    "selected_sentence_ids", "selection_order", "actual_words",
}
IDENTITIES = (("AB-5", "RP-11"), ("AB-6", "RP-10"), ("AB-6", "G-T"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    errors: list[str] = []

    final_path = run_dir / "final_info.json"
    final = json.loads(final_path.read_text(encoding="utf-8"))
    metrics = read_csv(run_dir / "factorial_item_metrics.csv")
    selected = [json.loads(line) for line in (run_dir / "factorial_selected_ids.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    inference = json.loads((run_dir / "factorial_inference.json").read_text(encoding="utf-8"))

    if final.get("mode") != "DEV_PILOT_NONCONFIRMATORY":
        errors.append("run mode is not development-only")
    if final.get("confirmatory_claims_allowed") is not False:
        errors.append("confirmatory_claims_allowed must be false")
    if final.get("external_test_accessed") is not False:
        errors.append("external_test_accessed must be false")
    expected = int(final["reports"]) * int(final["conditions"]) * len(final["word_budgets"])
    if len(metrics) != expected or len(selected) != expected:
        errors.append(f"row count mismatch: expected {expected}, metrics={len(metrics)}, selected={len(selected)}")
    if any(row.get("status") != "PASS" for row in metrics):
        errors.append("one or more metric rows failed")
    for row in metrics:
        budget = int(row["word_budget"])
        words = int(float(row["actual_words"]))
        utilization = float(row["budget_utilization"])
        if words > budget:
            errors.append(f"over-budget row: {row['doc_id']} {row['condition']} {budget}")
        if not (0.0 <= utilization <= 1.0) or not math.isclose(utilization, words / budget, abs_tol=1e-12):
            errors.append(f"invalid utilization: {row['doc_id']} {row['condition']} {budget}")

    selected_by_key = {
        (row["doc_id"], int(row["word_budget"]), row["condition"]): row
        for row in selected
    }
    for row in selected:
        unsafe = set(row) - SAFE_SELECTED_KEYS
        if unsafe:
            errors.append(f"unexpected selected-output fields: {sorted(unsafe)}")
    for doc_id, budget, _ in selected_by_key:
        for left, right in IDENTITIES:
            left_row = selected_by_key[(doc_id, budget, left)]
            right_row = selected_by_key[(doc_id, budget, right)]
            if left_row["selected_sentence_ids"] != right_row["selected_sentence_ids"]:
                errors.append(f"identity failed: {doc_id} {budget} {left}!={right}")

    expected_families = {"incremental_chain", "reservation_path_factorial", "graph_type"}
    if set(inference) != expected_families:
        errors.append(f"inference family mismatch: {sorted(inference)}")
    expected_sizes = {"incremental_chain": 12, "reservation_path_factorial": 6, "graph_type": 2}
    for family, size in expected_sizes.items():
        if len(inference.get(family, [])) != size:
            errors.append(f"wrong {family} contrast count")

    for name, expected_hash in final.get("artifacts", {}).items():
        path = run_dir / name
        if not path.is_file() or sha256(path) != expected_hash:
            errors.append(f"artifact hash mismatch: {name}")

    if errors:
        print("VALIDATION FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("VALIDATION PASS")
    print(f"rows={len(metrics)} reports={final['reports']} series={final['series']} identities={len(IDENTITIES)}")
    print("external_test_accessed=false confirmatory_claims_allowed=false")


if __name__ == "__main__":
    main()
