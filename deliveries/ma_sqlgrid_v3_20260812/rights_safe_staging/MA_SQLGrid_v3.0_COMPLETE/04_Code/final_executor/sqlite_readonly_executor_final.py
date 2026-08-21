"""FINAL additive SQLite execution boundary for MA-SQLGrid.

The lexical :class:`Validator` is only a prefilter.  This module is the actual
database boundary used only by the post-review FINAL executor tests: it opens a
frozen snapshot through a read-only URI, enables SQLite ``query_only``, disables
loadable extensions, installs a deny-by-default mutation/metadata authorizer,
and terminates work that exceeds the registered opcode, time, result-row,
raw-cell-byte, budgeted-result-byte, or output-column limit.  These controls
were added after, and were not used by, the historical release-v3 descriptive
re-execution or the Round-2 experiments.  Callers can additionally select an
explicit SQLite function allowlist.  ``allowed_functions=None`` preserves the
historical default policy (all functions except the retained denylist).

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


_BLOB_JSON_PREFIX = b'{"bytes_sha256":"'
_BLOB_JSON_MIDDLE = b'","length":'
_BLOB_JSON_SUFFIX = b'}'


def _blob_bytes(value: Any) -> bytes | None:
    """Return a byte payload without allowing a hash proxy to hide its size."""

    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    return None


def _json_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    blob = _blob_bytes(value)
    if blob is not None:
        return {"bytes_sha256": hashlib.sha256(blob).hexdigest(), "length": len(blob)}
    return str(value)


def _result_hash(columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    body = {
        "columns": list(columns),
        "rows": [[_json_value(value) for value in row] for row in rows],
    }
    encoded = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _raw_value_size(value: Any) -> int:
    """Return raw scalar bytes for the per-cell boundary.

    SQLite BLOBs are charged at their original payload length before hashing.
    Text is charged at its unescaped UTF-8 length; other scalar values use their
    deterministic canonical JSON encoding.
    """

    blob = _blob_bytes(value)
    if blob is not None:
        return len(blob)
    if isinstance(value, str):
        return len(value.encode("utf-8"))
    encoded = json.dumps(
        _json_value(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return len(encoded.encode("utf-8"))


def _budgeted_value_size(value: Any) -> int:
    """Charge raw payload plus deterministic canonical-envelope overhead.

    For BLOBs, the returned representation contains a digest rather than the
    payload.  The budget deliberately charges the *raw* payload and the exact
    structural bytes of the digest/length envelope, so hashing cannot reduce
    the charged size.  Other values are charged at canonical JSON size.
    """

    blob = _blob_bytes(value)
    if blob is None:
        encoded = json.dumps(
            _json_value(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        return len(encoded.encode("utf-8"))
    length_digits = len(str(len(blob)).encode("ascii"))
    return (
        len(blob)
        + len(_BLOB_JSON_PREFIX)
        + 64
        + len(_BLOB_JSON_MIDDLE)
        + length_digits
        + len(_BLOB_JSON_SUFFIX)
    )


def _result_prefix_size(columns: Sequence[str]) -> int:
    encoded_columns = json.dumps(
        list(columns), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return len(b'{"columns":') + len(encoded_columns) + len(b',"rows":[') + len(b']}')


def _budgeted_row_size(row: Sequence[Any]) -> int:
    return 2 + max(0, len(row) - 1) + sum(_budgeted_value_size(value) for value in row)


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
    result_byte_limit: int
    cell_byte_limit: int
    output_column_limit: int
    opcode_limit: int
    timeout_seconds: float
    function_policy: str
    allowed_functions: tuple[str, ...]
    result_bytes_accounted: int
    largest_cell_bytes: int


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
        max_result_bytes: int = 16_777_216,
        max_cell_bytes: int = 1_048_576,
        max_output_columns: int = 256,
        allowed_tables: Mapping[str, Sequence[str] | None] | None = None,
        allowed_functions: Sequence[str] | None = None,
        allow_metadata: bool = False,
        trace_path: str | Path | None = None,
    ) -> None:
        self.database_path = Path(database_path).resolve(strict=True)
        if not self.database_path.is_file():
            raise ValueError(f"database is not a file: {self.database_path}")
        limits = (
            timeout_seconds,
            max_opcodes,
            progress_step,
            max_rows,
            max_result_bytes,
            max_cell_bytes,
            max_output_columns,
        )
        if any(limit <= 0 for limit in limits):
            raise ValueError("all executor resource limits must be positive")
        self.timeout_seconds = float(timeout_seconds)
        self.max_opcodes = int(max_opcodes)
        self.progress_step = int(progress_step)
        self.max_rows = int(max_rows)
        self.max_result_bytes = int(max_result_bytes)
        self.max_cell_bytes = int(max_cell_bytes)
        self.max_output_columns = int(max_output_columns)
        self.allowed_functions = (
            None
            if allowed_functions is None
            else frozenset(str(name).strip().lower() for name in allowed_functions)
        )
        if self.allowed_functions is not None and (not self.allowed_functions or "" in self.allowed_functions):
            raise ValueError("allowed_functions must contain one or more nonempty names")
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
        result_bytes_accounted = 0
        largest_cell_bytes = 0
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
                if function_name in _BLOCKED_FUNCTIONS:
                    return sqlite3.SQLITE_DENY
                if self.allowed_functions is not None and function_name not in self.allowed_functions:
                    return sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK
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
            if len(columns) > self.max_output_columns:
                failure_kind = "output_column_limit"
                error = f"result exceeds registered output-column limit {self.max_output_columns}"
            else:
                result_bytes_accounted = _result_prefix_size(columns)
                if result_bytes_accounted > self.max_result_bytes:
                    failure_kind = "result_byte_limit"
                    error = f"result exceeds registered byte limit {self.max_result_bytes}"
                for row in cursor:
                    if failure_kind is not None:
                        break
                    if len(rows) >= self.max_rows:
                        failure_kind = "row_limit"
                        error = f"result exceeds registered row limit {self.max_rows}"
                        break
                    cell_sizes = [_raw_value_size(value) for value in row]
                    largest_cell_bytes = max([largest_cell_bytes, *cell_sizes])
                    if largest_cell_bytes > self.max_cell_bytes:
                        failure_kind = "cell_byte_limit"
                        error = f"result contains a cell exceeding registered byte limit {self.max_cell_bytes}"
                        break
                    row_bytes = _budgeted_row_size(row)
                    added_bytes = row_bytes + (1 if rows else 0)
                    prospective_bytes = result_bytes_accounted + added_bytes
                    if prospective_bytes > self.max_result_bytes:
                        failure_kind = "result_byte_limit"
                        error = f"result exceeds registered byte limit {self.max_result_bytes}"
                        result_bytes_accounted = prospective_bytes
                        break
                    result_bytes_accounted = prospective_bytes
                    rows.append(tuple(row))
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
            result_byte_limit=self.max_result_bytes,
            cell_byte_limit=self.max_cell_bytes,
            output_column_limit=self.max_output_columns,
            opcode_limit=self.max_opcodes,
            timeout_seconds=self.timeout_seconds,
            function_policy="historical_denylist" if self.allowed_functions is None else "explicit_allowlist",
            allowed_functions=tuple(sorted(self.allowed_functions or ())),
            result_bytes_accounted=result_bytes_accounted,
            largest_cell_bytes=largest_cell_bytes,
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
