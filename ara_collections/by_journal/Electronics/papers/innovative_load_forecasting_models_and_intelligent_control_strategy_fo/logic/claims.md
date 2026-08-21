# Claims

## C01: Gated recurrent networks capture short-term temporal load structure well enough to forecast heterogeneous regional hourly demand at low percentage error
- **Statement**: A gated recurrent network trained on past hourly consumption alone learns the temporal regularities of a regional load series closely enough that its next-step forecasts deviate from actual demand by well under one percent on average — the recurrent gating, not any exogenous feature, carries the predictive signal across distinct regional consumption profiles.
- **Conditions**: Holds for short-horizon (next-timestamp) hourly forecasting on five PJM-style regional datasets after min–max normalisation, using history-only inputs; untested boundaries include multi-step horizons, unnormalised or non-stationary regimes, and datasets with sharp regime shifts or missing exogenous drivers (weather/price).
- **Sources**: [0.418% ← evidence/tables/table3.md «| DOM_hourly.csv | 0.418% |» [result]; 0.667% ← evidence/tables/table3.md «| COMED_hourly.csv | 0.667% |» [result]; 0.391% ← evidence/tables/table5.md «| DOM_hourly.csv | 0.391% |» [result]]
- **Status**: supported
- **Falsification criteria**: On a comparable regional hourly load dataset, a correctly trained LSTM/GRU whose next-step forecasts systematically exceed a few percent MAPE (i.e. the gating fails to recover the temporal structure) would refute the claim that history-only gated recurrence suffices for low-error short-term forecasting.
- **Proof**: [E01, E02]
- **Evidence basis**: LSTM MAPE ranges 0.418%–0.667% (Table 3) and GRU MAPE 0.391%–0.618% (Table 5) across the five datasets; the comparative time-series plots (Figure 9) show predictions tracking actual load for COMED/EKPC/NI/PJM_Load. Numbers are in the evidence layer, not restated here.
- **Tags**: forecasting, LSTM, GRU, MAPE, temporal-dependencies

## C02: For short-term hourly load forecasting the LSTM and GRU architectures are near-equivalent in accuracy, so model choice can be governed by compute rather than accuracy
- **Statement**: Two gated recurrent architectures that differ in internal state complexity — a dual-state (cell+hidden) design versus a single-hidden-state design — converge to statistically indistinguishable forecasting accuracy on the same load series, with the simpler design never worse and marginally ahead; the extra state machinery buys no accuracy advantage in this regime, making the architecture a compute/latency decision rather than an accuracy one.
- **Conditions**: Established on five regional hourly datasets with next-step forecasting; the "marginal GRU edge" is small and consistent in sign but its practical significance is unquantified (no variance/significance testing), and the paper's own abstract frames the two as "equally good," so the equivalence is the load-bearing relationship and the direction of the small gap is secondary. Untested outside short-horizon hourly load.
- **Sources**: [GRU-superior ← evidence/tables/table6.md «In all the cases, it is observed that the performance of the GRU model is superior to that of the LSTM model as per the analysis based on the MSE and MAPE.» [result]; near-equivalence ← evidence/tables/table6.md «the results of the GRU model are very close to those obtained by the LSTM model, with only slight changes in the MSE and MAPE» [result]]
- **Status**: supported
- **Falsification criteria**: A head-to-head evaluation on comparable datasets where one architecture beats the other by a margin large enough to change downstream operational decisions (not a sub-tenth-of-a-percent MAPE difference) would refute the near-equivalence and restore accuracy as the deciding factor.
- **Proof**: [E01, E02, E03]
- **Evidence basis**: Table 6 places GRU MSE/MAPE below LSTM on every one of the five datasets, yet the deltas are small (e.g. DOM MAPE 0.418% vs 0.391%); the paper concludes selection "may depend on needs and computing limitations." Direction (GRU ≤ LSTM) and magnitude (tiny) together support near-equivalence.
- **Dependencies**: C01
- **Tags**: model-selection, LSTM-vs-GRU, parameter-efficiency, equivalence

