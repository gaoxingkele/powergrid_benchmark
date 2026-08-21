# Related Work

Typed dependency graph. Full `RW` blocks for works with a specific technical delta to this paper;
briefer entries preserve the paper's full citation footprint.

## RW01: Semmelmann, Henni & Weinhardt, 2022 — LSTM-XGBoost hybrid for energy communities
- **DOI**: 10.1186/s42162-022-00212-9
- **Type**: extends
- **Delta**:
  - What changed: This paper adopts the same LSTM-XGBoost hybrid family but applies it to 15-min Elia transmission-operator load with an explicit LSTM→XGBoost residual-refinement cascade.
  - Why: Prior LSTM-XGBoost hybrid on smart-meter data motivates the combination; this work targets grid-operator load and residual correction.
- **Claims affected**: C01
- **Adopted elements**: The LSTM+XGBoost hybrid concept ([9] in paper).

## RW02: Zhou & Zhang, 2024 — ARIMA-LSTM short-term load forecasting
- **DOI**: 10.1088/1742-6596/2803/1/012002
- **Type**: baseline
- **Delta**:
  - What changed: [35] dynamically weights ARIMA and LSTM on hourly Southern China Grid data (MAPE 2.828, R2 0.9732); this paper uses 15-min data and a tree-based residual stage instead of ARIMA weighting.
  - Why: Argues its 15-min task is harder / more practically relevant than hourly weighting hybrids.
- **Claims affected**: C05
- **Adopted elements**: Hybridization principle; used as a comparison point in Table 2.

## RW03: Liu, Liang & Li, 2023 — TimeGAN-CNN-LSTM for I/C buildings
- **DOI**: 10.1109/OJIES.2023.3319040
- **Type**: baseline
- **Delta**:
  - What changed: [36] uses TimeGAN synthetic data + CNN-LSTM (15-min, MAPE 4.486%, R2 0.812); this paper trains only on real grid data ("maintains pattern fidelity without artificial bias").
  - Why: Avoids generalization concerns from synthetic augmentation.
- **Claims affected**: C05
- **Adopted elements**: None (contrast).

## RW04: Ibrahim, Rabelo, Gutierrez-Franco & Clavijo-Buritica, 2022 — DNN regression on Panama grid
- **DOI**: 10.3390/en15218079
- **Type**: baseline
- **Delta**:
  - What changed: [37] dense NN (3 layers × 95 units) on hourly Panama national data (RMSE 50.34 MW, MAPE 2.90%, R2 0.93); lower RMSE but on smoother hourly national-level data.
  - Why: Cited to argue reported RMSE is not resolution-controlled.
- **Claims affected**: C05
- **Adopted elements**: None (contrast).

## RW05: Liu, Song, Tao, Wang, Mo & Du, 2025 — CNN-BiLSTM-Attention with CEEMDAN/K-Means/VMD
- **DOI**: 10.3390/en18112675
- **Type**: baseline
- **Delta**:
  - What changed: [38] deep decomposition-heavy pipeline (RMSE 0.77 GWh, MAPE 1.08–1.67%, R2 0.985–0.991); this paper argues its preprocessing complexity limits real-time scalability.
  - Why: Contrast on accuracy-vs-simplicity trade-off; also a data point that attention-based architectures can work elsewhere (relevant to the C04 dead end).
- **Claims affected**: C04, C05
- **Adopted elements**: None (contrast).

## RW06: Ullah et al., 2024 — CNN-LSTM hybrid review + simulation (NTDC)
- **DOI**: 10.1109/ACCESS.2024.3440631
- **Type**: baseline
- **Delta**:
  - What changed: [39] CNN-LSTM on NTDC Pakistan hourly data (RMSE 538.71); much higher error attributed to data/modeling differences.
  - Why: Comparison point showing high RMSE from differing data characteristics.
- **Claims affected**: C05
- **Adopted elements**: None (contrast).

## RW07: Chen & Guestrin, 2016 — XGBoost
- **DOI**: (KDD 2016, pp. 785–794)
- **Type**: imports
- **Delta**:
  - What changed: Provides the gradient-boosting engine used as the refinement stage.
  - Why: Core algorithmic dependency.
- **Claims affected**: C01, C02
- **Adopted elements**: XGBoost algorithm ([17]).

## RW08: Siami-Namini, Tavakoli & Namin, 2018 — ARIMA vs LSTM comparison
- **DOI**: 10.1109/ICMLA.2018.00227
- **Type**: bounds
- **Delta**:
  - What changed: [21] establishes LSTM > ARIMA on non-linear series, motivating LSTM over statistical baselines.
  - Why: Justifies not using ARIMA/SARIMA as the primary model.
- **Claims affected**: C01
- **Adopted elements**: Empirical LSTM-over-ARIMA finding.

