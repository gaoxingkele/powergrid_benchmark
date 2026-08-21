#!/usr/bin/env python3
"""Shared infrastructure for the prepared C2GES baseline scripts.

These scripts are PREPARED but cannot produce results in this repository,
because the original experiment workspace (verification_pilot/agent_audit_40doc
with the 40 documents / 200 questions / agent-verified labels) is not included
here. See MISSING_ARTIFACTS.md in the paper project root for the exact files to
supply. Once the workspace (or just the data directory) is available, each
baseline runs end-to-end with the same protocol as the paper:

- same documents, questions, and agent-verified candidate labels;
- same K=3 prediction budget (configurable via --k for sensitivity checks);
- same evidence precision/recall/F1 (+ ROUGE-L) metrics, reused by import from
  the paper's main.py;
- same document-cluster bootstrap CIs and paired-delta machinery, reused by
  import from main.py (bootstrap_ci / bootstrap_delta);
- optional paired comparison against the paper's Executor predictions when a
  reference details.jsonl (e.g. c2ges_role_selective_graph/details.jsonl) is
  supplied via --reference-details.

Output format mirrors the paper artifact: <out-dir>/details.jsonl with one row
per question and <out-dir>/summary.json with aggregate, role-stratified,
document-level, bootstrap, and paired-comparison blocks.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np

CODE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_ENV_VAR = "C2GES_WORKSPACE"

# Ranker signature: (doc_id, qid, question, role, sids, texts) -> ranked sid list (top-k).
RankFn = Callable[[str, str, str, str, list[str], list[str]], list[str]]


def load_c2ges_main() -> Any:
    """Import the paper's main.py so metric/bootstrap logic is shared, not re-implemented."""
    main_path = CODE_DIR / "main.py"
    spec = importlib.util.spec_from_file_location("c2ges_paper_main", main_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import paper main module from {main_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help=(
            "Experiment workspace root containing verification_pilot/agent_audit_40doc. "
            f"Falls back to ${WORKSPACE_ENV_VAR}. Alternatively pass --data-dir directly."
        ),
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Direct path to the benchmark directory with nerc_*.json documents.",
    )
    parser.add_argument("--out-dir", type=Path, required=True, help="Output directory for details.jsonl and summary.json.")
    parser.add_argument("--k", type=int, default=3, help="Prediction budget (paper primary: 3).")
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--bootstrap-seed", type=int, default=202502, help="Matches the paper's Executor bootstrap seed.")
    parser.add_argument("--limit-docs", type=int, default=0, help="Smoke-test helper. 0 means all documents.")
    parser.add_argument(
        "--reference-details",
        type=Path,
        default=None,
        help=(
            "Optional details.jsonl from the paper's Executor artifact "
            "(e.g. c2ges_role_selective_graph/details.jsonl) for paired comparisons."
        ),
    )
    parser.add_argument(
        "--reference-conditions",
        type=str,
        default="c2ges_full,tfidf_query,sbert_query",
        help="Comma-separated conditions in --reference-details to compare against.",
    )
    return parser


def resolve_data_dir(args: argparse.Namespace) -> Path:
    if args.data_dir is not None:
        data_dir = Path(args.data_dir).expanduser().resolve()
        if not data_dir.is_dir():
            raise FileNotFoundError(f"--data-dir {data_dir} does not exist.")
        return data_dir
    candidates: list[Path] = []
    if args.workspace is not None:
        candidates.append(Path(args.workspace).expanduser().resolve())
    env_value = os.environ.get(WORKSPACE_ENV_VAR, "").strip()
    if env_value:
        candidates.append(Path(env_value).expanduser().resolve())
    for root in candidates:
        data_dir = root / "verification_pilot" / "agent_audit_40doc"
        if data_dir.is_dir():
            return data_dir
    raise FileNotFoundError(
        "Benchmark data not found. Supply --data-dir /path/to/agent_audit_40doc, or "
        f"--workspace / ${WORKSPACE_ENV_VAR} pointing at a workspace containing "
        "verification_pilot/agent_audit_40doc/. This data is NOT part of this repository; "
        "see MISSING_ARTIFACTS.md for the exact request list."
    )


def make_rouge_scorer() -> Any:
    from rouge_score import rouge_scorer  # matches main.py's metric configuration

    return rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)


