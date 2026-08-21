#!/usr/bin/env python3
"""Build a deterministic RTS-GMLC SQLite and AUTO_CANDIDATE NL-to-SQL pilot.

The generated questions are programmatic candidates, not human annotations and
not a sealed benchmark.  The builder performs no network access and treats the
local RTS-GMLC checkout as immutable source material.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterable


PILOT = Path(__file__).resolve().parents[1]
WORKSPACE = PILOT.parents[4]
SOURCE_ROOT = WORKSPACE / "data" / "public_datasets" / "production_cost" / "rts-gmlc"
RTS_DATA = SOURCE_ROOT / "RTS_Data"
OUTPUT = PILOT / "artifacts"

SOURCE_FILES = {
    "license_readme": SOURCE_ROOT / "README.md",
    "buses": RTS_DATA / "SourceData" / "bus.csv",
    "generators": RTS_DATA / "SourceData" / "gen.csv",
    "branches": RTS_DATA / "SourceData" / "branch.csv",
    "reserve_products": RTS_DATA / "SourceData" / "reserves.csv",
    "load_da": RTS_DATA / "timeseries_data_files" / "Load" / "DAY_AHEAD_regional_Load.csv",
    "wind_da": RTS_DATA / "timeseries_data_files" / "WIND" / "DAY_AHEAD_wind.csv",
    "pv_da": RTS_DATA / "timeseries_data_files" / "PV" / "DAY_AHEAD_pv.csv",
    "reserve_r1_da": RTS_DATA / "timeseries_data_files" / "Reserves" / "DAY_AHEAD_regional_Spin_Up_R1.csv",
    "reserve_r2_da": RTS_DATA / "timeseries_data_files" / "Reserves" / "DAY_AHEAD_regional_Spin_Up_R2.csv",
    "reserve_r3_da": RTS_DATA / "timeseries_data_files" / "Reserves" / "DAY_AHEAD_regional_Spin_Up_R3.csv",
    "dispatch_generation": RTS_DATA / "FormattedData" / "PLEXOS" / "PLEXOS_Solution" / "DAY_AHEAD Solution Files" / "allTX" / "PLEXOS_DA_solution_generation.csv",
    "dispatch_commitment": RTS_DATA / "FormattedData" / "PLEXOS" / "PLEXOS_Solution" / "DAY_AHEAD Solution Files" / "allTX" / "PLEXOS_DA_solution_commitment.csv",
    "dispatch_cost": RTS_DATA / "FormattedData" / "PLEXOS" / "PLEXOS_Solution" / "DAY_AHEAD Solution Files" / "allTX" / "PLEXOS_DA_solution_cost.csv",
}

SCHEMA_SQL = """PRAGMA foreign_keys = ON;
PRAGMA journal_mode = DELETE;

CREATE TABLE buses (
    bus_id INTEGER PRIMARY KEY,
    bus_name TEXT NOT NULL,
    base_kv REAL NOT NULL,
    bus_type TEXT NOT NULL,
    mw_load REAL NOT NULL,
    mvar_load REAL NOT NULL,
    area INTEGER NOT NULL,
    sub_area REAL,
    zone REAL,
    latitude REAL,
    longitude REAL
);

CREATE TABLE generators (
    generator_uid TEXT PRIMARY KEY,
    bus_id INTEGER NOT NULL REFERENCES buses(bus_id),
    generator_id TEXT NOT NULL,
    unit_group TEXT,
    unit_type TEXT NOT NULL,
    category TEXT NOT NULL,
    fuel TEXT NOT NULL,
    initial_mw REAL,
    initial_mvar REAL
);

CREATE TABLE generator_constraints (
    generator_uid TEXT PRIMARY KEY REFERENCES generators(generator_uid),
    pmax_mw REAL,
    pmin_mw REAL,
    qmax_mvar REAL,
    qmin_mvar REAL,
    min_down_time_hr REAL,
    min_up_time_hr REAL,
    ramp_rate_mw_per_min REAL,
    cold_start_time_hr REAL,
    warm_start_time_hr REAL,
    hot_start_time_hr REAL,
    forced_outage_rate REAL,
    mean_time_to_failure_hr REAL,
    mean_time_to_repair_hr REAL,
    scheduled_maintenance_weeks REAL
);

CREATE TABLE generator_costs (
    generator_uid TEXT PRIMARY KEY REFERENCES generators(generator_uid),
    fuel_price_usd_per_mmbtu REAL,
    nonfuel_start_cost_usd REAL,
    nonfuel_shutdown_cost_usd REAL,
    variable_om_source_value REAL,
    output_fraction_0 REAL,
    output_fraction_1 REAL,
    output_fraction_2 REAL,
    output_fraction_3 REAL,
    average_heat_rate_0 REAL,
    incremental_heat_rate_1 REAL,
    incremental_heat_rate_2 REAL,
    incremental_heat_rate_3 REAL
);

CREATE TABLE branches (
    branch_uid TEXT PRIMARY KEY,
    from_bus_id INTEGER NOT NULL REFERENCES buses(bus_id),
    to_bus_id INTEGER NOT NULL REFERENCES buses(bus_id),
    resistance_pu REAL NOT NULL,
    reactance_pu REAL NOT NULL,
    susceptance_pu REAL NOT NULL,
    continuous_rating_mva REAL,
    long_term_emergency_rating_mva REAL,
    short_term_emergency_rating_mva REAL,
    permanent_outage_rate REAL,
    outage_duration_hr REAL,
    transformer_ratio REAL,
    transient_outage_rate REAL,
    length_miles_source_value REAL
);

