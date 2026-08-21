"""Read-only BIRD Mini-Dev database and gold-SQL compatibility preflight."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
META = ROOT / "official_metadata" / "bird_mini_dev_sqlite.json"
DB_ROOT = ROOT / "official_downloads" / "bird_dev_databases_extracted" / "dev_databases"
OUT = ROOT / "BIRD_GOLD_PREFLIGHT.json"
# Gold compatibility is checked before model execution. Two official queries
# exceed 30 seconds on the local SQLite build, so the preflight uses a frozen
# 180-second ceiling and records every elapsed time for later evaluator design.
TIMEOUT_SECONDS = 180.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    rows = json.loads(META.read_text(encoding="utf-8"))
    assert len(rows) == 500
    assert len({row["question_id"] for row in rows}) == 500
    db_ids = sorted({row["db_id"] for row in rows})
    database_files = {db_id: DB_ROOT / db_id / f"{db_id}.sqlite" for db_id in db_ids}
    missing = [db_id for db_id, path in database_files.items() if not path.is_file()]
    if missing:
        raise SystemExit(f"Missing database files: {missing}")

    database_manifest = {
        db_id: {"relative_path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for db_id, path in database_files.items()
    }
    failures = []
    summaries = []
    start_all = time.perf_counter()
    for index, row in enumerate(rows):
        sql = row["SQL"].strip()
        if not sql.lower().startswith(("select", "with")):
            failures.append({"question_id": row["question_id"], "db_id": row["db_id"], "error": "non_read_only_prefix"})
            continue
        path = database_files[row["db_id"]]
        uri = path.resolve().as_uri() + "?mode=ro"
        started = time.perf_counter()
        try:
            connection = sqlite3.connect(uri, uri=True)
            connection.execute("PRAGMA query_only=ON")
            connection.set_progress_handler(
                lambda: 1 if time.perf_counter() - started > TIMEOUT_SECONDS else 0,
                10_000,
            )
            cursor = connection.execute(sql)
            result = cursor.fetchall()
            columns = len(cursor.description or ())
            payload_hash = hashlib.sha256(repr(result).encode("utf-8")).hexdigest()
            summaries.append(
                {
                    "question_id": row["question_id"],
                    "db_id": row["db_id"],
                    "rows": len(result),
                    "columns": columns,
                    "result_repr_sha256": payload_hash,
                    "elapsed_seconds": round(time.perf_counter() - started, 6),
                }
            )
        except Exception as exc:  # retained in an all-attempt preflight ledger
            failures.append(
                {
                    "question_id": row["question_id"],
                    "db_id": row["db_id"],
                    "error": type(exc).__name__,
                    "message": str(exc),
                }
            )
        finally:
            if "connection" in locals():
                connection.close()
                del connection

    report = {
        "schema_version": "ma-bird-gold-preflight-v1",
        "population": 500,
        "unique_question_ids": 500,
        "databases_expected": 11,
        "databases_present": len(database_manifest),
        "metadata_sha256": sha256(META),
        "database_manifest": database_manifest,
        "executed_successfully": len(summaries),
        "failures": failures,
        "difficulty_counts": dict(Counter(row["difficulty"] for row in rows)),
        "database_counts": dict(Counter(row["db_id"] for row in rows)),
        "total_elapsed_seconds": round(time.perf_counter() - start_all, 6),
        "decision": "PASS" if len(summaries) == 500 and not failures else "BLOCK",
        "model_calls": 0,
        "per_query_timeout_seconds": TIMEOUT_SECONDS,
        "python_version": sys.version,
        "sqlite_version": sqlite3.sqlite_version,
        "result_summaries": summaries,
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("decision", "executed_successfully", "failures", "total_elapsed_seconds")}, ensure_ascii=False))
    if report["decision"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
