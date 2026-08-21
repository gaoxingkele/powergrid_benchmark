# Experiments

## E01: Three-Case Comparison (Baseline vs PDR vs PDR+V2G)
- **Verifies**: C01, C05, C06
- **Evidence**: evidence/tables/table1.md through evidence/tables/table4.md; evidence/figures/figure1.md through evidence/figures/figure12.md
- **Run**: MATLAB 2024a + CPLEX 12.7.1 on coupled IEEE 33-bus + 20-node gas system
- **Setup**:
  - Case 1: No PDR, no V2G (EVs as fixed unidirectional charging loads)
  - Case 2: PDR only (TOU with cross-price elasticity, market-stability constraints)
  - Case 3: PDR + bidirectional V2G
  - Horizon: 24 h, hourly resolution
- **Procedure**:
  1. Define TOU price bands and elasticity matrix
  2. Set up DistFlow power flow and Weymouth gas flow constraints
  3. Solve single-instance MILP for each case with CPLEX
  4. Record total operating cost, peak-valley load difference, wind curtailment
- **Metrics**: Total cost, peak-to-valley reduction, wind curtailment, price profiles, gas source profiles
- **Expected outcome**: Case 3 best (lowest cost, flattest load); Case 2 intermediate; Case 1 worst.
- **Baselines**: Case 1 (uncoordinated baseline)
- **Dependencies**: none

## E02: Computational Performance Benchmarking
- **Verifies**: C07
- **Evidence**: §4.2.4
- **Run**: CPLEX 12.7.1 on standard desktop workstation
- **Setup**:
  - Full model: ~15,000 decision variables, ~4,000 binary
  - Includes Weymouth PWL (12 segments/pipeline), EV aggregation
- **Procedure**:
  1. Solve Case 3 configuration
  2. Record solution time and optimality gap
- **Metrics**: Wall-clock time to 0.01% optimality gap
- **Expected outcome**: Convergence within seconds to 0.01% gap.
- **Baselines**: None
- **Dependencies**: E01

## E03: Ablation Study
- **Verifies**: C02, C03, C04
- **Evidence**: evidence/tables/table4.md (ablation results)
- **Run**: Same toolchain as E01
- **Setup**:
  - Base: Full Case 3 configuration
  - Ablations: Without LCOE, Without P2G, Without gas-network constraints, Wind penetration −30%
- **Procedure**:
  1. Remove each component individually from the full model
  2. Re-solve and record ∆Total Cost and ∆Wind Curtailment
- **Metrics**: Cost change (%), curtailment change (percentage points)
- **Expected outcome**: P2G removal increases curtailment most; wind reduction increases cost most; LCOE removal affects cost accounting only; gas constraints non-binding.
- **Baselines**: Full Case 3 (reference)
- **Dependencies**: E01
