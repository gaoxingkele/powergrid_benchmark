# Six-Paper ARA-Core Replanning Portfolio

Date: 2026-07-11

Status: planning revision based on local ARA comparator collection.

Evidence base:

- Target-journal comparator set: `papers/literature/target_journal_related/comparison_analysis.md`
- Comparator ARAs: `ara_collections/target_journal_related/`
- Public dataset manifest: `data/public_datasets/manifests/public_dataset_manifest.csv`
- Previous planning draft: `papers/planning/2026_six_paper_portfolio.md`

Journal constraints used:

- MDPI Energies, Applied Sciences, and Electronics instructions require enough experimental detail for reproducibility and encourage full dataset availability where possible.
- IEEE Access submission guidance requires a complete submission package and recommends concise manuscripts, with supplementary material used for extra content.

## Portfolio-Level Replanning Logic

The 67-paper comparator ARA collection shows that recent target-journal papers are already strong in PSO/GWO/WOA/GA/NSGA-II/DE dispatch and planning, CNN-LSTM/TCN/BiLSTM/Transformer/GCN forecasting, stochastic MILP, resilience restoration, and grid-investment risk-benefit optimization. The six planned papers therefore should avoid generic "improved optimizer" claims. Each paper should instead be positioned around a verifiable ARA kernel:

1. A clearly defined downstream task.
2. A public benchmark or benchmark-derived dataset.
3. A reproducible method with traceable configs.
4. Multiple baseline families, not only one algorithm family.
5. Ablations that isolate the claimed novelty.
6. Evidence tables that support each claim.

## Paper 1

### Recommended Title

Digital-Twin Siamese GRU for Similarity-Aware Multi-Objective Power Grid Dispatch under Load and Topology Uncertainty

### Target Journal

Primary: IEEE Access. Backup: Electronics.

Rationale: The topic combines neural temporal modeling, digital-twin state retrieval, dispatch optimization, and topology/security operation. IEEE Access is the stronger first target if the validation package is broad; Electronics is suitable if the manuscript emphasizes AI/control implementation.

### Abstract

Power grid dispatch increasingly requires decision support that can transfer validated operating experience from historical or simulated states to new load and topology conditions. Existing dispatch studies in the target-journal literature are dominated by direct heuristic optimization, conventional unit commitment, and sequence predictors that do not explicitly model similarity between current and previously validated operating states. This paper proposes a digital-twin Siamese GRU framework for similarity-aware multi-objective power grid dispatch. The framework constructs paired operating-state sequences from production-cost, OPF, and topology-control benchmark scenarios, encodes each sequence through weight-shared GRU branches, and learns a dispatch-transferability metric between the query state and candidate reference states. The learned similarity score is coupled with a constrained multi-objective dispatch layer to balance operating cost, renewable curtailment, reserve shortage, voltage/security violations, and topology risk. Experiments are designed on RTS-GMLC, PGLib-OPF, MATPOWER, and Grid2Op-style scenarios. The proposed method is compared with OPF/UC baselines, GRU/LSTM dispatch predictors, CNN-LSTM, reinforcement-learning topology-control baselines where feasible, and population-based dispatch optimizers. The study aims to demonstrate that similarity-aware temporal representation improves dispatch recommendation robustness under load perturbation and topology uncertainty while preserving reproducible engineering constraints.

### Downstream Task Definition

Task: Given a current grid operating sequence, load forecast window, generator/branch constraints, and optional topology state, recommend a feasible dispatch or dispatch-adjustment plan.

Inputs: bus loads, generator availability, renewable profiles, topology indicators, branch limits, historical operating sequences, candidate reference dispatch states.

Outputs: generator dispatch setpoints, reserve allocation, curtailment decisions, topology-risk score, and ranked historical reference cases.

### Datasets

Primary:

- RTS-GMLC: production cost, unit commitment, renewable integration.
- PGLib-OPF: AC/DC OPF benchmark cases.
- MATPOWER: additional IEEE and synthetic test cases.
- Grid2Op datasets: topology-control and operational stress scenarios.

Optional supporting data:

