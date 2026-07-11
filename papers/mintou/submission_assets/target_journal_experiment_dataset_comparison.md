# Mintou vs Target-Journal Comparator Papers: Experiment and Dataset Strength

Date: 2026-07-11

Evidence base:

- Mintou ARA directories under `papers/mintou/`
- Mintou submission assets under `papers/mintou/submission_assets/`
- Target-journal comparator collection: `papers/literature/target_journal_related/comparison_analysis.md`
- Comparator manifest: `ara_collections/target_journal_related/collection_manifest.csv`

Scope: first-round comparison against same-theme papers from Energies, Applied Sciences, Electronics, and IEEE Access, 2023-07-11 to 2026-07-11. This comparison focuses on experiment quantity, experiment strength, and dataset sufficiency. It does not yet claim a full novelty or performance ranking because exact dataset/metric tables have not been extracted from every cached comparator PDF.

## Comparator Collection Baseline

| Mintou Paper | Comparator Topic | Comparator Papers | Main Comparator Journals |
| --- | --- | ---: | --- |
| P1 DSTAR-GRU dispatch | Twin/Siamese GRU dispatch and dispatch optimization | 12 | Applied Sciences, Electronics, Energies, IEEE Access |
| P2 HyG-LoadFormer forecasting | Hyperbolic GCN / smart dispatch / load forecasting | 12 | Applied Sciences, Electronics, Energies, IEEE Access |
| P3 CARS-MODE planning | Self-adaptive MODE / distribution planning | 12 | Electronics, Energies, IEEE Access |
| P4 SHIELD-MOEA resilience | Resilience distribution planning | 12 | Applied Sciences, Electronics, Energies |
| P5 TRACE-MOEA review | Hybrid MOEA feasibility/investment review | 10 | Applied Sciences, Energies |
| P6 BiLo-NSGA review | NSGA + local search feasibility/investment review | 9 | Applied Sciences, Electronics, Energies |

## Current Strength Comparison

| Paper | Current Mintou Dataset/Split Coverage | Target-Journal Comparator Norm | Relative Position Now | Main Gap |
| --- | --- | --- | --- | --- |
| P1 DSTAR-GRU | RTS-GMLC fixed, rolling, and high-renewable/topology/ramp stress subsets. | Dispatch papers usually use OPF/UC, microgrid, integrated-energy, N-1, transformer/line/security constraints, or multi-stage dispatch cases. | Below target-journal strong level; acceptable only as scoped dispatch-proxy evidence. | Needs OPF/UC or Grid2Op-style feasibility validation; current gain is marginal. |
| P2 HyG-LoadFormer | OPSD + SimBench, fixed and rolling splits, 1h/24h horizon views, normalized SimBench metrics. | Forecasting papers commonly use at least one public or regional load dataset, multiple horizons, neural baselines such as CNN-LSTM, TCN, BiLSTM, Transformer, GCN hybrids. | Near target-journal level for day-ahead/24h; below level for short-horizon claims. | Needs stronger neural baselines if claiming 1h superiority; otherwise position around 24h/day-ahead. |
| P3 CARS-MODE | SimBench DER/storage stress proxy, several weak/near-miss revisions preserved. | Distribution planning papers usually include active distribution network cases, DER/storage/EV scenarios, load-flow feasibility, Pareto metrics, and scenario uncertainty. | Below target-journal strong level. | Needs pandapower/AC load-flow, DER penetration variance, storage-cost scenarios, and feasibility tables. |
| P4 SHIELD-MOEA | SimBench resilience-planning proxy with positive signal and ablations. | Resilience papers usually include outage/fault recovery, islanding, N-1/N-k contingencies, renewable/load uncertainty, stochastic or multi-scenario tests. | Medium; closer to target-journal level than P3 but not complete. | Needs contingency scenario variance and feasibility metrics. |
| P5 TRACE-MOEA | RTS-GMLC + SimBench + NERC/C2GES report-cache project-review proxy. | Investment/review papers often use real project portfolios, risk-benefit indicators, interruption cost, reliability investment, storage ROI, and policy/economic assumptions. | Below target-journal decision-support level; good proxy benchmark only. | Needs expert-labeled or rule-audited review outcomes, calibrated costs, and sensitivity to criteria weights. |
| P6 BiLo-NSGA | Same public proxy family as P5, stronger optimization gain, budget-constrained portfolio view. | NSGA/planning papers usually show multiple planning cases, budget or investment constraints, Pareto/convergence curves, and repeated runs. | Medium for algorithmic optimization; below level for real project-review claims. | Needs dependency-aware portfolio labels, seed variance, convergence curves, and budget sensitivity. |

