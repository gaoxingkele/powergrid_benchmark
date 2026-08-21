"""Read-only replay of frozen MA-SQLGrid candidates.

The output is a *retrospective offline coordination diagnostic*.  It is not a
new multi-agent generation run: no prompt is built, no model is called, and no
gold-derived correctness signal is admitted to candidate selection.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from ma_sqlgrid_agents import (
    Adjudicator,
    Blackboard,
    CounterfactualCritic,
    SQLSynthesizer,
    Validator,
    canonical_sql,
)


LABEL = "retrospective offline coordination diagnostic"
HERE = Path(__file__).resolve().parent
MA_ROOT = HERE.parent
DEFAULT_INPUTS = {
    "qwen_predictions": MA_ROOT / "formal_run" / "qwen25coder7b_q4km_seed20260805_clean_rerun1" / "predictions.jsonl",
    "granite_predictions": MA_ROOT / "granite_formal" / "granite33_8b_q4km_seed20260805_clean1" / "predictions.jsonl",
    "atomic_scores": MA_ROOT / "semantic_reliability_experiment" / "formal_v5_results" / "atomic_scores.jsonl",
}
EXPECTED_INPUT_SHA256 = {
    "qwen_predictions": "53aaf0c9659f6a6b71b66ff64d34ed925664742205d0ca4fd7585d7fe5c9f5e3",
    "granite_predictions": "be433ac853f60ebc8882fdcc7bd01033bca8868fa23b298114b0977476983e3d",
    "atomic_scores": "89c0ede848b4487a1edadb2fd771dabaf21a16c8359d7000ad9955c3196968cd",
}
CONDITIONS = (
    "F00_Full_NoShape",
    "F01_Full_WithShape",
    "F10_Compact_NoShape",
    "F11_Compact_WithShape",
)
EXPECTED_STATES = (
    "T1_insertion_permutation_a",
    "T1_insertion_permutation_b",
    "T1_insertion_permutation_c",
    "L1_exact_clone_retained",
    "L2_attribute_rotation_retained",
    "L3_relation_rewire_retained",
    "L4_numeric_time_shift_retained",
    "L5_combined_retained",
    "L6_two_cohorts_retained",
    "T3_categorical_covering",
    "T4_numeric_date_boundaries",
    "T4b_dense_calendar_boundaries",
    "T5_null_witnesses",
    "T6_relationship_anti_join_cover",
    "T6b_isolated_parent_cover",
    "T7_topology_motifs",
    "T8_string_decoys",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            rows.append(item)
    return rows


def verify_inputs(paths: Mapping[str, Path]) -> dict[str, dict[str, Any]]:
    verified: dict[str, dict[str, Any]] = {}
    resolved_output = HERE.resolve()
    for name, path in paths.items():
        resolved = path.resolve(strict=True)
        if resolved_output in resolved.parents:
            raise ValueError(f"frozen input cannot be inside writable rebuild directory: {resolved}")
        actual = sha256_file(resolved)
        expected = EXPECTED_INPUT_SHA256[name]
        if actual.lower() != expected.lower():
            raise ValueError(f"input hash mismatch for {name}: expected {expected}, got {actual}")
        verified[name] = {
            "path": resolved.as_posix(),
            "sha256": actual,
            "bytes": resolved.stat().st_size,
        }
    return verified


def _prediction_sources(
    qwen_rows: Sequence[Mapping[str, Any]], granite_rows: Sequence[Mapping[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    by_question: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str, str]] = set()
    for backbone, rows in (("qwen", qwen_rows), ("granite", granite_rows)):
        for row in rows:
            question_id = str(row.get("question_id", ""))
            condition = str(row.get("condition", ""))
            identity = (backbone, question_id, condition)
            if not question_id or condition not in CONDITIONS:
                raise ValueError(f"invalid prediction identity: {identity}")
            if identity in seen:
                raise ValueError(f"duplicate prediction identity: {identity}")
            seen.add(identity)
            if row.get("status") != "success" or not str(row.get("predicted_sql", "")).strip():
                continue
            by_question[question_id].append(
                {
                    "backbone": backbone,
                    "condition": condition,
                    "sql": canonical_sql(str(row["predicted_sql"])),
                    "response_hash": row.get("response_hash"),
                }
            )
    return by_question


def _snapshot_index(atomic_rows: Sequence[Mapping[str, Any]]) -> dict[tuple[str, str, str], Mapping[str, Any]]:
    index: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    for row in atomic_rows:
        if row.get("state") != "T0_snapshot":
            continue
        key = (str(row.get("backbone", "")), str(row.get("question_id", "")), str(row.get("condition", "")))
        if key in index:
            raise ValueError(f"duplicate T0 evidence identity: {key}")
        index[key] = row
    return index


def build_diagnostic(
    qwen_rows: Sequence[Mapping[str, Any]],
    granite_rows: Sequence[Mapping[str, Any]],
    atomic_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build diagnostic rows without reading gold-relative agreement fields."""

    sources_by_question = _prediction_sources(qwen_rows, granite_rows)
    snapshot = _snapshot_index(atomic_rows)
    synthesizer = SQLSynthesizer()
    validator = Validator()
    critic = CounterfactualCritic()
    adjudicator = Adjudicator()
    outputs: list[dict[str, Any]] = []

    for question_id in sorted(sources_by_question):
        source_rows = sorted(
            sources_by_question[question_id],
            key=lambda row: ((0 if row["backbone"] == "qwen" else 1), CONDITIONS.index(row["condition"])),
        )
        candidates = synthesizer.package(
            [row["sql"] for row in source_rows], source="frozen_factorial_predictions"
        )
        source_by_sql: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in source_rows:
            source_by_sql[row["sql"]].append(row)
        board = Blackboard(question_id)
        board.post(
            "Frozen Asset Pooler",
            "candidate_pool",
            {
                "diagnostic_label": LABEL,
                "source_prediction_count": len(source_rows),
                "unique_candidate_count": len(candidates),
                "candidates": [
                    {
                        "candidate_id": candidate.candidate_id,
                        "sql_sha256": hashlib.sha256(candidate.sql.encode("utf-8")).hexdigest(),
                        "sources": [
                            {"backbone": row["backbone"], "condition": row["condition"], "response_hash": row["response_hash"]}
                            for row in source_by_sql[candidate.sql]
                        ],
                    }
                    for candidate in candidates
                ],
            },
        )

        validations = {}
        counterfactuals = {}
        evidence_conflicts: list[str] = []
        for candidate in candidates:
            evidence_rows = []
            for source in source_by_sql[candidate.sql]:
                key = (source["backbone"], question_id, source["condition"])
                if key not in snapshot:
                    evidence_conflicts.append(f"missing_T0:{'|'.join(key)}")
                    continue
                evidence_rows.append(snapshot[key])

            def executor(_: str, rows=evidence_rows) -> Mapping[str, Any]:
                if not rows:
                    return {"ok": False, "error": "no frozen T0 execution evidence"}
                exec_values = {bool(row.get("prediction_ok", False)) for row in rows}
                shape_values = {bool(row.get("prediction_vs_metadata_header_match", False)) for row in rows}
                if len(exec_values) != 1 or len(shape_values) != 1:
                    return {"ok": False, "error": "conflicting frozen T0 evidence for identical SQL"}
                return {
                    "ok": next(iter(exec_values)),
                    "shape_ok": next(iter(shape_values)),
                    "order_ok": False,
                    "value_hits": 0,
                }

            validation = validator.validate(candidate, executor)
            validations[candidate.candidate_id] = validation
            board.post("Execution and Safety Validator", "frozen_T0_validation", asdict(validation))

            # formal-v5 agreement fields compare predictions with gold. They are
            # deliberately excluded from selection, so no reference-free
            # counterfactual equivalence evidence is available in these assets.
            cf = critic.review(candidate, [], EXPECTED_STATES)
            counterfactuals[candidate.candidate_id] = cf
            board.post(
                "Counterfactual Critic",
                "coverage_fail_closed",
                {
                    **asdict(cf),
                    "reason": "available multi-state agreement labels are gold-relative and forbidden for candidate selection",
                },
            )

        eligible_count = sum(item.safe and item.executable for item in validations.values())
        if len(candidates) < 2:
            status = "insufficient_unique_candidate_coverage"
            decision = None
        elif eligible_count < 2:
            status = "insufficient_eligible_candidate_coverage"
            decision = None
        else:
            decision = adjudicator.decide(candidates, validations, counterfactuals)
            status = "retrospective_offline_adjudicated"
            board.post("Adjudicator", "retrospective_decision", asdict(decision))
        board.seal()
        outputs.append(
            {
                "diagnostic_label": LABEL,
                "question_id": question_id,
                "status": status,
                "source_prediction_count": len(source_rows),
                "unique_candidate_count": len(candidates),
                "eligible_candidate_count": eligible_count,
                "counterfactual_eligible_candidate_count": 0,
                "counterfactual_binding_status": "fail_closed_gold_relative_only",
                "selected_candidate_id": decision.selected_candidate_id if decision else None,
                "selected_sql_sha256": (
                    hashlib.sha256(decision.selected_sql.encode("utf-8")).hexdigest()
                    if decision and decision.selected_sql
                    else None
                ),
                "evidence_conflicts": sorted(evidence_conflicts),
                "blackboard_sha256": board.audit_digest(),
                "messages": [asdict(message) for message in board.messages],
            }
        )

    statuses = Counter(row["status"] for row in outputs)
    unique_counts = Counter(row["unique_candidate_count"] for row in outputs)
    summary = {
        "diagnostic_label": LABEL,
        "scientific_status": "diagnostic_only_not_new_multi_agent_generation_result",
        "question_count": len(outputs),
        "status_counts": dict(sorted(statuses.items())),
        "unique_candidate_count_distribution": {str(key): value for key, value in sorted(unique_counts.items())},
        "questions_with_at_least_two_unique_candidates": sum(row["unique_candidate_count"] >= 2 for row in outputs),
        "questions_with_at_least_two_eligible_candidates": sum(row["eligible_candidate_count"] >= 2 for row in outputs),
        "questions_with_reference_free_counterfactual_evidence": 0,
        "counterfactual_fail_closed_reason": (
            "formal-v5 multi-state equivalence fields are gold-relative; using them to select a candidate would leak evaluation evidence"
        ),
        "accuracy_claim_authorized": False,
    }
    return outputs, summary


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def run(output_dir: Path, paths: Mapping[str, Path] = DEFAULT_INPUTS) -> dict[str, Any]:
    verified = verify_inputs(paths)
    qwen = load_jsonl(paths["qwen_predictions"])
    granite = load_jsonl(paths["granite_predictions"])
    atomic = load_jsonl(paths["atomic_scores"])
    rows, summary = build_diagnostic(qwen, granite, atomic)
    output_dir = output_dir.resolve()
    if any(output_dir == path.resolve() or output_dir in path.resolve().parents for path in paths.values()):
        raise ValueError("output directory cannot contain or equal a frozen input")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows_path = output_dir / "diagnostic_rows.jsonl"
    summary_path = output_dir / "coverage_summary.json"
    write_jsonl(rows_path, rows)
    write_json(summary_path, summary)
    tool_paths = [HERE / "replay_diagnostic.py", HERE / "ma_sqlgrid_agents.py"]
    manifest = {
        "schema_version": "ma-sqlgrid-retrospective-offline-coordination-diagnostic-v1",
        "diagnostic_label": LABEL,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": verified,
        "tools": {
            path.name: {"sha256": sha256_file(path), "bytes": path.stat().st_size}
            for path in tool_paths
        },
        "outputs": {
            rows_path.name: {"sha256": sha256_file(rows_path), "bytes": rows_path.stat().st_size},
            summary_path.name: {"sha256": sha256_file(summary_path), "bytes": summary_path.stat().st_size},
        },
        "summary": summary,
        "prohibitions": [
            "not a new multi-agent generation result",
            "not an accuracy estimate",
            "not evidence of a counterfactual coordination gain",
            "must not replace or modify any frozen run artifact",
        ],
    }
    write_json(output_dir / "manifest.json", manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=HERE / "retrospective_diagnostic")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    completed = run(arguments.output_dir)
    print(json.dumps(completed["summary"], ensure_ascii=False, indent=2, sort_keys=True))

