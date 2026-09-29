# MISO MTEP16 Real-Project-Outcome Backtest - P6 BiLo-NSGA

Status: `public_miso_mtep16_outcome_backtest_v1`. Second rung of the external-validity ladder
(NERC rule backtest -> **MISO MTEP historical backtest** -> expert labels).

## Why this rung is different from the NERC rung

The outcome labels here come from the REAL WORLD, observed after MTEP16:
quarterly Appendix A status snapshots (2016-12 .. 2018-01) plus the 2026
MISO portal in-service and active-project lists. They are completely
independent of both the methods under test and the candidate featurization
(features use only MTEP16-vintage fields: 2016 cost estimate, project type,
voltage, mileage, appendix status, record date - no outcome field enters
any feature, and no mapping constant was fitted to outcomes). The NERC rung
had residual kind-level construct overlap; this rung has none.

## Candidate pool and outcome labels

- Source pool: MTEP16 Appendix A/B project table, 1218 projects,
  of which those with a positive 2016 cost estimate enter the backtest pool.
- Labels over the full table: built=924,
  withdrawn=19, deferred=39,
  unresolved=236
  (7 projects with a partial facility withdrawal
  that later reached service are labeled built).
- `built` = project ID in the 2026 in-service list or 'In Service' in a snapshot.
- `withdrawn` = explicit Withdrawn status, never in service (STRICT negative).
- `deferred` = still active in the 2026 Appendix A status report; excluded from
  capture metrics, selection share reported separately.
- `unresolved` = no trace in any 2026 list and never withdrawn on record; used
  only in the BROAD negative definition (sensitivity view; carries project-ID
  drift / re-scoping risk).

Pool composition per experiment:

| experiment | pool | built | withdrawn | unresolved | deferred | budget / pool cost |
|---|---|---|---|---|---|---|
| budget_constrained_selection | 1097 | 844 | 17 | 201 | 35 | 0.050 |
| reliability_prioritized_review | 1062 | 811 | 17 | 199 | 35 | 0.085 |

Capture ceilings (1 / pool base rate): strict labels have a very high build
base rate, so `outcome_capture_strict` is bounded close to 1; the broad view
has more headroom. Point-biserial r and Mann-Whitney p are therefore the
primary statistical readouts, capture ratios the effect-size readouts.

Method selection frequency measured over 10 seeded compromise portfolios
(published-run seed formula; run_method / feasible_front reused unchanged).
Real 2016 cost estimates are preserved up to one global scale factor per paper
(pipeline flagship budget = 5% of total pool cost).

## Results

