# Concepts

## C01: Branch Flexibility Adequacy (FBF)

**Notation:** FBF, F^BF_c

**Definition:** A branch-level metric quantifying the capacity of a distribution network branch to accommodate variability and disturbances while maintaining stable operation. It is calculated as the average of individual branch flexibility contributions (F^BF_c) across all branches N_c in the network over time horizon T.

**Mathematical Expression:**
FBF = sum_{c in N_c} F^BF_c / T

where FBF is incorporated into the upper-layer objective as:
max [ (C_loss - min(C_loss)) / (max(C_loss) - min(C_loss)) - (FBF - min(FBF)) / (max(FBF) - min(FBF)) ]

**Boundary Conditions:**
- Normalized to [0, 1] range through min-max normalization.
- Defined for radial or weakly meshed distribution networks.
- Time-averaged over the dispatch horizon T.
- Requires branch current and voltage measurements or estimates.

**Related Concepts:** Flexibility deficit (inverse concept), Grid branch flexibility adequacy (aggregate), Power loss cost (used jointly in objective).

---

## C02: Distributionally Robust Optimization (DRO) with Comprehensive Norm Ambiguity Set

**Notation:** DRO, ambiguity set Psi, 1-norm bound theta_1, infinity-norm bound theta_inf

**Definition:** A two-stage optimization approach where the first-stage decisions (x, including substation power purchase, GT generation, ESS operation) are made before uncertainty is realized, and second-stage decisions (y, including transferable loads, curtailment, flexibility deficit recovery) adapt to each scenario. Uncertainty is captured through an ambiguity set Psi constructed from historical data with joint 1-norm and infinity-norm constraints on scenario probability deviations.

**Mathematical Expression:**
min_x f1(x) + max_{p_k in Psi} sum_{k=1}^K p_k * min_{y_k} f2(y_k)

where:
Psi = {p_k | p_k >= 0, sum p_k = 1, sum |p_k - p^0_k| <= theta_1, max |p_k - p^0_k| <= theta_inf}

theta_1 = K/(2M) * ln(2K/(1-alpha))
theta_inf = 1/(2M) * ln(2K/(1-alpha))

**Boundary Conditions:**
- Requires historical data of sufficient sample size M for reliable ambiguity set construction.
- Number of clusters K determines scenario granularity.
- Confidence level alpha governs conservatism (higher alpha -> larger ambiguity set -> more conservative).
- Assumes the true probability distribution lies within the constructed ambiguity set.

**Related Concepts:** Stochastic programming (special case with degenerate ambiguity set), Robust optimization (special case with worst-case singleton), Ambiguity set, Two-stage optimization.

---

## C03: Two-Layer Bilevel Optimization Architecture

**Notation:** Upper-layer model, Lower-layer model, feedback loop

**Definition:** A hierarchical optimization structure where the upper layer solves network topology and reconfiguration decisions (branch switching states, grid partitioning) using the FBF index and power loss minimization as objectives, while the lower layer performs distributed robust dispatch for each sub-grid under uncertainty. The lower layer feeds dispatch results back to the upper layer, which adjusts its strategy iteratively until convergence.

**Mathematical Expression:**
Upper: max_{l, topology} [ normalized(C_loss) - normalized(FBF) ]
Subject to: Disflow power flow constraints (3)-(6), security constraints (7)-(9), substation constraints (10)
Lower: min_x f1(x) + DRO_{p in Psi} [sum p_k * min_{y_k} f2(y_k)]
Subject to: resource constraints, grid-specific limits

**Boundary Conditions:**
- Requires radial or weakly meshed topology (Disflow assumption).
- Upper-layer decisions (branch states l) are binary; lower-layer variables are continuous.
- Convergence requires sufficient iterations between layers.
- The big-M relaxation (Equation 6) requires M sufficiently large to avoid numerical issues.

**Related Concepts:** Bilevel programming, Stackelberg game, Decomposition, Web-of-cells (related architecture from literature).

---

## C04: Hybrid ACO-FHO-DE Metaheuristic Algorithm

**Notation:** ACO (Ant Colony Optimization), FHO (Fire Hawk Optimization), DE (Differential Evolution)

**Definition:** A hybrid metaheuristic optimization algorithm combining three nature-inspired algorithms: ACO for global path exploration and initial solution construction via pheromone-based path selection probability P^k_ij(t); FHO for local refinement using adaptive weight position updates; DE for population diversity through mutation (V_i^t = X_{r1}^t + F * (X_{r2}^t - X_{r3}^t)), crossover (U_{ij}^t), and selection. Tent chaos mapping initializes the population to enhance diversity, and an adaptive weight w(t) balances global and local search.

