# Rolling Forecasting Analysis - simbench

Status: rolling temporal split benchmark over train ratios `0.55, 0.65, 0.75`. Primary rolling metric: `normalized MAE`.

## Horizon 1h

- Proposed mean normalized MAE: `0.04347893` +/- `0.00144896`
- Best baseline: `Persistence` with mean normalized MAE `0.04401900`
- Best ablation: `Ablation-NoCalendar` with mean normalized MAE `0.04324563`
- Relative gain over best baseline: `1.24%`
- Relative gain over best ablation: `-0.54%`
- Rolling value signal: `rolling_limitation`

## Horizon 24h

- Proposed mean normalized MAE: `0.07951836` +/- `0.00283821`
- Best baseline: `Persistence` with mean normalized MAE `0.08361752`
- Best ablation: `Ablation-NoCalendar` with mean normalized MAE `0.09887603`
- Relative gain over best baseline: `5.15%`
- Relative gain over best ablation: `24.34%`
- Rolling value signal: `promising_rolling_signal`

## Boundary

Rolling split results improve evidence quality but remain lightweight standard-library benchmarks. SimBench MAPE is retained in the CSV tables, but normalized MAE is the primary rolling metric because several feeder-profile hours have near-zero load denominators.
