#!/usr/bin/env python3
"""Post-review role-utilization and score-component ablation audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any


REPRO_ROOT = Path(__file__).resolve().parents[2]
BLACKBOARDS = REPRO_ROOT / "Data" / "historical_pool" / "run_v3a" / "blackboards_sealed_before_gold.jsonl"
CANONICAL = REPRO_ROOT / "Data" / "canonical_v2" / "canonical_rows_v2.jsonl"
ATTEMPTS = REPRO_ROOT / "Data" / "historical_pool" / "run_v3a" / "candidate_execution_attempts.jsonl"
OUTPUT = REPRO_ROOT / "Data" / "role_ablation" / "unified_v1"

SLOT_TO_CELL = {
    "C000": ("qwen", "F00_Full_NoShape"),
    "C001": ("qwen", "F01_Full_WithShape"),
    "C002": ("qwen", "F10_Compact_NoShape"),
    "C003": ("qwen", "F11_Compact_WithShape"),
    "C004": ("granite", "F00_Full_NoShape"),
    "C005": ("granite", "F01_Full_WithShape"),
    "C006": ("granite", "F10_Compact_NoShape"),
    "C007": ("granite", "F11_Compact_WithShape"),
}
SLOTS = tuple(SLOT_TO_CELL)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def messages(board: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    return [message["payload"] for message in board["messages"] if message["kind"] == kind]


def original_decision(board: dict[str, Any], suffix: str) -> dict[str, Any]:
    rows = messages(board, f"decision:{suffix}")
    if len(rows) != 1:
        raise AssertionError(f"{board['question_id']}: missing decision {suffix}")
    return rows[0]


def choose(
    validation: dict[str, dict[str, Any]],
    counterfactual: dict[str, dict[str, Any]],
    *,
    require_constructed_state: bool,
    include_shape: bool = True,
    include_order: bool = True,
    include_value: bool = True,
) -> str:
    ranked: list[tuple[tuple[int, int, int, int], str]] = []
    for ordinal, slot in enumerate(SLOTS):
        item = validation[slot]
        cf = counterfactual[slot]
        eligible = bool(item["safe"] and item["executable"])
        if require_constructed_state:
            eligible = eligible and bool(
                cf["coverage_complete"] and cf["evaluated_states"] == 3 and cf["passed_states"] >= 3
            )
        if not eligible:
            continue
        points = 40 * int(item["safe"]) + 40 * int(item["executable"])
        if include_shape:
            points += 10 * int(item["shape_ok"])
        if include_order:
            points += 5 * int(item["order_ok"])
        if include_value:
            points += min(int(item["value_hits"]), 5)
        total = int(cf["evaluated_states"]) if require_constructed_state else 0
        passes = int(cf["passed_states"]) if require_constructed_state else 0
        cf_scaled = passes * 1_000_000 // total if total else -1
        ranked.append(((points, cf_scaled, total, -ordinal), slot))
    if not ranked:
        raise AssertionError("No eligible candidate in frozen pool")
    return max(ranked)[1]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    boards = load_jsonl(BLACKBOARDS)
    canonical = load_jsonl(CANONICAL)
    attempts = load_jsonl(ATTEMPTS)
    if len(boards) != 180 or len({row["question_id"] for row in boards}) != 180:
        raise AssertionError("Expected 180 unique boards")
    if {len(row["messages"]) for row in boards} != {22}:
        raise AssertionError("Expected exactly 22 messages per board")
    if len(canonical) != 1440 or len(attempts) != 5760:
        raise AssertionError("Frozen outcome or execution-attempt cardinality mismatch")

    correctness: dict[tuple[str, str], bool] = {}
    for row in canonical:
        slot = next(slot for slot, cell in SLOT_TO_CELL.items() if cell == (row["backbone"], row["condition"]))
        correctness[(row["question_id"], slot)] = bool(row["execution"])
    if len(correctness) != 1440:
        raise AssertionError("Incomplete fixed-slot outcome matrix")

    qids = sorted(row["question_id"] for row in boards)
    board_by_qid = {row["question_id"]: row for row in boards}
    choices: dict[str, dict[str, str]] = {
        name: {}
        for name in (
            "validation_original",
            "validation_no_query_features",
            "validation_no_shape",
            "validation_no_order",
            "validation_no_value",
            "complete_original",
            "complete_no_query_features",
            "complete_no_constructed_state",
            "complete_no_schema_grounding",
        )
    }

    for qid in qids:
        board = board_by_qid[qid]
        validation_rows = messages(board, "validation_evidence")
        cf_rows = messages(board, "counterfactual_evidence")
        if len(validation_rows) != 8 or len(cf_rows) != 8:
            raise AssertionError(f"{qid}: incomplete candidate evidence")
        validation = {row["candidate_id"]: row for row in validation_rows}
        counterfactual = {row["candidate_id"]: row for row in cf_rows}

        choices["validation_original"][qid] = choose(validation, counterfactual, require_constructed_state=False)
        choices["validation_no_query_features"][qid] = choose(
            validation, counterfactual, require_constructed_state=False,
            include_shape=False, include_order=False, include_value=False,
        )
        choices["validation_no_shape"][qid] = choose(
            validation, counterfactual, require_constructed_state=False, include_shape=False,
        )
        choices["validation_no_order"][qid] = choose(
            validation, counterfactual, require_constructed_state=False, include_order=False,
        )
        choices["validation_no_value"][qid] = choose(
            validation, counterfactual, require_constructed_state=False, include_value=False,
        )
        choices["complete_original"][qid] = choose(validation, counterfactual, require_constructed_state=True)
        choices["complete_no_query_features"][qid] = choose(
            validation, counterfactual, require_constructed_state=True,
            include_shape=False, include_order=False, include_value=False,
        )
        choices["complete_no_constructed_state"][qid] = choices["validation_original"][qid]
        choices["complete_no_schema_grounding"][qid] = choices["complete_original"][qid]

        recorded_validation = original_decision(board, "validation_rank_equal_budget_no_cf")["selected_candidate_id"]
        recorded_complete = original_decision(board, "full_coordination_complete_metamorphic")["selected_candidate_id"]
        if choices["validation_original"][qid] != recorded_validation:
            raise AssertionError(f"{qid}: validation reconstruction mismatch")
        if choices["complete_original"][qid] != recorded_complete:
            raise AssertionError(f"{qid}: complete reconstruction mismatch")

    correct_counts = {
        variant: sum(correctness[(qid, selected[qid])] for qid in qids)
        for variant, selected in choices.items()
    }
    if correct_counts["validation_original"] != 99 or correct_counts["complete_original"] != 100:
        raise AssertionError(f"Original unified counts do not reproduce: {correct_counts}")
    if choices["complete_no_constructed_state"] != choices["validation_original"]:
        raise AssertionError("No-constructed-state variant must equal validation-only")
    if choices["complete_no_schema_grounding"] != choices["complete_original"]:
        raise AssertionError("Schema-grounding removal unexpectedly changed a choice")

    parents = {
        "validation_original": None,
        "validation_no_query_features": "validation_original",
        "validation_no_shape": "validation_original",
        "validation_no_order": "validation_original",
        "validation_no_value": "validation_original",
        "complete_original": None,
        "complete_no_query_features": "complete_original",
        "complete_no_constructed_state": "complete_original",
        "complete_no_schema_grounding": "complete_original",
    }
    ablation_rows: list[dict[str, Any]] = []
    for variant, selected in choices.items():
        parent = parents[variant]
        if parent is None:
            changed = gains = losses = 0
        else:
            changed = sum(selected[qid] != choices[parent][qid] for qid in qids)
            gains = sum(
                correctness[(qid, selected[qid])] and not correctness[(qid, choices[parent][qid])]
                for qid in qids
            )
            losses = sum(
                not correctness[(qid, selected[qid])] and correctness[(qid, choices[parent][qid])]
                for qid in qids
            )
        ablation_rows.append(
            {
                "variant": variant,
                "parent": parent or "",
                "correct": correct_counts[variant],
                "n": 180,
                "accuracy": correct_counts[variant] / 180,
                "changed_choices_vs_parent": changed,
                "gains_vs_parent": gains,
                "losses_vs_parent": losses,
                "net_correct_vs_parent": gains - losses,
            }
        )

    message_counts = Counter((message["role"], message["kind"]) for board in boards for message in board["messages"])
    role_rows = [
        {
            "role": "Query Analyst",
            "invocations": 180,
            "blackboard_messages": sum(count for (role, _), count in message_counts.items() if role == "Query Analyst"),
            "downstream_status": "consumed",
            "consumed_fields": "aggregations|order_required|lexical_tokens",
            "incremental_database_attempts": 0,
            "interpretation": "feeds validation shape/order/value features; deterministic, no model call",
        },
        {
            "role": "Schema Cartographer",
            "invocations": 180,
            "blackboard_messages": sum(count for (role, _), count in message_counts.items() if role == "Schema Cartographer"),
            "downstream_status": "recorded_only",
            "consumed_fields": "",
            "incremental_database_attempts": 0,
            "interpretation": "grounding is posted but not passed to generation, validation, critic, or adjudicator",
        },
        {
            "role": "Frozen Candidate Provider",
            "invocations": 180,
            "blackboard_messages": sum(count for (role, _), count in message_counts.items() if role == "Frozen Candidate Provider"),
            "downstream_status": "consumed",
            "consumed_fields": "candidate_id|sql|source|ordinal",
            "incremental_database_attempts": 0,
            "interpretation": "supplies eight historical candidates; not a generative role in this study",
        },
        {
            "role": "Execution and Safety Validator",
            "invocations": 1440,
            "blackboard_messages": sum(count for (role, _), count in message_counts.items() if role == "Execution and Safety Validator"),
            "downstream_status": "consumed",
            "consumed_fields": "safe|executable|shape_ok|order_ok|value_hits",
            "incremental_database_attempts": 5760,
            "interpretation": "reference T0 plus three constructed states were executed for every slot",
        },
        {
            "role": "Counterfactual Critic",
            "invocations": 1440,
            "blackboard_messages": sum(count for (role, _), count in message_counts.items() if role == "Counterfactual Critic"),
            "downstream_status": "consumed_by_complete_only",
            "consumed_fields": "coverage_complete|evaluated_states|passed_states",
            "incremental_database_attempts": 0,
            "interpretation": "summarizes the three already-executed constructed-state results",
        },
        {
            "role": "Adjudicator",
            "invocations": 540,
            "blackboard_messages": sum(count for (role, _), count in message_counts.items() if role == "Adjudicator"),
            "downstream_status": "consumed",
            "consumed_fields": "eligibility|validation_points|counterfactual evidence|ordinal",
            "incremental_database_attempts": 0,
            "interpretation": "three deterministic decisions per question, including the C000 control",
        },
    ]

    elapsed = [float(row["elapsed_ms"]) for row in attempts]
    failures = Counter((row.get("failure_kind") or "none") for row in attempts)
    cost_summary = {
        "boards": len(boards),
        "messages": sum(message_counts.values()),
        "messages_per_board": sum(message_counts.values()) / len(boards),
        "candidate_slots": 1440,
        "database_attempts": len(attempts),
        "executable_attempts": sum(bool(row["executable"]) for row in attempts),
        "failed_attempts": sum(not bool(row["executable"]) for row in attempts),
        "failure_kinds": dict(sorted(failures.items())),
        "recorded_elapsed_ms_total": sum(elapsed),
        "recorded_elapsed_ms_median": statistics.median(elapsed),
        "recorded_elapsed_ms_p95": percentile(elapsed, 0.95),
        "distinct_sql_hashes": len({row["sql_sha256"] for row in attempts}),
        "model_calls_in_historical_selector_study": 0,
    }

    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUT / "ablation_results.csv", ablation_rows)
    write_csv(OUTPUT / "role_utilization.csv", role_rows)
    (OUTPUT / "cost_summary.json").write_text(json.dumps(cost_summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "protocol_id": "MA-SQLGrid-role-ablation-unified-v1",
        "post_review_diagnostic": True,
        "inputs": {
            "blackboards_sha256": sha256(BLACKBOARDS),
            "canonical_sha256": sha256(CANONICAL),
            "attempts_sha256": sha256(ATTEMPTS),
        },
        "correct_counts": correct_counts,
        "cost": cost_summary,
    }
    (OUTPUT / "role_ablation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    by_variant = {row["variant"]: row for row in ablation_rows}
    report = [
        "# Role-Utilization and Score-Ablation Audit",
        "",
        "This is a post-review diagnostic over the frozen historical pool, not a prospective role-removal experiment.",
        "",
        "## Utilization finding",
        "",
        "The Query Analyst feeds aggregation, ordering, and lexical-match features into validation. The Schema Cartographer's grounding is recorded in the blackboard but has no downstream consumer in the frozen historical-pool driver. The candidate provider is a frozen-ledger adapter and makes no model calls. Validation evidence drives both selectors; constructed-state evidence is consumed only by the complete selector.",
        "",
        "## Unified-evaluator ablations",
        "",
        "| Variant | Correct/180 | Changed choices | Gains/losses vs parent |",
        "|---|---:|---:|---:|",
    ]
    for row in ablation_rows:
        report.append(
            f"| {row['variant']} | {row['correct']}/180 | {row['changed_choices_vs_parent']} | "
            f"{row['gains_vs_parent']}/{row['losses_vs_parent']} |"
        )
    report.extend(
        [
            "",
            "Removing Schema Cartographer output changes zero selections because the frozen driver never consumes that output. This is an implementation finding, not evidence that schema grounding is generally unnecessary. Removing constructed-state evidence reduces the complete selector exactly to validation-only; its one-match difference is Q039 in the original order.",
            "",
            "## Recorded cost boundary",
            "",
            f"The ledgers contain {cost_summary['messages']} blackboard messages and {cost_summary['database_attempts']} database attempts, of which {cost_summary['failed_attempts']} failed. Recorded attempt time totals {cost_summary['recorded_elapsed_ms_total']:.3f} ms (median {cost_summary['recorded_elapsed_ms_median']:.3f} ms; p95 {cost_summary['recorded_elapsed_ms_p95']:.3f} ms). These are local ledger measurements, not deployment-scale or model-token estimates.",
            "",
        ]
    )
    (OUTPUT / "ROLE_ABLATION_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
