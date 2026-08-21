#!/usr/bin/env python3
"""Release wrapper that binds provenance/tests around unchanged v2 rules."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

import offline_coordination_study_v2 as core


ROOT = core.ROOT
SCRIPT = Path(__file__).resolve()
HERE = SCRIPT.parent
BUILDER = HERE / "build_metamorphic_witnesses_v3.py"
CORE = HERE / "offline_coordination_study_v2.py"
AGENTS = HERE / "ma_sqlgrid_agents.py"
EXECUTOR = HERE / "sqlite_readonly_executor.py"
TEST_DIR = HERE / "tests"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def file_record(path: Path) -> dict[str, Any]:
    path = path.resolve(strict=True)
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}


def make_config(base_config: Path, witness_dir: Path, freeze_dir: Path) -> Path:
    config = json.loads(base_config.read_text(encoding="utf-8"))
    config["schema_version"] = "ma-sqlgrid-offline-coordination-selection-v3"
    config["study_label"] = "release-v3 prospective-from-freeze offline coordination selection study"
    config["selector_inputs"]["witness_directory"] = witness_dir.relative_to(ROOT).as_posix()
    config["selector_inputs"]["witness_manifest"] = (witness_dir / "WITNESS_MANIFEST.json").relative_to(ROOT).as_posix()
    path = freeze_dir / "study_config_v3.json"
    core.write_json(path, config)
    return path


def run_prefreeze_tests(result_path: Path) -> list[Path]:
    test_files = sorted(TEST_DIR.glob("test_*.py"))
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(TEST_DIR), "-v"]
    completed = subprocess.run(command, cwd=HERE, text=True, capture_output=True)
    report = {
        "schema_version": "ma-sqlgrid-v3-prefreeze-tests-v1",
        "created_at_utc": now_utc(),
        "command": command,
        "working_directory": HERE.relative_to(ROOT).as_posix(),
        "returncode": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest(),
        "passed": completed.returncode == 0,
    }
    core.write_json(result_path, report)
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout + "\n" + completed.stderr)
    return test_files


def freeze(base_config: Path, witness_dir: Path, freeze_dir: Path) -> None:
    if freeze_dir.exists():
        raise FileExistsError(f"freeze directory exists; refusing overwrite: {freeze_dir}")
    freeze_dir.mkdir(parents=True)
    created_at_utc = now_utc()
    config_path = make_config(base_config, witness_dir, freeze_dir)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    selection_path = freeze_dir / "selection_inputs.jsonl"
    core.write_jsonl(selection_path, core.selection_view_from_prompts(core.resolved(config, "qwen_prompts")))
    test_result = freeze_dir / "prefreeze_test_result.json"
    test_files = run_prefreeze_tests(test_result)

    files: dict[str, dict[str, Any]] = {}
    for key in ["qwen_prompts", "schema_sql", "qwen_predictions", "granite_predictions", "reference_database", "witness_manifest"]:
        files[key] = file_record(core.resolved(config, key))
    for state in config["reference_free_states"]:
        files[f"state:{state}"] = file_record(witness_dir / f"{state}.sqlite")
    fixed = {
        "config": config_path,
        "release_runner": SCRIPT,
        "core_runner": CORE,
        "witness_builder": BUILDER,
        "agents_code": AGENTS,
        "executor_code": EXECUTOR,
        "selection_inputs": selection_path,
        "prefreeze_test_result": test_result,
    }
    for key, path in fixed.items():
        files[key] = file_record(path)
    for test_file in test_files:
        files[f"test:{test_file.name}"] = file_record(test_file)

    witness_manifest = json.loads((witness_dir / "WITNESS_MANIFEST.json").read_text(encoding="utf-8"))
    manifest = {
        "schema_version": "ma-sqlgrid-offline-coordination-freeze-v3",
        "status": "FROZEN_BEFORE_V3_SELECTION_AND_GOLD_EVALUATION",
        "created_at_utc": created_at_utc,
        "study_label": config["study_label"],
        "question_count": 180,
        "candidate_slots_per_question": 8,
        "states_per_candidate": 4,
        "no_llm_calls": True,
        "gold_selection_access": False,
        "gold_binding_recorded_without_opening": config["evaluation_after_seal"],
        "witness_manifest_content_sha256": witness_manifest["manifest_content_sha256"],
        "files": files,
    }
    manifest["freeze_content_sha256"] = canonical_hash(manifest)
    core.write_json(freeze_dir / "freeze_manifest.json", manifest)
    print(json.dumps({"freeze_content_sha256": manifest["freeze_content_sha256"], "file_count": len(files)}, sort_keys=True))


def run(config_path: Path, freeze_dir: Path, run_dir: Path) -> None:
    started_at_utc = now_utc()
    core.run(config_path, freeze_dir, run_dir)
    files = {p.name: file_record(p) for p in sorted(run_dir.iterdir()) if p.is_file()}
    manifest = {
        "schema_version": "ma-sqlgrid-offline-run-release-v3",
        "status": "COMPLETED_NO_OVERWRITE",
        "created_at_utc": started_at_utc,
        "completed_at_utc": now_utc(),
        "freeze_content_sha256": json.loads((freeze_dir / "freeze_manifest.json").read_text(encoding="utf-8"))["freeze_content_sha256"],
        "runtime": {"python": platform.python_version()},
        "files": files,
    }
    manifest["run_manifest_content_sha256"] = canonical_hash(manifest)
    core.write_json(run_dir / "run_release_manifest_v3.json", manifest)


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p_freeze = sub.add_parser("freeze")
    p_freeze.add_argument("--base-config", type=Path, required=True)
    p_freeze.add_argument("--witness-dir", type=Path, required=True)
    p_freeze.add_argument("--freeze-dir", type=Path, required=True)
    p_run = sub.add_parser("run")
    p_run.add_argument("--config", type=Path, required=True)
    p_run.add_argument("--freeze-dir", type=Path, required=True)
    p_run.add_argument("--run-dir", type=Path, required=True)
    p_compare = sub.add_parser("compare")
    p_compare.add_argument("--run-a", type=Path, required=True)
    p_compare.add_argument("--run-b", type=Path, required=True)
    p_compare.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "freeze":
        freeze(args.base_config.resolve(strict=True), args.witness_dir.resolve(strict=True), args.freeze_dir.resolve())
    elif args.command == "run":
        run(args.config.resolve(strict=True), args.freeze_dir.resolve(strict=True), args.run_dir.resolve())
    else:
        core.compare(args.run_a.resolve(strict=True), args.run_b.resolve(strict=True), args.out.resolve())


if __name__ == "__main__":
    main()
