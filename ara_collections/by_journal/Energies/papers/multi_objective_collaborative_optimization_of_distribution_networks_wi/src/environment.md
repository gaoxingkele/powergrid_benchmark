# Source Environment

## Hardware & Software Context
- **Test system**: IEEE 33-bus distribution network
- **Simulation environment**: Not specified
- **Algorithm implementation**: Not specified (programming language, libraries not mentioned)

## Data Sources
- Wind turbine parameters: cut-in speed vci, cut-out speed vco, rated speed vr; rated power Pr-WT
- Photovoltaic parameters: number of cells nPV, rated power Pr-PV, rated irradiance Rr, temperature coefficient k
- EV parameters: daily driving distance (normal distribution, mu and sigma not specified numerically), battery capacity CEV, charging power PEV_charging
- ES parameters: charge/discharge efficiency eta, SOC limits, power limits
- IEEE 33-bus network topology: standard test feeder with the longest feeder covering nodes 5-17

## Specific Parameter Values (from Table 1)
- CES (ES cost): 130 million yuan/MW
- CPV (PV cost): 100 million yuan/MW
- Cwind (wind cost): 100 million yuan/MW
- a: 46.5 million yuan/MW
- b: 5 million yuan
- pin: 0.0013
- pout: 0.01
- epsilon: 0
- lambda: 0.25
- lambda': 0.33
- Nl,max: 3
- Npv,max, Nwind,max: 3

## Algorithm Parameters
- Crossover factor: 0.8
- Mutation factor: 0.8
- Population size: 250
- Maximum generations: 100
- Penalty factors: w1,w2,w3 = 6.0e-3; w4,w5 = 1.0e-3; w6,w7 = 7.0e-3; w8 = 1.0e-3

## DG Design Capacities
- Wind power: 0.50 MW
- Photovoltaic: 1.10 MW
- Load: 2.00 MW
