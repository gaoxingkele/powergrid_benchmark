---
title: "The Study of an Improved Particle Swarm Optimization Algorithm Applied to Economic Dispatch in Microgrids"
authors: ["Ang Dong", "Seon-Keun Lee"]
year: 2024
venue: "Electronics"
doi: "10.3390/electronics13204086"
ara_version: "1.0"
domain: "Microgrid economic-environmental dispatch; metaheuristic optimization (particle swarm optimization)"
keywords: ["microgrid", "economic-environmental dispatch", "SCMPSO", "particle swarm optimization", "chaotic mapping", "second-order oscillation", "energy storage", "renewable energy", "distributed generation"]
claims_summary:
  - "Injecting a Henon-chaotic initial distribution, an adaptive nonlinear inertia weight, complementary dynamic learning factors, and a second-order oscillation term into PSO trades early exploration for late exploitation, improving convergence and local-optima escape on standard multimodal benchmarks."
  - "Splitting the oscillation factor by a mid-run threshold (t <= Tmax/2 oscillatory, t > Tmax/2 progressive) is what lets a single search phase deliver both wide early exploration and stable late refinement."
  - "For this multi-source microgrid, a merit-order dispatch (renewables first, storage for buffering, thermal as slack, grid as final balance) minimizes total operating-plus-environmental cost while respecting power balance and device limits."
  - "A stronger metaheuristic lowers the whole cost stack jointly (operation/maintenance, fuel, depreciation, environmental) rather than trading one against another, because a cheaper dispatch simultaneously burns less fuel and emits less pollutant."
  - "Setting the iteration budget well above the point where competing PSO variants first reach the acceptance band buys robustness margin at the cost of extra compute, not better final accuracy."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__12__the_study_of_an_improved_particle_swarm_optimization_algorithm_applied__a9403b686a.pdf"
abstract: "With the widespread use of fossil fuels, the Earth's environment is facing a severe threat of degradation. Traditional large-scale power grids have struggled to meet the ever-growing demands of modern society. The implementation and functioning of microgrids not only enhance the use of renewable energy sources but also considerably diminish the environmental damage resulting from fossil fuel consumption. However, the inherent instability of renewable energy presents a major challenge to the reliability of microgrids. To address the uncertainties of wind and photovoltaic power generation, it is urgent to adopt effective operational control methods to adjust power distribution, thereby achieving an economically efficient system operation and ensuring a reliable power supply. This paper utilizes a microgrid system consisting of wind power, photovoltaic power generation, thermal power units, and energy storage devices as the research object, establishing an economic dispatch model aimed at minimizing the total operating cost of the system. To solve this problem, the paper introduces second-order oscillatory particles and improves the Particle Swarm Optimization algorithm, proposing a second-order oscillatory chaotic mapping particle swarm optimization (SCMPSO). The simulation results show that this method can effectively optimize system operating costs while ensuring the stable operation of the microgrid."
---

# The Study of an Improved Particle Swarm Optimization Algorithm Applied to Economic Dispatch in Microgrids

## Overview

This paper addresses the economic-environmental dispatch of a multi-source microgrid composed of distributed photovoltaic (PV), wind turbine (WT), small thermal generator (DG), and energy storage system (ESS) units, coupled to a main grid. It builds a per-device cost model (operation/maintenance, fuel, depreciation, grid-interaction, and pollutant-treatment costs), subject to power-balance, device-output, grid-interaction, pollutant-emission, and ramp-rate constraints, with the objective of minimizing total daily cost over a 24-hour horizon.

To solve the resulting nonlinear constrained problem, the authors propose **SCMPSO** (labelled "second-order oscillatory chaotic mapping PSO" in the abstract and "Stochastic Constrained Multi-Objective PSO" in the Figure 1 flowchart), a modified particle swarm optimizer combining four mechanisms over standard PSO: (1) Henon chaotic-mapping population initialization, (2) an adaptive nonlinear inertia-weight schedule, (3) complementary sinusoidal dynamic learning factors, and (4) a second-order oscillation term in the velocity update with a mid-run threshold switching between oscillatory and progressive convergence. The method is validated on five standard benchmark functions and compared against PSO, CPSO, and QPSO, then applied to a 24-hour summer dispatch case study for a microgrid in Jiangsu Province, China.

Note on ownership: this is an external, published third-party paper (MDPI *Electronics*, 2024); it is not an original artifact of this repository. No source code was released with the paper (software is stated only as "MATLAB 2020a"; raw data withheld for confidentiality).

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations -> gaps -> key insight -> assumptions |
| [claims.md](logic/claims.md) | 6 falsifiable claims (C01-C06) |
| [concepts.md](logic/concepts.md) | 9 key technical terms, formally defined |
| [experiments.md](logic/experiments.md) | 5 declarative verification plans (E01-E05) |
| [related_work.md](logic/related_work.md) | Typed citation dependency graph (26 references) |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |
| [solution/algorithm.md](logic/solution/algorithm.md) | The improved PSO (SCMPSO): formulation, mechanisms, pseudocode |
| [solution/formulation.md](logic/solution/formulation.md) | Microgrid economic-environmental dispatch problem formulation |
| [solution/heuristics.md](logic/solution/heuristics.md) | Practical tuning heuristics stated by the paper |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Runtime (MATLAB 2020a), data provenance, protocols, seeds | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 18-node research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 7 tables + 14 figures |
