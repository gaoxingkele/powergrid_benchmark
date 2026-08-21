# MA-SQLGrid FINAL Executor Test Report

## Verdict

**PASS for the registered in-process returned-value boundary.** This is a
post-review engineering correction. It was not used by the historical
release-v3 descriptive re-execution and does not modify, rerun, or reinterpret
the 80/180, 100/180, or 101/180 results.

## Frozen test object

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `code/sqlite_readonly_executor_final.py` | 15,073 | `15723D46506806AE2ED15828AB980187B4828948C4FD3269010B5957E735B6B1` |
| `tests/test_sqlite_readonly_executor_final.py` | 7,995 | `516EE07EB2A1B6BD51FAA5D78140EFFA6FEB85B087710B1AF989201B717B8716` |

## Registered command and result

From the FINAL package root, with `code/` on `PYTHONPATH`:

```text
python -m unittest discover -s tests -p "test_*.py" -v
Ran 14 tests
OK
```

The immutable historical implementation was also rechecked separately in its
original tree: 30/30 agent, release-v3, replay, and historical executor tests
passed. The two counts describe different suites and are not added as 44
independent scientific tests.

## BLOB and result-budget acceptance tests

| Probe | Limits | Expected and observed result |
|---|---|---|
| `zeroblob(1000000)` | cell 1,024 B; result 1,024 B | fail closed: `cell_byte_limit`; raw observed cell 1,000,000 B; no returned partial row |
| `zeroblob(5000000)` | cell 1,024 B; result 1,024 B | fail closed: `cell_byte_limit`; raw observed cell 5,000,000 B; failure retained in JSONL trace |
| `zeroblob(50000000)` | cell 1,024 B; result 1,024 B | fail closed: `cell_byte_limit`; raw observed cell 50,000,000 B; no returned partial row |
| `zeroblob(1000000)` | cell 2,000,000 B; result 1,024 B | fail closed: `result_byte_limit`; accounted result exceeds 1,000,000 B because raw payload plus deterministic structure is charged |
| `zeroblob(1024)` | cell exactly 1,024 B; result 4,096 B | accepted at boundary |
| `zeroblob(1024)` | cell 1,023 B; result 4,096 B | fail closed: `cell_byte_limit` |
| 1,024-byte `memoryview` helper probe | direct accounting | raw charge exactly 1,024 B; result charge greater than 1,024 B after deterministic envelope overhead |

## Accounting definition

- `bytes`, `bytearray`, and `memoryview` cells are checked at their original
  payload length before conversion to a digest-bearing public representation.
- Text cells are checked at their unescaped UTF-8 payload length.
- The total returned-result budget charges canonical column/container/row/
  delimiter overhead and, for BLOBs, the original payload plus the deterministic
  digest/length envelope. A small hash proxy therefore cannot reduce the charge.
- On any row, cell, width, authorization, opcode, timeout, or total-result
  failure, the public result is non-executable and contains no partial rows.
  The trace retains the failure kind, configured bounds, bytes accounted, and
  largest raw cell observed.

## Scope boundary

These tests cover the Python/SQLite executor's returned-value accounting,
read-only URI, `query_only`, authorizer, extension denial, table/column and
optional function allowlists, opcode/time/row/column limits, and trace
retention. They do not prove user entitlement, row-level institutional access
policy, OS-level process isolation, or a bound on every SQLite temporary-memory
allocation. They also provide no evidence of a five-role accuracy benefit or
qualified power-grid semantic validity.
