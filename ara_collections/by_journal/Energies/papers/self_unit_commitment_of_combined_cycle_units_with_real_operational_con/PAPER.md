---
title: "Self-Unit Commitment of Combined-Cycle Units with Real Operational Constraints"
authors: ["Mauro González-Sierra", "Sonja Wogrin"]
year: 2023
venue: "Energies"
doi: "10.3390/en17010051"
ara_version: "1.0"
domain: "Power systems — unit commitment / combined-cycle gas turbine operational scheduling (MIP optimization)"
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__10__self_unit_commitment_of_combined_cycle_units_with_real_operational_con__c6281ef483.pdf"
keywords: ["combined-cycle gas turbine", "unit commitment", "self-unit commitment", "steam turbines", "startup ramps", "mixed-integer programming", "load distribution", "supplementary fires", "thermal state", "Colombian power market"]
claims_summary:
  - "Representing a CCGT as individual coupled gas/steam units (with configuration-style coupling constraints) exposes a per-unit dispatch that aggregate/mode models structurally cannot express."
  - "Startup trajectories are gated by the unit's thermal state (hot/warm/cold), so schedules assuming a hotter state than the plant occupies are physically unfollowable."
  - "Requiring minimum gas-turbine operating hours (and unit count) before a steam-turbine start imposes a heat-accumulation precedence that reshapes the feasible plant ramp."
  - "Supplementary fires at the HRSG decouple steam-turbine output boosts from gas-turbine output, letting the plant reach maximum capacity without raising gas generation."
  - "Penalising pairwise gas-turbine output differences (when both units exceed technical minimum) drives even loading, argued to reduce steam-rotor thermal stress."
  - "Schedules from models that omit ramp/thermal-state constraints deviate from realisable output beyond the market's 5% tolerance, converting the modelling omission into recurring daily monetary penalties."
abstract: "This paper highlights the importance of accurately modeling the operational constraints of Combined-Cycle Gas Turbines (CCGTs) within a unit-commitment framework. In practice, in Colombia, when given an initial dispatch by the Independent System Operator, CCGT plants are operated according to the results of heuristic simulation codes. Such heuristics often omit technical operating constraints, including hot, warm, or cold startup ramps; the minimum operation hours required for a gas turbine to start a steam turbine; the relationship between the dispatched number of steam and gas turbines; the load distribution among gas turbines; and supplementary fires. Most unit-commitment models in the literature represent standard technical constraints like startup, shutdown, up/down ramps, and in some cases, supplementary fires. However, they typically overlook other real-life CCGT operating constraints, which were considered in this work. These constraints are crucial in integrated energy systems to avoid equipment damage, which can potentially put CCGT plants out of service and ultimately lead to lower operating costs."
---

# Self-Unit Commitment of Combined-Cycle Units with Real Operational Constraints

## Overview

The paper proposes a Self-Unit-Commitment (SEUC) model — a Mixed-Integer Programming (MIP) formulation — for a single Combined-Cycle Gas Turbine (CCGT) plant that, given an initial dispatch from the Independent System Operator (ISO), produces an hourly commitment and dispatch plan the plant can physically follow. Its distinguishing choice is a hybrid representation: gas and steam turbines are modelled as separate individual units (component representation) while carrying configuration-style coupling constraints (plant output limits, startup/shutdown ramps, gas/steam unit-count relations). Two constraints are claimed as novel to UC models: (i) the minimum gas-turbine operating hours required before a steam turbine may start (thermal prerequisite via the HRSGs), with hot vs cold steam-turbine startups differentiated; (ii) a load-distribution constraint penalising output differences between gas turbines that are both above technical minimum, motivated by steam-rotor thermal-stress uniformity. The model also captures hot/warm/cold startup ramp blocks per Colombian grid-code declarations, supplementary fires at the HRSG, steam waste, and auxiliary consumption. Two 24-hour case studies on a TEBSA-like 5 × 2 plant (5 gas + 2 steam turbines, 800 MW) show the model's followable dispatch vs a heuristic schedule, and quantify daily deviation penalties (USD 60,957 and USD 66,093) the heuristic would incur under the Colombian 5% deviation rule.

Note on citation date: the article was published 21 December 2023 (© 2023 by the authors); the issue citation is Energies 2024, 17, 51.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (heuristic dispatch, equipment damage, penalties) → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 6 falsifiable claims (C01–C06) |
| [concepts.md](logic/concepts.md) | 12 key technical terms formally defined |
| [experiments.md](logic/experiments.md) | 4 declarative verification plans (E01–E04) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the 25 references |
| [solution/formulation.md](logic/solution/formulation.md) | The SEUC MIP: objective (Eq. 1) + all constraint groups (Eqs. 2–46) |
| [solution/method.md](logic/solution/method.md) | Hybrid component+mode modelling approach, plant topology, startup state machine, case-study design |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, known limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Model type, data provenance (TEBSA / Colombian grid code); solver/software not specified in paper | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 14-node research DAG (motivation → formulation decisions → case studies → penalty analysis → future work) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 6 tables + 7 figures (each markdown + PNG) |
