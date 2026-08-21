# Claims

## C01: Adding a flexibility objective turns single-objective dispatch into a tunable economy–flexibility trade-off
- **Statement**: When a system-flexibility objective is optimized jointly with operator economics, the dispatch stops maximizing profit alone and instead trades a bounded amount of operator revenue for a measurable gain in flexibility; the flexibility gain is realized by pricing that activates demand-response and storage-type regulation the profit-only solution left idle.
- **Conditions**: Park-level IES on a deterministic typical day; lower level fixed to aggregator-only (no EVs), no carbon/GCT trading (Scenario 1→2); weights ω_e,ω_h,ω_q unspecified. Untested boundary: whether the trade-off stays favorable under stochastic loads or other weight settings.
- **Sources**: [1133 yuan ← Table 5/§4.2.1 «the IES operator incurring a revenue loss of 1133 yuan in exchange for a 10.7% enhancement in flexibility» [result]; 10.7% ← §4.2.1 «a 10.7% enhancement in flexibility» [result]]
- **Status**: supported
- **Falsification criteria**: If, holding all else fixed, adding the flexibility objective changed neither the flexibility indices nor the dispatch schedule (operator revenue unchanged), the objective would carry no regulating effect and the claim fails. Equally, if flexibility could be raised with no revenue cost, the "trade-off" framing fails.
- **Proof**: [E01]
- **Evidence basis**: Table 5 Scenario 1 vs 2 — revenue 25,059→23,926, system flexibility 0.56→0.62; §4.2.1 states the 1133-yuan loss buys a 10.7% flexibility gain. Numbers live in evidence/tables/table5.md; do not restate in Statement.
- **Tags**: multi-objective, flexibility, economic-dispatch, trade-off

## C02: A price-guided aggregator holds its total cost near-invariant by reallocating demand response across regimes
- **Statement**: A user aggregator that responds to operator prices keeps its total cost nearly constant across dispatch regimes not because the operator shields it, but because it self-hedges — shifting spend between energy purchase and demand-response compensation so that operator-side cost shocks are absorbed by re-optimized load flexibility.
- **Conditions**: Five scenarios differing in upper-level objective, EV inclusion, and carbon/GCT mechanisms; aggregator has transferable/curtailable/substitutable load with fixed compensation prices (Table 2) and time-of-use energy prices (Table 3). Untested boundary: larger price swings or tighter DR limits than those simulated.
- **Sources**: [74 yuan ← §4.2.2 «The highest total cost is 39,809 yuan, while the lowest is 39,735 yuan, resulting in a narrow range of only 74 yuan» [result]; 357 yuan ← §4.2.2 «the user aggregator raises its demand response expenditure by 357 yuan to counteract the operational cost increase» [result]]
- **Status**: supported
- **Falsification criteria**: If aggregator total cost tracked the operator's cost swings (e.g. moved by thousands of yuan across scenarios) rather than staying within a narrow band, the self-hedging-via-DR mechanism would be refuted. Or if DR expenditure did not move to offset energy-price changes.
- **Proof**: [E02]
- **Evidence basis**: Table 5 User-Aggregator rows — total cost 39,735–39,809 across all five scenarios; energy-purchase cost falls while DR cost rises in Scenario 5 vs 3 (§4.2.2). Figures 9–12 show the DR reallocation and prices.
- **Dependencies**: C01
- **Tags**: demand-response, aggregator, cost-stability, multi-entity