- OPSD time series for external load/renewable profile perturbation.

### Experiment Quantity

Minimum publishable package: 7 main experiments and 6 ablations.

Main experiments:

| ID | Purpose | Dataset | Key metrics |
|---|---|---|---|
| E1 | Dispatch feasibility and cost under nominal load | RTS-GMLC | cost, reserve shortage, constraint violation |
| E2 | OPF transferability across grid sizes | PGLib-OPF, MATPOWER | feasibility rate, cost gap, runtime |
| E3 | Load perturbation robustness | RTS-GMLC + OPSD profiles | violation rate, curtailment, cost increase |
| E4 | Renewable uncertainty stress test | RTS-GMLC | curtailment, reserve shortage, robustness score |
| E5 | Topology disturbance support | Grid2Op | overload rate, topology-risk score |
| E6 | Similarity retrieval quality | RTS-GMLC/PGLib scenario bank | top-k reference hit rate, dispatch regret |
| E7 | Runtime and scalability | all benchmark groups | inference time, optimization time |

### Ablation and Baseline Design

Baselines:

- DC OPF, AC OPF, UC/economic dispatch where available.
- GRU, LSTM, CNN-LSTM without Siamese retrieval.
- PSO/GWO/WOA-style dispatch optimizers from comparator literature.
- Grid2Op rule or RL baselines where the environment supports them.

Ablations:

- Remove Siamese branch and use single GRU.
- Replace GRU with LSTM under the same retrieval loss.
- Remove digital-twin retrieval and use direct prediction only.
- Remove topology features.
- Remove multi-objective dispatch layer and use weighted single objective.
- Vary reference-bank size and top-k retrieval count.

### Main Innovations

1. Dispatch-state similarity is treated as a first-class learning target, not only a hidden sequence feature.
2. The digital-twin state bank links historical validated cases with current dispatch recommendation.
3. Neural retrieval and constrained multi-objective dispatch are evaluated together, with explicit feasibility and violation metrics.
4. The ARA package can expose every claim through scenario generation configs, retrieval evidence, and dispatch result tables.

## Paper 2

### Recommended Title

Hyperbolic Graph Neural Forecasting for Hierarchical Power Load Prediction in Smart Dispatch Systems

### Target Journal

Primary: Electronics. Backup: Applied Sciences.

Rationale: Recent target-journal papers already include CNN-LSTM, GCN-Transformer, GCN-BiLSTM, and tensor GCN. The novelty must be framed as hierarchical grid/load representation in hyperbolic space, not simply another neural hybrid.

### Abstract

Short-term and day-ahead load forecasting are central inputs for smart dispatch, yet many forecasting models represent power-system spatial relationships in Euclidean graph space even when load regions, substations, feeders, and market zones have hierarchical structure. This paper proposes a hyperbolic graph neural forecasting framework for hierarchical power load prediction. The method maps grid or regional load nodes into a hyperbolic latent space, performs graph message passing under a curvature-aware distance metric, and fuses the resulting spatial representation with temporal modules for multi-horizon forecasting. The design is evaluated on public time-series and grid benchmark data, including Open Power System Data, SimBench profiles, PSML, and optional weather features from public renewable/weather sources. Baselines include ARIMA, XGBoost, LSTM, BiLSTM, TCN, Transformer, Euclidean GCN, GCN-Transformer, and CNN-LSTM. The experiments assess forecasting accuracy, peak-load error, spatial transferability, robustness under missing nodes, and downstream dispatch sensitivity. The expected contribution is a reproducible load-forecasting model that explains when hyperbolic geometry improves hierarchical grid representation and when ordinary Euclidean GNNs are sufficient.

### Downstream Task Definition

Task: Predict short-term and day-ahead load for nodes, zones, feeders, or synthetic grid regions and quantify how forecast errors affect dispatch-support decisions.

Inputs: historical load, time/calendar features, grid hierarchy, adjacency or electrical-distance graph, optional renewable/weather features.

Outputs: multi-horizon load forecasts, uncertainty bands if enabled, spatial transfer scores, dispatch sensitivity indicators.

