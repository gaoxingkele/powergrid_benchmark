---
title: "Research on BiLSTM-Transformer Power Load Forecasting Method Based on Dynamic Adaptive Fusion"
authors:
  - "Jialong Xu"
  - "Lei Zhang"
  - "Zhenxiong Zhang"
year: 2026
venue: "Energies"
doi: "10.3390/en19061473"
collection: "by_journal"
journal: "Energies"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__03__research_on_bilstm_transformer_power_load_forecasting_meth__4763935b50.pdf"
ara_version: "1.0"
domain: "Power load forecasting; BiLSTM-Transformer hybrid; dynamic adaptive fusion for smart grids"
keywords:
  - "power load forecasting"
  - "BiLSTM"
  - "Transformer"
  - "dynamic adaptive fusion"
  - "hybrid model"
  - "smart grids"
  - "attention mechanism"
claims_summary:
  - "DAF module's dual-path adaptive weighting outperforms static fusion approaches for multi-source heterogeneous load data"
  - "BiLSTM-Transformer cascade captures both local bidirectional dependencies (BiLSTM) and global contextual patterns (Transformer)"
  - "DAF interaction term enables cross-dimensional coupling learning between feature channels and temporal contributions"
  - "Model achieves superior peak prediction accuracy and stability at load transition boundaries (weekend effect, PV fluctuations)"
  - "DAF module introduces minimal computational overhead (0.12M params, 1.8ms inference increase) for 0.46% MAPE reduction"
  - "Feature fusion mechanism (DAF) proves more critical than stacking additional temporal layers for overall accuracy improvement"
---

# Layer Index

## Layer 1: Core Logic (logic/)
- **`logic/problem.md`** — Problem formulation: observations (O1-O4), gaps (G1-G2), key insight, assumptions (A1-A3)
- **`logic/claims.md`** — Six central claims (C01-C06) with evidence mapping and confidence scoring
- **`logic/concepts.md`** — Ten key concepts with definitions, mathematical formulations, and paper references
- **`logic/experiments.md`** — Five experiment groups (E01-E05) mapping to tables and figures
- **`logic/related_work.md`** — Literature review covering CNN, LSTM, Transformer, CNN-LSTM hybrids, and attention-based fusion methods

## Layer 2: Proposed Solution (logic/solution/)
- **`logic/solution/architecture.md`** — DAF-BT system architecture: Input -> N-space transformer -> BiLSTM -> Transformer (local enhanced attention) -> DAF module -> Output
- **`logic/solution/method.md`** — Key mathematical formulations: equations (1)-(9) covering CNN convolution, LSTM gates, Transformer attention, BiLSTM, local enhanced attention, DAF channel/temporal weights, and synergistic fusion
- **`logic/solution/constraints.md`** — Assumptions, limitations, and boundary conditions of the proposed approach

## Layer 3: Evidence (evidence/)
- **`evidence/README.md`** — Index of all tables (4) and figures (12)
- **`evidence/tables/table1.md`** through **`evidence/tables/table4.md`** — Transcribed data from each table
- **`evidence/figures/figure1.md`** through **`evidence/figures/figure12.md`** — Structured descriptions of each figure

## Layer 4: Execution Environment (src/)
- **`src/environment.md`** — Hardware/software specifications, hyperparameters, dataset details, and preprocessing pipeline

## Layer 5: Research Trace (trace/)
- **`trace/exploration_tree.yaml`** — Research decision DAG: central question -> architectural decisions -> experiments -> findings

---

## Overview

This paper presents DAF-BT, a hybrid deep learning model for short-term power load forecasting that integrates a Bidirectional LSTM (BiLSTM) with a Transformer architecture through a novel Dynamic Adaptive Fusion (DAF) module. The key innovation lies in the DAF module's dual-path adaptive weighting mechanism, which comprises a Feature Channel Adaptive Unit and a Temporal Contribution Evaluation Unit, combined with a nonlinear interaction term for cross-dimensional coupling. Evaluated on a commercial complex power load dataset (17,516 samples at 0.5-hour intervals over the full year 2016), the proposed model achieves an MAE of 4.560, RMSE of 5.925, MAPE of 1.58%, and R-squared of 0.983, outperforming eight baseline models including CNN, LSTM, GRU, TCN, CNN-LSTM, Transformer, TCN-GRU, and TCN-LSTM-Attention. Ablation studies confirm that the DAF module contributes more significantly to accuracy gains than stacking additional temporal layers, and computational complexity analysis shows the method maintains practical efficiency (1.28M parameters, 12.4ms inference time) suitable for real-world smart grid deployment.
