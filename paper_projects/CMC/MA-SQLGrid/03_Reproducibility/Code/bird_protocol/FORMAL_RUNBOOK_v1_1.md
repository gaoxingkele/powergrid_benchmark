# MA public BIRD baseline formal runbook — protocol v1.1

## Preconditions

Do not execute until all of the following are true:

1. `BASELINE_PROTOCOL_FREEZE_v1_1.json` is `FROZEN_NOT_RUN`.
2. `INDEPENDENT_TECHNICAL_FREEZE_AUDIT_v1_1.json` is `PASS` and binds the
   exact v1.1 freeze SHA-256.
3. A real human approval binds that exact hash, acknowledges 5,000 new calls
   and the 7,476 maximum physical-call total, and excludes both incidents.
4. Ports 8091 and 8092 are unused and no competing `llama-server` is active.

The two backbones run sequentially.  A failed run is retained, never resumed
or overwritten.  No partial score enters the manuscript.

## Required runtime

Formal runner and SQLite evaluation must use:

`runtime_compat/python31011/python.exe` — Python 3.10.11, SQLite 3.40.1.

The embedded interpreter has an isolated module path.  Invoke the runner with
a small `runpy` launcher that inserts this protocol directory into `sys.path`;
the launcher must assert the Python and SQLite versions before execution.

## Qwen then Granite

Start each pinned `llama-server` with the unchanged v1.0 arguments and a
loopback-only port.  Invoke `run_formal_public_baseline_v1_1.py` through the
pinned interpreter, first for Qwen on port 8091 and only after its 2,500-call /
2,000-final-row manifest passes, for Granite on port 8092.

Use new, non-overlapping output directories such as:

- `MA_PUBLIC_BIRD_v1_1_qwen_clean1`
- `MA_PUBLIC_BIRD_v1_1_granite_clean1`

## Post-run gate

A separate auditor must verify 5,000 unique call rows, 4,000 final rows, zero
retries, model/prompt/data/runtime hashes, incident exclusion, and direct
re-execution under SQLite 3.40.1 before regenerating database-clustered
intervals and Holm-adjusted tables.  Only audited outputs may enter the paper.

