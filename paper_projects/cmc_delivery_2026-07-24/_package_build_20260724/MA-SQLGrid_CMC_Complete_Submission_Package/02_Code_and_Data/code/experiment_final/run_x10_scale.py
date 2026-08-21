#!/usr/bin/env python3
"""x10 scaled-database scale-robustness experiment (second generator).

Runs C2 / C4 / C5 on the 180 held-out test questions against the x10
expanded database (data/griddb_maintenance_v2_x10: 10x rows plus two
distractor tables) using the ORIGINAL context builders from the received
dev_chess_style_pilot module and the prompt templates from main.py (the
archived formal-run driver). The original gpt-5.4-mini/krill endpoint is
unavailable; this experiment therefore runs on deepseek-chat, the paper's
validated second generator, and is framed as scale robustness on the second
generator.

Fidelity notes
--------------
* Contexts/prompts are REBUILT with the received builders
  (chess.render_full_schema_values, chess.infer_domain_context,
  chess.render_selected_context) pointed at the x10 SQLite file via path
  overrides only; no builder code is modified.
* C5 uses the ORIGINAL chess.rank_candidates / chess.reference_free_validation
  and mirrors main.py's candidate/repair flow (including passing the selected
  rank-trace entry to the repair prompt, as main.py does).
* The HTTP client reuses run_second_model.ChatClient (temperature 0,
  max_tokens 700, 4 call attempts).
* No gold information is used at prediction time; scoring runs afterwards
  with the packaged evaluator against the x10 database.

Usage:
  set DEEPSEEK_API_KEY in the process environment (never written to disk),
  then:  python run_x10_scale.py [--max-questions N] [--workers K]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

EXPERIMENT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = EXPERIMENT_DIR.parents[1]
X10_DIR = SOURCE_DIR / "data" / "griddb_maintenance_v2_x10"

import main  # noqa: E402  (sets sys.path; provides formal prompt templates)
import dev_chess_style_pilot as chess  # noqa: E402
import minimal_text2sql_smoke as smoke  # noqa: E402
import run_second_model as rsm  # noqa: E402
from evaluator import load_questions, validate_dataset  # noqa: E402

CONDITIONS = [
    "C2_FullSchemaValues_Direct",
    "C4_MASQLGrid_DomainContext",
    "C5_MASQLGrid_DomainContext_Validated",
]
CONTRACT_VERSION = "griddb-maintenance-v2-x10/no-gold-v1"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def point_builders_at_x10() -> None:
    """Redirect the received modules' dataset constants to the x10 copy."""
    smoke.DATA_DIR = X10_DIR
    smoke.DB_PATH = X10_DIR / "database.sqlite"
    smoke.SCHEMA_PATH = X10_DIR / "schema.sql"
    smoke.QUESTIONS_PATH = X10_DIR / "questions.jsonl"


def prediction_record(
    *,
    qid: str,
    condition: str,
    model: str,
    prompt: str,
    context_text: str,
    predicted_sql: str,
    candidates: list[str],
    selected_idx: int,
    trace_path: Path,
    latency_ms: int,
    token_input: int,
    token_output: int,
    retry_count: int,
    error: str | None,
) -> dict[str, Any]:
    return {
        "question_id": qid,
        "condition": condition,
        "seed": 0,
        "model": model,
        "provider": "deepseek",
        "prompt_hash": sha256_text(prompt),
        "schema_context_hash": sha256_text(context_text),
        "input_contract_version": CONTRACT_VERSION,
        "predicted_sql": predicted_sql,
        "candidate_sql": candidates,
        "selected_candidate_index": selected_idx,
        "intermediate_trace_path": str(trace_path),
        "latency_ms": latency_ms,
        "token_input": token_input,
        "token_output": token_output,
        "retry_count": retry_count,
        "error": error,
        "prompt_token_estimate": chess.estimate_tokens(prompt),
    }


