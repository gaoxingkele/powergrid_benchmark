# Title-to-Evidence Map

## Binding conservative paper story

This is a fixed-policy, single-system **retrospective lag-forecasting** benchmark and a matched-mechanism study. It constructs a curtailment-risk proxy from one RTS-GMLC weather year under a fixed 0.70 SNSP-type acceptance rule, then evaluates whether learned-space analogue retrieval changes performance at 1 h and 24 h lags. The loader indexes the source rows by `Year`, `Month`, `Day`, and `Period`; the inspected source, configuration, and result files contain no forecast issue timestamp, as-of mapping, or data-vintage identifier. The evidence therefore does not support an operational day-ahead claim.

The paper-facing method name is **GRU learned-space retrieval (GRU-LSR)**. `DSTAR-GRU` remains only as the immutable archive label needed to join the configuration, run rows, evidence tables, and existing figures. No digital twin is implemented. Bank and query windows use the same frozen encoder, but there is no contrastive or pairwise Siamese objective; the supported term is shared-encoder learned-space retrieval.

The headline result contract is indivisible:

- At 1 h, **Persistence** has the lowest MAE: 0.00690531.
- At 24 h, **Ablation-SmallBank** has the lowest MAE: 0.01534389, but its event F1 is 0.000000. This is a degenerate low-MAE outcome, not a recommended winner.
- At 24 h, **kNN-RawFeature** is the strongest non-degenerate MAE reference: 0.01946336 with event F1 0.131737. It ties Ablation-NoSiamese on MAE and event F1; the raw-kNN label identifies the external baseline rather than an exclusive overall winner.
- Persistence and Seasonal-24h both have 24 h MAE 0.02035887 and event F1 0.340000. Neither is the 24 h MAE leader.

Direct numerical sources are the v6 `../../papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/tables/real_curtailment_leaderboard.csv`, `../../papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/runs/real_curtailment_results.csv`, and inferential tables named in `TABLE_TO_CONFIG_MANIFEST.md`.

## Title terms

| Title term | Meaning supported here | Direct evidence | Boundary or blocker |
|---|---|---|---|
| **Reproducible** | Fixed code paths, v6 configuration, split rules, seeds, method definitions, and frozen result tables exist in the supplied package. | v6 config; 208-row archive; leaderboard; inference tables; `TABLE_TO_CONFIG_MANIFEST.md`. | Supports computational repeatability of the package, not independent reproduction. Public URL/DOI remains author input. |
| **Retrospective** | A query window ends at row $s$ and predicts the proxy at delivery row $s+h$ for $h\in\{1,24\}$. | `build_task`: `starts`, `target_t=starts+horizon`, and windows ending at `starts`. | No operational issuance time or source vintage is recorded. |
| **Curtailment-risk** | Fraction of available renewable generation rejected by the fixed 0.70 load-relative acceptance rule. | `build_series`; Manuscript Eq. (1); `figures/series_stats.json`. | Policy-derived proxy, not measured curtailment, operator action, AC-OPF output, or unit-commitment result. |
| **Benchmark** | Common target, temporal split, metrics, eight baselines, five ablations, and GRU-LSR at two lag horizons. | v6 config; 14-method leaderboard; 208-row archive. | One RTS-GMLC year and cap 0.70 identify rankings. Caps 0.60/0.80 are series-only checks. |
| **GRU learned-space retrieval** | A GRU head and embedding, fit-only k-NN bank with $k=8$, and validation-MAE-selected convex blend. | `train_torch`, `retrieval_blend`, and `run_method`; archive row `DSTAR-GRU`. | Retrieval helps only for stated 1 h contrasts and harms stated 24 h onset contrasts. Selected blend weights are not archived. |
| **RTS-GMLC** | Source of delivery-indexed aggregate load, wind, PV, and branch ratings used by the static feature. | Source loader paths and RTS-GMLC citation [6]. | Source filenames say `DAY_AHEAD`, but the experiment does not preserve issuance/vintage metadata. |

## Contribution terms

