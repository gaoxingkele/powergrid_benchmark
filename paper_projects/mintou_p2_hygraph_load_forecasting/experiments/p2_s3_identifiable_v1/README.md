# P2 S3 identifiable experiment namespace

`p2_s3_identifiable_v1` is a new append-only namespace. It does not overwrite
the historical fixed-split or proxy rolling evidence under `../../papers`.
The driver refuses to run after a completed `run_manifest.json` exists.

The experiment is deliberately narrow: OPSD, scalar lead 24, six component
conditions, five common seeds, and eight quarterly rolling origins. It does
not rerun the historical external architecture screen. This equalizes seed
support within the new comparison family and avoids promoting the earlier
three-seed screen to confirmation.

The central control, `TargetSelfContext-Matched`, keeps the shared encoder,
48-dimensional context slot, 100-to-64-to-1 head, every instantiated
parameter, optimizer, epoch/batch schedule, seed list, and the parameterized
attention computation. It replaces the neighbor aggregate supplied to the
head with the value-mapped target encoding. The comparison therefore asks
whether cross-series content helps beyond an equally sized target-history
context, without the smaller-head defect of the historical TemporalOnly arm.

`UniformCrossSeries-Matched` supplies informative cross-series context using
the mean of the other five encoded histories while retaining the same
instantiated parameter and execution path. Euclidean and fixed-scale controls
retain the earlier weighting-form question. The independent-encoder arm has
the same total parameter count and downstream head, but its narrower
series-specific hidden layers use less encoder arithmetic; its result is
therefore scoped as a sharing-versus-width-allocation control, not a clean
causal estimate of weight sharing.

The inferential replicate is the rolling origin. Five seed runs are averaged
within each method-origin before testing. Hourly targets, series, forecast
days, and seeds are not treated as independent replicates. MAPE is primary;
WAPE is secondary. No equivalence margin was frozen, so failure to separate
weight forms remains a null result and is not evidence of equivalence.

## Frozen command

```powershell
$env:PYTHONPATH='D:\aicoding\powergrid_benchmark\.venv_mintou_cuda\Lib\site-packages'
& 'C:\Users\10175\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  experiments\p2_s3_identifiable_v1\run_identifiable_experiments.py
```

The exact executed command, environment, input hashes, and output hashes are
recorded in `run_manifest.json`. `--preflight` performs data, model, parameter,
and deterministic backward checks without writing experiment results.

## Expected outputs

- `results/run_results.csv`: one row per method, rolling origin, and seed.
- `results/day_metrics.csv`: forecast-day audit metrics; not the inferential
  unit.
- `results/origin_metrics.csv`: seed-averaged outer-unit metrics.
- `results/leaderboard.csv`: means and standard deviations over eight origins.
- `results/paired_comparisons.csv`: exact paired tests and bootstrap intervals.
- `EXPERIMENT_RESULT.md`: evidence-bounded run report.
- `VALIDATION_REPORT.md`: statistical interpretation and 11-type fallacy scan.
- `run_manifest.json`: immutable completion and provenance record.
