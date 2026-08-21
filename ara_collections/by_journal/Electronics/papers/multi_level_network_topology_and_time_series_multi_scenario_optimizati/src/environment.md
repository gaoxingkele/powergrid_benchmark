# Environment

- **Language/runtime**: Not specified in paper. No code or implementation artifact is released
  ("Data Availability Statement: Data are within the article."). The work is simulation-based;
  the ARA therefore carries no `src/execution/` code (Rule: no concrete artifact → no stub).
- **Framework**: Not specified in paper (solver is the SABPSO procedure described in §4; no
  software package named).
- **Hardware**: Not specified in paper.
- **Data sources**:
  - 13-node radial distribution test system with distributed PV/WT and a diesel generator
    (§5.1, Figures 7–8) — parameters partially given in-text (discount rate 7.5%, VSC $170/kVA,
    line investment $28,000/km, converter efficiency 95%, planning life 15 years, conventional
    output cost $100/MWh).
  - Modified IEEE33 node distribution system (§5.2, Figure 9): per-node DC-load proportions in
    Table 4; five added load points 33–37 (total 600 kW + j320 kvar; DC proportions 0/30/50/70/
    100%); DG candidate node set {7, 10, 12, 13, 14, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 29,
    30, 31, 32}; DG unit capacity 60 kVA (m × 60 kVA, m = 0…7); new AC line 70,000 RMB/km, new
    DC line 20,000 RMB/km.
  - Regional field data (§5.4, Table 9): maximum annual load rates of feeder/link pairs across
    four substations (A–D) of "a certain region"; region not identified.
- **Key dependencies**: Not specified in paper.
- **Protocols**: multi-objective SABPSO planning procedure (§4.2, 14 steps; Figure 6): probabilistic
  load flow per time slot (t = 1…48) per typical time-series scenario (n = 1…12) per particle;
  constraint-violation penalty to Cmax; Pareto non-dominated sorting with crowding degree and
  elite retention; global optimum by small-niche sharing; final compromise solution by fuzzy
  affiliation and variance assignment. Scenario-generation protocol not specified in paper.
- **Random seeds**: Not specified in paper.
