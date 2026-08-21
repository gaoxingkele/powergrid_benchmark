# Experiments

## E01: Scenario M1 -- Traditional Planning Baseline
- **Verifies:** Baseline for C02 (coordinated planning impact on LOLH); baseline for C05 (scheme comparison reference).
- **Setup:** IEEE 24-bus system; 250 MW wind at nodes 3,5; 250 MW PV at nodes 7,13; max 750 MW per type; short-term storage at nodes 1,7,23; no long-term storage; no dynamic frequency security constraints; no generalized adequacy iteration. Transmission candidate lines at 500 MW and 800 MW.
- **Procedure:** Run integrated planning model (SS3.2) without long-term storage, without frequency constraints, and without generalized adequacy feedback. Evaluate post-plan adequacy using Section 2.2 metrics.
- **Metrics:** LOLH (h/a), EENS (MWh), EENS_CVaR (MWh), flexible ramp capacity margin (MW), flexible ramp rate margin (MW/h), system inertia margin (%), minimum inertia requirement (MW-s), LCOE ($/kWh), renewable utilization rate (%), carbon emission intensity (t/MWh).
- **Expected outcome:** Highest LOLH, EENS, EENS_CVaR among all scenarios; negative inertia margin indicating frequency insecurity; lowest investment cost but worst adequacy.
- **Baselines:** N/A (primary baseline).
- **Dependencies:** None.

## E02: Scenario M2 -- With Long-Term Storage
- **Verifies:** C02 (progressive improvement from coordinated resources), C03 (need for inertia constraints), C05 (scheme comparison).
- **Setup:** Same as M1 but adds long-term energy storage at nodes 13, 18, 20 (duration >4h). No dynamic frequency security constraints. No generalized adequacy iteration.
- **Procedure:** Run integrated planning model including long-term storage optimization. Post-plan adequacy evaluation.
- **Metrics:** Same as E01.
- **Expected outcome:** Lower LOLH/EENS than M1 due to cross-day energy shifting; inertia margin still negative, confirming that storage alone does not solve frequency security; net flow intermediate between M1 and M3.
- **Baselines:** M1 (E01).
- **Dependencies:** E01.

## E03: Scenario M3 -- With Dynamic Frequency Security Constraints
- **Verifies:** C03 (effectiveness of frequency constraints on inertia margin), C04 (comparison with extreme-scenario planning), C05.
- **Setup:** Same as M2 but adds RoCoF constraint (Eq. 34), frequency nadir constraint (Eq. 35), PFR capacity constraints (Eqs. 31--33, 36). Uses typical (clustered) scenarios only.
- **Procedure:** Run planning model with frequency security constraints. Evaluate post-plan adequacy.
- **Metrics:** Same as E01, plus inertia margin verification.
- **Expected outcome:** Positive inertia margin indicating frequency adequacy; LOLH below 3.14 h (target approaches European 3 h/a standard); higher short-term storage deployment than M2 (to provide PFR); net flow positive but lower than M4.
- **Baselines:** M1 (E01), M2 (E02).
- **Dependencies:** E02.

## E04: Scenario M4 -- Full Generalized Adequacy Framework
- **Verifies:** C01 (generalized adequacy framework end-to-end), C02 (coordinated planning impact maximized), C04 (extreme scenario embedding), C05 (top-ranked scheme).
- **Setup:** Same as M3 plus iterative generalized adequacy feedback: extreme scenarios from Table 1 are embedded in the planning model scenario set via sequential Monte Carlo sampling with extreme event probabilities (~0.01 each). Planning model is run iteratively until adequacy criteria are satisfied (Figure 1).
- **Procedure:** Run iterative planning framework (Figure 1): cluster historical data -> plan -> evaluate generalized adequacy -> if inadequate, incorporate extreme scenarios -> re-plan -> repeat. Final scheme evaluated on all metrics and compared via PROMETHEE-II.
- **Metrics:** Same as E01, plus extreme scenario EENS_CVaR impact.
- **Expected outcome:** Lowest LOLH (2.91 h), EENS (291.48 MWh), EENS_CVaR (1316.64 MWh) among all scenarios; highest inertia margin (10.26%); highest renewable capacity (750 MW wind, 585.76 MW PV, 750 MW short-term storage); highest LCOE ($1.30/kWh) but best overall PROMETHEE-II net flow (+2.00); rank 1/4.
- **Baselines:** M1 (E01), M2 (E02), M3 (E03).
- **Dependencies:** E03.

## E05: Robustness Check -- 95% Demand Percentile
- **Verifies:** C05 (ranking robustness to demand quantification method).
- **Setup:** Same four scenarios (M1--M4) but with adequacy indicators calculated using 95th percentile of hourly demand instead of maximum demand, thereby excluding influence of extreme peaks.
- **Procedure:** Recompute all adequacy indicators in Tables 5/6 using 95% demand threshold. Compare rankings.
- **Metrics:** Same indicator set, calculated at 95% demand.
- **Expected outcome:** Numerical values of shortage indicators decrease compared to max-based calculation, but relative scheme ranking remains identical: M4 > M3 > M2 > M1. Confirms structural nature of scheme superiority.
- **Baselines:** E01--E04.
- **Dependencies:** E01, E02, E03, E04.

## E06: Inertia Adequacy Verification Under M2 vs M3
- **Verifies:** C03 (effect of frequency constraints on inertia margin).
- **Setup:** Compare hourly operating inertia H_sys(t) against minimum inertia requirement H_min for M2 (no constraints) and M3 (with constraints) across the 8760-h simulation.
- **Procedure:** Plot H_sys(t) and H_min for both scenarios. Compute inertia margin distribution.
- **Metrics:** Inertia margin A_H (%); frequency of hours with A_H < 0.
- **Expected outcome:** M2 shows frequent violations with A_H = -17.31% (Table 5); M3 shows consistent satisfaction with A_H = +2.90%. Results visualized in Figure 8.
- **Baselines:** M2 (E02), M3 (E03).
- **Dependencies:** E02, E03.
