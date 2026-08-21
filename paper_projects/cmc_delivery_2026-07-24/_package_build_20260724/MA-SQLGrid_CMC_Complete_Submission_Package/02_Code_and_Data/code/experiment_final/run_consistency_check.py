#!/usr/bin/env python3
"""Temperature-0 repeat-consistency check for MA-SQLGrid (P0-6).

Re-issues the archived formal-run prompts for the selected conditions three
times each at temperature 0 against the original (or any OpenAI-compatible)
endpoint, then reports per-condition agreement:

  * exact-SQL agreement: fraction of questions where all repeats return the
    same extracted SQL string;
  * denotation agreement: fraction where all repeats produce the same
    evaluator verdict (correct/incorrect with the same denotation);
  * per-repeat execution accuracy.

For C5 the full generate -> rank -> repair pipeline is repeated each time,
so the number quantifies end-to-end pipeline stability, not just raw
decoding stability.

Usage (original endpoint):
  python run_consistency_check.py \
      --model gpt-5.4-mini-2026-03-17 \
      --base-url https://api.krill-ai.com/v1 \
      --api-key-env KRILL_API_KEY \
      [--conditions C4,C5] [--repeats 3] [--max-questions N]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

EXPERIMENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXPERIMENT_DIR))
sys.path.insert(0, str(EXPERIMENT_DIR.parent / "evaluator"))

from evaluator import load_questions, score_prediction  # noqa: E402
from run_second_model import (  # noqa: E402
    CONDITION_MAP,
    DATA_DIR,
    ChatClient,
    load_archived_prompts,
    load_domain_contexts,
    run_condition,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--api-key-env", default="KRILL_API_KEY")
    parser.add_argument("--provider", default="consistency-check")
    parser.add_argument("--conditions", default="C4,C5")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--max-questions", type=int, default=0)
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()

    api_key = os.environ.get(args.api_key_env, "")
    if not api_key:
        raise SystemExit(f"environment variable {args.api_key_env} is not set")

    conditions = [CONDITION_MAP[c.strip().upper()] for c in args.conditions.split(",")]
    model_slug = re.sub(r"[^A-Za-z0-9._-]+", "-", args.model)
    out_dir = Path(args.output_dir) if args.output_dir else EXPERIMENT_DIR / f"outputs_consistency_{model_slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    questions = {q["question_id"]: q for q in load_questions(DATA_DIR / "questions.jsonl")}
    domain_ctx = load_domain_contexts()
    client = ChatClient(args.base_url, api_key, args.model)
    conn = sqlite3.connect(DATA_DIR / "database.sqlite")

    report: dict[str, Any] = {"model": args.model, "repeats": args.repeats, "temperature": 0, "conditions": {}}
    try:
        for condition in conditions:
            prompts = load_archived_prompts(condition)
            if args.max_questions:
                prompts = {qid: prompts[qid] for qid in sorted(prompts)[: args.max_questions]}
            per_repeat: list[dict[str, dict[str, Any]]] = []
            for repeat in range(args.repeats):
                trace_dir = out_dir / f"traces_repeat{repeat}"
                trace_dir.mkdir(parents=True, exist_ok=True)
                print(f"{condition} repeat {repeat + 1}/{args.repeats} on {len(prompts)} questions")
                preds = run_condition(client, conn, condition, questions, prompts, domain_ctx, trace_dir, args.provider)
                by_qid = {}
                for p in preds:
                    verdict = score_prediction(conn, questions[p["question_id"]], p["predicted_sql"])
                    by_qid[p["question_id"]] = {
                        "sql": p["predicted_sql"].strip(),
                        "correct": verdict.correct,
                        "error_type": verdict.error_type,
                    }
                per_repeat.append(by_qid)
                with (out_dir / f"predictions_{condition}_repeat{repeat}.jsonl").open("w", encoding="utf-8") as fh:
                    for p in preds:
                        fh.write(json.dumps(p, sort_keys=True) + "\n")

            qids = sorted(prompts)
            exact_sql_agree = sum(1 for q in qids if len({r[q]["sql"] for r in per_repeat}) == 1)
            verdict_agree = sum(1 for q in qids if len({r[q]["correct"] for r in per_repeat}) == 1)
            accs = [sum(1 for q in qids if r[q]["correct"]) / len(qids) for r in per_repeat]
            report["conditions"][condition] = {
                "n_questions": len(qids),
                "exact_sql_agreement": round(exact_sql_agree / len(qids), 4),
                "verdict_agreement": round(verdict_agree / len(qids), 4),
                "per_repeat_execution_accuracy": [round(a, 4) for a in accs],
                "disagreeing_question_ids": [q for q in qids if len({r[q]["sql"] for r in per_repeat}) != 1],
            }
            print(json.dumps(report["conditions"][condition], indent=2))
    finally:
        conn.close()

    (out_dir / "consistency_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: wrote {out_dir / 'consistency_report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
