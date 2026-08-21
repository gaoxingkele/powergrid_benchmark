#!/usr/bin/env python3
"""Dev-only CHESS-style MA-SQLGrid feasibility pilot.

This is pre-three-pack evidence. It intentionally uses only the dev split
Q001-Q020 and must not be treated as a formal experiment.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import sys
import time
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
OUT_DIR = WORKSPACE / "smoke" / "dev_chess_style"
PREDICTIONS_PATH = OUT_DIR / "predictions.jsonl"
SCORES_PATH = OUT_DIR / "scores.jsonl"
CONTEXTS_PATH = OUT_DIR / "contexts.jsonl"
REPORT_PATH = OUT_DIR / "dev_chess_style_report.md"
TRACE_DIR = OUT_DIR / "traces"
DEFAULT_MAX_WORKERS = 4
MODEL_CALL_ATTEMPTS = 4

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

TABLE_DESCRIPTIONS = {
    "asset_types": "equipment type catalog such as Transformer, Breaker, Line, Relay, Substation, Capacitor",
    "locations": "grid yards, substations, regions, coordinates, and location criticality",
    "assets": "individual grid assets with names, type, location, install date, status, and MW capacity",
    "technicians": "maintenance technicians, specialties, home regions, and active flag",
    "work_orders": "maintenance work orders with priority, status, schedule, completion date, and fault code",
    "maintenance_logs": "maintenance actions, timestamps, notes, and parts cost",
    "sensor_readings": "time-series sensor readings for assets with sensor type, value, unit, and alarm flag",
    "grid_topology": "directed upstream/downstream asset connections and switch status",
}

GENERIC_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "by",
    "for",
    "from",
    "have",
    "how",
    "in",
    "is",
    "list",
    "many",
    "of",
    "on",
    "return",
    "show",
    "the",
    "their",
    "to",
    "what",
    "which",
    "with",
}

DOMAIN_SYNONYMS = [
    (re.compile(r"\bin[- ]?service\b|\bcurrently in service\b", re.I), "assets.status = 'in_service'", ["assets"], ["assets.status"], ["in_service"]),
    (re.compile(r"\btransformers?\b|\bxfmrs?\b", re.I), "asset_types.type_name = 'Transformer'", ["asset_types", "assets"], ["asset_types.type_name"], ["Transformer"]),
    (re.compile(r"\bhigh[- ]priority\b|\bpriority high\b", re.I), "work_orders.priority = 'high'", ["work_orders"], ["work_orders.priority"], ["high"]),
    (re.compile(r"\bopen\b", re.I), "work_orders.status = 'open'", ["work_orders"], ["work_orders.status"], ["open"]),
    (re.compile(r"\binactive technicians?\b|\binactive\b", re.I), "technicians.active = 0", ["technicians"], ["technicians.active"], ["0"]),
    (re.compile(r"\bcompleted in 2024\b", re.I), "work_orders.completed_date >= '2024-01-01' AND work_orders.completed_date < '2025-01-01'", ["work_orders"], ["work_orders.completed_date"], ["2024-01-01", "2025-01-01"]),
    (re.compile(r"\bcompleted\b", re.I), "work_orders.status = 'completed' OR work_orders.completed_date IS NOT NULL", ["work_orders"], ["work_orders.status", "work_orders.completed_date"], ["completed"]),
    (re.compile(r"\bactive technicians?\b|\bactive\b", re.I), "technicians.active = 1", ["technicians"], ["technicians.active"], ["1"]),
    (re.compile(r"\bcritical\b", re.I), "locations.criticality = 'critical'", ["locations"], ["locations.criticality"], ["critical"]),
    (re.compile(r"\btemperature\b", re.I), "sensor_readings.sensor_type = 'temperature'", ["sensor_readings"], ["sensor_readings.sensor_type"], ["temperature"]),
    (re.compile(r"\bload readings?\b|\bload sensors?\b", re.I), "sensor_readings.sensor_type = 'load'", ["sensor_readings"], ["sensor_readings.sensor_type"], ["load"]),
    (re.compile(r"\bvoltage\b(?!\s+class(?:es)?\b)", re.I), "sensor_readings.sensor_type = 'voltage'", ["sensor_readings"], ["sensor_readings.sensor_type"], ["voltage"]),
    (re.compile(r"\balarmed?\b|\balarm\b", re.I), "sensor_readings.alarm_flag = 1", ["sensor_readings"], ["sensor_readings.alarm_flag"], ["1"]),
    (re.compile(r"\bclosed feeders?\b", re.I), "grid_topology.connection_type = 'feeder' AND grid_topology.switch_status = 'closed'", ["grid_topology"], ["grid_topology.connection_type", "grid_topology.switch_status"], ["feeder", "closed"]),
    (re.compile(r"\bopen controls?\b", re.I), "grid_topology.connection_type = 'control' AND grid_topology.switch_status = 'open'", ["grid_topology"], ["grid_topology.connection_type", "grid_topology.switch_status"], ["control", "open"]),
    (re.compile(r"\bno completed date\b|\bwithout completed date\b", re.I), "work_orders.completed_date IS NULL", ["work_orders"], ["work_orders.completed_date"], []),
    (re.compile(r"\binstalled before 2018\b|\bbefore 2018\b", re.I), "assets.install_date < '2018-01-01'", ["assets"], ["assets.install_date"], ["2018-01-01"]),
    (re.compile(r"\bhyphens? removed\b|\bremove hyphens?\b", re.I), "use REPLACE(asset_name, '-', '') for normalized asset names", ["assets"], ["assets.asset_name"], ["-", ""]),
]

COLUMN_PHRASES = [
    (re.compile(r"\btype,\s*location,\s+and\s+status\b|\btype,?\s+location,?\s+and\s+status\b", re.I), ["asset_types.type_name", "locations.location_name", "assets.status"]),
    (re.compile(r"\basset names? and statuses\b", re.I), ["assets.asset_name", "assets.status"]),
    (re.compile(r"\bassets?\s+(?:with|and)\s+their\s+status\b|\ball\s+\w+\s+assets?\s+with\s+their\s+status\b", re.I), ["assets.asset_name", "assets.status"]),
    (re.compile(r"\bassets?\s+(?:with|and)\s+their\s+locations?\b|\ball\s+\w+\s+assets?\s+with\s+their\s+locations?\b", re.I), ["assets.asset_name", "locations.location_name"]),
    (re.compile(r"\bassets?\s+(?:with|and)\s+their\s+type\s+names?\b|\btype\s+names?\b", re.I), ["assets.asset_name", "asset_types.type_name"]),
    (re.compile(r"\bassets?\s+in\s+critical\s+locations?\s+with\s+their\s+region\b", re.I), ["assets.asset_name", "locations.region"]),
    (re.compile(r"\basset names?\b|\bwhich assets?\b", re.I), ["assets.asset_name"]),
    (re.compile(r"\bmanufacturers?\b", re.I), ["asset_types.manufacturer"]),
    (re.compile(r"\bvoltage class(?:es)?\b", re.I), ["asset_types.voltage_class"]),
    (re.compile(r"\bexpected lifetimes?\b", re.I), ["asset_types.type_name", "asset_types.expected_lifetime_years"]),
    (re.compile(r"\bcapacity\b", re.I), ["assets.asset_name", "assets.capacity_mw"]),
    (re.compile(r"\bregions?\b", re.I), ["locations.region"]),
    (re.compile(r"\blocations?\b", re.I), ["locations.location_name"]),
    (re.compile(r"\btechnicians?\b", re.I), ["technicians.technician_name"]),
    (re.compile(r"\bwork orders?\b", re.I), ["work_orders.work_order_id", "work_orders.priority", "work_orders.status"]),
    (re.compile(r"\bfault code\b", re.I), ["work_orders.work_order_id", "work_orders.asset_id", "work_orders.status", "work_orders.priority", "work_orders.fault_code"]),
    (re.compile(r"\bscheduled(?:_|\s+)date\b|\bscheduled before\b|\bscheduled after\b|\bscheduled in\b", re.I), ["work_orders.scheduled_date"]),
    (re.compile(r"\bfirst scheduled work order\b", re.I), ["work_orders.work_order_id", "work_orders.scheduled_date"]),
    (re.compile(r"\bcompletion dates?\b|\bcompleted dates?\b", re.I), ["work_orders.completed_date"]),
    (re.compile(r"\bstatuses?\b", re.I), ["assets.status", "work_orders.status"]),
    (re.compile(r"\bspecialt(?:y|ies)\b", re.I), ["technicians.specialty"]),
    (re.compile(r"\bhome region\b", re.I), ["technicians.home_region"]),
    (re.compile(r"\baction type\b", re.I), ["maintenance_logs.action_type"]),
    (re.compile(r"\bparts cost\b", re.I), ["maintenance_logs.parts_cost"]),
    (re.compile(r"\bmaintenance logs?\b|\blogs?\s+mention\b", re.I), ["maintenance_logs.log_id", "maintenance_logs.work_order_id", "maintenance_logs.notes"]),
    (re.compile(r"\balarmed readings?.*asset names?\b", re.I), ["assets.asset_name", "sensor_readings.reading_time", "sensor_readings.reading_value", "sensor_readings.alarm_flag"]),
    (re.compile(r"\bmost alarmed sensor readings?\b", re.I), ["asset_types.type_name", "sensor_readings.alarm_flag"]),
    (re.compile(r"\breading\b", re.I), ["sensor_readings.reading_time", "sensor_readings.sensor_type", "sensor_readings.reading_value", "sensor_readings.unit"]),
    (re.compile(r"\bsensor readings?\b|\breadings?\s+by\s+unit\b", re.I), ["sensor_readings.reading_id", "sensor_readings.sensor_type", "sensor_readings.unit"]),
    (re.compile(r"\bupstream\b|\btopology edges?\b|\btopology connections?\b", re.I), ["grid_topology.edge_id", "grid_topology.upstream_asset_id", "grid_topology.downstream_asset_id", "grid_topology.connection_type", "grid_topology.switch_status"]),
    (re.compile(r"\btopology edges? that originate from upstream asset\b", re.I), ["grid_topology.edge_id", "grid_topology.downstream_asset_id", "grid_topology.connection_type", "grid_topology.switch_status"]),
    (re.compile(r"\bdownstream assets?\b", re.I), ["grid_topology.downstream_asset_id", "assets.asset_name"]),
]

MONTH_STARTS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z0-9_+-]+", text) if token.lower() not in GENERIC_STOPWORDS}


def estimate_tokens(text: str) -> int:
    return max(1, len(re.findall(r"\S+", text)))


def value_inventory(conn: sqlite3.Connection, *, include_numeric_flags: bool) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}
    for table, columns in TABLE_COLUMNS.items():
        for column in columns:
            if column.endswith("_id") or column in {"latitude", "longitude", "capacity_mw", "reading_value", "parts_cost"}:
                continue
            if not include_numeric_flags and column in {"active", "alarm_flag"}:
                continue
            rows = conn.execute(f"SELECT DISTINCT {column} FROM {table} ORDER BY {column} LIMIT 80").fetchall()
            values = [str(row[0]) for row in rows if row[0] is not None]
            if values:
                inventory[f"{table}.{column}"] = values
    return inventory


def related_tables(seed_tables: set[str], *, max_tables: int = 6) -> set[str]:
    graph: dict[str, set[str]] = {table: set() for table in TABLE_COLUMNS}
    for left, _, right, _ in FOREIGN_KEYS:
        graph[left].add(right)
        graph[right].add(left)
    selected = set(seed_tables)
    queue = deque(sorted(seed_tables))
    while queue and len(selected) < max_tables:
        table = queue.popleft()
        for neighbor in sorted(graph[table]):
            if neighbor not in selected:
                selected.add(neighbor)
                queue.append(neighbor)
                if len(selected) >= max_tables:
                    break
    return selected


def split_column_ref(ref: str) -> tuple[str, str]:
    table, column = ref.split(".", 1)
    return table, column


def add_column(selected: dict[str, set[str]], ref: str) -> None:
    table, column = split_column_ref(ref)
    selected.setdefault(table, set()).add(column)


def exact_value_matches(question: str, inventory: dict[str, list[str]]) -> dict[str, list[str]]:
    q = question.lower()
    matches: dict[str, list[str]] = {}
    for key, values in inventory.items():
        found = []
        for value in values:
            value_lower = value.lower()
            if not value_lower:
                continue
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(value_lower)}(?![A-Za-z0-9_])", q):
                found.append(value)
        if found:
            matches[key] = found[:10]
    return matches


def prune_ambiguous_value_matches(question: str, matches: dict[str, list[str]]) -> dict[str, list[str]]:
    q = question.lower()
    pruned = {key: list(values) for key, values in matches.items()}
    if re.search(r"\bsensor readings?\b|\breadings?\s+by\s+unit\b", q):
        pruned.pop("technicians.specialty", None)
    if re.search(r"\bvoltage class(?:es)?\b", q):
        values = [value for value in pruned.get("sensor_readings.sensor_type", []) if value.lower() != "voltage"]
        if values:
            pruned["sensor_readings.sensor_type"] = values
        else:
            pruned.pop("sensor_readings.sensor_type", None)
    if re.search(r"\bopen\s+work\s+orders?\b|\bwork\s+order\s+count\b", q):
        values = [value for value in pruned.get("grid_topology.switch_status", []) if value.lower() != "open"]
        if values:
            pruned["grid_topology.switch_status"] = values
        else:
            pruned.pop("grid_topology.switch_status", None)
    if re.search(r"\brelay assets?\b", q):
        pruned.pop("technicians.specialty", None)
        pruned.pop("work_orders.fault_code", None)
    if re.search(r"\b(transformer|breaker|line|relay|substation|capacitor)s?\s+assets?\b", q):
        pruned.pop("technicians.specialty", None)
    return {key: values for key, values in pruned.items() if values}


def next_month(year: int, month: int) -> tuple[int, int]:
    if month == 12:
        return year + 1, 1
    return year, month + 1


def infer_question_literal_hints(question: str) -> list[tuple[str, list[str], list[str], list[str]]]:
    q = question.lower()
    hints: list[tuple[str, list[str], list[str], list[str]]] = []

    before_match = re.search(r"\bscheduled before ([a-z]+) (\d{4})\b", q)
    if before_match and before_match.group(1) in MONTH_STARTS:
        month = MONTH_STARTS[before_match.group(1)]
        year = before_match.group(2)
        hints.append((f"work_orders.scheduled_date < '{year}-{month}-01'", ["work_orders"], ["work_orders.scheduled_date"], [f"{year}-{month}-01"]))

    after_match = re.search(r"\b(?:scheduled work order )?after ([a-z]+) (\d{4})\b", q)
    if after_match and after_match.group(1) in MONTH_STARTS:
        month_i = int(MONTH_STARTS[after_match.group(1)])
        year_i = int(after_match.group(2))
        next_year, next_month_i = next_month(year_i, month_i)
        boundary = f"{next_year}-{next_month_i:02d}-01"
        hints.append((f"work_orders.scheduled_date >= '{boundary}'", ["work_orders"], ["work_orders.scheduled_date"], [boundary]))

    in_month_match = re.search(r"\bscheduled in ([a-z]+) (\d{4})\b", q)
    if in_month_match and in_month_match.group(1) in MONTH_STARTS:
        month_i = int(MONTH_STARTS[in_month_match.group(1)])
        year_i = int(in_month_match.group(2))
        next_year, next_month_i = next_month(year_i, month_i)
        start = f"{year_i}-{month_i:02d}-01"
        end = f"{next_year}-{next_month_i:02d}-01"
        hints.append((f"work_orders.scheduled_date >= '{start}' AND work_orders.scheduled_date < '{end}'", ["work_orders"], ["work_orders.scheduled_date"], [start, end]))

    installed_later = re.search(r"\binstalled in (\d{4}) or later\b", q)
    if installed_later:
        boundary = f"{installed_later.group(1)}-01-01"
        hints.append((f"assets.install_date >= '{boundary}'", ["assets"], ["assets.install_date"], [boundary]))

    lifetime_match = re.search(r"\bexpected lifetimes? greater than (\d+) years?\b", q)
    if lifetime_match:
        value = lifetime_match.group(1)
        hints.append((f"asset_types.expected_lifetime_years > {value}", ["asset_types"], ["asset_types.expected_lifetime_years"], [value]))

    capacity_match = re.search(r"\bcapacity above (\d+)\s*mw\b", q)
    if capacity_match:
        value = capacity_match.group(1)
        hints.append((f"assets.capacity_mw > {value}", ["assets"], ["assets.capacity_mw"], [value]))

    reading_match = re.search(r"\breadings? above (\d+)\s*mw\b", q)
    if reading_match:
        value = reading_match.group(1)
        hints.append((f"sensor_readings.reading_value > {value}", ["sensor_readings"], ["sensor_readings.reading_value"], [value]))

    if re.search(r"\bmore than one asset\b", q):
        hints.append(("GROUP BY the requested entity and use HAVING COUNT(*) > 1", ["assets"], ["assets.asset_id"], ["1"]))
    if re.search(r"\bmore than one topology edge\b", q):
        hints.append(("GROUP BY the upstream asset and use HAVING COUNT(*) > 1", ["grid_topology"], ["grid_topology.edge_id"], ["1"]))

    return hints


def generic_context(conn: sqlite3.Connection, record: dict[str, Any]) -> dict[str, Any]:
    tokens = tokenize(record["question"])
    inventory = value_inventory(conn, include_numeric_flags=False)
    matched_values = prune_ambiguous_value_matches(record["question"], exact_value_matches(record["question"], inventory))
    selected_tables: set[str] = set()
    selected_columns: dict[str, set[str]] = {}

    for table, columns in TABLE_COLUMNS.items():
        table_tokens = set(table.lower().split("_")) | {table.lower(), table.lower().rstrip("s")}
        if tokens & table_tokens:
            selected_tables.add(table)
        for column in columns:
            column_tokens = set(column.lower().split("_")) | {column.lower(), column.lower().rstrip("s")}
            if tokens & column_tokens:
                selected_tables.add(table)
                selected_columns.setdefault(table, set()).add(column)

    for key, values in matched_values.items():
        table, column = split_column_ref(key)
        if values:
            selected_tables.add(table)
            selected_columns.setdefault(table, set()).add(column)

    if not selected_tables:
        selected_tables.add("assets")
    selected_tables = related_tables(selected_tables, max_tables=5)
    for table in selected_tables:
        selected_columns.setdefault(table, set()).update({col for col in TABLE_COLUMNS[table] if col.endswith("_id")})
    for left, left_col, right, right_col in FOREIGN_KEYS:
        if left in selected_tables and right in selected_tables:
            selected_columns.setdefault(left, set()).add(left_col)
            selected_columns.setdefault(right, set()).add(right_col)

    return finalize_context(
        record=record,
        mode="generic",
        selected_tables=selected_tables,
        selected_columns=selected_columns,
        matched_values=matched_values,
        normalized_values=[],
        inferred_shape={},
    )


def infer_domain_context(conn: sqlite3.Connection, record: dict[str, Any]) -> dict[str, Any]:
    question = record["question"]
    tokens = tokenize(question)
    inventory = value_inventory(conn, include_numeric_flags=True)
    matched_values = prune_ambiguous_value_matches(question, exact_value_matches(question, inventory))
    selected_tables: set[str] = set()
    selected_columns: dict[str, set[str]] = {}
    normalized_values: list[str] = []

    for key, values in matched_values.items():
        table, column = split_column_ref(key)
        selected_tables.add(table)
        selected_columns.setdefault(table, set()).add(column)
        normalized_values.extend(f"{key} = {json.dumps(value)}" for value in values)

    for pattern, hint, tables, columns, values in DOMAIN_SYNONYMS:
        if pattern.search(question):
            selected_tables.update(tables)
            for ref in columns:
                add_column(selected_columns, ref)
            normalized_values.append(hint)
            for key, inv_values in inventory.items():
                for value in values:
                    if value in inv_values:
                        table, column = split_column_ref(key)
                        selected_tables.add(table)
                        selected_columns.setdefault(table, set()).add(column)

    for pattern, refs in COLUMN_PHRASES:
        if pattern.search(question):
            for ref in refs:
                add_column(selected_columns, ref)
                selected_tables.add(ref.split(".", 1)[0])

    for hint, tables, columns, values in infer_question_literal_hints(question):
        normalized_values.append(hint)
        selected_tables.update(tables)
        for ref in columns:
            add_column(selected_columns, ref)
        for key, inv_values in inventory.items():
            for value in values:
                if value in inv_values:
                    table, column = split_column_ref(key)
                    selected_tables.add(table)
                    selected_columns.setdefault(table, set()).add(column)

    if {"average", "avg"} & tokens:
        selected_columns.setdefault("assets", set()).add("capacity_mw")
        selected_columns.setdefault("sensor_readings", set()).add("reading_value")
    if "manufacturer" in tokens or "manufacturers" in tokens:
        selected_tables.add("asset_types")
        selected_columns.setdefault("asset_types", set()).add("manufacturer")
    if "voltage" in tokens and ("class" in tokens or "classes" in tokens):
        selected_tables.update({"asset_types", "assets"})
        selected_columns.setdefault("asset_types", set()).update({"voltage_class", "asset_type_id"})
        selected_columns.setdefault("assets", set()).add("asset_type_id")
    if "unit" in tokens and ("reading" in tokens or "readings" in tokens):
        selected_tables.add("sensor_readings")
        selected_columns.setdefault("sensor_readings", set()).update({"unit", "reading_id"})
    if {"count", "many"} & tokens:
        for table in ["assets", "work_orders", "technicians"]:
            if table in selected_tables:
                selected_columns.setdefault(table, set()).add(TABLE_COLUMNS[table][0])
    if {"latest", "highest", "lowest"} & tokens:
        selected_tables.add("sensor_readings")
        selected_columns.setdefault("sensor_readings", set()).update({"reading_time", "reading_value"})
    if "downstream" in tokens or "upstream" in tokens or "connected" in tokens:
        selected_tables.update({"grid_topology", "assets"})
        selected_columns.setdefault("grid_topology", set()).update({"upstream_asset_id", "downstream_asset_id", "connection_type", "switch_status"})
        selected_columns.setdefault("assets", set()).update({"asset_id", "asset_name"})

    if not selected_tables:
        selected_tables.add("assets")
    selected_tables = related_tables(selected_tables, max_tables=6)
    for table in selected_tables:
        selected_columns.setdefault(table, set()).update({col for col in TABLE_COLUMNS[table] if col.endswith("_id")})
    for left, left_col, right, right_col in FOREIGN_KEYS:
        if left in selected_tables and right in selected_tables:
            selected_columns.setdefault(left, set()).add(left_col)
            selected_columns.setdefault(right, set()).add(right_col)

    inferred_shape = infer_answer_shape(question)
    return finalize_context(
        record=record,
        mode="domain",
        selected_tables=selected_tables,
        selected_columns=selected_columns,
        matched_values=matched_values,
        normalized_values=dedupe(normalized_values),
        inferred_shape=inferred_shape,
    )


def infer_answer_shape(question: str) -> dict[str, Any]:
    q = question.lower()
    hints: list[str] = []
    column_count: int | None = None
    row_granularity = "multi-row"
    order_required = bool(re.search(r"\b(list|which|show|return|latest|highest|lowest|by|each)\b", q))

    if re.search(r"\bhow many\b|\bcount\b|\bnumber of\b", q):
        grouped = bool(re.search(r"\bby\b|\beach\b|\bper\b|\bin each\b", q))
        column_count = 2 if grouped else 1
        row_granularity = "multi-row" if grouped else "scalar"
        hints.append("Use COUNT(*) for count questions.")
    if re.search(r"\bmore than one asset\b|\bmore than one topology edge\b", q):
        column_count = 2
        row_granularity = "multi-row"
        order_required = True
        hints.append("Use GROUP BY with HAVING COUNT(*) > 1.")
    if re.search(r"\bminimum capacity by asset type\b", q):
        column_count = 2
        hints.append("Project type_name and MIN(capacity_mw).")
    if "average" in q or "avg" in q:
        column_count = 1 if "each" not in q and " by " not in q else 2
        hints.append("Use AVG(...) for average questions.")
    if re.search(r"\blargest average capacity\b", q):
        column_count = 2
        row_granularity = "one-row"
        order_required = True
        hints.append("Project type_name and AVG(capacity_mw), ordered descending with LIMIT 1.")
    if "total" in q:
        column_count = 2 if " by " in q else 1
        hints.append("Use SUM(...) for total questions.")
    if re.search(r"\btype,?\s+location,?\s+and\s+status\b", q):
        column_count = 3
        row_granularity = "one-row"
        hints.append("Project type_name, location_name, and status.")
    if "asset names and statuses" in q or re.search(r"\bassets?\s+(?:with|and)\s+their\s+status\b", q):
        column_count = 2
        hints.append("Project asset_name and status.")
    if re.search(r"\bassets?\s+in\s+critical\s+locations?\s+with\s+their\s+region\b", q):
        column_count = 2
        hints.append("Project asset_name and region.")
    if re.search(r"\bassets?\s+(?:with|and)\s+their\s+locations?\b", q):
        column_count = 2
        hints.append("Project asset_name and location_name.")
    if re.search(r"\bassets?\s+(?:with|and)\s+their\s+type\s+names?\b|\bassets? whose type manufacturer\b|\bat .+ with their type names?\b", q):
        column_count = 2
        hints.append("Project asset_name and type_name.")
    if re.search(r"\bassets? installed before\b|\bassets? installed in \d{4} or later\b", q):
        column_count = 2
        hints.append("Project asset_name and install_date.")
    if re.search(r"\bassets? (?:have )?capacity above\b", q):
        column_count = 2
        hints.append("Project asset_name and capacity_mw.")
    elif re.search(r"\basset names?\b|\bwhich assets?\b", q):
        column_count = column_count or 1
        hints.append("Project asset_name for asset listing questions.")
    technician_listing = bool(re.search(r"\bwhich technicians\b|\bactive technicians\b", q))
    if re.search(r"\bwhich technicians are inactive\b", q):
        column_count = 2
        hints.append("Project technician_name and specialty.")
    elif technician_listing:
        column_count = 1
        hints.append("Project technician_name for technician listing questions.")
    if re.search(r"\basset types? have expected lifetimes\b", q):
        column_count = 2
        hints.append("Project type_name and expected_lifetime_years.")
    if "work orders" in q and ("asset names" in q or "their asset names" in q):
        column_count = 4
        hints.append("Project work_order_id, asset_name, priority, and status.")
    elif "work order" in q and re.search(r"\bcompletion dates?\b|\bscheduled before\b|\bscheduled after\b|\bscheduled in\b|\bfirst scheduled\b", q):
        column_count = 2
        order_required = order_required or "first scheduled" in q
        hints.append("Project work_order_id with the relevant scheduled/completed date.")
    elif "work orders" in q and re.search(r"\bare assigned to technician\b|\bassigned to technician [a-z]", q):
        column_count = 3
        hints.append("Project work_order_id, status, and scheduled_date for technician assignments.")
    elif "work orders" in q and re.search(r"\bassigned to [a-z]", q):
        column_count = 2
        hints.append("Project work_order_id and status for named assignee questions.")
    elif "work orders" in q and re.search(r"\bassigned to technicians\b", q):
        column_count = 2
        hints.append("Project work_order_id with status or technician_name as requested.")
    elif "work orders" in q and re.search(r"\bcapacitor assets\b|\btechnician specialties\b", q):
        column_count = 2
        hints.append("Project work_order_id with the requested asset or technician field.")
    elif "work orders" in q and re.search(r"\bwhich work orders have fault code\b", q):
        column_count = 3
        hints.append("Project work_order_id, asset_id, and status.")
    elif "work orders" in q and re.search(r"\bfault code\b", q):
        column_count = 4
        hints.append("Project work_order_id, asset_id, status, and priority.")
    elif "work orders" in q and column_count is None:
        column_count = 3
        hints.append("Project work_order_id, status, and scheduled_date unless question asks for aggregation.")
    if technician_listing and "work orders" in q:
        column_count = 1
        hints.append("Technician listing questions should project technician_name, not work_order columns.")
    if re.search(r"\bmost expensive maintenance log\b", q):
        column_count = 2
        row_granularity = "one-row"
        order_required = True
        hints.append("Project work_order_id and parts_cost ordered by parts_cost DESC LIMIT 1.")
    if re.search(r"\bmaintenance logs? mention\b", q):
        column_count = 2
        hints.append("Project log_id and work_order_id.")
    if "latest" in q:
        row_granularity = "multi-row" if re.search(r"\bevery asset\b", q) else "one-row"
        order_required = True
        if re.search(r"\blatest sensor reading recorded for asset\b", q):
            column_count = 4
            hints.append("Project reading_time, sensor_type, reading_value, and unit.")
        elif re.search(r"\blatest reading for every asset\b", q):
            column_count = 4
            hints.append("Project asset_name, reading_time, sensor_type, and reading_value.")
        elif re.search(r"\blatest .*reading\b", q):
            column_count = 3
            hints.append("Project reading_time, reading_value, and unit.")
        hints.append("Use ORDER BY reading_time DESC for latest readings.")
    if "highest" in q:
        row_granularity = "one-row"
        order_required = True
        if re.search(r"\bhighest recorded temperature alarm\b", q):
            column_count = 2
            hints.append("Project asset_name and reading_value.")
        hints.append("Use ORDER BY reading_value DESC LIMIT 1 for highest readings.")
    if "manufacturers" in q:
        column_count = column_count or 1
        hints.append("Project manufacturer for manufacturer questions.")
    if "regions" in q:
        column_count = column_count or 1
        hints.append("Use DISTINCT region when asking which regions.")
    if (
        "by specialty" in q
        or "by status" in q
        or "by action type" in q
        or "by unit" in q
        or "each asset type" in q
        or "each voltage class" in q
        or "in each voltage class" in q
    ):
        column_count = 2
        row_granularity = "multi-row"
        order_required = True
        hints.append("Use GROUP BY and deterministic ORDER BY for grouped results.")
    if re.search(r"\bclosed topology connections? with upstream and downstream asset names\b", q):
        column_count = 3
        hints.append("Project upstream asset, downstream asset, and connection_type.")
    if re.search(r"\btopology edges? are open controls\b", q):
        column_count = 3
        hints.append("Project edge_id, upstream_asset_id, and downstream_asset_id.")
    if re.search(r"\balarmed readings?.*with asset names\b", q):
        column_count = 3
        hints.append("Project asset_name, reading_time, and reading_value.")
    if re.search(r"\breadings? with alarm flag set\b|\bload readings? above\b", q):
        column_count = 3
        hints.append("Project the relevant reading identifier/asset, reading_time or asset_id, and reading_value.")
    if re.search(r"\btopology edges? that originate from upstream asset\b", q):
        column_count = 4
        hints.append("Project edge_id, downstream asset, connection_type, and switch_status.")
    if re.search(r"\basset type has the most alarmed sensor readings\b", q):
        column_count = 2
        row_granularity = "one-row"
        order_required = True
        hints.append("Project type_name and alarm_count ordered descending with LIMIT 1.")
    if "hyphens removed" in q:
        column_count = 1
        hints.append("Use REPLACE(asset_name, '-', '').")
    if column_count is None:
        column_count = 1

    return {
        "column_count": column_count,
        "row_granularity": row_granularity,
        "order_required": order_required,
        "hints": dedupe(hints),
    }


def dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def finalize_context(
    *,
    record: dict[str, Any],
    mode: str,
    selected_tables: set[str],
    selected_columns: dict[str, set[str]],
    matched_values: dict[str, list[str]],
    normalized_values: list[str],
    inferred_shape: dict[str, Any],
) -> dict[str, Any]:
    selected_columns_list = {
        table: [column for column in TABLE_COLUMNS[table] if column in selected_columns.get(table, set())]
        for table in sorted(selected_tables)
    }
    for table in sorted(selected_tables):
        if not selected_columns_list[table]:
            selected_columns_list[table] = list(TABLE_COLUMNS[table])
    return {
        "question_id": record["question_id"],
        "mode": mode,
        "selected_tables": sorted(selected_tables),
        "selected_columns": selected_columns_list,
        "matched_values": matched_values,
        "normalized_value_hints": normalized_values,
        "inferred_shape": inferred_shape,
    }


def render_full_schema_values(conn: sqlite3.Connection) -> str:
    lines = ["SQLite schema:", smoke.SCHEMA_PATH.read_text(encoding="utf-8").strip(), "", "Database value dictionary:"]
    inventory = value_inventory(conn, include_numeric_flags=True)
    for key, values in sorted(inventory.items()):
        lines.append(f"- {key}: {', '.join(values)}")
    return "\n".join(lines)


def render_selected_context(context: dict[str, Any], *, domain: bool) -> str:
    lines = ["SQLite selected context:"]
    lines.append("Tables and selected columns:")
    for table in context["selected_tables"]:
        description = TABLE_DESCRIPTIONS.get(table, "")
        columns = ", ".join(context["selected_columns"].get(table, TABLE_COLUMNS[table]))
        lines.append(f"- {table}({columns}) -- {description}")
    join_lines = []
    for left, left_col, right, right_col in FOREIGN_KEYS:
        if left in context["selected_tables"] and right in context["selected_tables"]:
            join_lines.append(f"- {left}.{left_col} = {right}.{right_col}")
    if join_lines:
        lines.append("Join paths:")
        lines.extend(join_lines)
    if context["matched_values"]:
        lines.append("Exact database values matched from the question:")
        for key, values in sorted(context["matched_values"].items()):
            lines.append(f"- {key}: {', '.join(values)}")
    if domain and context["normalized_value_hints"]:
        lines.append("Power-grid domain normalization hints inferred from the question:")
        lines.extend(f"- {hint}" for hint in context["normalized_value_hints"])
    if domain and context["inferred_shape"]:
        shape = context["inferred_shape"]
        lines.append("Answer-shape hints inferred from the question text:")
        lines.append(f"- expected column count: {shape['column_count']}")
        lines.append(f"- row granularity: {shape['row_granularity']}")
        lines.append(f"- deterministic ordering needed: {shape['order_required']}")
        for hint in shape["hints"]:
            lines.append(f"- {hint}")
    return "\n".join(lines)


def direct_prompt(record: dict[str, Any], context_text: str, condition: str) -> str:
    return f"""You are a Text-to-SQL system for a synthetic SQLite power-grid maintenance database.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.
