# Mintou Six-Paper Experiment Strength Upgrade Plan

This file turns the current reviewer-facing gaps into execution targets. It is a planning and gating document, not a result table. Existing weak, mixed, and near-miss evidence must stay in each ARA trace.

## Portfolio Rules

| Rule | Requirement |
| --- | --- |
| Public-data sufficiency | Each paper should use at least two public or benchmark-derived data sources when the task naturally allows it. Single-dataset papers must add rolling, stress, or domain-shift splits. |
| Baseline sufficiency | Each paper should compare against at least 5 method families: simple heuristic, classical optimization/statistics, strong domain baseline, recent ML/evolutionary baseline, and task-specific ablation. |
| Ablation sufficiency | Each named algorithm component must have a matching removal or replacement condition. |
| Robustness sufficiency | Report at least one of rolling temporal splits, scenario variance, stress subsets, seed variance, or sensitivity analysis. |
| Engineering validity | Dispatch and planning papers must not make strong operational claims without OPF/load-flow feasibility checks. |
| Review-label validity | Feasibility-review papers must distinguish public proxy labels from expert-labeled approval outcomes. |
| Packaging boundary | Data optimization means broader public data coverage, calibrated task construction, stratified reporting, and clear claim scoping. It does not mean fabricated labels or hidden failed runs. |

## Priority Upgrade Matrix

| Paper | Current Sufficiency | Required Dataset Upgrade | Required Baseline Upgrade | Required Robustness Upgrade | Submission Gate |
| --- | --- | --- | --- | --- | --- |
| P1 DSTAR-GRU dispatch | RTS-GMLC fixed, rolling, and stress evidence; signal is positive but marginal. | Add one OPF-capable benchmark layer: PGLib-OPF/MATPOWER cases, DC-OPF feasibility, or Grid2Op-style topology scenarios. | Add OPF/UC-style comparator if feasible: DC-OPF economic dispatch, reserve-aware dispatch, topology-action heuristic, and learned dispatch proxy. | Feasibility violation rate, line overload rate, reserve shortfall, renewable curtailment, high-renewable/topology/ramp stress subsets. | Manuscript can claim similarity-aware dispatch assistance only after feasibility metrics are reported; no AC-OPF or UC superiority claim without direct validation. |
| P2 HyG-LoadFormer forecasting | OPSD and SimBench fixed/rolling evidence; day-ahead signal is strong, 1h remains weak. | Keep OPSD + SimBench as core; optionally add ENTSO-E national load or GEFCom-style load/weather if licensing and cache permit. | Add stronger forecasting comparators if short-horizon claims are needed: LightGBM/XGBoost lag features, TCN, N-BEATS/N-HiTS, DLinear/PatchTST, simple GNN temporal baseline. | Rolling windows by season/country/feeder; horizon-specific 1h/6h/24h/48h reporting; near-zero load robust metrics for SimBench. | Strongest claim should remain 24h/day-ahead hierarchical forecasting unless 1h improves against neural short-horizon baselines. |
| P3 CARS-MODE distribution planning | SimBench DER/storage stress proxy; narrow gain. | Add AC load-flow feasibility with pandapower/SimBench networks; add multiple DER penetration levels and storage cost scenarios. | Add NSGA-II, MOEA/D, SPEA2, multi-objective DE, greedy cost-benefit, random portfolio, and no-DER/no-storage ablations. | Repeat scenario variance over DER penetration, load growth, storage cost, and budget caps; report feasibility and hosting capacity separately from hypervolume proxy. | Energies-level claim needs AC feasibility or clearly scoped proxy wording. Hypervolume alone is insufficient for strong planning claims. |
| P4 SHIELD-MOEA resilience planning | SimBench resilience proxy; signal is better than P3. | Add outage/topology contingency sets from SimBench lines/transformers; add AC load-flow if available. | Add resilience-specific baselines: critical-load heuristic, redundancy-first heuristic, NSGA-II, MOEA/D, SPEA2, scenario-screening ablation, repair/no-repair ablation. | Scenario variance across N-1/N-k contingencies, high-load stress, DER outage stress, and budget limits. | Can be positioned as the stronger planning paper if contingency variance and feasibility reporting are added. |
| P5 TRACE-MOEA feasibility review | RTS-GMLC + SimBench + NERC/C2GES report-cache proxy; lacks expert labels. | Add a small expert-labeled or rule-audited review set: approval/reject/risk categories, cost assumptions, dependency tags, and traceable evidence fields. | Add AHP, TOPSIS, AHP-TOPSIS, weighted-sum, NSGA-II, MOEA/D, random portfolio, single-objective ablation, no-traceability ablation. | Sensitivity to cost calibration, criterion weights, budget caps, risk penalties, and label noise. | Strong claim requires expert or rule-audited review outcomes. Until then, call it a reproducible review proxy benchmark. |
| P6 BiLo-NSGA project review | Same proxy family as P5; stronger optimization gain than P5. | Add dependency-aware project portfolio labels: mutually exclusive projects, prerequisite relations, regional budget caps, and staged investment periods. | Add NSGA-II, NSGA-III if many objectives, MOEA/D, SPEA2, greedy budget, AHP-TOPSIS, local-search ablations, direction-only ablations. | Seed variance, budget sensitivity, dependency-density sensitivity, and local-search step-depth sensitivity. | Good Applied Sciences/IEEE Access candidate after dependency labels and repeated-seed stability are added. |

## Minimum Experiment Counts

| Paper | Minimum Main Comparators | Minimum Ablations | Minimum Dataset/Split Views | Minimum Tables/Figures |
| --- | ---: | ---: | ---: | --- |
| P1 DSTAR-GRU | 7 | 4 | 4 | Main leaderboard, stress leaderboard, feasibility table, ablation table, sensitivity figure |
| P2 HyG-LoadFormer | 8 | 4 | 6 | Dataset summary, horizon table, rolling table, neural baseline table, ablation table, error distribution figure |
| P3 CARS-MODE | 7 | 5 | 5 | Planning-objective table, feasibility table, DER-stress table, ablation table, Pareto/frontier figure |
| P4 SHIELD-MOEA | 8 | 5 | 5 | Resilience leaderboard, contingency table, feasibility table, ablation table, scenario variance figure |
| P5 TRACE-MOEA | 7 | 5 | 4 | Criteria table, review-outcome table, cost sensitivity table, ablation table, traceability case table |
| P6 BiLo-NSGA | 8 | 5 | 5 | Portfolio leaderboard, dependency sensitivity table, budget sensitivity table, ablation table, convergence figure |

## Execution Priority

1. P2: Add stronger neural baselines only if the manuscript wants 1h claims. Otherwise keep the paper focused on day-ahead forecasting and improve presentation.
2. P4: Add contingency variance and feasibility metrics; this is the fastest route to a strong planning paper.
3. P6: Add dependency-aware portfolio labels and seed variance; current gain is already attractive.
4. P1: Add OPF/Grid2Op feasibility before any strong dispatch wording.
5. P3: Add AC load-flow and DER-hosting scenario variance; otherwise keep claims narrow.
6. P5: Add expert or rule-audited review labels before claiming real feasibility-review decision support.

## Acceptance Checklist

- [ ] Every paper has a data-card paragraph naming source layer, label layer, task construction, and known limitations.
- [ ] Every paper has at least one robustness or variance table.
- [ ] Every algorithm name maps to testable components in ablation tables.
- [ ] Every public-data claim points to files under the paper's `evidence/` directory.
- [ ] Every proxy label is called a proxy label unless expert verification is available.
- [ ] Every failed or weak run remains discoverable in `trace/` or `evidence/runs/`.
