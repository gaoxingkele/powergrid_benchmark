# Environment

Current smoke experiments use Python standard library only.

Run:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_experiments
```

Future public benchmark runs may require pandapower, numpy, scipy, torch, grid2op, or other task-specific dependencies.
## Public Benchmark-Derived Run

Run from repository root:

```powershell
$env:PYTHONPATH='src'; python papers\mintou\mintou_p5_trace_moea_feasibility_review\src\code\run_real_project_review.py
```

Primary module: `src/powergrid_benchmark/mintou_real_project_review.py`.

Inputs:

- `data/public_datasets/production_cost/rts-gmlc/RTS_Data/SourceData`
- `data/public_datasets/grid_cases/simbench/simbench/networks/1-complete_data-mixed-all-0-sw`
- `data/public_datasets/reliability_reports/c2ges_nerc_reports`
