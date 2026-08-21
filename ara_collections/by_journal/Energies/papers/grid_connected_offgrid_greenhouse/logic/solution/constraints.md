# Constraints

## Site Constraints
- **Location**: Sandikli, Afyonkarahisar, Turkiye (38.45N, 30.25E)
- **Solar resource**: Avg daily irradiation 4.18 kWh/m2, annual total 1527.46 kWh/m2
- **Wind resource**: Avg wind speed ~4-5 m/s (modest)
- **Temperature**: Seasonal range ~1-25 degC
- **Land availability**: North of administrative building, no shading structures

## Load Constraints
- **Annual demand**: 134,875 kWh/year
- **Daily average**: 369.52 kWh/day
- **Peak load**: 52.59 kW
- **Load components**: Ventilation, cooling, irrigation-fertilization, heating systems, administrative offices
- **Operating schedule**: Year-round, uninterrupted production

## Component Constraints
- **PV panels**: LG410N2W-V5, 410W monocrystalline-Si, 19.8% efficiency, 25-year lifetime
- **Wind turbines**: Eocycle EOX S-16, 30 kW rated, 15.8 m rotor diameter, cut-in 2.75 m/s, 30-year lifetime
- **Diesel generator**: Generic Gen60, 60 kW, 15,000 h lifetime, min load 25%
- **Battery**: SAFT/Kinetic 28S24M Li-ion, 55 kWh nominal, 720 V, 97% roundtrip efficiency, 20-year lifetime
- **Inverter**: TommaTech Hybrid, 60 kW, 97.6% efficiency, 15-year lifetime
- All components selected from domestically produced and easily accessible options

## Economic Constraints
- **Project lifetime**: 25 years
- **Discount rate**: 9.75% (Turkiye central bank rate)
- **Grid purchase price**: USD 0.096/kWh (EPIAS April-June 2025)
- **Grid sellback price**: USD 0.076/kWh (EPIAS April-June 2025)
- **Grid contract**: 150 kW capacity
- **Expected inflation**: Base 10% (varied 5-30% in sensitivity)

## Operational Constraints
- **Grid-connected**: Utility grid available; buy/sell arrangement with net metering
- **Off-grid**: No grid access; full autonomy required
- **Grid-connected vs standalone**: Mutually exclusive operational modes
- **Battery constraints**: Min state of charge 5%, max charge rate 1 A/Ah, throughput 240,000 kWh

## Software Constraints
- **Tool**: HOMER Pro ver. 3.14.2
- **Time resolution**: Hourly simulation for one year with optimization across 25-year lifetime
- **Optimization objective**: Minimize NPC
- **Data source**: NASA Surface Meteorology and Solar Energy database [84]