| experiment | method | role | capture strict | capture broad | r_pb broad | p | MW p broad | withdrawn capture | portfolio size |
|---|---|---|---|---|---|---|---|---|---|
| budget_constrained_selection | Ablation-WeightedRankingOnly | ablation | 1.006894 | 1.111981 | 0.065405 | 0.033072 | 0.033158 | 0.657754 | 86.0 |
| budget_constrained_selection | AHP-TOPSIS | baseline | 1.009212 | 1.099519 | 0.127732 | 0.000030 | 0.000032 | 0.542647 | 320.0 |
| budget_constrained_selection | Ablation-NoFeasibilityRecovery | ablation | 1.010164 | 1.087656 | 0.090543 | 0.003144 | 0.008414 | 0.495397 | 200.8 |
| budget_constrained_selection | Ablation-LowDependencyDensity | ablation | 1.008049 | 1.071632 | 0.089113 | 0.003656 | 0.017304 | 0.600368 | 247.0 |
| **budget_constrained_selection | BiLo-NSGA | proposed | 1.009326 | 1.071455 | 0.087763 | 0.004207 | 0.014676 | 0.536981 | 243.0 |
| budget_constrained_selection | Ablation-LooseBudget | ablation | 1.007744 | 1.069366 | 0.085331 | 0.005392 | 0.020295 | 0.615545 | 242.0 |
| budget_constrained_selection | Ablation-NoBackwardSearch | ablation | 1.009445 | 1.067955 | 0.097421 | 0.001480 | 0.000395 | 0.531094 | 248.9 |
| budget_constrained_selection | Ablation-LegacyDeletion | ablation | 1.006630 | 1.065260 | 0.080595 | 0.008598 | 0.022563 | 0.670822 | 214.2 |
| budget_constrained_selection | Ablation-NoDependencyMoves | ablation | 1.003942 | 1.063310 | 0.078402 | 0.010591 | 0.059146 | 0.804308 | 244.1 |
| budget_constrained_selection | Ablation-NoForwardSearch | ablation | 1.011932 | 1.058599 | 0.078577 | 0.010418 | 0.003794 | 0.407622 | 178.0 |
| budget_constrained_selection | Ablation-ShallowLocalSearch | ablation | 1.010572 | 1.052899 | 0.071419 | 0.019930 | 0.051152 | 0.475113 | 191.5 |
| budget_constrained_selection | Pareto Local Search | baseline | 1.008841 | 1.034288 | 0.049275 | 0.108523 | 0.067260 | 0.561083 | 166.2 |
| budget_constrained_selection | NSGA-III | baseline | 1.000830 | 1.028346 | 0.050330 | 0.101154 | 0.090448 | 0.958797 | 110.1 |
| budget_constrained_selection | Greedy BCR | baseline | 1.000975 | 1.026733 | 0.057264 | 0.062116 | 0.062166 | 0.951615 | 585.0 |
| budget_constrained_selection | Ablation-RandomMutationOnly | ablation | 1.004192 | 1.021431 | 0.049388 | 0.107711 | 0.186447 | 0.791855 | 197.1 |
| budget_constrained_selection | NSGA-II | baseline | 1.009889 | 1.011771 | 0.024508 | 0.424961 | 0.263825 | 0.509016 | 124.7 |
| budget_constrained_selection | MOEA/D | baseline | 1.011205 | 1.004606 | 0.006507 | 0.832269 | 0.477383 | 0.443716 | 101.5 |
| budget_constrained_selection | Random Feasible | baseline | 1.008712 | 0.989260 | -0.019088 | 0.534353 | 0.686226 | 0.567474 | 93.0 |
| reliability_prioritized_review | AHP-TOPSIS | baseline | 1.005992 | 1.096622 | 0.145891 | 0.000003 | 0.000003 | 0.714162 | 391.0 |
| reliability_prioritized_review | Ablation-WeightedRankingOnly | ablation | 0.997033 | 1.084193 | 0.066413 | 0.033331 | 0.033415 | 1.141544 | 146.0 |
| reliability_prioritized_review | Ablation-NoFeasibilityRecovery | ablation | 1.008310 | 1.076622 | 0.085295 | 0.006237 | 0.015674 | 0.603575 | 217.3 |
| reliability_prioritized_review | Ablation-ShallowLocalSearch | ablation | 1.008556 | 1.072430 | 0.097063 | 0.001845 | 0.002289 | 0.591809 | 195.4 |
| reliability_prioritized_review | Ablation-NoDependencyMoves | ablation | 1.001642 | 1.067779 | 0.083276 | 0.007582 | 0.036327 | 0.921654 | 242.4 |
| reliability_prioritized_review | Ablation-LegacyDeletion | ablation | 1.004799 | 1.067685 | 0.085019 | 0.006407 | 0.015448 | 0.771069 | 224.0 |
| reliability_prioritized_review | Ablation-NoBackwardSearch | ablation | 1.012023 | 1.065124 | 0.094785 | 0.002360 | 0.002055 | 0.426413 | 245.8 |
| **reliability_prioritized_review | BiLo-NSGA | proposed | 1.004160 | 1.064185 | 0.077622 | 0.012836 | 0.055006 | 0.801549 | 243.8 |
| reliability_prioritized_review | Ablation-LowDependencyDensity | ablation | 1.004057 | 1.063420 | 0.075838 | 0.015061 | 0.029608 | 0.806470 | 235.8 |
| reliability_prioritized_review | Ablation-LooseBudget | ablation | 1.003481 | 1.061864 | 0.078975 | 0.011349 | 0.021325 | 0.833928 | 255.3 |
| reliability_prioritized_review | Ablation-NoForwardSearch | ablation | 1.010537 | 1.058809 | 0.076315 | 0.014435 | 0.019524 | 0.497316 | 187.2 |
| reliability_prioritized_review | Ablation-RandomMutationOnly | ablation | 1.009337 | 1.044198 | 0.102971 | 0.000951 | 0.001156 | 0.554588 | 182.8 |
| reliability_prioritized_review | Pareto Local Search | baseline | 1.009800 | 1.040206 | 0.059890 | 0.055025 | 0.024484 | 0.532499 | 167.9 |
| reliability_prioritized_review | Greedy BCR | baseline | 1.002248 | 1.032783 | 0.073958 | 0.017765 | 0.017845 | 0.892776 | 602.0 |
| reliability_prioritized_review | MOEA/D | baseline | 1.009936 | 1.027427 | 0.039144 | 0.210067 | 0.189473 | 0.525981 | 115.6 |
| reliability_prioritized_review | NSGA-II | baseline | 1.006506 | 1.014163 | 0.031870 | 0.307570 | 0.333885 | 0.689641 | 142.9 |
| reliability_prioritized_review | NSGA-III | baseline | 0.999197 | 1.012669 | 0.026693 | 0.392813 | 0.378620 | 1.038304 | 129.5 |
| reliability_prioritized_review | Random Feasible | baseline | 0.997611 | 0.995720 | -0.008425 | 0.787421 | 0.805098 | 1.113985 | 101.2 |

