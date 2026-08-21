# Claims

## C01: Penalty terms in a dispatch fitness function decouple the optimizer's objective scale from real operating cost while encoding non-monetary operating goals
- **Statement**: Folding power-quality and equipment-longevity penalties (main-grid exchange excursions; start/end ESS energy imbalance) into a single fitness function makes the optimized fitness value numerically distinct from the system's actual monetary cost, but lets one optimizer trade pure economics against operationally-desirable behaviour that a cost-only objective cannot express.
- **Conditions**: Holds for a weighted-sum multi-objective dispatch objective that adds penalty terms to cost terms; the paper does not report a sensitivity study of the penalty coefficients, so the regime of coefficient magnitudes over which the decoupling stays benign is untested.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Exhibit an MGC dispatch where minimizing the penalty-augmented fitness produces a schedule that violates the power-quality / ESS-cycle goals the penalties encode (e.g. large start/end ESS imbalance) no less than minimizing a cost-only objective would — i.e. the penalty terms fail to steer the solution.
- **Proof**: [E03, E04]
- **Evidence basis**: §2.3 objective (Eq. 8) and its penalty terms (Eqs. 13-15); the §4.3.1 note that "the fitness value and the actual daily cost ... are not numerically equivalent"; Table A1 (actual daily costs differ from Table 5 fitness values); Table A4 cost breakdown. Do not restate the values here — see the evidence files.
- **Tags**: objective-function, penalty, multi-objective, power-quality

## C02: A leader-averaging swarm update buys exploitation at the cost of population diversity, creating the structural opening for a diversity-restoring operator
- **Statement**: Guiding all subordinate agents toward the average pull of the current best trio (α/β/δ) concentrates the search near the incumbent optimum, so such hierarchical leader-guided updates gain exploitation strength but lose exploratory diversity — which is why bolting a diversity-injecting mechanism onto the base update improves late-stage escape from local optima.
- **Conditions**: Applies to leader-guided population metaheuristics of the GWO family on high-dimensional, multimodal dispatch landscapes; the claim is about the mechanism's direction, not a measured diversity quantity (the paper reports no explicit diversity metric).
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that adding an adaptive reverse-solution (opposition) operator to the leader-guided update leaves convergence stability and local-optima escape unchanged or worse across dispatch instances — indicating the base update did not under-explore.
- **Proof**: [E02]
- **Evidence basis**: §3.2.2 (strong exploitation "can limit the search diversity and can hinder the exploratory potential"); GWO hierarchy (Figure 2, Table 2); Table 5 shows the DOBL-augmented CDGWO cuts convergence variance far below traditional GWO, the empirical trace of restored diversity.
- **Dependencies**: 
- **Tags**: GWO, exploration-exploitation, hierarchy, diversity

## C03: Choosing a chaotic initialization map is an accuracy-versus-cost trade-off, so the highest-accuracy map is not automatically the best choice
- **Statement**: Different chaotic maps used to seed a population optimizer differ both in the fitness they ultimately reach and in the per-run compute they cost; when the accuracy gap between the most-accurate map and a cheaper map is negligible, the cheaper map is the better engineering choice, because the map's distributional properties affect search quality and runtime independently.
- **Conditions**: Demonstrated for Tent/Sine/Chebyshev/Logistic maps seeding GWO on one MGC dispatch instance (24-hour, 3-MG); generalization to other maps/problems is asserted qualitatively, not proven.
- **Sources**: [1.6895 × 10^3 ← evidence/tables/table4.md «| Chebyshev | 1.6895 × 10^3 | 11.616561 |» [result]; 1.7150 × 10^3 ← evidence/tables/table4.md «| Logistic | 1.7150 × 10^3 | 7.9097413 |» [result]]
- **Status**: supported
- **Falsification criteria**: Find a deployment where the accuracy edge of the highest-fitness map (Chebyshev here) is large enough, or its extra runtime small enough, that selecting the cheaper map (Logistic) measurably degrades the delivered dispatch — contradicting the "negligible gap → pick cheaper" rule.
- **Proof**: [E01]
- **Evidence basis**: Table 4 (Chebyshev reaches the best fitness but the slowest runtime; Logistic reaches near-identical fitness at the fastest runtime); Figure 6 convergence curves; §4.2 conclusion adopting Logistic.
- **Tags**: chaotic-map, initialization, accuracy-cost-tradeoff, Logistic

