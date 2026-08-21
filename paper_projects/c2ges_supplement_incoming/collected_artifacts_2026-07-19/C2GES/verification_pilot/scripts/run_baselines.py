#!/usr/bin/env python3
"""Run lightweight evidence-selection baselines for the 5-doc pilot."""

from __future__ import annotations

import json
import math
import re
import argparse
from collections import defaultdict
from pathlib import Path
from typing import Callable

import networkx as nx
import numpy as np
from lexrank import LexRank
from lexrank.mappings.stopwords import STOPWORDS
from rouge_score import rouge_scorer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


K = 3
TRIGGER_TERMS = [
    "cause",
    "caused",
    "contributing",
    "fault",
    "failure",
    "trip",
    "tripped",
    "outage",
    "disturbance",
    "relay",
    "protection",
    "voltage",
    "frequency",
    "inverter",
    "generator",
    "loss",
    "load",
    "mitigation",
    "recommendation",
    "corrective",
    "resulted",
    "led to",
    "because",
]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_docs(data_dir: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(data_dir.glob("nerc_*.json"))]


def topk(indices: list[int], sids: list[str]) -> list[str]:
    return [sids[i] for i in indices[:K]]


def lead_k(question: str, sids: list[str], texts: list[str], state: dict) -> list[str]:
    return sids[:K]


def tfidf_query(question: str, sids: list[str], texts: list[str], state: dict) -> list[str]:
    vectorizer = TfidfVectorizer(stop_words="english", max_features=8000)
    X = vectorizer.fit_transform(texts + [question])
    scores = cosine_similarity(X[:-1], X[-1]).ravel()
    return topk(scores.argsort()[::-1].tolist(), sids)


def tfidf_centroid(question: str, sids: list[str], texts: list[str], state: dict) -> list[str]:
    vectorizer = TfidfVectorizer(stop_words="english", max_features=8000)
    X = vectorizer.fit_transform(texts)
    centroid = np.asarray(X.mean(axis=0))
    scores = cosine_similarity(X, centroid).ravel()
    return topk(scores.argsort()[::-1].tolist(), sids)


def textrank_networkx(question: str, sids: list[str], texts: list[str], state: dict) -> list[str]:
    vectorizer = TfidfVectorizer(stop_words="english", max_features=8000)
    X = vectorizer.fit_transform(texts)
    sim = cosine_similarity(X)
    np.fill_diagonal(sim, 0.0)
    graph = nx.from_numpy_array(sim)
    ranks = nx.pagerank(graph, max_iter=100)
    return topk(sorted(ranks, key=ranks.get, reverse=True), sids)


def lexrank_baseline(question: str, sids: list[str], texts: list[str], state: dict) -> list[str]:
    lxr = LexRank([texts], stopwords=STOPWORDS["en"])
    scores = lxr.rank_sentences(texts, threshold=None, fast_power_method=True)
    return topk(np.asarray(scores).argsort()[::-1].tolist(), sids)


def causal_trigger_rank(question: str, sids: list[str], texts: list[str], state: dict) -> list[str]:
    q_terms = [t for t in TRIGGER_TERMS if t in question.lower()]
    scores = []
    for text in texts:
        lower = text.lower()
        trigger_score = sum(term in lower for term in TRIGGER_TERMS)
        query_trigger_score = sum(term in lower for term in q_terms)
        scores.append(trigger_score + 0.5 * query_trigger_score)
    return topk(np.asarray(scores).argsort()[::-1].tolist(), sids)


def sbert_query(question: str, sids: list[str], texts: list[str], state: dict) -> list[str]:
    model = state.get("sbert_model")
    if model is None:
        raise RuntimeError(state.get("sbert_error", "SBERT model unavailable"))
    emb = model.encode(texts + [question], normalize_embeddings=True, show_progress_bar=False)
    scores = np.dot(emb[:-1], emb[-1])
    return topk(np.asarray(scores).argsort()[::-1].tolist(), sids)


BASELINES: dict[str, Callable[[str, list[str], list[str], dict], list[str]]] = {
    "lead_k": lead_k,
    "tfidf_query": tfidf_query,
    "tfidf_centroid": tfidf_centroid,
    "textrank_networkx": textrank_networkx,
    "lexrank": lexrank_baseline,
    "causal_trigger_rank": causal_trigger_rank,
    "sbert_query": sbert_query,
}


