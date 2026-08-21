"""Promotion-gate audit part B: independent re-execution of all 4000 final predictions + 500 golds.

MUST run under the pinned runtime (runtime_compat/python31011/python.exe, SQLite 3.40.1)
via the runpy launcher so that `import freeze_public_baseline` resolves.
Read-only w.r.t. all frozen/ledger files; writes _reexecution.jsonl + _reexecution_summary.json.
"""
import json
import sqlite3
import sys
import time
from pathlib import Path

import freeze_public_baseline as f

P = Path(f.__file__).resolve().parent
OUT = P / "formal_runs" / "promotion_gate_20260807"
MODELS = ("qwen", "granite")

rows = {r["question_id"]: r for r in f.load_rows()}
gold_cache = {}  # question_id -> (status, rows)
gold_mismatch_qids = []

out_path = OUT / "_reexecution.jsonl"
mismatches = []
counts = {"rows": 0, "status_mismatch": 0, "ex_mismatch": 0, "gold_not_safe": 0,
          "pred_status_hist": {}}
started_all = time.perf_counter()
with out_path.open("w", encoding="utf-8", buffering=1) as out:
    for model in MODELS:
        fs_path = P / "formal_runs" / f"MA_PUBLIC_BIRD_v101_{model}" / "final_scores.jsonl"
        for line in fs_path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            qid, db_id = rec["question_id"], rec["db_id"]
            if qid not in gold_cache:
                gold_cache[qid] = f.safe_execute(rows[qid]["SQL"], f.db_path(db_id), timeout_seconds=180.0)
            gold_status, gold_rows = gold_cache[qid]
            if gold_status != "SAFE_EXECUTED":
                counts["gold_not_safe"] += 1
                gold_mismatch_qids.append({"question_id": qid, "gold_status": gold_status})
            t0 = time.perf_counter()
            pred_status, pred_rows = f.safe_execute(rec["final_sql"], f.db_path(db_id), timeout_seconds=180.0)
            elapsed = time.perf_counter() - t0
            if pred_status == "SAFE_EXECUTED" and gold_status == "SAFE_EXECUTED":
                ex = f.official_ex(pred_rows or [], gold_rows or [])
            else:
                ex = 0
            status_ok = pred_status == rec["prediction_status"]
            ex_ok = ex == rec["official_ex"]
            counts["rows"] += 1
            counts["pred_status_hist"][pred_status] = counts["pred_status_hist"].get(pred_status, 0) + 1
            if not status_ok:
                counts["status_mismatch"] += 1
            if not ex_ok:
                counts["ex_mismatch"] += 1
            if not (status_ok and ex_ok):
                mismatches.append({
                    "model": model, "question_id": qid, "db_id": db_id, "method": rec["method"],
                    "ledger_status": rec["prediction_status"], "reexec_status": pred_status,
                    "ledger_ex": rec["official_ex"], "reexec_ex": ex,
                })
            out.write(json.dumps({
                "model": model, "question_id": qid, "db_id": db_id, "method": rec["method"],
                "ledger_status": rec["prediction_status"], "reexec_status": pred_status,
                "ledger_ex": rec["official_ex"], "reexec_ex": ex,
                "gold_status": gold_status, "elapsed_seconds": elapsed,
            }, ensure_ascii=False, sort_keys=True) + "\n")

summary = {
    "python_version": sys.version,
    "sqlite_version": sqlite3.sqlite_version,
    "counts": counts,
    "gold_cache_size": len(gold_cache),
    "gold_status_hist": {s: sum(1 for v in gold_cache.values() if v[0] == s) for s in {v[0] for v in gold_cache.values()}},
    "gold_not_safe": gold_mismatch_qids,
    "mismatches": mismatches,
    "wall_seconds": time.perf_counter() - started_all,
}
(OUT / "_reexecution_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"rows": counts["rows"], "status_mismatch": counts["status_mismatch"],
                  "ex_mismatch": counts["ex_mismatch"], "gold_not_safe": counts["gold_not_safe"],
                  "sqlite": sqlite3.sqlite_version, "wall_seconds": summary["wall_seconds"]}))
