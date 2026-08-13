# P1 S3 fair experiment namespace

`p1_s3_fair_v1` is append-only with respect to the frozen v5/v6 evidence. It
does not write to `../../papers/.../evidence` and does not rename or remove any
prior run.

The run applies one symmetric information gate to Ridge and the learned GRU
conditions: fit-only normalization and fitting, selection-only checkpoint,
ridge-penalty, and blend choice, calibration-only onset thresholds, and a
horizon embargo before every downstream phase. The same selected GRU
checkpoint is used for retrieval-on, retrieval-off, and fixed-blend controls.
This separates retrieval presence from the MAE versus onset-F1 selection
objective.

The `DirectPolicyTransform-Privileged` control is included because the three
inspected `DAY_AHEAD_*` files contain load, wind, and PV rows for each target
delivery hour. It directly applies the label-generating rule to those target
rows. It is intentionally privileged and partly circular: it diagnoses what
happens if target-hour inputs are admitted, but it is not an operational
forecast because the source has no issue timestamp, as-of mapping, or vintage.

Cap 0.70 is primary. Caps 0.60 and 0.80 are method-level sensitivity reruns on
the same source series and protocol. Cross-cap differences are descriptive;
they are not additional independent weather years or systems.

## Frozen command

The exact executed command and environment are recorded in `run_manifest.json`
and `logs/run.log`. The script refuses to overwrite a completed namespace.

```powershell
$env:PYTHONPATH='D:\aicoding\powergrid_benchmark\.venv_mintou_cuda\Lib\site-packages'
& 'C:\Users\10175\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  experiments\p1_s3_fair_v1\run_fair_experiments.py `
  --rts-data 'D:\aicoding\powergrid_benchmark\data\public_datasets\production_cost\rts-gmlc\RTS_Data'
```

## Outputs

- `results/run_results.csv`: method-seed results and selected settings.
- `results/leaderboard.csv`: method-level aggregates.
- `results/paired_primary.csv`: paired-seed primary contrasts at cap 0.70.
- `results/cap_sensitivity.csv`: descriptive method-level cap changes.
- `results/policy_transform_audit.csv`: applicability and direct-control audit.
- `run_manifest.json`: hashes, environment, completion state, and output index.
- `EXPERIMENT_RESULT.md`: evidence-bound run report with a Material Passport.

Do not merge these results into the manuscript narrative during this stage;
that is the separately approved P1 S4 objective.
