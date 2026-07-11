# Six-Paper Planning Portfolio for Power Grid Benchmark Research

Date: 2026-07-11

Status: planning draft. These are manuscript concepts, not submitted papers.

## Journal Fit Principles

- **MDPI Energies**: best fit for energy dispatch, smart grids, microgrids, power systems, energy management, and AI in energy-system control. The journal explicitly expects full experimental detail for reproducibility and detailed numerical/simulation methods.
- **MDPI Applied Sciences**: best fit for applied engineering algorithm papers with reproducible experiments, software/supplementary material, and broad engineering framing.
- **MDPI Electronics**: best fit for AI, systems/control engineering, power electronics, electrical/autonomous vehicles, networks, and electronic/computing methods.
- **IEEE Access**: best fit for multidisciplinary, applications-oriented, technically correct engineering papers with clear experiments and reproducible methods.

Local evidence base:

- Public datasets: `data/public_datasets/manifests/public_dataset_manifest.csv`
- External literature map: `papers/literature/dataset_benchmark_papers/algorithm_task_map.md`
- External ARA collection: `ara_collections/dataset_benchmark_papers/`

## Portfolio Overview

| No. | Direction | Proposed Target | Dataset Basis | Core Method |
|---:|---|---|---|---|
| 1 | Twin-GRU power grid dispatch | IEEE Access / Electronics | RTS-GMLC, PGLib-OPF, MATPOWER, Grid2Op | Siamese/Twin GRU + dispatch optimization |
| 2 | Smart dispatch / load intelligence | Electronics / Applied Sciences | OPSD, SimBench, NSRDB, ENTSO-E metadata | Hyperbolic GCN + spatio-temporal forecasting |
| 3 | Distribution planning 1 | Energies / Applied Sciences | SimBench, pandapower, RTS-GMLC | Self-adaptive multi-objective differential evolution |
| 4 | Distribution planning 2 | Energies | SimBench, pandapower, MATPOWER | Resilience-aware hybrid multi-objective evolution |
| 5 | Feasibility review 1 | Energies / IEEE Access | RTS-GMLC, SimBench, NERC reports, semi-synthetic project portfolio | Hybrid multi-objective investment effectiveness optimization |
| 6 | Feasibility review 2 | Applied Sciences / IEEE Access | Same as No. 5 plus review-rule features | NSGA + bidirectional local search for review recommendation |

## Paper 1

### Title

Digital Twin-Driven Siamese GRU for Load-Aware Multi-Objective Power Grid Dispatch Optimization

### Target Journal

Primary: **IEEE Access**. Backup: **Electronics**.

### Planned Abstract

Reliable grid dispatch requires a model that can jointly represent temporal operating patterns and the similarity between current operating states and historically validated dispatch cases. This paper proposes a digital twin-driven Siamese GRU framework for load-aware multi-objective power grid dispatch optimization. The method constructs paired dispatch-state sequences from historical or simulated operating scenarios and uses a twin GRU encoder to learn state similarity, operating-risk proximity, and dispatch-transferability. The learned representation is coupled with a multi-objective dispatch layer that balances generation cost, renewable accommodation, reserve adequacy, and operational security constraints. Experiments will be built on RTS-GMLC, MATPOWER/PGLib-OPF cases, and Grid2Op-style topology-control scenarios. Baselines will include conventional GRU/LSTM forecasting, static OPF/UC dispatch, and reinforcement-learning dispatch agents where applicable. The expected contribution is a dispatch framework that connects digital-twin state retrieval with temporal neural modeling and optimization-based decision making, enabling more robust dispatch recommendations under load fluctuation and renewable uncertainty.

### Experiment Plan

- Tasks: load-aware dispatch, UC/OPF scenario recommendation, N-1 or topology-risk-aware dispatch.
- Baselines: GRU, LSTM, CNN-LSTM, OPF/UC without learned state retrieval, Grid2Op RL baselines where feasible.
- Metrics: total dispatch cost, renewable curtailment, constraint violation rate, reserve shortage, runtime, robustness under perturbed load.

## Paper 2

### Title

Graph Convolutional Network Based on Hyperbolic Space for Power Load Forecasting in Smart Dispatch Systems

### Target Journal

Primary: **Electronics**. Backup: **Applied Sciences**.

### Planned Abstract

