# Claims

## C01: Coordinating chaotic initialization, an adaptive weight, and complementary learning factors shifts a swarm optimizer from exploration to exploitation across the run, improving convergence and local-optima escape
- **Statement**: In a swarm optimizer, replacing random initialization with a diversity-spreading chaotic map, decreasing the inertia weight nonlinearly with fitness progress, and driving the cognitive coefficient down while the social coefficient rises together move the search from wide early exploration toward stable late exploitation; this coordinated schedule is what yields faster convergence and better escape from local optima than a fixed-parameter swarm, across both unimodal and multimodal landscapes.
- **Conditions**: Demonstrated on five standard benchmark functions at dimension 50 with a fixed iteration budget and an acceptance band near the known optimum; the learning-factor coefficients are bounded in [0,2] and the inertia weight is scheduled between a fixed max and min. Untested boundary: higher dimensions, other function classes, other population sizes, and whether each mechanism individually (vs jointly) is necessary are not isolated by an ablation.
- **Sources**: [50 ← §4.2.5 «population size of 100, dimension of 50, and 2000 iterations» [input]; 0.9 ← §4.2.2 «wmax is the maximum weight factor, set to 0.9, and wmin is the minimum weight factor, set to 0.4» [input]; 0.4 ← §4.2.2 «wmax is the maximum weight factor, set to 0.9, and wmin is the minimum weight factor, set to 0.4» [input]]
- **Status**: supported
- **Falsification criteria**: If a fixed-parameter PSO (random init, constant w, constant c1/c2) reached the acceptance band on these benchmarks in as few or fewer iterations as the scheduled variant, or if the scheduled variant failed to converge on the multimodal functions (Rastrigin/Schwefel/Levy), the mechanism claim would be refuted.
- **Proof**: [E01, E02]
- **Evidence basis**: Figure 5 (all five benchmarks collapse to the near-zero acceptance band early), Figure 2 (c1 decreasing / c2 increasing crossover), Table 3 (benchmark settings, acceptance 0.01, optimum 0), Figure 6 (fastest descent vs baselines). Exact convergence values are in the evidence layer, not restated here.
- **Dependencies**: none
- **Tags**: PSO, exploration-exploitation, chaotic-mapping, adaptive-weight, learning-factor, convergence

## C02: Splitting a perturbation term by a mid-run threshold lets one search phase deliver both wide early exploration and damped late refinement
- **Statement**: When a velocity update carries a second-order oscillation term built from the current and previous global-best positions, gating the oscillation factor by a run-fraction threshold — above-threshold magnitude early, below-threshold magnitude late — produces two-sided perturbations that widen exploration around the optimum in the first half of the run and a one-sided damped approach that stabilizes refinement in the second half; the threshold split, not the oscillation term alone, is what buys both behaviours from a single mechanism.
- **Conditions**: Holds for the second-order oscillation velocity update as formulated, with the oscillation/progressive factor bounded by the stated inequality on the coefficient-random-number product, and the regime boundary placed at the half-way iteration. Untested boundary: sensitivity to the exact threshold location (only the midpoint is shown), and the interaction of the oscillation term with the other three modifications is not isolated.
- **Sources**: [Tmax/2 ← §4.2.4 «When the iteration count t ≤ Tmax/2, the algorithm exhibits oscillation convergence» [input]; Tmax/2 ← §4.2.4 «When the iteration count t > Tmax/2, the algorithm exhibits progressive convergence» [input]]
- **Status**: supported
- **Falsification criteria**: If the oscillation-regime curve showed no two-sided (positive and negative) excursions in the first half of the run, or the progressive-regime curve showed oscillation across zero rather than monotone one-sided decay, the threshold-split mechanism would be refuted.
- **Proof**: [E01]
- **Evidence basis**: Figure 3 (oscillation convergence curve: two-sided amplitude, widest early, contracting envelope) and Figure 4 (progressive/asymptotic curve: non-negative monotone decay), corresponding to Eqs. 30-34. The threshold at Tmax/2 governs which regime applies.
- **Dependencies**: [C01]
- **Tags**: second-order-oscillation, threshold-switching, convergence-regime, local-optima

## C03: A merit-order dispatch that stacks renewables-first, storage-buffer, thermal-slack, and grid-balance keeps a multi-source microgrid feasible while pushing cost down
- **Statement**: For a microgrid mixing intermittent renewables, dispatchable thermal, storage, and a grid tie, prioritizing renewable output, using storage to absorb midday surplus and release it at peak, running thermal as the baseload slack, and exchanging with the main grid only as the final balancing step produces a supply-demand-feasible schedule in which the grid is imported from when local generation is short and exported to when it is in surplus — turning storage into a peak-shaving/valley-filling buffer that lowers total operating-plus-environmental cost.
- **Conditions**: Shown for a single typical summer day (24 h, 1-h steps) of a subtropical-monsoon Jiangsu microgrid with 10 PV units, one small thermal generator, wind, and two storage units, under time-of-use pricing and deterministic (forecast-known) weather/load. Untested boundary: other seasons, stochastic/uncertain inputs, multi-day operation, and different device mixes are not evaluated.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: If the reported hourly dispatch violated the power-balance identity (sources + grid != load at some hour), or if storage were shown charging at peak-load hours and discharging during high-PV surplus (the opposite of buffering), the merit-order mechanism claim would be refuted.
- **Proof**: [E03]
- **Evidence basis**: Table 5 (hourly PV/WT/DG/ESS/interaction power over 24 h), Figure 13 (source power curves — ESS negative/charging midday, positive/discharging at night), Figure 14 (buy at night, sell midday), Figure 1/Figure 7/Figure 8 (strategy, algorithm, topology), Figures 9-12 and Table 4 (inputs). Exact hourly values live in the evidence layer.
- **Dependencies**: none
- **Tags**: economic-dispatch, merit-order, energy-storage, peak-shaving, grid-interaction, microgrid