**Mathematical Elements:**
Tent chaos: x_{n+1} = x_n/mu for 0 <= x_n < mu, (1-x_n)/(1-mu) for mu <= x_n <= 1
ACO path probability: P^k_ij(t) = [tau_ij(t)]^alpha * [eta_ij]^beta / sum_{l in N_i^k} [tau_il(t)]^alpha * [eta_il]^beta
FHO update: X_i^{t+1} = w(t) * X_i^t + X_i^t
DE mutation: V_i^t = X_{r1}^t + F * (X_{r2}^t - X_{r3}^t)
Pheromone update: tau_ij(t+1) = (1-rho) * tau_ij(t) + Delta_tau_ij(t)

**Boundary Conditions:**
- Population size, mutation factor F in [0,2], crossover rate CR in [0,1] must be tuned.
- Tent chaos control parameter mu typically = 0.5.
- Pheromone evaporation rate rho and enhancement constant Q require problem-specific tuning.
- Scalability to ultra-large systems not validated (acknowledged limitation).

**Related Concepts:** Metaheuristic, Population-based optimization, Swarm intelligence, Evolutionary algorithm.

---

## C05: Disflow Power Flow with Big-M Convex Relaxation

**Notation:** Disflow, l (branch state 0-1), M (big-M constant)

**Definition:** A simplified power flow model adapted from Baran and Wu's original Disflow for radial distribution networks, modified to include branch switching state variables l (binary: 1 = closed, 0 = open). The non-convex quadratic constraints are relaxed using a big-M convexification approach (Equation 6), enabling the model to handle network reconfiguration with continuous topology adjustments.

**Mathematical Expression:**
sum_{l(j,:)} l * P_{l,t} - sum_{l(:,j)} l * (P_{l,t} - r_l * L_{l,t}) = P_{j,t}
V_{j,t} = V_{i,t} - 2(P_{l,t}*r_l + Q_{l,t}*x_l) + (r_l^2 + x_l^2)*L_{l,t} for l(i,j) in b, l = 1
Convex relaxation: V_{j,t} >= M*(1 - l) + V_{i,t} - 2(P_{l,t}*r_l + Q_{l,t}*x_l) + (r_l^2 + x_l^2)*L_{l,t}
V_{j,t} <= -M*(1 - l) + V_{i,t} - 2(P_{l,t}*r_l + Q_{l,t}*x_l) + (r_l^2 + x_l^2)*L_{l,t}

**Boundary Conditions:**
- Valid only for radial or weakly meshed distribution networks.
- Big-M must be chosen appropriately: too small leads to constraint violation; too large causes numerical ill-conditioning.
- Voltage magnitudes squared (V_{i,t}) and current squared (L_{l,t}) are used to avoid square roots.
- Security bounds: 0 <= L_{l,t} <= (I_l^max)^2, (U_i^min)^2 <= V_{i,t} <= (U_i^max)^2.

**Related Concepts:** Optimal power flow (OPF), Convex relaxation, Second-order cone programming (SOCP), Network reconfiguration.

---

## C06: Comprehensive Norm Ambiguity Set for Scenario Probability

**Notation:** Psi, theta_1, theta_inf, p_k, p^0_k

**Definition:** A confidence set for scenario probability distributions that jointly constrains both the sum of absolute deviations (1-norm) and the maximum individual deviation (infinity-norm) of scenario probabilities from their initial empirical estimates. This joint constraint is tighter than either norm alone and avoids extreme probability distributions while maintaining tractability.

**Mathematical Expression:**
Psi = {p_k | p_k >= 0, sum p_k = 1, sum |p_k - p^0_k| <= theta_1, max |p_k - p^0_k| <= theta_inf}

Where theta_1 and theta_inf are derived from confidence level alpha and sample size M:
theta_1 = K/(2M) * ln(2K/(1-alpha))
theta_inf = 1/(2M) * ln(2K/(1-alpha))

**Boundary Conditions:**
- Requires M historical samples for construction.
- Number of scenarios K affects conservatism (larger K -> larger theta_1).
- Confidence level alpha typically set to 0.9 or 0.95.
- As M -> infinity, theta_1, theta_inf -> 0, reducing DRO to stochastic programming.
- As M -> 0, theta_1, theta_inf -> infinity, reducing DRO to robust optimization.

**Related Concepts:** 1-norm constraint, Infinity-norm constraint, Ambiguity set, Distributionally robust optimization, Confidence interval.
