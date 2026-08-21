# Claims

## C1: G/PV is the most cost-effective grid-connected configuration
- **Statement**: The grid-connected G/PV (grid + photovoltaic) configuration achieves the lowest NPC ($282,492) and LCOE ($0.0401/kWh) among all grid-connected hybrid architectures evaluated.
- **Conditions**: Assumes Turkiye EPIAS April-June 2025 electricity prices ($0.096/kWh purchase, $0.076/kWh sellback), 9.75% discount rate, 25-year project lifetime, site conditions in Sandikli, Afyonkarahisar.
- **Sources**: Table 2, Section 3.1
- **Status**: Supported
- **Falsification criteria**: Any alternative grid-connected configuration achieving lower NPC and/or LCOE under the same assumptions would falsify this claim.
- **Proof**: NPC optimization via HOMER Pro across 6 grid-connected architectures shows G/PV has lowest NPC ($282,492) and LCOE ($0.0401/kWh). G/PV/WT has higher NPC ($401,065) and LCOE ($0.0542/kWh).
- **Evidence basis**: Table 2 quantitative comparison
- **Dependencies**: HOMER Pro optimization algorithm, component cost assumptions
- **Tags**: [economics, grid-connected, PV, optimization]

## C2: G/PV achieves meaningful but not maximal CO2 reduction
- **Statement**: The G/PV configuration achieves a 54.94% reduction in CO2 emissions compared to a grid-only baseline.
- **Conditions**: Same as C1. Comparison is against grid-only (100% fossil-derived electricity) baseline.
- **Sources**: Table 2
- **Status**: Supported
- **Falsification criteria**: If actual CO2 reduction deviates from 54.94% by more than measurement uncertainty.
- **Proof**: HOMER Pro simulation of annual energy flows: 134,875 kWh demand, 60,771 kWh purchased from grid, 138,638 kWh surplus sold to grid. Net grid consumption = 60,771 - 138,638 = -77,866 kWh. Annual CO2 emissions = 38,408 kg.
- **Evidence basis**: Table 2, Table 4
- **Dependencies**: Grid emission factor assumptions
- **Tags**: [environmental, CO2, PV, grid-connected]

## C3: Gen/PV/B is the most cost-effective off-grid configuration
- **Statement**: The standalone Gen/PV/B (generator + PV + battery) configuration achieves the lowest NPC ($1.19M) and LCOE ($0.342/kWh) among all off-grid architectures.
- **Conditions**: Assumes diesel fuel price range, no grid access, 25-year lifetime, Sandikli site conditions.
- **Sources**: Table 7, Section 3.2
- **Status**: Supported
- **Falsification criteria**: Any alternative off-grid configuration achieving lower NPC and/or LCOE under the same assumptions.
- **Proof**: HOMER Pro simulation across 10 off-grid architectures. Runner-up Gen/PV/WT/B has NPC $1.22M and LCOE $0.350/kWh. Pure diesel (Gen) has NPC $1.92M, LCOE $0.554/kWh.
- **Evidence basis**: Table 7
- **Dependencies**: HOMER Pro optimization, diesel price assumptions
- **Tags**: [economics, off-grid, generator, PV, battery]

## C4: Fully renewable off-grid systems are economically unfeasible
- **Statement**: Off-grid systems achieving 100% renewable fraction (PV/WT/B, PV/B, WT/B) have prohibitively high NPC ($2.54M-$4.52M) and LCOE ($0.759-$1.370/kWh), making them economically unviable for the greenhouse application.
- **Conditions**: Current technology costs (2025), 25-year lifetime, Sandikli site conditions. Does not account for potential future cost reductions or subsidies.
- **Sources**: Table 7, Section 3.2
- **Status**: Supported
- **Falsification criteria**: Demonstration of economic feasibility for 100% renewable off-grid greenhouse systems at comparable or lower cost thresholds.
- **Proof**: PV/WT/B NPC $2.54M, LCOE $0.759/kWh; PV/B NPC $2.80M, LCOE $0.837/kWh; WT/B NPC $4.52M, LCOE $1.370/kWh. These are 2.1-3.8x more expensive than the optimal Gen/PV/B configuration.
- **Evidence basis**: Table 7
- **Dependencies**: Current renewable technology and battery costs
- **Tags**: [economics, off-grid, 100% renewable, feasibility]

## C5: Gen/PV/B achieves 64.58% CO2 reduction as a balanced solution
- **Statement**: The Gen/PV/B standalone configuration achieves a 64.58% reduction in CO2 emissions compared to a generator-only (Gen) baseline.
- **Conditions**: Same as C3. Compared against Gen-only baseline.
- **Sources**: Table 7, Section 3.2
- **Status**: Supported
- **Falsification criteria**: Actual operational CO2 reduction deviating significantly from 64.58%.
- **Proof**: Gen-only baseline emits 150,377 kg CO2/year. Gen/PV/B total annual fuel = 20,363 L/year, achieving 64.58% reduction. Gen/PV/WT/B achieves 69.43% reduction with 17,574 L/year fuel consumption.
- **Evidence basis**: Table 7, Section 3.2
- **Dependencies**: Diesel generator emission factors
- **Tags**: [environmental, CO2, off-grid, hybrid]