| Contribution | Supported statement | Negative/null result that travels with it | Blocker |
|---|---|---|---|
| **C1: retrospective proxy benchmark** | The target is computed before model fitting and shared by all methods; the information gate and temporal split are explicit. | Labels are proxies; rankings are conditional on one system/year/cap; the NREL-118 fixed-cap check has zero positive targets. | Operational day-ahead wording needs a forecast-vintage archive with issue-to-delivery mapping. |
| **C1: onset/transition slice** | Onset is `y_t >= 0.02` and `y_{t-h} < 0.02`; a common training-window threshold procedure is applied unchanged to test. | Only 57 and 172 test onsets exist at 1 h and 24 h; seed uncertainty is not event/year uncertainty. | Stronger uncertainty claims need event-block or multi-year units. |
| **C1: seeded statistical protocol** | Ten seeds for stochastic methods; two-sided Mann–Whitney U tests; Holm correction over 27 comparisons per horizon; paired sign-flip sensitivity. | Deterministic methods are descriptive only; intervals are pointwise and multiplicity-unadjusted. | No dated preregistration supports “prespecified” or “predeclared.” |
| **C2: learned-space retrieval with matched controls** | Archive rows DSTAR-GRU, NoSiamese, NoRetrievalBank, SmallBank, LSTMEncoder, and NoTopology implement switches in one pipeline. | Combined ablations support only joint, within-pipeline conclusions. NoTopology is unresolved and does not establish topology capability. | No independent code audit or external reproduction is recorded. |
| **C3: horizon-dependent utility** | At 1 h, archive-label DSTAR-GRU MAE is lower than NoSiamese, NoRetrievalBank, SmallBank, LSTM, and MLP; at 24 h its onset F1 is lower than NoSiamese, NoRetrievalBank, and LSTM after Holm correction. | TCN is unresolved in the primary unpaired test; MLP's 24 h onset-F1 contrast is unresolved; GRU-LSR is not the overall leader. | Mechanistic “persistence prior” language remains a hypothesis until targeted probes are run. |

# Primary Estimand and Analysis Unit

The primary inferential estimand is the mean **archive-label DSTAR-GRU minus seeded-opponent** performance difference over pipeline seed variation, conditional on the fixed RTS-GMLC year, 0.70 proxy rule, temporal split, feature/metric definitions, and lag horizon. Lower values favor GRU-LSR for curtailment MAE and onset MAE; higher values favor it for onset F1. The recorded primary family contains these three metrics against nine seeded opponents at each horizon.

The analysis unit is one method-seed run, not an hour, onset, network, weather year, forecast vintage, or deployment. Each metric aggregates the same final 30% delivery-row test partition: 2628 target rows, including 57 onset rows at 1 h and 172 at 24 h. Reusing the same rows across seeds means uncertainty covers training randomness only.

Persistence, Seasonal-24h, Ridge, and kNN-RawFeature each have one deterministic row. Their rankings are descriptive and have no seed-based p-value. In particular, the 1 h Persistence lead and 24 h raw-kNN reference result must not be described as inferentially significant.

Holm-adjusted p-values control the recorded 27-test family within each horizon. Bootstrap intervals are pointwise and multiplicity-unadjusted. Exact paired sign-flip tests use common seed indices as a sensitivity analysis and do not replace the primary Mann–Whitney family. Neither procedure covers event-block, weather-year, system, policy, issue-time, or vintage uncertainty.

# Comparison Budget and Data Visibility

## Forecast information gate

| Item | Frozen rule | Evidence boundary |
|---|---|---|
| Benchmark issue index | Window ends at row $s$; there is no operational issue timestamp. | `build_task` uses features through `starts=s`. |
| Delivery time | Target row is $t=s+h$ for 1 h or 24 h lag. | `target_t = starts + horizon`. |
| Data vintage | Not recorded in source/config/result assets. | Loader retains delivery row key only; no as-of or revision field is archived. |
| Common raw query | Seven features for rows $s-47:s$. | Raw query tensors end at $s$. |
| Shared normalization | Mean/SD use feature rows 0--6131 (first 70%). | For the first 23 targets of the 24 h test, these statistics include pre-test feature rows later than $s$. |
| Test-result visibility | Final 30% is held out by delivery-row order. | No test row/label is used, but the delivery-keyed split is not a strict per-issue as-of split; no dated audit proves method/inference choices preceded test inspection. |

## Method-specific availability

