#!/usr/bin/env python3
"""Materialize already accepted raw synthetic responses after a stopped run."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from generate_deepseek_synthetic import THEMES, expand_report, read_numeric_rows, sha256, validate_core, validate_dataset


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-envelope", type=Path, required=True)
    parser.add_argument("--metadata-csv", type=Path, required=True)
    parser.add_argument("--layout-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--series-number", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    envelope = json.loads(args.raw_envelope.read_text(encoding="utf-8"))
    value = json.loads(envelope["choices"][0]["message"]["content"])
    cores = validate_core(value)
    profiles = read_numeric_rows(args.metadata_csv, args.layout_csv)
    regime = ("explicit", "paraphrased", "ambiguous")[(args.series_number - 1) % 3]
    rng = random.Random(args.seed)
    rows = [expand_report(core, profiles[i], f"synthetic_s{args.series_number:02d}_r{i + 1:02d}",
                          f"synthetic_series_{args.series_number:02d}", regime,
                          THEMES[args.series_number - 1], rng) for i, core in enumerate(cores)]
    validation = validate_dataset(rows)
    dataset = args.output / "synthetic_reports.jsonl"
    dataset.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    manifest = {"schema": "c2ges-partial-synthetic-diagnostic-v1", "status": "PARTIAL_DIAGNOSTIC_ONLY",
                "source_run_failed": True, "source_raw_sha256": sha256(args.raw_envelope),
                "dataset_sha256": sha256(dataset), "synthetic": True, "confirmatory_claims_allowed": False,
                "eligible_for_parent_promotion": False, **validation}
    (args.output / "PARTIAL_DIAGNOSTIC_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PARTIAL_DIAGNOSTIC_ONLY", **validation}))


if __name__ == "__main__":
    main()
