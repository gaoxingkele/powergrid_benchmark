#!/usr/bin/env python3
"""Freeze and reproduce the independently audited MA-SQLGrid R2 v2 study.

This study performs no model calls. It applies prospectively frozen selectors
to the historical eight-slot candidate pool and opens the gold-bearing question
file only after all 180 blackboards have been sealed and written.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import random
import re
import sqlite3
import sys
from typing import Any, Iterable, Mapping, Sequence

from ma_sqlgrid_agents import (
    Adjudicator,
    Blackboard,
    CounterfactualCritic,
    Decision,
    QueryAnalyst,
    SQLCandidate,
    SchemaCartographer,
    ValidationEvidence,
)
from sqlite_readonly_executor import SQLiteReadOnlyExecutor


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = Path(__file__).resolve()
AGENTS = SCRIPT.with_name("ma_sqlgrid_agents.py")
EXECUTOR = SCRIPT.with_name("sqlite_readonly_executor.py")
CONDITIONS = ["F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape"]
METHODS = ["fixed_order_equal_budget", "validation_rank_equal_budget_no_cf", "full_coordination_complete_metamorphic"]
FORBIDDEN_SELECTION_FIELDS = {
    "gold_sql", "answer_shape", "order_sensitive", "required_value_literals",
    "difficulty", "sql_feature_tags", "tables", "columns",
}
ORDER_RE = re.compile(r"\border\s+by\b", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(dict(row), ensure_ascii=False, sort_keys=True) + "\n")


def resolved(config: Mapping[str, Any], key: str) -> Path:
    return ROOT / config["selector_inputs"][key]


def parse_schema(path: Path) -> dict[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    schema: dict[str, list[str]] = {}
    for match in re.finditer(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[\"`\[]?([A-Za-z_][\w]*)[\"`\]]?\s*\((.*?)\)\s*;", text, re.I | re.S):
        table, body = match.group(1), match.group(2)
        columns: list[str] = []
        for fragment in body.split(","):
            token = fragment.strip().split(None, 1)[0].strip('"`[]') if fragment.strip() else ""
            if token and token.upper() not in {"PRIMARY", "FOREIGN", "UNIQUE", "CHECK", "CONSTRAINT"}:
                columns.append(token)
        schema[table] = columns
    if not schema:
        raise RuntimeError("schema parser found no tables")
    return schema


def selection_view_from_prompts(path: Path) -> list[dict[str, str]]:
    rows = load_jsonl(path)
    records: dict[str, str] = {}
    for row in rows:
        if row["condition"] != "F00_Full_NoShape":
            continue
        match = re.search(r"\nQuestion ID:\s*([^\n]+)\nQuestion:\s*(.*?)\s*$", row["prompt"], re.S)
        if not match or match.group(1).strip() != row["question_id"]:
            raise AssertionError(f"question text missing from frozen prompt: {row['question_id']}")
        records[row["question_id"]] = match.group(2).strip()
    view = [{"question_id": qid, "question": records[qid]} for qid in sorted(records)]
    if len(rows) != 720 or len(view) != 180:
        raise AssertionError("prompt ledger must provide exactly one no-gold question view for 180 IDs")
    if any(FORBIDDEN_SELECTION_FIELDS & set(row) for row in view):
        raise AssertionError("forbidden selection field entered selection view")
    return view


def freeze(config_path: Path, freeze_dir: Path) -> None:
    if (freeze_dir / "freeze_manifest.json").exists() or (freeze_dir / "selection_inputs.jsonl").exists():
        raise FileExistsError("freeze outputs already exist; no overwrite is permitted")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    selection_view = selection_view_from_prompts(resolved(config, "qwen_prompts"))
    selection_path = freeze_dir / "selection_inputs.jsonl"
    write_jsonl(selection_path, selection_view)

    input_keys = ["qwen_prompts", "schema_sql", "qwen_predictions", "granite_predictions", "reference_database", "witness_manifest"]
    files: dict[str, dict[str, Any]] = {}
    for key in input_keys:
        path = resolved(config, key).resolve(strict=True)
        files[key] = {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}
    witness_dir = resolved(config, "witness_directory")
    for state in config["reference_free_states"]:
        path = (witness_dir / f"{state}.sqlite").resolve(strict=True)
        files[f"state:{state}"] = {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}
    for key, path in {"config": config_path, "study_code": SCRIPT, "agents_code": AGENTS, "executor_code": EXECUTOR, "selection_inputs": selection_path}.items():
        path = path.resolve(strict=True)
        files[key] = {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}

    manifest = {
        "schema_version": "ma-sqlgrid-offline-coordination-freeze-v1",
        "status": "FROZEN_BEFORE_SELECTION_AND_GOLD_EVALUATION",
        "study_label": config["study_label"],
        "question_count": len(selection_view),
        "candidate_slots_per_question": config["candidate_slots_per_question"],
        "no_llm_calls": True,
        "gold_selection_access": False,
        "gold_binding_recorded_without_opening": config["evaluation_after_seal"],
        "files": files,
    }
    manifest["freeze_content_sha256"] = canonical_hash(manifest)
    write_json(freeze_dir / "freeze_manifest.json", manifest)
    print(json.dumps({"freeze_content_sha256": manifest["freeze_content_sha256"], "file_count": len(files)}, sort_keys=True))


def verify_freeze(config_path: Path, freeze_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    manifest = json.loads((freeze_dir / "freeze_manifest.json").read_text(encoding="utf-8"))
    expected = manifest.pop("freeze_content_sha256")
    if canonical_hash(manifest) != expected:
        raise AssertionError("freeze manifest content hash mismatch")
    manifest["freeze_content_sha256"] = expected
    for label, item in manifest["files"].items():
        path = ROOT / item["path"]
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise AssertionError(f"frozen file changed: {label}")
    return config, manifest


def load_candidates(config: Mapping[str, Any], question_ids: Sequence[str]) -> dict[str, list[SQLCandidate]]:
    pools: dict[str, list[SQLCandidate]] = {qid: [] for qid in question_ids}
    ledgers = [("qwen", resolved(config, "qwen_predictions")), ("granite", resolved(config, "granite_predictions"))]
    for backbone, path in ledgers:
        rows = load_jsonl(path)
        keyed = {(row["question_id"], row["condition"]): row for row in rows}
        if len(rows) != 720 or len(keyed) != 720:
            raise AssertionError(f"candidate ledger is not 180x4: {backbone}")
        for qid in question_ids:
            for condition in CONDITIONS:
                row = keyed[(qid, condition)]
                if row["status"] != "success" or not row.get("predicted_sql"):
                    raise AssertionError(f"frozen candidate unavailable: {backbone}/{qid}/{condition}")
                ordinal = len(pools[qid])
                pools[qid].append(SQLCandidate(f"C{ordinal:03d}", row["predicted_sql"].strip(), f"{backbone}:{condition}", ordinal))
    if any(len(pool) != 8 for pool in pools.values()):
        raise AssertionError("every question must retain exactly eight candidate slots")
    return pools


def result_equivalent(left: Mapping[str, Any], right: Mapping[str, Any], ordered: bool) -> bool:
    if not left.get("executable") or not right.get("executable"):
        return False
    lrows = [tuple(row) for row in left["rows"]]
    rrows = [tuple(row) for row in right["rows"]]
    if len(lrows) != len(rrows):
        return False
    if ordered:
        return lrows == rrows
    return sorted(lrows, key=repr) == sorted(rrows, key=repr)


def validation_for(candidate: SQLCandidate, execution: Mapping[str, Any], intent: Any) -> ValidationEvidence:
    sql_lower = candidate.sql.lower()
    aggregations_ok = not intent.aggregations or all(operator.lower() + "(" in sql_lower for operator in intent.aggregations)
    order_ok = not intent.order_required or bool(ORDER_RE.search(candidate.sql))
    hits = sum(1 for token in intent.lexical_tokens if len(token) > 2 and token in sql_lower)
    return ValidationEvidence(
        candidate_id=candidate.candidate_id,
        safe=bool(execution.get("executable")),
        single_statement=bool(execution.get("executable")),
        executable=bool(execution.get("executable")),
        shape_ok=aggregations_ok,
        order_ok=order_ok,
        value_hits=min(hits, 5),
        error=execution.get("error"),
        result_hash=execution.get("result_hash"),
    )


def select_with_policy(
    candidates: Sequence[SQLCandidate], validations: Mapping[str, ValidationEvidence], counterfactuals: Mapping[str, Any],
    weights: Mapping[str, int], threshold: int, reverse_tie: bool = False,
) -> str | None:
    eligible = []
    for candidate in candidates:
        v, cf = validations[candidate.candidate_id], counterfactuals[candidate.candidate_id]
        if not (v.safe and v.executable and cf.coverage_complete and cf.evaluated_states == 3 and cf.passed_states >= threshold):
            continue
        score = (
            weights["safe"] * int(v.safe) + weights["executable"] * int(v.executable)
            + weights["shape"] * int(v.shape_ok) + weights["order"] * int(v.order_ok)
            + weights["value_hit_each"] * min(v.value_hits, weights["value_hit_cap"])
        )
        tie = candidate.ordinal if reverse_tie else -candidate.ordinal
        eligible.append((score, cf.passed_states, tie, candidate.candidate_id))
    return max(eligible)[-1] if eligible else None


def run(config_path: Path, freeze_dir: Path, run_dir: Path) -> None:
    if run_dir.exists():
        raise FileExistsError(f"run directory exists; refusing overwrite: {run_dir}")
    run_dir.mkdir(parents=True)
    config, manifest = verify_freeze(config_path, freeze_dir)
    selection_path = freeze_dir / "selection_inputs.jsonl"
    selection_rows = load_jsonl(selection_path)
    if any(FORBIDDEN_SELECTION_FIELDS & set(row) for row in selection_rows):
        raise AssertionError("gold-derived field found in frozen selection view")
    question_ids = [row["question_id"] for row in selection_rows]
    pools = load_candidates(config, question_ids)
    schema = parse_schema(resolved(config, "schema_sql"))
    allowed = {table: columns for table, columns in schema.items()}
    state_names = [config["reference_state"], *config["reference_free_states"]]
    witness_dir = resolved(config, "witness_directory")
    state_paths = {config["reference_state"]: resolved(config, "reference_database")}
    state_paths.update({state: witness_dir / f"{state}.sqlite" for state in config["reference_free_states"]})
    for table in ("assets", "work_orders", "sensor_readings"):
        allowed[table] = [*allowed[table], "__ma_probe_nullable"]
    executors = {
        state: SQLiteReadOnlyExecutor(
            state_paths[state],
            timeout_seconds=config["executor"]["timeout_seconds"],
            max_opcodes=config["executor"]["max_opcodes"],
            progress_step=config["executor"]["progress_step"],
            max_rows=config["executor"]["max_rows"],
            allowed_tables=allowed,
            allow_metadata=False,
            trace_path=run_dir / "candidate_execution_attempts.jsonl",
        )
        for state in state_names
    }
    analyst, cartographer, critic, adjudicator = QueryAnalyst(), SchemaCartographer(), CounterfactualCritic(), Adjudicator()
    blackboards: list[dict[str, Any]] = []
    selections: list[dict[str, Any]] = []
    cache: dict[str, dict[str, dict[str, Mapping[str, Any]]]] = {}
    sensitivity_choices: list[dict[str, Any]] = []

    for qrow in selection_rows:
        qid, question = qrow["question_id"], qrow["question"]
        board = Blackboard(qid)
        intent = analyst.analyze(qid, question)
        grounding = cartographer.ground(intent, schema)
        board.post(analyst.role, "query_intent", asdict(intent))
        board.post(cartographer.role, "schema_grounding", asdict(grounding))
        board.post("Frozen Candidate Provider", "eight_slot_candidate_pool", {"candidates": [asdict(candidate) for candidate in pools[qid]], "slot_count": 8})
        validations: dict[str, ValidationEvidence] = {}
        counterfactuals: dict[str, Any] = {}
        cache[qid] = {}
        for candidate in pools[qid]:
            state_results = {state: executors[state](candidate.sql) for state in state_names}
            cache[qid][candidate.candidate_id] = state_results
            validation = validation_for(candidate, state_results[config["reference_state"]], intent)
            validations[candidate.candidate_id] = validation
            board.post("Execution and Safety Validator", "validation_evidence", asdict(validation))
            ordered = bool(ORDER_RE.search(candidate.sql))
            cf_rows = [
                {
                    "state_id": state,
                    "executable": state_results[state].get("executable", False),
                    "equivalent": result_equivalent(state_results[config["reference_state"]], state_results[state], ordered),
                }
                for state in config["reference_free_states"]
            ]
            cf = critic.review(candidate, cf_rows, config["reference_free_states"])
            counterfactuals[candidate.candidate_id] = cf
            board.post(critic.role, "counterfactual_evidence", asdict(cf))

        first = Decision(pools[qid][0].candidate_id, pools[qid][0].sql, "selected", "all equal-budget evidence collected; frozen fixed-order control ignores it and chooses frozen slot 0", ())
        validation_only = adjudicator.decide(pools[qid], validations, {})
        full = adjudicator.decide(
            pools[qid], validations, counterfactuals,
            require_counterfactual=True, expected_state_count=3, minimum_counterfactual_passes=3,
        )
        decisions = {METHODS[0]: first, METHODS[1]: validation_only, METHODS[2]: full}
        for method, decision in decisions.items():
            board.post(adjudicator.role, f"decision:{method}", asdict(decision))
            selections.append({
                "question_id": qid, "method": method, "selected_candidate_id": decision.selected_candidate_id,
                "selected_sql": decision.selected_sql, "status": decision.status,
            })
        for policy_name, weights in config["prespecified_sensitivity"]["weight_policies"].items():
            for threshold in config["prespecified_sensitivity"]["minimum_invariant_passes"]:
                for tie_rule in config["prespecified_sensitivity"]["tie_rules"]:
                    choice = select_with_policy(pools[qid], validations, counterfactuals, weights, threshold, tie_rule == "reverse_candidate_order")
                    sensitivity_choices.append({"question_id": qid, "weight_policy": policy_name, "minimum_invariant_passes": threshold, "tie_rule": tie_rule, "selected_candidate_id": choice})
        board.seal()
        blackboards.append({"question_id": qid, "sealed": True, "audit_digest": board.audit_digest(), "messages": [asdict(message) for message in board.messages]})

    if len(blackboards) != 180 or not all(row["sealed"] for row in blackboards):
        raise AssertionError("all 180 blackboards must be sealed before gold access")
    write_jsonl(run_dir / "blackboards_sealed_before_gold.jsonl", blackboards)
    write_jsonl(run_dir / "selection_ledger_pre_gold.jsonl", selections)
    write_jsonl(run_dir / "sensitivity_selection_pre_gold.jsonl", sensitivity_choices)
    seal_manifest = {
        "blackboard_count": len(blackboards),
        "all_sealed": True,
        "digest_set_sha256": canonical_hash(sorted(row["audit_digest"] for row in blackboards)),
        "selection_ledger_sha256": sha256(run_dir / "selection_ledger_pre_gold.jsonl"),
        "gold_file_opened": False,
    }
    write_json(run_dir / "pre_gold_seal_manifest.json", seal_manifest)

    # Gold boundary: this is the first read of the gold-bearing file in run().
    gold_path = ROOT / config["evaluation_after_seal"]["gold_path"]
    if sha256(gold_path) != config["evaluation_after_seal"]["externally_fixed_sha256"]:
        raise AssertionError("post-seal gold binding mismatch")
    gold_records = {row["question_id"]: row for row in load_jsonl(gold_path)}
    gold_executor = SQLiteReadOnlyExecutor(
        resolved(config, "reference_database"),
        timeout_seconds=config["executor"]["timeout_seconds"], max_opcodes=config["executor"]["max_opcodes"],
        progress_step=config["executor"]["progress_step"], max_rows=config["executor"]["max_rows"],
        allowed_tables=allowed, allow_metadata=False, trace_path=run_dir / "gold_evaluation_attempts.jsonl",
    )
    gold_outputs = {qid: gold_executor(gold_records[qid]["gold_sql"]) for qid in question_ids}
    selection_index = {(row["question_id"], row["method"]): row for row in selections}
    evaluated: list[dict[str, Any]] = []
    correctness: dict[tuple[str, str], bool] = {}
    for qid in question_ids:
        order_sensitive = bool(gold_records[qid]["order_sensitive"])
        for method in METHODS:
            choice = selection_index[(qid, method)]["selected_candidate_id"]
            selected_result = cache[qid][choice][config["reference_state"]] if choice is not None else {"executable": False, "rows": []}
            correct = bool(choice is not None and result_equivalent(selected_result, gold_outputs[qid], order_sensitive))
            correctness[(qid, method)] = correct
            invariant = bool(choice is not None and all(
                result_equivalent(cache[qid][choice][config["reference_state"]], cache[qid][choice][state], bool(ORDER_RE.search(pools[qid][int(choice[1:])].sql)))
                for state in config["reference_free_states"]
            ))
            evaluated.append({
                "question_id": qid, "method": method, "selected_candidate_id": choice,
                "covered": choice is not None, "abstained": choice is None, "correct": correct,
                "robust_invariance": invariant, "gold_access_phase": "after_all_blackboards_sealed",
            })
    write_jsonl(run_dir / "evaluation_ledger.jsonl", evaluated)

    sensitivity_eval: list[dict[str, Any]] = []
    for row in sensitivity_choices:
        qid, choice = row["question_id"], row["selected_candidate_id"]
        selected_result = cache[qid][choice][config["reference_state"]] if choice else {"executable": False, "rows": []}
        correct = bool(choice and result_equivalent(selected_result, gold_outputs[qid], bool(gold_records[qid]["order_sensitive"])))
        sensitivity_eval.append({**row, "covered": choice is not None, "correct": correct})
    write_jsonl(run_dir / "sensitivity_evaluation.jsonl", sensitivity_eval)

    summary: dict[str, Any] = {
        "schema_version": "ma-sqlgrid-offline-coordination-results-v1",
        "interpretation": config["interpretation"],
        "freeze_content_sha256": manifest["freeze_content_sha256"],
        "runtime": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version, "platform": platform.platform()},
        "question_count": 180,
        "candidate_slots": 1440,
        "state_attempts": 5760,
        "methods": {},
    }
    first_correct = {qid: correctness[(qid, METHODS[0])] for qid in question_ids}
    for method in METHODS:
        rows = [row for row in evaluated if row["method"] == method]
        covered = sum(row["covered"] for row in rows)
        correct = sum(row["correct"] for row in rows)
        robust = sum(row["robust_invariance"] for row in rows)
        rescue = sum(row["correct"] and not first_correct[row["question_id"]] for row in rows)
        harm = sum((not row["correct"]) and first_correct[row["question_id"]] for row in rows)
        summary["methods"][method] = {
            "n": 180, "covered": covered, "abstained": 180 - covered, "correct": correct,
            "accuracy_all": correct / 180, "coverage": covered / 180,
            "accuracy_when_covered": correct / covered if covered else None,
            "robust_invariance_selected": robust, "robust_invariance_rate_all": robust / 180,
            "rescues_vs_first": rescue, "harms_vs_first": harm,
        }
    groups: dict[tuple[str, int, str], list[dict[str, Any]]] = {}
    for row in sensitivity_eval:
        key = (row["weight_policy"], row["minimum_invariant_passes"], row["tie_rule"])
        groups.setdefault(key, []).append(row)
    summary["sensitivity"] = [
        {"weight_policy": key[0], "minimum_invariant_passes": key[1], "tie_rule": key[2],
         "covered": sum(row["covered"] for row in rows), "correct": sum(row["correct"] for row in rows),
         "accuracy_all": sum(row["correct"] for row in rows) / 180}
        for key, rows in sorted(groups.items())
    ]
    write_json(run_dir / "summary.json", summary)

    canonical = {
        "freeze_content_sha256": manifest["freeze_content_sha256"],
        "blackboard_digest_set": sorted(row["audit_digest"] for row in blackboards),
        "selection_sha256": sha256(run_dir / "selection_ledger_pre_gold.jsonl"),
        "evaluation_sha256": sha256(run_dir / "evaluation_ledger.jsonl"),
        "sensitivity_sha256": sha256(run_dir / "sensitivity_evaluation.jsonl"),
        "summary_sha256": sha256(run_dir / "summary.json"),
    }
    canonical["canonical_reproduction_sha256"] = canonical_hash(canonical)
    write_json(run_dir / "reproduction_manifest.json", canonical)
    print(json.dumps(summary["methods"], sort_keys=True))


def compare(run_a: Path, run_b: Path, out: Path) -> None:
    if out.exists():
        raise FileExistsError(f"comparison output exists: {out}")
    pairs = ["selection_ledger_pre_gold.jsonl", "evaluation_ledger.jsonl", "sensitivity_evaluation.jsonl", "summary.json"]
    checks = {name: {"run_a": sha256(run_a / name), "run_b": sha256(run_b / name), "identical": sha256(run_a / name) == sha256(run_b / name)} for name in pairs}
    report = {"schema_version": "ma-sqlgrid-offline-independent-reproduction-check-v1", "checks": checks, "all_canonical_outputs_identical": all(item["identical"] for item in checks.values())}
    write_json(out, report)
    if not report["all_canonical_outputs_identical"]:
        raise AssertionError("independent reproduction mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p_freeze = sub.add_parser("freeze")
    p_freeze.add_argument("--config", type=Path, required=True)
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
        freeze(args.config.resolve(), args.freeze_dir.resolve())
    elif args.command == "run":
        run(args.config.resolve(), args.freeze_dir.resolve(), args.run_dir.resolve())
    else:
        compare(args.run_a.resolve(), args.run_b.resolve(), args.out.resolve())


if __name__ == "__main__":
    main()
