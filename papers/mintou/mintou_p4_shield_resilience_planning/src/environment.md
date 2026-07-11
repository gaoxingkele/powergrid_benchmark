# Environment

Current smoke experiments use Python standard library only.

Run:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_experiments
```

Run the public SimBench resilience-planning benchmark:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_real_planning
```

Future public benchmark runs may require pandapower, numpy, scipy, torch, grid2op, or other task-specific dependencies.
