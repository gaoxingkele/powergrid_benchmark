#!/usr/bin/env python3
"""Recompute Semantic-MMR under 256, 512, and chunk-mean MiniLM representations."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_OUTPUT = PROJECT / "03_Reproducibility" / "Data" / "postrun_embedding_ranking" / "minilm_v1"
VARIANTS = ("production_256", "extended_512", "chunk_mean_254")
ALTERNATIVES = ("extended_512", "chunk_mean_254")
BOOTSTRAP_SAMPLES = 10_000
SEED_BASE = 20_260_823


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=Path, required=True)
    parser.add_argument("--formal-predictions", type=Path, required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256(path).encode("ascii"))
    return digest.hexdigest().upper()


def normalize_rows(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    return matrix / norms


def semantic_mmr(sids: list[str], positions: dict[str, int], embeddings: np.ndarray, budget: int) -> list[str]:
    centroid = embeddings.mean(axis=0)
    norm = float(np.linalg.norm(centroid))
    if norm:
        centroid = centroid / norm
    relevance = embeddings @ centroid
    similarity = embeddings @ embeddings.T
    selected: list[int] = []
    while len(selected) < min(budget, len(sids)):
        candidates: list[tuple[float, int, str, int]] = []
        for index, sid in enumerate(sids):
            if index in selected:
                continue
            maximum_similarity = max((float(similarity[index, prior]) for prior in selected), default=0.0)
            adjusted = 0.5 * float(relevance[index]) - 0.5 * maximum_similarity
            candidates.append((adjusted, -positions[sid], sid, index))
        selected.append(max(candidates)[3])
    return [sids[index] for index in selected]


def jaccard(left: str, right: str) -> float:
    a = set(left.lower().split())
    b = set(right.lower().split())
    return len(a & b) / len(a | b) if a or b else 0.0


def redundancy(texts: list[str]) -> float:
    values = [jaccard(left, right) for index, left in enumerate(texts) for right in texts[index + 1 :]]
    return statistics.fmean(values) if values else 0.0


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def exact_sign_flip(values: list[float]) -> float:
    observed = abs(statistics.fmean(values))
    extreme = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(values)):
        total += 1
        statistic = abs(statistics.fmean(sign * value for sign, value in zip(signs, values)))
        if statistic >= observed - 1e-15:
            extreme += 1
    return extreme / total


def holm(rows: list[dict[str, Any]]) -> None:
    order = sorted(range(len(rows)), key=lambda index: rows[index]["exact_series_signflip_p"])
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(rows) - rank) * rows[index]["exact_series_signflip_p"]))
        rows[index]["holm_adjusted_p_four"] = running


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite output: {args.output}")
    test_rows = load_jsonl(args.test)
    formal_rows = [
        row for row in load_jsonl(args.formal_predictions)
        if row["condition"] == "semantic_mmr"
    ]
    if len(test_rows) != 15 or len(formal_rows) != 30:
        raise AssertionError("Expected 15 test reports and 30 frozen Semantic-MMR rows")

    tokenizer = AutoTokenizer.from_pretrained(args.model_snapshot, local_files_only=True)
    model = SentenceTransformer(str(args.model_snapshot), device="cpu", local_files_only=True)
    if int(model.max_seq_length) != 256:
        raise AssertionError(f"Expected production max_seq_length=256, found {model.max_seq_length}")
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    formal = {(row["doc_id"], int(row["budget"])): row for row in formal_rows}

    result_rows: list[dict[str, Any]] = []
    embedding_rows: list[dict[str, Any]] = []
    series_by_doc: dict[str, str] = {}
    total_candidates = 0
    total_over_256 = 0
    total_over_512 = 0

    for report in test_rows:
        doc_id = report["doc_id"]
        series_by_doc[doc_id] = report["report_series_id"]
        candidates = report["candidate_sentences"]
        sids = [item["sid"] for item in candidates]
        texts = [item["text"] for item in candidates]
        text_by_sid = {item["sid"]: item["text"] for item in candidates}
        positions = {item["sid"]: index for index, item in enumerate(candidates)}
        token_ids = tokenizer(texts, add_special_tokens=True, truncation=False, padding=False)["input_ids"]
        token_lengths = [len(value) for value in token_ids]
        total_candidates += len(candidates)
        total_over_256 += sum(value > 256 for value in token_lengths)
        total_over_512 += sum(value > 512 for value in token_lengths)

        model.max_seq_length = 256
        production = np.asarray(
            model.encode(texts, batch_size=32, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False),
            dtype=np.float32,
        )
        model.max_seq_length = 512
        extended = np.asarray(
            model.encode(texts, batch_size=32, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False),
            dtype=np.float32,
        )
        model.max_seq_length = 256
        chunked = production.copy()
        for index, length in enumerate(token_lengths):
            if length <= 256:
                continue
            content_ids = tokenizer(texts[index], add_special_tokens=False, truncation=False)["input_ids"]
            chunks = [content_ids[start : start + 254] for start in range(0, len(content_ids), 254)]
            decoded = [tokenizer.decode(chunk, skip_special_tokens=True, clean_up_tokenization_spaces=False) for chunk in chunks]
            chunk_embeddings = np.asarray(
                model.encode(decoded, batch_size=16, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False),
                dtype=np.float32,
            )
            pooled = chunk_embeddings.mean(axis=0, keepdims=True)
            chunked[index] = normalize_rows(pooled)[0]
        variants = {
            "production_256": production,
            "extended_512": extended,
            "chunk_mean_254": chunked,
        }

        cos_extended = np.sum(production * extended, axis=1)
        cos_chunked = np.sum(production * chunked, axis=1)
        embedding_rows.append(
            {
                "doc_id": doc_id,
                "report_series_id": report["report_series_id"],
                "candidate_count": len(candidates),
                "candidates_over_256": sum(value > 256 for value in token_lengths),
                "candidates_over_512": sum(value > 512 for value in token_lengths),
                "mean_cosine_256_vs_512_all": float(np.mean(cos_extended)),
                "minimum_cosine_256_vs_512_all": float(np.min(cos_extended)),
                "mean_cosine_256_vs_chunk_all": float(np.mean(cos_chunked)),
                "minimum_cosine_256_vs_chunk_all": float(np.min(cos_chunked)),
                "mean_cosine_256_vs_512_over256": float(np.mean(cos_extended[np.array(token_lengths) > 256])) if any(value > 256 for value in token_lengths) else "",
                "mean_cosine_256_vs_chunk_over256": float(np.mean(cos_chunked[np.array(token_lengths) > 256])) if any(value > 256 for value in token_lengths) else "",
            }
        )

        selections: dict[tuple[str, int], list[str]] = {}
        for variant, embeddings in variants.items():
            for budget in (5, 10):
                order = semantic_mmr(sids, positions, embeddings, budget)
                selections[(variant, budget)] = order
                document_order = sorted(order, key=lambda sid: (positions[sid], sid))
                selected_texts = [text_by_sid[sid] for sid in document_order]
                prediction = " ".join(selected_texts)
                scores = scorer.score(report["reference_summary"], prediction)
                base_set = set(selections.get(("production_256", budget), order))
                result_rows.append(
                    {
                        "doc_id": doc_id,
                        "report_series_id": report["report_series_id"],
                        "variant": variant,
                        "budget": budget,
                        "selected_sentence_ids": "|".join(document_order),
                        "selection_overlap_with_production": len(set(order) & base_set) / budget,
                        "rouge1_f1": float(scores["rouge1"].fmeasure),
                        "rouge2_f1": float(scores["rouge2"].fmeasure),
                        "rougeL_f1": float(scores["rougeL"].fmeasure),
                        "redundancy": redundancy(selected_texts),
                    }
                )

        for budget in (5, 10):
            reproduced = next(
                row for row in result_rows
                if row["doc_id"] == doc_id and row["variant"] == "production_256" and row["budget"] == budget
            )
            frozen = formal[(doc_id, budget)]
            if set(reproduced["selected_sentence_ids"].split("|")) != set(frozen["selected_sentence_ids"]):
                raise AssertionError(f"{doc_id}/K={budget}: production selection does not reproduce")
            if abs(reproduced["rougeL_f1"] - float(frozen["metrics"]["rougeL_f1"])) > 1e-12:
                raise AssertionError(f"{doc_id}/K={budget}: production metric does not reproduce")

    if total_candidates != 9504 or len(result_rows) != 90:
        raise AssertionError(f"Cardinality mismatch: candidates={total_candidates}, rows={len(result_rows)}")
    metric = {(row["doc_id"], row["variant"], row["budget"]): row["rougeL_f1"] for row in result_rows}
    reports_by_series: dict[str, list[str]] = defaultdict(list)
    for doc_id, series_id in series_by_doc.items():
        reports_by_series[series_id].append(doc_id)
    series_ids = sorted(reports_by_series)
    if len(series_ids) != 10:
        raise AssertionError("Expected 10 report series")

    contrasts: list[dict[str, Any]] = []
    for budget in (5, 10):
        for variant_index, variant in enumerate(ALTERNATIVES):
            report_differences = {
                doc_id: metric[(doc_id, variant, budget)] - metric[(doc_id, "production_256", budget)]
                for doc_id in series_by_doc
            }
            series_differences = [
                statistics.fmean(report_differences[doc_id] for doc_id in reports_by_series[series_id])
                for series_id in series_ids
            ]
            rng = random.Random(SEED_BASE + budget * 100 + variant_index)
            bootstrap = [statistics.fmean(rng.choice(series_differences) for _ in series_differences) for _ in range(BOOTSTRAP_SAMPLES)]
            changed = sum(
                next(row for row in result_rows if row["doc_id"] == doc_id and row["variant"] == variant and row["budget"] == budget)["selection_overlap_with_production"] < 1.0
                for doc_id in series_by_doc
            )
            contrasts.append(
                {
                    "budget": budget,
                    "contrast": f"{variant}_minus_production_256",
                    "changed_report_budget_cells": changed,
                    "equal_series_mean_rougeL_difference": statistics.fmean(series_differences),
                    "equal_report_mean_rougeL_difference": statistics.fmean(report_differences.values()),
                    "cluster_bootstrap_95_low": percentile(bootstrap, 0.025),
                    "cluster_bootstrap_95_high": percentile(bootstrap, 0.975),
                    "exact_series_signflip_p": exact_sign_flip(series_differences),
                    "holm_adjusted_p_four": 0.0,
                    "bootstrap_samples": BOOTSTRAP_SAMPLES,
                    "bootstrap_seed": SEED_BASE + budget * 100 + variant_index,
                }
            )
    holm(contrasts)

    args.output.mkdir(parents=True)
    write_csv(args.output / "embedding_report_diagnostics.csv", embedding_rows)
    write_csv(args.output / "embedding_selection_metrics.csv", result_rows)
    write_csv(args.output / "embedding_ranking_contrasts.csv", contrasts)
    summary = {
        "analysis_id": "C2GES-MiniLM-ranking-sensitivity-v1",
        "status": "post_run_representation_sensitivity_not_confirmatory",
        "model": {
            "name": "sentence-transformers/all-MiniLM-L6-v2",
            "revision": args.model_snapshot.name,
            "snapshot_tree_sha256": tree_sha256(args.model_snapshot),
            "production_max_seq_length": 256,
            "extended_max_seq_length": 512,
            "chunk_content_tokens": 254,
        },
        "inputs": {"test_sha256": sha256(args.test), "formal_predictions_sha256": sha256(args.formal_predictions)},
        "reports": 15,
        "series": 10,
        "candidates": total_candidates,
        "candidates_over_256": total_over_256,
        "candidates_over_512": total_over_512,
        "selection_rows": len(result_rows),
        "contrasts": contrasts,
        "privacy": "No candidate, reference, prediction, or decoded chunk text is written to outputs.",
    }
    (args.output / "embedding_ranking_results.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# C2GES MiniLM ranking sensitivity",
        "",
        "Status: post-run representation sensitivity. The production 256-token selections and metrics were reproduced before alternatives were accepted.",
        "",
        "| K | Contrast | Changed cells | Equal-series ROUGE-L difference | Cluster-bootstrap 95% interval | Holm p |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    for row in contrasts:
        lines.append(
            f"| {row['budget']} | {row['contrast']} | {row['changed_report_budget_cells']}/15 | "
            f"{row['equal_series_mean_rougeL_difference']:+.5f} | "
            f"[{row['cluster_bootstrap_95_low']:+.5f}, {row['cluster_bootstrap_95_high']:+.5f}] | "
            f"{row['holm_adjusted_p_four']:.6f} |"
        )
    lines.extend(
        [
            "",
            "The alternatives diagnose whether the small truncated subset can change Semantic-MMR rankings. They are post-run rules on one retained corpus and do not establish a preferred long-text encoder.",
            "",
        ]
    )
    (args.output / "EMBEDDING_RANKING_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": "PASS", "candidates": total_candidates, "over_256": total_over_256, "output": str(args.output)}))


if __name__ == "__main__":
    main()
