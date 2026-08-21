---
title: "A Power Load Forecasting Method Based on Intelligent Data Analysis"
authors: [He Liu, Xuanrui Xiong, Biao Yang, Zhanwei Cheng, Kai Shao, Amr Tolba]
year: 2023
venue: "Electronics"
doi: "10.3390/electronics12163441"
ara_version: "1.0"
domain: "Time-series load forecasting / smart-grid data analysis"
keywords: [power forecasting, data analysis, CEEMDAN decomposition, LSTM forecasting, signal decomposition, sliding window, empirical mode decomposition, non-stationary time series]
claims_summary:
  - "Decomposing non-stationary residential load into trend/periodic/random sub-components before neural forecasting lowers error versus forecasting the raw signal."
  - "Adaptive-noise ensemble decomposition (CEEMDAN) separates load components more cleanly for forecasting than plain EMD, by suppressing mode mixing."
  - "The decomposition-based forecaster improves accuracy and stability jointly (RMSE and MAE fall together across time scales), indicating a representational rather than metric-specific gain."
  - "A sliding window spanning multiple periodic cycles is required for the decomposition to separate trend from periodicity."
  - "CEEMDAN components of residential load map onto distinct physical roles (stochastic / periodic / trend), enabling interpretable per-component modeling."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__07__a_power_load_forecasting_method_based_on_intelligent_data__f0d322f4c0.pdf"
abstract: "Abnormal electricity consumption behavior not only affects the safety of power supply but also damages the infrastructure of the power system, posing a threat to the secure and stable operation of the grid. Predicting future electricity consumption plays a crucial role in resource management in the energy sector. Analyzing historical electricity consumption data is essential for improving the energy service capabilities of end-users. To forecast user energy consumption, this paper proposes a method that combines adaptive noise-assisted complete ensemble empirical mode decomposition (CEEMDAN) with long short-term memory (LSTM) networks. Firstly, considering the challenge of directly applying prediction models to non-stationary and nonlinear user electricity consumption data, the adaptive noise-assisted complete ensemble empirical mode decomposition algorithm is used to decompose the signal into trend components, periodic components, and random components. Then, based on the CEEMDAN decomposition, an LSTM prediction sub-model is constructed to forecast the overall electricity consumption by using an overlaying approach. Finally, through multiple comparative experiments, the effectiveness of the CEEMDAN-LSTM method is demonstrated, showing its ability to explore hidden temporal relationships and achieve smaller prediction errors."
---

# A Power Load Forecasting Method Based on Intelligent Data Analysis

## Overview

The paper addresses short-term residential electricity load forecasting on non-stationary,
nonlinear consumption data. Its contribution is a two-stage pipeline, **CEEMDAN-LSTM**: (1) an
adaptive-noise complete ensemble empirical mode decomposition (CEEMDAN), applied through a
large sliding window, decomposes each user's load series into a set of intrinsic mode functions
(IMFs) plus a residual that separate the signal into stochastic, periodic, and trend content; and
(2) a per-component LSTM sub-model (with batch normalization, dropout, and three dense layers)
forecasts each component, and the component forecasts are reconstructed (overlaid) into the final
load prediction. On smart-meter data from 50 Irish users, evaluated by RMSE and MAE at hourly and
daily granularity, CEEMDAN-LSTM reports lower error than LSTM, RNN, and EMD-LSTM baselines. The
paper is largely methodological/analytical: it presents the decomposition mathematics (EMD → EEMD
→ CEEMDAN), the network design, and two experiment sets (a decomposition analysis and a prediction
comparison); it releases no code.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable claims (C01–C05) |
| [concepts.md](logic/concepts.md) | Key technical terms (CEEMDAN, EMD, EEMD, IMF, mode mixing, sliding-window decomposition, LSTM, BN, dropout, RMSE/MAE) |
| [experiments.md](logic/experiments.md) | 3 verification plans (E01–E03), directional only |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the paper's 48 references |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |
| [solution/method.md](logic/solution/method.md) | The CEEMDAN + sliding-window + per-component LSTM forecasting pipeline |
| [solution/architecture.md](logic/solution/architecture.md) | LSTM sub-model network architecture |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Data (Irish smart meters), Keras/CuDNNLSTM runtime, protocols | — |
| [configs/model.md](src/configs/model.md) | Concrete network hyperparameters (layer sizes, batch, LR, dropout, CEEMDAN noise) | C01, C02 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG of the method's design decisions and experiments |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 4 tables + 10 figures |
