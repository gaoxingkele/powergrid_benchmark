---
title: "A Two-Stage Energy and Service Market Framework Involving Unit Commitment and Network-Based Redispatch"
authors: ["Roberto Cometa", "Gioacchino Tricarico", "Maria Dicorato", "Giuseppe Forte"]
year: 2026
venue: "Energies"
doi: "10.3390/en19102377"
ara_version: "1.0"
domain: "Electricity market design, ancillary services, unit commitment, network redispatch"
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__01__a_two_stage_energy_and_service_market_framework_involving_unit_commitm__1bc5ffee79.pdf"
keywords: ["ancillary service market", "market coordination", "network-based redispatch", "reserve provision", "unit commitment", "NREL-118 bus", "DC load flow", "PTDF", "secondary reserve", "zonal market"]
claims_summary:
  - "A sequential DAM-then-ASM framework with bid adjustment can resolve network overloads, RES/load forecast updates, and secondary reserve requirements with a single NCUCER MILP solved daily."
  - "The DAM-ASM bid adjustment process (5 case-dependent DT clearing orders) correctly captures unit technical limits, routing DT units below their technical minimum to mandatory SU or SD bids."
  - "The proposed two-stage sequential approach yields total costs 5.6 times lower than a benchmark UC-with-reserve DAM model, because the sequential framework lets the DAM clear at marginal cost and reserves are procured only as needed in ASM."
  - "CC NG technology is the most economically attractive for ASM service provision; ST NG units are mainly shut down due to large MUT/MDT; DH units contribute primarily to UR/DR."
  - "DSM is sufficient to cover SRR year-round but USM requires SU or DR clearance for 741 time steps, confirming that asymmetric SR provision is a structural constraint."
  - "Sensitivity on bid factors shows UR service is price-inelastic (mainly for overload mitigation), whereas DR, SU, and SD quantities respond to price changes."
  - "The bid adjustment mechanism success depends on DH bidding strategy (85% vs 90% DAM allocation) which affects zonal prices, overload occurrences, and ASM costs."
abstract: "The provision of power and grid services requires the co-ordination between Day-Ahead Market (DAM) and Ancillary Service Market (ASM) to attain reserve services and technically feasible operating conditions for market players and for the network. In this context, this work proposes a multi-stage approach to evaluate the dispatched power to balance the forecast updates of renewable energy sources and load from DAM to ASM, taking into account network and Unit Commitment (UC) constraints. The DAM is solved considering a zonal market framework and neglecting the UC constraints. Then, a mechanism to adjust the ASM bids is developed, defining time-varying costs for each regulation. Finally, the ASM is modelled as a network-constrained UC and economic redispatch (NCUCER) optimization problem, aiming at minimizing the overall cost, in order to procure secondary reserve requirement and to adjust the DAM schedules, taking into account network and UC constraints and balancing forecast updates. DC load flow sensitivity factors are exploited to evaluate the influence of redispatch actions and forecast updates on the observed power flow. This procedure is applied to NREL 118-Bus Test System assessing its performances throughout a yearly time horizon."
---

# A Two-Stage Energy and Service Market Framework Involving Unit Commitment and Network-Based Redispatch

## Overview

This paper proposes a multi-stage market framework modeling the sequential interaction between a zonal Day-Ahead Market (DAM) and a nodal Ancillary Service Market (ASM) in the European context. The DAM is solved as a merit-order zonal LP without UC constraints. A bid adjustment mechanism then prepares ASM bids accounting for DAM schedules and unit technical limits. The ASM is formulated as a Network-Constrained UC and Economic Redispatch (NCUCER) MILP that minimizes redispatching costs while procuring secondary reserve, handling RES/load forecast updates, and enforcing branch flow limits and unit commitment constraints (MUT/MDT). The methodology is applied to the NREL 118-Bus system with 327 units (40.5 GW) over a full leap year at hourly resolution. Results demonstrate practical feasibility and show the sequential approach achieves total costs 5.6 times lower than a benchmark co-optimized model.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (O1–O5) \(\rightarrow\) gaps (G1–G3) \(\rightarrow\) key insight |
| [claims.md](logic/claims.md) | 7 falsifiable claims (C01–C07) |
| [concepts.md](logic/concepts.md) | 12 key technical terms formally defined |
| [experiments.md](logic/experiments.md) | 6 declarative verification/analysis plans (E01–E06) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the 44 references |
| [solution/constraints.md](logic/solution/constraints.md) | Assumptions, boundary conditions, and limitations of the market framework |
| [solution/formulation.md](logic/solution/formulation.md) | DAM and ASM objective functions and constraints (Eqs. 1–44) |
| [solution/method.md](logic/solution/method.md) | Four-stage procedure: DAM, bid adjustment, DCLF/sensitivity, ASM optimization |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Python/Pyomo/Gurobi toolchain, DIgSILENT PowerFactory, NREL-118 system data | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG covering DAM-ASM sequential design, bid adjustment, sensitivity studies |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 8 tables + 19 figures (each markdown + PNG) |
