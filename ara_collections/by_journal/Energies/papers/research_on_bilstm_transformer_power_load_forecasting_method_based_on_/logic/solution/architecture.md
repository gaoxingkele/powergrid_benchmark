# DAF-BT Architecture

## Overview

The DAF-BT (Dynamic Adaptive Fusion — Bidirectional LSTM Transformer) architecture is a hybrid deep learning model designed for short-term power load forecasting. The architecture follows a sequential cascade with a parallel fusion termination: the input passes through an initial embedding stage, then through BiLSTM and Transformer branches, and finally through the DAF module which adaptively combines the extracted representations before producing the output prediction.

## Architecture Diagram (Textual)

```
Input (X)
  |
  v
N-Space Transformer (Embedding / Feature Projection)
  |
  v
BiLSTM Layer (Bidirectional Short-Term Dependency Extraction)
  |                                          |
  |    Forward LSTM: h_f = [h_f1, ..., h_fT]
  |    Backward LSTM: h_b = [h_bT, ..., h_b1]
  |    Concat: h_bi = [h_f; h_b]
  |                                          |
  v                                          v
Transformer Encoder with Local Enhanced Attention (Mask M)
  |
  |    Self-Attention with local mask:
  |    Attention(Q,K,V) = softmax(QK^T/√d + M)V
  |    M_ij = 0 if |i-j| ≤ w, -∞ otherwise
  |
  v
Feature Map F (concatenated BiLSTM + Transformer outputs)
     |
     v
┌─────────────────────────────────────────────────────┐
│                DAF Module                           │
│                                                     │
│  Feature Channel ──> ω_c = σ(W_c · [F_c; F_t] + b_c)│
│  Adaptive Unit                                      │
│                                                     │
│  Temporal ──> ω_t = σ(W_t · [F_c; F_t] + b_t)      │
│  Contribution Unit                                  │
│                                                     │
│  Synergistic Fusion:                                │
│  F_out = ω_c ⊙ F_c + ω_t ⊙ F_t + λ(ω_c ⊙ ω_t)     │
└─────────────────────────────────────────────────────┘
     |
     v
Output Layer (Linear Projection)
     |
     v
Forecast (y_hat)
```

## Component Details

### 1. N-Space Transformer (Input Embedding)
The input sequence X ∈ ℝ^(T × d_in) (where T is sequence length and d_in is input feature dimension: load, temperature, wind speed) is first projected into a higher-dimensional representation space. This "N-space" transformation maps the raw features into a unified embedding dimension d_model, preparing them for subsequent processing by the BiLSTM and Transformer components.

### 2. BiLSTM Layer
The bidirectional LSTM processes the embedded sequence in both forward and backward directions:
- **Forward pass:** LSTM reads from t=1 to t=T, producing hidden states [h_1^f, ..., h_T^f]
- **Backward pass:** LSTM reads from t=T to t=1, producing hidden states [h_T^b, ..., h_1^b]
- **Output:** h_t = [h_t^f; h_t^b] concatenated at each time step

This captures both past temporal context (what happened before) and future temporal context (what happens after) for each position, providing richer short-term dependency modeling than a unidirectional LSTM.

### 3. Transformer with Local Enhanced Attention
The Transformer encoder processes the BiLSTM outputs through self-attention layers modified with a local mask matrix M. The mask constrains each position's attention to a neighborhood window of size w:

- M_ij = 0 for |i-j| ≤ w (within window)
- M_ij = -∞ for |i-j| > w (outside window, attention masked out)

This preserves the Transformer's ability to capture global patterns (through residual connections across layers) while preventing the dilution of local patterns that occurs in unrestricted global self-attention.

### 4. DAF Module (Dynamic Adaptive Fusion)
The DAF module receives features from both the BiLSTM and Transformer branches and performs adaptive fusion through three parallel operations:

1. **Feature Channel Adaptive Unit:** Computes channel-wise importance weights ω_c based on the combined feature representation, allowing the model to emphasize informative channels (e.g., load patterns over temperature or vice versa) depending on the input context.

2. **Temporal Contribution Evaluation Unit:** Computes time-step-wise importance weights ω_t, allowing the model to focus on temporally relevant positions while downweighting uninformative or noisy time steps.

3. **Synergistic Fusion:** Combines the weighted features through element-wise multiplication and addition, with a nonlinear interaction term λ(ω_c ⊙ ω_t) that enables cross-dimensional coupling between channel and temporal importance.

### 5. Output Layer
A linear projection maps the fused representation to the target prediction dimension (single-step or multi-step load forecast).

## Architectural Design Rationale

The sequential BiLSTM → Transformer design processes temporal information at two complementary levels: fine-grained bidirectional local patterns first, then global contextual patterns. The final DAF module then adaptively fuses the contributions rather than relying on simple concatenation or summation. This design explicitly addresses the identified limitations of static fusion approaches (G1) and insufficient dynamic adaptability (G2) by making the fusion process context-dependent and learnable.
