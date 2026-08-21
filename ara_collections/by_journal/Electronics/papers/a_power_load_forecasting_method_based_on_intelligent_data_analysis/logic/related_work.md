# Related Work

Typed dependency graph over the paper's citations. Works with a specific technical delta get full
`RW` blocks; the remaining references are captured briefly at the end to preserve the citation
footprint.

## RW01: Kong et al., 2019 — Short-term residential load forecasting based on LSTM RNN
- **DOI**: 10.1109/TSG.2017.2753802 (IEEE Trans. Smart Grid, [8])
- **Type**: baseline
- **Delta**:
  - What changed: This paper uses a plain LSTM-RNN framework to predict expected future load, with no adaptive decomposition front-end.
  - Why: Serves as the "LSTM" comparison model and the Table 1 reference [8] lacking Adaptive Data and Signal Frequency Overlap handling.
- **Claims affected**: C01, C03
- **Adopted elements**: LSTM as the recurrent forecaster backbone.

## RW02: Wang et al., 2021 — EMD-LSTM-CNN for activity signal frequencies
- **DOI**: Assessment of Heart Rate and Respiratory Rate ... ELC Model, IEEE Sens. J. 2021 ([9])
- **Type**: baseline / extends
- **Delta**:
  - What changed: A deep model (EMD-LSTM-CNN) based on LSTM, CNN, and EMD; provides adaptive data handling but not signal-frequency-overlap handling (Table 1).
  - Why: Basis for the "EMD-LSTM" comparison model; this paper replaces EMD with CEEMDAN to suppress mode mixing.
- **Claims affected**: C02
- **Adopted elements**: EMD-based signal decomposition as a forecasting front-end.

## RW03: Xia et al. (Shao et al.), 2021 — Stacked GRU-RNN / BN-RNN for circuit prediction
- **DOI**: 10.1109/TII.xxxx (A Stacked GRU-RNN-Based Approach ..., IEEE Trans. Ind. Inform. 2021, [10])
- **Type**: baseline
- **Delta**:
  - What changed: A BN-RNN method for predicting circuits (Table 1 reference [10]); lacks adaptive data and signal-frequency-overlap handling.
  - Why: Serves as the "RNN" comparison model.
- **Claims affected**: C01, C03
- **Adopted elements**: RNN forecasting with batch normalization.

## RW04: Taheri et al., 2021 — EMD + LSTM for electricity demand
- **DOI**: Electricity Demand Time Series Forecasting Based on EMD and LSTM, Energy Eng. 2021 ([41])
- **Type**: extends
- **Delta**:
  - What changed: Combined EMD with LSTM for short-term load forecasting, showing the advantage of signal decomposition.
  - Why: Directly motivates decomposition + LSTM; this paper argues EMD is prone to mode mixing and upgrades the front-end to CEEMDAN.
- **Claims affected**: C01, C02
- **Adopted elements**: The decompose-then-LSTM strategy.

## RW05: Wang et al., 2022 — Two-step improved EEMD (mode mixing)
- **DOI**: Harmonic Detection for Active Power Filter Based on Two-Step Improved EEMD, IEEE Trans. Instrum. Meas. 2022 ([42])
- **Type**: bounds
- **Delta**:
  - What changed: Establishes that EMD mode mixing causes loss of physical meaning in IMFs.
  - Why: Justifies moving beyond plain EMD; bounds the reliability of EMD components.
- **Claims affected**: C02, C05
- **Adopted elements**: Mode-mixing critique of EMD.

## RW06: Chen et al., 2019 — Deep residual networks for short-term load
- **DOI**: 10.1109/TSG.2019.xxxxx (Short-Term Load Forecasting with Deep Residual Networks, IEEE Trans. Smart Grid 2019, [43])
- **Type**: imports
- **Delta**:
  - What changed: Two-stage ensemble strategy with improved deep residual networks to enhance generalization for short-term load.
  - Why: Prior art on improving short-term load prediction; cited as context that room for improvement remains.
- **Claims affected**: C01
- **Adopted elements**: Motivation for ensemble/decomposition strategies.

## RW07: Lin et al., 2023 — Hybrid short-term load forecasting for individual residential customers
- **DOI**: A Hybrid Short-Term Load Forecasting Approach for Individual Residential Customer, IEEE Trans. Power Deliv. 2023 ([36])
- **Type**: imports
- **Delta**:
  - What changed: Validated suitability of LSTM-based models for residential load, with improvements as more data become available.
  - Why: Supports the choice of LSTM for residential load and the use of many users' data.
- **Claims affected**: C01
- **Adopted elements**: LSTM suitability for residential load.

## RW08: Laurent et al., 2016 — Batch normalized recurrent neural networks
- **DOI**: ICASSP 2016, pp. 2657–2661 ([46])
- **Type**: imports
- **Delta**:
  - What changed: Introduced BN into a five-layer LSTM RNN; found vertical BN improves convergence but horizontal BN did not.
  - Why: Informs where to place the BN layer; this paper places BN after the LSTM layer for small-scale data.
