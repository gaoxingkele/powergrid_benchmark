# R3 SQLite Executor Extension Test Report

## Scope

The additive R3 executor extends the previously frozen SQLite research boundary
with three result-shape/resource budgets and an optional explicit function
allowlist:

- `max_result_bytes` (default 16,777,216 bytes);
- `max_cell_bytes` (default 1,048,576 bytes);
- `max_output_columns` (default 256 columns); and
- `allowed_functions`, where `None` preserves the historical denylist behavior
  and a supplied sequence activates deny-by-default function authorization.

The byte budget is computed over the same canonical JSON body used for the
result hash. Oversized results fail closed and return no rows. These controls do
not provide OS process isolation, process-memory containment, user entitlement,
or power-grid semantic authorization.

## Execution

Command, from `original_title_manuscript/R3_staging`:

```powershell
$env:PYTHONPATH=(Resolve-Path '.\code').Path
python -m unittest discover -s tests -p 'test_*_r3.py' -v
```

Result: **10/10 tests passed**. The added cases cover an oversized scalar, an
oversized aggregate result, a projection wider than the registered limit, and
explicit allow/deny function behavior. The inherited mutation, metadata,
table/column, row, opcode/time, trace-retention, and database-immutability tests
also passed against the R3 implementation.

The untouched frozen suite was then rerun from `original_title_rebuild`:

```powershell
python -m unittest discover -s tests -v
```

Result: **30/30 tests passed**. A separate manifest check verified all **21/21**
frozen file hashes and byte counts; no mismatch remained.

## Evidence boundary

The R3 tests demonstrate implemented, deterministic SQLite controls in the
tested local runtime. They do not establish that release-v3 used these new
limits, that the executor is sandboxed or production-safe, or that any query is
authorized for a particular human user.