## Experiment Quantity Comparison

| Paper | Current Mintou Evidence Strength | Minimum Needed to Match Target-Journal Pattern | Current Verdict |
| --- | --- | --- | --- |
| P1 DSTAR-GRU | Fixed + rolling + stress results; baselines and ablations exist. | At least 7 main comparators, 4 ablations, 4 split/stress views, and one feasibility table. | Experiment count is reasonable, engineering validity is insufficient. |
| P2 HyG-LoadFormer | Two datasets, rolling evidence, multiple horizons, baselines and ablations. | 8 comparators, 4 ablations, 6 dataset/split/horizon views. | Dataset/split coverage is good; baseline strength should be upgraded for neural comparators. |
| P3 CARS-MODE | One public benchmark-derived stress task plus ablations; gain is narrow. | 7 comparators, 5 ablations, 5 scenario views, AC feasibility and Pareto/frontier evidence. | Not enough yet for Energies-level planning claim. |
| P4 SHIELD-MOEA | One public benchmark-derived resilience task; positive signal. | 8 comparators, 5 ablations, 5 contingency/scenario views. | Close enough to prioritize; missing contingency breadth. |
| P5 TRACE-MOEA | Multi-source proxy dataset and several baselines/ablations. | 7 comparators, 5 ablations, 4 review/cost/sensitivity views. | Quantity can be made adequate; label validity is the key weakness. |
| P6 BiLo-NSGA | Multi-source proxy dataset, budget-constrained evidence, stronger gain than P5. | 8 comparators, 5 ablations, 5 budget/dependency/seed views. | Algorithm experiment direction is promising; needs repeated-run and dependency data. |

## Dataset Sufficiency Ranking

| Rank | Paper | Rationale |
| ---: | --- | --- |
| 1 | P2 HyG-LoadFormer | OPSD + SimBench with fixed and rolling splits is the closest to target-journal dataset sufficiency. |
| 2 | P1 DSTAR-GRU | RTS-GMLC is credible, and stress splits help, but OPF/UC/Grid2Op feasibility is still missing. |
| 3 | P4 SHIELD-MOEA | SimBench resilience proxy is useful, but needs explicit outage/contingency datasets and feasibility evidence. |
| 4 | P6 BiLo-NSGA | Public proxy evidence is useful for optimization, but real review/dependency labels are missing. |
| 5 | P5 TRACE-MOEA | Multi-source proxy is traceable, but feasibility-review labels and calibrated costs are missing. |
| 6 | P3 CARS-MODE | Current SimBench DER/storage proxy is narrow and must add AC load-flow plus scenario variance. |

## Practical Submission Readiness

| Paper | Dataset Readiness | Experiment Strength | First-Round Submission Risk |
| --- | --- | --- | --- |
| P1 DSTAR-GRU | Medium | Medium-low | High unless feasibility validation is added. |
| P2 HyG-LoadFormer | High for 24h; medium for 1h | Medium-high | Moderate; strongest near-term manuscript if scoped to day-ahead. |
| P3 CARS-MODE | Low-medium | Low-medium | High; needs planning feasibility evidence. |
| P4 SHIELD-MOEA | Medium | Medium | Moderate-high; can improve quickly with contingency variance. |
| P5 TRACE-MOEA | Medium as proxy; low as expert-review dataset | Medium-low | High unless label boundary is explicit or expert labels are added. |
| P6 BiLo-NSGA | Medium as proxy | Medium | Moderate-high; needs seed/convergence/dependency experiments. |

## Immediate Upgrade Targets

1. P2: keep as strongest near-term paper; add LightGBM/XGBoost, TCN/N-BEATS/N-HiTS/PatchTST only if claiming short-horizon competitiveness.
2. P4: add N-1/N-k contingency scenario variance and feasibility metrics; this can push it close to Energies-level strength.
3. P6: add seed variance, convergence curves, budget sensitivity, and dependency-aware project labels.
4. P1: add DC-OPF/UC/PGLib/Grid2Op validation before strong dispatch claims.
5. P3: add pandapower/AC load-flow and DER-hosting variance.
6. P5: add expert-labeled or rule-audited review outcomes and cost calibration.