Accurate load forecasting is a core prerequisite for smart dispatch, yet conventional Euclidean graph neural networks may inadequately represent hierarchical grid structures and multi-scale spatial dependencies. This paper proposes a hyperbolic-space graph convolutional network for power load forecasting in smart dispatch systems. The approach embeds substations, feeders, regional loads, and weather-related exogenous variables into a hyperbolic latent space, where tree-like and hierarchical electrical relationships can be represented with lower distortion. A temporal forecasting module then fuses hyperbolic graph features with historical load sequences to produce day-ahead and short-term load predictions. Experiments will use Open Power System Data, SimBench time-series profiles, NSRDB weather/irradiance features, and available ENTSO-E/PJM-style load metadata when access permits. The model will be compared with ARIMA, XGBoost, LSTM, TCN, Euclidean GCN, and Transformer-based forecasting baselines. The study aims to demonstrate that hyperbolic graph representation can improve spatial generalization and provide a stronger forecasting foundation for downstream dispatch and planning workflows.

### Experiment Plan

- Tasks: day-ahead load forecasting, regional/feeder-level load forecasting, weather-aware forecasting.
- Baselines: LSTM, BiLSTM, TCN, Transformer, Euclidean GCN, XGBoost.
- Metrics: MAE, RMSE, MAPE/sMAPE, peak-load error, spatial transfer error.

## Paper 3

### Title

Power Distribution Network Planning Strategy Optimization Based on a Self-Adaptive Multi-Objective Differential Evolution Algorithm

### Target Journal

Primary: **Energies**. Backup: **Applied Sciences**.

### Planned Abstract

Distribution network planning must balance investment cost, reliability, voltage quality, renewable integration, and operational flexibility under uncertain load and distributed energy resources. This paper proposes a self-adaptive multi-objective differential evolution algorithm for distribution network planning strategy optimization. The algorithm adaptively adjusts mutation, crossover, and selection parameters according to population diversity, Pareto-front convergence, and constraint violation patterns. Candidate planning strategies include feeder reinforcement, distributed generation siting, storage allocation, and topology adjustment. SimBench and pandapower distribution networks will be used as reproducible benchmark systems, with additional MATPOWER or RTS-GMLC cases used for transmission-distribution consistency checks when appropriate. The method will be compared with NSGA-II, MOEA/D, standard differential evolution, particle swarm optimization, and rule-based planning heuristics. The expected contribution is a reproducible planning optimizer that improves Pareto-front quality and constraint satisfaction while maintaining computational feasibility for realistic distribution-network scenarios.

### Experiment Plan

- Tasks: distribution expansion planning, DER/storage siting, voltage/security constrained planning.
- Baselines: NSGA-II, MOEA/D, standard DE, PSO, heuristic planning.
- Metrics: investment cost, energy loss, voltage deviation, reliability proxy, renewable hosting capacity, hypervolume, IGD, runtime.

## Paper 4

### Title

Resilience-Oriented Distribution Network Planning with Hybrid Multi-Objective Evolution and Scenario-Based DER Uncertainty

### Target Journal

Primary: **Energies**.

### Planned Abstract

The increasing penetration of distributed renewable energy resources makes distribution network planning a resilience-oriented and uncertainty-aware optimization problem. This paper develops a hybrid multi-objective evolutionary framework for distribution network planning under scenario-based load, renewable, and outage uncertainty. The proposed framework combines global evolutionary search with local repair and scenario screening to optimize investment cost, expected energy loss, voltage-security performance, renewable hosting capacity, and resilience under contingency scenarios. SimBench and pandapower networks provide distribution test systems, while RTS-GMLC and public renewable/weather datasets provide scenario templates for renewable and demand uncertainty. Compared with single-scenario planning and standard multi-objective evolutionary algorithms, the proposed approach is intended to produce planning portfolios that remain feasible across a wider operating envelope. The contribution is a practical planning strategy that links public grid benchmarks, uncertainty scenario generation, and resilience-aware multi-objective optimization in a reproducible experimental package.

### Experiment Plan

- Tasks: resilience-aware distribution planning, DER hosting capacity planning, scenario-based outage planning.
- Baselines: deterministic planning, NSGA-II, MOEA/D, hybrid evolutionary algorithm without local repair.
- Metrics: Pareto hypervolume, expected loss, voltage violation probability, contingency survivability, investment efficiency.

## Paper 5

### Title

Investment Effectiveness Optimization Strategy Based on Hybrid Multi-Objective Evolution for Power Grid Feasibility Review

