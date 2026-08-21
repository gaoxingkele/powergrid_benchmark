---
title: "A Review of Energy Storage Economics, Load Forecasting, and Hybrid Control Strategies for AC Microgrids in Modern Power Systems"
authors: ["Yaser Ibrahim Rashed Alshdaifat", "Krishnamachar Prasad", "Jeff Kilby"]
year: 2026
venue: "Electronics"
doi: "10.3390/electronics15122549"
ara_version: "1.0"
domain: "Power systems engineering — energy storage integration, techno-economic optimization, load forecasting, hybrid metaheuristic control for AC microgrids (review/survey)"
keywords: ["energy storage systems", "non-network solutions (NNS)", "techno-economic optimization", "active distribution networks", "hybrid metaheuristics", "battery management systems (BMS)", "grid resilience", "GWO-PSO", "state of energy (SoE)", "degradation-aware planning"]
claims_summary:
  - "Energy storage integration must be treated as a tightly coupled macro-planning/micro-control optimization problem, not a hardware installation, because decoupling planning from operation lets forecast errors and degradation accumulate into capital-efficiency losses."
  - "Degradation-aware modelling that distinguishes calendar from cycle ageing is the primary economic lever for storage, whereas static planning traps sizing in local optima."
  - "State of Energy is the grid-aware dispatch metric of record over State of Charge because usable releasable energy varies nonlinearly with terminal voltage and temperature that SoC ignores."
  - "Hybrid metaheuristics that pair a global explorer (GWO) with a local exploiter (PSO) resolve the exploration-exploitation dilemma better than standalone or rule-based/MPC controllers under renewable uncertainty."
  - "Migrating from statistical to structured deterministic/ML forecasting compresses forecast error enough to convert reactive dispatch into proactive scheduling."
  - "Whether external sizing optimization or external dispatch control dominates is set by the operating environment (isolated/high-CAPEX vs grid-integrated/dynamic-pricing), not by an absolute ranking."
  - "Storage technology and integration topology (AC/DC/hybrid) impose fundamental upstream constraints on achievable control bandwidth, efficiency, and degradation."
  - "Coupling macro-economic sizing tools with meso-scale physical and micro-scale dynamic simulators bridges the fidelity gap that static economic models leave open."
  - "Strategically deployed BESS acting as a non-network solution, coordinated with reactive-power devices such as STATCOMs, defers capital-intensive network reinforcement at fixed investment cost."
abstract: "As power grids transition towards highly renewable generation on a global scale, maintaining dynamic stability is becoming a major challenge. Replacing traditional synchronous generators with inverter-based renewables strips the grid of rotational inertia, leaving active distribution networks highly vulnerable to frequency deviations and voltage spikes. To avoid expensive poles and wires upgrades, Battery Energy Storage Systems (BESS) are increasingly being deployed as Non-Network Solutions (NNS). However, the current literature reveals a distinct gap between the macro-scale economic planning of these storage assets and the micro-scale dynamic control actually required to keep the grid resilient. To address this gap, this review proposes a multi-layer deterministic synthesis framework that links physical renewable modelling, degradation-aware techno-economic planning, deterministic forecasting, and EMS dispatch through offline time-domain control validation for AC-microgrid energy storage integration. The research examines how advanced central control units within battery management systems can rigorously and jointly estimate State of Charge (SoC) and State of Energy (SoE) to ensure accurate grid-aware dispatch. Furthermore, the study explores the integration of degradation-aware economic modelling in HOMER Pro with dynamic transient control in MATLAB/Simulink R2025b, driven by hybrid metaheuristic optimization algorithms like Grey Wolf Optimizer (GWO) and Particle Swarm Optimization (PSO). This analysis demonstrates that integrating energy storage must be treated as a tightly coupled multidimensional optimization problem to successfully deliver the secure and sustainable infrastructure needed to solve the modern energy trilemma."
collection: "by_journal"
journal: "Electronics"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p2_hyperbolic_gcn_smart_dispatch/p2_hyperbolic_gcn_smart_dispatch__12__a_review_of_energy_storage_economics_load_forecasting_and__53115a260d.pdf"
---

# A Review of Energy Storage Economics, Load Forecasting, and Hybrid Control Strategies for AC Microgrids in Modern Power Systems

## Overview

This is a narrative/technical review (Electronics, MDPI, 2026) that synthesizes 103 screened studies (PRISMA-informed) on energy storage integration in renewable-dominated AC microgrids. Its organizing thesis is that the literature treats macro-scale techno-economic storage *planning* and micro-scale dynamic *control* as isolated domains, and that this decoupling is the central gap. The review's proposed contribution is a **multi-layer deterministic synthesis framework** that links physical renewable modelling (PVsyst/ETAP), degradation-aware techno-economic planning (HOMER Pro), deterministic forecasting, and EMS dispatch validated through offline time-domain simulation (MATLAB/Simulink), driven by hybrid metaheuristics (GWO-PSO) and grounded in joint SoC/SoE state estimation.

Because it is a review, this ARA carries **no original experiment**. Claims are the review's synthesizing/taxonomic takeaways (each bounded with conditions, falsification criteria, and pointers to the surveyed evidence/tables); `experiments.md` records the review's comparison/analysis axes (directional only); `logic/solution/` holds the taxonomy and the proposed framework and objective-function formalization (no algorithm is invented by the review); `src/` is `environment.md` alone (no released code accompanies the paper).

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (low-inertia grids, planning/operation decoupling) → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 9 falsifiable review takeaways (C01–C09) |
| [concepts.md](logic/concepts.md) | 17 technical concepts (NNS, SoC/SoE, degradation-aware modelling, HESS, GWO-PSO, LPSP, SST, signal decomposition, …) |
| [experiments.md](logic/experiments.md) | 11 directional review comparison/analysis axes (E01–E11) |
| [related_work.md](logic/related_work.md) | Typed citation landscape (102 references; full RW blocks for load-bearing deltas) |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations of the review |
| [solution/framework.md](logic/solution/framework.md) | The proposed multi-layer / multi-scale synthesis framework (Fig 2) |
| [solution/taxonomy.md](logic/solution/taxonomy.md) | Taxonomy of storage economics / forecasting / hybrid control |
| [solution/objective_functions.md](logic/solution/objective_functions.md) | Optimization objective + state-estimation formalization (Eqs 1–11) |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Review methodology environment (databases, tools cited, PRISMA); analytical — no code released | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 31-node DAG reconstructing the review's argument structure (7 questions, 12 experiments/syntheses, 6 decisions, 6 dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 9 tables + 7 figures |
| tables/table1–table9 | Storage tech, configs, sizing-vs-dispatch, tool alignment, forecasting, preprocessing, NNS factors, planning studies, SoC/SoE synthesis |
| figures/figure1–figure7 | PRISMA flow, multi-layer framework, AC-coupled architecture, AC/DC/HESS topologies, GWO-PSO workflow |