CREATE TABLE reserve_products (
    reserve_product TEXT PRIMARY KEY,
    timeframe_sec REAL,
    static_requirement_mw REAL,
    eligible_regions TEXT,
    eligible_device_categories TEXT,
    eligible_device_subcategories TEXT,
    direction TEXT
);

CREATE TABLE load_timeseries_da (
    timestamp TEXT NOT NULL,
    period INTEGER NOT NULL,
    region INTEGER NOT NULL,
    load_mw REAL NOT NULL,
    PRIMARY KEY (timestamp, region)
);

CREATE TABLE renewable_availability_da (
    timestamp TEXT NOT NULL,
    period INTEGER NOT NULL,
    generator_uid TEXT NOT NULL REFERENCES generators(generator_uid),
    resource_type TEXT NOT NULL CHECK (resource_type IN ('WIND', 'PV')),
    available_mw REAL NOT NULL,
    PRIMARY KEY (timestamp, generator_uid)
);

CREATE TABLE reserve_requirements_da (
    timestamp TEXT NOT NULL,
    period INTEGER NOT NULL,
    reserve_product TEXT NOT NULL REFERENCES reserve_products(reserve_product),
    requirement_mw REAL NOT NULL,
    PRIMARY KEY (timestamp, reserve_product)
);

CREATE TABLE dispatch_da (
    timestamp TEXT NOT NULL,
    generator_uid TEXT NOT NULL REFERENCES generators(generator_uid),
    generation_mw REAL NOT NULL,
    committed INTEGER NOT NULL CHECK (committed IN (0, 1)),
    production_cost_value REAL NOT NULL,
    transmission_scenario TEXT NOT NULL CHECK (transmission_scenario = 'allTX'),
    PRIMARY KEY (timestamp, generator_uid, transmission_scenario)
);

