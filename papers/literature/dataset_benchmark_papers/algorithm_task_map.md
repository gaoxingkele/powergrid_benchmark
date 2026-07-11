# Algorithm and Downstream Task Map

Date: 2026-07-11

Scope: 111 deduplicated external papers in `ara_collections/dataset_benchmark_papers/`.
This is a first-pass map derived from titles, dataset links, venue metadata, and the
five cloned code snapshots. Exact architectures, hyperparameters, tables, and claims
still require full-text ARA extraction.

## Main Algorithm / Framework Families

| Family | Typical methods seen in the collection | Main datasets |
|---|---|---|
| Optimization and mathematical programming | AC/DC OPF, convex relaxation, QC/SOC/SDP relaxation, unit commitment, economic dispatch, expansion planning, scheduling, bilevel optimization, submodular optimization | `pglib_opf`, `matpower`, `rts_gmlc`, `pandapower`, `tamu_test_cases`, `pjm_dataminer` |
| Forecasting and time-series ML | CNN, LSTM, BiLSTM, CNN-LSTM-AM, Transformer/Autoformer variants, residual learning, conformal calibration, categorical boosting, ensemble learning | `acn_data`, `opsd_time_series`, `nsrdb`, `simbench`, `entsoe_transparency`, `pjm_dataminer` |
| Reinforcement learning and multi-agent control | Deep RL, DQN/Deep-Q style control, SAC-style control, multi-agent RL, physics-guided RL, adversarial/defensive RL | `grid2op_datasets`, `simbench`, `pjm_dataminer`, `acn_data` |
| Graph and topology learning | Graph neural networks, TGCN-style graph temporal learning, topology control, topology optimization, feature propagation, islanding, cascading-sequence identification | `grid2op_datasets`, `tamu_test_cases`, `pglib_opf`, `simbench` |
| Security, resilience, and risk analytics | Cascading failure analysis, N-1 robust control, blackout mitigation, attack/defense, electricity theft detection, risk-oriented security assessment, grid fragility analysis | `grid2op_datasets`, `tamu_test_cases`, `simbench`, `rts_gmlc`, `c2ges_nerc_reports` |
| Clustering, tree models, KNN, and ensembles | Hierarchical clustering, K-nearest neighbours, tree/cluster methods, ensemble stacking, boosting, kernel density estimation, fuzzy MCDM | `acn_data`, `nsrdb`, `matpower` |
| Simulation, digital twin, and benchmark tooling | Hardware emulation, digital twins, CGMES-to-network conversion, Python power-flow solver comparison, benchmark/toolbox papers | `pandapower`, `matpower`, `pglib_opf`, `tamu_test_cases` |
| LLM/NLP-oriented power-system analysis | LLM-assisted power system control/analysis, language-model aided state estimation, report/evidence analysis, reasoning agents | `pandapower`, `matpower`, `c2ges_nerc_reports`, `psml` |

## Downstream Task Categories

| Task category | Description | Main datasets |
|---|---|---|
| EV charging forecasting and scheduling | Charging load forecasting, charging flexibility forecasting, EV scheduling, incentive pricing, out-of-distribution EV charging | `acn_data`, `eia_opendata`, `entsoe_transparency` |
| Load, PV, wind, and irradiance forecasting | Day-ahead load forecasting, probabilistic PV forecasting, solar irradiance estimation, weather-aware forecasting | `opsd_time_series`, `nsrdb`, `entsoe_transparency`, `simbench`, `pjm_dataminer` |
| OPF, power flow, dispatch, and planning | AC/DC OPF, OPF approximation, dispatch, UC, expansion planning, transmission/distribution co-optimization | `pglib_opf`, `matpower`, `rts_gmlc`, `pandapower`, `tamu_test_cases` |
| Grid topology control and RL operation | Topology optimization, safe low-carbon operation, N-1 robust control, blackout mitigation, attack defense | `grid2op_datasets`, `tamu_test_cases`, `simbench` |
| Stability, reliability, cascading, and resilience | Cascading failure, controlled islanding, dynamic stability assessment, reliability/security risk, outage/fragility analysis | `tamu_test_cases`, `rts_gmlc`, `c2ges_nerc_reports`, `grid2op_datasets` |
| Market and energy-hub decision making | Day-ahead scheduling, online dispatch, bidding, price/incentive design, capacity accreditation | `pjm_dataminer`, `eia_opendata`, `rts_gmlc` |
| Distribution grid and DER control | DER coordination, curtailment, storage sizing, low-voltage grid studies, microgrid economic dispatch | `simbench`, `pandapower`, `rts_gmlc`, `opsd_time_series` |
| Dataset, benchmark, and software evaluation | Dataset generation, benchmark toolboxes, survey/overview papers, solver/library comparison | `pglib_opf`, `matpower`, `pandapower`, `grid2op_datasets`, `psml` |

