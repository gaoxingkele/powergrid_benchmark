#!/usr/bin/env python3
"""Frozen zero-shot BGE reranker over the document-grouped FEVER test set."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import threading
import time
from pathlib import Path

import numpy as np
import psutil
import sentence_transformers
import torch
from sentence_transformers import CrossEncoder


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def tree_inventory(root: Path) -> dict:
    files = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        files.append({"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    return {"file_count": len(files), "bytes": sum(x["bytes"] for x in files), "files": files}


def evidence_scores(pred: list[str], gold: list[str]) -> tuple[float, float, float]:
    ps, gs = set(pred), set(gold)
    if not ps or not gs:
        return 0.0, 0.0, 0.0
    tp = len(ps & gs)
    precision, recall = tp / len(ps), tp / len(gs)
    return precision, recall, 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    freeze = json.loads(args.freeze.read_text(encoding="utf-8"))
    if freeze["status"] != "FROZEN_NOT_RUN" or not freeze["formal_execution_authorized"]:
        raise RuntimeError("freeze does not authorize the formal run")
    if args.out.exists():
        raise RuntimeError(f"refusing existing formal output directory: {args.out}")
    if sha256(args.data / "manifest.json") != freeze["inputs"]["data_manifest"]["sha256"]:
        raise RuntimeError("data manifest hash mismatch")
    model_inventory = tree_inventory(args.model_path)
    if model_inventory != freeze["inputs"]["model"]["inventory"]:
        raise RuntimeError("model inventory mismatch")
    runner_hash = sha256(Path(__file__))
    if runner_hash != freeze["code"]["runner_sha256"]:
        raise RuntimeError("runner hash mismatch")
    args.out.mkdir(parents=True, exist_ok=False)

    seed = int(freeze["execution"]["seed"])
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    cutoffs = [int(x) for x in freeze["execution"]["cutoffs"]]
    batch_size = int(freeze["execution"]["batch_size"])
    max_length = int(freeze["execution"]["max_length"])

    stop = threading.Event()
    peak = {"rss": 0}
    process = psutil.Process()

    def monitor() -> None:
        while not stop.wait(0.1):
            try:
                rss = process.memory_info().rss + sum(c.memory_info().rss for c in process.children(recursive=True))
                peak["rss"] = max(peak["rss"], rss)
            except psutil.Error:
                pass

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    started = time.perf_counter()
    model = CrossEncoder(str(args.model_path.resolve()), max_length=max_length, device="cpu")
    rows = []
    candidate_pairs = 0
    documents = sorted((args.data / "test").glob("*.json"))
    for doc_path in documents:
        doc = json.loads(doc_path.read_text(encoding="utf-8"))
        sids = [str(s["sid"]) for s in doc["sentences"]]
        texts = [str(s["text"]) for s in doc["sentences"]]
        for question in doc["causal_questions"]:
            claim = str(question["question"])
            pairs = list(zip([claim] * len(texts), texts))
            candidate_pairs += len(pairs)
            scores = np.asarray(model.predict(pairs, batch_size=batch_size, show_progress_bar=False), dtype=float).reshape(-1)
            if scores.shape != (len(sids),) or not np.all(np.isfinite(scores)):
                raise RuntimeError(f"invalid score vector for {question['qid']}")
            order = np.argsort(-scores, kind="stable")
            gold = [str(x) for x in question["evidence_sentence_ids"]]
            score_map = {sid: float(score) for sid, score in zip(sids, scores)}
            for k in cutoffs:
                pred = [sids[i] for i in order[:k]]
                precision, recall, f1 = evidence_scores(pred, gold)
                rows.append({
                    "qid": str(question["qid"]),
                    "doc_id": str(doc["doc_id"]),
                    "underlying_document_id": str(doc["underlying_document_id"]),
                    "wikipedia_title": str(doc.get("wikipedia_title", doc["underlying_document_id"])),
                    "gold_role": str(question["role"]),
                    "selector_role": "not_used",
                    "mode": "bge_reranker_base",
                    "k": k,
                    "predicted_sentence_ids": pred,
                    "gold_sentence_ids": gold,
                    "candidate_scores": score_map,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                })
    elapsed = time.perf_counter() - started
    stop.set()
    thread.join(timeout=1)
    expected_rows = int(freeze["execution"]["expected_prediction_rows"])
    keys = [(r["qid"], r["k"]) for r in rows]
    if len(rows) != expected_rows or len(set(keys)) != expected_rows:
        raise RuntimeError(f"prediction coverage mismatch rows={len(rows)} unique={len(set(keys))}")
    predictions = args.out / "predictions.jsonl"
    with predictions.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    resource = {
        "status": "success",
        "boundary": "model load plus complete FEVER test scoring and all-K extraction",
        "device": "cpu",
        "wall_seconds": elapsed,
        "sampled_peak_rss_bytes": peak["rss"],
        "documents": len(documents),
        "instances": len(rows) // len(cutoffs),
        "candidate_pairs": candidate_pairs,
        "prediction_rows": len(rows),
    }
    (args.out / "resource_usage.json").write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "freeze_sha256": sha256(args.freeze),
        "freeze_content_sha256": freeze["freeze_content_sha256"],
        "command": sys.argv,
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "sentence_transformers": sentence_transformers.__version__,
        "runner_sha256": runner_hash,
        "data_manifest_sha256": sha256(args.data / "manifest.json"),
        "test_partition_sha256": json.loads((args.data / "manifest.json").read_text(encoding="utf-8"))["content_hashes"]["test"]["sha256"],
        "model_revision": freeze["inputs"]["model"]["revision"],
        "model_inventory": model_inventory,
        "predictions_sha256": sha256(predictions),
        "resource_usage_sha256": sha256(args.out / "resource_usage.json"),
        "cutoffs": cutoffs,
        "batch_size": batch_size,
        "max_length": max_length,
        "seed": seed,
    }
    (args.out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(resource))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
