# Related Work

Typed dependency graph. Full RW blocks for works with a specific technical delta; brief entries preserve the paper's remaining citation footprint.

## RW01: Duan, Xue & Tan, 2024 — SVMD (Improved BWO-TimeNet on SVMD)
- **DOI**: ref [28], J. Guangxi Norm. Univ. (Nat. Sci. Ed.) 2024
- **Type**: imports
- **Delta**:
  - What changed: This paper adopts SVMD (successive VMD, no preset K) as the decomposition front-end; here its key parameter (maxAlpha) is optimized by SBOA rather than by BWO.
  - Why: Avoid preset mode count and mode mixing; get more predictable components.
- **Claims affected**: C01, C02
- **Adopted elements**: The SVMD formulation (Eqs. 1–8) and successive extraction idea.

## RW02: Fu, Liu & Chen, 2024 — Secretary Bird Optimization Algorithm
- **DOI**: ref [29], Artif. Intell. Rev. 57:123
- **Type**: imports
- **Delta**:
  - What changed: SBOA is used as the metaheuristic to optimize SVMD's compactness parameter (objective = minimum permutation entropy).
  - Why: Global search that avoids local optima; stable convergence.
- **Claims affected**: C01, C07
- **Adopted elements**: The hunting (Eqs. 12/15/17) and escape (Eq. 22) update rules verbatim.

## RW03: Zhang, Huang & Liao, 2023 — TCN for load (GBDT + TCN)
- **DOI**: ref [20], Appl. Energy 351:121768
- **Type**: extends
- **Delta**:
  - What changed: TCN's dilated causal convolution is used here as the per-component feature extractor feeding a BiLSTM, instead of standalone TCN forecasting.
  - Why: TCN captures long-range multi-scale local features without recurrence.
- **Claims affected**: C04
- **Adopted elements**: Dilated causal convolution + residual unit design (Eqs. 25–26).

## RW04: Yang, Wu & Ding, 2021 / Zhu, Zeng & Chen, 2024 — BiLSTM for load
- **DOI**: refs [18], [19] (ref [19] = Electronics 2024, 13, 3098, CrossRef)
- **Type**: extends
- **Delta**:
  - What changed: BiLSTM is used as the recurrent head on TCN-extracted features rather than directly on raw/selected features.
  - Why: Bidirectional context improves accuracy/stability; ref [19] is also a same-journal BiLSTM baseline family.
- **Claims affected**: C04
- **Adopted elements**: Bidirectional LSTM structure (Eqs. 27–32 + bidirectional wiring).

## RW05: Lu, Huo & Yu, 2023 — LSTM baseline
- **DOI**: ref [16], Proc. CSEE 43:2273
- **Type**: baseline
- **Delta**:
  - What changed: LSTM used as a comparison forecaster on the same IMFs.
  - Why: Establish the gain of the hybrid over a plain recurrent model.
- **Claims affected**: C04, C05
- **Adopted elements**: LSTM gating equations.

## RW06: EMD / VMD / CEEMDAN-family decomposition baselines
- **DOI**: refs [21] (EMD), [22] (VMD), [23] (MPA-VMD)
- **Type**: bounds / baseline
- **Delta**:
  - What changed: EMD/VMD framed as prior decomposition art; CEEMDAN and ICEEMDAN (EMD-family) serve as head-to-head decomposition baselines (Table 3/4).
  - Why: Show SVMD reduces mode mixing and error relative to these.
- **Claims affected**: C02
- **Adopted elements**: Comparison framing; parameter settings for CEEMDAN/ICEEMDAN.

## RW07: Permutation-entropy for signal complexity
- **DOI**: refs [30] (Electronics 2019, 8, 61, CrossRef), [31]
- **Type**: imports
- **Delta**:
  - What changed: Permutation entropy adopted as the optimization objective and decomposition-quality metric.
  - Why: Lower entropy ⇒ higher predictability.
- **Claims affected**: C01, C07
- **Adopted elements**: Permutation-entropy complexity measure.

## RW08: CNN-RNN hybrid forecasting
- **DOI**: refs [24] (CNN-LSTM), [25] (CNN-BiLSTM)
- **Type**: bounds
- **Delta**:
  - What changed: Prior CNN-RNN hybrids motivate but are argued to be inefficient on long-term dependencies; this paper uses TCN (not plain CNN) + BiLSTM.
  - Why: Excessive convolution reduces long-term efficiency.
- **Claims affected**: C04

## Brief citation footprint (background / infrastructure / inline comparison)
- [1][2] load-forecasting reviews (Kong 2023; Zhu 2021) — motivation.
- [3][4] new-power-system scheduling (Yang 2024; Hong 2024) — application context.
- [5] multidimensional feature extraction for STLF (Kim 2022) — load multi-periodicity.
- [6] chaotic time series; [7] multivariate linear regression; [8] Holt-Winters + TCN — traditional/statistical methods.
- [9] SVR; [10] random forest; [11] stacked deep learning PV (Electronics 2023); [12] ANN; [13] deep learning IES — shallow/ML methods.
- [14] AlexNet/CNN (Krizhevsky 2017); [15] RNN with attention — deep-model lineage.
- [17] quantum-weighted multi-level GRU (Wang 2022) — GRU comparison context.
- [26] image-encoding deep learning (Estebsari 2020, Electronics); [27] seq2seq transfer learning STLF (Laitsos 2024, Electronics) — temporal-continuity challenge framing.