| Method or family | Training/reference information available | Selection information | Test-query information |
|---|---|---|---|
| Persistence | No fitted model; proxy series itself. | None. | $y_s$. |
| Seasonal-24h | No fitted model; proxy series itself. | None. | $y_{t-24}$, which equals $y_s$ when $h=24$. |
| Ridge and kNN-RawFeature | Fit + validation windows/targets through delivery row 6131. | Fixed ridge penalty or fixed $k=8$; no test selection. | $X_s$ plus model/bank that is not per-issue refitted. |
| MLP, LSTM, DLinear, TCN | Fit windows/targets. | Validation targets through delivery row 6131 select checkpoint. | $X_s$ plus validation-selected checkpoint. |
| GRU-LSR / DSTAR-GRU and retrieval-preserving controls | Fit windows/targets train encoder/head; fit-only retrieval bank. | Validation targets through row 6131 select checkpoint and blend coefficient. | $X_s$ plus fixed fitted artifacts and fit-bank targets. |
| NoRetrievalBank | Fit windows/targets. | Validation targets through row 6131 select checkpoint. | $X_s$ plus validation-selected checkpoint. |
| Every method's onset classifier | Fit + validation predictions and onset labels through delivery row 6131. | 40-quantile grid maximizes training-window onset F1. | Frozen threshold applied to test prediction. |

For the 24 h task, test delivery rows begin at 6132 while the associated issue index is 24 rows earlier. Therefore delivery rows 6132--6154 have issue indices 6108--6130: shared normalization and, depending on method, validation-selected artifacts use pre-test rows that occur after the nominal issue index. This is not test-set leakage under the executed delivery-row split, but it prevents a strict operational as-of interpretation.

## Frozen budgets

| Contract item | Budget | Boundary |
|---|---|---|
| Data | RTS-GMLC, 8760 rows, one weather year. | NREL-118 is an applicability audit only: 8784 rows and zero positive targets at cap 0.70. |
| Tasks | Lags 1 h and 24 h; rankings only at cap 0.70. | Caps 0.60/0.80 have target-density/onset counts, not model reruns. |
| Methods | 14 methods; ten stochastic methods × 10 seeds and four deterministic methods × 1 row at two horizons = 208 records. | Local `p1_method_diagnostics.csv` is a 12-method subset and not the v6 source of truth. |
| Inference | GRU-LSR versus nine seeded opponents on three metrics = 27 Holm-corrected tests per horizon. | Deterministic comparisons, event F1, stress MAE, ranks, and runtime are descriptive. |
| Tuning | Shared neural training settings; retrieval blend selected on validation MAE; onset threshold calibrated on training partition. | Selected blend coefficients are not in the run archive. |

# Negative and Null Results

1. GRU-LSR does not lead overall MAE at either lag. Persistence leads at 1 h. At 24 h, SmallBank has the lowest MAE but zero event F1; raw-kNN is the strongest non-degenerate MAE reference.
2. GRU-LSR event F1 at 24 h is 0.034290 versus 0.340000 for Persistence/Seasonal-24h and 0.131737 for raw-kNN/NoSiamese.
3. GRU-LSR ranks seventh on 24 h onset F1 (0.176789). Ridge is the descriptive leader (0.235602); raw-kNN is second (0.226415); NoSiamese is third (0.224913).
4. At 1 h onset F1, LSTMEncoder (0.185409) and NoTopology (0.184597) nominally exceed GRU-LSR (0.176114), but neither primary contrast survives Holm correction.
5. At 1 h onset MAE, GRU-LSR is significantly worse than LSTM, NoRetrievalBank, LSTMEncoder, and DLinear in the primary table.
6. At 24 h, NoSiamese significantly improves MAE, onset MAE, and onset F1 relative to GRU-LSR. NoRetrievalBank and LSTM improve onset F1; MLP's onset-F1 contrast is unresolved after Holm correction.
7. TCN is unresolved against GRU-LSR at both horizons in the primary unpaired analysis; paired sensitivity resolves only the smaller 1 h MAE difference.
8. NoTopology is unresolved; the static topology feature is not shown to be load-bearing. There is no topology-uncertainty capability evidence.
9. The high-renewable stress subset shows no GRU-LSR advantage.
10. The NREL-118 fixed-cap audit yields zero positive target rows. It is a task-transport boundary, not external validation.
11. The first 23 samples of the 24 h test do not satisfy a strict per-issue information cutoff because scaling and validation-selected artifacts may use later pre-test rows. No ranking exists under an issue-time-aware forecast-vintage protocol, at caps 0.60/0.80, across another weather year, or on observed curtailment. No OPF/UC feasibility, probabilistic forecast, operator study, deployment, or economic outcome is reported.

