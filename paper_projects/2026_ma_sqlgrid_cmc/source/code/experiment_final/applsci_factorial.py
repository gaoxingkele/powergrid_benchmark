#!/usr/bin/env python3
"""Reproducible 2x2 context-scope x answer-shape experiment for MA-SQLGrid.

The default mode is a zero-cost dry run that freezes prompts and hashes.  Model
execution is opt-in via ``--execute`` and uses a caller-supplied
OpenAI-compatible endpoint.  Gold SQL/results are removed before any context or
prompt builder is called.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import random
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import main as formal


CELLS = [
    ("F00_Full_NoShape", "full", False),
    ("F01_Full_WithShape", "full", True),
    ("F10_Compact_NoShape", "compact", False),
    ("F11_Compact_WithShape", "compact", True),
]
CELL_NAMES = [cell[0] for cell in CELLS]
DEFAULT_OUT = formal.EXPERIMENT_DIR.parent / "applsci_factorial"
GOLD_KEYS = {"gold_sql", "gold_result", "gold_results", "answer", "answers"}
LOCAL_MANIFEST_REQUIRED = {
    "schema_version",
    "served_model_id",
    "model_repo",
    "model_revision",
    "model_file",
    "model_sha256",
    "model_bytes",
    "license",
    "backend",
    "backend_revision",
}


def stable_hash(value: str | bytes) -> str:
    data = value if isinstance(value, bytes) else value.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    return stable_hash(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def combined_file_hash(paths: Iterable[Path]) -> str:
    entries = []
    for path in sorted({Path(item).resolve() for item in paths}, key=str):
        entries.append({"name": path.name, "sha256": hash_file(path), "bytes": path.stat().st_size})
    return canonical_hash(entries)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sanitize_base_url(base_url: str) -> str:
    """Remove credentials, query strings, and fragments before logging a URL."""
    parsed = urllib.parse.urlsplit(base_url)
    host = parsed.hostname or ""
    if parsed.port:
        host += f":{parsed.port}"
    return urllib.parse.urlunsplit((parsed.scheme, host, parsed.path.rstrip("/"), "", ""))


def chat_completions_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    return base if base.endswith("/chat/completions") else base + "/chat/completions"


def is_loopback_url(base_url: str) -> bool:
    """Return true only for an HTTP(S) URL whose host resolves syntactically to loopback."""
    parsed = urllib.parse.urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    if parsed.hostname.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(parsed.hostname).is_loopback
    except ValueError:
        return False


def load_local_model_manifest(path: Path, *, served_model_id: str, verify_file: bool) -> dict[str, Any]:
    """Validate pinned local-model provenance and optionally hash the model artifact."""
    manifest_path = path.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    missing = sorted(LOCAL_MANIFEST_REQUIRED - set(data))
    if missing:
        raise ValueError(f"local model manifest is missing required fields: {missing}")
    if data["schema_version"] != "ma-sqlgrid-local-model-v1":
        raise ValueError("unsupported local model manifest schema_version")
    if data["served_model_id"] != served_model_id:
        raise ValueError("--model differs from local model manifest served_model_id")
    if not isinstance(data["model_sha256"], str) or len(data["model_sha256"]) != 64:
        raise ValueError("local model manifest model_sha256 must be a 64-character SHA-256")
    model_file = Path(data["model_file"])
    if not model_file.is_absolute():
        model_file = (manifest_path.parent / model_file).resolve()
    if verify_file:
        if not model_file.is_file():
            raise ValueError(f"local model file does not exist: {model_file}")
        if model_file.stat().st_size != int(data["model_bytes"]):
            raise ValueError("local model file size differs from manifest")
        if hash_file(model_file) != data["model_sha256"].lower():
            raise ValueError("local model file SHA-256 differs from manifest")
    return {
        "manifest_sha256": hash_file(manifest_path),
        "served_model_id": data["served_model_id"],
        "model_repo": data["model_repo"],
        "model_revision": data["model_revision"],
        "model_file_name": model_file.name,
        "model_sha256": data["model_sha256"].lower(),
        "model_bytes": int(data["model_bytes"]),
        "license": data["license"],
        "backend": data["backend"],
        "backend_revision": data["backend_revision"],
    }


def without_gold(record: dict[str, Any]) -> dict[str, Any]:
    """Create the only record representation permitted on the prompt path."""
    return {key: value for key, value in record.items() if key.lower() not in GOLD_KEYS}


def build_contexts(conn: sqlite3.Connection, record: dict[str, Any]) -> dict[str, tuple[str, dict[str, Any]]]:
    if any(key.lower() in GOLD_KEYS for key in record):
        raise ValueError("prompt-path record contains prohibited gold fields")
    bundle = formal.load_context_bundle(conn, record)
    domain = bundle["domain"]
    no_shape = json.loads(json.dumps(domain))
    no_shape["inferred_shape"] = {}
    full_base = bundle["full_schema_values_context"]
    shape_block = "\n\nQuestion-derived answer-shape hints:\n" + json.dumps(
        domain.get("inferred_shape") or {}, sort_keys=True
    )
    return {
        "F00_Full_NoShape": (full_base, no_shape),
        "F01_Full_WithShape": (full_base + shape_block, domain),
        "F10_Compact_NoShape": (formal.chess.render_selected_context(no_shape, domain=True), no_shape),
        "F11_Compact_WithShape": (bundle["domain_text"], domain),
    }


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    temporary.replace(path)


def assert_safe_output_directory(out: Path, *, resume: bool, overwrite: bool) -> None:
    managed = [out / name for name in ("prompts.jsonl", "predictions.jsonl", "scores.jsonl", "manifest.json")]
    existing = [path for path in managed if path.exists()]
    if existing and not (resume or overwrite):
        names = ", ".join(path.name for path in existing)
        raise RuntimeError(f"refusing to overwrite existing run artifacts ({names}); pass --resume or --overwrite")
    if resume and overwrite:
        raise RuntimeError("--resume and --overwrite are mutually exclusive")


def clear_managed_artifacts(out: Path) -> None:
    for name in ("prompts.jsonl", "predictions.jsonl", "scores.jsonl", "manifest.json"):
        (out / name).unlink(missing_ok=True)


def request_payload(prompt: str, args: argparse.Namespace) -> dict[str, Any]:
    return {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "seed": args.seed,
    }


def call_openai_compatible(prompt: str, args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    """Call an OpenAI-compatible chat-completions endpoint with full telemetry."""
    total_latency_ms = 0
    last_error: Exception | None = None
    for attempt in range(args.retries + 1):
        started = time.monotonic()
        try:
            body = json.dumps(request_payload(prompt, args), ensure_ascii=False).encode("utf-8")
            request = urllib.request.Request(
                chat_completions_url(args.base_url),
                data=body,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                decoded = json.loads(response.read().decode("utf-8"))
            total_latency_ms += int((time.monotonic() - started) * 1000)
            choice = decoded["choices"][0]
            content = choice.get("message", {}).get("content")
            if not isinstance(content, str):
                raise ValueError("response choices[0].message.content is not a string")
            usage = decoded.get("usage") or {}
            return {
                "ok": True,
                "response": content,
                "response_hash": stable_hash(content),
                "model_returned": decoded.get("model") or args.model,
                "latency_ms": total_latency_ms,
                "token_input": int(usage.get("prompt_tokens") or 0),
                "token_output": int(usage.get("completion_tokens") or 0),
                "token_total": int(usage.get("total_tokens") or 0),
                "retry_count": attempt,
                "error_type": None,
                "error_message": None,
            }
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, KeyError, json.JSONDecodeError) as exc:
            total_latency_ms += int((time.monotonic() - started) * 1000)
            last_error = exc
            if attempt < args.retries:
                time.sleep(min(args.retry_wait * (attempt + 1), 30.0))
    assert last_error is not None
    return {
        "ok": False,
        "response": None,
        "response_hash": None,
        "model_returned": None,
        "latency_ms": total_latency_ms,
        "token_input": 0,
        "token_output": 0,
        "token_total": 0,
        "retry_count": args.retries,
        "error_type": type(last_error).__name__,
        "error_message": str(last_error)[:1000],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--execute", action="store_true", help="Opt in to model execution; local execution is supported.")
    parser.add_argument("--provider", default="openai-compatible", choices=["openai-compatible", "local-openai-compatible"])
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL"))
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL"))
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY", help="Environment variable name only; its value is never logged.")
    parser.add_argument("--local-model-manifest", type=Path, help="Pinned model/runtime manifest required by local execution.")
    parser.add_argument("--split", choices=["formal", "dev-smoke"], default="formal")
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=800)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-wait", type=float, default=2.0)
    parser.add_argument("--max-questions", type=int, default=0, help="Smoke limit; 0 requires the complete 180-question test split.")
    parser.add_argument("--resume", "--skip-existing", dest="resume", action="store_true")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace managed artifacts in --out.")
    args = parser.parse_args(argv)
    if args.execute:
        if not args.base_url or not args.model:
            parser.error("--execute requires --base-url and --model (or OPENAI_BASE_URL/OPENAI_MODEL)")
        if args.provider == "local-openai-compatible":
            if not is_loopback_url(args.base_url):
                parser.error("local-openai-compatible requires a loopback --base-url")
            if args.local_model_manifest is None:
                parser.error("local-openai-compatible requires --local-model-manifest")
        elif not os.environ.get(args.api_key_env):
            parser.error(f"--execute requires a non-empty {args.api_key_env} environment variable")
    if args.provider != "local-openai-compatible" and args.local_model_manifest is not None:
        parser.error("--local-model-manifest is only valid with local-openai-compatible")
    if args.max_questions < 0 or args.retries < 0 or args.max_tokens < 1:
        parser.error("limits and retry counts must be non-negative, and --max-tokens must be positive")
    return args


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    args.out = args.out.resolve()
    assert_safe_output_directory(args.out, resume=args.resume, overwrite=args.overwrite)
    args.out.mkdir(parents=True, exist_ok=True)
    if args.overwrite:
        clear_managed_artifacts(args.out)

    formal.validate_foundation()
    records = formal.load_split_records("smoke" if args.split == "dev-smoke" else "formal")
    full_split_count = len(records)
    if args.split == "formal" and not args.max_questions and full_split_count != 180:
        raise RuntimeError(f"registered factorial requires exactly 180 held-out questions, found {full_split_count}")
    if args.max_questions:
        records = records[: args.max_questions]
    random.seed(args.seed)

    script_path = Path(__file__).resolve()
    data_paths = [formal.DB_PATH, formal.QUESTIONS_PATH, formal.DATA_DIR / "splits.json", formal.SCHEMA_PATH]
    code_paths = [
        script_path,
        Path(formal.__file__).resolve(),
        Path(formal.chess.__file__).resolve(),
        Path(formal.smoke.__file__).resolve(),
    ]
    run_started = utc_now()
    local_model = None
    if args.provider == "local-openai-compatible":
        local_model = load_local_model_manifest(
            args.local_model_manifest,
            served_model_id=args.model,
            verify_file=args.execute,
        )
    safe_config = {
        "provider": args.provider,
        "base_url": sanitize_base_url(args.base_url) if args.base_url else None,
        "model": args.model,
        "api_key_env": args.api_key_env if args.execute else None,
        "seed": args.seed,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "timeout_sec": args.timeout,
        "retries": args.retries,
        "retry_wait_sec": args.retry_wait,
        "execute": args.execute,
        "split": args.split,
        "local_model": local_model,
    }
    run_hashes = {
        "configuration_sha256": canonical_hash(safe_config),
        "data_sha256": combined_file_hash(data_paths),
        "code_sha256": combined_file_hash(code_paths),
    }

    prompts_path = args.out / "prompts.jsonl"
    predictions_path = args.out / "predictions.jsonl"
    scores_path = args.out / "scores.jsonl"
    old_prompts = read_jsonl(prompts_path) if args.resume else []
    old_predictions = read_jsonl(predictions_path) if args.resume else []
    old_scores = read_jsonl(scores_path) if args.resume else []
    old_manifest_path = args.out / "manifest.json"
    if args.resume and old_manifest_path.exists():
        old_manifest = json.loads(old_manifest_path.read_text(encoding="utf-8"))
        if old_manifest.get("question_count") != len(records):
            raise RuntimeError("resume question count differs from the existing manifest")
        if old_manifest.get("hashes") != run_hashes:
            raise RuntimeError("resume configuration/data/code hashes differ from the existing manifest")
    for row in old_predictions:
        for field, expected in run_hashes.items():
            if row.get(field) != expected:
                raise RuntimeError(f"resume {field} differs for prediction {(row.get('question_id'), row.get('condition'))}")
    old_prompt_by_key = {(row["question_id"], row["condition"]): row for row in old_prompts}
    prediction_by_key = {(row["question_id"], row["condition"]): row for row in old_predictions}
    score_by_key = {(row["question_id"], row["condition"]): row for row in old_scores}

    prompts: list[dict[str, Any]] = []
    conn = sqlite3.connect(formal.DB_PATH)
    try:
        for original_record in records:
            prompt_record = without_gold(original_record)
            contexts = build_contexts(conn, prompt_record)
            for condition, scope, with_shape in CELLS:
                context_text, validation_context = contexts[condition]
                prompt = formal.direct_prompt(prompt_record, context_text, condition)
                gold_sql = str(original_record.get("gold_sql") or "").strip()
                if gold_sql and gold_sql in prompt:
                    raise RuntimeError(f"gold SQL leaked into prompt for {original_record['question_id']} {condition}")
                prompt_row = {
                    "question_id": original_record["question_id"],
                    "condition": condition,
                    "context_scope": scope,
                    "answer_shape_hints": with_shape,
                    "prompt_hash": stable_hash(prompt),
                    "context_hash": stable_hash(context_text),
                    "prompt": prompt,
                    "context": context_text,
                }
                key = (original_record["question_id"], condition)
                if key in old_prompt_by_key:
                    old = old_prompt_by_key[key]
                    if old.get("prompt_hash") != prompt_row["prompt_hash"] or old.get("context_hash") != prompt_row["context_hash"]:
                        raise RuntimeError(f"resume hash mismatch for prompt {key}")
                prompts.append(prompt_row)

                if not args.execute or key in prediction_by_key:
                    continue
                called_at = utc_now()
                api_key = os.environ.get(args.api_key_env) or "local-no-auth"
                call = call_openai_compatible(prompt, args, api_key)
                predicted_sql = formal.smoke.extract_sql(call["response"]) if call["ok"] else None
                status = "success" if predicted_sql else ("parse_error" if call["ok"] else "provider_error")
                prediction = {
                    "question_id": original_record["question_id"],
                    "condition": condition,
                    "status": status,
                    "provider": args.provider,
                    "base_url": safe_config["base_url"],
                    "model_requested": args.model,
                    "model_returned": call["model_returned"],
                    "seed": args.seed,
                    "temperature": args.temperature,
                    "called_at_utc": called_at,
                    "predicted_sql": predicted_sql,
                    "raw_response": call["response"],
                    "latency_ms": call["latency_ms"],
                    "token_input": call["token_input"],
                    "token_output": call["token_output"],
                    "token_total": call["token_total"],
                    "retry_count": call["retry_count"],
                    "error_type": call["error_type"] if status == "provider_error" else ("SQLParseError" if status == "parse_error" else None),
                    "error_message": call["error_message"] if status == "provider_error" else ("no read-only SQL extracted" if status == "parse_error" else None),
                    "prompt_hash": prompt_row["prompt_hash"],
                    "context_hash": prompt_row["context_hash"],
                    "response_hash": call["response_hash"],
                    **run_hashes,
                }
                prediction_by_key[key] = prediction
                if predicted_sql is None:
                    score_by_key[key] = {
                        "question_id": original_record["question_id"],
                        "condition": condition,
                        "status": "not_scored",
                        "correct": False,
                        "error_type": prediction["error_type"],
                        "shape_ok": False,
                        "exec_ok": False,
                    }
                elif args.split == "dev-smoke":
                    try:
                        validation = formal.chess.reference_free_validation(conn, validation_context, predicted_sql)
                        score_by_key[key] = {
                            "question_id": original_record["question_id"],
                            "condition": condition,
                            "status": "diagnostic_only",
                            "correct": None,
                            "error_type": validation.get("error_type"),
                            "shape_ok": bool(validation.get("shape_ok")),
                            "exec_ok": bool(validation.get("exec_ok")),
                        }
                    except Exception as exc:
                        score_by_key[key] = {
                            "question_id": original_record["question_id"],
                            "condition": condition,
                            "status": "diagnostic_error",
                            "correct": None,
                            "error_type": type(exc).__name__,
                            "shape_ok": False,
                            "exec_ok": False,
                        }
                else:
                    try:
                        evaluated = formal.score_prediction(conn, original_record, predicted_sql)
                        validation = formal.chess.reference_free_validation(conn, validation_context, predicted_sql)
                        score_by_key[key] = {
                            "question_id": original_record["question_id"],
                            "condition": condition,
                            "status": "scored",
                            "correct": evaluated.correct,
                            "error_type": evaluated.error_type,
                            "shape_ok": bool(validation.get("shape_ok")),
                            "exec_ok": bool(validation.get("exec_ok")),
                        }
                    except Exception as exc:  # scoring failure is evidence, not a fabricated query
                        score_by_key[key] = {
                            "question_id": original_record["question_id"],
                            "condition": condition,
                            "status": "scoring_error",
                            "correct": False,
                            "error_type": type(exc).__name__,
                            "shape_ok": False,
                            "exec_ok": False,
                        }
                score_by_key[key].update(
                    {
                        "prompt_hash": prompt_row["prompt_hash"],
                        "context_hash": prompt_row["context_hash"],
                        "response_hash": call["response_hash"],
                        **run_hashes,
                    }
                )
                write_jsonl(predictions_path, sorted(prediction_by_key.values(), key=lambda row: (row["question_id"], row["condition"])))
                write_jsonl(scores_path, sorted(score_by_key.values(), key=lambda row: (row["question_id"], row["condition"])))
    finally:
        conn.close()

    prompts.sort(key=lambda row: (row["question_id"], row["condition"]))
    write_jsonl(prompts_path, prompts)
    predictions = sorted(prediction_by_key.values(), key=lambda row: (row["question_id"], row["condition"]))
    scores = sorted(score_by_key.values(), key=lambda row: (row["question_id"], row["condition"]))
    if args.execute:
        write_jsonl(predictions_path, predictions)
        write_jsonl(scores_path, scores)

    prompt_counts = {condition: sum(row["condition"] == condition for row in prompts) for condition in CELL_NAMES}
    expected_per_cell = len(records)
    if prompt_counts != {condition: expected_per_cell for condition in CELL_NAMES}:
        raise RuntimeError(f"factorial cell imbalance: {prompt_counts}")
    unique_prompt_keys = {(row["question_id"], row["condition"]) for row in prompts}
    if len(unique_prompt_keys) != len(prompts):
        raise RuntimeError("duplicate question-condition prompt keys")

    execution_complete = args.execute and len(predictions) == len(prompts) and len(scores) == len(prompts)
    execution_failures = sum(row.get("status") != "success" for row in predictions)
    accepted_score_status = "diagnostic_only" if args.split == "dev-smoke" else "scored"
    scoring_failures = sum(row.get("status") != accepted_score_status for row in scores)
    if not args.execute:
        run_status = "prompts_frozen_not_executed"
    elif not execution_complete:
        run_status = "partial"
    elif execution_failures or scoring_failures:
        run_status = "completed_with_failures"
    elif args.split == "dev-smoke":
        run_status = "noncanonical_smoke_completed"
    else:
        run_status = "completed"

    manifest: dict[str, Any] = {
        "schema_version": "ma-sqlgrid-applsci-factorial-v1",
        "design": "2x2 context scope (full/compact) x answer-shape hints (absent/present)",
        "split": "GridDB-Maintenance-v2 v0.1 development smoke" if args.split == "dev-smoke" else "frozen GridDB-Maintenance-v2 v0.1 held-out test",
        "run_started_utc": run_started,
        "run_finished_utc": utc_now(),
        "question_count": len(records),
        "registered_full_split_count": full_split_count,
        "is_full_registered_run": args.split == "formal" and not args.max_questions and len(records) == 180,
        "canonical_result_eligible": args.split == "formal" and not args.max_questions and len(records) == 180,
        "gold_scoring_enabled": args.split == "formal",
        "cells": CELL_NAMES,
        "expected_predictions": len(records) * len(CELLS),
        "prompt_count": len(prompts),
        "prompt_counts_by_cell": prompt_counts,
        "prediction_count": len(predictions),
        "score_count": len(scores),
        "status": run_status,
        "resume_mode": args.resume,
        "configuration": safe_config,
        "hashes": run_hashes,
        "prompt_set_sha256": canonical_hash([{"key": [row["question_id"], row["condition"]], "prompt": row["prompt_hash"], "context": row["context_hash"]} for row in prompts]),
        "gold_leakage_policy": "gold fields are removed before context/prompt construction; exact gold SQL absence is asserted per prompt",
        "artifacts": {"prompts": "prompts.jsonl", "predictions": "predictions.jsonl" if args.execute else None, "scores": "scores.jsonl" if args.execute else None},
    }
    if args.execute:
        manifest["status_counts"] = {status: sum(row["status"] == status for row in predictions) for status in ("success", "parse_error", "provider_error")}
        manifest["score_status_counts"] = {
            status: sum(row["status"] == status for row in scores)
            for status in ("scored", "not_scored", "scoring_error", "diagnostic_only", "diagnostic_error")
        }
        manifest["results"] = {}
        for condition in CELL_NAMES:
            rows = [row for row in scores if row["condition"] == condition]
            scored = [row for row in rows if row["status"] == "scored"]
            result = {"row_count": len(rows), "scored_count": len(scored)}
            if args.split == "formal":
                result.update(
                    {
                        "execution_accuracy_all_attempts": sum(bool(row["correct"]) for row in rows) / expected_per_cell,
                        "answer_shape_accuracy_all_attempts": sum(bool(row["shape_ok"]) for row in rows) / expected_per_cell,
                    }
                )
            else:
                result.update(
                    {
                        "diagnostic_only_count": sum(row["status"] == "diagnostic_only" for row in rows),
                        "safe_execution_count": sum(bool(row["exec_ok"]) for row in rows),
                        "gold_accuracy_reported": False,
                    }
                )
            manifest["results"][condition] = result
    (args.out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
