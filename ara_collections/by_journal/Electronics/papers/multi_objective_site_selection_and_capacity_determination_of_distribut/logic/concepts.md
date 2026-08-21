# Concepts

## Active Distribution Network (ADN)
- **Notation**: —
- **Definition**: A distribution network able to combine and control various distributed energy resources (distributed power, controllable load, energy storage, demand-side management). Here modeled on the IEEE 33-node system (total load 3715 kW + j2300 kvar, rated voltage 12.66 kV).
- **Boundary conditions**: Radial distribution feeder; validated on a single test system.
- **Related concepts**: Distributed Generation, EV Shared Energy Storage, Network Loss objective.

## Distributed Generation (DG)
- **Notation**: —
- **Definition**: Renewable generation (wind turbines WT, photovoltaic PV) connected at the supply end; carbon-free but with highly uncertain output. In the case, WT at nodes 20 and 14, PV at nodes 9 and 30.
- **Boundary conditions**: Output treated as a stochastic process requiring scenario modeling; assumed to have negative wind–solar correlation/complementarity.
- **Related concepts**: Frank Copula, Kernel Density Estimation, Scenario Reduction.

## EV Shared Energy Storage (EVS cluster)
- **Notation**: S_t^EVS (SOC state), P_cha / P_dis (charge/discharge power)
- **Definition**: An EV charging-station fleet ("electric vehicle station", EVS) modeled as an aggregate dispatchable energy-storage device: its accumulated SOC charges/discharges within limits, substituting for dedicated stationary storage. Multi-type EV cluster with fixed arrival/departure time and initial SOC (Table A1).
- **Boundary conditions**: Fixed T_arrive/T_leave and S0 per EV type; SOC bounded S_min^EVS ≤ S_t^EVS ≤ S_max^EVS; power bounded by P_cha,max / P_dis,max; must return to expected SOC S_exp^EVS at horizon end (Eqs. 6–9).
- **Related concepts**: State of Charge, Dispatchable Potential, CNN-BiLSTM.

## Frank Copula Function
- **Notation**: F^n(x^i, y^i) = C(F_Xi(x^i), F_Yi(y^i))
- **Definition**: A copula joining the marginal CDFs of wind and PV output into a joint distribution; chosen because it handles both non-negative and negative correlations, matching DG's negative correlation/complementarity.
- **Boundary conditions**: Applied per time period; marginals fitted by KDE; used to sample correlated 24-hour wind/PV scenarios.
- **Related concepts**: Kernel Density Estimation, Scenario Reduction, DG.

## Kernel Density Estimation (KDE)
- **Notation**: f̂(x) = (1/nh) Σ_{t=i}^T K((x − X_i)/h)
- **Definition**: A non-parametric estimator of the DG output probability density from historical data (n = sample size, h = window width, K = kernel), avoiding distributional assumptions (e.g., Weibull/Beta).
- **Boundary conditions**: Requires representative historical WT/PV output data; produces per-period output PDF.
- **Related concepts**: Frank Copula, DG.

## Multi-Objective Particle Swarm Optimizer (MOPSO)
- **Notation**: —
- **Definition**: The metaheuristic solver used to co-optimize EVS siting/capacity against the three objectives (voltage fluctuation, network loss, storage capacity); iterates particle fitness updates until convergence (Figure A1), invoking "cplex" within the scheme-solving step.
- **Boundary conditions**: The paper notes MOPSO's solution efficiency is slow and to be improved; a specific "improved" MOPSO variant is referenced in the abstract but algorithmic modifications are not detailed.
- **Related concepts**: Multi-Objective Optimization, Node Voltage Fluctuation, Network Loss.

## CNN-BiLSTM
- **Notation**: —
- **Definition**: A hybrid predictor: a convolutional neural network (local connection + weight sharing for feature extraction) feeding a bidirectional LSTM (forward + reverse passes) to predict EV-cluster state (arrival/departure time, initial SOC) from historical data.
- **Boundary conditions**: Data split into training/test groups; predicts three EV quantities on a 40-sample test set; single dataset.
- **Related concepts**: EV Shared Energy Storage, State of Charge.

## Node Voltage Fluctuation (objective f1)
- **Notation**: f1 = Σ_{i=1}^{Nbus} Σ_{j=1}^{T} |V_ij − V̄_i|
- **Definition**: The summed absolute deviation of node voltages from standard voltage over all nodes and 24 hours; the first optimization objective, a proxy for voltage stability ("vulnerability").
- **Boundary conditions**: T = 24 h; over all Nbus nodes; V̄_i = standard voltage.
- **Related concepts**: Network Loss objective, Energy Storage Capacity objective, ADN.

## Network Loss (objective f2)
- **Notation**: f2 = c_loss Σ_{t=1}^{T} Σ_{ij∈Eline} I_ij,t² r_ij
- **Definition**: The cost-weighted sum of I²r branch losses over all ADN branches and 24 hours; the second optimization objective. Motivated by DG sited far from the main line increasing electrical distance and hence loss.
- **Boundary conditions**: c_loss = unit network loss cost (value not specified in paper); Eline = set of ADN branches; evaluated over T = 24 h.
- **Related concepts**: Node Voltage Fluctuation objective, Energy Storage Capacity objective, ADN, DG.

## Energy Storage Capacity (objective f3)
- **Notation**: f3 = Σ_{j=1}^{2} Σ^{t0+nΔt} P_cha(j)/P_dis(j) Δt
- **Definition**: The total committed capacity of the (two) energy-storage devices, accumulated from their charge/discharge power over the charging window; the third optimization objective, minimized to avoid large investment and low utilization in the early ADN construction stage.
- **Boundary conditions**: t0 = time when charging starts; Δt = charge/discharge duration; applies only to scenarios that include storage (Table 1 marks it "/" for scenarios 1–2).
- **Related concepts**: Node Voltage Fluctuation objective, Network Loss objective, EV Shared Energy Storage.