# Shared Assets and Independent Contribution

- Public substrate: RTS-GMLC inputs and cited NREL-118 assets are external. Public data do not by themselves make the code/evidence package publicly released.
- Project-specific assets: source, configs, run archive, leaderboard, inference tables, and transportability summary reside under `../../papers/mintou/mintou_p1_dstar_gru_dispatch/` and `../../src/powergrid_benchmark/`. Manuscript figures and local diagnostics are derived views, not independent experiments.
- v5 source state is repository commit `3f0371eb5d775f5967ad59120e937d4804bd5a21` (2026-07-26). It has 12 methods and 168 rows under `public_rts_curtailment_v5_onset_eval`.
- v6 source state is repository commit `a728800bd48b11bc8f07647f82e4c9c2841a3e45` (2026-08-13). It adds DLinear and TCN and changes the run/config status to `public_rts_curtailment_v6_modern_temporal_controls`, yielding 208 rows. The v5 archive copies have the same Git blob IDs as the v5 current-name files at `3f0371e`, and all scientific metric fields in the 168 shared v5/v6 rows are identical.
- Source-of-truth order: v6 run archive and v6 tables; then manuscript tables/figures generated from them; then local diagnostic subsets. v5 and deprecated dispatch-proxy artifacts are historical only.
- The independent scientific contribution supported here is the P1-specific retrospective proxy/onset benchmark plus its controlled cross-lag retrieval evaluation. No claim is made about independent authorship, reimplementation, or external reproduction.
- No companion paper is named by this project's acceptance contract. Authors must disclose any overlap with another submission; it cannot be inferred from the inspected files.

# New or Rerun Experiments

No experiment was newly run or rerun for this narrative/information-gate stage, and no result file was edited. The v5/v6 reconciliation was a read-only comparison of archived files. The conservative story is supported by frozen v6 evidence.

Experiments required only for stronger future claims are:

1. An issue-time/vintage-aware evaluation with an as-of mapping from issuance to delivery before making an operational day-ahead claim.
2. Full 14-method reruns at caps 0.60 and 0.80.
3. A policy-calibrated second-system experiment whose rule is fixed independently of model test outcomes.
4. Additional weather years or event-block resampling.
5. Logging selected blend weights by horizon and seed.
6. Onset-oriented blend selection or class-balanced embedding probes to test the proposed persistence-prior mechanism.
7. OPF/UC, operator, economic, interface, or deployment evaluation before making stronger decision-support or physical-operation claims.

# Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** final author list and public ORCIDs.
- **AUTHOR INPUT REQUIRED:** complete affiliations and corresponding-author name/e-mail.
- **AUTHOR INPUT REQUIRED:** funder and grant number, or an explicit no-external-funding statement. Funding status may not be inferred.
- **AUTHOR INPUT REQUIRED:** IEEE Access biography and photograph for every author.
- **AUTHOR INPUT REQUIRED:** public repository URL and/or archival DOI if the package is to be called publicly released. Until then, use “benchmark on public RTS-GMLC data.”
- **AUTHOR INPUT REQUIRED:** author-contribution/CRediT statement. Contributions cannot be assigned from repository history.
- **AUTHOR INPUT REQUIRED:** confirm conflicts-of-interest and generative-AI disclosures.
- **AUTHOR INPUT REQUIRED:** identify the exact RTS-GMLC source release/vintage and provide issue timestamps or an issue-to-delivery archive if operational day-ahead language is desired.
- **AUTHOR INPUT REQUIRED:** provide dated support for any “prespecified”/“predeclared” claim; otherwise retain “matched,” “primary,” and “scope check.”
- **AUTHOR INPUT REQUIRED:** disclose shared code, text, figures, data preparation, or evidence tables with another manuscript and state the P1-specific contribution.

Scientific blockers that wording alone cannot resolve are absent issue-time/vintage metadata, absent observed-curtailment labels, independent reproduction, cross-year evidence, identifiable frozen-cap external task, physical-feasibility evaluation, and deployment/user evidence. These limitations must remain without new evidence.