### Datasets

Primary:

- OPSD time series: European load/renewable time series.
- SimBench: distribution grid profiles and time-series scenarios.
- PSML: public power-system ML time-series repository.

Optional:

- NSRDB weather/irradiance features if API access is configured.
- ENTSO-E/PJM only as optional external validation when access is available.

### Experiment Quantity

Minimum publishable package: 8 main experiments and 7 ablations.

Main experiments:

| ID | Purpose | Dataset | Key metrics |
|---|---|---|---|
| E1 | One-step and multi-step forecasting | OPSD | MAE, RMSE, MAPE/sMAPE |
| E2 | Day-ahead forecasting | OPSD | MAE, RMSE, peak error |
| E3 | Feeder/profile forecasting | SimBench | MAE, RMSE, feeder-level error |
| E4 | Cross-region transfer | OPSD/PSML | transfer MAE, degradation rate |
| E5 | Missing-node robustness | SimBench | error under node masking |
| E6 | Weather-aware extension | OPSD + optional NSRDB | error reduction, peak-load error |
| E7 | Dispatch sensitivity | RTS-GMLC or MATPOWER load injection | cost sensitivity, violation change |
| E8 | Scalability and inference cost | all datasets | training time, inference time |

### Ablation and Baseline Design

Baselines:

- ARIMA/SARIMA, XGBoost/LightGBM.
- LSTM, BiLSTM, TCN, Transformer.
- Euclidean GCN, GAT, GCN-Transformer.
- CNN-LSTM and GCN-BiLSTM comparator variants.

Ablations:

- Hyperbolic graph convolution replaced by Euclidean GCN.
- Learnable curvature replaced by fixed curvature.
- Remove graph structure and use temporal-only model.
- Remove weather/exogenous features.
- Remove hierarchical edges and keep physical adjacency only.
- Compare Lorentz/Poincare implementations if feasible.
- Horizon-length sensitivity.

### Main Innovations

1. Hyperbolic geometry is tied to power-load hierarchy and spatial transfer, not used as a decorative embedding.
2. Forecasting is connected to downstream dispatch sensitivity, which improves engineering relevance for Electronics or Applied Sciences.
3. The paper directly compares against recent GCN/Transformer/CNN-LSTM target-journal patterns.
4. The ARA evidence layer can separate raw forecasting tables from dispatch-sensitivity interpretation.

## Paper 3

### Recommended Title

Self-Adaptive Multi-Objective Differential Evolution for Reproducible Distribution Network Planning with DER and Storage Integration

### Target Journal

Primary: Energies. Backup: Applied Sciences.

Rationale: Energies is the strongest fit because the paper is directly about energy-system planning. Applied Sciences is a backup if the algorithm engineering contribution is emphasized.

### Abstract

Distribution network planning must balance investment cost, voltage quality, reliability, losses, renewable hosting capacity, and operational flexibility under DER and storage integration. Recent target-journal papers show strong interest in active distribution network expansion, improved NSGA-II, dual relaxation, and differential-evolution-style optimization, but many studies do not isolate the contribution of adaptive evolutionary operators under reproducible benchmark conditions. This paper proposes a self-adaptive multi-objective differential evolution algorithm for distribution network planning. The algorithm adjusts mutation factor, crossover rate, strategy selection, and repair intensity according to Pareto-front diversity, constraint violations, and convergence stagnation. Candidate planning actions include feeder reinforcement, distributed generation siting, storage allocation, and topology adjustment. Experiments are built on SimBench and pandapower distribution cases, with MATPOWER/PGLib cases used for cross-checking OPF feasibility. The proposed method is compared with standard DE, NSGA-II, MOEA/D, PSO, GA, and deterministic planning heuristics. The study aims to provide a reproducible planning optimizer that improves Pareto quality, constraint satisfaction, and planning feasibility under public benchmark settings.

### Downstream Task Definition

Task: Select a planning portfolio of candidate line upgrades, DER/storage placements, and topology options that optimizes economic and technical objectives under distribution-network constraints.

