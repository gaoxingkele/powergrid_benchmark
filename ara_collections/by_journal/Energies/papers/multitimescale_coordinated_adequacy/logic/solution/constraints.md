# Constraints and Limitations

## Model Scope Constraints

1. **Resource types limited.** Only wind, solar PV, short-term energy storage (duration <= 4 h), and long-term energy storage (duration > 4 h) are modeled as planned resources. Excluded: hydropower expansion, geothermal, biomass, nuclear, demand-side response (EVs, smart buildings), and the synergistic interactions among wind, solar, hydro, thermal, and storage.

2. **Single test system.** Validation was performed exclusively on an augmented IEEE 24-bus system (3500 MW peak load). Generalization to larger, more meshed, or region-specific networks (e.g., provincial Chinese grid) is not demonstrated.

3. **One type of preference function.** PROMETHEE-II used the stepwise 0/1 criterion; alternative preference functions (Gaussian, linear, quasi-criterion) were not tested, and no parameter sensitivity analysis was performed on the preference function threshold settings.

## Modeling Assumptions

4. **Linearized frequency dynamics.** The frequency nadir constraint (Eq. 35) is linearized per [30]; this approximation may diverge from true electro-mechanical dynamics under certain conditions (e.g., multiple contingencies, nonlinear governor response).

5. **Single-contingency assumption.** Inertia adequacy is verified against a single 10% load disturbance; multi-contingency or cascading events are not considered.

6. **Primary frequency regulation modeled as linear ramp.** PFR is assumed to ramp linearly within T_PFR seconds to cover a fraction alpha of the power imbalance. Real PFR response may be nonlinear.

7. **Climate-pattern specific extreme scenarios.** The three extreme scenarios (extreme heat with low wind, extreme cold with low solar, severe drought) are designed based on China-specific climate patterns. Their applicability to other geographic regions is unvalidated.

8. **Extreme scenario probabilities approximated.** Each extreme scenario is assigned a probability of ~0.01 (1--2%) based on historical statistics. Precise probability calibration is not provided.

## Data and Parameter Limitations

9. **External parameter reliance.** Carbon price, load/renewable profiles, network constraints, RoCoF/Nadir parameters, frequency response limits, and response times are sourced from [31] and may not reflect all operating regimes.

10. **Cost parameter dependency.** Storage and renewable cost parameters from [33,34] reflect specific market conditions and may not generalize across all jurisdictions or time horizons.

11. **Renewable output curves from a single province.** Wind and solar output curves and transmission dispatch data are from real measurements of one Chinese province, limiting geographic generalizability.

## Evaluation Limitations

12. **No sensitivity analysis on indicator weights.** The combined AHP-entropy weights were computed for the four evaluated schemes. No formal sensitivity analysis demonstrates ranking stability under weight perturbations.

13. **Four schemes only.** The comparison is limited to four scenarios (M1--M4). A larger scheme space could reveal non-dominated alternatives not captured.

14. **Thermal capacity fixed.** The total installed thermal power capacity remains unchanged, which may not reflect realistic expansion planning where thermal capacity can also be adjusted.

15. **95% demand robustness only partially tested.** Robustness of rankings was tested at only two demand quantification levels (max vs. 95th percentile). More comprehensive sensitivity analysis is absent.
