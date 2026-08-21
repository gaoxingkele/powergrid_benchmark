# Architecture: LSTM Load-Prediction Sub-model

Each IMF/residual component from the CEEMDAN decomposition is forecast by an identical LSTM
sub-model. The overall model is a bank of these sub-models (one per component) whose outputs are
overlaid to reconstruct the final load prediction; the sub-models are independent and can run in
parallel (§4.3). Structure from Figure 5 (evidence/figures/figure5.md) and the layer parameter
table Figure 8 (evidence/figures/figure8.md).

## Component graph (single sub-model)

```
Input (48 historical IMF values)
   → LSTM layer (unfolded 48 time steps; last-time-step output used as feature)
   → Batch Normalization
   → Dropout
   → Dense 1
   → Dense 2
   → Result (Dense, next IMF value)
```

## Components

### InputLayer
- **Purpose**: Feed the 48-length historical component sequence.
- **Inputs**: shape (None, 48, 1)
- **Outputs**: (None, 48, 1)
- **Design choice**: A single-step-ahead protocol — 48 historical IMF values → next value (Table 2).

### LSTM layer
- **Purpose**: Encode the temporal sequence; the output at the **last time step** captures and
  integrates information from the entire series and is used as the feature.
- **Inputs**: (None, 48, 1)
- **Outputs**: (None, 81) — output vector size 81; LSTM is unfolded for 48 time steps.
- **Design choice**: LSTM addresses RNN gradient vanishing; weight sharing keeps the number of
  weights independent of input length. Implemented with CuDNNLSTM on Keras.

### Batch Normalization
- **Purpose**: Keep each mini-batch's hidden-layer input in a common distribution; partial
  overfitting mitigation / data augmentation (Eqs. 16–19).
- **Inputs / Outputs**: (None, 81) → (None, 81); BN layer consists of 81 neurons.
- **Design choice**: Placed **after** the LSTM layer (vertical BN before LSTM did not yield
  satisfactory results for the small-scale electricity data).

### Dropout
- **Purpose**: Regularization by randomly deactivating neurons during training.
- **Inputs / Outputs**: (None, 81) → (None, 81); Dropout layer consists of 81 neurons; dropout
  probability 0.5.

### Dense 1
- **Purpose**: Fully connected learning capacity.
- **Inputs / Outputs**: (None, 81) → (None, 27).

### Dense 2
- **Purpose**: Fully connected learning capacity.
- **Inputs / Outputs**: (None, 27) → (None, 9) per Figure 8. (Text §5.2 states the three dense
  layers have 27, 8, and 1 neurons — i.e. the middle layer is 8 in text but 9 in the figure; this
  discrepancy is internal to the paper and recorded in evidence/figures/figure8.md.)

### Result (output Dense)
- **Purpose**: Produce the predicted IMF value for the next time interval.
- **Inputs / Outputs**: (None, 9) → (None, 1).
- **Design choice**: The three fully connected layers (27, 8/9, 1) enhance the network's learning
  capacity and yield the single-value prediction.

## Model-bank / reconstruction
- **Purpose**: Assemble per-component forecasts into the overall load prediction.
- **Interaction**: One sub-model per IMF/residual component (8 IMFs + RES); each predicts its own
  component; the predictions are overlaid (summed/reconstructed, following $x(t)=\sum \widetilde{IMF_k}+r_K(t)$).
- **Design choice**: Independent sub-models enable parallel execution (§4.3).

## Training configuration (see src/configs/model.md)
- Batch size 30; learning rate 0.005; dropout probability 0.5; optimizer context: mini-batch
  gradient descent; platform Keras with CuDNNLSTM.
