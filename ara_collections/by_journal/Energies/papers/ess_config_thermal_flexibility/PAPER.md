---
title: "Multi-Objective Optimization of Energy Storage Station Configuration in Power Grids Considering the Flexibility of Thermal Load Control"
authors:
  - "Kaikai Wang"
  - "Yao Wang"
  - "Jin Gao"
  - "Yan Liang"
  - "Zhenfei Ma"
  - "Hanyue Liu"
  - "Zening Li"
year: 2025
venue: "Energies"
doi: "10.3390/en18102527"
ara_version: "1.0"
domain: "Power systems, energy storage optimization, demand-side flexibility"
keywords:
  - "temperature-controlled load flexibility"
  - "energy storage station"
  - "POA-GWO-CSO algorithm"
  - "multi-objective optimization"
  - "distribution network"
  - "renewable energy consumption"
  - "demand-side management"
  - "second-order cone programming"
  - "building thermal dynamics"
  - "grid operating costs"
claims_summary:
  - "C01: Incorporating temperature-controlled load flexibility into ESS configuration reduces total system operating costs compared with ESS-only deployment."
  - "C02: The POA-GWO-CSO hybrid algorithm achieves faster convergence and higher fitness values than standalone POA, GWO, or POA-GWO without CSO on the grid ESS multi-objective optimization problem."
  - "C03: ESS configuration without load flexibility reduces annual operating costs by approximately 32% and enables 100% RE consumption relative to no-ESS baselines."
  - "C04: Pre-cooling via building thermal mass leverages temperature-controlled load flexibility to shift air conditioning energy consumption away from peak tariff periods while maintaining thermal comfort."
abstract: "Given that traditional grid energy storage planning neglects the impact of power supply demand on the effectiveness of storage deployment, the resulting system suffers from limited operational economic performance and restricted renewable energy integration capability. In response to this challenge, this paper presents a multi-objective optimization approach for configuring a distribution network energy storage station (ESS) by incorporating the flexibility of temperature-controlled loads. This approach aims to enhance the efficiency of energy storage utilization, facilitate the local consumption of renewable energy (RE), and achieve mutually beneficial outcomes for both energy providers and consumers. Firstly, a controllable load model for the distribution network was developed, incorporating power balance constraints and the flexibility of temperature-controlled loads. Additionally, an ESS model was formulated, taking into account economic considerations and other influencing factors to ensure optimal deployment and operation. Secondly, this paper introduces a multi-objective optimization strategy for a distribution network ESS, targeting the minimization of both the microgrid operating costs and energy storage allocation costs. The proposed model was solved using the POA-GWO-CSO optimization algorithm to achieve the optimal energy storage deployment and cost efficiency. Finally, the effectiveness of the proposed model was verified through case analysis. The results demonstrate that the proposed grid energy storage optimization configuration model not only satisfies the requirements of both parties, but also enhances the overall system economic performance."
---

# Multi-Objective Optimization of Energy Storage Station Configuration in Power Grids Considering the Flexibility of Thermal Load Control

## Overview

This paper addresses the problem of configuring energy storage stations (ESS) in distribution networks by jointly considering supply-side economics and demand-side flexibility from temperature-controlled loads (air conditioning systems). The authors develop a multi-objective optimization framework that minimizes both grid operating costs (power purchase, generation, network loss, load costs) and ESS configuration costs (acquisition, installation, O&M, residual value recovery). A hybrid POA-GWO-CSO metaheuristic algorithm is proposed by augmenting the Pelican Optimization Algorithm with Grey Wolf Optimization leader strategies and Crisscross Optimization crossover operators. Case studies on a Shanxi Province dataset across three scenarios demonstrate that combining ESS with temperature-controlled load flexibility reduces annual operating costs by 33.6% versus no-ESS baselines, achieves 100% renewable energy consumption, and yields a static investment payback period of 8.5 years for the ESS.

## Layer Index

### Cognitive Layer (`logic/`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations, gaps, key insight, and assumptions |
| [claims.md](logic/claims.md) | 4 falsifiable claims (C01–C04) |
| [concepts.md](logic/concepts.md) | 8 technical terms with notation and definition |
| [experiments.md](logic/experiments.md) | 3 declarative experiment plans (E01–E03) |
| [related_work.md](logic/related_work.md) | Typed dependency graph of 27 cited works |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, known limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Data sources, hardware dependencies, software environment | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 10-node research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 1 table + 9 figures |
