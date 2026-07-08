# Stage 10 Experiment Package

This executor-repaired package implements the approved C1-C5 MA-SQLGrid
experiment contract from `pipeline/runs/run_001/stage-09/exp_plan.yaml`.

## Scope

- Dataset: `data/griddb_maintenance_v2_v0_1/`.
- Formal split: `Q021`-`Q200` test records.
- Smoke split: dev records only, enabled with `MA_SQLGRID_RUN_MODE=smoke`.
- Formal pass count: one deterministic pass per C1-C5 condition, labeled
  `seed=0` for reproducibility bookkeeping only.
- Smoke pass count: dev-smoke contract evidence uses seeds `[0, 1, 2]`.
- Model/provider: `gpt-5.4-mini` via Krill responses API, temperature 0.
- Conditions: `C1_SchemaOnly_Direct`, `C2_FullSchemaValues_Direct`,
  `C3_CHESSLite_Generic`, `C4_MASQLGrid_DomainContext`,
  `C5_MASQLGrid_DomainContext_Validated`.

## Gold-Leakage Boundary

Prediction prompts, traces, candidate selection, repair prompts, and prediction
records do not include gold SQL, gold result rows, evaluator correctness,
dataset answer metadata, required-literal metadata, or order-sensitive metadata.
Dataset metadata is used only after prediction for scoring and diagnostics.

## Outputs

The runner writes:

- `outputs/predictions.jsonl`
- `outputs/scores.jsonl`
- `outputs/contexts.jsonl`
- `outputs/report.md`
- `outputs/results.json`
- `results.json`

Stdout includes parseable `REGISTERED_CONDITIONS`, per-seed condition metrics,
`SUMMARY`, and `ABLATION_CHECK` lines for downstream stages.

The runner resolves the paper workspace from `MA_SQLGRID_WORKSPACE` when set,
then by searching parent directories, and finally by the fixed approved
workspace path. This keeps Stage 12 sandbox copies connected to the checked-in
dataset and evaluator without copying gold artifacts into prompts.

## Harness Protocol

Paper-Harness ad hoc review `run_20260622-173217` selected
`PROCEED_WITH_PROTOCOL_B`: formal Stage 12 must use the complete test split
once per condition, not three formal seeds. Downstream analysis may use paired
per-question comparisons over the 180 test questions, but must not claim
multi-seed variance or seed robustness.
