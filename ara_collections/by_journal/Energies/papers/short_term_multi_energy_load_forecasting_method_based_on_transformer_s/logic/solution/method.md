# Method: TSTG Formulations

## Notation

Let N be the number of buildings (nodes), D the number of energy load types (features), T_hist the input time window, d_model the hidden dimension, and H the number of attention heads.

---

## 1. Input Embedding

Each time step t for each node n is linearly projected from D to d_model, and sinusoidal positional encoding is added:

```
X_emb[n, t, :] = X_in[n, t, :] · W_emb + PE(t)
                                   (Eq. 1)
```

where W_emb ∈ ℝ^{D × d_model} and PE(t) is the sinusoidal positional encoding at position t.

---

## 2. Multi-Head Spatio-Temporal Attention

In each head h, the module computes parallel attention over the time axis and the feature axis. For a given head, let Q_h, K_h, V_h be the query, key, value projections for the time dimension, and Q'_h, K'_h, V'_h for the feature dimension.

### 2.1 Mutual Information Calculation

Given two vectors u_i, u_j ∈ ℝ^{d_n} (where d_n is the projection dimension per head), the mutual information is estimated via a bilinear form:

```
MI(u_i, u_j) = σ( u_i^T · W_mi · u_j )
                                     (Eq. 2)
```

where W_mi ∈ ℝ^{d_n × d_n} is a learnable bilinear weight matrix and σ(·) is a nonlinear activation.

### 2.2 Temporal Attention with MI

For the temporal axis, attention from time i to time j:

```
A_time(i, j) = softmax_j( (q_i · k_j^T) / √d_k  +  λ · MI(q_i, k_j) )
                                     (Eq. 3)
```

where λ is a learnable scalar controlling the MI contribution. The output is:

```
Z_time[h] = A_time · V_time
                                     (Eq. 4)
```

### 2.3 Feature Attention with MI

For the feature (energy-type) axis, attention from feature a to feature b:

```
A_feat(a, b) = softmax_b( (q'_a · k'_b^T) / √d_k  +  λ' · MI(q'_a, k'_b) )
                                     (Eq. 5)
```

Output:

```
Z_feat[h] = A_feat · V_feat
                                     (Eq. 6)
```

### 2.4 Multi-Head Combination

Each head's temporal and feature outputs are concatenated, then all heads are concatenated and projected:

```
Z_attn = Concat( [ Concat(Z_time[h], Z_feat[h]) for h = 1..H ] ) · W_o
                                     (Eq. 7)
```

where W_o ∈ ℝ^{(H · 2 · d_n) × d_model}.

---

## 3. Dynamic Adaptive Graph Convolution

### 3.1 Physical Adjacency

A_phy ∈ ℝ^{N × N} is a pre-defined static adjacency (symmetrically normalized):

```
A_phy = D_phy^(-1/2) · A_raw · D_phy^(-1/2)
                                     (Eq. 8)
```

where A_raw is the binary/weighted physical connectivity matrix and D_phy is its degree matrix.

### 3.2 MI-Based Feature Similarity

For each pair of nodes (i, j), given their feature representations Z_i, Z_j ∈ ℝ^{d_model} from the attention module output, compute the MI similarity:

```
S_mi(i, j) = tanh( Z_i^T · W_sim · Z_j )
                                     (Eq. 9)
```

where W_sim ∈ ℝ^{d_model × d_model}. The similarity matrix A_mi is obtained by applying softmax row-wise to S_mi.

### 3.3 Dynamic Adjacency Fusion

The final adjacency matrix is a learnable fusion of physical and MI-based similarity:

```
A_dyn = gate_1 · A_phy  +  gate_2 · A_mi
                                     (Eq. 10)
```

where gate_1, gate_2 ∈ (0, 1) are gating parameters learned via a sigmoid network conditioned on current load features.

### 3.4 Graph Convolution Update

Node representations are updated via a single-layer graph convolution:

```
Z_gcn = ReLU( A_dyn · Z_attn · W_gcn )
                                     (Eq. 11)
```

where W_gcn ∈ ℝ^{d_model × d_model} is a learnable weight matrix shared across nodes.

---

## 4. Training Objective

The model is trained end-to-end by minimizing the mean absolute error (MAE) between predicted and actual loads for all energy types over the forecast horizon:

```
L = (1 / (N · T_pred · D)) · Σ_n Σ_t Σ_d | Y_hat[n, t, d] - Y[n, t, d] |
                                     (Loss)
```

No separate regularization or auxiliary losses are reported.
