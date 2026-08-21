# Method

## Key Equations

### Equation (1): CNN Convolution Operation
Standard 1D convolution for local feature extraction in power load sequences:

```
y_i = Σ_{k=1}^{K} w_k · x_{i+k-1} + b
```

where K is the kernel size, w_k are learnable convolutional kernels, x is the input sequence, y is the output feature map, and b is the bias term. The fixed receptive field K limits the temporal scope the CNN can capture without stacking multiple layers. This equation is used in the related work discussion (Section 2) to establish CNN baseline capabilities and limitations.

### Equation (2): LSTM Cell Update
The LSTM gating mechanism for temporal memory:

```
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
c_t = f_t ⊙ c_{t-1} + i_t ⊙ tanh(W_c · [h_{t-1}, x_t] + b_c)
h_t = o_t ⊙ tanh(c_t)
```

where i_t, f_t, o_t are input, forget, and output gates respectively; c_t is the cell state; h_t is the hidden state; σ is the sigmoid activation; and ⊙ denotes element-wise multiplication. Despite the gating structure, information decay over very long sequences remains a limitation (Section 2, O2).

### Equation (3): Transformer Self-Attention
The standard Transformer attention mechanism for global context:

```
Attention(Q, K, V) = softmax(QK^T / √d) V
```

where Q = XW_Q, K = XW_K, V = XW_V are linear projections of the input sequence, and d is the scaling dimension. This provides direct pairwise attention across all positions but can dilute local patterns (Section 2, O3; Section 3.2 for proposed mitigation).

### Equation (4): CNN-LSTM Cascade
Sequential hybrid feature extraction:

```
h_t = LSTM(CNN(x_t), h_{t-1})
```

CNN-extracted features are passed as input to the LSTM sequentially. The paper identifies approximately 25% information loss in this cascade due to representational shifts between convolutional and recurrent feature spaces (Section 2, G2).

### Equation (5): Bidirectional LSTM
The BiLSTM processes sequences in both directions:

```
h_t^f = LSTM_f(x_1, ..., x_t)
h_t^b = LSTM_b(x_T, ..., x_t)
h_t = [h_t^f; h_t^b]
```

The forward hidden state h_t^f captures past context, and the backward hidden state h_t^b captures future context. The final representation is the concatenation of both (Section 3.2, Figure 3).

### Equation (6): Local Enhanced Attention
Transformer attention modified with a local mask matrix M:

```
Attention(Q, K, V) = softmax(QK^T / √d + M) V
M_ij = 0  if |i-j| ≤ w
M_ij = -∞ if |i-j| > w
```

where w is the local window size and M is a fixed mask matrix. Positions within the window receive full attention; positions outside the window are masked out (attention weight set to zero after softmax). This preserves local pattern fidelity while maintaining the Transformer's parallel computation advantage (Section 3.2, Figure 3).

### Equation (7): DAF Feature Channel Adaptive Weights
Channel-wise importance weight computation:

```
ω_c = σ(W_c · [F_c; F_t] + b_c)
```

where ω_c ∈ ℝ^{d_c} are the channel importance weights, F_c are channel-domain features, F_t are temporal-domain features, W_c and b_c are learnable parameters, and σ is the sigmoid activation. Each feature channel (load, temperature, wind speed) receives a context-dependent importance score (Section 3.3, Figure 4).

### Equation (8): DAF Temporal Contribution Weights
Time-step-wise importance weight computation:

```
ω_t = σ(W_t · [F_c; F_t] + b_t)
```

where ω_t ∈ ℝ^{d_t} are the temporal importance weights, and W_t, b_t are learnable parameters. Each time step's hidden representation receives a context-dependent relevance score, enabling the model to focus on temporally informative positions (Section 3.3, Figure 4).

### Equation (9): DAF Synergistic Fusion
The complete DAF fusion operation combining channel-weighted, temporal-weighted, and interaction terms:

```
F_out = ω_c ⊙ F_c + ω_t ⊙ F_t + λ · (ω_c ⊙ ω_t)
```

where λ is a learnable scalar parameter controlling the strength of the cross-dimensional interaction term. The first term applies channel-wise attention to the channel features, the second applies temporal attention to temporal features, and the third captures coupling effects between the two weight spaces through element-wise multiplication scaled by λ (Section 3.3, Figure 4).
