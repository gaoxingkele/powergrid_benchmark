# Title-to-Evidence Map

## Binding conservative paper story

This is a fixed-policy, single-system benchmark and matched-mechanism study. It constructs a curtailment-risk **proxy** from one RTS-GMLC weather year under a fixed 0.70 SNSP-type acceptance rule, then evaluates whether learned-space analogue retrieval changes forecasting performance at 1 h and 24 h. The supported mechanism result is conditional: learned-space retrieval lowers 1 h MAE relative to the matched retrieval-removal and retrieval-degradation controls, but it harms 24 h onset warning relative to no-retrieval and raw-space variants. The paper is not a dispatch-optimization, physical-feasibility, deployment, topology-capability, cross-system-generalization, or universal-superiority paper.

The headline MAE contract is indivisible:

- At 1 h, **Persistence** has the lowest MAE: 0.00690531.
- At 24 h, **Ablation-SmallBank** has the lowest MAE: 0.01534389, but its event F1 is 0.000000. This is the degenerate low-MAE warning, not a recommended winner.
- At 24 h, **kNN-RawFeature** is the strongest non-degenerate MAE reference: 0.01946336 with event F1 0.131737. It ties Ablation-NoSiamese on MAE and event F1; the raw-kNN label identifies the external baseline/reference rather than an exclusive overall winner.
- Persistence and Seasonal-24h both have 24 h MAE 0.02035887 and event F1 0.340000. Neither is the 24 h MAE leader.

Direct numerical sources are `../../papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/tables/real_curtailment_leaderboard.csv`, `../../papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/runs/real_curtailment_results.csv`, and the manuscript-local diagnostic subset `derived_tables/p1_method_diagnostics.csv`.

## Title terms

| Title term | Operational meaning in this paper | Method and direct evidence | Negative result or scope boundary | Human or evidence blocker |
|---|---|---|---|---|
| **Operating-state** | A 48 h window of seven system-aggregated inputs: load, wind, PV, net load, load ramp, renewable share, and a static topology-stress feature. | `../../src/powergrid_benchmark/mintou_real_curtailment.py` (`build_series`, `build_task`); `../../papers/mintou/mintou_p1_dstar_gru_dispatch/src/configs/real_curtailment_config.json`; Manuscript Sections III-A and V-B. | This is an input representation, not a state estimator, AC network state, or observed operator state. | Stronger operational-state wording would require state-estimation or operator evidence; none is present. |
| **Retrieval** | k = 8 nearest-neighbor retrieval from the fit-split bank, using the frozen GRU embedding, followed by a validation-selected convex blend with the GRU head. | Source functions `retrieval_blend` and `run_method`; Manuscript Section IV; full, NoSiamese, NoRetrievalBank, and SmallBank rows in the run archive. | Retrieval is beneficial only for the stated 1 h MAE contrasts. At 24 h, learned-space retrieval is worse than NoSiamese on MAE and worse than NoSiamese, NoRetrievalBank, and LSTM on onset F1 after Holm correction. | Selected blend weights are not recorded in the archived result rows. Reporting their distribution requires a rerun or another preserved log. |
| **Framework** | The implemented pipeline joining proxy construction, temporal splitting, a GRU head, optional retrieval, validation selection, and common evaluation. | `../../src/powergrid_benchmark/mintou_real_curtailment.py`; the v6 config; 208 archived method-seed records; Manuscript Fig. 2. | “Framework” denotes an inspectable software/evaluation structure. No API evaluation, user study, integration study, or deployment is evidenced. | A public release URL/DOI and independent reproduction are not yet supplied. |
| **Reproducible** | Fixed code paths, configuration, split rules, seeds, method definitions, and frozen result tables exist for the reported benchmark. | v6 config; run archive; leaderboard; primary-inference table; paired-sensitivity table; `figures/series_stats.json`; `figures/cap_sensitivity.json`. | The evidence supports computational repeatability of the supplied package, not independent reproduction by an external group or replication across years/systems. | Authors must provide the release location/DOI and confirm that the public package contains the code, inputs or retrieval instructions, configs, and frozen outputs. |
| **Curtailment-risk** | The target is the fraction of available renewable generation rejected by a fixed 0.70 load-relative acceptance rule. | `build_series`; Manuscript Eq. (1); `figures/series_stats.json` (8760 h; 8.24% nonzero; maximum 0.38336). | The label is a policy-derived proxy, not measured curtailment, operator action, AC-OPF output, or unit-commitment result. | None for the current proxy wording. Any observed-curtailment claim requires a different dataset and validation. |
| **Benchmark** | A common target, temporal split, metric family, eight baselines, five ablations, and DSTAR-GRU at two horizons. | v6 config; 14-method leaderboard; 208-row run archive; Manuscript Tables 1–4. | All model rankings are from one RTS-GMLC year and cap 0.70. Cap 0.60/0.80 results are series-level only. | External benchmark status is blocked by public release metadata; broader benchmark scope requires additional fixed-policy systems/years. |
| **Power system** | RTS-GMLC supplies synchronized aggregate load and renewable inputs and branch ratings used by the static feature. | Source data loader called by `build_series`; Manuscript Section III-A; RTS-GMLC citation [6]. | No power-flow, security-constrained dispatch, frequency response, or network-feasibility outcome is evaluated. | None for “on RTS-GMLC.” Stronger system-operation claims need physical validation. |
| **Decision support** | Point forecasts and thresholded onset warnings can inform a human-facing risk-assessment workflow. | Overall MAE, event F1, onset MAE, and onset F1 outputs in the run archive and Manuscript Sections III-C and VI. | No action recommendation, utility study, operator study, economic impact, live interface, or deployment evidence exists. | Authors must retain the informational/forecasting qualifier; any stronger use claim requires downstream and human evaluation. |

