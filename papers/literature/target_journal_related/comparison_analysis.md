# Target-Journal Related Literature Comparison

Date boundary: 2023-07-11 to 2026-07-11.

Target journals: Energies, Applied Sciences, Electronics, IEEE Access.

Scope: external published papers only. These papers are comparator literature for the six planned manuscripts and are not marked as project-original work.

## Collection Snapshot

| Planned topic | Papers | Local PDFs | Main journals |
|---|---:|---:|---|
| `p1_twin_gru_dispatch` | 12 | 12 | Applied Sciences, Electronics, Energies, IEEE Access |
| `p2_hyperbolic_gcn_smart_dispatch` | 12 | 12 | Applied Sciences, Electronics, Energies, IEEE Access |
| `p3_self_adaptive_mode_distribution_planning` | 12 | 12 | Electronics, Energies, IEEE Access |
| `p4_resilience_distribution_planning` | 12 | 12 | Applied Sciences, Electronics, Energies |
| `p5_hybrid_moea_feasibility_review` | 10 | 10 | Applied Sciences, Energies |
| `p6_nsga_bls_feasibility_review` | 9 | 9 | Applied Sciences, Electronics, Energies |

Total: 67 papers, 67 cached PDFs.

## Cross-Topic Findings

The target-journal literature is strong in engineering optimization, short-term load forecasting, distribution-network planning, resilience modeling, energy storage configuration, and investment-risk analysis. The dominant algorithm families are PSO, grey wolf optimization, whale optimization, genetic algorithms, NSGA-II, differential evolution, stochastic MILP, dual relaxation, CNN-LSTM, BiLSTM, TCN, Transformer, and GCN hybrids.

The most visible downstream tasks are economic dispatch, unit commitment, microgrid dispatch, short-term power-load forecasting, active distribution network expansion planning, renewable and DER uncertainty planning, resilience restoration, energy storage siting and sizing, grid-side investment return analysis, reliability investment, and power-grid project delay impact assessment.

The main gap across the six planned manuscripts is not a lack of optimization or forecasting papers. The gap is the missing integration of learning-based state representation, multi-objective decision optimization, project-review logic, and reproducible benchmark evidence in one ARA-style engineering package.

## Topic-Level Comparison

| Planned topic | Existing algorithm landscape | Existing downstream tasks | Positioning gap for planned manuscript |
|---|---|---|---|
| Twin/Siamese GRU dispatch | Heuristic dispatch optimizers, improved PSO/GWO/WOA, combined heat-power dispatch, unit commitment models, LSTM-assisted dispatch in renewable or virtual power plant settings. | Economic dispatch, low-carbon microgrid dispatch, unit commitment, hybrid renewable dispatch, transformer life-loss aware scheduling. | Published comparators optimize dispatch directly or use ordinary sequential predictors. The planned Siamese GRU direction should emphasize paired-state similarity learning, load-aware dispatch state representation, and multi-objective dispatch decisions under comparable benchmark settings. |
| Hyperbolic GCN smart dispatch/load forecasting | CNN-LSTM with attention, GCN-Transformer, TCN-BiLSTM, GCN-BiLSTM-AdaBoost, tensor GCN, intelligent data analysis pipelines. | Short-term load forecasting, smart-grid load forecasting, dispatch-support forecasting, distributed load leveling. | GCN and Transformer hybrids are active, but hyperbolic geometry is not yet the visible default in the target set. The planned paper should justify hyperbolic space as a grid/topology hierarchy representation rather than another neural hybrid. |
| Self-adaptive MODE distribution planning | Wasserstein distance and dual relaxation, distribution network expansion planning, differential evolution comparisons, improved NSGA-II, topology/time-series scenario optimization. | Active distribution network planning, expansion planning, distributed generation integration, energy storage and EV collaborative planning. | Existing work covers multi-objective planning, but self-adaptation and differential-evolution operator control need to be tied to planning constraints, benchmark cases, and convergence evidence. |
| Resilience-oriented distribution planning | Stochastic MILP, fault recovery, islanding operation, GA-based resilience enhancement, multi-criteria resilient microgrid planning, uncertainty-aware reconfiguration. | Resilience planning, renewable/load uncertainty, DER uncertainty, distribution network recovery, microgrid dispatch under high renewable penetration. | The planned work should distinguish itself by linking scenario-based DER uncertainty with resilience metrics and hybrid multi-objective search, not only outage restoration or stochastic scheduling. |
| Hybrid MOEA feasibility review | Hybrid power-grid investment risk-benefit optimization, reliability investment valuation, grid-side storage ROI analysis, transmission and storage coordinated planning. | Investment effectiveness, reliability investment, energy storage planning, grid project portfolio/risk-benefit assessment. | There is a credible target-journal precedent for power-grid investment optimization, but less visible work on feasibility-review workflows. The planned paper should make review criteria, investment effectiveness indicators, and audit-like decision traceability central. |
| NSGA + bidirectional local search feasibility review | NSGA-II and multi-objective planning, grid-side storage investment return, substation delay impact assessment, load-flow multi-objective optimization overviews. | Investment planning, grid project scheduling impact, portfolio-style project selection, grid flexibility planning. | Existing papers use NSGA-style optimization, but the bidirectional local-search contribution must be made concrete: neighborhood definition, dominance-preserving moves, project-review constraints, and ablation against NSGA-II/MOEA baselines. |

