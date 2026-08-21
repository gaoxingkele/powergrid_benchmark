# Concepts

## C01: Decision-Dependent Uncertainty (DDU)

- **Notation**: `p_{ij,t}^d` — failure probability of line (i,j) at time t under hardening level d; depends on both disaster intensity v^k_t and hardening coefficient alpha_d.
- **Definition**: A type of endogenous uncertainty where the probability distribution of a random variable (here, line failure state) depends on the decision variables (hardening level). In this paper, the line failure probability changes with the hardening decision according to Equation (5): p_{ij,t}^{d,k,s} = exp(0.6931 * (v^k_t - alpha_d * V_N) / (alpha_d * V_N)) for V_N < v^k_t < 2V_N.
- **Boundary conditions**: Only applicable where decisions affect outcome probabilities (not applicable to purely exogenous uncertainties like weather forecasts independent of planning). Requires known vulnerability curves linking decision to probability.
- **Related concepts**: Exogenous uncertainty (probability distribution independent of decisions); Endogenous uncertainty (broader class where decisions influence uncertainty parameters).

## C02: Distributionally Robust Optimization (DRO)

- **Notation**: min_x max_p Sum_k p_k min_y c^T y_k — tri-level optimization with worst-case probability distribution p_k in ambiguity set Phi; x: hardening decisions; y: operational decisions.
- **Definition**: A stochastic optimization framework that minimizes expected cost under the worst-case probability distribution within a pre-specified ambiguity set. Unlike robust optimization (protects against all outcomes) and stochastic programming (assumes a single known distribution), DRO protects against distributional ambiguity while avoiding excessive conservatism.
- **Boundary conditions**: Requires definition of an ambiguity set (here, l1-norm and l-infinity-norm constraints around initial distribution). The ambiguity set size is controlled by parameters theta_1 and theta_infinity (or equivalently confidence levels alpha_1, alpha_infinity).
- **Related concepts**: Robust optimization (worst-case over outcomes, not distributions); Stochastic programming (single known distribution); Ambiguity set.

## C03: Multi-Level Line Hardening

- **Notation**: `h_{ij}^d` — binary indicator of whether line (i,j) receives hardening level d, where d = 1,2,...,D; `a_{ij,t}` — availability coefficient of line (i,j) at time t.
- **Definition**: A graduated reinforcement scheme where lines can be hardened to multiple discrete levels, each with different cost (CNY 200k/300k/500k for Levels 1/2/3) and different hardening coefficient (alpha_d = 2/4/6 for Levels 1/2/3). Higher levels imply lower failure probability but higher cost. This contrasts with single-level (binary) hardening where a line is either hardened or not, with no gradation.
- **Boundary conditions**: Levels are discrete (not continuous). Hardening reduces but cannot eliminate failure risk. The total hardening cost is budget-constrained: Sum_{d} Sum_{(i,j)} c^h_{ij,d} * h^h_{ij,d} <= Delta_h.
- **Related concepts**: Differential planning (the broader strategy of targeted, non-uniform reinforcement); Full-level hardening (uniform binary approach).

## C04: Sobol' Global Sensitivity Analysis

- **Notation**: `S_i` — first-order Sobol' index for input variable X_i, measuring direct contribution to output variance; `S_Ti` — total-effect index measuring both direct and interaction contributions; `S_ij` — second-order interaction index.
- **Definition**: A variance-based sensitivity analysis method that decomposes the total variance of a model output V(Y) into portions attributable to each input variable and their interactions: V(Y) = Sum_i V_i + Sum_{i<j} V_ij + ... + V_{1,2,...,n}. First-order index S_i = V_i / V(Y) measures the direct effect of X_i; total-effect index S_Ti = 1 - V_{~i} / V(Y) captures all contributions involving X_i.
- **Boundary conditions**: Requires input variables to be mutually independent (a key assumption). Requires Monte Carlo or Latin Hypercube sampling of the input space. The number of function evaluations grows with the number of inputs and sampling density.
- **Related concepts**: Local sensitivity analysis (derivative-based, examines around a nominal point); ANOVA decomposition; Saltelli sampling.

