# Problem Analysis

## Observations

**O1 — Increasing DG penetration creates bidirectional power flows and operational uncertainty in distribution networks.**
> "High penetration of distributed generation (DG) and flexible loads is transforming distribution networks from passive, unidirectional systems into active, bidirectional 'generation-network-load-storage' systems. However, the resulting uncertainties and fluctuations on both generation and load sides challenge grid stability and efficiency." (Section 1.1, p. 1–2)

**O2 — Traditional solutions (grid reinforcement, demand-side management, reactive compensation) lack the speed and adaptability to handle renewable intermittency at the distribution level.**
> "Traditional methods—such as grid reinforcement, demand-side management, and conventional reactive compensation—lack the speed and adaptability to address real-time imbalances from renewable intermittency. Insufficient resilience can lead to voltage and frequency deviations, cascading failures, and even large-scale blackouts with severe economic impacts." (Section 1.1, p. 2)

**O3 — Existing cluster-based or centralized DESS planning approaches rely on simplified representations of load dynamics and renewable uncertainty.**
> "While many existing centralized or cluster-based DESS architectures are effective in maintaining regional power equilibrium and voltage regulation, their reliance on simplified or deterministic representations of load dynamics and renewable generation uncertainty may undermine operational resilience, leading to storage over-allocation, reduced utilization efficiency, and suboptimal economic performance." (Section 1.2, p. 2)

**O4 — Node-prioritization-based DESS planning methods mostly assume well-defined network topology and single/representative scenarios, which can produce inefficient configurations for large-scale networks with heterogeneous source–load characteristics.**
> "Most existing DESS planning approaches based on node prioritization and sequential deployment are developed under well-defined network topology and load characteristics, often considering single or representative scenarios and limited functional objectives. Such assumptions may lead to complex, redundant, and economically inefficient configurations when applied to large-scale distribution networks with heterogeneous source–load characteristics." (Section 1.2, p. 3)

**O5 — Existing research focuses on strategic expansion planning with detailed power-flow modeling, but tactical planning-oriented DESS deployment under incomplete network information has received limited attention.**
> "Existing research largely focuses on strategic expansion planning with detailed power-flow modeling, whereas tactical, planning-oriented DESS deployment under incomplete network information—where prioritization, deployment order, and multi-scale resilience assessment are critical—has received relatively limited attention." (Section 1.2, p. 3)

**O6 — China's energy storage capacity is growing rapidly: 21.5 GW added in 2023 alone, with projected cumulative capacity exceeding 200 GW by 2030.**
> "In 2023, China added 21.5 GW of new energy storage capacity, nearly half of the global total. By 2030, cumulative installed capacity is projected to exceed 200 GW." (Section 1.1, p. 2)

**O7 — Distribution networks exhibit diverse regional needs: urban grids prioritize supply reliability, rural grids face excess renewable generation outpacing local consumption.**
> "This growth is driven by varying regional needs: urban grids, where supply reliability is essential despite limited DG penetration, and rural grids, where excess renewable generation often outpaces local consumption." (Section 1.1, p. 2)

## Gaps

**G1 — No existing method integrates demand-driven priority indices with sequential DESS planning under multi-objective optimization and renewable uncertainty for distribution networks.**
Most existing methods treat DESS siting and sizing as a single-stage optimization or use sensitivity indices that only consider voltage or loss, without multi-dimensional quality and efficiency indicators.

**G2 — Existing multi-objective DESS planning lacks a systematic node–block–grid multi-scale resilience evaluation framework.**
Studies report system-level performance but do not jointly assess node-level stability, block-level source-load matching, and grid-wide coordination uniformity.

**G3 — Renewable scenario generation for planning applications often lacks the balance between interpretability (statistical methods) and diversity (deep generative methods).**
The paper argues for GMM as a middle ground, but existing GMM applications in DESS planning do not incorporate RV-coefficient-based initialization for improved clustering of extreme scenarios.

**G4 — No comparative study exists that quantitatively demonstrates the benefit of sequential priority-index updating versus one-shot priority ranking for DESS siting in distribution grids.**
The paper directly addresses this gap through Case 2 (one-shot) vs. Case 3 (sequential) comparison.

## Key Insight

The paper's central insight is that **demand-driven priority indices, when recalculated after each DESS deployment iteration (sequential planning), yield a more balanced spatial configuration of energy storage across heterogeneous grid blocks** compared to either global traversal (exhaustive search) or one-shot priority ranking. The sequential update prevents over-concentration of storage in a single block while maintaining alignment with actual demand intensity, thus improving both economic returns and multi-scale resilience metrics simultaneously.

## Assumptions

1. **Block partitioning is given and follows existing grid planning standards (DL/T 5729-2023).** The paper does not propose a new partitioning method but adopts existing planning outcomes.
2. **Load and renewable generation data are available at the node/block level** from historical measurements (96-point daily profiles with 15-minute resolution) and annual statistical records.
3. **The planning horizon and investment budget are specified by the utility** at the upper planning level, not optimized within the framework.
4. **Demand response capacity is fixed at 10–20% of nodal load**, with critical sectors (administrative, medical, educational) excluded from DR programs.
5. **DG units share uniform power output characteristics** within the same category, differing only in installed capacity.
6. **All indicators are calculated using planning-stage data** (typical daily curves and annual statistics), not high-resolution full-year time-series simulations.
7. **Renewable generation scenarios are stationary** — the GMM is fitted to historical data and scenarios are assumed representative of future operating conditions.
8. **The multi-objective optimization uses a weighted-sum approach** with normalized objectives, which assumes that a single Pareto-optimal solution is sufficient for the planning decision.
