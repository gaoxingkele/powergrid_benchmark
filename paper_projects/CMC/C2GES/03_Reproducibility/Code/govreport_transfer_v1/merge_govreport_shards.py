"""Merge disjoint shard outputs of the GovReport transfer runner into one record.

Each shard is produced by `run_govreport_transfer.py --shard i/N`; this script
concatenates rows and diagnostics, then recomputes the contrasts and the Holm
family exactly as the single-process runner does.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
EXTERNAL = PROJECT / "03_Reproducibility" / "Data" / "external_prospective_v1"
sys.path.insert(0, str(EXTERNAL))
import run_external_arms_v3 as A3  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shards", nargs="+", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    payloads = [json.loads(Path(name).read_text(encoding="utf-8")) for name in args.shards]
    head = payloads[0]
    rows = [row for payload in payloads for row in payload["rows"]]
    diagnostics = [item for payload in payloads for item in payload["per_document"]]
    docs = {row["doc_id"] for row in rows}
    if len(docs) != len(diagnostics):
        raise AssertionError(f"row/diagnostic mismatch: {len(docs)} documents vs {len(diagnostics)} diagnostics")

    contrasts = []
    for kind, budget in (("word", 110), ("word", 260), ("unit", 5), ("unit", 10)):
        key = f"{kind}:{budget}"
        for cand, ref in (
            ("AB2", "AB0"),
            ("AB1", "AB0"),
            ("Full", "no_path"),
            ("TextRank", "no_path"),
            ("Lead", "no_path"),
        ):
            item = A3.contrast(rows, ref, cand, key)
            if item:
                contrasts.append(item)
    for item, adjusted in zip(contrasts, A3.holm([c["p"] for c in contrasts])):
        item["holm"] = round(adjusted, 6)

    merged = {
        **{k: v for k, v in head.items() if k not in ("contrasts", "rows", "per_document", "documents")},
        "documents": len(diagnostics),
        "shards": len(payloads),
        "diagnostics": {
            "role_coverage_mean": round(
                statistics.fmean(d["role_coverage"] for d in diagnostics), 4
            ),
            "role_coverage_min": min(d["role_coverage"] for d in diagnostics),
            "candidate_units_median": statistics.median(d["candidate_units"] for d in diagnostics),
        },
        "per_document": sorted(diagnostics, key=lambda d: d["doc_id"]),
        "contrasts": contrasts,
        "rows": rows,
    }
    target = Path(args.json)
    target.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    print(f"merged {len(payloads)} shards -> {target} ({merged['documents']} documents, {len(rows)} rows)")
    for item in contrasts:
        print(
            f"  {item['budget']:9s} {item['contrast']:18s} mean={item['mean']:+.5f} "
            f"p={item['p']:.4f} holm={item['holm']:.4f} neg/pos/zero="
            f"{item['negative']}/{item['positive']}/{item['zero']}"
        )


if __name__ == "__main__":
    main()
