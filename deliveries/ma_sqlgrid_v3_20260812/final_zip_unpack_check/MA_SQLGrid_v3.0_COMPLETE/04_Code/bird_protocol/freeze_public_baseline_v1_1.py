"""Protocol v1.1 execution guard layered over immutable v1.0 assets.

The only behavioral change is that sqlite3.Warning is routed through the
existing frozen error classifier.  Dataset, prompts, call order, models,
evaluation semantics, token limits, and statistics remain inherited from v1.0.
"""
from __future__ import annotations

import re
import sqlite3
import time
from pathlib import Path
from typing import Any

from freeze_public_baseline_v1_0_snapshot import *  # noqa: F401,F403 - intentional frozen inheritance
import freeze_public_baseline_v1_0_snapshot as _v1

PROTOCOL_ID_V1_1 = "MA-PUBLIC-BIRD-MINIDEV-v1.1"
BASE_PROTOCOL_ID = _v1.PROTOCOL_ID


def safe_execute(sql: str, path: Path, timeout_seconds: float = 30.0) -> tuple[str, list[tuple[Any, ...]] | None]:
    """Execute one read-only query and deterministically classify SQLite warnings.

    This is byte-for-byte equivalent in control policy to v1.0 except for the
    final exception tuple, which adds ``sqlite3.Warning``.  Under the pinned
    Python 3.10.11 runtime, multi-statement input raises sqlite3.Warning rather
    than sqlite3.Error; v1.1 maps it to the existing OTHER_EXECUTION_ERROR label.
    """
    candidate = sql.strip()
    if not re.match(r"(?is)^(select|with)\b", candidate) or "\x00" in candidate:
        return "PARSE_ERROR", None
    if len(candidate.encode("utf-8")) > 64 * 1024:
        return "PARSE_ERROR", None
    started = time.perf_counter()
    con = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        con.execute("PRAGMA query_only=ON")
        denied = {
            sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE,
            sqlite3.SQLITE_CREATE_INDEX, sqlite3.SQLITE_CREATE_TABLE, sqlite3.SQLITE_CREATE_TEMP_INDEX,
            sqlite3.SQLITE_CREATE_TEMP_TABLE, sqlite3.SQLITE_CREATE_TEMP_TRIGGER, sqlite3.SQLITE_CREATE_TEMP_VIEW,
            sqlite3.SQLITE_CREATE_TRIGGER, sqlite3.SQLITE_CREATE_VIEW, sqlite3.SQLITE_DROP_INDEX,
            sqlite3.SQLITE_DROP_TABLE, sqlite3.SQLITE_DROP_TEMP_INDEX, sqlite3.SQLITE_DROP_TEMP_TABLE,
            sqlite3.SQLITE_DROP_TEMP_TRIGGER, sqlite3.SQLITE_DROP_TEMP_VIEW, sqlite3.SQLITE_DROP_TRIGGER,
            sqlite3.SQLITE_DROP_VIEW, sqlite3.SQLITE_ALTER_TABLE, sqlite3.SQLITE_REINDEX,
            sqlite3.SQLITE_ANALYZE, sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH,
        }
        con.set_authorizer(
            lambda action, *_: sqlite3.SQLITE_DENY
            if action in denied or action == sqlite3.SQLITE_PRAGMA
            else sqlite3.SQLITE_OK
        )
        con.set_progress_handler(lambda: 1 if time.perf_counter() - started > timeout_seconds else 0, 10_000)
        cursor = con.execute(candidate)
        return "SAFE_EXECUTED", cursor.fetchall()
    except (sqlite3.Error, sqlite3.Warning) as exc:
        return _v1.classify_sqlite_error(str(exc)), None
    finally:
        con.close()
