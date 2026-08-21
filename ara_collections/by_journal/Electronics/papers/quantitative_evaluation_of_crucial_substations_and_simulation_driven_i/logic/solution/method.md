# Method — Criticality Scoring + Simulation-Driven Delay Impact Assessment

The framework has two coupled stages: (A) a static AHP-based criticality score for planned substations, and (B) a dynamic multi-voltage grid-evolution simulation used to quantify — and to validate the score against — the incremental cost of a commissioning delay. The exact index/objective/constraint equations are in [formulation.md](formulation.md); this file describes the procedure and design choices.

## Stage A — Quantitative criticality scoring (§2)

### A1. Evaluation indices (§2.1, Eqs. 1–5)
For each candidate substation $i$, five indices are computed from load allocation and 10 kV topology:
1. **Substation load level** $x_{i1}=\sum q_i$ — aggregate served load demand (operational significance).
2. **Influence on low-voltage grid** $x_{i2}=\sum n_i$ — number of connected 10 kV feeder lines (breadth of downstream service).
3. **Power supply coverage** $x_{i3}=\max l_i$ — distance to the farthest supplied load point (service radius).
4. **Spatial influence** $x_{i4}=\sum l_i$ — total length of connected 10 kV lines (geographical footprint).
5. **Load density** $x_{i5}=\sum l_i / n_i$ — average substation-to-load distance (load concentration).

### A2. AHP weighting (§2.2, Table 1–3)
- Build a 5×5 pairwise comparison matrix on the Santy 1–9 scale (Table 2).
- Derive weights by column-sum normalization then row averaging → weights (Table 3): load level 0.385, LV-grid influence 0.043, coverage 0.120, spatial influence 0.226, load density 0.226.
- Verify consistency: CR = 0.00726 < 0.1 (acceptable).

### A3. Normalization and composite score (Eqs. 6–7)
- Sum-normalize each raw index across the $n_p$ substations being scored: $X_{ij}=x_{ij}/\sum_i x_{ij}$ (Eq. 7) — chosen over fixed-limit normalization to avoid subjective score bounds.
- Composite importance: $score_i=\sum_{j=1}^5 w_{ij}X_{ij}$ (Eq. 6).
- Rank substations; high scores = critical substations.

## Stage B — Multi-voltage grid evolution simulation (§3)

### B1. Model structure
- Co-plans 220 kV, 110 kV, and 10 kV networks; **decision variables**: optimal siting/sizing of 220 kV and 110 kV substations and the 110 kV network reconfiguration strategy.
- **Objective**: minimize per-horizon total construction+operating cost (Eq. 8), summing annualized 220/110 kV substation cost (Eqs. 9–10), 110 kV line cost (Eq. 11), and 10 kV line cost incl. network-loss conversion (Eq. 12).
- **Rolling optimization**: starts from the previous period's topology and evolves forward across horizons (2020→2025→2035), yielding an evolutionary trajectory rather than a single-shot plan.

### B2. Automatic topology reconfiguration (contribution 3)
A specialized routine autonomously connects newly built substations to the existing grid:
- 110 kV: new-line construction plus adaptive tee-off ('3T') breakout retrofits onto existing 110 kV infrastructure (loop + '3T' architecture, Figures 1–2).
- 10 kV: enforces N-1 security with (n+1) redundancy; when load exceeds capacity thresholds, provisions additional feeders and connects to the nearest under-loaded substation.
- Radial dual-supply is preserved by a traveling-salesman-type anti-loop constraint (Eq. 21); on detected loop closure or overload, connections are automatically reassigned.

### B3. Solver (§3.3)
- Genetic algorithm. Genes: $2\times(N+M)$ substation x/y coordinates plus $M$ upstream-connection genes for new 110 kV substations. Infeasible candidates receive a large penalty in the fitness (cost) function.
- Parameters: max generations 200, population 800, crossover rate 0.5, mutation rate 0.5.

## Stage C — Delay impact assessment and score validation (§4)

### C1. Incremental-cost measurement
- Run the baseline (all substations on schedule) to get reference per-layer costs (Table 6, Figure 4).
- For a delay scenario, postpone one substation's commissioning by a horizon (2020→2025), re-run the evolution, discount annual investments (8%) to the initial year, and compute
  incremental cost = (cumulative converted total for delay scenario − baseline) / baseline.

### C2. Paired and swept experiments
- **Paired** (§4.3): delay high-criticality No. 1 vs low-criticality No. 6, comparing magnitude, layer concentration, and temporal persistence (Figures 5–6, Table 6).
- **Swept** (§4.4): defer each of the six substations individually, pair incremental cost with importance score, and fit a linear regression to test the score–cost relationship (Table 7, Figure 7).

### Design rationale
The static score is cheap but unvalidated; the simulation is expensive but physically grounded. Running the simulation once over all six candidates and showing the score predicts its incremental-cost ranking converts the score into a standalone screen for construction sequencing, and the demonstrated positive cost gradient justifies the "defer least-critical first" rule.