CREATE INDEX idx_generators_fuel ON generators(fuel);
CREATE INDEX idx_generators_bus ON generators(bus_id);
CREATE INDEX idx_constraints_pmax ON generator_constraints(pmax_mw);
CREATE INDEX idx_branches_from_to ON branches(from_bus_id, to_bus_id);
CREATE INDEX idx_load_time ON load_timeseries_da(timestamp);
CREATE INDEX idx_renewable_time_type ON renewable_availability_da(timestamp, resource_type);
CREATE INDEX idx_dispatch_generator_time ON dispatch_da(generator_uid, timestamp);
CREATE INDEX idx_dispatch_time_generation ON dispatch_da(timestamp, generation_mw DESC);
"""

TABLE_DESCRIPTIONS = {
    "buses": "RTS-GMLC buses and static load/geographic attributes.",
    "generators": "Generator identity, classification, fuel, bus, and initial injection.",
    "generator_constraints": "Unit operating, ramping, start-time, and outage constraints.",
    "generator_costs": "Fuel, start/shutdown, O&M, and heat-rate source values.",
    "branches": "AC branch topology, impedance, ratings, and outage attributes.",
    "reserve_products": "Static reserve-product definitions and eligibility.",
    "load_timeseries_da": "Long-form day-ahead regional load series for 2020.",
    "renewable_availability_da": "Long-form day-ahead WIND/PV availability series for 2020.",
    "reserve_requirements_da": "Long-form day-ahead spinning reserve requirements by region product.",
    "dispatch_da": "Long-form PLEXOS day-ahead all-transmission generation, commitment, and cost solution.",
}

SOURCE_TABLE_MAP = {
    "buses": "RTS_Data/SourceData/bus.csv",
    "generators": "RTS_Data/SourceData/gen.csv",
    "generator_constraints": "RTS_Data/SourceData/gen.csv",
    "generator_costs": "RTS_Data/SourceData/gen.csv",
    "branches": "RTS_Data/SourceData/branch.csv",
    "reserve_products": "RTS_Data/SourceData/reserves.csv",
    "load_timeseries_da": "RTS_Data/timeseries_data_files/Load/DAY_AHEAD_regional_Load.csv",
    "renewable_availability_da": "RTS_Data/timeseries_data_files/{WIND,PV}/DAY_AHEAD_*.csv",
    "reserve_requirements_da": "RTS_Data/timeseries_data_files/Reserves/DAY_AHEAD_regional_Spin_Up_R{1,2,3}.csv",
    "dispatch_da": "RTS_Data/FormattedData/PLEXOS/PLEXOS_Solution/DAY_AHEAD Solution Files/allTX/{generation,commitment,cost}.csv",
}

SPECIAL_COLUMN_NOTES = {
    ("load_timeseries_da", "timestamp"): "Derived deterministically as local calendar date plus Period-1 hours; source does not provide a timezone.",
    ("renewable_availability_da", "timestamp"): "Derived deterministically as local calendar date plus Period-1 hours; source does not provide a timezone.",
    ("reserve_requirements_da", "timestamp"): "Derived deterministically as local calendar date plus Period-1 hours; source does not provide a timezone.",
    ("dispatch_da", "production_cost_value"): "PLEXOS solution value retained without asserting currency or interval semantics; source documentation was insufficient for independent unit verification.",
    ("branches", "length_miles_source_value"): "Source column is named Length; miles are suggested by RTS conventions but not independently verified in this pilot.",
    ("generator_costs", "variable_om_source_value"): "Source VOM value retained; unit not independently verified in this pilot.",
}

FAMILY_SPLITS = {
    "F01_generator_fuel_filter": "candidate_train",
    "F02_capacity_aggregate_by_fuel": "candidate_train",
    "F03_operating_constraint_filter": "candidate_train",
    "F04_generator_bus_join": "candidate_train",
    "F05_capacity_topk": "candidate_train",
    "F06_dispatch_timestamp_filter": "candidate_train",
    "F07_dispatch_fuel_daily_aggregate": "candidate_validation",
    "F08_regional_load_daily_aggregate": "candidate_validation",
    "F09_renewable_availability_topk": "candidate_holdout_unsealed",
    "F10_reserve_daily_aggregate": "candidate_holdout_unsealed",
    "F11_cost_topk": "candidate_holdout_unsealed",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def canonical_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def parse_float(value: str | None) -> float | None:
    text = (value or "").strip()
    if not text or text.upper() in {"NA", "N/A", "NULL"} or text == "Unit-specific":
        return None
    return float(text)


def parse_int(value: str) -> int:
    return int(float(value))


def csv_rows(path: Path) -> Iterable[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def timestamp_from_period(row: dict[str, str]) -> str:
    base = datetime(parse_int(row["Year"]), parse_int(row["Month"]), parse_int(row["Day"]))
    return (base + timedelta(hours=parse_int(row["Period"]) - 1)).strftime("%Y-%m-%d %H:%M:%S")


def initialize_database(path: Path) -> sqlite3.Connection:
    path.unlink(missing_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript("PRAGMA page_size=4096;\n" + SCHEMA_SQL)
    return conn


def load_static_tables(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO buses VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                parse_int(row["Bus ID"]), row["Bus Name"], parse_float(row["BaseKV"]), row["Bus Type"],
                parse_float(row["MW Load"]), parse_float(row["MVAR Load"]), parse_int(row["Area"]),
                parse_float(row["Sub Area"]), parse_float(row["Zone"]), parse_float(row["lat"]), parse_float(row["lng"]),
            )
            for row in csv_rows(SOURCE_FILES["buses"])
        ],
    )
    generator_rows = list(csv_rows(SOURCE_FILES["generators"]))
    conn.executemany(
        "INSERT INTO generators VALUES (?,?,?,?,?,?,?,?,?)",
        [
            (
                row["GEN UID"], parse_int(row["Bus ID"]), row["Gen ID"], row["Unit Group"],
                row["Unit Type"], row["Category"], row["Fuel"], parse_float(row["MW Inj"]), parse_float(row["MVAR Inj"]),
            )
            for row in generator_rows
        ],
    )
    conn.executemany(
        "INSERT INTO generator_constraints VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                row["GEN UID"], parse_float(row["PMax MW"]), parse_float(row["PMin MW"]),
                parse_float(row["QMax MVAR"]), parse_float(row["QMin MVAR"]),
                parse_float(row["Min Down Time Hr"]), parse_float(row["Min Up Time Hr"]),
                parse_float(row["Ramp Rate MW/Min"]), parse_float(row["Start Time Cold Hr"]),
                parse_float(row["Start Time Warm Hr"]), parse_float(row["Start Time Hot Hr"]),
                parse_float(row["FOR"]), parse_float(row["MTTF Hr"]), parse_float(row["MTTR Hr"]),
                parse_float(row["Scheduled Maint Weeks"]),
            )
            for row in generator_rows
        ],
    )
    conn.executemany(
        "INSERT INTO generator_costs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                row["GEN UID"], parse_float(row["Fuel Price $/MMBTU"]), parse_float(row["Non Fuel Start Cost $"]),
                parse_float(row["Non Fuel Shutdown Cost $"]), parse_float(row["VOM"]),
                parse_float(row["Output_pct_0"]), parse_float(row["Output_pct_1"]),
                parse_float(row["Output_pct_2"]), parse_float(row["Output_pct_3"]),
                parse_float(row["HR_avg_0"]), parse_float(row["HR_incr_1"]),
                parse_float(row["HR_incr_2"]), parse_float(row["HR_incr_3"]),
            )
            for row in generator_rows
        ],
    )
    conn.executemany(
        "INSERT INTO branches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [
            (
                row["UID"], parse_int(row["From Bus"]), parse_int(row["To Bus"]), parse_float(row["R"]),
                parse_float(row["X"]), parse_float(row["B"]), parse_float(row["Cont Rating"]),
                parse_float(row["LTE Rating"]), parse_float(row["STE Rating"]), parse_float(row["Perm OutRate"]),
                parse_float(row["Duration"]), parse_float(row["Tr Ratio"]), parse_float(row["Tran OutRate"]),
                parse_float(row["Length"]),
            )
            for row in csv_rows(SOURCE_FILES["branches"])
        ],
    )
    conn.executemany(
        "INSERT INTO reserve_products VALUES (?,?,?,?,?,?,?)",
        [
            (
                row["Reserve Product"], parse_float(row["Timeframe (sec)"]), parse_float(row["Requirement (MW)"]),
                row["Eligible Regions"], row["Eligible Device Categories"], row["Eligible Device SubCategories"],
                row["Direction"],
            )
            for row in csv_rows(SOURCE_FILES["reserve_products"])
        ],
    )


def load_long_timeseries(conn: sqlite3.Connection) -> None:
    load_batch = []
    for row in csv_rows(SOURCE_FILES["load_da"]):
        stamp, period = timestamp_from_period(row), parse_int(row["Period"])
        for region in (1, 2, 3):
            load_batch.append((stamp, period, region, parse_float(row[str(region)])))
    conn.executemany("INSERT INTO load_timeseries_da VALUES (?,?,?,?)", load_batch)

    renewable_batch = []
    for source_key, resource in (("wind_da", "WIND"), ("pv_da", "PV")):
        with SOURCE_FILES[source_key].open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            generator_columns = [name for name in (reader.fieldnames or []) if name not in {"Year", "Month", "Day", "Period"}]
            for row in reader:
                stamp, period = timestamp_from_period(row), parse_int(row["Period"])
                renewable_batch.extend(
                    (stamp, period, generator_uid, resource, parse_float(row[generator_uid]))
                    for generator_uid in generator_columns
                )
                if len(renewable_batch) >= 20000:
                    conn.executemany("INSERT INTO renewable_availability_da VALUES (?,?,?,?,?)", renewable_batch)
                    renewable_batch.clear()
    if renewable_batch:
        conn.executemany("INSERT INTO renewable_availability_da VALUES (?,?,?,?,?)", renewable_batch)

    reserve_batch = []
    for source_key in ("reserve_r1_da", "reserve_r2_da", "reserve_r3_da"):
        with SOURCE_FILES[source_key].open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            value_columns = [name for name in (reader.fieldnames or []) if name not in {"Year", "Month", "Day", "Period"}]
            if len(value_columns) != 1:
                raise RuntimeError(f"expected one reserve value column in {SOURCE_FILES[source_key]}")
            product = value_columns[0]
            for row in reader:
                reserve_batch.append((timestamp_from_period(row), parse_int(row["Period"]), product, parse_float(row[product])))
    conn.executemany("INSERT INTO reserve_requirements_da VALUES (?,?,?,?)", reserve_batch)


def read_wide_solution(path: Path) -> tuple[list[str], dict[str, list[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        generators = header[1:]
        values = {row[0]: row[1:] for row in reader}
    return generators, values


def load_dispatch(conn: sqlite3.Connection) -> None:
    generators, generation = read_wide_solution(SOURCE_FILES["dispatch_generation"])
    commitment_generators, commitment = read_wide_solution(SOURCE_FILES["dispatch_commitment"])
    cost_generators, costs = read_wide_solution(SOURCE_FILES["dispatch_cost"])
    if generators != commitment_generators or generators != cost_generators:
        raise RuntimeError("PLEXOS generation/commitment/cost generator headers differ")
    if set(generation) != set(commitment) or set(generation) != set(costs):
        raise RuntimeError("PLEXOS generation/commitment/cost timestamps differ")
    rows = []
    for timestamp in sorted(generation):
        for index, generator_uid in enumerate(generators):
            rows.append((
                timestamp, generator_uid, float(generation[timestamp][index]),
                parse_int(commitment[timestamp][index]), float(costs[timestamp][index]), "allTX",
            ))
    conn.executemany("INSERT INTO dispatch_da VALUES (?,?,?,?,?,?)", rows)


def database_table_counts(conn: sqlite3.Connection) -> dict[str, int]:
    tables = [row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )]
    return {table: conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0] for table in tables}


def build_field_dictionary(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    entries = []
    tables = [row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )]
    for table in tables:
        for cid, name, declared_type, notnull, default, primary_key in conn.execute(f'PRAGMA table_info("{table}")'):
            entries.append({
                "table": table,
                "table_description": TABLE_DESCRIPTIONS[table],
                "column": name,
                "sqlite_type": declared_type,
                "not_null": bool(notnull),
                "primary_key_position": primary_key,
                "default": default,
                "source": SOURCE_TABLE_MAP[table],
                "transformation_or_unit_note": SPECIAL_COLUMN_NOTES.get((table, name), "Directly renamed/cast from the documented source table; consult original RTS-GMLC headers for units."),
            })
    return entries


def quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def candidate_questions(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    raw: list[dict[str, Any]] = []

    def add(family: str, question: str, sql: str, tags: list[str], tables: list[str], difficulty: str = "medium") -> None:
        raw.append({
            "template_family": family,
            "split": FAMILY_SPLITS[family],
            "question": question,
            "gold_sql": sql,
            "sql_feature_tags": tags,
            "tables": tables,
            "difficulty": difficulty,
        })

    fuels = [row[0] for row in conn.execute(
        "SELECT fuel FROM generators GROUP BY fuel HAVING COUNT(*) >= 2 ORDER BY COUNT(*) DESC, fuel LIMIT 5"
    )]
    for fuel in fuels:
        add("F01_generator_fuel_filter", f"List the generator identifiers and unit types for {fuel}-fueled units.",
            f"SELECT generator_uid, unit_type FROM generators WHERE fuel = {quote(fuel)} ORDER BY generator_uid;",
            ["single-table", "filter", "order-by"], ["generators"], "easy")
        add("F02_capacity_aggregate_by_fuel", f"How many {fuel}-fueled generators are there and what is their total maximum capacity?",
            f"SELECT g.fuel, COUNT(*) AS generator_count, ROUND(SUM(c.pmax_mw), 2) AS total_pmax_mw FROM generators g JOIN generator_constraints c ON g.generator_uid = c.generator_uid WHERE g.fuel = {quote(fuel)} GROUP BY g.fuel;",
            ["join", "filter", "aggregate", "group-by"], ["generators", "generator_constraints"])

    for threshold in (1, 2, 4, 8, 12):
        add("F03_operating_constraint_filter", f"Which generators require at least {threshold} hours of minimum up time?",
            f"SELECT g.generator_uid, g.unit_type, c.min_up_time_hr FROM generators g JOIN generator_constraints c ON g.generator_uid = c.generator_uid WHERE c.min_up_time_hr >= {threshold} ORDER BY c.min_up_time_hr DESC, g.generator_uid;",
            ["join", "filter", "constraint", "order-by"], ["generators", "generator_constraints"])

    for area in (1, 2, 3):
        add("F04_generator_bus_join", f"List generators connected to buses in area {area}, with their bus names and fuels.",
            f"SELECT g.generator_uid, b.bus_name, g.fuel FROM generators g JOIN buses b ON g.bus_id = b.bus_id WHERE b.area = {area} ORDER BY b.bus_name, g.generator_uid;",
            ["join", "filter", "order-by"], ["generators", "buses"])
    for bus_type in ("PQ", "PV"):
        add("F04_generator_bus_join", f"List generators connected to {bus_type} buses, with bus names and base voltage.",
            f"SELECT g.generator_uid, b.bus_name, b.base_kv FROM generators g JOIN buses b ON g.bus_id = b.bus_id WHERE b.bus_type = {quote(bus_type)} ORDER BY b.base_kv DESC, g.generator_uid;",
            ["join", "filter", "order-by"], ["generators", "buses"])

    for limit in (1, 3, 5, 10, 15):
        add("F05_capacity_topk", f"Return the top {limit} generators by maximum MW capacity.",
            f"SELECT g.generator_uid, g.fuel, c.pmax_mw FROM generators g JOIN generator_constraints c ON g.generator_uid = c.generator_uid ORDER BY c.pmax_mw DESC, g.generator_uid LIMIT {limit};",
            ["join", "top-k", "order-by"], ["generators", "generator_constraints"], "easy")

    dispatch_times = [row[0] for row in conn.execute("SELECT DISTINCT timestamp FROM dispatch_da ORDER BY timestamp LIMIT 5")]
    for stamp in dispatch_times:
        add("F06_dispatch_timestamp_filter", f"Which generators produced positive output at {stamp} in the all-transmission day-ahead solution?",
            f"SELECT generator_uid, generation_mw FROM dispatch_da WHERE timestamp = {quote(stamp)} AND transmission_scenario = 'allTX' AND generation_mw > 0 ORDER BY generation_mw DESC, generator_uid;",
            ["single-table", "time", "filter", "order-by"], ["dispatch_da"])

    dispatch_dates = [row[0] for row in conn.execute("SELECT DISTINCT substr(timestamp, 1, 10) FROM dispatch_da ORDER BY 1 LIMIT 5")]
    for date in dispatch_dates:
        add("F07_dispatch_fuel_daily_aggregate", f"For {date}, summarize total day-ahead generation by fuel.",
            f"SELECT g.fuel, ROUND(SUM(d.generation_mw), 2) AS total_generation_mwh FROM dispatch_da d JOIN generators g ON d.generator_uid = g.generator_uid WHERE d.timestamp >= {quote(date + ' 00:00:00')} AND d.timestamp < datetime({quote(date + ' 00:00:00')}, '+1 day') GROUP BY g.fuel ORDER BY total_generation_mwh DESC, g.fuel;",
            ["join", "time", "filter", "aggregate", "group-by", "order-by"], ["dispatch_da", "generators"], "hard")

    load_dates = [row[0] for row in conn.execute("SELECT DISTINCT substr(timestamp, 1, 10) FROM load_timeseries_da ORDER BY 1 LIMIT 5")]
    for date in load_dates:
        add("F08_regional_load_daily_aggregate", f"What was the average day-ahead load for each region on {date}?",
            f"SELECT region, ROUND(AVG(load_mw), 2) AS average_load_mw FROM load_timeseries_da WHERE timestamp >= {quote(date + ' 00:00:00')} AND timestamp < datetime({quote(date + ' 00:00:00')}, '+1 day') GROUP BY region ORDER BY region;",
            ["single-table", "time", "filter", "aggregate", "group-by"], ["load_timeseries_da"])

    renewable_times = [row[0] for row in conn.execute(
        "SELECT timestamp FROM renewable_availability_da GROUP BY timestamp HAVING SUM(available_mw) > 0 ORDER BY timestamp LIMIT 5"
    )]
    for stamp in renewable_times:
        add("F09_renewable_availability_topk", f"Return the five renewable generators with the highest available MW at {stamp}, including their fuel labels.",
            f"SELECT r.generator_uid, g.fuel, r.available_mw FROM renewable_availability_da r JOIN generators g ON r.generator_uid = g.generator_uid WHERE r.timestamp = {quote(stamp)} ORDER BY r.available_mw DESC, r.generator_uid LIMIT 5;",
            ["join", "time", "filter", "top-k", "order-by"], ["renewable_availability_da", "generators"])

    reserve_dates = [row[0] for row in conn.execute("SELECT DISTINCT substr(timestamp, 1, 10) FROM reserve_requirements_da ORDER BY 1 LIMIT 5")]
    for date in reserve_dates:
        add("F10_reserve_daily_aggregate", f"What was the maximum day-ahead spinning reserve requirement for each product on {date}?",
            f"SELECT reserve_product, ROUND(MAX(requirement_mw), 3) AS maximum_requirement_mw FROM reserve_requirements_da WHERE timestamp >= {quote(date + ' 00:00:00')} AND timestamp < datetime({quote(date + ' 00:00:00')}, '+1 day') GROUP BY reserve_product ORDER BY reserve_product;",
            ["single-table", "time", "filter", "aggregate", "group-by"], ["reserve_requirements_da"])

    for limit in (1, 3, 5, 10, 15):
        add("F11_cost_topk", f"Return the top {limit} generators by non-fuel start cost, excluding missing values.",
            f"SELECT g.generator_uid, g.fuel, c.nonfuel_start_cost_usd FROM generator_costs c JOIN generators g ON c.generator_uid = g.generator_uid WHERE c.nonfuel_start_cost_usd IS NOT NULL ORDER BY c.nonfuel_start_cost_usd DESC, g.generator_uid LIMIT {limit};",
            ["join", "cost", "filter", "top-k", "order-by"], ["generator_costs", "generators"])

    questions = []
    for index, record in enumerate(raw, 1):
        questions.append({
            "question_id": f"RTS_AUTO_{index:03d}",
            "annotation_status": "AUTO_CANDIDATE",
            "human_reviewed": False,
            "sealed": False,
            "benchmark_claim_eligible": False,
            **record,
        })
    return questions


FORBIDDEN_SQL = re.compile(r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum)\b", re.IGNORECASE)


def execute_gold(conn: sqlite3.Connection, questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence = []
    for question in questions:
        sql = question["gold_sql"].strip()
        if not sql.lower().startswith(("select", "with")) or FORBIDDEN_SQL.search(sql) or sql.count(";") > 1:
            raise RuntimeError(f"unsafe gold SQL for {question['question_id']}")
        cursor = conn.execute(sql)
        columns = [item[0] for item in cursor.description or []]
        rows = [list(row) for row in cursor.fetchall()]
        if not rows:
            raise RuntimeError(f"gold SQL returned no rows for {question['question_id']}")
        result_object = {"columns": columns, "rows": rows}
        result_hash = canonical_hash(result_object)
        question["answer_shape"] = {"column_count": len(columns), "columns": columns}
        question["gold_sql_sha256"] = sha256_text(sql)
        question["gold_result_sha256"] = result_hash
        evidence.append({
            "question_id": question["question_id"],
            "status": "executed",
            "row_count": len(rows),
            "column_count": len(columns),
            "columns": columns,
            "gold_sql_sha256": question["gold_sql_sha256"],
            "result_sha256": result_hash,
            "result_preview": rows[:5],
        })
    return evidence


def build_source_manifest() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    missing = [name for name, path in SOURCE_FILES.items() if not path.exists()]
    if missing:
        raise RuntimeError(f"missing RTS-GMLC source files: {missing}")
    commit = subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "rev-parse", "HEAD"], capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=True,
    ).stdout.strip()
    files = [
        {
            "source_key": name,
            "path_within_rts_gmlc": path.relative_to(SOURCE_ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for name, path in sorted(SOURCE_FILES.items())
    ]
    readme = SOURCE_FILES["license_readme"].read_text(encoding="utf-8", errors="replace")
    notice_marker = "## DATA USE DISCLAIMER AGREEMENT"
    notice = readme[readme.index(notice_marker):].rstrip() + "\n"
    (OUTPUT / "SOURCE_DATA_USE_NOTICE.md").write_text(
        "# RTS-GMLC Source Data Use Notice\n\n"
        "> Verbatim from the locally pinned upstream README. The upstream text itself ends mid-sentence; legal review is required before redistribution.\n\n"
        + notice,
        encoding="utf-8",
    )
    manifest = {
        "schema_version": "rts-gmlc-pilot-source-manifest-v1",
        "source_name": "RTS-GMLC (Reliability Test System - Grid Modernization Lab Consortium)",
        "source_url": "https://github.com/GridMod/RTS-GMLC.git",
        "local_source_path": SOURCE_ROOT.relative_to(WORKSPACE).as_posix(),
        "git_commit": commit,
        "acquisition_status": "pre-existing local Git checkout; no W3 download performed",
        "license_audit": {
            "notice_location": "README.md, DATA USE DISCLAIMER AGREEMENT",
            "use_copy_distribute": "permitted without fee subject to retaining the entire notice",
            "publication_credit_required": "DOE/NREL/ALLIANCE",
            "redistribution_notice_required": True,
            "upstream_notice_integrity_warning": "The pinned upstream README notice ends mid-sentence; preserved verbatim and flagged for legal review.",
            "derived_copy_notice": "artifacts/SOURCE_DATA_USE_NOTICE.md",
        },
        "source_file_count": len(files),
        "source_file_set_sha256": canonical_hash(files),
    }
    return manifest, files


def write_field_dictionary(entries: list[dict[str, Any]]) -> None:
    write_json(OUTPUT / "field_dictionary.json", {"schema_version": "rts-gmlc-pilot-field-dictionary-v1", "fields": entries})
    with (OUTPUT / "field_dictionary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(entries[0]))
        writer.writeheader()
        writer.writerows(entries)


def build_report(summary: dict[str, Any], source_manifest: dict[str, Any]) -> str:
    counts = summary["table_row_counts"]
    coverage = summary["timeseries_coverage"]
    families = summary["question_family_counts"]
    splits = summary["question_split_counts"]
    return "\n".join([
        "# W3 RTS-GMLC Pilot Data Engineering Report",
        "",
        "## Outcome",
        "",
        f"- Source: RTS-GMLC commit `{source_manifest['git_commit']}`.",
        f"- SQLite tables: **{len(counts)}**; rows: **{sum(counts.values()):,}**.",
        f"- Programmatic NL/SQL records: **{summary['question_count']}**, all explicitly `AUTO_CANDIDATE`.",
        f"- Gold SQL execution: **{summary['gold_execution_success_count']}/{summary['question_count']}** successful with result hashes.",
        f"- Template families: **{len(families)}**; family overlap across splits: **{summary['template_family_overlap_count']}**.",
        f"- Database SHA-256: `{summary['database_sha256']}`.",
        "",
        "## SQLite row counts",
        "",
        "| Table | Rows |",
        "|---|---:|",
        *[f"| `{table}` | {count:,} |" for table, count in counts.items()],
        "",
        "## Time-series coverage",
        "",
        f"- Load, renewable availability, and reserve requirements: {coverage['load_da']['timestamp_count']:,} hourly timestamps from `{coverage['load_da']['min_timestamp']}` through `{coverage['load_da']['max_timestamp']}`.",
        f"- PLEXOS allTX dispatch: {coverage['dispatch_da']['timestamp_count']:,} hourly timestamps from `{coverage['dispatch_da']['min_timestamp']}` through `{coverage['dispatch_da']['max_timestamp']}`, covering {coverage['dispatch_da']['generator_count']} of {counts['generators']} generator identifiers.",
        "",
        "## Candidate question design",
        "",
        "| Split label | Candidate rows |",
        "|---|---:|",
        *[f"| `{split}` | {count} |" for split, count in splits.items()],
        "",
        "Families are assigned wholly to one split label. The holdout is named `candidate_holdout_unsealed` because generation was automatic and no independent human annotation or sealing occurred.",
        "",
        "Coverage includes single-table retrieval, joins, aggregation/grouping, time predicates, filters, top-k, generator costs, operating constraints, renewable availability, regional load, reserves, and PLEXOS dispatch.",
        "",
        "## License and provenance",
        "",
        "The pinned upstream README permits use/copy/distribution subject to retaining the complete data-use notice and crediting DOE/NREL/Alliance. The upstream notice in this commit ends mid-sentence; the exact local text is preserved in `SOURCE_DATA_USE_NOTICE.md`, and redistribution remains subject to legal review.",
        "",
        "## Scientific limitations",
        "",
        "- Questions are deterministic `AUTO_CANDIDATE` records, not human gold labels and not publication-ready sealed evidence.",
        "- PLEXOS `production_cost_value` retains source values without an independently verified unit.",
        "- Period-based timestamps assume Period 1 maps to 00:00 and have no asserted timezone.",
        "- Human domain review, paraphrase review, ambiguity adjudication, and an independently sealed split remain mandatory before confirmatory experiments.",
        "",
    ])


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source_manifest, source_files = build_source_manifest()
    write_json(OUTPUT / "source_manifest.json", source_manifest)
    write_jsonl(OUTPUT / "source_files.jsonl", source_files)
    (OUTPUT / "schema.sql").write_text(SCHEMA_SQL, encoding="utf-8")

    database = OUTPUT / "database.sqlite"
    conn = initialize_database(database)
    try:
        with conn:
            load_static_tables(conn)
            load_long_timeseries(conn)
            load_dispatch(conn)
        violations = list(conn.execute("PRAGMA foreign_key_check"))
        if violations:
            raise RuntimeError(f"foreign-key violations: {violations[:10]}")
        conn.execute("PRAGMA optimize")
        conn.execute("VACUUM")
        counts = database_table_counts(conn)
        field_dictionary = build_field_dictionary(conn)
        questions = candidate_questions(conn)
        gold_evidence = execute_gold(conn, questions)
        conn_value = conn.execute(
            "SELECT MIN(timestamp), MAX(timestamp), COUNT(DISTINCT timestamp), COUNT(DISTINCT region) FROM load_timeseries_da"
        ).fetchone()
        renewable_value = conn.execute(
            "SELECT MIN(timestamp), MAX(timestamp), COUNT(DISTINCT timestamp), COUNT(DISTINCT generator_uid) FROM renewable_availability_da"
        ).fetchone()
        reserve_value = conn.execute(
            "SELECT MIN(timestamp), MAX(timestamp), COUNT(DISTINCT timestamp), COUNT(DISTINCT reserve_product) FROM reserve_requirements_da"
        ).fetchone()
        dispatch_value = conn.execute(
            "SELECT MIN(timestamp), MAX(timestamp), COUNT(DISTINCT timestamp), COUNT(DISTINCT generator_uid) FROM dispatch_da"
        ).fetchone()
        renewable_coverage = {
            "min_timestamp": renewable_value[0], "max_timestamp": renewable_value[1],
            "timestamp_count": renewable_value[2], "generator_count": renewable_value[3],
        }
        reserve_coverage = {
            "min_timestamp": reserve_value[0], "max_timestamp": reserve_value[1],
            "timestamp_count": reserve_value[2], "product_count": reserve_value[3],
        }
        dispatch_coverage = {
            "min_timestamp": dispatch_value[0], "max_timestamp": dispatch_value[1],
            "timestamp_count": dispatch_value[2], "generator_count": dispatch_value[3],
        }
    finally:
        conn.close()

    write_field_dictionary(field_dictionary)
    questions.sort(key=lambda row: row["question_id"])
    write_jsonl(OUTPUT / "questions_auto_candidate.jsonl", questions)
    write_jsonl(OUTPUT / "gold_execution.jsonl", gold_evidence)
    split_families: dict[str, list[str]] = {}
    for family, split in FAMILY_SPLITS.items():
        split_families.setdefault(split, []).append(family)
    split_payload = {
        "schema_version": "rts-gmlc-auto-candidate-family-splits-v1",
        "split_policy": "Template families are atomic and cannot cross split labels.",
        "sealed": False,
        "human_reviewed": False,
        "splits": {split: sorted(families) for split, families in sorted(split_families.items())},
        "question_ids": {
            split: [row["question_id"] for row in questions if row["split"] == split]
            for split in sorted(split_families)
        },
    }
    write_json(OUTPUT / "splits_template_family.json", split_payload)

    family_splits: dict[str, set[str]] = {}
    for row in questions:
        family_splits.setdefault(row["template_family"], set()).add(row["split"])
    summary = {
        "schema_version": "rts-gmlc-pilot-build-summary-v1",
        "source_commit": source_manifest["git_commit"],
        "database_sha256": sha256_file(database),
        "database_bytes": database.stat().st_size,
        "schema_sha256": sha256_file(OUTPUT / "schema.sql"),
        "table_row_counts": counts,
        "timeseries_coverage": {
            "load_da": {
                "min_timestamp": conn_value[0],
                "max_timestamp": conn_value[1],
                "timestamp_count": conn_value[2],
                "region_count": conn_value[3],
            },
            "renewable_da": renewable_coverage,
            "reserve_da": reserve_coverage,
            "dispatch_da": dispatch_coverage,
        },
        "question_count": len(questions),
        "question_family_counts": dict(sorted(Counter(row["template_family"] for row in questions).items())),
        "question_split_counts": dict(sorted(Counter(row["split"] for row in questions).items())),
        "annotation_status_counts": dict(sorted(Counter(row["annotation_status"] for row in questions).items())),
        "human_reviewed_count": sum(bool(row["human_reviewed"]) for row in questions),
        "sealed_count": sum(bool(row["sealed"]) for row in questions),
        "template_family_overlap_count": sum(len(splits) != 1 for splits in family_splits.values()),
        "gold_execution_success_count": sum(row["status"] == "executed" for row in gold_evidence),
        "gold_execution_result_set_sha256": canonical_hash([
            {"question_id": row["question_id"], "result_sha256": row["result_sha256"]} for row in gold_evidence
        ]),
    }
    write_json(OUTPUT / "build_summary.json", summary)
    (PILOT / "W3_RTS_GMLC_REPORT.md").write_text(build_report(summary, source_manifest), encoding="utf-8")

    artifact_names = [
        "SOURCE_DATA_USE_NOTICE.md", "schema.sql", "database.sqlite", "field_dictionary.json",
        "field_dictionary.csv", "source_manifest.json", "source_files.jsonl",
        "questions_auto_candidate.jsonl", "splits_template_family.json", "gold_execution.jsonl",
        "build_summary.json",
    ]
    artifacts = [
        {"path": name, "bytes": (OUTPUT / name).stat().st_size, "sha256": sha256_file(OUTPUT / name)}
        for name in artifact_names
    ]
    artifacts.append({
        "path": "../W3_RTS_GMLC_REPORT.md",
        "bytes": (PILOT / "W3_RTS_GMLC_REPORT.md").stat().st_size,
        "sha256": sha256_file(PILOT / "W3_RTS_GMLC_REPORT.md"),
    })
    write_json(OUTPUT / "artifact_manifest.json", {
        "schema_version": "rts-gmlc-pilot-artifact-manifest-v1",
        "builder_sha256": sha256_file(Path(__file__)),
        "artifacts": artifacts,
        "artifact_set_sha256": canonical_hash(artifacts),
    })
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
