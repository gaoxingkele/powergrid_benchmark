# Claims

## C01: Cost-only DA UC hides feasibility risk that a joint criticality/robustness/reliability/margin read exposes
- **Statement**: In day-ahead unit commitment, the least-cost schedule alone does not reveal whether that schedule will survive the loss of a single generator; jointly reading which generators/buses are critical, which contingencies are benign, the probabilistic reliability under outages, and a residual operating margin surfaces vulnerabilities that a cost figure cannot, turning a schedule into a feasibility-and-resilience assessment.
- **Conditions**: Holds for DA UC under N-1 thermal-generator contingencies on a test system whose peak demand is near total dispatchable capacity (IEEE RTS, peak 2670 MW vs 3105 MW installed). Untested boundary: N-k / simultaneous outages, transmission-line contingencies, and systems with large capacity headroom, where the four metrics may co-vary differently.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: If, across the contingency set, every N-1 outage that produces a benign cost signal also always keeps LOLP, criticality ranking, and operating margin benign (and vice versa) — i.e. the four metrics are redundant with cost — then the framework adds no information over cost-only optimization.
- **Proof**: [E01, E02, E05, E06]
- **Evidence basis**: Table 12 and Table 13 assemble criticality (Cy6,7 / buses 18,21), robustness (stable Cy4,5 / robust buses 13,15), reliability (LOLP), and operating margin side by side for all cases; contingencies that raise little cost still change LOLP/margin across reserve levels.
- **Tags**: framework, contingency-aware, DA-UC

## C02: Losing the largest-capacity generators drives the greatest cost escalation and marks the weakest buses
- **Statement**: Under N-1 generator contingencies, the operational cost penalty of an outage scales with the lost unit's capacity because higher-cost replacement generation must be committed to serve the same demand; the outages that force the largest cost rise therefore identify the network's weakest buses, while small-unit outages leave cost essentially unchanged or slightly lower.
- **Conditions**: Holds on the IEEE RTS where the largest units are the 400 MW generators at buses 18 and 21; established at 10% spinning reserve (Case 1) and reproduced at 8%/5% CM (Case 2a/2b). Untested boundary: systems where the largest unit is cheap baseload, or where transmission limits rather than capacity dominate the replacement cost.
- **Sources**: [$895,400 ← evidence/tables/table5.md «6 | 18 | 400 | 774100 | 895400 | 15.67 | 1» [result]; $895,400 ← evidence/tables/table5.md «7 | 21 | 400 | 774100 | 895400 | 15.67 | 1» [result]; +11.67% ← evidence/tables/table5.md «9 | 23 | 350 | 774100 | 864440 | 11.67 | 2» [result]; 0% ← evidence/tables/table5.md «1 | 1 | 20 | 774100 | 774100 | 0 | -» [result]]
- **Status**: supported
- **Falsification criteria**: Observe an N-1 contingency set in which a small-capacity generator outage forces a larger DA-UC cost increase than the largest-capacity outage under the same reserve — i.e. cost penalty does not track lost capacity.
- **Proof**: [E02]
- **Evidence basis**: Table 5 / Table 6 rank the nine contingencies by percentage cost rise: 400 MW (buses 18,21) +15.67% (rank 1), 350 MW (bus 23) +11.67%, down to 0% (20 MW, bus 1) and slight decreases for 197 MW/12 MW; buses 18 and 21 are named the weakest.
- **Dependencies**: C01
- **Tags**: criticality, weak-bus, cost

## C03: Some generator outages are benign or cost-reducing, identifying robust buses
- **Statement**: A subset of N-1 generator outages does not disrupt UC feasibility and can even lower DA UC cost relative to the no-contingency Base Case, because removing a particular unit lets the optimizer redispatch onto a cheaper commitment; the buses connected to such stable contingencies are the network's robust buses that can absorb an outage with minimal impact.
- **Conditions**: Holds on IEEE RTS where the 197 MW (bus 13) and 12 MW (bus 15) outages are cost-neutral-to-reducing; robust-bus identity is stable across Case 1 and Case 2a/2b and extends to bus 1 in Case 2c. Untested boundary: whether the same buses remain robust under multiple concurrent outages or tighter demand.
- **Sources**: [-0.703% ← evidence/tables/table5.md «4 | 13 | 197 | 774100 | 768660 | -0.703 | -» [result]; -0.01% ← evidence/tables/table5.md «5 | 15 | 12 | 774100 | 774020 | -0.01 | -» [result]; 768660 ← evidence/tables/table6.md «4 | 13 | 197 | 774100 | 768660 | 768660 | 768660 | 768660» [result]]
- **Status**: supported
- **Falsification criteria**: Show that every generator outage strictly increases DA-UC cost above the Base Case (no cost-reducing/benign contingencies exist), or that buses labeled robust here incur among the largest cost rises.
- **Proof**: [E02]
- **Evidence basis**: Table 5 shows contingency 4 (bus 13, 197 MW) at 768660 (-0.703%, the lowest cost, "most stable") and contingency 5 (bus 15, 12 MW) at 774020 (-0.01%); text names buses 13 and 15 the robust buses, contingencies 4 and 5 the most stable.
- **Dependencies**: C01
- **Tags**: robustness, robust-bus, redispatch