## C04: Chaotic initialization and dynamic opposition-based learning act on complementary search phases, so combining them yields joint gains rather than a speed/accuracy trade-off
- **Statement**: Because chaotic seeding diversifies the start of the search (helping early convergence but decaying later) while a dynamic, iteration-varying opposition operator keeps injecting adaptive reverse solutions throughout the run, applying both together improves convergence speed, solution precision, and run-to-run stability simultaneously instead of trading one against another.
- **Conditions**: Established on the paper's MGC dispatch instance comparing the combined method against traditional GWO and a panel of metaheuristics; the two enhancements' individual contributions past initialization are not separately ablated (chaos-only is tested, DOBL-only is not), so the decomposition is inferred from the early-vs-late convergence argument.
- **Sources**: [6.906439 ← evidence/tables/table5.md «| CDGWO | 1.044 × 10^3 | 6.906439 | 65 | 48.678354 |» [result]; 48.678354 ← evidence/tables/table5.md «| CDGWO | 1.044 × 10^3 | 6.906439 | 65 | 48.678354 |» [result]]
- **Status**: supported
- **Falsification criteria**: Show an instance where adding the dynamic opposition operator on top of chaotic initialization worsens at least one of {converged fitness, runtime, convergence variance} relative to chaotic-init alone — i.e. the two mechanisms interfere rather than complement.
- **Proof**: [E01, E02]
- **Evidence basis**: §4.3.1 rationale (chaos accelerates early, decays late → add DOBL); Figure 3 procedure; Table 5 and Figure 7 (combined method attains the lowest fitness, lowest runtime, and lowest convergence variance of the seven algorithms).
- **Dependencies**: C02, C03
- **Tags**: CDGWO, DOBL, chaos, complementary-mechanisms

## C05: Iterations-to-converge is not a faithful proxy for a metaheuristic's efficiency or solution quality
- **Statement**: An optimizer can reach its convergence point in comparatively few iterations yet still be slower in wall-clock time and land on a worse solution than a rival that uses more iterations, so ranking solvers by iteration count alone is misleading — runtime, precision, and run-to-run variance must be weighed jointly.
- **Conditions**: Read across one comparison table of seven metaheuristics on a single MGC dispatch instance; the per-iteration cost differences arise from each algorithm's internal operations (e.g. pairwise firefly interactions, genetic operators) and may differ on other problems.
- **Sources**: [56 ← evidence/tables/table5.md «| GA | 1.576 × 10^3 | 103.635457 | 56 | 206.875623 |» [result]; 65 ← evidence/tables/table5.md «| CDGWO | 1.044 × 10^3 | 6.906439 | 65 | 48.678354 |» [result]]
- **Status**: supported
- **Falsification criteria**: Demonstrate that, within a fixed algorithm family and problem, fewest-iterations-to-converge reliably co-selects the lowest runtime and best fitness — restoring iteration count as a sufficient single ranking key.
- **Proof**: [E02]
- **Evidence basis**: Table 5 — GA converges in the fewest iterations yet has a far higher runtime, higher variance, and worse fitness than the method that converges in slightly more iterations; FA converges in few iterations but has by far the largest runtime.
- **Tags**: benchmarking, convergence, runtime, methodology

## C06: When better optimizer fitness carries through to lower real operating cost, the penalty-encoded objective is economically faithful
- **Statement**: Despite fitness and monetary cost being numerically decoupled by the penalty terms, the ordering of algorithms by optimized fitness still predicts their ordering by actual daily operating cost, so search-quality improvements on the penalized objective translate into genuine economic savings rather than penalty-encoding artifacts.
- **Conditions**: Observed for the five algorithms that report both a fitness (Table 5) and an actual daily cost (Table A1) on the same nominal MGC instance; holds under the paper's fixed penalty coefficients and single test day.
- **Sources**: [780.46 ← evidence/tables/tableA1.md «| CDGWO | 780.46 |» [result]]
- **Status**: supported
- **Falsification criteria**: Exhibit an algorithm that attains lower penalized fitness yet a higher actual daily cost than a rival on the same instance — breaking the fitness→cost order-preservation.
- **Proof**: [E02, E03]
- **Evidence basis**: Table 5 fitness ranking vs Table A1 actual daily cost ranking — the best-fitness algorithm also posts the lowest daily cost; the two rankings agree in direction.
- **Dependencies**: C01
- **Tags**: economic-dispatch, cost, fitness-cost-correspondence

