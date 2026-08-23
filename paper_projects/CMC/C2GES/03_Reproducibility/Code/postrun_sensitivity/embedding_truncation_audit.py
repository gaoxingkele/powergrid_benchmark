#!/usr/bin/env python3
"""Audit MiniLM token lengths without releasing candidate text."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

from transformers import AutoTokenizer


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_OUTPUT = PROJECT / "03_Reproducibility" / "Data" / "postrun_embedding_audit"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def percentile(values: list[int], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def summarize(values: list[int], maximum: int) -> dict[str, float | int]:
    return {
        "n_candidates": len(values),
        "mean_tokens": statistics.fmean(values),
        "median_tokens": percentile(values, 0.5),
        "p90_tokens": percentile(values, 0.9),
        "p95_tokens": percentile(values, 0.95),
        "p99_tokens": percentile(values, 0.99),
        "max_tokens": max(values),
        "n_over_max_seq_length": sum(value > maximum for value in values),
        "fraction_over_max_seq_length": sum(value > maximum for value in values) / len(values),
        "n_over_512": sum(value > 512 for value in values),
    }


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=Path, required=True)
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    sentence_config = json.loads((args.model_snapshot / "sentence_bert_config.json").read_text(encoding="utf-8"))
    maximum = int(sentence_config["max_seq_length"])
    tokenizer = AutoTokenizer.from_pretrained(args.model_snapshot, local_files_only=True)

    report_rows = []
    all_lengths: list[int] = []
    split_lengths: dict[str, list[int]] = {"dev": [], "test": []}
    for split, path in (("dev", args.dev), ("test", args.test)):
        for report in read_rows(path):
            texts = [row["text"] for row in report["candidate_sentences"]]
            encodings = tokenizer(texts, add_special_tokens=True, truncation=False, padding=False)
            lengths = [len(ids) for ids in encodings["input_ids"]]
            all_lengths.extend(lengths)
            split_lengths[split].extend(lengths)
            summary = summarize(lengths, maximum)
            report_rows.append({"split": split, "doc_id": report["doc_id"], **summary})

    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "embedding_truncation_per_report.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(report_rows[0]))
        writer.writeheader()
        writer.writerows(report_rows)
    payload = {
        "analysis_id": "C2GES-v0.3.1-postrun-MiniLM-truncation-audit-v1",
        "status": "post_run_diagnostic_not_confirmatory",
        "model": {
            "name": "sentence-transformers/all-MiniLM-L6-v2",
            "revision": args.model_snapshot.name,
            "tokenizer_class": tokenizer.__class__.__name__,
            "vocab_size": tokenizer.vocab_size,
            "model_max_position_embeddings": json.loads((args.model_snapshot / "config.json").read_text(encoding="utf-8"))["max_position_embeddings"],
            "sentence_transformers_max_seq_length": maximum,
            "padding": False,
            "truncation_during_audit": False,
            "production_policy": "SentenceTransformer encodes with max_seq_length=256",
        },
        "inputs": {
            "dev_sha256": sha256(args.dev),
            "test_sha256": sha256(args.test),
            "dev_reports": len(read_rows(args.dev)),
            "test_reports": len(read_rows(args.test)),
        },
        "overall": summarize(all_lengths, maximum),
        "by_split": {split: summarize(values, maximum) for split, values in split_lengths.items()},
        "token_length_bins": dict(sorted(Counter(
            "<=128" if value <= 128 else "129-256" if value <= 256 else "257-512" if value <= 512 else ">512"
            for value in all_lengths
        ).items())),
        "privacy": "No candidate or reference text is written to the output artifacts.",
    }
    (args.output / "embedding_truncation_audit.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    report = [
        "# C2GES MiniLM truncation audit",
        "",
        "Status: post-run diagnostic; no embeddings or selections were regenerated.",
        "",
        f"The frozen model is `sentence-transformers/all-MiniLM-L6-v2` at revision `{args.model_snapshot.name}`. Its Sentence-Transformers configuration sets `max_seq_length={maximum}` although the underlying BERT configuration supports 512 positions. Token lengths below include special tokens and were measured with truncation disabled solely to quantify what the production encoder would truncate.",
        "",
        "| Split | Candidates | Median tokens | P95 | Maximum | Over 256 | Fraction over 256 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for split in ("dev", "test"):
        item = payload["by_split"][split]
        report.append(f"| {split} | {item['n_candidates']} | {item['median_tokens']:.1f} | {item['p95_tokens']:.1f} | {item['max_tokens']} | {item['n_over_max_seq_length']} | {item['fraction_over_max_seq_length']:.4f} |")
    item = payload["overall"]
    report.append(f"| all | {item['n_candidates']} | {item['median_tokens']:.1f} | {item['p95_tokens']:.1f} | {item['max_tokens']} | {item['n_over_max_seq_length']} | {item['fraction_over_max_seq_length']:.4f} |")
    report.extend(["", "This audit measures exposure to truncation; it does not establish whether truncation changed rankings. A ranking comparison with layout-aware short units or an explicitly pooled long-context representation remains required before claiming truncation robustness.", ""])
    (args.output / "EMBEDDING_TRUNCATION_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(args.output), "overall": payload["overall"]}))


if __name__ == "__main__":
    main()
