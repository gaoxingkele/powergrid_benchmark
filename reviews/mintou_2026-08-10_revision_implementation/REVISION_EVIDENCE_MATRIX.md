# Mintou Six-Paper Revision Evidence Matrix

Date: 2026-08-10  
Scope: the latest `paper_projects/mintou_p*/manuscript/MANUSCRIPT.md` files and the corresponding code/evidence under `papers/mintou/mintou_p*`.

## Integrity rules

1. Existing run CSV files are immutable evidence. New experiments must use a new run identifier and new output paths.
2. Manuscript numbers may be copied only from machine-readable evidence or from a newly completed run with a frozen configuration.
3. GPT Image 2 outputs are visual style masters only. Final algorithm diagrams are reconstructed as editable SVG and vector PDF, with labels checked against code and equations.
4. Negative and null ablations remain in the abstract, results, and conclusion where they delimit the contribution.
5. No method is described as state of the art. Claims are limited to the evaluated data, scenarios, budgets, seeds, and metrics.

## P1 — DSTAR-GRU curtailment benchmark (IEEE Access)

- Revision objective: strengthen the benchmark and mechanism-characterization contribution without claiming forecasting superiority.
- Frozen evidence: `real_curtailment_results.csv`, `real_curtailment_leaderboard.csv`, `real_curtailment_significance.csv`, figure JSON files, and the v5 onset-evaluation configuration.
- Formalization target: reference-policy curtailment target; temporal split; onset event; GRU state; Siamese/metric loss; neighbor retrieval; head–retrieval blend; MAE/F1 definitions.
- Diagram target: public time series → method-independent target → temporal windows → GRU/metric embedding → retrieval bank and prediction head → horizon/onset evaluation.
- Existing plots retained: benchmark overview, horizon leaderboard, retrieval scale-dependency result.
- Experiment decision: preserve the honest result that persistence/ridge can lead. Add a recent forecasting baseline only if it can be run under the identical split, target, and seed protocol; otherwise state the benchmark’s baseline limitation explicitly.

## P2 — CSA-LoadNet / cross-series load forecasting (Electronics)

- Revision objective: make the cross-series aggregation mechanism reproducible and demote hyperbolic geometry from a success claim where the ablation does not support it.
- Frozen evidence: OPSD, SimBench, and Ausgrid v7 run files and their current leaderboard/significance tables.
- Formalization target: temporal encoder; series embedding; pairwise distance; attention weights; curvature/Euclidean switch; context fusion; prediction loss; training and inference complexity.
- Diagram target: multi-region histories and calendar features → shared encoder → cross-series attention geometry → context fusion → 1 h/24 h heads → multi-dataset statistics.
- Existing plots retained: pooled leaderboard, component analysis, Ausgrid transfer result.
- Experiment decision: do not multiply similar ablations. Prefer a hierarchical-reconciliation comparator or a clearly justified scope limitation; unequal Ausgrid seed counts must be visible wherever reported.

## P3 — CARS-MODE / self-adaptive MODE planning (Energies)

- Revision objective: raise optimization-method formal density and distinguish the valid planning contribution from the null proxy-HV contribution of strategy adaptation.
- Frozen evidence: `real_simbench_planning_results.csv`, leaderboard/significance, sensitivity sweep, and AC-validation files.
- Formalization target: binary multiobjective model; constraint dominance; jDE parameter update; strategy sampling; binary decoding; budget repair; crowding/archive update; hypervolume.
- Diagram target: SimBench candidates → adaptive DE population → strategy/parameter update → decoding and repair → constrained selection/archive → standard HV and AC validation.
- Existing plots retained: HV distribution, ablation, sensitivity, AC validation.
- Experiment decision: a direct adaptive-DE baseline (JADE/SHADE family) is valuable only if implemented with the same encoding, repair, evaluation budget, and seeds. AC results remain a consistency check unless the independent-plan sample is expanded.

## P4 — SHIELD-MOEA resilience planning (Energies)

- Revision objective: close the mathematical loop between scenario risk, worst-K screening, hybrid variation, repair, and robust evaluation.
- Frozen evidence: current SimBench planning, sensitivity, and AC-validation result sets; deprecated proxy-method files remain excluded.
- Formalization target: scenario objectives; population-dependent worst-K score; screening set; GA/DE mixture; feasibility repair; mean/worst-case selection; evaluation-count and wall-clock accounting.
- Diagram target: candidate grid and uncertainty scenarios → population-dependent screening → GA/DE variation → repair → robust selection → unseen-stress and AC checks.
- Existing plots retained: HV distribution, ablation, sensitivity, AC validation.
- Experiment decision: prioritize GA-only, DE-only, and fixed-scenario-screening controls. Any economy claim requires real objective-call and wall-clock measurements, not a proxy count.

## P5 — TRACE-MOEA project review (Energies)

- Revision objective: center the defensible innovation on feasibility repair plus a quarantined audit archive; treat preference adaptation as auxiliary because its isolated gain is small.
- Frozen evidence: 3150 main run records, 0.75× budget sweep, NERC rule backtest, and MISO MTEP16 outcome backtest.
- Formalization target: five-objective portfolio; preference response scalarization; adaptive weight-vector update; deterministic repair; constrained sorting; trace-event schema and quarantine invariant; hypervolume.
- Diagram target: public candidate derivation → five-objective constrained population → preference layer and repair → NSGA-II kernel → feasible front, with a one-way quarantined trace-output branch.
- Existing plots retained: HV distribution, component ablation, external-validity ladder.
- Experiment decision: add a genuine preference-based MOEA comparator only under identical objectives, repair, budget, and evaluation count. LLM annotations, if later used, are auxiliary labels and must never be called expert adjudication.

## P6 — BiLo-NSGA project review (Applied Sciences)

- Revision objective: formalize local-search semantics and openly resolve the asymmetry that forward insertion contributes while backward deletion shows no HV gain.
- Frozen evidence: 3840 main/sensitivity runs, NERC rule and MTEP outcome backtests.
- Formalization target: four-objective binary portfolio; hard budget/dependency constraints; forward move; backward move; dependency bonus; acceptance/replacement rule; repair; time complexity.
- Diagram target: candidate portfolio → NSGA-II offspring → forward insertion / backward deletion → dependency-aware repair → environmental selection → front and audit output.
- Existing plots retained: HV distribution, ablation, budget sensitivity, NERC backtest.
- Experiment decision: use the existing forward-only ablation as the engineering comparator and add swap/look-ahead only as a separately named redesign if actually run. The title and contribution text must not imply symmetric measured gains.

## Required output set per paper

- One exact, editable algorithm/data-flow figure in SVG and vector PDF, plus a 300 dpi PNG preview.
- All existing statistical figures regenerated from their scripts and checked against the cited CSV rows.
- A compact notation table or symbol paragraph, sufficient equations for independent reimplementation, and algorithm pseudocode.
- A baseline/ablation table stating whether each comparator is external, internal, or a mechanism control; its tuning and evaluation budget must be explicit.
- An evidence-to-claim cross-check covering abstract, contribution list, results, limitations, conclusion, captions, and supplementary files.

## Submission gate

Technical revision can proceed, but final submission packaging remains blocked until authors confirm all author names/order/affiliations, corresponding-author email, funding statement, CRediT roles, conflicts, and persistent repository/DOI fields for every paper.
