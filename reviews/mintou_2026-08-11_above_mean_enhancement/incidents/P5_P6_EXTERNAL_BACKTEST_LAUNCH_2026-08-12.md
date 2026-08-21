# P5/P6 external-backtest launch incident — 2026-08-12

- Command: `python -m powergrid_benchmark.mintou_review_backtest`
- Working directory: `D:\aicoding\powergrid_benchmark`
- Outcome: failed before experiment initialization with `ModuleNotFoundError: No module named 'powergrid_benchmark'`.
- Cause: the system Python process did not include the repository `src` directory on `PYTHONPATH`.
- Data impact: none. No result table was generated or overwritten; the pre-atomic-substitution backtests had already been copied to explicitly suffixed provenance files.
- Corrective action: run the same frozen module from a fresh process with `PYTHONPATH=src`. The failed launch is excluded from all manuscript evidence.
