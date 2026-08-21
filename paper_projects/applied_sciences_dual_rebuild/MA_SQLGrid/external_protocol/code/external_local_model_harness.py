#!/usr/bin/env python3
"""Safe local execution harness for the registered MA-SQLGrid external protocol.

Dry-run is the default. Network I/O is possible only with --execute and a
syntactically loopback OpenAI-compatible URL. This module never promotes or
seals review records.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import shutil
import socket
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
ARTIFACTS = ROOT / "artifacts"
DEFAULT_OUT = ROOT / "model_runs" / "external_local_dry_run"
PROMPT_SOURCE = ARTIFACTS / "factorial_prompts.jsonl"
PROTOCOL_MANIFEST = ARTIFACTS / "manifest.json"
REFERENCE_SOURCE = ARTIFACTS / "reference_sql_evaluation.jsonl"
INCIDENT_SOURCE = ROOT.parent / "FORMAL_RUN_INCIDENT_01.json"
EXPECTED_CELLS = {
    "F00_Full_NoShape", "F01_Full_WithShape",
    "F10_Compact_NoShape", "F11_Compact_WithShape",
}
IDENTITY_FIELDS = (
    "dataset_id", "database_id", "database_hash", "schema_hash",
    "instance_id", "question_id", "question_hash", "questions_file_hash",
    "perturbation_id", "perturbation_hash", "condition", "prompt_hash",
    "context_hash", "code_hash", "source_manifest_hash",
)
RUNTIME_REQUIRED = {
    "schema_version", "served_model_id", "model_repo", "model_revision",
    "model_file", "model_sha256", "model_bytes", "license", "backend",
    "backend_revision", "runtime_command",
}
FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum|"
    r"replace|reindex|analyze|load_extension)\b", re.IGNORECASE,
)
PROHIBITED_PROMPT_MARKERS = (
    "registered_reference_sql", "gold_sql", "gold_result", "human_gold",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"invalid JSONL at {path}:{number}: {exc}") from exc
    return rows


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        # os.kill(pid, 0) is not a harmless existence probe on Windows.
        import ctypes
        process_query_limited_information = 0x1000
        still_active = 259
        handle = ctypes.windll.kernel32.OpenProcess(process_query_limited_information, False, pid)
        if not handle:
            return False
        try:
            exit_code = ctypes.c_ulong()
            if not ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                return True  # inability to inspect is treated conservatively as active
            return exit_code.value == still_active
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False


class RunLock:
    """Exclusive create lock. Stale locks are evidence and are never removed."""

    def __init__(self, out: Path, run_fingerprint: str):
        self.path = out / "run.lock.json"
        self.token = uuid.uuid4().hex
        self.payload = {
            "schema_version": "ma-external-run-lock-v1", "pid": os.getpid(),
            "hostname": socket.gethostname(), "started_utc": utc_now(),
            "run_fingerprint": run_fingerprint, "owner_token": self.token,
        }

    def __enter__(self) -> "RunLock":
        try:
            descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        except FileExistsError as exc:
            try:
                old = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                old = {"pid": None, "unreadable": True}
            state = "active" if old.get("hostname") == socket.gethostname() and process_alive(int(old.get("pid") or -1)) else "stale_or_remote"
            raise RuntimeError(
                f"refusing overlapping generation: {self.path} is {state}; "
                "do not delete it. Preserve/quarantine the entire run directory."
            ) from exc
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(self.payload, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        try:
            current = json.loads(self.path.read_text(encoding="utf-8"))
            if current.get("owner_token") == self.token:
                self.path.unlink()
        except FileNotFoundError:
            pass


def is_loopback_url(value: str) -> bool:
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        return False
    if parsed.hostname.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(parsed.hostname).is_loopback
    except ValueError:
        return False


def sanitized_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    host = parsed.hostname or ""
    if parsed.port:
        host += f":{parsed.port}"
    return urllib.parse.urlunsplit((parsed.scheme, host, parsed.path.rstrip("/"), "", ""))


def completions_url(value: str) -> str:
    base = value.rstrip("/")
    return base if base.endswith("/chat/completions") else base + "/chat/completions"


def validate_runtime_manifest(path: Path, model: str, verify_model_file: bool = True) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(RUNTIME_REQUIRED - set(data))
    if missing:
        raise RuntimeError(f"runtime manifest missing fields: {missing}")
    if data["schema_version"] != "ma-external-local-runtime-v1":
        raise RuntimeError("unsupported runtime manifest schema")
    if data["served_model_id"] != model:
        raise RuntimeError("--model does not match runtime manifest served_model_id")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", str(data["model_sha256"])):
        raise RuntimeError("runtime manifest model_sha256 must be exactly 64 hexadecimal characters")
    if int(data["model_bytes"]) < 1:
        raise RuntimeError("runtime manifest model_bytes must be positive")
    model_file = Path(data["model_file"])
    if not model_file.is_absolute():
        model_file = (path.parent / model_file).resolve()
    if verify_model_file:
        if not model_file.is_file():
            raise RuntimeError(f"model file is absent: {model_file}")
        if model_file.stat().st_size != int(data["model_bytes"]):
            raise RuntimeError("model file size differs from runtime manifest")
        if sha256_file(model_file) != str(data["model_sha256"]).lower():
            raise RuntimeError("model file hash differs from runtime manifest")
    return {
        "manifest_sha256": sha256_file(path), "served_model_id": data["served_model_id"],
        "model_repo": data["model_repo"], "model_revision": data["model_revision"],
        "model_file_name": model_file.name, "model_sha256": str(data["model_sha256"]).lower(),
        "model_bytes": int(data["model_bytes"]), "license": data["license"],
        "backend": data["backend"], "backend_revision": data["backend_revision"],
        "runtime_command": data["runtime_command"],
    }


def registered_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return row["dataset_id"], row["question_id"], row["perturbation_id"], row["condition"]


def validate_registered_protocol() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, dict[str, Any]]]:
    manifest = json.loads(PROTOCOL_MANIFEST.read_text(encoding="utf-8"))
    prompts = read_jsonl(PROMPT_SOURCE)
    references = {row["instance_id"]: row for row in read_jsonl(REFERENCE_SOURCE)}
    if manifest.get("question_count") != 91 or manifest.get("cell_count") != 364 or len(prompts) != 364:
        raise RuntimeError("registered protocol is not the required 91 x 4 design")
    counts = Counter(row["condition"] for row in prompts)
    if counts != Counter({cell: 91 for cell in EXPECTED_CELLS}):
        raise RuntimeError(f"registered protocol is not symmetric: {dict(counts)}")
    keys = [registered_key(row) for row in prompts]
    if len(set(keys)) != len(keys):
        raise RuntimeError("registered prompt source contains duplicate exact keys")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in prompts:
        grouped[row["instance_id"]].append(row)
        missing = [field for field in IDENTITY_FIELDS if field not in row]
        if missing:
            raise RuntimeError(f"prompt identity fields missing: {missing}")
        if row.get("annotation_status") != "AUTO_CANDIDATE" or row.get("human_reviewed") or row.get("sealed"):
            raise RuntimeError("only unsealed AUTO_CANDIDATE prompts are accepted")
        if sha256_text(row["prompt"]) != row["prompt_hash"] or sha256_text(row["context"]) != row["context_hash"]:
            raise RuntimeError(f"prompt/context hash mismatch for {registered_key(row)}")
        question_match = re.search(r"\nQuestion:\s*(.*?)\s*$", row["prompt"], flags=re.DOTALL)
        if not question_match or sha256_text(question_match.group(1)) != row["question_hash"]:
            raise RuntimeError(f"question hash mismatch for {registered_key(row)}")
        if canonical_hash({"id": row["perturbation_id"], "block": row["perturbation_block"]}) != row["perturbation_hash"]:
            raise RuntimeError(f"perturbation hash mismatch for {registered_key(row)}")
        lower = row["prompt"].lower()
        if any(marker in lower for marker in PROHIBITED_PROMPT_MARKERS):
            raise RuntimeError(f"prohibited reference/gold field in prompt {registered_key(row)}")
        reference = references.get(row["instance_id"])
        if reference is None or reference["registered_reference_sql"].strip() in row["prompt"]:
            raise RuntimeError(f"registered reference SQL leakage for {registered_key(row)}")
        if any(row[field] != reference[field] for field in ("dataset_id", "question_id", "instance_id")):
            raise RuntimeError(f"reference identity mismatch for {registered_key(row)}")
    if len(grouped) != 91:
        raise RuntimeError(f"expected 91 unique question instances, found {len(grouped)}")
    for instance_id, rows in grouped.items():
        if len(rows) != 4 or {row["condition"] for row in rows} != EXPECTED_CELLS:
            raise RuntimeError(f"incomplete factorial cells for {instance_id}")
        for field in ("database_id", "database_hash", "schema_hash", "question_id", "question_hash",
                      "perturbation_id", "perturbation_hash", "questions_file_hash", "source_manifest_hash"):
            if len({row[field] for row in rows}) != 1:
                raise RuntimeError(f"asymmetric {field} for {instance_id}")
    for dataset_id, dataset in manifest["datasets"].items():
        path = (WORKSPACE / dataset["database_path"]).resolve()
        if sha256_file(path) != dataset["database_sha256"]:
            raise RuntimeError(f"registered database bytes changed for {dataset_id}")
    registered_prompt_hash = canonical_hash([
        {"instance_id": row["instance_id"], "condition": row["condition"],
         "prompt_hash": row["prompt_hash"], "context_hash": row["context_hash"]}
        for row in prompts
    ])
    if registered_prompt_hash != manifest["prompt_set_sha256"]:
        raise RuntimeError("registered prompt-set hash differs from prompt artifact")
    expected_hash = canonical_hash([
        {"key": [r["dataset_id"], r["question_id"], r["condition"]], "prompt": r["prompt_hash"],
         "context": r["context_hash"], "perturbation": r["perturbation_hash"]}
        for r in sorted(prompts, key=lambda x: (x["dataset_id"], x["question_id"], x["condition"]))
    ])
    # The builder's prompt_set hash is authoritative, while this second hash is
    # retained as a harness-specific exact-key fingerprint.
    return sorted(prompts, key=registered_key), manifest, references | {"__harness_prompt_hash__": {"value": expected_hash}}


def strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    return re.sub(r"--[^\r\n]*", " ", sql)


def split_statements(sql: str) -> list[str]:
    statements, buf, quote, index = [], [], None, 0
    while index < len(sql):
        char = sql[index]
        if quote:
            buf.append(char)
            if char == quote:
                if index + 1 < len(sql) and sql[index + 1] == quote:
                    buf.append(sql[index + 1]); index += 1
                else:
                    quote = None
        elif char in {"'", '"', "`"}:
            quote = char; buf.append(char)
        elif char == ";":
            if "".join(buf).strip(): statements.append("".join(buf).strip())
            buf = []
        else:
            buf.append(char)
        index += 1
    if "".join(buf).strip(): statements.append("".join(buf).strip())
    return statements


def validate_single_select(sql: str) -> str:
    normalized = strip_comments(sql).strip()
    statements = split_statements(normalized)
    if len(statements) != 1:
        raise ValueError("exactly one SQL statement is required")
    statement = statements[0]
    if not re.match(r"^(select|with)\b", statement, re.IGNORECASE):
        raise ValueError("only SELECT or WITH ... SELECT is permitted")
    if FORBIDDEN_SQL.search(statement):
        raise ValueError("write/schema-changing SQL token is forbidden")
    return statement


def execute_select(database: Path, sql: str, *, max_rows: int = 100000, step_budget: int = 20_000_000) -> dict[str, Any]:
    try:
        statement = validate_single_select(sql)
    except ValueError as exc:
        return {"safe": False, "executable": False, "error_type": "unsafe_sql", "error_message": str(exc)}
    uri = f"file:{database.resolve().as_posix()}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    denied = {
        getattr(sqlite3, name) for name in (
            "SQLITE_INSERT", "SQLITE_UPDATE", "SQLITE_DELETE", "SQLITE_CREATE_INDEX",
            "SQLITE_CREATE_TABLE", "SQLITE_CREATE_TEMP_INDEX", "SQLITE_CREATE_TEMP_TABLE",
            "SQLITE_CREATE_TEMP_TRIGGER", "SQLITE_CREATE_TEMP_VIEW", "SQLITE_CREATE_TRIGGER",
            "SQLITE_CREATE_VIEW", "SQLITE_DROP_INDEX", "SQLITE_DROP_TABLE", "SQLITE_DROP_TEMP_INDEX",
            "SQLITE_DROP_TEMP_TABLE", "SQLITE_DROP_TEMP_TRIGGER", "SQLITE_DROP_TEMP_VIEW",
            "SQLITE_DROP_TRIGGER", "SQLITE_DROP_VIEW", "SQLITE_ALTER_TABLE", "SQLITE_ATTACH",
            "SQLITE_DETACH", "SQLITE_PRAGMA",
        ) if hasattr(sqlite3, name)
    }
    steps = 0
    def progress() -> int:
        nonlocal steps
        steps += 1000
        return int(steps > step_budget)
    try:
        conn.execute("PRAGMA query_only = ON")
        conn.set_authorizer(lambda action, _a, _b, _db, _src: sqlite3.SQLITE_DENY if action in denied else sqlite3.SQLITE_OK)
        conn.set_progress_handler(progress, 1000)
        cursor = conn.execute(statement)
        columns = [item[0] for item in cursor.description or []]
        rows = [list(row) for row in cursor.fetchmany(max_rows + 1)]
        if len(rows) > max_rows:
            raise RuntimeError(f"result exceeds max_rows={max_rows}")
        return {"safe": True, "executable": True, "error_type": None, "error_message": None,
                "columns": columns, "column_count": len(columns), "row_count": len(rows),
                "result_sha256": canonical_hash({"columns": columns, "rows": rows})}
    except (sqlite3.Error, RuntimeError) as exc:
        return {"safe": True, "executable": False, "error_type": "execution_error", "error_message": str(exc)}
    finally:
        conn.close()


def extract_sql(response: str) -> str:
    text = response.strip()
    match = re.fullmatch(r"```(?:sql)?\s*(.*?)\s*```", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(1).strip()
    return validate_single_select(text)


def database_path(protocol_manifest: dict[str, Any], dataset_id: str) -> Path:
    relative = protocol_manifest["datasets"][dataset_id]["database_path"]
    path = (WORKSPACE / relative).resolve()
    if sha256_file(path) != protocol_manifest["datasets"][dataset_id]["database_sha256"]:
        raise RuntimeError(f"database hash changed for {dataset_id}")
    return path


def call_local(prompt: str, args: argparse.Namespace) -> dict[str, Any]:
    payload = {"model": args.model, "messages": [{"role": "user", "content": prompt}],
               "temperature": args.temperature, "max_tokens": args.max_tokens, "seed": args.seed}
    request = urllib.request.Request(
        completions_url(args.base_url), data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer local-no-auth", "Content-Type": "application/json"}, method="POST",
    )
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=args.timeout) as response:
        decoded = json.loads(response.read().decode("utf-8"))
    content = decoded["choices"][0]["message"]["content"]
    if not isinstance(content, str):
        raise ValueError("response content is not a string")
    return {"raw_response": content, "response_hash": sha256_text(content),
            "model_returned": decoded.get("model") or args.model,
            "latency_ms": int((time.monotonic() - started) * 1000), "usage": decoded.get("usage") or {}}


def quarantine_existing(out: Path, reason: str) -> Path:
    out = out.resolve()
    managed_root = (ROOT / "model_runs").resolve()
    if out == managed_root or not out.is_relative_to(managed_root):
        raise RuntimeError(f"quarantine is restricted to a specific child of {managed_root}")
    if not out.exists():
        raise RuntimeError("--quarantine-existing requested but output directory does not exist")
    if not out.is_dir():
        raise RuntimeError("quarantine target is not a directory")
    for candidate in (out, *out.parents):
        if candidate == managed_root.parent:
            break
        if candidate.is_symlink() or (hasattr(candidate, "is_junction") and candidate.is_junction()):
            raise RuntimeError(f"quarantine refuses symbolic links/junctions: {candidate}")
    lock_path = out / "run.lock.json"
    if lock_path.exists():
        try: lock = json.loads(lock_path.read_text(encoding="utf-8"))
        except Exception: lock = {}
        if lock.get("hostname") == socket.gethostname() and process_alive(int(lock.get("pid") or -1)):
            raise RuntimeError("refusing to quarantine a run owned by an active local PID")
    quarantine = ROOT / "quarantine"
    quarantine.mkdir(parents=True, exist_ok=True)
    destination = quarantine / f"{out.name}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    shutil.move(str(out), str(destination))
    atomic_json(destination / "QUARANTINE_INCIDENT.json", {
        "schema_version": "ma-external-run-incident-v1", "status": "quarantined_not_eligible",
        "reason": reason, "quarantined_utc": utc_now(), "original_directory": str(out),
        "precedent": str(INCIDENT_SOURCE.relative_to(WORKSPACE)).replace("\\", "/"),
        "integrity_decision": "preserved intact; never merge, edit, or promote this run",
    })
    return destination


def validate_resume_checkpoints(
    predictions: list[dict[str, Any]], scores: list[dict[str, Any]], fingerprint: str,
) -> set[tuple[str, str, str, str]]:
    """Reject ambiguous or contaminated journals; never deduplicate them."""
    key_sets: dict[str, set[tuple[str, str, str, str]]] = {}
    for label, rows in (("prediction", predictions), ("score", scores)):
        keys = [tuple(row.get("exact_key", [])) for row in rows]
        if any(len(key) != 4 for key in keys):
            raise RuntimeError(f"invalid exact key in {label} checkpoint; quarantine this run")
        if len(keys) != len(set(keys)):
            raise RuntimeError(f"duplicate {label} generations detected; quarantine this run")
        if any(row.get("run_fingerprint") != fingerprint for row in rows):
            raise RuntimeError(f"resume {label} fingerprint mismatch; quarantine this run")
        key_sets[label] = set(keys)  # type: ignore[assignment]
    if key_sets["prediction"] != key_sets["score"]:
        raise RuntimeError("prediction/score checkpoint key mismatch; quarantine this run")
    return key_sets["prediction"]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--execute", action="store_true", help="Opt in to calls to a loopback endpoint.")
    parser.add_argument("--resume", action="store_true", help="Resume only a clean, unlocked, hash-identical partial run.")
    parser.add_argument("--quarantine-existing", action="store_true", help="Preserve an inactive suspect output directory, then exit.")
    parser.add_argument("--quarantine-reason", default="operator-requested integrity quarantine")
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--runtime-manifest", type=Path)
    parser.add_argument("--scoring-authority", choices=["AUTO_CANDIDATE", "HUMAN_SEALED"], default="AUTO_CANDIDATE")
    parser.add_argument("--seed", type=int, default=20260805)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=800)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--max-rows", type=int, default=100000)
    args = parser.parse_args(argv)
    if args.execute and (not args.base_url or not args.model or not args.runtime_manifest):
        parser.error("--execute requires --base-url, --model, and --runtime-manifest")
    if args.execute and not is_loopback_url(args.base_url):
        parser.error("only a syntactic loopback OpenAI-compatible URL is allowed")
    if args.scoring_authority == "HUMAN_SEALED":
        parser.error("HUMAN_SEALED scoring is unavailable: real dual review/adjudication and sealing are incomplete")
    if args.resume and not args.execute:
        parser.error("--resume is meaningful only with --execute")
    return args


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    out = args.out.resolve()
    if args.quarantine_existing:
        destination = quarantine_existing(out, args.quarantine_reason)
        print(f"quarantined intact: {destination}")
        return 0
    prompts, protocol_manifest, reference_map = validate_registered_protocol()
    runtime = validate_runtime_manifest(args.runtime_manifest.resolve(), args.model) if args.execute else None
    config = {
        "provider": "local-openai-compatible", "base_url": sanitized_url(args.base_url) if args.base_url else None,
        "model": args.model, "runtime": runtime, "seed": args.seed, "temperature": args.temperature,
        "max_tokens": args.max_tokens, "timeout_sec": args.timeout, "max_rows": args.max_rows,
        "execute": args.execute, "scoring_authority": args.scoring_authority,
    }
    source_hashes = {"protocol_manifest_sha256": sha256_file(PROTOCOL_MANIFEST),
                     "prompt_source_sha256": sha256_file(PROMPT_SOURCE),
                     "reference_source_sha256": sha256_file(REFERENCE_SOURCE),
                     "harness_code_sha256": sha256_file(Path(__file__))}
    fingerprint = canonical_hash({"configuration": config, "sources": source_hashes})
    if out.exists() and not args.resume:
        raise RuntimeError("output directory exists; use a new directory, --resume, or explicit --quarantine-existing")
    out.mkdir(parents=True, exist_ok=True)
    with RunLock(out, fingerprint):
        prompt_out = out / "prompts.jsonl"
        prediction_out = out / "predictions.jsonl"
        score_out = out / "scores.jsonl"
        old_predictions = read_jsonl(prediction_out) if args.resume else []
        old_scores = read_jsonl(score_out) if args.resume else []
        manifest_path = out / "run_manifest.json"
        if args.resume:
            if not manifest_path.exists():
                raise RuntimeError("resume requires run_manifest.json")
            old_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if old_manifest.get("run_fingerprint") != fingerprint:
                raise RuntimeError("resume fingerprint differs from frozen configuration/code/data/runtime")
        prediction_keys = validate_resume_checkpoints(old_predictions, old_scores, fingerprint)
        prompt_lines = "".join(json.dumps({**{field: row[field] for field in IDENTITY_FIELDS},
            "exact_key": list(registered_key(row)), "exact_key_sha256": canonical_hash(list(registered_key(row))),
            "prompt": row["prompt"]}, ensure_ascii=False, sort_keys=True) + "\n" for row in prompts)
        if prompt_out.exists():
            if sha256_text(prompt_lines) != sha256_file(prompt_out):
                raise RuntimeError("resume prompt artifact differs from registered prompts")
        else:
            prompt_out.write_text(prompt_lines, encoding="utf-8")
        manifest = {
            "schema_version": "ma-external-local-model-run-v1", "run_started_utc": utc_now(),
            "status": "active" if args.execute else "dry_run_prompts_frozen_not_executed",
            "question_count": 91, "cell_count": 364, "cells": sorted(EXPECTED_CELLS),
            "expected_generation_count": 364, "canonical_result_eligible": False,
            "annotation_status": "AUTO_CANDIDATE", "human_review_complete": False, "sealed": False,
            "scoring_authority": args.scoring_authority,
            "scoring_label": "AUTO_CANDIDATE_REFERENCE_SCORING_NOT_HUMAN_GOLD",
            "human_sealed_scoring_enabled": False,
            "evidence_boundary": "development-only; never eligible for sealed/canonical claims until real review and a valid future sealing protocol complete",
            "configuration": config, "source_hashes": source_hashes, "run_fingerprint": fingerprint,
            "registered_prompt_set_sha256": protocol_manifest["prompt_set_sha256"],
            "harness_exact_key_prompt_sha256": reference_map["__harness_prompt_hash__"]["value"],
            "prompt_artifact_sha256": sha256_file(prompt_out),
            "prediction_count": len(old_predictions), "score_count": len(old_scores),
            "resume_mode": args.resume, "network_scope": "loopback-only" if args.execute else "none",
        }
        atomic_json(manifest_path, manifest)
        if not args.execute:
            print(json.dumps(manifest, indent=2, sort_keys=True))
            return 0
        done = prediction_keys
        for prompt in prompts:
            key = registered_key(prompt)
            if key in done:
                continue
            called_at = utc_now()
            call: dict[str, Any] = {}
            try:
                call = call_local(prompt["prompt"], args)
                predicted_sql = extract_sql(call["raw_response"])
                execution = execute_select(database_path(protocol_manifest, prompt["dataset_id"]), predicted_sql, max_rows=args.max_rows)
                status = "success" if execution.get("executable") else "execution_error"
                error_type = execution.get("error_type")
                error_message = execution.get("error_message")
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as exc:
                predicted_sql, execution = None, {"safe": False, "executable": False, "result_sha256": None}
                status = "provider_error" if isinstance(exc, (urllib.error.URLError, urllib.error.HTTPError, TimeoutError)) else "parse_error"
                error_type, error_message = type(exc).__name__, str(exc)[:1000]
            identity = {field: prompt[field] for field in IDENTITY_FIELDS}
            identity["exact_key_sha256"] = canonical_hash(list(key))
            prediction = {**identity, "exact_key": list(key), "generation_id": uuid.uuid4().hex,
                "run_fingerprint": fingerprint, "called_at_utc": called_at, "status": status,
                "predicted_sql": predicted_sql, "predicted_sql_sha256": sha256_text(predicted_sql) if predicted_sql else None,
                "raw_response": call.get("raw_response"), "response_hash": call.get("response_hash"),
                "model_requested": args.model, "model_returned": call.get("model_returned"),
                "latency_ms": call.get("latency_ms"), "error_type": error_type, "error_message": error_message}
            reference = reference_map[prompt["instance_id"]]
            score = {**identity, "exact_key": list(key), "run_fingerprint": fingerprint,
                "scoring_authority": "AUTO_CANDIDATE", "scoring_label": "AUTO_CANDIDATE_REFERENCE_SCORING_NOT_HUMAN_GOLD",
                "canonical_result_eligible": False, "human_reviewed": False, "sealed": False,
                "status": "auto_candidate_scored" if execution.get("executable") else "not_scored",
                "safe": execution.get("safe", False), "executable": execution.get("executable", False),
                "row_count": execution.get("row_count"), "column_count": execution.get("column_count"),
                "prediction_result_sha256": execution.get("result_sha256"),
                "auto_candidate_reference_result_sha256": reference["result_sha256"],
                "execution_match_auto_candidate_reference": execution.get("result_sha256") == reference["result_sha256"] if execution.get("executable") else False,
                "error_type": error_type, "error_message": error_message}
            append_jsonl(prediction_out, prediction)
            append_jsonl(score_out, score)
            done.add(key)
            manifest["prediction_count"] = len(done); manifest["score_count"] = len(done)
            atomic_json(manifest_path, manifest)
        manifest["status"] = "completed_auto_candidate_development_run"
        manifest["run_finished_utc"] = utc_now()
        manifest["prediction_sha256"] = sha256_file(prediction_out)
        manifest["score_sha256"] = sha256_file(score_out)
        atomic_json(manifest_path, manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
