# Claims

## C01: Cascading a temporal sequence learner with a tree-based residual corrector pushes short-term load-forecasting error below either component alone
- **Statement**: When a gradient-boosted tree stage is applied downstream of a recurrent sequence model so that it learns the sequence model's non-linear residual error, the two-stage cascade attains lower absolute and relative forecast error than either family achieves standalone — because each stage absorbs the error structure the other cannot represent (sequential dependency vs. non-linear residual). The improvement is a property of the division of labor, not of either learner individually.
- **Conditions**: High-resolution (15-min) real single-operator grid load, ~1 year, min-max normalized, with the tree stage consuming the sequence model's output plus engineered lag/date features. Untested boundary: unknown whether the ordering advantage persists at coarser resolution, on multi-operator/regional data, or against a jointly-trained (non-cascaded) alternative.
- **Sources**: [119.41 ← Table 1 «LSTM 119.41 1.30 0.992» [result]; 109.48 ← Table 1 «XGBoost 109.48 1.21 0.994» [result]; 106.54 ← Table 1 «LSTM-XGBoost 106.54 1.18 0.994» [result]; 106.54 ← §5 «gave an overall lowest RMSE of 106.54 MW and the lowest MAPE of 1.18% with the highest R2 value of 0.994» [result]]
- **Status**: supported
- **Falsification criteria**: On comparable high-resolution grid load, a standalone LSTM or standalone XGBoost (properly tuned) matching or beating the cascade on both RMSE and MAPE would refute the claimed complementarity advantage; likewise if the cascade's gain vanishes once each component is individually optimized.
- **Proof**: [E01, E02, E03]
- **Evidence basis**: Table 1 shows the hybrid's RMSE (106.54 MW) and MAPE (1.18%) are the lowest of the three, below both LSTM (119.41 / 1.30) and XGBoost (109.48 / 1.21); §4.4 and §5 restate the ranking. Numbers live in evidence/tables/table1.md.
- **Tags**: hybrid, residual-correction, cascade, ensemble

## C02: The tree-based refinement stage buys its gain in error-magnitude metrics, not in variance-explained, which is already saturated
- **Statement**: Once a non-linear refinement stage is stacked on a strong base learner on this data, its measurable benefit appears in error-magnitude metrics (RMSE, MAPE) while the coefficient of determination stays at its ceiling — i.e., the refinement redistributes/reduces residual error magnitude without further increasing the fraction of variance the model explains. This exposes that on near-saturated-R2 load data, R2 is an insensitive discriminator between good models and RMSE/MAPE carry the discriminating signal.
- **Conditions**: Regime where the base and hybrid models already explain ~0.99 of load variance; single dataset. Untested boundary: on harder data where R2 is well below ceiling, the refinement stage might move R2 too — not shown here.
- **Sources**: [0.994 ← Table 1 «XGBoost 109.48 1.21 0.994» [result]; 0.994 ← Table 1 «LSTM-XGBoost 106.54 1.18 0.994» [result]; 109.48 ← Table 1 «XGBoost 109.48 1.21 0.994» [result]; 106.54 ← Table 1 «LSTM-XGBoost 106.54 1.18 0.994» [result]]
- **Status**: supported
- **Falsification criteria**: If a dataset/refinement pairing showed R2 rising materially while RMSE/MAPE stayed flat, the claim that the refinement acts on error magnitude rather than variance-explained would be contradicted.
- **Proof**: [E01, E02]
- **Evidence basis**: XGBoost and the hybrid both report R2 = 0.994 (identical), yet hybrid RMSE falls from 109.48 to 106.54 MW and MAPE from 1.21% to 1.18% — the delta lives entirely in the error-magnitude columns. See evidence/tables/table1.md.
- **Dependencies**: C01
- **Tags**: metrics, R2-saturation, RMSE, MAPE, evaluation

