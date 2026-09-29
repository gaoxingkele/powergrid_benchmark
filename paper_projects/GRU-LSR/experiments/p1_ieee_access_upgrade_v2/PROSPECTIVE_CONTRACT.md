# Prospective IEEE Access Upgrade Contract

Status: **frozen before v2 execution**. This document explains the normative
machine contract in `upgrade_contract.json`. If prose and JSON differ, the JSON
controls. No v2 result, result directory, run manifest, estimate, p-value,
ranking, or effect direction is created or inspected in this stage.

## 1. Evidence and claim boundary

The existing v1 title, abstract, contributions, RQs, figures, tables,
discussion, conclusion, negative results, null results, onset-inapplicability
finding, and evidence qualifications remain unchanged. They are preserved by
SHA-256 bindings to `manuscript/MANUSCRIPT.md`,
`manuscript/TABLE_TO_CONFIG_MANIFEST.md`, and
`manuscript/DEEP_REVISION_EVIDENCE.md`. Existing numbers remain v1 evidence;
they are not prospective v2 outcomes and may be replaced only by a later
evidence-validated results-narrative stage.

The task remains a retrospective delivery-row lag benchmark on the first 8760
of 8784 hashed RTS-GMLC rows. The sequence ends on December 30 and is neither a
complete calendar year nor an independent multi-year sample. Its fixed
SNSP-type cap creates a proxy, not observed curtailment, an operator action,
OPF/UC output, or an economic outcome. Forecast issue times, as-of mappings,
release identifiers, and vintages are absent. The 1 h and 24 h tasks therefore
remain retrospective lags, not operational forecasts or dispatch evidence.

Human metadata is outside this stage. Author, affiliation, corresponding-author,
ORCID, funding, CRediT, conflict, biography, photograph, and disclosure
placeholders remain untouched and may not be inferred.

## 2. Frozen task grid and temporal gate

All conditions use caps 0.60, 0.70, and 0.80, with 0.70 primary. Cap 0.60 and
0.80 readouts and every cross-cap comparison are descriptive on the same fixed
sequence. No cap is selected after test inspection. The horizons are exactly
1 h and 24 h, the window is 48 rows with seven fit-standardized features, and
the ten common seeds are 11, 23, 47, 59, 71, 83, 97, 109, 127, and 139.

Delivery-row indices are zero-based and intervals below are half-open:

| Horizon | Fit targets | Selection targets | Calibration targets | Test targets | Counts: fit/selection/calibration/test |
|---:|---|---|---|---|---:|
| 1 h | `[48,4380)` | `[4381,5256)` | `[5257,6132)` | `[6133,8760)` | 4332 / 875 / 875 / 2627 |
| 24 h | `[71,4380)` | `[4404,5256)` | `[5280,6132)` | `[6156,8760)` | 4309 / 852 / 852 / 2604 |

The three horizon-length embargoes begin at 4380, 5256, and 6132. Their purpose
is to place the query endpoint `s=t-h` inside the downstream phase. Earlier
phase history within the 48-row query window remains permitted, as in v1.
Normalization, learned parameters, Ridge coefficients, and retrieval banks use
fit data only. Checkpoints, Ridge penalties, and the learned-space head weight
use selection data only. Detection thresholds use calibration data only. Test
data are scored once and cannot select any artifact, retry, family, or wording.

## 3. Architectures and common budget

GRU and LSTM each have one unidirectional layer, hidden size 48, zero dropout,
and a linear scalar head from the last time step. DLinear uses a centered
25-row moving average with endpoint replication, shared `Linear(48,1)` trend
and seasonal temporal maps applied featurewise, and a `Linear(7,1)` feature
head. TCN uses a `Conv1d(7,48,1)` input projection and two causal residual
blocks, with two kernel-3 convolutions per block, dilations 1 and 2, 48
channels, ReLU, zero dropout, and a scalar head from the final time step.
Architectures are not claimed to be parameter-count matched.