Use only the provided database context. When normalization hints or answer-shape hints are present, treat them as question-derived constraints. Match the requested projection count and include relevant literal predicates.

Condition: {condition}

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
"""


def literal_groups_from_hints(hints: list[str]) -> list[tuple[str, list[str]]]:
    groups = []
    for hint in hints:
        literals = re.findall(r"'([^']*)'|\"([^\"]*)\"|=\s*([0-9]+)\b|<\s*([0-9]+)\b|>\s*([0-9]+)\b|<\s*'([^']*)'|>\s*'([^']*)'", hint)
        flat = [piece for match in literals for piece in match if piece]
        if flat:
            groups.append((hint, flat))
    return groups


def call_model_with_retries(client: Any, prompt: str) -> tuple[str, str, int, int, int, int]:
    last_exc: Exception | None = None
    total_latency = 0
    for attempt in range(MODEL_CALL_ATTEMPTS):
        try:
            raw, model, latency_ms, input_tokens, output_tokens = smoke.call_model(client, prompt)
            return raw, model, total_latency + latency_ms, input_tokens, output_tokens, attempt
        except Exception as exc:
            last_exc = exc
            total_latency += 0
            time.sleep(min(8, 2 * (attempt + 1)))
    assert last_exc is not None
    raise last_exc


def candidate_prompt(record: dict[str, Any], context_text: str, condition: str) -> str:
    return f"""You are generating candidate SQLite SQL for a CHESS-style Text-to-SQL pilot.

