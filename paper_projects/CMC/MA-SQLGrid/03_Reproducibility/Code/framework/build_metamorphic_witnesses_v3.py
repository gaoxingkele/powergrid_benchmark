#!/usr/bin/env python3
"""Build release-v3 query-blind SQLite witnesses with bound provenance."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3


SCRIPT = Path(__file__).resolve()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def build(base: Path, out: Path) -> None:
    if out.exists():
        raise FileExistsError(f"output exists; refusing overwrite: {out}")
    created_at_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out.mkdir(parents=True)
    specs = [
        (
            "M1_irrelevant_relation_rows",
            [
                "CREATE TABLE __ma_probe_irrelevant(probe_id INTEGER PRIMARY KEY, note TEXT NOT NULL)",
                "INSERT INTO __ma_probe_irrelevant VALUES (1,'alpha'),(2,'beta'),(3,'gamma')",
            ],
            "All original tables, named columns, and rows are unchanged; queries restricted to the original schema retain their denotation.",
        ),
        (
            "M2_harmless_indexes_rebuild",
            [
                "CREATE INDEX __ma_probe_assets_status ON assets(status)",
                "CREATE INDEX __ma_probe_work_orders_status ON work_orders(status, priority)",
                "CREATE INDEX __ma_probe_sensor_type ON sensor_readings(sensor_type, reading_time)",
                "VACUUM",
            ],
            "Only indexes and physical storage are changed; ordered results preserve order and unordered results are compared as multisets.",
        ),
        (
            "M3_nullable_schema_extension",
            [
                "ALTER TABLE assets ADD COLUMN __ma_probe_nullable TEXT",
                "ALTER TABLE work_orders ADD COLUMN __ma_probe_nullable TEXT",
                "ALTER TABLE sensor_readings ADD COLUMN __ma_probe_nullable TEXT",
            ],
            "Existing named columns and rows are unchanged; explicit-column queries retain denotation, while wildcard projections may fail invariance by design.",
        ),
    ]
    records = []
    for name, statements, invariant in specs:
        target = out / f"{name}.sqlite"
        shutil.copy2(base, target)
        connection = sqlite3.connect(target)
        try:
            for statement in statements:
                connection.execute(statement)
            connection.commit()
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        finally:
            connection.close()
        records.append({
            "state_id": name,
            "path": target.name,
            "bytes": target.stat().st_size,
            "sha256": sha(target),
            "operator_sql": statements,
            "invariant": invariant,
            "integrity_check": integrity,
        })
    hashes = {row["sha256"] for row in records}
    if len(hashes) != 3 or sha(base) in hashes:
        raise AssertionError("witness databases must have three unique hashes distinct from T0")
    manifest = {
        "schema_version": "ma-sqlgrid-query-blind-metamorphic-witnesses-v3",
        "status": "BUILT_BEFORE_V3_FREEZE_AND_SELECTION",
        "created_at_utc": created_at_utc,
        "builder": {
            "path": SCRIPT.name,
            "bytes": SCRIPT.stat().st_size,
            "sha256": sha(SCRIPT),
            "schema_version": "ma-sqlgrid-witness-builder-v3",
        },
        "base": {"path": str(base), "bytes": base.stat().st_size, "sha256": sha(base)},
        "forbidden_inputs_accessed": {
            "questions": False,
            "gold_sql": False,
            "predictions": False,
            "prompts": False,
            "scores": False,
        },
        "comparison_policy": "Candidate SQL determines ordered versus multiset comparison; M3 wildcard arity changes are predeclared non-invariance and are not normalized away.",
        "states": records,
    }
    manifest["manifest_content_sha256"] = canonical_hash(manifest)
    (out / "WITNESS_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    build(args.base.resolve(strict=True), args.out.resolve())
