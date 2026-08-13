# Title-to-Evidence Map

## Binding paper story

The title is **A Reproducible Retrospective Curtailment-Risk Benchmark and Fair
Evaluation of GRU Learned-Space Retrieval on RTS-GMLC**.

| Title/contribution term | Evidence-supported meaning | Boundary that must travel with the claim |
|---|---|---|
| Reproducible | The completed manifest hashes the configuration, script, four source files, and six outputs. A separate execution reproduced all 510 non-timing fields and the four scientific derived tables byte-for-byte. | This is computational reproduction on the same GPU and source files, not external-investigator or cross-hardware replication. |
| Retrospective | A 48-row query ending at benchmark index $s$ predicts the proxy at delivery row $s+h$, $h\in\{1,24\}$. | Issue timestamps, as-of mappings, and source vintages are absent; no operational day-ahead claim is licensed. |
| Curtailment-risk | A fixed SNSP-type acceptance rule converts load, wind, and PV into a method-independent rate. | The label is a proxy, not observed curtailment, operator action, OPF/UC output, or economic outcome. |
| Benchmark | Common target, phase gate, lags, metrics, baselines, controls, and statistics are executable and manifest-bound. | One RTS-GMLC system and weather year identify every result. |
| Fair evaluation | Fit, selection, calibration, and test phases are disjoint and horizon-embargoed. GRU retrieval controls share the selected checkpoint within each objective. | The fair run covers a mechanism subset, not the full historical 14-method roster. |
| GRU learned-space retrieval | The same forecasting-trained GRU encoder maps query and fit-bank windows; $k=8$ retrieved targets are combined with the head by selected or fixed weights. | No contrastive/Siamese loss, digital twin, live synchronization, or deployment is implemented. |

## Aligned contributions

1. The benchmark contribution is a method-independent retrospective proxy task
   with an explicit information boundary and a privileged target-hour visibility
   audit.
2. The method contribution is a checkpoint-matched comparison of retrieval-only,
   equal-blend, and head-only predictions under two selection objectives.
3. The result contribution is conditional: retrieval lowers MAE relative to the
   matched head at both lags, Persistence remains lower-MAE at the primary cap,
   onset-targeted selection is inapplicable, and cap crossings are descriptive.

# Primary Estimand and Analysis Unit

The primary estimand is the mean paired within-seed treatment-minus-control
difference at cap 0.70, conditional on the fixed RTS-GMLC system-year, temporal
gate, feature/metric definitions, checkpoint budget, retrieval bank, selection
objective, and lag. Six frozen GRU contrasts per lag compare selected retrieval,
fixed 0.5 blending, and the matched head for MAE or onset F1.

The analysis unit is one paired method-seed run. Ten common training seeds are
available. The 2627 (1 h) and 2604 (24 h) test delivery targets, including 57
and 172 onset rows, are reused across seeds and are not treated as independent
replicates. Seed uncertainty covers training randomness only, not hours, onset
blocks, years, systems, policies, vintages, operators, or deployments.

The primary test is the two-sided exact sign-flip test. Holm adjustment is
applied over the frozen six-contrast family separately within each lag.
Deterministic methods and cross-cap comparisons have no seed-based p-value.

# Comparison Budget and Data Visibility

## Fair temporal gate

| Phase | Delivery-target rule | Permitted use | 1 h / 24 h targets |
|---|---|---|---:|
| Fit | before row 4380 | normalization, model fitting, Ridge coefficients, retrieval bank | 4332 / 4309 |
| Selection | `4380+h` through 5255 | Ridge penalty, GRU checkpoint, head weight | 875 / 852 |
| Calibration | `5256+h` through 6131 | detection threshold only | 875 / 852 |
| Test | at or after `6132+h` | scoring only | 2627 / 2604 |

The source loader retains delivery calendar keys. It does not retain forecast
issue time, an as-of mapping, release identifier, or revision/vintage field.
The fair gate prevents artifact building from using downstream delivery phases,
but it cannot establish an operational issue-time gate.

## Frozen comparison budget

| Item | Budget | Scope |
|---|---|---|
| Data | First 8760 aligned rows of the hashed RTS-GMLC load/wind/PV files plus static branch data | One system and weather year |
| Lags/caps | 1 h and 24 h; cap 0.70 primary; 0.60/0.80 sensitivity | Cross-cap values are descriptive |
| GRU | hidden 48, 20 epochs, checkpoints 5/10/15/20, ten common seeds | Training randomness only |
| Retrieval | fit-only bank, $k=8$, selected grid plus fixed head weights 0/0.5/1 | Checkpoint shared across controls within objective |
| Baselines | Persistence, Seasonal-24h, objective-selected Ridge | Deterministic descriptive references |
| Privileged control | Target-hour direct policy transform | Construction/visibility audit, not a forecast |
| Inference | Six paired GRU contrasts per lag | Exact sign flip plus within-lag Holm |

# Negative and Null Results

1. **Persistence remains lower-MAE at the primary cap.** Its MAE is 0.00690794
   versus 0.00777391 for selected GRU-LSR at 1 h and 0.02054651 versus
   0.02076857 at 24 h. These deterministic comparisons are descriptive.
