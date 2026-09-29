# Environment

Current smoke experiments use Python standard library only.

Run:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_experiments
```

Run the public SimBench planning benchmark:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_real_planning
```

Current public benchmark-derived run uses Python standard library only and reads SimBench `Load.csv`, `Line.csv`, and `RES.csv`.

`pandapower` is not installed in the current environment, so AC load-flow validation is still pending. Future public benchmark runs may require pandapower, numpy, scipy, torch, grid2op, or other task-specific dependencies.
