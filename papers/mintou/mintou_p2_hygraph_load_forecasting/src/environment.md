# Environment

Current smoke experiments use Python standard library only.

Run:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_experiments
```

Run the public OPSD and SimBench benchmarks:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_real_load_forecasting
```

This command also regenerates rolling temporal split results:

- `evidence/runs/real_opsd_rolling_results.csv`
- `evidence/runs/real_simbench_rolling_results.csv`

Future public benchmark runs may require pandapower, numpy, scipy, torch, grid2op, or other task-specific dependencies.