Every architecture receives the same fit-only budget: float32 MSE training,
manual Adam with learning rate 0.001, betas 0.9/0.999, epsilon 1e-8, no weight
decay or gradient clipping, batch size 256, 20 epochs, and checkpoints at
5/10/15/20. There are exactly 240 training trajectories: 3 caps x 2 horizons x
4 architectures x 10 seeds. MAE and onset-F1 objectives select independently
from the same four stored checkpoints; they do not receive separate training
runs. No extra seed, restart, checkpoint, epoch, early-stopping budget, or
result-triggered tuning is allowed.

For each architecture and objective, its direct head selects the checkpoint
first. Learned GRU retrieval then uses the frozen head-selected checkpoint.
The learned k=8 selected blend searches head weights in the ordered grid
`[1.0, 0.8, 0.6, 0.5, 0.4, 0.2, 0.0]`. Exact ties retain the earliest frozen
candidate. Selection uses unclipped predictions, matching the v1 executable
order; final calibration and scoring clip predictions to `[0,1]`.

## 4. Baselines, retrieval spaces, and k sensitivity

Persistence predicts `y_(t-h)`. Seasonal-24h predicts `y_(t-24)` and is an
explicit identity check against Persistence at h=24. Ridge uses the flattened
normalized window without an intercept; fit-only coefficients are computed for
penalties `[1e-6,1e-4,1e-3,1e-2,1e-1,1,10]`, selected separately by objective.
These three conditions are comparison baselines. Persistence, Seasonal-24h,
and Ridge comparisons are descriptive and receive no seed-based p-value.
`DirectPolicyTransform-Privileged` remains a construction/visibility audit and
is never ranked as a forecaster.

Retrieval always uses the fit-target bank, Euclidean distance, deterministic
lowest-index tie breaking, and the unweighted mean of neighbor targets. The
three spaces are:

- learned: the 48-dimensional last-time-step output of the forecasting-trained,
  head-selected GRU;
- raw: the flattened 336-dimensional fit-standardized input window;
- randomized: the 48-dimensional output of an untrained one-layer GRU created
  from the same common seed with zero training updates.

Every space is evaluated at k=4, 8, 16, and 32. k=8 is primary; k=4/16/32 are
descriptive sensitivity and are never selected from test results. An advantage
of the *learned space* may be stated only if both named attribution controls
have complete valid k=8 rows and the learned-versus-raw and
learned-versus-randomized paired contrasts warrant the direction stated. A
learned-versus-head contrast alone cannot support learned-geometry attribution.

## 5. Complete row contract and failures

There are 19 seeded conditions for every cap-horizon-objective-seed cell: four
architecture heads; learned, raw, and randomized retrieval-only conditions at
four k values each; and learned-k8 selected, fixed-0.5, and fixed-1 blends.
This gives 2280 seeded rows. Three objective-free deterministic rows per
cap-horizon give 18 more rows, and objective-selected Ridge gives 12 rows.
The required total is therefore **2310 rows**, with 385 per cap-horizon, 770 at
the primary cap, and 1540 at sensitivity caps.

Every expected key is emitted even after a condition fails. A failed row keeps
its key, records a controlled failure code and sanitized exception class, and
uses null scientific metrics. Dependent rows inherit the failure. Seeds are
not replaced; architectures, metrics, batch sizes, or methods are not
substituted; failed values are not imputed; and results do not trigger retries
or tuning. Complete protocol evidence requires all 2310 keys and completed
status for every evidence-bearing row.

A valid completed effect may be favorable, null, mixed, or adverse. Effect
direction never changes execution status or protocol validity. Likewise,
`fallback_no_positive_onsets` is a scientific-support state rather than an
execution failure. If selection or calibration has zero positive onsets, the
audit row and diagnostic metrics remain, but `onset_targeted_claim_valid` is
false. A tie produced by that fallback is not proof of no onset effect.

## 6. Paired effects, exact tests, and seed interval

Primary inference uses cap 0.70, k=8, and the ten common paired seeds. Every
contrast reports treatment-minus-control mean and median differences, sample
SD, paired standardized mean difference `dz`, and win/tie/loss counts. If the
paired SD is zero, `dz` is null with a zero-variance flag.

