#!/usr/bin/env python3
"""Read-mostly orchestration and integrity checks for paper portfolios."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


VALID_STATUS = {"complete", "pending", "blocked", "optional", "superseded"}


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    message: str


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("profile root must be a JSON object")
    return value


def profile_context(profile_path: Path) -> Tuple[Dict[str, Any], Path, Path]:
    profile_path = profile_path.resolve()
    profile = read_json(profile_path)
    workspace_value = profile.get("workspace_root")
    if not isinstance(workspace_value, str) or not workspace_value:
        raise ValueError("workspace_root must be a non-empty string")
    workspace = (profile_path.parent / workspace_value).resolve()
    return profile, profile_path, workspace


def resolve_path(workspace: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate.resolve()
    return (workspace / candidate).resolve()


def is_within(candidate: Path, parent: Path) -> bool:
    try:
        candidate.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _require_list(profile: Dict[str, Any], key: str, issues: List[Issue]) -> list:
    value = profile.get(key)
    if not isinstance(value, list):
        issues.append(Issue("ERROR", "SCHEMA", f"{key} must be a list"))
        return []
    return value


def topological_stages(stages: Sequence[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Issue]]:
    issues: List[Issue] = []
    by_id: Dict[str, Dict[str, Any]] = {}
    for stage in stages:
        if not isinstance(stage, dict):
            issues.append(Issue("ERROR", "STAGE_SCHEMA", "each stage must be an object"))
            continue
        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id:
            issues.append(Issue("ERROR", "STAGE_SCHEMA", "each stage requires a non-empty id"))
            continue
        if stage_id in by_id:
            issues.append(Issue("ERROR", "DUPLICATE_STAGE", stage_id))
        by_id[stage_id] = stage

    incoming: Dict[str, int] = {stage_id: 0 for stage_id in by_id}
    outgoing: Dict[str, List[str]] = {stage_id: [] for stage_id in by_id}
    for stage_id, stage in by_id.items():
        dependencies = stage.get("depends_on", [])
        if not isinstance(dependencies, list) or not all(isinstance(item, str) for item in dependencies):
            issues.append(Issue("ERROR", "STAGE_SCHEMA", f"{stage_id}.depends_on must be a string list"))
            continue
        for dependency in dependencies:
            if dependency not in by_id:
                issues.append(Issue("ERROR", "UNKNOWN_DEPENDENCY", f"{stage_id} -> {dependency}"))
                continue
            incoming[stage_id] += 1
            outgoing[dependency].append(stage_id)

    queue = [stage_id for stage_id in by_id if incoming[stage_id] == 0]
    ordered: List[Dict[str, Any]] = []
    while queue:
        stage_id = queue.pop(0)
        ordered.append(by_id[stage_id])
        for next_id in outgoing[stage_id]:
            incoming[next_id] -= 1
            if incoming[next_id] == 0:
                queue.append(next_id)
    if len(ordered) != len(by_id):
        issues.append(Issue("ERROR", "STAGE_CYCLE", "stage graph contains a cycle"))
    return ordered, issues


def audit_profile(profile: Dict[str, Any], workspace: Path) -> List[Issue]:
    issues: List[Issue] = []
    for key in ("schema_version", "portfolio_id", "workspace_root", "authority"):
        if key not in profile:
            issues.append(Issue("ERROR", "SCHEMA", f"missing top-level key: {key}"))
    if profile.get("schema_version") != "1.0":
        issues.append(Issue("ERROR", "SCHEMA_VERSION", "schema_version must be 1.0"))
    if not workspace.is_dir():
        issues.append(Issue("ERROR", "WORKSPACE", f"workspace does not exist: {workspace}"))

    papers = _require_list(profile, "papers", issues)
    stages = _require_list(profile, "stages", issues)
    _require_list(profile, "hard_rules", issues)
    _require_list(profile, "manual_gates", issues)

    paper_ids = set()
    for paper in papers:
        if not isinstance(paper, dict):
            issues.append(Issue("ERROR", "PAPER_SCHEMA", "each paper must be an object"))
            continue
        paper_id = paper.get("id")
        if not isinstance(paper_id, str) or not paper_id:
            issues.append(Issue("ERROR", "PAPER_SCHEMA", "paper id is required"))
            continue
        if paper_id in paper_ids:
            issues.append(Issue("ERROR", "DUPLICATE_PAPER", paper_id))
        paper_ids.add(paper_id)
        for key in ("title", "target", "manuscript", "pdf", "evidence_root"):
            if not isinstance(paper.get(key), str) or not paper[key]:
                issues.append(Issue("ERROR", "PAPER_SCHEMA", f"{paper_id}.{key} is required"))
        for key in ("manuscript", "pdf", "evidence_root"):
            value = paper.get(key)
            if isinstance(value, str) and value:
                path = resolve_path(workspace, value)
                if not path.exists():
                    issues.append(Issue("ERROR", "MISSING_PAPER_ASSET", f"{paper_id}: {value}"))

    ordered, graph_issues = topological_stages(stages)
    issues.extend(graph_issues)
    stage_status = {stage.get("id"): stage.get("status") for stage in stages if isinstance(stage, dict)}
    for stage in stages:
        if not isinstance(stage, dict) or not isinstance(stage.get("id"), str):
            continue
        stage_id = stage["id"]
        if stage.get("status") not in VALID_STATUS:
            issues.append(Issue("ERROR", "STAGE_STATUS", f"{stage_id}: {stage.get('status')}"))
        if not isinstance(stage.get("auto_safe"), bool):
            issues.append(Issue("ERROR", "STAGE_SCHEMA", f"{stage_id}.auto_safe must be boolean"))
        for dependency in stage.get("depends_on", []):
            if stage.get("status") == "complete" and stage_status.get(dependency) in {"pending", "blocked"}:
                issues.append(Issue("ERROR", "UNSATISFIED_DEPENDENCY", f"{stage_id} depends on {dependency}"))
        artifacts = stage.get("artifacts", [])
        if not isinstance(artifacts, list) or not all(isinstance(item, str) for item in artifacts):
            issues.append(Issue("ERROR", "STAGE_SCHEMA", f"{stage_id}.artifacts must be a string list"))
        elif stage.get("status") == "complete":
            for value in artifacts:
                if not resolve_path(workspace, value).exists():
                    issues.append(Issue("ERROR", "MISSING_STAGE_ARTIFACT", f"{stage_id}: {value}"))
        commands = stage.get("commands", [])
        if not isinstance(commands, list):
            issues.append(Issue("ERROR", "COMMAND_SCHEMA", f"{stage_id}.commands must be a list"))
        else:
            for index, command in enumerate(commands):
                argv = command.get("argv") if isinstance(command, dict) else None
                if not isinstance(argv, list) or not argv or not all(isinstance(arg, str) for arg in argv):
                    issues.append(Issue("ERROR", "COMMAND_SCHEMA", f"{stage_id}.commands[{index}].argv"))

    authority = profile.get("authority")
    if not isinstance(authority, dict):
        issues.append(Issue("ERROR", "AUTHORITY_SCHEMA", "authority must be an object"))
        return issues
    for key in ("canonical_roots", "legacy_roots", "incident_roots", "required_paths", "expected_hashes"):
        if not isinstance(authority.get(key), list):
            issues.append(Issue("ERROR", "AUTHORITY_SCHEMA", f"authority.{key} must be a list"))

    canonical = [resolve_path(workspace, value) for value in authority.get("canonical_roots", []) if isinstance(value, str)]
    excluded = [resolve_path(workspace, value) for key in ("legacy_roots", "incident_roots") for value in authority.get(key, []) if isinstance(value, str)]
    for root in canonical:
        if not root.exists():
            issues.append(Issue("ERROR", "MISSING_CANONICAL_ROOT", str(root)))
        for forbidden in excluded:
            if is_within(root, forbidden) or is_within(forbidden, root):
                issues.append(Issue("ERROR", "AUTHORITY_OVERLAP", f"canonical={root}; excluded={forbidden}"))

    for value in authority.get("required_paths", []):
        if isinstance(value, str) and not resolve_path(workspace, value).exists():
            issues.append(Issue("ERROR", "MISSING_REQUIRED_PATH", value))

    for entry in authority.get("expected_hashes", []):
        if not isinstance(entry, dict):
            issues.append(Issue("ERROR", "HASH_SCHEMA", "expected_hashes entry must be an object"))
            continue
        value, expected = entry.get("path"), entry.get("sha256")
        if not isinstance(value, str) or not isinstance(expected, str) or len(expected) != 64:
            issues.append(Issue("ERROR", "HASH_SCHEMA", str(entry)))
            continue
        path = resolve_path(workspace, value)
        if not path.is_file():
            issues.append(Issue("ERROR", "MISSING_HASH_TARGET", value))
            continue
        actual = sha256_file(path)
        if actual != expected.upper():
            issues.append(Issue("ERROR", "HASH_MISMATCH", f"{value}: expected {expected.upper()}, got {actual}"))

    if ordered and not issues:
        issues.append(Issue("INFO", "PASS", f"{len(papers)} papers; {len(ordered)} stages; authority and hashes verified"))
    return issues


def print_issues(issues: Iterable[Issue]) -> None:
    for issue in issues:
        print(f"[{issue.level}] {issue.code}: {issue.message}")


def command_check(profile_path: Path) -> int:
    profile, _, workspace = profile_context(profile_path)
    issues = audit_profile(profile, workspace)
    print_issues(issues)
    return 1 if any(issue.level == "ERROR" for issue in issues) else 0


def command_status(profile_path: Path) -> int:
    profile, _, workspace = profile_context(profile_path)
    issues = audit_profile(profile, workspace)
    print(f"Portfolio: {profile.get('portfolio_id')}")
    print(f"Workspace: {workspace}")
    for stage in profile.get("stages", []):
        print(f"{stage.get('id', '?'):28} {stage.get('status', '?'):11} {stage.get('title', '')}")
    errors = [issue for issue in issues if issue.level == "ERROR"]
    print(f"Integrity errors: {len(errors)}")
    return 1 if errors else 0


def command_plan(profile_path: Path) -> int:
    profile, _, _ = profile_context(profile_path)
    ordered, issues = topological_stages(profile.get("stages", []))
    print_issues(issues)
    if issues:
        return 1
    for number, stage in enumerate(ordered, 1):
        safety = "auto-safe" if stage.get("auto_safe") else "manual/authorized"
        print(f"{number:02d}. {stage['id']} [{stage.get('status')}; {safety}]")
        print(f"    gate: {stage.get('gate', '')}")
        for command in stage.get("commands", []):
            print("    command: " + subprocess.list2cmdline(command["argv"]))
            if command.get("note"):
                print("    note: " + command["note"])
    return 0


def build_manifest(profile: Dict[str, Any], workspace: Path) -> Dict[str, Any]:
    entries = []
    for value in profile.get("manifest_paths", []):
        path = resolve_path(workspace, value)
        entry: Dict[str, Any] = {"path": value.replace("\\", "/")}
        if path.is_file():
            entry.update({"type": "file", "bytes": path.stat().st_size, "sha256": sha256_file(path)})
        elif path.is_dir():
            entry.update({"type": "directory"})
        else:
            entry.update({"type": "missing"})
        entries.append(entry)
    return {
        "schema_version": "1.0",
        "portfolio_id": profile.get("portfolio_id"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entries": entries,
    }


def command_manifest(profile_path: Path, output: Path | None) -> int:
    profile, _, workspace = profile_context(profile_path)
    manifest = build_manifest(profile, workspace)
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        print(rendered, end="")
        return 0
    output = output.resolve()
    if output.exists():
        print(f"refusing to overwrite existing manifest: {output}", file=sys.stderr)
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(rendered)
    print(output)
    return 0


def command_run_stage(profile_path: Path, stage_id: str, execute: bool) -> int:
    profile, _, workspace = profile_context(profile_path)
    issues = audit_profile(profile, workspace)
    errors = [issue for issue in issues if issue.level == "ERROR"]
    if errors:
        print_issues(errors)
        return 1
    stages = {stage["id"]: stage for stage in profile.get("stages", [])}
    stage = stages.get(stage_id)
    if stage is None:
        print(f"unknown stage: {stage_id}", file=sys.stderr)
        return 2
    commands = stage.get("commands", [])
    if not commands:
        print(f"stage has no command: {stage_id}")
        return 0
    for command in commands:
        argv = command["argv"]
        cwd = resolve_path(workspace, command.get("cwd", "."))
        print(f"cwd={cwd}")
        print(subprocess.list2cmdline(argv))
    if not execute:
        print("dry run only; add --execute to run an auto-safe stage")
        return 0
    if not stage.get("auto_safe"):
        print(f"refusing to execute manual/authorized stage: {stage_id}", file=sys.stderr)
        return 3
    for command in commands:
        cwd = resolve_path(workspace, command.get("cwd", "."))
        completed = subprocess.run(command["argv"], cwd=str(cwd), check=False, env=os.environ.copy())
        if completed.returncode != 0:
            return completed.returncode
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    for name in ("check", "status", "plan"):
        child = subparsers.add_parser(name)
        child.add_argument("--profile", type=Path, required=True)
    manifest = subparsers.add_parser("manifest")
    manifest.add_argument("--profile", type=Path, required=True)
    manifest.add_argument("--write", type=Path)
    run_stage = subparsers.add_parser("run-stage")
    run_stage.add_argument("--profile", type=Path, required=True)
    run_stage.add_argument("--stage", required=True)
    run_stage.add_argument("--execute", action="store_true")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "check":
            return command_check(args.profile)
        if args.command == "status":
            return command_status(args.profile)
        if args.command == "plan":
            return command_plan(args.profile)
        if args.command == "manifest":
            return command_manifest(args.profile, args.write)
        if args.command == "run-stage":
            return command_run_stage(args.profile, args.stage, args.execute)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"harness error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

