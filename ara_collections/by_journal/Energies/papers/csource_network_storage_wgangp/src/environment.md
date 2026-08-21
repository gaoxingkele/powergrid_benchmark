# System Environment

## Hardware (Inferred)
- Not specified in paper. Typical workstation for power system optimization studies.

## Software & Libraries
- **Optimization solver**: Not specified (commercial solver such as CPLEX, Gurobi, or MOSEK implied for SOCP)
- **Scenario generation framework**: Python (implied; WGAN-GP model with PyTorch or TensorFlow)
- **Programming language**: Not explicitly specified in paper

## Test System
- **Network**: Modified Portuguese 54-bus distribution network [21]
- **Substations**: 4 (S1 existing 16.7 MVA, S2 existing 30 MVA, S3 new 22.2 MVA, S4 new 22.2 MVA)
- **Feeder impedance**: 0.307 + j0.380 Ω/km
- **Feeder rated capacity**: 6.12 MVA
- **Voltage range**: [0.95, 1.05] p.u.
- **Load power factor**: 0.9

## WGAN-GP Model Configuration
- **Input noise dimension**: Z, 128
- **Generator output**: 24×24 wind–PV time series
- **Discriminator input**: 24×24
- **Activation**: Tanh (generator output), LeakyReLU(0.2) (discriminator)
- **Dropout**: 0.3 (discriminator)
- **Loss**: Wasserstein Loss + Gradient Penalty

## Planning Parameters
- **Planning horizon**: 15 years
- **Discount rate**: 5%
- **Number of representative scenarios**: 4 (determined by Silhouette Coefficient)
- **Maximum DG penetration**: 60%

## E-SOP Parameters
- **SOP unit rating**: 100 kVA
- **SOP investment cost**: 1000 CNY/kVA
- **SOP power loss coefficient**: 0.02
- **SOP O&M coefficient**: 0.01
- **BESS energy cost**: 1000 CNY/kWh
- **BESS power cost**: 1500 CNY/kW
- **BESS total energy capacity limit**: 6000 kWh
- **BESS total power capacity limit**: 2000 kW
- **BESS initial SOC**: 0.5
- **BESS SOC range**: [0.2, 1.0]

## DG Parameters
- **PV unit investment cost**: 4300 CNY/kW
- **Wind unit investment cost**: 5600 CNY/kW
- **DG O&M cost**: 0.03 CNY/kWh
- **Rated power per unit**: 100 kW
- **Power factor range**: 0.95 leading to 0.95 lagging

## SCCR Algorithm Parameters
- **Convergence threshold (ε)**: Not explicitly specified (relaxation gap reduced below order of 10^(-5))
- **Initial penalty weight (χ0)**: Not explicitly specified
- **Step-size factor (ω)**: Not explicitly specified
