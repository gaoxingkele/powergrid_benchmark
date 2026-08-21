---
title: "Bi-Objective Resilient Backbone-Grid Planning via a Three-Stage TER-NSGA-II Approach Considering Pumped-Storage Hub Effects"
authors:
  - "Jinxiu Ding"
  - "Qingfen Liao"
  - "Fei Tang"
  - "Bincheng Li"
  - "Yixin Yu"
  - "Tingyu Zhou"
year: 2026
venue: "Energies"
doi: "10.3390/en19122798"
ara_version: "1.0"
domain: "Power Systems, Grid Planning, Resilience, Multi-Objective Optimization"
keywords:
  - "pumped storage"
  - "backbone-grid planning"
  - "power system resilience"
  - "N-1 connectivity constraint"
  - "TER-NSGA-II"
  - "multi-objective optimization"
  - "edge connectivity"
  - "resilience mismatch index"
  - "capacity-weighted betweenness centrality"
  - "evolutionary algorithm"
claims_summary:
  - "C01: The proposed resilience mismatch index F2, coupling recovery-distance contribution and capacity-weighted betweenness centrality, provides an explicit quantification of pumped-storage resilience value in backbone-grid planning."
  - "C02: The TER-NSGA-II algorithm achieves 100% feasible-run rate on the IEEE 118-bus system, significantly outperforming standard NSGA-II (48.11%) under rigid connectivity, N-1 connectivity, and power flow safety constraints."
  - "C03: The three-stage hierarchical constraint-handling framework (connectivity construction, N-1 reinforcement, safety convergence) with max-flow min-cut validation ensures strict edge connectivity >= 2 while maintaining search efficiency."
  - "C04: The periodic reverse learning mechanism enhances global search capability by generating structurally diverse yet feasible candidate solutions, reducing the risk of premature convergence."
  - "C05: The proposed method achieves lower F1 (economy) and F2 (resilience) mean values compared to NSGA-II and NSGA-III/NG on both IEEE 118-bus and IEEE 300-bus systems."
  - "C06: The multiplicative surrogate form of the resilience mismatch index provides stronger discriminative capability for resilience differences compared to additive alternatives under severe perturbation scenarios."
abstract: "In the global transition toward low-carbon power systems with high renewable energy penetration, pumped storage has emerged as a strategic cornerstone for modern power grids. However, the collaborative planning of pumped storage and backbone-grids faces critical challenges, including the lack of explicit quantification of the resilience value of pumped storage and the coarse treatment of N-1 connectivity constraints. This paper proposes a bi-objective resilient backbone-grid planning approach that integrates the pumped-storage hub effect, aiming to minimize total life-cycle costs and the system resilience mismatch index. The proposed framework incorporates network connectivity, N-1 connectivity (edge connectivity >= 2), and dual-scenario power flow security as rigid constraints. Furthermore, a three-stage constrained evolutionary algorithm TER-NSGA-II is developed. During the N-1 connectivity reinforcement phase, the max-flow min-cut theorem is employed to achieve precise validation and guidance for edge-connectivity enhancement. Case studies on the IEEE 118-bus system, together with extended validation on the IEEE 300-bus system, show that the proposed method can explicitly quantify the resilience value of pumped storage, obtain Pareto solutions that balance economy and resilience under strict edge-connectivity constraints, and demonstrate competitive overall performance in terms of solution-set quality, feasible-domain search stability, and scalability compared with NSGA-II and the more recent NSGA-III/NG benchmark."
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p6_nsga_bls_feasibility_review/p6_nsga_bls_feasibility_review__03__bi_objective_resilient_backbone_grid_planning_via_a_three_st__90d73ce782.pdf"
---

# Overview

This paper addresses the bi-objective resilient backbone-grid planning problem integrating pumped-storage hub effects. The authors propose a three-stage constrained evolutionary algorithm (TER-NSGA-II) that hierarchically handles connectivity, N-1 connectivity (edge connectivity >= 2), and dual-scenario power flow security constraints. A novel system resilience mismatch index (F2) quantifies the resilience value of pumped storage by coupling recovery-distance contribution with capacity-weighted betweenness centrality. The approach is validated on the IEEE 118-bus system (main) and IEEE 300-bus system (scalability), demonstrating superior feasible-domain search capability and solution quality compared to NSGA-II and NSGA-III/NG.

