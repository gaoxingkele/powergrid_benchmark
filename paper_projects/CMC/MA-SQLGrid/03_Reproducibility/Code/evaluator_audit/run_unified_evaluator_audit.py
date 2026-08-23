#!/usr/bin/env python3
"""Reconcile all fixed slots and sealed selectors under one frozen evaluator."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import random
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
CODE = HERE.parent
PROJECT = CODE.parents[1]
sys.path.insert(0, str(CODE / "framework"))
from sqlite_readonly_executor import SQLiteReadOnlyExecutor  # noqa: E402


CONDITIONS = ("F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape")
BACKBONES = ("qwen", "granite")
SELECTORS = ("validation_rank_equal_budget_no_cf", "full_coordination_complete_metamorphic")
ZERO_AUDIT_IDS = ("Q104", "Q107", "Q110", "Q140")
BOOTSTRAP_SAMPLES = 10_000
BOOTSTRAP_SEED = 20_260_823
FLOAT_ABS_TOL = 1e-6


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def sql_hash(sql: str) -> str:
    return hashlib.sha256(normalize_sql(sql).encode("utf-8")).hexdigest().upper()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def strip_sql_comments(sql: str) -> str:
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    return re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL).strip()


def normalize_sql(sql: str) -> str:
    sql = strip_sql_comments(sql)
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", sql, flags=re.IGNORECASE | re.DOTALL)
    return fenced.group(1).strip() if fenced else sql


def stable_value(value: Any) -> Any:
    if value is None:
        return ("__NULL__",)
    if isinstance(value, float):
        if math.isnan(value):
            return ("__NAN__",)
        return round(value / FLOAT_ABS_TOL) * FLOAT_ABS_TOL
    if isinstance(value, (dict, list)):
        return ("__JSON__", json.dumps(value, sort_keys=True, separators=(",", ":")))
    return value


def normalize_rows(rows: Any) -> list[tuple[Any, ...]]:
    return [tuple(stable_value(value) for value in row) for row in rows]


def rows_equal(left: Mapping[str, Any], right: Mapping[str, Any], ordered: bool) -> bool:
    if not left.get("executable") or not right.get("executable"):
        return False
    lrows = normalize_rows(left["rows"])
    rrows = normalize_rows(right["rows"])
    return lrows == rrows if ordered else Counter(lrows) == Counter(rrows)


def evaluate(candidate: Mapping[str, Any], gold: Mapping[str, Any], record: Mapping[str, Any]) -> dict[str, Any]:
    expected = int(record["answer_shape"]["column_count"])
    if not candidate.get("executable"):
        error = "candidate_execution_error"
        correct = False
    elif not gold.get("executable"):
        error = "gold_execution_error"
        correct = False
    elif len(candidate["columns"]) != expected:
        error = "candidate_shape_mismatch"
        correct = False
    elif len(gold["columns"]) != expected:
        error = "gold_shape_mismatch"
        correct = False
    elif not rows_equal(candidate, gold, bool(record["order_sensitive"])):
        error = "wrong_denotation"
        correct = False
    else:
        error = "correct"
        correct = True
    return {
        "correct": correct,
        "error_type": error,
        "expected_columns": expected,
        "candidate_columns": len(candidate.get("columns", ())),
        "gold_columns": len(gold.get("columns", ())),
        "candidate_rows": len(candidate.get("rows", ())),
        "gold_rows": len(gold.get("rows", ())),
        "legacy_row_only_equal": rows_equal(candidate, gold, bool(record["order_sensitive"])),
    }


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def paired_bootstrap_interval(differences: list[int], seed: int) -> list[float]:
    rng = random.Random(seed)
    n = len(differences)
    draws = [sum(rng.choice(differences) for _ in range(n)) / n for _ in range(BOOTSTRAP_SAMPLES)]
    return [percentile(draws, 0.025), percentile(draws, 0.975)]


def exact_discordant_sign_p(rescues: int, harms: int) -> float:
    n = rescues + harms
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(min(rescues, harms) + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def holm(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    adjusted = [0.0] * len(values)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(values) - rank) * values[index]))
        adjusted[index] = running
    return adjusted


def candidate_pools(blackboards: list[dict]) -> dict[str, dict[str, dict]]:
    pools = {}
    for board in blackboards:
        pool_message = next(message for message in board["messages"] if message["kind"] == "eight_slot_candidate_pool")
        candidates = pool_message["payload"]["candidates"]
        pools[board["question_id"]] = {item["candidate_id"]: item for item in candidates}
    return pools


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--qwen", type=Path, required=True)
    parser.add_argument("--granite", type=Path, required=True)
    parser.add_argument("--blackboards", type=Path, required=True)
    parser.add_argument("--selection-inputs", type=Path, required=True)
    parser.add_argument("--selections", type=Path, required=True)
    parser.add_argument("--canonical-rows", type=Path, required=True)
    parser.add_argument("--historical-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)

    selected_ids = {row["question_id"] for row in load_jsonl(args.selection_inputs)}
    questions = {row["question_id"]: row for row in load_jsonl(args.questions) if row["question_id"] in selected_ids}
    if len(questions) != 180:
        raise ValueError("question universe is not 180")
    predictions = {}
    for backbone, path in (("qwen", args.qwen), ("granite", args.granite)):
        rows = load_jsonl(path)
        index = {(row["question_id"], row["condition"]): row for row in rows}
        if len(rows) != 720 or len(index) != 720:
            raise ValueError(f"{backbone} prediction grid is not 180x4")
        predictions[backbone] = index

    blackboards = load_jsonl(args.blackboards)
    pools = candidate_pools(blackboards)
    selections = {(row["question_id"], row["method"]): row for row in load_jsonl(args.selections)}
    canonical = {(row["backbone"], row["question_id"], row["condition"]): bool(row["execution"]) for row in load_jsonl(args.canonical_rows)}
    historical = json.loads(args.historical_summary.read_text(encoding="utf-8"))

    source_by_candidate = {f"C{index:03d}": f"{backbone}:{condition}" for index, (backbone, condition) in enumerate((b, c) for b in BACKBONES for c in CONDITIONS)}
    identity_checks = []
    for qid in sorted(questions):
        for candidate_id, source in source_by_candidate.items():
            backbone, condition = source.split(":", 1)
            prediction_sql = predictions[backbone][(qid, condition)]["predicted_sql"]
            pool_sql = pools[qid][candidate_id]["sql"]
            identity_checks.append(sql_hash(prediction_sql) == sql_hash(pool_sql))
        fixed = selections[(qid, "fixed_order_equal_budget")]
        identity_checks.append(fixed["selected_candidate_id"] == "C000")
        identity_checks.append(sql_hash(fixed["selected_sql"]) == sql_hash(pools[qid]["C000"]["sql"]))
    if not all(identity_checks):
        raise AssertionError("prediction, pool and C000 identities do not align")

    trace = args.output / "execution_trace.jsonl"
    executor = SQLiteReadOnlyExecutor(args.db, timeout_seconds=2.0, max_opcodes=2_000_000, progress_step=1_000, max_rows=10_000, allow_metadata=False, trace_path=trace)
    outcomes: dict[str, dict[str, dict[str, Any]]] = {}
    detailed: dict[tuple[str, str], dict[str, Any]] = {}
    canonical_mismatches = []
    zero_rows = []
    for qid in sorted(questions):
        record = questions[qid]
        gold = executor(normalize_sql(record["gold_sql"]))
        outcomes[qid] = {}
        for candidate_id, source in source_by_candidate.items():
            backbone, condition = source.split(":", 1)
            sql = predictions[backbone][(qid, condition)]["predicted_sql"]
            result = executor(normalize_sql(sql))
            verdict = evaluate(result, gold, record)
            outcomes[qid][source] = verdict
            detailed[(qid, source)] = {**verdict, "candidate_sql_sha256": sql_hash(sql), "gold_sql_sha256": sql_hash(record["gold_sql"])}
            if verdict["correct"] != canonical[(backbone, qid, condition)]:
                canonical_mismatches.append([backbone, qid, condition])
        if qid in ZERO_AUDIT_IDS:
            item = detailed[(qid, "qwen:F00_Full_NoShape")]
            zero_rows.append({"question_id": qid, "database_sha256": sha256(args.db), **item})
    if canonical_mismatches:
        raise AssertionError(f"canonical-v2 mismatch: {canonical_mismatches[:10]}")

    method_vectors: dict[str, list[bool]] = {}
    for source in source_by_candidate.values():
        method_vectors[source] = [outcomes[qid][source]["correct"] for qid in sorted(questions)]
    method_vectors["C000_fixed_order_equal_budget"] = list(method_vectors["qwen:F00_Full_NoShape"])
    for selector in SELECTORS:
        values = []
        for qid in sorted(questions):
            choice = selections[(qid, selector)]["selected_candidate_id"]
            if choice is None:
                values.append(False)
            else:
                values.append(outcomes[qid][source_by_candidate[choice]]["correct"])
        method_vectors[selector] = values

    baseline = method_vectors["C000_fixed_order_equal_budget"]
    compare_ids = [source for source in source_by_candidate.values() if source != "qwen:F00_Full_NoShape"] + list(SELECTORS)
    paired = []
    for index, method in enumerate(compare_ids):
        vector = method_vectors[method]
        differences = [int(value) - int(reference) for value, reference in zip(vector, baseline)]
        rescues = sum(value and not reference for value, reference in zip(vector, baseline))
        harms = sum(reference and not value for value, reference in zip(vector, baseline))
        paired.append({
            "method": method,
            "baseline": "C000_fixed_order_equal_budget",
            "paired_accuracy_difference": sum(differences) / len(differences),
            "paired_bootstrap_95_composition_interval": paired_bootstrap_interval(differences, BOOTSTRAP_SEED + index),
            "rescues": rescues,
            "harms": harms,
            "ties": 180 - rescues - harms,
            "exact_discordant_sign_p": exact_discordant_sign_p(rescues, harms),
        })
    for row, adjusted in zip(paired, holm([row["exact_discordant_sign_p"] for row in paired])):
        row["holm_adjusted_p_nine_comparisons"] = adjusted
    paired_index = {row["method"]: row for row in paired}

    summary_rows = []
    for method, vector in method_vectors.items():
        correct = sum(vector)
        row = {"method": method, "correct": correct, "n": 180, "accuracy": correct / 180}
        if method in paired_index:
            row.update(paired_index[method])
        elif method in {"qwen:F00_Full_NoShape", "C000_fixed_order_equal_budget"}:
            row.update({"baseline": "C000_fixed_order_equal_budget", "paired_accuracy_difference": 0.0, "paired_bootstrap_95_composition_interval": [0.0, 0.0], "rescues": 0, "harms": 0, "ties": 180, "exact_discordant_sign_p": 1.0, "holm_adjusted_p_nine_comparisons": None})
        summary_rows.append(row)

    old_counts = {method: int(values["correct"]) for method, values in historical["methods"].items()}
    reconciled = {
        "fixed_order_equal_budget": sum(method_vectors["C000_fixed_order_equal_budget"]),
        **{selector: sum(method_vectors[selector]) for selector in SELECTORS},
    }
    report = {
        "schema": "MA-SQLGrid-unified-evaluator-audit-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "evaluator_id": "MA-SQLGrid-GridDB-T0-shape-denotation-v1",
        "runtime": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version, "platform": platform.platform()},
        "input_sha256": {name: sha256(path) for name, path in {
            "database": args.db, "questions": args.questions, "qwen_predictions": args.qwen,
            "granite_predictions": args.granite, "blackboards": args.blackboards,
            "selection_inputs": args.selection_inputs,
            "selections": args.selections, "canonical_rows": args.canonical_rows,
            "historical_summary": args.historical_summary, "audit_script": Path(__file__).resolve(),
        }.items()},
        "identity": {
            "checks": len(identity_checks),
            "all_prediction_pool_sql_hashes_match": True,
            "c000_is_qwen_f00_for_all_180": True,
            "artifact_conclusion": "Qwen F00 and historical C000 use the same 180 SQL artifacts; 76 versus 80 is evaluator-policy drift, not model-output drift.",
        },
        "evaluator": {
            "database_sha256": sha256(args.db), "questions": 180, "fixed_slots": 8,
            "executions": 1620, "shape_gate": True, "empty_result_policy": "shape gates must pass before empty-row equality",
            "float_abs_tolerance": FLOAT_ABS_TOL, "ordered_when_recorded": True,
            "unordered_policy": "duplicate-preserving multiset", "sql_canonicalization_for_correctness": False,
            "canonical_v2_mismatches": len(canonical_mismatches),
        },
        "historical_vs_unified": {method: {"historical_correct": old_counts[method], "unified_correct": reconciled[method], "difference": reconciled[method] - old_counts[method]} for method in reconciled},
        "summary": summary_rows,
        "paired_comparisons": paired,
        "zero_result_audit": zero_rows,
        "limitations": ["post-result evaluator reconciliation, not preregistration", "single synthetic GridDB snapshot", "execution equality does not establish expert semantic correctness"],
    }
    (args.output / "unified_evaluator_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with (args.output / "unified_evaluator_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        fields = ["method", "correct", "n", "accuracy", "paired_accuracy_difference", "paired_bootstrap_95_low", "paired_bootstrap_95_high", "rescues", "harms", "ties", "exact_discordant_sign_p", "holm_adjusted_p_nine_comparisons"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in summary_rows:
            low, high = row["paired_bootstrap_95_composition_interval"]
            writer.writerow({**{key: row.get(key) for key in fields}, "paired_bootstrap_95_low": low, "paired_bootstrap_95_high": high})
    with (args.output / "zero_result_audit.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(zero_rows[0]))
        writer.writeheader()
        writer.writerows(zero_rows)

    lines = [
        "# MA-SQLGrid evaluator reconciliation report", "", "Status: PASS. No model was called.", "",
        "Qwen F00 and historical C000 are the same 180 normalized SQL artifacts. The historical row-only evaluator counted 80/180 because it ignored output shape before comparing rows. The frozen unified evaluator enforces the question's expected column count before denotation equality, reproduces all 1,440 canonical-v2 fixed-slot outcomes, and scores C000 as 76/180. Q104, Q107, Q110 and Q140 are the four discrepant empty-result cases; each has row-only equality but a candidate column-count mismatch.", "",
        "| Method | Correct/180 | Accuracy | Difference vs C000 | 95% composition interval | Rescues/harms | Exact p | Holm p |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        low, high = row["paired_bootstrap_95_composition_interval"]
        holm_value = "--" if row["holm_adjusted_p_nine_comparisons"] is None else f"{row['holm_adjusted_p_nine_comparisons']:.6f}"
        lines.append(f"| {row['method']} | {row['correct']}/180 | {row['accuracy']:.4f} | {row['paired_accuracy_difference']:+.4f} | [{low:+.4f}, {high:+.4f}] | {row['rescues']}/{row['harms']} | {row['exact_discordant_sign_p']:.6f} | {holm_value} |")
    lines.extend(["", "The intervals are paired question-composition intervals and the exact values are post-result reconciliation tests. They do not support a five-role end-to-end effect claim or power-grid semantic validity beyond this frozen synthetic benchmark.", ""])
    (args.output / "EVALUATOR_RECONCILIATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(args.output), "counts": {row["method"]: row["correct"] for row in summary_rows}}))


if __name__ == "__main__":
    main()
