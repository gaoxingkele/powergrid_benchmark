from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path.insert(0, str(ROOT))

from evaluator import execute_sql, load_questions, score_prediction, validate_dataset, validate_read_only_select  # noqa: E402


DATA_DIR = WORKSPACE / "data" / "griddb_maintenance_v2_v0_1"
DB_PATH = DATA_DIR / "database.sqlite"
QUESTIONS_PATH = DATA_DIR / "questions.jsonl"


def connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def by_id(question_id: str) -> dict:
    for record in load_questions(QUESTIONS_PATH):
        if record["question_id"] == question_id:
            return record
    raise AssertionError(f"missing {question_id}")


def test_dataset_records_validate_and_gold_sql_executes() -> None:
    result = validate_dataset(DB_PATH, QUESTIONS_PATH)
    assert result["question_count"] >= 80
    assert result["error_count"] == 0, result["errors"][:5]


def test_unordered_row_equivalence_ignores_row_order() -> None:
    record = dict(by_id("Q021"))
    record["order_sensitive"] = False
    predicted = "SELECT asset_name FROM assets WHERE status = 'offline' ORDER BY asset_name DESC;"
    conn = connect()
    try:
        score = score_prediction(conn, record, predicted)
    finally:
        conn.close()
    assert score.correct


def test_order_sensitive_topk_requires_order() -> None:
    record = by_id("Q015")
    predicted = (
        "SELECT a.asset_name, s.reading_value "
        "FROM sensor_readings s JOIN assets a ON s.asset_id = a.asset_id "
        "WHERE s.sensor_type = 'temperature' AND s.alarm_flag = 1 "
        "ORDER BY s.reading_value ASC LIMIT 1;"
    )
    conn = connect()
    try:
        score = score_prediction(conn, record, predicted)
    finally:
        conn.close()
    assert not score.correct
    assert score.error_type == "wrong_denotation"


def test_aliases_do_not_affect_correctness() -> None:
    record = by_id("Q001")
    predicted = "SELECT COUNT(*) AS totally_different_alias FROM assets WHERE status = 'in_service';"
    conn = connect()
    try:
        score = score_prediction(conn, record, predicted)
    finally:
        conn.close()
    assert score.correct


def test_projection_shape_mismatch_fails() -> None:
    record = by_id("Q001")
    predicted = "SELECT COUNT(*) AS asset_count, status FROM assets WHERE status = 'in_service';"
    conn = connect()
    try:
        score = score_prediction(conn, record, predicted)
    finally:
        conn.close()
    assert not score.correct
    assert score.error_type in {"shape_mismatch", "execution_error"}


def test_null_normalization_scores_equivalent_null_results() -> None:
    record = by_id("Q010")
    predicted = (
        "SELECT work_order_id, status, NULL AS scheduled_date "
        "FROM work_orders WHERE completed_date IS NULL ORDER BY work_order_id;"
    )
    conn = connect()
    try:
        wrong = score_prediction(conn, record, predicted)
        correct = score_prediction(conn, record, record["gold_sql"])
    finally:
        conn.close()
    assert correct.correct
    assert not wrong.correct


def test_float_tolerance_allows_small_difference() -> None:
    record = by_id("Q057")
    predicted = "SELECT ROUND(AVG(reading_value), 2) + 0.0000004 AS avg_voltage_kv FROM sensor_readings WHERE sensor_type = 'voltage';"
    conn = connect()
    try:
        score = score_prediction(conn, record, predicted, float_abs_tol=1e-5)
    finally:
        conn.close()
    assert score.correct


def test_invalid_sql_is_tagged_without_crashing() -> None:
    record = by_id("Q001")
    conn = connect()
    try:
        score = score_prediction(conn, record, "SELECT FROM WHERE")
    finally:
        conn.close()
    assert not score.correct
    assert score.error_type == "execution_error"


def test_non_select_sql_is_rejected() -> None:
    ok, _, reason = validate_read_only_select("UPDATE assets SET status = 'offline'")
    assert not ok
    assert "SELECT" in reason


def test_scalar_replace_function_is_allowed() -> None:
    record = by_id("Q020")
    conn = connect()
    try:
        score = score_prediction(conn, record, record["gold_sql"])
    finally:
        conn.close()
    assert score.correct


def test_multiple_statements_are_rejected() -> None:
    ok, _, reason = validate_read_only_select("SELECT 1; SELECT 2;")
    assert not ok
    assert "single statement" in reason


def test_old_pilot_regression_analogs_are_present_and_score() -> None:
    conn = connect()
    try:
        for qid in ["Q001", "Q003", "Q009", "Q013", "Q015", "Q024"]:
            record = by_id(qid)
            assert score_prediction(conn, record, record["gold_sql"]).correct
    finally:
        conn.close()


def test_execute_sql_allows_replace_in_select() -> None:
    conn = connect()
    try:
        result = execute_sql(conn, "SELECT REPLACE('TX-001', '-', '') AS normalized")
    finally:
        conn.close()
    assert result.ok
    assert result.rows == [("TX001",)]
