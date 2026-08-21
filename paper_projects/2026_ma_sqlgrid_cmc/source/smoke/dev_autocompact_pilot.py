#!/usr/bin/env python3
"""Dev-only AutoCompact context pilot.

Compares schema-only, full-context, automatic compact context, and automatic
compact context with one validation/repair attempt. This remains pre-three-pack
evidence and must not be treated as a formal experiment.
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from collections import Counter, deque
from dataclasses import asdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
OUT_DIR = WORKSPACE / "smoke" / "dev_autocompact"
PREDICTIONS_PATH = OUT_DIR / "predictions.jsonl"
SCORES_PATH = OUT_DIR / "scores.jsonl"
CONTEXTS_PATH = OUT_DIR / "contexts.jsonl"
REPORT_PATH = OUT_DIR / "dev_autocompact_report.md"
TRACE_DIR = OUT_DIR / "traces"

sys.path.insert(0, str(WORKSPACE / "smoke"))

import dev_superiority_pilot as dev_pilot  # noqa: E402
import minimal_text2sql_smoke as smoke  # noqa: E402


TABLE_COLUMNS = {
    "asset_types": ["asset_type_id", "type_name", "voltage_class", "manufacturer", "expected_lifetime_years"],
    "locations": ["location_id", "location_name", "region", "latitude", "longitude", "criticality"],
    "assets": ["asset_id", "asset_name", "asset_type_id", "location_id", "install_date", "status", "capacity_mw"],
    "technicians": ["technician_id", "technician_name", "specialty", "home_region", "active"],
    "work_orders": [
        "work_order_id",
        "asset_id",
        "assigned_technician_id",
        "priority",
        "status",
        "scheduled_date",
        "completed_date",
        "fault_code",
    ],
    "maintenance_logs": ["log_id", "work_order_id", "technician_id", "action_type", "started_at", "ended_at", "notes", "parts_cost"],
    "sensor_readings": ["reading_id", "asset_id", "reading_time", "sensor_type", "reading_value", "unit", "alarm_flag"],
    "grid_topology": ["edge_id", "upstream_asset_id", "downstream_asset_id", "connection_type", "switch_status"],
}

FOREIGN_KEYS = [
    ("assets", "asset_type_id", "asset_types", "asset_type_id"),
    ("assets", "location_id", "locations", "location_id"),
    ("work_orders", "asset_id", "assets", "asset_id"),
    ("work_orders", "assigned_technician_id", "technicians", "technician_id"),
    ("maintenance_logs", "work_order_id", "work_orders", "work_order_id"),
    ("maintenance_logs", "technician_id", "technicians", "technician_id"),
    ("sensor_readings", "asset_id", "assets", "asset_id"),
    ("grid_topology", "upstream_asset_id", "assets", "asset_id"),
    ("grid_topology", "downstream_asset_id", "assets", "asset_id"),
]

TABLE_HINTS = {
    "asset_types": {"type", "types", "transformer", "breaker", "substation", "relay", "line", "capacitor", "manufacturer", "voltage"},
    "locations": {"location", "locations", "region", "regions", "critical", "criticality", "south", "north", "east", "west", "central", "yard", "hub"},
    "assets": {"asset", "assets", "transformer", "breaker", "substation", "relay", "line", "capacitor", "installed", "capacity", "status"},
    "technicians": {"technician", "technicians", "specialty", "active", "assigned"},
    "work_orders": {"work", "order", "orders", "priority", "open", "scheduled", "completed", "fault", "high"},
    "maintenance_logs": {"maintenance", "log", "logs", "parts", "cost", "action", "repair", "inspection", "calibration"},
    "sensor_readings": {"sensor", "reading", "readings", "temperature", "voltage", "load", "alarm", "alarmed", "latest", "average"},
    "grid_topology": {"topology", "downstream", "upstream", "connected", "feeder", "feeders", "switch", "closed", "open"},
}

COLUMN_HINTS = {
    "asset_name": {"asset", "assets", "name", "names", "tx", "br", "ln", "rel", "sub", "cap"},
    "status": {"status", "open", "scheduled", "completed", "offline", "maintenance", "service", "in-service", "in_service"},
    "type_name": {"type", "transformer", "breaker", "substation", "relay", "line", "capacitor"},
    "region": {"region", "regions", "north", "south", "east", "west", "central"},
    "criticality": {"critical", "criticality", "low", "standard"},
    "technician_name": {"technician", "technicians", "assigned"},
    "specialty": {"specialty", "specialties"},
    "priority": {"priority", "high", "medium", "low"},
    "scheduled_date": {"scheduled", "schedule", "before", "after"},
    "completed_date": {"completed", "completion", "date"},
    "sensor_type": {"sensor", "temperature", "voltage", "load", "power"},
    "reading_value": {"reading", "value", "average", "highest", "recorded"},
    "reading_time": {"latest", "reading", "time"},
    "alarm_flag": {"alarm", "alarmed"},
    "connection_type": {"connection", "feeder", "feeders", "tie", "control"},
    "switch_status": {"switch", "closed", "open"},
    "parts_cost": {"parts", "cost"},
    "action_type": {"action", "repair", "inspection", "calibration", "replacement"},
}


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z0-9_+-]+", text)}


def value_inventory(conn: sqlite3.Connection) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}
    for table, columns in TABLE_COLUMNS.items():
        for column in columns:
            if column.endswith("_id") or column in {"latitude", "longitude", "capacity_mw", "reading_value", "parts_cost"}:
                continue
            try:
                rows = conn.execute(f"SELECT DISTINCT {column} FROM {table} ORDER BY {column} LIMIT 40").fetchall()
            except sqlite3.Error:
                continue
            values = [str(row[0]) for row in rows if row[0] is not None]
            if values:
                inventory[f"{table}.{column}"] = values
    return inventory


def related_tables(seed_tables: set[str], max_tables: int = 4) -> set[str]:
    graph: dict[str, set[str]] = {table: set() for table in TABLE_COLUMNS}
    for left, _, right, _ in FOREIGN_KEYS:
        graph[left].add(right)
        graph[right].add(left)
    selected = set(seed_tables)
    queue = deque(seed_tables)
    while queue and len(selected) < max_tables:
        table = queue.popleft()
        for neighbor in sorted(graph[table]):
            if neighbor not in selected:
                selected.add(neighbor)
                queue.append(neighbor)
                if len(selected) >= max_tables:
                    break
    return selected


def select_context(conn: sqlite3.Connection, record: dict[str, Any]) -> dict[str, Any]:
    question = record["question"]
    tokens = tokenize(question)
    selected_tables: set[str] = set()
    for table, hints in TABLE_HINTS.items():
        if tokens & hints:
            selected_tables.add(table)
    inventory = value_inventory(conn)
    matched_values: dict[str, list[str]] = {}
    question_lower = question.lower()
    for key, values in inventory.items():
        matches = [value for value in values if value and value.lower() in question_lower]
        if matches:
            matched_values[key] = matches[:8]
            selected_tables.add(key.split(".", 1)[0])
    if not selected_tables:
        selected_tables.add("assets")
    selected_tables = related_tables(selected_tables)

    selected_columns: dict[str, list[str]] = {}
    for table in sorted(selected_tables):
        cols = {"*"}
        for column in TABLE_COLUMNS[table]:
            column_tokens = set(column.lower().split("_"))
            hints = COLUMN_HINTS.get(column, set())
            if tokens & column_tokens or tokens & hints:
                cols.add(column)
        for key in matched_values:
            value_table, value_col = key.split(".", 1)
            if value_table == table:
                cols.add(value_col)
        for left, left_col, right, right_col in FOREIGN_KEYS:
            if table == left and right in selected_tables:
                cols.add(left_col)
            if table == right and left in selected_tables:
                cols.add(right_col)
        selected_columns[table] = [col for col in TABLE_COLUMNS[table] if "*" in cols or col in cols]

    return {
        "question_id": record["question_id"],
        "selected_tables": sorted(selected_tables),
        "selected_columns": selected_columns,
        "matched_values": matched_values,
    }


def render_autocompact_context(context: dict[str, Any], include_shape: bool, record: dict[str, Any]) -> str:
    lines = ["SQLite compact context:"]
    lines.append("Tables and selected columns:")
    for table in context["selected_tables"]:
        columns = ", ".join(context["selected_columns"].get(table, TABLE_COLUMNS[table]))
        lines.append(f"- {table}({columns})")
    join_lines = []
    for left, left_col, right, right_col in FOREIGN_KEYS:
        if left in context["selected_tables"] and right in context["selected_tables"]:
            join_lines.append(f"- {left}.{left_col} = {right}.{right_col}")
    if join_lines:
        lines.append("Join paths:")
        lines.extend(join_lines)
    if context["matched_values"]:
        lines.append("Matched database values:")
        for key, values in sorted(context["matched_values"].items()):
            lines.append(f"- {key}: {', '.join(values)}")
    if include_shape:
        lines.append("Inferred answer hints from question text:")
        lines.append(f"- expected_shape_metadata_for_dev_pilot: {json.dumps(record['answer_shape'], sort_keys=True)}")
        lines.append(f"- order_sensitive_metadata_for_dev_pilot: {record['order_sensitive']}")
    return "\n".join(lines)


def autocompact_prompt(record: dict[str, Any], context_text: str) -> str:
    return f"""You are a Text-to-SQL system for a synthetic SQLite power-grid maintenance database.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Use only the compact context below. Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
