# Independent FINAL SQLite Executor Audit

**Audit date:** 2026-08-08 (Asia/Shanghai)  
**Auditor role:** independent read-only code/test auditor  
**Overall executor verdict:** **PASS**  
**Historical-result non-retroactivity verdict:** **PASS**  
**Manuscript-claim alignment verdict:** **PASS, with two non-blocking scope advisories**

## Task frame

- **Goal:** independently determine whether the raw-BLOB accounting defect reported by the Round-3 reviewers is closed in the FINAL SQLite executor, without editing the implementation or manuscript.
- **Context:** `code/sqlite_readonly_executor_final.py`, its FINAL tests, the restored 30-test release-v3 tree, the three retained Round-3 reviews, and the current `paper_applsci.tex`.
- **Constraints:** no implementation/manuscript edits; no reinterpretation or rerun of release-v3 scientific outcomes; no claim that an in-process fetch-time guard is whole-process memory isolation.
- **Done criterion:** reproduce the reported exploit and its closure; exercise exact BLOB, scalar, total-budget, trace, and function-policy boundaries; rerun both registered suites; bind audited files by SHA-256; and verify that the manuscript distinguishes FINAL controls from historical v3.

## Audited byte identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `code/sqlite_readonly_executor_final.py` | 15,073 | `15723D46506806AE2ED15828AB980187B4828948C4FD3269010B5957E735B6B1` |
| `tests/test_sqlite_readonly_executor_final.py` | 7,995 | `516EE07EB2A1B6BD51FAA5D78140EFFA6FEB85B087710B1AF989201B717B8716` |
| retained R3 executor | 12,957 | `1474AF733B044491B65266C2EBBFD52E9E180C8291FCE2E725B881BFB37CD652` |
| retained R3 executor tests | 5,321 | `60B9D698395C5EC95699860528508675B389EC48EC9EFA06D9797A43C4BC46C8` |
| frozen release-v3 executor | not modified by this audit | `3F28F832F437CFE74DEC56E989D54A5626BBEB5DD4B1311A7D2681D3F314DC55` |
| current manuscript source at claim audit | 69,672 | `32F5616F07F04E3665613385231189CE9532BCF6E9601319BBF655DEE5240CC9` |

The frozen release-v3 executor hash matches its 21-artifact freeze manifest entry. The FINAL executor has a distinct name, path, byte count, and hash. No frozen file was changed for this audit.

## Runtime and registered-suite results

The independent reproduction used Windows 11, CPython 3.12.10, and the Python runtime's SQLite 3.49.1. This is an audit runtime, not a retroactive claim about the historical BIRD or release-v3 runtime.

| Suite | Invocation scope | Result |
|---|---|---:|
| FINAL additive suite | discovery under `FINAL/tests`, importing only `FINAL/code` | **14/14 PASS** |
| restored frozen tree | discovery over the four files under `original_title_rebuild/tests` | **30/30 PASS** |
| independent adversarial/accounting probes | temporary databases and direct helper probes | **38/38 PASS** |

The 38 independent checks comprise 33 general adversarial/accounting assertions plus five stored-BLOB assertions. They are audit probes, not additional registered unit-test counts and not scientific observations.

## Reproduction of the Round-3 defect and FINAL closure

The retained R3 executor and FINAL executor were invoked against the same temporary read-only database and the same query, `SELECT zeroblob(1000000)`, with `max_cell_bytes=128`, `max_result_bytes=256`, and one output column. The retained R3 implementation returned success and exposed a one-million-byte BLOB through its digest envelope. The FINAL implementation returned:

- `executable=false`;
- `failure_kind="cell_byte_limit"`;
- `row_count=0`;
- `rows=()`;
- `result_hash=null`; and
- `largest_cell_bytes=1000000`.

Fresh FINAL probes at exactly 1,000,000, 5,000,000, and 50,000,000 bytes, all under the 128-byte cell and 256-byte result limits, produced the same named fail-closed outcome with zero returned rows. Thus the hash-envelope representation no longer hides the raw BLOB length from the cell boundary.

## Boundary and accounting findings

### Raw bytes-like values

Direct checks of `bytes`, `bytearray`, and `memoryview` established that `_raw_value_size` returns the original payload length. For a 128-byte value, `_budgeted_value_size` returned 224 bytes: the original 128 bytes plus the exact 96-byte canonical digest/length envelope. The calculation therefore cannot reduce a large payload to the digest's serialized size.