## C05: Column-and-Constraint Generation (C&CG) with Fault-State Pruning

- **Notation**: `L_low`, `L_up` — lower and upper bounds of the objective; `alpha_cut` — pruning ratio for fault state retention (set to 0.95).
- **Definition**: A decomposition algorithm for solving tri-level optimization problems. The master problem solves the first-stage hardening decisions and lower bound. The subproblem identifies the worst-case probability distribution and computes the upper bound. Endogenous cutting planes iteratively tighten the feasible region with respect to DDU. Fault-state pruning pre-filters low-impact scenarios to reduce combinatorial complexity: only the top R fault states covering alpha_cut of total weighted load loss are retained.
- **Boundary conditions**: Requires finite-step convergence (guaranteed when the ambiguity set is a convex polytope). The pruning ratio alpha_cut trades accuracy for speed (alpha_cut=0.95 yields 1% error and 73% time reduction).
- **Related concepts**: Benders decomposition; Two-stage robust optimization; Scenario reduction.

## C06: Norm-Bounded Ambiguity Set

- **Notation**: `Phi = {p_k >= 0, Sum p_k = 1, Sum |p_k - p_{k,0}| <= theta_1, max |p_k - p_{k,0}| <= theta_infinity}`.
- **Definition**: A set of allowable probability distributions for the disaster scenarios, constructed using l1-norm and l-infinity-norm constraints around the initial empirical distribution p_{k,0}. The l1-norm controls overall deviation (sparsity of perturbations); the l-infinity-norm limits the maximum deviation of any single scenario probability. Bounds theta_1 and theta_infinity are calibrated from historical data size M and confidence levels alpha_1, alpha_infinity.
- **Boundary conditions**: Requires historical samples M to calibrate bounds. The l1-norm is linearly tractable; KL/JS divergences introduce nonlinearities. The set is a convex polytope, enabling efficient optimization.
- **Related concepts**: Wasserstein ambiguity set; KL-divergence ambiguity set; Moment-based ambiguity set.

## C07: Mobile Emergency Generator (MEG)

- **Notation**: `x_{MEG,i}^{k,g}` — binary decision variable for MEG deployment at node i; `P_{MEG,j,t}^{k,g}`, `Q_{MEG,j,t}^{k,g}` — active/reactive power output of MEG at node j, time t; `Delta_MEG` — total MEG budget.
- **Definition**: A transportable emergency generation resource that can be prepositioned at a node before a disaster and activated post-event to supply critical loads. MEG deployment is subject to a budget constraint and each MEG has maximum active/reactive power output limits.
- **Boundary conditions**: Deployed pre-disaster (not mobile during the event). One MEG station is assumed to exist at node 11 in the base case. MEGs are not re-deployed during the disaster horizon.
- **Related concepts**: Distributed generation (stationary vs. mobile); Energy storage systems; Black-start resources.

## C08: Availability Coefficient

- **Notation**: `a_{ij,t}^{k,g}` — availability coefficient of line (i,j) at time t under scenario k and fault state g; `chi_{ij,t}^{d,k,s}` — failure state variable (1 if failed, 0 if operational).
- **Definition**: A composite indicator reflecting whether a line is operational at a given time, accounting for both the hardening decision and the random failure state: a_{ij,t} = 1 - [(1 - H_j) * chi^0_{ij,t} + Sum_d h^d_j * chi^d_{ij,t}]. If no hardening (H_j=0), the line fails if the base failure state indicates failure. If hardened to level d, the line fails if the level-d failure state indicates failure (less likely due to lower p^d_{ij,t}).
- **Boundary conditions**: Values in {0,1} (binary: operational or failed). No partial availability or repair during the disaster horizon. The failure sampling uses a uniform [0,1] random variable compared against p^d_{ij,t}.
- **Related concepts**: Component state model; Bernoulli failure process; Vulnerability curve.