## Layer Index

| File | Description |
|------|-------------|
| `PAPER.md` | This file: metadata, overview, and layer index |
| `logic/problem.md` | Problem statement: bi-objective resilient backbone-grid planning |
| `logic/claims.md` | All claims (C01-C06) with conditions, sources, status, falsification |
| `logic/concepts.md` | Key concepts: backbone grid, resilience mismatch index, TER-NSGA-II, edge connectivity, pumped-storage hub effect |
| `logic/experiments.md` | Experiments E01-E04: IEEE 118-bus main validation, parameter tuning, weighting scheme comparison, IEEE 300-bus scalability |
| `logic/related_work.md` | Analysis of related work and positioning |
| `logic/solution/constraints.md` | Hard constraints: connectivity, N-1 connectivity, power flow safety |
| `logic/solution/algorithm.md` | TER-NSGA-II algorithm description |
| `logic/solution/objective.md` | Objective functions: F1 (economic) and F2 (resilience mismatch) |
| `logic/solution/framework.md` | Three-stage optimization framework |
| `src/environment.md` | Experimental environment, test systems, and configuration |
| `trace/exploration_tree.yaml` | Exploration tree capturing the epistemic chain |
| `evidence/README.md` | Evidence inventory |
| `evidence/tables/table1.md` | Table 1: irace candidate parameter configurations |
| `evidence/tables/table1.png` | Table 1 rendered page |
| `evidence/tables/table2.md` | Table 2: Core-objective indicators on IEEE 118-bus |
| `evidence/tables/table2.png` | Table 2 rendered page |
| `evidence/tables/table3.md` | Table 3: Multi-objective performance metrics on IEEE 118-bus |
| `evidence/tables/table3.png` | Table 3 rendered page |
| `evidence/tables/table4.md` | Table 4: Performance comparison of aggregation forms |
| `evidence/tables/table4.png` | Table 4 rendered page |
| `evidence/tables/table5.md` | Table 5: Representative planning schemes |
| `evidence/tables/table5.png` | Table 5 rendered page |
| `evidence/tables/table6.md` | Table 6: Core-objective indicators on IEEE 300-bus |
| `evidence/tables/table6.png` | Table 6 rendered page |
| `evidence/tables/table7.md` | Table 7: Multi-objective metrics on IEEE 300-bus |
| `evidence/tables/table7.png` | Table 7 rendered page |
| `evidence/tables/table8.md` | Table 8: Computational performance comparison |
| `evidence/tables/table8.png` | Table 8 rendered page |
| `evidence/tables/tableA1.md` | Table A1: Relative degradation of surrogate indices |
| `evidence/tables/tableA1.png` | Table A1 rendered page |
| `evidence/tables/tableA2.md` | Table A2: Statistical results of F2 under different alpha values |
| `evidence/tables/tableA2.png` | Table A2 rendered page |
| `evidence/figures/figure1.md` | Figure 1: Reverse learning and connectivity repair |
| `evidence/figures/figure1.png` | Figure 1 rendered page |
| `evidence/figures/figure2.md` | Figure 2: TER-NSGA-II solution process flowchart |
| `evidence/figures/figure2.png` | Figure 2 rendered page |
| `evidence/figures/figure3.md` | Figure 3: Convergence curves on IEEE 118-bus |
| `evidence/figures/figure3.png` | Figure 3 rendered page |
| `evidence/figures/figure4.md` | Figure 4: Pareto fronts on IEEE 118-bus |
| `evidence/figures/figure4.png` | Figure 4 rendered page |
| `evidence/figures/figure5.md` | Figure 5: Topological configurations of backbone-grid schemes |
| `evidence/figures/figure5.png` | Figure 5 rendered page |
| `evidence/figures/figure6.md` | Figure 6: Pareto fronts on IEEE 300-bus |
| `evidence/figures/figure6.png` | Figure 6 rendered page |
