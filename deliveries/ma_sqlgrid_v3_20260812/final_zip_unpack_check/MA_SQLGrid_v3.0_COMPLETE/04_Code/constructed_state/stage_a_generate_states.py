#!/usr/bin/env python3
"""Query-blind Stage A: generate database states from schema/base rows only.

The executable intentionally has only four filesystem inputs/outputs on its
CLI: base SQLite, operator policy, output directory, and trace directory.  It
does not import the scorer and has no option for benchmark records or ledgers.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import re
import shutil
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

TABLES = ["asset_types", "locations", "technicians", "assets", "work_orders", "maintenance_logs", "sensor_readings", "grid_topology"]
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(.*)$")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def info(conn: sqlite3.Connection) -> dict[str, Any]:
    out = {}
    for table in TABLES:
        cols = conn.execute(f'PRAGMA table_info("{table}")').fetchall()
        fks = conn.execute(f'PRAGMA foreign_key_list("{table}")').fetchall()
        out[table] = {
            "columns": [c[1] for c in cols], "types": {c[1]: (c[2] or "").upper() for c in cols},
            "pk": next(c[1] for c in cols if c[5] == 1),
            "fks": {r[3]: {"table": r[2], "column": r[4]} for r in fks},
        }
    return out


def base_rows(conn: sqlite3.Connection, meta: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    return {t: [dict(zip(meta[t]["columns"], r)) for r in conn.execute(f'SELECT * FROM "{t}" ORDER BY "{meta[t]["pk"]}"')] for t in TABLES}


class Builder:
    def __init__(self, conn: sqlite3.Connection, meta: dict[str, Any], original: dict[str, list[dict[str, Any]]], state: str, trace_path: Path):
        self.conn, self.meta, self.original, self.state = conn, meta, original, state
        self.trace = trace_path.open("w", encoding="utf-8", newline="\n")
        self.count = 0
        self.next_id = {t: max(r[meta[t]["pk"]] for r in original[t]) + 1 for t in TABLES}

    def close(self) -> None:
        self.trace.close()

    def new_id(self, table: str) -> int:
        value = self.next_id[table]; self.next_id[table] += 1; return value

    def insert(self, table: str, row: dict[str, Any], operator: str) -> int:
        cols = self.meta[table]["columns"]
        missing = [c for c in cols if c not in row]
        if missing:
            raise ValueError(f"{table} missing {missing}")
        self.conn.execute(f'INSERT INTO "{table}" ({",".join(chr(34)+c+chr(34) for c in cols)}) VALUES ({",".join("?" for _ in cols)})', [row[c] for c in cols])
        self.count += 1
        self.trace.write(json.dumps({"sequence": self.count, "state": self.state, "operator": operator, "table": table, "row": row}, ensure_ascii=False, sort_keys=True) + "\n")
        return row[self.meta[table]["pk"]]


def copy_base(base: Path, target: Path) -> None:
    shutil.copyfile(base, target)


def rebuild_permuted(base: Path, target: Path, seed: int) -> None:
    src = sqlite3.connect(base)
    try:
        schema = [(r[0], r[1]) for r in src.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        m = info(src); rows = base_rows(src, m)
    finally:
        src.close()
    out = sqlite3.connect(target)
    try:
        out.execute("PRAGMA foreign_keys=OFF")
        for _name, ddl in schema: out.execute(ddl)
        rng = random.Random(seed)
        for table in TABLES:
            rr = list(rows[table]); rng.shuffle(rr); cols = m[table]["columns"]
            for row in rr:
                out.execute(f'INSERT INTO "{table}" ({",".join(chr(34)+c+chr(34) for c in cols)}) VALUES ({",".join("?" for _ in cols)})', [row[c] for c in cols])
        out.commit(); out.execute("VACUUM")
    finally:
        out.close()


def transform_date(value: str, days: int) -> str:
    m = DATE_RE.match(value)
    if not m: return value
    try: return (datetime.strptime(m.group(1), "%Y-%m-%d") + timedelta(days=days)).strftime("%Y-%m-%d") + m.group(2)
    except ValueError: return value


def append_cohort(b: Builder, mode: str, cohort: int) -> None:
    maps: dict[str, dict[Any, Any]] = {t: {} for t in TABLES}
    for table in TABLES:
        pk = b.meta[table]["pk"]
        for row in b.original[table]: maps[table][row[pk]] = b.new_id(table)
    rotate = mode in {"rotate", "combined"}; rewire = mode in {"rewire", "combined"}; shift = mode in {"shift", "combined"}
    for table in TABLES:
        meta, rows = b.meta[table], b.original[table]
        for i, source in enumerate(rows):
            attr_source = rows[(i + 1) % len(rows)] if rotate and len(rows) > 1 else source
            row = {}
            for col in meta["columns"]:
                if col == meta["pk"]: value = maps[table][source[col]]
                elif col in meta["fks"]:
                    ref = meta["fks"][col]["table"]; key = source[col]; refkeys = list(maps[ref])
                    if rewire and len(refkeys) > 1:
                        pos = refkeys.index(key); step = 1 + sum(map(ord, table + col)) % (len(refkeys) - 1); key = refkeys[(pos + step) % len(refkeys)]
                    value = maps[ref][key]
                else:
                    value = attr_source[col]
                    if shift and isinstance(value, float): value = round(value * (1 + .125 * cohort) + .25 * cohort, 6)
                    elif shift and isinstance(value, int) and col not in {"active", "alarm_flag"}: value += 3 * cohort
                    elif shift and isinstance(value, str) and DATE_RE.match(value): value = transform_date(value, 37 * cohort)
                row[col] = value
            b.insert(table, row, f"cohort:{mode}:{cohort}")


def domains(original: dict[str, list[dict[str, Any]]], table: str, col: str) -> list[Any]:
    return sorted({r[col] for r in original[table] if r[col] is not None}, key=lambda x: (str(type(x)), str(x)))


def categorical_cover(b: Builder, prefix: str, policy: dict[str, Any]) -> None:
    o = b.original
    type_ids = {}
    for vals in itertools.product(domains(o, "asset_types", "type_name"), domains(o, "asset_types", "voltage_class"), domains(o, "asset_types", "manufacturer")):
        rid = b.new_id("asset_types"); b.insert("asset_types", {"asset_type_id": rid, "type_name": vals[0], "voltage_class": vals[1], "manufacturer": vals[2], "expected_lifetime_years": 20 + rid % 21}, "categorical_cover"); type_ids.setdefault(vals[0], rid)
    loc_ids = {}
    for region, crit in itertools.product(domains(o, "locations", "region"), domains(o, "locations", "criticality")):
        rid = b.new_id("locations"); b.insert("locations", {"location_id": rid, "location_name": f"{prefix}_LOC_{rid}", "region": region, "latitude": 30 + rid % 30 + .125, "longitude": -120 + rid % 40 + .125, "criticality": crit}, "categorical_cover"); loc_ids[(region, crit)] = rid
    tech_ids = []
    for spec, region, active in itertools.product(domains(o, "technicians", "specialty"), domains(o, "technicians", "home_region"), domains(o, "technicians", "active")):
        rid = b.new_id("technicians"); b.insert("technicians", {"technician_id": rid, "technician_name": f"{prefix}_TECH_{rid}", "specialty": spec, "home_region": region, "active": active}, "categorical_cover"); tech_ids.append(rid)
    asset_ids = []
    status_d = domains(o, "assets", "status")
    for type_name, (region, crit), status in itertools.product(type_ids, loc_ids, status_d):
        rid = b.new_id("assets"); b.insert("assets", {"asset_id": rid, "asset_name": f"{prefix}_ASSET_{rid}", "asset_type_id": type_ids[type_name], "location_id": loc_ids[(region, crit)], "install_date": f"20{10 + rid % 15:02d}-06-15", "status": status, "capacity_mw": 1.0 + rid % 500 + .125}, "categorical_cover"); asset_ids.append(rid)
    priorities = domains(o, "work_orders", "priority")
    statuses = sorted(set(domains(o, "work_orders", "status") + policy.get("schema_lifecycle_sentinels", {}).get("work_orders.status", [])))
    faults = domains(o, "work_orders", "fault_code")
    wo_ids = []
    for i, vals in enumerate(itertools.product(priorities, statuses, faults)):
        rid = b.new_id("work_orders"); done = None if vals[1] != "completed" else f"2024-{1 + i % 12:02d}-{1 + i % 27:02d}"
        b.insert("work_orders", {"work_order_id": rid, "asset_id": asset_ids[i % len(asset_ids)], "assigned_technician_id": tech_ids[i % len(tech_ids)], "priority": vals[0], "status": vals[1], "scheduled_date": f"2024-{1 + i % 12:02d}-{1 + (i * 3) % 27:02d}", "completed_date": done, "fault_code": vals[2]}, "categorical_cover"); wo_ids.append(rid)
    actions = domains(o, "maintenance_logs", "action_type")
    for i, wid in enumerate(wo_ids):
        rid = b.new_id("maintenance_logs"); b.insert("maintenance_logs", {"log_id": rid, "work_order_id": wid, "technician_id": tech_ids[i % len(tech_ids)], "action_type": actions[i % len(actions)], "started_at": "2024-06-01 08:00", "ended_at": "2024-06-01 10:00", "notes": f"{prefix} categorical witness", "parts_cost": 10.125 + i}, "categorical_cover")
    stypes = domains(o, "sensor_readings", "sensor_type"); units = domains(o, "sensor_readings", "unit"); alarms = domains(o, "sensor_readings", "alarm_flag")
    # Pairwise type x unit x alarm coverage, spread across every synthetic asset.
    for i, (stype, unit, alarm) in enumerate(itertools.product(stypes, units, alarms)):
        for aid in asset_ids[i::max(1, len(stypes) * len(units) * len(alarms))] or [asset_ids[i % len(asset_ids)]]:
            rid = b.new_id("sensor_readings"); b.insert("sensor_readings", {"reading_id": rid, "asset_id": aid, "reading_time": f"2024-07-{1 + i % 27:02d} 00:00", "sensor_type": stype, "reading_value": 1.125 + i, "unit": unit, "alarm_flag": alarm}, "categorical_cover")


def boundary_state(b: Builder, policy: dict[str, Any]) -> None:
    # Six coherent cohorts apply min/min/mid/max/max+epsilon/tie points to every numeric/date field.
    points = policy["boundary_policy"]["numeric_points"]
    maps_all = []
    for ci, point in enumerate(points, 1):
        maps = {t: {r[b.meta[t]["pk"]]: b.new_id(t) for r in b.original[t]} for t in TABLES}; maps_all.append(maps)
        for table in TABLES:
            meta, rows = b.meta[table], b.original[table]
            profiles = {}
            for col in meta["columns"]:
                if col == meta["pk"] or col in meta["fks"] or col in {"active", "alarm_flag"}: continue
                vals = [r[col] for r in rows if r[col] is not None]
                if vals and all(isinstance(v, (int, float)) for v in vals): profiles[col] = (min(vals), max(vals), "num")
                elif vals and all(isinstance(v, str) and DATE_RE.match(v) for v in vals): profiles[col] = (min(vals), max(vals), "date")
            for source in rows:
                row = {}
                for col in meta["columns"]:
                    if col == meta["pk"]: value = maps[table][source[col]]
                    elif col in meta["fks"]: value = maps[meta["fks"][col]["table"]][source[col]]
                    elif col in profiles:
                        lo, hi, kind = profiles[col]
                        if kind == "date":
                            values = [transform_date(lo, -37), lo, transform_date(lo, (datetime.strptime(hi[:10], '%Y-%m-%d') - datetime.strptime(lo[:10], '%Y-%m-%d')).days // 2), hi, transform_date(hi, 37), hi]
                        else:
                            eps = 1 if isinstance(lo, int) and isinstance(hi, int) else .125
                            values = [lo - eps, lo, (lo + hi) / 2, hi, hi + eps, hi]
                        value = values[ci - 1]
                    else: value = source[col]
                    row[col] = value
                b.insert(table, row, f"boundary:{point}")


def dense_calendar_boundaries(b: Builder) -> None:
    """Uniform half-day witnesses over the observed work-order calendar envelope."""
    dates = []
    for row in b.original["work_orders"]:
        for col in ("scheduled_date", "completed_date"):
            if row[col] and DATE_RE.match(row[col]): dates.append(datetime.strptime(row[col][:10], "%Y-%m-%d"))
    start, end = min(dates) - timedelta(days=37), max(dates) + timedelta(days=37)
    templates = b.original["work_orders"]
    day = start; i = 0
    while day <= end:
        source = templates[i % len(templates)]; rid = b.new_id("work_orders")
        scheduled = day.strftime("%Y-%m-%d") + " 12:00:00"
        completed = None if source["completed_date"] is None else (day + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
        row = dict(source); row.update({"work_order_id":rid,"scheduled_date":scheduled,"completed_date":completed})
        b.insert("work_orders", row, "dense_calendar_half_day_grid"); day += timedelta(days=1); i += 1


def null_witnesses(b: Builder) -> None:
    tech = b.original["technicians"][0]["technician_id"]
    for i, asset in enumerate(b.original["assets"]):
        common = {"asset_id": asset["asset_id"], "assigned_technician_id": tech, "priority": "medium", "status": "completed", "scheduled_date": "2024-06-15", "fault_code": "INSPECT"}
        for done in [None, "2024-06-16"]:
            rid = b.new_id("work_orders"); b.insert("work_orders", {"work_order_id": rid, **common, "completed_date": done}, "null_witness")


def relationship_cover(b: Builder, prefix: str) -> None:
    o = b.original; base_type = o["asset_types"][0]["asset_type_id"]; base_loc = o["locations"][0]["location_id"]
    # Isolated active technicians cover every schema-derived specialty x region pair.
    for spec, region in itertools.product(domains(o, "technicians", "specialty"), domains(o, "technicians", "home_region")):
        rid = b.new_id("technicians"); b.insert("technicians", {"technician_id": rid, "technician_name": f"{prefix}_ISOLATED_TECH_{rid}", "specialty": spec, "home_region": region, "active": 1}, "anti_join_isolated_technician")
    # Isolated assets cover type x region x status and deliberately have no children.
    type_by_name = {r["type_name"]: r["asset_type_id"] for r in o["asset_types"]}; loc_by_region = {r["region"]: r["location_id"] for r in o["locations"]}
    for tname, region, status in itertools.product(type_by_name, loc_by_region, domains(o, "assets", "status")):
        rid = b.new_id("assets"); b.insert("assets", {"asset_id": rid, "asset_name": f"{prefix}_ISOLATED_ASSET_{rid}", "asset_type_id": type_by_name[tname], "location_id": loc_by_region[region], "install_date": "2024-01-01", "status": status, "capacity_mw": 77.125}, "anti_join_isolated_asset")
    # Every original asset receives both child/counter-child categories and all sensor type/alarm pairs.
    tech = o["technicians"][0]["technician_id"]
    for ai, asset in enumerate(o["assets"]):
        for status in domains(o, "work_orders", "status"):
            rid = b.new_id("work_orders"); b.insert("work_orders", {"work_order_id": rid, "asset_id": asset["asset_id"], "assigned_technician_id": tech, "priority": domains(o, "work_orders", "priority")[ai % 3], "status": status, "scheduled_date": "2024-09-15", "completed_date": "2024-09-16" if status == "completed" else None, "fault_code": domains(o, "work_orders", "fault_code")[ai % len(domains(o, "work_orders", "fault_code"))]}, "child_for_every_asset")
        for stype, alarm in itertools.product(domains(o, "sensor_readings", "sensor_type"), domains(o, "sensor_readings", "alarm_flag")):
            rid = b.new_id("sensor_readings"); unit = {"load": "MW", "power_factor": "pu", "temperature": "C", "voltage": "kV"}.get(stype, "pu")
            b.insert("sensor_readings", {"reading_id": rid, "asset_id": asset["asset_id"], "reading_time": "2024-09-15 00:00", "sensor_type": stype, "reading_value": 88.125 + ai, "unit": unit, "alarm_flag": alarm}, "sensor_child_for_every_asset")
    # Alarm witnesses with no work order, uniformly across type x region.
    for tname, region in itertools.product(type_by_name, loc_by_region):
        aid = b.new_id("assets"); b.insert("assets", {"asset_id": aid, "asset_name": f"{prefix}_ALARM_NO_WO_{aid}", "asset_type_id": type_by_name[tname], "location_id": loc_by_region[region], "install_date": "2024-02-02", "status": "in_service", "capacity_mw": 99.125}, "alarm_without_work_order")
        for stype in domains(o, "sensor_readings", "sensor_type"):
            rid = b.new_id("sensor_readings"); unit = {"load": "MW", "power_factor": "pu", "temperature": "C", "voltage": "kV"}.get(stype, "pu")
            b.insert("sensor_readings", {"reading_id": rid, "asset_id": aid, "reading_time": "2024-10-01 00:00", "sensor_type": stype, "reading_value": 101.125, "unit": unit, "alarm_flag": 1}, "alarm_without_work_order")


def isolated_parent_cover(b: Builder, prefix: str) -> None:
    """Independent all-category parent-without-child state (no child inserts)."""
    o = b.original
    for spec, region, active in itertools.product(domains(o,"technicians","specialty"), domains(o,"technicians","home_region"), domains(o,"technicians","active")):
        rid=b.new_id("technicians"); b.insert("technicians", {"technician_id":rid,"technician_name":f"{prefix}_PARENT_ONLY_TECH_{rid}","specialty":spec,"home_region":region,"active":active}, "isolated_parent_cover")
    type_by_name={r["type_name"]:r["asset_type_id"] for r in o["asset_types"]}; loc_by_region={r["region"]:r["location_id"] for r in o["locations"]}
    for tname,region,status in itertools.product(type_by_name,loc_by_region,domains(o,"assets","status")):
        rid=b.new_id("assets"); b.insert("assets", {"asset_id":rid,"asset_name":f"{prefix}_PARENT_ONLY_ASSET_{rid}","asset_type_id":type_by_name[tname],"location_id":loc_by_region[region],"install_date":"2024-01-01","status":status,"capacity_mw":66.125}, "isolated_parent_cover")


def topology_motifs(b: Builder, prefix: str) -> None:
    o = b.original; at, loc = o["asset_types"][0]["asset_type_id"], o["locations"][0]["location_id"]
    ids = []
    for i in range(8):
        aid = b.new_id("assets"); b.insert("assets", {"asset_id": aid, "asset_name": f"{prefix}_TOPO_{i}", "asset_type_id": at, "location_id": loc, "install_date": "2024-01-01", "status": "in_service", "capacity_mw": 10.125 + i}, "topology_node"); ids.append(aid)
    edges = [(0,1,"feeder","closed"),(1,0,"feeder","open"),(1,2,"control","closed"),(1,3,"tie","open"),(2,4,"feeder","closed"),(3,4,"tie","closed"),(4,5,"control","open")]
    for u,v,kind,status in edges:
        rid=b.new_id("grid_topology"); b.insert("grid_topology", {"edge_id":rid,"upstream_asset_id":ids[u],"downstream_asset_id":ids[v],"connection_type":kind,"switch_status":status}, "topology_motif")


def string_decoys(b: Builder, policy: dict[str, Any]) -> None:
    transforms = {
        "upper": lambda s: s.upper(), "lower": lambda s: s.lower(), "prefix": lambda s: "SYNV2_" + s,
        "suffix": lambda s: s + "_SYNV2", "outer_space": lambda s: " " + s + " ", "punctuation": lambda s: s + ".v2",
    }
    for ci, name in enumerate(policy["string_decoys"], 1):
        maps = {t: {r[b.meta[t]["pk"]]: b.new_id(t) for r in b.original[t]} for t in TABLES}
        for table in TABLES:
            meta = b.meta[table]
            for source in b.original[table]:
                row = {}
                for col in meta["columns"]:
                    if col == meta["pk"]: value = maps[table][source[col]]
                    elif col in meta["fks"]: value = maps[meta["fks"][col]["table"]][source[col]]
                    elif isinstance(source[col], str) and not DATE_RE.match(source[col]): value = transforms[name](source[col])
                    else: value = source[col]
                    row[col] = value
                b.insert(table, row, f"string_decoy:{name}")


def validate(conn: sqlite3.Connection) -> dict[str, Any]:
    integrity = [r[0] for r in conn.execute("PRAGMA integrity_check")]
    fk = conn.execute("PRAGMA foreign_key_check").fetchall()
    counts = {t: conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in TABLES}
    return {"integrity_check": integrity, "foreign_key_violations": len(fk), "row_counts": counts}


def generate(base: Path, policy_path: Path, out: Path, trace_dir: Path) -> None:
    policy = json.loads(policy_path.read_text(encoding="utf-8")); out.mkdir(parents=True, exist_ok=True); trace_dir.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(f"file:{base.resolve().as_posix()}?mode=ro", uri=True); m = info(src); original = base_rows(src, m); src.close()
    compile_options = [r[0] for r in sqlite3.connect(":memory:").execute("PRAGMA compile_options")]
    records = []
    for spec in policy["state_plan"]:
        state, operator = spec["state"], spec["operator"]; target = out / f"{state}.sqlite"; trace = trace_dir / f"{state}.jsonl"
        if operator == "permutation": rebuild_permuted(base, target, int(spec["permutation_seed"])); trace.write_text(json.dumps({"state":state,"operator":"permutation","seed":spec["permutation_seed"]},sort_keys=True)+"\n",encoding="utf-8")
        else:
            copy_base(base, target); conn = sqlite3.connect(target); conn.execute("PRAGMA foreign_keys=ON"); b = Builder(conn, m, original, state, trace)
            try:
                if operator == "snapshot": pass
                elif operator == "cohorts":
                    for ci, mode in enumerate(spec["cohorts"], 1): append_cohort(b, mode, ci)
                elif operator == "categorical_covering": categorical_cover(b, policy["sentinel_prefix"], policy)
                elif operator == "numeric_date_boundaries": boundary_state(b, policy)
                elif operator == "dense_calendar_boundaries": dense_calendar_boundaries(b)
                elif operator == "null_witnesses": null_witnesses(b)
                elif operator == "relationship_anti_join_cover": relationship_cover(b, policy["sentinel_prefix"])
                elif operator == "isolated_parent_cover": isolated_parent_cover(b, policy["sentinel_prefix"])
                elif operator == "topology_motifs": topology_motifs(b, policy["sentinel_prefix"])
                elif operator == "string_decoys": string_decoys(b, policy)
                else: raise ValueError(operator)
                conn.commit()
            finally: b.close(); conn.close()
        check = sqlite3.connect(target); check.execute("PRAGMA foreign_keys=ON"); valid = validate(check); check.close()
        if valid["integrity_check"] != ["ok"] or valid["foreign_key_violations"]: raise RuntimeError({state:valid})
        records.append({"state":state,"operator":operator,"state_path":target.name,"state_sha256":sha(target),"state_bytes":target.stat().st_size,"trace_path":trace.name,"trace_sha256":sha(trace),"trace_bytes":trace.stat().st_size,**valid})
    manifest = {"schema_version":"ma-sqlgrid-query-blind-state-manifest-v2","status":"STAGE_A_COMPLETE_UNSIGNED","created_at_utc":now(),"generator_sha256":sha(Path(__file__)),"base_db":{"sha256":sha(base),"bytes":base.stat().st_size},"operator_policy":{"sha256":sha(policy_path),"bytes":policy_path.stat().st_size},"sqlite":{"version":sqlite3.sqlite_version,"compile_options":compile_options},"forbidden_inputs_accessed":{"benchmark_records":False,"gold_sql":False,"prediction_ledgers":False,"scores":False,"correctness":False},"states":records}
    manifest["manifest_content_sha256"] = canonical_hash(manifest); write_json(out / "STAGE_A_STATE_MANIFEST.json", manifest)
    print(f"STAGE_A_COMPLETE_UNSIGNED states={len(records)} sha={manifest['manifest_content_sha256']}")


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--base-db",type=Path,required=True); p.add_argument("--policy",type=Path,required=True); p.add_argument("--out",type=Path,required=True); p.add_argument("--trace-dir",type=Path,required=True); a=p.parse_args(); generate(a.base_db,a.policy,a.out,a.trace_dir)


if __name__ == "__main__": main()