### Exact BLOB boundaries

- `zeroblob(128)` passes `max_cell_bytes=128`; the same value fails at 127.
- With column alias `b`, the independently computed total charge for a 128-byte BLOB is 253 bytes. It passes at `max_result_bytes=253` and fails at 252.
- A one-million-byte BLOB with a permissive cell limit but a 256-byte total limit fails with `failure_kind="result_byte_limit"` and `result_bytes_accounted > 1,000,000`.
- Stored BLOBs of 127 and 128 bytes pass a 128-byte cell limit; stored BLOBs of 129 and 1,000,000 bytes fail it. A later-row failure suppresses all earlier buffered rows from the public result.

### Integer, NULL, Unicode, row, and container charges

Independent canonical-JSON arithmetic agreed exactly with the implementation for zero, a negative integer, the maximum signed 64-bit integer, `NULL`, multibyte Unicode, combining Unicode, and escaped string characters. A mixed row containing `(42, NULL, a U+6C49 plus U+1F642 multibyte sample)` had an independently calculated complete-result charge of 50 bytes and passed at 50 while failing at 49. A two-row result had an exact charge of 56 bytes and passed at 56 while failing at 55. These probes cover commas, row brackets, column serialization, and outer-container overhead; no integer, `NULL`, Unicode, or row-separator undercount was observed.

## Failure traces and row leakage

A two-row query was constructed so that the first row fit and the second contained a unique oversized sentinel. The public failure object and appended JSONL trace reported `cell_byte_limit`, zero rows, and no result hash. The trace contained the SQL hash, column name, failure kind, configured limits, and largest observed raw-cell size, but neither the first-row value nor the oversized sentinel nor raw SQL. The ledger appended attempts rather than overwriting them. This closes the tested partial-row leakage path.

## Explicit function policy

With `allowed_functions=["COUNT"]`, case normalization produced the frozen trace value `("count",)`, `count(*)` executed, and both `lower(...)` and `zeroblob(...)` failed with `failure_kind="authorization"`. The retained dangerous-function denylist and table/column authorizer tests also passed. This supports an explicit SQLite-function allowlist claim; it does not establish authentication, row-level identity policy, or a whole-language sandbox.

## Manuscript claim audit

The current manuscript is consistent with the audited implementation at the material locations:

- Methods states that the FINAL variant was added **after R3 review**, charges BLOBs/memory views at original payload length, and has a 14-test additive suite.
- The chronology distinguishes the restored frozen 30/30 suite, the superseded R3 10-test suite that missed raw BLOBs, and the FINAL 14-test suite.
- The manuscript explicitly says the FINAL controls were not used to obtain or reinterpret the release-v3 5,760-attempt ledger or the 80/100/101 counts.
- Discussion and Conclusions label the controls as FINAL rather than R3, and explicitly deny whole-process memory isolation and retroactive use.
- The frozen release-v3 executor still matches its freeze-manifest hash, while the corrected implementation resides under a separate FINAL filename.

No statement was found that retrospectively attributes the FINAL BLOB fix to release v3.

## Scope advisories (non-blocking)

1. The limits are enforced after SQLite/Python has materialized each fetched scalar. The audit proves fail-closed returned-result behavior and accounting, not a pre-allocation cap on SQLite temporary memory or total process RSS. The manuscript now states this limitation correctly.
2. The registered 14-test file exercises `zeroblob` rather than a stored-BLOB column. The same `bytes` path is reached and the independent stored-BLOB probes passed, so this is not an implementation failure. Adding a permanent stored-BLOB regression in a future version would improve coverage, but changing the current frozen FINAL bytes would require new hashes and a new audit.

## Final decision

**PASS.** The specific Round-3 raw-BLOB/hash-proxy defect is closed for the audited FINAL implementation. Raw bytes-like values are charged before hashing; exact cell and total-budget boundaries behave correctly; integer, `NULL`, Unicode, row, delimiter, and container accounting matched independent calculations; function allowlisting fails closed; resource failures return no rows and retain named, non-row-bearing traces; the FINAL and frozen 30-test suites pass; and the manuscript does not apply the correction retroactively to release-v3 results.
