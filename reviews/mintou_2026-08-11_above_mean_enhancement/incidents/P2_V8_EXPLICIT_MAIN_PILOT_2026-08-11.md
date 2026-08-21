# P2 v8 Explicit-Main Pilot Incident Record

- Start: 2026-08-11 21:30:44 Asia/Shanghai
- Stop: 2026-08-11 21:32:40 Asia/Shanghai
- Invocation: CUDA venv with the workspace `src` inserted at `sys.path[0]`, followed by a direct call to `mintou_hierarchy_reconciliation.main()`
- Observed state: the first unit again did not finish within about 116 seconds, despite a 3.8-second isolated call to the same training function and inputs.
- Action: terminated without a completed unit; no evidence or partial output was created.
- Audit conclusion: package-resolution drift is ruled out. The next invocation must use timed stage/stack instrumentation to locate the wrapper-only bottleneck before any complete rerun.

