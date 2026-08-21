---
title: "Low Carbon Economic Dispatch of IES Considering Flexibility and Multi-Entity Participation Based on Improved PSO"
authors: ["Guodong Wang", "Haiyang Li", "Xiao Yang", "Huayong Lu", "Xiao Song", "Zhaoyuan Zhang", "Jinfeng Wang"]
year: 2026
venue: "Electronics"
doi: "10.3390/electronics15050933"
ara_version: "1.0"
domain: "Power systems — integrated energy system dispatch optimization"
keywords: ["low carbon economic dispatch", "integrated energy system", "multi-entity", "flexibility", "improved Particle Swarm Optimization", "bi-level optimization", "green certificate carbon trading", "electric vehicles"]
claims_summary:
  - "Adding a flexibility objective turns single-objective dispatch into a tunable economy-flexibility trade-off"
  - "A price-guided aggregator holds total cost near-invariant by reallocating demand response"
  - "Aggregated EVs are a dispatchable flexibility resource whose benefit is time-localized and cost-effective"
  - "Pricing carbon inside the operator objective imposes an irreducible economy-emissions trade-off"
  - "Green-certificate trading complements carbon trading, cutting emissions further while offsetting part of the carbon cost"
  - "A normalized per-carrier flexibility index makes heterogeneous resources comparable and exposes the bottleneck carrier"
  - "System-flexibility timing is governed by EV fleet composition, a lever for relieving a deficit hour"
  - "The carbon price is a monotone lever trading emissions against operator revenue"
  - "Injecting search diversity into PSO improves convergence speed, solution quality, and run-to-run stability"
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__07__low_carbon_economic_dispatch_of_ies_considering_flexibility_and_multi__7d90cf7078.pdf"
abstract: "To address the significant scheduling challenges arising from high-penetration renewable integration and coupled multi-energy loads, this study examines the operational scheduling of an integrated energy system (IES) that incorporates system operators, user aggregators, electric vehicles, and other stakeholders. First, the flexibility demand and supply resources in the IES were analyzed, and flexibility indicators were quantified. Subsequently, a multi-objective bi-level optimization model considering flexibility and multi-entity participation was established for the IES's low-carbon economic dispatch. The upper-level model considered the IES operator's revenue and system flexibility, incorporating a green certificate carbon trading mechanism, while the lower-level model accounted for user aggregator costs and electric vehicle self-benefits, with interactions between the two levels through energy prices and purchase quantities. Finally, an improved Particle Swarm Optimization (PSO) algorithm was employed to solve the proposed upper-level model, and CPLEX 12.10 software was used for the lower-level model. A typical scenario in northern China was selected to validate the proposed model. The results demonstrated that the proposed model balanced system economy and flexibility compared to the traditional single-objective economic dispatch. Compared with only considering the benefits of operators, the proposed model can balance the interests of multiple parties. Additionally, compared to the traditional PSO algorithm, the improved PSO algorithm reduced the number of iterations at convergence by 52.0%, improved the closeness of the obtained optimal solution to the ideal solution by 7.5%, and had better convergence and optimization performance. (Note: the body of the paper reports the iteration reduction as 54.0%; see evidence/README.md.)"
---

# Low Carbon Economic Dispatch of IES Considering Flexibility and Multi-Entity Participation Based on Improved PSO

## Overview

This paper develops a bi-level (Stackelberg) low-carbon economic dispatch model for a park-level integrated energy system (IES) that jointly optimizes operator economics and system flexibility while balancing three stakeholder classes — the IES operator (leader), a user aggregator, and aggregated electric-vehicle clusters (followers). Flexibility is quantified as a normalized per-carrier index built from upward/downward supply margins of conversion equipment, storage, demand response, and EVs. The operator objective embeds a green-certificate–carbon (GCT-CET) trading mechanism. The upper level is solved by an improved PSO (adaptive inertia weight, sine-modulated learning factors, four sub-populations with distinct position-update rules, DBO-tuned), the lower level by CPLEX 12.10, with a TOPSIS compromise chosen from the Pareto front. A five-scenario ablation on a northern-China typical-day case shows the model trades revenue for flexibility, keeps aggregator cost stable, uses EVs as time-localized flexibility, and cuts emissions via carbon + green-certificate trading; the improved PSO converges faster, closer, and more stably than plain PSO and DBO.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (O1-O4) → gaps (G1-G2) → key insight → assumptions |
| [claims.md](logic/claims.md) | 9 falsifiable claims (C01-C09) |
| [concepts.md](logic/concepts.md) | 8 core technical terms |
| [experiments.md](logic/experiments.md) | 7 declarative verification plans (E01-E07) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over all 31 references |
| [solution/constraints.md](logic/solution/constraints.md) | Model constraints (Eq. 12-25), assumptions, limitations |
| [solution/formulation.md](logic/solution/formulation.md) | Full bi-level formulation with equation numbers |
| [solution/algorithm.md](logic/solution/algorithm.md) | Improved PSO mechanisms + solution procedure |
| [solution/architecture.md](logic/solution/architecture.md) | Optimization + physical architecture (Figures 1-2) |
| [solution/heuristics.md](logic/solution/heuristics.md) | 5 improved-PSO implementation heuristics (H01-H05) |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Solvers, data sources, protocols, reproducibility | — |
| [execution/improved_pso.py](src/execution/improved_pso.py) | Reconstructed IPSO update mechanism (Eqs. 26-31) | C09 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 14-node research DAG (questions, decisions, experiments, dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 7 tables + 16 figures (all with .md + .png) |
| tables/table1.md … table7.md | Device params, DR prices, TOU prices, EV params, scenario results, carbon-price sweep, algorithm stats |
| figures/figure1.md … figure16.md | Bi-level & physical diagrams, forecasts, optimized power/DR/EV schedules, flexibility & convergence plots |
