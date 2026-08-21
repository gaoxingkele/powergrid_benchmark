# Related Work

## CNN Local Feature Extraction and Limitations

Convolutional neural networks (CNNs) have been applied to power load forecasting for their ability to extract local temporal patterns through sliding convolutional kernels. The standard 1D convolution operation is defined as:

y_i = Σ(k=1 to K) w_k · x_{i+k-1} + b   (Eq. 1)

where K is the kernel size, w_k are learnable weights, and b is the bias term. CNNs efficiently capture short-range dependencies through hierarchical local receptive fields but are fundamentally limited by their fixed kernel size, which constrains the temporal scope of features they can represent. Stacking convolutional layers extends the effective receptive field but introduces optimization difficulties including gradient propagation challenges and parameter proliferation. The paper documents that CNN-based models show degraded performance on sequences requiring extended temporal context, consistent with the broader literature on CNN limitations for sequential data.

## LSTM Gating Mechanism and Long-Term Decay

Long Short-Term Memory (LSTM) networks address the vanishing gradient problem of vanilla RNNs through a gated cell structure. The LSTM cell update equations are:

i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
c_t = f_t ⊙ c_{t-1} + i_t ⊙ tanh(W_c · [h_{t-1}, x_t] + b_c)
h_t = o_t ⊙ tanh(c_t)   (Eq. 2)

where i, f, o are the input, forget, and output gates respectively, c is the cell state, and h is the hidden state. Despite the gating mechanism, LSTM networks still suffer from information decay over very long sequences. The paper identifies a specific manifestation: 22.4% prediction error during the Spring Festival transition period, where the gap between training patterns and holiday load profiles exceeds what the LSTM's gating mechanism can compensate for through temporal memory alone.

## Transformer Self-Attention and Global Context

The Transformer architecture revolutionized sequence modeling through its self-attention mechanism, which computes pairwise attention scores across all positions:

Attention(Q, K, V) = softmax(QK^T / √d) V   (Eq. 3)

where Q, K, V are query, key, and value projections of the input, and d is the scaling dimension. Self-attention provides direct access to any position in the sequence, eliminating the sequential bottleneck of RNNs. For load forecasting, this enables the model to capture long-range dependencies such as daily or weekly periodic patterns. However, the global nature of standard self-attention can dilute fine-grained local patterns: the paper documents approximately ±15% error during PV fluctuation periods, where rapid local changes require focused attention that the uniform global attention distribution fails to provide. This motivates the local enhanced attention mechanism (mask M) in the proposed architecture.

## CNN-LSTM Hybrid and Information Loss

CNN-LSTM hybrid models combine CNN layers for local feature extraction with LSTM layers for temporal sequence modeling. The typical architecture passes CNN-extracted features as input to the LSTM:

h_t = LSTM(CNN(x_t), h_{t-1})   (Eq. 4)

While this sequential combination leverages the strengths of both architectures, the paper identifies a critical limitation: approximately 25% information loss rate during feature transmission from the CNN module to the LSTM module. The feature compression imposed by CNN pooling and the representational shift between convolutional and recurrent feature spaces cause cumulative degradation. This finding motivates the DAF module's dual-path design, which processes features from both the BiLSTM and Transformer branches in parallel before adaptive fusion, rather than in a loss-prone sequential cascade.

## Attention-Based Fusion Methods (CBAM, Self-Attention)

Existing attention-based fusion approaches including Convolutional Block Attention Module (CBAM) and standard self-attention fusion provide mechanisms for feature recalibration but have significant limitations for multi-source heterogeneous load data. CBAM applies channel and spatial attention sequentially within convolutional blocks but lacks temporal modeling capability. Standard self-attention fusion treats all features uniformly without distinguishing between feature channel contributions and temporal contributions as separate semantic spaces. The DAF module addresses these limitations through its dual-path architecture that explicitly separates and then recombines feature channel evaluation and temporal contribution evaluation, with the nonlinear interaction term enabling cross-dimensional coupling that existing attention fusion approaches cannot achieve.