## Contribution terms

| Contribution term | Method and direct evidence | Supported statement | Negative/null result that must travel with it | Human or evidence blocker |
|---|---|---|---|---|
| **C1: reproducible, method-agnostic curtailment-risk benchmark on public data** | The fixed target is computed before model fitting in `build_series`; all methods share the target, feature construction, and temporal split. Evidence: v6 config, run archive, `series_stats.json`, cap-sensitivity JSON. | The package defines an executable benchmark on public RTS-GMLC inputs. “Method-agnostic” applies to target construction, not to a claim that every possible forecasting family was included. | Labels are proxy labels; one system/year and cap 0.70 identify model rankings. The fixed-cap NREL-118 check has zero positive targets and yields no external ranking. | “Public benchmark” must mean “benchmark on public data” until authors supply a public code/evidence URL or DOI. |
| **C1: onset/transition slice and common threshold calibration** | Onset is `y_t >= 0.02` and `y_{t-h} < 0.02`; per-method warning thresholds maximize training-window onset F1 over a 40-quantile grid and are applied unchanged to test. Evidence: `evaluate`; 57 test onsets at 1 h and 172 at 24 h. | The same calibration procedure and frozen test application are implemented for every method. | F1 is based on one fixed test window and limited onset counts; it does not quantify year-to-year or event-block uncertainty. | None for the implemented protocol; stronger uncertainty claims need new resampling units or additional years. |
| **C1: seeded statistical protocol** | Ten seeds for stochastic methods; two-sided Mann–Whitney U tests; Holm correction over 27 comparisons per horizon; paired sign-flip analysis is supplementary. Evidence: `real_curtailment_primary_inference_v2.csv` and `real_curtailment_paired_sensitivity_v2.csv`. | Corrected inference is available for DSTAR-GRU versus nine seeded opponents on MAE, onset MAE, and onset F1. | Deterministic methods have one row and are descriptive only. Bootstrap intervals are pointwise and multiplicity-unadjusted; seed variation is not data/year uncertainty. | Claims that tests were “prespecified” or methods were added before test inspection require a dated protocol or author confirmation; none was found in the inspected artifacts. |
| **C2: operating-state retrieval framework with matched controls** | DSTAR-GRU, NoSiamese, NoRetrievalBank, SmallBank, LSTMEncoder, and NoTopology are implemented switches in the same pipeline; eight baseline families complete the comparison. | The controls characterize the implemented switches within this pipeline. NoSiamese and NoRetrievalBank directly test learned-space retrieval versus raw-space retrieval and removal. | NoTopology is unresolved and does not support topology capability. LSTMEncoder/NoTopology nominally exceed DSTAR-GRU on 1 h onset F1 but are not Holm-separated. Combined controls support only the joint statement that performance depends on representation, retrieval presence, and bank design; they do not isolate a universal causal mechanism. | No independent code audit or external reproduction is recorded. Author-level software contributions cannot be inferred. |
| **C3: statistically resolved horizon-dependent utility** | Primary table: at 1 h, DSTAR-GRU MAE is lower than NoSiamese, NoRetrievalBank, SmallBank, LSTM, and MLP (Holm p <= 0.00402). At 24 h, DSTAR-GRU onset F1 is lower than NoSiamese, NoRetrievalBank, and LSTM (Holm p <= 0.00394). | The supported central result is a conditional cross-horizon sign reversal for the implemented retrieval mechanism on this benchmark. | TCN is unresolved in the primary unpaired test; MLP’s 24 h onset-F1 contrast does not survive Holm correction; the framework is not the overall leader. | Mechanistic explanations such as a “persistence prior” remain hypotheses until targeted probes are run. |
| **C3: metric- and horizon-specific negative findings** | Frozen 14-method leaderboard and Manuscript Table 4. | Persistence is the 1 h MAE leader; SmallBank is the 24 h MAE leader but has event F1 = 0; raw-kNN is the strongest non-degenerate 24 h MAE reference; Ridge leads 24 h onset F1. | These outcomes prohibit a universal MAE, event-detection, onset-warning, or architecture-superiority claim. | None. These are mandatory findings, not items to tune away. |

