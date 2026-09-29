# Real SimBench Forecasting Analysis - HyG-LoadFormer

Status: public data benchmark. This result uses cached SimBench load data and Python standard library implementation.

## Horizon 1h

- Proposed MAPE: `0.14812336`
- Best baseline: `Persistence` with MAPE `0.14812336`
- Best ablation: `Ablation-NoCalendar` with MAPE `0.19855467`
- Relative gain over best baseline: `0.00%`
- Relative gain over best ablation: `34.05%`
- Proposed normalized MAE: `0.04316202`
- Best normalized-MAE baseline: `Persistence` with normalized MAE `0.04316202`
- Best normalized-MAE ablation: `Ablation-NoCalendar` with normalized MAE `0.04331806`
- Relative normalized-MAE gain over best baseline: `0.00%`
- Relative normalized-MAE gain over best ablation: `0.36%`
- Current value signal: `needs_compliant_optimization`

## Horizon 24h

- Proposed MAPE: `0.41451949`
- Best baseline: `Weekly-168h` with MAPE `0.41451949`
- Best ablation: `Ablation-NoCalendar` with MAPE `0.69330349`
- Relative gain over best baseline: `0.00%`
- Relative gain over best ablation: `67.25%`
- Proposed normalized MAE: `0.09253661`
- Best normalized-MAE baseline: `Persistence` with normalized MAE `0.08103131`
- Best normalized-MAE ablation: `Ablation-NoCalendar` with normalized MAE `0.09513336`
- Relative normalized-MAE gain over best baseline: `-12.43%`
- Relative normalized-MAE gain over best ablation: `2.81%`
- Current value signal: `needs_compliant_optimization`

## Interpretation Boundary

This benchmark validates a second public dataset and feeder/profile-level forecasting task. Manuscript-level claims still require rolling temporal splits and, ideally, stronger neural baselines.
