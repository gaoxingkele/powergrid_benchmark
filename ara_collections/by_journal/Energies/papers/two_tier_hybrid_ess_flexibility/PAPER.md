---
title: "A Two-Tier Planning Approach for Hybrid Energy Storage Systems Considering Grid Power Flexibility in New Energy High-Penetration Grids"
authors:
  - "Wei Huang"
  - "Dongbo Qu"
  - "Chen Wu"
  - "Kai Hu"
  - "Tao Qiu"
  - "Weidong Wei"
  - "Guanhui Yin"
  - "Xianguang Jia"
year: 2025
venue: "Energies"
doi: "10.3390/en18184986"
ara_version: "1.0"
domain: "Energy Storage, Power Systems, Grid Flexibility"
keywords:
  - "Bi-level optimization"
  - "Hybrid energy storage system (HESS)"
  - "Renewable energy integration"
  - "Variational Mode Decomposition (VMD)"
  - "Particle Swarm Optimization (PSO)"
  - "Improved Weighted Average Algorithm (IWAA)"
  - "Flow battery"
  - "Lithium-ion battery"
  - "Power flexibility"
  - "Multi-objective optimization"
claims_summary:
  - "A bi-level HESS planning model integrating upper-level siting/sizing with lower-level operational optimization is proposed."
  - "PSO-VMD adaptively determines VMD parameters (K, alpha) eliminating subjectivity in frequency-based power allocation."
  - "IWAA incorporates refraction opposition-based learning and dynamic crowding distance to enhance global search and maintain Pareto diversity."
  - "Multi-node coordinated HESS deployment outperforms single-node hybrid configurations across economic and stability metrics."
  - "Validation on a modified IEEE 39-bus system with real Southwest China grid data shows significant improvements over five comparative schemes."
abstract: "This paper proposes a flow battery-lithium-ion battery hybrid energy storage system (HESS) bi-level optimization planning method to address flexibility supply-demand balance challenges in regional power grids with high renewable penetration at 220 kV and above voltage levels. The method establishes a planning-operation coordination framework: Upper-level planning minimizes total lifecycle investment and operation-maintenance costs; Lower-level operation incorporates multiple constraints including flexibility gap penalties, voltage fluctuations, and line losses, overcoming single-timescale limitations. The approach enhances global search capability through the Improved Weighted Average Algorithm (IWAA) and optimizes power allocation accuracy using adaptive Variational Mode Decomposition (VMD). Validation using grid data from Southwest China demonstrates significant improvements across five comparative schemes. Results show substantial reductions in total investment costs, penalty costs, voltage fluctuations, and line losses compared to benchmark solutions, enhancing grid power supply stability and verifying the effectiveness of the model and algorithm."
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p6_nsga_bls_feasibility_review/p6_nsga_bls_feasibility_review__05__a_two_tier_planning_approach_for_hybrid_energy_storage_syste__0e00a23b09.pdf"
---

# Overview

This paper presents a **bi-level (two-tier) optimization planning method** for Hybrid Energy Storage Systems (HESS) composed of flow batteries (long-duration) and lithium-ion batteries (short-duration) in regional power grids with high penetration of renewable energy (wind and solar photovoltaic). The work addresses the flexibility supply-demand balance challenge in power grids at the 220 kV and above voltage levels.

## Core Contributions

1. **Bi-Level Optimization Model for Multi-Timescale HESS Planning**: An upper-level planning and lower-level operation collaborative model integrating HESS siting, sizing, and multi-timescale power allocation. The upper level optimizes investment and O&M costs; the lower level incorporates flexibility gap penalties, voltage fluctuation, and line loss constraints.

2. **PSO-VMD Power Allocation Method**: An adaptive Variational Mode Decomposition method integrated with Particle Swarm Optimization that eliminates subjectivity in frequency division key parameter selection (mode number K and penalty factor alpha) and uses a median spectrum threshold for precise separation of high/low-frequency components.

3. **Improved Weighted Average Algorithm (IWAA)**: Enhances the standard WAA via Refraction Opposition-based Learning (improving exploration phase escape from local optima) and Dynamic Crowding Distance (sequential removal method for maintaining Pareto solution diversity).

4. **Comprehensive Validation**: Five comparative schemes and five algorithm comparisons (COOT, PSO, DE, WAA, IWAA) on a modified IEEE 39-bus system using real operational data from a regional grid in Southwest China.

## Layer Index

| Layer | File | Description |
|-------|------|-------------|
| Problem | `logic/problem.md` | Problem formulation: flexibility supply-demand imbalance in high-renewable penetration grids |
| Claims | `logic/claims.md` | Central claims and contributions of the paper |
| Concepts | `logic/concepts.md` | Key concepts: HESS, VMD, WAA, bi-level optimization, flexibility metrics |
| Experiments | `logic/experiments.md` | Experimental setup, case studies, comparative schemes, and results |
| Related Work | `logic/related_work.md` | Related literature and positioning of this work |
| Solution Constraints | `logic/solution/constraints.md` | Mathematical constraints of the optimization model |
| Solution Algorithm | `logic/solution/algorithm.md` | IWAA detailed algorithm description |
| Solution Architecture | `logic/solution/architecture.md` | Bi-level optimization architecture |
| Solution Method | `logic/solution/method.md` | VMD-PSO power allocation method |
| Environment | `src/environment.md` | Computational environment and implementation details |
| Exploration Tree | `trace/exploration_tree.yaml` | Decision tree of the research |