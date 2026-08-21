# Experiments

## E01: Four-scenario multi-objective comparison on IEEE 33-node
- **Verifies**: C01, C02, C05
- **Evidence**: evidence/tables/table1.md
- **Run**: MOPSO planning model (see logic/solution/algorithm.md; solver flow Figure A1); no released code — reconstructed from paper
- **Setup**:
  - Model: ADN multi-objective siting/sizing model (objectives f1/f2/f3, Eqs. 1–3)
  - Hardware: Not specified in paper
  - Dataset: IEEE 33-node system, total load 3715 kW + j2300 kvar, rated voltage 12.66 kV; DG at WT nodes 20/14, PV nodes 9/30
  - System: four scenarios — (1) no DG; (2) DG, no storage; (3) DG + EVS storage; (4) DG + normal storage
- **Procedure**:
  1. Generate DG scenarios (E05) and EV cluster prediction (E06) as inputs.
  2. Run MOPSO for each scenario configuration.
  3. Record the three objective values (voltage fluctuation, network loss, storage capacity) per scenario.
  4. Compare storage vs no-storage and EVS vs normal storage.
- **Metrics**: Target 1 = voltage fluctuation objective; Target 2 = network loss; Target 3 = storage capacity (dimensionless objective values)
- **Expected outcome**:
  - Adding storage (sc3/sc4) reduces network loss vs DG-only (sc2) on the loss objective relative to DG-only's degradation.
  - EVS storage (sc3) achieves lower voltage-fluctuation and network-loss objectives than normal storage (sc4), at the cost of a higher capacity objective.
- **Baselines**: no-DG, DG-only, normal-storage scenarios
- **Dependencies**: E05, E06

## E02: Node voltage surface comparison across scenarios 1–3
- **Verifies**: C01
- **Evidence**: evidence/figures/figure7.md
- **Run**: MOPSO planning model; power-flow evaluation over 24 h (reconstructed from paper)
- **Setup**:
  - Model: ADN power-flow / voltage evaluation under each scenario
  - Hardware: Not specified in paper
  - Dataset: IEEE 33-node; scenarios 1 (no DG), 2 (DG), 3 (DG + EVS storage)
  - System: 24-hour horizon, 33 nodes
- **Procedure**:
  1. Compute node voltages over 24 h for each scenario.
  2. Plot 3-D voltage surface (node × time × voltage).
  3. Compare surface roughness and the node-16 voltage deviation across scenarios.
- **Metrics**: node voltage (p.u.) over time; per-node voltage deviation (%) vs scenario 1
- **Expected outcome**:
  - Scenario 2 (DG) surface is rougher/more volatile than scenario 1.
  - Scenario 3 (DG + EVS) is smoother than scenario 2; node-16 deviation is far smaller in sc3 than sc2.
- **Baselines**: scenario 1 (no DG), scenario 2 (DG only)
- **Dependencies**: E01

## E03: EVS charge/discharge–SOC operational trace (scenario 3)
- **Verifies**: C01
- **Evidence**: evidence/figures/figure8.md
- **Run**: dispatch of the EVS storage model (Eqs. 6–9) under scenario 3 (reconstructed from paper)
- **Setup**:
  - Model: EVS cluster dispatchable storage (two devices)
  - Hardware: Not specified in paper
  - Dataset: scenario-3 DG profile and EV cluster parameters (Table A1)
  - System: 24-hour horizon, two energy-storage devices
- **Procedure**:
  1. Simulate charge/discharge decisions over 24 h under DG output.
  2. Record charge/discharge power (bars) and SOC (line) per device.
  3. Check SOC-band maintenance during the high-DG window.
- **Metrics**: charge/discharge power; SOC over time
- **Expected outcome**:
  - Devices charge when DG output is high and discharge when DG output is low; SOC stays within its band around the 10:00–15:00 high-DG window.
- **Baselines**: none
- **Dependencies**: E01

## E04: EVS siting result and average-voltage reduction at selected nodes
- **Verifies**: C01, C05
- **Evidence**: evidence/figures/figure9.md
- **Run**: MOPSO siting/sizing optimization (reconstructed from paper)
- **Setup**:
  - Model: multi-objective siting/capacity model with ≤2 EVS nodes, max installed power 400 kW, connectable node index 2–33
  - Hardware: Not specified in paper
  - Dataset: IEEE 33-node
  - System: MOPSO-selected EVS locations
- **Procedure**:
  1. Solve the multi-objective model for EVS site/capacity.
  2. Read off the selected node locations.
  3. Compare average node voltage at selected nodes before/after considering EVS.
- **Metrics**: selected node indices; average node voltage reduction (%) at the sited nodes
- **Expected outcome**:
  - The optimizer selects two nodes; average voltage at those nodes is reduced after considering the EVS siting/capacity model versus the no-EVS baseline.
- **Baselines**: no-EVS (pre-siting) voltage levels
- **Dependencies**: E01

## E05: DG scenario generation via KDE + Frank copula
- **Verifies**: C03
- **Evidence**: evidence/figures/figure4.md, evidence/figures/figure5.md, evidence/figures/figure1.md
- **Run**: scenario generator (KDE marginals + Frank copula sampling + scenario reduction); see logic/solution/method.md (reconstructed from paper)
- **Setup**:
  - Model: KDE (Eq. 4) + Frank copula (Eq. 5) joint wind–PV distribution
  - Hardware: Not specified in paper
  - Dataset: historical WT/PV output data (source per Reference [18]); details not released
  - System: 24-hour scenarios
- **Procedure**:
  1. Fit WT and PV marginals with KDE.
  2. Sample correlated uniforms via the Frank copula; invert marginals to build 24-h wind/PV scenarios.
  3. Generate many scenarios, then reduce to a small weighted representative set.
  4. Inspect whether scenarios retain randomness and wind–PV correlation.
- **Metrics**: per-scenario probability weights; scenario spread/envelope; qualitative wind–PV complementarity
- **Expected outcome**:
  - Reduced scenarios retain a spread (not one mean curve); wind is ragged and PV single-humped (complementary); the set reflects DG randomness and correlation better than independent/reliability-only sampling.
- **Baselines**: (conceptual) Weibull/Beta reliability sampling; day-ahead error sampling (both discussed as inferior in §3)
- **Dependencies**: none

## E06: CNN-BiLSTM vs CNN vs Bi-LSTM for EV-cluster state prediction
- **Verifies**: C04
- **Evidence**: evidence/figures/figure6.md
- **Run**: CNN-BiLSTM predictor (Figures 2–3); see logic/solution/method.md (reconstructed from paper)
- **Setup**:
  - Model: CNN-BiLSTM vs standalone CNN vs standalone Bi-LSTM
  - Hardware: Not specified in paper
  - Dataset: EV cluster historical data (arrival/departure time, initial SOC); 40-sample test set
  - System: train/test split
- **Procedure**:
  1. Train each model on the EV-cluster training group.
  2. Predict arrival time, departure time, initial SOC on the test group.
  3. Compare each model's predictions against ground truth.
- **Metrics**: prediction error vs true value (relative %); tracking closeness across the three quantities
- **Expected outcome**:
  - CNN-BiLSTM tracks true values more closely than CNN or Bi-LSTM alone across all three predicted quantities; its error is lower than both baselines.
- **Baselines**: ordinary CNN; Bi-LSTM
- **Dependencies**: none
