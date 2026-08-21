# Method — Forward Model and Formulation

The method (as described in prose + equations in §2; no printed pseudocode) proceeds:
sequence construction → per-channel LSTM encoding → concatenate + transpose → Conv1D fusion →
max-pooling → FC → inverse normalization.

## 1. Input-sequence construction (§2.3)
- Predicted point: $X_t$, with $t$ the moment of the predicted load.
- Historical-load channel input: $\{X_{t-24}, X_{t-24*2}, \dots, X_{t-24*m}\}$ (24 = the hourly load value across one day; $m$ = number of prior days; chosen $m=1$).
- Meteorological channel input: $\{W^1_t, \dots, W^r_t\}$, $r$ = number of meteorological features.
- Time channel input: $\{T^1_t, \dots, T^e_t\}$, $e$ = number of time-encoding features.
- Each sequence is **normalized** before entering its LSTM module.

## 2. LSTM encoding (§2.1, Eqs. 1–6)
Each channel is a single LSTM layer (64 neurons). Gate mechanism:

$$f_t = \mathrm{Sigmoid}(w_f\cdot[x_t, y_{t-1}] + b_f) \quad (1)$$
$$i_t = \mathrm{Sigmoid}(w_i\cdot[x_t, y_{t-1}] + b_i) \quad (2)$$
$$\tilde c_t = \mathrm{Sigmoid}(w_c\cdot[x_t, y_{t-1}] + b_c) \quad (3)$$
$$c_t = f_t\cdot c_{t-1} + i_t\cdot \tilde c_t \quad (4)$$
$$o_t = \mathrm{Sigmoid}(w_0\cdot[x_t, y_{t-1}] + b_0) \quad (5)$$
$$y_t = o_t\cdot \tanh(c_t) \quad (6)$$

- $x_t$ = input at time $t$; $y_{t-1}$ = hidden-layer output at $t-1$; $w_*$ weight matrices, $b_*$ bias vectors; $[]$ = concatenation.
- Forget gate output in $[0,1]$: 0 discards, 1 retains the previous cell state $C_{t-1}$.

> Note (transcription fidelity): the paper prints Eq. 3 (candidate cell state $\tilde c_t$) with a
> `Sigmoid` activation, though the surrounding text says the candidate uses `tanh`. Reproduced as
> printed; the discrepancy is flagged, not silently corrected.

Outputs per channel: $(H_{1,\cdot})$ historical, $(H_{2,\cdot})$ meteorological, $(H_{3,\cdot})$ time, each of length $n=64$.

## 3. Concatenate + transpose (§2.3)
The three channels' output neurons are concatenated into a $3\times n$ matrix $H_{(i,j)}$ and
**transposed** so the layout conforms to the TensorFlow Conv1D operation mode (convolution runs
across the modality/channel direction; see Figure 8).

## 4. Convolutional fusion (§2.3, Eq. 8)
$$S_{(1,n)} = f\!\left(\sum_{i=1}^{3}\sum_{j=1}^{n} H_{(i,j)} * w_{(i,j)} + b\right) \quad (8)$$
- $S$ = convolution output; $w$ = kernel weight matrix; $f$ = activation; $b$ = bias.
- Two stacked Conv1D layers (first with 8 kernels, second with 2 kernels) extract and fuse the
  correlation between the modality features and load.

## 5. Pooling + FC + de-normalization (§2.2, §2.3, Eq. 7)
- MaxPooling1D reduces dimensionality (cuts compute, speeds up).
- Fully connected layer: $y(x) = f(w\cdot x + b)$ (Eq. 7) yields the preliminary prediction.
- **Inverse normalization** gives the final next-day load prediction.

## Convolution / pooling primer (§2.2, Figures 4–5)
- Conv1D hyperparameters: kernel size, stride, padding. Example dot-product (Figure 4): a 4×4 input
  with a 2×2 kernel, stride 1, no padding → e.g. $3\times1 + 1\times0 + 5\times0 + 2\times1 = 5$.
- Pooling window 2×2, stride 2; the paper uses 1-D **max** pooling.

## Activation & optimizer (fixed by ablation)
- Activation: **Leaky ReLU** (negative-slope $\alpha\in(0,1)$) — see C03.
- Optimizer: **Adam** — see C04.
- Historical lookback: **1 day** — see C05.

## Complexity
Not specified in paper (the paper only contrasts Transformer's quadratic complexity as motivation, ref [14]).
</content>
