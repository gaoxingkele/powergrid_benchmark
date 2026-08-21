---
title: "A Two-Stage Coordinated Dispatch Framework for Integrated Energy Systems with Growing Wind Power Penetration Considering Price-Based Demand Response"
authors: ["Xun Lu", "Peng Rao", "Jinye Cao", "Ruisheng Diao"]
year: 2026
venue: "Energies"
doi: "10.3390/en19143238"
ara_version: "1.0"
domain: "Integrated energy system (electricity–gas) day-ahead economic dispatch optimization"
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__08__a_two_stage_coordinated_dispatch_framework_for_integrated_energy_syste__4dadd14e4b.pdf"
keywords: ["integrated energy system", "price-based demand response", "vehicle-to-grid", "power-to-gas", "time-of-use tariff", "cross-price elasticity", "LCOE degradation", "security-constrained dispatch", "Weymouth equation", "MILP"]
claims_summary:
  - "Coupling price-based demand response with bidirectional V2G in a security-constrained power–gas co-optimization lowers total operating cost and flattens the load curve beyond price-response alone, with V2G contributing most of the incremental peak-shaving."
  - "Power-to-gas is the decisive enabler of renewable accommodation: it converts surplus wind into synthetic gas, eliminating curtailment at a small cost penalty."
  - "Dispatch cost is governed primarily by wind availability, more than by any single demand-side or storage flexibility mechanism."
  - "An LCOE storage-degradation term reprices cycling but does not alter the dispatch when storage already runs at its cycle-count limit."
  - "Electrical-side demand flexibility propagates across carriers, relaxing ramping stress on the coupled gas network."
  - "Adding V2G lifts the valley price and damps peak-price anomalies that demand-only pricing cannot resolve."
  - "Assembling the two coupled decision stages as a single MILP/MISOCP stays computationally lightweight (sub-0.01% gap in seconds) at this test-system scale."
abstract: "With energy-structure transformation and carbon-neutrality goals, the Integrated Energy System (IES) faces challenges of multi-energy coupling complexity, renewable-induced supply–demand imbalance, and under-used demand-side flexibility. This paper establishes a security-constrained economic dispatch model embedding multi-level demand response for a coupled electricity–gas IES. Four modules are developed: a time-of-use price-based demand response (PDR) strategy with cross-price elasticity and market-stability constraints; an aggregated bidirectional vehicle-to-grid (V2G) EV model; a combined economic index pairing TOU tariff with a Levelized Cost of Electricity (LCOE) storage-degradation term; and power-to-gas (P2G) electricity–gas coupling. The framework is cast as a two-stage (retail-pricing/demand-shaping then security-constrained dispatch) yet single-instance MILP. Numerical simulations on a modified IEEE 33-node distribution network coupled with a 20-node gas network show the co-optimization reduces total operating cost and improves local renewable accommodation."
---

# A Two-Stage Coordinated Dispatch Framework for Integrated Energy Systems with Growing Wind Power Penetration Considering Price-Based Demand Response

## Overview

The paper builds a day-ahead, security-constrained economic dispatch model for a coupled electricity–gas Integrated Energy System (IES) that jointly unlocks demand-side flexibility (price-based demand response, PDR) and mobile storage flexibility (bidirectional vehicle-to-grid, V2G), while coupling the two carriers through power-to-gas (P2G) conversion and pricing storage/EV wear through a Levelized-Cost-of-Electricity (LCOE) degradation term. The novelty relative to prior art (Table 1) is embedding all four mechanisms — PDR with cross-price elasticity, bidirectional V2G, P2G coupling, and LCOE degradation — inside a single security-constrained co-optimization that also enforces DistFlow power flow, Weymouth gas dynamics, and explicit retail market-stability limits (bounded peak-to-valley ratio, enforced peak/flat/valley tariff ordering). The framework is organized as two sequentially coupled decision stages (retail pricing/demand-shaping → security-constrained dispatch) but assembled and solved as one mixed-integer program to preserve global optimality. A case study on a modified IEEE 33-node distribution network coupled to a 20-node gas grid, solved in MATLAB 2024a with CPLEX 12.7.1, compares three scenarios (baseline, PDR-only, PDR+V2G) and an ablation study to isolate each mechanism's marginal contribution.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 7 falsifiable claims (C01–C07) |
| [concepts.md](logic/concepts.md) | 11 key technical terms formally defined |
| [experiments.md](logic/experiments.md) | 6 declarative verification plans (E01–E06) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the 30 references |
| [solution/formulation.md](logic/solution/formulation.md) | Objective function + PDR / elasticity load models (Eq. 1–12, 63) |
| [solution/method.md](logic/solution/method.md) | Two-stage architecture, IESO, TOU mechanism, case design |
| [solution/constraints.md](logic/solution/constraints.md) | All operational/network/device constraints (Eq. 13–62), assumptions, limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | MATLAB/CPLEX toolchain, test system, data provenance; no code released | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG (question → design → cases → ablation → dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 10 tables + 12 figures (each markdown + PNG) |
