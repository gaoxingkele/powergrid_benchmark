# Experiments

## E01: LSTM forecasting-error evaluation across regional datasets
- **Verifies**: C01, C02, C03
- **Evidence**: evidence/tables/table2.md (LSTM MSE), evidence/tables/table3.md (LSTM MAPE), evidence/figures/figure6.md (load balancing curve)
- **Run**: Not externally persisted (no code released); method described in §3.3–§3.6. See src/environment.md.
- **Setup**:
  - Model: Enhanced LSTM (LSTM layers + ReLU-activated fully connected head + dropout; claimed attention modification)
  - Hardware: Not specified in paper
  - Dataset: Five regional hourly load CSVs from Kaggle — AEP, COMED, DAYTON, DEOK, DOM (PJM-style). Sizes/splits not specified.
  - System: Min–max normalisation; next-timestamp forecasting from historical sequence
- **Procedure**:
  1. Normalise each feature (load, temperature, price) via min–max scaling.
  2. Train the LSTM to predict next-step load from historical sequence.
  3. Evaluate MSE and MAPE per test dataset.
- **Metrics**: MSE (Eq. 16), MAPE (%) (Eq. 17)
- **Expected outcome**:
  - Consistently low percentage error across all five datasets.
  - MSE varies substantially across datasets; MAPE varies little.
- **Baselines**: GRU (E02); prior works at macro level (E05)
- **Dependencies**: none

## E02: GRU forecasting-error evaluation across regional datasets
- **Verifies**: C01, C02, C03
- **Evidence**: evidence/tables/table4.md (GRU MSE), evidence/tables/table5.md (GRU MAPE), evidence/figures/figure7.md (load balancing curve)
- **Run**: Not externally persisted; method §3.3–§3.6. See src/environment.md.
- **Setup**:
  - Model: Enhanced GRU (GRU layers + ReLU head + dropout; claimed dynamic-gating modification)
  - Hardware: Not specified in paper
  - Dataset: Same five datasets as E01
  - System: Same preprocessing/forecasting protocol as E01
- **Procedure**:
  1. Same preprocessing as E01.
  2. Train GRU to predict next-step load.
  3. Evaluate MSE and MAPE per dataset.
- **Metrics**: MSE, MAPE (%)
- **Expected outcome**:
  - GRU MSE and MAPE at least as low as LSTM on each dataset.
  - Differences from LSTM are small.
- **Baselines**: LSTM (E01)
- **Dependencies**: none

## E03: Head-to-head LSTM vs GRU comparison and resilience scoring
- **Verifies**: C02, C05
- **Evidence**: evidence/tables/table6.md (combined MSE/MAPE), evidence/figures/figure9.md (prediction-vs-actual time series), evidence/figures/figure10.md (grid resilience scores)
- **Run**: Not externally persisted; §4.2–§4.3.
- **Setup**:
  - Model: LSTM vs GRU (as in E01/E02)
  - Hardware: Not specified in paper
  - Dataset: Five datasets (Table 6); qualitative plots additionally show COMED, EKPC, NI, PJM_Load (Figure 9)
  - System: Same forecasting protocol; a "grid resilience score" (definition not specified in paper) computed per dataset per model
- **Procedure**:
  1. Tabulate MSE and MAPE for both models on the same datasets.
  2. Overlay GRU/LSTM predictions against actual load time series.
  3. Compute and plot a grid-resilience score per model per dataset.
- **Metrics**: MSE, MAPE, grid-resilience score (units/definition unspecified)
- **Expected outcome**:
  - GRU MSE/MAPE below LSTM on every dataset, but by a small margin.
  - Resilience-score ranking differs from the error ranking (LSTM scored above GRU).
- **Baselines**: the two models against each other
- **Dependencies**: E01, E02

## E04: Intelligent control strategy simulation (peak shaving + voltage stability)
- **Verifies**: C04
- **Evidence**: evidence/figures/figure8.md (peak-load reduction & voltage-fluctuation panels), evidence/figures/figure6.md and evidence/figures/figure7.md (load-balancing / peak-shaving curves)
- **Run**: Simulation described in §3.3.3, §3.5, §4.3; no code released.
- **Setup**:
  - Model: ICS driven by LSTM/GRU real-time forecasts
  - Hardware: Not specified in paper (simulation)
  - Dataset: Monthly and diurnal load profiles (time in months / hours)
  - System: ESS charge/discharge, DR load shifting, DER (solar/wind) output adjustment; voltage/frequency monitoring
- **Procedure**:
  1. Generate real-time forecasts.
  2. Dispatch ESS/DR/DER against the forecast to flatten the load curve.
  3. Compare peak load and voltage fluctuation before vs after applying the strategy over a 12-month horizon.
- **Metrics**: Peak load (MW), voltage fluctuation (%), operational cost, grid-stability improvement
- **Expected outcome**:
  - Peak load reduced after control; load curve flattened toward a threshold.
  - Voltage-fluctuation range narrowed after control.
- **Baselines**: Reactive (before-strategy) operation; conventional ESS/DR without predictive foresight
- **Dependencies**: E01, E02

## E05: Macro-level comparison against prior forecasting works
- **Verifies**: C01
- **Evidence**: evidence/tables/table7.md
- **Run**: Literature comparison, §4.3, Table 7.
- **Setup**:
  - Model: Proposed LSTM-GRU vs prior techniques (AMI data, DNN+metaheuristics, LSTM-RNN, cognitive algorithms, smart-meter algorithms, adaptive forecasting, cloud computing)
  - Hardware: n/a (qualitative comparison)
  - Dataset: n/a
  - System: Tabulated technique / outcome / limitation
- **Procedure**:
  1. Enumerate prior techniques with their outcomes and limitations.
  2. Position the proposed method (low MSE/MAPE) against them, noting its generalisation limitation.
- **Metrics**: Qualitative outcome and limitation per reference
- **Expected outcome**:
  - Proposed method shows commendable accuracy but a generalisation caveat vs prior works.
- **Baselines**: Prior works [8], [12], [16], [14], [18], [2], [20], [11]
- **Dependencies**: E01, E02
