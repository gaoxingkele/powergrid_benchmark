# Claims: TSTG Paper

## C01 — MI-Augmented Attention Captures Nonlinear/Asymmetric Dependencies

**Claim:** Augmenting standard scaled dot-product attention with a mutual-information term, applied in parallel over both the time axis and the feature (energy-type) axis, captures nonlinear and asymmetric load dependencies that linear dot-product attention alone misses.

**Falsifiability:** A controlled experiment comparing TSTG against a variant that uses standard dot-product attention (without MI) on the same architecture should show statistically significant degradation across all energy types and horizons. If the MI term contributes nothing beyond linear attention, the variant would match TSTG.

**Evidence:** Table 5 ablation — removing MI attention (-SA, -MSA) increases MAE/RMSE across all load types. The -SA variant (single-head, no MI) shows the largest degradation.

---

## C02 — Dynamic Adjacency Matrix Outperforms Static Graph Structures

**Claim:** Fusing a static physical adjacency matrix with an MI-based, feature-driven similarity graph that is recomputed from real-time load representations produces a dynamic adjacency matrix that models shifting spatial dependencies better than any static graph structure.

**Falsifiability:** If the dynamic component adds no benefit, then the model with only the static physical adjacency plus the same convolution should match or exceed TSTG. An ablation replacing the dynamic fusion with a fixed graph (physical-only or similarity-only) should underperform.

**Evidence:** Table 5 ablation — -DynamicGCN (static adjacency only) and -GAT (no convolution, no dynamic) both underperform full TSTG. -StaticGCN also degrades.

---

## C03 — Joint Multi-Energy Forecasting Reduces Error vs. Independent Forecasting

**Claim:** Jointly modeling electric, cooling, and heating loads in a single encoder-decoder with spatio-temporal joint optimization exploits inter-load correlation and yields lower forecasting error compared to training three independent models (one per energy type).

**Falsifiability:** If inter-load correlation is unimportant, independent per-energy models would match or outperform the joint model. An experiment comparing Case 1 (independent) vs. Case 2 (joint) on identical architecture and data should show joint outperforming.

**Evidence:** Table 3 — Case 2 (joint forecasting) achieves lower MAE/RMSE across all three load types compared to Case 1 (independent).

---

## C04 — Calendar Auxiliary Features Carry More Predictive Value Than Meteorological Features

**Claim:** Calendar features (hour of day, day of week, month) encode the dominant temporal patterns in multi-energy consumption and contribute more to forecasting accuracy than meteorological features (temperature, humidity). Combining both is optimal.

**Falsifiability:** If meteorological features dominate, then adding weather alone (Case 3) would outperform adding calendar alone (Case 2). A systematic ablation of auxiliary inputs should rank: both > calendar-only > weather-only > no-aux.

**Evidence:** Table 4 — Case 3 (only weather) MAE = 1.721/0.540/0.699; Case 2 (only calendar) MAE = 0.850/0.257/0.358; Case 4 (both) MAE = 0.711/0.216/0.245 for electric/cooling/heating. Calendar alone reduces error by approximately 2x versus weather alone.

---

## C05 — MI-Attention and Dynamic Graph Are Synergistic

**Claim:** The MI-augmented multi-head spatio-temporal attention module and the dynamic adaptive graph convolution module interact synergistically — the combined improvement from using both together is greater than the sum of individual improvements from either module in isolation.

**Falsifiability:** If the modules are independent, then the performance of the full model should be predictable from the product (or additive combination) of the module-level ablations. A superadditive improvement (full model improvement > improvement from attention-only + improvement from graph-only) indicates synergy.

**Evidence:** The gap between full TSTG and the best single-module variant in Table 5 (-DynamicGCN or -MSA or -SA) is larger than the sum of the gaps between single-module variants and the worst. Full TSTG MAE (electric, 24h) ≈ 0.711, while -DynamicGCN ≈ 1.064, -SA ≈ 1.253 — the synergy gap is substantial.

---

## C06 — End-to-End Spatio-Temporal Joint Optimization Outperforms All Baselines

**Claim:** TSTG's end-to-end encoder-decoder with spatio-temporal joint optimization achieves lower forecasting error across all load types (electric, cooling, heating) and all forecast horizons (6/12/24/96 h) compared to state-of-the-art Transformer variants (FEDformer, Autoformer, Informer, Pyraformer, Reformer), MLP-based models (LightTS, TiDE, TSMixer), and statistical models (ARIMA, Prophet).

**Falsifiability:** If any baseline matches or exceeds TSTG on any load type or horizon, the claim is weakened. A comprehensive benchmark (Table 1) with consistent metrics (MAE, RMSE, MAPE, R2) should show TSTG best across all settings.

**Evidence:** Table 1 — TSTG achieves lowest MAE/RMSE/MAPE and highest R2 across all three load types and all four horizons. For electric 24h: TSTG MAE 0.711 vs. next best (FEDformer) 1.270.

---

## C07 — Dynamic MI Adaptivity Trades Quadratic Compute for Dominant Accuracy

**Claim:** The dynamic MI-based attention and graph modules introduce O(T^2 + D^2) per-layer complexity and O(N^2) graph similarity cost, but the accuracy gains are large enough to justify the added compute, placing TSTG at a favorable accuracy-to-efficiency trade-off point among deep learning models.

**Falsifiability:** If the compute overhead is not justified, TSTG would be either (a) slower than all baselines without dominating accuracy, or (b) only marginally better than a much faster model. Training time (2700 s) and inference time (0.72 s) must be reported alongside accuracy to establish the trade-off.

**Evidence:** Table 2 — TSTG trains in 2700 s (vs. FEDformer 3900 s, Autoformer 7200 s, LightTS 600 s) and infers in 0.72 s (competitive with TiDE 0.85 s, faster than FEDformer 1.20 s). It is not the fastest but achieves the best accuracy.
