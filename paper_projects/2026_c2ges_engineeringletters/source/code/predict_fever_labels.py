#!/usr/bin/env python3
"""Leakage-controlled upstream FEVER label predictor for C2GES.

The selector's train instances receive out-of-fold (OOF) role predictions.  The
folds are grouped by the original Wikipedia document, so neither the same claim
nor another claim from the same page can train its own role predictor.  Dev and
test predictions come from one model fitted exclusively on the complete train
split.  Gold roles are used only as training targets and for post-hoc metrics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import FeatureUnion, Pipeline


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "workspace/fever_benchmark_document_grouped"
DEFAULT_OUT = ROOT / "workspace/fever_label_predictions/tfidf_logreg"
VALID_ROLES = ("supports", "refutes")


def role_from_question(question: dict) -> str:
    role = str(question.get("role") or "").lower()
    if role not in VALID_ROLES:
        raise ValueError(f"unsupported FEVER role {role!r}")
    return role


def load_instances(split_dir: Path, limit: int | None = None) -> list[dict]:
    rows = []
    for path in sorted(split_dir.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        group = doc.get("underlying_document_id") or doc.get("document_id") or doc.get("wikipedia_title") or doc.get("title")
        if not group:
            raise ValueError(f"missing underlying document identifier: {path}")
        for question in doc.get("causal_questions", []):
            qid = str(question.get("qid") or "")
            claim = str(question.get("question") or "").strip()
            if not qid or not claim:
                continue
            rows.append(
                {
                    "qid": qid,
                    "claim": claim,
                    "gold_role": role_from_question(question),
                    "underlying_document_id": str(group),
                    "source_file": str(path.resolve()),
                }
            )
            if limit is not None and len(rows) >= limit:
                return rows
    return rows


def document_leakage_audit(splits: dict[str, list[dict]]) -> dict:
    groups = {split: {row["underlying_document_id"] for row in rows} for split, rows in splits.items()}
    pairwise = {}
    all_shared = set()
    for left, right in (("train", "dev"), ("train", "test"), ("dev", "test")):
        shared = sorted(groups[left] & groups[right])
        pairwise[f"{left}_vs_{right}"] = {"count": len(shared), "document_ids": shared}
        all_shared.update(shared)
    return {
        "grouping_key": "underlying_document_id",
        "unique_documents": {split: len(value) for split, value in groups.items()},
        "pairwise_overlap": pairwise,
        "overlap_document_count": len(all_shared),
        "passed": not all_shared,
    }


def make_pipeline(seed: int, max_features: int, min_df: int, c_value: float) -> Pipeline:
    features = FeatureUnion(
        [
            (
                "word",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=min_df,
                    max_features=max_features,
                    sublinear_tf=True,
                    strip_accents="unicode",
                ),
            ),
            (
                "char",
                TfidfVectorizer(
                    analyzer="char_wb",
                    lowercase=True,
                    ngram_range=(3, 5),
                    min_df=min_df,
                    max_features=max_features,
                    sublinear_tf=True,
                ),
            ),
        ]
    )
    classifier = LogisticRegression(
        C=c_value,
        class_weight="balanced",
        max_iter=1000,
        random_state=seed,
        solver="liblinear",
    )
    return Pipeline([("features", features), ("classifier", classifier)])


def predict_with_probabilities(model: Pipeline, texts: list[str]) -> tuple[np.ndarray, np.ndarray]:
    labels = model.predict(texts)
    raw_prob = model.predict_proba(texts)
    classes = list(model.named_steps["classifier"].classes_)
    probs = np.column_stack([raw_prob[:, classes.index(role)] for role in VALID_ROLES])
    return labels, probs


def out_of_fold_train_predictions(
    train: list[dict], *, seed: int, folds: int, max_features: int, min_df: int, c_value: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    texts = np.asarray([row["claim"] for row in train], dtype=object)
    labels = np.asarray([row["gold_role"] for row in train])
    groups = np.asarray([row["underlying_document_id"] for row in train])
    unique_groups = np.unique(groups)
    if len(unique_groups) < folds:
        raise ValueError(f"OOF requires at least {folds} unique train documents; found {len(unique_groups)}")
    predictions = np.empty(len(train), dtype=object)
    probabilities = np.zeros((len(train), len(VALID_ROLES)), dtype=np.float64)
    fold_ids = np.full(len(train), -1, dtype=np.int64)
    splitter = StratifiedGroupKFold(n_splits=folds, shuffle=True, random_state=seed)
    for fold, (fit_idx, holdout_idx) in enumerate(splitter.split(texts, labels, groups)):
        fit_groups = set(groups[fit_idx])
        holdout_groups = set(groups[holdout_idx])
        if fit_groups & holdout_groups:
            raise RuntimeError("group leakage inside OOF label-predictor fold")
        model = make_pipeline(seed + fold, max_features, min_df, c_value)
        model.fit(texts[fit_idx].tolist(), labels[fit_idx].tolist())
        fold_pred, fold_prob = predict_with_probabilities(model, texts[holdout_idx].tolist())
        predictions[holdout_idx] = fold_pred
        probabilities[holdout_idx] = fold_prob
        fold_ids[holdout_idx] = fold
    if np.any(fold_ids < 0) or any(value is None for value in predictions):
        raise RuntimeError("OOF predictions are incomplete")
    return predictions.astype(str), probabilities, fold_ids


def metrics(gold: list[str], predicted: list[str]) -> dict:
    return {
        "n": len(gold),
        "accuracy": float(accuracy_score(gold, predicted)),
        "balanced_accuracy": float(balanced_accuracy_score(gold, predicted)),
        "macro_f1": float(f1_score(gold, predicted, labels=list(VALID_ROLES), average="macro")),
        "confusion_matrix": {
            "labels": list(VALID_ROLES),
            "values": confusion_matrix(gold, predicted, labels=list(VALID_ROLES)).tolist(),
        },
    }


def data_hash(rows: list[dict]) -> dict:
    files = sorted({Path(row["source_file"]) for row in rows}, key=lambda path: path.as_posix())
    digest = hashlib.sha256()
    for path in files:
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        digest.update(path.name.encode("utf-8"))
        digest.update(file_hash.encode("ascii"))
    return {"sha256": digest.hexdigest(), "file_count": len(files), "instance_count": len(rows)}


def git_value(*args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--max-features", type=int, default=30000, help="Maximum features for each of the word and character channels.")
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--c", type=float, default=1.0)
    parser.add_argument("--train-limit", type=int)
    parser.add_argument("--dev-limit", type=int)
    parser.add_argument("--test-limit", type=int)
    args = parser.parse_args()
    if args.folds < 2 or args.min_df < 1 or args.max_features < 1 or args.c <= 0:
        parser.error("folds>=2, min-df>=1, max-features>=1, and C>0 are required")
    if args.out.exists() and any(args.out.iterdir()):
        parser.error(f"refusing to overwrite non-empty output directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    limits = {"train": args.train_limit, "dev": args.dev_limit, "test": args.test_limit}
    splits = {split: load_instances(args.data / split, limits[split]) for split in ("train", "dev", "test")}
    if any(not rows for rows in splits.values()):
        raise ValueError("train/dev/test must each contain at least one valid instance")
    audit = document_leakage_audit(splits)
    if not audit["passed"]:
        raise RuntimeError(f"document-disjoint gate failed: {audit['overlap_document_count']} shared Wikipedia pages")

    train_pred, train_prob, fold_ids = out_of_fold_train_predictions(
        splits["train"],
        seed=args.seed,
        folds=args.folds,
        max_features=args.max_features,
        min_df=args.min_df,
        c_value=args.c,
    )
    full_model = make_pipeline(args.seed, args.max_features, args.min_df, args.c)
    full_model.fit(
        [row["claim"] for row in splits["train"]],
        [row["gold_role"] for row in splits["train"]],
    )

    split_outputs = {}
    all_rows = []
    for split in ("train", "dev", "test"):
        rows = splits[split]
        if split == "train":
            predicted, probabilities = train_pred, train_prob
            sources = [f"train_oof_group_fold_{fold}" for fold in fold_ids]
        else:
            predicted, probabilities = predict_with_probabilities(full_model, [row["claim"] for row in rows])
            sources = ["full_train_only_model"] * len(rows)
        output_rows = []
        for row, pred, prob, source in zip(rows, predicted, probabilities, sources):
            output_rows.append(
                {
                    "qid": row["qid"],
                    "split": split,
                    "underlying_document_id": row["underlying_document_id"],
                    "predicted_role": str(pred),
                    "probabilities": {role: float(value) for role, value in zip(VALID_ROLES, prob)},
                    "prediction_source": source,
                    "gold_role_for_audit_only": row["gold_role"],
                }
            )
        split_outputs[split] = output_rows
        all_rows.extend(output_rows)

    qids = [row["qid"] for row in all_rows]
    if len(qids) != len(set(qids)):
        raise RuntimeError("qid collision across splits")
    label_map = {row["qid"]: row["predicted_role"] for row in all_rows}
    (args.out / "predicted_labels.json").write_text(json.dumps(label_map, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.out / "predictions.jsonl").open("w", encoding="utf-8") as handle:
        for row in all_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    for split, rows in split_outputs.items():
        (args.out / f"predicted_labels_{split}.json").write_text(
            json.dumps({row["qid"]: row["predicted_role"] for row in rows}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    metric_output = {
        split: metrics(
            [row["gold_role"] for row in splits[split]],
            [row["predicted_role"] for row in split_outputs[split]],
        )
        for split in ("train", "dev", "test")
    }
    metric_output["train_prediction_protocol"] = "StratifiedGroupKFold OOF by underlying_document_id"
    metric_output["dev_test_prediction_protocol"] = "single model fitted only on complete train split"
    (args.out / "metrics.json").write_text(json.dumps(metric_output, ensure_ascii=False, indent=2), encoding="utf-8")
    joblib.dump(full_model, args.out / "full_train_model.joblib")

    config = {key: str(value.resolve()) if isinstance(value, Path) else value for key, value in vars(args).items()}
    provenance = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "configuration": config,
        "no_gold_leakage_contract": {
            "features": "claim text only",
            "train_predictions": "out-of-fold; folds grouped by underlying Wikipedia document",
            "dev_test_predictions": "model fitted only on train",
            "gold_role_in_predictions_file": "audit/evaluation only; never supplied as a model feature",
        },
        "document_leakage_audit": audit,
        "data_hashes": {split: data_hash(rows) for split, rows in splits.items()},
        "output_predicted_labels_sha256": hashlib.sha256((args.out / "predicted_labels.json").read_bytes()).hexdigest(),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "sklearn": sklearn.__version__,
            "numpy": np.__version__,
            "git_commit": git_value("rev-parse", "HEAD"),
            "git_dirty": bool(git_value("status", "--porcelain")),
            "command": sys.argv,
            "cwd": os.getcwd(),
        },
    }
    (args.out / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"counts": {split: len(rows) for split, rows in splits.items()}, "metrics": metric_output, "audit": audit}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
