# Problem Formulation

## Observations

**O1 — CNN limited temporal dependency capture.** Standard convolutional neural networks excel at local feature extraction but struggle to model long-range temporal dependencies in power load sequences. Their fixed receptive field constrains the model's ability to capture load patterns spanning multiple time steps, leading to degraded accuracy on sequences with extended temporal correlations.

**O2 — LSTM gradient degradation on long sequences and extreme transition events.** While LSTM networks mitigate vanishing gradients better than vanilla RNNs, they still suffer from information decay over extended sequences. This limitation is particularly pronounced during atypical load transition periods. The paper documents a 22.4% prediction error during the Spring Festival transition period, where the load pattern diverges significantly from regular daily profiles.

**O3 — Transformer global context without local precision.** The standard Transformer architecture captures global dependencies effectively through self-attention but misses fine-grained local temporal patterns. This results in approximately ±15% error on periods with photovoltaic (PV) fluctuation impacts, where rapid local changes demand precise short-term context that global attention mechanisms may dilute.

**O4 — Information loss in CNN-LSTM cascade hybrids.** Sequential CNN-LSTM hybrid architectures suffer from cumulative information degradation during feature transmission across the two heterogeneous modules. The paper identifies a 25% information loss rate in feature transmission between CNN and LSTM components, reducing the effectiveness of the combined representation.

## Gaps

**G1 — Static fusion methods for multi-source heterogeneous data.** Existing fusion approaches (simple concatenation, weighted summation, or sequential stacking) treat feature contributions as static and fail to dynamically adapt to the varying importance of different feature channels and temporal positions under changing load conditions. This static treatment creates a fundamental mismatch with the dynamic nature of power load data, where the relative importance of features (e.g., temperature vs. historical load) shifts across different operational contexts.

**G2 — Severe insufficiency of dynamic adaptability.** Current hybrid models lack mechanisms to dynamically evaluate and reweight features based on contextual conditions. The inability to perform instance-adaptive fusion means models apply the same fusion strategy regardless of whether the input represents a regular weekday, a holiday transition, or a weather-driven load swing. This severely limits forecasting robustness across diverse operating scenarios.

## Key Insight

The Dynamic Adaptive Fusion (DAF) module addresses the identified gaps through a dual-path adaptive weighting mechanism combined with a nonlinear interaction term. The DAF module comprises two parallel evaluation units — a Feature Channel Adaptive Unit that computes context-dependent importance weights for each feature channel, and a Temporal Contribution Evaluation Unit that assesses the relevance of each time step's contribution. These two weight vectors are combined through element-wise multiplication with a learned nonlinear interaction coefficient (λ), enabling the model to capture cross-dimensional coupling between feature channels and temporal positions. This design allows the fusion process to dynamically adapt its behavior based on the specific characteristics of each input instance, moving beyond static fusion toward truly context-aware representation integration.

## Assumptions

**A1 — Historical temporal patterns generalize to future load behavior.** The model assumes that the statistical properties and temporal patterns present in the training data (full-year 2016 commercial complex load) are representative of future operating conditions. This is a standard assumption for supervised time series forecasting but implies vulnerability to non-stationary shifts caused by policy changes, infrastructure upgrades, or extreme weather events not represented in the training distribution.

**A2 — Bidirectional context improves forecasting for non-causal tasks.** The use of BiLSTM assumes that access to both past and future context (within each training window) provides beneficial information. This is valid for offline training and evaluation where full sequences are available, but the model's applicability to strictly online (real-time, causal) forecasting scenarios would require architectural adaptation to remove the backward dependency.

**A3 — Multi-source features (load, temperature, wind speed) contribute complementary information.** The feature set assumes that external meteorological variables provide meaningful predictive signals beyond what can be extracted from load history alone. The DAF module is designed to adaptively weight these contributions, but the assumption that temperature and wind speed measurements at the same temporal resolution as load readings are both available and informative bounds the approach to settings with adequate sensor infrastructure.
