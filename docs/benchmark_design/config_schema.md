# Benchmark Config Schema

Benchmark experiments use JSON files under `configs/experiments/`.

## Required Top-Level Fields

| Field | Purpose |
| --- | --- |
| `id` | Stable experiment identifier. |
| `task` | Task name such as `load_forecasting`, `opf`, `fault_detection`, `state_estimation`, or `grid_control`. |
| `domain` | Usually `power_grid`, or a more specific cyber-physical domain if needed. |
| `system` | Path to a grid-system config. |
| `dataset` | Path to a dataset config. |
| `split` | Path to a train/validation/test split config. |
| `model` | Path to a model or baseline config. |
| `metrics` | Path to metric-set config. |
| `outputs` | Run directory and report targets. |

## Evidence Rule

Experiment configs are not evidence by themselves. Results should be recorded in `experiments/runs/` and linked from the matching ARA `evidence/runs/` file.