def evaluate_condition(
    *,
    condition: str,
    docs: list[dict[str, Any]],
    rank_fn: RankFn,
    k: int,
    paper: Any,
    scorer: Any,
) -> list[dict[str, Any]]:
    """Run one ranker over every document-role question, mirroring main.py row schema."""
    rows: list[dict[str, Any]] = []
    for doc in docs:
        sids = [str(sentence["sid"]) for sentence in doc["sentences"]]
        texts = [paper.clean(str(sentence["text"])) for sentence in doc["sentences"]]
        by_sid = dict(zip(sids, texts, strict=True))
        for question in doc["causal_questions"]:
            gold = [str(sid) for sid in question["evidence_sentence_ids"]]
            role = str(question["role"])
            qtext = str(question["question"])
            status = "ok"
            error = ""
            try:
                selected = [str(sid) for sid in rank_fn(str(doc["doc_id"]), str(question["qid"]), qtext, role, sids, texts)][:k]
            except Exception as exc:  # noqa: BLE001 - record per-question failures like main.py
                status = "failed"
                error = f"{type(exc).__name__}: {exc}"
                selected = []
            selected_text = paper.sentence_text(by_sid, selected)
            gold_text = paper.sentence_text(by_sid, gold)
            metric_values = paper.prf(selected, gold)
            rouge_l = (
                scorer.score(gold_text, selected_text)["rougeL"].fmeasure
                if gold_text and selected_text
                else 0.0
            )
            rows.append(
                {
                    "doc_id": str(doc["doc_id"]),
                    "qid": str(question["qid"]),
                    "role": role,
                    "question": qtext,
                    "original_question": qtext,
                    "condition": condition,
                    "status": status,
                    "label_status": "agent_verified_candidate",
                    "evidence_precision": metric_values["evidence_precision"],
                    "evidence_recall": metric_values["evidence_recall"],
                    "evidence_f1": metric_values["evidence_f1"],
                    "rouge_l_selected_evidence_text": float(rouge_l),
                    "predicted_sentence_ids": selected,
                    "gold_sentence_ids": gold,
                    "selected_sentence_text": selected_text,
                    "gold_evidence_text": gold_text,
                    "local_context": paper.local_context(doc["sentences"], selected, gold),
                    "error": error,
                }
            )
    return rows


def aggregate_rows(rows: list[dict[str, Any]], paper: Any) -> dict[str, Any]:
    ok = [row for row in rows if row["status"] == "ok"]
    return {
        "status": "ok" if len(ok) == len(rows) else "partial_or_failed",
        "questions": len(rows),
        "ok_questions": len(ok),
        **{metric: paper.mean([float(row[metric]) for row in ok]) for metric in paper.METRICS},
        **{f"{metric}_std": paper.std([float(row[metric]) for row in ok]) for metric in paper.METRICS},
    }


def role_stratified_rows(rows: list[dict[str, Any]], paper: Any) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role in paper.ROLES:
        subset = [row for row in rows if row["role"] == role and row["status"] == "ok"]
        result[role] = {
            "questions": len(subset),
            **{metric: paper.mean([float(row[metric]) for row in subset]) for metric in paper.METRICS},
            "role_coverage": (
                sum(1 for row in subset if float(row["evidence_f1"]) > 0.0) / len(subset)
                if subset
                else 0.0
            ),
        }
    return result


def document_level_rows(rows: list[dict[str, Any]], paper: Any) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for doc_id in sorted({str(row["doc_id"]) for row in rows}):
        subset = [row for row in rows if row["doc_id"] == doc_id and row["status"] == "ok"]
        result[doc_id] = {
            "questions": len(subset),
            **{metric: paper.mean([float(row[metric]) for row in subset]) for metric in paper.METRICS},
        }
    return result


