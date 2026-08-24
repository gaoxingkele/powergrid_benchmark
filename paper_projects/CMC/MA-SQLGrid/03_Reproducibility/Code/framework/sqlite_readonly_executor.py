"""Database-enforced, resource-bounded SQLite execution for MA-SQLGrid.

The lexical :class:`Validator` is only a prefilter.  This module is the actual
database boundary used by the Round-2 offline study: it opens a frozen snapshot
through a read-only URI, enables SQLite ``query_only``, disables loadable
extensions, installs a deny-by-default mutation/metadata authorizer, and
terminates work that exceeds the configured opcode, time, or result-row budget.

Every call returns a structured trace.  When ``trace_path`` is supplied, that
trace is appended as one JSON line; failures are never retried or overwritten.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import sqlite3
import time
from typing import Any, Mapping, Sequence


_BLOCKED_FUNCTIONS = {
    "edit",
    "fts3_tokenizer",
    "load_extension",
    "readfile",
    "shell_add_schema",
    "writefile",
}

_ALLOWED_ACTIONS = {
    sqlite3.SQLITE_FUNCTION,
    sqlite3.SQLITE_READ,
    sqlite3.SQLITE_RECURSIVE,
    sqlite3.SQLITE_SELECT,
}


def _json_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, bytes):
        return {"bytes_sha256": hashlib.sha256(value).hexdigest(), "length": len(value)}
    return str(value)


def _result_hash(columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    body = {
        "columns": list(columns),
        "rows": [[_json_value(value) for value in row] for row in rows],
    }
    encoded = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SQLiteExecutionTrace:
    database_sha256: str
    sql_sha256: str
    executable: bool
    failure_kind: str | None
    error: str | None
    elapsed_ms: float
    progress_callbacks: int
    row_count: int
    columns: tuple[str, ...]
    result_hash: str | None
    query_only: bool
    read_only_uri: bool
    row_limit: int
    opcode_limit: int
    timeout_seconds: float


class SQLiteReadOnlyExecutor:
    """Callable SQLite executor with fail-closed authorization and limits."""

    def __init__(
        self,
        database_path: str | Path,
        *,
        timeout_seconds: float = 2.0,
        max_opcodes: int = 2_000_000,
        progress_step: int = 1_000,
        max_rows: int = 10_000,
        allowed_tables: Mapping[str, Sequence[str] | None] | None = None,
        allow_metadata: bool = False,
        trace_path: str | Path | None = None,
    ) -> None:
        self.database_path = Path(database_path).resolve(strict=True)
        if not self.database_path.is_file():
            raise ValueError(f"database is not a file: {self.database_path}")
        if timeout_seconds <= 0 or max_opcodes < 1 or progress_step < 1 or max_rows < 1:
            raise ValueError("timeout/opcode/progress/row limits must be positive")
        self.timeout_seconds = float(timeout_seconds)
        self.max_opcodes = int(max_opcodes)
        self.progress_step = int(progress_step)
        self.max_rows = int(max_rows)
        self.allow_metadata = bool(allow_metadata)
        self.trace_path = Path(trace_path).resolve() if trace_path else None
        self.database_sha256 = hashlib.sha256(self.database_path.read_bytes()).hexdigest()
        self.allowed_tables = None
        if allowed_tables is not None:
            self.allowed_tables = {
                str(table).lower(): None if columns is None else {str(column).lower() for column in columns}
                for table, columns in allowed_tables.items()
            }

    def _append_trace(self, trace: SQLiteExecutionTrace) -> None:
        if self.trace_path is None:
            return
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        with self.trace_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(asdict(trace), ensure_ascii=False, sort_keys=True) + "\n")

    def __call__(self, sql: str) -> Mapping[str, Any]:
        started = time.monotonic()
        deadline = started + self.timeout_seconds
        callbacks = 0
        interruption_reason: str | None = None
        columns: tuple[str, ...] = ()
        rows: list[tuple[Any, ...]] = []
        query_only = False
        uri = self.database_path.as_uri() + "?mode=ro&immutable=1"

        def progress() -> int:
            nonlocal callbacks, interruption_reason
            callbacks += 1
            if callbacks * self.progress_step > self.max_opcodes:
                interruption_reason = "opcode_limit"
                return 1
            if time.monotonic() > deadline:
                interruption_reason = "timeout"
                return 1
            return 0

        def authorizer(action: int, arg1: str | None, arg2: str | None, _db: str | None, _source: str | None) -> int:
            if action not in _ALLOWED_ACTIONS:
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_FUNCTION:
                function_name = (arg2 or arg1 or "").lower()
                return sqlite3.SQLITE_DENY if function_name in _BLOCKED_FUNCTIONS else sqlite3.SQLITE_OK
            if action == sqlite3.SQLITE_READ:
                table = (arg1 or "").lower()
                column = (arg2 or "").lower()
                if table in {"sqlite_master", "sqlite_schema", "sqlite_temp_master", "sqlite_temp_schema"}:
                    return sqlite3.SQLITE_OK if self.allow_metadata else sqlite3.SQLITE_DENY
                if self.allowed_tables is not None:
                    allowed_columns = self.allowed_tables.get(table, "missing")
                    if allowed_columns == "missing":
                        return sqlite3.SQLITE_DENY
                    if allowed_columns is not None and column and column not in allowed_columns:
                        return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK

        failure_kind: str | None = None
        error: str | None = None
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(uri, uri=True, timeout=self.timeout_seconds)
            connection.enable_load_extension(False)
            connection.execute("PRAGMA query_only=ON")
            query_only = bool(connection.execute("PRAGMA query_only").fetchone()[0])
            if not query_only:
                raise RuntimeError("SQLite query_only could not be enabled")
            connection.set_authorizer(authorizer)
            connection.set_progress_handler(progress, self.progress_step)
            cursor = connection.execute(sql)
            columns = tuple(item[0] for item in (cursor.description or ()))
            rows = cursor.fetchmany(self.max_rows + 1)
            if len(rows) > self.max_rows:
                failure_kind = "row_limit"
                error = f"result exceeds configured row limit {self.max_rows}"
                rows = rows[: self.max_rows]
        except sqlite3.DatabaseError as exc:
            failure_kind = interruption_reason or ("authorization" if "not authorized" in str(exc).lower() else "sqlite_error")
            error = f"{type(exc).__name__}: {exc}"
        except Exception as exc:
            failure_kind = "executor_error"
            error = f"{type(exc).__name__}: {exc}"
        finally:
            if connection is not None:
                connection.set_progress_handler(None, 0)
                connection.set_authorizer(None)
                connection.close()

        elapsed_ms = round((time.monotonic() - started) * 1_000, 6)
        executable = failure_kind is None
        result_hash = _result_hash(columns, rows) if executable else None
        trace = SQLiteExecutionTrace(
            database_sha256=self.database_sha256,
            sql_sha256=hashlib.sha256(sql.encode("utf-8")).hexdigest(),
            executable=executable,
            failure_kind=failure_kind,
            error=error,
            elapsed_ms=elapsed_ms,
            progress_callbacks=callbacks,
            row_count=len(rows) if executable else 0,
            columns=columns,
            result_hash=result_hash,
            query_only=query_only,
            read_only_uri=True,
            row_limit=self.max_rows,
            opcode_limit=self.max_opcodes,
            timeout_seconds=self.timeout_seconds,
        )
        self._append_trace(trace)
        return {
            "ok": executable,
            "executable": executable,
            "error": error,
            "failure_kind": failure_kind,
            "row_count": trace.row_count,
            "columns": columns,
            "rows": tuple(tuple(_json_value(value) for value in row) for row in rows) if executable else (),
            "result_hash": result_hash,
            "trace": asdict(trace),
        }
