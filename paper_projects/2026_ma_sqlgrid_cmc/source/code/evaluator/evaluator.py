#!/usr/bin/env python3
"""Semantic evaluator for GridDB-Maintenance-v2 v0.1."""

from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "question_id",
    "question",
    "gold_sql",
    "order_sensitive",
    "answer_shape",
    "sql_feature_tags",
    "tables",
    "columns",
    "required_value_literals",
    "difficulty",
    "split",
}

FORBIDDEN_SQL_RE = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum|replace\s+into)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class QueryResult:
    ok: bool
    columns: list[str]
    rows: list[tuple[Any, ...]]
    error: str = ""


@dataclass(frozen=True)
class ScoreResult:
    correct: bool
    error_type: str
    details: str
    gold: QueryResult | None = None
    prediction: QueryResult | None = None


def load_questions(path: Path) -> list[dict[str, Any]]:
    questions = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            questions.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return questions


def strip_sql_comments(sql: str) -> str:
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    return sql.strip()


def split_sql_statements(sql: str) -> list[str]:
    statements: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    i = 0
    while i < len(sql):
        ch = sql[i]
        if quote:
            buf.append(ch)
            if ch == quote:
                if i + 1 < len(sql) and sql[i + 1] == quote:
                    buf.append(sql[i + 1])
                    i += 1
                else:
                    quote = None
        else:
            if ch in {"'", '"'}:
                quote = ch
                buf.append(ch)
            elif ch == ";":
                statement = "".join(buf).strip()
                if statement:
                    statements.append(statement)
                buf = []
            else:
                buf.append(ch)
        i += 1
    statement = "".join(buf).strip()
    if statement:
        statements.append(statement)
    return statements


def normalize_sql(sql: str) -> str:
    sql = strip_sql_comments(sql)
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", sql, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        sql = fenced.group(1).strip()
    return sql


def validate_read_only_select(sql: str) -> tuple[bool, str, str]:
    sql = normalize_sql(sql)
    statements = split_sql_statements(sql)
    if len(statements) != 1:
        return False, sql, "only a single statement is allowed"
    statement = statements[0].strip()
    if not re.match(r"^(select|with)\b", statement, flags=re.IGNORECASE):
        return False, statement, "only SELECT or WITH ... SELECT queries are allowed"
    if FORBIDDEN_SQL_RE.search(statement):
        return False, statement, "write or schema-changing SQL is forbidden"
    return True, statement, ""


def execute_sql(conn: sqlite3.Connection, sql: str) -> QueryResult:
    safe, statement, error = validate_read_only_select(sql)
    if not safe:
        return QueryResult(False, [], [], error)
    try:
        cursor = conn.execute(statement)
        columns = [desc[0] for desc in cursor.description or []]
        rows = [tuple(row) for row in cursor.fetchall()]
        return QueryResult(True, columns, rows)
    except sqlite3.Error as exc:
        return QueryResult(False, [], [], str(exc))


def normalize_value(value: Any, *, float_abs_tol: float) -> Any:
    if value is None:
        return ("__NULL__",)
    if isinstance(value, float):
        if math.isnan(value):
            return ("__NAN__",)
        return round(value / float_abs_tol) * float_abs_tol
    return value


def normalize_row(row: tuple[Any, ...], *, float_abs_tol: float) -> tuple[Any, ...]:
    return tuple(normalize_value(value, float_abs_tol=float_abs_tol) for value in row)