Inputs: distribution network topology, load/DG profiles, candidate assets, investment costs, voltage/current constraints, reliability or resilience proxies.

Outputs: Pareto set of planning portfolios, asset siting/capacity decisions, technical performance metrics.

### Datasets

Primary:

- SimBench: distribution networks and profiles.
- pandapower networks: distribution and benchmark networks.

Supporting:

- MATPOWER and PGLib-OPF for OPF feasibility cross-checks.
- OPSD profiles for load/renewable scenario perturbation.

### Experiment Quantity

Minimum publishable package: 7 main experiments and 8 ablations.

Main experiments:

| ID | Purpose | Dataset | Key metrics |
|---|---|---|---|
| E1 | Base distribution planning | SimBench | cost, loss, voltage deviation |
| E2 | DER siting and sizing | SimBench | hosting capacity, voltage violations |
| E3 | Storage allocation | SimBench/pandapower | peak reduction, loss, cost |
| E4 | Expansion planning under load growth | pandapower | cost, feasibility, reliability proxy |
| E5 | Multi-objective Pareto quality | all planning cases | hypervolume, IGD, spacing |
| E6 | Constraint repair effectiveness | SimBench | violation rate, repair count |
| E7 | Runtime scalability | increasing case sizes | runtime, evaluations to convergence |

### Ablation and Baseline Design

Baselines:

- Standard DE.
- NSGA-II, NSGA-III, MOEA/D.
- PSO, GA.
- Rule-based planning heuristic.

Ablations:

- Fixed mutation/crossover instead of adaptive parameters.
- Disable adaptive strategy selection.
- Disable constraint repair.
- Disable diversity preservation.
- Single-objective weighted-sum variant.
- Remove storage candidates.
- Remove DER candidates.
- Scenario count sensitivity.

### Main Innovations

1. The adaptive DE operators are linked to observable planning-state signals: diversity, violations, and stagnation.
2. Planning actions are evaluated as engineering portfolios, not only numerical vectors.
3. Public SimBench/pandapower cases make the results reproducible for MDPI requirements.
4. The ARA structure can expose optimization traces, constraint-repair logs, and Pareto result tables.

## Paper 4

### Recommended Title

Scenario-Aware Hybrid Multi-Objective Evolution for Resilient Distribution Network Planning under DER and Load Uncertainty

### Target Journal

Primary: Energies.

Rationale: The paper aligns tightly with Energies topics: distribution systems, DER uncertainty, resilience, energy-system planning, and reproducible simulation.

### Abstract

High DER penetration and increasingly volatile load profiles make distribution network planning a resilience-oriented problem rather than a deterministic investment problem. Recent target-journal papers address stochastic MILP, fault recovery, islanding operation, and genetic-algorithm-based resilience enhancement, but fewer studies combine scenario screening, local repair, and multi-objective evolutionary search in a reproducible public-benchmark package. This paper proposes a scenario-aware hybrid multi-objective evolutionary framework for resilient distribution network planning under DER and load uncertainty. The framework generates renewable, load, and outage scenarios from public benchmark profiles, screens high-risk scenarios, and optimizes planning portfolios with objectives including investment cost, expected loss, voltage-security performance, renewable hosting capacity, load served during contingencies, and restoration capability. The hybrid optimizer combines global evolutionary search with feasibility repair and local resilience-improvement moves. Experiments use SimBench and pandapower networks, RTS-GMLC/OPSD profiles for scenario construction, and reliability-report-inspired contingency patterns. The method is compared with deterministic planning, stochastic MILP where tractable, NSGA-II, MOEA/D, GA, and hybrid search without repair. The expected contribution is a reproducible resilience-planning framework that links DER uncertainty to explicit planning trade-offs.

### Downstream Task Definition

Task: Produce a planning portfolio that remains feasible and resilient across uncertain DER/load/outage scenarios.

Inputs: distribution grid, candidate reinforcement/storage/DER actions, scenario library, contingency list, restoration constraints.

Outputs: Pareto-resilient planning portfolios, scenario feasibility profile, resilience and cost trade-off curves.

