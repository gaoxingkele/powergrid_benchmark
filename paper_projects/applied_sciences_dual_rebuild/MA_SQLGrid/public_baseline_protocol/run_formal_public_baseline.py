"""Formal runner for one frozen backbone. DO NOT run before human approval.

The runner refuses draft/unreviewed freezes, existing output directories, and
missing or mismatched human approval. It never retries a generation call.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import time
import urllib.request
from urllib.parse import urlparse
from pathlib import Path

import freeze_public_baseline as f

ROOT = Path(__file__).resolve().parent


def request_json(opener, url: str, payload: dict, timeout: float = 600) -> dict:
    request = urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers={"Content-Type": "application/json"})
    with opener.open(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=("qwen", "granite"), required=True)
    parser.add_argument("--server-url", required=True, help="Loopback llama.cpp URL for the matching frozen model.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--human-approval", type=Path, required=True)
    args = parser.parse_args()
    parsed_url = urlparse(args.server_url)
    if not (
        parsed_url.scheme == "http"
        and parsed_url.hostname in {"127.0.0.1", "::1", "localhost"}
        and parsed_url.username is None and parsed_url.password is None
        and parsed_url.path in {"", "/"}
        and not parsed_url.params and not parsed_url.query and not parsed_url.fragment
        and parsed_url.port is not None
    ):
        raise SystemExit("--server-url must be an explicit loopback-only http URL with port and no path/query/userinfo")
    server_url = args.server_url.rstrip("/")
    freeze_path = ROOT / "BASELINE_PROTOCOL_FREEZE.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "INDEPENDENT_TECHNICAL_FREEZE_AUDIT.json").read_text(encoding="utf-8"))
    approval = json.loads(args.human_approval.read_text(encoding="utf-8"))
    freeze_hash = f.sha256(freeze_path)
    if freeze["status"] != "FROZEN_NOT_RUN" or audit["decision"] != "PASS":
        raise SystemExit("Freeze/audit gate is not PASS FROZEN_NOT_RUN")
    if audit.get("protocol_id") != freeze["protocol_id"] or audit.get("freeze_sha256") != freeze_hash:
        raise SystemExit("Independent audit does not bind this exact freeze")
    if not (approval.get("approved_by_human") and approval.get("acknowledge_5000_generation_calls") is True and approval.get("protocol_id") == freeze["protocol_id"] and approval.get("freeze_sha256") == freeze_hash):
        raise SystemExit("Human launch approval is absent or does not bind this exact freeze")
    expected_model = freeze["models"][args.model]
    if f.sha256(Path(expected_model["path"])) != expected_model["sha256"]:
        raise SystemExit("Model hash drift")
    material = freeze["prompt_materialization"]
    prompt_content_path = ROOT / "materialized_prompts" / f"{args.model}_prompts.jsonl.gz"
    prompt_manifest_path = ROOT / "materialized_prompts" / f"{args.model}_prompt_manifest.jsonl"
    order_path = ROOT / "DETERMINISTIC_CALL_ORDER.jsonl"
    frozen_hashes = {
        prompt_content_path: material["prompt_manifests"][prompt_content_path.name]["sha256"],
        prompt_manifest_path: material["prompt_manifests"][prompt_manifest_path.name]["sha256"],
        order_path: material["call_order"]["sha256"],
        ROOT / "official_metadata" / "bird_mini_dev_sqlite.json": freeze["dataset"]["metadata"]["sha256"],
    }
    for path, expected in frozen_hashes.items():
        if f.sha256(path) != expected:
            raise SystemExit(f"Frozen input hash drift: {path}")
    for item in freeze["dataset"]["database_manifest"].values():
        if f.sha256(Path(item["path"])) != item["sha256"]:
            raise SystemExit(f"Database hash drift: {item['path']}")
    if args.output_dir.exists():
        raise SystemExit("Output directory already exists; resume/overlap is prohibited")
    args.output_dir.mkdir(parents=True)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(server_url + "/health", timeout=5) as health:
        if health.status != 200:
            raise SystemExit("Server unhealthy")
    with gzip.open(prompt_content_path, "rt", encoding="utf-8") as handle:
        prompts = [json.loads(line) for line in handle]
    order = [json.loads(line) for line in order_path.read_text(encoding="utf-8").splitlines()]
    if len(prompts) != 2500 or len(order) != 2500:
        raise SystemExit("Call population drift")
    rows = {r["question_id"]: r for r in f.load_rows()}
    call_ledger = args.output_dir / "call_ledger.jsonl"
    final_ledger = args.output_dir / "final_scores.jsonl"
    first_candidates = {}
    token_totals = {}
    calls_completed = 0
    with call_ledger.open("x", encoding="utf-8", buffering=1) as call_out, final_ledger.open("x", encoding="utf-8", buffering=1) as final_out:
        for index, (prompt_record, call) in enumerate(zip(prompts, order)):
            identity = (prompt_record["question_id"], prompt_record["db_id"], prompt_record["method"], prompt_record["call"])
            expected_identity = (call["question_id"], call["db_id"], call["method"], call["call"])
            if identity != expected_identity:
                raise RuntimeError(f"Prompt/order mismatch at {index}")
            rendered = prompt_record["rendered_prompt"]
            if call["method"] == "B3_EXEC_REPAIR" and call["call"] == 2:
                state = first_candidates[call["question_id"]]
                rendered = rendered.replace("{{FIRST_CANDIDATE_RUNTIME_MAX_400_TOKENS}}", state["candidate"])
                rendered = rendered.replace("{{ONE_OF_FROZEN_FEEDBACK_VOCABULARY}}", state["feedback"])
            token_answer = request_json(opener, server_url + "/tokenize", {"content": rendered, "add_special": False}, timeout=120)
            input_tokens = len(token_answer["tokens"])
            key = (call["question_id"], call["method"])
            token_totals[key] = token_totals.get(key, 0) + input_tokens
            if token_totals[key] > 12000 or input_tokens > 15872:
                raise RuntimeError(f"Runtime token budget violation at {identity}")
            output_cap = 400 if call["method"] == "B3_EXEC_REPAIR" else 800
            started = time.perf_counter()
            answer = request_json(opener, server_url + "/completion", {
                "prompt": rendered, "n_predict": output_cap, "temperature": 0.0,
                "seed": 20260805, "stream": False, "cache_prompt": False,
            })
            elapsed = time.perf_counter() - started
            raw = str(answer.get("content", ""))
            candidate = f.extract_sql(raw, call["method"])
            calls_completed += 1
            entry = {
                "call_index": index, **call, "model": args.model,
                "rendered_prompt_sha256": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
                "input_tokens": input_tokens, "output_cap": output_cap,
                "raw_output": raw, "raw_output_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "extracted_sql": candidate, "elapsed_seconds": elapsed,
                "retry_count": 0, "formal_call_number": calls_completed,
            }
            if call["method"] == "B3_EXEC_REPAIR" and call["call"] == 1:
                feedback, _ = f.safe_execute(candidate, f.db_path(call["db_id"]), timeout_seconds=30.0)
                first_candidates[call["question_id"]] = {"candidate": candidate, "feedback": feedback}
                entry["validator_feedback"] = feedback
            call_out.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
            os.fsync(call_out.fileno())
            is_final = call["method"] != "B3_EXEC_REPAIR" or call["call"] == 2
            if is_final:
                pred_status, pred_rows = f.safe_execute(candidate, f.db_path(call["db_id"]), timeout_seconds=180.0)
                gold_status, gold_rows = f.safe_execute(rows[call["question_id"]]["SQL"], f.db_path(call["db_id"]), timeout_seconds=180.0)
                if gold_status != "SAFE_EXECUTED":
                    raise RuntimeError(f"Frozen gold stopped executing at question {call['question_id']}")
                score = f.official_ex(pred_rows or [], gold_rows or []) if pred_status == "SAFE_EXECUTED" else 0
                final_out.write(json.dumps({
                    "question_id": call["question_id"], "db_id": call["db_id"], "method": call["method"],
                    "model": args.model, "prediction_status": pred_status, "official_ex": score,
                    "final_sql": candidate, "all_attempt_denominator": True,
                }, ensure_ascii=False, sort_keys=True) + "\n")
                os.fsync(final_out.fileno())
    expected_calls = 2500
    if calls_completed != expected_calls:
        raise RuntimeError(f"Expected {expected_calls} calls, got {calls_completed}")
    manifest = {
        "protocol_id": freeze["protocol_id"], "freeze_sha256": freeze_hash, "model": args.model,
        "model_sha256": expected_model["sha256"], "calls": calls_completed, "retries": 0,
        "expected_final_rows": 2000, "formal_run_complete": True,
        "call_ledger_sha256": f.sha256(call_ledger), "final_scores_sha256": f.sha256(final_ledger),
    }
    (args.output_dir / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
