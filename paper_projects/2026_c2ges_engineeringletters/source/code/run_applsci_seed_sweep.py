#!/usr/bin/env python3
"""Run and aggregate the Applied Sciences robustness matrix for learnable C2GES.

Each seed gets an isolated directory. The base runner evaluates K sensitivity in
one trained run, so the evidence budget is varied without retraining or changing
the test set. This wrapper never fabricates domain labels; NERC human annotation
is a separate prerequisite described in the experiment plan.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parents[1] / "workspace" / "fever_runs" / "applsci_seed_sweep"
DEFAULT_GROUPED_DATA = HERE.parents[1] / "workspace" / "fever_benchmark_document_grouped"


def parse_seeds(value: str) -> list[int]:
    seeds = [int(item.strip()) for item in value.split(",") if item.strip()]
    if len(set(seeds)) != len(seeds) or not seeds:
        raise argparse.ArgumentTypeError("seeds must be a non-empty unique comma-separated list")
    return seeds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=parse_seeds, default=parse_seeds("2026,2027,2028,2029,2030"))
    parser.add_argument("--out", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--encoder", default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--eval-k", default="1,3,5,10")
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--train-limit", type=int, default=8000)
    parser.add_argument("--dev-limit", type=int, default=1500)
    parser.add_argument("--test-limit", type=int, default=1500)
    parser.add_argument("--protocol", choices=("oracle-label", "predicted-label", "label-blind"), default="oracle-label")
    parser.add_argument("--predicted-labels", type=Path)
    parser.add_argument("--build-predicted-labels", action="store_true", help="Build leakage-controlled TF-IDF/logistic predictions once before a predicted-label sweep.")
    parser.add_argument("--label-predictor-seed", type=int, default=2026)
    parser.add_argument("--label-predictor-folds", type=int, default=5)
    parser.add_argument("--allow-document-overlap", action="store_true", help="Legacy reproduction only; forwarded to the base runner.")
    parser.add_argument("--skip-existing", action="store_true")
    args = parser.parse_args()
    if args.protocol == "predicted-label" and args.predicted_labels is None and not args.build_predicted_labels:
        parser.error("predicted-label requires --predicted-labels or --build-predicted-labels")
    if args.protocol != "predicted-label" and args.predicted_labels is not None:
        parser.error("--predicted-labels is only valid for predicted-label protocol")
    if args.protocol != "predicted-label" and args.build_predicted_labels:
        parser.error("--build-predicted-labels is only valid for predicted-label protocol")

    args.out.mkdir(parents=True, exist_ok=True)
    data_path = args.data or DEFAULT_GROUPED_DATA
    predicted_labels_path = args.predicted_labels
    if args.build_predicted_labels:
        predictor_dir = args.out / "upstream_label_predictor"
        predicted_labels_path = predictor_dir / "predicted_labels.json"
        if not predicted_labels_path.exists():
            predictor_command = [
                sys.executable,
                str(HERE / "predict_fever_labels.py"),
                "--data",
                str(data_path),
                "--out",
                str(predictor_dir),
                "--seed",
                str(args.label_predictor_seed),
                "--folds",
                str(args.label_predictor_folds),
                "--train-limit",
                str(args.train_limit),
                "--dev-limit",
                str(args.dev_limit),
                "--test-limit",
                str(args.test_limit),
            ]
            subprocess.run(predictor_command, check=True)
        provenance_path = predictor_dir / "provenance.json"
        if not provenance_path.exists():
            raise RuntimeError(f"missing upstream predictor provenance: {provenance_path}")
        predictor_provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        config = predictor_provenance.get("configuration", {})
        expected = {
            "data": str(data_path.resolve()),
            "seed": args.label_predictor_seed,
            "folds": args.label_predictor_folds,
            "train_limit": args.train_limit,
            "dev_limit": args.dev_limit,
            "test_limit": args.test_limit,
        }
        mismatches = {key: {"expected": value, "found": config.get(key)} for key, value in expected.items() if config.get(key) != value}
        if mismatches:
            raise RuntimeError(f"refusing stale/incompatible upstream predictions: {mismatches}")
    summaries = []
    for seed in args.seeds:
        seed_dir = args.out / f"seed_{seed}"
        summary_path = seed_dir / "summary.json"
        if not (args.skip_existing and summary_path.exists()):
            command = [
                sys.executable,
                str(HERE / "c2ges_learnable.py"),
                "--out",
                str(seed_dir),
                "--seed",
                str(seed),
                "--encoder",
                args.encoder,
                "--eval-k",
                args.eval_k,
                "--epochs",
                str(args.epochs),
                "--bootstrap-samples",
                str(args.bootstrap_samples),
                "--device",
                args.device,
                "--train-limit",
                str(args.train_limit),
                "--dev-limit",
                str(args.dev_limit),
                "--test-limit",
                str(args.test_limit),
                "--protocol",
                args.protocol,
            ]
            command.extend(["--data", str(data_path)])
            if predicted_labels_path:
                command.extend(["--predicted-labels", str(predicted_labels_path)])
            if args.allow_document_overlap:
                command.append("--allow-document-overlap")
            subprocess.run(command, check=True)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("protocol") != args.protocol:
            raise RuntimeError(
                f"{summary_path} uses protocol={summary.get('protocol')!r}, expected {args.protocol!r}; "
                "do not mix legacy or cross-protocol runs in one aggregate"
            )
        audit = summary.get("document_leakage_audit", {})
        if not audit.get("passed", False) and not args.allow_document_overlap:
            raise RuntimeError(f"{summary_path} does not pass the Wikipedia-document leakage gate")
        summaries.append(summary)

    methods = ["full", "no_role", "no_graph", "query_only", "tfidf", "bm25", "sbert", "lexcue"]
    aggregate: dict[str, object] = {
        "protocol": args.protocol,
        "protocol_definition": summaries[0].get("protocol_definition"),
        "end_to_end": summaries[0].get("end_to_end"),
        "design": "five-seed training robustness with Wikipedia-document-disjoint FEVER splits",
        "seeds": args.seeds,
        "encoder": args.encoder,
        "k_sensitivity": {},
        "bootstrap_cluster_unit": "underlying_wikipedia_document",
        "document_leakage_audits": [summary.get("document_leakage_audit") for summary in summaries],
        "upstream_predicted_labels": str(predicted_labels_path.resolve()) if predicted_labels_path else None,
        "upstream_predicted_labels_sha256": (
            hashlib.sha256(predicted_labels_path.read_bytes()).hexdigest() if predicted_labels_path else None
        ),
    }
    all_k = sorted({key for summary in summaries for key in summary["k_sensitivity"]}, key=int)
    for k in all_k:
        aggregate["k_sensitivity"][k] = {}
        for method in methods:
            values = [summary["k_sensitivity"][k]["test"][method]["evidence_f1"] for summary in summaries]
            aggregate["k_sensitivity"][k][method] = {
                "mean_f1": statistics.fmean(values),
                "sample_std_f1": statistics.stdev(values) if len(values) > 1 else 0.0,
                "min_f1": min(values),
                "max_f1": max(values),
                "per_seed_f1": values,
            }

    output_path = args.out / "aggregate_summary.json"
    output_path.write_text(json.dumps(aggregate, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