def rows_equal(
    pred_rows: list[tuple[Any, ...]],
    gold_rows: list[tuple[Any, ...]],
    *,
    order_sensitive: bool,
    float_abs_tol: float,
) -> bool:
    pred_norm = [normalize_row(row, float_abs_tol=float_abs_tol) for row in pred_rows]
    gold_norm = [normalize_row(row, float_abs_tol=float_abs_tol) for row in gold_rows]
    if order_sensitive:
        return pred_norm == gold_norm
    return Counter(pred_norm) == Counter(gold_norm)


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS - set(record)
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
    shape = record.get("answer_shape")
    if not isinstance(shape, dict):
        errors.append("answer_shape must be an object")
    else:
        columns = shape.get("columns")
        column_count = shape.get("column_count")
        if not isinstance(columns, list) or not all(isinstance(c, str) for c in columns):
            errors.append("answer_shape.columns must be a list of strings")
        if not isinstance(column_count, int) or column_count < 1:
            errors.append("answer_shape.column_count must be a positive integer")
        if isinstance(columns, list) and isinstance(column_count, int) and len(columns) != column_count:
            errors.append("answer_shape.column_count must equal len(answer_shape.columns)")
    for key in ["sql_feature_tags", "tables", "columns", "required_value_literals"]:
        if not isinstance(record.get(key), list):
            errors.append(f"{key} must be a list")
    if record.get("split") not in {"dev", "test"}:
        errors.append("split must be dev or test")
    if record.get("difficulty") not in {"easy", "medium", "hard"}:
        errors.append("difficulty must be easy, medium, or hard")
    if not isinstance(record.get("order_sensitive"), bool):
        errors.append("order_sensitive must be boolean")
    return errors


def score_prediction(
    conn: sqlite3.Connection,
    record: dict[str, Any],
    predicted_sql: str,
    *,
    float_abs_tol: float = 1e-6,
) -> ScoreResult:
    record_errors = validate_record(record)
    if record_errors:
        return ScoreResult(False, "record_invalid", "; ".join(record_errors))
    gold = execute_sql(conn, record["gold_sql"])
    if not gold.ok:
        return ScoreResult(False, "gold_execution_error", gold.error, gold=gold)
    pred = execute_sql(conn, predicted_sql)
    if not pred.ok:
        safe, _, safety_error = validate_read_only_select(predicted_sql)
        error_type = "unsafe_sql" if not safe and "forbidden" in safety_error else "execution_error"
        if not safe and ("only SELECT" in safety_error or "single statement" in safety_error):
            error_type = "unsafe_sql"
        return ScoreResult(False, error_type, pred.error, gold=gold, prediction=pred)
    expected_cols = int(record["answer_shape"]["column_count"])
    if len(pred.columns) != expected_cols:
        return ScoreResult(
            False,
            "shape_mismatch",
            f"predicted {len(pred.columns)} columns, expected {expected_cols}",
            gold=gold,
            prediction=pred,
        )
    if len(gold.columns) != expected_cols:
        return ScoreResult(
            False,
            "gold_shape_mismatch",
            f"gold has {len(gold.columns)} columns, metadata expects {expected_cols}",
            gold=gold,
            prediction=pred,
        )
    if not rows_equal(
        pred.rows,
        gold.rows,
        order_sensitive=bool(record["order_sensitive"]),
        float_abs_tol=float_abs_tol,
    ):
        return ScoreResult(False, "wrong_denotation", "row denotation mismatch", gold=gold, prediction=pred)
    return ScoreResult(True, "correct", "validated denotation match", gold=gold, prediction=pred)


def validate_dataset(db_path: Path, questions_path: Path) -> dict[str, Any]:
    questions = load_questions(questions_path)
    seen: set[str] = set()
    errors: list[str] = []
    conn = sqlite3.connect(db_path)
    try:
        for record in questions:
            qid = str(record.get("question_id", "<missing>"))
            if qid in seen:
                errors.append(f"{qid}: duplicate question_id")
            seen.add(qid)
            for error in validate_record(record):
                errors.append(f"{qid}: {error}")
            score = score_prediction(conn, record, str(record.get("gold_sql", "")))
            if not score.correct:
                errors.append(f"{qid}: gold SQL failed self-score: {score.error_type} {score.details}")
    finally:
        conn.close()
    return {"question_count": len(questions), "error_count": len(errors), "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--questions", required=True, type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if not args.validate_only:
        raise SystemExit("Only --validate-only is supported by this CLI.")
    result = validate_dataset(args.db, args.questions)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["error_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
