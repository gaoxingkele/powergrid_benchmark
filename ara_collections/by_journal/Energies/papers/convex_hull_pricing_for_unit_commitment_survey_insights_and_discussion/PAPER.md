---
title: "Convex Hull Pricing for Unit Commitment: Survey, Insights, and Discussions"
authors: ["Farhan Hyder", "Bing Yan", "Mikhail Bragin", "Peter Luh"]
year: 2024
venue: "Energies"
doi: "10.3390/en17194851"
ara_version: "1.0"
domain: "Electricity market pricing, unit commitment, convex optimization"
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__11__convex_hull_pricing_for_unit_commitment_survey_insights_and_discussion__af00d128c1.pdf"
keywords: ["electricity markets", "uplift payments", "convex hull pricing", "unit commitment", "Lagrangian duality", "non-smooth optimization", "surrogate Lagrangian relaxation", "convex envelope", "decarbonization", "survey"]
claims_summary:
  - "Convexification restores price monotonicity that discreteness destroys, because the slope of a convex envelope is non-decreasing in demand."
  - "Excluding a cost category from the price signal forces opaque side payments, converting a pricing problem into a transparency problem."
  - "The primal and dual routes to convex hull prices compute the same object via strong duality and conjugate-function additivity."
  - "Convex hull prices are properties of the formulation, not just the feasible set; formulation tightening changes the priced object."
  - "Integer relaxation delivers the convex envelope exactly when cost convexity survives domain convexification."
  - "Formulation tightness is the single property deciding whether relaxation suffices; tight formulations are network-flow representable."
  - "Status enumeration buys generality by linearizing cost, and pays in constraint count."
  - "Few-slot exact hulls parameterize into scalable approximate hulls, trading exactness for a controlled constraint budget."
  - "Dual-route difficulty is non-smoothness; every remedy relocates the cost rather than removing it."
  - "Surrogate Lagrangian Relaxation resolves dual convergence by replacing exact subproblem optimality with a surrogate condition."
  - "Decarbonization moves UC outside the regime current convex hull pricing covers, with new binary variables and renewable uncertainty."
abstract: "Energy prices are usually determined by the marginal costs obtained by solving economic dispatch problems without considering commitment costs. Hence, generating units are compensated through uplift payments. However, uplift payments may undermine market transparency as they are not publicly disclosed. Alternatively, energy prices can be obtained from the unit commitment problem which considers commitment costs. But, due to non-convexity, prices may not monotonically increase with demand. To resolve this issue, convex hull pricing has been introduced. It is defined as the slope of the convex envelope of the total cost function over the convex hull of a unit commitment (UC) problem. Although several approaches have been developed, a relevant survey has not been found to aid the understanding of convex hull pricing from the current limited literature. This paper provides a systematic survey of convex hull pricing. It reviews, compares, and links various existing approaches, focusing on the modeling and computation of convex hull prices. Furthermore, this paper explores potential areas of improvement and future challenges due to the ongoing efforts for power system decarbonization."
---

# Convex Hull Pricing for Unit Commitment: Survey, Insights, and Discussions

## Overview

This survey paper organizes the 27-paper convex hull pricing (CHP) literature for unit commitment (UC) into a unified modeling taxonomy. It identifies two major approach categories: (1) solving the convexified UC problem (the "primal" route, requiring explicit convex-envelope and convex-hull formulations per unit) and (2) solving the Lagrangian dual of the original UC problem (the "dual" route, whose optimal multipliers equal the convex hull prices). The survey compares primal methods across three tightness cases (tight formulations where integer relaxation suffices; non-tight formulations requiring explicit hull construction; and approximate hulls as a compromise) and dual methods across four convergence-remedy families (subgradient, subdifferential, level, and Surrogate Lagrangian Relaxation). It concludes with remaining limitations and decarbonization-driven open challenges.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (O1–O5) \(\rightarrow\) gaps (G1–G4) \(\rightarrow\) key insight \(\rightarrow\) assumptions |
| [claims.md](logic/claims.md) | 11 falsifiable claims (C01–C11) synthesizing the surveyed literature |
| [concepts.md](logic/concepts.md) | 14 key technical terms formally defined |
| [experiments.md](logic/experiments.md) | 6 declarative verification/analysis plans (E01–E06) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the surveyed literature |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, and limitations of the survey scope |
| [solution/uc_formulation.md](logic/solution/uc_formulation.md) | Mathematical formulation of the UC problem (Eqs. 1–14) |
| [solution/dual_approaches.md](logic/solution/dual_approaches.md) | Lagrangian dual, subgradient, subdifferential, level, and SLR methods |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Analytical survey; no code or runtime environment | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 12-node research DAG covering the survey's organizing logic |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 0 tables + 9 figures (each markdown + PNG) |
