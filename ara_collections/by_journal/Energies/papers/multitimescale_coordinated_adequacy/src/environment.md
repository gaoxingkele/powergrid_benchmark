# Environment

## Test System
- **Modified IEEE 24-bus system** (Figure 4).
- Peak load: 3500 MW.
- Transmission line capacities: 500 MW and 800 MW.
- Thermal power: total installed capacity unchanged from original IEEE 24-bus.
- Wind farms (250 MW each): nodes 3, 5 (max 750 MW per node).
- PV stations (250 MW each): nodes 7, 13 (max 750 MW per node).
- Short-term energy storage candidates: nodes 1, 7, 23 (duration <= 4 h).
- Long-term energy storage candidates: nodes 13, 18, 20 (duration > 4 h).

## Data Sources
- **Renewable output curves:** Real-world measurement data from a province in China (Figure 3).
- **Carbon price, load profiles, network constraints, RoCoF/Nadir parameters, frequency response limits, response times:** Consistent with reference [31] (Liang et al., 2024).
- **Cost parameters:** Consistent with references [33,34]:
  - Wind, PV, short-term/long-term storage unit investment costs: per [33,34] (specific numerical values not provided in the paper).
  - Carbon emission penalty coefficient: per [31].
- **Extreme scenarios:** Constructed using recent 3-year historical meteorological and power system data (Table 1).

## Planning Model Parameters
- **Nominal frequency f0:** 50 Hz.
- **Maximum allowable RoCoF (RoCoF_max):** Per [31] (value not stated in paper).
- **Maximum allowable frequency deviation |Delta_f_max|:** Per [31].
- **PFR effective time T_PFR:** Per [31, reference Ahmadi & Ghasemi, 2014].
- **PFR coverage proportion alpha:** 0 <= alpha <= 1 (exact value from [31] not stated).
- **Primary frequency regulation capacity limit lambda_i,PFR:** 8% of thermal unit capacity.
- **Disturbance magnitude Delta_P:** 10% of system load.
- **Inertia time constants:** H_C_i (thermal), H_C_ses (short-term storage) -- exact values from [31].
- **Carbon emission penalty coefficient c_carb:** Per [31].
- **Weighting factor delta:** 0.5 (equal weighting between long-term and short-term operating costs).
- **Discount rate:** Annual interest rate used for investment cost annuity calculation (per resource type).
- **EENS_CVaR alpha:** 5%.

## Software and Dependencies
- **Planning model:** The integrated grid planning model described in Section 3.2, implemented in an unspecified solver (not stated in paper). The temporal decomposition method from [29] is used.
- **Adequacy evaluation:** Sequential Monte Carlo sampling per [27].
- **Statistical analysis:** First-order difference method for net load variation (Eqs. 6--8).
- **MCDM:** PROMETHEE-II with AHP (subjective) and entropy weight (objective) methods.
- **Note:** The paper does not specify the exact solver (e.g., Gurobi, CPLEX), programming language, or computing hardware used.

## Source References
- [27] UK DESNZ, 2023 — Monte Carlo sampling methodology.
- [29] Jiang et al., 2023 — Temporal decomposition method.
- [30] Ahmadi & Ghasemi, 2014 — Linearization method for frequency nadir constraint.
- [31] Liang et al., 2024 — Parameter source for case study.
- [32] Twitchell et al., 2023 — Long-duration energy storage definition.
- [33] Cost parameter reference (not explicitly named in text).
- [34] Chen et al., 2025 — Cost parameter reference.
