#!/usr/bin/env python3
"""Scale GridDB-Maintenance-v2 to a x10 variant with distractor tables (P1-2).

Builds data/griddb_maintenance_v2_x10 from the frozen v0.1 dataset:

  * every entity/transaction table (locations, technicians, assets,
    work_orders, maintenance_logs, sensor_readings, grid_topology) is scaled
    x10 by deterministic block replication: copy k (k = 1..9) shifts every
    primary key by k * BLOCK, remaps foreign keys into the same block, and
    renames unique name fields following the original naming conventions
    (asset prefixes such as TX-/BR-/LN-, "Firstname Lastname" technicians,
    "<Direction> <Noun>" locations). Value vocabularies (statuses,
    priorities, regions, fault codes, sensor types, asset_types) are kept
    identical so the question set remains answerable.
  * two distractor tables (vegetation_inspections, spare_parts_inventory)
    are added with plausible rows; no question references them, so they only
    enlarge the schema/value space a Text-to-SQL system must ignore.
  * questions.jsonl and splits.json are copied unchanged; gold SQL is
    re-executed against the new database, and the packaged evaluator's
    validate_dataset must report zero errors, otherwise the script fails.

Because name-filtered questions (e.g. technician or asset names) still match
only original-block rows, the scaled database increases the distractor value
space roughly tenfold while keeping every gold query executable.

Re-running C2/C4/C5 on the expanded dataset requires a live model endpoint
(KRILL_API_KEY or a second model; see README_EXPANSION.md). This script only
builds the data.

Usage:
  python expand_dataset.py [--factor 10] [--output-dir ../../data/griddb_maintenance_v2_x10]
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import sqlite3
import sys
from pathlib import Path

EXPERIMENT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = EXPERIMENT_DIR.parents[1]
SRC_DATA = SOURCE_DIR / "data" / "griddb_maintenance_v2_v0_1"

sys.path.insert(0, str(EXPERIMENT_DIR.parent / "evaluator"))
from evaluator import validate_dataset  # noqa: E402

BLOCK = 100000  # id offset per replication block; far above any original id
SEED = 20260716

FIRST_NAMES = ["Noah", "Lena", "Omar", "Ivy", "Ruth", "Kai", "Mira", "Theo", "Zara", "Eli",
               "Nina", "Owen", "Pia", "Rex", "Sana", "Tom", "Uma", "Vik", "Wren", "Yuri"]
LAST_NAMES = ["Novak", "Iqbal", "Fonseca", "Grant", "Hale", "Ibsen", "Joshi", "Kerr", "Lund",
              "Moss", "Nunez", "Oduya", "Pratt", "Quinn", "Rhee", "Sato", "Tran", "Ueda", "Vance", "Wolfe"]
LOCATION_NOUNS = ["Basin", "Bluff", "Canyon", "Crossing", "Delta", "Flats", "Gate", "Glen",
                  "Harbor", "Junction", "Mesa", "Pass", "Point", "Prairie", "Summit", "Terrace", "Vale", "Yard"]
REGIONS = ["North", "South", "East", "West", "Central"]

DISTRACTOR_SCHEMA = """
CREATE TABLE vegetation_inspections (
    inspection_id INTEGER PRIMARY KEY,
    location_id INTEGER NOT NULL REFERENCES locations(location_id),
    inspection_date TEXT NOT NULL,
    encroachment_level TEXT NOT NULL,
    inspector_name TEXT NOT NULL,
    cleared INTEGER NOT NULL
);

