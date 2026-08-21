# Concepts

Technical terms as defined/used in Yang et al., Electronics 2023, 12, 4230. Symbols follow the
paper's Nomenclature (pp. 29–30).

## Island division and operation stage
- **Notation**: islands k ∈ Ω, node/line states y_{i,k}, y_{ij,k}
- **Definition**: The first fault-handling stage: when faults strike both the distribution system
  and the superior grid and the superior grid cannot supply power, the distribution network
  integrates its internal DG resources to form small-scale distribution islands that keep important
  loads supplied. Each DG must be assigned to exactly one island (Eq. 3), and a line assigned to an
  island drags both end nodes into the same island (Eqs. 4–5).
- **Boundary conditions**: Applies while the superior grid is unavailable; islands must be radial
  and self-sufficient (Eq. 13).
- **Related concepts**: Fault recovery stage, Radiality constraints, Load weight coefficient

## Fault recovery stage
- **Notation**: recovery objective Eq. (35); load restoration state w_i; switch state z_d
- **Definition**: The second stage, after the superior grid restores supply: outage loads are
  reconnected to the main network through distribution lines, possibly with network reconstruction.
  Objectives (weighted, Eq. 35): maximize restored load (weighted by β_i), minimize network loss,
  minimize switching actions. Loads supplied during islanding must not be cut off (Eq. 38).
- **Boundary conditions**: The superior grid may still be fragile; exchange power with the main
  network is capacity-limited (Eq. 39).
- **Related concepts**: Island division and operation stage, Recovery-stage load weight,
  Network reconstruction

## Rolling optimization with feedback correction
- **Notation**: T = {t, t+ΔT, …, t+τ_f·ΔT}; ΔT = 15 min
- **Definition**: Scheduling scheme that, at each period t, solves a joint optimization over the
  short look-ahead window T but issues only the next step's plan; when the next period arrives the
  process repeats, correcting for realized deviations. Exploits the higher accuracy of short-term
  wind/PV prediction relative to long-term prediction and avoids committing to a fixed (e.g. 24 h)
  horizon when the troubleshooting time is uncertain.
- **Boundary conditions**: A new island partition is only re-computed when new-energy/load changes
  exceed the thresholds of Eq. (2); otherwise the existing partition persists and only DG dispatch
  is re-optimized.
- **Related concepts**: Island division and operation stage, Scenario generation and reduction

## Load weight coefficient (island stage)
- **Notation**: α_{i,k}
- **Definition**: Static importance weight of node i's load in island k, set by load level:
  first-level loads weight 100, second-level 10, third-level 1 (Table 2). In the islanding
  objective (Eq. 1), α_{i,k}·P^s_{i,k,t} penalizes shedding important loads, driving them into
  islands.