### Datasets

Primary:

- SimBench and pandapower distribution cases.
- OPSD and RTS-GMLC profiles for load/renewable scenario templates.

Supporting:

- NERC reliability reports for contingency taxonomy and event-style stress templates.
- MATPOWER cases for additional OPF stress checks.

### Experiment Quantity

Minimum publishable package: 8 main experiments and 7 ablations.

Main experiments:

| ID | Purpose | Dataset | Key metrics |
|---|---|---|---|
| E1 | Deterministic vs scenario-aware planning | SimBench | cost, loss, violations |
| E2 | DER uncertainty planning | SimBench + OPSD/RTS profiles | hosting capacity, voltage risk |
| E3 | Load uncertainty planning | SimBench | expected loss, violation probability |
| E4 | Outage contingency planning | SimBench/pandapower | load served, survivability |
| E5 | Restoration-aware evaluation | pandapower | restoration rate, outage cost proxy |
| E6 | Scenario-screening efficiency | all scenario libraries | retained risk, runtime |
| E7 | Pareto-front quality | all cases | hypervolume, IGD, spacing |
| E8 | Stress-test generalization | unseen scenarios | feasibility rate, resilience degradation |

### Ablation and Baseline Design

Baselines:

- Deterministic single-scenario planning.
- Stochastic MILP for small cases.
- NSGA-II, MOEA/D, GA.
- Hybrid evolutionary algorithm without scenario screening.
- Hybrid evolutionary algorithm without local repair.

Ablations:

- Remove scenario screening.
- Remove local repair.
- Remove resilience objective.
- Remove DER uncertainty.
- Remove outage uncertainty.
- Vary scenario count and severity.
- Compare weighted-sum vs Pareto formulation.

### Main Innovations

1. Resilience is measured across generated scenarios instead of claimed from a single deterministic plan.
2. Scenario screening reduces computational burden while retaining high-risk evidence.
3. Local repair is tied to voltage/security/restoration feasibility.
4. The ARA package can preserve rejected plans, failed scenarios, and stress-test evidence.

## Paper 5

### Recommended Title

Hybrid Multi-Objective Evolution for Traceable Power Grid Feasibility Review and Investment Effectiveness Optimization

### Target Journal

Primary: IEEE Access. Backup: Energies.

Rationale: The topic is cross-disciplinary: power-system planning, investment review, reliability, decision support, and optimization. IEEE Access is suitable if the manuscript emphasizes a generalizable engineering decision framework. Energies is suitable if the power-grid planning and investment-effectiveness angle dominates.

### Abstract

Power grid feasibility review requires simultaneous assessment of investment effectiveness, technical necessity, reliability benefit, renewable accommodation, schedule risk, and budget feasibility. Existing target-journal papers include power-grid investment risk-benefit optimization and reliability investment valuation, but feasibility review is often represented as static expert scoring or isolated portfolio optimization. This paper proposes a hybrid multi-objective evolutionary framework for traceable power grid feasibility review and investment effectiveness optimization. Candidate projects are represented through a reproducible feature schema derived from public grid benchmarks, reliability-report evidence, and semi-synthetic project portfolios. The optimizer combines Pareto search, feasibility-rule repair, and preference-aware ranking to generate project portfolios under budget, reliability, load-growth, renewable-integration, and schedule constraints. Experiments use RTS-GMLC, SimBench, MATPOWER/PGLib-derived project candidates, NERC report features, and C2GES-style reliability evidence. Baselines include weighted scoring, AHP, TOPSIS, greedy budget allocation, NSGA-II, MOEA/D, and standard evolutionary search. The expected contribution is a transparent feasibility-review framework where each recommendation can be traced to objectives, constraints, evidence features, and optimization decisions.

### Downstream Task Definition

Task: Given a candidate pool of grid projects and review constraints, generate and rank project portfolios for feasibility-review recommendation.

Inputs: candidate project features, budget, reliability benefit proxy, load-growth benefit, renewable accommodation benefit, schedule risk, policy/compliance indicators, evidence references.