### Target Journal

Primary: **IEEE Access**. Backup: **Energies**.

### Planned Abstract

Power grid feasibility review requires systematic evaluation of investment effectiveness, technical necessity, reliability benefit, and risk exposure before project approval. This paper proposes a hybrid multi-objective evolutionary optimization strategy for investment effectiveness assessment in power grid feasibility review. The framework converts candidate grid projects into a portfolio optimization problem with objectives including cost efficiency, reliability improvement, load-growth support, renewable accommodation, and implementation risk. Public benchmark systems such as RTS-GMLC, SimBench, MATPOWER, and NERC reliability reports will be used to construct reproducible semi-synthetic project portfolios, while private enterprise data can be incorporated later under the same feature schema. A hybrid evolutionary optimizer will combine global Pareto search with feasibility-rule repair and decision preference modeling. The method will be compared with weighted scoring, TOPSIS/AHP-style multi-criteria evaluation, NSGA-II, and standard evolutionary search. The expected contribution is a transparent and reproducible feasibility-review decision framework that supports investment prioritization rather than relying only on static expert scoring.

### Experiment Plan

- Tasks: project portfolio ranking, investment effectiveness evaluation, feasibility-review recommendation.
- Data: benchmark-derived semi-synthetic project portfolios; optional internal project records later.
- Baselines: expert scoring rules, AHP/TOPSIS, NSGA-II, MOEA/D, weighted-sum optimization.
- Metrics: Pareto quality, ranking stability, budget-feasibility, reliability-benefit per investment, decision consistency.

## Paper 6

### Title

A Non-Dominated Sorting and Bidirectional Local Search Multi-Objective Evolution Algorithm for Investment Effectiveness Review of Power Grid Projects

### Target Journal

Primary: **Applied Sciences**. Backup: **IEEE Access**.

### Planned Abstract

Investment effectiveness review for power grid projects is a constrained multi-objective decision problem involving economic return, grid reliability, load-growth support, renewable integration, schedule risk, and policy compliance. This paper proposes a non-dominated sorting multi-objective evolutionary algorithm enhanced by bidirectional local search for power grid project review. The forward local search improves promising investment portfolios by adding or strengthening high-benefit projects, while the backward local search removes low-effectiveness or constraint-violating project components. Non-dominated sorting maintains diverse trade-off solutions for decision makers under budget, reliability, and schedule constraints. Reproducible experiments will be constructed from public grid benchmarks, distribution planning cases, reliability report features, and semi-synthetic investment portfolios. The proposed method will be compared with NSGA-II, NSGA-III, MOEA/D, greedy budget allocation, and rule-based feasibility scoring. The expected outcome is an interpretable optimization framework that can support feasibility-review recommendations, sensitivity analysis, and project-priority explanation.

### Experiment Plan

- Tasks: project prioritization, budget-constrained review, sensitivity analysis, investment portfolio optimization.
- Baselines: NSGA-II, NSGA-III, MOEA/D, greedy allocation, rule-based review.
- Metrics: hypervolume, spacing, constraint violation, ranking robustness, review explanation consistency.

## Shared Experimental Standards

1. Every paper should provide a reproducible benchmark package: dataset manifest, preprocessing scripts, configuration files, random seeds, and result tables.
2. For MDPI submissions, include full experimental details and supplementary software where possible.
3. For IEEE Access, emphasize technical correctness, application-oriented engineering value, and clear experimental validation.
4. Avoid claiming real project-review effectiveness unless enterprise project data are actually available; otherwise label experiments as benchmark-derived or semi-synthetic.
5. Separate public benchmark experiments from confidential enterprise validation.

## Suggested Submission Allocation

| Paper | Best first target | Reason |
|---|---|---|
| Twin-GRU dispatch | IEEE Access | Crosses digital twin, neural sequence modeling, and dispatch optimization. |
| Hyperbolic GCN load forecasting | Electronics | AI/network/control fit; strong electronics and computing method angle. |
| Self-adaptive MODE distribution planning | Energies | Direct smart-grid/distribution planning fit. |
| Resilience-oriented planning | Energies | Energy systems, DER, resilience, planning fit. |
| Hybrid MOEA feasibility review | IEEE Access | Application-oriented cross-disciplinary review/optimization system. |
| NSGA + bidirectional local search review | Applied Sciences | Applied engineering algorithm paper with reproducible benchmarks. |
