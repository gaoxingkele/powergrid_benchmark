# Problem Specification

## Observations

### O1: Load is large and weather/holiday-coupled
- **Statement**: China's total electricity consumption reached 8.64 trillion kWh in 2022, with air conditioning and industrial loads accounting for over 60%; these fluctuations are highly related to meteorological conditions and holiday arrangements.
- **Evidence**: §1 Introduction (citing the International Energy Agency, refs [1–3]).
- **Implication**: Accurate STLF must integrate exogenous meteorological and calendar signals, not just past load.

### O2: Accuracy has direct economic/reliability value
- **Statement**: For every 1% improvement in prediction accuracy, power-plant fuel cost can be reduced by approximately 0.3% to 0.8%, and outage probability from supply-demand imbalance is significantly lowered.
- **Evidence**: §1 Introduction (ref [4]).
- **Implication**: Even sub-percent MAPE gains are practically meaningful, justifying architectural effort.

### O3: Classical models cannot fuse exogenous variables well
- **Statement**: ARIMA removes non-stationarity via differencing but cannot effectively integrate external variables (temperature, humidity) and adapts poorly to sudden load changes; SVR works on small/medium data but its cost grows exponentially with data size and depends on empirical kernel tuning.
- **Evidence**: §2 (refs [5–10]).
- **Implication**: Statistical baselines are structurally limited for multi-source STLF.

### O4: Existing deep models use single-channel input
- **Statement**: LSTM models long-term temporal dependencies via gating and excels at single-step prediction; CNNs extract local spatial features and are often hybridized with LSTM; but existing architectures mostly adopt a single-channel input structure and do not fully consider the heterogeneity of meteorological, temporal, and load sequences.
- **Evidence**: §1–§2 (refs [11–16]); Transformer suffers quadratic complexity [14]; GNNs need accurate topology graphs often unavailable [15].
- **Implication**: The dominant hybrid recipe leaves heterogeneous-modality fusion unsolved.

## Gaps

### G1: Heterogeneous modalities forced into one representation space
- **Statement**: Temporal features are strictly periodic but lack nonlinear weather interaction; meteorological data act on load with a delay (building thermal inertia); historical load carries both trend and stochastic components. Single-channel approaches force these distinct modalities into a homogeneous representation, causing feature entanglement and information loss.
- **Caused by**: O1, O4.
- **Existing attempts**: Single-channel CNN-LSTM hybrids [16]; Transformers [14]; GNNs [15].
- **Why they fail**: A shared encoder cannot preserve modality-specific dynamics (periodicity vs delay vs trend) simultaneously; entanglement degrades cross-modal signal.

### G2: Most hybrids predict only one future point
- **Statement**: In existing studies most models can only predict one load point in the future, which is of little significance in practical dispatching.
- **Caused by**: O4.
- **Existing attempts**: Single-step CNN-LSTM.
- **Why they fail**: A single future point does not give dispatchers a next-day load curve.

## Key Insight
- **Insight**: Independent per-modality encoding pathways followed by late fusion can preserve modality-specific characteristics while still enabling cross-modal interaction; give each of time / weather / historical-load its own LSTM channel, then let a CNN mine the cross-modal correlation over the concatenated (transposed) channel outputs.
- **Derived from**: G1, and multi-modal learning theory (ref [17]).
- **Enables**: A three-channel LSTM-CNN whose historical-load channel uses same-time-previous-day input so each output corresponds to a same-time future point, yielding a full consecutive-day forecast (addresses G2).

## Assumptions
- A1: Real-time meteorological features (temperature, humidity) for the prediction day are available from the dataset at inference time.
- A2: Historical load at the same hour on prior day(s) is a strong predictor of the target hour.
- A3: The three modalities (time codes, weather, historical load) are the relevant driver set for STLF.
- A4: Datasets are stationary enough that a model trained on the training split generalizes to the test split.
</content>
