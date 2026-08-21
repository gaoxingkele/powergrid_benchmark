# Method Overview — Two-Stage Islanding Operation + Fault Recovery Pipeline

End-to-end structure of the proposed strategy (referenced by evidence/figures/figure1.md, figure6.md,
figure14.md, figure16.md, figure18.md, figure20.md). Detail files:
[islanding_formulation.md](islanding_formulation.md), [recovery_formulation.md](recovery_formulation.md),
[uncertainty_method.md](uncertainty_method.md), [constraints.md](constraints.md).

## Pipeline

1. **Fault event** — faults in the distribution system AND the superior grid; upstream substation
   outlet breaker trips, so the superior grid cannot supply the distribution network.
2. **Stage 1 — island division & operation** (§2): solve the weighted load-shedding + loss
   objective (Eq. 1) under membership/radiality/capacity/safety/DG constraints (Eqs. 2–34) as a
   rolling optimization (ΔT = 15 min; commit one step, re-solve with feedback correction).
   Re-partition only when the Eq. (2) thresholds are exceeded. Record each node's island-stage
   supply trajectory y_{i,k,t}.
3. **Stage 2 — fault recovery** (§3): once the main grid resumes, solve the recovery objective
   (Eq. 35: restored load − losses − switching) with network reconstruction, using the
   history-aware load weight β_{i,k} (Eq. 36) that carries island-stage churn and outage periods
   into recovery priority. Constraints Eqs. (6),(7),(10)–(12),(14)–(34),(37)–(39).
4. **Uncertainty handling** (§4): wind (Weibull) / PV (normal error) models → Latin hypercube
   generation (N = 500) → K-means reduction (K = 5, weights ρ) → extreme-scenario augmentation
   (Ψcom) → scenario-weighted SOCP (Eq. 48) → CPLEX 12.10.

## Test system (§5.1 — mirrored from Figure 1 / Tables 1–2)
- Improved IEEE 33-node distribution network (nodes 0–32; branches S1–S32; tie switches S33–S37);
  G1 = upstream source behind breaker at node 0.
- 4 DGs: DG1 wind-or-PV 500 kW pf 0.85 at node 6; DG2 energy storage 700 kW pf 0.9 at node 13;
  DG3 diesel 1000 kW pf 0.8 at node 24; DG4 diesel 1000 kW pf 0.9 at node 31.
- Load levels: weight 100 (nodes 5, 6, 12, 13, 23, 24, 29, 31), weight 10 (7, 11, 15, 22, 26, 30,
  32), weight 1 (the remaining 17 nodes).

## Reconfiguration behaviors observed (mirrored from Figures 6, 14, 16, 18, 20)
- Extreme fault (breaker + S28): two islands — Island 1 (2 DGs, 12 loads), Island 2 (2 DGs,
  11 loads) (Figure 6).
- S28 + DG3 fault: S29 opens → DG4 islands; S22 recloses to main grid; node 28 reconnects via tie
  S37 (Figure 14).
- S28 fault only: same S29/DG4 islanding; DG1, DG2 join the reconnected system; node 28 via S37
  (Figure 16).
- S9 + S22 faults: two islands — DG2 supplies nodes 10–16 (S17 opens), DG3 supplies nodes 22–24
  (S3 stays open); S29 recloses; node 17 reconnects via tie S36 (Figure 18).
- Comparison method (β = α): node 28 left unpowered (Figure 20) — the stage-coupling weight is
  what restores it.

## Semi-physical implementation (§6 — mirrored from Figure 21)
- OPAL-RT real-time simulator hosts the distribution-network environment; a DSP controller runs
  the islanding-operation/fault-recovery strategy; analog outputs / digital inputs close the loop;
  an oscilloscope observes node voltages (node 24 = phase reference).
- With PV at node 6 and an S28 fault, the DSP detects the fault, issues switch signals, and the
  network bifurcates into the two islands of Figure 6; three periods of stable islanded waveforms
  are recorded (Figures 22–24).

**Source**: §§2–6.