## C03: Cross-dataset MSE rankings track series magnitude/variance, not model quality, whereas percentage error stays low and roughly flat
- **Statement**: When the same model is evaluated on load series of different absolute scale, its squared-error metric inflates with the magnitude and variance of the series while its percentage-error metric remains low and comparatively stable — so a large MSE gap between datasets reflects how big the load numbers are, not that the model forecasts one region worse than another; scale-free metrics are required to compare forecasting skill across heterogeneous grids.
- **Conditions**: Observed across five datasets spanning ~one to three orders of magnitude in load level; holds for MSE-vs-MAPE on this collection. The claim is about metric behaviour under scale, not a universal law; datasets engineered to have equal scale but different volatility could decouple magnitude from variance and are untested here.
- **Sources**: [162.435 ← evidence/tables/table2.md «| AEP_hourly.csv | 162.435 |» [result]; 23.962 ← evidence/tables/table2.md «| DOM_hourly.csv | 23.962 |» [result]; 0.546% ← evidence/tables/table3.md «| AEP_hourly.csv | 0.546% |» [result]; 0.418% ← evidence/tables/table3.md «| DOM_hourly.csv | 0.418% |» [result]]
- **Status**: supported
- **Falsification criteria**: If, on these datasets, MSE ordering did not follow the absolute load scale of the series (e.g. a small-magnitude series showed the largest MSE while its MAPE stayed low), the "MSE tracks scale" mechanism would be refuted.
- **Proof**: [E01, E02]
- **Evidence basis**: LSTM MSE spans 23.962 (DOM) to 162.435 (AEP) — nearly 7× — while LSTM MAPE spans only 0.418%–0.667% (Tables 2, 3); GRU mirrors this (Tables 4, 5). The largest-MSE dataset (AEP) does not have the largest MAPE, showing the two metrics rank datasets differently.
- **Dependencies**: C01
- **Tags**: evaluation-metrics, MSE, MAPE, scale-dependence, cross-dataset

## C04: Coupling real-time forecasts to storage, demand-response and DER dispatch flattens the peak-load curve and narrows voltage-fluctuation bands relative to reactive control
- **Statement**: Driving the dispatch of energy-storage, demand-response and distributed generation from a live load forecast (rather than reacting after demand materialises) shifts consumption off the peak and holds voltage within a tighter band — predictive foresight converts the same physical assets into a proactive load-levelling mechanism that both lowers peak magnitude and reduces deviation variance.
- **Conditions**: Demonstrated in a simulation with monthly/diurnal load profiles; the reported cost and stability figures are simulation outcomes, not field measurements, and the control law and simulation model are described only qualitatively. Untested on real hardware, under forecast error stress, or against a strong optimisation baseline.
- **Sources**: [10% ← evidence/figures/figure8.md «the strategy achieving an average reduction of 10% across various time periods» [result]; 160 MW→140 MW ← evidence/figures/figure8.md «the peak load decreased from 160 MW to 140 MW after applying the control strategy» [result]; 4%–7.5%→3%–5% ← evidence/figures/figure8.md «voltage fluctuations ranged from 4% to 7.5%. After the strategy was applied, fluctuations were reduced to a range of 3% to 5%» [result]]
- **Status**: supported
- **Falsification criteria**: A simulation or deployment where forecast-driven ESS/DR/DER dispatch fails to reduce peak magnitude or voltage-deviation range below reactive (non-predictive) dispatch of the same assets would refute the predictive-foresight mechanism.
- **Proof**: [E04]
- **Evidence basis**: Figure 8 shows the "After Control Strategy" curves below "Before" for both peak load (MW) and voltage fluctuation (%) across 12 months; §4.3 reports the 10% average peak reduction, the July 160→140 MW case, and the 7.5%→5% upper-bound narrowing. Headline conclusions add "up to 15%" cost and "~20%" stability figures (recorded in evidence, not restated).
- **Tags**: intelligent-control, load-levelling, peak-shaving, ESS, demand-response, DER, grid-stability

## C05: Downstream grid-resilience benefit does not track point-forecast accuracy
- **Statement**: The architecture that produces the lower point-forecast error is not necessarily the one that yields the higher grid-resilience benefit — a forecasting model's ranking on prediction accuracy and its ranking on a resilience/control objective can invert, so selecting a forecaster for a resilient-grid control loop cannot be reduced to minimising MSE/MAPE.
- **Conditions**: Rests on a single comparison (LSTM vs GRU) where GRU has lower MSE/MAPE on all five datasets yet LSTM is scored higher on the paper's grid-resilience metric; critically, the resilience-score construction is not defined in the paper, so the inversion is an observed pattern whose cause is unestablished. This bounds it to a hypothesis-strength cross-metric observation, not a demonstrated causal mechanism.
- **Sources**: [GRU lower error ← evidence/tables/table6.md «In all the cases, it is observed that the performance of the GRU model is superior to that of the LSTM model as per the analysis based on the MSE and MAPE.» [result]; LSTM higher resilience ← evidence/figures/figure10.md «Grid Resilience Scores for LSTM and GRU Models» [result]]
- **Status**: hypothesis
- **Falsification criteria**: If, under a defined resilience metric, the lower-forecast-error model were also consistently the higher-resilience model across datasets, the claimed decoupling would fail; conversely the current evidence is weakened by the undefined score, so a specified metric that reproduces the inversion would strengthen it.
- **Proof**: [E03]
- **Evidence basis**: Table 6 (GRU ≤ LSTM on MSE and MAPE everywhere) juxtaposed with Figure 10, where the LSTM series sits above the GRU series at all five datasets on the resilience-score axis. The two rankings disagree.
- **Dependencies**: C02
- **Tags**: resilience, model-selection, metric-divergence, control-objective
