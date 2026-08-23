"""Generate R3 descriptive evidence tables from retained, immutable ledgers.

This script performs no model call, changes no source/frozen artifact, and does
not select or tune a rule.  It only recomputes complete numeric tables requested
in the Round-2 reviews and records source hashes for traceability.
"""

from __future__ import annotations

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[4]
MA = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid"
REBUILD = MA / "original_title_rebuild"
V3 = REBUILD / "prospective_from_freeze_offline_study_v3"
OUT = MA / "original_title_manuscript/R3_staging/evidence_tables"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def source(path: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def decision(board: dict[str, Any], method: str) -> dict[str, Any]:
    kind = f"decision:{method}"
    return next(m["payload"] for m in board["messages"] if m["kind"] == kind)


def candidate_sources(board: dict[str, Any]) -> dict[str, str]:
    pool = next(m["payload"] for m in board["messages"] if m["kind"] == "eight_slot_candidate_pool")
    return {row["candidate_id"]: row["source"] for row in pool["candidates"]}


def tie_tables(boards: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    item_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    methods = [
        "validation_rank_equal_budget_no_cf",
        "full_coordination_complete_metamorphic",
    ]
    for method in methods:
        multiplicities: Counter[int] = Counter()
        selected_sources: Counter[str] = Counter()
        for board in boards:
            payload = decision(board, method)
            sources = candidate_sources(board)
            eligible = [row for row in payload["scores"] if row["eligible"]]
            top_score = max(row["validation_points"] for row in eligible)
            tied = [row for row in eligible if row["validation_points"] == top_score]
            selected = payload["selected_candidate_id"]
            multiplicities[len(tied)] += 1
            selected_sources[sources[selected]] += 1
            item_rows.append(
                {
                    "question_id": board["question_id"],
                    "method": method,
                    "eligible_candidates": len(eligible),
                    "top_validation_points": top_score,
                    "top_tie_multiplicity": len(tied),
                    "top_candidate_ids": "|".join(row["candidate_id"] for row in tied),
                    "top_sources": "|".join(sources[row["candidate_id"]] for row in tied),
                    "selected_candidate_id": selected,
                    "selected_source": sources[selected],
                    "tie_rule": "original_candidate_order",
                }
            )
        summary_rows.append(
            {
                "method": method,
                "questions": len(boards),
                "questions_with_top_tie": sum(n for k, n in multiplicities.items() if k > 1),
                "mean_top_tie_multiplicity": sum(k * n for k, n in multiplicities.items()) / len(boards),
                "multiplicity_counts": dict(sorted(multiplicities.items())),
                "selected_source_counts": dict(sorted(selected_sources.items())),
            }
        )
    return item_rows, summary_rows


def griddb_cells(paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for backbone, path in paths.items():
        scores = jsonl(path)
        for condition in sorted({row["condition"] for row in scores}):
            cell = [row for row in scores if row["condition"] == condition]
            correct = sum(bool(row["correct"]) for row in cell)
            rows.append(
                {
                    "backbone": backbone,
                    "condition": condition,
                    "correct": correct,
                    "n": len(cell),
                    "rate": correct / len(cell),
                    "status": "development-visible synthetic GridDB descriptive cell",
                }
            )
    return rows


def component_endpoints(paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    endpoints = [
        "first_correct",
        "validator_selected_correct",
        "oracle_at_3_correct_diagnostic_only",
    ]
    for backbone, path in paths.items():
        scored = jsonl(path)
        for condition in sorted({row["condition"] for row in scored}):
            cell = [row for row in scored if row["condition"] == condition]
            for endpoint in endpoints:
                observed = [row[endpoint] for row in cell if row.get(endpoint) is not None]
                if not observed:
                    continue
                correct = sum(bool(value) for value in observed)
                rows.append(
                    {
                        "backbone": backbone,
                        "condition": condition,
                        "endpoint": endpoint,
                        "correct": correct,
                        "n": len(observed),
                        "rate": correct / len(observed),
                        "status": "descriptive; oracle endpoint is gold-only upper bound",
                    }
                )
    return rows


def multistate_cells(path: Path) -> list[dict[str, Any]]:
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))
    out: list[dict[str, Any]] = []
    for backbone in sorted({row["backbone"] for row in rows}):
        for condition in sorted({row["condition"] for row in rows}):
            cell = [
                row
                for row in rows
                if row["backbone"] == backbone
                and row["condition"] == condition
                and row["automatic_primary_eligible"] == "True"
            ]
            values = [row["suite_15state_and"] == "True" for row in cell]
            passed = sum(values)
            out.append(
                {
                    "backbone": backbone,
                    "condition": condition,
                    "passed_all_15_states": passed,
                    "n": len(values),
                    "rate": passed / len(values),
                    "status": "constructed-state diagnostic; automatic 66-question subset",
                }
            )
    return out


def sensitivity(path: Path) -> list[dict[str, Any]]:
    summary = json.loads(path.read_text(encoding="utf-8"))
    return [
        {
            "weight_policy": row["weight_policy"],
            "minimum_invariant_passes": row["minimum_invariant_passes"],
            "tie_rule": row["tie_rule"],
            "correct": row["correct"],
            "covered": row["covered"],
            "n": summary["question_count"],
            "accuracy_all": row["accuracy_all"],
            "status": "outcome-exposed descriptive sensitivity",
        }
        for row in summary["sensitivity"]
    ]


def q039_trace(selection_path: Path, evaluation_path: Path) -> list[dict[str, Any]]:
    selections = {
        row["method"]: row for row in jsonl(selection_path) if row["question_id"] == "Q039"
    }
    evaluations = {
        row["method"]: row for row in jsonl(evaluation_path) if row["question_id"] == "Q039"
    }
    out = []
    for method, row in selections.items():
        evaluation = evaluations[method]
        out.append(
            {
                "question_id": "Q039",
                "method": method,
                "selected_candidate_id": row["selected_candidate_id"],
                "selected_sql": row["selected_sql"],
                "correct": evaluation["correct"],
                "robust_invariance": evaluation["robust_invariance"],
                "gold_access_phase": evaluation["gold_access_phase"],
                "interpretation": "outcome-exposed synthetic projection-stability trace; not a general gain",
            }
        )
    return out


def markdown_table(rows: Iterable[dict[str, Any]], columns: list[str]) -> str:
    data = list(rows)
    header = "| " + " | ".join(columns) + " |"
    rule = "|" + "|".join(["---"] * len(columns)) + "|"
    body = []
    for row in data:
        values = []
        for column in columns:
            value = row[column]
            if isinstance(value, float):
                value = f"{value:.4f}"
            values.append(str(value))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, rule, *body])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {
        "boards": V3 / "run_v3a/blackboards_sealed_before_gold.jsonl",
        "v3_summary": V3 / "run_v3a/summary.json",
        "v3_selection": V3 / "run_v3a/selection_ledger_pre_gold.jsonl",
        "v3_evaluation": V3 / "run_v3a/evaluation_ledger.jsonl",
        "qwen_scores": MA / "formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1/scores.jsonl",
        "granite_scores": MA / "granite_formal/granite33_8b_q4km_seed20260805_clean1/scores.jsonl",
        "qwen_component": MA / "prospective_component_experiments/runs/qwen/scored_rows.jsonl",
        "granite_component": MA / "prospective_component_experiments/runs/granite/scored_rows.jsonl",
        "multistate": MA / "semantic_reliability_experiment/formal_v5_analysis/suite_outcomes.csv",
    }
    ties, tie_summary = tie_tables(jsonl(paths["boards"]))
    cells = griddb_cells({"qwen": paths["qwen_scores"], "granite": paths["granite_scores"]})
    components = component_endpoints(
        {"qwen": paths["qwen_component"], "granite": paths["granite_component"]}
    )
    states = multistate_cells(paths["multistate"])
    sensitivities = sensitivity(paths["v3_summary"])
    q039 = q039_trace(paths["v3_selection"], paths["v3_evaluation"])

    write_csv(OUT / "top_tie_item_level.csv", ties)
    write_csv(OUT / "griddb_8_cells.csv", cells)
    write_csv(OUT / "component_endpoints.csv", components)
    write_csv(OUT / "multistate_8_cells.csv", states)
    write_csv(OUT / "selector_sensitivity_18_cells.csv", sensitivities)
    write_csv(OUT / "q039_projection_trace.csv", q039)

    artifact = {
        "schema_version": "ma-sqlgrid-r3-descriptive-evidence-tables-v1",
        "evidence_class": "descriptive recomputation from retained historical ledgers; no model generation and no rule selection",
        "source_artifacts": {name: source(path) for name, path in paths.items()},
        "top_tie_summary": tie_summary,
        "griddb_8_cells": cells,
        "component_endpoints": components,
        "multistate_8_cells": states,
        "selector_sensitivity_18_cells": sensitivities,
        "q039_projection_trace": q039,
        "integrity_checks": {
            "tie_item_rows": len(ties),
            "tie_expected_rows": 360,
            "top_ties_each_method": [row["questions_with_top_tie"] for row in tie_summary],
            "griddb_cells": len(cells),
            "component_endpoint_rows": len(components),
            "multistate_cells": len(states),
            "sensitivity_cells": len(sensitivities),
            "q039_method_rows": len(q039),
        },
    }
    if len(ties) != 360 or len(cells) != 8 or len(states) != 8 or len(sensitivities) != 18:
        raise RuntimeError(f"evidence-table cardinality failure: {artifact['integrity_checks']}")
    if [row["questions_with_top_tie"] for row in tie_summary] != [130, 130]:
        raise RuntimeError(f"unexpected tie counts: {tie_summary}")
    json_path = OUT / "R3_EVIDENCE_TABLES.json"
    json_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# MA-SQLGrid R3 Complete Descriptive Evidence Tables",
        "",
        "These tables are deterministic recomputations from retained ledgers. They involve no model call, no new label, and no post-hoc rule selection. Source paths, SHA-256 values, and byte counts are recorded in `R3_EVIDENCE_TABLES.json`.",
        "",
        "## Top-tie diagnostic",
        "",
        markdown_table(
            [
                {
                    "method": row["method"],
                    "questions": row["questions"],
                    "top_ties": row["questions_with_top_tie"],
                    "mean_multiplicity": row["mean_top_tie_multiplicity"],
                    "multiplicity_counts": json.dumps(row["multiplicity_counts"], sort_keys=True),
                }
                for row in tie_summary
            ],
            ["method", "questions", "top_ties", "mean_multiplicity", "multiplicity_counts"],
        ),
        "",
        "The original-order rule is arbitrary for this outcome-exposed release. The complete 360-row item table and selected-source distributions are retained in the JSON/CSV artifacts.",
        "",
        "## GridDB eight cells",
        "",
        markdown_table(cells, ["backbone", "condition", "correct", "n", "rate"]),
        "",
        "## Component endpoints",
        "",
        markdown_table(components, ["backbone", "condition", "endpoint", "correct", "n", "rate"]),
        "",
        "## Fifteen-state eight cells",
        "",
        markdown_table(states, ["backbone", "condition", "passed_all_15_states", "n", "rate"]),
        "",
        "## Selector sensitivity: all 18 cells",
        "",
        markdown_table(
            sensitivities,
            ["weight_policy", "minimum_invariant_passes", "tie_rule", "correct", "covered", "n", "accuracy_all"],
        ),
        "",
        "## Q039 projection trace",
        "",
        markdown_table(
            q039,
            ["method", "selected_candidate_id", "correct", "robust_invariance", "gold_access_phase"],
        ),
        "",
        "Q039 is an outcome-exposed synthetic projection trace. The SQL text is retained in the JSON/CSV artifact; this case is not evidence of a general semantic rescue, counterfactual-reasoning benefit, robustness gain, or multi-agent gain.",
        "",
    ]
    (OUT / "R3_EVIDENCE_TABLES.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
