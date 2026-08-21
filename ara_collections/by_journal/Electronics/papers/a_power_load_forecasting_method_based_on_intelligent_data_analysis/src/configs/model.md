# Model Configuration

Concrete hyperparameters of the CEEMDAN-LSTM sub-model and its decomposition front-end, as printed
in the paper (§5.1–§5.2, Table 2, Figure 8). No code was released; these are the values needed to
reproduce the described network.

## LSTM output vector size
- **Value**: 81
- **Rationale**: Output vector size of the LSTM; the LSTM is unfolded for 48 time steps (§5.2). Not
  otherwise justified.
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: §5.2 "the output vector size of the LSTM is set to 81"; Figure 8 (LSTM output (None,81)).

## Batch Normalization layer size
- **Value**: 81 neurons
- **Rationale**: Matches the LSTM output width; BN placed after LSTM.
- **Sensitivity**: Not specified in paper
- **Source**: §5.2 "Both the BN layer and Dropout layer consist of 81 neurons"; Figure 8.

## Dropout layer size and probability
- **Value**: 81 neurons; dropout probability 0.5
- **Rationale**: Regularization against overfitting.
- **Sensitivity**: Not specified in paper
- **Source**: §5.2 "the dropout probability is 0.5"; Figure 8.

## Dense layer sizes
- **Value**: 3 dense layers — 27, 8, 1 neurons (text) / 27, 9, 1 (Figure 8)
- **Rationale**: Three fully connected layers enhance learning capacity; final layer outputs the
  next IMF value.
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: §5.2 "The Dense layer is composed of 3 layers, with the respective number of neurons
  being 27, 8, and 1"; Figure 8 shows Dense1→27, Dense2→9, Result→1 (internal discrepancy on the
  middle layer, recorded in evidence/figures/figure8.md).

## Input sequence length
- **Value**: 48 (historical IMF values → next IMF value)
- **Rationale**: A uniform choice for comparative experiments; LSTM unfolded for 48 time steps.
  Hourly → input length 2 days; daily → input length 24 days (Table 2).
- **Sensitivity**: Longer input increases training complexity and can cause optimization difficulty
  (§5.2); LSTM weight count is independent of input length.
- **Source**: Table 2; §5.2.

## Batch size
- **Value**: 30
- **Rationale**: Not specified in paper (mini-batch gradient descent used).
- **Sensitivity**: Not specified in paper
- **Source**: §5.2 "The batch size is set to 30".

## Learning rate
- **Value**: 0.005
- **Rationale**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: §5.2 "the learning rate is 0.005".

## CEEMDAN noise amplitude
- **Value**: 0.1× the standard deviation of the original data
- **Rationale**: Small-amplitude noise suits high-frequency-dominated signals; amplitude too small
  or too large yields suboptimal decomposition (§3.3, §5.1).
- **Search range**: Not specified in paper
- **Sensitivity**: Qualitatively high (§3.3) but not quantified
- **Source**: §5.1 "The white noise was added with an amplitude of 0.1 times the standard deviation
  of the original data".

## CEEMDAN ensemble size (noise realizations)
- **Value**: 200 sets of white noise
- **Rationale**: Ensemble averaging cancels added noise; CEEMDAN needs fewer runs than EEMD.
- **Sensitivity**: Not specified in paper
- **Source**: §5.1 "a total of 200 sets of white noise was added in CEEMDAN".

## Number of IMF components (decomposition depth)
- **Value**: 8 (plus 1 residual, RES)
- **Rationale**: Prevent generation of an excessive number of IMF components that would increase
  later training complexity.
- **Sensitivity**: Not specified in paper
- **Source**: §5.1 "the number of IMF components is set to 8".

## Sliding window
- **Value**: 60-day span, step size 1 (decomposition/hourly); 180-day span, step 1 for the daily
  training set
- **Rationale**: Window must be large enough to encompass periodic and trend components.
- **Sensitivity**: Not specified in paper
- **Source**: §5.1, §5.2.

## SD sifting stopping criterion
- **Value**: 0.1 < SD < 0.3
- **Rationale**: Standard recommended range for accepting an IMF (Eq. 2).
- **Source**: §3.1 "generally recommended to set the SD value between 0.1 and 0.3".