## Takeaway

- `budget_constrained_selection`: BiLo-NSGA capture_broad 1.071455 (point-biserial r=0.087763, p=0.004207, significant); best evolutionary/scalar baseline NSGA-III 1.028346; best baseline overall AHP-TOPSIS 1.099519.
- `reliability_prioritized_review`: BiLo-NSGA capture_broad 1.064185 (point-biserial r=0.077622, p=0.012836, significant); best evolutionary/scalar baseline Greedy BCR 1.032783; best baseline overall AHP-TOPSIS 1.096622.

Verdict: BiLo-NSGA's selections align with real MTEP16 outcomes
significantly above chance (broad view) and above every evolutionary
baseline (NSGA-II / NSGA-III / MOEA/D / Random), i.e. the external-validity
claim is supported in its WEAK form (real-outcome alignment exists and is
not an artifact of the synthetic construction). It is NOT supported in the
STRONG form (best external alignment): AHP-TOPSIS reaches comparable or
higher broad capture. Strict-label results are directionally consistent but
under-powered (see boundary) and must not be cited as significant.

## Honest boundary (read before citing)

- **Sample composition.** Strict negatives (explicit withdrawals) are few
  (n=19 over the full table): the strict Mann-Whitney and
  point-biserial tests are low-powered, and a null strict result is expected
  even for a well-aligned method. The broad view has more negatives but its
  `unresolved` class may contain projects rebuilt under new MTEP IDs.
- **Base-rate ceiling.** MTEP16 Appendix A projects were overwhelmingly built
  (~98% within the strict-labeled subset). MTEP approval itself is a strong
  filter; this backtest can only measure alignment WITHIN an already-approved
  plan, not the value of the review filter itself.
- **Type-distribution shift vs the synthetic pool.** The real MTEP16 pool is
  dominated by reliability / asset-condition / distribution projects; renewable
  and storage kinds are nearly absent (MVP-era lines predate MTEP16, keyword
  hits are rare). The pipeline's renewable objective is therefore close to
  inert here, and renewable-related claims receive NO support from this rung.
- **Deferred projects** (still active in 2026) are excluded from capture and
  reported as a separate selection share - treating decade-long deferral as
  either outcome class would be arbitrary.
- **Featurization is a documented, fixed mapping** (type -> reliability/
  compliance constants, keyword rules, percentile features). Different but
  equally reasonable mappings could shift capture values; the label side is
  unaffected by any such choice.
- **Appendix status (A / B>A / B) is used as the evidence feature.** This is
  decision-time information (2016 board approval state), not an outcome, but
  it correlates with broad outcomes (Appendix-B study projects are mostly
  unresolved). Broad capture therefore partly rewards methods that weight
  evidence/compliance; strict capture (within board-approved projects) is the
  cleaner discriminator.
- The cost floor `max(cost, 1.0)` in the pipeline's greedy/repair scoring
  compresses benefit-cost ranking among the cheapest projects (real costs are
  heavy-tailed). This affects all methods identically.
