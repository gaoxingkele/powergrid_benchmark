---
title: "A Distributed Energy Storage-Based Planning Method for Enhancing Distribution Network Resilience"
authors:
  - "Yitong Chen"
  - "Qinlin Shi"
  - "Bo Tang"
  - "Yu Zhang"
  - "Haojing Wang"
year: 2026
venue: "Energies"
doi: "10.3390/en19020574"
ara_version: 1.0
domain: "Power systems, distribution network resilience, energy storage planning"
keywords:
  - "distributed energy storage systems"
  - "distribution network operation optimization"
  - "priority indices"
  - "sequential configuration"
  - "multi-dimensional evaluation framework"
claims_summary: "A priority-index-based sequential planning method for distributed energy storage systems improves distribution network resilience under high renewable uncertainty, achieving better node-level stability, block-level source-load matching, and grid-wide coordination uniformity compared to global traversal or one-shot priority planning, with only a marginal increase in investment cost."
abstract: "With the widespread adoption of renewable energy, distribution grids face increasing challenges in efficiency, safety, and economic performance due to stochastic generation and fluctuating load demand. Traditional operational models often exhibit limited adaptability, weak coordination, and insufficient holistic optimization, particularly in early-/mid-stage distribution planning where feeder-level network information may be incomplete. Accordingly, this study adopts a planning-oriented formulation and proposes a distributed energy storage system (DESS) planning strategy to enhance distribution network resilience under high uncertainty. First, representative wind and photovoltaic (PV) scenarios are generated using an improved Gaussian Mixture Model (GMM) to characterize source-side uncertainty. Based on a grid-based network partition, a priority index model is developed to quantify regional storage demand using quality- and efficiency-oriented indicators, enabling the screening and ranking of candidate DESS locations. A mixed-integer linear multi-objective optimization model is then formulated to coordinate lifecycle economics, operational benefits, and technical constraints, and a sequential connection strategy is employed to align storage deployment with load-balancing requirements. Furthermore, a node–block–grid multi-dimensional evaluation framework is introduced to assess resilience enhancement from node-, block-, and grid-level perspectives. A case study on a Zhejiang Province distribution grid validates the proposed method. Results demonstrate that, with only a 4% increase in investment cost, the proposed strategy improves critical-node stability by 27%, enhances block-level matching by 88%, increases quality-demand satisfaction by 68%, and improves grid-wide coordination uniformity by 324%."
collection: by_journal
journal: "Energies"
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p4_resilience_distribution_planning/p4_resilience_distribution_planning__01__a_distributed_energy_storage_based_planning_method_for__b115741548.pdf"
---

# Overview

This paper proposes a **priority-index-based sequential planning method** for distributed energy storage systems (DESS) to enhance the operational resilience of active distribution networks under high renewable energy uncertainty. The approach integrates three components: (1) an improved Gaussian Mixture Model (GMM) for generating representative wind and PV scenarios; (2) a priority index model that uses quality- and efficiency-oriented demand indicators (I1–I7) with Critic-method weighting to rank candidate DESS locations at the node level within grid-based blocks; and (3) a multi-objective mixed-integer linear optimization (solved via Gurobi) that coordinates lifecycle cost, operational benefit, renewable curtailment rate, and peak-to-valley difference across sequential iterations. A node–block–grid multi-dimensional evaluation framework quantifies resilience outcomes at three spatial scales. A case study on a real Zhejiang Province distribution grid with six end-user block types validates the method against two baselines: global traversal (Case 1) and one-shot priority-index planning (Case 2).

## Layer Index

| Layer | File | Description |
|-------|------|-------------|
| Paper Metadata | `PAPER.md` | This file — title, authors, abstract, keywords, collection info |
| Logic — Problem | `logic/problem.md` | Observations, gaps, key insight, assumptions behind the work |
| Logic — Claims | `logic/claims.md` | Falsifiable claims (C01–C05) with proof references and falsification criteria |
| Logic — Concepts | `logic/concepts.md` | Technical terms: DESS, priority index, GMM, sequential planning, node–block–grid evaluation, matching degree, generalized load, Critic method |
| Logic — Experiments | `logic/experiments.md` | Experiment blocks E01–E04: GMM scenario generation, priority index construction, sequential planning comparison, multi-dimensional evaluation |
| Logic — Constraints | `logic/solution/constraints.md` | Boundary conditions, assumptions, limitations |
| Logic — Related Work | `logic/related_work.md` | Typed dependency graph for key citations |
| Source Environment | `src/environment.md` | Language, solver, hardware, data sources |
| Exploration Trace | `trace/exploration_tree.yaml` | Research DAG with root, decision, experiment, and dead-end nodes |
| Evidence Index | `evidence/README.md` | Index of all tables and figures |
| Evidence — Tables | `evidence/tables/` | Table 1–6 screenshots and markdown |
| Evidence — Figures | `evidence/figures/` | Figure 1–16 screenshots and markdown |
