# Problem Specification

## Observations

### O1: N-1 contingency is the mandated standard for power-system planning
- **Statement**: An outage experienced by a single entity at one time is an n-1 contingency; NERC industry standards require compliance with n-1 contingency protocols as a foundational reliability criterion, whereas n-k analysis is not typically mandated for routine operations and is economically impractical to design for.
- **Evidence**: §I (Introduction), p.181180–181181.
- **Implication**: DA UC schedules must be evaluated specifically against N-1 generator outages, and doing so is both necessary and tractable.

### O2: Thermal generator outages raise cost and threaten supply-demand balance
- **Statement**: Thermal generator outages can cause increased generation costs, grid instability, and the need for rapid adjustments; the failure of a single thermal generator can disrupt the supply-demand equilibrium and lead to an inability to meet load.
- **Evidence**: §I, p.181181.
- **Implication**: A DA UC schedule optimized only for predicted conditions may become infeasible under an outage, so preparedness must be quantified before real time.

### O3: The IEEE RTS peak demand approaches total dispatchable capacity
- **Statement**: The 24-bus, 26-generator IEEE RTS has total available capacity 3105 MW; the highest forecasted next-day demand is 2670 MW at hour 11. After a 10% spinning reserve (CM ≈ 310.5 MW), only 2795 MW is available for dispatch in the Base Case and Case 1.
- **Evidence**: §VI (System Description) p.181188; Fig. 6; Table 4.
- **Implication**: Loss of a large generator can push available capacity below peak demand, creating a non-zero probability of loss of load for specific contingencies.

### O4: The largest generator outages produce the largest cost escalation
- **Statement**: Outage of the 400 MW generators at buses 18 and 21 raises DA UC cost from the $774,100 Base Case to $895,400 (+15.67%), the highest across all cases; the 350 MW outage at bus 23 gives +11.67%; small-unit outages (20 MW at bus 1) give 0% and some (197 MW bus 13, 12 MW bus 15) give slight cost decreases.
- **Evidence**: Table 5, Table 6, §VII-A2; p.181191–181192.
- **Implication**: Contingency severity is highly non-uniform across generators, motivating a generator-level criticality ranking.

### O5: Reliability and margin depend directly on the reserve level
- **Statement**: Overall next-day LOLP is 0.050113 for Case 1 (10% SR), 0.0369387 for Case 2a (8%), 0.0153346 for Case 2b (5%), and 0 for Case 2c (0% SR); operating margin is -0.000113, 0.0130613, 0.0346654, and 0.05 respectively.
- **Evidence**: Table 9, Table 10, Table 11, Table 12, Table 13; §VII-B.
- **Implication**: There is a measurable, monotone relationship between reserve allocation and both reliability and residual margin, exposing a reserve-vs-cost-vs-resilience trade-off.

## Gaps

### G1: No integrated system-performance framework for contingency-aware DA UC
- **Statement**: Current research concentrates on discrete elements (cost optimization, reserve scheduling, generator coordination) and lacks a comprehensive methodology that simultaneously evaluates criticality, robustness, reliability, and operating margin in the context of N-1 generator contingencies impacting DA UC.
- **Caused by**: O1, O2.
- **Existing attempts**: Combined heat & electricity flexibility studies, transmission-line switching, integrated renewable sources, n-1 transmission-line contingency UC.
- **Why they fail**: They target specific contingency-management strategies or integrated systems and do not assess system-wide performance metrics together.

### G2: No established generator-level criticality metric in DA UC
- **Statement**: Criticality indices (FMEA, SOC, topological analysis, Birnbaum, Fussell-Vesely, RAW, RRW) exist for components/systems but are not designed to rank individual thermal generators in DA UC under N-1 scenarios.
- **Caused by**: O2, O4.
- **Existing attempts**: FMEA-based criticality metrics; SOC via AC-OPF; graph-theory ranking of critical assets.
- **Why they fail**: They do not produce generator-specific criticality directly influencing DA UC schedules.

### G3: Inadequate robustness evaluation for contingency-based DA UC schedules
- **Statement**: Robustness metrics are applied to cascading failures, control systems, or network topologies, but the resilience of DA UC schedules under generator-outage scenarios has not been analyzed.
- **Caused by**: O2.
- **Existing attempts**: Frequency-domain robustness margins (SMIB/MIMO), cascading-failure robustness, cyber-physical attack robustness, topological metrics.
- **Why they fail**: None devises robustness of DA UC exposed to N-1 generator contingencies at the bus level.

### G4: Probabilistic reliability indices not integrated into DA UC performance evaluation
- **Statement**: LOLP and LOLE are well-established in reliability analysis, but few studies integrate these measures into the evaluation of DA UC schedules under contingencies.
- **Caused by**: O2, O3.
- **Existing attempts**: LOLP/LOLE for planning or risk analysis.
- **Why they fail**: They do not connect probabilistic reliability with DA UC execution under generator contingencies for system preparedness.

### G5: No quantified operating-margin metric for dispatch feasibility
- **Statement**: Most DA UC research emphasizes cost-minimizing schedules under predicted conditions, without a clear quantitative assessment of how closely the schedule aligns with operational limits (headroom beyond committed reserves).
- **Caused by**: O3, O5.
- **Existing attempts**: Conventional DA UC cost minimization.
- **Why they fail**: They give no explicit operating-margin metric, so operators cannot tell whether the schedule stays feasible under unforeseen contingencies.

## Key Insight
- **Insight**: DA-UC preparedness is not a single number but a jointly-observable state — criticality (which generators/buses matter), robustness (which contingencies are benign), reliability (LOLP under outages), and a residual operating margin — all controllable through one lever, the spinning-reserve-derived Contingency Margin. Reading these four together turns a cost-only schedule into a feasibility-and-resilience assessment.
- **Derived from**: O1, O2, O3, O4, O5.
- **Enables**: A five-step methodology that ranks generator criticality, identifies weak/robust buses, estimates LOLP-based reliability across reserve levels, and computes an operating margin that directly signals dispatch feasibility.

## Assumptions
- A1: For N-1 contingency, only one unit fails at a time; no simultaneous outages of single units of other ratings are considered (avoids compounding shutdown/startup/maintenance costs; periodic maintenance keeps units available).
- A2: The conditional probability of one generator outage with other generators is not considered; conditional probabilities between generators are not modeled and their impact is deemed negligible.
- A3: LOLP is assessed considering forced outage of only one generating unit at a time; outages of more than one unit are not considered for LOLP.
- A4: DC power flow is assumed for the supply-demand balance.
- A5: Maintenance cost is neglected in the cost formulation.
- A6: LOLP_max is taken as 0.05 (per Central Electricity Authority, India), assuming operation under strict limits.