## C04: Spinning-reserve level trades off against reliability and residual margin
- **Statement**: Raising the committed spinning reserve (and the Contingency Margin it produces) monotonically improves DA-UC reliability and operating margin under N-1 contingencies but simultaneously withdraws capacity from dispatch and raises cost, so reserve allocation is a direct, tunable trade-off between economic efficiency and contingency resilience rather than a free reliability gain.
- **Conditions**: Established over four reserve settings on IEEE RTS — 10%/8%/5%/0% SR giving CM 310.5/248/155/0 MW; the "reliability improves as reserve rises" direction is the inverse of the paper's sweep (reserve reduced 10%→0%). Untested boundary: reserve levels above 10%, and systems where reserve is cheap or demand is far below capacity so the trade-off is slack.
- **Sources**: [310.5 MW ← evidence/tables/table12.md «CM remaining (to be utilized for generation) | 310.5 MW | 248 MW | 155 MW | 0» [input]; 0.050113 ← evidence/tables/table13.md «Evaluated LOLP | 0.050113 | 0.0369387 | 0.0153346 | 0» [result]; 0 ← evidence/tables/table13.md «Evaluated LOLP | 0.050113 | 0.0369387 | 0.0153346 | 0» [result]]
- **Status**: supported
- **Falsification criteria**: Observe a case where increasing spinning reserve worsens LOLP or operating margin, or where reducing reserve to zero improves rather than degrades the system's ability to withstand further contingencies.
- **Proof**: [E03, E04, E05]
- **Evidence basis**: As SR falls 10%→8%→5%→0%, CM falls 310.5→248→155→0 MW, dispatchable capacity rises 2795→2857→2950→3105 MW (Table 12), LOLP falls 0.050113→0.0369387→0.0153346→0 (Tables 9,10) and operating margin rises -0.000113→0.0130613→0.0346654→0.05 (Table 11); but 0% CM leaves no headroom for further disturbances.
- **Dependencies**: C01
- **Tags**: reserve, reliability, LOLP, trade-off

## C05: A non-positive operating margin flags an at-limit/infeasible schedule; a positive margin quantifies headroom
- **Statement**: The operating margin, defined as the gap between the maximum allowable LOLP and the realized LOLP, acts as a feasibility signal: a value at or below zero means the committed generation is operating at its limit with heightened probability of failure if generation is not augmented, whereas a positive value quantifies residual capability to absorb additional load or contingencies.
- **Conditions**: Holds under LOLP_max = 0.05 (CEA India limit) on IEEE RTS; the single negative instance is Case 1 at -0.000113. Untested boundary: other regulatory LOLP_max values (US DOE 0.002, EU 0.008) shift the zero-crossing, and the margin does not capture severity of a specific single contingency, only the aggregated 24-hour LOLP.
- **Sources**: [-0.000113 ← evidence/tables/table11.md «Operating Margin | -0.000113 | 0.0130613 | 0.0346654 | 0.05» [result]; 0.05 ← evidence/tables/table13.md «Estimated value | -0.000113 | 0.0130613 | 0.0346654 | 0.05» [result]; 0.05 ← src/environment.md «LOLP_max = 0.05 from Central Electricity Authority» [input]]
- **Status**: supported
- **Falsification criteria**: Find a schedule with a negative operating margin that is nonetheless demonstrably feasible with headroom under the same LOLP_max, or a positive-margin schedule that fails to meet demand under a single contingency — i.e. the margin's sign does not track feasibility.
- **Proof**: [E05, E06]
- **Evidence basis**: Table 11/Table 13 give margins -0.000113 (Case 1, "does margin exist? No", working on extreme limits), 0.0130613 (2a), 0.0346654 (2b), 0.05 (2c); Case 1's negative margin is described as heightened probability of failure if generation is not augmented.
- **Dependencies**: C04
- **Tags**: operating-margin, feasibility, metric

