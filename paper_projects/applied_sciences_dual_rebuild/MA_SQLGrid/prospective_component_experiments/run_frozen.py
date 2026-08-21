#!/usr/bin/env python3
"""Opt-in local runner for the frozen E1/E2/E4 candidate-generation calls.

This script deliberately does not load gold SQL or score outcomes. Formal calls
are impossible unless ``--execute-frozen`` is supplied and the freeze verifies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import verify_freeze


HERE = Path(__file__).resolve().parent
MA = HERE.parent
MANIFESTS = {
    "qwen": MA / "local_model_artifact_manifest.json",
    "granite": MA / "granite33_local_model_artifact_manifest.json",
}


def jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def gpu_snapshot() -> dict:
    command = shutil.which("nvidia-smi")
    if not command:
        return {"available": False, "output": None}
    completed = subprocess.run(
        [command, "--query-gpu=name,driver_version,memory.total,temperature.gpu,pstate", "--format=csv,noheader"],
        capture_output=True, text=True, timeout=15, check=False,
    )
    return {"available": completed.returncode == 0, "output": completed.stdout.strip() or completed.stderr.strip()}


def served_models(base_url: str) -> list[str]:
    with urllib.request.urlopen(base_url.rstrip("/") + "/models", timeout=10) as response:
        body = json.loads(response.read().decode("utf-8"))
    return [str(row.get("id")) for row in body.get("data", []) if row.get("id")]


def call(prompt: str, model_id: str, base_url: str, config: dict) -> dict:
    endpoint = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config["temperature"],
        "seed": config["seed"],
        "max_tokens": config["max_tokens"],
    }
    last_error = None
    elapsed_ms = 0
    for attempt in range(config["retries"] + 1):
        started = time.monotonic()
        try:
            request = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=config["timeout_sec"]) as response:
                body = json.loads(response.read().decode("utf-8"))
            elapsed_ms += round((time.monotonic() - started) * 1000)
            text = body["choices"][0]["message"]["content"]
            usage = body.get("usage") or {}
            return {
                "status": "success", "raw_response": text, "response_sha256": sha256_text(text),
                "latency_ms": elapsed_ms, "token_input": int(usage.get("prompt_tokens") or 0),
                "token_output": int(usage.get("completion_tokens") or 0),
                "token_total": int(usage.get("total_tokens") or 0), "retry_count": attempt,
                "model_returned": body.get("model"), "error": None,
            }
        except Exception as exc:  # persisted as evidence; resume is explicit
            elapsed_ms += round((time.monotonic() - started) * 1000)
            last_error = f"{type(exc).__name__}: {str(exc)[:500]}"
    return {"status": "provider_error", "raw_response": None, "response_sha256": None,
            "latency_ms": elapsed_ms, "token_input": 0, "token_output": 0, "token_total": 0,
            "retry_count": config["retries"], "model_returned": None, "error": last_error}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=sorted(MANIFESTS))
    parser.add_argument("--base-url", required=True, help="Loopback OpenAI-compatible /v1 base URL")
    parser.add_argument("--execute-frozen", action="store_true", help="Required opt-in; otherwise no calls occur")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if not args.execute_frozen:
        parser.error("formal execution requires --execute-frozen")
    if not (args.base_url.startswith("http://127.0.0.1:") or args.base_url.startswith("http://localhost:")):
        parser.error("only a loopback local endpoint is allowed")
    return args


def main() -> int:
    args = parse_args()
    verify_freeze.main()
    freeze = json.loads((HERE / "PROTOCOL_FREEZE.json").read_text(encoding="utf-8"))
    config = freeze["generation"]
    model_manifest = json.loads(MANIFESTS[args.model].read_text(encoding="utf-8"))
    model_spec = freeze["models"][args.model]
    if model_manifest["model_sha256"] != model_spec["model_sha256"] or model_manifest["served_model_id"] != model_spec["served_model_id"]:
        raise RuntimeError("local model manifest drifted from freeze")
    model_file = Path(model_manifest["model_file"])
    if not model_file.is_file() or model_file.stat().st_size != int(model_spec["model_bytes"]):
        raise RuntimeError("frozen local model artifact is missing or has the wrong size")
    if sha256_file(model_file) != model_spec["model_sha256"]:
        raise RuntimeError("frozen local model artifact SHA-256 mismatch")
    prompts = {(row["question_id"], row["condition"]): row for row in jsonl(HERE / "frozen_prompts.jsonl")}
    warmups = jsonl(HERE / "warmup_prompts.jsonl")
    order = jsonl(HERE / f"call_order_{args.model}.jsonl")
    out = HERE / "runs" / args.model
    out.mkdir(parents=True, exist_ok=True)
    pred_path = out / "predictions.jsonl"
    run_manifest_path = out / "RUN_MANIFEST.json"
    existing = jsonl(pred_path)
    if existing and not args.resume:
        raise RuntimeError("predictions already exist; use --resume after checking the run incident")
    done = {(row["question_id"], row["condition"]) for row in existing if row["status"] == "success"}

    ids = served_models(args.base_url)
    if model_spec["served_model_id"] not in ids:
        raise RuntimeError(f"frozen served model is absent from /models: {ids}")
    run_manifest = {
        "schema_version": "ma-sqlgrid-prospective-component-run-v1", "status": "started",
        "started_utc": utc_now(), "model_key": args.model, "served_model_id": model_spec["served_model_id"],
        "model_sha256": model_spec["model_sha256"], "backend": model_spec["backend"],
        "backend_revision": model_spec["backend_revision"], "base_url": args.base_url.rstrip("/"),
        "freeze_sha256": sha256_file(HERE / "PROTOCOL_FREEZE.json"), "gpu_before": gpu_snapshot(),
        "expected_formal_calls": len(order), "resume": args.resume,
    }
    run_manifest_path.write_text(json.dumps(run_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not existing:
        for row in warmups:
            result = call(row["prompt"], model_spec["served_model_id"], args.base_url, config)
            append_jsonl(out / "warmup_log.jsonl", {"question_id": row["question_id"], "condition": row["condition"], **result})

    for item in order:
        key = (item["question_id"], item["condition"])
        if key in done:
            continue
        prompt = prompts[key]
        result = call(prompt["prompt"], model_spec["served_model_id"], args.base_url, config)
        append_jsonl(pred_path, {
            "call_index": item["call_index"], "called_at_utc": utc_now(), "question_id": key[0], "condition": key[1],
            "prompt_sha256": prompt["prompt_sha256"], "model_key": args.model,
            "served_model_id": model_spec["served_model_id"], "model_sha256": model_spec["model_sha256"], **result,
        })
        if result["status"] != "success":
            raise RuntimeError(f"call failed at {key}; inspect evidence and resume explicitly")
    completed_rows = jsonl(pred_path)
    run_manifest.update({"status": "completed_predictions_unscored", "finished_utc": utc_now(),
                         "prediction_rows": len(completed_rows), "gpu_after": gpu_snapshot(),
                         "prediction_ledger_sha256": sha256_file(pred_path),
                         "zero_retry_fraction": sum(row["retry_count"] == 0 for row in completed_rows) / len(completed_rows)})
    run_manifest_path.write_text(json.dumps(run_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: completed {len(order)} frozen formal calls for {args.model}; scoring has not run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
