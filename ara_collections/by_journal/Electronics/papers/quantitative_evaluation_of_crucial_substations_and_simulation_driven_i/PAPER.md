---
title: "Quantitative Evaluation of Crucial Substations and Simulation-Driven Impact Assessment of Commissioning Delays in Multi-Voltage Grid Planning"
authors: ["Xun Lu", "Fengjiao Li", "Jun Liu", "Chengwei Yang", "Lingxue Lin"]
year: 2025
venue: "Electronics"
doi: "10.3390/electronics14132633"
ara_version: "1.0"
domain: "Power systems engineering — multi-voltage grid planning; substation criticality assessment; investment/economic impact simulation"
keywords: ["power grid planning", "multi-voltage level", "planned substation evaluation", "grid evolution modeling", "analytic hierarchy process", "commissioning delay", "criticality assessment", "genetic algorithm", "incremental construction cost"]
claims_summary:
  - "Served-load magnitude is the dominant determinant of a planned substation's systemic criticality, far above topological connectivity counts."
  - "A composite AHP importance score linearly predicts the incremental multi-voltage construction cost caused by a substation's commissioning delay."
  - "Because delay cost rises with importance, a delay-sequencing rule that defers the least-critical substations bounds the induced cost."
  - "Commissioning-delay cost concentrates in and persists within the low-voltage (10 kV) layer across the full planning horizon."
  - "Local load density is the operative physical driver of the transfer/feeder cost incurred when a substation is delayed."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p6_nsga_bls_feasibility_review/p6_nsga_bls_feasibility_review__07__quantitative_evaluation_of_crucial_substations_and_simulatio__f316911d85.pdf"
abstract: "Rapidly expanding power demand in economically developing regions significantly amplifies the operational risks associated with the delayed commissioning of planned substations. This study proposes a data–physics fusion framework integrating analytic hierarchy process-based quantitative assessment with multi-voltage level grid evolution simulation. First, a novel set of evaluation indicators for assessing planned substation criticality, with weights determined through the analytic hierarchy process (AHP), was established, enabling rapid assessment of delay impacts on investments and identification of crucial substations. This approach addresses the fundamental limitation of traditional planning methodologies, which inadequately quantify the compound effects of substation commissioning delays on multi-voltage grid evolution and associated investment inefficiencies. Subsequently, a multi-voltage level grid evolution model was developed, which quantitatively measures the cascading effects of substation commissioning delays on both low-voltage grid development and multi-level grid construction investments. Case study validation demonstrated a strong linear correlation between the proposed substation importance scores and the incremental construction costs induced by delays. The simulation-driven impact assessment model exhibits superior accuracy in evaluating commissioning delay consequences on multi-voltage grid construction compared to conventional approaches. This research provides power grid planners with a robust decision support framework for optimizing substation construction scheduling and minimizing delay-related cost escalations in complex grid development scenarios."
---

# Quantitative Evaluation of Crucial Substations and Simulation-Driven Impact Assessment of Commissioning Delays in Multi-Voltage Grid Planning

## Overview

This paper couples two components into a "data–physics fusion" decision-support framework for multi-voltage grid planning. (1) A **quantitative criticality-scoring method** for newly planned substations: five topology/load indices (Eqs. 1–5) are combined via **AHP** weights (Table 3) into a composite importance score (Eq. 6) after sum-normalization (Eq. 7). (2) A **multi-voltage level grid evolution simulation** (220/110/10 kV, Eqs. 8–25) solved by a genetic algorithm that autonomously reconfigures topology, generating construction-investment trajectories across planning horizons (2020→2025→2035). By re-running the simulation with individual substation commissioning delayed by one horizon and differencing against a baseline, the framework quantifies the **incremental cost** each delay induces. A regional case study (220 equivalent load nodes; six new 110 kV substations) shows the AHP importance score is strongly, monotonically/linearly correlated with simulation-derived incremental cost, cross-validating the score without needing the expensive simulation for every candidate, and motivating a delay-sequencing rule that defers the least-critical substations.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable claims (C01–C05) |
| [concepts.md](logic/concepts.md) | 11 technical terms formally defined |
| [experiments.md](logic/experiments.md) | 5 declarative verification plans (E01–E05) |
| [related_work.md](logic/related_work.md) | Typed citation graph (RW01–RW19) |
| [solution/method.md](logic/solution/method.md) | Criticality metric + simulation-driven impact-assessment procedure |
| [solution/formulation.md](logic/solution/formulation.md) | Indices, objective, constraints (Eqs. 1–25) |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Data / software / GA config / protocols | C02, C04 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 18-node research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 7 tables + 7 figures |
| tables/table1–table7 | Santy scale, AHP matrix, weights, indicator values, scores, cost breakdown, score–cost comparison |
| figures/figure1–figure7 | Connection schemes, load map, grid-evolution panels, delay experiments, score–cost regression |
