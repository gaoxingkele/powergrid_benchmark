# Problem Specification

## Observations

### O1: Abnormal consumption threatens grid safety and forecasting guides mitigation
- **Statement**: Non-technical losses (e.g. electricity theft) can overload lines and cause fires; the paper states that in recent years nearly 40% of electrical fires have been caused by abnormal electricity consumption and illegal acts of damaging power facilities. Predicting user electricity consumption gives power companies guidance for handling such matters.
- **Evidence**: §1 Introduction.
- **Implication**: Accurate user-level load forecasting is motivated by grid security, not only resource planning.

### O2: Better use of power data raises utility profitability
- **Statement**: The paper cites statistics that with every 10% increase in the utilization of power data, the profitability of power companies can rise by 20–40%, but valuable information is hard to extract from vast heterogeneous power data.
- **Evidence**: §1 Introduction ([7]).
- **Implication**: There is economic incentive to mine load data, but the extraction problem (identifying abnormal users, predicting short-term load) is the bottleneck.

### O3: Residential load is non-stationary, nonlinear, and multi-scale
- **Statement**: A user's load profile is a time series showing both periodicity (observed at hours, days, weeks, months, years) and random elements from user behavior; directly applying prediction models to such non-stationary short-term data hinders exploration of deeper temporal features.
- **Evidence**: §2 Related Works, §3.3.
- **Implication**: A model operating on the raw signal must simultaneously fit stochastic and structured content, which limits accuracy.

### O4: RNNs suffer vanishing gradients; LSTM mitigates but does not solve non-stationarity
- **Statement**: For electricity load forecasting requiring extensive time-series analysis, the gradient-vanishing problem of RNNs limits predictive performance; LSTM addresses gradient vanishing and has become the main research direction, but LSTM alone applied to raw non-stationary data still struggles with deeper temporal features.
- **Evidence**: §2 Related Works ([33,34,35,36,8,37]).
- **Implication**: Improving the input representation (decomposition), not just the network, is needed.

### O5: Plain EMD decomposition is prone to mode mixing
- **Statement**: EMD is adaptive and suited to nonlinear/non-stationary signals, but EMD algorithms are prone to mode mixing, which can lead to a loss of specific physical meanings in the intrinsic mode functions (IMFs).
- **Evidence**: §2 ([41,42]), §3.2.
- **Implication**: A decomposition that suppresses mode mixing (EEMD, then CEEMDAN) is preferable as a front-end.

## Gaps

### G1: Room to improve non-stationary short-term user load prediction accuracy
- **Statement**: Despite prior short-term forecasting work, there is still room for improving the accuracy of non-stationary short-term user electricity predictions.
- **Caused by**: O3, O4.
- **Existing attempts**: LSTM-RNN frameworks [8], EMD-LSTM-CNN [9], BN-RNN [10], EMD+LSTM [41], deep residual networks [43].
- **Why they fail**: Directly modeling non-stationary raw signals hinders deeper temporal feature extraction; EMD-based decompositions leak physical meaning via mode mixing.

### G2: Decomposition front-ends lose accuracy to mode mixing and inefficient windowing
- **Statement**: EMD-based front-ends mix modes, and sizing the analysis window naively to the network input length makes it difficult to separate trend from periodic components.
- **Caused by**: O5, O3.
- **Existing attempts**: EMD-LSTM [41], EMD-LSTM-CNN [9].
- **Why they fail**: Mode mixing produces physically meaningless IMFs; too-short windows cannot encompass the periodic and trend scales of the load.

## Key Insight
- **Insight**: If a non-stationary load signal is first separated — using an adaptive-noise ensemble decomposition (CEEMDAN) applied through a window large enough to span the periodic and trend scales — into stochastic, periodic, and trend sub-sequences, then each sub-sequence is individually more predictable, and per-component LSTM forecasts reconstructed together beat a single LSTM on the raw signal.
- **Derived from**: O3, O4, O5.
- **Enables**: The CEEMDAN-LSTM pipeline with a designed 60-day sliding window and per-component parallel LSTM sub-models.

## Assumptions
- A1: A user's load at any moment can be composed as a superposition of stochastic, periodic, and trend components (the decomposition assumption).
- A2: CEEMDAN's near-noise-free reconstruction preserves the essential information of the original sequence while distributing it among more stable components.
- A3: A sliding window of 60 days is large enough to encompass the periodic and trend components of residential load for the studied users.
- A4: 8 IMF components (plus residual) is a sufficient decomposition depth to represent the load without generating excessive components that complicate later training.