2. **MAE selection chooses retrieval only.** Head weight is zero in all ten
   seeds at both lags. The result supports the retrieval estimator relative to
   the matched head, not a beneficial head/retrieval mixture.
3. **Every selection and calibration phase has zero positive onsets** at both
   lags and all three caps. Onset-targeted checkpoint/blend selection and
   threshold calibration use declared fallbacks.
4. **Selected onset GRU-LSR equals the head.** The paired difference is zero in
   all ten cap-0.70 pairs at both lags, with Holm p=1. This is inapplicability
   evidence, not proof of no retrieval effect.
5. **The fixed-blend onset result is horizon-specific.** Fixed 0.5 improves 1 h
   onset F1 over the head by 0.02441871 in all pairs (Holm p=0.01171875), but
   the 24 h mean difference is 0.00163439 with five wins/five losses (Holm p=1).
   Both remain diagnostics under the unsupported onset arm.
6. **The privileged direct transform has subunit onset F1 despite zero MAE.**
   Onset F1 is 0.3333 at 1 h and 0.7527 at 24 h because the predicted-positive
   rule does not encode the onset target's quiet-state prerequisite. This is a
   metric-definition limitation.
7. **Cap ordering is unstable.** Selected GRU-LSR is descriptively lower-MAE
   than Persistence only at cap 0.60/1 h and cap 0.80/24 h; Persistence is lower
   in the other four cells. These are same-series crossings, not generalization.
8. **The fair subset cannot identify a full-roster winner.** It does not rerun
   MLP, LSTM, DLinear, TCN, raw-feature kNN, SmallBank, encoder, or topology
   ablations under the fair gate.
9. No result covers another system-year, observed curtailment, forecast vintages,
   OPF/UC feasibility, probabilistic forecasts, operators, deployment, or
   economic outcomes.

# Shared Assets and Independent Contribution

- RTS-GMLC is an external public substrate. Public input data do not imply that
  this manuscript's code/evidence package is publicly released.
- `p1_s3_fair_v1` is the sole source for main scientific tables, figures, and
  inferences. Legacy v5/v6 archives remain supplementary historical evidence.
- `manuscript/figures/make_figures.py` verifies the fair manifest outputs before
  deriving tables and figures; `figures/artifact_manifest.json` records the
  resulting hashes.
- The supported independent contribution is the retrospective proxy/onset
  benchmark plus a matched within-pipeline retrieval evaluation. No independent
  authorship, external reproduction, deployment, or companion-paper fact is
  inferred.
- No companion paper is named by the project acceptance contract. Authors must
  disclose any shared code, text, figures, or evidence rather than relying on
  repository inference.

# New or Rerun Experiments

The append-only fair namespace completed with 510 rows on 2026-08-13. It
executed:

1. A symmetric fit/selection/calibration/test gate with horizon embargoes.
2. MAE- and onset-F1-targeted checkpoint/hyperparameter arms.
3. Retrieval-only, equal-blend, head-only, and selected-head-weight controls
   sharing the selected checkpoint within objective.
4. Ten common GRU seeds and paired exact sign-flip inference at cap 0.70.
5. Persistence, Seasonal-24h, objective-selected Ridge, and the privileged
   target-hour direct transform.
6. Method-level reruns at caps 0.60 and 0.80 on the same system-year.

A separate execution rerun used the same frozen script/config/source hashes and
seeds. All non-timing fields in all 510 rows matched, and the four scientific
derived tables were byte-identical. Different raw CSV hashes are retained
because wall-clock timing differs. This changes the status from "no rerun" to
"scientific outputs reproduced by a separate execution," but not to external
independent replication.

Runtime, environment versions, primary/rerun hashes, incident logs, and legacy
version chronology are retained in `SUPPLEMENTARY_METHODS_AND_AUDIT.md`.

# Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** final author list and public ORCIDs.
- **AUTHOR INPUT REQUIRED:** complete affiliations and corresponding-author
  name/e-mail.
- **AUTHOR INPUT REQUIRED:** funder/grant information or an explicit
  no-external-funding statement.
- **AUTHOR INPUT REQUIRED:** CRediT contribution statement; contributions may
  not be inferred from repository history.
- **AUTHOR INPUT REQUIRED:** conflicts-of-interest and generative-AI disclosure.
- **AUTHOR INPUT REQUIRED:** IEEE Access biography and photograph for every
  author.
- **AUTHOR INPUT REQUIRED:** public repository URL and/or archival DOI before
  claiming the package is publicly released.
- **AUTHOR INPUT REQUIRED:** exact RTS-GMLC release/vintage beyond the hashed
  files, and an issue-to-delivery archive if operational language is desired.
- **AUTHOR INPUT REQUIRED:** disclose any shared code, text, figures, data
  preparation, or evidence tables with another manuscript.

Scientific blockers that wording cannot resolve are absent issue/vintage
metadata, absent observed-curtailment labels, zero positive onset support in
all fair selection/calibration phases, absent full-roster fair rerun, absent
cross-system/year units, and absent physical/user/deployment validation.
Changing temporal boundaries after seeing test outcomes to obtain positive
onsets or a favorable result is not permitted.
