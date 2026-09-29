"""Derived bounds and diagnostics for the GovReport transfer layer (G2).

Reuses the equivalence-bound machinery so the transfer layer is reported with the
same quantities as the power-domain layers: mean, discordant split, one-sided 95%
bootstrap upper limit, and a leave-one-out envelope.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
BOUNDS_CODE = PROJECT / "03_Reproducibility" / "Code" / "equivalence_bounds_v1"
sys.path.insert(0, str(BOUNDS_CODE))
import run_equivalence_bounds as EB  # noqa: E402

DEFAULT_SOURCE = PROJECT / "03_Reproducibility" / "Data" / "govreport_transfer_v1" / "govreport_transfer_v1.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--json", type=Path, default=None, help="output path (default: beside the source)")
    parser.add_argument("--draws", type=int, default=200000)
    args = parser.parse_args()
    source = args.source

    payload = json.loads(source.read_text(encoding="utf-8"))
    cells: dict[tuple[str, str], dict[str, dict]] = {}
    for row in payload["rows"]:
        cells.setdefault((row["doc_id"], row["key"]), {})[row["condition"]] = row

    records = []
    for cand, ref, label in (
        ("Full", "no_path", "path layer"),
        ("AB2", "AB0", "role layer"),
        ("TextRank", "no_path", "TextRank baseline"),
        ("Lead", "no_path", "Lead baseline"),
    ):
        for key in ("word:110", "word:260", "unit:5", "unit:10"):
            pairs = EB.paired(cells, cand, ref, key)
            if not pairs:
                continue
            item = EB.summarise(pairs, draws=args.draws, loo=len(pairs) <= 200)
            item.update({"contrast": f"{cand} - {ref}", "label": label, "budget": key})
            records.append(item)

    out = {
        "schema": "c2ges-govreport-transfer-bounds-v1",
        "source": source.name,
        "source_sha256": EB.sha256(source),
        "documents": payload["documents"],
        "diagnostics": payload["diagnostics"],
        "records": records,
        "headline": {},
    }
    for label in ("path layer", "role layer", "TextRank baseline", "Lead baseline"):
        sub = [r for r in records if r["label"] == label]
        if not sub:
            continue
        out["headline"][label] = {
            "max_upper_limit_one_sided_95": max(r["upper_limit_one_sided_95"] for r in sub),
            "upper_limit_max_under_leave_one_out": (
                None
                if any(r["leave_one_out"] is None for r in sub)
                else max(r["leave_one_out"]["upper_limit_max"] for r in sub)
            ),
            "min_mean": min(r["mean"] for r in sub),
            "max_mean": max(r["mean"] for r in sub),
            "holm_min_budget": min(
                (
                    (c["holm"], c["budget"])
                    for c in payload["contrasts"]
                    if c["contrast"] == f"{'Full - no_path' if label == 'path layer' else 'AB2 - AB0'}"
                    and label in ("path layer", "role layer")
                ),
                default=(None, None),
            ),
        }

    target = args.json or source.with_name("govreport_transfer_bounds_v1.json")
    target.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("role coverage:", json.dumps(payload["diagnostics"], ensure_ascii=False))
    for item in records:
        loo = item["leave_one_out"]
        loo_text = (
            "LOO=n/a"
            if loo is None
            else f"LOOmean=[{loo['mean_min']:+.5f},{loo['mean_max']:+.5f}] LOOUB={loo['upper_limit_max']:+.5f}"
        )
        print(
            f"  {item['label']:18s} {item['budget']:9s} mean={item['mean']:+.5f} "
            f"neg/pos/zero={item['negative']}/{item['positive']}/{item['zero']} "
            f"UB95={item['upper_limit_one_sided_95']:+.5f} {loo_text}"
        )
    print("headline:", json.dumps(out["headline"], indent=2))
    print("median units:", statistics.median(d["candidate_units"] for d in payload["per_document"]))


if __name__ == "__main__":
    main()
