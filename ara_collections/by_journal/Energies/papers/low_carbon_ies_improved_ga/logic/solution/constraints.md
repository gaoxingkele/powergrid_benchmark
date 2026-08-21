# Constraints

## Boundary Conditions

### IES Operational Boundaries
- CHP unit electric power: 50 kW (min) to 250 kW (max)
- CHP unit thermal power upper limit: 125 kW
- Gas boiler heat production upper limit: 150 kW
- ESS charge/discharge power upper limit: 30 kW each
- ESS capacity: 200 kWh
- ESS state of charge: 0% to 100% (initial and final: 50%)
- PV generation: 0 to PPV_max_t (per time slot)
- Wind generation: 0 to PWT_max_t (per time slot)
- WHU recovered thermal power: 0 to QWHU_max (not numerically specified)

### Pricing Boundaries
- Tiered electricity threshold: E0 = 175 kWh (base LMP rate, 120% surcharge above)
- Tiered gas threshold: V0 = 50 m3 (base rate, 120% surcharge above)
- Tiered carbon thresholds: e1 = 5000, e2 = 6000, e3 = 6500 m3
- Carbon unit prices: 0.2, 0.3, 0.4 CNY/m3 (tiers 1, 2, 3)
- Gas unit price: 2.5 CNY/m3
- Abandoned electricity costs: Mcur = 1.5 CNY/kWh (maintenance), Ncur = 1 CNY/kWh (environmental)

### Algorithm Parameters
- Mutation distribution index initial value: βmin_m = 1
- Weight coefficients for Pareto selection: w1 = w2 = 1
- Penalty function weights (for MPSO, MABC): α1 = α2 = 1
- Population parameters (size, generation count): Not specified in paper

## Assumptions

### System Modeling
- A1: CHP unit efficiency ηCHP = 0.9 (fixed, not load-dependent)
- A2: WHU recovery efficiency ηWHU = 0.6 (fixed)
- A3: Gas boiler efficiency ηGB = 0.85 (fixed)
- A4: Natural gas lower heating value LNG = 9.7 kWh/m3 (fixed)
- A5: ESS charging/discharging efficiency considered via ηch and ηdch; round-trip not explicitly modeled
- A6: Carbon emission conversion factors: γh = 0.6 (heat-to-emissions), γe = 0.997 (electricity-to-emissions), ϵeh = 3.6 (electrical-to-thermal conversion for CHP)
- A7: Binary variables zch_t and zdch_t ensure ESS cannot simultaneously charge and discharge

### Operational Assumptions
- A8: Day-ahead scheduling over 24 hourly time slots (∆t = 1 hour)
- A9: Renewable generation (PV, wind) output is known/predictable for the scheduling horizon
- A10: Electrical and thermal load profiles are known
- A11: The IES can purchase electricity from the grid at locational marginal price (LMP)
- A12: Natural gas is available for purchase at the specified unit price
- A13: The ESS returns to its initial SOC (50%) at the end of the scheduling day
- A14: PV system inoperable under rainy conditions (Scenarios 2 and 3)

## Known Limitations

### Algorithm Limitations (stated in paper)
- L1: The IGA's overly complex crossover and mutation operations increase computational overhead and reduce operational efficiency (Section 5, Conclusions).
- L2: As a day-ahead scheduling algorithm, the IGA cannot handle potential fluctuations in renewable energy generation and load demand during real-time operation (Section 5).
- L3: The IGA does not incorporate uncertainty modeling for renewable generation or load; stochastic or robust optimization would be needed for real-time applications (Section 5, future work).

### Modeling Limitations (identified from paper content)
- L4: CHP, WHU, and GB efficiencies are modeled as fixed constants rather than load-dependent or time-varying values.
- L5: Only two objectives (cost and emissions) are considered; additional criteria such as system reliability, equipment lifespan, or grid stability are not included.
- L6: The tiered pricing models use simplified 120% surcharge rates rather than the actual rate schedules of real utilities.
- L7: The initial population size and maximum generation count are not specified, limiting reproducibility of the evolutionary search dynamics.
- L8: The IGA has not been tested on larger IES configurations or compared with state-of-the-art multi-objective evolutionary algorithms beyond the four baselines.
- L9: The paper evaluates performance on three specific scenarios; generalization to arbitrary IES configurations is not established.
