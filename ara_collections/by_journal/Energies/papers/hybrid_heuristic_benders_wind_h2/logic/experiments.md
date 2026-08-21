# Experiments

## Experiment 1: Explicit Non-Convex Problem (N=1000) — Validation Baseline

- **Verifies**: Claim 1 — Commercial solvers are superior for explicit analytical MINLP models. Also verifies that GSOA-Benders can solve explicit problems but with lower performance.
- **Evidence**: Table 1 (page 14 of PDF)
- **Run**: Single run per algorithm on same hardware and scenario set.
- **Setup**: N=1000 scenarios, explicit analytical non-convex hydrogen tank cost (power function C ∝ x^0.6, no sinusoidal perturbation). Wind: binary. Gurobi MINLP vs GSOA-Benders.
- **Procedure**: Both algorithms are run on the mathematically explicit formulation. Gurobi uses its native MINLP branch-and-bound with presolve. GSOA-Benders uses the hybrid framework. Scenario generation, hardware (Intel i5-12490F, 16GB RAM, MATLAB R2023b, Gurobi 12.0.3), and data are identical.
- **Metrics**: Solution time (s), optimal objective value (total annualized cost).
- **Expected outcome**: Gurobi is expected to outperform GSOA-Benders on both speed and solution quality. The experiment is designed to establish the baseline that the proposed method is NOT intended for explicit formulations.
- **Directional results**: Gurobi: 36.58s, objective −381,058.9. GSOA-Benders: 45.66s, objective −342,939.52. Gurobi's presolve eliminated ~25% of problem scale in 0.43s.
- **Baselines**: None needed — this experiment compares the proposed method against the state-of-the-art commercial solver (Gurobi) on its home turf.
- **Dependencies**: None

---

## Experiment 2: Intractable Black-Box Problem (N=500) — Main Benchmark

- **Verifies**: Claims 2, 5, 6 — GSOA-Benders provides a viable framework for black-box WH-IES planning; simulation-based optimization is prohibitive; GSOA-Benders outperforms SFOA-Benders.
- **Evidence**: Table 2 (page 15 of PDF), Figure 6 (convergence curve)
- **Run**: Single run per algorithm on identical scenarios and hardware.
- **Setup**: N=500 scenarios, black-box hydrogen tank cost (power-law x^0.7 + sinusoidal perturbation + minimum threshold). Five algorithms compared:
  - A: Gurobi-Monolithic (direct MINLP)
  - B: MILP-Benders (reformulation via Big-M)
  - C: GSOA+Simulation (exhaustive LP evaluation per fitness call)
  - D: SFOA-Benders (Starfish Optimization Algorithm as master solver)
  - E: GSOA-Benders (proposed)
- **Procedure**: Each algorithm is run on the same scenario set and hardware. Algorithms A and B are attempted directly on the black-box formulation. Algorithms C, D, E execute their respective search procedures. Timeout for C is implicitly set by the estimated runtime (~17,500s).
- **Metrics**: Solution status (converged/failed/timeout), solution time (s), objective value.
- **Expected outcome**: A and B should fail due to inability to handle the black-box cost. C should time out due to prohibitive computation. D and E should both converge to the same objective, with E being faster.
- **Directional results**: A and B: "Direct exact solve unavailable" (0.00s, N/A). C: "Failed (Timeout) >17,500" (N/A). D: 51.15s, −242,940.18. E: 35.86s, −242,940.18. Both D and E found the same objective, confirming solution consistency.
- **Baselines**: Algorithms A (Gurobi MONOLITHIC), B (MILP BENDERS REFORMULATION), C (GSOA+SIMULATION EXHAUSTIVE), D (SFOA-BENDERS)
- **Dependencies**: Experiment 1 establishes that Gurobi is the correct tool for explicit problems. Experiment 2 tests the scenario where explicit formulation is unavailable.

---

## Experiment 3: Sensitivity, Scalability, and Environmental Extension Analysis

- **Verifies**: Claims 7, 8 — Economic interpretation and practical considerations.
- **Evidence**: Table 3 (annualization sensitivity), Section 4.6, Equation (28)
- **Run**: Sensitivity analysis on the GSOA-Benders optimal solution; no re-optimization performed.
- **Setup**: Analysis based on the optimal solution x* = [1, 0.53, 23.23, 0] from Experiment 2.
- **Procedure**:
  1. Project lifetime sensitivity (Table 3): reports annualization factors for 10yr, 20yr, 30yr horizons under straight-line (1/L) and CRF (r=8%) methods.
  2. Scalability boundary: acknowledges empirical range (500-1000 scenarios) and discusses theoretical parallelization potential.
  3. Emission extension: proposes carbon-cost term (Equation 28) that preserves Benders-cut structure.
- **Metrics**: Annualization factors, qualitative interpretation of scalability.
- **Expected outcome**: Longer project horizons reduce annualized capital burden, making capital-intensive assets more attractive. The framework is limited to tested scenario sizes (500-1000). The CO2 extension is linear-compatible.
- **Directional results**: 10yr: CRF 0.149; 20yr: CRF 0.102; 30yr: CRF 0.089. Longer horizons favor capital-intensive assets.
- **Baselines**: None
- **Dependencies**: Experiment 2 provides the optimal solution for sensitivity interpretation.
