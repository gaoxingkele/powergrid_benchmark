---
title: "Distribution Network Optimization and Flexibility Enhancement Based on Power Grid Equipment Maintenance"
authors:
  - "Runquan He"
  - "Manlu Chen"
  - "Renli Yang"
  - "Fei Chen"
year: 2025
venue: "Energies"
doi: "10.3390/en18184833"
ara_version: 1.0
domain: "Power Systems, Distribution Network Optimization"
keywords:
  - "two-layer optimization framework"
  - "distributed robust dispatch"
  - "Monte Carlo scenarios"
  - "renewable generation uncertainty"
  - "branch flexibility adequacy"
  - "grid reconfiguration"
  - "ant colony optimization"
  - "fire hawk optimization"
  - "differential evolution"
claims_summary: "Integrating flexibility adequacy index with grid reconfiguration in a two-layer optimization framework reduces flexibility deficits, renewable curtailment, and total operational cost under renewable uncertainty compared to deterministic, stochastic, and traditional robust methods."
abstract: "With increasing integration of renewable energy, traditional distribution networks face challenges such as low flexibility, poor response speed, and operational inefficiency. To address these issues, this paper proposes a two-layer optimization framework for active distribution networks that integrates grid reconfiguration and equipment maintenance considerations. The upper layer optimizes the network topology and branch flexibility using a flexibility adequacy index and power loss minimization. The lower layer performs distributed robust dispatch under renewable generation uncertainty. A hybrid algorithm combining Ant Colony Optimization (ACO), Fire Hawk Optimization (FHO), and Differential Evolution (DE) is developed to solve the model efficiently. Simulation is conducted on a modified 62-node test system. Comparative results with deterministic, stochastic, and robust models show that the proposed approach achieves the lowest average cost and maximum cost under 500 Monte Carlo scenarios. It also significantly reduces flexibility deficits and renewable curtailment. In addition, the model contributes to predictive maintenance by identifying optimal switching strategies and branch stress levels. These findings demonstrate the method's effectiveness in improving economic efficiency, system flexibility, and equipment sustainability."
collection: "by_journal"
journal: "Energies"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p4_resilience_distribution_planning/p4_resilience_distribution_planning__09__distribution_network_optimization_and_flexibility_enhan__b694db46c3.pdf"
---

## Overview

This paper proposes a two-layer optimization framework for active distribution networks that integrates grid reconfiguration with equipment maintenance considerations. The upper layer optimizes network topology based on a branch flexibility adequacy index (FBF) and power loss minimization. The lower layer performs distributionally robust dispatch (DRO) under renewable generation uncertainty using a comprehensive norm ambiguity set. A hybrid metaheuristic algorithm combining Ant Colony Optimization (ACO), Fire Hawk Optimization (FHO), and Differential Evolution (DE) is developed, with Tent chaos mapping for population initialization and adaptive weight mechanisms. The model is validated on a modified CPS62-node test system representing a real-world medium-voltage grid in China. Three schemes are compared: (1) no flexibility index or grid interconnection, (2) flexibility index without interconnection, (3) both flexibility index and interconnection. The proposed DRO approach is also compared against deterministic, stochastic, and traditional robust optimization models under 500 Monte Carlo scenarios. Results show Scheme 3 achieves the lowest comprehensive cost (3.6686 CNY 10,000) and flexibility deficit cost (0.0184 CNY 10,000). The DRO framework achieves lower average and maximum cost than all comparative methods, and the hybrid ACO-FHO-DE algorithm efficiently solves the two-layer model.

## Layer Index

| Layer | File | Description |
|-------|------|-------------|
| Paper metadata | PAPER.md | This file |
| Problem | logic/problem.md | Observations, Gaps, Key Insight, Assumptions |
| Claims | logic/claims.md | Falsifiable claims with evidence traces |
| Concepts | logic/concepts.md | Technical terms with definitions and boundary conditions |
| Experiments | logic/experiments.md | Analysis blocks with setup, metrics, expected outcomes |
| Constraints | logic/solution/constraints.md | Boundary conditions and limitations |
| Related work | logic/related_work.md | Typed citation dependency graph |
| Environment | src/environment.md | Language, runtime, hardware, data sources |
| Exploration tree | trace/exploration_tree.yaml | Research DAG |
| Evidence index | evidence/README.md | Table/figure index |