def prf(pred: list[str], gold: list[str]) -> tuple[float, float, float]:
    pset = set(pred)
    gset = set(gold)
    if not pset and not gset:
        return 1.0, 1.0, 1.0
    tp = len(pset & gset)
    precision = tp / len(pset) if pset else 0.0
    recall = tp / len(gset) if gset else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def try_load_sbert() -> dict:
    state: dict = {}
    try:
        from sentence_transformers import SentenceTransformer

        # Small, common model. If no cache/network is available, this failure is recorded.
        state["sbert_model"] = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        state["sbert_status"] = "loaded"
    except Exception as exc:  # noqa: BLE001 - this is a feasibility harness.
        state["sbert_model"] = None
        state["sbert_status"] = "unavailable"
        state["sbert_error"] = f"{type(exc).__name__}: {exc}"
    return state


def parse_args() -> argparse.Namespace:
    workspace = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=workspace / "data")
    parser.add_argument("--out-dir", type=Path, default=workspace / "results")
    return parser.parse_args()


def load_manifest(data_dir: Path, docs: list[dict]) -> dict:
    manifest_path = data_dir / "manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {
        "name": data_dir.name,
        "schema_anchor": "QMSum-style query/answer/evidence spans",
        "status": "agent_verified_candidate",
        "documents": [doc["doc_id"] for doc in docs],
        "question_count": sum(len(doc["causal_questions"]) for doc in docs),
        "questions_per_document": len(docs[0]["causal_questions"]) if docs else 0,
    }


def main() -> None:
    args = parse_args()
    workspace = Path(__file__).resolve().parents[1]
    data_dir = args.data_dir
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    docs = load_docs(data_dir)
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    state = try_load_sbert()

    rows = []
    details = []
    role_hits: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    role_totals: dict[str, set[str]] = defaultdict(set)

    for doc in docs:
        sids = [s["sid"] for s in doc["sentences"]]
        texts = [clean(s["text"]) for s in doc["sentences"]]
        by_sid = dict(zip(sids, texts, strict=True))
        for q in doc["causal_questions"]:
            gold = q["evidence_sentence_ids"]
            role = q["role"]
            role_totals[role].add(q["qid"])
            gold_text = " ".join(by_sid[sid] for sid in gold if sid in by_sid)
            for name, fn in BASELINES.items():
                try:
                    pred = fn(q["question"], sids, texts, state)
                    status = "ok"
                    error = ""
                except Exception as exc:  # noqa: BLE001 - per-baseline feasibility.
                    pred = []
                    status = "failed"
                    error = f"{type(exc).__name__}: {exc}"
                precision, recall, f1 = prf(pred, gold)
                if f1 > 0:
                    role_hits[name][role].add(q["qid"])
                pred_text = " ".join(by_sid[sid] for sid in pred if sid in by_sid)
                rouge_l = scorer.score(gold_text, pred_text)["rougeL"].fmeasure if pred_text and gold_text else 0.0
                row = {
                    "doc_id": doc["doc_id"],
                    "qid": q["qid"],
                    "role": role,
                    "baseline": name,
                    "status": status,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "rougeL": rouge_l,
                    "gold": gold,
                    "pred": pred,
                    "error": error,
                }
                rows.append(row)
                details.append(row)

    aggregate = []
    for name in BASELINES:
        subset = [r for r in rows if r["baseline"] == name]
        ok = [r for r in subset if r["status"] == "ok"]
        role_coverage = {
            role: len(role_hits[name][role]) / len(qids) if qids else 0.0
            for role, qids in role_totals.items()
        }
        aggregate.append(
            {
                "baseline": name,
                "status": "ok" if len(ok) == len(subset) else "partial_or_failed",
                "questions": len(subset),
                "ok_questions": len(ok),
                "mean_precision": float(np.mean([r["precision"] for r in ok])) if ok else 0.0,
                "mean_recall": float(np.mean([r["recall"] for r in ok])) if ok else 0.0,
                "mean_f1": float(np.mean([r["f1"] for r in ok])) if ok else 0.0,
                "mean_rougeL": float(np.mean([r["rougeL"] for r in ok])) if ok else 0.0,
                "role_coverage": role_coverage,
                "errors": sorted({r["error"] for r in subset if r["error"]}),
            }
        )

    result = {
        "dataset": load_manifest(data_dir, docs),
        "k": K,
        "dependency_status": {
            "sbert": state.get("sbert_status"),
            "sbert_error": state.get("sbert_error", ""),
            "bert_score": "not_run_in_harness; package import was validated separately but model scoring is deferred",
        },
        "aggregate": aggregate,
    }
    (out_dir / "baseline_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out_dir / "baseline_details.jsonl").write_text(
        "\n".join(json.dumps(row) for row in details) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
