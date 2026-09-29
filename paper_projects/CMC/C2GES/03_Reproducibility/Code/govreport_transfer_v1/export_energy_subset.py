"""Ship the energy-subset records (bounds + per-document pairs) of the transfer layer."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
SOURCE = PROJECT / "tmp/govreport_energy160.json"
BOUNDS = PROJECT / "tmp/govreport_energy160_bounds.json"
BASE = PROJECT / "03_Reproducibility/Data/govreport_transfer_v1"
PAIRS = (("Full", "no_path"), ("AB2", "AB0"), ("TextRank", "no_path"), ("Lead", "no_path"))


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    cells: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for row in payload["rows"]:
        cells[(row["doc_id"], row["key"])][row["condition"]] = row

    csv_path = BASE / "govreport_energy160_pairs.csv"
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
    bounds["schema"] = "c2ges-govreport-energy160-bounds-v1"
    bounds["provenance"] = {
        "protocol": "03_Reproducibility/Data/govreport_transfer_v1/PROTOCOL_govreport_energy_subset_addendum.md",
        "selector": "03_Reproducibility/Code/govreport_transfer_v1/select_energy_subset.py",
        "selection": ">= 3 distinct keywords of the frozen list, report body only",
        "documents": payload["documents"],
        "note": "convenience stratum by topic words; not a random sample of energy-domain documents",
    }
    (BASE / "govreport_energy160_bounds_v1.json").write_text(
        json.dumps(bounds, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {csv_path.name} ({written} pairs) and govreport_energy160_bounds_v1.json")


if __name__ == "__main__":
    main()