Return 3 distinct read-only SQLite SELECT queries as a numbered list. Do not include explanation.
Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.
Use only the selected context, normalization hints, and inferred answer-shape hints below.

Condition: {condition}

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
"""


def repair_prompt(record: dict[str, Any], context_text: str, sql: str, validation: dict[str, Any]) -> str:
    return f"""Repair this SQLite SELECT query using only the selected context and inferred hints.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.

{context_text}

Question ID: {record['question_id']}
Question: {record['question']}
Previous SQL: {sql}
Reference-free validation result: {json.dumps(validation, sort_keys=True)}
"""


def run_direct_condition(
    *,
    client: Any,
    record: dict[str, Any],
    condition: str,
    context_text: str,
) -> dict[str, Any]:
    prompt = direct_prompt(record, context_text, condition)
    error = None
    raw = ""
    model = smoke.MODEL_NAME
    latency_ms = 0
    input_tokens = 0
    output_tokens = 0
    retry_count = 0
    sql = "SELECT 1;"
    try:
        raw, model, latency_ms, input_tokens, output_tokens, retry_count = call_model_with_retries(client, prompt)
        sql = smoke.extract_sql(raw)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    trace_path = TRACE_DIR / f"{record['question_id']}_{condition}.json"
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
    prediction["retry_count"] = retry_count
    return prediction


def reference_free_validation(conn: sqlite3.Connection, context: dict[str, Any], sql: str) -> dict[str, Any]:
    safe, _, safety_error = smoke.validate_read_only_select(sql)
    result = smoke.execute_sql(conn, sql)
    shape = context.get("inferred_shape") or {}
    expected_cols = int(shape.get("column_count") or 1)
    normalized_hints = context.get("normalized_value_hints") or []
    value_hits = 0
    missing_hints = []
    for hint, flat in literal_groups_from_hints(normalized_hints):
        if all(value in sql for value in flat):
            value_hits += 1
        else:
            missing_hints.append(hint)
    shape_ok = bool(result.ok and len(result.columns) == expected_cols)
    order_required = bool(shape.get("order_required"))
    order_ok = not order_required or "order by" in sql.lower() or "limit" in sql.lower()
    empty_result = bool(result.ok and not result.rows)
    return {
        "safe": safe,
        "safety_error": safety_error,
        "exec_ok": result.ok,
        "exec_error": result.error,
        "column_count": len(result.columns),
        "expected_column_count": expected_cols,
        "shape_ok": shape_ok,
        "order_required": order_required,
        "order_ok": order_ok,
        "empty_result": empty_result,
        "value_hint_count": len(normalized_hints),
        "value_hits": value_hits,
        "missing_value_hints": missing_hints[:5],
    }


def rank_candidates(conn: sqlite3.Connection, context: dict[str, Any], candidates: list[str]) -> tuple[int, list[dict[str, Any]]]:
    trace = []
    best_idx = 0
    best_score = -10_000
    for idx, sql in enumerate(candidates):
        validation = reference_free_validation(conn, context, sql)
        score = 0
        score += 10 if validation["safe"] else -20
        score += 10 if validation["exec_ok"] else -15
        score += 6 if validation["shape_ok"] else -5
        score += 3 if validation["order_ok"] else -2
        score -= 2 if validation["empty_result"] else 0
        score += 4 * validation["value_hits"]
        score -= 3 * len(validation["missing_value_hints"])
        score -= idx
        entry = {"candidate_index": idx, "sql": sql, "ranker_score": score, **validation}
        trace.append(entry)
        if score > best_score:
            best_idx = idx
            best_score = score
    return best_idx, trace


def run_validated_condition(
    *,
    conn: sqlite3.Connection,
    client: Any,
    record: dict[str, Any],
    context: dict[str, Any],
    context_text: str,
) -> dict[str, Any]:
    condition = "C5_MASQLGrid_DomainContext_Validated"
    prompt = candidate_prompt(record, context_text, condition)
    error = None
    raw = ""
    model = smoke.MODEL_NAME
    latency_ms = 0
    input_tokens = 0
    output_tokens = 0
    retry_count = 0
    candidates = ["SELECT 1;"]
    try:
        raw, model, latency_ms, input_tokens, output_tokens, retry_count = call_model_with_retries(client, prompt)
        candidates = smoke.extract_candidate_sql(raw)
        if not candidates:
            candidates = ["SELECT 1;"]
            error = "no SQL candidate extracted"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    selected_idx, rank_trace = rank_candidates(conn, context, candidates)
    predicted_sql = candidates[selected_idx]
    validation = rank_trace[selected_idx] if rank_trace else reference_free_validation(conn, context, predicted_sql)
    repair_raw = ""
    repaired_sql = ""
    if not error and (not validation["exec_ok"] or not validation["shape_ok"] or not validation["order_ok"] or validation["missing_value_hints"]):
        try:
            prompt2 = repair_prompt(record, context_text, predicted_sql, validation)
            repair_raw, model2, repair_latency, repair_in, repair_out, repair_retries = call_model_with_retries(client, prompt2)
            repaired_sql = smoke.extract_sql(repair_raw)
            repaired_validation = reference_free_validation(conn, context, repaired_sql)
            if repaired_validation["exec_ok"] and (
                not validation["exec_ok"]
                or repaired_validation["shape_ok"] >= validation["shape_ok"]
                or repaired_validation["value_hits"] >= validation["value_hits"]
            ):
                candidates.append(repaired_sql)
                selected_idx = len(candidates) - 1
                predicted_sql = repaired_sql
                rank_trace.append({"candidate_index": selected_idx, "sql": repaired_sql, "ranker_score": None, **repaired_validation})
            latency_ms += repair_latency
            input_tokens += repair_in
            output_tokens += repair_out
            retry_count += repair_retries
            model = model2
        except Exception as exc:
            error = f"repair {type(exc).__name__}: {exc}"
    trace_path = TRACE_DIR / f"{record['question_id']}_{condition}.json"
    trace_path.write_text(
        json.dumps(
            {
                "prompt": prompt,
                "raw_response": raw,
                "rank_trace": rank_trace,
                "repair_raw_response": repair_raw,
                "repaired_sql": repaired_sql,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    prediction = smoke.prediction_record(
        question_id=record["question_id"],
        condition=condition,
        model=model,
        prompt=prompt,
        schema_text=context_text,
        predicted_sql=predicted_sql,
        candidate_sql=candidates,
        selected_candidate_index=selected_idx,
        trace_path=str(trace_path.relative_to(WORKSPACE)),
        latency_ms=latency_ms,
        token_input=input_tokens,
        token_output=output_tokens,
        error=error,
    )
    prediction["retry_count"] = retry_count
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
    return 1.0 if denominator == 0 else numerator / denominator


def context_metric_rows(records: list[dict[str, Any]], contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {record["question_id"]: record for record in records}
    rows = []
    for context in contexts:
        record = by_id[context["question_id"]]
        selected_tables = set(context["selected_tables"])
        gold_tables = set(record["tables"])
        selected_columns = {f"{table}.{column}" for table, cols in context["selected_columns"].items() for column in cols}
        gold_columns = set(record["columns"])
        selected_values = {
            value
            for values in context["matched_values"].values()
            for value in values
        }
        for hint in context["normalized_value_hints"]:
            selected_values.update(v for v in record["required_value_literals"] if str(v) and str(v) in hint)
        gold_values = {str(value) for value in record["required_value_literals"] if str(value)}
        rows.append(
            {
                "question_id": context["question_id"],
                "mode": context["mode"],
                "table_recall": recall(len(gold_tables & selected_tables), len(gold_tables)),
                "column_recall": recall(len(gold_columns & selected_columns), len(gold_columns)),
                "value_recall": recall(len(gold_values & selected_values), len(gold_values)),
                "selected_table_count": len(selected_tables),
                "selected_column_count": len(selected_columns),
                "matched_value_count": len(selected_values),
            }
        )
    return rows


def prediction_diagnostics(conn: sqlite3.Connection, predictions: list[dict[str, Any]], contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    context_by_key = {(context["question_id"], context["mode"]): context for context in contexts}
    rows = []
    for prediction in predictions:
        mode = "domain" if prediction["condition"] in {"C4_MASQLGrid_DomainContext", "C5_MASQLGrid_DomainContext_Validated"} else "generic"
        context = context_by_key.get((prediction["question_id"], mode))
        if not context:
            context = {"inferred_shape": {}, "normalized_value_hints": []}
        validation = reference_free_validation(conn, context, prediction["predicted_sql"])
        rows.append({"question_id": prediction["question_id"], "condition": prediction["condition"], **validation})
    return rows


def prompt_token_rows(predictions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for prediction in predictions:
        trace = json.loads((WORKSPACE / prediction["intermediate_trace_path"]).read_text(encoding="utf-8"))
        prompt = trace.get("prompt", "")
        rows.append(
            {
                "question_id": prediction["question_id"],
                "condition": prediction["condition"],
                "prompt_tokens_est": estimate_tokens(prompt),
                "api_prompt_tokens": int(prediction.get("token_input") or 0),
                "api_output_tokens": int(prediction.get("token_output") or 0),
            }
        )
    return rows


def write_report(
    *,
    predictions: list[dict[str, Any]],
    scores: list[smoke.SmokeScore],
    contexts: list[dict[str, Any]],
    context_metrics: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
    token_rows: list[dict[str, Any]],
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
    valid_by_condition = {
        condition: sum(score.safe_sql for score in scores if score.condition == condition)
        for condition in sorted(condition_counts)
    }
    provider_failures = Counter(prediction["condition"] for prediction in predictions if prediction.get("error"))
    retry_by_condition = {
        condition: sum(int(prediction.get("retry_count") or 0) for prediction in predictions if prediction["condition"] == condition)
        for condition in sorted(condition_counts)
    }
    avg_prompt_tokens = {
        condition: sum(row["prompt_tokens_est"] for row in token_rows if row["condition"] == condition)
        / max(1, sum(1 for row in token_rows if row["condition"] == condition))
        for condition in sorted(condition_counts)
    }
    diag_by_condition = {
        condition: [row for row in diagnostics if row["condition"] == condition]
        for condition in sorted(condition_counts)
    }
    rows_by_q: dict[str, dict[str, smoke.SmokeScore]] = {}
    for score in scores:
        rows_by_q.setdefault(score.question_id, {})[score.condition] = score
    domain_context_metrics = [row for row in context_metrics if row["mode"] == "domain"]
    generic_context_metrics = [row for row in context_metrics if row["mode"] == "generic"]

    def avg(rows: list[dict[str, Any]], key: str) -> float:
        return sum(float(row[key]) for row in rows) / max(1, len(rows))

    c1 = "C1_SchemaOnly_Direct"
    c2 = "C2_FullSchemaValues_Direct"
    c3 = "C3_CHESSLite_Generic"
    c4 = "C4_MASQLGrid_DomainContext"
    c5 = "C5_MASQLGrid_DomainContext_Validated"
    c4_over_c1 = sum(rows[c4].evaluator_correct and not rows[c1].evaluator_correct for rows in rows_by_q.values())
    c5_over_c1 = sum(rows[c5].evaluator_correct and not rows[c1].evaluator_correct for rows in rows_by_q.values())
    c4_over_c3 = sum(rows[c4].evaluator_correct and not rows[c3].evaluator_correct for rows in rows_by_q.values())
    c5_over_c3 = sum(rows[c5].evaluator_correct and not rows[c3].evaluator_correct for rows in rows_by_q.values())
    c2_over_c5 = sum(rows[c2].evaluator_correct and not rows[c5].evaluator_correct for rows in rows_by_q.values())
    c5_over_c2 = sum(rows[c5].evaluator_correct and not rows[c2].evaluator_correct for rows in rows_by_q.values())
    c4_acc = correct_by_condition[c4] / condition_counts[c4]
    c5_acc = correct_by_condition[c5] / condition_counts[c5]
    c3_acc = correct_by_condition[c3] / condition_counts[c3]
    c2_acc = correct_by_condition[c2] / condition_counts[c2]
    method_beats_generic = c4_acc > c3_acc or c5_acc > c3_acc
    method_beats_schema = c4_acc > correct_by_condition[c1] / condition_counts[c1] or c5_acc > correct_by_condition[c1] / condition_counts[c1]
    method_near_c2 = max(c4_acc, c5_acc) >= max(0.0, c2_acc - 0.15)

    lines = [
        "# Dev-Only CHESS-Style MA-SQLGrid Feasibility Pilot",
        "",
        "## Scope",
        "",
        "- Purpose: test whether a CHESS-style pipeline with power-grid domain context, value normalization, shape control, and validation is viable before three-pack generation.",
        "- This is not a formal experiment and must not be used for paper claims.",
        "- Split: dev only, Q001-Q020. The test split Q021-Q200 is not evaluated.",
        f"- Model/provider: `{smoke.MODEL_NAME}` via `{smoke.PROVIDER}` `{smoke.BASE_URL}` with `wire_api={smoke.WIRE_API}` and temperature `{smoke.TEMPERATURE}`.",
        "",
        "## Conditions",
        "",
        "- C1_SchemaOnly_Direct: full schema and question only.",
        "- C2_FullSchemaValues_Direct: full schema plus database value dictionary, without gold metadata.",
        "- C3_CHESSLite_Generic: generic keyword/value retrieval, schema selection, and direct SQL generation.",
        "- C4_MASQLGrid_DomainContext: C3 plus power-grid domain normalization and answer-shape hints inferred from question text.",
        "- C5_MASQLGrid_DomainContext_Validated: C4 plus multi-candidate generation, reference-free execution/shape/value validation, ranking, and one repair opportunity.",
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
        "- expected records: 100",
        f"- records with contract errors: {sum(1 for score in scores if score.contract_errors)}",
        f"- records with unsafe SQL: {sum(1 for score in scores if not score.safe_sql)}",
        f"- records with model/extraction/provider errors: {sum(1 for prediction in predictions if prediction.get('error'))}",
        f"- provider/model failure counts by condition: {dict(provider_failures) if provider_failures else 'none'}",
        f"- outer model-call retries by condition: {retry_by_condition}",
        "- Note: the project LLM client may perform internal retries before surfacing an exception; those internal retries are visible in console logs but are not exposed in prediction records.",
        "",
        "## Accuracy, Validity, And Prompt Size",
        "",
        "| condition | records | correct | accuracy | valid SQL rate | avg prompt tokens est. | evaluator errors |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for condition in sorted(condition_counts):
        records = condition_counts[condition]
        correct = correct_by_condition[condition]
        valid = valid_by_condition[condition]
        errors = errors_by_condition[condition]
        lines.append(
            f"| {condition} | {records} | {correct} | {correct / records:.3f} | {valid / records:.3f} | "
            f"{avg_prompt_tokens[condition]:.1f} | {dict(errors) if errors else 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Shape And Value Diagnostics",
            "",
            "| condition | shape mismatches by inferred shape | missing value-hint records | execution failures | empty-result records |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for condition in sorted(condition_counts):
        rows = diag_by_condition[condition]
        shape_mismatch = sum(1 for row in rows if not row["shape_ok"])
        missing_values = sum(1 for row in rows if row["missing_value_hints"])
        exec_failures = sum(1 for row in rows if not row["exec_ok"])
        empty_results = sum(1 for row in rows if row["empty_result"])
        lines.append(f"| {condition} | {shape_mismatch} | {missing_values} | {exec_failures} | {empty_results} |")
    lines.extend(
        [
            "",
            "## Context Selection Diagnostics",
            "",
            f"- Generic context average table recall vs dev metadata: {avg(generic_context_metrics, 'table_recall'):.3f}",
            f"- Generic context average column recall vs dev metadata: {avg(generic_context_metrics, 'column_recall'):.3f}",
            f"- Generic context average value recall vs dev metadata: {avg(generic_context_metrics, 'value_recall'):.3f}",
            f"- Domain context average table recall vs dev metadata: {avg(domain_context_metrics, 'table_recall'):.3f}",
            f"- Domain context average column recall vs dev metadata: {avg(domain_context_metrics, 'column_recall'):.3f}",
            f"- Domain context average value recall vs dev metadata: {avg(domain_context_metrics, 'value_recall'):.3f}",
            "",
            "| question_id | generic table R | generic column R | generic value R | domain table R | domain column R | domain value R |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    metrics_by_key = {(row["question_id"], row["mode"]): row for row in context_metrics}
    for qid in sorted(rows_by_q):
        g = metrics_by_key[(qid, "generic")]
        d = metrics_by_key[(qid, "domain")]
        lines.append(
            f"| {qid} | {g['table_recall']:.3f} | {g['column_recall']:.3f} | {g['value_recall']:.3f} | "
            f"{d['table_recall']:.3f} | {d['column_recall']:.3f} | {d['value_recall']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Paired Viability Checks",
            "",
            f"- C4 correct while C1 is wrong: {c4_over_c1}",
            f"- C5 correct while C1 is wrong: {c5_over_c1}",
            f"- C4 correct while C3 is wrong: {c4_over_c3}",
            f"- C5 correct while C3 is wrong: {c5_over_c3}",
            f"- C2 correct while C5 is wrong: {c2_over_c5}",
            f"- C5 correct while C2 is wrong: {c5_over_c2}",
            "",
            "| question_id | C1 | C2 | C3 | C4 | C5 | C1 error | C3 error | C5 error |",
            "|---|---:|---:|---:|---:|---:|---|---|---|",
        ]
    )
    for qid in sorted(rows_by_q):
        row = rows_by_q[qid]
        lines.append(
            f"| {qid} | {row[c1].evaluator_correct} | {row[c2].evaluator_correct} | {row[c3].evaluator_correct} | "
            f"{row[c4].evaluator_correct} | {row[c5].evaluator_correct} | {row[c1].evaluator_error_type} | "
            f"{row[c3].evaluator_error_type} | {row[c5].evaluator_error_type} |"
        )
    lines.extend(
        [
            "",
            "## Gold-Leakage Check",
            "",
            "- C1 receives only schema and question.",
            "- C2 receives schema, database value dictionary, and question; it does not receive answer-shape metadata, required-literal metadata, order-sensitive metadata, gold SQL, or gold result rows.",
            "- C3/C4/C5 context selection uses question text, schema, foreign-key graph, database values, and fixed local normalization rules only.",
            "- Dev metadata is used only after prediction generation for scoring and diagnostic recall/error analysis.",
            "- C5 validation uses only read-only execution status, inferred shape, inferred value hints, and inferred ordering hints. It does not use evaluator denotation feedback.",
            "",
            "## Decision",
            "",
        ]
    )
    if method_beats_schema and method_beats_generic and method_near_c2:
        lines.append("PASS: the CHESS-style MA-SQLGrid direction is viable on this dev-only pilot. C4/C5 improve over schema-only and generic CHESS-lite context while staying close enough to the full-schema-values direct baseline to justify prepare-paper packaging.")
    elif method_beats_schema and method_beats_generic:
        lines.append("MIXED: C4/C5 improve over schema-only and generic CHESS-lite context, but remain too far from C2. The method needs either harder dev cases explaining C2's advantage or a stronger validation/ranking module before three-pack.")
    else:
        lines.append("FAIL: C4/C5 do not show the required advantage over C1/C3. Do not package this as the paper method; return to direction selection or reframe around dataset/evaluator diagnostics.")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_question_bundle(
    *,
    record: dict[str, Any],
    schema_only_context: str,
    full_schema_values_context: str,
    generic: dict[str, Any],
    domain: dict[str, Any],
    generic_text: str,
    domain_text: str,
) -> list[dict[str, Any]]:
    client = smoke.llm_client()
    conn = sqlite3.connect(smoke.DB_PATH)
    try:
        return [
            run_direct_condition(
                client=client,
                record=record,
                condition="C1_SchemaOnly_Direct",
                context_text=schema_only_context,
            ),
            run_direct_condition(
                client=client,
                record=record,
                condition="C2_FullSchemaValues_Direct",
                context_text=full_schema_values_context,
            ),
            run_direct_condition(
                client=client,
                record=record,
                condition="C3_CHESSLite_Generic",
                context_text=generic_text,
            ),
            run_direct_condition(
                client=client,
                record=record,
                condition="C4_MASQLGrid_DomainContext",
                context_text=domain_text,
            ),
            run_validated_condition(
                conn=conn,
                client=client,
                record=record,
                context=domain,
                context_text=domain_text,
            ),
        ]
    finally:
        conn.close()


def run() -> int:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    questions = dev_pilot.load_dev_questions()
    predictions: list[dict[str, Any]] = []
    contexts: list[dict[str, Any]] = []
    bundles: list[dict[str, Any]] = []
    conn = sqlite3.connect(smoke.DB_PATH)
    try:
        schema_only_context = "\n".join(["SQLite schema:", smoke.SCHEMA_PATH.read_text(encoding="utf-8").strip()])
        full_schema_values_context = render_full_schema_values(conn)
        for record in questions:
            generic = generic_context(conn, record)
            domain = infer_domain_context(conn, record)
            contexts.extend([generic, domain])
            generic_text = render_selected_context(generic, domain=False)
            domain_text = render_selected_context(domain, domain=True)
            bundles.append(
                {
                    "record": record,
                    "schema_only_context": schema_only_context,
                    "full_schema_values_context": full_schema_values_context,
                    "generic": generic,
                    "domain": domain,
                    "generic_text": generic_text,
                    "domain_text": domain_text,
                }
            )
    finally:
        conn.close()

    max_workers = max(1, int(os.environ.get("CHESS_STYLE_MAX_WORKERS", str(DEFAULT_MAX_WORKERS))))
    print(f"Running CHESS-style pilot with max_workers={max_workers} on {len(bundles)} dev questions")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_qid = {
            executor.submit(run_question_bundle, **bundle): bundle["record"]["question_id"]
            for bundle in bundles
        }
        for future in as_completed(future_to_qid):
            qid = future_to_qid[future]
            try:
                predictions.extend(future.result())
                print(f"completed {qid}")
            except Exception as exc:
                print(f"worker failed for {qid}: {type(exc).__name__}: {exc}")
                raise

    condition_order = {
        "C1_SchemaOnly_Direct": 1,
        "C2_FullSchemaValues_Direct": 2,
        "C3_CHESSLite_Generic": 3,
        "C4_MASQLGrid_DomainContext": 4,
        "C5_MASQLGrid_DomainContext_Validated": 5,
    }
    predictions.sort(key=lambda item: (item["question_id"], condition_order[item["condition"]]))

    conn = sqlite3.connect(smoke.DB_PATH)
    try:
        with PREDICTIONS_PATH.open("w", encoding="utf-8") as f:
            for prediction in predictions:
                f.write(json.dumps(prediction, sort_keys=True) + "\n")
        with CONTEXTS_PATH.open("w", encoding="utf-8") as f:
            for context in contexts:
                f.write(json.dumps(context, sort_keys=True) + "\n")

        scores = score_predictions(conn, questions, predictions)
        context_rows = context_metric_rows(questions, contexts)
        diagnostics = prediction_diagnostics(conn, predictions, contexts)
        token_rows = prompt_token_rows(predictions)
    finally:
        conn.close()

    with SCORES_PATH.open("w", encoding="utf-8") as f:
        for score in scores:
            f.write(json.dumps(asdict(score), sort_keys=True) + "\n")

    write_report(
        predictions=predictions,
        scores=scores,
        contexts=contexts,
        context_metrics=context_rows,
        diagnostics=diagnostics,
        token_rows=token_rows,
    )

    if len(predictions) != 100:
        print(f"FAIL: expected 100 prediction records, got {len(predictions)}")
        return 1
    if any(score.contract_errors for score in scores):
        print("FAIL: at least one prediction record violates the contract")
        return 1
    if any(not score.safe_sql for score in scores):
        print("FAIL: at least one prediction record contains unsafe SQL")
        return 1
    if any(prediction.get("error") for prediction in predictions):
        print("FAIL: at least one prediction record has a model/extraction/provider error")
        return 1
    print(f"PASS: wrote {PREDICTIONS_PATH.relative_to(WORKSPACE)} and {REPORT_PATH.relative_to(WORKSPACE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
