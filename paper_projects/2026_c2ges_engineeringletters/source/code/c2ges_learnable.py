#!/usr/bin/env python3
"""Learnable-role C2GES on FEVER human-gold evidence selection.

Score(s) = w_q * Q(s,q) + w_r * R_theta(s,q,role) + w_g * G(s,D)
where Q is frozen SBERT cosine, R_theta is an MLP on [h_s; h_q; h_r],
and G is a light local-chain consistency feature.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import random
import re
import subprocess
import sys
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[2]  # .../2026_c2ges_engineeringletters
DEFAULT_DATA = ROOT / "workspace/fever_benchmark"
DEFAULT_OUT = ROOT / "workspace/fever_runs/learnable_role"

ROLES = ["supports", "refutes", "unknown"]
PROTOCOLS = {
    "oracle-label": {
        "role_source": "human_gold_FEVER_veracity_label",
        "is_end_to_end": False,
        "reporting_constraint": "Conditional evidence-selection only; MUST NOT be reported as end-to-end performance.",
    },
    "predicted-label": {
        "role_source": "external_predictions",
        "is_end_to_end": True,
        "reporting_constraint": "Include the upstream label predictor and its errors when reporting end-to-end performance.",
    },
    "label-blind": {
        "role_source": "constant_unknown_role",
        "is_end_to_end": True,
        "reporting_constraint": "No gold or predicted veracity label is exposed to the selector.",
    },
}
DEFAULT_K = 3


def load_docs(split_dir: Path) -> list[dict]:
    docs = []
    for p in sorted(split_dir.glob("*.json")):
        doc = json.loads(p.read_text(encoding="utf-8"))
        # Backward-compatible recovery for corpora produced before the original
        # FEVER document ID was made explicit.  `title` was preserved verbatim.
        underlying = doc.get("underlying_document_id") or doc.get("document_id") or doc.get("wikipedia_title") or doc.get("title")
        if not underlying:
            raise ValueError(f"missing underlying Wikipedia document identifier: {p}")
        doc["underlying_document_id"] = str(underlying)
        doc.setdefault("wikipedia_title", str(underlying))
        doc["_source_path"] = str(p.resolve())
        docs.append(doc)
    return docs


def load_predicted_labels(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    raw = path.read_text(encoding="utf-8")
    records = []
    if path.suffix.lower() == ".jsonl":
        records = [json.loads(line) for line in raw.splitlines() if line.strip()]
    else:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            records = [{"qid": key, "predicted_label": value} for key, value in parsed.items()]
        elif isinstance(parsed, list):
            records = parsed
        else:
            raise ValueError("predicted-label file must be a JSON object/list or JSONL")
    out = {}
    for record in records:
        qid = str(record.get("qid") or record.get("id") or "")
        value = record.get("predicted_role", record.get("predicted_label"))
        if isinstance(value, dict):
            value = value.get("role", value.get("label"))
        role = str(value or "").lower().replace(" ", "_")
        if role.startswith("support"):
            role = "supports"
        elif role.startswith("refute"):
            role = "refutes"
        if not qid or role not in {"supports", "refutes"}:
            raise ValueError(f"invalid predicted-label record: {record!r}")
        out[qid] = role
    return out


def protocol_role(q: dict, protocol: str, predicted_labels: dict[str, str]) -> str:
    if protocol == "label-blind":
        return "unknown"
    gold_role = q["role"]
    if protocol == "oracle-label":
        return gold_role
    qid = str(q.get("qid") or "")
    if qid not in predicted_labels:
        raise ValueError(f"predicted-label protocol is missing a prediction for qid={qid!r}")
    return predicted_labels[qid]


def evidence_f1(pred: list[str], gold: list[str]) -> tuple[float, float, float]:
    ps, gs = set(pred), set(gold)
    if not ps and not gs:
        return 1.0, 1.0, 1.0
    if not ps or not gs:
        return 0.0, 0.0, 0.0
    tp = len(ps & gs)
    prec = tp / len(ps)
    rec = tp / len(gs)
    f1 = 0.0 if prec + rec == 0 else 2 * prec * rec / (prec + rec)
    return prec, rec, f1


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def bm25_scores(query: str, sentences: list[str], k1: float = 1.5, b: float = 0.75) -> np.ndarray:
    docs_tok = [tokenize(s) for s in sentences]
    q_tok = tokenize(query)
    N = len(docs_tok)
    avgdl = np.mean([len(d) for d in docs_tok]) if docs_tok else 0.0
    df = defaultdict(int)
    for d in docs_tok:
        for t in set(d):
            df[t] += 1
    scores = np.zeros(N, dtype=np.float64)
    for i, d in enumerate(docs_tok):
        tf = defaultdict(int)
        for t in d:
            tf[t] += 1
        dl = len(d) or 1
        s = 0.0
        for t in q_tok:
            if tf[t] == 0:
                continue
            idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
            s += idf * (tf[t] * (k1 + 1)) / (tf[t] + k1 * (1 - b + b * dl / (avgdl or 1)))
        scores[i] = s
    return scores


def local_chain_scores(n: int, goldish_proxy: np.ndarray | None = None) -> np.ndarray:
    """Proximity-smoothed salience; uses sentence index structure only + optional proxy."""
    base = np.ones(n, dtype=np.float64)
    if goldish_proxy is not None:
        base = goldish_proxy.copy()
    out = np.zeros(n, dtype=np.float64)
    for i in range(n):
        acc = 0.0
        wsum = 0.0
        for j in range(n):
            if i == j:
                continue
            w = math.exp(-abs(i - j) / 3.0)
            acc += w * base[j]
            wsum += w
        out[i] = acc / (wsum or 1.0)
    return out


def minmax(x: np.ndarray) -> np.ndarray:
    lo, hi = float(x.min()), float(x.max())
    if hi - lo < 1e-12:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


class RoleHead(nn.Module):
    def __init__(self, dim: int, n_roles: int, hidden: int = 256):
        super().__init__()
        self.role_emb = nn.Embedding(n_roles, dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim * 3, hidden),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden, 1),
        )

    def forward(self, h_s: torch.Tensor, h_q: torch.Tensor, role_ids: torch.Tensor) -> torch.Tensor:
        h_r = self.role_emb(role_ids)
        x = torch.cat([h_s, h_q, h_r], dim=-1)
        return self.mlp(x).squeeze(-1)


class MixtureParams(nn.Module):
    """Positive mixture with floors so the role term cannot collapse to ~0."""

    def __init__(self, floors: tuple[float, float, float] = (0.35, 0.25, 0.05)):
        super().__init__()
        self.raw = nn.Parameter(torch.tensor([0.8, 0.7, 0.2], dtype=torch.float32))
        self.register_buffer("floors", torch.tensor(floors, dtype=torch.float32))

    def weights(self) -> torch.Tensor:
        free = torch.nn.functional.softplus(self.raw) + 1e-3
        free = free / free.sum()
        # Blend free allocation with floors, then renormalize.
        w = self.floors + (1.0 - self.floors.sum()) * free
        return w / w.sum()


class TwoChannelMixture(nn.Module):
    """Query/local mixture with the role channel and its floor structurally absent."""

    def __init__(self, floors: tuple[float, float] = (0.35, 0.05)):
        super().__init__()
        self.raw = nn.Parameter(torch.tensor([0.8, 0.2], dtype=torch.float32))
        self.register_buffer("floors", torch.tensor(floors, dtype=torch.float32))

    def weights(self) -> torch.Tensor:
        free = torch.nn.functional.softplus(self.raw) + 1e-3
        free = free / free.sum()
        w2 = self.floors + (1.0 - self.floors.sum()) * free
        w2 = w2 / w2.sum()
        return torch.stack((w2[0], w2.new_tensor(0.0), w2[1]))


class ZeroRoleHead(nn.Module):
    """Parameter-free role placeholder; its output has exactly zero mixture weight."""

    def forward(self, h_s: torch.Tensor, h_q: torch.Tensor, role_ids: torch.Tensor) -> torch.Tensor:
        return torch.zeros(h_s.shape[0], dtype=h_s.dtype, device=h_s.device)


def encode_corpus(encoder: SentenceTransformer, texts: list[str], batch_size: int = 64) -> np.ndarray:
    if not texts:
        return np.zeros((0, encoder.get_sentence_embedding_dimension()), dtype=np.float32)
    emb = encoder.encode(texts, batch_size=batch_size, show_progress_bar=False, convert_to_numpy=True)
    return np.asarray(emb, dtype=np.float32)


def build_examples(
    docs: list[dict],
    encoder: SentenceTransformer,
    role2id: dict[str, int],
    *,
    protocol: str = "oracle-label",
    predicted_labels: dict[str, str] | None = None,
):
    predicted_labels = predicted_labels or {}
    examples = []
    all_sent_texts = []
    all_claims = []
    meta = []
    for doc in docs:
        sents = doc["sentences"]
        texts = [s["text"] for s in sents]
        sids = [s["sid"] for s in sents]
        for q in doc["causal_questions"]:
            gold_role = q["role"]
            if gold_role not in {"supports", "refutes"}:
                continue
            role = protocol_role(q, protocol, predicted_labels)
            gold = q["evidence_sentence_ids"]
            if not gold:
                continue
            all_sent_texts.extend(texts)
            all_claims.append(q["question"])
            meta.append(
                {
                    "doc_id": doc["doc_id"],
                    "underlying_document_id": doc["underlying_document_id"],
                    "wikipedia_title": doc.get("wikipedia_title", doc["underlying_document_id"]),
                    "qid": q.get("qid", f"{doc['doc_id']}::{gold_role}"),
                    "sids": sids,
                    "texts": texts,
                    "claim": q["question"],
                    "role": role,
                    "gold_role": gold_role,
                    "role_id": role2id[role],
                    "gold": gold,
                    "n": len(texts),
                }
            )
    # Encode all sentences in one pass per unique string to save time
    uniq_sents = list(dict.fromkeys(all_sent_texts))
    uniq_claims = list(dict.fromkeys(all_claims))
    sent_map = {t: i for i, t in enumerate(uniq_sents)}
    claim_map = {t: i for i, t in enumerate(uniq_claims)}
    print(f"  encoding {len(uniq_sents)} sentences, {len(uniq_claims)} claims...", flush=True)
    sent_emb = encode_corpus(encoder, uniq_sents)
    claim_emb = encode_corpus(encoder, uniq_claims)
    for m in meta:
        hs = np.stack([sent_emb[sent_map[t]] for t in m["texts"]], axis=0)
        hq = claim_emb[claim_map[m["claim"]]]
        q_cos = cosine_similarity(hs, hq.reshape(1, -1)).reshape(-1)
        tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        try:
            X = tfidf.fit_transform(m["texts"] + [m["claim"]])
            tfidf_q = cosine_similarity(X[:-1], X[-1]).reshape(-1)
        except ValueError:
            tfidf_q = np.zeros(m["n"])
        bm25 = bm25_scores(m["claim"], m["texts"])
        g = local_chain_scores(m["n"], minmax(q_cos))
        examples.append(
            {
                **m,
                "hs": hs.astype(np.float32),
                "hq": hq.astype(np.float32),
                "Q": minmax(0.5 * minmax(q_cos) + 0.5 * minmax(tfidf_q)).astype(np.float32),
                "G": minmax(g).astype(np.float32),
                "bm25": minmax(bm25).astype(np.float32),
                "sbert": minmax(q_cos).astype(np.float32),
                "tfidf": minmax(tfidf_q).astype(np.float32),
            }
        )
    return examples


def pairwise_loss(scores: torch.Tensor, gold_mask: torch.Tensor) -> torch.Tensor:
    pos = scores[gold_mask]
    neg = scores[~gold_mask]
    if pos.numel() == 0 or neg.numel() == 0:
        return scores.new_tensor(0.0)
    # softplus(neg - pos) averaged
    diff = neg.unsqueeze(0) - pos.unsqueeze(1)
    return torch.nn.functional.softplus(diff).mean()


def role_contrast_loss(r_scores: torch.Tensor, gold_mask: torch.Tensor) -> torch.Tensor:
    """Directly supervise the role head so it cannot be ignored by the mixer."""
    return pairwise_loss(r_scores, gold_mask)


def train_model(train_ex, dev_ex, dim: int, epochs: int, lr: float, device: str, seed: int, k: int, architecture: str = "original"):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    role2id = {r: i for i, r in enumerate(ROLES)}
    if architecture == "true_no_role":
        head = ZeroRoleHead().to(device)
        mix = TwoChannelMixture().to(device)
    else:
        head = RoleHead(dim, n_roles=len(ROLES)).to(device)
        floors = (0.0, 0.0, 0.0) if architecture == "true_no_floor" else (0.35, 0.25, 0.05)
        mix = MixtureParams(floors=floors).to(device)
    opt = torch.optim.Adam(list(head.parameters()) + list(mix.parameters()), lr=lr)
    best = {"f1": -1.0, "state": None}

    def run_epoch(examples, train: bool):
        if train:
            head.train()
            mix.train()
            random.shuffle(examples)
        else:
            head.eval()
            mix.eval()
        total_loss = 0.0
        f1s = []
        with torch.set_grad_enabled(train):
            for ex in examples:
                hs = torch.tensor(ex["hs"], device=device)
                hq = torch.tensor(ex["hq"], device=device).unsqueeze(0).expand(ex["n"], -1)
                role = torch.tensor([ex["role_id"]] * ex["n"], device=device)
                r = head(hs, hq, role)
                r_sig = torch.sigmoid(r)
                Q = torch.tensor(ex["Q"], device=device)
                G = torch.tensor(ex["G"], device=device)
                w = mix.weights()
                scores = w[0] * Q + w[1] * r_sig + w[2] * G
                gold_mask = torch.tensor([sid in set(ex["gold"]) for sid in ex["sids"]], device=device)
                loss = pairwise_loss(scores, gold_mask)
                if architecture != "true_no_role":
                    loss = loss + 0.5 * role_contrast_loss(r_sig, gold_mask)
                if train and loss.requires_grad:
                    opt.zero_grad()
                    loss.backward()
                    opt.step()
                total_loss += float(loss.detach().cpu())
                # predict
                sc = scores.detach().cpu().numpy()
                order = np.argsort(-sc)
                pred = [ex["sids"][i] for i in order[:k]]
                f1s.append(evidence_f1(pred, ex["gold"])[2])
        return total_loss / max(1, len(examples)), float(np.mean(f1s) if f1s else 0.0)

    for ep in range(1, epochs + 1):
        tr_loss, tr_f1 = run_epoch(train_ex, True)
        dv_loss, dv_f1 = run_epoch(dev_ex, False)
        print(f"epoch {ep}: train_loss={tr_loss:.4f} train_f1={tr_f1:.4f} dev_f1={dv_f1:.4f} w={mix.weights().detach().cpu().tolist()}", flush=True)
        if dv_f1 > best["f1"]:
            best = {
                "f1": dv_f1,
                "state": {
                    "head": {k: v.detach().cpu() for k, v in head.state_dict().items()},
                    "mix": {k: v.detach().cpu() for k, v in mix.state_dict().items()},
                    "role2id": role2id,
                    "dim": dim,
                },
            }
    head.load_state_dict(best["state"]["head"])
    mix.load_state_dict(best["state"]["mix"])
    head.to(device)
    mix.to(device)
    return head, mix, best


@torch.no_grad()
def predict_scores(ex, head, mix, device, mode: str = "full") -> np.ndarray:
    head.eval()
    mix.eval()
    n = ex["n"]
    if mode == "tfidf":
        return ex["tfidf"]
    if mode == "bm25":
        return ex["bm25"]
    if mode == "sbert":
        return ex["sbert"]
    if mode == "lead_k":
        return np.linspace(1.0, 0.0, n)
    if mode == "lexcue":
        # lightweight lexical cue baseline for supports/refutes
        cues_sup = ["is", "was", "born", "known", "writer", "actor", "directed", "authored"]
        cues_ref = ["not", "never", "false", "incorrect", "denied"]
        if ex["role"] == "supports":
            cues = cues_sup
        elif ex["role"] == "refutes":
            cues = cues_ref
        else:
            cues = cues_sup + cues_ref
        scores = np.zeros(n)
        for i, t in enumerate(ex["texts"]):
            low = t.lower()
            scores[i] = sum(1.0 for c in cues if c in low) + 0.1 * ex["sbert"][i]
        return minmax(scores)
    hs = torch.tensor(ex["hs"], device=device)
    hq = torch.tensor(ex["hq"], device=device).unsqueeze(0).expand(n, -1)
    role = torch.tensor([ex["role_id"]] * n, device=device)
    r = torch.sigmoid(head(hs, hq, role)).cpu().numpy()
    w = mix.weights().detach().cpu().numpy()
    Q, G = ex["Q"], ex["G"]
    if mode == "query_only":
        return Q
    if mode == "no_role":
        return minmax(w[0] * Q + w[2] * G)
    if mode == "no_graph":
        return minmax(w[0] * Q + w[1] * r)
    return minmax(w[0] * Q + w[1] * r + w[2] * G)


def evaluate(examples, head, mix, device, modes: list[str], k: int) -> dict:
    out = {}
    for mode in modes:
        rows = []
        for ex in examples:
            sc = predict_scores(ex, head, mix, device, mode=mode)
            order = np.argsort(-sc)
            pred = [ex["sids"][i] for i in order[:k]]
            p, r, f1 = evidence_f1(pred, ex["gold"])
            rows.append({"doc_id": ex["doc_id"], "role": ex["gold_role"], "precision": p, "recall": r, "f1": f1, "pred": pred, "gold": ex["gold"]})
        out[mode] = {
            "n": len(rows),
            "evidence_precision": float(np.mean([x["precision"] for x in rows])),
            "evidence_recall": float(np.mean([x["recall"] for x in rows])),
            "evidence_f1": float(np.mean([x["f1"] for x in rows])),
            "by_role": {
                role: float(np.mean([x["f1"] for x in rows if x["role"] == role] or [0.0]))
                for role in ("supports", "refutes")
            },
        }
    return out


def prediction_rows(examples, head, mix, device, modes: list[str], k_values: list[int]):
    """Yield auditable, per-instance predictions with candidate scores."""
    for ex in examples:
        for mode in modes:
            scores = predict_scores(ex, head, mix, device, mode=mode)
            order = np.argsort(-scores)
            for k in k_values:
                pred = [ex["sids"][i] for i in order[:k]]
                p, r, f1 = evidence_f1(pred, ex["gold"])
                yield {
                    "qid": ex["qid"],
                    "doc_id": ex["doc_id"],
                    "underlying_document_id": ex["underlying_document_id"],
                    "wikipedia_title": ex["wikipedia_title"],
                    "gold_role": ex["gold_role"],
                    "selector_role": ex["role"],
                    "mode": mode,
                    "k": k,
                    "predicted_sentence_ids": pred,
                    "gold_sentence_ids": ex["gold"],
                    "candidate_scores": {sid: float(score) for sid, score in zip(ex["sids"], scores)},
                    "precision": p,
                    "recall": r,
                    "f1": f1,
                }


def bootstrap_delta(
    examples,
    head,
    mix,
    device,
    mode_a: str,
    mode_b: str,
    *,
    k: int,
    samples: int = 2000,
    seed: int = 2026,
) -> dict:
    rng = np.random.default_rng(seed)
    by_doc = defaultdict(list)
    # Precompute per-example F1 for both modes once.
    for ex in examples:
        pa = predict_scores(ex, head, mix, device, mode_a)
        pb = predict_scores(ex, head, mix, device, mode_b)
        oa = [ex["sids"][i] for i in np.argsort(-pa)[:k]]
        ob = [ex["sids"][i] for i in np.argsort(-pb)[:k]]
        by_doc[ex["underlying_document_id"]].append(
            (evidence_f1(oa, ex["gold"])[2], evidence_f1(ob, ex["gold"])[2])
        )
    docs = list(by_doc.keys())
    deltas = []
    for _ in range(samples):
        chosen = rng.choice(docs, size=len(docs), replace=True)
        fa, fb = [], []
        for d in chosen:
            for a, b in by_doc[d]:
                fa.append(a)
                fb.append(b)
        deltas.append(float(np.mean(fa) - np.mean(fb)))
    arr = np.asarray(deltas)
    return {
        "mean": float(arr.mean()),
        "ci95": [float(np.quantile(arr, 0.025)), float(np.quantile(arr, 0.975))],
        "p_two_sided": float(min(1.0, 2 * min(np.mean(arr <= 0), np.mean(arr >= 0)))),
        "cluster_unit": "underlying_wikipedia_document",
        "cluster_count": len(docs),
    }


def document_leakage_audit(splits: dict[str, list[dict]]) -> dict:
    ids = {split: {doc["underlying_document_id"] for doc in docs} for split, docs in splits.items()}
    pairs = {}
    overlap = set()
    for left, right in (("train", "dev"), ("train", "test"), ("dev", "test")):
        shared = sorted(ids[left] & ids[right])
        pairs[f"{left}_vs_{right}"] = {"count": len(shared), "document_ids": shared}
        overlap.update(shared)
    return {
        "grouping_key": "underlying_document_id",
        "unique_documents": {split: len(values) for split, values in ids.items()},
        "pairwise_overlap": pairs,
        "overlap_document_count": len(overlap),
        "passed": not overlap,
    }


def hash_files(paths: list[Path]) -> dict:
    aggregate = hashlib.sha256()
    items = []
    for path in sorted(paths, key=lambda item: item.as_posix()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        aggregate.update(path.name.encode("utf-8"))
        aggregate.update(digest.encode("ascii"))
        items.append({"file": path.name, "sha256": digest})
    return {"sha256": aggregate.hexdigest(), "file_count": len(items), "files": items}


def git_environment() -> dict:
    def git(*args: str) -> str | None:
        try:
            return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    return {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "numpy": np.__version__,
        "git_commit": git("rev-parse", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "command": sys.argv,
        "cuda_available": torch.cuda.is_available(),
        "cwd": os.getcwd(),
    }


GENERATED_OUTPUT_FILES = (
    "checkpoint.pt",
    "leakage_audit.json",
    "predictions.jsonl",
    "provenance.json",
    "run_config.json",
    "summary.json",
)


def prepare_output_directory(out: Path, overwrite: bool = False) -> list[Path]:
    """Refuse accidental result replacement; remove only known files on request."""
    existing = [out / name for name in GENERATED_OUTPUT_FILES if (out / name).exists()]
    if existing and not overwrite:
        names = ", ".join(path.name for path in existing)
        raise FileExistsError(
            f"output contains generated artifacts ({names}); use a fresh --out path "
            "or explicitly pass --overwrite"
        )
    if overwrite:
        for path in existing:
            path.unlink()
    out.mkdir(parents=True, exist_ok=True)
    return existing


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=DEFAULT_DATA)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--encoder", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--train-limit", type=int, default=8000)
    ap.add_argument("--dev-limit", type=int, default=1500)
    ap.add_argument("--test-limit", type=int, default=1500)
    ap.add_argument("--epochs", type=int, default=4)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--architecture", choices=("original", "true_no_floor", "true_no_role"), default="original")
    ap.add_argument("--train-k", type=int, default=DEFAULT_K, help="Evidence budget used for development selection.")
    ap.add_argument(
        "--eval-k",
        default="1,3,5,10",
        help="Comma-separated evidence budgets for test sensitivity; train-k is always included.",
    )
    ap.add_argument("--bootstrap-samples", type=int, default=2000)
    ap.add_argument("--protocol", choices=tuple(PROTOCOLS), default="oracle-label")
    ap.add_argument("--predicted-labels", type=Path, help="JSON/JSONL qid-to-role predictions; required for predicted-label protocol.")
    ap.add_argument("--allow-document-overlap", action="store_true", help="Legacy reproduction only: continue despite Wikipedia-document leakage across splits.")
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Explicitly replace only the known generated artifacts in --out.",
    )
    args = ap.parse_args()
    if args.protocol == "predicted-label" and args.predicted_labels is None:
        ap.error("--predicted-labels is required for the predicted-label protocol")
    if args.protocol != "predicted-label" and args.predicted_labels is not None:
        ap.error("--predicted-labels is only valid with --protocol predicted-label")
    eval_ks = sorted({int(value.strip()) for value in args.eval_k.split(",") if value.strip()} | {args.train_k})
    if args.train_k < 1 or any(k < 1 for k in eval_ks):
        ap.error("all evidence budgets must be positive integers")
    try:
        prepare_output_directory(args.out, overwrite=args.overwrite)
    except FileExistsError as exc:
        ap.error(str(exc))

    print("loading docs...", flush=True)
    train_docs = load_docs(args.data / "train")[: args.train_limit]
    dev_docs = load_docs(args.data / "dev")[: args.dev_limit]
    test_docs = load_docs(args.data / "test")[: args.test_limit]
    print(f"docs train/dev/test = {len(train_docs)}/{len(dev_docs)}/{len(test_docs)}", flush=True)
    split_docs = {"train": train_docs, "dev": dev_docs, "test": test_docs}
    audit = document_leakage_audit(split_docs)
    (args.out / "leakage_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    if not audit["passed"] and not args.allow_document_overlap:
        raise RuntimeError(
            f"underlying Wikipedia-document leakage detected ({audit['overlap_document_count']} documents); "
            "prepare data with --split-strategy document_grouped, or use --allow-document-overlap only for explicitly labelled legacy reproduction"
        )

    predicted_labels = load_predicted_labels(args.predicted_labels)

    print(f"loading encoder {args.encoder}...", flush=True)
    encoder = SentenceTransformer(args.encoder, device=args.device)
    dim = encoder.get_sentence_embedding_dimension()
    role2id = {r: i for i, r in enumerate(ROLES)}

    print("building train examples...", flush=True)
    train_ex = build_examples(train_docs, encoder, role2id, protocol=args.protocol, predicted_labels=predicted_labels)
    print("building dev examples...", flush=True)
    dev_ex = build_examples(dev_docs, encoder, role2id, protocol=args.protocol, predicted_labels=predicted_labels)
    print("building test examples...", flush=True)
    test_ex = build_examples(test_docs, encoder, role2id, protocol=args.protocol, predicted_labels=predicted_labels)
    print(f"examples train/dev/test = {len(train_ex)}/{len(dev_ex)}/{len(test_ex)}", flush=True)

    head, mix, best = train_model(train_ex, dev_ex, dim, args.epochs, args.lr, args.device, args.seed, args.train_k, args.architecture)
    torch.save(best["state"], args.out / "checkpoint.pt")

    modes = ["full", "query_only", "no_role", "no_graph", "tfidf", "bm25", "sbert", "lead_k", "lexcue"]
    print("evaluating test...", flush=True)
    test_metrics = evaluate(test_ex, head, mix, args.device, modes, args.train_k)
    print("evaluating dev...", flush=True)
    dev_metrics = evaluate(dev_ex, head, mix, args.device, modes, args.train_k)

    comps = {}
    for baseline in ["tfidf", "bm25", "sbert", "query_only", "no_role", "lexcue"]:
        comps[f"full_vs_{baseline}"] = bootstrap_delta(
            test_ex,
            head,
            mix,
            args.device,
            "full",
            baseline,
            k=args.train_k,
            samples=args.bootstrap_samples,
            seed=args.seed,
        )

    k_sensitivity = {}
    for eval_k in eval_ks:
        metrics = evaluate(test_ex, head, mix, args.device, modes, eval_k)
        k_sensitivity[str(eval_k)] = {
            "test": metrics,
            "full_vs_bm25": bootstrap_delta(
                test_ex,
                head,
                mix,
                args.device,
                "full",
                "bm25",
                k=eval_k,
                samples=args.bootstrap_samples,
                seed=args.seed + eval_k,
            ),
            "full_vs_no_role": bootstrap_delta(
                test_ex,
                head,
                mix,
                args.device,
                "full",
                "no_role",
                k=eval_k,
                samples=args.bootstrap_samples,
                seed=args.seed + 100 + eval_k,
            ),
        }

    with (args.out / "predictions.jsonl").open("w", encoding="utf-8") as handle:
        for row in prediction_rows(test_ex, head, mix, args.device, modes, eval_ks):
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    selected_paths = {
        split: [Path(doc["_source_path"]) for doc in docs]
        for split, docs in split_docs.items()
    }
    data_hashes = {split: hash_files(paths) for split, paths in selected_paths.items()}
    run_config = {
        **vars(args),
        "data": str(args.data.resolve()),
        "out": str(args.out.resolve()),
        "predicted_labels": str(args.predicted_labels.resolve()) if args.predicted_labels else None,
        "eval_k": eval_ks,
        "protocol_definition": PROTOCOLS[args.protocol],
    }
    (args.out / "run_config.json").write_text(json.dumps(run_config, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    provenance = {"environment": git_environment(), "data_hashes": data_hashes, "leakage_audit": audit,
                  "executable_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if args.predicted_labels:
        provenance["predicted_labels_sha256"] = hashlib.sha256(args.predicted_labels.read_bytes()).hexdigest()
    (args.out / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "dataset": "fever_filtered_evidence_selection",
        "label_provenance": "human_gold",  # compatibility: evidence targets are human gold
        "evidence_target_provenance": "FEVER_human_gold_evidence",
        "selector_role_input_provenance": PROTOCOLS[args.protocol]["role_source"],
        "protocol": args.protocol,
        "protocol_definition": PROTOCOLS[args.protocol],
        "end_to_end": PROTOCOLS[args.protocol]["is_end_to_end"],
        "document_leakage_audit": audit,
        "bootstrap_cluster_unit": "underlying_wikipedia_document",
        "k": args.train_k,
        "evaluated_k": eval_ks,
        "encoder": args.encoder,
        "architecture": args.architecture,
        "train_n": len(train_ex),
        "dev_n": len(dev_ex),
        "test_n": len(test_ex),
        "best_dev_f1_during_train": best["f1"],
        "mixture_weights": mix.weights().detach().cpu().tolist(),
        "test": test_metrics,
        "dev": dev_metrics,
        "bootstrap_test": comps,
        "k_sensitivity": k_sensitivity,
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"test_full_f1": test_metrics["full"]["evidence_f1"], "weights": summary["mixture_weights"]}, indent=2))
    print(f"wrote {args.out / 'summary.json'}", flush=True)


if __name__ == "__main__":
    main()
