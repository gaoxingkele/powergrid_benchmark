# Environment: TSTG Paper

## Hardware

- **GPU:** Not explicitly specified in the paper. Experiments likely run on a single NVIDIA GPU (e.g., RTX 3090/4090 or Tesla V100) based on training times reported in Table 2 (TSTG: 2700 s).
- **CPU/RAM:** Not specified.

## Software

- **Framework:** PyTorch (deep learning framework). Specific version not reported.
- **Libraries:** Standard PyTorch ecosystem (torch, torch.nn, torch.optim). Additional libraries for baseline models (e.g., Autoformer, FEDformer implementations) were used but versions not specified.
- **CUDA:** Not specified.

## Dataset

- **Name:** Arizona State University (ASU) Campus Metabolism multi-energy consumption dataset.
- **Source:** [campusmetabolism.asu.edu](https://campusmetabolism.asu.edu/) (public access).
- **Coverage:** 2017-01-01 to 2019-01-28 (approximately 1095 days, roughly 3 years).
- **Resolution:** Hourly.
- **Energy types:** 3 — Electric load, Cooling load, Heating load.
- **Buildings (nodes):** N = 20 individual buildings or measurement points.
- **Total samples:** 1095 days x 24 h = 26,280 hourly time steps (per building per load type).
- **Auxiliary features:** Calendar (hour of day, day of week, month); Meteorological (temperature, humidity).

## Preprocessing

- **Missing values:** Not explicitly discussed. Likely linear interpolation or forward-fill for any missing hourly readings.
- **Normalization:** Standard min-max or z-score normalization applied per load type. Specific method not stated.
- **Train/Val/Test split:** 7:1:2 ratio (chronological).
  - Train: ~767 days (approx. 2017-01-01 to 2019-01-06)
  - Validation: ~109 days (approx. 2019-01-07 to 2019-01-17)
  - Test: ~219 days (approx. 2019-01-18 to 2019-01-28, or approximately 2 years -- check exact split; "7:1:2" may refer to a random split or a different breakdown)
- **Random seed:** Not specified.

## Hyperparameters

| Parameter | Value |
|-----------|-------|
| N (nodes) | 20 |
| D (load types) | 3 |
| T_hist (historical window) | 24 |
| d_model (hidden dimension) | 64 |
| H (attention heads) | 4 (assumed; not explicitly stated) |
| d_n (per-head dimension) | 16 (= d_model / H) |
| Depth (encoder/decoder layers) | 3 |
| Batch size | Not specified (typical: 32 or 64) |
| Learning rate | Not specified (typical: 1e-3 or 1e-4) |
| Optimizer | Adam (assumed; standard for Transformer models) |
| Epochs | Not specified |
| Loss function | MAE |
| Dropout | Not specified (possible: 0.1) |

## Metrics

- **MAE:** Mean Absolute Error (primary metric for training loss and evaluation)
- **RMSE:** Root Mean Squared Error
- **MAPE:** Mean Absolute Percentage Error
- **R2:** Coefficient of determination

## Reproducibility

The paper does not report random seeds, specific GPU model, PyTorch version, or optimizer hyperparameters, making exact reproduction challenging. However, the public ASU Campus Metabolism dataset and standard Transformer/GCN building blocks provide a reasonable basis for re-implementation.
