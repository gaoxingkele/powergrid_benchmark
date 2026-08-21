# Experiments

Declarative verification plans. Directional outcomes only — exact values live in `evidence/`.
Claims and experiments are many-to-many.

## E01: Steady-state voltage profile, base vs GA-optimized
- **Verifies**: C01, C02
- **Evidence**: evidence/tables/table3.md, evidence/figures/figure4.md
- **Run**: Power flow + GA optimization on the 6-bus feeder (MATLAB R2025 + PowerFactory 2024);
  method described in §5, no released code — see src/environment.md.
- **Setup**:
  - Model: 6-bus radial distribution feeder; DERs at buses 2, 3, 4
  - Hardware: Not specified in paper
  - Dataset: Line data (Table 1: R, X, thermal limit 200 A) and load data (Table 2: P/Q at buses 2–6)
  - System: GA — population 50, crossover prob. 0.8, mutation rate 0.05, 100 generations; objective
    F = w1·f1 + w2·f2 + w3·f3 with weights (0.4, 0.4, 0.2); constraint 0.95 ≤ V_i ≤ 1.05
- **Procedure**:
  1. Solve base-case power flow, record per-bus voltage.
  2. Run the GA to optimize DER setpoints / reconfiguration under operational + thermal constraints.
  3. Record optimized per-bus voltage; compare against the 0.95–1.05 pu band.
- **Metrics**: Per-bus voltage (pu); minimum bus voltage.
- **Expected outcome**:
  - Optimized minimum bus voltage is higher than base case and lies within the operational band.
  - The base-vs-optimized voltage gap widens with electrical distance from the substation.
- **Baselines**: Un-optimized base case.
- **Dependencies**: none

## E02: Real power loss reduction and GA convergence
- **Verifies**: C01, C03
- **Evidence**: evidence/tables/table4.md, evidence/figures/figure5.md
- **Run**: GA optimization run on the 6-bus feeder (MATLAB R2025 + PowerFactory 2024); §5–§6.
- **Setup**:
  - Model: 6-bus radial feeder; DERs at buses 2, 3, 4
  - Hardware: Not specified in paper
  - Dataset: Table 1 line data, Table 2 load data
  - System: same GA configuration as E01
- **Procedure**:
  1. Record total real power loss (Σ I²R) in the base case.
  2. Run the GA and log per-generation loss (fitness) over the run.
  3. Record optimized total loss; compute the reduction; inspect the convergence trace shape.
- **Metrics**: Total real power loss (kW); loss per GA generation.
- **Expected outcome**:
  - Optimized loss is substantially lower than base case.
  - The convergence curve decreases monotonically and smoothly, with most reduction in early
    generations and a slow tail.
- **Baselines**: Base case (no DER) loss.
- **Dependencies**: none

## E03: Contingency (DER-trip) resilience assessment
- **Verifies**: C01, C04
- **Evidence**: evidence/tables/table6.md
- **Run**: Contingency evaluation of base vs optimized configuration under a fault-induced DER trip at
  bus 3 (MATLAB R2025 + PowerFactory 2024); §6.
- **Setup**:
  - Model: 6-bus radial feeder; DER trip injected at bus 3
  - Hardware: Not specified in paper
  - Dataset: Table 1 line data, Table 2 load data; DER capacities
  - System: base configuration vs GA-optimized configuration (objective includes f3 resilience penalty)
- **Procedure**:
  1. Simulate a fault-induced DER trip at bus 3 for the base configuration; record min voltage,
     number of overloaded branches, and load served.
  2. Repeat for the GA-optimized configuration.
  3. Compare the three resilience metrics; map onto the trapezoidal resilience curve.
- **Metrics**: Minimum bus voltage (pu); count of overloaded branches; load served (%).
- **Expected outcome**:
  - Optimized configuration holds higher min voltage, fewer/zero overloaded branches, and higher
    load served than the base case under the DER outage.
- **Baselines**: Base configuration under the same contingency.
- **Dependencies**: E01, E02

## E04: Optimal DER dispatch pattern
- **Verifies**: C01, C04, C05
- **Evidence**: evidence/tables/table5.md
- **Run**: Extraction of the GA-selected DER real/reactive setpoints (MATLAB R2025 + PowerFactory 2024); §6.
- **Setup**:
  - Model: 6-bus radial feeder; DERs at buses 2, 3, 4 with inverter limits
  - Hardware: Not specified in paper
  - Dataset: Table 1 line data, Table 2 load data
  - System: GA-optimized objective F (voltage + loss + resilience penalty)
- **Procedure**:
  1. Run the GA to convergence.
  2. Read out the optimal P_DER and Q_DER at buses 2, 3, 4.
  3. Relate the dispatch pattern (reactive absorption; central real injection) to the voltage/loss
     outcomes; confirm inverter limits are respected.
- **Metrics**: P_DER (kW) and Q_DER (kVAR) per DER bus; sign of Q; location of largest P.
- **Expected outcome**:
  - DER units absorb reactive power (negative Q) for voltage support.
  - The largest real-power injection sits at the electrically central bus.
- **Baselines**: none (dispatch readout)
- **Dependencies**: E01, E02