## C06: A 10% spinning reserve keeps N-1 generator contingencies feasible while only re-pricing a subset
- **Statement**: With a 10% spinning reserve, the day-ahead schedule maintains supply-demand balance under every simulated single-generator outage, so N-1 contingencies do not threaten dispatchability at this reserve; their only operational effect is a cost increase concentrated in the high-capacity outages, leaving most contingencies economically negligible.
- **Conditions**: Holds at 10% SR (CM 310.5 MW) on IEEE RTS where post-outage available capacity never drops below the 2670 MW peak demand for outages at buses 1, 2, 7, 13; non-zero LOLP arises only for outages at buses 15, 18, 21, 23. Untested boundary: reserve below the level that keeps post-outage capacity above peak demand, and demand profiles with higher peaks.
- **Sources**: [2670 MW ← evidence/figures/figure6.md «11 | 2670 (peak) |» [result]; 2508 ← evidence/tables/table7.md «6 | 18 | 400 | 2508 | 0.000909» [result]]
- **Status**: supported
- **Falsification criteria**: Observe an N-1 generator outage at 10% SR that drives post-outage available capacity below peak demand for a bus the paper lists as safe (1, 2, 7, 13), causing infeasibility rather than a mere cost change.
- **Proof**: [E02, E03]
- **Evidence basis**: §VII text states n-1 with 10% SR "doesn't have any significant impact on DA UC implementation since the supply-demand balance is maintained"; Table 7 COPT shows post-outage capacity ≥ 2670 MW except for buses 15, 18, 21, 23; only those buses carry non-zero generation-unavailability probability.
- **Dependencies**: C02, C04
- **Tags**: feasibility, spinning-reserve, supply-demand-balance

## C07: The same generators/buses stay critical or robust across reserve levels, so criticality is a reserve-invariant property
- **Statement**: The identity of critical contingencies and weak buses (and of stable contingencies and robust buses) is preserved as the spinning reserve is swept from 10% down to 0%, indicating that generator-level criticality on this system is a structural property of capacity and location rather than an artifact of the chosen reserve margin — reserve changes the magnitude of the cost/reliability impact, not which generators dominate it.
- **Conditions**: Holds across Case 1 and Case 2a/2b/2c on IEEE RTS; robust-bus set gains bus 1 (and stable contingency 1) only in Case 2c, a minor extension. Untested boundary: whether criticality identity is preserved under demand growth, network reconfiguration, or transmission contingencies.
- **Sources**: [6, 7 ← evidence/tables/table12.md «Critical Contingencies (Cy) | 6, 7 | 6, 7 | 6, 7 | 6, 7» [result]; 18, 21 ← evidence/tables/table12.md «Corresponding weak buses | 18, 21 | 18, 21 | 18, 21 | 18, 21» [result]]
- **Status**: supported
- **Falsification criteria**: Show a reserve setting under which a different generator/bus becomes the most critical (or a previously weak bus becomes robust) purely due to the reserve change, with capacity and location held fixed.
- **Proof**: [E02, E06]
- **Evidence basis**: Table 12 lists critical contingencies Cy6,7 and weak buses 18,21 identically for Case 1 and all three Case 2 conditions; stable contingencies 4,5 and robust buses 13,15 are identical too, with 2c adding contingency 1 / bus 1.
- **Dependencies**: C02, C03
- **Tags**: criticality, robustness, invariance

## C08: Probabilistic reliability (LOLP) is a direct, monotone function of dispatchable-capacity headroom over peak demand
- **Statement**: Loss-of-load probability under N-1 contingencies is governed by whether post-outage available capacity can cover the hourly forecasted demand; because raising reserve reduces the dispatchable capacity that remains above peak demand for the largest outages, LOLP is a monotone function of the capacity-headroom the reserve policy leaves, and it collapses to zero exactly when every bus retains enough capacity after any single outage.
- **Conditions**: Established on IEEE RTS with hourly demand peaking at 2670 MW; LOLP is aggregated over 24 hours from per-hour, per-contingency probabilities under the single-unit-outage assumption. Untested boundary: multi-unit outages (excluded here), correlated failures, and hours where demand exceeds the values tabulated.
- **Sources**: [0 ← evidence/tables/table13.md «Evaluated LOLP | 0.050113 | 0.0369387 | 0.0153346 | 0» [result]; 3105 ← evidence/tables/table2.md «Total Available Generation capacity = 3105» [result]]
- **Status**: supported
- **Falsification criteria**: Observe non-zero LOLP in a case where post-outage available capacity exceeds peak demand for every single-generator outage, or LOLP staying constant while capacity headroom changes materially.
- **Proof**: [E04, E05]
- **Evidence basis**: Case 2c (0% CM, full 3105 MW dispatchable) yields LOLP = 0 because "all buses carry sufficient generation capacity even after the loss of one generator" (§VII); non-zero LOLP in Cases 1/2a/2b arises only for hours/contingencies where forecasted demand exceeds post-outage capacity (Tables 9, 10).
- **Dependencies**: C04, C06
- **Tags**: LOLP, reliability, capacity-headroom