## Dataset-Level Map

| Dataset | Dominant algorithms / frameworks | Dominant downstream tasks |
|---|---|---|
| `acn_data` | Time-series ML, CNN/LSTM/BiLSTM, Transformer-style forecasting, clustering, KNN, ensembles, RL scheduling | EV charging load forecasting, charging flexibility, real-time charging optimization |
| `grid2op_datasets` | Reinforcement learning, multi-agent RL, physics-guided RL, graph/topology learning, adversarial RL | Power-grid topology control, safe operation, blackout mitigation, attack/defense |
| `pglib_opf` | OPF optimization, convex relaxations, typed GNN, dataset generation, optimization benchmarks | AC OPF, OPF approximation, relaxation quality, dynamic security assessment |
| `rts_gmlc` | UC/dispatch optimization, GNN acceleration, storage planning, capacity credit, risk/security assessment | Unit commitment, renewable/storage planning, reliability, frequency support |
| `matpower` | Power-flow/OPF algorithms, simulation tooling, LLM-assisted simulation, optimization, fuzzy/software comparison | Power-flow simulation, OPF, grid-transit co-optimization, software education/evaluation |
| `pandapower` | Pandapower modeling, CGMES conversion, OPF, LLM-assisted control, distribution simulation | Operational network modeling, distribution/grid studies, OPF, state/control analysis |
| `simbench` | Distribution-grid simulation, DER optimization, ensemble forecasting, symbolic regression, edge/LLM learning | Low-voltage/distribution studies, DER coordination, load forecasting, voltage prediction |
| `tamu_test_cases` | Convex relaxation, GNN, submodular optimization, digital twin, cascading/stability analytics | Cascading failure, islanding, dynamic stability, transmission switching, restoration |
| `opsd_time_series` | Forecasting ML, residual learning, conformal calibration, online/meta learning | Load/PV forecasting, probabilistic forecasting, microgrid economic dispatch |
| `nsrdb` | Solar irradiance ML, BiLSTM, boosting, physics-based DNI modeling, downscaling | Solar irradiance estimation, short-term irradiance forecasting, weather feature modeling |
| `entsoe_transparency` | Forecasting, GAN uncertainty modeling, market/data analytics, outage analysis | Load forecasting, European market transparency, generation/outage availability, EV strategy evaluation |
| `pjm_dataminer` | Scheduling optimization, flexibility envelopes, hierarchical RL, uncertainty modeling | Energy hub dispatch, market bidding, capacity accreditation |
| `eia_opendata` | Scheduling optimization, data/replication packages, energy risk analytics | EV scheduling, energy-security risk, EIA data processing |
| `c2ges_nerc_reports` | Report/risk analysis, reliability evidence analysis | Grid fragility, reliability/security report analysis |
| `lbnl_pmu_event_library` | Cross-domain transfer and PMU-oriented event analysis candidate | PMU event/fault/disturbance analysis |
| `psml` | IDS/anomaly-detection survey candidate, time-series reasoning candidate | Power/time-series anomaly detection and reasoning |

## Locally Cloned Code Snapshots

| Paper | Repository | Status | Algorithm clue |
|---|---|---|---|
| EV load forecasting using a refined CNN-LSTM-AM | `gyboo/Refined-CNN-LSTM-AM` | `cloned` | CNN-LSTM with attention mechanism for EV load forecasting |
| Blackout Mitigation via Physics-Guided RL | `anmold-07/Physics-Guided-Blackout-Mitigation` | `cloned` | Physics-guided reinforcement learning for blackout mitigation |
| Heterogeneous reinforcement learning for defending power grids against attacks | `AminMoradiXL/TGCN` | `cloned_sparse` | Graph/temporal RL-style grid attack/defense code; sparse snapshot due Windows path limits |
| Optimizing Power Grid Topologies with Reinforcement Learning: A Survey of Methods and Challenges | `EricavanderSar/rl4pnc-survey` | `cloned` | RL topology-control survey support code/material |
| Short-term global horizontal irradiance forecasting using weather classified categorical boosting | `Ubaid014/Short-term-Global-Horizontal-Irradiance-Forecasting-Using-Weather-Classified-Categorical-Boosting` | `cloned` | Categorical boosting for GHI forecasting |

## Current Confidence Boundary

- High confidence: dataset link, broad task category, and methods explicitly visible in titles or cloned repositories.
- Medium confidence: algorithm family inferred from title keywords such as OPF, GNN, RL, forecasting, or convex relaxation.
- Low confidence: exact model architecture, hyperparameters, baselines, metrics, and ablation logic until full paper extraction is completed.
