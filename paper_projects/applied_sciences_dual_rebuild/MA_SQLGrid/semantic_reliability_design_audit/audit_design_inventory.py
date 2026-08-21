#!/usr/bin/env python3
"""Independent, query-blind diagnostic inventory for the GridDB test-suite design.

This is not the formal semantic-reliability experiment.  It reads the frozen
database/questions/predictions, creates transient in-memory states, and reports
which gold denotations and snapshot-correct predictions are mutation-sensitive.
No source database or formal experiment artifact is modified.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
MA = ROOT / "paper_projects" / "applied_sciences_dual_rebuild" / "MA_SQLGrid"
GRID = ROOT / "paper_projects" / "2026_ma_sqlgrid_cmc" / "source"
DATA = GRID / "data" / "griddb_maintenance_v2_v0_1"
EVALUATOR_PATH = GRID / "code" / "evaluator" / "evaluator.py"
QWEN = MA / "formal_run" / "qwen25coder7b_q4km_seed20260805_clean_rerun1" / "predictions.jsonl"
GRANITE = MA / "granite_formal" / "granite33_8b_q4km_seed20260805_clean1" / "predictions.jsonl"
QWEN_MANIFEST = QWEN.parent / "manifest.json"
GRANITE_MANIFEST = GRANITE.parent / "manifest.json"
CANONICAL_FREEZE = MA / "canonical_v2_reanalysis" / "FREEZE_AND_METHOD.json"
CANONICAL_RELEASE = MA / "canonical_v2_reanalysis" / "release_manifest.json"
OUT = Path(__file__).resolve().parent / "diagnostic_inventory.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_evaluator():
    spec = importlib.util.spec_from_file_location("griddb_evaluator_audit", EVALUATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    import sys

    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def memory_copy() -> sqlite3.Connection:
    source = sqlite3.connect(DATA / "database.sqlite")
    target = sqlite3.connect(":memory:")
    source.backup(target)
    source.close()
    target.execute("PRAGMA foreign_keys=ON")
    return target


def clone_world(conn: sqlite3.Connection, offset: int, mode: str) -> None:
    """Clone a relational world using schema-fixed rules that never inspect SQL."""
    if mode not in {"exact", "numeric_date_shift", "crosslink"}:
        raise ValueError(mode)
    shift = mode == "numeric_date_shift"
    cross = mode == "crosslink"

    conn.execute(
        "INSERT INTO asset_types SELECT asset_type_id+?, type_name, voltage_class, manufacturer, "
        + ("expected_lifetime_years+1" if shift else "expected_lifetime_years")
        + " FROM asset_types WHERE asset_type_id < ?",
        (offset, offset),
    )
    conn.execute(
        "INSERT INTO locations SELECT location_id+?, location_name, region, "
        + ("latitude+0.01, longitude-0.01" if shift else "latitude, longitude")
        + ", criticality FROM locations WHERE location_id < ?",
        (offset, offset),
    )
    conn.execute(
        "INSERT INTO technicians SELECT technician_id+?, technician_name, specialty, home_region, active "
        "FROM technicians WHERE technician_id < ?",
        (offset, offset),
    )

    type_ids = [r[0] for r in conn.execute("SELECT asset_type_id FROM asset_types WHERE asset_type_id < ? ORDER BY 1", (offset,))]
    loc_ids = [r[0] for r in conn.execute("SELECT location_id FROM locations WHERE location_id < ? ORDER BY 1", (offset,))]
    tech_ids = [r[0] for r in conn.execute("SELECT technician_id FROM technicians WHERE technician_id < ? ORDER BY 1", (offset,))]
    rotate_type = {v: type_ids[(i + 1) % len(type_ids)] for i, v in enumerate(type_ids)}
    rotate_loc = {v: loc_ids[(i + 1) % len(loc_ids)] for i, v in enumerate(loc_ids)}
    rotate_tech = {v: tech_ids[(i + 1) % len(tech_ids)] for i, v in enumerate(tech_ids)}

    assets = list(conn.execute("SELECT * FROM assets WHERE asset_id < ? ORDER BY asset_id", (offset,)))
    conn.executemany(
        "INSERT INTO assets VALUES (?,?,?,?,?,?,?)",
        [
            (
                a[0] + offset,
                a[1],
                (rotate_type[a[2]] if cross else a[2]) + offset,
                (rotate_loc[a[3]] if cross else a[3]) + offset,
                conn.execute("SELECT date(?, '+1 day')", (a[4],)).fetchone()[0] if shift else a[4],
                a[5],
                a[6] + 0.125 if shift else a[6],
            )
            for a in assets
        ],
    )
    work_orders = list(conn.execute("SELECT * FROM work_orders WHERE work_order_id < ? ORDER BY work_order_id", (offset,)))
    conn.executemany(
        "INSERT INTO work_orders VALUES (?,?,?,?,?,?,?,?)",
        [
            (
                w[0] + offset,
                w[1] + offset,
                (rotate_tech[w[2]] if cross else w[2]) + offset,
                w[3],
                w[4],
                conn.execute("SELECT date(?, '+1 day')", (w[5],)).fetchone()[0] if shift else w[5],
                (conn.execute("SELECT date(?, '+1 day')", (w[6],)).fetchone()[0] if shift and w[6] else w[6]),
                w[7],
            )
            for w in work_orders
        ],
    )
    logs = list(conn.execute("SELECT * FROM maintenance_logs WHERE log_id < ? ORDER BY log_id", (offset,)))
    conn.executemany(
        "INSERT INTO maintenance_logs VALUES (?,?,?,?,?,?,?,?)",
        [
            (
                m[0] + offset,
                m[1] + offset,
                (rotate_tech[m[2]] if cross else m[2]) + offset,
                m[3],
                conn.execute("SELECT datetime(?, '+1 hour')", (m[4],)).fetchone()[0] if shift else m[4],
                conn.execute("SELECT datetime(?, '+1 hour')", (m[5],)).fetchone()[0] if shift else m[5],
                m[6],
                m[7] + 0.125 if shift else m[7],
            )
            for m in logs
        ],
    )
    readings = list(conn.execute("SELECT * FROM sensor_readings WHERE reading_id < ? ORDER BY reading_id", (offset,)))
    conn.executemany(
        "INSERT INTO sensor_readings VALUES (?,?,?,?,?,?,?)",
        [
            (
                s[0] + offset,
                s[1] + offset,
                conn.execute("SELECT datetime(?, '+1 hour')", (s[2],)).fetchone()[0] if shift else s[2],
                s[3],
                s[4] + 0.125 if shift else s[4],
                s[5],
                s[6],
            )
            for s in readings
        ],
    )
    edges = list(conn.execute("SELECT * FROM grid_topology WHERE edge_id < ? ORDER BY edge_id", (offset,)))
    statuses = sorted({e[4] for e in edges})
    toggle = {v: statuses[(i + 1) % len(statuses)] for i, v in enumerate(statuses)}
    conn.executemany(
        "INSERT INTO grid_topology VALUES (?,?,?,?,?)",
        [
            (
                e[0] + offset,
                (e[2] if cross else e[1]) + offset,
                (e[1] if cross else e[2]) + offset,
                e[3],
                toggle[e[4]] if cross else e[4],
            )
            for e in edges
        ],
    )
    conn.commit()


def null_completion_clone(conn: sqlite3.Connection, offset: int = 4000) -> None:
    """Clone all work orders while toggling the schema's sole nullable field."""
    rows = list(conn.execute("SELECT * FROM work_orders WHERE work_order_id < ? ORDER BY work_order_id", (offset,)))
    conn.executemany(
        "INSERT INTO work_orders VALUES (?,?,?,?,?,?,?,?)",
        [
            (
                w[0] + offset,
                w[1],
                w[2],
                w[3],
                w[4],
                w[5],
                (conn.execute("SELECT date(?, '+7 day')", (w[5],)).fetchone()[0] if w[6] is None else None),
                w[7],
            )
            for w in rows
        ],
    )
    conn.commit()


