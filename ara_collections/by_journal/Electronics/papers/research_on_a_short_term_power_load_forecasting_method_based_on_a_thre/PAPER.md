---
title: "Research on a Short-Term Power Load Forecasting Method Based on a Three-Channel LSTM-CNN"
authors: ["Xiaojing Zhao", "Huimin Peng", "Lanyong Zhang", "Hongwei Ma"]
year: 2025
venue: "Electronics"
doi: "10.3390/electronics14112262"
ara_version: "1.0"
domain: "Short-term power load forecasting / multi-source deep learning time series"
keywords: ["three-channel model", "LSTM-CNN", "short-term load forecasting", "multi-source feature fusion", "cross-modal correlation", "Conv1D", "smart grid dispatching", "MAPE"]
claims_summary:
  - "Encoding each heterogeneous modality in its own LSTM channel and fusing late with a CNN beats forcing all modalities through a single-channel encoder."
  - "Stacking CNN feature extraction on top of LSTM recovers cross-modal correlation that an LSTM-only model leaves on the table."
  - "A non-saturating, non-dead-gradient activation (Leaky ReLU) fits this recurrent-convolutional stack better than saturating (Sigmoid/Tanh) or zero-clipping (ReLU) activations."
  - "Plain Adam's first-moment estimate aligns with the gradient patterns of a multi-channel LSTM-CNN better than SGD, RMSprop, or Nadam."
  - "For same-time-next-day forecasting, a one-day historical lookback aligned with the target hour beats longer lookbacks, which inject noise."
  - "Independent-encode-then-fuse yields the gentlest prediction residuals, especially at abrupt load transitions."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__01__research_on_a_short_term_power_load_forecasting_method_bas__4bf42c2879.pdf"
abstract: "Aiming at addressing the problem of insufficient fusion of multi-source heterogeneous features in short-term power load forecasting, this paper proposes a three-channel LSTM-CNN hybrid forecasting model. This method extracts the temporal characteristics of time, weather, and historical loads through independent LSTM channels and realizes cross-modal spatial correlation mining by using a Convolutional Neural Network (CNN). The time channel takes hour, week, and holiday codes as input to capture the daily/weekly cycle patterns. The meteorological channel integrates real-time data such as temperature and humidity and models the nonlinear delay effect between them and the load. The historical load channel sequence of the past 24 h is analyzed to interpret the internal trend and fluctuation characteristics. The output of the three channels is concatenated and then input into a one-dimensional convolutional layer. Cross-modal cooperative features are extracted through local perception. Finally, the 24 h load prediction value is output through the fully connected layer. The experimental results show that the prediction model based on the three-channel LSTM-CNN has a better prediction effect compared with the existing models, and its average absolute percentage error on the two datasets is reduced to 1.367% and 0.974%, respectively. The research results provide an expandable framework for multi-source time series data modeling, supporting the precise dispatching of smart grids and optimal energy allocation."
---

# Research on a Short-Term Power Load Forecasting Method Based on a Three-Channel LSTM-CNN

## Overview

The paper proposes a **three-channel LSTM-CNN** hybrid model for short-term power load
forecasting (STLF). Its core design decision is architectural: rather than concatenating time,
weather, and historical-load features into one input tensor for a single-channel encoder, it gives
each modality its **own** LSTM channel (so periodicity, thermal-inertia delay, and trend/stochastic
structure are each encoded in a representation space suited to it), transposes and concatenates the
three channels' neuron outputs, then applies a **two-layer 1-D CNN + max-pooling + fully connected
head** to mine cross-modal correlations and emit a full next-day (24-point) load curve. On two
public datasets (a Tétouan, Morocco distribution network for 2017; the Electrician Cup competition
set) the model reaches MAPE of 1.367% and 0.974%, beating LSTM, CNN-LSTM, and TCN baselines. The
work also reports ablations over activation function, optimizer, and historical-load lookback
length that fix the final configuration (Leaky ReLU, Adam, one-day lookback).

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (multi-source heterogeneity, single-channel entanglement) → gaps → key insight |
| [claims.md](logic/claims.md) | 6 falsifiable claims (C01–C06) |
| [concepts.md](logic/concepts.md) | 9 technical concepts (three-channel model, LSTM gating, Conv1D fusion, late fusion, Leaky ReLU, MAPE/RMSE/MAE, …) |
| [experiments.md](logic/experiments.md) | 5 verification plans (E01–E05), directional only |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the paper's 29 references |
| [solution/architecture.md](logic/solution/architecture.md) | The three-channel LSTM-CNN component graph |
| [solution/method.md](logic/solution/method.md) | Forward method: sequence construction, LSTM equations, convolution fusion, FC output |
| [solution/constraints.md](logic/solution/constraints.md) | Assumptions, boundary conditions, limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Hardware/software/data/hyperparameters | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG (question → design → ablations → comparison → decisions/dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Index of 5 tables + 12 figures |
| tables/table1–table5 | Activation, optimizer, lookback ablations; model comparison on both datasets |
| figures/figure1–figure12 | Architecture/schematic diagrams (F1–F8) and prediction/residual plots (F9–F12) |
</content>
</invoke>
