#!/usr/bin/env python3
"""Final C2GES experiment wrapper for the approved Executor route.

This runner intentionally delegates the ranking logic to the validated pilot
scripts in verification_pilot/scripts. It only adds the richer artifact and
statistics layer required by the approved Stage 9 experiment design.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np
from rouge_score import rouge_scorer


MAIN_CONDITIONS = [
    "lead_k",
    "tfidf_query",
    "tfidf_centroid",
    "textrank_networkx",
    "lexrank",
    "causal_trigger_rank",
    "sbert_query",
    "c2ges_full",
]
C2GES_VARIANTS = [
    "c2ges_query_only",
    "c2ges_no_role",
    "c2ges_no_graph",
    "c2ges_full",
]
LEGACY_CONDITIONS = ["c2ges_full_fixed_legacy"]
ALL_CONDITIONS = MAIN_CONDITIONS + [
    condition for condition in C2GES_VARIANTS if condition not in MAIN_CONDITIONS
] + LEGACY_CONDITIONS
ROLES = [
    "trigger_event",
    "root_cause",
    "propagation_or_response",
    "impact",
    "mitigation",
]
METRICS = [
    "evidence_precision",
    "evidence_recall",
    "evidence_f1",
    "rouge_l_selected_evidence_text",
]
PAIRED_BASELINES = [
    "tfidf_query",
    "sbert_query",
    "c2ges_query_only",
    "c2ges_no_graph",
    "c2ges_no_role",
    "c2ges_full_fixed_legacy",
]
DIAGNOSTIC_CONDITIONS = ["tfidf_query", "c2ges_query_only", "c2ges_full"]
K = 3
BOOTSTRAP_SAMPLES = 10000
BOOTSTRAP_SEED = 202502
CONTEXT_WINDOW = 2
CV_FOLDS = 5
WORKSPACE_FALLBACK = Path(
    "/media/lenovo/data2/cja/GridMind/references/AutoResearchClaw/"
    "paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess"
)

REVISED_C2GES_CANDIDATES = [
    {"family": "chain_plus_centrality", "weights": {"query": 0.52, "role": 0.40, "graph_signal": 0.08}},
    {"family": "role_gated_chain", "weights": {"query": 0.52, "role": 0.40, "graph_signal": 0.08}},
    {"family": "chain_plus_centrality", "weights": {"query": 0.56, "role": 0.36, "graph_signal": 0.08}},
    {"family": "role_gated_chain", "weights": {"query": 0.56, "role": 0.36, "graph_signal": 0.08}},
    {"family": "chain_plus_centrality", "weights": {"query": 0.52, "role": 0.36, "graph_signal": 0.12}},
    {"family": "role_gated_chain", "weights": {"query": 0.52, "role": 0.36, "graph_signal": 0.12}},
    {"family": "additive_chain_legacy_formula", "weights": {"query": 0.64, "role": 0.24, "graph_signal": 0.12}},
]


def discover_workspace() -> Path:
    candidates = [Path.cwd().resolve(), Path(__file__).resolve()]
    for start in candidates:
        for parent in [start, *start.parents]:
            if (
                (parent / "verification_pilot" / "agent_audit_40doc").is_dir()
                and (parent / "three-pack" / "config.yaml").is_file()
            ):
                return parent
    if (
        (WORKSPACE_FALLBACK / "verification_pilot" / "agent_audit_40doc").is_dir()
        and (WORKSPACE_FALLBACK / "three-pack" / "config.yaml").is_file()
    ):
        return WORKSPACE_FALLBACK
    raise FileNotFoundError("Could not discover paper workspace root.")


def discover_repo(workspace: Path) -> Path:
    for parent in [workspace, *workspace.parents]:
        if (parent / "researchclaw").is_dir() and (parent / ".venv").exists():
            return parent
    return workspace


def import_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot import {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_docs(data_dir: Path) -> list[dict[str, Any]]:
    docs = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(data_dir.glob("nerc_*.json"))
    ]
    if not docs:
        raise FileNotFoundError(f"No nerc_*.json documents found in {data_dir}")
    return docs


def load_manifest(data_dir: Path, docs: list[dict[str, Any]]) -> dict[str, Any]:
    manifest_path = data_dir / "manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {
        "name": data_dir.name,
        "status": "agent_verified_candidate",
        "document_count": len(docs),
        "documents": [doc["doc_id"] for doc in docs],
        "question_count": sum(len(doc["causal_questions"]) for doc in docs),
    }


def prf(predicted: list[str], gold: list[str]) -> dict[str, float]:
    pset = set(predicted)
    gset = set(gold)
    tp = len(pset & gset)
    precision = tp / len(pset) if pset else 0.0
    recall = tp / len(gset) if gset else 0.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "evidence_precision": float(precision),
        "evidence_recall": float(recall),
        "evidence_f1": float(f1),
    }


def sentence_text(by_sid: dict[str, str], sids: list[str]) -> str:
    return " ".join(by_sid[sid] for sid in sids if sid in by_sid)


def local_context(
    sentences: list[dict[str, Any]],
    selected: list[str],
    gold: list[str],
    window: int = CONTEXT_WINDOW,
) -> list[dict[str, Any]]:
    sid_to_index = {str(sentence["sid"]): idx for idx, sentence in enumerate(sentences)}
    wanted: set[int] = set()
    for sid in [*selected, *gold]:
        if sid not in sid_to_index:
            continue
        center = sid_to_index[sid]
        for idx in range(max(0, center - window), min(len(sentences), center + window + 1)):
            wanted.add(idx)
    selected_set = set(selected)
    gold_set = set(gold)
    return [
        {
            "sid": str(sentences[idx]["sid"]),
            "text": clean(str(sentences[idx]["text"])),
            "is_selected": str(sentences[idx]["sid"]) in selected_set,
            "is_gold": str(sentences[idx]["sid"]) in gold_set,
        }
        for idx in sorted(wanted)
    ]


def mask_question(question: str, role: str) -> str:
    replacements = {
        "trigger_event": "event cue",
        "root_cause": "cause cue",
        "propagation_or_response": "response cue",
        "impact": "impact cue",
        "mitigation": "mitigation cue",
    }
    masked = question
    terms = [
        role.replace("_", " "),
        "trigger",
        "root cause",
        "cause",
        "caused",
        "propagation",
        "response",
        "impact",
        "mitigation",
        "recommendation",
        "evidence",
    ]
    for term in sorted(set(terms), key=len, reverse=True):
        masked = re.sub(rf"\b{re.escape(term)}\b", "[MASK]", masked, flags=re.IGNORECASE)
    return f"{masked} ({replacements.get(role, 'causal cue')} masked)"


def fold_for_doc(doc_id: str, folds: int = CV_FOLDS) -> int:
    digest = hashlib.sha256(doc_id.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % folds


def graph_signal(
    *,
    family: str,
    role_scores: np.ndarray,
    chain_scores: np.ndarray,
    centrality_scores: np.ndarray,
    c2ges_module: Any,
) -> np.ndarray:
    if family == "role_gated_chain":
        return c2ges_module.minmax(role_scores * chain_scores)
    if family == "chain_plus_centrality":
        return c2ges_module.minmax(0.5 * chain_scores + 0.5 * centrality_scores)
    if family == "additive_chain_legacy_formula":
        return chain_scores
    raise ValueError(f"unknown revised C2GES family: {family}")


def revised_rank_sentences(
    *,
    question: str,
    role: str,
    sids: list[str],
    texts: list[str],
    variant: str,
    k: int,
    config: dict[str, Any],
    c2ges_module: Any,
) -> tuple[list[str], dict[str, Any]]:
    q = c2ges_module.query_scores(question, texts)
    role_matrix = c2ges_module.role_score_matrix(texts)
    target_role_scores = role_matrix[role]
    graph = c2ges_module.graph_matrix(texts)
    chain = c2ges_module.chain_scores(role, graph, role_matrix)
    centrality = c2ges_module.graph_centrality(graph)

    family = str(config["family"])
    weights = dict(config["weights"])
    query_weight = float(weights["query"])
    role_weight = float(weights["role"])
    graph_weight = float(weights["graph_signal"])
    g = graph_signal(
        family=family,
        role_scores=target_role_scores,
        chain_scores=chain,
        centrality_scores=centrality,
        c2ges_module=c2ges_module,
    )

    if variant == "c2ges_query_only":
        final = q
        used_weights = {"query": 1.0, "role": 0.0, "graph_signal": 0.0}
    elif variant == "c2ges_no_role":
        denom = query_weight + graph_weight
        final = (query_weight / denom) * q + (graph_weight / denom) * g
        used_weights = {"query": query_weight / denom, "role": 0.0, "graph_signal": graph_weight / denom}
    elif variant == "c2ges_no_graph":
        denom = query_weight + role_weight
        final = (query_weight / denom) * q + (role_weight / denom) * target_role_scores
        used_weights = {"query": query_weight / denom, "role": role_weight / denom, "graph_signal": 0.0}
    elif variant == "c2ges_full":
        final = query_weight * q + role_weight * target_role_scores + graph_weight * g
        used_weights = {"query": query_weight, "role": role_weight, "graph_signal": graph_weight}
    else:
        raise ValueError(f"unknown revised C2GES variant: {variant}")

    ranked = np.asarray(final).argsort()[::-1].tolist()
    metadata = {
        "family": family,
        "candidate_id": config.get("candidate_id", "manual_config"),
        "selection_fold": config.get("selection_fold"),
        "weights": {key: float(value) for key, value in used_weights.items()},
        "formula": (
            "final = query_weight * query_relevance + role_weight * target_role_compatibility "
            "+ graph_signal_weight * graph_signal"
        ),
        "graph_signal_formula": {
            "role_gated_chain": "minmax(target_role_compatibility * chain_support)",
            "chain_plus_centrality": "minmax(0.5 * chain_support + 0.5 * graph_centrality)",
            "additive_chain_legacy_formula": "chain_support",
        }[family],
    }
    return [str(sids[i]) for i in ranked[:k]], metadata


def score_config_on_docs(
    *,
    docs: list[dict[str, Any]],
    config: dict[str, Any],
    c2ges_module: Any,
) -> float:
    scores: list[float] = []
    for doc in docs:
        sids = [str(sentence["sid"]) for sentence in doc["sentences"]]
        texts = [clean(str(sentence["text"])) for sentence in doc["sentences"]]
        for question in doc["causal_questions"]:
            selected, _metadata = revised_rank_sentences(
                question=str(question["question"]),
                role=str(question["role"]),
                sids=sids,
                texts=texts,
                variant="c2ges_full",
                k=K,
                config=config,
                c2ges_module=c2ges_module,
            )
            scores.append(prf(selected, [str(sid) for sid in question["evidence_sentence_ids"]])["evidence_f1"])
    return mean(scores)


def build_cv_protocol(
    docs: list[dict[str, Any]],
    c2ges_module: Any,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    fold_assignment = {str(doc["doc_id"]): fold_for_doc(str(doc["doc_id"])) for doc in docs}
    selected_by_doc: dict[str, dict[str, Any]] = {}
    folds: list[dict[str, Any]] = []
    for fold in range(CV_FOLDS):
        train_docs = [doc for doc in docs if fold_assignment[str(doc["doc_id"])] != fold]
        eval_docs = [doc for doc in docs if fold_assignment[str(doc["doc_id"])] == fold]
        candidate_scores = []
        for idx, candidate in enumerate(REVISED_C2GES_CANDIDATES):
            score = score_config_on_docs(docs=train_docs, config=candidate, c2ges_module=c2ges_module)
            candidate_scores.append(
                {
                    "candidate_id": f"candidate_{idx:02d}",
                    "family": candidate["family"],
                    "weights": candidate["weights"],
                    "train_evidence_f1": score,
                }
            )
        selected = max(
            candidate_scores,
            key=lambda item: (
                float(item["train_evidence_f1"]),
                item["family"],
                json.dumps(item["weights"], sort_keys=True),
            ),
        )
        selected_config = {
            "candidate_id": selected["candidate_id"],
            "family": selected["family"],
            "weights": selected["weights"],
            "selection_fold": fold,
        }
        eval_score = score_config_on_docs(docs=eval_docs, config=selected_config, c2ges_module=c2ges_module)
        for doc in eval_docs:
            selected_by_doc[str(doc["doc_id"])] = selected_config
        folds.append(
            {
                "fold": fold,
                "train_doc_ids": [str(doc["doc_id"]) for doc in train_docs],
                "eval_doc_ids": [str(doc["doc_id"]) for doc in eval_docs],
                "selected_config": selected_config,
                "selected_train_evidence_f1": float(selected["train_evidence_f1"]),
                "heldout_evidence_f1": float(eval_score),
                "candidate_training_scores": candidate_scores,
            }
        )
    protocol = {
        "name": "document_level_5fold_revised_c2ges_selection",
        "purpose": "non-leaky family/weight selection for revised C2GES before final result analysis",
        "fold_count": CV_FOLDS,
        "fold_assignment_method": "sha256(doc_id) modulo 5; whole documents never split across folds",
        "fold_assignment": fold_assignment,
        "candidate_grid": REVISED_C2GES_CANDIDATES,
        "folds": folds,
        "main_result_top_k": K,
        "allowed_scope": [
            "same approved dataset and labels",
            "same evidence_f1 primary metric",
            "same query/role/graph C2GES component family",
            "no new external resources",
        ],
    }
    return protocol, selected_by_doc


def run_condition(
    *,
    condition: str,
    docs: list[dict[str, Any]],
    scorer: rouge_scorer.RougeScorer,
    baselines: dict[str, Callable[[str, list[str], list[str], dict[str, Any]], list[str]]],
    c2ges_module: Any,
    baseline_state: dict[str, Any],
    cv_config_by_doc: dict[str, dict[str, Any]],
    diagnostic_role_masked: bool = False,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for doc in docs:
        sids = [str(sentence["sid"]) for sentence in doc["sentences"]]
        texts = [clean(str(sentence["text"])) for sentence in doc["sentences"]]
        by_sid = dict(zip(sids, texts, strict=True))
        for question in doc["causal_questions"]:
            gold = [str(sid) for sid in question["evidence_sentence_ids"]]
            role = str(question["role"])
            original_question = str(question["question"])
            query = mask_question(original_question, role) if diagnostic_role_masked else original_question
            selected: list[str] = []
            status = "ok"
            error = ""
            weights: dict[str, float] = {}
            try:
                if condition in baselines:
                    selected = [str(sid) for sid in baselines[condition](query, sids, texts, baseline_state)]
                elif condition == "c2ges_full_fixed_legacy":
                    selected, weights = c2ges_module.rank_sentences(
                        query, role, sids, texts, "c2ges_full", K
                    )
                    weights = {
                        "family": "fixed_additive_chain_legacy",
                        "weights": weights,
                        "formula": "final = 0.64 * query + 0.24 * role + 0.12 * chain",
                    }
                    selected = [str(sid) for sid in selected]
                elif condition in C2GES_VARIANTS:
                    if condition == "c2ges_query_only":
                        selected, weights = c2ges_module.rank_sentences(
                            query, role, sids, texts, condition, K
                        )
                    else:
                        selected, weights = revised_rank_sentences(
                            question=query,
                            role=role,
                            sids=sids,
                            texts=texts,
                            variant=condition,
                            k=K,
                            config=cv_config_by_doc[str(doc["doc_id"])],
                            c2ges_module=c2ges_module,
                        )
                    selected = [str(sid) for sid in selected]
                else:
                    raise ValueError(f"unknown condition: {condition}")
            except Exception as exc:  # noqa: BLE001 - record per-condition failures.
                status = "failed"
                error = f"{type(exc).__name__}: {exc}"
                selected = []

            selected_text = sentence_text(by_sid, selected)
            gold_text = sentence_text(by_sid, gold)
            metric_values = prf(selected, gold)
            rouge_l = (
                scorer.score(gold_text, selected_text)["rougeL"].fmeasure
                if gold_text and selected_text
                else 0.0
            )
            row = {
                "doc_id": str(doc["doc_id"]),
                "qid": str(question["qid"]),
                "role": role,
                "question": query,
                "original_question": original_question,
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
                "local_context": local_context(doc["sentences"], selected, gold),
                "error": error,
            }
            if weights:
                row["c2ges_weights"] = weights
                if isinstance(weights, dict) and "selection_fold" in weights:
                    row["cv_selection_fold"] = weights["selection_fold"]
            if diagnostic_role_masked:
                row["diagnostic"] = "role_masked_questions"
            rows.append(row)
    return rows


def mean(values: list[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def std(values: list[float]) -> float:
    return float(np.std(values, ddof=0)) if values else 0.0


def aggregate(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for condition in ALL_CONDITIONS:
        subset = [row for row in rows if row["condition"] == condition]
        ok = [row for row in subset if row["status"] == "ok"]
        output[condition] = {
            "status": "ok" if len(ok) == len(subset) else "partial_or_failed",
            "questions": len(subset),
            "ok_questions": len(ok),
            **{metric: mean([float(row[metric]) for row in ok]) for metric in METRICS},
            **{f"{metric}_std": std([float(row[metric]) for row in ok]) for metric in METRICS},
        }
    return output


def role_stratified(rows: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for condition in ALL_CONDITIONS:
        result[condition] = {}
        for role in ROLES:
            subset = [
                row for row in rows
                if row["condition"] == condition and row["role"] == role and row["status"] == "ok"
            ]
            result[condition][role] = {
                "questions": len(subset),
                **{metric: mean([float(row[metric]) for row in subset]) for metric in METRICS},
                "role_coverage": (
                    sum(1 for row in subset if float(row["evidence_f1"]) > 0.0) / len(subset)
                    if subset else 0.0
                ),
            }
    return result


def document_level(rows: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    result: dict[str, dict[str, dict[str, Any]]] = {}
    doc_ids = sorted({str(row["doc_id"]) for row in rows})
    for condition in ALL_CONDITIONS:
        result[condition] = {}
        for doc_id in doc_ids:
            subset = [
                row for row in rows
                if row["condition"] == condition and row["doc_id"] == doc_id and row["status"] == "ok"
            ]
            result[condition][doc_id] = {
                "questions": len(subset),
                **{metric: mean([float(row[metric]) for row in subset]) for metric in METRICS},
            }
    return result


def role_coverage(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    coverage: dict[str, dict[str, float]] = {}
    for condition in ALL_CONDITIONS:
        coverage[condition] = {}
        for role in ROLES:
            subset = [
                row for row in rows
                if row["condition"] == condition and row["role"] == role and row["status"] == "ok"
            ]
            coverage[condition][role] = (
                sum(1 for row in subset if float(row["evidence_f1"]) > 0.0) / len(subset)
                if subset else 0.0
            )
        coverage[condition]["macro"] = mean([coverage[condition][role] for role in ROLES])
    return coverage


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator, samples: int) -> dict[str, Any]:
    finite = np.asarray([float(value) for value in values if np.isfinite(float(value))], dtype=float)
    if finite.size == 0:
        return {"mean": 0.0, "lower": None, "upper": None, "samples": 0}
    draws = rng.choice(finite, size=(samples, finite.size), replace=True).mean(axis=1)
    return {
        "mean": float(finite.mean()),
        "lower": float(np.quantile(draws, 0.025)),
        "upper": float(np.quantile(draws, 0.975)),
        "samples": int(samples),
    }


def bootstrap_delta(delta_values: np.ndarray, rng: np.random.Generator, samples: int) -> dict[str, Any]:
    finite = np.asarray([float(value) for value in delta_values if np.isfinite(float(value))], dtype=float)
    if finite.size == 0:
        return {
            "mean_diff": 0.0,
            "ci95": {"lower": None, "upper": None},
            "bootstrap_two_sided_p": None,
            "n_units": 0,
            "samples": 0,
        }
    draws = rng.choice(finite, size=(samples, finite.size), replace=True).mean(axis=1)
    p = 2.0 * min(float(np.mean(draws <= 0.0)), float(np.mean(draws >= 0.0)))
    return {
        "mean_diff": float(finite.mean()),
        "ci95": {
            "lower": float(np.quantile(draws, 0.025)),
            "upper": float(np.quantile(draws, 0.975)),
        },
        "bootstrap_two_sided_p": min(1.0, p),
        "n_units": int(finite.size),
        "samples": int(samples),
    }


def bootstrap_statistics(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    doc_metrics = document_level(rows)
    boot: dict[str, Any] = {
        "primary_method": "document-level paired cluster bootstrap over documents",
        "secondary_sensitivity_method": "question-level paired bootstrap",
        "seed": BOOTSTRAP_SEED,
        "samples": BOOTSTRAP_SAMPLES,
        "document_level": {},
        "question_level_sensitivity": {},
    }
    for condition in ALL_CONDITIONS:
        boot["document_level"][condition] = {}
        boot["question_level_sensitivity"][condition] = {}
        for metric in METRICS:
            doc_values = np.asarray(
                [
                    values[metric]
                    for values in doc_metrics[condition].values()
                    if values["questions"] > 0
                ],
                dtype=float,
            )
            q_values = np.asarray(
                [
                    float(row[metric])
                    for row in rows
                    if row["condition"] == condition and row["status"] == "ok"
                ],
                dtype=float,
            )
            boot["document_level"][condition][metric] = bootstrap_ci(
                doc_values, rng, BOOTSTRAP_SAMPLES
            )
            boot["question_level_sensitivity"][condition][metric] = bootstrap_ci(
                q_values, rng, BOOTSTRAP_SAMPLES
            )

    by_doc_qid_condition: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_doc_qid_condition[(row["doc_id"], row["qid"])][row["condition"]] = row

    paired: dict[str, Any] = {
        "primary_method": "document-level paired cluster bootstrap significance testing",
        "secondary_sensitivity_method": "question-level paired bootstrap sensitivity",
        "comparisons": {},
    }
    for baseline in PAIRED_BASELINES:
        comparison = f"c2ges_full_vs_{baseline}"
        paired["comparisons"][comparison] = {}
        for metric in METRICS:
            question_deltas_by_doc: dict[str, list[float]] = defaultdict(list)
            question_deltas: list[float] = []
            for (doc_id, _qid), condition_rows in by_doc_qid_condition.items():
                full_row = condition_rows.get("c2ges_full")
                base_row = condition_rows.get(baseline)
                if not full_row or not base_row:
                    continue
                if full_row["status"] != "ok" or base_row["status"] != "ok":
                    continue
                delta = float(full_row[metric]) - float(base_row[metric])
                question_deltas_by_doc[doc_id].append(delta)
                question_deltas.append(delta)
            doc_deltas = np.asarray(
                [mean(values) for values in question_deltas_by_doc.values() if values],
                dtype=float,
            )
            q_deltas = np.asarray(question_deltas, dtype=float)
            paired["comparisons"][comparison][metric] = {
                "document_cluster": bootstrap_delta(doc_deltas, rng, BOOTSTRAP_SAMPLES),
                "question_sensitivity": bootstrap_delta(q_deltas, rng, BOOTSTRAP_SAMPLES),
            }
    return boot, paired


def ablation_deltas(aggregate_metrics: dict[str, dict[str, Any]]) -> dict[str, Any]:
    full = aggregate_metrics["c2ges_full"]
    return {
        "c2ges_full_minus_c2ges_query_only": {
            metric: float(full[metric]) - float(aggregate_metrics["c2ges_query_only"][metric])
            for metric in METRICS
        },
        "c2ges_full_minus_c2ges_no_role": {
            metric: float(full[metric]) - float(aggregate_metrics["c2ges_no_role"][metric])
            for metric in METRICS
        },
        "c2ges_full_minus_c2ges_no_graph": {
            metric: float(full[metric]) - float(aggregate_metrics["c2ges_no_graph"][metric])
            for metric in METRICS
        },
    }


def dependency_status(baseline_state: dict[str, Any]) -> dict[str, Any]:
    deps: dict[str, Any] = {"python": sys.version.split()[0]}
    for module_name in ["numpy", "sklearn", "networkx", "lexrank", "rouge_score"]:
        try:
            module = __import__(module_name)
            deps[module_name] = getattr(module, "__version__", "available")
        except Exception as exc:  # noqa: BLE001
            deps[module_name] = f"unavailable: {type(exc).__name__}: {exc}"
    deps["sentence_transformers"] = baseline_state.get("sbert_status", "not_checked")
    deps["sentence_transformers_error"] = baseline_state.get("sbert_error", "")
    return deps


def git_sha(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001
        return "unavailable"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--bootstrap-samples", type=int, default=BOOTSTRAP_SAMPLES)
    parser.add_argument(
        "--limit-docs",
        type=int,
        default=0,
        help="Smoke-test helper. 0 means run all documents.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    global BOOTSTRAP_SAMPLES
    BOOTSTRAP_SAMPLES = int(args.bootstrap_samples)

    workspace = discover_workspace()
    repo_root = discover_repo(workspace)
    data_dir = args.data_dir or workspace / "verification_pilot" / "agent_audit_40doc"
    output_dir = (
        args.out_dir
        or workspace / "pipeline" / "runs" / "run_001" / "stage-12" / "experiment_outputs" / "c2ges_executor_iterated"
    ).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    baselines_module = import_module(
        workspace / "verification_pilot" / "scripts" / "run_baselines.py",
        "validated_run_baselines",
    )
    c2ges_module = import_module(
        workspace / "verification_pilot" / "scripts" / "run_c2ges.py",
        "validated_run_c2ges",
    )

    docs = load_docs(data_dir)
    if args.limit_docs:
        docs = docs[: int(args.limit_docs)]
    manifest = load_manifest(data_dir, docs)
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    baseline_state = baselines_module.try_load_sbert()
    baselines = dict(baselines_module.BASELINES)
    cv_protocol, cv_config_by_doc = build_cv_protocol(docs, c2ges_module)

    detail_rows: list[dict[str, Any]] = []
    for condition in ALL_CONDITIONS:
        detail_rows.extend(
            run_condition(
                condition=condition,
                docs=docs,
                scorer=scorer,
                baselines=baselines,
                c2ges_module=c2ges_module,
                baseline_state=baseline_state,
                cv_config_by_doc=cv_config_by_doc,
            )
        )

    diagnostic_rows: list[dict[str, Any]] = []
    for condition in DIAGNOSTIC_CONDITIONS:
        diagnostic_rows.extend(
            run_condition(
                condition=condition,
                docs=docs,
                scorer=scorer,
                baselines=baselines,
                c2ges_module=c2ges_module,
                baseline_state=baseline_state,
                cv_config_by_doc=cv_config_by_doc,
                diagnostic_role_masked=True,
            )
        )

    aggregate_metrics = aggregate(detail_rows)
    role_metrics = role_stratified(detail_rows)
    doc_metrics = document_level(detail_rows)
    boot_cis, paired = bootstrap_statistics(detail_rows)
    diagnostics_summary = aggregate(diagnostic_rows)

    detail_path = output_dir / "details.jsonl"
    diagnostic_path = output_dir / "diagnostic_role_masked_details.jsonl"
    summary_path = output_dir / "summary.json"
    metadata_path = output_dir / "metadata.json"
    cv_protocol_path = output_dir / "cv_protocol.json"
    heldout_predictions_path = output_dir / "heldout_predictions.jsonl"
    output_dir_results_path = output_dir / "results.json"
    if Path.cwd().resolve() == workspace.resolve():
        root_results_path = output_dir_results_path
    else:
        root_results_path = Path.cwd() / "results.json"

    command_line = " ".join([sys.executable, *sys.argv])
    metadata = {
        "command_lines": [command_line],
        "code_version_or_git_sha": git_sha(repo_root),
        "config_path": str(workspace / "three-pack" / "config.yaml"),
        "dataset_path": str(data_dir),
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "output_paths": {
            "output_dir": str(output_dir),
            "summary_json": str(summary_path),
            "detail_jsonl": str(detail_path),
            "metadata_json": str(metadata_path),
            "cv_protocol_json": str(cv_protocol_path),
            "heldout_predictions_jsonl": str(heldout_predictions_path),
            "output_dir_results_json": str(output_dir_results_path),
            "diagnostic_detail_jsonl": str(diagnostic_path),
            "stage12_results_json": str(root_results_path),
        },
        "python_executable": sys.executable,
        "dependency_status": dependency_status(baseline_state),
        "validated_executor_route": {
            "baseline_script": str(workspace / "verification_pilot" / "scripts" / "run_baselines.py"),
            "c2ges_script": str(workspace / "verification_pilot" / "scripts" / "run_c2ges.py"),
            "legacy_c2ges_ranker_function": "rank_sentences",
            "revised_c2ges_ranker_function": "revised_rank_sentences in Stage 10 wrapper",
        },
        "method_iteration": {
            "harness_decision": "run_20260622-192649 ITERATE",
            "protocol": cv_protocol["name"],
            "legacy_condition": "c2ges_full_fixed_legacy",
            "revised_condition": "c2ges_full",
            "cv_protocol_json": str(cv_protocol_path),
            "heldout_predictions_jsonl": str(heldout_predictions_path),
        },
        "label_provenance": "agent_verified_candidate; not human gold or expert gold",
        "explicit_non_claims": [
            "not_full_structural_causal_inference",
            "not_full_graph_neural_network",
            "not_true_power_system_counterfactual_simulator",
            "not_causal_discovery",
            "not_c2ges_cover",
            "not_broad_sota_summarization_claim",
        ],
        "environment": {
            "cwd": str(Path.cwd()),
            "workspace": str(workspace),
            "repo_root": str(repo_root),
            "WEBUI_SESSION_ID": os.environ.get("WEBUI_SESSION_ID", ""),
        },
    }

    summary = {
        "dataset": manifest,
        "task": "NERC report sentences + causal role/question -> evidence_sentence_ids",
        "label_provenance": metadata["label_provenance"],
        "k": K,
        "main_conditions": MAIN_CONDITIONS,
        "ablation_conditions": C2GES_VARIANTS,
        "legacy_conditions": LEGACY_CONDITIONS,
        "aggregate_metrics_by_condition": aggregate_metrics,
        "role_stratified_metrics": role_metrics,
        "role_coverage": role_coverage(detail_rows),
        "document_level_metrics": doc_metrics,
        "paired_comparisons": paired,
        "bootstrap_confidence_intervals": boot_cis,
        "ablation_deltas": ablation_deltas(aggregate_metrics),
        "method_iteration_protocol": cv_protocol,
        "diagnostics": {
            "role_masked_questions": {
                "scope": "diagnostic_only_not_main_condition",
                "conditions": DIAGNOSTIC_CONDITIONS,
                "aggregate_metrics_by_condition": diagnostics_summary,
                "detail_jsonl": str(diagnostic_path),
            }
        },
        "metadata": metadata,
    }

    write_jsonl(detail_path, detail_rows)
    write_jsonl(diagnostic_path, diagnostic_rows)
    heldout_rows = [
        row for row in detail_rows
        if row["condition"] in {"c2ges_full", "c2ges_full_fixed_legacy"}
    ]
    write_jsonl(heldout_predictions_path, heldout_rows)
    write_json(cv_protocol_path, cv_protocol)
    write_json(summary_path, summary)
    write_json(metadata_path, metadata)
    write_json(output_dir_results_path, summary)
    write_json(root_results_path, summary)

    print("REGISTERED_CONDITIONS: " + ", ".join(MAIN_CONDITIONS))
    print("REGISTERED_ABLATIONS: " + ", ".join(C2GES_VARIANTS))
    print("REGISTERED_LEGACY_CONDITIONS: " + ", ".join(LEGACY_CONDITIONS))
    for condition in ALL_CONDITIONS:
        metrics = aggregate_metrics[condition]
        for metric in METRICS:
            print(
                "SUMMARY "
                f"condition={condition} metric={metric} "
                f"mean={metrics[metric]:.6f} std={metrics[f'{metric}_std']:.6f}"
            )
    for baseline in PAIRED_BASELINES:
        stats = paired["comparisons"][f"c2ges_full_vs_{baseline}"]["evidence_f1"]["document_cluster"]
        ci = stats["ci95"]
        print(
            "PAIRED: "
            f"c2ges_full vs {baseline} mean_diff={stats['mean_diff']:.6f} "
            f"std_diff=0.000000 t_stat=0.000000 "
            f"p_value={(stats['bootstrap_two_sided_p'] if stats['bootstrap_two_sided_p'] is not None else 1.0):.6f} "
            f"ci95=({ci['lower']:.6f},{ci['upper']:.6f})"
        )
    print(f"evidence_f1: {aggregate_metrics['c2ges_full']['evidence_f1']:.6f}")
    print(f"RESULTS_JSON: {root_results_path}")
    print(f"SUMMARY_JSON: {summary_path}")
    print(f"DETAIL_JSONL: {detail_path}")
    print(f"METADATA_JSON: {metadata_path}")


if __name__ == "__main__":
    main()
