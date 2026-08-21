# Environment

## Distribution System Configuration
- **System**: 54-bus radial distribution system
- **Substations**: 3 (existing)
- **Existing Feeders**: 50
- **Candidate Tie Lines**: 8
- **Nominal Voltage**: 15 kV
- **Power Factor**: 0.9

## System Parameters
- **Existing substation capacity**: 16.7 MVA
- **Substation upgrade options**:
  - 13.3 MVA unit at $8x10^6 installation cost
  - 16.7 MVA unit at $10x10^6 installation cost
- **Feeder upgrade options**:
  - Alternative 1: 250 A at $3.5x10^5/km
  - Alternative 2: 450 A at $4.6x10^5/km
  - Alternative 3: 900 A at $9.2x10^5/km

## Reliability Parameters (Table 6)
- **Feeders**: Failure rate = 0.21/km, Repair time = 8 h
- **Substation**: Failure rate = 0.6/100, Repair time = 24 h
- **Target SAIDI**: <= 2.5 h/year per bus per stage
- **Target ENS**: <= 5 MWh/year per bus per stage

## Cost Parameters
- **Interruption cost penalty**: $2,000/MWh
- **NO switch installation cost**: $4,700 each
- **Tie line construction cost**: $2x10^6 per km

## Planning Horizon
- **Duration**: 15 years
- **Stages**: 3 (each 5 years)
- **Annual load growth rate**: 3%
- **Discount rate (interest rate)**: 10%

## Wind Turbine Parameters (Table 2)
- **Cut-in speed (v_cin)**: 3 m/s
- **Rated speed (v_rated)**: 12 m/s
- **Cut-out speed (v_co)**: 25 m/s

## PV Module Specifications (Table 3)
- **Nominal Power (+/-5%)**: 75.0 W
- **Voltage at Pmax**: 46.9 V
- **Current at Pmax**: 1.6 A
- **Open Circuit Voltage**: 60.1 V
- **Short Circuit Current**: 1.82 A
- **Temperature Coefficient of Voc**: -0.2%/C
- **Temperature Coefficient of Isc**: +0.04%/C
- **Nominal Cell Operating Temperature**: 43 C

## Probabilistic Models
- **Load demand**: Normal distribution (fitted via K-S test)
- **Solar irradiance**: Beta distribution (fitted via K-S test)
- **Wind speed**: Weibull distribution (fitted via K-S test)

## DG Distribution

### Case Study 1 (CDG Only) -- Stage 1
Locations (bus number, capacity in MW):
Bus 6 (0), Bus 8 (0.7), Bus 10 (1.5), Bus 16 (0.4), Bus 17 (0.1), Bus 23 (0.9), Bus 25 (0.7), Bus 26 (1.1), Bus 28 (0.4), Bus 34 (2.6), Bus 36 (0.4), Bus 37 (0.3), Bus 38 (0.9), Bus 48 (1.3), Bus 50 (0.4)

### Case Study 2 (CDG + Wind + PV) -- Stage 1
- **CDG**: Buses 6(0.1), 8(0.8), 10(1.5), 16(0.4), 17(0.1), 23(0.8), 25(0.7), 26(1.1), 28(0.3), 34(2.4), 36(0.5), 37(0.0), 38(1.0), 48(0.9), 50(0.8) MW
- **Wind-DG**: Buses 3(0.1), 13(1.3), 19(1.0), 31(1.9), 42(0.3) MW
- **PV-DG**: Buses 6(2.0), 22(0.6), 32(1.2), 40(0.8), 44(0.1) MW

## Solution Software / Algorithm Requirements
- **Optimization method**: Genetic Algorithm (GA)
- **Load flow method**: Forward/backward sweep
- **Reliability assessment**: Analytical probabilistic model
- **Programming**: Not specified in paper (no specific language/tool mentioned)
