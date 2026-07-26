#!/usr/bin/env python3
"""Second-generator comparison runner for MA-SQLGrid (P0-1).

Runs C2 / C4 / C5 on the same 180 held-out test questions against ANY
OpenAI-compatible chat-completions endpoint, writing outputs in the same
schema as the archived formal run so that all analysis scripts
(analysis/recompute_relaxed_metrics.py, analysis/recompute_efficiency.py)
work unchanged on the new outputs directory.

Design notes
------------
* Prompt fidelity: the original condition-building module
  (dev_chess_style_pilot) is not part of this package, so this runner reuses
  the EXACT archived prompts stored in outputs/traces/*.json. Those prompts
  embed the condition-specific context (full schema+values for C2, compact
  domain context for C4/C5) byte-for-byte as used in the reported run, which
  guarantees the new model sees identical inputs.
* C5 validation/ranking/repair: reimplemented here from the specification
  published in the paper (ranker weights: safe +10/-20, execution +10/-15,
  shape +6/-5, ordering +3/-2, empty result -2, value hit +4, missing value
  hint -3, deterministic tie-break by candidate index). Inferred shapes and
  normalized value hints are read from the archived outputs/contexts.jsonl.
* No gold information is used at prediction time; scoring runs afterwards
  with the packaged evaluator.

Usage
-----
  python run_second_model.py \
      --model Qwen2.5-Coder-32B-Instruct \
      --base-url https://<endpoint>/v1 \
      --api-key-env SECOND_MODEL_API_KEY \
      [--conditions C2,C4,C5] [--max-questions N] [--output-dir DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import os
import sqlite3
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

EXPERIMENT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = EXPERIMENT_DIR.parents[1]
DATA_DIR = SOURCE_DIR / "data" / "griddb_maintenance_v2_v0_1"
ARCHIVED_OUT = EXPERIMENT_DIR / "outputs"

sys.path.insert(0, str(EXPERIMENT_DIR.parent / "evaluator"))
from evaluator import execute_sql, load_questions, score_prediction, validate_read_only_select  # noqa: E402

CONDITION_MAP = {
    "C2": "C2_FullSchemaValues_Direct",
    "C4": "C4_MASQLGrid_DomainContext",
    "C5": "C5_MASQLGrid_DomainContext_Validated",
}
HYPERPARAMETERS = {
    "temperature": 0,
    "max_tokens": 700,
    "model_call_attempts": 4,
    "repair_attempts": 1,
    "c5_candidate_limit": 5,
}
RANKER_WEIGHTS = {
    "safe": (10, -20),
    "exec": (10, -15),
    "shape": (6, -5),
    "order": (3, -2),
    "empty": -2,
    "value_hit": 4,
    "missing_hint": -3,
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# OpenAI-compatible client (stdlib only)
# ---------------------------------------------------------------------------
class ChatClient:
    def __init__(self, base_url: str, api_key: str, model: str, timeout_sec: int = 120) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout_sec = timeout_sec

    def chat_once(self, prompt: str) -> tuple[str, str, int, int]:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": HYPERPARAMETERS["temperature"],
            "max_tokens": HYPERPARAMETERS["max_tokens"],
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"] or ""
        usage = body.get("usage") or {}
        model = body.get("model") or self.model
        return content, model, int(usage.get("prompt_tokens") or 0), int(usage.get("completion_tokens") or 0)

    def chat_with_retries(self, prompt: str) -> tuple[str, str, int, int, int, int]:
        last_exc: Exception | None = None
        total_latency_ms = 0
        for attempt in range(int(HYPERPARAMETERS["model_call_attempts"])):
            start = time.monotonic()
            try:
                content, model, tin, tout = self.chat_once(prompt)
                total_latency_ms += int((time.monotonic() - start) * 1000)
                return content, model, total_latency_ms, tin, tout, attempt
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                total_latency_ms += int((time.monotonic() - start) * 1000)
                time.sleep(min(8, 2 * (attempt + 1)))
        assert last_exc is not None
        raise last_exc


# ---------------------------------------------------------------------------
# SQL extraction (reimplementation; original minimal_text2sql_smoke missing)
# ---------------------------------------------------------------------------
def _strip_fences(text: str) -> str:
    fenced = re.findall(r"```(?:sql)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        return "\n".join(fenced)
    return text


def extract_sql(raw: str) -> str:
    text = _strip_fences(raw or "").strip()
    match = re.search(r"(?is)\b(select|with)\b.*", text)
    if not match:
        return ""
    sql = match.group(0).strip()
    if ";" in sql:
        sql = sql.split(";", 1)[0] + ";"
    elif not sql.endswith(";"):
        sql += ";"
    return sql


def extract_candidate_sql(raw: str) -> list[str]:
    text = _strip_fences(raw or "")
    # split on numbered-list markers at line starts: "1.", "2)", etc.
    parts = re.split(r"(?m)^\s*\d+[\.\)]\s*", text)
    candidates: list[str] = []
    for part in parts:
        sql = extract_sql(part)
        if sql:
            candidates.append(sql)
    if not candidates:
        sql = extract_sql(text)
        if sql:
            candidates = [sql]
    return candidates


# ---------------------------------------------------------------------------
# Reference-free validation and ranking (reimplemented per published spec)
# ---------------------------------------------------------------------------
def parse_hint_literal(hint: str) -> str:
    match = re.search(r'=\s*"(.*)"\s*$', hint)
    return match.group(1) if match else hint


def reference_free_validation(conn: sqlite3.Connection, ctx: dict[str, Any], sql: str) -> dict[str, Any]:
    safe, _, _ = validate_read_only_select(sql)
    result = execute_sql(conn, sql)
    shape = ctx.get("inferred_shape") or {}
    expected_cols = shape.get("column_count")
    shape_ok = True
    if result.ok and isinstance(expected_cols, int):
        shape_ok = len(result.columns) == expected_cols
        if shape_ok and shape.get("row_granularity") == "scalar":
            shape_ok = len(result.rows) == 1
    order_ok = True
    if shape.get("order_required"):
        order_ok = bool(re.search(r"(?i)\border\s+by\b", sql))
    hints = list(ctx.get("normalized_value_hints") or [])
    lowered = sql.lower()
    hits = [h for h in hints if parse_hint_literal(h).lower() in lowered]
    missing = [h for h in hints if h not in hits]
    return {
        "safe": bool(safe),
        "exec_ok": bool(result.ok),
        "shape_ok": bool(shape_ok) if result.ok else False,
        "order_ok": bool(order_ok),
        "empty_result": bool(result.ok and not result.rows),
        "value_hits": len(hits),
        "value_hint_count": len(hints),
        "missing_value_hints": missing,
        "execution_error": "" if result.ok else result.error,
    }


def ranker_score(validation: dict[str, Any], index: int) -> float:
    w = RANKER_WEIGHTS
    score = 0.0
    score += w["safe"][0] if validation["safe"] else w["safe"][1]
    score += w["exec"][0] if validation["exec_ok"] else w["exec"][1]
    score += w["shape"][0] if validation["shape_ok"] else w["shape"][1]
    score += w["order"][0] if validation["order_ok"] else w["order"][1]
    if validation["empty_result"]:
        score += w["empty"]
    score += w["value_hit"] * validation["value_hits"]
    score += w["missing_hint"] * len(validation["missing_value_hints"])
    score -= index  # deterministic tie-break: earlier candidates preferred
    return score


def rank_candidates(conn: sqlite3.Connection, ctx: dict[str, Any], candidates: list[str]) -> tuple[int, list[dict[str, Any]]]:
    trace: list[dict[str, Any]] = []
    best_idx, best_score = 0, float("-inf")
    for i, sql in enumerate(candidates):
        validation = reference_free_validation(conn, ctx, sql)
        score = ranker_score(validation, i)
        trace.append({"candidate_index": i, "sql": sql, "ranker_score": score, **validation})
        if score > best_score:
            best_idx, best_score = i, score
    return best_idx, trace


def repair_prompt(question_id: str, question: str, context_hint: str, sql: str, validation: dict[str, Any]) -> str:
    # Mirrors the archived repair template from main.py.
    return f"""Repair this SQLite SELECT query using only selected context and inferred hints.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.