## C6: High inflation (>10%) critically undermines economic feasibility
- **Statement**: Expected inflation rates at or above 10% significantly extend payback periods and reduce IRR for both grid-connected and off-grid systems; at 30% inflation, the grid-connected system remains in debt throughout its operational lifespan.
- **Conditions**: Inflation scenarios of 5%, 10%, and 30% tested. Grid power price scenarios $0.10-$0.16/kWh, sellback $0.08-$0.18/kWh.
- **Sources**: Table 6, Table 10, Figures 12 and 16
- **Status**: Supported
- **Falsification criteria**: Demonstration that hybrid energy investments remain profitable under >10% inflation in comparable economic conditions.
- **Proof**: At 5% inflation with $0.16/kWh power price and $0.18/kWh sellback: payback = 2.1 years, IRR = 47%. At 30% inflation: payback exceeds 25 years (system in debt), IRR shows "-" (undetermined). Similar pattern for off-grid: at 5% inflation payback ranges 1.7-4.0 years; at 30% inflation payback extends to 4.6-7.8 years.
- **Evidence basis**: Tables 6, 10; Figures 12, 16
- **Dependencies**: Turkiye-specific economic conditions
- **Tags**: [sensitivity, inflation, economic risk]

## C7: PV-dominated grid-connected systems outperform wind-dominated ones
- **Statement**: Grid-connected configurations with PV (G/PV, G/PV/WT, G/PV/B, G/PV/WT/B) consistently achieve lower NPC and higher emission reductions than wind-dominated configurations (G/WT, G/WT/B).
- **Conditions**: Sandikli site has modest average wind speeds (~3.5-5 m/s), making wind less competitive than solar.
- **Sources**: Table 2, Section 3.1
- **Status**: Supported
- **Falsification criteria**: Demonstration of wind-dominated grid-connected systems achieving competitive NPC and emission reductions at this specific site.
- **Proof**: G/WT: NPC $445,910, CO2 reduction 16.39%. G/WT/B: NPC $785,724, CO2 reduction 28.48%. In contrast, G/PV: NPC $282,492, CO2 reduction 54.94%. G/WT/B operating cost ($20,007/yr) is 4.3x G/PV ($4,601/yr) due to wind turbine maintenance.
- **Evidence basis**: Table 2
- **Dependencies**: Site-specific wind resource availability
- **Tags**: [PV vs wind, grid-connected, site-specific]

## C8: Generator-based systems without PV have poor environmental performance
- **Statement**: Standalone systems relying solely on diesel generators (Gen) or generator + wind (Gen/WT) show negligible CO2 reduction (0-7.12%) and are unsuitable for meeting sustainability goals.
- **Conditions**: Off-grid operation, no carbon capture, standard diesel generator emission rates.
- **Sources**: Table 7, Section 3.2
- **Status**: Supported
- **Falsification criteria**: Demonstration that generator-only systems achieve meaningful emission reductions through efficiency improvements alone.
- **Proof**: Gen-only: 0% CO2 reduction, 57,493 L/yr fuel, 150,377 kg CO2/yr. Gen/WT: 7.12% reduction. Gen/PV (without battery): 9.19% reduction. Adding PV significantly improves to 64.58% (with battery).
- **Evidence basis**: Table 7
- **Dependencies**: Diesel emission factors
- **Tags**: [environmental, generator, emissions]

## C9: The G/PV system achieves net-negative grid energy consumption during summer
- **Statement**: From April to October, the G/PV system consistently sells more energy to the grid than it purchases, resulting in negative net energy costs during these months.
- **Conditions**: Turkiye grid pricing structure, net metering arrangement with buy/sell price differential.
- **Sources**: Table 4, Figures 10, 11
- **Status**: Supported
- **Falsification criteria**: Actual monthly net metering data deviating from simulation results.
- **Proof**: Monthly net energy purchased: April -7,045 kWh, May -14,546 kWh, June -18,162 kWh, July -21,833 kWh, August -17,723 kWh, September -11,195 kWh, October -3,583 kWh. Annual net: -77,866 kWh (net seller). Energy charge: -$4,702.46 annual (net revenue).
- **Evidence basis**: Table 4
- **Dependencies**: Net metering policy, solar resource availability
- **Tags**: [grid-connected, net metering, seasonal, PV]

## C10: Battery storage adds significant cost with marginal environmental benefit in grid-connected systems
- **Statement**: Adding battery storage to grid-connected PV systems (G/PV/B vs. G/PV) increases NPC by 79% ($282,492 to $506,112) while providing identical CO2 reduction (54.94%), making batteries economically unattractive when grid backup is available.
- **Conditions**: Grid-connected operation with reliable grid access and net metering.
- **Sources**: Table 2, Section 3.1
- **Status**: Supported
- **Falsification criteria**: Demonstration that battery storage provides cost-effective benefits (demand charge reduction, backup value) that offset the added cost in grid-connected greenhouse settings.
- **Proof**: G/PV vs G/PV/B: identical RF (77.8%) and CO2 reduction (54.94%). G/PV/B has NPC $506,112 vs $282,492 (+79%), LCOE $0.0718 vs $0.0401 (+79%). Operating cost increases from $4,601 to $10,954 (+138%).
- **Evidence basis**: Table 2
- **Dependencies**: Battery cost assumptions ($60,000 initial cost per unit), Li-ion chemistry
- **Tags**: [economics, battery storage, grid-connected, cost-effectiveness]
