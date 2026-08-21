# P5/P6 figure-script relative-path incident — 2026-08-12

- Affected scripts: the manuscript-local `make_figures.py` files for P5 and P6.
- Outcome: both invocations failed before reading their evidence CSVs because their repository-root calculations resolved to `paper_projects` and consequently requested a nonexistent `paper_projects/papers/...` path.
- Data impact: none. No experimental CSV or existing figure was overwritten by either failed invocation.
- Corrective action: changed the fixed parent index to the actual repository root (`parents[4]` from the P5 script file and `parents[3]` from the P6 figure directory), then reran each script from a fresh process.
- Evidence status: the failed launches are excluded; only figures generated after the corrected path resolution may be used.
