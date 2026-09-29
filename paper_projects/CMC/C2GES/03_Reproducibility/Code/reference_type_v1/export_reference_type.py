"""Ship the reference-type sensitivity records (bounds + per-document pairs)."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
SOURCE = PROJECT / "tmp/ref_type_400.json"
BOUNDS = PROJECT / "tmp/ref_type_400_bounds.json"
BASE = PROJECT / "03_Reproducibility/Data/reference_type_v1"
PAIRS = (("Full", "no_path"), ("AB2", "AB0"), ("TextRank", "no_path"), ("Lead", "no_path"))


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    cells: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for row in payload["rows"]:
        cells[(row["doc_id"], row["key"])][row["condition"]] = row

    csv_path = BASE / "reference_type_400_pairs.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["doc_id", "contrast", "budget", "value"])
        written = 0
        for (doc_id, key), conditions in sorted(cells.items()):
            for cand, ref in PAIRS:
                if cand in conditions and ref in conditions:
                    writer.writerow(
                        [doc_id, f"{cand} - {ref}", key,
                         conditions[cand]["rougeL_f1"] - conditions[ref]["rougeL_f1"]]
                    )
                    written += 1

    bounds = json.loads(BOUNDS.read_text(encoding="utf-8"))
    bounds["schema"] = "c2ges-reference-type-400-bounds-v1"
    bounds["provenance"] = {
        "protocol": "03_Reproducibility/Data/reference_type_v1/PROTOCOL_reference_type_v1.md",
        "runner": "03_Reproducibility/Code/reference_type_v1/run_reference_type.py --shard i/8",
        "merge": "03_Reproducibility/Code/govreport_transfer_v1/merge_govreport_shards.py",
        "documents": payload["documents"],
        "corpus": payload["corpus"],
        "note": "reference-type sensitivity (human-written highlights); no domain claim",
    }
    (BASE / "reference_type_400_bounds_v1.json").write_text(
        json.dumps(bounds, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {csv_path.name} ({written} pairs) and reference_type_400_bounds_v1.json")


if __name__ == "__main__":
    main()
