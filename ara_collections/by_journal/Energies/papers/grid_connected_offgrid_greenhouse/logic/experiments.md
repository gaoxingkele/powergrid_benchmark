# Experiments

## E1: Grid-connected system optimization
- **Verifies**: C1, C2, C7, C9, C10
- **Evidence**: Table 2, Table 3, Table 4, Figures 6-11
- **Run**: HOMER Pro simulation (ver. 3.14.2)
- **Setup**: Six grid-connected architectures evaluated (G/PV, G/PV/WT, G/WT, G/PV/B, G/PV/WT/B, G/WT/B) for a greenhouse in Sandikli, Turkiye. Load: 134,875 kWh/yr (avg 369.52 kWh/day, peak 52.59 kW). Grid buy: $0.096/kWh, sell: $0.076/kWh. Discount rate: 9.75%.
- **Procedure**: Software optimizes component sizing for each architecture to minimize NPC. 8,760 hourly simulations per year over 25-year project lifetime.
- **Metrics**: NPC, LCOE, Operating Cost, Initial Capital, Renewable Fraction, CO2 Reduction, Energy Purchased, Energy Sold
- **Expected outcome (directional)**: PV-dominant configurations will have lower NPC and LCOE than wind-dominant ones. Adding battery storage will increase costs without proportional environmental benefit.
- **Baselines**: G-only (grid-only) for economic comparison; grid-only emissions for environmental comparison
- **Dependencies**: NASA POWER meteorological data, EPIAS grid pricing, component cost catalog

## E2: Off-grid (standalone) system optimization
- **Verifies**: C3, C4, C5, C8
- **Evidence**: Table 7, Table 8, Figures 13-15
- **Run**: HOMER Pro simulation
- **Setup**: Ten standalone architectures evaluated (Gen, Gen/PV, Gen/PV/B, Gen/PV/WT, Gen/PV/WT/B, Gen/WT, Gen/WT/B, PV/WT/B, PV/B, WT/B). Same load profile as E1. No grid access. Diesel price assumed in sensitivity range.
- **Procedure**: Software optimizes component sizing to minimize NPC for each off-grid architecture.
- **Metrics**: NPC, LCOE, Operating Cost, Initial Capital, Renewable Fraction, Total Fuel Consumption, CO2 Reduction
- **Expected outcome (directional)**: Hybrid PV/diesel/battery systems will have lowest NPC. Fully renewable systems will achieve zero emissions but at substantially higher cost. Generator-only systems will have lowest capital but highest operating cost and emissions.
- **Baselines**: Gen-only for cost and emission baselines
- **Dependencies**: Component cost catalog, diesel price assumptions, NASA meteorological data

## E3: Sensitivity analysis for grid-connected G/PV system
- **Verifies**: C6
- **Evidence**: Table 5, Table 6, Figure 12
- **Run**: Parametric sensitivity analysis via HOMER Pro
- **Setup**: Vary five parameters across minimum/average/maximum values: solar scaled average (2.0-7.0 kWh/m2/d), temperature (1-25 degC), inflation rate (5-30%), grid power price ($0.12-$0.16/kWh), grid sellback rate ($0.10-$0.18/kWh). Additional scenarios in Table 6 test power price ($0.10-$0.16/kWh) x sellback rate ($0.08-$0.18/kWh) x inflation (5-30%).
- **Procedure**: For each parameter combination, recalculate NPC, LCOE, IRR, and payback period.
- **Metrics**: NPC, LCOE, IRR, Simple Payback Period
- **Expected outcome (directional)**: Higher inflation increases NPC and extends payback period. Higher power price and sellback rate improve IRR and shorten payback.
- **Baselines**: Base case (average parameters)
- **Dependencies**: EPIAS grid pricing, Turkiye inflation data

## E4: Sensitivity analysis for standalone Gen/PV/B system
- **Verifies**: C6
- **Evidence**: Table 9, Table 10, Figure 16
- **Run**: Parametric sensitivity analysis via HOMER Pro
- **Setup**: Vary four parameters: solar scaled average (2.0-7.0 kWh/m2/d), temperature (1-25 degC), diesel fuel price ($1.2-$1.8/L), inflation rate (5-30%). Additional scenarios in Table 10 test solar irradiation (2.0-7.0 kWh/m2/d) x fuel price ($1.2-$1.8/L) x inflation (5-30%).
- **Procedure**: For each parameter combination, recalculate NPC, LCOE, IRR, and payback period.
- **Metrics**: NPC, LCOE, IRR, Simple Payback Period
- **Expected outcome (directional)**: Higher solar irradiance reduces NPC and payback. Higher fuel prices increase NPC but improve IRR due to PV substitution benefit. Higher inflation extends payback.
- **Baselines**: Base case (average parameters)
- **Dependencies**: NASA solar data, diesel price assumptions, Turkiye inflation data
