"""Run the frozen C2GES arm set on a stratified GovReport test sample (G2 pilot).

Protocol: Data/govreport_transfer_v1/PROTOCOL_govreport_transfer_v1.md (frozen
before any outcome).  The raw corpus stays outside the release scope; this script
emits derived numbers only.

Usage:
    python -B run_govreport_transfer.py --corpus <govreport_test_full.jsonl> \
        --json <out.json> [--documents 100]
"""

from __future__ import annotations

import argparse
import json
import random
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
EXTERNAL = PROJECT / "03_Reproducibility" / "Data" / "external_prospective_v1"
sys.path.insert(0, str(EXTERNAL))
import run_external_arms_v3 as A3  # noqa: E402

ARMS = ("AB0", "AB1", "AB2", "no_path", "Full", "TextRank", "Lead")
BUDGETS = (("word", 110), ("word", 260), ("unit", 5), ("unit", 10))
STRATA = 5
SEED = 20260926
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def units_for(report: str) -> list[dict]:
    units: list[dict] = []
    position = 0
    for block_index, block in enumerate(report.split("\n")):
        for sentence in SENTENCE_SPLIT.split(block):
            text = re.sub(r"\s+", " ", sentence).strip()
            if len(text.split()) < 3:
                continue
            position += 1
            units.append(
                {
                    "page": block_index,             # block index, used for ordering only
                    "sid": f"u{position:05d}",
                    "text": text,
                    "unit_type": "body",
                }
            )
    return units


def stratified_sample(rows: list[dict], documents: int) -> list[dict]:
    ordered = sorted(rows, key=lambda r: r["report_chars"])
    rng = random.Random(SEED)
    per_stratum = documents // STRATA
    sample: list[dict] = []
    for index in range(STRATA):
        start = index * len(ordered) // STRATA
        end = (index + 1) * len(ordered) // STRATA
        sample.extend(rng.sample(ordered[start:end], min(per_stratum, end - start)))
    return sorted(sample, key=lambda r: r["doc_id"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True, help="govreport_test_full.jsonl")
    parser.add_argument("--json", required=True)
    parser.add_argument("--documents", type=int, default=100)
    parser.add_argument("--limit", type=int, default=0, help="debug: cap the number of sampled documents")
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=None,
        help="resumable per-document JSONL (default: <json>.partial.jsonl)",
    )
    parser.add_argument(
        "--shard",
        default=None,
        help="run a disjoint slice of the frozen sample, e.g. 3/12; merge the shard JSONs afterwards",
    )
    args = parser.parse_args()

    # Read line by line: report text can contain U+0085/U+2028, which str.splitlines()
    # would treat as record separators even though they are valid inside a JSON string.
    rows = []
    with Path(args.corpus).open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    sample = stratified_sample(rows, args.documents)
    if args.shard:
        index_text, _, total_text = args.shard.partition("/")
        shard_index, shard_total = int(index_text), int(total_text)
        if not 0 <= shard_index < shard_total:
            raise SystemExit("--shard must satisfy 0 <= index < total")
        sample = [record for position, record in enumerate(sample) if position % shard_total == shard_index]
        print(f"shard {shard_index}/{shard_total}: {len(sample)} documents", flush=True)
    if args.limit:
        sample = sample[: args.limit]
    print(f"test rows {len(rows)}; sample {len(sample)} (seed {SEED}, {STRATA} strata)", flush=True)

    checkpoint = args.checkpoint or Path(args.json).with_suffix(".partial.jsonl")
    done: dict[str, dict] = {}
    if checkpoint.is_file():
        with checkpoint.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    record = json.loads(line)
                    done[record["doc_id"]] = record
        print(f"resuming: {len(done)} documents already computed in {checkpoint.name}", flush=True)

    settings = A3.R.load_protocol()["textrank"]
    out_rows: list[dict] = []
    diagnostics: list[dict] = []
    for index, record in enumerate(sample, start=1):
        if record["doc_id"] in done:
            cached = done[record["doc_id"]]
            out_rows.extend(cached["rows"])
            diagnostics.append(cached["diagnostic"])
            continue
        units = units_for(record["report"])
        prepared = A3.R.prepare_report(
            {
                "doc_id": record["doc_id"],
                "report_series_id": "govreport_test",
                "candidate_sentences": units,
                "reference_summary": record["summary"],
            }
        )
        nodes = prepared["graph"].nodes
        diagnostics.append(
            {
                "doc_id": record["doc_id"],
                "report_chars": record["report_chars"],
                "summary_chars": record["summary_chars"],
                "candidate_units": len(nodes),
                "role_coverage": round(
                    sum(1 for node in nodes if node.dominant_role) / max(1, len(nodes)), 4
                ),
            }
        )
        first_row = len(out_rows)
        for kind, budget in BUDGETS:
            for condition in ARMS:
                result = A3.run_condition(prepared, condition, kind, budget, settings)
                out_rows.append(
                    {
                        "doc_id": record["doc_id"],
                        "condition": condition,
                        "kind": kind,
                        "budget": budget,
                        "key": f"{kind}:{budget}",
                        "rougeL_f1": result["rougeL_f1"],
                        "units": result["units"],
                        "words": result["words"],
                    }
                )
        document_rows = out_rows[first_row:]
        with checkpoint.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {"doc_id": record["doc_id"], "diagnostic": diagnostics[-1], "rows": document_rows},
                    ensure_ascii=False,
                )
                + "\n"
            )
        print(f"[{index}/{len(sample)}] {record['doc_id']} units={len(nodes)}", flush=True)

    contrasts = []
    for kind, budget in BUDGETS:
        key = f"{kind}:{budget}"
        for cand, ref in (("AB2", "AB0"), ("AB1", "AB0"), ("Full", "no_path"), ("TextRank", "no_path"), ("Lead", "no_path")):
            item = A3.contrast(out_rows, ref, cand, key)
            if item:
                contrasts.append(item)
    for item, adjusted in zip(contrasts, A3.holm([c["p"] for c in contrasts])):
        item["holm"] = round(adjusted, 6)

    payload = {
        "schema": "c2ges-govreport-transfer-v1",
        "protocol": "03_Reproducibility/Data/govreport_transfer_v1/PROTOCOL_govreport_transfer_v1.md",
        "claim_class": "OUT_OF_DOMAIN_ROBUSTNESS_TRANSFER_NOT_DOMAIN_EVIDENCE",
        "corpus": "ccdv/govreport-summarization test split (CRS + GAO reports, CC BY 4.0)",
        "test_rows_available": len(rows),
        "documents": len(sample),
        "seed": SEED,
        "strata": STRATA,
        "arms": list(ARMS),
        "budgets": [f"{kind}:{budget}" for kind, budget in BUDGETS],
        "diagnostics": {
            "role_coverage_mean": round(statistics.fmean(d["role_coverage"] for d in diagnostics), 4),
            "role_coverage_min": min(d["role_coverage"] for d in diagnostics),
            "candidate_units_median": statistics.median(d["candidate_units"] for d in diagnostics),
        },
        "per_document": diagnostics,
        "contrasts": contrasts,
        "rows": out_rows,
    }
    target = Path(args.json)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {target} ({len(out_rows)} rows)")
    for item in contrasts:
        print(
            f"  {item['budget']:9s} {item['contrast']:18s} mean={item['mean']:+.5f} "
            f"p={item['p']:.4f} holm={item['holm']:.4f} neg/pos/zero="
            f"{item['negative']}/{item['positive']}/{item['zero']}"
        )


if __name__ == "__main__":
    main()
