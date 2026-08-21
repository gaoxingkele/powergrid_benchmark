# Constraints, Assumptions, and Limitations

## Boundary conditions / constraint families (as formulated in the paper)

### Island-membership and switch-state constraints (§2.2, Eqs. 3–5)
- Σ_{k∈Ω} y_{i,k} = 1 ∀i ∈ N_DG (Eq. 3): every DG node is assigned to exactly one island.
- y_{ij,k} ≤ y_{i,k} and y_{ij,k} ≤ y_{j,k} ∀ij ∈ E, k ∈ Ω (Eqs. 4–5): a line assigned to island k
  requires both end nodes in the same island.

### Radial topology constraints (§2.2, Eqs. 6–12)
- 0 ≤ P_{ij,t} ≤ M_e·ϕ_{ij,t}, 0 ≤ Q_{ij,t} ≤ M_e·ϕ_{ij,t} (Eqs. 6–7): flow only along the oriented
  direction, big-M M_e.
- ϕ_{ij,t} ≥ 0 ∀i ∈ N\N_S; ϕ_{ij,t} = 0 ∀i ∈ N_S (Eqs. 8–9): source-node orientation rules
  (islanding stage). In the recovery stage Eqs. (8)–(9) are REPLACED by ϕ_{ij,t} ≥ 0 ∀i ∈ N
  (Eq. 37) because the main grid participates.
- ϕ_{ij,t} + ϕ_{ji,t} = 1 ∀ij ∈ E\E_F; ϕ_{ij,t} + ϕ_{ji,t} = 0 ∀ij ∈ E_F (Eqs. 10–11): each healthy
  line has exactly one orientation; faulty lines carry none.
- Σ_{j:ij∈E} ϕ_{ji,t} ≤ 1 ∀i ∈ N (Eq. 12): at most one supplying parent per node (tree property).
- Shortcut: if the re-partition trigger Eq. (2) is not met, Eqs. (3)–(12) are dropped from the
  rolling model (the existing partition already satisfies them).

### Island power-supply capacity (§2.2, Eq. 13)
- Σ_{i∈N_k} P^DG_{i,t} ≥ Σ_{i∈N_k} P^L_{i,t} ∀t, k: total island load must not exceed island DG
  generation capacity.

### Safety (line flow / voltage) constraints (§2.2, Eqs. 14–15)
- −S_{ij}·y_{ij} ≤ P_{ij,t} ≤ S_{ij}·y_{ij} (Eq. 14): line-flow limit, zeroed for disconnected lines.
- U_min·y_i ≤ U_{i,t} ≤ U_max·y_i (Eq. 15): node-voltage band, zeroed for de-energized nodes.
- Observed operating band in the case study: node voltages within [1.08, 1.1] pu.

### Second-order cone branch-flow constraints (§2.2, Eqs. 16–20)
- U²_{i,t}·I²_{ij,t} ≥ P²_{ij,t} + Q²_{ij,t} (Eq. 16): SOC relaxation of the branch-flow coupling —
  stated accurate for radial networks.
- Nodal active/reactive balance (Eqs. 17–18).
- Big-M voltage-drop double inequalities (Eqs. 19–20) with M_v = U²_max relaxing disconnected lines.

### Diesel generator constraints (§2.2, Eqs. 21–24)
- Active/reactive output bounds (Eqs. 21–22); ramp-rate limits |P^d_{i,t} − P^d_{i,t−1}| ≤ R^p_i·ΔT
  and reactive analogue (Eqs. 23–24).

### Energy storage constraints (§2.2, Eqs. 25–34)
- Net injection decomposition (Eqs. 25–26); charge/discharge power bounds gated by mutually
  exclusive 0–1 state variables β^dis_{i,t}, β^ch_{i,t} (Eqs. 27–31).
- Energy (state-of-charge) recursion (Eq. 32) with bounds (Eq. 33).
- End-state condition ϱ^es_{i,t} = ϱ^es_{i,t+T} (Eq. 34): storage returns to its initial energy at
  the end of the scheduling horizon.

### Fault-recovery-specific constraints (§3.2, Eqs. 37–39)
- Eq. 37 replaces Eqs. 8–9 (main-grid participation).
- w_i = 1 ∀i ∈ N_k, k ∈ Ω (Eq. 38): loads supplied during islanding must not be cut off during
  recovery.
- −S_{ij}·y_{ij} ≤ P_{ij,t} ≤ S_{ij}·y_{ij} ∀ij ∈ E_S (Eq. 39): distribution↔main-grid exchange
  capacity limit.

### Re-partition trigger (§2.2, Eq. 2)
- A new island scheme is formulated only when island-wise absolute changes in load, wind, or PV
  power versus the last partitioning period t1 exceed thresholds σ^L, σ^wind, σ^pv. Threshold
  values: not specified in paper.

## Assumptions
- A1: Island/network topology is radial; radiality enforced by Eqs. (6)–(12).
- A2: The SOC relaxation of the branch-flow model is accurate for radial distribution networks
  (asserted, not proven — evidence/proofs/socp_relaxation.md).
- A3: Wind speed follows a Weibull distribution (Eq. 40); PV prediction error is normally
  distributed (Eq. 42); PV output distribution follows Eq. (42).
- A4: Scheduling interval ΔT = 15 min; short-term DG-output prediction is more accurate than
  long-term prediction (motivates rolling optimization).
- A5: Storage begins and ends the scheduling horizon at the same energy level (Eq. 34).
- A6: Load importance is exogenous and three-leveled (weights 100/10/1, Table 2).
- A7: DG capacity within each island is sufficient for its assigned load (enforced by Eq. 13,
  presumed feasible for the test system).

## Known limitations
- ξ1, ξ2 (recovery-weight penalty coefficients), µ_loss, ϑ_loss, ϑ_switch (objective weights), and
  the thresholds σ^L/σ^wind/σ^pv are not given numeric values in the paper — reproduction requires
  re-tuning.
- Validation is on a single test system (improved IEEE 33-node) with 4 DGs; scalability to larger
  or meshed networks is untested.
- Uncertainty covers wind and PV only; the conclusion notes other renewable sources are future work.
- Only one comparison/baseline (β = α) is evaluated for the stage-coupling contribution; no
  comparison against other published recovery methods is run.
- The semi-physical experiment simulates the network in OPAL-RT (no field deployment); control
  latency and communication constraints are not quantified.
- No formal exactness proof for the SOC relaxation; standard radial-network result is invoked.
- Optimization algorithm refinement is explicitly deferred to future research (§7).
