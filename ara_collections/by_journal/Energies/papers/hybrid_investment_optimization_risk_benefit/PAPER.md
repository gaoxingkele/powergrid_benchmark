---
title: "A Novel Hybrid Power-Grid Investment Optimization Model with Collaborative Consideration of Risk and Benefit"
authors:
  - "Changzheng Gao"
  - "Xiuna Wang"
  - "Dongwei Li"
  - "Chao Han"
  - "Weiyang You"
  - "Yihang Zhao"
year: 2023
venue: "Energies"
doi: "10.3390/en16207215"
ara_version: 1.0
domain: "Power systems, investment optimization, multi-criteria decision-making"
keywords:
  - "power-grid investment"
  - "investment risk"
  - "investment benefit"
  - "multi-criteria decision-making"
  - "optimization"
claims_summary: "A two-stage hybrid PGI optimization model using Bayesian BWM-TOPSIS for risk/benefit evaluation and ILA for constrained optimization yields superior investment portfolios compared to single-objective or traditional approaches."
abstract: "Power-grid investment (PGI) optimization is crucial for boosting investment performance, lowering investment risks, and assuring the sustainable development of power-grid businesses. However, existing studies, which primarily concentrate on financial aspects, have not adequately considered the risk and benefit factors in the process of PGI. In this context, this research suggests a novel hybrid PGI optimization model that collaboratively accounts for the risks and benefits. In the first step, risk and benefit indicator systems for PGI are built, and a comprehensive evaluation model based on the Bayesian best-worst method and TOPSIS is suggested. In the second stage, a PGI optimization model considering the investment amount, power demand, and low-carbon restrictions is further developed based on the evaluation results. Furthermore, the incomprehensible but intelligible-in-time logic algorithm is adopted to solve the problem. By conducting an empirical analysis of ten projects within a power-grid company, the optimal investment plan and a differentiated investment portfolio strategy are obtained by adjusting the key elements."
collection: by_journal
journal: "Energies"
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p5_hybrid_moea_feasibility_review/p5_hybrid_moea_feasibility_review__03__a_novel_hybrid_power_grid_investment_optimization_model_w__1b76a815c6.pdf"
---

# Overview

This paper, published in Energies (MDPI) in 2023, proposes a two-stage hybrid model for power-grid investment (PGI) optimization that jointly considers risk and benefit dimensions. The first stage uses a Bayesian Best-Worst Method (Bayesian BWM) combined with TOPSIS to compute comprehensive risk and benefit scores for candidate projects. The second stage formulates a constrained optimization with the objective of maximizing "benefit per unit risk," subject to investment amount, power demand, and low-carbon (CO2 emission reduction) constraints, solved using the Incomprehensible but Intelligible-in-time Logic Algorithm (ILA). An empirical study on ten projects from a Chinese power-grid company demonstrates the model's effectiveness and provides sensitivity analysis across three constraint dimensions.

## Layer Index

| Layer | File | Description |
|-------|------|-------------|
| Problem | `logic/problem.md` | Observations, gaps, key insight, assumptions |
| Claims | `logic/claims.md` | Falsifiable claims with proof references |
| Concepts | `logic/concepts.md` | Technical terms with definitions and boundaries |
| Experiments | `logic/experiments.md` | Analysis blocks with procedures and metrics |
| Constraints | `logic/solution/constraints.md` | Boundary conditions and assumptions |
| Related Work | `logic/related_work.md` | Typed dependency graph for citations |
| Environment | `src/environment.md` | Runtime, framework, data, dependencies |
| Trace | `trace/exploration_tree.yaml` | Research DAG |
| Evidence | `evidence/README.md` | Index of tables and figures |
