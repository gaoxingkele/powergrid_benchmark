#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 1 of stage 3 batch: produce fixed v2 SQL for the 3 candidates judged
semantically_correct=false in stage 2 (SB-AUTO-005, SB-AUTO-014, RTS_AUTO_047).

Rules: the original 91-item files are NOT modified. Fixes follow the adjudicator's
minimal_fix, grounded in actual schema/column domains (DISTINCT values were queried
read-only first). Each fixed SQL is validated in the read-only sandbox.
Output: runs/ma_stage2/candidate_fixes_v2.jsonl
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_annotation_pilot import (  # noqa: E402
    PILOT_DIR, MA_DBS, load_ma_items, execute_sql_sandbox, utc_now,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT = PILOT_DIR / "runs/ma_stage2/candidate_fixes_v2.jsonl"

# Fixed SQLs, derived from adjudicator minimal_fix + live DISTINCT/schema inspection:
# - SimBench generators: generator_type in {'lv_RES' (133 rows), 'Hydro_MV' (1 row)},
#   physical_type = 'RES' for all rows. "Distributed generators" := low-voltage
#   grid-connected units => generator_type = 'lv_RES' (the only non-degenerate,
#   data-grounded reading; there is no literal 'Distributed' value in the domain).
# - SimBench caveat: maximum_active_power_mw is NULL for ALL rows; kept as-is per the
#   adjudicator's minimal_fix (filter only) and the question's "maximum" wording.
# - RTS reserve_requirements_da only contains Spin_Up_R1/R2/R3, so the spinning filter
#   is result-equivalent here but semantically required by the question.
FIXES = [
    {
        "question_id": "SB-AUTO-005",
        "dataset_id": "SIMBENCH_AUTO_PILOT",
        "fixed_sql": ("SELECT COUNT(*) AS generator_count FROM generators "
                      "WHERE generator_type = 'lv_RES';"),
        "fix_rationale": ("Adjudicator minimal_fix: count only distributed generators via "
                          "generator_type/physical_type. Live DISTINCT query: generator_type in "
                          "{'lv_RES'(133), 'Hydro_MV'(1)}, physical_type='RES' for all rows (a "
                          "physical_type filter would be degenerate). 'Distributed' read as "
                          "low-voltage-connected units => generator_type='lv_RES'."),
    },
    {
        "question_id": "SB-AUTO-014",
        "dataset_id": "SIMBENCH_AUTO_PILOT",
        "fixed_sql": ("SELECT ROUND(SUM(maximum_active_power_mw), 6) AS total_generation_max_mw "
                      "FROM generators WHERE generator_type = 'lv_RES';"),
        "fix_rationale": ("Adjudicator minimal_fix: add distributed-generator filter; same "
                          "reasoning as SB-AUTO-005 (generator_type='lv_RES'). Data caveat: "
                          "maximum_active_power_mw is NULL for every row, so the SUM evaluates "
                          "to NULL; the metric column is kept per the adjudicator's fix and the "
                          "question's 'maximum' wording, and this caveat is recorded here."),
    },
    {
        "question_id": "RTS_AUTO_047",
        "dataset_id": "RTS_GMLC_AUTO_PILOT",
        "fixed_sql": ("SELECT reserve_product, ROUND(MAX(requirement_mw), 3) AS "
                      "maximum_requirement_mw FROM reserve_requirements_da "
                      "WHERE timestamp >= '2020-01-02 00:00:00' "
                      "AND timestamp < datetime('2020-01-02 00:00:00', '+1 day') "
                      "AND reserve_product LIKE 'Spin_%' "
                      "GROUP BY reserve_product ORDER BY reserve_product;"),
        "fix_rationale": ("Adjudicator minimal_fix: filter to spinning reserve products before "
                          "grouping (reserve_product like '%spin%'). Live DISTINCT query: "
                          "reserve_requirements_da holds only Spin_Up_R1/R2/R3, so the filter is "
                          "result-equivalent on this DB but semantically required by the "
                          "question ('spinning reserve')."),
    },
]


def main():
    items = {it["question_id"]: it for it in load_ma_items()}
    recs = []
    for fix in FIXES:
        qid = fix["question_id"]
        src = items[qid]
        facts = execute_sql_sandbox(MA_DBS[fix["dataset_id"]], fix["fixed_sql"])
        rec = {
            "question_id": qid,
            "dataset_id": fix["dataset_id"],
            "original_sql_sha256": hashlib.sha256(src["sql"].encode("utf-8")).hexdigest(),
            "fixed_sql": fix["fixed_sql"],
            "fix_rationale": fix["fix_rationale"],
            "executed_row_count": facts["row_count"],
            "executed_columns": facts["columns"],
            "sandbox_executable": facts["executable"],
            "sandbox_error": facts["error"],
            "created_at": utc_now(),
        }
        recs.append(rec)
        print(f"[{'ok' if facts['executable'] else 'FAIL'}] {qid}: rows={facts['row_count']} "
              f"cols={facts['columns']} err={facts['error']}")
    if not all(r["sandbox_executable"] for r in recs):
        raise SystemExit("FATAL: a fixed SQL is not executable")
    with open(OUT, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[ok] {len(recs)} fixes -> {OUT}")


if __name__ == "__main__":
    main()
