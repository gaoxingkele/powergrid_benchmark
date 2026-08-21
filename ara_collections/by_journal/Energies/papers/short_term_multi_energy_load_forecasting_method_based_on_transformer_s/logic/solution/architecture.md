# Architecture: TSTG

## Overview

TSTG follows an encoder-decoder architecture where each layer in both encoder and decoder contains two core modules connected sequentially:

1. **Multi-head spatio-temporal attention module** — operates in parallel on the temporal and feature axes
2. **Dynamic adaptive graph convolution module** — operates on the spatial (node) dimension

The encoder processes historical load data X_in of shape (N, T_hist, D) and the decoder produces the forecast Y_hat of shape (N, T_pred, D).

## Component Flow

```
Input: X_in ∈ ℝ^{N × T_hist × D}
  │
  ▼
[Embedding Layer]
  ├─ Linear projection: D → d_model (per time step, shared across nodes)
  └─ Positional encoding (sinusoidal, as in standard Transformer)
  │
  ▼
[Encoder × L layers]
  │
  ├─ Multi-head Spatio-Temporal Attention
  │   ├─ Temporal attention head (T × T) with MI augmentation
  │   ├─ Feature attention head (D × D) with MI augmentation
  │   └─ Concatenate + project heads → output ∈ ℝ^{d_model}
  │
  ├─ [Skip connection + LayerNorm]
  │
  └─ Dynamic Adaptive Graph Convolution
      ├─ Physical adjacency: A_phy ∈ ℝ^{N × N}
      ├─ MI similarity: A_mi ← MI(Z_i, Z_j) from current features
      ├─ Fusion: A_dyn = α · A_phy + β · A_mi  (α, β learned gates)
      └─ Graph convolution: Z' = σ(A_dyn Z W)
      │
      └─ [Skip connection + LayerNorm]
  │
  ▼
[Decoder × L layers] (same structure, cross-attends to encoder output)
  │
  ▼
[Output Projection]
  └─ Linear: d_model → T_pred × D  (single step or auto-regressive)
  │
  ▼
Output: Y_hat ∈ ℝ^{N × T_pred × D}
```

## Module Details (Refer to Method)

- Multi-head spatio-temporal attention: see [method.md](method.md), Equations (1)--(7)
- Dynamic adaptive graph convolution: see [method.md](method.md), Equations (8)--(11)

## Figure Reference

- **Figure 1** in `/evidence/figures/figure1.png` — Overall TSTG framework diagram
- **Figure 2** in `/evidence/figures/figure2.png` — Multi-head spatio-temporal attention module structure
- **Figure 3** in `/evidence/figures/figure3.png` — Dynamic adaptive graph convolution module structure