Outputs: Pareto project portfolios, ranked recommendation list, investment-effectiveness score, constraint and evidence trace.

### Datasets

Primary:

- RTS-GMLC-derived project portfolio features.
- SimBench-derived distribution project candidates.
- MATPOWER/PGLib-derived reinforcement and OPF-benefit candidates.
- C2GES/NERC reliability report collection for event and reliability evidence features.

Important boundary:

- If no enterprise project data are available, all claims must be stated as benchmark-derived and semi-synthetic, not real enterprise approval effectiveness.

### Experiment Quantity

Minimum publishable package: 7 main experiments and 8 ablations.

Main experiments:

| ID | Purpose | Dataset | Key metrics |
|---|---|---|---|
| E1 | Benchmark-derived portfolio optimization | RTS-GMLC | hypervolume, budget feasibility |
| E2 | Distribution project review | SimBench | voltage/loss benefit per investment |
| E3 | Reliability-driven review | NERC/C2GES features | reliability benefit proxy, trace coverage |
| E4 | Renewable accommodation review | RTS-GMLC/OPSD profiles | curtailment reduction proxy |
| E5 | Ranking stability under budget changes | all portfolios | Kendall tau, rank variance |
| E6 | Preference-aware decision support | all portfolios | decision consistency, regret proxy |
| E7 | Explanation and traceability evaluation | all portfolios | trace completeness, rule conflict count |

### Ablation and Baseline Design

Baselines:

- Expert-weighted scoring.
- AHP, TOPSIS.
- Greedy benefit-cost allocation.
- NSGA-II, MOEA/D.
- Standard GA/DE without feasibility review repair.

Ablations:

- Remove feasibility-rule repair.
- Remove preference-aware ranking.
- Remove reliability feature group.
- Remove renewable accommodation feature group.
- Remove schedule-risk constraints.
- Use single weighted objective.
- Replace hybrid optimizer with NSGA-II only.
- Vary budget and project pool size.

### Main Innovations

1. Feasibility review is formalized as a traceable multi-objective decision process rather than static scoring.
2. Public benchmark systems are converted into reproducible project-review portfolios.
3. Reliability-report evidence is treated as a feature source, creating a bridge between report NLP and project review.
4. The ARA evidence layer can link each recommendation to objective values, violated rules, and supporting project features.

## Paper 6

### Recommended Title

Non-Dominated Sorting with Bidirectional Local Search for Budget-Constrained Power Grid Project Review

### Target Journal

Primary: Applied Sciences. Backup: IEEE Access.

Rationale: Applied Sciences is appropriate for a well-controlled applied optimization algorithm paper. IEEE Access is a backup if the manuscript broadens into a general engineering decision-support system.

### Abstract

Budget-constrained power grid project review is a constrained multi-objective optimization problem involving investment effectiveness, reliability improvement, load-growth support, renewable integration, schedule risk, and policy compliance. Recent target-journal papers use NSGA-II and other multi-objective methods in planning and energy-storage configuration, but the local neighborhood design for project-review portfolios is rarely made explicit. This paper proposes a non-dominated sorting evolutionary algorithm enhanced by bidirectional local search for power grid project review. The forward local search adds, expands, or substitutes high-benefit projects to improve portfolio value, while the backward local search removes low-effectiveness or constraint-violating projects to recover feasibility and reduce risk. Non-dominated sorting maintains diverse trade-off portfolios under budget, reliability, schedule, and compliance constraints. Experiments use the same public benchmark-derived project pool as the feasibility-review framework, including RTS-GMLC, SimBench, MATPOWER/PGLib, and NERC/C2GES evidence features. Baselines include NSGA-II, NSGA-III, MOEA/D, greedy allocation, AHP/TOPSIS ranking, and hybrid evolutionary search without bidirectional local search. The expected contribution is an interpretable local-search mechanism that improves Pareto quality, feasibility recovery, and review recommendation stability.

### Downstream Task Definition

Task: Select and rank a subset of candidate power grid projects under budget and review constraints, with explicit local modifications that explain why a project is added, removed, or substituted.

