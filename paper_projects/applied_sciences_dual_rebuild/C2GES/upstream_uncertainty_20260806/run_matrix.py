#!/usr/bin/env python3
"""Execute a frozen upstream-by-downstream seed matrix for C2GES.

This wrapper never edits, retries, or replaces a completed child run. It builds
five document-grouped OOF role ledgers and binds each ledger to five downstream
training seeds. The resulting 25 pipelines quantify uncertainty omitted when a
single upstream ledger is reused by every downstream seed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / "paper_projects").is_dir())
CODE = ROOT / "paper_projects/2026_c2ges_engineeringletters/source/code"
DATA = ROOT / "paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark_document_grouped"
PREDICTOR = CODE / "predict_fever_labels.py"
SELECTOR = CODE / "c2ges_learnable.py"
FREEZE = HERE / "PROTOCOL_FREEZE.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def assert_freeze() -> dict:
    if not FREEZE.is_file():
        raise RuntimeError(f"missing protocol freeze: {FREEZE}")
    freeze = read_json(FREEZE)
    if freeze.get("status") != "FROZEN_NOT_RUN":
        raise RuntimeError("protocol status is not FROZEN_NOT_RUN")
    for label, path in (("predictor", PREDICTOR), ("selector", SELECTOR), ("runner", Path(__file__))):
        expected = freeze["code_sha256"][label]
        observed = sha256(path)
        if observed != expected:
            raise RuntimeError(f"{label} hash drift: {observed} != {expected}")
    manifest = DATA / "manifest.json"
    if sha256(manifest) != freeze["data_manifest_sha256"]:
        raise RuntimeError("data manifest hash drift")
    return freeze


def command_plan(out: Path, freeze: dict) -> list[dict]:
    upstream_seeds = [int(value) for value in freeze["upstream_seeds"]]
    downstream_seeds = [int(value) for value in freeze["downstream_seeds"]]
    rows: list[dict] = []
    for upstream_seed in upstream_seeds:
        upstream_out = out / "upstream" / f"seed_{upstream_seed}"
        rows.append(
            {
                "kind": "upstream",
                "upstream_seed": upstream_seed,
                "downstream_seed": None,
                "output": str(upstream_out),
                "command": [
                    sys.executable,
                    str(PREDICTOR),
                    "--data", str(DATA),
                    "--out", str(upstream_out),
                    "--seed", str(upstream_seed),
                    "--folds", str(freeze["upstream_folds"]),
                    "--train-limit", str(freeze["limits"]["train"]),
                    "--dev-limit", str(freeze["limits"]["dev"]),
                    "--test-limit", str(freeze["limits"]["test"]),
                ],
            }
        )
        for downstream_seed in downstream_seeds:
            run_out = out / "runs" / f"up_{upstream_seed}" / f"down_{downstream_seed}"
            rows.append(
                {
                    "kind": "downstream",
                    "upstream_seed": upstream_seed,
                    "downstream_seed": downstream_seed,
                    "output": str(run_out),
                    "command": [
                        sys.executable,
                        str(SELECTOR),
                        "--data", str(DATA),
                        "--out", str(run_out),
                        "--encoder", freeze["encoder"],
                        "--train-limit", str(freeze["limits"]["train"]),
                        "--dev-limit", str(freeze["limits"]["dev"]),
                        "--test-limit", str(freeze["limits"]["test"]),
                        "--epochs", str(freeze["epochs"]),
                        "--lr", str(freeze["learning_rate"]),
                        "--seed", str(downstream_seed),
                        "--device", freeze["device"],
                        "--train-k", str(freeze["primary_k"]),
                        "--eval-k", ",".join(str(value) for value in freeze["cutoffs"]),
                        "--bootstrap-samples", str(freeze["child_bootstrap_samples"]),
                        "--protocol", "predicted-label",
                        "--predicted-labels", str(upstream_out / "predicted_labels.json"),
                    ],
                }
            )
    return rows


def validate_plan(plan: list[dict], freeze: dict) -> None:
    expected_upstream = len(freeze["upstream_seeds"])
    expected_downstream = expected_upstream * len(freeze["downstream_seeds"])
    if sum(row["kind"] == "upstream" for row in plan) != expected_upstream:
        raise RuntimeError("upstream plan cardinality mismatch")
    if sum(row["kind"] == "downstream" for row in plan) != expected_downstream:
        raise RuntimeError("downstream plan cardinality mismatch")
    outputs = [row["output"] for row in plan]
    if len(outputs) != len(set(outputs)):
        raise RuntimeError("duplicate output directory in plan")


def run_one(row: dict, logs: Path, env: dict[str, str]) -> dict:
    output = Path(row["output"])
    if output.exists():
        raise RuntimeError(f"refusing existing child output: {output}")
    log_stem = (
        f"up_{row['upstream_seed']}"
        if row["kind"] == "upstream"
        else f"up_{row['upstream_seed']}_down_{row['downstream_seed']}"
    )
    started = time.time()
    with (logs / f"{log_stem}.stdout.log").open("wb") as stdout, (logs / f"{log_stem}.stderr.log").open("wb") as stderr:
        completed = subprocess.run(row["command"], cwd=ROOT, env=env, stdout=stdout, stderr=stderr, check=False)
    record = {
        **{key: row[key] for key in ("kind", "upstream_seed", "downstream_seed", "output", "command")},
        "returncode": completed.returncode,
        "wall_seconds": time.time() - started,
    }
    if completed.returncode != 0:
        raise RuntimeError(f"child failed and was retained: {log_stem}, returncode={completed.returncode}")
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    freeze = assert_freeze()
    out = args.out.resolve()
    if out.exists():
        raise RuntimeError(f"refusing existing formal output root: {out}")
    plan = command_plan(out, freeze)
    validate_plan(plan, freeze)
    if not args.execute:
        print(json.dumps({"status": "PREFLIGHT_PASS_NOT_RUN", "commands": len(plan), "plan": plan}, indent=2))
        return 0

    out.mkdir(parents=True)
    logs = out / "logs"
    logs.mkdir()
    write_json(out / "execution_plan.json", plan)
    write_json(
        out / "provenance.json",
        {
            "freeze_sha256": sha256(FREEZE),
            "runner_sha256": sha256(Path(__file__)),
            "python": sys.version,
            "platform": platform.platform(),
            "started_unix": time.time(),
        },
    )
    env = os.environ.copy()
    env.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"})
    records = []
    try:
        for row in plan:
            records.append(run_one(row, logs, env))
            write_json(out / "completed_children.json", records)
    except Exception as exc:
        write_json(out / "incident.json", {"error": str(exc), "completed": len(records), "time_unix": time.time()})
        raise
    write_json(
        out / "SUCCESS.json",
        {
            "status": "success",
            "upstream_ledgers": len(freeze["upstream_seeds"]),
            "downstream_runs": len(freeze["upstream_seeds"]) * len(freeze["downstream_seeds"]),
            "completed_children": len(records),
            "finished_unix": time.time(),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
