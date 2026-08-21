# Architecture — Three-Channel LSTM-CNN

Component graph reconstructed from Figure 7 (network structure), Figure 1 (training flow), and §2.3.
The model is an **independent-encode-then-fuse** design: three parallel LSTM channels each encode one
modality, their outputs are concatenated + transposed, and a 1-D CNN fuses them before a fully
connected head emits the next-day load curve.

## Data-flow overview (Figure 7)

```
Historical load ──▶ LSTM 1 ┐
Meteorological  ──▶ LSTM 2 ├─▶ concat outputs ─▶ transpose ─▶ Conv1D ─▶ Conv1D ─▶ MaxPooling1D ─▶ FC ─▶ Prediction (24 pts)
Time class      ──▶ LSTM 3 ┘
```

## Components

### C-1: Historical-load LSTM channel (LSTM 1)
- **Purpose**: Encode trend + stochastic structure of past load.
- **Inputs**: Same-hour load from prior days: $\{X_{t-24}, X_{t-24*2}, \dots, X_{t-24*m}\}$ (24 = hours/day). Chosen $m=1$ (previous day) per the lookback ablation.
- **Outputs**: Neuron vector $(H_{1,1}, H_{1,2}, \dots, H_{1,n})$, $n=64$.
- **Interactions**: Feeds the concatenation node.
- **Key design choice**: Same-hour alignment so each output maps to a same-time future point (enables a full consecutive-day forecast; addresses G2).

### C-2: Meteorological-environment LSTM channel (LSTM 2)
- **Purpose**: Model delayed nonlinear weather→load effect (building thermal inertia).
- **Inputs**: $\{W^1_t, \dots, W^r_t\}$, $r$ = number of meteorological features (e.g. temperature, humidity for the prediction day).
- **Outputs**: $(H_{2,1}, \dots, H_{2,n})$, $n=64$.
- **Interactions**: Feeds the concatenation node.
- **Key design choice**: Separate channel keeps delayed weather dynamics from being averaged against periodic time codes.

### C-3: Time LSTM channel (LSTM 3)
- **Purpose**: Capture daily/weekly periodicity.
- **Inputs**: $\{T^1_t, \dots, T^e_t\}$, $e$ = number of time-encoding features (months, hours, whether a working day, etc.).
- **Outputs**: $(H_{3,1}, \dots, H_{3,n})$, $n=64$.
- **Interactions**: Feeds the concatenation node.
- **Key design choice**: Strict-periodicity signal isolated in its own pathway.

### C-4: Concatenation + transposition
- **Purpose**: Stack the three channel outputs into a matrix $H_{(i,j)}$ ($i\in\{1,2,3\}$, $j\in\{1..n\}$) and transpose so the layout conforms to the TensorFlow Conv1D operation mode.
- **Inputs**: $H_1, H_2, H_3$.
- **Outputs**: Transposed $3\times n$ feature matrix.
- **Interactions**: Feeds the CNN. Convolution runs across the channel (modality) direction — see Figure 8.

### C-5: Convolutional fusion block (2× Conv1D)
- **Purpose**: Mine cross-modal correlation via local perception; fuse the three modalities.
- **Inputs**: Transposed feature matrix.
- **Outputs**: Fused feature map $S_{(1,n)}$ per Eq. 8.
- **Interactions**: First Conv1D (8 kernels) → second Conv1D (2 kernels) → pooling.
- **Key design choice**: 1-D convolution (Conv1D) is used rather than 2-D; the CNN sits after (not before) the LSTMs.

### C-6: Max-pooling (MaxPooling1D)
- **Purpose**: Dimension reduction — drop invalid info, cut compute, speed up.
- **Inputs**: Conv output.
- **Outputs**: Down-sampled feature vector.
- **Interactions**: Feeds the FC head.

### C-7: Fully connected head (FC) + inverse normalization
- **Purpose**: Map fused features to the preliminary load prediction; after inverse normalization, output final 24-point next-day load.
- **Inputs**: Pooled features.
- **Outputs**: 24 h load prediction.
- **Interactions**: Terminal component. Formula $y(x)=f(w\cdot x+b)$ (Eq. 7).

## Training loop (Figure 1)
Start → Data preprocessing → Feature engineering → Dataset partitioning → build three-channel
LSTM-CNN → train (predict on training set → compute error → if error not met and max iterations not
reached, update weights and increment training count → loop; else derive optimal weights) → predict
on test set → End.

## Design rationale
Each modality's distinct statistical structure (periodicity / delayed response / trend+noise) is
preserved by a dedicated LSTM (late fusion, RW02), and the CNN recovers cross-modal correlation the
LSTMs cannot see individually (C01, C02). This is mirrored from the Figure 7 diagram and §2.3 prose.
</content>
