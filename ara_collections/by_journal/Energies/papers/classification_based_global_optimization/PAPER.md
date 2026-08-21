---
title: "A Classification-Based Global Optimization Approach for Integrated Planning of Distributed Generation, Capacitor Banks, and Electric Vehicle Charging Stations in Radial Distribution Networks"
authors:
  - "Abdullah Alrashidi"
  - "Ashraf Ahmad Fahmy"
  - "Omar Saif"
  - "Mohamed Kassem"
  - "Adel Elsamahy"
  - "Abdelazim Salem"
year: 2026
venue: "Energies"
doi: "10.3390/en19143262"
ara_version: "1.0"
domain: "Power distribution network planning, optimization, electric vehicle integration"
keywords:
  - "classification-based optimization"
  - "distributed generation"
  - "capacitor banks"
  - "EV charging stations"
  - "power loss minimization"
  - "voltage deviation index"
  - "Sustainable Development Goals"
  - "radial distribution networks"
  - "hosting factor"
  - "deterministic optimization"
claims_summary:
  - "Classification-based bus selection narrows the search space and improves solution quality compared to stochastic metaheuristics."
  - "Coordinated integration of DGs, CBs, and EVCSs yields synergistic loss reduction exceeding 94% even under high EV penetration."
  - "The CGO framework is deterministic, reproducible, and achieves lower computational cost than PSO and GWO while delivering better or equivalent loss reduction."
  - "Reactive power compensation via CBs is essential to maintain substation power factor when DGs operate at unity power factor under EV penetration."
abstract: "In order to improve the electrical grid flexibility and efficiency, distributed energy resources (DERs), capacitor banks (CBs), and electric vehicle charging stations (EVCSs) are being integrated into active power distribution networks. However, radial distribution networks have large electrical losses from unidirectional power flow and growing EV penetration, as well as voltage drops and power flow exceeding the thermal capacity limit of some distribution branches. This study is based on the Classification Global Optimization (CGO) approach to include EVCS's under different hosting factors (30%, 40%, and 50%). The applied CGO framework uses a deterministic global function that includes minimization of electrical losses, reducing the voltage deviation index, increasing the cost of saved energy due to losses and decreasing the annual amount of CO2 emission, this done for the simultaneous placement and sizing of EVCSs, DGs, and CBs after classifying the network buses according to voltage sensitivity and power consumption. Active power loss reductions of up to 94.75% and 98.061% with combined integration are demonstrated by validation on IEEE 33-bus and 69-bus systems, while computational efficiency (simulation times < 5 s) is maintained. This enhanced technique offers a scalable solution for contemporary active distribution networks and directly helps Sustainable Development Goals (SDGs) 7, 9, 11, and 13 by improving grid performance with high EV adoption."
collection: "by_journal"
journal: "Energies"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/pdfs/p3_self_adaptive_mode_distribution_planning/p3_self_adaptive_mode_distribution_planning__06__a_classification_based_global_optimization_appr__5b5b865830.pdf"
---

# A Classification-Based Global Optimization Approach for Integrated Planning of DG, Capacitor Banks, and EV Charging Stations in Radial Distribution Networks

## Overview

This paper presents a Classification-based Global Optimization (CGO) framework for the simultaneous placement and sizing of distributed generation (DG) units, capacitor banks (CBs), and electric vehicle charging stations (EVCSs) in radial distribution networks. The method classifies network buses by voltage sensitivity and power demand to narrow the search space, then applies a deterministic multi-objective function minimizing power losses, voltage deviation index, and CO2 emissions while maximizing cost savings. Validated on IEEE 33-bus and 69-bus systems under EV hosting factors of 30%, 40%, and 50%, the approach achieves 94.75% and 98.061% active power loss reductions respectively, with computation times under 29 seconds — outperforming PSO and GWO baselines.

## Layer Index

### Cognitive Layer (`logic/`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations on distribution network challenges, gaps in existing methods, key insight of bus classification, and assumptions |
| [claims.md](logic/claims.md) | 4 falsifiable claims (C01–C04) covering classification-driven search efficiency, coordinated integration synergy, deterministic performance, and reactive compensation necessity |
| [concepts.md](logic/concepts.md) | 8 technical terms: CGO, Hosting Factor, Voltage Deviation Index, Classification-Based Bus Selection, Thermal Capacity Limit, Global Multi-Objective Function, Payback Period, CO2 Emission Reduction Factor |
| [experiments.md](logic/experiments.md) | 5 experiments (E01–E05) covering 33-bus DG+EVCS, 33-bus combined, 69-bus combined, comparative metaheuristic benchmark, and thermal capacity validation |
| [solution/algorithm.md](logic/solution/algorithm.md) | CGO unified optimization algorithm with pseudocode and mathematical formulation |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, and known limitations |
| [related_work.md](logic/related_work.md) | Full citation footprint with typed dependency graph |

### Physical Layer (`src/`)
| File | Description |
|------|-------------|
| [environment.md](src/environment.md) | Software, hardware, data sources, and protocols |

### Exploration Graph (`trace/`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 9-node research DAG covering the central research questions, experiments, decisions, and dead ends |

### Evidence (`evidence/`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 11 tables and 12 figures |
| [tables/](evidence/tables/) | 11 tables (Table 1–11) with markdown transcriptions and PNG screenshots |
| [figures/](evidence/figures/) | 12 figures (Figure 1–12) with markdown descriptions and PNG screenshots |
