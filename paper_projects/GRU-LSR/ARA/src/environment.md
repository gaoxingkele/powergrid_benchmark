# Environment

Current smoke experiments use Python standard library only.

Run:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_experiments
```

Run the public RTS-GMLC dispatch benchmark:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_real_dispatch
```

This command regenerates fixed, rolling, and pressure-subset RTS-GMLC evidence:

- `evidence/runs/real_rts_dispatch_results.csv`
- `evidence/tables/real_rts_dispatch_rolling_summary.csv`
- `evidence/tables/real_rts_dispatch_stress_leaderboard.csv`

Future public benchmark runs may require pandapower, numpy, scipy, torch, grid2op, or other task-specific dependencies.