"""


def validation_repair_prompt(record: dict[str, Any], context_text: str, sql: str, error_type: str, details: str) -> str:
    return f"""Repair the SQLite SELECT query for the question using only the compact context.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
Previous SQL: {sql}
Validation failure type: {error_type}
Validation details: {details}
"""


def run_single_sql_condition(
    *,
    client: Any,
    condition: str,
    record: dict[str, Any],
    context_text: str,
    trace_suffix: str,
) -> tuple[dict[str, Any], str]:
    prompt = autocompact_prompt(record, context_text)
    error = None
    raw = ""
    model = smoke.MODEL_NAME
    latency_ms = 0
    input_tokens = 0
    output_tokens = 0
    sql = "SELECT 1;"
    try:
        raw, model, latency_ms, input_tokens, output_tokens = smoke.call_model(client, prompt)
        sql = smoke.extract_sql(raw)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    trace_path = TRACE_DIR / f"{record['question_id']}_{trace_suffix}.json"
    trace_path.write_text(json.dumps({"prompt": prompt, "raw_response": raw}, indent=2) + "\n", encoding="utf-8")
    prediction = smoke.prediction_record(
        question_id=record["question_id"],
        condition=condition,
        model=model,
        prompt=prompt,
        schema_text=context_text,
        predicted_sql=sql,
        candidate_sql=[sql],
        selected_candidate_index=0,
        trace_path=str(trace_path.relative_to(WORKSPACE)),
        latency_ms=latency_ms,
        token_input=input_tokens,
        token_output=output_tokens,
        error=error,
    )
    return prediction, raw


def run_direct_condition(
    *,
    client: Any,
    condition: str,
    record: dict[str, Any],
    context_text: str,
    prompt_text: str,
    trace_suffix: str,
) -> dict[str, Any]:
    error = None
    raw = ""
    model = smoke.MODEL_NAME
    latency_ms = 0
    input_tokens = 0
    output_tokens = 0
    sql = "SELECT 1;"
    try:
        raw, model, latency_ms, input_tokens, output_tokens = smoke.call_model(client, prompt_text)
        sql = smoke.extract_sql(raw)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    trace_path = TRACE_DIR / f"{record['question_id']}_{trace_suffix}.json"
    trace_path.write_text(json.dumps({"prompt": prompt_text, "raw_response": raw}, indent=2) + "\n", encoding="utf-8")
    return smoke.prediction_record(
        question_id=record["question_id"],
        condition=condition,
        model=model,
        prompt=prompt_text,
        schema_text=context_text,
        predicted_sql=sql,
        candidate_sql=[sql],
        selected_candidate_index=0,
        trace_path=str(trace_path.relative_to(WORKSPACE)),
        latency_ms=latency_ms,
        token_input=input_tokens,
        token_output=output_tokens,
        error=error,
    )


def run_validated_condition(
    *,
    conn: sqlite3.Connection,
    client: Any,
    record: dict[str, Any],
    context_text: str,
) -> dict[str, Any]:
    prediction, raw = run_single_sql_condition(
        client=client,
        condition="C4_AutoCompactContext_Validated",
        record=record,
        context_text=context_text,
        trace_suffix="C4_AutoCompactContext_Validated",
    )
    if prediction["error"]:
        return prediction
    execution = smoke.execute_sql(conn, prediction["predicted_sql"])
    if execution.ok:
        return prediction
    repair_prompt = validation_repair_prompt(record, context_text, prediction["predicted_sql"], "execution_error", execution.error)
    repair_raw = ""
    try:
        repair_raw, model, repair_latency, repair_in, repair_out = smoke.call_model(client, repair_prompt)
        repaired_sql = smoke.extract_sql(repair_raw)
        prediction["candidate_sql"] = [prediction["predicted_sql"], repaired_sql]
        prediction["predicted_sql"] = repaired_sql
        prediction["selected_candidate_index"] = 1
        prediction["latency_ms"] += repair_latency
        prediction["token_input"] += repair_in
        prediction["token_output"] += repair_out
        prediction["retry_count"] = 1
        prediction["model"] = model
        prediction["prompt_hash"] = smoke.sha256_text(repair_prompt)
    except Exception as exc:
        prediction["error"] = f"repair {type(exc).__name__}: {exc}"
    trace_path = TRACE_DIR / f"{record['question_id']}_C4_AutoCompactContext_Validated.json"
    trace_path.write_text(
        json.dumps(
            {
                "initial_raw_response": raw,
                "initial_sql": prediction["candidate_sql"][0],
                "initial_score": {
                    "exec_ok": execution.ok,
                    "error_type": "execution_error",
                    "details": execution.error,
                },
                "repair_prompt": repair_prompt,
                "repair_raw_response": repair_raw,
                "final_sql": prediction["predicted_sql"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    prediction["intermediate_trace_path"] = str(trace_path.relative_to(WORKSPACE))
    return prediction


def score_predictions(conn: sqlite3.Connection, questions: list[dict[str, Any]], predictions: list[dict[str, Any]]) -> list[smoke.SmokeScore]:
    by_id = {record["question_id"]: record for record in questions}
    scores: list[smoke.SmokeScore] = []
    for prediction in predictions:
        question = by_id[prediction["question_id"]]
        contract_errors = smoke.validate_prediction_contract(prediction)
        score = smoke.score_prediction(conn, question, prediction["predicted_sql"])
        safe, _, _ = smoke.validate_read_only_select(prediction["predicted_sql"])
        scores.append(
            smoke.SmokeScore(
                question_id=prediction["question_id"],
                condition=prediction["condition"],
                predicted_sql=prediction["predicted_sql"],
                safe_sql=safe,
                evaluator_correct=score.correct,
                evaluator_error_type=score.error_type,
                evaluator_details=score.details,
                contract_errors=contract_errors,
            )
        )
    return scores


def recall(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0
    return numerator / denominator


def context_metrics(records: list[dict[str, Any]], contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {record["question_id"]: record for record in records}
    metrics = []
    for context in contexts:
        record = by_id[context["question_id"]]
        selected_tables = set(context["selected_tables"])
        gold_tables = set(record["tables"])
        selected_columns = {
            f"{table}.{column}"
            for table, cols in context["selected_columns"].items()
            for column in cols
        }
        gold_columns = set(record["columns"])
        selected_values = {
            value
            for values in context["matched_values"].values()
            for value in values
        }
        gold_values = {str(value) for value in record["required_value_literals"] if str(value)}
        metrics.append(
            {
                "question_id": record["question_id"],
                "table_recall": recall(len(gold_tables & selected_tables), len(gold_tables)),
                "column_recall": recall(len(gold_columns & selected_columns), len(gold_columns)),
                "value_recall": recall(len(gold_values & selected_values), len(gold_values)),
                "selected_table_count": len(selected_tables),
                "selected_column_count": len(selected_columns),
                "matched_value_count": len(selected_values),
            }
        )
    return metrics


def estimate_tokens(text: str) -> int:
    return max(1, len(re.findall(r"\S+", text)))


def write_report(
    predictions: list[dict[str, Any]],
    scores: list[smoke.SmokeScore],
    contexts: list[dict[str, Any]],
    context_metric_rows: list[dict[str, Any]],
) -> None:
    condition_counts = Counter(prediction["condition"] for prediction in predictions)
    correct_by_condition = {
        condition: sum(score.evaluator_correct for score in scores if score.condition == condition)
        for condition in sorted(condition_counts)
    }
    errors_by_condition = {
        condition: Counter(score.evaluator_error_type for score in scores if score.condition == condition and not score.evaluator_correct)
        for condition in sorted(condition_counts)
    }
    token_by_condition = {
        condition: [estimate_tokens(prediction["schema_context_hash"]) + int(prediction["token_input"] or 0) for prediction in predictions if prediction["condition"] == condition]
        for condition in sorted(condition_counts)
    }
    # Use prompt hashes in prediction records, but compute actual context tokens from traces for compact/full comparisons.
    context_token_rows = []
    for prediction in predictions:
        trace_path = WORKSPACE / prediction["intermediate_trace_path"]
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        prompt = trace.get("prompt") or trace.get("repair_prompt") or ""
        context_token_rows.append(
            {
                "question_id": prediction["question_id"],
                "condition": prediction["condition"],
                "prompt_tokens_est": estimate_tokens(prompt),
            }
        )
    prompt_tokens = {
        condition: [row["prompt_tokens_est"] for row in context_token_rows if row["condition"] == condition]
        for condition in sorted(condition_counts)
    }
    avg_table_recall = sum(row["table_recall"] for row in context_metric_rows) / len(context_metric_rows)
    avg_column_recall = sum(row["column_recall"] for row in context_metric_rows) / len(context_metric_rows)
    avg_value_recall = sum(row["value_recall"] for row in context_metric_rows) / len(context_metric_rows)
    rows_by_q: dict[str, dict[str, bool]] = {}
    for score in scores:
        rows_by_q.setdefault(score.question_id, {})[score.condition] = score.evaluator_correct
    c3_matches_c2 = sum(row.get("C3_AutoCompactContext") == row.get("C2_FullContext") for row in rows_by_q.values())
    c4_matches_c2 = sum(row.get("C4_AutoCompactContext_Validated") == row.get("C2_FullContext") for row in rows_by_q.values())

    lines = [
        "# Dev-Only AutoCompact Context Pilot",
        "",
        "## Scope",
        "",
        "- Purpose: test whether automatic compact context approaches full-context accuracy with materially smaller prompts.",
        "- This is not a formal experiment and must not be used for paper claims.",
        "- Split: dev only, Q001-Q020. The test split Q021-Q200 is untouched.",
        f"- Model/provider: `{smoke.MODEL_NAME}` via `{smoke.PROVIDER}` `{smoke.BASE_URL}` with `wire_api={smoke.WIRE_API}` and temperature `{smoke.TEMPERATURE}`.",
        "",
        "## Conditions",
        "",
        "- C1_SchemaOnly: full schema and question only.",
        "- C2_FullContext: full schema, compact value dictionary, answer-shape metadata, order sensitivity, and required literals.",
        "- C3_AutoCompactContext: deterministic question/schema/DB-value selector builds compact context, then one SQL generation call.",
        "- C4_AutoCompactContext_Validated: C3 plus one execution/shape repair attempt when validation fails.",
        "",
        "## Artifacts",
        "",
        f"- predictions: `{PREDICTIONS_PATH.relative_to(WORKSPACE)}`",
        f"- scores: `{SCORES_PATH.relative_to(WORKSPACE)}`",
        f"- contexts: `{CONTEXTS_PATH.relative_to(WORKSPACE)}`",
        f"- traces: `{TRACE_DIR.relative_to(WORKSPACE)}/`",
        "",
        "## Contract And Runtime Checks",
        "",
        f"- prediction records written: {len(predictions)}",
        "- expected records: 80",
        f"- records with contract errors: {sum(1 for score in scores if score.contract_errors)}",
        f"- records with unsafe SQL: {sum(1 for score in scores if not score.safe_sql)}",
        f"- records with model/extraction errors: {sum(1 for prediction in predictions if prediction.get('error'))}",
        "",
        "## Accuracy And Prompt Size",
        "",
        "| condition | records | correct | accuracy | avg prompt tokens est. | errors |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for condition in sorted(condition_counts):
        records = condition_counts[condition]
        correct = correct_by_condition[condition]
        avg_prompt = sum(prompt_tokens[condition]) / len(prompt_tokens[condition])
        errors = errors_by_condition[condition]
        lines.append(
            f"| {condition} | {records} | {correct} | {correct / records:.3f} | {avg_prompt:.1f} | "
            f"{dict(errors) if errors else 'none'} |"
        )
    full_avg = sum(prompt_tokens["C2_FullContext"]) / len(prompt_tokens["C2_FullContext"])
    c3_avg = sum(prompt_tokens["C3_AutoCompactContext"]) / len(prompt_tokens["C3_AutoCompactContext"])
    c4_avg = sum(prompt_tokens["C4_AutoCompactContext_Validated"]) / len(prompt_tokens["C4_AutoCompactContext_Validated"])
    lines.extend(
        [
            "",
            "## AutoCompact Context Selection Quality",
            "",
            f"- average table recall vs dev metadata: {avg_table_recall:.3f}",
            f"- average column recall vs dev metadata: {avg_column_recall:.3f}",
            f"- average value recall vs dev metadata: {avg_value_recall:.3f}",
            f"- C3 prompt token reduction vs C2: {(1 - c3_avg / full_avg) * 100:.1f}%",
            f"- C4 prompt token reduction vs C2: {(1 - c4_avg / full_avg) * 100:.1f}%",
            f"- C3 matches C2 correctness on {c3_matches_c2}/20 dev questions",
            f"- C4 matches C2 correctness on {c4_matches_c2}/20 dev questions",
            "",
            "| question_id | table_recall | column_recall | value_recall | selected_tables | selected_columns | matched_values |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in context_metric_rows:
        lines.append(
            f"| {row['question_id']} | {row['table_recall']:.3f} | {row['column_recall']:.3f} | {row['value_recall']:.3f} | "
            f"{row['selected_table_count']} | {row['selected_column_count']} | {row['matched_value_count']} |"
        )
    lines.extend(
        [
            "",
            "## Gold-Leakage Check",
            "",
            "- AutoCompact selection uses only question text, schema, foreign-key graph, and database values.",
            "- Dev metadata is used only after prediction generation to compute table/column/value recall in this report.",
            "- C2_FullContext includes metadata and is therefore an oracle-like full-context reference, not a deployable baseline.",
            "- C4 repair uses only SQL execution errors from the local database, not gold denotation feedback.",
            "- Gold SQL and gold result rows are used only by `evaluator.score_prediction` after prediction generation.",
            "",
            "## Decision",
            "",
        ]
    )
    c2_acc = correct_by_condition["C2_FullContext"] / condition_counts["C2_FullContext"]
    c3_acc = correct_by_condition["C3_AutoCompactContext"] / condition_counts["C3_AutoCompactContext"]
    c4_acc = correct_by_condition["C4_AutoCompactContext_Validated"] / condition_counts["C4_AutoCompactContext_Validated"]
    if c4_acc >= 0.9 * c2_acc and (1 - c4_avg / full_avg) >= 0.3:
        lines.append("AutoCompact+Validation reaches near-FullContext dev accuracy with materially smaller prompts.")
    elif c3_acc >= 0.9 * c2_acc and (1 - c3_avg / full_avg) >= 0.3:
        lines.append("AutoCompact reaches near-FullContext dev accuracy with materially smaller prompts.")
    else:
        lines.append("AutoCompact does not yet reach the near-FullContext accuracy plus prompt-reduction target.")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    questions = dev_pilot.load_dev_questions()
    client = smoke.llm_client()
    predictions: list[dict[str, Any]] = []
    contexts: list[dict[str, Any]] = []
    conn = sqlite3.connect(smoke.DB_PATH)
    try:
        schema_only_context = "\n".join(["SQLite schema:", smoke.SCHEMA_PATH.read_text(encoding="utf-8").strip()])
        full_context = smoke.schema_context(conn)
        for record in questions:
            predictions.append(
                run_direct_condition(
                    client=client,
                    condition="C1_SchemaOnly",
                    record=record,
                    context_text=schema_only_context,
                    prompt_text=f"""You are a Text-to-SQL system for a synthetic SQLite power-grid maintenance database.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Use only the schema below. Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.

