# Claims

## C01: Temperature-controlled load flexibility reduces total system cost beyond ESS-only deployment
- **Statement**: Exploiting building thermal inertia through a user-defined comfort temperature range enables pre-cooling strategies that reduce peak-tariff air conditioning energy consumption, thereby lowering grid operating costs and increasing ESS annual net revenue compared with ESS deployment without demand-side flexibility.
- **Conditions**: Holds under time-of-use tariff structures with peak/valley periods and for building types with sufficient thermal mass (e.g., office buildings with integrated air conditioning). Untested boundary: does not apply under real-time pricing without predictable peak periods, or for buildings with very low thermal capacitance (poorly insulated lightweight structures).
- **Sources**: [12,996,483; 8,832,489; 8,624,186 CNY ← Table 1 «Load Annual Operating Costs» rows S1/S2/S3] [result]; [86.7%; 100%; 100% ← Table 1 «RE Consumption Rate» rows S1/S2/S3] [result]; [301,648; 324,349 CNY ← Table 1 «Annual Net Income from ESS» rows S2/S3] [result]; [2.35% operating cost saving; 7.64% ESS net income improvement ← Section 6.2 «Scenario 3 ... saving of 2.35% ... improved by 7.64%»] [result]
- **Status**: supported
- **Falsification criteria**: For a similar building stock and tariff structure (same climate zone, same peak/valley ratio), an alternative configuration where the ESS is sized identically but temperature-controlled loads follow a fixed setpoint (no pre-cooling) achieves equal or lower total operating cost than when a comfort range is exploited — or where the pre-cooling strategy increases total cost due to thermal rebound effects.
- **Proof**: [E01]
- **Evidence basis**: Table 1 shows Scenario 3 (ESS + TCL flexibility) reduces load annual operating costs to 8,624,186 CNY versus 8,832,489 CNY in Scenario 2 (ESS only) — a 2.35% saving — and increases ESS annual net income from 301,648 CNY to 324,349 CNY — a 7.64% improvement. RE consumption is 100% in both Scenarios 2 and 3 versus 86.7% in Scenario 1 (no ESS). Figures 7 and 8 show qualitative evidence of pre-cooling behavior: air conditioning increases power at 08:00 and 16:00 (before peak periods) causing a temperature drop at 09:00 and 17:00, reducing consumption during peak tariff hours.
- **Dependencies**: None (direct empirical evidence from Table 1)
- **Tags**: temperature-controlled loads, demand-side flexibility, operating cost, ESS revenue, pre-cooling

## C02: POA-GWO-CSO achieves faster convergence and higher fitness than component algorithms
- **Statement**: The hybrid POA-GWO-CSO algorithm, which incorporates GWO leader strategies into the POA position update and CSO horizontal/vertical crossover operators, achieves higher fitness values per iteration count than standalone POA, standalone GWO, or POA-GWO without CSO on the ESS multi-objective optimization problem, demonstrating more efficient solution-space exploration and faster convergence.
- **Conditions**: Holds for the specific multi-objective ESS configuration problem formulation (bi-objective with SOCP convexification) and the parameter setting described in the paper (population size, max iterations = 500, inertia weight parameters). Untested boundary: may not generalize to other optimization problems with different fitness landscape topologies (e.g., unimodal, highly multimodal) or objective function structures outside power system ESS planning.
- **Sources**: [Method 1 (POA-GWO-CSO) fitness values plotted highest across 500 iterations ← Figure 9 «Fitness value» curves] [visual_description]; [Section 6.2 «fitness function value of method 1 ... was significantly higher than in the other schemes for the same number of iterations»] [result]
- **Status**: supported
- **Falsification criteria**: On the same ESS optimization instance (same data, same constraints, same starting population seed), a re-implementation of any of the three component algorithms (POA, GWO, POA-GWO) produces a final fitness value equal to or higher than POA-GWO-CSO when run for the same number of iterations, or POA-GWO-CSO requires more iterations to reach a given fitness threshold than one of the component algorithms.
- **Proof**: [E02]
- **Evidence basis**: Figure 9 shows Method 1 (POA-GWO-CSO) achieving higher scaled fitness values than Methods 2 (standalone POA), 3 (standalone GWO), and 4 (POA-GWO without CSO) across the 500-iteration run. The text states the POA-GWO-CSO algorithm "was able to explore the solution space more efficiently and converge quickly toward the optimal solution" and "could obtain better fitness values in fewer iterations."
- **Dependencies**: None
- **Tags**: POA-GWO-CSO, hybrid algorithm, convergence, fitness, optimization

