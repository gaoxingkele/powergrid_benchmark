"""Ship a compact, rights-safe summary of the full-split transfer run.

The raw arm x budget x document record is ~6.5 MB and fully regenerable from the
protocol (sharded runner + merge).  What ships instead is the bounds record plus
one row per document and contrast, so any reader can recompute the statistics
without carrying the raw file.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
SOURCE = PROJECT / "tmp/govreport_transfer_full970.json"
TARGET_JSON = PROJECT / "03_Reproducibility/Data/govreport_transfer_v1/govreport_transfer_full970_bounds_v1.json"
TARGET_CSV = PROJECT / "03_Reproducibility/Data/govreport_transfer_v1/govreport_transfer_full970_pairs.csv"

PAIRS = (("Full", "no_path", "path layer"), ("AB2", "AB0", "role layer"),
         ("TextRank", "no_path", "TextRank baseline"), ("Lead", "no_path", "Lead baseline"))


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    cells: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for row in payload["rows"]:
        cells[(row["doc_id"], row["key"])][row["condition"]] = row

    counts: dict[tuple[str, str], list[float]] = defaultdict(list)
    with TARGET_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["doc_id", "contrast", "budget", "value"])
        for (doc_id, key), conditions in sorted(cells.items()):
            for cand, ref, label in PAIRS:
                if cand in conditions and ref in conditions:
                    value = conditions[cand]["rougeL_f1"] - conditions[ref]["rougeL_f1"]
                    counts[(label, key)].append(value)
                    writer.writerow([doc_id, f"{cand} - {ref}", key, value])

    summary = {
        "schema": "c2ges-govreport-transfer-full970-v1",
        "documents": payload["documents"],
        "shards": payload.get("shards"),
        "provenance": {
            "protocol": "03_Reproducibility/Data/govreport_transfer_v1/PROTOCOL_govreport_transfer_v1.md",
            "runner": "03_Reproducibility/Code/govreport_transfer_v1/run_govreport_transfer.py --shard i/12",
            "merge": "03_Reproducibility/Code/govreport_transfer_v1/merge_govreport_shards.py",
            "note": "frozen strata fully sampled (970 of 973 test rows); sensitivity, not a new freeze",
        },
        "diagnostics": payload["diagnostics"],
        "pairs_file": TARGET_CSV.name,
        "pair_counts": {f"{label} @ {key}": len(values) for (label, key), values in sorted(counts.items())},
    }
    TARGET_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {TARGET_CSV.name} ({sum(len(v) for v in counts.values())} pairs) and {TARGET_JSON.name}")


if __name__ == "__main__":
    main()
