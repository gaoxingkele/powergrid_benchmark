---
title: "Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load Forecasting"
authors: ["Jiarui Li", "Jian Li", "Jiatong Li", "Guozheng Zhang"]
year: 2025
venue: "Electronics"
doi: "10.3390/electronics14163332"
ara_version: "1.0"
domain: "Power-load forecasting — hybrid deep learning (graph + recurrent) with boosting ensemble and Bayesian uncertainty"
keywords: ["power-load forecasting", "graph convolutional network", "BiLSTM", "AdaBoost ensemble", "Monte Carlo Dropout", "Bayesian uncertainty", "Spearman correlation graph", "spatiotemporal features"]
claims_summary:
  - "Stacking spatial (GCN) then temporal (BiLSTM) feature extraction and then boosting + uncertainty weighting reduces load-forecast error at each added stage."
  - "Attenuating ensemble weights of high-variance base learners preserves accuracy at abrupt load turning points."
  - "Building the GCN adjacency from a Spearman rank-correlation threshold yields lower error than similarity/learned/information-theoretic graph builders in this weather-load setting."
  - "Selectively re-weighting only above-threshold-error samples focuses boosting on hard/mutation samples without amplifying noise."
  - "Monte Carlo Dropout equips the point forecast with a 95% predictive interval usable as a dispatch risk-quantification signal."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__02__bayesian_optimized_gcn_bilstm_adaboost_model_for_power_loa__9b2dc47b52.pdf"
abstract: "Accurate and stable power-load forecasting is crucial for optimizing generation scheduling and ensuring the economic and secure operation of power grids. To address the issues of low prediction accuracy and poor robustness during abrupt load changes, this study proposes a Bayesian-optimized GCN-BiLSTM-Adaboost model (abbreviated as GCN-BiLSTM-AB). It combines Graph Convolutional Networks (GCN), Bidirectional Long Short-Term Memory Networks (BiLSTM), and a Bayesian-optimized AdaBoost framework. Firstly, the GCN is employed to capture the spatial correlation features of the input data. Then, the BiLSTM is employed to extract the long-term dependencies of the data time series. Finally, the AdaBoost framework is used to dynamically adjust the base learner weights, and a Bayesian method is employed to optimize the weight adjustment process and prevent overfitting. The experiment results on actual load data from a regional power grid show the GCN-BiLSTM-AB outperforms other compared models in prediction error metrics, with MAE, MAPE, and RMSE values of 1.86, 3.13%, and 2.26, respectively, which improve the prediction robustness during load change periods. Therefore, the proposed method shows that the synergistic effect of spatiotemporal feature extraction and dynamic weight adjustment improves prediction accuracy and robustness, which provides a new forecasting model with high precision and reliability for power system dispatch decisions."
---

# Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load Forecasting

## Overview

This paper proposes **GCN-BiLSTM-AB**, a hybrid short-term power-load forecasting model that stacks
four ideas: (1) a Graph Convolutional Network (GCN) over a graph whose nodes are meteorological
factors and whose edges come from a Spearman rank-correlation threshold (|ρ| ≥ 0.8), extracting
spatial dependencies; (2) a Bidirectional LSTM (BiLSTM) extracting forward/backward temporal
dependencies; (3) a modified AdaBoost that ensembles 10 GCN-BiLSTM weak learners, up-weighting
samples whose error exceeds a 0.3 threshold; and (4) a Monte Carlo Dropout "Bayesian" step that
estimates each weak learner's predictive variance and attenuates the weights of high-variance
learners, while also yielding a 95% predictive interval. Evaluated on one year of hourly regional
load-plus-weather data, the model is compared against single-model baselines (LSTM, GRU, CNN-LSTM,
GCN-LSTM, CNN-BiLSTM), against a stage-wise ablation (BiLSTM → GCN-BiLSTM → GCN-BiLSTM-Adaboost →
proposed), and against alternative graph-construction methods (KNN, learned graphs, mutual
information), on one-day and one-week horizons using MAE / MAPE / RMSE.

**Ownership note:** This ARA is a structured extraction of an externally published, third-party
paper (MDPI *Electronics*, CC BY 4.0). It is not an original project artifact. No source code was
released by the authors (data availability: restricted); all code-layer content is reconstructed
from printed equations/steps and marked as such.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable claims (C01–C05) |
| [concepts.md](logic/concepts.md) | 8 technical concepts |
| [experiments.md](logic/experiments.md) | 5 declarative verification plans (E01–E05) |
| [related_work.md](logic/related_work.md) | Typed citation dependency graph (RW01–RW14) |
| [solution/architecture.md](logic/solution/architecture.md) | The GCN-BiLSTM-AB ensemble pipeline (component graph) |
| [solution/algorithm.md](logic/solution/algorithm.md) | AdaBoost weight update + Bayesian (MC Dropout) uncertainty weighting |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Data / framework / hardware / hyperparameters / seeds | — |
| [execution/adaboost_bayesian_weighting.py](src/execution/adaboost_bayesian_weighting.py) | Reconstructed stub of the modified AdaBoost + MC-Dropout uncertainty weighting (Eqs 11–19) | C01, C02, C04, C05 |
| [configs/model.md](src/configs/model.md) | Layer/training hyperparameters (Table 3, §4.2) | C01 |

### Data Layer (`/data`)
| File | Description |
|------|-------------|
| [dataset.md](data/dataset.md) | Regional hourly load + 8 weather features, 2018 |
| [preprocessing.md](data/preprocessing.md) | Imputation, min-max normalization, 24-h sliding window, adjacency construction |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG (questions → decisions → experiments → dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 4 tables + 12 figures |
