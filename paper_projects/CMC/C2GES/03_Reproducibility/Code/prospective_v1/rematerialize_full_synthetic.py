#!/usr/bin/env python3
"""Re-materialize an accepted DeepSeek run after deterministic expander fixes.

No API request is made. Accepted raw response envelopes, the generation log,
the frozen seed, and the numeric profile inputs are used to create a child run.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

from generate_deepseek_synthetic import (
    THEMES,
    expand_report,
    read_numeric_rows,
    sha256,
    validate_core,
    validate_dataset,
)


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--metadata-csv", type=Path, required=True)
    parser.add_argument("--layout-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version-id", required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    parent = json.loads((args.source_run / "SYNTHETIC_RUN_MANIFEST.json").read_text(encoding="utf-8"))
    records = sorted(jsonl(args.source_run / "generation_log.jsonl"), key=lambda row: row["call_number"])
    if not records or any(row["status"] != "accepted" for row in records):
        raise ValueError("source run must contain only accepted API calls")
    profiles = read_numeric_rows(args.metadata_csv, args.layout_csv)
    report_total = 2 * len(records)
    selected_profiles = [profiles[min(len(profiles) - 1, math.floor((i + .5) * len(profiles) / report_total))]
                         for i in range(report_total)]
    rng = random.Random(parent["seed"])
    scheduled = list(enumerate(THEMES, 1))
    rng.shuffle(scheduled)
    scheduled_numbers = [number for number, _ in scheduled[:len(records)]]
    recorded_numbers = [int(row["series_id"].split("_")[-1]) for row in records]
    if scheduled_numbers != recorded_numbers:
        raise ValueError("source schedule does not match parent seed")
    reports = []
    raw_hashes = []
    for call_index, record in enumerate(records):
        raw_path = args.source_run / "raw_synthetic_responses" / record["raw_file"]
        envelope = json.loads(raw_path.read_text(encoding="utf-8"))
        value = json.loads(envelope["choices"][0]["message"]["content"])
        cores = validate_core(value, require_distractor_seeds=True)
        series_number = int(record["series_id"].split("_")[-1])
        theme = THEMES[series_number - 1]
        regime = ("explicit", "paraphrased", "ambiguous")[(series_number - 1) % 3]
        for report_index, core in enumerate(cores):
            profile = selected_profiles[2 * call_index + report_index]
            reports.append(expand_report(
                core, profile, f"synthetic_s{series_number:02d}_r{report_index + 1:02d}",
                record["series_id"], regime, theme, rng))
        raw_hashes.append({"call_number": record["call_number"], "sha256": sha256(raw_path)})
    validation = validate_dataset(reports)
    dataset = args.output / "synthetic_reports.jsonl"
    dataset.write_text("".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
        for row in sorted(reports, key=lambda row: row["doc_id"])), encoding="utf-8")
    manifest = {
        "schema": "c2ges-deepseek-synthetic-rematerialized-v1",
        "version_id": args.version_id,
        "synthetic": True,
        "confirmatory_claims_allowed": False,
        "external_test_accessed": False,
        "provider": parent["provider"],
        "model": parent["model"],
        "seed": parent["seed"],
        "api_calls_in_child": 0,
        "accepted_api_calls_in_parent": len(records),
        "derived_from": str(args.source_run),
        "parent_dataset_sha256": parent["dataset_sha256"],
        "source_raw_response_hashes": raw_hashes,
        "dataset_sha256": sha256(dataset),
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "change": "Deterministic filler uniqueness and heading encoding fix; LLM semantic cores unchanged.",
        **validation,
    }
    (args.output / "SYNTHETIC_RUN_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(args.output), **validation}))


if __name__ == "__main__":
    main()