## C03: Aggregated EVs are a dispatchable flexibility resource whose benefit is time-localized and cost-effective
- **Statement**: Aggregating EVs into price-responsive clusters supplies genuine grid flexibility that is concentrated in their grid-connection window rather than spread uniformly over the day, and the marginal operating cost of enrolling them is repaid by a larger operator profit gain — so EV flexibility is net-positive, not merely a cost.
- **Conditions**: Five fixed EV categories with deterministic connection windows and proportions (Table 4); Scenario 2→3 adds EVs to the lower level; flexibility measured as the electrical index. Untested boundary: uncontrolled/stochastic EV behavior or different fleet mixes.
- **Sources**: [296 yuan ← §4.2.1 «the system incurs an additional 296 yuan in operating costs» [result]; 356 yuan ← §4.2.1 «this investment yields a greater profit increase of 356 yuan» [result]; 16.7% ← §4.2.1 «the system's electrical energy flexibility is improved by 16.7%» [result]]
- **Status**: supported
- **Falsification criteria**: If introducing EV clusters raised operating cost without a matching or greater profit gain, or if the flexibility gain were spread evenly across all hours rather than peaking in the connection window, the "time-localized, cost-effective flexibility" mechanism fails.
- **Proof**: [E03]
- **Evidence basis**: Table 5 Scenario 2→3: operating cost 12,427→12,723 (+296), revenue 23,926→24,282 (+356), electrical flexibility 0.30→0.35; Figure 8 shows the Scenario-5 vs Scenario-2 flexibility gap concentrated over 18:00–08:00; Figures 13–14 show price-timed EV charge/discharge.
- **Dependencies**: C01
- **Tags**: electric-vehicles, flexibility, V2G, multi-entity

## C04: Pricing carbon inside the operator objective imposes an irreducible economy–emissions trade-off
- **Statement**: Once a carbon-trading cost enters the operator's objective, emission reduction and operator profitability cannot be improved together — driving emissions down requires accepting lower profit, because low-carbon dispatch substitutes cheaper high-emission generation for costlier low-emission operation.
- **Conditions**: Scenario 3→4 introduces carbon trading with coefficients from ref [29] (values unspecified here); single carbon base price. Untested boundary: very high carbon prices where dispatch saturates, or systems with abundant zero-marginal-cost low-carbon capacity.
- **Sources**: [5587 yuan ← §4.2.1 «a decrease of 5587 yuan in the total profit of the IES operator» [result]; 989 kg ← §4.2.1 «a reduction of 989 kg in carbon emissions» [result]; 5.19% ← §4.2.1 «a 5.19% reduction in system carbon emissions relative to Scenario 3» [result]]
- **Status**: supported
- **Falsification criteria**: If adding the carbon cost reduced emissions while leaving operator profit unchanged or higher, the claimed trade-off (emissions down ⇒ profit down) would be refuted.
- **Proof**: [E04]
- **Evidence basis**: Table 5 Scenario 3→4: revenue 24,282→18,695, carbon emissions 19,062→18,073, carbon-trading cost 4867 appears; §4.2.1 quantifies the 5587-yuan profit drop and 989-kg (5.19%) emission cut.
- **Tags**: carbon-trading, low-carbon, trade-off, economic-dispatch

## C05: Green-certificate trading complements carbon trading, cutting emissions further while offsetting part of the carbon cost
- **Statement**: Layering a green-certificate mechanism on top of carbon trading is not redundant: it reduces emissions beyond what carbon trading alone achieves and simultaneously lowers the carbon-trading cost (by crediting renewable output), so the two market instruments act synergistically rather than substituting for each other.
- **Conditions**: Scenario 4→5 adds green-certificate trading to the already-carbon-priced system; GCT coefficients from ref [29]. Untested boundary: certificate/carbon price ratios other than the one simulated.
- **Sources**: [1109 kg ← §4.2.1 «an additional reduction of 1109 kg in carbon emissions» [result]; 302 yuan ← §4.2.1 «carbon trading costs decrease by 302 yuan» [result]; 298 yuan ← §4.2.1 «the system incurs an additional 298 yuan in green certificate trading costs» [result]; 6.19% ← §4.2.1 «green certificate trading in Scenario 5 drives a further 6.19% decrease» [result]]
- **Status**: supported
- **Falsification criteria**: If adding green-certificate trading left emissions unchanged versus carbon-trading-only, or raised carbon-trading cost rather than lowering it, the complementarity/synergy claim fails.
- **Proof**: [E04]
- **Evidence basis**: Table 5 Scenario 4→5: carbon emissions 18,073→16,964, carbon-trading cost 4867→4565, green-certificate cost 298 appears; §4.2.1 states the further 1109-kg (6.19%) reduction. Figure 6 shows the boiler/gas-turbine reallocation behind it.
- **Dependencies**: C04
- **Tags**: green-certificate, carbon-trading, synergy, low-carbon

## C06: Normalizing up/down supply margins onto one per-carrier index makes heterogeneous flexibility resources comparable and exposes the bottleneck carrier
- **Statement**: Expressing flexibility as the average of upward and downward supply margins normalized by supplied power yields a single dimensionless index per energy carrier, which renders otherwise incommensurable resources (conversion equipment, storage, demand response, EVs) additively comparable and reveals which carrier limits overall system flexibility.
- **Conditions**: Electrical/thermal/cooling carriers of a park IES (Eq. 2–6); margins summed linearly (Eq. 5). Untested boundary: whether linear additivity of margins holds when resources are coupled/contended, or under uncertainty.
- **Sources**: [0.25 ← Table 5 «Electrical Energy Flexibility ... 0.25» [result]; 0.70 ← Table 5 «Thermal Energy Flexibility ... 0.70» [result]; 0.73 ← Table 5 «Cooling Energy Flexibility ... 0.73» [result]]
- **Status**: supported
- **Falsification criteria**: If the index assigned similar values to carriers with visibly different regulating headroom, or could not separate the electrical carrier (repeatedly the lowest and the one EVs improve) from thermal/cooling, it would fail as a bottleneck-revealing measure.
- **Proof**: [E01, E03]
- **Evidence basis**: Eq. 6 defines the index; Table 5 shows electrical flexibility lowest (0.25 in Scenario 1) and the carrier that EV enrollment most improves (to 0.35), while thermal (~0.70) and cooling (~0.73–0.83) stay higher — the index localizes the electrical bottleneck. Figure 2 gives the resource topology.
- **Tags**: flexibility-metric, quantification, multi-energy, indicator

## C07: System-flexibility timing is governed by EV fleet composition, so retuning category proportions relieves a specific deficit hour
- **Statement**: Because each EV category is available only in its own connection window, the hourly profile of system flexibility is shaped by the mix of categories; deliberately reweighting the fleet toward categories present at a deficit hour raises flexibility precisely at that hour, making fleet composition a targeted control lever rather than a fixed input.
- **Conditions**: Scenario 5, EV proportions changed from Table 4 to 13%/30.2%/9.4%/36.4%/11% to target the 12:00 minimum; single reweighting tested. Untested boundary: whether arbitrary hours can be targeted, or gains at one hour cost flexibility elsewhere.
- **Sources**: [0.2 to 0.22 ← §4.2.4 «a notable rise from 0.2 to 0.22 at 12:00» [result]; 10% ← §4.2.4 «reflecting a 10% improvement» [result]]
- **Status**: supported
- **Falsification criteria**: If reweighting the fleet toward categories connected at 12:00 did not raise 12:00 flexibility (or raised it identically regardless of which categories were boosted), the composition-as-lever mechanism fails.
- **Proof**: [E05]
- **Evidence basis**: Figure 15 vs Figure 8 — after the proportion change, the 12:00 electrical-flexibility low point rises 0.2→0.22 (10%); §4.2.4 attributes it to coordinated EV charge/discharge broadening the regulation window.
- **Dependencies**: C03
- **Tags**: electric-vehicles, flexibility, sensitivity, fleet-composition

## C08: The carbon price is a monotone lever trading emissions against operator revenue
- **Statement**: Scaling up the carbon base price steers dispatch monotonically toward lower emissions and monotonically lower operator revenue, so the carbon price functions as a single continuous control knob on the emissions-versus-profit frontier rather than triggering an abrupt regime switch.
- **Conditions**: Scenario 5 with carbon base price scaled to 1.0×, 1.05×, 1.1×, all else fixed; only three points sampled. Untested boundary: larger multiples, non-monotonicity or saturation outside the tested range.
- **Sources**: [16,964 / 16,645 / 16,372 ← Table 6 «Carbon Emissions/(t) 16,964 16,645 16,372» [result]; 18,890 / 18,552 / 18,215 ← Table 6 «Revenue of IES operator/(yuan) 18,890 18,552 18,215» [result]]
- **Status**: supported
- **Falsification criteria**: If raising the carbon price failed to lower emissions, or lowered emissions without lowering revenue, across the sampled multiples, the monotone-lever claim fails.
- **Proof**: [E06]
- **Evidence basis**: Table 6 — as the multiple rises 1.0→1.05→1.1, emissions fall 16,964→16,645→16,372 and revenue falls 18,890→18,552→18,215, both monotone.
- **Dependencies**: C04
- **Tags**: carbon-price, sensitivity, trade-off, low-carbon

## C09: Injecting search diversity into PSO improves convergence speed, solution quality, and run-to-run stability on the constrained dispatch
- **Statement**: Augmenting PSO with a nonlinearly decreasing inertia weight, sine-modulated learning factors, and a partitioned swarm whose sub-populations follow distinct position-update rules counters premature clustering under many equality (balance) constraints, so the algorithm reaches a near-ideal solution in fewer iterations, at higher closeness, and with lower variance than plain PSO or a single-strategy metaheuristic (DBO).
- **Conditions**: Upper-level model of Scenario 5; population 50, 200 max iterations, 30 independent runs; closeness measured by TOPSIS to the ideal solution. Untested boundary: other problem instances/dimensions, or metaheuristics beyond PSO/DBO.
- **Sources**: [46 iterations ← §4.3 «convergence is achieved after 46 iterations, with the proximity being 0.86» [result]; 54.0% ← §4.3 «reduced the number of iterations at convergence by 54.0%» [result]; 7.5% ← §4.3 «improved the closeness of the obtained optimal solution to the ideal solution by 7.5%» [result]; 5.733 × 10⁻⁵ ← §4.3 «the variance of IPSO is 5.733 × 10⁻⁵, which is lower than that of PSO and DBO» [result]]
- **Status**: supported
- **Falsification criteria**: If the diversity-augmented PSO converged in no fewer iterations, to no higher closeness, and with no lower variance than plain PSO on the same problem, the mechanism (diversity counters premature convergence) would be refuted.
- **Proof**: [E07]
- **Evidence basis**: Figure 16 — PSO 100 iter/0.80, DBO 73/0.82, IPSO 46/0.86; Table 7 — IPSO max 0.86, mean 0.849, variance 5.733×10⁻⁵, runtime 105 s, all best. Text derives 54.0% fewer iterations and 7.5% higher closeness vs PSO. (Abstract's 52.0% is an internal inconsistency — see evidence/README.md.)
- **Tags**: PSO, metaheuristic, convergence, optimization, algorithm

## Dead ends / non-adopted alternatives (for completeness)
- The paper cites plain **PSO** and **DBO** only as baselines that IPSO outperforms (Figure 16, Table 7) — not adopted as the final solver. Genetic Algorithm [27] and ADMM [26] are noted as alternative solution methods used by other works, not tried here. These are recorded to preserve the comparison footprint; they are not standalone claims.
