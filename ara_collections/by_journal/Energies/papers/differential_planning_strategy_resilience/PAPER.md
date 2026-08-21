---
title: "A Differential Planning Strategy for Distribution Network Resilience Enhancement Considering Decision Dependence Uncertainty"
authors:
  - "Xuming Chen"
  - "Le Liu"
  - "Xiaoning Kang"
year: 2025
venue: "Energies"
doi: "10.3390/en18236353"
ara_version: 1.0
domain:
  - "Power Systems"
  - "Distribution Network Resilience"
  - "Decision-Dependent Uncertainty"
  - "Distributionally Robust Optimization"
  - "Global Sensitivity Analysis"
keywords:
  - "resilience of power distribution system"
  - "decision dependence uncertainty"
  - "extreme natural disasters"
  - "global sensitivity analysis"
  - "multi-level line hardening"
  - "distributionally robust optimization"
claims_summary: "This paper proposes a distributionally robust multi-level line hardening model incorporating decision-dependent uncertainty (DDU) for distribution network resilience enhancement. It establishes that: (1) DDU-based multi-level hardening achieves cost reduction up to CNY 8.553 million compared with traditional single-level hardening; (2) coordinated optimization of MEG, EVs, demand response, network reconfiguration, and line hardening reduces average loss-of-load cost by 16.89%; (3) the distributionally robust optimization (DRO) approach provides a financial insurance policy against worst-case disaster scenarios, sacrificing modest nominal cost for significant worst-case loss reduction; (4) Sobol' global sensitivity analysis quantifies marginal contributions of individual reinforcement measures, revealing that main feeder lines (1--2, 2--3) and critical tie lines (31--32, 32--33) have the highest first-order contributions and strong interaction effects."
abstract: "To reduce the impact of extreme natural disasters on urban distribution networks and improve the interpretability of planning decisions, this paper proposes a distributionally robust planning strategy for distribution networks that considers decision-dependent uncertainty. First, a decision-dependent uncertainty model is established to represent the relationship between power line failure probability and reinforcement decisions, with uncertainty described using norm-bounded fuzzy sets. Then, a three-level distributionally robust multi-grade reinforcement model is developed, which retains typical fault scenarios to reduce computational complexity and improve efficiency. Next, a global sensitivity analysis method based on the Sobol' approach is introduced to analyze the marginal effects of resilience investments and quantify the impact of specific reinforcement measures on total planning cost and overall power system resilience. Finally, simulations based on the IEEE 33-bus test system verify the effectiveness of the proposed planning strategy. The results show that the proposed method can effectively enhance grid resilience while improving the interpretability of planning strategies."
collection: "by_journal"
journal: "Energies"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p4_resilience_distribution_planning/p4_resilience_distribution_planning__03__a_differential_planning_strategy_for_distribution_netwo__ec280c8734.pdf"
---

# Overview

This paper, authored by Xuming Chen, Le Liu, and Xiaoning Kang from Xi'an Jiaotong University, addresses the challenge of enhancing distribution network resilience against extreme natural disasters (typhoons, floods, ice disasters) through a **differential planning strategy** that incorporates **decision-dependent uncertainty (DDU)**.

The core contribution is a three-level distributionally robust optimization (DRO) framework for multi-level line hardening. Unlike conventional models where line failure probability is assumed exogenous, the proposed DDU model captures the intrinsic relationship between hardening decisions and failure probability: the failure probability of a line depends on both the hardening level applied and the disaster intensity. The model integrates multiple resilience measures including mobile emergency generators (MEGs), electric vehicles (EVs) with V2G capability, demand response, and network reconfiguration.

A customized Column-and-Constraint Generation (C&CG) algorithm with fault-state pruning is developed to solve the computationally challenging tri-level optimization. Global sensitivity analysis via the Sobol' method quantifies the marginal contribution of each reinforcement measure, enhancing interpretability.

The framework is validated on the IEEE 33-bus and IEEE 123-bus test systems under typhoon wind-speed scenarios.

# Layer Index

| Layer | File | Description |
|-------|------|-------------|
| Problem | `logic/problem.md` | Observations, gaps, key insights, assumptions |
| Claims | `logic/claims.md` | Falsifiable claims with proof and evidence mapping |
| Concepts | `logic/concepts.md` | Technical terms with notation and definitions |
| Experiments | `logic/experiments.md` | Analysis blocks with setup, metrics, baselines |
| Constraints | `logic/solution/constraints.md` | Boundary conditions and limitations |
| Related Work | `logic/related_work.md` | Typed dependency graph of citations |
| Environment | `src/environment.md` | Computational environment and data sources |
| Exploration Tree | `trace/exploration_tree.yaml` | Research DAG of decisions and experiments |
| Evidence Index | `evidence/README.md` | Index of all figures and tables |
