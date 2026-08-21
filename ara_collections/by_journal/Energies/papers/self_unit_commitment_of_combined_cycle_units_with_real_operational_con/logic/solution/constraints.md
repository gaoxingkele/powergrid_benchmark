# Constraints — Boundary Conditions, Assumptions, Limitations

## Boundary conditions (model scope)

- **Plant**: Single CCGT plant, TEBSA-like 5 × 2 configuration (5 identical gas turbines, 2 identical steam turbines), 800 MW maximum capacity. Results are specific to this topology.
- **Horizon**: 24 hours, hourly time resolution (matching the Colombian market dispatch interval).
- **Network**: No transmission network is modelled; the plant is treated as a single bus injecting P^plant_t. Reactive power is excluded (only active power per unit is produced).
- **Test cases**: Two initial-condition scenarios — Case I (hot startup, some units online) and Case II (warm startup, all units initially offline) — representing different operating states of the same plant.

## Assumptions

- A1: Constant steam-to-gas output factor (STF = 0.613) — variable ratios left to future work. [§2.3.2]
- A2: Steam quality is maintained when the modelled operational constraints are met (HRSG supplementary fires assumed to preserve steam quality). [§1.2]
- A3: All NC gas turbines are identical, all NS steam turbines are identical. [§3]
- A4: The plant is the sole price-taker in the market; the ISO dispatch is a fixed input, not co-optimised.
- A5: Startup ramp blocks (Table 2) follow Colombian grid-code declarations exactly; no degradation or deviation from the prescribed block MW values.
- A6: Hourly dispatch resolution means sub-hourly dynamics (e.g., intra-hour ramping) are not captured.
- A7: Supplementary fire (PAF) contribution to steam output is linear and additive per the STF factor; no efficiency degradation with sustained firing is modelled.
- A8: Auxiliary consumption is treated as a constant per-unit value allocated to steam turbines (Eq. 17), not as a function of ambient conditions or partial loading.
- A9: The deviation penalty computation uses the simplified PCC price and the 5% market rule; no interaction with the balancing market or intraday re-dispatch is considered beyond the threshold.

## Known limitations (stated or implied by the paper)

- **Single plant, single topology**: Only a 5 × 2 configuration is tested; the paper does not evaluate different CCGT configurations (e.g., 2 × 1, 3 × 1, 1 × 1) or heterogeneous unit sets with different ramp rates and output capacities.
- **Two case studies**: Only two initial-condition scenarios are presented; a broader sensitivity analysis (e.g., varying ISO dispatch profiles, different thermal states, seasonal effects) is not performed.
- **Constant STF**: The constant steam-to-gas factor is a simplification; real HRSG dynamics exhibit variable ratios depending on firing level and ambient conditions (acknowledged as future work in §4).
- **Damage link not quantified**: The claimed link between even loading and reduced steam-rotor thermal stress (C05 motivation) is argued qualitatively from plant experience, not measured or simulated.
- **No stochasticity**: The model is fully deterministic (given ISO dispatch and parameters); uncertainty in load, wind, or pricing is not incorporated.
- **No comparison to mode-only models**: The paper compares its SEUC model against a heuristic simulation code (which omits many real constraints), but does not benchmark against a pure mode/configuration representation from the literature (Cluster B in related work) to isolate the marginal benefit of the hybrid component+mode representation.
- **Computational performance not reported**: The paper does not report solution times, iteration counts, or MIP gap for the two case studies, so scalability to larger configurations or multi-plant systems is unknown.