## Representative Papers by Topic

### `p1_twin_gru_dispatch`

- Analysis of Heuristic Optimization Technique Solutions for Combined Heat-Power Economic Load Dispatch, Applied Sciences, 2023-09-16.
- Optimizing Economic Dispatch for Microgrid Clusters Using Improved Grey Wolf Optimization, Electronics, 2024-08-08.
- Dynamic Line Rating and Transformer-Life-Loss-Related Unit Commitment Under Extreme High-Temperature Conditions, Electronics, 2025-10-14.
- Forecast-Driven Virtual Power Plant Dispatch for Hybrid Renewable Energy Systems: Reducing Grid Dependency Using LSTM Models, Energies, 2026-04-09.

### `p2_hyperbolic_gcn_smart_dispatch`

- Power Grid Load Forecasting Using a CNN-LSTM Network Based on a Multi-Modal Attention Mechanism, Applied Sciences, 2025-02-24.
- Short-Term Power Load Forecasting Using an Improved Model Integrating GCN and Transformer, Applied Sciences, 2025-06-21.
- Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load Forecasting, Electronics, 2025-08-21.
- LoadSeer: Exploiting Tensor Graph Convolutional Network for Power Load Forecasting With Spatio-Temporal Characteristics, IEEE Access, 2024.

### `p3_self_adaptive_mode_distribution_planning`

- Active Distribution Network Expansion Planning Based on Wasserstein Distance and Dual Relaxation, Energies, 2024-06-18.
- Multi-Objective Collaborative Optimization of Distribution Networks with Energy Storage and Electric Vehicles Using an Improved NSGA-II Algorithm, Energies, 2025-10-02.
- Economic Dispatch in Electrical Systems with Hybrid Generation Using the Differential Evolution Algorithm, Energies, 2025-06-29.
- Enhanced Coati Optimization Algorithm for Static and Dynamic Transmission Network Expansion Planning, IEEE Access, 2023.

### `p4_resilience_distribution_planning`

- Research of Islanding Operation and Fault Recovery Strategies of Distribution Network Considering Uncertainty of New Energy, Electronics, 2023-10-13.
- Multi-Objective Site Selection and Capacity Determination of Distribution Network Considering New Energy Uncertainties and Shared Energy Storage of Electric Vehicles, Electronics, 2025-01-02.
- Enhancing Distribution Network Resilience Using Genetic Algorithms, Electronics, 2025-11-04.
- Integrated Multi-Criteria Planning for Resilient Renewable Energy-Based Microgrid Considering Advanced Demand Response and Uncertainty, Energies, 2023-09-27.

### `p5_hybrid_moea_feasibility_review`

- A Novel Hybrid Power-Grid Investment Optimization Model with Collaborative Consideration of Risk and Benefit, Energies, 2023-10-23.
- Interruption Cost Estimation for Value-Based Reliability Investment in Emerging Smart Grid Resources, Applied Sciences, 2024-09-25.
- Optimal Planning and Investment Return Analysis of Grid-Side Energy Storage System Addressing Multi-Dimensional Grid Security Requirements, Applied Sciences, 2025-11-10.
- Multi-Stage Coordinated Planning for Transmission and Energy Storage Considering Large-Scale Renewable Energy Integration, Applied Sciences, 2024-07-25.

### `p6_nsga_bls_feasibility_review`

- A Novel Hybrid Power-Grid Investment Optimization Model with Collaborative Consideration of Risk and Benefit, Energies, 2023-10-23.
- Quantitative Evaluation of Crucial Substations and Simulation-Driven Impact Assessment of Commissioning Delays in Multi-Voltage Grid Planning, Electronics, 2025-06-29.
- Multi-Objective Optimization of Offshore Wind Farm Configuration for Energy Storage Based on NSGA-II, Energies, 2025-06-10.
- Multi-Objective Optimization of Load Flow in Power Systems: An Overview, Energies, 2025-11-20.

## ARA Follow-Up Requirements

1. Extract exact datasets, benchmarks, metrics, and baselines from each cached PDF into the corresponding `evidence/source/` directory.
2. For papers with reproducible code, attach repositories under each paper's `src/code/` directory and mark provenance.
3. Convert high-value comparator papers into experiment tasks under the relevant planned manuscript project only after the PDF evidence has been extracted.
4. Keep the external collection separate from the two project-original unpublished manuscripts.

## Source Systems

- Crossref metadata API: https://api.crossref.org/works
- OpenAlex was attempted first but rate-limited during this session: https://openalex.org/
- Target journal scope: Energies, Applied Sciences, Electronics, IEEE Access.