## C03: Residual-refinement stacking delivers its largest benefit in high-volatility, spike-prone demand regimes
- **Statement**: The complementary-stacking advantage is regime-dependent: it is largest where demand is volatile and spike-laden, because the sequential base learner systematically under-predicts sudden anomalies while the tree stage is comparatively spike-insensitive — so combining them mostly repairs the base learner's spike/high-volatility errors rather than its steady-state fit.
- **Conditions**: Real load with pronounced short-term spikes and non-stationarity (daily/weekly/seasonal). Untested boundary: the paper argues this qualitatively from prediction overlays; it does not report a per-regime error decomposition, so the size of the regime-specific gain is not quantified.
- **Sources**: []
- **Status**: hypothesis
- **Falsification criteria**: A per-regime (calm vs. volatile window) error breakdown showing the hybrid's improvement over the base learner is equal or larger in calm windows than in volatile ones would refute the spike-repair mechanism.
- **Proof**: [E03]
- **Evidence basis**: §4.5 Error Analysis states the LSTM "struggles during sudden spikes" and XGBoost "exhibits a lower sensitivity to spikes but underperforms for continuous patterns," with the hybrid "combining the strengths of both"; Figure 7(c),(d) show the ensemble tracks actual load more precisely "particularly during the dynamic load variations." Qualitative/visual only.
- **Dependencies**: C01
- **Tags**: robustness, volatility, spikes, error-analysis, regime

## C04: Adding an attention mechanism to this hybrid did not improve accuracy and was discarded
- **Statement**: Bolting an attention mechanism onto an already-complementary LSTM+tree hybrid yielded no accuracy improvement on this forecasting task — evidence that added architectural complexity is not automatically beneficial once two complementary learners already cover the dominant error modes, and can be net-negative in effort/accuracy trade-off.
- **Conditions**: This specific hybrid and 15-min single-grid dataset; the paper reports the negative outcome without publishing the attention-variant's metrics. Untested boundary: a different attention formulation or dataset might still help; only "limited benefit" here is claimed.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A controlled comparison on the same data showing an attention-augmented hybrid with materially lower RMSE/MAPE than the plain hybrid would refute the "no benefit here" finding.
- **Proof**: [E04]
- **Evidence basis**: Abstract, §1.2, §2.3 and §4.6 all report the attention experiment was tried and excluded because "the resulting accuracy was inferior to the base hybrid model" / "a limited benefit in the current hybrid setting." No metrics table given — a documented dead end.
- **Tags**: dead-end, attention, ablation, negative-result

## C05: The reported accuracy is conditioned on a harder high-resolution regime than several compared studies, bounding cross-study comparison
- **Statement**: Headline error figures are only comparable across studies once forecasting resolution is controlled: forecasting 15-min real single-operator load is a higher-volatility task than the hourly/national-level series several cited hybrids use, so lower reported RMSE elsewhere does not by itself imply a better method. Resolution/aggregation is a confound that must be held fixed when ranking load forecasters.
- **Conditions**: Cross-study comparison over Table 2's 2022–2025 studies with heterogeneous data sources, resolutions, and units (MW vs GWh). Untested boundary: the paper does not re-run competitors on its own 15-min data, so the confound is argued, not experimentally isolated.
- **Sources**: [106.54 ← Table 2 «RMSE: 106.54 MW MAPE: 1.18% R2: 0.994» [result]; 50.34 ← Table 2 «RMSE: 50.34 MW MAPE: 2.90%R2: 0.93» [result]; 538.71 ← Table 2 «RMSE: 538.71 MAPE: 2.72% R2: N.R.» [result]]
- **Status**: hypothesis
- **Falsification criteria**: Running the cited hourly/national models and this hybrid on one common 15-min dataset and finding the resolution gap does not change their relative ranking would refute the confound argument.
- **Proof**: [E05]
- **Evidence basis**: §4.6 and Table 2 contrast this study (15-min, RMSE 106.54 MW) with e.g. [37] Panama hourly (RMSE 50.34 MW) and [39] NTDC (RMSE 538.71 MW), arguing hourly/national data "naturally smooths out fluctuations." See evidence/tables/table2.md.
- **Dependencies**: C01
- **Tags**: benchmarking, resolution-confound, comparison, external-validity
