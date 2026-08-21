# Experiments: TSTG Paper

## E01 — Full Benchmark Comparison

**Purpose:** Evaluate TSTG against 11 state-of-the-art baselines across all three load types and four forecast horizons. Tests claim C06 and provides the primary evidence for C07.

**Baselines:**
- Transformer variants: FEDformer, LightTS, Pyraformer, TiDE, Autoformer, Informer, Reformer, TSMixer
- Statistical: ARIMA, Prophet

**Metrics:** MAE, RMSE, MAPE, R2

**Horizons:** 6 h, 12 h, 24 h, 96 h

**Load types:** Electric, Cooling, Heating

**Implementation:** All baselines run on same train/val/test split (7:1:2) and same dataset. Hyperparameters per baseline per original paper. 5 random seeds with mean ± std reported.

**Expected outcome:** TSTG achieves lowest MAE/RMSE/MAPE and highest R2 across all 12 settings (3 loads x 4 horizons).

**Evidence source:** Table 1

---

## E02 — Computational Efficiency Analysis

**Purpose:** Measure training time, inference time, and parameter count for TSTG versus representative baselines. Contextualizes the accuracy gains of claim C07 against computational cost.

**Metrics:** Training time (s), Inference time (s)

**Procedure:** All models run on same GPU hardware. Training time measured as wall-clock from first batch to last epoch. Inference time measured as per-sample average over test set.

**Expected outcome:** TSTG has moderate training time (2700 s) and fast inference (0.72 s), not the fastest (LightTS: 600 s/0.14 s) but much better than heavy Transformers (Autoformer: 7200 s/1.54 s), while dominating accuracy.

**Evidence source:** Table 2

---

## E03 — Multi-Energy Coupling Analysis

**Purpose:** Compare joint multi-energy forecasting (Case 2) against independent per-load forecasting (Case 1) to quantify the benefit of modeling inter-load coupling. Tests claim C03.

**Cases:**
- Case 1: Three independent TSTG models, one per energy type
- Case 2: Single TSTG model jointly forecasting all three loads

**Metrics:** MAE, RMSE

**Expected outcome:** Case 2 (joint) achieves lower error on all three loads, confirming that modeling inter-load coupling reduces forecasting error.

**Evidence source:** Table 3

---

## E04 — Auxiliary Information Analysis

**Purpose:** Ablate the contribution of calendar and meteorological auxiliary features to determine their relative importance. Tests claim C04.

**Cases:**
- Case 1: No auxiliary features (baseline)
- Case 2: Calendar only (hour, day of week, month)
- Case 3: Meteorological only (temperature, humidity)
- Case 4: Both calendar and meteorological

**Metrics:** MAE, RMSE (electric, cooling, heating at 24 h horizon)

**Expected outcome:** Ranking: Case 4 > Case 2 > Case 3 > Case 1. Calendar features dominate meteorological, but fusing both gives best results.

**Evidence source:** Table 4

---

## E05 — Module Ablation Experiments

**Purpose:** Isolate the contribution of each TSTG component by removing or replacing individual modules. Tests claims C01, C02, and C05.

**Variants:**
- -StaticGCN: Replace dynamic graph with static physical adjacency only
- -GAT: Replace graph convolution with graph attention (GAT)
- -DynamicGCN: Remove graph module entirely
- -WO-MSA: Without multi-head spatio-temporal attention
- -SA: Replace multi-head attention with single-head attention (no MI)
- -MSA: Replace MI-augmented attention with standard multi-head attention
- TSTG (full): Complete model

**Metrics:** MAE, RMSE (electric, cooling, heating at 24 h horizon)

**Expected outcome:** TSTG full > all variants; -SA (biggest drop) > -MSA > -DynamicGCN > -StaticGCN > -GAT > -WO-MSA, confirming that both MI attention and dynamic graph are essential and synergistic.

**Evidence source:** Table 5