The two-sided exact sign-flip test enumerates all 1024 sign assignments,
including zero differences, and uses the absolute mean difference. There is no
plus-one correction. Holm adjustment is separate for each frozen family and
horizon; caps, objectives, horizons, and families are never pooled.

The families are:

| Family | Objective / metric | Frozen contrasts per horizon |
|---|---|---:|
| `primary_mae_mechanism_attribution` | MAE / continuous MAE | 6 |
| `architecture_head_mae` | MAE / continuous MAE | 3 |
| `onset_f1_diagnostic` | onset F1 / onset F1 | 6 |

The six primary MAE contrasts cover selected learned versus the GRU head,
learned retrieval versus the head, fixed-half versus the head, learned
retrieval versus fixed-half, learned versus raw retrieval, and learned versus
randomized retrieval. The architecture family compares the GRU head separately
with LSTM, DLinear, and TCN heads. Architecture-superiority language is licensed
only for the named contrast, horizon, metric, cap, and adjusted family actually
observed; it is not a gate for the benchmark contribution. The onset family
uses the analogous mechanism/attribution contrasts, but remains diagnostic
whenever pre-test onset support is absent.

Each paired contrast also reports the frozen 95% seed-conditional t interval

`mean(d) +/- 2.2621571627409915 * sample_sd(d) / sqrt(10)`.

The interval describes training-seed variability conditional on the ten seeds,
sequence, cap, horizon, protocol, and contrast. It is not uncertainty over
hours, blocks, years, systems, policies, vintages, operators, or deployments.

## 7. Supplementary moving-block analysis

The supplementary dependence sensitivity covers the nine primary-cap MAE
contrasts from the primary mechanism/attribution and architecture families.
For test target t and paired seed s, its loss difference is

`d_(s,t) = |y_t - clipped_treatment_(s,t)| - |y_t - clipped_control_(s,t)|`.

The chronological series resampled is `d_t`, the mean of `d_(s,t)` across all
ten paired seeds. Its length is 2627 at 1 h and 2604 at 24 h.

Use the ordinary overlapping moving-block bootstrap without circular wrap at
block lengths 24 and 168. Form all `n-L+1` consecutive blocks, draw
`ceil(n/L)` starts with replacement, concatenate the blocks, truncate to n,
and record the mean. Run exactly 5000 repetitions with NumPy `PCG64`. Reset the
generator for each contrast and use common resamples across contrasts. The
literal RNG seeds are 610024 (1 h, L=24), 610168 (1 h, L=168), 624024 (24 h,
L=24), and 624168 (24 h, L=168). Report the unresampled mean and the 2.5/97.5
percentiles with linear quantile interpolation.

Both block lengths are a descriptive dependence sensitivity on the single
observed sequence. Their intervals are not confidence intervals across years
or systems, do not enter Holm decisions, and do not override the seed-paired
analysis. Missing predictions or a missing paired seed make the affected cell
incomplete; they are never imputed.

## 8. Validity and IEEE Access interpretation gate

Protocol validity and effect direction are separate decisions. A complete,
leakage-free run with null, mixed, or adverse findings remains a valid bounded
benchmark result. It can support the auditable retrospective benchmark and its
failure-aware comparison protocol, but not a favorable method claim. Negative
comparisons, ties, naive-baseline wins, onset inapplicability, and cap crossings
must remain aligned across results, discussion, and conclusion with their scope
qualifiers. Combined ablations support only joint conclusions; proxy and
historical studies retain their original scope.

The IEEE Access clear-advance gate requires both:

1. complete protocol-valid v2 evidence under this contract; and
2. Stage-4 verified literature positioning of the auditable benchmark.

It does not require every model comparison to be favorable, GRU to win both
horizons, retrieval to beat every baseline, or every Holm family to be
significant. If Stage-4 literature positioning is not verified, clear advance
remains unverified even after a complete experiment. No systematic-review,
global-SOTA-exclusion, or external-domain-expert claim is licensed here.
