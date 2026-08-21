#!/usr/bin/env python3
"""Run one C2GES protocol while recording wall time, memory, logs, and failure."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil


HERE = Path(__file__).resolve().parent


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--protocol", choices=("oracle-label", "predicted-label", "label-blind"), required=True)
    parser.add_argument("--predicted-labels", type=Path)
    parser.add_argument("--train-limit", type=int, required=True)
    parser.add_argument("--dev-limit", type=int, required=True)
    parser.add_argument("--test-limit", type=int, required=True)
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--sample-interval", type=float, default=0.2)
    args = parser.parse_args()
    if args.protocol == "predicted-label" and not args.predicted_labels:
        parser.error("predicted-label requires --predicted-labels")
    if args.protocol != "predicted-label" and args.predicted_labels:
        parser.error("--predicted-labels only applies to predicted-label")
    if args.out.exists() and any(args.out.iterdir()):
        parser.error(f"refusing to overwrite non-empty pilot directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(HERE / "c2ges_learnable.py"),
        "--data", str(args.data),
        "--out", str(args.out),
        "--protocol", args.protocol,
        "--train-limit", str(args.train_limit),
        "--dev-limit", str(args.dev_limit),
        "--test-limit", str(args.test_limit),
        "--epochs", str(args.epochs),
        "--bootstrap-samples", str(args.bootstrap_samples),
        "--eval-k", "1,3,5,10",
        "--train-k", "3",
        "--seed", str(args.seed),
        "--device", args.device,
    ]
    if args.predicted_labels:
        command.extend(["--predicted-labels", str(args.predicted_labels)])

    stdout_path = args.out / "process_stdout.log"
    stderr_path = args.out / "process_stderr.log"
    started_utc = utc_now()
    started = time.perf_counter()
    min_system_available = psutil.virtual_memory().available
    peak_tree_rss = 0
    peak_process_count = 0
    samples = 0
    failure = None
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr, text=True)
        root = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                processes = [root, *root.children(recursive=True)]
                rss = sum(item.memory_info().rss for item in processes if item.is_running())
                peak_tree_rss = max(peak_tree_rss, rss)
                peak_process_count = max(peak_process_count, len(processes))
                min_system_available = min(min_system_available, psutil.virtual_memory().available)
                samples += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            time.sleep(args.sample_interval)
        exit_code = process.wait()
    wall_seconds = time.perf_counter() - started
    if exit_code != 0:
        failure = {"exit_code": exit_code, "message": "c2ges_learnable subprocess failed; inspect process_stderr.log"}
    record = {
        "protocol": args.protocol,
        "status": "success" if exit_code == 0 else "failed",
        "failure": failure,
        "command": command,
        "started_utc": started_utc,
        "finished_utc": utc_now(),
        "wall_seconds": wall_seconds,
        "resource_sampling": {
            "method": "psutil RSS sum over runner process tree",
            "sample_interval_seconds": args.sample_interval,
            "samples": samples,
            "peak_tree_rss_bytes": peak_tree_rss,
            "peak_tree_rss_gib": peak_tree_rss / 1024**3,
            "peak_process_count": peak_process_count,
            "minimum_system_available_memory_bytes": min_system_available,
            "minimum_system_available_memory_gib": min_system_available / 1024**3,
            "limitations": "RSS polling may miss sub-interval spikes; GPU memory is not measured; concurrent system workloads affect available-memory readings.",
        },
        "logs": {
            "stdout_sha256": hashlib.sha256(stdout_path.read_bytes()).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr_path.read_bytes()).hexdigest(),
        },
    }
    (args.out / "resource_usage.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(record, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