Inputs: project candidate pool, objective vector, constraints, project dependency graph, review rules, budget levels.

Outputs: non-dominated project portfolios, local-search move log, ranking and explanation for each selected project.

### Datasets

Primary:

- Same semi-synthetic project pool as Paper 5.
- RTS-GMLC, SimBench, MATPOWER/PGLib-derived project candidates.
- C2GES/NERC reliability evidence features.

Optional:

- Enterprise project data can be added as a private validation set only after anonymization and permission.

### Experiment Quantity

Minimum publishable package: 8 main experiments and 9 ablations.

Main experiments:

| ID | Purpose | Dataset | Key metrics |
|---|---|---|---|
| E1 | Budget-constrained project selection | benchmark portfolio | hypervolume, feasibility rate |
| E2 | Reliability-prioritized review | NERC/C2GES-featured portfolio | reliability benefit proxy |
| E3 | Renewable-accommodation project review | RTS-GMLC/OPSD-derived portfolio | renewable benefit proxy |
| E4 | Dependency-constrained project review | synthetic dependency graph | violation rate, repair success |
| E5 | Local move explainability | all portfolios | move trace completeness |
| E6 | Ranking robustness | all portfolios | Kendall tau, rank variance |
| E7 | Budget sensitivity | all portfolios | Pareto stability, marginal benefit |
| E8 | Scalability with project pool size | synthetic scale-up | runtime, evaluations |

### Ablation and Baseline Design

Baselines:

- NSGA-II, NSGA-III, MOEA/D.
- Greedy budget allocation.
- AHP/TOPSIS ranking.
- Random feasible portfolios.
- Hybrid MOEA without local search.

Ablations:

- Remove forward local search.
- Remove backward local search.
- Replace bidirectional search with random mutation only.
- Remove dependency-aware moves.
- Remove feasibility recovery.
- Remove non-dominated sorting and use weighted ranking.
- Vary local-search depth.
- Vary project dependency density.
- Vary budget tightness.

### Main Innovations

1. Bidirectional local search is defined in project-review terms, not generic vector mutation.
2. Forward and backward moves produce an interpretable audit trail for feasibility-review recommendations.
3. The paper isolates the algorithmic contribution more cleanly than Paper 5.
4. ARA traces can preserve every local move, rejected move, and feasibility-recovery step.

## Cross-Paper Dataset Allocation

| Dataset | P1 | P2 | P3 | P4 | P5 | P6 |
|---|---|---|---|---|---|---|
| RTS-GMLC | primary | dispatch sensitivity | optional | scenario source | primary | primary |
| PGLib-OPF | primary | optional | supporting | optional | primary | primary |
| MATPOWER | primary | optional | supporting | supporting | primary | primary |
| Grid2Op | primary | no | no | optional | no | no |
| OPSD | optional | primary | supporting | scenario source | optional | optional |
| SimBench | optional | primary | primary | primary | primary | primary |
| pandapower | supporting | optional | primary | primary | optional | optional |
| PSML | no | primary | no | optional | no | no |
| NERC/C2GES reports | no | no | no | supporting | primary | primary |

## Claim Discipline for ARA Implementation

Each paper should create an ARA artifact before manuscript writing. Suggested core claims:

- C1: The method improves the target task metric against strong baselines.
- C2: The proposed component contributes independently, proven by ablation.
- C3: The method remains feasible or robust under stress tests.
- C4: The experiment package is reproducible from public or explicitly described semi-synthetic data.

Each claim must map to experiment IDs and evidence files. Exact numerical claims are not allowed in the manuscript draft until result tables are generated.

## Minimum Reviewer-Ready Evidence Package

For every paper:

1. Dataset manifest with local path, source URL, preprocessing script, and license/access notes.
2. Config files for every baseline and proposed model.
3. Fixed random seeds and repeated runs.
4. Main result table, ablation table, runtime table, and stress-test table.
5. Statistical comparison or repeated-run variance for key metrics.
6. Supplementary material linking code, data processing, and result logs.

This package directly supports MDPI reproducibility expectations and IEEE Access validation expectations.
