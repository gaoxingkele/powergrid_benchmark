# Claims

## C01 — DAF Dual-Path Adaptive Weighting Superiority

**Claim:** The DAF module's dual-path (Feature Channel + Temporal Contribution) adaptive weighting mechanism captures cross-dimensional coupling between feature channels and temporal positions more effectively than static or sequential fusion approaches.

**Grounding:** Table 2 and Table 3 provide comparative metrics. The full DAF-BT model achieves MAPE=1.58% vs. CNN-LSTM (2.89%), Transformer (2.31%), and BiLSTM-Transformer without DAF (2.04%). Ablation results (Table 3) show that adding DAF to BiLSTM (BiLSTM-DAF: MAPE=1.92%) and Transformer (Transformer-DAF: MAPE=1.74%) consistently improves over their non-DAF counterparts (BiLSTM: MAPE=2.18%; Transformer: MAPE=2.31%), demonstrating the module's generality across different backbone architectures.

**Confidence:** High (supported by comprehensive ablation and baseline comparisons in Tables 2 and 3, Figures 5-6, 11-12).
**Evidence:** Table 2, Table 3, Figure 5, Figure 6, Figure 11, Figure 12.

---

## C02 — BiLSTM-Transformer Cascade Complementary Representation

**Claim:** The BiLSTM-Transformer cascade architecture extracts both local bidirectional dependencies (via BiLSTM) and global contextual patterns (via Transformer), where neither component alone provides sufficient representational power for accurate load forecasting.

**Grounding:** Ablation results (Table 3) show BiLSTM alone achieves MAPE=2.18%, Transformer alone achieves MAPE=2.31%, while BiLSTM-Transformer (without DAF) achieves MAPE=2.04%. The cascade improves over both individual components, confirming complementary benefits. Further gains with DAF (full model: MAPE=1.58%) indicate that the cascade provides richer intermediate representations for the fusion module to exploit.

**Confidence:** High (directly supported by ablation variants isolating each component).
**Evidence:** Table 3, Figure 11, Figure 12.

---

## C03 — Nonlinear Interaction Term for Cross-Dimensional Coupling

**Claim:** The DAF module's nonlinear interaction term (λ · Fs ⊙ Ft) enables the model to learn which historical patterns matter under specific environmental profiles, creating a dynamic coupling between feature channel importance and temporal contribution.

**Grounding:** The interaction term is defined as the element-wise product of the Feature Channel weight vector (ω_c) and the Temporal Contribution weight vector (ω_t), scaled by a learnable parameter λ. This allows the model to modulate feature importance differently at different time positions. The full model (with interaction) achieves substantial improvements over variants where feature and temporal contributions would be combined additively or independently.

**Confidence:** Medium (the interaction term is theoretically motivated, but the paper does not provide an explicit ablation experiment isolating the interaction term from the individual channel/temporal units).
**Evidence:** Section on DAF module (Figures 3-4), Table 3 (full model vs. partial variants).

---

## C04 — Superior Peak Prediction and Transition Stability

**Claim:** The DAF-BT model achieves superior peak prediction accuracy and stability at load transition boundaries (weekend effect, PV fluctuation periods) compared to baseline models.

**Grounding:** Figures 7-10 present daily and weekly load forecasting curves. The DAF-BT predictions more closely track actual load curves during weekend transitions and peak demand periods. Figure 6 shows representative forecasting model comparisons where the proposed model maintains tighter tracking during sharp ramps. Quantitative error distributions in Figures 8 and 10 confirm lower error dispersion for the proposed model across all time scales evaluated.

**Confidence:** High (qualitative curve comparisons in Figures 6, 7, 9 and quantitative error distributions in Figures 8, 10 consistently support this claim).
**Evidence:** Figure 6, Figure 7, Figure 8, Figure 9, Figure 10.

---

## C05 — Lightweight DAF Overhead for Significant Accuracy Gain

**Claim:** The DAF module introduces minimal computational overhead (0.12M additional parameters, 1.8ms inference time increase) while delivering a 0.46% MAPE reduction (from 2.04% to 1.58%).

**Grounding:** Table 4 reports computational complexity: the full DAF-BT model has 1.28M parameters vs. BiLSTM-Transformer (1.16M parameters, delta 0.12M). Training time increases from 22.3s/epoch (BiLSTM-Transformer) to 24.5s/epoch (DAF-BT), and inference time from 10.6ms to 12.4ms. The marginal overhead contrasts with alternative approaches that stack additional layers (which would incur proportionally larger costs).

**Confidence:** High (directly quantified in Table 4 with per-component breakdown).
**Evidence:** Table 4.

---

## C06 — Fusion Mechanism Dominance over Temporal Layer Stacking

**Claim:** The feature fusion mechanism (DAF module) is more critical for accuracy improvement than stacking additional temporal layers — Transformer-DAF (MAPE 1.74%) outperforms BiLSTM-Transformer (MAPE 2.04%) despite having a simpler temporal backbone.

**Grounding:** This is a direct finding from the ablation study (Table 3). Transformer-DAF (single-direction Transformer with DAF) achieves MAPE=1.74% vs. BiLSTM-Transformer (bidirectional LSTM + Transformer without DAF) at MAPE=2.04%. The 0.30% MAPE advantage of the DAF-equipped simpler backbone over the more complex temporal cascade without DAF demonstrates that fusion quality dominates the accuracy ceiling more than temporal depth.

**Confidence:** High (directly supported by ablation results in Table 3).
**Evidence:** Table 3.
