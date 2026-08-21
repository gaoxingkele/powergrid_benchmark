#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 2 of stage 3 batch: deterministic column-check layer over the 121 stage-2 items
(91 originals + 30 negative controls), compensating the annotators' wrong_column
blind spot (detection 0.30).

For each item: execute the candidate SQL read-only, take the result column names,
and compare (ordered) against the expected columns:
  - RTS: answer_shape.columns from questions_auto_candidate.jsonl
  - SimBench: result columns of the item's gold_sql executed in the same sandbox
Negative controls inherit the expected columns of their source question.

Output: runs/ma_stage2/column_check_report.json
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_annotation_pilot import (  # noqa: E402
    PILOT_DIR, MA_DBS, MA_RTS_QUESTIONS, MA_SB_QUESTIONS, utc_now,
)
from generate_negative_controls import exec_rows  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT_DIR = PILOT_DIR / "runs/ma_stage2"


def load_expected_columns():
    """question_id -> expected ordered result columns."""
    expected = {}
    for line in open(MA_RTS_QUESTIONS, encoding="utf-8"):
        r = json.loads(line)
        cols = (r.get("answer_shape") or {}).get("columns")
        if cols:
            expected[r["question_id"]] = list(cols)
    with open(MA_SB_QUESTIONS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ok, rows, cols, err = exec_rows(MA_DBS["SIMBENCH_AUTO_PILOT"], r["gold_sql"])
            expected[r["question_id"]] = cols if ok else None
    return expected


def load_expected_columns():
    """question_id -> expected ordered result columns."""
    expected = {}
    for line in open(MA_RTS_QUESTIONS, encoding="utf-8"):
        r = json.loads(line)
        cols = (r.get("answer_shape") or {}).get("columns")
        if cols:
            expected[r["question_id"]] = list(cols)
    with open(MA_SB_QUESTIONS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ok, rows, cols, err = exec_rows(MA_DBS["SIMBENCH_AUTO_PILOT"], r["gold_sql"])
            expected[r["question_id"]] = cols if ok else None
    return expected


def load_expected_columns_stage3():
    """Sealed items carry answer_shape.columns registered from actual execution."""
    expected = {}
    pkt = PILOT_DIR / "runs/ma_stage3/sealed_questions.jsonl"
    for line in pkt.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        expected[r["question_id"]] = list(r["answer_shape"]["columns"])
    return expected


def main():
    stage3 = "--stage3" in sys.argv
    out_dir = PILOT_DIR / ("runs/ma_stage3" if stage3 else "runs/ma_stage2")
    manifest = json.loads((out_dir / "sample_manifest.json").read_text(encoding="utf-8"))
    expected = load_expected_columns_stage3() if stage3 else load_expected_columns()
    items = manifest["items"]  # blind_id, source_id, sql, dataset_id, is_control, neg_family
    per_item, missing_expected = [], []
    for it in items:
        exp = expected.get(it["source_id"])
        if exp is None:
            missing_expected.append(it["source_id"])
        ok, rows, cols, err = exec_rows(MA_DBS[it["dataset_id"]], it["sql"])
        match = (ok and exp is not None and list(cols) == list(exp))
        per_item.append({
            "question_id": it["blind_id"], "source_id": it["source_id"],
            "dataset_id": it["dataset_id"], "is_control": it["is_control"],
            "neg_family": it.get("neg_family"),
            "expected_cols": exp, "actual_cols": cols if ok else None,
            "executable": ok, "exec_error": err, "match": match,
        })

    originals = [p for p in per_item if not p["is_control"]]
    controls = [p for p in per_item if p["is_control"]]
    orig_mismatch = [p for p in originals if not p["match"]]
    per_family = {}
    for p in controls:
        d = per_family.setdefault(p["neg_family"], {"n": 0, "caught": 0})
        d["n"] += 1
        d["caught"] += 0 if p["match"] else 1
    for d in per_family.values():
        d["capture_rate"] = round(d["caught"] / d["n"], 4)
    caught_total = sum(1 for p in controls if not p["match"])

    report = {
        "created_at": utc_now(),
        "stage": "ma_stage3_sealed" if stage3 else "ma_stage2",
        "rule": ("ordered result-column equality: candidate SQL result columns vs expected "
                 "(sealed: answer_shape.columns registered from actual execution). "
                 "Controls inherit expected columns of their source question."
                 if stage3 else
                 "ordered result-column equality: candidate SQL result columns vs expected "
                 "(RTS: answer_shape.columns; SimBench: gold_sql sandbox result columns). "
                 "Controls inherit expected columns of their source question."),
        "n_items": len(per_item),
        "missing_expected_columns_for": sorted(set(missing_expected)),
        "originals": {"n": len(originals), "mismatch": len(orig_mismatch),
                      "mismatch_items": [
                          {"question_id": p["question_id"], "source_id": p["source_id"],
                           "expected_cols": p["expected_cols"], "actual_cols": p["actual_cols"],
                           "executable": p["executable"], "exec_error": p["exec_error"]}
                          for p in orig_mismatch]},
        "controls": {"n": len(controls), "caught": caught_total,
                     "capture_rate": round(caught_total / len(controls), 4),
                     "per_family": per_family},
        "items": per_item,
    }
    with open(out_dir / "column_check_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"[ok] originals mismatch: {len(orig_mismatch)}/{len(originals)}")
    for p in orig_mismatch:
        print("  ", p["source_id"], "exp", p["expected_cols"], "got", p["actual_cols"],
              "exec", p["executable"], p["exec_error"])
    print(f"[ok] controls caught: {caught_total}/{len(controls)} "
          f"({report['controls']['capture_rate']})")
    print("[ok] per family:", json.dumps(per_family, ensure_ascii=False))
    print(f"[ok] -> {out_dir / 'column_check_report.json'}")


if __name__ == "__main__":
    main()
