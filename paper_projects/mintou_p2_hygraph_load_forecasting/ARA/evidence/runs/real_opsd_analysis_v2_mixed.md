# Real OPSD Forecasting Analysis - HyG-LoadFormer

Status: public data benchmark v2. This result uses the cached OPSD 60-minute single-index load data and Python standard library implementation.

Version note: v1 weak-result evidence is preserved in `real_opsd_analysis_v1_weak.md`, `real_opsd_forecasting_results_v1_weak.csv`, and `real_opsd_leaderboard_v1_weak.csv`. The v2 method is a compliant algorithm refinement: HyG-LoadFormer learns residual corrections over strong seasonal baselines instead of replacing them.

## Horizon 1h

- Proposed MAPE: `0.02244670`
- Best baseline: `Euclidean-GCN Ridge` with MAPE `0.02250389`
- Best ablation: `Ablation-NoCalendar` with MAPE `0.02068559`
- Relative gain over best baseline: `0.25%`
- Relative gain over best ablation: `-7.85%`
- Proposed normalized MAE: `0.00887378`
- Best normalized-MAE baseline: `Euclidean-GCN Ridge` with normalized MAE `0.00888464`
- Best normalized-MAE ablation: `Ablation-NoCalendar` with normalized MAE `0.00842894`
- Relative normalized-MAE gain over best baseline: `0.12%`
- Relative normalized-MAE gain over best ablation: `-5.01%`
- Current value signal: `needs_compliant_optimization`

## Horizon 24h

- Proposed MAPE: `0.03972575`
- Best baseline: `Weekly-168h` with MAPE `0.05632632`
- Best ablation: `Ablation-FixedCurvature` with MAPE `0.06915059`
- Relative gain over best baseline: `41.79%`
- Relative gain over best ablation: `74.07%`
- Proposed normalized MAE: `0.01621211`
- Best normalized-MAE baseline: `Weekly-168h` with normalized MAE `0.02405159`
- Best normalized-MAE ablation: `Ablation-EqualNeighbors` with normalized MAE `0.02588215`
- Relative normalized-MAE gain over best baseline: `48.36%`
- Relative normalized-MAE gain over best ablation: `59.65%`
- Current value signal: `promising_public_signal`

## Interpretation Boundary

The experiment is a lightweight public-data benchmark, not a final deep-learning training run. It is suitable for validating the load-forecasting task definition, baseline matrix, graph-feature contribution, and ARA evidence path. A manuscript-level claim still requires broader repeated runs, stronger neural baselines, SimBench feeder-level validation, and statistical testing.

## Compliant Optimization Path

- Add SimBench feeder profiles as a second public dataset.
- Tune graph weighting and lag-window design on validation splits only.
- Add variance over rolling temporal splits.
- Preserve weak horizons and failed variants in the ARA trace.
