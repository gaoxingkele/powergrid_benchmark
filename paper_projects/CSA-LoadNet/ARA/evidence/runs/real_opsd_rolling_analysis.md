# Rolling Forecasting Analysis - opsd

Status: rolling temporal split benchmark over train ratios `0.55, 0.65, 0.75`. Primary rolling metric: `MAPE`.

## Horizon 1h

- Proposed mean MAPE: `0.02381135` +/- `0.00341692`
- Best baseline: `Euclidean-GCN Ridge` with mean MAPE `0.02350066`
- Best ablation: `Ablation-NoCalendar` with mean MAPE `0.02007022`
- Relative gain over best baseline: `-1.30%`
- Relative gain over best ablation: `-15.71%`
- Rolling value signal: `rolling_limitation`

## Horizon 24h

- Proposed mean MAPE: `0.03931968` +/- `0.00055769`
- Best baseline: `Weekly-168h` with mean MAPE `0.05471780`
- Best ablation: `Ablation-FixedCurvature` with mean MAPE `0.07061538`
- Relative gain over best baseline: `39.16%`
- Relative gain over best ablation: `79.59%`
- Rolling value signal: `promising_rolling_signal`

## Boundary

Rolling split results improve evidence quality but remain lightweight standard-library benchmarks. They should be treated as reproducibility and stability evidence rather than final neural-training results.
