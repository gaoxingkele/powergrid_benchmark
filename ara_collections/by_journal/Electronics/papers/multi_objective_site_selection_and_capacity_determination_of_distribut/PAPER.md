---
title: "Multi-Objective Site Selection and Capacity Determination of Distribution Network Considering New Energy Uncertainties and Shared Energy Storage of Electric Vehicles"
authors: ["Guodong Wang", "Haiyang Li", "Xiao Yang", "Huayong Lu", "Xiao Song", "Zheng Li", "Yi Wang"]
year: 2025
venue: "Electronics"
doi: "10.3390/electronics14010151"
ara_version: "1.0"
domain: "Power systems — active distribution network planning; multi-objective siting/sizing of EV shared energy storage under renewable uncertainty"
keywords: ["distribution networks", "electric vehicle", "multi-objective particle swarm optimization", "uncertainty", "renewable energy", "Frank copula function", "CNN", "Bi-LSTM", "site selection", "capacity determination"]
claims_summary:
  - "Siting dispatchable EV-fleet shared storage at network-selected nodes suppresses local DG-driven voltage deviation via charge-at-surplus / discharge-at-deficit within a maintained SOC band."
  - "EV-fleet shared storage substitutes for equal-role conventional stationary storage, improving voltage stability and network loss because fleet availability aligns temporally with wind-solar output."
  - "A KDE + Frank-copula scenario generator reproduces the negative wind-solar correlation and randomness that independent-marginal sampling omits."
  - "A CNN-BiLSTM predictor lowers EV cluster state (arrival/departure/SOC) prediction error relative to standalone CNN or Bi-LSTM."
  - "A three-objective (voltage fluctuation + network loss + storage capacity) formulation exposes trade-offs a single-objective model cannot balance, improving planning feasibility."
abstract: "In recent years, the share of renewable energy in the distribution network has been increasing. To deal with high renewable energy penetration, it is important to improve the energy efficiency and stability of the distribution network. In this paper, the optimal configuration of a distribution network with a high proportion of new energy and electric vehicles is investigated. Firstly, based on the copula theory, the clustered new energy data are obtained by optimizing the wind and solar output scenarios. Secondly, the uncertainty of renewable energy output is fully considered in the planning stage of the distribution network. Subsequently, an improved multi-objective particle swarm optimization algorithm is adopted to determine the optimal capacity and location of charging stations. Finally, the IEEE 33-node distribution network is used for case analysis. Through the comparison of network loss, voltage change, and other related parameters, the advantages of shared energy storage characteristics of electric vehicles in smoothing the uncertainty of the high proportion of new energy are verified."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p4_resilience_distribution_planning/p4_resilience_distribution_planning__04__multi_objective_site_selection_and_capacity_determinati__25730500a1.pdf"
---

# Multi-Objective Site Selection and Capacity Determination of Distribution Network Considering New Energy Uncertainties and Shared Energy Storage of Electric Vehicles

## Overview

This paper proposes a planning-stage method for an active distribution network (ADN) with high renewable (DG) penetration and electric-vehicle (EV) fleets. It combines three pieces: (i) a DG-output scenario generator using non-parametric kernel density estimation (KDE) plus a Frank-copula joint distribution to capture wind–solar correlation and randomness (500 scenarios reduced to 5 representatives); (ii) a CNN-BiLSTM predictor that processes EV-cluster historical data (arrival time, departure time, initial SOC) to build a dispatchable "shared energy storage" model of the fleet; and (iii) a three-objective optimization — node voltage fluctuation, network loss, and energy-storage capacity — solved with a multi-objective particle swarm optimizer (MOPSO) to jointly select EV-charging-station (EVS) sites and capacities. The method is validated on the IEEE 33-node system across four scenarios (no DG; DG only; DG + EVS storage; DG + conventional storage). Results argue that EV shared storage stabilizes DG-induced voltage fluctuation at lower upfront cost than dedicated storage. The work is a modeling/simulation study; no code or numerical dataset is released (data availability statement points only to the article).

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable claims (C01–C05) |
| [concepts.md](logic/concepts.md) | 10 key technical terms |
| [experiments.md](logic/experiments.md) | 6 declarative verification plans (E01–E06) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the 35-reference footprint |
| [solution/formulation.md](logic/solution/formulation.md) | Multi-objective objective functions + siting/capacity constraints (Eq. 1–9) |
| [solution/method.md](logic/solution/method.md) | Scenario generation (KDE + Frank copula) and EV uncertainty handling (CNN-BiLSTM) |
| [solution/algorithm.md](logic/solution/algorithm.md) | MOPSO solver and its planning flow (Figure A1) |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Test system, tooling, data availability, seeds | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG (questions → method decisions → scenario experiments → dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 2 tables + 10 figures |
