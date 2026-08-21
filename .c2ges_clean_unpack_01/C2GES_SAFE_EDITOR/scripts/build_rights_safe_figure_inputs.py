"""Derive the non-verbatim numerical input used by the paired-difference figure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


EXPECTED_PREDICTION_SHA256 = (
    "AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F"
)
BASELINES = ("graph_no_cf_strict", "semantic_mmr", "textrank")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    got = digest(args.predictions)
    if got != EXPECTED_PREDICTION_SHA256:
        raise SystemExit(f"refused: prediction hash mismatch {got}")
    rows = [json.loads(line) for line in args.predictions.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 210:
        raise SystemExit(f"refused: expected 210 rows, found {len(rows)}")
    values = {
        (row["doc_id"], int(row["budget"]), row["condition"]): float(row["metrics"]["rougeL_f1"])
        for row in rows
    }
    docs = sorted({row["doc_id"] for row in rows})
    doc_index = {doc_id: index for index, doc_id in enumerate(docs, start=1)}
    output = []
    for budget in (5, 10):
        for baseline in BASELINES:
            for doc_id in docs:
                output.append(
                    {
                        "rights_safe_report_index": doc_index[doc_id],
                        "budget": budget,
                        "baseline": baseline,
                        "full_minus_baseline_rougeL_f1": values[(doc_id, budget, "c2ges_full")]
                        - values[(doc_id, budget, baseline)],
                    }
                )
    if len(output) != 90:
        raise AssertionError(len(output))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "paired_rougel_differences_nonverbatim.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    manifest = {
        "schema": "c2ges-rights-safe-figure-input-v1",
        "status": "PASS",
        "source_prediction_sha256": got,
        "source_prediction_included": False,
        "output_path": csv_path.name,
        "output_sha256": digest(csv_path),
        "output_bytes": csv_path.stat().st_size,
        "rows": len(output),
        "contains_verbatim_text": False,
        "definition": "Full-minus-baseline ROUGE-L F1 by rights-safe report index, three registered contrasts and two budgets",
    }
    (args.output_dir / "RIGHTS_SAFE_FIGURE_INPUT_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