CREATE TABLE spare_parts_inventory (
    part_id INTEGER PRIMARY KEY,
    part_name TEXT NOT NULL,
    asset_type_id INTEGER NOT NULL REFERENCES asset_types(asset_type_id),
    quantity_on_hand INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    warehouse_region TEXT NOT NULL
);
"""

PART_NAMES = ["bushing kit", "SF6 canister", "arc chute", "trip coil", "CT clamp", "relay card",
              "oil filter", "gasket set", "fan motor", "tap changer contact", "surge arrester", "fuse link"]
ENCROACHMENT = ["low", "moderate", "high"]


def fetch_all(conn: sqlite3.Connection, table: str) -> list[tuple]:
    return conn.execute(f"SELECT * FROM {table}").fetchall()


def replicate(args: argparse.Namespace) -> Path:
    rng = random.Random(SEED)
    out_dir = Path(args.output_dir).resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    # 1. schema: original schema + distractor tables
    schema_sql = (SRC_DATA / "schema.sql").read_text(encoding="utf-8")
    extended_schema = schema_sql.rstrip() + "\n\nDROP TABLE IF EXISTS vegetation_inspections;\nDROP TABLE IF EXISTS spare_parts_inventory;\n" + DISTRACTOR_SCHEMA
    (out_dir / "schema.sql").write_text(extended_schema, encoding="utf-8")

    src = sqlite3.connect(SRC_DATA / "database.sqlite")
    dst = sqlite3.connect(out_dir / "database.sqlite")
    dst.executescript(extended_schema)

    asset_prefix = {}  # asset_type_id -> name prefix, derived from original data
    for asset_id, name, type_id, *_ in src.execute("SELECT asset_id, asset_name, asset_type_id FROM assets"):
        asset_prefix.setdefault(type_id, name.split("-", 1)[0])

    tables = {
        "asset_types": fetch_all(src, "asset_types"),
        "locations": fetch_all(src, "locations"),
        "assets": fetch_all(src, "assets"),
        "technicians": fetch_all(src, "technicians"),
        "work_orders": fetch_all(src, "work_orders"),
        "maintenance_logs": fetch_all(src, "maintenance_logs"),
        "sensor_readings": fetch_all(src, "sensor_readings"),
        "grid_topology": fetch_all(src, "grid_topology"),
    }

    def insert(table: str, rows: list[tuple]) -> None:
        if not rows:
            return
        placeholders = ",".join("?" * len(rows[0]))
        dst.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)

    # asset_types: vocabulary table, kept identical (questions filter on type names)
    insert("asset_types", tables["asset_types"])

    used_names: set[str] = set()

    def fresh_person() -> str:
        while True:
            name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
            if name not in used_names:
                used_names.add(name)
                return name

    used_locations: set[str] = set()

    def fresh_location() -> str:
        while True:
            name = f"{rng.choice(REGIONS)} {rng.choice(LOCATION_NOUNS)} {rng.randint(2, 99)}"
            if name not in used_locations:
                used_locations.add(name)
                return name

    for block in range(args.factor):
        off = block * BLOCK
        is_original = block == 0

        loc_rows = []
        for (lid, lname, region, lat, lon, crit) in tables["locations"]:
            loc_rows.append((
                lid + off,
                lname if is_original else fresh_location(),
                region,
                round(lat + (0 if is_original else rng.uniform(-0.5, 0.5)), 2),
                round(lon + (0 if is_original else rng.uniform(-0.5, 0.5)), 2),
                crit,
            ))
        insert("locations", loc_rows)

        tech_rows = []
        for (tid, tname, spec, region, active) in tables["technicians"]:
            tech_rows.append((tid + off, tname if is_original else fresh_person(), spec, region, active))
        insert("technicians", tech_rows)

        asset_rows = []
        for (aid, aname, type_id, lid, install, status, cap) in tables["assets"]:
            if is_original:
                new_name = aname
            else:
                prefix = asset_prefix.get(type_id, "AS")
                new_name = f"{prefix}-{block}{aid:02d}"  # e.g. TX-101 for block 1, asset 1
            asset_rows.append((aid + off, new_name, type_id, lid + off, install, status, cap))
        insert("assets", asset_rows)

        wo_rows = []
        for (wid, aid, tid, prio, status, sched, comp, fault) in tables["work_orders"]:
            wo_rows.append((wid + off, aid + off, tid + off, prio, status, sched, comp, fault))
        insert("work_orders", wo_rows)

        log_rows = []
        for (lgid, wid, tid, action, start, end, notes, cost) in tables["maintenance_logs"]:
            log_rows.append((lgid + off, wid + off, tid + off, action, start, end, notes,
                             cost if is_original else round(cost * rng.uniform(0.8, 1.2), 2)))
        insert("maintenance_logs", log_rows)

        sr_rows = []
        for (rid, aid, rtime, stype, val, unit, alarm) in tables["sensor_readings"]:
            sr_rows.append((rid + off, aid + off, rtime, stype,
                            val if is_original else round(val * rng.uniform(0.9, 1.1), 1), unit, alarm))
        insert("sensor_readings", sr_rows)

        topo_rows = []
        for (eid, up, down, ctype, sw) in tables["grid_topology"]:
            topo_rows.append((eid + off, up + off, down + off, ctype, sw))
        insert("grid_topology", topo_rows)

    # distractor rows
    all_location_ids = [r[0] for r in dst.execute("SELECT location_id FROM locations")]
    veg_rows = []
    for i in range(1, 61):
        veg_rows.append((
            i,
            rng.choice(all_location_ids),
            f"2024-{rng.randint(1, 6):02d}-{rng.randint(1, 28):02d}",
            rng.choice(ENCROACHMENT),
            fresh_person(),
            rng.randint(0, 1),
        ))
    insert("vegetation_inspections", veg_rows)

    type_ids = [r[0] for r in tables["asset_types"]]
    part_rows = []
    for i, part in enumerate(PART_NAMES, start=1):
        part_rows.append((i, part, rng.choice(type_ids), rng.randint(0, 40),
                          round(rng.uniform(15, 900), 2), rng.choice(REGIONS)))
    insert("spare_parts_inventory", part_rows)

    dst.commit()
    src.close()
    dst.close()

    # 2. questions/splits/protocol copied unchanged
    for name in ["questions.jsonl", "splits.json", "annotation_protocol.md"]:
        if (SRC_DATA / name).exists():
            shutil.copy2(SRC_DATA / name, out_dir / name)

    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--factor", type=int, default=10)
    parser.add_argument("--output-dir", default=str(SOURCE_DIR / "data" / "griddb_maintenance_v2_x10"))
    args = parser.parse_args()

    out_dir = replicate(args)

    conn = sqlite3.connect(out_dir / "database.sqlite")
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for (t,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")}
    conn.close()
    print("table row counts:", json.dumps(counts, indent=2, sort_keys=True))

    result = validate_dataset(out_dir / "database.sqlite", out_dir / "questions.jsonl")
    print(f"validate_dataset: {result['question_count']} questions, {result['error_count']} errors")
    if result["error_count"]:
        for err in result["errors"][:10]:
            print("  ", err)
        return 1

    manifest = {
        "source": str(SRC_DATA),
        "factor": args.factor,
        "seed": SEED,
        "distractor_tables": ["vegetation_inspections", "spare_parts_inventory"],
        "row_counts": counts,
        "gold_validation_errors": result["error_count"],
    }
    (out_dir / "expansion_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: wrote {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
