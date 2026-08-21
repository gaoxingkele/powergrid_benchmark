# Mintou Six-Paper Above-Mean Enhancement Protocol

Status: frozen before any enhancement run  
Date: 2026-08-11 (Asia/Shanghai)  
Scope: scientific supplementation of the six current journal manuscripts  

## Non-negotiable evidence rules

1. Existing main, weak, near-miss, deprecated, and failed runs remain in place.
2. Enhancement results are reported irrespective of direction or statistical significance.
3. No method-specific target, metric, normalization bound, test set, or stopping rule may be changed after observing enhancement results.
4. Hyperparameters below are fixed from the existing shared budgets or from a cited algorithm's standard form. There is no result-driven search.
5. Main comparisons retain two-sided Mann--Whitney U tests with Holm correction within the declared comparison family. Effect size and confidence intervals accompany p-values where the available samples permit them.
6. A new dataset or baseline may strengthen only the claim it directly tests. It does not retroactively upgrade unrelated deployment, expert-label, economic-calibration, or causal claims.

## P1: IEEE Access / curtailment-risk benchmark

- Independent dataset: NREL-118 day-ahead load, wind, and solar time series, joined by timestamp and evaluated with the same 70% reference acceptance-cap construction, 48 h input window, 70/15/15 chronological split, horizons 1 h and 24 h, and onset threshold rule.
- Modern controls: DLinear and a causal TCN, trained with the same optimizer, epoch ceiling, validation checkpointing, seeds, features, and clipping rule as the existing learned models.
- Runs: ten fixed seeds for each stochastic method; deterministic methods remain single-run.
- Primary readout: curtailment-rate MAE; secondary readouts: onset F1, onset MAE, RMSE, and runtime.
- Decision rule: report whether the RTS-GMLC retrieval sign reversal transfers; do not require or imply that it must transfer.

## P2: Electronics / hierarchical load forecasting

- Dataset correction: rebuild Ausgrid as an exact hierarchy containing the 12 selected complete customers, four deterministic postcode-group aggregates formed only from those 12 customers, and their exact system sum. Preserve the previous all-customer aggregate cache/results as superseded provenance.
- Reconciliation controls: independently forecast every node, then evaluate Base, Bottom-Up, Top-Down, and OLS/MinT-style projection reconciliation on the exact summing matrix. Reconciliation parameters use training/validation data only.
- Seed fairness: use the same ten fixed seeds for HyG-LoadFormer, all neural ablations, MLP, DLinear, TCN, PatchTST-lite, and LSTM on the corrected Ausgrid benchmark.
- Primary readout: hierarchy-weighted sMAPE and coherence violation; secondary readouts: level-specific sMAPE/MAE and runtime.
- Decision rule: distinguish forecasting accuracy from coherence. A reconciliation method is not declared superior unless it improves the declared primary accuracy metric without violating exact coherence.

## P3: Energies / CARS-MODE

- Direct differential-evolution controls: binary-decoded GDE3 and NSDE under population 40, 40 generations, identical low-density initialization, budget constraint, scenario sets, normalization bounds, and 30 seeds.
- Existing seven planning experiments and AC validation protocol remain unchanged.
- Primary readout: method-independent feasible-front hypervolume; secondary readouts: feasible-front size, runtime, planning-target diagnostics, worst-scenario readouts, and AC composition back-check.
- Decision rule: CARS-MODE may be described as stronger than the implemented adaptive/multiobjective-DE family only where the corrected per-experiment comparisons support that statement.

## P4: Energies / SHIELD-MOEA

- Independent AC network extension: retain the four SimBench MV networks and add pandapower's CIGRE MV network and IEEE 33-bus case as separately labelled external network families.
- Apply the already frozen composition-to-network mapping and six stress scenarios without network-specific tuning.
- Preserve the completed GA-only, DE-only, and fixed-worst-K mechanism-control runs.
- Primary readout: AC-feasible rate by network family; secondary readouts: convergence, voltage-band violations, line overloads, losses, and stress-only feasibility.
- Decision rule: the extension tests composition transfer only; it remains distinct from optimizer-controlled nodal siting and field deployment.

## P5: Energies / TRACE-MOEA

- Direct preference-based comparator: R-NSGA-II with one scenario-derived reference point, the same binary operators, population 40, 40 generations, budget constraint, and 30 seeds.
- Preference readout: report both global feasible-front hypervolume and a predeclared normalized achievement distance to the scenario reference point.
- Sensitivity: retain 0.75x budget evidence and add 1.00x and 1.25x comparison for TRACE-MOEA, R-NSGA-II, and NSGA-II only; no preference-layer tuning is permitted.
- Primary readout: global hypervolume; secondary readouts: achievement distance, runtime, trace coverage, and budget sensitivity.
- Decision rule: do not claim preference-family superiority unless both the global and preference-region evidence support it; otherwise present R-NSGA-II as a boundary-defining control.

## P6: Applied Sciences / BiLo-NSGA

- Algorithm revision: replace isolated greedy backward deletion with an atomic backward-forward substitution. The move removes the lowest benefit-cost selected project, evaluates one highest-scoring feasible replacement under the released dependency rule, and accepts the pair only when the fixed normalized scalar fitness improves. The deletion and insertion are logged as one substitution event.
- Direct local-search comparator: multi-start Pareto Local Search using add, delete, and swap moves under the same project representation and a fixed 1600-neighbour evaluation budget per seed.
- Controls: revised full method, forward-only, legacy greedy deletion, no-dependency, no-repair, NSGA-II, NSGA-III, MOEA/D, and Pareto Local Search; all existing negative results remain available.
- Runs: eight experiments, 30 fixed seeds, unchanged objective definitions, budgets, normalization, and final evaluation.
- Primary readout: feasible-front hypervolume; secondary readouts: runtime, accepted move types, decision coverage, feasible-front size, and budget-stratified performance.
- Decision rule: retain a bidirectional-performance claim only if the atomic substitution contributes measurable value. If it does not, the title and abstract must be revised to a forward-dominant local-search framework while preserving the null result.

## Execution and manuscript gate

For every paper: smoke test -> complete run in a new versioned output path -> statistical validation -> figure/table regeneration -> manuscript patch -> journal-template PDF rebuild -> reference/data/claim integrity audit. A failed run is retained and not silently retried. External journal submission remains blocked until author metadata, CRediT, funding/APC fields, and the final author approval are complete.
