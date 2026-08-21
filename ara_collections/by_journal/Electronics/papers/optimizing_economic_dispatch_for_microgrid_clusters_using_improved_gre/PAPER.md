---
title: "Optimizing Economic Dispatch for Microgrid Clusters Using Improved Grey Wolf Optimization"
authors: ["Xinchen Wang", "Shaorong Wang", "Jiaxuan Ren", "Zhaoxia Song", "Shun Zhang", "Hupeng Feng"]
year: 2024
venue: "Electronics"
doi: "10.3390/electronics13163139"
ara_version: "1.0"
domain: "Power systems / microgrid economic dispatch; metaheuristic optimization"
keywords: ["microgrid cluster", "grey wolf optimization", "CDGWO", "chaotic mapping", "dynamic opposition-based learning", "economic dispatch", "multi-objective optimization", "energy storage", "time-of-use pricing", "robustness"]
claims_summary:
  - "Penalty terms decouple the optimizer's fitness from real cost while encoding power-quality/lifespan goals a cost-only objective cannot express."
  - "GWO's leader-averaging update trades exploitation for lost diversity, motivating a diversity-restoring operator."
  - "Choosing a chaotic init map is an accuracy-vs-cost trade-off; the cheaper map wins when the accuracy gap is negligible."
  - "Chaotic init and dynamic opposition-based learning act on complementary phases, so combining them gives joint speed/precision/stability gains."
  - "Iterations-to-converge is not a faithful proxy for a metaheuristic's runtime or solution quality."
  - "When better fitness carries through to lower real cost, the penalty-encoded objective is economically faithful."
  - "Hard power-balance/equipment/SOC constraints keep the economic solution feasible every interval."
  - "TOU price structure plus storage and inter-MG exchange drives temporal energy arbitrage in the dispatch."
  - "The penalty-structured multi-objective dispatch degrades gracefully under bounded forecast uncertainty."
abstract: "With the rapid development of renewable energy generation in recent years, microgrid technology has increasingly emerged as an effective means to facilitate the integration of renewable energy. To efficiently achieve optimal scheduling for microgrid cluster (MGC) systems while guaranteeing the safe and stable operation of a power grid, this study, drawing on actual electricity-consumption patterns and renewable energy generation in low-latitude coastal areas, proposes an integrated multi-objective coordinated optimization strategy. The objective function includes not only operational costs, environmental costs, and energy storage losses but also introduces penalty terms to comprehensively reflect the operation of the MGC system. To further enhance the efficiency of solving the economic dispatch model, this study combines chaotic mapping and dynamic opposition-based learning with the traditional Grey Wolf Optimization (GWO) algorithm, using the improved GWO (CDGWO) algorithm for optimization. Comparative experiments comprehensively validate the significant advantages of the proposed optimization algorithm in terms of economic benefits and scheduling efficiency. The results indicate that the proposed scheduling strategy, objective model, and solution algorithm can efficiently and effectively achieve multi-objective coordinated optimization scheduling for MGC systems, significantly enhancing the overall economic benefits of the MGC while ensuring a reliable power supply."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__09__optimizing_economic_dispatch_for_microgrid_clusters_using_improved_gre__31a69df1d7.pdf"
---

# Optimizing Economic Dispatch for Microgrid Clusters Using Improved Grey Wolf Optimization

## Overview
This paper tackles day-ahead economic dispatch for a three-microgrid cluster (MGC) coordinated by a
central Energy Management Center. It makes two contributions: (1) an enriched multi-objective dispatch
objective that adds an ESS loss cost and two penalty terms (main-grid/MGC power-exchange excursions;
ESS start/end energy discrepancy) on top of the usual operational and pollution costs, to jointly
express economics, power quality, and equipment longevity; and (2) an improved Grey Wolf Optimizer,
CDGWO, that adds chaotic-map population initialization and a dynamic opposition-based learning
operator (dynamic factor r = sin(t/T)) to the base GWO. A chaotic-map selection study picks the
Logistic map; CDGWO is then benchmarked against FA, PSO, WOA, GWO, GA, and SA, achieving the best
fitness, shortest runtime, and lowest convergence variance, and the lowest actual daily cost. A ±10%
disturbance study shows the dispatch maintains hourly power balance with only a modest cost rise,
evidencing robustness. Method is given as equations + a printed procedure; no code/data is released.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (O1-O4) → gaps (G1-G3) → key insight → assumptions |
| [claims.md](logic/claims.md) | 9 falsifiable claims (C01-C09) |
| [concepts.md](logic/concepts.md) | 11 technical terms (MGC, GWO, CDGWO, chaotic mapping, DOBL, penalties, ESS/SOC, TOU, convergence variance, …) |
| [experiments.md](logic/experiments.md) | 5 verification plans (E01-E05), directional only |
| [related_work.md](logic/related_work.md) | Typed dependency graph (7 full RW blocks + citation footprint) |
| [solution/formulation.md](logic/solution/formulation.md) | Economic-dispatch objective + constraint formulation (Eqs. 1-15) |
| [solution/algorithm.md](logic/solution/algorithm.md) | CDGWO: GWO base + chaos + DOBL, printed Steps 1-7 (Eqs. 16-20) |
| [solution/architecture.md](logic/solution/architecture.md) | MGC system structure + method flow (Figures 1, 4) |
| [solution/constraints.md](logic/solution/constraints.md) | Constraints, assumptions, and limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Data sources, horizon, protocols; notes no code/data released | — |

_No `src/execution/` code stub: the method is equation/prose-only with unspecified hyperparameters (ARA rule 14a)._

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 15-node research DAG (2 questions branch, decisions, experiments, 3 dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 10 tables + 10 figures (20 PNGs) |
| tables/table1-5, tableA1-A5 | 10 numbered tables (`.md` + `.png`) |
| figures/figure1-10 | 10 numbered figures (`.md` + `.png`) |
