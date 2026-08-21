# Concepts

## SCMPSO (Second-order oscillatory Chaotic Mapping Particle Swarm Optimization)
- **Notation**: —
- **Definition**: The paper's proposed improved PSO variant, combining four modifications to standard PSO: (1) Henon chaotic-mapping population initialization, (2) an adaptive nonlinear inertia-weight schedule, (3) complementary sinusoidal dynamic learning factors c1/c2, and (4) a second-order oscillation term in the velocity update (Eq. 30) with a mid-run threshold switching between oscillatory and progressive convergence. Used to solve the microgrid economic-environmental dispatch problem.
- **Boundary conditions**: Named inconsistently in the source — expanded as "second-order oscillatory chaotic mapping particle swarm optimization" in the abstract and as "Stochastic Constrained Multi-Objective Particle Swarm Optimization" in the Figure 1 flowchart. Validated on 5 benchmark functions (dim 50) and one 24-h microgrid case.
- **Related concepts**: Particle Swarm Optimization, Chaotic mapping initialization, Second-order oscillation term, Adaptive inertia weight, Dynamic learning factor.

## Particle Swarm Optimization (PSO)
- **Notation**: velocity update V_i^{k+1} = w V_i^k + r1 c1 (Xpbest_i^k - x_i^k) + r2 c2 (Xgbest_i^k - x_i^k); position update X_i^{k+1} = X_i^k + V_i^{k+1} (Eqs. 23-24)
- **Definition**: A population-based stochastic optimizer inspired by collective bird movement; each particle is a candidate solution that updates its velocity toward its own best-known position (pbest) and the swarm's global best (gbest), iteratively converging on individual and global optima.
- **Boundary conditions**: Prone to local optima, premature convergence, and uneven particle distribution (per §4.1); serves as the baseline the paper improves upon.
- **Related concepts**: SCMPSO, CPSO, QPSO, Inertia weight, Learning factor.

## Chaotic Mapping Initialization (Henon mapping)
- **Notation**: X_{i+1}^k = F(x,r) = 1 - a * (X_i^k)^2 + b * X_i^k (Eq. 25); a in [1,2], b in [0,1]
- **Definition**: Replacing random population initialization with a deterministic chaotic sequence (Henon map) to spread initial particle positions more diversely across the search space, improving early global search and convergence speed. Parameter a controls nonlinearity/chaos; b controls symmetry and coupling strength.
- **Boundary conditions**: a in [1,2], b in [0,1], smaller b typically used; produces a D-dimensional vector with values confined per the source's stated range.
- **Related concepts**: PSO, SCMPSO, Population diversity.

## Adaptive Inertia Weight
- **Notation**: b = (fit_i - fit_gbest)/(fit_0 - fit_gbest) (Eq. 26); w = wmax + (wmax - wmin)(1 - 1/b) if b>=1, else wmin + b(wmax - wmin) (Eq. 27); wmax = 0.9, wmin = 0.4
- **Definition**: A fitness-dependent, nonlinearly decreasing inertia weight: large early (strong global search), decreased nonlinearly later (strong local search), driven by the ratio of the current particle's fitness gap to a critical fitness gap.
- **Boundary conditions**: wmax = 0.9, wmin = 0.4; behaviour branches on whether the fitness ratio b >= 1 or b < 1.
- **Related concepts**: PSO, Inertia weight, Exploration-exploitation trade-off.

## Dynamic Learning Factors
- **Notation**: c1 = 2 sin^2[(pi/2)(1 - t/Tmax)] (Eq. 28); c2 = 2 sin^2(pi t / (2 Tmax)) (Eq. 29)
- **Definition**: Iteration-dependent cognitive/social coefficients: c1 (individual/cognitive) monotonically decreasing, c2 (group/social) monotonically increasing, so the swarm emphasizes individual exploration early and social convergence late. Both range over [0,2] and cross at t = Tmax/2.
- **Boundary conditions**: t in [0, Tmax]; realized as sin^2 functions bounded in [0,2].
- **Related concepts**: Learning factor, SCMPSO, Second-order oscillation term.

## Second-order Oscillation Term
- **Notation**: V_i^{k+1} = w v_i^k + u1[Xpbest_i^k - (1+lambda1)Xgbest_i^k + lambda1 Xgbest_i^{k-1}] + u2[Xpbest_i^k - (1+lambda2)Xgbest_i^k + lambda2 Xgbest_i^{k-1}] (Eq. 30); u1=c1 r1, u2=c2 r2 (Eqs. 31-32)
- **Definition**: A modified velocity update that uses both the current and previous global-best positions (Xgbest^k and Xgbest^{k-1}), introducing a controllable oscillation/perturbation near the optimum to enhance solution diversity and escape local minima. lambda1, lambda2 are progressive/oscillation convergence factors.
- **Boundary conditions**: Oscillatory convergence when t <= Tmax/2 with lambda >= (2 sqrt(c r) - 1)/(c r) (Eq. 33); progressive convergence when t > Tmax/2 with lambda <= (2 sqrt(c r) - 1)/(c r) (Eq. 34).
- **Related concepts**: PSO, Dynamic learning factors, Oscillation convergence, Progressive convergence.

## Economic-Environmental Dispatch
- **Notation**: Min C_sun = C1 + C2 (Eq. 6)
- **Definition**: The optimization of distributed-source output over a horizon to minimize total cost, where C1 = operating cost (O&M + fuel + depreciation + grid interaction) and C2 = environmental/pollutant-management cost, subject to power balance and device/emission/ramp constraints.
- **Boundary conditions**: 24-h horizon, 1-h steps; costs in RMB; applies to the PV+WT+DG+ESS+grid microgrid modeled here.
- **Related concepts**: Objective function, Power balance constraint, Pollutant emission constraint.

## Energy Storage State of Charge (SOC)
- **Notation**: SOC.1(t) = (1-delta)Soc(t-1) + Pc*dt*eta_c/Ec (charge, Eq. 4); SOC.2(t) = (1-delta)Soc(t-1) - Pd*dt/(Ec*eta_d) (discharge, Eq. 5)
- **Definition**: The remaining stored energy of the ESS, evolving each period by self-discharge (rate delta), charge power Pc at efficiency eta_c, or discharge power Pd at efficiency eta_d, normalized by rated capacity Ec. Enables peak-shaving/valley-filling.
- **Boundary conditions**: Soc.min <= Soc(t) <= Soc.max (Eq. 18); charge/discharge power capped by Eqs. 19-20.
- **Related concepts**: Energy Storage System, Power balance constraint, Scheduling strategy.

## Merit-order Scheduling Strategy
- **Notation**: —
- **Definition**: The dispatch priority rule: fully utilize PV and wind first; use ESS to buffer their variability; add thermal (DG) output as needed; exchange with the main grid as the final balancing mechanism (buy when short, sell when in surplus).
- **Boundary conditions**: Stated in §3.3 and Figure 1; applied over the 24-h summer case; grid exchange bounded by Eq. 14.
- **Related concepts**: Economic-Environmental Dispatch, Power balance constraint, Energy Storage SOC.
