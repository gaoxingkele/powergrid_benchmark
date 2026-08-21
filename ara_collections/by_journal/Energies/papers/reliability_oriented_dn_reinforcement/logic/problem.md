# Problem Description

## Observations
- Distribution system planning must meet rising electricity demand by adding reliable and affordable components to the power grid.
- Renewable energy resources (wind, PV) are increasingly integrated into distribution networks, improving reliability indices (SAIFI, SAIDI, ENS).
- Reliability assessment is frequently conducted using failure-oriented analytical techniques (FMEA) under N-1 contingency conditions.
- When a fault occurs in a distribution network with DGs, the isolated section may operate in an intentional islanded configuration, requiring generation adequacy assessment.
- Existing approaches treat long-term reinforcement planning and real-time contingency management as separate optimization problems.
- Limited attention has been given to integrating hierarchical restoration and intentional islanding within a unified probabilistic reinforcement framework accounting for renewable intermittency and regulatory reliability thresholds.

## Research Gaps
- Traditional Monte Carlo Simulation approaches [6-8,14,20] have high computational burden and limited suitability for long-term planning optimization.
- Analytical and simplified methods [9-13,15-17,22] have reduced modeling granularity and limited coordination with restoration strategies.
- Operational and recovery models [19,21] often neglect DG intermittency and long-term reinforcement planning.
- Recent ADN planning frameworks [23-28] lack a unified reinforcement planning framework incorporating hierarchical contingency recovery.
- Most existing frameworks do not simultaneously optimize tie line allocation, NO switch placement, feeder upgrades, and substation reinforcement within a single reliability-constrained optimization.
- The combined impact of DG intermittency and synchronized grid connectivity during recovery is largely overlooked.
- Maintaining synchronization during load transfers to mitigate hardware overheating is missing from current simulation-based models.

## Key Insight
The paper proposes a unified planning framework that simultaneously optimizes multiple reinforcement alternatives (tie lines, NO switches, feeder upgrades, substation upgrades) while embedding a two-level operational hierarchy (network restoration followed by intentional islanding) within a probabilistic analytical reliability assessment. This bridges the gap between infrastructure investment and operational flexibility by ensuring that long-term planning decisions account for realistic contingency management strategies and renewable intermittency.

## Assumptions
- N-1 contingency principle: system must remain capable of supplying demand if any single component fails.
- Only outages or failures in substations and lines are considered.
- Load demand follows a normal distribution (determined via K-S test).
- Solar irradiance follows a beta distribution (determined via K-S test).
- Wind speed follows a Weibull distribution (determined via K-S test).
- DG units are customer-owned; the utility does not control their size or location but manages reliability through tie line and switch placement.
- Component failures, load variability, and renewable intermittency are independent events.
- System losses during islanded operation are assumed to be 5% of the islanded load.
- Planning horizon is 15 years divided into three 5-year stages.
- Annual load growth rate of 3%.
- Interest rate of 10%.
- System power factor of 0.9.
- Constant loss assumption (5%) during islanded operations; actual losses may vary dynamically.
