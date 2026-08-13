# Supplementary Methods and Audit Record

This supplement retains implementation timing, software/version history,
hashes, and incident detail that are not scientific outcomes and are therefore
excluded from the main Results narrative. Scientific interpretation remains
governed by `DEEP_REVISION_EVIDENCE.md` and the completed fair-run manifest.

## S1. Fair-run identity and frozen command

- Run namespace: `p1_s3_fair_v1`
- Primary start/completion: 2026-08-13 08:53:11--08:53:48 UTC
- Configuration SHA-256: `bb0a920069490b6c4fcbc015849358a653a3c3710c0c51a19bb8e782e74e2c69`
- Script SHA-256: `4f209a5faf1071aa2b7da78a7556aa331026f4581df8e759f17d8e568b7958fe`
- Frozen invocation: `run_fair_experiments.py --rts-data <RTS_Data> --device auto`
- Completed rows: 510 run rows, 78 leaderboard rows, 12 paired-primary rows,
  78 cap-sensitivity rows, and 10 policy-audit rows.

The absolute interpreter, worktree, and data paths remain in
`experiments/p1_s3_fair_v1/run_manifest.json`; they are machine-local audit
metadata and are not publication claims.

## S2. Source identity

| Input | Rows/bytes | SHA-256 |
|---|---:|---|
| RTS-GMLC load `DAY_AHEAD_regional_Load.csv` | 8784 rows / 432487 bytes | `6efb6e3e06f7f1cee0d59eaf33768e06c33c737beb875676433850d8659943ee` |
| RTS-GMLC wind `DAY_AHEAD_wind.csv` | 8784 rows / 288304 bytes | `b933f810511ce3d2128c490e4b230defcdc3c15ed4db0838c6fd4c62640e2208` |
| RTS-GMLC PV `DAY_AHEAD_pv.csv` | 8784 rows / 842651 bytes | `bfede6e558df5ea0f244b6326940a4ee0b95138643aa8a062897c67134c9c185` |
| RTS-GMLC `branch.csv` | 120 branches / 7263 bytes | `2f8f80f6f95ca46c2997646d56892436b50d7fb81163b680d06767bc3c1b179f` |

The source files contain 8784 rows, while the aligned experiment intentionally
preserves the historical construction by using their first 8760 delivery rows.
The first and last manifest delivery keys are 2020-01-01 period 1 and
2020-12-30 period 24. The executed sequence is therefore not a complete
calendar year. These are delivery keys; issue times and data vintages remain
unavailable. The frozen manifest's `cap_sensitivity_scope` retains the earlier
label "same system and weather year"; the recorded row counts and delivery keys
are authoritative, and publication-facing text uses "fixed 8760-row sequence."

## S3. Primary environment and determinism boundary

| Item | Primary run |
|---|---|
| Python | 3.12.13, MSC v.1944, 64 bit |
| NumPy | 2.3.5 |
| PyTorch | 2.13.0+cu130 |
| CUDA / device | CUDA 13.0 / NVIDIA GeForce RTX 3090 |
| cuDNN deterministic | true |
| cuDNN benchmark | false |
| `CUBLAS_WORKSPACE_CONFIG` | `:4096:8` |
| PyTorch global deterministic algorithms | false |

The preserved environment lacked `sympy`, which the packaged `torch.optim`
dynamo wrapper imported. The first smoke attempt therefore failed and is
retained in `experiments/p1_s3_fair_v1/logs/smoke.log`. The completed run uses
manual eager-mode Adam equations with the frozen standard parameters
($\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-8}$, learning rate
$10^{-3}$); the successful smoke is retained in `logs/smoke2.log`. The
manifest records that global deterministic-algorithm enforcement was not
available. No stronger determinism claim is made.

## S4. Manifest-listed primary outputs

| Output | Bytes | SHA-256 |
|---|---:|---|
| `run_results.csv` | 151756 | `6e8c169121882cfaf69fa67feb49f83768ae5c441ff027b059a676c89f85253b` |
| `run_results.completed_snapshot.csv` | 151756 | `6e8c169121882cfaf69fa67feb49f83768ae5c441ff027b059a676c89f85253b` |
| `leaderboard.csv` | 18396 | `6a84dbb2974c3964a63d396d01beab8049ba0af6742055b57dd06cc20e5d4a85` |
| `paired_primary.csv` | 1985 | `303d14a7fe9243815768d3ffb382bcd477687c3fd5337b71775630e5016c5b0d` |
| `cap_sensitivity.csv` | 9844 | `6320c5b70cdd904b15d5d4efbaf6ff109d061d4b72f7986206b0505b3463e210` |
| `policy_transform_audit.csv` | 2411 | `3c658c3e9773ddf1fcd0fe60c9e4b0bc209d3a6fb52c9f7ed1b904190c1d9208` |