# Primary Estimand and Analysis Unit

The primary inferential estimand is the mean **DSTAR-GRU minus seeded-opponent** performance difference over the pipeline’s seed variation, conditional on the fixed RTS-GMLC year, fixed 0.70 policy, fixed temporal split, fixed feature/metric definitions, and a specified horizon. Lower values favor DSTAR-GRU for curtailment MAE and onset MAE; higher values favor it for onset F1. The primary inference family contains these three metrics against nine seeded opponents at each horizon.

The inferential analysis unit is one method-seed run, not an hour, onset, network, weather year, or deployment. Each run-level metric aggregates the same final 30% temporal test window. The test split contains 2628 target hours, including 57 onset hours at 1 h and 172 at 24 h. Reusing the same hours across seeds means the reported uncertainty covers training randomness only.

Deterministic Persistence, Seasonal-24h, Ridge, and kNN-RawFeature each have one row. Their rankings and differences are descriptive estimands on the fixed test window and carry no seed-based p-value. In particular, the 1 h Persistence lead and 24 h raw-kNN reference result must not be described as inferentially significant.

Holm-adjusted p-values control the recorded 27-test family within each horizon. The archived bootstrap intervals are pointwise and multiplicity-unadjusted. Exact paired sign-flip tests use common seed indices as a sensitivity analysis and do not replace the primary Mann–Whitney family. Neither procedure covers event-block, weather-year, system, or policy uncertainty.

# Comparison Budget and Data Visibility

| Contract item | Frozen budget or visibility rule | Evidence boundary |
|---|---|---|
| Data substrate | RTS-GMLC; 8760 hourly observations from one supplied weather year. | NREL-118 is an applicability audit only: 8784 hours, zero positive targets at the frozen 0.70 cap, no model ranking. |
| Task variants | Two horizons: 1 h and 24 h; model rankings only at cap 0.70. | Caps 0.60 and 0.80 have target-density/onset counts only, not method reruns. |
| Temporal visibility | First 70% is the training window; its last 15% is validation; final 30% is test. Normalization uses training-window statistics. Retrieval bank uses fit rows. Blend selection uses validation MAE. Warning-threshold calibration uses fit + validation onsets. | The code enforces the split, but the repository contains no independent audit log proving that all method choices preceded inspection of test results. |
| Method budget | 14 methods: one framework, eight baselines, and five ablations. Ten stochastic methods have 10 seeds; four deterministic methods have one row; two horizons produce 208 run records. | `derived_tables/p1_method_diagnostics.csv` is a 12-method subset and omits DLinear and TCN; it is adequate for the headline MAE repair but not the complete v6 comparison source. |
| Inferential budget | DSTAR-GRU versus nine seeded opponents on three metrics = 27 Holm-corrected tests per horizon. | Deterministic comparisons, event F1, stress-subset MAE, ranks, runtime, and multi-metric profiles are descriptive unless a recorded test says otherwise. |
| Test-result visibility | The manuscript calls some controls/tests “prespecified” or “predeclared.” | No dated preregistration or frozen comparison plan was found. Keep those adjectives only after author verification; the conservative story requires only “matched,” “primary,” and “scope check.” |
| Tuning | Shared training settings; DSTAR blend selected on validation MAE; warning threshold calibrated on the training window. | Selected alpha values are absent from the run archive. No claim about alpha distributions is allowed without a rerun/log. |

# Negative and Null Results