- **Claims affected**: —
- **Adopted elements**: Batch normalization inside recurrent networks.

## RW09: Faraji et al., 2022 — Batch-normalized deep RNN for high-speed nonlinear circuit macromodeling
- **DOI**: IEEE Trans. Microw. Theory Tech. 2022 ([47])
- **Type**: imports
- **Delta**:
  - What changed: Also found horizontal BN performed poorly in RNNs; poor performance attributed to improper scaling-parameter settings.
  - Why: Supports the BN placement decision.
- **Claims affected**: —
- **Adopted elements**: BN scaling-parameter insight.

## RW10: Xie et al., 2022 — Advanced Dropout (Bayesian dropout optimization)
- **DOI**: IEEE Trans. Pattern Anal. Mach. Intell. 2022 ([48])
- **Type**: imports
- **Delta**:
  - What changed: Model-free methodology for Bayesian dropout optimization; notes dropout doubles training time due to stochastic weight updates.
  - Why: Basis for the dropout regularization used in the sub-model.
- **Claims affected**: —
- **Adopted elements**: Dropout regularization.

## RW11: Gang et al., 2017 — Adaptive hybrid CEEMDAN for sea-clutter denoising
- **DOI**: ICEMI 2017, pp. 471–476 ([44])
- **Type**: imports
- **Delta**:
  - What changed: CEEMDAN with additional noise coefficients controlling noise level and complete noise-free reconstruction.
  - Why: Source of CEEMDAN's stated advantages (noise coefficients, noise-free reconstruction).
- **Claims affected**: C02
- **Adopted elements**: The CEEMDAN algorithm and its noise-control property.

## RW12: Zhao et al., 2020 — CEEMDAN-PSO-NNCT for ultra-short-term wind speed
- **DOI**: CCC 2020, pp. 2429–2433 ([45])
- **Type**: imports
- **Delta**:
  - What changed: CEEMDAN combined with a multi-model forecast; fewer experimental runs / more efficient.
  - Why: Supports CEEMDAN efficiency advantage over EEMD.
- **Claims affected**: C02
- **Adopted elements**: CEEMDAN efficiency argument.

## Additional references (brief — no distinct technical delta claimed here)
- **[1] Alavikia & Shabro, 2022** — layered IoT-enabled smart grid survey (background: advanced metering infrastructure).
- **[2] Ning et al., 2021** — intelligent resource allocation in mobile blockchain (background: electricity-theft avenue via metering network layers).
- **[3] Kong et al., 2022** — RMGen vehicular trajectory generation (background: IoT data utilization).
- **[4] Gai et al., 2022; [5] Qiao et al., 2022; [6] Wang et al., 2022** — data aggregation / blockchain / mean-field edge learning (background: grid data utilization and security).
- **[7] Ning et al., 2023** — lightweight imitation learning for service migration (background: extracting value from heterogeneous power data).
- **[11] Catalina et al., 2020** — PV nowcasting from weather + satellite (background: anomaly/forecasting in energy).
- **[12–14] Ning et al. / Wang et al.** — blockchain-enabled ITS, 5G IoV, IoV challenges (background: transportation anomaly analysis).
- **[15] Raza et al., 2020** — multivariate ensemble forecast for anomalous demand days (background: electricity forecasting).
- **[16] González et al., 2018** — Hilbertian ARMAX for electricity price (traditional time-series forecasting category).
- **[17] Xia et al., 2023** — ETD-ConvLSTM electricity theft detection (deep-learning networks category).
- **[18] Kong et al., 2022** — DRL energy-efficient edge computing for IoV (deep-learning networks category).
- **[19] Zhang & Guo, 2020** — hourly electricity demand forecasting (SVR/gradient-boosting category).
- **[20–27] Ning/Kong/Wang et al.** — edge/fog computing, MEC, wireless-powered MEC surveys (background: edge computing for distributed detection/prediction).
- **[28] Almalaq & Edwards, 2017** — review of deep learning for load forecasting (background).
- **[29] Tan et al., 2020** — ultra-short-term industrial demand via LSTM hybrid ensemble (deep-learning time-series forecasting).
- **[30] Otter et al., 2021; [31] Vidyaratne et al., 2022; [32] Yang et al., 2021** — deep learning for NLP / time-series / image recognition (RNN success domains).
- **[33] Shan et al., 2023; [34] Li et al., 2022** — DRRNets / fuzzy RNN for noisy time series (RNN gradient-vanishing limitation).
- **[35] Yazdinejad et al., 2022** — ensemble deep learning for IIoT threat hunting (LSTM direction context).
- **[37] Tu et al., 2021** — scenario generation for wind farms with time-series characteristics (non-stationary temporal features).
- **[38–40] Ning/Wang et al.** — intelligent edge computing / vehicular social networks / imitation-learning scheduling (EV temporal-feature complexity context).