{context_hint}

Question ID: {question_id}
Question: {question}
Previous SQL: {sql}
Reference-free validation result: {json.dumps(validation, sort_keys=True)}
"""


# ---------------------------------------------------------------------------
# Archived-prompt loading
# ---------------------------------------------------------------------------
def load_archived_prompts(condition: str) -> dict[str, str]:
    prompts: dict[str, str] = {}
    for trace_path in (ARCHIVED_OUT / "traces").glob(f"Q*_seed0_{condition}.json"):
        qid = trace_path.name.split("_", 1)[0]
        prompts[qid] = json.loads(trace_path.read_text(encoding="utf-8"))["prompt"]
    return prompts


def load_domain_contexts() -> dict[str, dict[str, Any]]:
    contexts: dict[str, dict[str, Any]] = {}
    for line in (ARCHIVED_OUT / "contexts.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        ctx = json.loads(line)
        if ctx.get("mode") == "domain":
            contexts[ctx["question_id"]] = ctx
    return contexts


def extract_context_block(prompt: str) -> str:
    """Recover the context text between the condition line and the question footer."""
    match = re.search(r"(?s)Condition: \S+\n\n(.*)\n\nQuestion ID:", prompt)
    return match.group(1) if match else ""


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_condition(
    client: ChatClient,
    conn: sqlite3.Connection,
    condition: str,
    questions: dict[str, dict[str, Any]],
    prompts: dict[str, str],
    domain_ctx: dict[str, dict[str, Any]],
    trace_dir: Path,
    provider: str,
) -> list[dict[str, Any]]:
    predictions: list[dict[str, Any]] = []
    validated = condition.startswith("C5")
    for qid in sorted(prompts):
        record = questions[qid]
        prompt = prompts[qid]
        context_text = extract_context_block(prompt)
        ctx = domain_ctx.get(qid, {}) if condition.startswith(("C4", "C5")) else {}
        raw = ""
        repair_raw = ""
        repaired_sql = ""
        model = client.model
        latency_ms = token_input = token_output = retry_count = 0
        error: str | None = None
        candidates = ["SELECT 1;"]
        selected_idx = 0
        rank_trace: list[dict[str, Any]] = []
        try:
            raw, model, latency_ms, token_input, token_output, retry_count = client.chat_with_retries(prompt)
            if validated:
                candidates = extract_candidate_sql(raw)[: int(HYPERPARAMETERS["c5_candidate_limit"])]
            else:
                sql = extract_sql(raw)
                candidates = [sql] if sql else []
            if not candidates:
                candidates = ["SELECT 1;"]
                error = "no SQL candidate extracted"
        except Exception as exc:  # noqa: BLE001
            error = f"{type(exc).__name__}: {exc}"

        if validated:
            selected_idx, rank_trace = rank_candidates(conn, ctx, candidates)
            predicted_sql = candidates[selected_idx]
            validation = rank_trace[selected_idx]
            needs_repair = (
                not validation["exec_ok"]
                or not validation["shape_ok"]
                or not validation["order_ok"]
                or bool(validation["missing_value_hints"])
            )
            if not error and needs_repair and int(HYPERPARAMETERS["repair_attempts"]) > 0:
                try:
                    prompt2 = repair_prompt(qid, record["question"], context_text, predicted_sql,
                                            {k: v for k, v in validation.items() if k not in {"candidate_index", "sql", "ranker_score"}})
                    repair_raw, model2, lat2, in2, out2, retr2 = client.chat_with_retries(prompt2)
                    repaired_sql = extract_sql(repair_raw)
                    repaired_validation = reference_free_validation(conn, ctx, repaired_sql)
                    if repaired_validation["exec_ok"] and (
                        not validation["exec_ok"]
                        or int(repaired_validation["shape_ok"]) >= int(validation["shape_ok"])
                        or repaired_validation["value_hits"] >= validation["value_hits"]
                    ):
                        candidates.append(repaired_sql)
                        selected_idx = len(candidates) - 1
                        predicted_sql = repaired_sql
                        rank_trace.append({"candidate_index": selected_idx, "sql": repaired_sql,
                                           "ranker_score": None, **repaired_validation})
                    latency_ms += lat2
                    token_input += in2
                    token_output += out2
                    retry_count += retr2
                    model = model2
                except Exception as exc:  # noqa: BLE001
                    error = f"repair {type(exc).__name__}: {exc}"
        else:
            predicted_sql = candidates[0]

        if not predicted_sql.strip():
            predicted_sql = "SELECT 1;"
            error = error or "empty SQL extracted"

        trace_path = trace_dir / f"{qid}_seed0_{condition}.json"
        trace_payload: dict[str, Any] = {"prompt": prompt, "raw_response": raw}
        if validated:
            trace_payload.update({"rank_trace": rank_trace, "repair_raw_response": repair_raw, "repaired_sql": repaired_sql})
        trace_path.write_text(json.dumps(trace_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        predictions.append({
            "question_id": qid,
            "condition": condition,
            "seed": 0,
            "model": model,
            "provider": provider,
            "prompt_hash": sha256_text(prompt),
            "schema_context_hash": sha256_text(context_text),
            "input_contract_version": "griddb-maintenance-v2-v0.1/no-gold-v1",
            "predicted_sql": predicted_sql,
            "candidate_sql": candidates,
            "selected_candidate_index": selected_idx,
            "intermediate_trace_path": str(trace_path),
            "latency_ms": latency_ms,
            "token_input": token_input,
            "token_output": token_output,
            "retry_count": retry_count,
            "error": error,
        })
        done = len(predictions)
        if done % 20 == 0:
            print(f"  {condition}: {done}/{len(prompts)}")
    return predictions


def score_and_summarize(conn: sqlite3.Connection, questions: dict[str, dict[str, Any]],
                        predictions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    scores: list[dict[str, Any]] = []
    for p in predictions:
        record = questions[p["question_id"]]
        s = score_prediction(conn, record, p["predicted_sql"])
        safe, _, _ = validate_read_only_select(p["predicted_sql"])
        scores.append({
            "question_id": p["question_id"],
            "condition": p["condition"],
            "seed": 0,
            "safe_sql": bool(safe),
            "evaluator_correct": s.correct,
            "evaluator_error_type": s.error_type,
            "evaluator_details": s.details,
            "latency_ms": p["latency_ms"],
            "provider_error": bool(p.get("error")),
        })
    summary: dict[str, Any] = {}
    for condition in sorted({p["condition"] for p in predictions}):
        rows = [s for s in scores if s["condition"] == condition]
        preds = [p for p in predictions if p["condition"] == condition]
        summary[condition] = {
            "n": len(rows),
            "correct": sum(1 for s in rows if s["evaluator_correct"]),
            "execution_accuracy": round(sum(1 for s in rows if s["evaluator_correct"]) / max(1, len(rows)), 4),
            "safe_sql_rate": round(sum(1 for s in rows if s["safe_sql"]) / max(1, len(rows)), 4),
            "provider_error_count": sum(1 for p in preds if p.get("error")),
            "token_input_mean": round(statistics.mean([p["token_input"] for p in preds]), 1),
            "token_output_mean": round(statistics.mean([p["token_output"] for p in preds]), 1),
            "latency_ms_mean": round(statistics.mean([p["latency_ms"] for p in preds]), 1),
        }
    return scores, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="model name to request from the endpoint")
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible base URL (ending in /v1)")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY", help="environment variable holding the API key")
    parser.add_argument("--provider", default="second-model", help="provider label written to prediction records")
    parser.add_argument("--conditions", default="C2,C4,C5", help="comma-separated subset of C2,C4,C5")
    parser.add_argument("--max-questions", type=int, default=0, help="limit questions (0 = all 180)")
    parser.add_argument("--output-dir", default="", help="output directory (default outputs_<model>)")
    args = parser.parse_args()

    api_key = os.environ.get(args.api_key_env, "")
    if not api_key:
        raise SystemExit(f"environment variable {args.api_key_env} is not set")

    conditions = []
    for short in args.conditions.split(","):
        short = short.strip().upper()
        if short not in CONDITION_MAP:
            raise SystemExit(f"unsupported condition {short}; choose from {sorted(CONDITION_MAP)}")
        conditions.append(CONDITION_MAP[short])

    model_slug = re.sub(r"[^A-Za-z0-9._-]+", "-", args.model)
    out_dir = Path(args.output_dir) if args.output_dir else EXPERIMENT_DIR / f"outputs_{model_slug}"
    trace_dir = out_dir / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)

    questions = {q["question_id"]: q for q in load_questions(DATA_DIR / "questions.jsonl")}
    domain_ctx = load_domain_contexts()
    client = ChatClient(args.base_url, api_key, args.model)
    conn = sqlite3.connect(DATA_DIR / "database.sqlite")

    all_predictions: list[dict[str, Any]] = []
    try:
        for condition in conditions:
            prompts = load_archived_prompts(condition)
            if not prompts:
                raise SystemExit(f"no archived prompts found for {condition} under {ARCHIVED_OUT / 'traces'}")
            if args.max_questions:
                prompts = {qid: prompts[qid] for qid in sorted(prompts)[: args.max_questions]}
            print(f"running {condition} on {len(prompts)} questions with model={args.model}")
            all_predictions.extend(
                run_condition(client, conn, condition, questions, prompts, domain_ctx, trace_dir, args.provider)
            )
        scores, summary = score_and_summarize(conn, questions, all_predictions)
    finally:
        conn.close()

    with (out_dir / "predictions.jsonl").open("w", encoding="utf-8") as fh:
        for p in all_predictions:
            fh.write(json.dumps(p, sort_keys=True) + "\n")
    with (out_dir / "scores.jsonl").open("w", encoding="utf-8") as fh:
        for s in scores:
            fh.write(json.dumps(s, sort_keys=True) + "\n")
    results = {
        "model": args.model,
        "base_url": args.base_url,
        "provider": args.provider,
        "hyperparameters": HYPERPARAMETERS,
        "ranker_weights": RANKER_WEIGHTS,
        "conditions": conditions,
        "summary": summary,
        "prompt_source": "archived formal-run prompts (outputs/traces)",
    }
    (out_dir / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"PASS: wrote {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
