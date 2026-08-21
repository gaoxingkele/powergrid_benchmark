#!/usr/bin/env python3
"""Build a deterministic SimBench-derived SQLite pilot for MA-SQLGrid.

The generated NL/SQL records are machine-created AUTO_CANDIDATE items.  They
are neither human gold nor sealed test data.  The source SimBench database is
licensed under ODbL/DbCL; SimBench code is BSD-3-Clause (see source manifest).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import importlib.metadata
import json
import math
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any


NETWORK_CODE = "1-MV-urban--0-sw"
STATUS = "AUTO_CANDIDATE"
SCHEMA_VERSION = "simbench-ma-sqlgrid-pilot-1.0"

SCHEMA_SQL = """PRAGMA foreign_keys = ON;

CREATE TABLE networks (
    network_code TEXT PRIMARY KEY,
    source_dataset TEXT NOT NULL,
    scenario INTEGER NOT NULL,
    voltage_scope TEXT NOT NULL,
    settlement_type TEXT NOT NULL,
    switch_representation TEXT NOT NULL,
    base_power_mva REAL NOT NULL
);

CREATE TABLE voltage_levels (
    network_code TEXT NOT NULL,
    voltage_level_code INTEGER NOT NULL,
    nominal_kv REAL NOT NULL,
    bus_count INTEGER NOT NULL,
    PRIMARY KEY (network_code, voltage_level_code, nominal_kv),
    FOREIGN KEY (network_code) REFERENCES networks(network_code)
);

CREATE TABLE buses (
    bus_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    nominal_kv REAL NOT NULL,
    bus_type TEXT,
    subnet TEXT,
    substation TEXT,
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    min_voltage_pu REAL,
    max_voltage_pu REAL,
    FOREIGN KEY (network_code) REFERENCES networks(network_code)
);

