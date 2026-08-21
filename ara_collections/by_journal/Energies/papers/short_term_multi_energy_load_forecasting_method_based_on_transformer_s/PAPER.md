---
title: "Short-Term Multi-Energy Load Forecasting Method Based on Transformer Spatio-Temporal Graph Neural Network"
authors: ["Heng Zhou", "Qing Ai", "Ruiting Li"]
year: 2025
venue: "Energies"
doi: "10.3390/en18174466"
ara_version: "1.0"
domain: "Deep learning for multi-energy load forecasting in integrated energy systems (spatio-temporal graph neural networks + Transformers)"
keywords: ["multi-energy load forecasting", "transformer", "graph neural network", "integrated energy systems", "deep learning", "spatio-temporal attention", "mutual information", "dynamic adaptive graph convolution", "encoder-decoder", "short-term load forecasting"]
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__05__short_term_multi_energy_load_forecasting_method_based_on_t__03d8f76649.pdf"
claims_summary:
  - "Augmenting dot-product attention with a mutual-information term over both time and feature axes captures nonlinear/asymmetric load dependencies that linear attention alone misses."
  - "A dynamically reconstructed adjacency matrix (physical topology fused with MI feature similarity) models shifting spatial dependence better than static graph structures."
  - "Jointly forecasting coupled electric/cooling/heating loads exploits inter-load correlation and reduces error versus independent per-load forecasting."
  - "Calendar auxiliary features carry more predictive value than meteorological features for multi-energy load, and fusing both is best."
  - "The MI-enhanced attention and the dynamic graph module are synergistic — the pair beats either module alone."
  - "End-to-end spatio-temporal joint optimization in an encoder-decoder outperforms Transformer/MLP/statistical baselines across horizons and load types."
  - "The dynamic MI adaptivity trades quadratic compute overhead for accuracy, sitting at a balanced training/inference cost while dominating accuracy."
abstract: "To tackle the limitations in simultaneously modeling long-term dependencies in the time dimension and nonlinear interactions in the feature dimension, as well as their inability to fully reflect the impact of real-time load changes on spatial dependencies, a short-term multi-energy load forecasting method based on Transformer Spatio-Temporal Graph neural network (TSTG) is proposed. This method employs a multi-head spatio-temporal attention module to model long-term dependencies in the time dimension and nonlinear interactions in the feature dimension in parallel across multiple subspaces. Additionally, a dynamic adaptive graph convolution module is designed to construct adaptive adjacency matrices by combining physical topology and feature similarity, dynamically adjusting node connection weights based on real-time load characteristics to more accurately characterize the spatial dynamics of multi-energy interactions. Furthermore, TSTG adopts an end-to-end spatio-temporal joint optimization framework, achieving synchronous extraction and fusion of spatio-temporal features through an encoder-decoder architecture. Experimental results show that TSTG significantly outperforms existing methods in short-term load forecasting tasks, providing an effective solution for refined forecasting in integrated energy systems."
---

# Short-Term Multi-Energy Load Forecasting Method Based on Transformer Spatio-Temporal Graph Neural Network (TSTG)

## Overview

The paper proposes **TSTG**, an encoder-decoder deep-learning model for short-term multi-energy
(electric / cooling / heating) load forecasting in Integrated Energy Systems (IES). Each encoder/decoder
layer combines two novel modules: (1) a **multi-head spatio-temporal attention** module that runs dual
parallel attention along the temporal and feature axes and augments the scaled dot-product with a
**mutual-information (MI)** term to capture nonlinear/asymmetric dependencies; and (2) a **dynamic
adaptive graph convolution** module that builds the spatial adjacency matrix by fusing a static physical
topology with an MI-based, feature-driven similarity graph recomputed from real-time load features. The
two modules are co-trained end-to-end. On the Arizona State University Campus Metabolism dataset, TSTG
is evaluated against 11 baselines (Transformer/Informer/Autoformer/FEDformer/Reformer/Pyraformer,
MLP-based LightTS/TiDE/TSMixer, and statistical ARIMA/Prophet) across 6/12/24/96 h horizons, with
coupling, auxiliary-information, and module-ablation studies.

**Ownership**: external published paper (Energies 2025), not a project-original work. Compiled for
knowledge extraction only.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 7 falsifiable claims (C01–C07) |
| [concepts.md](logic/concepts.md) | 9 technical concepts |
| [experiments.md](logic/experiments.md) | 5 verification plans (E01–E05) |
| [related_work.md](logic/related_work.md) | Typed dependency graph (baselines + background) |
| [solution/architecture.md](logic/solution/architecture.md) | TSTG component graph (Figures 1–3) |
| [solution/method.md](logic/solution/method.md) | Formulations of the two modules + joint optimization (Eqs. 1–11) |
| [solution/constraints.md](logic/solution/constraints.md) | Assumptions, limitations, complexity |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Dataset, hyperparameters, split, metrics | — |
| [execution/tstg_inference.py](src/execution/tstg_inference.py) | Reconstructed pseudocode of Algorithm 1 (inference pipeline) | C01, C02, C05, C06 |
| [configs/model.md](src/configs/model.md) | Model hyperparameters (N, D, T_hist, d_model, depth, d_n) | C06 |

### Data Layer (`/data`)
| File | Description |
|------|-------------|
| [dataset.md](data/dataset.md) | ASU Campus Metabolism multi-energy dataset |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG (questions, decisions, ablations, dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Index of 5 tables + 4 figures |