## C07: Encoding hourly power balance plus equipment/SOC limits as hard constraints keeps dispatch solutions physically feasible each interval
- **Statement**: When per-interval power balance, generator output/ramp limits, and ESS charge/discharge/capacity/SOC bounds are imposed as constraints on the search, the resulting schedules satisfy supply-equals-demand at every scheduling interval and respect equipment limits — making the optimizer's economic solution operationally realizable rather than merely cheap.
- **Conditions**: Applies to the paper's 3-MG, 24-interval model with SOC bounded to [30%, 90%]; feasibility is demonstrated graphically (balanced stacks) rather than via a reported constraint-violation metric.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show a produced schedule in which the stacked hourly generation/import does not equal load, or an ESS trajectory that leaves [30%, 90%] or violates a ramp/output bound — i.e. the constraint encoding fails to enforce feasibility.
- **Proof**: [E04]
- **Evidence basis**: §2.2 constraint set (Eqs. 1-7); Table 1 symbol definitions; Figure 1 / Figure 4 structure; Figures 8-10 where hourly stacks track the load line ("maintain perfect power balance").
- **Tags**: constraints, power-balance, SOC, feasibility

## C08: Time-of-use price structure plus storage and inter-cluster exchange drives temporal energy arbitrage in the dispatch
- **Statement**: Given hour-varying grid prices and a roughly flat inter-microgrid trading price, cost-minimizing dispatch shifts grid purchases into low-price hours and pushes selling/discharging into high-price, high-demand hours, using the ESS and MG-to-MG exchange as the arbitrage vehicles — so the price signal, not the load alone, shapes the storage and exchange schedule.
- **Conditions**: Observed on the paper's low-latitude coastal TOU tariff and typical-day forecast; the flat inter-MG price makes intra-cluster trade a hedge whenever grid prices deviate from it.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show a cost-optimal schedule under a non-flat or inverted price structure where storage/exchange timing does not follow the price troughs and peaks — decoupling arbitrage behaviour from the price signal.
- **Proof**: [E04]
- **Evidence basis**: Figure 5 (three-tier TOU purchase/sale prices, flat inter-MG price); §4.3.2 economic-efficiency discussion (buy at low prices, sell around 1 PM and 8 PM); Figures 8-10 ESS charge/discharge and exchange bars; Table A2 net purchase/sale/exchange totals.
- **Tags**: TOU-pricing, arbitrage, energy-storage, inter-MG-exchange

## C09: A penalty-structured multi-objective dispatch degrades gracefully under bounded forecast uncertainty
- **Statement**: Under a bounded random disturbance to renewable output and load, the optimized dispatch continues to satisfy hourly power balance and its total operating cost rises only modestly rather than collapsing, indicating the penalized multi-objective model plus solver is robust to realistic forecast error rather than brittle to it.
- **Conditions**: Tested for a single ±10% random disturbance applied to MG1 wind, MG2 PV, and MG3 load on one test day; robustness to larger, correlated, or adversarial disturbances is untested.
- **Sources**: [7.80% ← evidence/tables/tableA5.md «Total cost rises from 780.46 CNY (normal, Table A4) to 841.35 CNY, an increase the paper reports as 7.80%.» [result]]
- **Status**: supported
- **Falsification criteria**: Introduce a bounded disturbance within the stated ±10% envelope that breaks hourly power balance or drives total cost up disproportionately (far beyond the observed modest rise) — showing the model does not degrade gracefully.
- **Proof**: [E05]
- **Evidence basis**: §4.3.2 robustness point (power balance maintained; costs rise by 7.80%); Tables A2-A5 (per-MG purchase/sale and cost, normal vs disturbed); Figures 8-10 panels (a) vs (b).
- **Dependencies**: C07
- **Tags**: robustness, uncertainty, disturbance, feasibility
