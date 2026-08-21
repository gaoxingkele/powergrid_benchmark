# Algorithm — Improved PSO (IPSO) for the Upper-Level Model

The upper-level multi-objective model is solved by an improved PSO whose parameters are tuned by the Dung Beetle Optimizer (DBO); the lower level is solved by CPLEX 12.10 each iteration. Equation numbers per source (§3.3.1).

## Novel mechanisms

### 1. Adaptive (nonlinearly decreasing) inertia weight — Eq. (26)
w = w_max · ((t−1)/(T−1))^{cos(t/T)} · (w_max − w_min)

- Large w early → strong global search; w decreases over iterations → stronger local search near high-quality solutions.
- t = current iteration, T = max iterations. w_max, w_min values: **Not specified in paper** (a separately reported linearly-decreasing 0.9→0.4 schedule in §4.1 refers to the parameter-setting sanity check, not necessarily Eq. 26's w_max/w_min).

### 2. Sine-function learning factors — Eq. (27)
- c1 = 2·√(1 − |sin(π/2 × t/T)|)   (individual/cognitive factor; larger early → global search)
- c2 = 2·√(|sin(π/2 × t/T)|)        (social factor; larger late → local search)

### 3. Four-subpopulation position update — Eqs. (28)–(31)
The swarm is partitioned into four sub-populations, each with a distinct rule (this is the paper's key diversity mechanism against local optima):
- **Sub-pop 1 (standard PSO)**, Eq. (28): v_i^{t+1} = w v_i^t + c1 r1 (p_{i.best}^t − x_i^t) + c2 r2 (g_{i.best}^t − x_i^t); x_i^{t+1} = x_i^t + v_i^{t+1}
- **Sub-pop 2 (cognitive only)**, Eq. (29): v_i^{t+1} = w v_i^t + c1 r1 (p_{i.best}^t − x_i^t)
- **Sub-pop 3 (social only)**, Eq. (30): v_i^{t+1} = w v_i^t + c2 r2 (g_{i.best}^t − x_i^t)
- **Sub-pop 4 (sine positional perturbation)**, Eq. (31): x_i^{t+1} = (1 + a·sin(π/2 × t/T)) x_i^t, with a random in (0,1)

r1, r2 random in [0,1]; p_{i.best}, g_{i.best} the individual and global best positions.

## Solution procedure (transcribed verbatim from §3.3.2)
1. Input typical daily electric, thermal, and cooling load data, wind/solar power output data, and relevant device parameters.
2. Initialize the improved PSO, randomly generate relevant variables, set the population size and maximum number of iterations.
3. Solve the lower-level model using CPLEX 12.10 to obtain optimal values; transmit variables such as purchased energy to the upper level.
4. Calculate the upper-level objective function values; record the individual best and global best.
5. If the maximum iteration count is not reached, update each particle's velocity/position per the improved PSO and transmit energy-price variables to the lower level; else output the Pareto front solution set.
6. Apply TOPSIS to select the optimal solution and obtain the final dispatch results.

(Flowchart: Figure 3 / evidence/figures/figure3.md. Pseudocode reconstruction of the update rules: src/execution/improved_pso.py.)

## Pareto selection
The solver returns a Pareto front (not a unique solution). TOPSIS computes each solution's relative closeness to the positive- and negative-ideal solutions using operator profit (F1) and the flexibility index (F2) as criteria; the highest-closeness solution is the final scheme (§3.3).

## Reported parameter setting (§4.1)
Population size 50; maximum iterations 200; inertia weight decreasing linearly 0.9 → 0.4; learning factors c1 = 2, c2 = 1.5 (these are the sanity-check settings; note they differ from the adaptive Eq. 26/27 forms — the paper reports both without fully reconciling them).

## Complexity
Not specified in paper. Empirically: IPSO converged in 46 iterations vs 100 (PSO)/73 (DBO), with runtime 105 s vs 134 s (PSO)/117 s (DBO) over 30 runs (Table 7, Figure 16).