## C04: A cheaper metaheuristic dispatch lowers the whole cost stack jointly rather than trading fuel against emissions, because a leaner thermal schedule cuts both at once
- **Statement**: Across optimizers solving the same microgrid dispatch, the method that finds the lower-cost schedule simultaneously incurs lower operation/maintenance, fuel, depreciation, and environmental costs and lower CO2/SO2/NOX emissions — the components move together, not against each other, because reducing thermal-generator reliance is the common lever that cuts fuel burn and pollutant treatment cost at the same time.
- **Conditions**: Observed for four PSO-family optimizers (the proposed variant vs CPSO, QPSO, PSO) on the same summer-day case with fixed device/emission/price coefficients; grid-interaction cost is a net revenue (negative) term that grows in magnitude for the cheaper schedules. Untested boundary: whether the co-movement holds when environmental cost is weighted much more heavily, or under a pricing/emission regime where fuel and emissions decouple, is not tested.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: If the lowest-total-cost optimizer had shown a higher fuel cost or higher pollutant emissions than a costlier optimizer (i.e. one component moving opposite to the rest), the "joint lowering" mechanism would be refuted.
- **Proof**: [E04]
- **Evidence basis**: Table 6 (O&M/fuel/depreciation/environmental costs ranked identically across the four algorithms) and Table 7 (CO2/SO2/NOX emissions and treatment costs ranked identically); the environmental-cost column of Table 6 equals the treatment-cost sum in Table 7. Named algorithms and their per-component numbers live in the evidence layer.
- **Dependencies**: [C03]
- **Tags**: economic-environmental-dispatch, cost-emissions-coupling, thermal-generation, optimizer-comparison

## C05: Setting the iteration budget above the point where competing solvers first reach the acceptance band buys reliability margin, not extra final accuracy
- **Statement**: When competing swarm variants all flatten near the optimum well before the run ends, extending the iteration budget past that first-approach point does not improve the final solution — the curves are already flat — so the extra iterations purchase robustness margin (insurance against a run that converges slowly) at the cost of compute, and the budget choice is a reliability decision rather than an accuracy one.
- **Conditions**: Grounded in the four-way PSO benchmark comparison at dimension 50 where all variants approach zero early and the run is continued far beyond; assumes the observed early flattening generalizes to the dispatch solve. Untested boundary: harder problems where variants have not yet plateaued at the chosen budget, for which the same margin argument would not apply.
- **Sources**: [500 ← §4.2.5 «when the population iterates to around 500 times, the results of the four PSO algorithms tend to approach 0» [result]; 500 ← §4.2.5 «it is crucial that the number of iterations does not fall below 500» [input]; 2000 ← §4.2.5 «2000 iterations were chosen as the standard in this paper» [input]]
- **Status**: supported
- **Falsification criteria**: If the convergence curves continued to descend materially between the first-approach point and the chosen budget (rather than staying flat), the "margin not accuracy" interpretation would be refuted.
- **Proof**: [E02, E05]
- **Evidence basis**: Figure 6 (all four curves approach zero around the first-approach point, then remain flat through the full budget, with a zoomed late-iteration inset). Exact iteration counts are quoted in Sources from the text.
- **Dependencies**: [C01]
- **Tags**: iteration-budget, convergence-margin, hyperparameter-choice, reliability

## C06: Aligning the dispatch objective with emissions makes economic optimization and environmental protection reinforce rather than compete in a renewable-plus-thermal microgrid
- **Statement**: When the only pollution and fuel cost in the system comes from the dispatchable thermal unit while renewables are emission-free, folding pollutant-treatment cost into the same objective as operating cost makes minimizing economic cost also minimize emissions — the optimizer displaces thermal output with renewables and storage for economic reasons and thereby reduces environmental burden as a byproduct, so the two goals are aligned rather than traded off.
- **Conditions**: Holds for a system where clean sources carry no emissions and a single thermal generator is the sole emitter, with pollutant-treatment costs and emission factors fixed as given. Untested boundary: systems with emission-bearing renewables (lifecycle), multiple heterogeneous thermal units, or a heavy carbon price that changes the balance are not examined.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: If a dispatch that lowered total cost had raised total pollutant emissions (economic and environmental objectives pulling apart), the alignment claim would be refuted.
- **Proof**: [E04]
- **Evidence basis**: Objective structure (Eq. 6, C1 operating + C2 environmental), Table 2 (only DG and grid emit), and Tables 6-7 (the lowest-cost schedule is also the lowest-emission schedule). Dependencies: rests on the joint-lowering evidence in C04.
- **Dependencies**: [C04]
- **Tags**: economic-environmental-alignment, emissions, objective-design, clean-energy
