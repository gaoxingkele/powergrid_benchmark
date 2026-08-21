#!/usr/bin/env python3
"""Rescore frozen predictions on the 75-question simulated-expert subset."""

from __future__ import annotations

import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
MAIN_DETAILS = (
    PROJECT / "source" / "supplement" / "c2ges_role_selective_graph" / "details.jsonl"
)
EXTRA_DETAILS = {
    "crossencoder_msmarco_minilm": (
        PROJECT / "baseline_runs_2026-07-20" / "crossencoder" / "details.jsonl"
    ),
    "bge_reranker_base": (
        PROJECT / "baseline_runs_2026-07-20" / "bge_reranker" / "details.jsonl"
    ),
    "llm_zeroshot::deepseek-chat": (
        PROJECT / "baseline_runs_2026-07-20" / "llm_zeroshot_deepseek" / "details.jsonl"
    ),
}
CONDITIONS = [
    "tfidf_query",
    "bm25_query",
    "sbert_query",
    "c2ges_query_only",
    "c2ges_no_role",
    "c2ges_no_graph",
    "c2ges_full",
    "bge_reranker_base",
    "crossencoder_msmarco_minilm",
    "llm_zeroshot::deepseek-chat",
]
BOOTSTRAP_SAMPLES = 10000
BOOTSTRAP_SEED = 20260724


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def prf(pred: list[str], gold: list[str]) -> tuple[float, float, float]:
    ps, gs = set(pred), set(gold)
    tp = len(ps & gs)
    p = tp / len(ps) if ps else 0.0
    r = tp / len(gs) if gs else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def rank_metrics(pred: list[str], gold: list[str]) -> tuple[float, float, float]:
    gs = set(gold)
    hit = float(any(sid in gs for sid in pred))
    reciprocal_rank = 0.0
    dcg = 0.0
    for rank, sid in enumerate(pred, 1):
        if sid in gs:
            if reciprocal_rank == 0:
                reciprocal_rank = 1 / rank
            dcg += 1 / math.log2(rank + 1)
    ideal_hits = min(len(gs), len(pred))
    idcg = sum(1 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    ndcg = dcg / idcg if idcg else 0.0
    return hit, reciprocal_rank, ndcg


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_]+", text.lower())


def bm25_scores(query: str, sentences: list[dict], k1: float = 1.5, b: float = 0.75):
    docs = [tokenize(row["text"]) for row in sentences]
    q = tokenize(query)
    n = len(docs)
    avgdl = mean(len(doc) for doc in docs) if docs else 0.0
    df = Counter()
    for doc in docs:
        df.update(set(doc))
    scores = []
    for index, doc in enumerate(docs):
        tf = Counter(doc)
        score = 0.0
        for term in q:
            freq = tf[term]
            if not freq:
                continue
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            denom = freq + k1 * (1 - b + b * len(doc) / avgdl)
            score += idf * freq * (k1 + 1) / denom
        scores.append((score, index))
    return [
        sentences[index]["sid"]
        for _, index in sorted(scores, key=lambda item: (-item[0], item[1]))[:3]
    ]


def percentile(values: list[float], p: float) -> float:
    values = sorted(values)
    position = (len(values) - 1) * p
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return values[lo]
    return values[lo] * (hi - position) + values[hi] * (position - lo)