- **Boundary conditions**: Fixed per node; does not reflect what happened during island operation
  (that is β's job).
- **Related concepts**: Recovery-stage load weight, Island division and operation stage

## Recovery-stage load weight
- **Notation**: β_{i,k} = α_{i,k} + ξ1·Σ_{t∈TIS}|y_{i,k,t} − y_{i,k,t−1}| + ξ2·Σ_{t∈TIS}|y_{i,k,t} − 1| (Eq. 36)
- **Definition**: Recovery-phase weight of node i's load that couples the two stages: the static
  weight α_{i,k} plus a penalty proportional to how often the node's island membership changed
  (second term) and how long it went unsupplied (third term) during islanding. ξ1, ξ2 are positive
  constants (values not specified in paper).
- **Boundary conditions**: Only meaningful when island operation preceded recovery; with
  ξ1 = ξ2 = 0 it degenerates to the static-weight comparison method of §5.3.4.
- **Related concepts**: Load weight coefficient, Fault recovery stage, User electricity satisfaction

## Radiality (topology) constraints
- **Notation**: flow-direction variables ϕ_{ij,t}; Eqs. (6)–(12); big-M constant M_e
- **Definition**: Constraint family that forces each energized island/network to remain a tree:
  power flows only along oriented lines (Eqs. 6–7 with big-M), non-source nodes have at most one
  supplying parent (Eq. 12), each non-faulty line is oriented exactly one way (Eq. 10), faulty
  lines carry no flow (Eq. 11); source-node rules (Eqs. 8–9) are relaxed to Eq. (37) in the
  recovery stage where the main grid participates.
- **Boundary conditions**: Needed only when the partition/topology is re-decided; if Eq. (2)'s
  thresholds are not exceeded, Eqs. (3)–(12) are dropped from the rolling model.
- **Related concepts**: Island division and operation stage, Network reconstruction

## Second-order cone relaxation of branch power flow
- **Notation**: U²_{i,t}·I²_{ij,t} ≥ P²_{ij,t} + Q²_{ij,t} (Eq. 16); big-M voltage-drop Eqs. (19)–(20)
- **Definition**: Convexification of the branch-flow (DistFlow) power-flow model: the nonconvex
  equality coupling voltage, current, and power is relaxed to a rotated second-order cone
  inequality, with nodal balances (Eqs. 17–18) and big-M voltage-drop inequalities (M_v = U²_max)
  that deactivate for disconnected lines. The paper states the relaxation is accurate in radial
  distribution networks. Standard SOC form and feasible region: Eqs. (43)–(45).
- **Boundary conditions**: Exactness asserted for radial networks; no formal proof given in the
  paper (see evidence/proofs/socp_relaxation.md).
- **Related concepts**: Radiality constraints, Scenario-weighted SOCP

## Scenario generation and reduction (restoration)
- **Notation**: sample scale N; cluster count K; Euclidean distance Eq. (46); weights ρ_i; Ψtyp
- **Definition**: Two-step uncertainty handling: (i) generation — Latin hypercube sampling of N
  daily wind/PV output curves from the fitted uncertainty models (Weibull wind speed Eq. 40 with
  turbine curve Eq. 41; normal PV prediction error Eq. 42) around a typical-day base profile;
  (ii) reduction ("restoration") — K-means clustering of the N curves into K representative
  scenarios, each weighted by its cluster size. In the case study N = 500, K = 5.
- **Boundary conditions**: Quality depends on the fitted distributions and the typical-day base
  profile; the paper measures wind data from a Hubei microgrid project.
- **Related concepts**: Extreme scenario set, Rolling optimization, Scenario-weighted SOCP

## Extreme scenario set
- **Notation**: Ψcom = Ψtyp ∪ {(P^wind_{i,max}, P^pv_{i,min}), (P^wind_{i,min}, P^pv_{i,max})} (Eq. 47)
- **Definition**: The reduced typical-scenario set augmented with the two boundary scenarios —
  maximum wind with minimum PV, and minimum wind with maximum PV — to keep the fault-recovery
  strategy resilient to fluctuations beyond the typical scenarios.
- **Boundary conditions**: Extremes are per-node output bounds, not correlated multi-day extremes.
- **Related concepts**: Scenario generation and reduction, Scenario-weighted SOCP

## Scenario-weighted SOCP (uncertainty-aware model)
- **Notation**: min Σ_{s∈Ψcom} ρ_s·f(x, y_s) s.t. SOC + g(x,y_s)=0, h(x,y_s)≤0 ∀s (Eq. 48)
- **Definition**: The deterministic islanding/recovery SOCP (Eq. 45) extended over the expanded
  scenario set: one shared decision x with scenario-dependent constraints, objective weighted by
  scenario probabilities ρ_s. Solved with CPLEX 12.10.
- **Boundary conditions**: Tractability rests on the small reduced scenario set (C02).
- **Related concepts**: Second-order cone relaxation, Extreme scenario set

## Semi-physical (hardware-in-the-loop) simulation
- **Notation**: —
- **Definition**: Validation setup in which the distribution-network environment runs on an OPAL-RT
  real-time simulator while the proposed strategy executes on a physical DSP controller connected
  through analog/digital I/O; node voltages are observed on an oscilloscope. Verifies that the
  strategy works as an online controller, not only as an offline optimizer.
- **Boundary conditions**: Network is simulated (not a field grid); controller and measurement
  chain are physical.
- **Related concepts**: Fault recovery stage, Island division and operation stage
