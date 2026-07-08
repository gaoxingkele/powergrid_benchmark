# Configs

Shared JSON configs for power-system datasets, benchmark systems, models, metrics, splits, and experiment runs.

```text
configs/
  datasets/       Dataset profiles and local path contracts.
  experiments/    Runnable experiment definitions.
  metrics/        Metric sets for forecasting, classification, OPF, RL, and robustness.
  models/         Baseline and paper-model config fragments.
  splits/         Reusable train/validation/test splits.
  systems/        Grid-system definitions such as IEEE bus cases or regional grids.
```

Validate the scaffold and sample configs with:

```powershell
python scripts/validate_scaffold.py
pytest
```