def main() -> None:
    gold_rows = read_jsonl(HERE / "adjudicated_labels.jsonl")
    gold = {row["qid"]: row for row in gold_rows}
    packet = read_jsonl(HERE / "blind_packet.jsonl")
    q_packet = {}
    for doc in packet:
        for q in doc["questions"]:
            q_packet[q["qid"]] = {
                "doc_id": doc["doc_id"],
                "question": q["question"],
                "role": q["role"],
                "sentences": doc["sentences"],
            }

    predictions: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for row in read_jsonl(MAIN_DETAILS):
        if row["qid"] in gold and row["condition"] in CONDITIONS:
            predictions[row["condition"]][row["qid"]] = row["predicted_sentence_ids"]
    for expected_condition, path in EXTRA_DETAILS.items():
        for row in read_jsonl(path):
            if row["qid"] in gold:
                predictions[expected_condition][row["qid"]] = row["predicted_sentence_ids"]
    for qid, meta in q_packet.items():
        predictions["bm25_query"][qid] = bm25_scores(
            meta["question"], meta["sentences"]
        )

    missing = {
        condition: sorted(set(gold) - set(predictions[condition]))
        for condition in CONDITIONS
        if set(gold) - set(predictions[condition])
    }
    if missing:
        raise RuntimeError(f"Missing frozen predictions: {missing}")

    details = []
    for condition in CONDITIONS:
        for qid, gold_row in gold.items():
            pred = predictions[condition][qid]
            p, r, f = prf(pred, gold_row["evidence_sentence_ids"])
            hit, mrr, ndcg = rank_metrics(pred, gold_row["evidence_sentence_ids"])
            details.append(
                {
                    "condition": condition,
                    "qid": qid,
                    "doc_id": gold_row["doc_id"],
                    "role": gold_row["role"],
                    "predicted_sentence_ids": pred,
                    "gold_sentence_ids": gold_row["evidence_sentence_ids"],
                    "evidence_precision": p,
                    "evidence_recall": r,
                    "evidence_f1": f,
                    "hit_at_3": hit,
                    "mrr_at_3": mrr,
                    "ndcg_at_3": ndcg,
                    "label_status": "simulated_expert_adjudicated",
                }
            )
    by_condition = defaultdict(list)
    for row in details:
        by_condition[row["condition"]].append(row)
    metrics = {}
    for condition in CONDITIONS:
        rows = by_condition[condition]
        metrics[condition] = {
            key: mean(row[key] for row in rows)
            for key in [
                "evidence_precision",
                "evidence_recall",
                "evidence_f1",
                "hit_at_3",
                "mrr_at_3",
                "ndcg_at_3",
            ]
        }
        metrics[condition]["questions"] = len(rows)

    docs = sorted({row["doc_id"] for row in gold_rows})
    by_cond_doc = defaultdict(lambda: defaultdict(list))
    for row in details:
        by_cond_doc[row["condition"]][row["doc_id"]].append(row["evidence_f1"])
    rng = random.Random(BOOTSTRAP_SEED)
    comparisons = {}
    for other in [condition for condition in CONDITIONS if condition != "c2ges_full"]:
        doc_deltas = {
            doc: mean(by_cond_doc["c2ges_full"][doc])
            - mean(by_cond_doc[other][doc])
            for doc in docs
        }
        samples = []
        for _ in range(BOOTSTRAP_SAMPLES):
            sampled = [rng.choice(docs) for _ in docs]
            samples.append(mean(doc_deltas[doc] for doc in sampled))
        observed = mean(doc_deltas.values())
        comparisons[f"c2ges_full_vs_{other}"] = {
            "mean_f1_difference": observed,
            "ci95": [percentile(samples, 0.025), percentile(samples, 0.975)],
            "bootstrap_two_sided_p": 2
            * min(
                sum(value <= 0 for value in samples) / len(samples),
                sum(value >= 0 for value in samples) / len(samples),
            ),
            "documents": len(docs),
        }

    role_metrics = defaultdict(dict)
    for condition in CONDITIONS:
        for role in sorted({row["role"] for row in gold_rows}):
            rows = [
                row
                for row in by_condition[condition]
                if row["role"] == role
            ]
            role_metrics[condition][role] = {
                "evidence_f1": mean(row["evidence_f1"] for row in rows),
                "hit_at_3": mean(row["hit_at_3"] for row in rows),
                "questions": len(rows),
            }

    original_dataset = PROJECT / "workspace" / "verification_pilot" / "agent_audit_40doc"
    original_gold = {}
    for doc_id in sorted({row["doc_id"] for row in gold_rows}):
        doc = json.loads((original_dataset / f"{doc_id}.json").read_text(encoding="utf-8"))
        original_gold.update(
            {q["qid"]: q["evidence_sentence_ids"] for q in doc["causal_questions"]}
        )
    label_f1s = [
        prf(original_gold[qid], row["evidence_sentence_ids"])[2]
        for qid, row in gold.items()
    ]
    exact = [
        set(original_gold[qid]) == set(row["evidence_sentence_ids"])
        for qid, row in gold.items()
    ]
    label_comparison = {
        "exact_set_agreement": mean(exact),
        "mean_set_f1": mean(label_f1s),
        "changed_questions": sum(not value for value in exact),
    }

    output = {
        "annotation_type": "AI_simulated_expert_adjudicated_not_human_gold",
        "documents": len(docs),
        "questions": len(gold),
        "bootstrap_samples": BOOTSTRAP_SAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "aggregate_metrics": metrics,
        "paired_document_bootstrap": comparisons,
        "role_metrics": role_metrics,
        "original_vs_adjudicated_labels": label_comparison,
    }
    (HERE / "rescored_details.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in details) + "\n",
        encoding="utf-8",
    )
    (HERE / "rescore_results.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Frozen-Prediction Rescoring on the Simulated-Expert Subset",
        "",
        "**Disclosure:** labels are adjudicated from three AI simulated-expert",
        "annotations; they are not human-gold labels.",
        "",
        f"- Documents: {len(docs)}",
        f"- Questions: {len(gold)}",
        f"- Original/adjudicated exact-set agreement: {label_comparison['exact_set_agreement']:.3f}",
        f"- Original/adjudicated mean set F1: {label_comparison['mean_set_f1']:.3f}",
        "",
        "| Method | F1 | Precision | Recall | Hit@3 | MRR@3 | nDCG@3 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for condition in CONDITIONS:
        m = metrics[condition]
        lines.append(
            f"| {condition} | {m['evidence_f1']:.4f} | "
            f"{m['evidence_precision']:.4f} | {m['evidence_recall']:.4f} | "
            f"{m['hit_at_3']:.4f} | {m['mrr_at_3']:.4f} | {m['ndcg_at_3']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Paired document-cluster bootstrap (F1)",
            "",
            "| Comparison | Mean difference | 95% CI | p |",
            "|---|---:|---:|---:|",
        ]
    )
    for name, comp in comparisons.items():
        lines.append(
            f"| {name} | {comp['mean_f1_difference']:.4f} | "
            f"[{comp['ci95'][0]:.4f}, {comp['ci95'][1]:.4f}] | "
            f"{comp['bootstrap_two_sided_p']:.4f} |"
        )
    (HERE / "rescore_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
