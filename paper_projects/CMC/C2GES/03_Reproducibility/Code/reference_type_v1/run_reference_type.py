"""Run the frozen arm set against human-written highlights (CNN/DailyMail).

Mirrors `run_govreport_transfer.py`: same arms, budgets, statistics, sharding and
checkpointing; only the corpus and the reference definition differ.  See
`Data/reference_type_v1/PROTOCOL_reference_type_v1.md` (frozen before any outcome).
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


def units_for(article: str) -> list[dict]:
    units: list[dict] = []
    position = 0
    for block_index, block in enumerate(article.split("\n")):
        for sentence in SENTENCE_SPLIT.split(block):
            text = re.sub(r"\s+", " ", sentence).strip()
            if len(text.split()) < 3:
                continue
            position += 1
            units.append({"page": block_index, "sid": f"u{position:05d}", "text": text, "unit_type": "body"})
    return units


def stratified_sample(rows: list[dict], documents: int) -> list[dict]:
    ordered = sorted(rows, key=lambda r: r["article_chars"])
    rng = random.Random(SEED)
    per_stratum = max(1, documents // STRATA)
    sample: list[dict] = []
    for index in range(STRATA):
        start = index * len(ordered) // STRATA
        end = (index + 1) * len(ordered) // STRATA
        want = min(per_stratum, max(0, end - start))
        if want:
            sample.extend(rng.sample(ordered[start:end], want))
    return sorted(sample, key=lambda r: r["doc_id"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--documents", type=int, default=400)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--shard", default=None)
    parser.add_argument("--checkpoint", type=Path, default=None)
    args = parser.parse_args()

    rows = []
    with Path(args.corpus).open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    sample = stratified_sample(rows, args.documents)
    if args.shard:
        index_text, _, total_text = args.shard.partition("/")
        shard_index, shard_total = int(index_text), int(total_text)
        sample = [r for position, r in enumerate(sample) if position % shard_total == shard_index]
        print(f"shard {shard_index}/{shard_total}: {len(sample)} documents", flush=True)
    if args.limit:
        sample = sample[: args.limit]
    print(f"rows {len(rows)}; sample {len(sample)} (seed {SEED}, {STRATA} strata)", flush=True)

    checkpoint = args.checkpoint or Path(args.json).with_suffix(".partial.jsonl")
    done: dict[str, dict] = {}
    if checkpoint.is_file():
        with checkpoint.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    record = json.loads(line)
                    done[record["doc_id"]] = record
        print(f"resuming: {len(done)} documents already computed", flush=True)

    settings = A3.R.load_protocol()["textrank"]
    out_rows: list[dict] = []
    diagnostics: list[dict] = []
    for index, record in enumerate(sample, start=1):
        if record["doc_id"] in done:
            cached = done[record["doc_id"]]
            out_rows.extend(cached["rows"])
            diagnostics.append(cached["diagnostic"])
            continue
        units = units_for(record["article"])
        prepared = A3.R.prepare_report(
            {
                "doc_id": record["doc_id"],
                "report_series_id": "cnndm_test",
                "candidate_sentences": units,
                "reference_summary": record["highlights"],
            }
        )
        nodes = prepared["graph"].nodes
        diagnostics.append(
            {
                "doc_id": record["doc_id"],
                "article_chars": record["article_chars"],
                "highlight_chars": record["highlight_chars"],
                "candidate_units": len(nodes),
                "role_coverage": round(sum(1 for node in nodes if node.dominant_role) / max(1, len(nodes)), 4),
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
        with checkpoint.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {"doc_id": record["doc_id"], "diagnostic": diagnostics[-1], "rows": out_rows[first_row:]},
                    ensure_ascii=False,
                )
                + "\n"
            )
        print(f"[{index}/{len(sample)}] {record['doc_id']} units={len(nodes)}", flush=True)

    contrasts = []
    for kind, budget in BUDGETS:
        key = f"{kind}:{budget}"
        for cand, ref in (
            ("AB2", "AB0"),
            ("AB1", "AB0"),
            ("Full", "no_path"),
            ("TextRank", "no_path"),
            ("Lead", "no_path"),
        ):
            item = A3.contrast(out_rows, ref, cand, key)
            if item:
                contrasts.append(item)
    for item, adjusted in zip(contrasts, A3.holm([c["p"] for c in contrasts])):
        item["holm"] = round(adjusted, 6)

    payload = {
        "schema": "c2ges-reference-type-v1",
        "protocol": "03_Reproducibility/Data/reference_type_v1/PROTOCOL_reference_type_v1.md",
        "claim_class": "REFERENCE_TYPE_SENSITIVITY_NOT_DOMAIN_EVIDENCE",
        "corpus": "abisee/cnn_dailymail 3.0.0 test slice (human-written highlights)",
        "documents": len({row["doc_id"] for row in out_rows}),
        "seed": SEED,
        "strata": STRATA,
        "arms": list(ARMS),
        "budgets": [f"{kind}:{budget}" for kind, budget in BUDGETS],
        "diagnostics": {
            "role_coverage_mean": round(statistics.fmean(d["role_coverage"] for d in diagnostics), 4),
            "role_coverage_min": min(d["role_coverage"] for d in diagnostics),
            "candidate_units_median": statistics.median(d["candidate_units"] for d in diagnostics),
            "highlight_chars_median": statistics.median(d["highlight_chars"] for d in diagnostics),
        },
        "per_document": diagnostics,
        "contrasts": contrasts,
        "rows": out_rows,
    }
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.json} ({len(out_rows)} rows over {payload['documents']} documents)")
    for item in contrasts:
        print(
            f"  {item['budget']:9s} {item['contrast']:18s} mean={item['mean']:+.5f} p={item['p']:.4f} "
            f"holm={item['holm']:.4f} neg/pos/zero={item['negative']}/{item['positive']}/{item['zero']}"
        )


if __name__ == "__main__":
    main()
