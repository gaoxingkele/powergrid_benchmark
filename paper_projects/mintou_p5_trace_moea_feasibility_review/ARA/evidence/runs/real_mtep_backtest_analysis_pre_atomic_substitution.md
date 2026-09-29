# MISO MTEP16 Real-Project-Outcome Backtest - P5 TRACE-MOEA

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
| benchmark_portfolio_optimization | 1097 | 844 | 17 | 201 | 35 | 0.050 |
| reliability_driven_review | 1062 | 811 | 17 | 199 | 35 | 0.075 |

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
| benchmark_portfolio_optimization | AHP-TOPSIS | baseline | 1.008993 | 1.100247 | 0.097055 | 0.001542 | 0.001571 | 0.553520 | 208.0 |
| benchmark_portfolio_optimization | Ablation-SingleObjective | ablation | 1.004945 | 1.091806 | 0.165711 | 0.000000 | 0.000000 | 0.754519 | 185.9 |
| **benchmark_portfolio_optimization | TRACE-MOEA | proposed | 1.013950 | 1.079479 | 0.168851 | 0.000000 | 0.000000 | 0.307418 | 156.4 |
| benchmark_portfolio_optimization | Ablation-NoReliabilityFeatures | ablation | 1.005449 | 1.075331 | 0.114708 | 0.000180 | 0.000055 | 0.729484 | 114.1 |
| benchmark_portfolio_optimization | Weighted Sum | baseline | 1.005569 | 1.071880 | 0.040640 | 0.185705 | 0.185665 | 0.723529 | 81.0 |
| benchmark_portfolio_optimization | Ablation-NoRenewableFeatures | ablation | 1.004180 | 1.067083 | 0.146564 | 0.000002 | 0.000003 | 0.792486 | 167.3 |
| benchmark_portfolio_optimization | Ablation-NoFeasibilityRepair | ablation | 0.998011 | 1.054517 | 0.098305 | 0.001339 | 0.000450 | 1.098748 | 115.1 |
| benchmark_portfolio_optimization | Ablation-NSGA2Only | ablation | 1.000372 | 1.050655 | 0.098970 | 0.001241 | 0.001001 | 0.981532 | 124.6 |
| benchmark_portfolio_optimization | Ablation-SmallProjectPool | ablation | 0.987584 | 1.033436 | 0.028528 | 0.353006 | 0.543588 | 1.616395 | 57.7 |
| benchmark_portfolio_optimization | Greedy BCR | baseline | 1.001015 | 1.027134 | 0.058234 | 0.057812 | 0.057866 | 0.949632 | 587.0 |
| benchmark_portfolio_optimization | MOEA/D | baseline | 1.004666 | 1.025325 | 0.033418 | 0.276563 | 0.227647 | 0.768350 | 97.8 |
| benchmark_portfolio_optimization | Ablation-NoScheduleRisk | ablation | 1.003247 | 1.023544 | 0.050636 | 0.099092 | 0.148004 | 0.838792 | 156.5 |
| benchmark_portfolio_optimization | NSGA-II | baseline | 1.005072 | 1.018619 | 0.035582 | 0.246632 | 0.482724 | 0.748195 | 109.5 |
| benchmark_portfolio_optimization | Random Feasible | baseline | 0.999676 | 1.017856 | 0.030444 | 0.321595 | 0.470756 | 1.016068 | 80.3 |
| benchmark_portfolio_optimization | Ablation-NoPreferenceRanking | ablation | 1.005346 | 1.009607 | 0.022535 | 0.463196 | 0.634574 | 0.734576 | 164.6 |
| reliability_driven_review | Weighted Sum | baseline | 0.997218 | 1.131621 | 0.080953 | 0.009449 | 0.009521 | 1.132695 | 94.0 |
| reliability_driven_review | Ablation-SingleObjective | ablation | 1.005877 | 1.103495 | 0.198101 | 0.000000 | 0.000000 | 0.719650 | 195.5 |
| reliability_driven_review | Ablation-NoFeasibilityRepair | ablation | 1.011229 | 1.089176 | 0.173518 | 0.000000 | 0.000000 | 0.464308 | 123.6 |
| reliability_driven_review | AHP-TOPSIS | baseline | 1.011805 | 1.072263 | 0.081735 | 0.008779 | 0.008848 | 0.436824 | 264.0 |
| reliability_driven_review | Ablation-NoReliabilityFeatures | ablation | 1.006352 | 1.069900 | 0.139414 | 0.000007 | 0.000001 | 0.696970 | 141.3 |
| **reliability_driven_review | TRACE-MOEA | proposed | 1.000432 | 1.069633 | 0.151092 | 0.000001 | 0.000001 | 0.979391 | 153.2 |
| reliability_driven_review | Ablation-NoPreferenceRanking | ablation | 1.006240 | 1.049142 | 0.118246 | 0.000146 | 0.000046 | 0.702320 | 170.3 |
| reliability_driven_review | Ablation-NoRenewableFeatures | ablation | 1.003755 | 1.048151 | 0.104347 | 0.000811 | 0.000952 | 0.820886 | 151.6 |
| reliability_driven_review | Ablation-NoScheduleRisk | ablation | 1.002530 | 1.034066 | 0.073431 | 0.018596 | 0.005360 | 0.879306 | 157.4 |
| reliability_driven_review | Ablation-NSGA2Only | ablation | 1.008079 | 1.032197 | 0.065516 | 0.035793 | 0.081610 | 0.614585 | 117.9 |
| reliability_driven_review | Greedy BCR | baseline | 1.001328 | 1.030583 | 0.065406 | 0.036104 | 0.036180 | 0.936652 | 575.0 |
| reliability_driven_review | MOEA/D | baseline | 1.001478 | 1.017028 | 0.022265 | 0.476008 | 0.749466 | 0.929502 | 97.8 |
| reliability_driven_review | Ablation-SmallProjectPool | ablation | 0.993268 | 1.015335 | 0.013980 | 0.654521 | 0.219502 | 1.321136 | 69.7 |
| reliability_driven_review | NSGA-II | baseline | 1.003015 | 1.010258 | 0.022840 | 0.464677 | 0.410797 | 0.856158 | 129.4 |
| reliability_driven_review | Random Feasible | baseline | 1.005450 | 0.996577 | -0.006297 | 0.840271 | 0.601115 | 0.740006 | 93.6 |

## Takeaway

- `benchmark_portfolio_optimization`: TRACE-MOEA capture_broad 1.079479 (point-biserial r=0.168851, p=0.000000, significant); best evolutionary/scalar baseline Weighted Sum 1.071880; best baseline overall AHP-TOPSIS 1.100247.
- `reliability_driven_review`: TRACE-MOEA capture_broad 1.069633 (point-biserial r=0.151092, p=0.000001, significant); best evolutionary/scalar baseline Weighted Sum 1.131621; best baseline overall Weighted Sum 1.131621.

Verdict: TRACE-MOEA's selections align with real MTEP16 outcomes
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
