#!/usr/bin/env python3
"""Run the C²GES causal-role graph reranker on the agent-audited pilot data."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from rouge_score import rouge_scorer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


K = 3

ROLE_ORDER = [
    "trigger_event",
    "root_cause",
    "propagation_or_response",
    "impact",
    "mitigation",
]

ROLE_TERMS = {
    "trigger_event": [
        "fault",
        "line fault",
        "transmission fault",
        "single-line-to-ground",
        "phase-to-phase",
        "outage",
        "occurred",
        "initiated",
        "triggered",
        "cleared",
        "relay",
        "fire",
        "failed splice",
        "insulator",
        "planned outage",
    ],
    "root_cause": [
        "cause",
        "caused",
        "root cause",
        "attributed",
        "due to",
        "because",
        "failure",
        "failed",
        "settings",
        "protection",
        "control",
        "inverter",
        "overcurrent",
        "overvoltage",
        "undervoltage",
        "momentary cessation",
        "frozen",
        "fuel",
        "winterization",
        "curtailment",
        "misoperated",
    ],
    "propagation_or_response": [
        "respond",
        "response",
        "tripped",
        "trip",
        "reduced",
        "reduction",
        "entered",
        "momentary cessation",
        "relay",
        "relayed",
        "voltage",
        "frequency",
        "island",
        "load shed",
        "ufls",
        "reserve",
        "output",
        "controller",
        "controls",
        "propagate",
        "flow",
    ],
    "impact": [
        "mw",
        "gw",
        "customers",
        "load shed",
        "firm load",
        "frequency dropped",
        "loss",
        "lost",
        "outage",
        "unavailable",
        "affected",
        "reduction",
        "derate",
        "deaths",
        "economic",
        "boil water",
        "category",
        "hours",
        "percent",
    ],
    "mitigation": [
        "recommend",
        "recommendation",
        "recommended",
        "mitigation",
        "mitigate",
        "corrective",
        "action",
        "settings",
        "standard",
        "requirement",
        "should",
        "must",
        "prevent",
        "future",
        "study",
        "guideline",
        "winterization",
        "reliability standard",
        "performance-based",
    ],
}

NEIGHBOR_ROLES = {
    "trigger_event": ["root_cause", "propagation_or_response"],
    "root_cause": ["trigger_event", "propagation_or_response"],
    "propagation_or_response": ["root_cause", "trigger_event", "impact"],
    "impact": ["propagation_or_response", "mitigation"],
    "mitigation": ["impact", "propagation_or_response"],
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_docs(data_dir: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(data_dir.glob("nerc_*.json"))]


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


def minmax(values: np.ndarray) -> np.ndarray:
    if len(values) == 0:
        return values
    lo = float(np.min(values))
    hi = float(np.max(values))
    if math.isclose(lo, hi):
        return np.zeros_like(values, dtype=float)
    return (values - lo) / (hi - lo)


def phrase_hits(text: str, terms: list[str]) -> float:
    lower = text.lower()
    score = 0.0
    for term in terms:
        if term in lower:
            score += 1.0 + 0.15 * max(0, len(term.split()) - 1)
    if re.search(r"\b\d+(?:,\d{3})*(?:\.\d+)?\s*(mw|gw|kv|hz|%)\b", lower):
        score += 0.8
    if re.search(r"\b(slg|ras|ibr|bess|pv|ercot|caiso|miso|nerc|wecc)\b", lower):
        score += 0.25
    return score


def role_score_matrix(texts: list[str]) -> dict[str, np.ndarray]:
    raw = {
        role: np.asarray([phrase_hits(text, terms) for text in texts], dtype=float)
        for role, terms in ROLE_TERMS.items()
    }
    return {role: minmax(scores) for role, scores in raw.items()}


def query_scores(question: str, texts: list[str]) -> np.ndarray:
    vectorizer = TfidfVectorizer(stop_words="english", max_features=8000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts + [question])
    return minmax(cosine_similarity(X[:-1], X[-1]).ravel())


def graph_matrix(texts: list[str]) -> np.ndarray:
    n = len(texts)
    vectorizer = TfidfVectorizer(stop_words="english", max_features=8000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)
    sim = cosine_similarity(X)
    graph = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            distance = abs(i - j)
            seq_weight = math.exp(-distance / 4.0) if distance <= 8 else 0.0
            sem_weight = float(sim[i, j]) if sim[i, j] >= 0.08 else 0.0
            graph[i, j] = 0.45 * seq_weight + 0.55 * sem_weight
    return graph


def chain_scores(role: str, graph: np.ndarray, role_scores: dict[str, np.ndarray]) -> np.ndarray:
    n = graph.shape[0]
    if n == 0:
        return np.asarray([], dtype=float)
    neighbors = NEIGHBOR_ROLES[role]
    support = np.zeros(n, dtype=float)
    role_index = ROLE_ORDER.index(role)
    for i in range(n):
        total = 0.0
        weight_total = 0.0
        for neighbor_role in neighbors:
            neighbor_index = ROLE_ORDER.index(neighbor_role)
            direction = -1 if neighbor_index < role_index else 1
            for j in range(n):
                if i == j:
                    continue
                # Prefer causal evidence appearing in a plausible report order, but do not
                # eliminate cross-reference support because NERC reports often summarize first.
                ordered = (j < i and direction < 0) or (j > i and direction > 0)
                order_weight = 1.0 if ordered else 0.45
                w = graph[i, j] * order_weight
                if w <= 0:
                    continue
                total += w * float(role_scores[neighbor_role][j])
                weight_total += w
        support[i] = total / weight_total if weight_total else 0.0
    return minmax(support)


def graph_centrality(graph: np.ndarray) -> np.ndarray:
    if graph.size == 0:
        return np.asarray([], dtype=float)
    return minmax(graph.sum(axis=1))


def rank_sentences(
    question: str,
    role: str,
    sids: list[str],
    texts: list[str],
    variant: str,
    k: int,
) -> tuple[list[str], dict[str, float]]:
    q = query_scores(question, texts)
    r_scores = role_score_matrix(texts)
    role_scores = r_scores[role]
    graph = graph_matrix(texts)
    chain = chain_scores(role, graph, r_scores)
    centrality = graph_centrality(graph)

    if variant == "c2ges_query_only":
        final = q
        weights = {"query": 1.0, "role": 0.0, "chain": 0.0, "centrality": 0.0}
    elif variant == "c2ges_no_role":
        final = 0.88 * q + 0.12 * centrality
        weights = {"query": 0.88, "role": 0.0, "chain": 0.0, "centrality": 0.12}
    elif variant == "c2ges_no_graph":
        final = 0.72 * q + 0.28 * role_scores
        weights = {"query": 0.72, "role": 0.28, "chain": 0.0, "centrality": 0.0}
    elif variant == "c2ges_full":
        final = 0.64 * q + 0.24 * role_scores + 0.12 * chain
        weights = {"query": 0.64, "role": 0.24, "chain": 0.12, "centrality": 0.0}
    else:
        raise ValueError(f"unknown variant: {variant}")

    ranked = np.asarray(final).argsort()[::-1].tolist()
    return [sids[i] for i in ranked[:k]], weights


def parse_args() -> argparse.Namespace:
    workspace = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=workspace / "agent_audit_15doc")
    parser.add_argument("--out-dir", type=Path, default=workspace / "results_c2ges_15doc")
    parser.add_argument("--k", type=int, default=K)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = args.data_dir
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    docs = load_docs(data_dir)
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    variants = ["c2ges_query_only", "c2ges_no_role", "c2ges_no_graph", "c2ges_full"]

    rows = []
    role_hits: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    role_totals: dict[str, set[str]] = defaultdict(set)
    variant_weights: dict[str, dict[str, float]] = {}

    for doc in docs:
        sids = [s["sid"] for s in doc["sentences"]]
        texts = [clean(s["text"]) for s in doc["sentences"]]
        by_sid = dict(zip(sids, texts, strict=True))
        for q in doc["causal_questions"]:
            gold = q["evidence_sentence_ids"]
            role = q["role"]
            role_totals[role].add(q["qid"])
            gold_text = " ".join(by_sid[sid] for sid in gold if sid in by_sid)
            for variant in variants:
                try:
                    pred, weights = rank_sentences(q["question"], role, sids, texts, variant, args.k)
                    variant_weights[variant] = weights
                    status = "ok"
                    error = ""
                except Exception as exc:  # noqa: BLE001 - feasibility harness.
                    pred = []
                    status = "failed"
                    error = f"{type(exc).__name__}: {exc}"
                precision, recall, f1 = prf(pred, gold)
                if f1 > 0:
                    role_hits[variant][role].add(q["qid"])
                pred_text = " ".join(by_sid[sid] for sid in pred if sid in by_sid)
                rouge_l = scorer.score(gold_text, pred_text)["rougeL"].fmeasure if pred_text and gold_text else 0.0
                rows.append(
                    {
                        "doc_id": doc["doc_id"],
                        "qid": q["qid"],
                        "role": role,
                        "method": variant,
                        "status": status,
                        "precision": precision,
                        "recall": recall,
                        "f1": f1,
                        "rougeL": rouge_l,
                        "gold": gold,
                        "pred": pred,
                        "error": error,
                    }
                )

    aggregate = []
    for variant in variants:
        subset = [r for r in rows if r["method"] == variant]
        ok = [r for r in subset if r["status"] == "ok"]
        aggregate.append(
            {
                "method": variant,
                "status": "ok" if len(ok) == len(subset) else "partial_or_failed",
                "questions": len(subset),
                "ok_questions": len(ok),
                "mean_precision": float(np.mean([r["precision"] for r in ok])) if ok else 0.0,
                "mean_recall": float(np.mean([r["recall"] for r in ok])) if ok else 0.0,
                "mean_f1": float(np.mean([r["f1"] for r in ok])) if ok else 0.0,
                "mean_rougeL": float(np.mean([r["rougeL"] for r in ok])) if ok else 0.0,
                "role_coverage": {
                    role: len(role_hits[variant][role]) / len(qids) if qids else 0.0
                    for role, qids in role_totals.items()
                },
                "weights": variant_weights.get(variant, {}),
                "errors": sorted({r["error"] for r in subset if r["error"]}),
            }
        )

    result = {
        "dataset": load_manifest(data_dir, docs),
        "k": args.k,
        "method_family": "C²GES causal-role graph-enhanced evidence sentence ranking",
        "aggregate": aggregate,
        "comparison_targets": {
            "tfidf_query_f1_agent15": 0.18463492063492065,
            "sbert_query_f1_agent15": 0.12546031746031747,
        },
    }
    (out_dir / "c2ges_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out_dir / "c2ges_details.jsonl").write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