{schema_only_context}

Question ID: {record['question_id']}
Question: {record['question']}
""",
                    trace_suffix="C1_SchemaOnly",
                )
            )
            predictions.append(
                run_direct_condition(
                    client=client,
                    condition="C2_FullContext",
                    record=record,
                    context_text=full_context,
                    prompt_text=smoke.strong_direct_prompt(record, full_context),
                    trace_suffix="C2_FullContext",
                )
            )

            context = select_context(conn, record)
            contexts.append(context)
            compact_text = render_autocompact_context(context, include_shape=False, record=record)
            c3_prediction, _ = run_single_sql_condition(
                client=client,
                condition="C3_AutoCompactContext",
                record=record,
                context_text=compact_text,
                trace_suffix="C3_AutoCompactContext",
            )
            predictions.append(c3_prediction)
            predictions.append(
                run_validated_condition(
                    conn=conn,
                    client=client,
                    record=record,
                    context_text=compact_text,
                )
            )
        with PREDICTIONS_PATH.open("w", encoding="utf-8") as f:
            for prediction in predictions:
                f.write(json.dumps(prediction, sort_keys=True) + "\n")
        with CONTEXTS_PATH.open("w", encoding="utf-8") as f:
            for context in contexts:
                f.write(json.dumps(context, sort_keys=True) + "\n")
        scores = score_predictions(conn, questions, predictions)
        metric_rows = context_metrics(questions, contexts)
    finally:
        conn.close()

    with SCORES_PATH.open("w", encoding="utf-8") as f:
        for score in scores:
            f.write(json.dumps(asdict(score), sort_keys=True) + "\n")

    write_report(predictions, scores, contexts, metric_rows)

    if len(predictions) != 80:
        print(f"FAIL: expected 80 prediction records, got {len(predictions)}")
        return 1
    if any(prediction.get("error") for prediction in predictions):
        print("FAIL: at least one prediction has a model/extraction error")
        return 1
    if any(score.contract_errors for score in scores):
        print("FAIL: at least one prediction has contract errors")
        return 1
    if any(not score.safe_sql for score in scores):
        print("FAIL: at least one prediction has unsafe SQL")
        return 1
    print(f"PASS: dev AutoCompact pilot completed; report={REPORT_PATH.relative_to(WORKSPACE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
