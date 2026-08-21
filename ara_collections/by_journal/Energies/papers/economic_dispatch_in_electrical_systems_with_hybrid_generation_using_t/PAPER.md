---
title: "Economic Dispatch in Electrical Systems with Hybrid Generation Using the Differential Evolution Algorithm: A Comparative Analysis with Other Optimization Techniques Under Energy Limitation Scenarios"
authors:
  - Jorge Cadena-Albuja
  - Carlos Barrera-Singaña
  - Hugo Arcos
  - Jorge Muñoz
year: 2025
venue: "Energies"
doi: "10.3390/en18133414"
ara_version: "1.0"
domain: "Power Systems Optimization, Economic Dispatch, Metaheuristic Algorithms"
keywords:
  - economic dispatch
  - hybrid generation
  - Monte Carlo
  - heuristic
  - metaheuristic
  - Differential Evolution
  - Particle Swarm Optimization
  - Cultural Algorithm
  - Grey Wolf Optimizer
claims_summary: "This paper demonstrates that the Differential Evolution (DE) algorithm achieves the lowest operating cost for short-term economic dispatch in hybrid generation systems under energy limitation scenarios, outperforming Particle Swarm Optimization (PSO), Cultural Algorithm (CA), and Grey Wolf Optimizer (GWO). DE achieved a 12.5% cost reduction compared to PSO in the drought scenario, with cost variation below 3% across 100 Monte Carlo iterations."
abstract: "This study focuses on the challenge of short-term economic dispatch in hybrid generation systems, specifically under scenarios where energy constraints arise due to reduced water availability. The primary aim is to compare various generation scenarios to evaluate the influence of renewable energy-based power plants on the overall operating cost of an Electric Power System. The hybrid generation system under analysis comprises hydroelectric, thermoelectric, photovoltaic solar, and wind power plants. The latter two, in particular, play a crucial role, yet their performance is highly dependent on the variability of their primary resources—solar radiation, wind speed, and ambient temperature—which are inherently stochastic. To estimate their behavior, the Monte Carlo method is applied, utilizing probability distribution functions to predict resource availability throughout the planning horizon. Once the scenarios are established, the problem is formulated as a hydrothermal dispatch optimization, which is then tackled using heuristic and metaheuristic approaches, with a strong focus on the Differential Evolution algorithm."
collection: "by_journal"
journal: "Energies"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "D:\\aicoding\\powergrid_benchmark\\papers\\literature\\target_journal_related\\pdfs\\p3_self_adaptive_mode_distribution_planning\\p3_self_adaptive_mode_distribution_planning__12__economic_dispatch_in_electrical_systems_with_hy__5ceb7551a4.pdf"
---

# Layer Index

## Layer 1: Environment
- src/environment.md — computational environment (MATLAB R2020b, Intel Core i7-1365U, 16GB RAM)

## Layer 2: Problem
- logic/problem.md — short-term economic dispatch in hybrid generation systems under energy constraints
- logic/solution/constraints.md — power balance, generation limits, water discharge, reservoir volume constraints

## Layer 3: Concepts
- logic/concepts.md — economic dispatch, hybrid generation, Monte Carlo simulation, metaheuristic optimization

## Layer 4: Related Work
- logic/related_work.md — comparative context with PSO, GSA, GPM, MILP, convex optimization, metaheuristic variants

## Layer 5: Claims
- logic/claims.md — claims with proof referencing experiment IDs

## Layer 6: Experiments
- logic/experiments.md — two scenarios (drought and high water availability), four algorithms compared

## Layer 7: Evidence
- evidence/README.md — index of all evidence artifacts
- evidence/figures/ — rendered PNGs for all 16 numbered figures
- evidence/tables/ — rendered PNGs for all 13 numbered tables
