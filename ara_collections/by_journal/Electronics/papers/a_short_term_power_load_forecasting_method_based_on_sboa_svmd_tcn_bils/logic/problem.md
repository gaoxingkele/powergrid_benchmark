# Problem Specification

## Observations

### O1: Load sequences are non-stationary with multiple periodicities and random fluctuations
- **Statement**: Electricity load varies strongly with seasonal change, day–night alternation and social-activity patterns, exhibiting multiple periodicities and stochastic fluctuations over time.
- **Evidence**: Introduction, §1 (citations [5]); confirmed by the SVMD decomposition of Belgian 2018 load into a trend IMF plus periodic and high-frequency components (Figure 9).
- **Implication**: A single flat model on the raw series must simultaneously fit trend, periodicity and noise, which is hard.

### O2: Classical and shallow ML models capture long-term dependencies poorly
- **Statement**: Statistical methods (time series, linear regression, exponential smoothing) suit stable periodic data but degrade on real-time nonlinear data; SVM/RF/ELM/ANN and even RNNs struggle with long-term dependencies (RNNs also suffer vanishing/exploding gradients).
- **Evidence**: §1–§2 literature synthesis; empirically LSTM/ELM/BiLSTM underperform the hybrid (Table 6).
- **Implication**: Motivates deep models with explicit long-range mechanisms (LSTM gates, TCN dilated convolutions).

### O3: Each deep architecture alone has a complementary blind spot
- **Statement**: CNN captures local patterns but not long-term dependency; LSTM captures long-term dependency but trains slowly; GRU is cheaper but weaker at dependencies; BiLSTM captures bidirectional context but is costly on long sequences; TCN captures long-range via dilated causal convolution but focuses on local patterns and may miss global context.
- **Evidence**: §1 (citations [14]–[20]).
- **Implication**: Suggests combining convolutional multi-scale extraction (TCN) with bidirectional recurrence (BiLSTM).

### O4: Decomposition helps but VMD-family parameter selection is fragile
- **Statement**: EMD decomposes into IMFs but suffers mode mixing; VMD improves robustness but needs a preset mode count K and complex, repeatedly-tuned parameters; SVMD removes the need to preset K by applying VMD successively.
- **Evidence**: §1, §2.1 (citations [21]–[23], [28]).
- **Implication**: A decomposition whose key parameter is chosen automatically (by an optimizer) can avoid mode mixing and reduce component complexity.

### O5: The mode-compactness parameter dominates SVMD quality
- **Statement**: Among SVMD parameters, the mode-compactness coefficient (maxAlpha) most strongly controls the compactness/fidelity of the modes; other parameters are set to empirical values.
- **Evidence**: §2.2; permutation entropy varies with compactness (Table 2).
- **Implication**: Optimizing maxAlpha specifically is the leverage point.

## Gaps

### G1: Weakened temporal continuity is not adequately captured
- **Statement**: Existing deep models' complex architectures still under-utilize temporal information, failing to capture the inherent multiple periodicities and stochastic fluctuations, i.e. the temporal continuity of load.
- **Caused by**: O1, O2, O3
- **Existing attempts**: CNN-RNN hybrids [24,25]; single deep models [26,27].
- **Why they fail**: Excessive convolution reduces efficiency on long-term dependencies; single models under-use temporal structure.

### G2: Decomposition parameter tuning is manual and error-prone
- **Statement**: VMD/SVMD decomposition quality hinges on parameters that are hard to set; poor settings cause mode mixing and less-predictable components.
- **Caused by**: O4, O5
- **Existing attempts**: Manual/empirical tuning; EMD-family methods (CEEMDAN/ICEEMDAN).
- **Why they fail**: Mode mixing yields components without clear periodicity, increasing forecast error.

## Key Insight
- **Insight**: Treat SVMD's key parameter (maxAlpha) as an optimization variable and minimize the permutation entropy (complexity) of the decomposed components with a global metaheuristic (SBOA); then forecast each resulting IMF with a TCN-BiLSTM that fuses multi-scale convolutional features with bidirectional recurrence, and reconstruct.
- **Derived from**: O3, O4, O5
- **Enables**: A decompose–optimize–predict–reconstruct pipeline that produces more predictable components and models each component's temporal structure.

## Assumptions
- A1: Permutation entropy of the decomposed sequence is a valid proxy for downstream predictability (lower entropy ⇒ lower forecast error).
- A2: The load can be adequately represented by exactly four IMFs at the optimized settings (as obtained here).
- A3: Day-ahead forecasting from the previous day's data is the operational target.
- A4: The single Belgian 2018 region dataset is representative enough to evaluate the method.
