# Concepts

## Microgrid Cluster (MGC)
- **Notation**: —
- **Definition**: A coordinated group of multiple adjacent microgrids whose generation, storage, and load are jointly scheduled — here three independent MGs, each with WT, PV, a dispatchable non-renewable unit (MT or DG), an ESS, and AC load, coordinated by a central Energy Management Center (EMC) that also handles main-grid transactions.
- **Boundary conditions**: The paper's MGC is exactly three MGs on a low-latitude coastal system; MG1/MG3 use diesel generators, MG2 uses a microturbine.
- **Related concepts**: Energy Management Center, Economic Dispatch, Inter-MG power exchange

## Economic Dispatch (of the MGC)
- **Notation**: minimize F_MGC
- **Definition**: The optimal-scheduling problem of choosing each unit's hourly output, ESS charge/discharge, grid purchase/sale, and inter-MG exchange over a 24-hour horizon to minimize a multi-objective cost/penalty function subject to power-balance and equipment constraints.
- **Boundary conditions**: Daily cycle, 1-hour intervals (24 intervals); deterministic forecast inputs.
- **Related concepts**: Objective function, Power balance constraint, Time-of-use pricing

## MGC Objective Function (F_MGC)
- **Notation**: F_MGC = C_Operation + C_Pollution + C_ESS + F_Main-MGC + F_ESS (Eq. 8)
- **Definition**: The scalarized multi-objective fitness combining Operational Costs, Pollution Control Costs, ESS Loss Costs, plus two penalty terms — one for main-grid/MGC power-exchange excursions and one for ESS start/end energy discrepancy.
- **Boundary conditions**: WT/PV treated emission-free; ESS pollutants neglected; penalty coefficients (δ, γ) values not specified in paper.
- **Related concepts**: Penalty function, ESS Loss Cost, Pollution Control Cost

## Grey Wolf Optimization (GWO)
- **Notation**: Eqs. (16)-(19); vectors A, C, a
- **Definition**: A swarm metaheuristic (Mirjalili et al., 2014) that mimics grey-wolf social hierarchy and hunting: the three best solutions (α, β, δ) guide the position update of the remaining (ω) wolves, with a convergence factor a decreasing linearly from 2 to 0 to shift from exploration to exploitation.
- **Boundary conditions**: Prone to local optima and slow convergence in complex, high-dimensional spaces.
- **Related concepts**: Wolf-pack hierarchy, CDGWO, Convergence factor

## CDGWO (improved GWO)
- **Notation**: —
- **Definition**: The paper's enhanced GWO = traditional GWO + Chaos optimization (chaotic-map population initialization) + Dynamic Opposition-Based Learning. "CD" = Chaos + Dynamic-opposition.
- **Boundary conditions**: Chaotic map chosen empirically (Logistic); improvements demonstrated on the MGC dispatch instance.
- **Related concepts**: Chaotic mapping, Dynamic Opposition-Based Learning, GWO

## Chaotic Mapping (in population initialization)
- **Notation**: x_{i+1} = f(x_i) (Table 3: Tent, Sine, Chebyshev, Logistic)
- **Definition**: A deterministic recurrence generating high-randomness, nonlinear sequences that replace uniformly-distributed random numbers when seeding the optimizer's initial population, to widen search diversity and reduce dependence on initial-solution/parameter choices.
- **Boundary conditions**: Different maps suit different problems; Logistic and Chebyshev judged best-suited here; chaos benefits early convergence and decays later.
- **Related concepts**: Logistic map, Chebyshev map, CDGWO

## Dynamic Opposition-Based Learning (DOBL)
- **Notation**: r = sin(t/T); X̃_i(t) = pop_max + pop_min − r·X_i(t) (Eq. 20)
- **Definition**: An opposition-based learning variant that generates reverse (opposite) candidate solutions using a dynamic factor r that changes nonlinearly with iteration t (T = total iterations), so reverse-solution generation tracks the evolving search landscape instead of using a static opposite.
- **Boundary conditions**: Advances static OBL/ROBL; applied to all individuals each iteration.
- **Related concepts**: Opposition-Based Learning, CDGWO, Search diversity

## Penalty Function (Main-MGC and ESS)
- **Notation**: F_Main-MGi = δ·Σ(P_MG,i − P_MI,i) (Eq. 13-14); F_ESS = γ·|Σ P_dis·η_dis + Σ P_ch/η_ch| (Eq. 15)
- **Definition**: Two soft-constraint terms added to the objective: (i) penalize main-grid/MGC power exchange exceeding predefined limits (coefficient δ), improving power quality; (ii) penalize discrepancies in ESS energy between the start and end of the operating cycle (coefficient γ), extending ESS lifespan.
- **Boundary conditions**: δ, γ magnitudes not specified in paper; penalties make fitness ≠ actual cost.
- **Related concepts**: Objective function, ESS Loss Cost, Power quality

## ESS Loss Cost and State-of-Charge (SOC)
- **Notation**: F_ESS = m_ESS·Σ∫|P_SCi|·f(SOC_SCi)dt; m_ESS = C_Investment/Q_ESS (Eq. 12); SOC^min ≤ SOC(t) ≤ SOC^max (Eq. 7)
- **Definition**: ESS loss cost charges the storage-degradation impact of charge/discharge depth and frequency, scaled by a unit loss coefficient m_ESS (investment cost / lifetime throughput). SOC is the battery energy state, bounded here to [30%, 90%] to protect battery life.
- **Boundary conditions**: SOC operating window 30%-90% in this study (general practice 20-30% min, 90-95% max); supercapacitor-based storage model.
- **Related concepts**: Capacity constraint, Charge/discharge constraint, Peak shaving

## Time-of-Use (TOU) Pricing
- **Notation**: —
- **Definition**: A dynamic tariff where grid electricity rates vary by hour — higher at peak demand, lower off-peak — used to compute MGC operational revenue and to incentivize load/storage shifting to off-peak periods.
- **Boundary conditions**: Region-specific tariff (Figure 5); inter-MG trading price is flat across the day.
- **Related concepts**: Economic dispatch, Energy arbitrage, Operational cost

## Convergence Variance
- **Notation**: S²_Con = (1/N)·Σ(F_i − F̄)² (Eq. 21)
- **Definition**: The mean squared deviation of the optimal fitness value across N repeated runs; a lower value indicates more consistent, stable optimization; a higher value indicates randomness/instability.
- **Boundary conditions**: Requires multiple runs; used as a stability indicator in the algorithm comparison.
- **Related concepts**: Optimal fitness value, Algorithm stability, Benchmarking
