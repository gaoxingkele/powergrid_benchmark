---
title: "Active Distribution Network Expansion Planning Based on Wasserstein Distance and Dual Relaxation"
authors: ["Jianchu Liu", "Xinghang Weng", "Mingyang Bao", "Shaohan Lu", "Changhao He"]
year: 2024
venue: "Energies"
doi: "10.3390/en17123005"
ara_version: "1.0"
domain: "Active distribution network expansion planning; distributionally robust optimization; Wasserstein distance; SOP; interconnection switches"
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p3_self_adaptive_mode_distribution_planning/p3_self_adaptive_mode_distribution_planning__02__active_distribution_network_expansion_planning__395ce02577.pdf"
keywords: ["active distribution network", "expansion planning", "Wasserstein distance", "distributionally robust optimization", "soft open point", "interconnection switch", "MISOCP", "dual relaxation", "McCormick relaxation"]
claims_summary:
  - "Collaborative planning of lines, SOPs, and interconnection switches achieves nearly 5% higher annual net profit than traditional planning without flexible interconnection devices."
  - "The Wasserstein-distance-based distributionally robust optimization method yields a net profit improvement of more than 3% over traditional robust optimization while remaining computationally tractable via MISOCP reformulation."
  - "The McCormick relaxation method converges to a feasible optimal solution (annual net profit 4.93×10^7 CNY) within 2.52 hours, whereas IPOPT fails to obtain an optimal solution within 5 hours."
  - "Replacing SOPs with interconnection switches reduces operation profit by more than 6%, demonstrating the economic value of power-electronic flexible interconnection devices in active distribution network operation."
  - "The distributionally robust optimization model is reformulated to a tractable MISOCP via SOCP relaxation, Lagrange duality, and McCormick relaxation without loss of solution quality."
abstract: "This paper proposes an expansion planning method for active distribution networks (ADNs) that considers the selection of multiple types of interconnection switches. To address the uncertainty of distributed generation (DG) and load, a Wasserstein distance probability distribution ambiguity set is established. Based on this, a distributionally robust optimization model for the collaborative planning of lines and multiple types of switches (SOPs and interconnection switches) is developed. The model is a mixed-integer non-linear programming (MINLP) problem. By applying second-order cone programming (SOCP) relaxation for the power flow constraints, Lagrange duality for the inner maximum function in the uncertainty model, and McCormick relaxation for bilinear terms, the model is transformed into a tractable mixed-integer second-order cone programming (MISOCP) problem solved by the CPLEX solver. The proposed method is tested on the Portugal 54-node system. Results show that collaborative planning of lines and multiple types of switches achieves nearly 5% higher annual net profit compared to traditional planning without interconnection switches, verifying the effectiveness of the proposed model and algorithm."
---

# Active Distribution Network Expansion Planning Based on Wasserstein Distance and Dual Relaxation

## Overview

This paper proposes a distributionally robust expansion planning method for active distribution networks that jointly optimizes the investment in lines, soft open points (SOPs), and interconnection switches under DG/load uncertainty. A Wasserstein-distance-based ambiguity set captures the probability distribution of renewable generation and load scenarios without assuming a specific parametric form. The resulting min-max-min optimization model is transformed through a sequence of convex relaxations (SOCP for power flow, Lagrange duality for the inner worst-case expectation, and McCormick relaxation for bilinear terms) into a single-level MISOCP that is solvable by CPLEX. Tested on the Portugal 54-node system over a 20-year planning horizon, the collaborative strategy yields a net profit of 4928.18 x 10^4 CNY/year, outperforming SOP-only (4927.00), switch-only (4689.15), and conventional deterministic (5089.49, too ideal) and robust (4770.01, too conservative) benchmarks.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations, gaps, key insight, assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable claims (C01–C05) |
| [concepts.md](logic/concepts.md) | 7 key technical terms |
| [experiments.md](logic/experiments.md) | 4 declarative evaluation plans (E01–E04) |
| [related_work.md](logic/related_work.md) | Typed citation dependency graph |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Test system, parameters, software | C01–C05 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG (question, decisions, experiments, dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 7 tables + 9 figures |
| tables/table1.md … table7.md | DG integration, ESS integration, planning results, costs, operation comparison, method comparison, relaxation comparison |
| figures/figure1.md … figure9.md | System topology, planning network structures, operation indexes, cost impact, error analysis |
