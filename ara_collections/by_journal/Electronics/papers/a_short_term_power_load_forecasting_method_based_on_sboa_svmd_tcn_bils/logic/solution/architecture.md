# Architecture — SBOA–SVMD–TCN–BiLSTM Forecasting Pipeline

End-to-end pipeline (Figure 8): decompose → optimize → forecast per component → reconstruct.

## Pipeline overview (component graph)

```
Original load ──► [Preprocess: quartile outlier removal + interpolation upsampling + min–max norm]
                       │
                       ▼
        [SBOA-optimized SVMD]  (SBOA minimizes permutation entropy over maxAlpha)
                       │
        ┌──────────┬───┴────┬──────────┐
      IMF1        IMF2     IMF3       IMF4
        │           │        │          │
   [TCN-BiLSTM] [TCN-BiLSTM] [TCN-BiLSTM] [TCN-BiLSTM]   (one forecaster per IMF)
        │           │        │          │
        └──────────┴───┬────┴──────────┘
                       ▼
             [Hybrid computation: sum component forecasts]
                       │
                       ▼
        [Denormalize + daily aggregation] ──► Day-ahead load forecast
```

## Components

### 1. Preprocessing
- **Purpose**: Clean and scale the raw load.
- **Inputs**: Raw 15-min load (35,040 points).
- **Outputs**: Cleaned, normalized series in [0,1].
- **Key choices**: Quartile method flags outliers → set to missing → interpolation upsampling (Eq. — interpolation function); min–max normalization (Eq. 33), inverse (Eq. 34).

### 2. SBOA-optimized SVMD (decomposition front-end)
- **Purpose**: Split the load into scale-separated, predictable IMFs while avoiding mode mixing.
- **Inputs**: Normalized load; SVMD params (Table 1); SBOA params (pop 30, iter 60).
- **Outputs**: Four IMFs (trend, periodic, two high-frequency).
- **Interactions**: SBOA proposes maxAlpha values; SVMD decomposes; permutation entropy of components is the fitness returned to SBOA; loop until iteration budget met, then decompose with the best maxAlpha.
- **Key choices**: Only maxAlpha optimized; SVMD chosen over VMD (no preset K) and over EMD-family (less mode mixing). See algorithm.md.

### 3. Per-IMF TCN feature extractor
- **Purpose**: Extract multi-scale local temporal features from each IMF.
- **Inputs**: One IMF (time-windowed).
- **Outputs**: Feature vector.
- **Key choices** (§5.2): 10 convolutional filters, filter size 2, 1 residual block, dropout 0.02, ReLU; dilated causal convolution (Eq. 25), residual unit f(x)=h(x)−x (Eq. 26), dilation 1→2→4 (Figure 3).

### 4. Per-IMF BiLSTM head
- **Purpose**: Model bidirectional temporal dependencies on the TCN features and output the component's one-step-ahead value.
- **Inputs**: TCN feature vector.
- **Outputs**: Forecast for that IMF.
- **Key choices** (§5.2): 60 hidden units, max 100 epochs, ReLU; forward + backward LSTM chains (Eqs. 27–32, Figure 6); output = 1 fully-connected layer with 1 neuron (Figure 7).

### 5. Reconstruction ("Hybrid computation")
- **Purpose**: Combine per-IMF forecasts into the final prediction.
- **Inputs**: Four IMF forecasts.
- **Outputs**: Reconstructed load forecast (then denormalized, daily-aggregated).
- **Key choices**: Summation/integration of component forecasts (Figure 8).

## Training / inference regime
- Optimizer Adam; initial learning rate 0.005 halved every 2 epochs (callback); GPU-accelerated.
- Offline training, online prediction (Table 7): one TCN-BiLSTM trained per IMF; inference is a fast forward pass.
- Data split 5:1 train/test; first 10 months train, remainder test (whole-year experiment); per-season experiments split each season 5:1.

## Design rationale (mirrored from figures)
- TCN before BiLSTM: TCN supplies dilated multi-scale local features (Figures 3–4) that BiLSTM alone under-captures; BiLSTM adds bidirectional context (Figure 6); the combination (Figure 7) improves accuracy and stability (C04).
- Per-component modeling: each IMF is simpler/more regular than the raw series, so a dedicated forecaster fits it better (C03), and SBOA-tuned SVMD makes components more predictable (C01).
