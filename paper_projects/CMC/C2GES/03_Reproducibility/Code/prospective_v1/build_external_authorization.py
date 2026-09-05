#!/usr/bin/env python3
"""Build a complete C2GES external-run authorization after human freeze.

This utility never changes protocol, tuning, audit, or dataset files.  It first
checks that the human-controlled records already say FROZEN/PASS.  Only then,
and only with the explicit administrator acknowledgement flag, does it hash the
private dataset and emit a new immutable authorization file.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from external_confirmatory import (
    MODE,
    REQUIRED_CODE_FILES,
    SCHEMA,
    load_json,
    read_inventory,
    read_seen_exclusions,
    find_seen_overlaps,
    sha256,
    utc_now,
    validate_ablation_registry,
    validate_config,
)


def require_state(record: dict[str, Any], path: Path, *, field: str, value: Any) -> None:
    if record.get(field) != value:
        raise RuntimeError(f"{path.name}: {field} must equal {value!r} before authorization")


def validate_layout_audit(path: Path) -> None:
    record = load_json(path)
    require_state(record, path, field="status", value="PASS")
    if float(record.get("candidate_validity_rate", -1)) < 0.90:
        raise RuntimeError("layout audit candidate_validity_rate is below 0.90")
    if float(record.get("table_body_fusion_rate", 1)) > 0.05:
        raise RuntimeError("layout audit table_body_fusion_rate exceeds 0.05")
    if int(record.get("independent_reviewers", 0)) < 2:
        raise RuntimeError("layout audit requires two independent reviewers")


def build(args: argparse.Namespace) -> dict[str, Any]:
    if args.authorization_output.exists():
        raise FileExistsError(f"refusing existing authorization output: {args.authorization_output}")
    if args.output_dir.exists():
        raise FileExistsError(f"formal output directory already exists: {args.output_dir}")
    if args.attempt_registry.exists():
        raise FileExistsError(f"attempt registry already exists: {args.attempt_registry}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,80}", args.run_id):
        raise ValueError("run-id must be a stable 3--81 character slug")
    if not args.operator.strip():
        raise ValueError("operator identity/role is required")

    config = load_json(args.config)
    external = load_json(args.external_protocol)
    factorial = load_json(args.factorial_protocol)
    tuning = load_json(args.tuning_decision)
    validate_config(config)
    require_state(external, args.external_protocol, field="protocol_status", value="FROZEN")
    require_state(external, args.external_protocol, field="execution_allowed", value=True)
    require_state(external, args.external_protocol, field="external_test_accessed", value=False)
    require_state(factorial, args.factorial_protocol, field="protocol_status", value="FROZEN")
    require_state(factorial, args.factorial_protocol, field="execution_allowed", value=True)
    require_state(tuning, args.tuning_decision, field="status", value="FROZEN")
    require_state(tuning, args.tuning_decision, field="external_test_accessed", value=False)
    if tuning.get("selected") != config.get("tuning_selected"):
        raise RuntimeError("config tuning_selected differs from the frozen tuning decision")
    ablation = load_json(args.ablation_registry)
    validate_ablation_registry(ablation, config)
    validate_layout_audit(args.layout_audit_summary)
    inventory = read_inventory(args.inventory)
    exclusions = read_seen_exclusions(args.seen_exclusion_registry)
    overlaps = find_seen_overlaps(inventory, exclusions)
    if overlaps:
        raise RuntimeError(f"external inventory overlaps the seen-exclusion registry: {overlaps}")
    if len(inventory) != int(config["expected_reports"]):
        raise RuntimeError("inventory count differs from frozen expected_reports")
    if len({row["report_series_id"] for row in inventory}) != int(config["expected_series"]):
        raise RuntimeError("inventory series count differs from frozen expected_series")

    if not args.administrator_confirms_no_content_review:
        raise RuntimeError("private dataset hashing requires --administrator-confirms-no-content-review")
    if not args.dataset.is_file():
        raise FileNotFoundError(args.dataset)
    if not args.model_snapshot.is_dir() or args.model_snapshot.name != config["model_revision"]:
        raise RuntimeError("model snapshot is missing or revision directory differs from config")

    hashes = {
        "config": sha256(args.config),
        "external_protocol": sha256(args.external_protocol),
        "factorial_protocol": sha256(args.factorial_protocol),
        "tuning_decision": sha256(args.tuning_decision),
        "tuning_grid": sha256(args.tuning_grid),
        "inventory": sha256(args.inventory),
        "seen_exclusion_registry": sha256(args.seen_exclusion_registry),
        "layout_candidate_audit": sha256(args.layout_candidate_audit),
        "layout_audit_summary": sha256(args.layout_audit_summary),
        "ablation_registry": sha256(args.ablation_registry),
        "dataset": sha256(args.dataset),
    }
    expected_external = {
        "config_sha256": hashes["config"],
        "dataset_sha256": hashes["dataset"],
        "inventory_sha256": hashes["inventory"],
        "seen_exclusion_registry_sha256": hashes["seen_exclusion_registry"],
        "layout_candidate_audit_sha256": hashes["layout_candidate_audit"],
        "layout_audit_summary_sha256": hashes["layout_audit_summary"],
        "tuning_grid_sha256": hashes["tuning_grid"],
        "tuning_decision_sha256": hashes["tuning_decision"],
    }
    if external.get("freeze_bindings") != expected_external:
        raise RuntimeError("external protocol freeze_bindings do not match current inputs")
    expected_factorial = {
        "config_sha256": hashes["config"],
        "ablation_registry_sha256": hashes["ablation_registry"],
    }
    if factorial.get("freeze_bindings") != expected_factorial:
        raise RuntimeError("factorial protocol freeze_bindings do not match current inputs")

    code_files = []
    workspace = Path(__file__).resolve().parents[6]
    for relative in sorted(REQUIRED_CODE_FILES):
        path = workspace / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        code_files.append({"path": relative, "sha256": sha256(path)})
    model_files = [
        {"path": path.relative_to(args.model_snapshot).as_posix(), "sha256": sha256(path)}
        for path in sorted((path for path in args.model_snapshot.rglob("*") if path.is_file()), key=lambda path: path.relative_to(args.model_snapshot).as_posix())
    ]
    if not model_files:
        raise RuntimeError("model snapshot contains no files")

    authorization = {
        "schema": SCHEMA,
        "status": "AUTHORIZED",
        "mode": MODE,
        "run_id": args.run_id,
        "operator": args.operator,
        "authorized_at": utc_now(),
        "execution_allowed": True,
        "external_test_accessed": False,
        "administrator_confirmation": "metadata/hashing only; no report-body or reference-outcome review",
        "paths": {
            "config": str(args.config.resolve()),
            "external_protocol": str(args.external_protocol.resolve()),
            "factorial_protocol": str(args.factorial_protocol.resolve()),
            "tuning_decision": str(args.tuning_decision.resolve()),
            "tuning_grid": str(args.tuning_grid.resolve()),
            "inventory": str(args.inventory.resolve()),
            "seen_exclusion_registry": str(args.seen_exclusion_registry.resolve()),
            "layout_candidate_audit": str(args.layout_candidate_audit.resolve()),
            "layout_audit_summary": str(args.layout_audit_summary.resolve()),
            "ablation_registry": str(args.ablation_registry.resolve()),
            "dataset": str(args.dataset.resolve()),
            "model_snapshot": str(args.model_snapshot.resolve()),
            "output_dir": str(args.output_dir.resolve()),
            "attempt_registry": str(args.attempt_registry.resolve()),
        },
        "sha256": hashes,
        "code_files": code_files,
        "model_snapshot_files": model_files,
    }
    args.authorization_output.parent.mkdir(parents=True, exist_ok=True)
    with args.authorization_output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(authorization, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return authorization


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("config", "external-protocol", "factorial-protocol", "tuning-decision", "tuning-grid", "inventory", "seen-exclusion-registry", "layout-candidate-audit", "layout-audit-summary", "ablation-registry", "dataset", "model-snapshot", "output-dir", "attempt-registry", "authorization-output"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--operator", required=True)
    parser.add_argument("--administrator-confirms-no-content-review", action="store_true")
    args = parser.parse_args()
    result = build(args)
    print(json.dumps({"status": result["status"], "run_id": result["run_id"], "authorization": str(args.authorization_output), "authorization_sha256": sha256(args.authorization_output)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
