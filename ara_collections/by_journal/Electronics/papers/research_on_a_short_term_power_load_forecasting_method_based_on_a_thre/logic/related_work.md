# Related Work

Typed dependency graph over the paper's 29 references. Works with a specific technical delta
against this paper get full `RW` blocks; the remaining background/infrastructure citations are
captured briefly at the end to preserve the full footprint.

## RW01: Ren, Jia & Wang, 2021 — CNN-LSTM hybrid STLF
- **DOI**: (PSGEC 2021, IEEE, pp. 182–186) — ref [16]
- **Type**: baseline / extends
- **Delta**:
  - What changed: This paper keeps the CNN-LSTM hybrid idea (LSTM temporal + CNN local spatial) but replaces its single-channel input with three independent per-modality LSTM channels fused late by CNN.
  - Why: Single-channel hybrids force heterogeneous modalities into one representation, causing entanglement (G1).
- **Claims affected**: C01, C02
- **Adopted elements**: The CNN-after-LSTM feature-extraction pattern; used directly as the "CNN-LSTM" comparison baseline (Tables 4, 5).

## RW02: Zhao, Zhang & Geng, 2024 — Deep multimodal data fusion
- **DOI**: 10.1145/... ACM Comput. Surv. 56, 1–36 — ref [17]
- **Type**: imports
- **Delta**:
  - What changed: Provides the theoretical foundation that independent encoding pathways followed by late fusion preserve modality-specific characteristics while enabling cross-modal interaction.
  - Why: Motivates the three-channel late-fusion design over early single-channel fusion.
- **Claims affected**: C01
- **Adopted elements**: The late-fusion / independent-pathway principle.

## RW03: Giacomazzi, Haag & Hopf, 2023 — Temporal Fusion Transformer for STLF
- **DOI**: (ACM e-Energy 2023, pp. 353–360) — ref [14]
- **Type**: bounds
- **Delta**:
  - What changed: Transformer self-attention captures global temporal dependencies but suffers quadratic complexity on long sequences; this paper avoids attention in favor of per-channel LSTM + Conv1D.
  - Why: Cited as a limitation of the attention route motivating the chosen architecture.
- **Claims affected**: C01
- **Adopted elements**: None (contrasted, not adopted).

## RW04: Lv, Wang, Long, Hu & Hu, 2024 — Spatiotemporal GNN for multi-area STLF
- **DOI**: 10.1016/j.engappai.2024.109398 — ref [15]
- **Type**: bounds
- **Delta**:
  - What changed: GNNs model spatial correlations between substations via predefined topology graphs; this paper notes their reliance on accurate grid-structure definitions often unavailable in practice, and instead mines cross-modal (not cross-substation) correlation with CNN.
  - Why: Justifies not requiring a grid topology graph.
- **Claims affected**: C01
- **Adopted elements**: None (contrasted).

## RW05: Li, Yu, Tian & Zhao, 2021 — LSTM-RNN for industrial-park STLF
- **DOI**: (AEEES 2021, pp. 684–689) — ref [19]
- **Type**: baseline
- **Delta**:
  - What changed: A single LSTM model; this paper reports its three-channel model's MAPE is "23.6% higher than that of the single LSTM model."
  - Why: The single-LSTM reference point for the headline improvement.
- **Claims affected**: C01, C02
- **Adopted elements**: The plain-LSTM comparison baseline (Tables 4, 5).

## RW06: Box–Jenkins ARIMA (as cited via ref [5])
- **DOI**: (ref [5]: Ji et al., Electr. Power Syst. Res. 2025, 244, 111551)
- **Type**: bounds
- **Delta**:
  - What changed: ARIMA removes non-stationarity via differencing but cannot integrate external variables (temperature, humidity) and adapts poorly to sudden load changes; deep multi-source model added instead.
  - Why: Classical-statistics limitation motivating deep learning.
- **Claims affected**: C01
- **Adopted elements**: None.

## Briefer citations (background / infrastructure / inline comparison)

- **[1] Hao et al., 2023** — urban residential electricity consumption factors (motivation, load magnitude context).
- **[2] Jiang et al., 2021** — electricity consumption & CO2 emissions in China (background).
- **[3] Hao et al., 2022** — digitalization & electricity intensity (background).
- **[4] Zou et al., 2023** — Phase Space Reconstruction + EMD-ELM STLF; source of the "1% accuracy → 0.3–0.8% fuel cost" figure (O2).
- **[6] Liu & Li, 2025** — GA-improved VMD-BP STLF (background on decomposition hybrids).
- **[7] Liu et al., 2025 (TDCN)** — temporal depthwise convolutional network (SVR-complexity discussion / conv STLF context).
- **[8] Chen et al., 2025** — hybrid deep learning building-load forecasting.
- **[9] Smyl et al., 2024** — ES-dRNN with dynamic attention.
- **[10] Du et al., 2021** — causality-mining combination forecasting.
- **[11] Cheng et al., 2017** — improved-entropy multi-energy load forecasting (LSTM single-step context).
- **[12] Chen et al., 2020/2021 (I-GWO-KELM)** — kernel-ELM STLF (CNN-LSTM hybrid context).
- **[13] Zeng & Li, 2013** — RBF neural network STLF (single-channel bottleneck context).
- **[18] Zhang et al., 2024** — sparrow-search + BiLSTM STLF (multi-source representation context).
- **[20] Wang et al., 2021** — LSTM residential load with weather features.
- **[21] Yalcinoz & Eminoglu, 2005** — neural-network distribution load forecasting.
- **[22] Greff et al., 2016** — "LSTM: A search space odyssey" (LSTM gating background).
- **[23] Mei et al., 2024** — IWOA-optimized CNN-BiLSTM.
- **[24] Zhang et al., 2020** — integrated LSTM STLF (long-term dependency background).
- **[25] Chua & Roska, 1993** — the CNN paradigm (CNN foundational).
- **[26] Dao et al., 2024** — Bayesian-optimized CNN-LSTM hydro-turbine fault diagnosis (CNN branch background).
- **[27] Farsi et al., 2021** — parallel deep LSTM-CNN STLF (parallel hybrid background).
- **[28] Yi et al., 2023** — self-attention deep LSTM-CNN with input reduction.
- **[29] Agga et al., 2022** — CNN + LSTM deep networks for STLF.

**Baseline not tied to a single reference**: TCN (Temporal Convolutional Network) is used as a comparison model in §4 without a dedicated citation; its hyperparameters were "selected as the best results after multiple experiments."
</content>
