# P2 v8 CUDA Transfer Pilot Incident Record

- Start: 2026-08-11 21:22:40 Asia/Shanghai
- Stop: 2026-08-11 21:25:20 Asia/Shanghai
- Command: workspace CUDA Python 3.12, `python -u -m powergrid_benchmark.mintou_hierarchy_reconciliation`
- Environment: Torch 2.13.0+cu130, RTX 3090, deterministic cuDNN mode
- Observed state: CUDA was active at approximately 70% utilization, but the first 10-epoch unit did not complete in about 160 seconds. Process profiling showed approximately four saturated CPU cores because every batch constructed the 17-series windows on CPU before transfer.
- Action: terminated as an execution-path performance pilot before any model--seed unit completed.
- Evidence handling: no result, leaderboard, or partial result file was produced; this pilot is excluded from all manuscript results.
- Retry rule: keep the frozen scientific protocol unchanged and move the same normalized tensors/window indexing to the selected execution device once per run, eliminating repeated host-to-device window transfer.

