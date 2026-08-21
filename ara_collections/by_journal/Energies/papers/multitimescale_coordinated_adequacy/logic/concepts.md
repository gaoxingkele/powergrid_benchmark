# Concepts

## C01: Generalized Adequacy
- **Notation:** Not directly assigned a single symbol; comprises three sub-dimensions.
- **Definition:** An extended concept of power system adequacy integrating (1) power and energy adequacy, (2) flexibility adequacy, and (3) inertia adequacy. Encompasses supply--demand matching across millisecond-to-second (inertia), minute-to-hour (flexibility), and daily-to-annual (power/energy) timescales.
- **Boundary conditions:** Assumes all three dimensions fundamentally rely on effective transmission of electrical energy. Excludes demand-side response resources (EVs, smart buildings) and compound extreme events.
- **Related concepts:** Traditional capacity adequacy, LOLH, EENS, flexibility ramp capacity/rate margin, minimum inertia requirement.

## C02: Loss of Load Hours (LOLH / HLOL)
- **Notation:** HLOL
- **Definition:** Average number of hours per year in which energy shortages occur. Calculated as: HLOL = (1/Y) sum_y sum_d sum_t sgn(max(L_{y,d,t} - S_{GC,y,d,t}, 0)).
- **Units:** h/a
- **Boundary conditions:** Threshold standard: 3 h/a in European practice [7].
- **Related concepts:** EENS, LOLE.

## C03: Expected Energy Not Served (EENS)
- **Notation:** EENS
- **Definition:** Annual average unmet energy demand. Calculated as: EENS = (1/Y) sum_y sum_d sum_t max(L_{y,d,t} - S_{GC,y,d,t}, 0).
- **Units:** MWh
- **Related concepts:** LOLE, LOLH, EENS_CVaR.

## C04: Conditional Value at Risk of EENS (EENS_CVaR)
- **Notation:** EENS_CVaR
- **Definition:** Mean value of EENS corresponding to the most severe part of the EENS probability distribution across all evaluated events (worst alpha proportion). EENS_CVaR = 1/(1-alpha) integral_{EENS >= VaR} phi(alpha, EENS)(EENS - VaR) dEENS.
- **Boundary conditions:** alpha typically set at 5%.
- **Related concepts:** VaR, EENS, extreme events.

## C05: Flexibility Ramp Capacity Margin
- **Notation:** I^{mile}_{F,T}
- **Definition:** Total additional ramping capacity of flexible resources required to meet net load variations within a given time period T. I^{mile}_{F,T} = D^{mile}_{F,T} - S^{mile}_{N,T}. Negative values indicate sufficient or surplus capacity.
- **Units:** MW
- **Related concepts:** Flexibility ramp rate margin, net load variation.

## C06: Flexibility Ramp Rate Margin
- **Notation:** I^{rate}_{F,T}
- **Definition:** Total additional ramping rate of flexible resources required to meet net load variation rates within a given time period T. I^{rate}_{F,T} = D^{rate}_{F,T} - R^{rate}_{N,T}. Negative values indicate sufficient ramping rate.
- **Units:** MW/h
- **Related concepts:** Flexibility ramp capacity margin.

## C07: Minimum Inertia Requirement
- **Notation:** H_min
- **Definition:** Minimum system inertia required to ensure that RoCoF and frequency deviation do not exceed safety limits after a system disturbance. H_min = max(H_RoCoF, H_nadir). H_RoCoF = f0 * Delta_P / RoCoF_max. H_nadir ≈ f0 * Delta_P * T_PFR * (1 - 0.5*alpha) / (2 * S_base * |Delta_f_max|).
- **Units:** MW·s
- **Boundary conditions:** Depends on disturbance magnitude (Delta_P, typically 10% of load), RoCoF limits, and frequency nadir limits.
- **Related concepts:** Inertia margin, system equivalent inertia H_sys, RoCoF.

## C08: System Inertia Margin
- **Notation:** A_H
- **Definition:** Relative ratio between system inertia and the minimum inertia requirement. A_H = (H_sys - H_min) / H_min * 100%. Positive values indicate adequate inertia.
- **Units:** %
- **Related concepts:** Minimum inertia requirement, H_sys.

## C09: Combined Subjective--Objective Weighting
- **Notation:** w_j (comprehensive weight of indicator j)
- **Definition:** Weight derived via game-theoretic combination of AHP (subjective) and entropy weight (objective) methods.
- **Related concepts:** AHP, entropy weight method, PROMETHEE-II.

## C10: PROMETHEE-II Net Flow
- **Notation:** phi(a)
- **Definition:** Net preference flow for scheme a, calculated as outflow minus inflow: phi(a) = phi^+(a) - phi^-(a), where phi^+(a) = sum_k Pi(a,k) and phi^-(a) = sum_k Pi(k,a). Schemes ranked by descending net flow.
- **Related concepts:** Preference index Pi(a,b), deviation function P_j(d), outflow/inflow.
