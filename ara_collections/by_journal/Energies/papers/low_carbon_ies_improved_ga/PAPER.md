---
title: "Multi-Objective Optimization for the Low-Carbon Operation of Integrated Energy Systems Based on an Improved Genetic Algorithm"
authors:
  - "Yao Duan"
  - "Chong Gao"
  - "Zhiheng Xu"
  - "Songyan Ren"
  - "Donghong Wu"
year: 2025
venue: "Energies"
doi: "10.3390/en18092283"
ara_version: "1.0"
collection: "by_journal"
journal: "Energies"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/pdfs/p5_hybrid_moea_feasibility_review/p5_hybrid_moea_feasibility_review__09__multi_objective_optimization_for_the_low_carbon_operation__d95461af17.pdf"
domain: "power systems, integrated energy systems, multi-objective optimization, evolutionary computation"
keywords:
  - "improved genetic algorithm"
  - "integrated energy system"
  - "low-carbon optimization"
  - "multi-objective optimization"
  - "cyclic crossover"
  - "polynomial mutation"
  - "constraint handling"
  - "Pareto optimization"
  - "tiered pricing"
  - "carbon emission reduction"
claims_summary:
  - "C01: Cyclic crossover preserves advantageous parental genetic structure while enhancing population diversity, improving convergence toward Pareto-optimal solutions."
  - "C02: Adaptive polynomial mutation with dynamic distribution index balances exploration and exploitation throughout the evolutionary search."
  - "C03: Constraint-prioritizing parent selection with infeasible-solution elimination reduces equality constraint violations below 0.3 kW (<0.2% of IES power demand)."
  - "C04: IGA achieves up to 5% improvement in both operating cost and carbon emission objectives compared to unimproved single-objective GA baselines."
  - "C05: GA-based approaches with the proposed parent selection outperform penalty-function-based methods (MPSO, MABC) in constraint satisfaction across all IES operational scenarios."
abstract: "As global climate change and energy crises intensify, the pursuit of low-carbon integrated energy systems (IESs) has become increasingly important. This paper proposes an improved genetic algorithm (IGA) designed to optimize the multi-objective low-carbon operations of IESs, aiming to minimize both operating costs and carbon emissions. The IGA incorporates circular crossover and polynomial mutation techniques, which not only preserve advantageous traits from the parent population but also enhance genetic diversity, enabling comprehensive exploration of potential solutions. Additionally, the algorithm selects parent populations based on individual fitness and dominance, retaining successful chromosomes and eliminating those that violate constraints. This process ensures that subsequent generations inherit superior genetic traits while minimizing constraint violations, thereby enhancing the feasibility of the solutions. To evaluate the effectiveness of the proposed algorithm, we tested it on three different IES scenarios. The results demonstrate that the IGA successfully reduces equality constraint violations to below 0.3 kW, representing less than 0.2% deviation from the IES's power demand in each time slot. We compared its performance against a multi-objective genetic algorithm, a multi-objective particle swarm algorithm, and a single-objective genetic algorithm. Compared to conventional genetic algorithms, the IGA achieved maximum 5% improvement in both operational cost reduction and carbon emission minimization objectives compared to the unimproved single-objective genetic algorithm, demonstrating its superior performance in multi-objective optimization for low-carbon IESs. These outcomes underscore the algorithm's reliability and practical applicability."
---

# Multi-Objective Optimization for the Low-Carbon Operation of Integrated Energy Systems Based on an Improved Genetic Algorithm

## Overview

This paper proposes an Improved Genetic Algorithm (IGA) for the multi-objective low-carbon day-ahead scheduling optimization of Integrated Energy Systems (IESs). The IES model integrates electricity, natural gas, and heat networks with photovoltaic and wind power generation, combined heat and power (CHP) units, gas boilers (GB), waste heat recovery units (WHU), and battery energy storage systems (ESS). The IGA introduces three key enhancements to the standard genetic algorithm framework: (1) a cyclic crossover operation that preserves advantageous parental genetic structure, (2) an adaptive polynomial mutation operation with dynamic distribution index adjustment, and (3) a constraint-prioritizing parent selection and offspring retention mechanism that systematically eliminates infeasible solutions. The algorithm is evaluated across three IES operational scenarios against four benchmark algorithms (MGA, MPSO, SGA, MABC), demonstrating that IGA maintains equality constraint violations below 0.3 kW (<0.2% deviation) while achieving up to 5% improvement in both operating cost and carbon emission minimization objectives.

## Layer Index

### Cognitive Layer (`logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations on IES optimization challenges, gaps in existing approaches, key insight, and assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable claims (C01-C05) on IGA mechanisms and performance |
| [concepts.md](logic/concepts.md) | 7 key technical terms covering IES components, pricing mechanisms, and algorithm operations |
| [experiments.md](logic/experiments.md) | 5 experimental analyses (E01-E05) covering three operational scenarios and comparative evaluation |
| [related_work.md](logic/related_work.md) | 8 typed dependency references (RW01-RW08) spanning IES optimization and evolutionary computation |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, and known limitations of the IGA-IES framework |

### Physical Layer (`/src`)
| File | Description |
|------|-------------|
| [environment.md](src/environment.md) | Hardware, software, and parameter specifications for reproducibility |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 12-node research DAG covering the IGA development and evaluation trajectory |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 1 table + 17 figures |
| [tables/table1.md](evidence/tables/table1.md) | Comparison of five algorithms across three scenarios |
| [figures/figure1.md](evidence/figures/figure1.md) | Diagram of IES operational architecture |
| [figures/figure2.md](evidence/figures/figure2.md) | Research flow chart of the proposed IGA |
| [figures/figure3.md](evidence/figures/figure3.md) | Diagram of cyclic crossover operation |
| [figures/figure4.md](evidence/figures/figure4.md) | Research framework for case study |
| [figures/figure5.md](evidence/figures/figure5.md) | Power and gas purchase in IES Scenario 1 |
| [figures/figure6.md](evidence/figures/figure6.md) | Electric load and heat load in Scenario 1 |
| [figures/figure7.md](evidence/figures/figure7.md) | ESS operation in Scenario 1 |
| [figures/figure8.md](evidence/figures/figure8.md) | Equality constraint violations in Scenario 1 |
| [figures/figure9.md](evidence/figures/figure9.md) | Power and gas purchase in Scenario 2 |
| [figures/figure10.md](evidence/figures/figure10.md) | Electric load and heat load in Scenario 2 |
| [figures/figure11.md](evidence/figures/figure11.md) | ESS operation in Scenario 2 |
| [figures/figure12.md](evidence/figures/figure12.md) | Equality constraint violations in Scenario 2 |
| [figures/figure13.md](evidence/figures/figure13.md) | Power and gas purchase in Scenario 3 |
| [figures/figure14.md](evidence/figures/figure14.md) | Electric load and heat load in Scenario 3 |
| [figures/figure15.md](evidence/figures/figure15.md) | ESS operation in Scenario 3 |
| [figures/figure16.md](evidence/figures/figure16.md) | Equality constraint violations in Scenario 3 |
| [figures/figure17.md](evidence/figures/figure17.md) | Pareto front comparison (IGA vs MGA) in Scenario 1 |
