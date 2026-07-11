# Real OPSD Forecasting Analysis - HyG-LoadFormer

Status: public data benchmark v1. This result uses the cached OPSD 60-minute single-index load data and Python standard library implementation.

## Horizon 1h

- Proposed MAPE: `0.02244670`
- Best baseline: `Euclidean-GCN Ridge` with MAPE `0.02250389`
- Best ablation: `Ablation-NoCalendar` with MAPE `0.02068559`
- Relative gain over best baseline: `0.25%`
- Relative gain over best ablation: `-7.85%`
- Current value signal: `needs_compliant_optimization`

## Horizon 24h

- Proposed MAPE: `0.06910397`
- Best baseline: `Weekly-168h` with MAPE `0.05632632`
- Best ablation: `Ablation-FixedCurvature` with MAPE `0.06915059`
- Relative gain over best baseline: `-18.49%`
- Relative gain over best ablation: `0.07%`
- Current value signal: `needs_compliant_optimization`

## Interpretation Boundary

The experiment is a lightweight public-data benchmark, not a final deep-learning training run. It is suitable for validating the load-forecasting task definition, baseline matrix, graph-feature contribution, and ARA evidence path. A manuscript-level claim still requires broader repeated runs, stronger neural baselines, SimBench feeder-level validation, and statistical testing.

## Compliant Optimization Path

- Add SimBench feeder profiles as a second public dataset.
- Tune graph weighting and lag-window design on validation splits only.
- Add variance over rolling temporal splits.
- Preserve weak horizons and failed variants in the ARA trace.