def bootstrap_blocks(
    rows: list[dict[str, Any]],
    paper: Any,
    samples: int,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    doc_metrics = document_level_rows(rows, paper)
    block: dict[str, Any] = {
        "primary_method": "document-level paired cluster bootstrap over documents",
        "secondary_sensitivity_method": "question-level paired bootstrap",
        "seed": seed,
        "samples": samples,
        "document_level": {},
        "question_level_sensitivity": {},
    }
    for metric in paper.METRICS:
        doc_values = np.asarray(
            [values[metric] for values in doc_metrics.values() if values["questions"] > 0],
            dtype=float,
        )
        q_values = np.asarray(
            [float(row[metric]) for row in rows if row["status"] == "ok"], dtype=float
        )
        block["document_level"][metric] = paper.bootstrap_ci(doc_values, rng, samples)
        block["question_level_sensitivity"][metric] = paper.bootstrap_ci(q_values, rng, samples)
    return block


def load_reference_rows(path: Path, conditions: list[str]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("condition") in conditions:
                grouped[str(row["condition"])].append(row)
    return grouped


def paired_comparisons(
    *,
    condition: str,
    rows: list[dict[str, Any]],
    reference_rows: dict[str, list[dict[str, Any]]],
    paper: Any,
    samples: int,
    seed: int,
) -> dict[str, Any]:
    """Paired document-cluster bootstrap: this baseline minus each reference condition."""
    rng = np.random.default_rng(seed)
    own = {(str(row["doc_id"]), str(row["qid"])): row for row in rows if row["status"] == "ok"}
    comparisons: dict[str, Any] = {
        "delta_definition": f"{condition} minus reference condition (positive favors {condition})",
        "comparisons": {},
    }
    for ref_condition, ref_rows in sorted(reference_rows.items()):
        name = f"{condition}_vs_{ref_condition}"
        comparisons["comparisons"][name] = {}
        for metric in paper.METRICS:
            deltas_by_doc: dict[str, list[float]] = defaultdict(list)
            question_deltas: list[float] = []
            for ref_row in ref_rows:
                if ref_row.get("status", "ok") != "ok":
                    continue
                key = (str(ref_row["doc_id"]), str(ref_row["qid"]))
                own_row = own.get(key)
                if not own_row or metric not in ref_row:
                    continue
                delta = float(own_row[metric]) - float(ref_row[metric])
                deltas_by_doc[key[0]].append(delta)
                question_deltas.append(delta)
            doc_deltas = np.asarray(
                [paper.mean(values) for values in deltas_by_doc.values() if values], dtype=float
            )
            q_deltas = np.asarray(question_deltas, dtype=float)
            comparisons["comparisons"][name][metric] = {
                "document_cluster": paper.bootstrap_delta(doc_deltas, rng, samples),
                "question_sensitivity": paper.bootstrap_delta(q_deltas, rng, samples),
            }
    return comparisons


def run_and_write(
    *,
    condition: str,
    rank_fn: RankFn,
    args: argparse.Namespace,
    extra_metadata: dict[str, Any],
) -> dict[str, Any]:
    """End-to-end flow shared by all prepared baselines."""
    paper = load_c2ges_main()
    data_dir = resolve_data_dir(args)
    docs = paper.load_docs(data_dir)
    if args.limit_docs:
        docs = docs[: int(args.limit_docs)]
    manifest = paper.load_manifest(data_dir, docs)
    scorer = make_rouge_scorer()

    rows = evaluate_condition(
        condition=condition, docs=docs, rank_fn=rank_fn, k=int(args.k), paper=paper, scorer=scorer
    )

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    details_path = out_dir / "details.jsonl"
    summary_path = out_dir / "summary.json"

    summary: dict[str, Any] = {
        "dataset": manifest,
        "task": "NERC report sentences + causal role/question -> evidence_sentence_ids",
        "label_provenance": "agent_verified_candidate; not human gold or expert gold",
        "k": int(args.k),
        "condition": condition,
        "aggregate_metrics_by_condition": {condition: aggregate_rows(rows, paper)},
        "role_stratified_metrics": {condition: role_stratified_rows(rows, paper)},
        "document_level_metrics": {condition: document_level_rows(rows, paper)},
        "bootstrap_confidence_intervals": {
            condition: bootstrap_blocks(rows, paper, int(args.bootstrap_samples), int(args.bootstrap_seed))
        },
        "metadata": {
            "command_lines": [" ".join([sys.executable, *sys.argv])],
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
            "dataset_path": str(data_dir),
            "output_paths": {"summary_json": str(summary_path), "detail_jsonl": str(details_path)},
            "python_executable": sys.executable,
            "bootstrap": {"samples": int(args.bootstrap_samples), "seed": int(args.bootstrap_seed)},
            **extra_metadata,
        },
    }

    if args.reference_details is not None:
        ref_path = Path(args.reference_details).expanduser().resolve()
        if not ref_path.is_file():
            raise FileNotFoundError(
                f"--reference-details {ref_path} not found. The paper's Executor details.jsonl "
                "is one of the missing artifacts listed in MISSING_ARTIFACTS.md."
            )
        ref_conditions = [item.strip() for item in str(args.reference_conditions).split(",") if item.strip()]
        reference_rows = load_reference_rows(ref_path, ref_conditions)
        summary["paired_comparisons"] = paired_comparisons(
            condition=condition,
            rows=rows,
            reference_rows=reference_rows,
            paper=paper,
            samples=int(args.bootstrap_samples),
            seed=int(args.bootstrap_seed),
        )

    paper.write_jsonl(details_path, rows)
    paper.write_json(summary_path, summary)

    agg = summary["aggregate_metrics_by_condition"][condition]
    for metric in paper.METRICS:
        print(
            f"SUMMARY condition={condition} metric={metric} "
            f"mean={agg[metric]:.6f} std={agg[f'{metric}_std']:.6f}"
        )
    if "paired_comparisons" in summary:
        for name, per_metric in summary["paired_comparisons"]["comparisons"].items():
            stats = per_metric["evidence_f1"]["document_cluster"]
            ci = stats["ci95"]
            p_value = stats["bootstrap_two_sided_p"]
            print(
                f"PAIRED: {name} mean_diff={stats['mean_diff']:.6f} "
                f"p_value={(p_value if p_value is not None else 1.0):.6f} "
                f"ci95=({ci['lower']},{ci['upper']})"
            )
    print(f"SUMMARY_JSON: {summary_path}")
    print(f"DETAIL_JSONL: {details_path}")
    return summary


def run_cross_encoder_condition(
    *,
    description: str,
    default_model: str,
    condition: str,
) -> None:
    """Shared entry point for sentence-transformers CrossEncoder-style rerankers (CPU-capable)."""
    parser = build_arg_parser(description)
    parser.add_argument("--model", type=str, default=default_model, help="CrossEncoder checkpoint name or path.")
    parser.add_argument("--device", type=str, default=None, help="torch device, e.g. cpu or cuda. Default: auto.")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=512)
    args = parser.parse_args()

    try:
        from sentence_transformers import CrossEncoder
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "sentence-transformers is required for this baseline: pip install sentence-transformers"
        ) from exc

    model = CrossEncoder(args.model, max_length=int(args.max_length), device=args.device)

    def rank_fn(doc_id: str, qid: str, question: str, role: str, sids: list[str], texts: list[str]) -> list[str]:
        query = f"{role.replace('_', ' ')}: {question}"
        scores = np.asarray(
            model.predict([(query, text) for text in texts], batch_size=int(args.batch_size)),
            dtype=float,
        )
        order = np.argsort(-scores, kind="stable")
        return [sids[i] for i in order[: int(args.k)]]

    run_and_write(
        condition=condition,
        rank_fn=rank_fn,
        args=args,
        extra_metadata={
            "model": str(args.model),
            "query_template": "'{role}: {question}' scored against each sentence",
            "device": str(args.device),
            "batch_size": int(args.batch_size),
            "max_length": int(args.max_length),
        },
    )
