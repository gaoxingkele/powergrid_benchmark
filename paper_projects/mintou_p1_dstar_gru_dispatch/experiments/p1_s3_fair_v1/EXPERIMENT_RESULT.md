## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run
- Origin Date: 2026-08-13T08:53:11Z
- Verification Status: UNVERIFIED
- Version Label: p1_s3_fair_v1_exp_result_v1
- Upstream Dependencies: frozen v6 task definition; hashed RTS-GMLC load/wind/PV/branch inputs

# Experiment Result

**Experiment ID:** `p1_s3_fair_v1`

**Type:** training, retrieval-mechanism controls, and deterministic analysis

**Status:** COMPLETED

**Result rows:** 510
**Primary analysis:** paired exact sign-flip tests over ten common seeds at cap 0.70, Holm-adjusted within each horizon

The run used disjoint fit, selection, calibration, and test phases with
horizon embargoes. Ridge penalties, GRU checkpoints, and retrieval blends used
selection rows only; thresholds used calibration rows only. Raw-source and
output hashes, the exact command, and the environment are in
`run_manifest.json`.

## Primary cap-0.70 findings

- The privileged direct policy transform has zero MAE and onset MAE at both
  lags by construction. It uses target-hour `DAY_AHEAD_*` rows and is not an
  operational forecast because issue timestamps and vintages are absent.
- MAE-selected retrieval chooses `alpha_head=0` for every seed. Relative to the
  matched GRU head, its paired mean MAE difference is -0.00496069 at 1 h and
  -0.00220055 at 24 h; all ten pairs favor retrieval-only and Holm
  `p=0.01171875` at each lag.
- Persistence remains lower-MAE than the selected GRU condition: 0.00690794
  versus 0.00777391 at 1 h and 0.02054651 versus 0.02076857 at 24 h.
- Fixed 0.5 blending improves GRU-head MAE in all ten pairs at both lags, but
  retrieval-only remains lower-MAE than fixed 0.5 in all pairs.

## Negative, null, and inapplicable evidence

Every selection and calibration phase has zero positive onsets at both lags
and at caps 0.60, 0.70, and 0.80. The onset-targeted arms therefore use the
frozen tie fallback: checkpoint 5 and `alpha_head=1`. Their selected retrieval
condition equals the no-retrieval head in all cap-0.70 pairs (`p=1`). This does
not estimate an onset-targeted retrieval effect.

The perfect continuous direct transform does not achieve onset F1 of one
(0.3333 at 1 h; 0.7527 at 24 h under cap 0.70) because the inherited onset
classifier flags ongoing high-curtailment rows as well as transitions. This is
a metric-definition limitation, not direct-control prediction error.

Cap sensitivity is descriptive on the same system/year. The selected GRU
condition is slightly lower-MAE than Persistence only at cap 0.60/1 h and cap
0.80/24 h; Persistence is lower in the other four cap/lag cells. The fair run
does not contain the complete v6 method roster and cannot establish a new
overall leaderboard.

## Environment anomaly retained

The compatible preserved PyTorch environment lacks `sympy`, which the packaged
`torch.optim` dynamo wrapper imports. The failed smoke trace is retained in
`logs/smoke.log`. The completed run uses the eager Adam equations with the
frozen standard parameters; `logs/smoke2.log` records the successful smoke.
Deterministic cuDNN, disabled cuDNN benchmarking, fixed seeds, and
`CUBLAS_WORKSPACE_CONFIG=:4096:8` were used. PyTorch's global deterministic-
algorithm enforcement was unavailable and is recorded as false in the
manifest.

## Output files

- `results/run_results.csv`
- `results/run_results.completed_snapshot.csv`
- `results/leaderboard.csv`
- `results/paired_primary.csv`
- `results/cap_sensitivity.csv`
- `results/policy_transform_audit.csv`
- `run_manifest.json`
- `logs/run.log`

No independent rerun has been performed, so this run artifact remains
`UNVERIFIED` under the experiment workflow's reproducibility status rules.
The required evidence acceptance command passed after supplying the read-only
source workspace for the shared regression module absent from this checkout;
the failed and successful import attempts are documented in `logs/README.md`.
