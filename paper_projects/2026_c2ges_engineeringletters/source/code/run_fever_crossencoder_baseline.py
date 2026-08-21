#!/usr/bin/env python3
"""Frozen zero-shot cross-encoder baseline for the document-grouped FEVER test set."""
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


def tree_sha(root: Path) -> dict:
    h = hashlib.sha256()
    files = sorted(p for p in root.rglob("*") if p.is_file())
    for path in files:
        rel = path.relative_to(root).as_posix().encode()
        h.update(len(rel).to_bytes(8, "big")); h.update(rel)
        digest = bytes.fromhex(sha256(path)); h.update(digest)
    return {"sha256": h.hexdigest(), "file_count": len(files), "bytes": sum(p.stat().st_size for p in files)}


def evidence_f1(pred: list[str], gold: list[str]) -> tuple[float, float, float]:
    ps, gs = set(pred), set(gold)
    if not ps or not gs:
        return 0.0, 0.0, 0.0
    tp = len(ps & gs); precision = tp / len(ps); recall = tp / len(gs)
    return precision, recall, 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model-path", type=Path, required=True)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--max-length", type=int, default=512)
    ap.add_argument("--cutoffs", default="1,3,5,10")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    cutoffs = [int(x) for x in args.cutoffs.split(",")]

    stop = threading.Event(); peak = {"rss": 0}
    process = psutil.Process()
    def monitor() -> None:
        while not stop.wait(0.1):
            try:
                rss = process.memory_info().rss + sum(c.memory_info().rss for c in process.children(recursive=True))
                peak["rss"] = max(peak["rss"], rss)
            except psutil.Error:
                pass
    thread = threading.Thread(target=monitor, daemon=True); thread.start()
    started = time.perf_counter()

    model = CrossEncoder(str(args.model_path.resolve()), max_length=args.max_length, device="cpu")
    rows = []
    documents = sorted((args.data / "test").glob("*.json"))
    for doc_path in documents:
        doc = json.loads(doc_path.read_text(encoding="utf-8"))
        sids = [str(s["sid"]) for s in doc["sentences"]]
        texts = [str(s["text"]) for s in doc["sentences"]]
        for question in doc["causal_questions"]:
            claim = str(question["question"])
            scores = np.asarray(model.predict(list(zip([claim] * len(texts), texts)), batch_size=args.batch_size, show_progress_bar=False), dtype=float).reshape(-1)
            order = np.argsort(-scores, kind="stable")
            gold = [str(x) for x in question["evidence_sentence_ids"]]
            score_map = {sid: float(score) for sid, score in zip(sids, scores)}
            for k in cutoffs:
                pred = [sids[i] for i in order[:k]]
                precision, recall, f1 = evidence_f1(pred, gold)
                rows.append({
                    "qid": str(question["qid"]), "doc_id": str(doc["doc_id"]),
                    "underlying_document_id": str(doc["underlying_document_id"]),
                    "wikipedia_title": str(doc.get("wikipedia_title", doc["underlying_document_id"])),
                    "gold_role": str(question["role"]), "selector_role": "not_used",
                    "mode": "cross_encoder", "k": k, "predicted_sentence_ids": pred,
                    "gold_sentence_ids": gold, "candidate_scores": score_map,
                    "precision": precision, "recall": recall, "f1": f1,
                })
    elapsed = time.perf_counter() - started
    stop.set(); thread.join(timeout=1)
    predictions = args.out / "predictions.jsonl"
    with predictions.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    resource = {
        "status": "success", "boundary": "model load plus complete test scoring and top-K extraction",
        "device": "cpu", "wall_seconds": elapsed, "sampled_peak_rss_bytes": peak["rss"],
        "documents": len(documents), "instances": len(rows) // len(cutoffs), "prediction_rows": len(rows)
    }
    (args.out / "resource_usage.json").write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")
    provenance = {
        "command": sys.argv, "python": sys.version, "platform": platform.platform(),
        "torch": torch.__version__, "sentence_transformers": sentence_transformers.__version__,
        "model_path": str(args.model_path.resolve()), "model_tree": tree_sha(args.model_path),
        "data_manifest_sha256": sha256(args.data / "manifest.json"),
        "test_partition_sha256": json.loads((args.data / "manifest.json").read_text(encoding="utf-8"))["content_hashes"]["test"]["sha256"],
        "predictions_sha256": sha256(predictions), "cutoffs": cutoffs,
        "batch_size": args.batch_size, "max_length": args.max_length,
    }
    (args.out / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(resource))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
