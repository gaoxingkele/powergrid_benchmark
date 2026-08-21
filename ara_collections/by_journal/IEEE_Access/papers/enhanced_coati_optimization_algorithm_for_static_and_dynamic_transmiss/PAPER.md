---
title: "Enhanced Coati Optimization Algorithm for Static and Dynamic Transmission Network Expansion Planning Problems"
authors: ["Muhammet Demirbas", "M. Kenan Dosoglu", "Serhat Duman"]
year: 2025
venue: "IEEE Access"
doi: "10.1109/ACCESS.2025.3544523"
ara_version: "1.0"
domain: "Metaheuristic optimization for power system planning (Transmission Network Expansion Planning)"
keywords: ["Coati optimization algorithm", "fitness-distance balance", "opposition-based learning", "transmission network expansion planning", "static TNEP", "dynamic multistage TNEP", "DC power flow", "metaheuristics", "CEC2020", "CEC2022"]
collection: "by_journal"
journal: "IEEE Access"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p3_self_adaptive_mode_distribution_planning/p3_self_adaptive_mode_distribution_planning__11__enhanced_coati_optimization_algorithm_for_stati__5a94f4597c.pdf"
claims_summary:
  - "Injecting Fitness-Distance Balance selection pressure into a metaheuristic's position-update steps counteracts premature convergence and improves solution quality/robustness on high-dimensional multimodal problems."
  - "Where the FDB selection is applied inside the search operators determines the exploration/exploitation trade-off: guiding only the exploration-phase update yields the best balance of accuracy and scalability, while guiding the exploitation-phase update degrades scalability."
  - "Seeding the initial population with opposition candidates increases starting diversity and accelerates convergence, and elite-guided opposition (Elite OBL) is the most effective seeding scheme because it derives opposites from the best incumbents."
  - "The two enhancements compose: an FDB+OBL-enhanced Coati algorithm reaches literature-optimal investment costs on small/medium TNEP systems and competitive costs on a large-scale dynamic multistage system."
  - "Benchmark-fitness gains translate into reliable feasible-solution generation on constrained real-world planning problems, measured by success rate, more than the base and other classic metaheuristics."
  - "No metaheuristic dominates universally (No Free Lunch): the enhanced variants still lose on a minority of problems, especially at lower dimensions and larger population sizes."
abstract: "The power systems are becoming more and more complex due to the inclusion of new components and increasing load demand. Consequently, it is imperative to incorporate additional generation units and transmission links into the system. Transmission Network Expansion Planning (TNEP) seeks to include generation units and transmission lines into the system at optimal locations and minimal costs. Mathematical techniques are extensively employed to address the problem. Nonetheless, mathematical methods necessitate extensive computation durations. Consequently, novel solution strategies are under investigation. The TNEP problem is characterized by an innovative and effective metaheuristic optimization techniques. This study presents a novel Opposition Based Learning and Fitness Distance Balance based Coati Optimization Algorithm (FDBCOA-OBL) designed to address Static and Dynamic TNEP problems. An extensive experimental investigation was undertaken to evaluate the efficacy of the suggested method in addressing the benchmark test suites and the TNEP problem. The FDBCOA-OBL algorithm, utilizing the Elite OBL approach, surpassed all other comparative versions in addressing the benchmark test problems. The Wilcoxon analysis indicates that it lost 6 problems, tied in 110, and won 166 problems. The proposed approach resolved the TNEP problem in 6, 25, and 93-bus test systems. The Static TNEP solution was applied to the 6 and 25 bus test systems, while the Dynamic Multistage TNEP method was utilized in the 93-bus test system. The acquired investment expenses were compared to the research already documented in the literature. The findings indicate that the suggested method demonstrates robust performance."
---

# Enhanced Coati Optimization Algorithm for Static and Dynamic Transmission Network Expansion Planning Problems

## Overview

This paper enhances the Coati Optimization Algorithm (COA) with two independent design operators — the Fitness-Distance Balance (FDB) selection method and Opposition-Based Learning (OBL) initial-population seeding — and applies the resulting FDBCOA-OBL algorithm to the Transmission Network Expansion Planning (TNEP) problem. The method is developed in two stages. First, FDB is injected at different position-update points of COA to create three variants (FDBCOA1–FDBCOA3); FDBCOA1 (FDB in the exploration-phase Eq. 17 update) is identified as the best via CEC2020/CEC2022 benchmarking with Friedman and Wilcoxon tests plus scalability analysis. Second, eight OBL schemes seed the initial population of FDBCOA1 (FDBCOA1-OBL1…OBL8); Elite OBL (FDBCOA1-OBL5) is identified as the best. The final FDBCOA1-OBL5 is used to solve Static TNEP on Garver's 6-bus and IEEE 25-bus systems and Dynamic multistage TNEP on the Colombian 93-bus system, using a DC power flow model (MATPOWER 6.0) with a penalized fitness function. Investment costs are compared against literature methods, and a stability analysis (SR%, MIT, MST) benchmarks feasibility reliability against COA, FDBCOA1, GA, and PSO.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 8 falsifiable claims (C01–C08) |
| [concepts.md](logic/concepts.md) | 12 key technical terms |
| [experiments.md](logic/experiments.md) | 9 declarative verification plans (E01–E09) |
| [related_work.md](logic/related_work.md) | Typed citation dependency graph |
| [solution/algorithm.md](logic/solution/algorithm.md) | COA, FDB integration, OBL seeding, FDBCOA-OBL pseudocode |
| [solution/formulation.md](logic/solution/formulation.md) | STNEP and DTNEP mathematical model (fitness/objective/penalty) |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |
| [solution/heuristics.md](logic/solution/heuristics.md) | FDB-placement, Elite OBL, penalty-coefficient tuning |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Hardware/software/benchmark/protocol reproducibility | — |
| [execution/fdbcoa_obl.py](src/execution/fdbcoa_obl.py) | Reconstructed pseudocode of FDBCOA-OBL (from Algorithm 1 + Fig. 7 + Eqs.) | C01, C02, C03 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG with FDB/OBL selection branches, ablations and dead ends |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 21 tables + 15 figures |