1. The framework does not lead overall MAE at either horizon. Persistence leads at 1 h. At 24 h, SmallBank has the lowest MAE but zero event F1, while raw-kNN is the strongest non-degenerate MAE reference.
2. DSTAR-GRU event F1 at 24 h is 0.034290 versus 0.340000 for Persistence/Seasonal-24h and 0.131737 for raw-kNN/NoSiamese.
3. DSTAR-GRU ranks seventh on 24 h onset F1 (0.176789). Ridge is the descriptive leader (0.235602); raw-kNN is second (0.226415); NoSiamese is third (0.224913).
4. At 1 h onset F1, LSTMEncoder (0.185409) and NoTopology (0.184597) nominally exceed DSTAR-GRU (0.176114), but neither primary contrast survives Holm correction.
5. At 1 h onset MAE, DSTAR-GRU is significantly worse than LSTM, NoRetrievalBank, LSTMEncoder, and DLinear in the primary table.
6. At 24 h, NoSiamese significantly improves MAE, onset MAE, and onset F1 relative to DSTAR-GRU. NoRetrievalBank and LSTM improve onset F1, while MLP’s onset-F1 difference is unresolved after Holm correction.
7. TCN is unresolved against DSTAR-GRU at both horizons in the primary unpaired analysis; the paired sensitivity resolves only the smaller 1 h MAE difference. This test-dependent result cannot be promoted to a robust architecture claim.
8. The NoTopology ablation is unresolved; the static topology feature is not shown to be load-bearing. There is no topology-uncertainty capability evidence.
9. The high-renewable stress subset shows no DSTAR-GRU advantage.
10. The NREL-118 fixed-cap audit yields zero positive target hours. It is a task-transport boundary, not external validation.
11. No model rankings exist at caps 0.60 or 0.80, across another weather year, or on observed curtailment. No OPF/UC feasibility, probabilistic forecast, operator study, deployment, or economic outcome is reported.

# Shared Assets and Independent Contribution

- Public substrate: RTS-GMLC inputs and the cited NREL-118 time-series assets are external data assets. Their public availability does not by itself make the manuscript’s code/evidence package public.
- Project-specific experimental assets: the P1 source, configs, run archive, leaderboard, inference tables, and transportability summary reside under `../../papers/mintou/mintou_p1_dstar_gru_dispatch/` and `../../src/powergrid_benchmark/`. Manuscript figures and the 12-method diagnostic subset are derived views, not independent experiments.
- Source-of-truth order for scientific claims: frozen v6 run archive and v6 evidence tables; then Manuscript Table 4 and figures generated from them; then local diagnostic subsets. Older logic cards and deprecated dispatch-proxy artifacts are not evidence for the current headline.
- The independent scientific contribution supported here is the P1-specific proxy/onset benchmark definition plus its controlled cross-horizon retrieval evaluation. No claim is made about independent authorship, independent reimplementation, or an independently reproduced result.
- No companion paper is named by this project’s acceptance contract. If code, text, figures, data preparation, or result tables overlap another submission, the authors must identify and disclose that overlap; it cannot be inferred from the inspected files.

# New or Rerun Experiments

No experiment was newly run or rerun for this narrative-repair stage, and no result file was edited. The current conservative story is supported by the frozen v6 evidence.

Experiments required only for stronger future claims are:

1. Full 14-method reruns at caps 0.60 and 0.80 to test whether method rankings and the retrieval sign reversal survive policy variation.
2. A policy-calibrated second-system experiment whose acceptance rule is fixed independently of model test outcomes; the frozen 0.70 NREL-118 audit cannot rank models.
3. Additional weather years or event-block resampling to estimate data/event uncertainty rather than seed variation alone.
4. Logging and reporting selected blend weights by horizon and seed.
5. Onset-oriented blend selection or class-balanced embedding probes if the paper wishes to test, rather than hypothesize, the proposed persistence-prior mechanism.
6. OPF/UC, operator, economic, interface, or deployment evaluation before making stronger decision-support or physical-operation claims.

# Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** final author list and public ORCIDs.
- **AUTHOR INPUT REQUIRED:** complete affiliations and corresponding-author name/e-mail.
- **AUTHOR INPUT REQUIRED:** funder and grant number, or an explicit no-external-funding statement. No funding status may be inferred.
- **AUTHOR INPUT REQUIRED:** IEEE Access biography and photograph for every author.
- **AUTHOR INPUT REQUIRED:** public repository URL and/or archival DOI if the benchmark or package is to be called publicly released. Until then, use “benchmark on public RTS-GMLC data.”
- **AUTHOR INPUT REQUIRED:** author-contribution/CRediT statement. Contributions cannot be assigned from repository history.
- **AUTHOR INPUT REQUIRED:** confirm the conflicts-of-interest and generative-AI disclosures already present in the manuscript.
- **AUTHOR INPUT REQUIRED:** provide dated support for “prespecified”/“predeclared” method and analysis claims, or approve conservative replacements such as “matched,” “primary,” and “scope check.”
- **AUTHOR INPUT REQUIRED:** disclose any shared code, text, figures, data preparation, or evidence tables with another manuscript and state the P1-specific contribution.

Scientific blockers that authors cannot resolve by wording alone are the absent observed-curtailment labels, independent reproduction, cross-year evidence, identifiable frozen-cap external task, physical feasibility evaluation, and deployment/user evidence. These limitations must remain if no new evidence is supplied.
