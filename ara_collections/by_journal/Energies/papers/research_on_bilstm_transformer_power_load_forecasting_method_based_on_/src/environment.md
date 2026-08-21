# Experimental Environment

## Hardware

| Component | Specification |
|-----------|---------------|
| CPU | Intel i9 (specific generation not specified; presumed 12th or 13th gen based on RTX 3090 pairing) |
| GPU | NVIDIA RTX 3090 (24GB GDDR6X VRAM, CUDA cores: 10496) |
| RAM | Not explicitly specified (presumed 32GB+ for deep learning workloads) |

## Software

| Component | Version |
|-----------|---------|
| Operating System | Not explicitly specified (presumed Linux, e.g., Ubuntu 20.04) |
| Python | 3.8 |
| Deep Learning Framework | PyTorch 1.12 |
| CUDA | Compatible with RTX 3090 (CUDA 11.x) |
| Additional Libraries | NumPy, Pandas, Matplotlib, Scikit-learn (presumed standard scientific Python stack) |

## Hyperparameters

### Optimizer: Adam
| Parameter | Value |
|-----------|-------|
| Learning Rate | 0.001 |
| Beta1 | 0.9 |
| Beta2 | 0.999 |
| Epsilon | 1e-8 (default) |

### Training Configuration
| Parameter | Value |
|-----------|-------|
| Batch Size | 64 |
| Maximum Epochs | 150 |
| Early Stopping Patience | 15 epochs |
| ReduceLROnPlateau Patience | 5 epochs |
| Learning Rate Reduction Factor | 0.1 (default ReduceLROnPlateau factor) |
| Gradient Clipping | Not explicitly specified |

### Model Architecture
| Parameter | Value |
|-----------|-------|
| Hidden Dimension | 64 |
| Number of LSTM Layers | 2 |
| Transformer Encoder Layers | Not explicitly specified (presumed 2-4 layers) |
| Attention Heads | Not explicitly specified (presumed 8 for d_model=64 or multiple of head_dim) |
| Local Mask Window Size (w) | Not explicitly specified |
| Dropout Rate | Not explicitly specified (presumed 0.1-0.3) |
| Activation Function | ReLU (standard for Transformer FFN) |
| Loss Function | MSE (Mean Squared Error) |

## Dataset

| Property | Detail |
|----------|--------|
| Type | Commercial complex power load |
| Location | Temperate climate zone (specific location not disclosed) |
| Time Period | January 2016 — December 2016 |
| Sampling Interval | 0.5 hours (30 minutes) |
| Total Samples | 17,516 |
| Features | Historical load (kW/MW), temperature (°C), wind speed (m/s) |
| Temporal Features | Cosine-encoded time features (hour of day, day of week, etc.) |

## Data Preprocessing

| Step | Method |
|------|--------|
| Missing Value Handling | Linear interpolation |
| Normalization | Z-score standardization: x' = (x - μ) / σ |
| Train/Val/Test Split | 7:1:2 ratio (chronological split) |
| Train Samples | ~12,261 (70%) |
| Validation Samples | ~1,752 (10%) |
| Test Samples | ~3,503 (20%) |
| Input Sequence Length | Not explicitly specified (presumed 24-48 time steps for 12-24 hour context) |
| Prediction Horizon | Single-step (0.5h ahead) |

## Baseline Model Tuning

| Procedure | Detail |
|-----------|--------|
| Method | Grid Search |
| Scope | Hyperparameter optimization for each baseline model |
| Criterion | Minimization of validation MAPE |
| Note | Specific optimal hyperparameters per baseline not reported in the paper |
