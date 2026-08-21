# Constraints

## Boundary conditions (dispatch problem)
- **Scheduling horizon**: 24 hours, 1-hour time steps (dt = 1 h); scheduling period defined in §4.3 Step 1 and §5.1.
- **Power balance (Eq. 13)**: at every time t, sum of PV + WT + DG + ESS outputs minus grid-interaction power must equal the system load: Σ(P_PV + P_WT + P_DG + P_ESS) - P_grid(t) = P_load(t).
- **Grid interaction limits (Eq. 14)**: P_grid,min <= P_grid(t) <= P_grid,max (specific numeric limits not given).
- **Distributed-source output limits (Eqs. 15-18)**: each of PV, WT, DG output and ESS state-of-charge bounded within [min, max]; per-device max power from Table 1 (PV 10 kW, WT 10 kW, DG 1000 kW, ESS 10 kW).
- **ESS charge/discharge power caps (Eqs. 19-20)**: max charge/discharge power bounded by both a fixed limit and the available SOC headroom/content.
- **Pollutant emission cap (Eq. 21)**: total thermal-generator pollutant emission over the horizon <= Wpg,max.
- **Ramp-rate limit (Eq. 22)**: |P_DG(t) - P_DG(t-1)| <= Pct,max (thermal generator inter-period power change bounded).
- **Thermal output floor**: thermal generator actual output fluctuates between 30% of rated power and rated power (§2.3, per ref [21]).

## Assumptions
- A1: Deterministic dispatch — load, prices, and weather-derived PV/WT availability are known inputs at solve time (no in-solve stochasticity).
- A2: PV and wind generation produce no pollutants; only the thermal generator (DG) and grid-imported power carry emissions.
- A3: Constant device coefficients (lifespan, install/maintenance/depreciation costs, emission factors, treatment costs) over the horizon (Tables 1-2).
- A4: A single aggregated objective (operating cost C1 + environmental cost C2) represents the economic-environmental trade-off adequately.
- A5: A single "typical summer day" of a Jiangsu-Province city represents daily operation for the case study; subtropical monsoon climate (hot, sunny summers).
- A6: The rotor speed of the wind turbine is linearly related to generator speed (§2.2, ref [20]); piecewise wind-power curve (Eq. 2).

## Known limitations (paper-acknowledged and evident)
- **Single-scenario validation**: only one season (summer) and one day are simulated; no winter/shoulder-season or multi-day robustness test.
- **No uncertainty modeling**: renewable/load uncertainty is discussed as motivation but the dispatch itself is deterministic; no stochastic/robust formulation despite the abstract emphasizing "uncertainties of wind and photovoltaic."
- **No ablation of the four SCMPSO mechanisms**: chaotic init, adaptive weight, dynamic learning factors, and second-order oscillation are always applied together; their individual contributions are not isolated.
- **Naming inconsistency**: SCMPSO is expanded two different ways (abstract vs Figure 1 flowchart), leaving the acronym's precise meaning ambiguous.
- **No released code or data**: software stated only as "MATLAB 2020a"; raw data withheld for confidentiality (Data Availability Statement) — limits reproducibility.
- **Some printed values are internally inconsistent**: e.g. Table 5 ESS entries at 01:00-02:00 (444.98) and 22:00-23:00 (445.48) are out of scale with the 10 kW ESS rating and neighbouring rows; the benchmark search-domain cell for "Sum of Different Powers" (Table 3) has garbled stacked ranges.
- **No statistical treatment**: single-run curves; no variance/standard-deviation across seeds reported for the stochastic optimizers.
- **Grid limits unspecified**: P_grid,min/max, Wpg,max, Pct,max, and several device min/max numeric values are referenced symbolically but not given.