def make_states() -> dict[str, sqlite3.Connection]:
    states = {"S0_snapshot": memory_copy()}
    for name, offset, mode in (
        # Offsets exceed every original primary key (work orders start at 1001).
        ("S1_exact_relational_clone", 10000, "exact"),
        ("S2_numeric_date_shift_clone", 20000, "numeric_date_shift"),
        ("S3_crosslink_topology_decoys", 30000, "crosslink"),
    ):
        conn = memory_copy()
        clone_world(conn, offset, mode)
        states[name] = conn
    conn = memory_copy()
    null_completion_clone(conn)
    states["S4_nullable_completion_toggle"] = conn
    return states


def result_changed(evaluator, base, altered, order_sensitive: bool) -> bool:
    if not base.ok or not altered.ok:
        return base.ok != altered.ok or base.error != altered.error
    if base.columns != altered.columns:
        return True
    return not evaluator.rows_equal(
        base.rows, altered.rows, order_sensitive=order_sensitive, float_abs_tol=1e-6
    )


def main() -> None:
    evaluator = load_evaluator()
    questions = [q for q in load_jsonl(DATA / "questions.jsonl") if q["split"] == "test"]
    by_qid = {q["question_id"]: q for q in questions}
    predictions = {"qwen": load_jsonl(QWEN), "granite": load_jsonl(GRANITE)}
    manifests = {
        "qwen": json.loads(QWEN_MANIFEST.read_text(encoding="utf-8")),
        "granite": json.loads(GRANITE_MANIFEST.read_text(encoding="utf-8")),
    }
    prediction_paths = {"qwen": QWEN, "granite": GRANITE}
    manifest_paths = {"qwen": QWEN_MANIFEST, "granite": GRANITE_MANIFEST}
    canonical_freeze = json.loads(CANONICAL_FREEZE.read_text(encoding="utf-8"))
    canonical_release = json.loads(CANONICAL_RELEASE.read_text(encoding="utf-8"))
    states = make_states()

    qids = {q["question_id"] for q in questions}
    ledger_integrity: dict[str, Any] = {}
    for backbone, rows in predictions.items():
        manifest = manifests[backbone]
        cells = set(manifest["cells"])
        keys = [(r.get("question_id"), r.get("condition")) for r in rows]
        expected_keys = {(qid, cell) for qid in qids for cell in cells}
        actual_keys = set(keys)
        freeze_inputs = canonical_freeze["accepted_inputs"]
        pred_rel = str(prediction_paths[backbone].relative_to(ROOT)).replace("\\", "/")
        manifest_rel = str(manifest_paths[backbone].relative_to(ROOT)).replace("\\", "/")
        field_hash_sets = {
            field: sorted({str(r.get(field)) for r in rows})
            for field in ("data_sha256", "code_sha256", "configuration_sha256")
        }
        manifest_hashes = manifest["hashes"]
        field_hash_match = {
            field: field_hash_sets[field] == [str(manifest_hashes[field])]
            for field in field_hash_sets
        }
        ledger_integrity[backbone] = {
            "row_count": len(rows),
            "manifest_expected_predictions": manifest["expected_predictions"],
            "unique_question_condition_key_count": len(actual_keys),
            "duplicate_key_count": len(keys) - len(actual_keys),
            "missing_expected_keys": [list(k) for k in sorted(expected_keys - actual_keys)],
            "unexpected_keys": [list(k) for k in sorted(actual_keys - expected_keys)],
            "question_id_count": len({k[0] for k in actual_keys}),
            "condition_count": len({k[1] for k in actual_keys}),
            "status_counts": dict(Counter(str(r.get("status")) for r in rows)),
            "field_hash_sets": field_hash_sets,
            "prediction_fields_match_run_manifest": field_hash_match,
            "manifest_status_completed": manifest.get("status") == "completed",
            "manifest_canonical_result_eligible": manifest.get("canonical_result_eligible") is True,
            "prediction_file_bound_in_canonical_freeze": pred_rel in freeze_inputs,
            "prediction_file_matches_canonical_freeze": (
                pred_rel in freeze_inputs and sha256(prediction_paths[backbone]) == freeze_inputs[pred_rel]["sha256"]
            ),
            "run_manifest_bound_in_canonical_freeze": manifest_rel in freeze_inputs,
            "run_manifest_matches_canonical_freeze": (
                manifest_rel in freeze_inputs and sha256(manifest_paths[backbone]) == freeze_inputs[manifest_rel]["sha256"]
            ),
        }
        ledger_integrity[backbone]["pass"] = all(
            (
                len(rows) == 720,
                manifest["expected_predictions"] == 720,
                len(actual_keys) == 720,
                len(keys) == len(actual_keys),
                actual_keys == expected_keys,
                ledger_integrity[backbone]["status_counts"] == {"success": 720},
                all(field_hash_match.values()),
                ledger_integrity[backbone]["manifest_status_completed"],
                ledger_integrity[backbone]["manifest_canonical_result_eligible"],
                ledger_integrity[backbone]["prediction_file_matches_canonical_freeze"],
                ledger_integrity[backbone]["run_manifest_matches_canonical_freeze"],
            )
        )

    state_audit: dict[str, Any] = {}
    gold_results: dict[str, dict[str, Any]] = defaultdict(dict)
    for state_name, conn in states.items():
        fk = conn.execute("PRAGMA foreign_key_check").fetchall()
        counts = {
            name: conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
            for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        }
        state_audit[state_name] = {"foreign_key_violation_count": len(fk), "table_row_counts": counts}
        for q in questions:
            gold_results[state_name][q["question_id"]] = evaluator.execute_sql(conn, q["gold_sql"])
        gold_error_ids = [qid for qid, result in gold_results[state_name].items() if not result.ok]
        state_audit[state_name]["gold_execution_error_count"] = len(gold_error_ids)
        state_audit[state_name]["gold_execution_error_question_ids"] = gold_error_ids

    sensitivity: dict[str, list[str]] = {}
    per_question_states: dict[str, list[str]] = defaultdict(list)
    for state_name in list(states)[1:]:
        changed = []
        for q in questions:
            qid = q["question_id"]
            if result_changed(
                evaluator,
                gold_results["S0_snapshot"][qid],
                gold_results[state_name][qid],
                bool(q["order_sensitive"]),
            ):
                changed.append(qid)
                per_question_states[qid].append(state_name)
        sensitivity[state_name] = changed

    prediction_audit: dict[str, Any] = {}
    for backbone, rows in predictions.items():
        by_state_correct: dict[str, set[tuple[str, str]]] = {}
        for state_name, conn in states.items():
            correct: set[tuple[str, str]] = set()
            for row in rows:
                key = (row["question_id"], row["condition"])
                score = evaluator.score_prediction(conn, by_qid[row["question_id"]], row["predicted_sql"])
                if score.correct:
                    correct.add(key)
            by_state_correct[state_name] = correct
        base = by_state_correct["S0_snapshot"]
        suite = set.intersection(*by_state_correct.values())
        prediction_audit[backbone] = {
            "prediction_rows": len(rows),
            "snapshot_correct_pairs": len(base),
            "all_state_suite_correct_pairs": len(suite),
            "snapshot_correct_rejected_by_suite": len(base - suite),
            "rejected_pair_examples": [list(x) for x in sorted(base - suite)[:30]],
            "correct_pairs_by_state": {k: len(v) for k, v in by_state_correct.items()},
        }

    tags: dict[str, list[str]] = defaultdict(list)
    for q in questions:
        for tag in q["sql_feature_tags"]:
            tags[tag].append(q["question_id"])
    empty_snapshot = [
        q["question_id"] for q in questions if len(gold_results["S0_snapshot"][q["question_id"]].rows) == 0
    ]
    inventory = {
        "scope": "independent design diagnostic; not the formal experiment and not claim-promoting evidence",
        "query_blinding": (
            "Mutation constructors are fixed by the GridDB schema and base rows; they do not read gold SQL, "
            "questions, predictions, scores, or correctness when constructing states."
        ),
        "inputs": {
            str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
            for path in (DATA / "database.sqlite", DATA / "questions.jsonl", EVALUATOR_PATH, QWEN, GRANITE)
        },
        "sqlite_runtime": sqlite3.sqlite_version,
        "test_question_count": len(questions),
        "prediction_row_counts": {k: len(v) for k, v in predictions.items()},
        "prediction_ledger_integrity": ledger_integrity,
        "canonical_release_manifest_passed": canonical_release.get("passed") is True,
        "evaluator_contract_checks": {
            "unordered_is_duplicate_preserving_multiset": (
                not evaluator.rows_equal([(1,), (1,)], [(1,)], order_sensitive=False, float_abs_tol=1e-6)
            ),
            "unordered_ignores_order": evaluator.rows_equal(
                [(1,), (2,)], [(2,), (1,)], order_sensitive=False, float_abs_tol=1e-6
            ),
            "ordered_enforces_order": (
                not evaluator.rows_equal([(1,), (2,)], [(2,), (1,)], order_sensitive=True, float_abs_tol=1e-6)
            ),
            "null_has_distinct_sentinel": (
                not evaluator.rows_equal([(None,)], [("__NULL__",)], order_sensitive=True, float_abs_tol=1e-6)
            ),
            "integer_and_equal_float_compare_equal": evaluator.rows_equal(
                [(1,)], [(1.0,)], order_sensitive=True, float_abs_tol=1e-6
            ),
            "float_quantization_can_reject_values_within_abs_tol": (
                not evaluator.rows_equal([(0.49e-6,)], [(0.51e-6,)], order_sensitive=True, float_abs_tol=1e-6)
            ),
            "column_labels_are_not_compared_by_score_prediction": True,
            "column_label_finding_basis": (
                "score_prediction checks len(pred.columns) and len(gold.columns), then calls rows_equal; "
                "it contains no pred.columns == gold.columns or metadata-name comparison."
            ),
        },
        "feature_question_ids": dict(sorted(tags.items())),
        "empty_snapshot_question_ids": empty_snapshot,
        "gold_denotation_sensitivity": {
            "changed_count_by_state": {k: len(v) for k, v in sensitivity.items()},
            "changed_question_ids_by_state": sensitivity,
            "question_ids_changed_in_any_state": sorted(per_question_states),
            "question_ids_unchanged_in_all_diagnostic_states": sorted(set(by_qid) - set(per_question_states)),
            "states_by_question_id": dict(sorted(per_question_states.items())),
        },
        "state_integrity": state_audit,
        "prediction_diagnostic": prediction_audit,
    }
    OUT.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT),
        "gold_changed": inventory["gold_denotation_sensitivity"]["changed_count_by_state"],
        "predictions": prediction_audit,
    }, indent=2, sort_keys=True))
    for conn in states.values():
        conn.close()


if __name__ == "__main__":
    main()
