# Constraints — Boundary Conditions, Assumptions, Limitations

## Boundary conditions
- Single test system: Portugal 54-node distribution network, 4 substations, 54 source-load nodes (reference [31]).
- Planning horizon: 20 years, discount rate 0.03 (annualized cost model).
- Device types considered: lines, SOPs (back-to-back VSC), interconnection switches (mechanical tie switches).
- Uncertainty sources: DG output (wind/solar) and load demand.
- DG locations fixed: 9 access nodes (1, 5, 9, 12, 14, 22, 30, 33, 47) with max power 2800–4100 kW.
- ESS locations fixed: 5 access nodes (8, 9, 13, 32, 50) with rated capacities 800–1500 kWh.
- 24-hour typical-scenario representation for annual operation simulation.
- Uncertainty modeled via Wasserstein-distance-based ambiguity set; comparisons against deterministic (scenario-based stochastic) and traditional robust optimization.

## Assumptions
- A1: The distribution network is radial enough for SOCP exactness conditions to hold (sufficient: radial topology, no reverse power flow at substations).
- A2: The Wasserstein distance radius epsilon can be selected empirically.
- A3: 24-hour typical scenarios adequately represent annual DG/load variation.
- A4: 20-year horizon at 3% discount rate is appropriate for utility planning.
- A5: Device costs and electricity prices are fixed over the planning horizon (no escalation).
- A6: Slater's condition holds for the Wasserstein inner problem, ensuring zero duality gap in the Lagrange dualization.
- A7: The McCormick relaxation bounds are sufficiently tight to yield a close approximation; further refinement via bound tightening is possible but not described.

## Known limitations (paper-stated)
- **Single test system**: Only validated on the Portugal 54-node system; generalizability to other networks (larger, meshed, different DG mix) is not tested.
- **ADN-specific model**: The model is tailored for active distribution networks with specific SOP/switch configurations and may not directly apply to transmission-level planning.
- **No code or data publishing**: The paper does not provide runnable code or the scenario data (historical DG/load observations used to construct the Wasserstein ambiguity set).
- **Annualized cost model**: The 20-year horizon uses annualized equivalent investment costs rather than detailed year-by-year cash flows with escalation.
- **24-hour typical scenarios**: The temporal granularity (24-hour typical day) may not capture intra-day correlations or seasonal extremes beyond the constructed scenarios.
- **SOCP relaxation exactness**: While radial networks typically satisfy exactness conditions, the paper acknowledges that deviations in network operation (e.g., reverse power flow under high DG penetration) could create a relaxation gap.
- **McCormick bound tightness**: The relaxation quality depends on the bounds of the bilinear variables; the paper does not perform iterative bound tightening.
- **Fixed DG/ESS locations**: DG and ESS access nodes are predetermined, not optimized as part of the planning decision.

## Internal tensions (as recorded, NOT silently resolved)
1. **Generality of results**: The paper reports "nearly 5%" improvement for Case 1 vs Case 3, and "more than 6%" reduction for Case 4 vs Case 1 operation profit. Both percentages are based on a single test system and specific cost parameters — their generalizability across different cost environments is untested beyond the sensitivity analysis of Section 5.4.
2. **Deterministic vs DRO gap**: The deterministic optimization (Table 6, 5089.49) is described as "too ideal" but the paper does not quantify its out-of-sample degradation. The DRO net profit (4928.18) is 3.2% below deterministic — whether this gap is the "price of robustness" or indicates over-conservatism is a matter of interpretation.
3. **Bilinear-Removed comparison**: Table 7 reports the Bilinear-Removed method achieving 3.75 x 10^7 CNY (76% of McCormick's 4.93 x 10^7). However, the units differ from the main result tables (Table 4 uses 10^4 CNY, Table 7 uses 10^7 CNY). The conversion (4.93 x 10^7 = 4930 x 10^4) is consistent with Table 4's 4928.18, confirming no scaling error.
