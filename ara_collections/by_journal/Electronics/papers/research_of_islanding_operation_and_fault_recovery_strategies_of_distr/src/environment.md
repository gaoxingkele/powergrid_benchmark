# Environment

Reproducibility record for Yang et al., Electronics 2023, 12, 4230. The paper releases no code
(Data Availability Statement: "Not applicable"), so `src/` holds only this environment record —
the method lives in `logic/solution/`.

- **Language/runtime**: Not specified in paper (optimization modeled and solved via CPLEX)
- **Framework / solver**: CPLEX 12.10 ("The optimization model in Equation (48) can be solved
  using mature commercial software CPLEX 12.10", §4.2)
- **Hardware (simulation)**: Not specified in paper
- **Hardware (semi-physical experiment, §6)**:
  - OPAL-RT real-time simulator — hosts the distribution-network environment
  - DSP controller — executes the islanding-operation and fault-recovery strategy
  - Oscilloscope — observes node voltage waveforms (node 24 as phase reference)
  - Interfaces: analog output (OPAL-RT → DSP measurements; DSP → oscilloscope), digital input
    (DSP → OPAL-RT switch signals); models/part numbers not specified in paper
- **Data sources**:
  - Improved IEEE 33-node distribution network (Baran & Wu benchmark, ref [28]) with 4 added DGs
    (Table 1) and three-level load weights (Table 2)
  - Measured wind-speed data from a microgrid project in Hubei Province, China; typical day at
    15-min intervals (96 points/day)
  - Metering: JZ818 smart meter (Jinzhi Technology Co., Ltd., Shenzhen, China), power measurement
    precision level 1.0, error ≤ 1%, bidirectional, RF/PLC/GPRS/NB-IoT communication
- **Key parameters**: ΔT = 15 min; scenario sample N = 500; reduced scenarios K = 5 (+2 extreme
  scenarios, Eq. 47); islanding fault case: substation breaker trip + S28; recovery cases:
  S28+DG3, S28, S9+S22; comparison recovery weight β = α; island autonomy duration in §5.3.4: 20 h
- **Unspecified parameters** (reproduction gaps): µ_loss, ϑ_loss, ϑ_switch, ξ1, ξ2, σ^L, σ^wind,
  σ^pv, τ_f, U_min/U_max numeric values (observed band 1.08–1.1 pu), Weibull k/c estimates, PV
  µ/σ profiles, line data of the improved network
- **Protocols**: rolling optimization (solve window T, commit one step, feedback correction);
  scenario generation (Latin hypercube) + K-means reduction; before/after-reconstruction
  comparison protocol for recovery cases
- **Random seeds**: Not specified in paper
