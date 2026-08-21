# Concepts

## Transmission Network Expansion Planning (TNEP)
- **Notation**: minimize OF(x) = Σ_{(i,j)∈Ω} c_ij n_ij
- **Definition**: The planning problem of selecting the number and location of new transmission lines (and optionally generation additions) to serve future demand at minimal investment cost, subject to power-balance and operating limits. First formalized by Garver (1970).
- **Boundary conditions**: This paper uses a DC power-flow model (line resistance and reactive flow neglected); the maximum parallel lines between two buses is 4.
- **Related concepts**: Static TNEP, Dynamic TNEP, DC power flow, penalized fitness function.

## Static TNEP (STNEP)
- **Notation**: FF_S(x) = OF_S(x) + ω₁P₁(x) + P₂(x); OF_S(x) = Σ c_ij n_ij (Eqs. 1–2)
- **Definition**: TNEP that determines line location and number for a single planning stage (one time horizon). Solved here for Garver 6-bus and IEEE 25-bus systems.
- **Boundary conditions**: Single planning stage; no discount/interest applied to the objective.
- **Related concepts**: TNEP, Dynamic TNEP, generation resizing.

## Dynamic (Multistage) TNEP (DTNEP)
- **Notation**: FF_D(x) = OF_D(x) + ω₁P₁(x) + P₂(x); OF_D(x) = Σ_{t=1}^{T} [ δ_inv^t Σ_{(i,j)∈Ω} c_ij^t n_ij^t ] (Eqs. 8–9)
- **Definition**: TNEP realized over multiple sequential time intervals/stages, incorporating load growth, inflation, equipment wear and the carry-over effect of one stage on the next. Solved here for the Colombian 93-bus system over 3 planning stages (2002–2005, 2005–2009, 2009–2012).
- **Boundary conditions**: Base year 2002; annual interest rate I = 10%; investment discounted per stage.
- **Related concepts**: Discount factor, Static TNEP.

## Discount factor (investment)
- **Notation**: δ_inv^t = (1 − I)^a (Eq. 10)
- **Definition**: Per-stage factor applied to discount investment cost to the base year, where I is the annual interest rate and a is the difference between the years covered by the planning stage.
- **Boundary conditions**: Used only in the dynamic (multistage) objective; I = 10% in this study.
- **Related concepts**: Dynamic TNEP.

## Penalized fitness function
- **Notation**: FF(x) = OF(x) + ω₁P₁(x) + P₂(x); P₁ = Σ|d_k + B_kθ_k − g_k| (equality), P₂ = Σ λ_l (inequality) (Eqs. 3–7, 11–15)
- **Definition**: The objective augmented with an equality-constraint penalty (nodal power balance) weighted by ω₁ and inequality-constraint penalties λ₁, λ₂, λ₃ (line-flow limit, generation limit, line-number limit) that are 0 when satisfied and a fixed large value otherwise.
- **Boundary conditions**: Penalty weights are system-specific (see heuristics.md); constraints handled softly, not as hard bounds.
- **Related concepts**: DC power flow, TNEP.

## DC power flow
- **Notation**: f_ij (line flow), B_k (susceptance), θ_k (voltage angle)
- **Definition**: Linearized power-flow model considering only active power (neglecting line resistances and reactive flow) used to compute nodal balance and line flows for constraint checking; obtained via MATPOWER.
- **Boundary conditions**: Approximation of AC flow; "produces fast solutions … with acceptable accuracy."
- **Related concepts**: Penalized fitness function, TNEP.

## Coati Optimization Algorithm (COA)
- **Notation**: X_i : x_{i,j}; two-stage update (Eqs. 16–23)
- **Definition**: A bio-inspired population metaheuristic (Dehghani et al., 2023) modeling coatimundis hunting/attacking iguanas (exploration, Stage 1) and escaping predators (exploitation, Stage 2). Half the population climbs trees (Eq. 17), the other half attacks the ground-fallen iguana (Eq. 19); Stage 2 retreats to a nearby safe area (Eqs. 21–22).
- **Boundary conditions**: Greedy acceptance (Eqs. 20, 23) keeps a new position only if it improves the objective.
- **Related concepts**: Fitness-Distance Balance, Opposition-Based Learning.

## Fitness-Distance Balance (FDB)
- **Notation**: SP_i = ω × normF_{P_i} + (1 − ω) × normD_{P_i} (Eqs. 24–28)
- **Definition**: A selection method (Kahraman et al., 2020) that scores each candidate by a weighted combination of its normalized fitness and its normalized Euclidean distance to the current best, then selects a guiding candidate that is both fit and far from the incumbent best to preserve diversity and avoid local traps.
- **Boundary conditions**: A weighting coefficient ω prevents the fitness and distance vectors from dominating one another; ω value not specified in paper.
- **Related concepts**: Coati Optimization Algorithm, exploration/exploitation balance.

## Opposition-Based Learning (OBL)
- **Notation**: x̄ = lb + ub − x (Classical OBL, Eq. 29)
- **Definition**: A technique that, for each candidate, also evaluates an "opposite" candidate under the supposition that the opposite may be closer to the global optimum, increasing convergence speed and search-space coverage. Used here only in the initial-population creation phase of FDBCOA1.
- **Boundary conditions**: Eight schemes evaluated; excessive randomness (e.g. Random OBL) can introduce low-quality candidates.
- **Related concepts**: Elite OBL, initialization.

## Elite OBL (EOBL)
- **Notation**: x̄_ij^E = rand × (lb_j + ub_j) − x_i^E (Eq. 34); reset x̄_ij^E = rand(ub_j − lb_j) if out of bounds (Eq. 35)
- **Definition**: An OBL scheme (Zhou et al., 2012) that treats the current population as elite individuals and forms opposites from them, using the best candidates to guide the opposition and thereby balancing exploration/exploitation; identified as the best OBL scheme (variant OBL5) in this study.
- **Boundary conditions**: Opposite must be reset within bounds when it exceeds limits.
- **Related concepts**: Opposition-Based Learning, FDBCOA1-OBL5.

## Generation resizing (re-planning)
- **Notation**: increases optimization parameters (Garver: 9→11; IEEE-25: 36→46)
- **Definition**: Allowing generator production values to be re-optimized jointly with line-addition decisions, rather than fixing generation; expands the decision vector and can lower total investment cost.
- **Boundary conditions**: Applied in "Case 2" of the static test systems; oscillation (slack) bus fixed.
- **Related concepts**: Static TNEP, transmission-generation coupling.

## Stability metrics (SR%, MIT, MST)
- **Notation**: SR% = (n_sr / total_runs) × 100 (Eq. 39); MIT = (1/n_sr) Σ iter_(i) (Eq. 40); MST = (1/n_sr) Σ st_(i) (Eq. 41)
- **Definition**: Success Rate (fraction of runs producing a feasible solution), Mean of Iteration Number (mean fitness-evaluations to reach a feasible solution over successful runs), and Mean Search Time (mean wall-clock time to feasibility), used to quantify algorithm reliability on constrained problems.
- **Boundary conditions**: Computed over 30 independent runs across seven TNEP case studies; MIT/MST count only successful (feasible) runs.
- **Related concepts**: TNEP, feasibility, No Free Lunch.