## C03: ESS configuration without load flexibility dramatically reduces costs and enables full RE consumption
- **Statement**: Configuring an energy storage station in the distribution network — even without demand-side flexibility — reduces annual load operating costs by approximately 32% and increases the renewable energy consumption rate to 100% compared with a no-ESS baseline, by enabling arbitrage between valley and peak tariff periods and storing excess RE output.
- **Conditions**: Holds for the Shanxi Province typical summer day dataset with the given time-of-use tariff structure, PV/wind profiles, and conventional load profile. Untested boundary: the magnitude of saving depends on the peak-to-valley tariff ratio and the RE curtailment level in the baseline — systems with already-low curtailment or flat tariffs would see smaller benefits.
- **Sources**: [12,996,483 → 8,832,489 CNY, 32.05% reduction ← Section 6.2 «annual operating cost of the load was saved by 32.05%»] [result]; [86.7% → 100% RE consumption ← Section 6.2 «RE consumption rate was increased by 13.3%»] [result]; [ess_config_costs ← Table 1 rows S1/S2] [result]
- **Status**: supported
- **Falsification criteria**: For the same dataset, running the optimization without ESS yields annual operating costs that are less than 20% different from the ESS-configured case, or the RE consumption rate without ESS already exceeds 95% (leaving insufficient curtailment for ESS to recover).
- **Proof**: [E01]
- **Evidence basis**: Table 1: Scenario 1 (no ESS) annual operating cost = 12,996,483 CNY, RE consumption rate = 86.7%. Scenario 2 (ESS, no TCL flexibility) annual operating cost = 8,832,489 CNY, RE consumption rate = 100%. The 32.05% saving and 13.3% RE consumption increase are stated explicitly in Section 6.2.
- **Dependencies**: None
- **Tags**: ESS configuration, renewable energy consumption, operating cost reduction, baseline comparison

## C04: Pre-cooling via building thermal mass shifts AC load from peak tariff periods
- **Statement**: By allowing indoor temperature to vary within a user-defined comfort range, the air conditioning system can pre-cool the building before peak tariff periods using the building's thermal mass as a cold storage medium, reducing AC power consumption during peak-price hours while keeping indoor temperature within comfort bounds.
- **Conditions**: Holds for buildings with sufficient thermal mass (heavyweight construction) and a temperature comfort range of at least 2–3 °C. The pre-cooling lead time depends on the thermal time constant of the building (on the order of 1–2 hours for typical office construction). Untested boundary: does not apply for buildings with very low thermal inertia (e.g., lightweight temporary structures with large window-to-wall ratios) or when the comfort range is too narrow to accumulate meaningful pre-cooled thermal storage.
- **Sources**: [Section 6.2 «air conditioning system to increase its operating power at 8:00 and 16:00 to pre-cool and store cold energy in advance»] [result]; [«temperature drop occurred at 9:00 and 17:00» Figure 8 description] [result]
- **Status**: supported
- **Falsification criteria**: In a building with the same thermal characteristics and tariff structure, operating the AC with a fixed setpoint (no pre-cooling) results in equal or lower total daily AC energy cost than the pre-cooling strategy, or the pre-cooling action causes indoor temperature to exceed the comfort range during peak hours.
- **Proof**: [E03]
- **Evidence basis**: Figure 7 (Scenario 2) shows fixed setpoint AC operation with power consumption tracking outdoor temperature. Figure 8 (Scenario 3) shows pre-cooling at 08:00 and 16:00, with indoor temperature dropping at 09:00 and 17:00 (peak tariff start times), while remaining within comfort bounds. The text explicitly describes the mechanism: «air conditioning system to increase its operating power at 8:00 and 16:00 to pre-cool and store cold energy in advance.»
- **Dependencies**: None
- **Tags**: pre-cooling, thermal mass, thermal load flexibility, demand shifting, peak shaving
