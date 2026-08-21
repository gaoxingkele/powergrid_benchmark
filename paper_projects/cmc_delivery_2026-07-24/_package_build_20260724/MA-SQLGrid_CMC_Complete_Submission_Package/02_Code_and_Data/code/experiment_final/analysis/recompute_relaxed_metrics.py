#!/usr/bin/env python3
"""Recompute strict and relaxed (order-insensitive) execution metrics.

Reads the archived formal-run predictions (outputs/predictions.jsonl) and the
frozen dataset (data/griddb_maintenance_v2_v0_1) and recomputes, for each of
the five conditions:

  1. strict      -- the paper's primary metric (evaluator contract: exact
                    column count, row order enforced when order_sensitive).
  2. set_exact   -- order-insensitive rows (multiset comparison), exact
                    projection width still required.
  3. set_relaxed -- order-insensitive rows AND projection-tolerant: the
                    prediction counts as correct if any permutation of a
                    subset of its projected columns reproduces the gold
                    denotation as a multiset.

No model calls are made; everything is recomputed from archived artifacts.
"""

from __future__ import annotations

import itertools
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENT_DIR = HERE.parent
SOURCE_DIR = EXPERIMENT_DIR.parents[1]
DATA_DIR = SOURCE_DIR / "data" / "griddb_maintenance_v2_v0_1"
OUT_DIR = EXPERIMENT_DIR / "outputs"

sys.path.insert(0, str(EXPERIMENT_DIR.parent / "evaluator"))
from evaluator import execute_sql, load_questions, normalize_row, score_prediction  # noqa: E402

CONDITIONS = [
    "C1_SchemaOnly_Direct",
    "C2_FullSchemaValues_Direct",
    "C3_CHESSLite_Generic",
    "C4_MASQLGrid_DomainContext",
    "C5_MASQLGrid_DomainContext_Validated",
]

FLOAT_TOL = 1e-6
MAX_PRED_COLUMNS = 10  # permutation guard


def multiset(rows, col_indices=None):
    normed = []
    for row in rows:
        if col_indices is not None:
            row = tuple(row[i] for i in col_indices)
        normed.append(normalize_row(row, float_abs_tol=FLOAT_TOL))
    return Counter(normed)


def set_exact_correct(pred, gold, expected_cols: int) -> bool:
    if not pred.ok or not gold.ok:
        return False
    if len(pred.columns) != expected_cols or len(gold.columns) != expected_cols:
        return False
    return multiset(pred.rows) == multiset(gold.rows)


def set_relaxed_correct(pred, gold, expected_cols: int) -> bool:
    if not pred.ok or not gold.ok:
        return False
    n = len(pred.columns)
    k = len(gold.columns)
    if n < k or n > MAX_PRED_COLUMNS:
        return False
    gold_ms = multiset(gold.rows)
    for combo in itertools.permutations(range(n), k):
        if multiset(pred.rows, combo) == gold_ms:
            return True
    return False


def main() -> None:
    questions = {q["question_id"]: q for q in load_questions(DATA_DIR / "questions.jsonl")}
    preds = [json.loads(line) for line in (OUT_DIR / "predictions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    conn = sqlite3.connect(DATA_DIR / "database.sqlite")

    tallies = {c: {"n": 0, "strict": 0, "set_exact": 0, "set_relaxed": 0} for c in CONDITIONS}
    flips = {c: [] for c in CONDITIONS}  # strict-wrong but relaxed-right question ids

    try:
        for p in preds:
            cond = p["condition"]
            record = questions[p["question_id"]]
            sql = p["predicted_sql"]
            strict = score_prediction(conn, record, sql).correct
            gold = execute_sql(conn, record["gold_sql"])
            pred = execute_sql(conn, sql)
            expected = int(record["answer_shape"]["column_count"])
            se = strict or set_exact_correct(pred, gold, expected)
            sr = se or set_relaxed_correct(pred, gold, expected)
            t = tallies[cond]
            t["n"] += 1
            t["strict"] += int(strict)
            t["set_exact"] += int(se)
            t["set_relaxed"] += int(sr)
            if sr and not strict:
                flips[cond].append(p["question_id"])
    finally:
        conn.close()

    result = {"metric_definitions": {
        "strict": "paper primary metric: evaluator contract (exact column count; row order enforced when order_sensitive)",
        "set_exact": "order-insensitive rows (multiset), exact projection width",
        "set_relaxed": "order-insensitive rows and projection-tolerant (any column permutation/subset of width gold_k)",
    }, "conditions": {}}
    print(f"{'condition':<42} {'n':>4} {'strict':>8} {'set_exact':>10} {'set_relaxed':>12}")
    for cond in CONDITIONS:
        t = tallies[cond]
        row = {
            "n": t["n"],
            "strict_correct": t["strict"],
            "strict_acc": round(t["strict"] / t["n"], 4),
            "set_exact_correct": t["set_exact"],
            "set_exact_acc": round(t["set_exact"] / t["n"], 4),
            "set_relaxed_correct": t["set_relaxed"],
            "set_relaxed_acc": round(t["set_relaxed"] / t["n"], 4),
            "relaxed_only_question_ids": flips[cond],
        }
        result["conditions"][cond] = row
        print(f"{cond:<42} {t['n']:>4} {t['strict']/t['n']:>8.4f} {t['set_exact']/t['n']:>10.4f} {t['set_relaxed']/t['n']:>12.4f}")

    out = HERE / "relaxed_metrics.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
