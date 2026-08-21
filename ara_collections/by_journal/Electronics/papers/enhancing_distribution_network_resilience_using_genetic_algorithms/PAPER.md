---
title: "Enhancing Distribution Network Resilience Using Genetic Algorithms"
authors: ["Theodoros I. Maris", "Christos Christodoulou", "Valeri Mladenov"]
year: 2025
venue: "Electronics"
doi: "10.3390/electronics14214324"
ara_version: "1.0"
domain: "Power systems — distribution network optimization, resilience, evolutionary computation"
keywords: ["distribution networks", "resilience", "genetic algorithms", "distributed energy resources", "voltage regulation", "power loss minimization", "multi-objective optimization", "network reconfiguration", "contingency analysis", "radial feeder"]
claims_summary:
  - "Folding a resilience penalty into a weighted multi-objective GA lets one optimizer improve steady-state and contingency performance together."
  - "GA-coordinated DER dispatch corrects downstream radial voltage sag, with benefit growing along the feeder."
  - "GA loss reduction accrues mostly in early generations, converging smoothly without oscillation."
  - "An explicit contingency-penalty term (f3) buys DER-outage resilience beyond steady-state optimization alone."
  - "In a radial feeder, DER reactive absorption is the voltage-support lever and central real injection is the loss/flow-balance lever."
abstract: "Ensuring the resilience and efficiency of modern distribution networks is increasingly critical in the presence of distributed energy resources (DERs). This study presents a multi-objective optimization framework based on a Genetic Algorithm (GA) to improve voltage profiles, minimize active power losses, and enhance resilience in a radial distribution network. A simplified 6-bus radial test system with DERs at buses 2, 3, and 4 is considered as a proof-of-concept case study. The GA optimizes control variables, including DER setpoints and network reconfiguration, under operational and thermal constraints. The optimization employs a weighted objective function combining voltage profile improvement, loss minimization, and a resilience penalty term that accounts for bus voltage collapse and branch overloads during DER contingencies. Simulation results demonstrate that the GA significantly improves network performance: the minimum bus voltage rises from 0.92 pu to 0.97 pu, while the total real power losses decrease by 46% (from 55.3 kW to 29.7 kW). Moreover, in the event of a DER outage, the optimized configuration preserves 100% load delivery, compared to 89% in the base case. These findings confirm that GA is an effective and practical tool for enhancing distribution network operation and resilience under high DER penetration. Future work will extend the approach to larger IEEE benchmark systems and time-series scenarios."
collection: "by_journal"
journal: "Electronics"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p4_resilience_distribution_planning/p4_resilience_distribution_planning__08__enhancing_distribution_network_resilience_using_genetic__8659a94551.pdf"
---

# Enhancing Distribution Network Resilience Using Genetic Algorithms

## Overview

This paper proposes a Genetic-Algorithm-based multi-objective optimization framework for radial
distribution networks with high DER penetration that treats **resilience as an explicit objective**
alongside voltage regulation and loss minimization. Its central contribution is a single scalarized
fitness F = w1·f1 + w2·f2 + w3·f3 whose third term (f3) penalizes configurations leading to voltage
collapse or branch overload during DER faults — linking conventional power-flow optimization directly
to contingency (resilience) assessment. On a proof-of-concept 6-bus radial feeder with DERs at buses
2–4, the GA improves the steady-state voltage profile (min bus voltage 0.92→0.97 pu), cuts real power
losses (~46%, 55.3→29.7 kW), and under a fault-induced DER trip preserves full load delivery (100% vs
89% base) with no overloaded branches. The work is demonstrative (one small feeder, deterministic
DERs); the authors defer larger IEEE feeders and time-series/stochastic scenarios to future work.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight (resilience penalty term) → assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable mechanism claims (C01–C05) |
| [concepts.md](logic/concepts.md) | 7 technical terms (resilience, trapezoidal curve, N-k, DER, weighted objective, GA, reconfiguration) |
| [experiments.md](logic/experiments.md) | 4 verification plans (E01–E04), directional |
| [related_work.md](logic/related_work.md) | 6 RW blocks + full citation footprint (refs 1–42) |
| [solution/formulation.md](logic/solution/formulation.md) | Objective F, terms f1/f2/f3, constraints |
| [solution/algorithm.md](logic/solution/algorithm.md) | GA: encoding, operators, fitness, control flow |
| [solution/architecture.md](logic/solution/architecture.md) | 6-bus radial network topology + control interface |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |
| [solution/heuristics.md](logic/solution/heuristics.md) | 3 design heuristics (weighting, soft constraints, elitist survival) |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | MATLAB R2025 + PowerFactory 2024; no released code; reproducibility gaps | — |
| [configs/ga_optimization.md](src/configs/ga_optimization.md) | GA hyperparameters + objective weights (verbatim from §5) | C01, C03 |

No `src/execution/` code: the paper prints no source code or formal pseudocode (only a generic GA
flowchart, Figure 2); the method lives in `logic/solution/`.

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 11-node research DAG (question → decisions → experiments → deferred scope) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Index of 6 tables + 5 figures (all filed with .md + .png) |
| tables/table1–6.md | Line data, load data, voltage profile, power losses, DER dispatch, resilience assessment |
| figures/figure1–5.md | Trapezoidal curve, GA flowchart, network diagram, voltage plot, convergence plot |