def run_direct(
    client: rsm.ChatClient,
    record: dict[str, Any],
    condition: str,
    context_text: str,
    trace_dir: Path,
) -> dict[str, Any]:
    prompt = main.direct_prompt(record, context_text, condition)
    raw = ""
    model = client.model
    latency_ms = token_input = token_output = retry_count = 0
    error: str | None = None
    sql = "SELECT 1;"
    try:
        raw, model, latency_ms, token_input, token_output, retry_count = client.chat_with_retries(prompt)
        sql = smoke.extract_sql(raw)
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"
    if not sql.strip():
        sql = "SELECT 1;"
        error = error or "empty SQL extracted"
    trace_path = trace_dir / f"{record['question_id']}_seed0_{condition}.json"
    trace_path.write_text(json.dumps({"prompt": prompt, "raw_response": raw}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return prediction_record(
        qid=record["question_id"],
        condition=condition,
        model=model,
        prompt=prompt,
        context_text=context_text,
        predicted_sql=sql,
        candidates=[sql],
        selected_idx=0,
        trace_path=trace_path,
        latency_ms=latency_ms,
        token_input=token_input,
        token_output=token_output,
        retry_count=retry_count,
        error=error,
    )


def run_validated(
    client: rsm.ChatClient,
    conn: sqlite3.Connection,
    record: dict[str, Any],
    context: dict[str, Any],
    context_text: str,
    trace_dir: Path,
) -> dict[str, Any]:
    condition = "C5_MASQLGrid_DomainContext_Validated"
    prompt = main.candidate_prompt(record, context_text, condition)
    raw = ""
    repair_raw = ""
    repaired_sql = ""
    model = client.model
    latency_ms = token_input = token_output = retry_count = 0
    error: str | None = None
    candidates = ["SELECT 1;"]
    try:
        raw, model, latency_ms, token_input, token_output, retry_count = client.chat_with_retries(prompt)
        candidates = smoke.extract_candidate_sql(raw)[: int(main.HYPERPARAMETERS["c5_candidate_limit"])]
        if not candidates:
            candidates = ["SELECT 1;"]
            error = "no SQL candidate extracted"
    except Exception as exc:  # noqa: BLE001
        error = f"{type(exc).__name__}: {exc}"
    selected_idx, rank_trace = chess.rank_candidates(conn, context, candidates)
    predicted_sql = candidates[selected_idx]
    validation = rank_trace[selected_idx] if rank_trace else chess.reference_free_validation(conn, context, predicted_sql)
    if not error and int(main.HYPERPARAMETERS["repair_attempts"]) > 0:
        needs_repair = (
            not validation["exec_ok"]
            or not validation["shape_ok"]
            or not validation["order_ok"]
            or bool(validation["missing_value_hints"])
        )
        if needs_repair:
            try:
                prompt2 = main.repair_prompt(record, context_text, predicted_sql, validation)
                repair_raw, model2, lat2, in2, out2, retr2 = client.chat_with_retries(prompt2)
                repaired_sql = smoke.extract_sql(repair_raw)
                repaired_validation = chess.reference_free_validation(conn, context, repaired_sql)
                if repaired_validation["exec_ok"] and (
                    not validation["exec_ok"]
                    or int(repaired_validation["shape_ok"]) >= int(validation["shape_ok"])
                    or repaired_validation["value_hits"] >= validation["value_hits"]
                ):
                    candidates.append(repaired_sql)
                    selected_idx = len(candidates) - 1
                    predicted_sql = repaired_sql
                    rank_trace.append({"candidate_index": selected_idx, "sql": repaired_sql, "ranker_score": None, **repaired_validation})
                latency_ms += lat2
                token_input += in2
                token_output += out2
                retry_count += retr2
                model = model2
            except Exception as exc:  # noqa: BLE001
                error = f"repair {type(exc).__name__}: {exc}"
    if not predicted_sql.strip():
        predicted_sql = "SELECT 1;"
        error = error or "empty SQL extracted"
    trace_path = trace_dir / f"{record['question_id']}_seed0_{condition}.json"
    trace_path.write_text(
        json.dumps(
            {
                "prompt": prompt,
                "raw_response": raw,
                "rank_trace": rank_trace,
                "repair_raw_response": repair_raw,
                "repaired_sql": repaired_sql,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return prediction_record(
        qid=record["question_id"],
        condition=condition,
        model=model,
        prompt=prompt,
        context_text=context_text,
        predicted_sql=predicted_sql,
        candidates=candidates,
        selected_idx=selected_idx,
        trace_path=trace_path,
        latency_ms=latency_ms,
        token_input=token_input,
        token_output=token_output,
        retry_count=retry_count,
        error=error,
    )


def run_question_bundle(
    client: rsm.ChatClient,
    record: dict[str, Any],
    c2_context: str,
    domain: dict[str, Any],
    domain_text: str,
    trace_dir: Path,
) -> list[dict[str, Any]]:
    conn = sqlite3.connect(X10_DIR / "database.sqlite")
    try:
        return [
            run_direct(client, record, "C2_FullSchemaValues_Direct", c2_context, trace_dir),
            run_direct(client, record, "C4_MASQLGrid_DomainContext", domain_text, trace_dir),
            run_validated(client, conn, record, domain, domain_text, trace_dir),
        ]
    finally:
        conn.close()


def main_cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", default="deepseek-chat")
    parser.add_argument("--base-url", default="https://api.deepseek.com/v1")
    parser.add_argument("--api-key-env", default="DEEPSEEK_API_KEY")
    parser.add_argument("--max-questions", type=int, default=0, help="limit questions (0 = all 180)")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--output-dir", default=str(EXPERIMENT_DIR / "outputs_deepseek_x10"))
    args = parser.parse_args()

    api_key = os.environ.get(args.api_key_env, "")
    if not api_key:
        raise SystemExit(f"environment variable {args.api_key_env} is not set")

    point_builders_at_x10()

    # Gold re-verification gate: never spend API money on an invalid dataset.
    dataset_check = validate_dataset(X10_DIR / "database.sqlite", X10_DIR / "questions.jsonl")
    if dataset_check["error_count"]:
        raise SystemExit(f"x10 dataset failed gold validation: {dataset_check['errors'][:5]}")
    print(f"GOLD_CHECK: {dataset_check['question_count']} questions, 0 errors on x10 database")

    splits = json.loads((X10_DIR / "splits.json").read_text(encoding="utf-8"))
    test_ids = list(splits["test"])
    if args.max_questions:
        test_ids = test_ids[: args.max_questions]
    by_id = {q["question_id"]: q for q in load_questions(X10_DIR / "questions.jsonl")}
    records = [by_id[qid] for qid in test_ids]
    print(f"RUN: {len(records)} test questions x C2/C4/C5 on {args.model} (x10 database)")

    out_dir = Path(args.output_dir)
    trace_dir = out_dir / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)

    # Build all contexts up-front with the original builders (offline).
    conn = sqlite3.connect(X10_DIR / "database.sqlite")
    try:
        c2_context = chess.render_full_schema_values(conn)
        bundles = []
        contexts_out = []
        for record in records:
            domain = chess.infer_domain_context(conn, record)
            domain_text = chess.render_selected_context(domain, domain=True)
            bundles.append((record, domain, domain_text))
            contexts_out.append(domain)
    finally:
        conn.close()
    with (out_dir / "contexts.jsonl").open("w", encoding="utf-8") as fh:
        for ctx in contexts_out:
            fh.write(json.dumps(ctx, sort_keys=True) + "\n")
    c4_ctx_tokens = [chess.estimate_tokens(text) for _, _, text in bundles]
    print(f"CONTEXTS: C2 full-schema-values ctx ~{chess.estimate_tokens(c2_context)} tokens; "
          f"C4 domain ctx mean ~{sum(c4_ctx_tokens)/len(c4_ctx_tokens):.1f} tokens")

    client = rsm.ChatClient(args.base_url, api_key, args.model)
    predictions: list[dict[str, Any]] = []
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {
            pool.submit(run_question_bundle, client, record, c2_context, domain, domain_text, trace_dir): record["question_id"]
            for record, domain, domain_text in bundles
        }
        done = 0
        for future in as_completed(futures):
            qid = futures[future]
            predictions.extend(future.result())
            done += 1
            if done % 20 == 0 or done == len(bundles):
                print(f"  progress: {done}/{len(bundles)} questions ({time.monotonic()-started:.0f}s)")

    order = {c: i for i, c in enumerate(CONDITIONS)}
    predictions.sort(key=lambda p: (p["question_id"], order[p["condition"]]))
    with (out_dir / "predictions.jsonl").open("w", encoding="utf-8") as fh:
        for p in predictions:
            fh.write(json.dumps(p, sort_keys=True) + "\n")

    conn = sqlite3.connect(X10_DIR / "database.sqlite")
    try:
        scores, summary = rsm.score_and_summarize(conn, by_id, predictions)
    finally:
        conn.close()
    with (out_dir / "scores.jsonl").open("w", encoding="utf-8") as fh:
        for s in scores:
            fh.write(json.dumps(s, sort_keys=True) + "\n")

    for condition in CONDITIONS:
        preds = [p for p in predictions if p["condition"] == condition]
        if preds and condition in summary:
            summary[condition]["prompt_token_estimate_mean"] = round(
                sum(p["prompt_token_estimate"] for p in preds) / len(preds), 1
            )

    results = {
        "model": args.model,
        "base_url": args.base_url,
        "provider": "deepseek",
        "dataset": "data/griddb_maintenance_v2_x10",
        "gold_validation": {"question_count": dataset_check["question_count"], "error_count": 0},
        "hyperparameters": main.HYPERPARAMETERS,
        "conditions": CONDITIONS,
        "summary": summary,
        "context_token_estimates": {
            "C2_full_schema_values_context": chess.estimate_tokens(c2_context),
            "C4_domain_context_mean": round(sum(c4_ctx_tokens) / len(c4_ctx_tokens), 1),
            "C4_domain_context_max": max(c4_ctx_tokens),
        },
        "prompt_source": "rebuilt with received dev_chess_style_pilot builders on the x10 database; templates from main.py",
        "elapsed_sec": round(time.monotonic() - started, 1),
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"PASS: wrote {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_cli())
