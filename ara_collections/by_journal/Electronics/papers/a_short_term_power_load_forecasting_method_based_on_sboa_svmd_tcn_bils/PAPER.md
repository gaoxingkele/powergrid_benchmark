---
title: "A Short-Term Power Load Forecasting Method Based on SBOA–SVMD-TCN–BiLSTM"
authors: ["Mao Yang", "Yiming Chen", "Guozhong Fang", "Chenglian Ma", "Yunjing Liu", "Jinxin Wang"]
year: 2024
venue: "Electronics"
doi: "10.3390/electronics13173441"
ara_version: "1.0"
domain: "Short-term electricity load forecasting; hybrid deep learning; signal decomposition"
keywords: ["secretary bird optimization algorithm", "successive variational mode decomposition", "temporal convolutional network", "BiLSTM", "temporal feature extraction", "short-term load forecasting", "permutation entropy", "mode mixing"]
claims_summary:
  - "Optimizing SVMD's compactness parameter toward minimum component permutation entropy yields more predictable, non-mixed sub-sequences (C01)."
  - "SVMD separates load frequency structure more cleanly than EMD-family decompositions, lowering forecast error with the forecaster held fixed (C02)."
  - "A decompose-then-forecast pipeline beats forecasting the raw series with the same model (C03)."
  - "Prepending TCN multi-scale feature extraction to a BiLSTM beats the recurrent net alone and shallow learners; the gain shrinks as the baseline captures more context (C04)."
  - "The hybrid's ranking advantage is season/peak-time robust but its absolute error tracks the load regime (C05)."
  - "Component-wise ensembles multiply training cost but keep inference latency negligible, staying deployable (C06)."
  - "Optimizer choice materially affects SVMD tuning; late-iteration stability distinguishes SBOA from SSA/GWO (C07)."
abstract: "Short-term electricity load forecasting provides a basis for day-ahead energy scheduling. To improve accuracy and deeply explore the temporal characteristics of load sequences, a method is proposed to extract predictable components based on the secretary bird optimization algorithm (SBOA)-optimized successive variational mode decomposition (SVMD). It decomposes the load sequence into multiple subsequences under different time series. A combined TCN–BiLSTM architecture mines the temporal characteristics of each load component to produce the short-term forecast. A case study uses annual 2018 electricity load data from a region in Belgium. The MAE of the TCN–BiLSTM model is reduced by 47.8%, 32.8%, and 11.5% versus other models; the RMSE by 42.9%, 39.2%, and 11.3%; with improved R²."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__10__a_short_term_power_load_forecasting_method_based_on_sboa_s__77aa7a9c07.pdf
---

# A Short-Term Power Load Forecasting Method Based on SBOA–SVMD-TCN–BiLSTM

## Overview
This paper proposes a decompose–optimize–predict–reconstruct pipeline for day-ahead short-term
load forecasting. The Secretary Bird Optimization Algorithm (SBOA) tunes the dominant parameter
(mode compactness / maxAlpha) of Successive Variational Mode Decomposition (SVMD) by minimizing the
permutation entropy of the resulting components, yielding four predictable, non-mode-mixed IMFs.
Each IMF is forecast by a hybrid TCN→BiLSTM model — TCN dilated causal convolutions extract
multi-scale local features and BiLSTM captures bidirectional temporal dependencies — and the
component forecasts are recombined. On a 2018 Belgian regional load dataset (35,040 points at
15-min sampling), the method beats EMD-family decomposition baselines (CEEMDAN/ICEEMDAN), a
no-decomposition ablation, and shallow/unidirectional forecasters (ELM, LSTM, BiLSTM), with the
advantage holding across seasons and peak periods.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (O1–O5) → gaps (G1–G2) → key insight → assumptions |
| [claims.md](logic/claims.md) | 7 falsifiable claims (C01–C07) |
| [concepts.md](logic/concepts.md) | 8 technical terms (SVMD, SBOA, TCN, BiLSTM, IMF, maxAlpha, permutation entropy, decompose-predict-reconstruct) |
| [experiments.md](logic/experiments.md) | 8 verification plans (E01–E08), directional only |
| [related_work.md](logic/related_work.md) | Typed dependency graph (RW01–RW08) + brief citation footprint |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |
| [solution/architecture.md](logic/solution/architecture.md) | Full pipeline / model component graph |
| [solution/algorithm.md](logic/solution/algorithm.md) | SVMD mode extraction + SBOA optimization (Eqs. 1–24) |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Data/hardware/software/protocols/config; no released code (analytical-from-paper) | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 12-node research DAG (all explicit) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 9 tables + 14 figures (each md + png) |
| evidence/tables/table1–9.md (+.png) | Parameter settings, permutation entropy, and all error-comparison tables |
| evidence/figures/figure1–14.md (+.png) | 8 architecture/flow diagrams + 6 quantitative result plots |

## Counts
- Claims: 7 (C01–C07)
- Experiments: 8 (E01–E08)
- Concepts: 8
- Tree nodes: 12
- Evidence: 9 tables + 14 figures = 23 objects (23 markdown + 23 png)
