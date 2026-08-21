---
title: "A Hybrid Heuristic–Benders Method for Wind–Hydrogen Investment Planning with Non-Analytical Cost Functions"
authors:
  - Haozhe Xiong
  - Bingyang Feng
  - Fangbin Yan
  - Yiqun Kang
  - Yuxuan Hu
  - Qiangsheng Li
  - Qinyue Tan
year: 2026
venue: Energies
doi: "10.3390/en19092172"
ara_version: 1
domain: power_systems
keywords:
  - wind-hydrogen integrated energy system
  - two-stage stochastic programming
  - Benders decomposition
  - black-box optimization
  - investment planning
  - metaheuristic
claims_summary: >
  This paper proposes a hybrid heuristic–Benders decomposition framework (GSOA-Benders) for two-stage stochastic
  investment planning of wind-hydrogen integrated energy systems where the first-stage hydrogen-storage investment
  cost may be a black-box non-analytical function while the second-stage operational recourse is linear. The method
  couples the General Soldiers Optimization Algorithm (GSOA) for derivative-free first-stage search with Benders
  cuts generated from linear programming subproblems. On a 500-scenario black-box test case, GSOA-Benders converges
  in 35.86s and finds investment plan x = [1, 0.53, 23.23, 0] (wind farm, 0.53 MW electrolyzer, 23.23 MWh hydrogen
  tank, no fuel cell). A stability gap is defined as the convergence metric, acknowledging that global optimality
  cannot be certified for the non-convex black-box master problem.
abstract: >
  This paper studies capacity planning for a wind-hydrogen integrated energy system under scenario-based uncertainty
  in wind generation, hydrogen demand, and electricity prices. The model is formulated as a two-stage stochastic
  program in which first-stage investment decisions are selected before uncertainty is realized and second-stage
  hourly operation is optimized for each representative scenario. The main methodological difficulty is that part
  of the first-stage hydrogen-storage investment cost may be available only through a non-analytical evaluator,
  such as supplier quotation logic, simulation software, or a data-driven estimator, while the operational recourse
  model remains linear. To address this setting, a hybrid heuristic-Benders framework, denoted as GSOA-Benders,
  is developed by coupling the General-Soldiers Optimization Algorithm for derivative-free first-stage search
  with Benders cuts generated from linear programming subproblems. The framework is not presented as a replacement
  for commercial solvers on explicit convex or mixed-integer models; rather, it is intended for cases where exact
  algebraic reformulation of the first-stage cost is unreliable or unavailable. In the black-box case study with 500
  scenarios, the method converges in 35.86 s and obtains an investment plan expressed as x = [1, 0.53, 23.23, 0],
  corresponding to wind-farm construction, a 0.53 MW electrolyzer, a 23.23 MWh hydrogen tank, and no fuel-cell
  investment. Additional discussion is provided on stability-gap interpretation, benchmark limitations, component
  lifetime assumptions, hydrogen losses, and environmental extensions.
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/pdfs/p5_hybrid_moea_feasibility_review/p5_hybrid_moea_feasibility_review__08__a_hybrid_heuristic_benders_method_for_wind_hydrogen_inves__da1f9c84c8.pdf"
---

## Layer Index

### Layer 1: Problem Statement
- [logic/problem.md](logic/problem.md) — Two-stage stochastic investment planning for WH-IES with black-box first-stage costs and linear recourse.

### Layer 2: Solution Logic
- [logic/claims.md](logic/claims.md) — 8 claims covering method positioning, algorithm properties, benchmark comparisons, and limitations.
- [logic/concepts.md](logic/concepts.md) — 12 technical concepts including WH-IES, GSOA, Benders decomposition, stability gap, non-analytical cost functions.
- [logic/experiments.md](logic/experiments.md) — 3 experiments: explicit non-convex baseline, black-box comparison, sensitivity/scalability analysis.
- [logic/related_work.md](logic/related_work.md) — Situates the work among stochastic/robust planning, MILP reformulation, heuristic optimization, and C&CG methods.
- [logic/solution/constraints.md](logic/solution/constraints.md) — Model constraints: power balance, hydrogen mass balance, investment capacity bounds, cyclic storage boundary.

### Layer 3: Implementation Context
- [src/environment.md](src/environment.md) — MATLAB R2023b, Gurobi 12.0.3, Intel i5-12490F, 16GB RAM.

### Layer 4: Exploration Trace
- [trace/exploration_tree.yaml](trace/exploration_tree.yaml) — 11-node YAML exploration tree covering problem decomposition, algorithm design, benchmark evaluation, and reviewer-driven refinements.

### Layer 5: Evidence
- [evidence/README.md](evidence/README.md) — Evidence inventory.
- [evidence/figures/](evidence/figures/) — PNG renderings of all 7 figures.
- [evidence/tables/](evidence/tables/) — PNG renderings of all 3 tables.
