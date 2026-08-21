# Concepts

## C01 — DAF-BT

**Definition:** The full proposed model: Dynamic Adaptive Fusion — Bidirectional LSTM Transformer. A hybrid deep learning architecture that combines BiLSTM, Transformer with local enhanced attention, and a Dynamic Adaptive Fusion (DAF) module for short-term power load forecasting.

**Mathematical Formulation:** DAF-BT(x) = Output(DAF(BiLSTM(Transformer(x))))

**Paper Reference:** Throughout — the complete proposed framework.

---

## C02 — Dynamic Adaptive Fusion (DAF)

**Definition:** A dual-path adaptive weighting module that computes context-dependent importance weights for feature channels and temporal contributions, combined with a nonlinear interaction term for cross-dimensional coupling learning.

**Mathematical Formulation:** DAF(F_c, F_t) = ω_c · F_c ⊕ ω_t · F_t ⊕ λ(ω_c ⊙ ω_t)

**Paper Reference:** Section 3, Figures 3-4.

---

## C03 — Feature Channel Adaptive Unit

**Definition:** A sub-module of DAF that generates adaptive weights for each feature channel (e.g., load, temperature, wind speed) based on the current input context, enabling the model to emphasize informative channels and suppress irrelevant ones dynamically.

**Mathematical Formulation:** ω_c = σ(W_c · [F_c; F_t] + b_c), where ω_c ∈ ℝ^d_c are channel importance weights.

**Paper Reference:** Section 3.3, Figure 4.

---

## C04 — Temporal Contribution Evaluation Unit

**Definition:** A sub-module of DAF that assesses the contribution significance of each time step's hidden representation, allowing the model to focus on temporally relevant patterns while downweighting uninformative time positions.

**Mathematical Formulation:** ω_t = σ(W_t · [F_c; F_t] + b_t), where ω_t ∈ ℝ^d_t are temporal importance weights.

**Paper Reference:** Section 3.3, Figure 4.

---

## C05 — Local Enhanced Attention Mechanism (Mask M)

**Definition:** A modified Transformer self-attention mechanism that incorporates a local mask matrix M to constrain attention to a neighborhood window around each position, preserving fine-grained local patterns that standard global self-attention may dilute.

**Mathematical Formulation:** Attention(Q,K,V) = softmax(QK^T/√d + M)V, where M_ij = 0 if |i-j| ≤ w and M_ij = -∞ otherwise.

**Paper Reference:** Section 3.2, Figure 3.

---

## C06 — BiLSTM Bidirectional Dependency

**Definition:** The use of two LSTM layers processing the input sequence in forward and backward directions, capturing both past-to-future and future-to-past temporal dependencies at each time step.

**Mathematical Formulation:** h_t = [h_t^f; h_t^b], where h_t^f = LSTM_f(x_1,...,x_t) and h_t^b = LSTM_b(x_T,...,x_t).

**Paper Reference:** Section 3.2.

---

## C07 — Global Contextual Features

**Definition:** Long-range dependencies and holistic sequence patterns captured by the Transformer's self-attention mechanism, which computes pairwise attention scores across all positions in the sequence.

**Mathematical Formulation:** GlobalContext(X) = Attention(XW_Q, XW_K, XW_V) as defined in Equation (3).

**Paper Reference:** Section 3.1 (Transformer background) and Section 3.2 (model architecture).

---

## C08 — Nonlinear Interaction Term (λ)

**Definition:** A learnable scalar parameter λ that scales the element-wise product of the Feature Channel weights and Temporal Contribution weights, enabling cross-dimensional coupling between the two weight spaces.

**Mathematical Formulation:** Interaction = λ · (ω_c ⊙ ω_t), where λ is a learned parameter and ⊙ denotes element-wise multiplication.

**Paper Reference:** Section 3.3, Equation (9).

---

## C09 — Weekend Effect

**Definition:** A systematic pattern in power load where consumption profiles on weekends differ substantially from weekday profiles due to reduced commercial/industrial activity, creating challenging transition periods between Friday and Saturday and between Sunday and Monday.

**Mathematical Formulation:** Non-quantified; observed as residual error clusters in daily load forecasting comparisons (Figures 7-8).

**Paper Reference:** Figures 7-10, discussed in context of model evaluation at multiple time scales.

---

## C10 — Information Retention Rate

**Definition:** The proportion of useful feature information preserved through sequential processing stages in a hybrid model. The paper identifies a 25% information loss rate in CNN-LSTM cascade hybrids, motivating the DAF approach.

**Mathematical Formulation:** Retention = Info_out / Info_in, where Info refers to task-relevant signal variance retained after feature transformation.

**Paper Reference:** Section 2 (Related Work), motivation gap G2.