## S5. Implementation timing

Timing is wall-clock implementation metadata, not an asymptotic or deployment
benchmark. GRU control rows share the same training/inference elapsed value
within an objective and seed; the value is not the incremental cost of an
individual blend.

At cap 0.70, the MAE-selected GRU rows have mean elapsed values of 0.6387771 s
at 1 h (range 0.553193--0.932679 s across ten seeds) and 0.5897739 s at 24 h
(range 0.563425--0.607335 s). The onset-objective rows have means of
0.6591314 s and 0.6099982 s. Deterministic Ridge rows require 0.0188--0.0199 s;
the direct transform and naive references require less than 0.0003 s in the
recorded run. These values describe this implementation on the recorded GPU
environment only. The supplementary figure
`figures/fig_runtime_error_tradeoff.png` visualizes the timing-bearing primary
rows and is intentionally not cited as a main scientific result.

## S6. Separate execution rerun

The separate verification parent reran the unchanged script and frozen
configuration from 2026-08-13 09:10:32 to 09:11:12 UTC. It used Python 3.12.10
and NumPy 2.4.6, while retaining PyTorch 2.13.0+cu130, CUDA 13.0, the RTX 3090,
the source hashes, seed list, and determinism settings above.

All non-timing fields in all 510 rows are identical. The leaderboard,
paired-primary, cap-sensitivity, and policy-audit CSVs are byte-identical to the
primary run. The timing-bearing raw result files are not byte-identical:

- Primary raw-results SHA-256:
  `6e8c169121882cfaf69fa67feb49f83768ae5c441ff027b059a676c89f85253b`
- Separate-rerun raw-results SHA-256:
  `f1896b8934f8ed8d5818f3814c717884d3cddf8ebfe8a52f10816a66cee3b5cd`

This supports reproduction of the scientific outputs by a separate execution.
It is not an external-investigator replication, a cross-hardware test, or
evidence beyond the original fixed 8760-row sequence and information boundary.

## S7. Legacy version history

The historical archives are retained for traceability but are not mixed into
the main fair-run Results:

| Version | Repository state | Methods / rows | Current role |
|---|---|---:|---|
| v5 `public_rts_curtailment_v5_onset_eval` | `3f0371eb5d775f5967ad59120e937d4804bd5a21` | 12 / 168 | Historical archive only |
| v6 `public_rts_curtailment_v6_modern_temporal_controls` | `a728800bd48b11bc8f07647f82e4c9c2841a3e45` | 14 / 208 | Historical full-roster evidence only |
| fair v1 `p1_s3_fair_v1` | append-only local namespace | 510 condition/seed rows | Sole main-result source |

All 15 scientific metric fields in the 168 method--lag--seed rows shared by v5
and v6 were recorded as identical; v6 added DLinear and TCN. This historical
fact does not validate those methods under the fair gate. The main paper
therefore makes no renewed v6 ranking or ablation claim.

## S8. Figure/table regeneration audit

`manuscript/figures/make_figures.py` performs the following fail-closed steps:

1. Read the completed fair manifest.
2. Verify the byte count and SHA-256 of every manifest-listed output.
3. Verify the 510-row count.
4. Derive the four `fair_*.csv` manuscript tables.
5. Regenerate PNG, PDF, and SVG-wrapper copies of each figure.
6. Record input and output hashes in `figures/artifact_manifest.json`.

The generated figures use only the fair-run manifest/config/results. The
compatibility filenames `fig_runtime_error_tradeoff` and
`fig_modern_baselines_transportability` are retained in the figure directory,
but their contents are regenerated from fair-run data and are not cited as old
v6/NREL scientific results.

## S9. Unresolved audit boundaries

- No public release URL or archival DOI has been supplied.
- The exact source release/vintage name beyond the hashed files is unresolved.
- No issue-time/vintage archive exists.
- No independent investigator or cross-hardware replication exists.
- No full legacy 14-method rerun under the fair gate exists.
- No raw-feature k-NN, randomized-encoder, alternative-distance, or $k$-sensitivity
  rerun under the fair gate exists; learned-space causality is not identified.
- No pre-test onset positives exist in any executed cap/lag arm.
- The experiment uses a truncated first-8760-row sequence rather than all 8784
  source rows or a complete calendar year.
- No observed-curtailment, OPF/UC, probabilistic, operator, deployment, or
  economic-outcome validation exists.
- Full-reference content verification, similarity/plagiarism screening, an
  external domain-expert review, and confirmation that the local IEEE Access
  class bundle matches the latest official download remain unverified.