CREATE TABLE lines (
    line_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    from_bus_id INTEGER NOT NULL,
    to_bus_id INTEGER NOT NULL,
    standard_type TEXT,
    length_km REAL NOT NULL,
    resistance_ohm_per_km REAL,
    reactance_ohm_per_km REAL,
    max_current_ka REAL,
    max_loading_percent REAL,
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (from_bus_id) REFERENCES buses(bus_id),
    FOREIGN KEY (to_bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE transformers (
    transformer_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    hv_bus_id INTEGER NOT NULL,
    lv_bus_id INTEGER NOT NULL,
    rated_power_mva REAL NOT NULL,
    hv_nominal_kv REAL NOT NULL,
    lv_nominal_kv REAL NOT NULL,
    vector_group TEXT,
    tap_position INTEGER,
    on_load_tap_changer INTEGER CHECK (on_load_tap_changer IN (0, 1)),
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (hv_bus_id) REFERENCES buses(bus_id),
    FOREIGN KEY (lv_bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE loads (
    load_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    bus_id INTEGER NOT NULL,
    active_power_mw REAL NOT NULL,
    reactive_power_mvar REAL NOT NULL,
    maximum_active_power_mw REAL,
    minimum_active_power_mw REAL,
    profile TEXT,
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE generators (
    generator_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT NOT NULL,
    bus_id INTEGER NOT NULL,
    active_power_mw REAL NOT NULL,
    reactive_power_mvar REAL NOT NULL,
    rated_power_mva REAL,
    maximum_active_power_mw REAL,
    minimum_active_power_mw REAL,
    generator_type TEXT,
    physical_type TEXT,
    profile TEXT,
    controllable INTEGER CHECK (controllable IN (0, 1)),
    voltage_level_code INTEGER,
    in_service INTEGER NOT NULL CHECK (in_service IN (0, 1)),
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id)
);

CREATE TABLE switches (
    switch_id INTEGER PRIMARY KEY,
    network_code TEXT NOT NULL,
    name TEXT,
    bus_id INTEGER NOT NULL,
    element_id INTEGER NOT NULL,
    element_type TEXT NOT NULL,
    switch_type TEXT,
    closed INTEGER NOT NULL CHECK (closed IN (0, 1)),
    voltage_level_code INTEGER,
    FOREIGN KEY (network_code) REFERENCES networks(network_code),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id)
);

CREATE INDEX idx_lines_from_bus ON lines(from_bus_id);
CREATE INDEX idx_lines_to_bus ON lines(to_bus_id);
CREATE INDEX idx_loads_bus ON loads(bus_id);
CREATE INDEX idx_generators_bus ON generators(bus_id);
CREATE INDEX idx_switches_bus ON switches(bus_id);
"""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_dump(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def clean(value: Any) -> Any:
    if value is None:
        return None
    try:
        if bool(math.isnan(value)):
            return None
    except (TypeError, ValueError):
        pass
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, bool):
        return int(value)
    return value


def git_value(root: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_simbench(source_root: Path):
    sys.path.insert(0, str(source_root))
    sys.modules.pop("simbench", None)
    return importlib.import_module("simbench")


def source_manifest(source_root: Path, simbench_module: Any) -> dict[str, Any]:
    network_dir = source_root / "simbench" / "networks" / "1-complete_data-mixed-all-0-sw"
    source_files = []
    for path in sorted(network_dir.glob("*.csv")):
        source_files.append({
            "relative_path": path.relative_to(source_root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    for relative in ("LICENSE", "AUTHORS"):
        path = source_root / relative
        source_files.append({
            "relative_path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    try:
        version = importlib.metadata.version("simbench")
    except importlib.metadata.PackageNotFoundError:
        version = getattr(simbench_module, "__version__", "unknown")
    return {
        "manifest_version": "1.0",
        "dataset": "SimBench",
        "selected_network_code": NETWORK_CODE,
        "selection_reason": "Representative urban MV distribution grid with 110/10 kV buses, lines, transformers, loads, distributed renewable generators, and switch topology.",
        "upstream_repository": "https://github.com/e2nIEE/simbench",
        "upstream_project": "https://simbench.de/",
        "local_source_root": str(source_root.resolve()),
        "git_commit": git_value(source_root, "rev-parse", "HEAD"),
        "git_remote": git_value(source_root, "remote", "get-url", "origin"),
        "simbench_version": version,
        "licenses": {
            "database": "Open Database License (ODbL) 1.0",
            "individual_database_contents": "Database Contents License (DbCL) 1.0",
            "software": "BSD 3-Clause",
            "authoritative_local_notice": str((source_root / "LICENSE").resolve()),
            "redistribution_note": "This SQLite database is a transformed/derived database. Preserve attribution and evaluate ODbL share-alike obligations before public redistribution; this manifest is not legal advice."
        },
        "source_files": source_files,
    }


def rows(frame, fields: list[tuple[str, str]]) -> list[tuple[Any, ...]]:
    output = []
    for index, record in frame.sort_index().iterrows():
        output.append(tuple(clean(index) if source == "__index__" else clean(record.get(source))
                            for _, source in fields))
    return output


def build_database(database_path: Path, net: Any) -> dict[str, int]:
    if database_path.exists():
        database_path.unlink()
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(SCHEMA_SQL)
        connection.execute(
            "INSERT INTO networks VALUES (?, ?, ?, ?, ?, ?, ?)",
            (NETWORK_CODE, "SimBench", 0, "MV urban with upstream HV", "urban", "switch-inclusive", float(net.sn_mva)),
        )
        voltage_rows = []
        grouped = net.bus.groupby(["voltLvl", "vn_kv"], dropna=False).size().sort_index()
        for (code, nominal_kv), count in grouped.items():
            voltage_rows.append((NETWORK_CODE, clean(code), clean(nominal_kv), int(count)))
        connection.executemany("INSERT INTO voltage_levels VALUES (?, ?, ?, ?)", voltage_rows)

        specifications = {
            "buses": (net.bus, [
                ("bus_id", "__index__"), ("network_code", "__constant__"), ("name", "name"),
                ("nominal_kv", "vn_kv"), ("bus_type", "type"), ("subnet", "subnet"),
                ("substation", "substation"), ("voltage_level_code", "voltLvl"),
                ("in_service", "in_service"), ("min_voltage_pu", "min_vm_pu"), ("max_voltage_pu", "max_vm_pu")]),
            "lines": (net.line, [
                ("line_id", "__index__"), ("network_code", "__constant__"), ("name", "name"),
                ("from_bus_id", "from_bus"), ("to_bus_id", "to_bus"), ("standard_type", "std_type"),
                ("length_km", "length_km"), ("resistance_ohm_per_km", "r_ohm_per_km"),
                ("reactance_ohm_per_km", "x_ohm_per_km"), ("max_current_ka", "max_i_ka"),
                ("max_loading_percent", "max_loading_percent"), ("voltage_level_code", "voltLvl"),
                ("in_service", "in_service")]),
            "transformers": (net.trafo, [
                ("transformer_id", "__index__"), ("network_code", "__constant__"), ("name", "name"),
                ("hv_bus_id", "hv_bus"), ("lv_bus_id", "lv_bus"), ("rated_power_mva", "sn_mva"),
                ("hv_nominal_kv", "vn_hv_kv"), ("lv_nominal_kv", "vn_lv_kv"),
                ("vector_group", "vector_group"), ("tap_position", "tap_pos"),
                ("on_load_tap_changer", "oltc"), ("in_service", "in_service")]),
            "loads": (net.load, [
                ("load_id", "__index__"), ("network_code", "__constant__"), ("name", "name"),
                ("bus_id", "bus"), ("active_power_mw", "p_mw"), ("reactive_power_mvar", "q_mvar"),
                ("maximum_active_power_mw", "max_p_mw"), ("minimum_active_power_mw", "min_p_mw"),
                ("profile", "profile"), ("voltage_level_code", "voltLvl"), ("in_service", "in_service")]),
            "generators": (net.sgen, [
                ("generator_id", "__index__"), ("network_code", "__constant__"), ("name", "name"),
                ("bus_id", "bus"), ("active_power_mw", "p_mw"), ("reactive_power_mvar", "q_mvar"),
                ("rated_power_mva", "sn_mva"), ("maximum_active_power_mw", "max_p_mw"),
                ("minimum_active_power_mw", "min_p_mw"), ("generator_type", "type"),
                ("physical_type", "phys_type"), ("profile", "profile"),
                ("controllable", "controllable"), ("voltage_level_code", "voltLvl"),
                ("in_service", "in_service")]),
            "switches": (net.switch, [
                ("switch_id", "__index__"), ("network_code", "__constant__"), ("name", "name"),
                ("bus_id", "bus"), ("element_id", "element"), ("element_type", "et"),
                ("switch_type", "type"), ("closed", "closed"),
                ("voltage_level_code", "voltLvl")]),
        }
        counts = {"networks": 1, "voltage_levels": len(voltage_rows)}
        for table, (frame, fields) in specifications.items():
            values = []
            for index, record in frame.sort_index().iterrows():
                row = []
                for _, source in fields:
                    if source == "__index__":
                        value = index
                    elif source == "__constant__":
                        value = NETWORK_CODE
                    else:
                        value = record.get(source)
                    row.append(clean(value))
                values.append(tuple(row))
            placeholders = ",".join("?" for _ in fields)
            connection.executemany(f"INSERT INTO {table} VALUES ({placeholders})", values)
            counts[table] = len(values)
        connection.commit()
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
        if integrity != "ok" or foreign_keys:
            raise RuntimeError(f"SQLite validation failed: integrity={integrity}, foreign_keys={foreign_keys}")
        connection.execute("VACUUM")
        return counts
    finally:
        connection.close()


def questions() -> list[dict[str, Any]]:
    families = {
        "asset_inventory": ("development_candidate", "single_table", [
            ("How many buses are represented in this SimBench network?", "SELECT COUNT(*) AS bus_count FROM buses"),
            ("How many lines are in the network?", "SELECT COUNT(*) AS line_count FROM lines"),
            ("How many transformers are available?", "SELECT COUNT(*) AS transformer_count FROM transformers"),
            ("How many load assets are recorded?", "SELECT COUNT(*) AS load_count FROM loads"),
            ("How many distributed generators are recorded?", "SELECT COUNT(*) AS generator_count FROM generators"),
            ("How many switches are represented?", "SELECT COUNT(*) AS switch_count FROM switches")]),
        "threshold_filter": ("development_candidate", "filter", [
            ("List buses whose nominal voltage is at least 100 kV.", "SELECT bus_id, name, nominal_kv FROM buses WHERE nominal_kv >= 100 ORDER BY bus_id"),
            ("List in-service lines longer than 2 km.", "SELECT line_id, name, length_km FROM lines WHERE in_service = 1 AND length_km > 2 ORDER BY length_km DESC, line_id"),
            ("Which loads have a maximum active power above 1 MW?", "SELECT load_id, name, maximum_active_power_mw FROM loads WHERE maximum_active_power_mw > 1 ORDER BY maximum_active_power_mw DESC, load_id"),
            ("Which generators are controllable?", "SELECT generator_id, name, generator_type FROM generators WHERE controllable = 1 ORDER BY generator_id"),
            ("List all normally open switches.", "SELECT switch_id, name, element_type FROM switches WHERE closed = 0 ORDER BY switch_id"),
            ("List hydro generators in service.", "SELECT generator_id, name, active_power_mw FROM generators WHERE generator_type LIKE '%Hydro%' AND in_service = 1 ORDER BY generator_id")]),
        "asset_aggregation": ("evaluation_candidate", "aggregate", [
            ("What is the total maximum active power of all loads in MW?", "SELECT ROUND(SUM(maximum_active_power_mw), 6) AS total_load_max_mw FROM loads"),
            ("What is the total maximum active power of all distributed generators in MW?", "SELECT ROUND(SUM(maximum_active_power_mw), 6) AS total_generation_max_mw FROM generators"),
            ("What is the average line length in kilometres?", "SELECT ROUND(AVG(length_km), 6) AS average_line_length_km FROM lines"),
            ("What is the total rated transformer capacity in MVA?", "SELECT ROUND(SUM(rated_power_mva), 6) AS total_transformer_mva FROM transformers"),
            ("How many buses belong to each nominal voltage level?", "SELECT nominal_kv, COUNT(*) AS bus_count FROM buses GROUP BY nominal_kv ORDER BY nominal_kv DESC"),
            ("How many open and closed switches are there?", "SELECT closed, COUNT(*) AS switch_count FROM switches GROUP BY closed ORDER BY closed")]),
        "cross_asset_join": ("evaluation_candidate", "join", [
            ("Show the five loads with the largest maximum active power and their bus names.", "SELECT l.load_id, l.name AS load_name, b.name AS bus_name, l.maximum_active_power_mw FROM loads l JOIN buses b ON b.bus_id = l.bus_id ORDER BY l.maximum_active_power_mw DESC, l.load_id LIMIT 5"),
            ("Show each hydro generator together with its connected bus and nominal voltage.", "SELECT g.name AS generator_name, b.name AS bus_name, b.nominal_kv FROM generators g JOIN buses b ON b.bus_id = g.bus_id WHERE g.generator_type LIKE '%Hydro%' ORDER BY g.generator_id"),
            ("Show transformer names with their high- and low-voltage bus names.", "SELECT t.name AS transformer_name, hb.name AS high_voltage_bus, lb.name AS low_voltage_bus FROM transformers t JOIN buses hb ON hb.bus_id = t.hv_bus_id JOIN buses lb ON lb.bus_id = t.lv_bus_id ORDER BY t.transformer_id"),
            ("Show the first five lines with their from-bus and to-bus names.", "SELECT l.line_id, l.name AS line_name, fb.name AS from_bus, tb.name AS to_bus FROM lines l JOIN buses fb ON fb.bus_id = l.from_bus_id JOIN buses tb ON tb.bus_id = l.to_bus_id ORDER BY l.line_id LIMIT 5"),
            ("Count loads by the nominal voltage of their connected bus.", "SELECT b.nominal_kv, COUNT(*) AS load_count FROM loads l JOIN buses b ON b.bus_id = l.bus_id GROUP BY b.nominal_kv ORDER BY b.nominal_kv DESC"),
            ("Count generators at each connected bus and show only buses with more than one generator.", "SELECT b.bus_id, b.name, COUNT(*) AS generator_count FROM generators g JOIN buses b ON b.bus_id = g.bus_id GROUP BY b.bus_id, b.name HAVING COUNT(*) > 1 ORDER BY generator_count DESC, b.bus_id")]),
        "ranked_assets": ("evaluation_candidate", "top_k", [
            ("Which five loads have the highest maximum active power?", "SELECT load_id, name, maximum_active_power_mw FROM loads ORDER BY maximum_active_power_mw DESC, load_id LIMIT 5"),
            ("Which five generators have the highest maximum active power?", "SELECT generator_id, name, maximum_active_power_mw FROM generators ORDER BY maximum_active_power_mw DESC, generator_id LIMIT 5"),
            ("Which five lines are the longest?", "SELECT line_id, name, length_km FROM lines ORDER BY length_km DESC, line_id LIMIT 5"),
            ("Which transformer has the largest rated power?", "SELECT transformer_id, name, rated_power_mva FROM transformers ORDER BY rated_power_mva DESC, transformer_id LIMIT 1"),
            ("Which five load profiles occur most often?", "SELECT profile, COUNT(*) AS load_count FROM loads GROUP BY profile ORDER BY load_count DESC, profile LIMIT 5"),
            ("Which five generator profiles occur most often?", "SELECT profile, COUNT(*) AS generator_count FROM generators GROUP BY profile ORDER BY generator_count DESC, profile LIMIT 5")]),
        "network_topology": ("evaluation_candidate", "topology", [
            ("Which five buses have the highest line degree?", "WITH endpoints AS (SELECT from_bus_id AS bus_id FROM lines UNION ALL SELECT to_bus_id AS bus_id FROM lines) SELECT b.bus_id, b.name, COUNT(*) AS line_degree FROM endpoints e JOIN buses b ON b.bus_id = e.bus_id GROUP BY b.bus_id, b.name ORDER BY line_degree DESC, b.bus_id LIMIT 5"),
            ("How many in-service line connections touch each of the five highest-degree buses?", "WITH endpoints AS (SELECT from_bus_id AS bus_id FROM lines WHERE in_service = 1 UNION ALL SELECT to_bus_id AS bus_id FROM lines WHERE in_service = 1) SELECT b.bus_id, b.name, COUNT(*) AS in_service_degree FROM endpoints e JOIN buses b ON b.bus_id = e.bus_id GROUP BY b.bus_id, b.name ORDER BY in_service_degree DESC, b.bus_id LIMIT 5"),
            ("Which buses have no incident line?", "SELECT b.bus_id, b.name FROM buses b LEFT JOIN lines l1 ON l1.from_bus_id = b.bus_id LEFT JOIN lines l2 ON l2.to_bus_id = b.bus_id WHERE l1.line_id IS NULL AND l2.line_id IS NULL ORDER BY b.bus_id"),
            ("Show open switches that are attached to line elements, including the line name.", "SELECT s.switch_id, s.name AS switch_name, l.line_id, l.name AS line_name FROM switches s JOIN lines l ON s.element_type = 'l' AND l.line_id = s.element_id WHERE s.closed = 0 ORDER BY s.switch_id"),
            ("Which lines connect buses with different nominal voltages?", "SELECT l.line_id, l.name, fb.nominal_kv AS from_kv, tb.nominal_kv AS to_kv FROM lines l JOIN buses fb ON fb.bus_id = l.from_bus_id JOIN buses tb ON tb.bus_id = l.to_bus_id WHERE fb.nominal_kv <> tb.nominal_kv ORDER BY l.line_id"),
            ("For each transformer, show the nominal voltage transition between its connected buses.", "SELECT t.transformer_id, t.name, hb.nominal_kv AS high_bus_kv, lb.nominal_kv AS low_bus_kv FROM transformers t JOIN buses hb ON hb.bus_id = t.hv_bus_id JOIN buses lb ON lb.bus_id = t.lv_bus_id ORDER BY t.transformer_id")])
    }
    records = []
    number = 1
    for family, (split, query_class, pairs) in families.items():
        for template_index, (natural_language, sql) in enumerate(pairs, 1):
            records.append({
                "question_id": f"SB-AUTO-{number:03d}",
                "natural_language": natural_language,
                "gold_sql": sql,
                "query_class": query_class,
                "template_family_id": family,
                "template_index": template_index,
                "split": split,
                "provenance_label": STATUS,
                "human_gold": False,
                "sealed": False,
                "network_code": NETWORK_CODE,
            })
            number += 1
    return records


def normalized_result(cursor: sqlite3.Cursor) -> dict[str, Any]:
    columns = [item[0] for item in cursor.description] if cursor.description else []
    output_rows = [[clean(value) for value in row] for row in cursor.fetchall()]
    payload = {"columns": columns, "rows": output_rows}
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return {**payload, "row_count": len(output_rows), "result_sha256": hashlib.sha256(encoded).hexdigest()}


def execute_questions(database_path: Path, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    connection = sqlite3.connect(f"file:{database_path.resolve()}?mode=ro", uri=True)
    try:
        results = []
        for record in records:
            sql = record["gold_sql"].strip()
            if not sql.upper().startswith(("SELECT", "WITH")) or ";" in sql:
                raise ValueError(f"Unsafe/non-single-statement SQL for {record['question_id']}")
            result = normalized_result(connection.execute(sql))
            results.append({"question_id": record["question_id"], **result})
        return results
    finally:
        connection.close()


def write_questions(path: Path, records: list[dict[str, Any]]) -> None:
    fields = list(records[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records), encoding="utf-8")


def field_description(table: str, column: str) -> str:
    special = {
        "network_code": "Stable SimBench network identifier.", "voltage_level_code": "SimBench categorical voltage-level code.",
        "nominal_kv": "Nominal bus voltage in kilovolts.", "from_bus_id": "Origin bus foreign key.",
        "to_bus_id": "Destination bus foreign key.", "bus_id": "Connected bus identifier/foreign key.",
        "element_id": "Identifier of the element referenced by the polymorphic switch element_type.",
        "element_type": "SimBench switch target code: l=line, b=bus, t=transformer.",
        "in_service": "Boolean service-state flag encoded as 0/1.", "closed": "Boolean switch state encoded as 0/1.",
        "controllable": "Boolean generator controllability flag encoded as 0/1.",
    }
    return special.get(column, column.replace("_", " ").capitalize() + f" for {table}.")


def write_field_dictionary(database_path: Path, path: Path) -> None:
    source_tables = {"networks": "derived", "voltage_levels": "derived from bus", "buses": "bus", "lines": "line",
                     "transformers": "trafo", "loads": "load", "generators": "sgen", "switches": "switch"}
    connection = sqlite3.connect(database_path)
    try:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["table", "column", "sqlite_type", "not_null", "primary_key", "foreign_key", "source_table", "description"])
            writer.writeheader()
            for table in source_tables:
                foreign = {row[3]: f"{row[2]}.{row[4]}" for row in connection.execute(f"PRAGMA foreign_key_list({table})")}
                for row in connection.execute(f"PRAGMA table_info({table})"):
                    writer.writerow({
                        "table": table, "column": row[1], "sqlite_type": row[2], "not_null": row[3],
                        "primary_key": row[5], "foreign_key": foreign.get(row[1], ""),
                        "source_table": source_tables[table], "description": field_description(table, row[1]),
                    })
    finally:
        connection.close()


def artifact_hashes(output_dir: Path, names: list[str]) -> dict[str, Any]:
    return {
        "manifest_version": "1.0",
        "artifacts": [{"path": name, "bytes": (output_dir / name).stat().st_size,
                       "sha256": sha256_file(output_dir / name)} for name in sorted(names)],
    }


def parse_args() -> argparse.Namespace:
    workspace = Path(__file__).resolve().parents[5]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=workspace / "data/public_datasets/grid_cases/simbench")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if not (source_root / "LICENSE").is_file():
        raise FileNotFoundError(f"SimBench source/LICENSE not found at {source_root}")
    simbench = load_simbench(source_root)
    net = simbench.get_simbench_net(NETWORK_CODE)

    schema_path = output_dir / "schema.sql"
    schema_path.write_text(SCHEMA_SQL, encoding="utf-8")
    manifest = source_manifest(source_root, simbench)
    json_dump(output_dir / "source_manifest.json", manifest)
    license_text = (source_root / "LICENSE").read_text(encoding="utf-8")
    (output_dir / "UPSTREAM_LICENSE.txt").write_text(license_text, encoding="utf-8")

    database_path = output_dir / "simbench_mv_urban.sqlite"
    table_counts = build_database(database_path, net)
    candidate_questions = questions()
    write_questions(output_dir / "questions_auto_candidate.csv", candidate_questions)
    gold_results = execute_questions(database_path, candidate_questions)
    write_jsonl(output_dir / "gold_execution_results.jsonl", gold_results)
    write_field_dictionary(database_path, output_dir / "field_dictionary.csv")

    family_splits: dict[str, str] = {}
    for item in candidate_questions:
        family = item["template_family_id"]
        if family in family_splits and family_splits[family] != item["split"]:
            raise RuntimeError(f"Template family leaked across splits: {family}")
        family_splits[family] = item["split"]
    data_card = {
        "schema_version": SCHEMA_VERSION,
        "network_code": NETWORK_CODE,
        "table_counts": table_counts,
        "question_count": len(candidate_questions),
        "query_class_counts": {name: sum(q["query_class"] == name for q in candidate_questions)
                               for name in sorted({q["query_class"] for q in candidate_questions})},
        "template_family_splits": family_splits,
        "label_status": STATUS,
        "human_gold": False,
        "sealed": False,
        "limitations": [
            "Questions and SQL were generated deterministically by code and have not received independent human domain review.",
            "The set is a pilot for pipeline/data feasibility and must not be described as a human-gold or sealed benchmark.",
            "One SimBench urban MV network does not establish cross-network generalization.",
        ],
    }
    json_dump(output_dir / "data_card.json", data_card)
    hashed = ["schema.sql", "source_manifest.json", "UPSTREAM_LICENSE.txt", "simbench_mv_urban.sqlite",
              "questions_auto_candidate.csv", "gold_execution_results.jsonl", "field_dictionary.csv", "data_card.json"]
    json_dump(output_dir / "artifact_hashes.json", artifact_hashes(output_dir, hashed))
    print(json.dumps({"status": "PASS", "network": NETWORK_CODE, "tables": table_counts,
                      "questions": len(candidate_questions), "database_sha256": sha256_file(database_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