## RW09: Vaswani et al., 2017 — Attention Is All You Need
- **DOI**: (NeurIPS 2017; arXiv 1706.03762)
- **Type**: bounds
- **Delta**:
  - What changed: [7] source of the attention mechanism the authors tested and then discarded in this hybrid.
  - Why: Grounds the attention dead end (C04).
- **Claims affected**: C04
- **Adopted elements**: Attention mechanism (tested, excluded).

## RW10: Huang et al., 2025 — ARIMA-LSTM-XGBoost with linear-regression stacking
- **DOI**: 10.3390/en18061432
- **Type**: extends
- **Delta**:
  - What changed: [23] stacks ARIMA+LSTM+XGBoost for transformer oil temperature; related multi-model stacking lineage.
  - Why: Adjacent hybrid-stacking approach in the same journal.
- **Claims affected**: C01
- **Adopted elements**: Multi-model stacking concept.

## Additional citations (brief footprint)
- [1] Shering et al., 2024 — LSTM with exogenous weather variables (Energies), 10.3390/EN17081827 — background/motivation.
- [2] Fan, Peng & Hong, 2022 — EWT + Random Forest STLF, 10.1007/s00202-022-01628-y — background.
- [3] Taieb & Hyndman, 2014 — gradient boosting for load forecasting, 10.1016/J.IJFORECAST.2013.07.005 — background (ML > linear for load).
- [4] Interpretable ML book (Molnar) — interpretability motivation.
- [5] Casolaro et al., 2023 — DL for time series review (Information), 10.3390/INFO14110598 — background.
- [6] Ahn, Sun & Kim, 2021 — missing-data imputation methods, 10.32604/CMC.2022.019369 — preprocessing basis.
- [8] Bandara, Bergmeir & Smyl, 2020 — RNN on grouped series, 10.1016/J.ESWA.2019.112896 — scalability.
- [10] Cui et al., 2024 — XGBoost-RF feature selection + CNN-GRU, 10.3390/PR12112466 — dynamic feature selection basis.
- [11] Kong, Ding & Su, 2022 — ensemble learning w/ CEEMDAN, 10.1088/1742-6596/2356/1/012028 — ensemble motivation.
- [12] Zhang, Zheng & Qi, 2017 — deep spatio-temporal residual nets (AAAI) — background.
- [13] ML Mastery — DL for time series tutorial — background.
- [14] Shumway & Stoffer, 2017 — Time Series Analysis textbook — time-series definition.
- [15] Zhou, Aryal & Bouadjenek, 2024 — missing-data review (arXiv 2404.04905) — preprocessing.
- [16] Hyndman & Athanasopoulos, 2021 — Forecasting: Principles and Practice — background.
- [18] Abdullah & Qureshi, 2022 — unsupervised IoT time series — background.
- [19] Chandola, Banerjee & Kumar, 2009 — anomaly detection survey, 10.1145/1541880.1541882 — background.
- [20] Fawaz et al., 2019 — DL for time-series classification review, 10.1007/s10618-019-00619-1 — background.
- [22] Nejadettehad, Mahini & Bahrak, 2019 — RNN car-hailing demand, 10.1080/08839514.2020.1771522 — GRU context.
- [24] Lim et al., 2021 — Temporal Fusion Transformers, 10.1016/j.ijforecast.2021.03.012 — attention/transformer context.
- [25] Meng, Guo & Sun, 2023 — meta-learning probabilistic wind forecasting, 10.1109/TSTE.2024.3379835 — meta-learning context.
- [26] Botchkarev, 2019 — typology of regression error metrics, 10.28945/4184 — metric definitions.
- [27] Chereddy & Bolla, 2023 — GAN synthetic tabular data, 10.1007/978-3-031-36402-0_4 — imbalance/SMOTE-GAN context.
- [28] Sarmas et al., 2022 — transfer learning for solar forecasting, 10.1038/s41598-022-18516-x — transfer learning context.
- [29] Mehdary et al., 2024 — GA + XGBoost hyperparameter optimization, 10.3390/s24041230 — hyperparameter tuning context.
- [30] Gafni, Gradwohl & Tennenholtz, 2024 — prediction-sharing (arXiv 2403.17515) — LLM-in-forecasting context.
- [31] Jin et al., 2024 — Time-LLM (ICLR), arXiv 2310.01728 — LLM-in-forecasting context.
- [32] Brownlee, 2019 — normalize/standardize time series tutorial — scaling basis.
- [33] López, López & Crossa, 2022 — overfitting/model tuning, 10.1007/978-3-030-89010-0_4 — train/val/test split basis.
- [34] Wang et al., 2023 — LSTM-Informer with ensemble learning, 10.3390/electronics12102175 — LSTM temporal-modeling support.
