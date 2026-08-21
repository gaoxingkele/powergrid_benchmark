# Experiments

Declarative verification plans reconstructed from §5 (Example Analysis) and §6 (Experiment).
Directional expectations only — exact numbers live in `evidence/`. All simulation experiments run
on the improved IEEE 33-node network (Figure 1, Tables 1–2), solved with CPLEX 12.10; no code or
seeds are released (see `src/environment.md`).

## E01: Island division under an extreme fault
- **Verifies**: C01
- **Evidence**: evidence/figures/figure6.md (partition result), evidence/figures/figure1.md,
  evidence/tables/table1.md, evidence/tables/table2.md (system inputs)
- **Run**: Not released; per §5.2, islanding division/operation model (Eqs. 1–34) solved in CPLEX 12.10
- **Setup**:
  - Model: island division & operation MISOCP (Eqs. 1–34), scenario-weighted form (Eq. 48)
  - Hardware: Not specified in paper
  - Dataset: improved IEEE 33-node network, 4 DGs (Table 1), load weights (Table 2)
  - System: upstream substation outlet breaker trips AND line S28 faults; wind power at node 6
- **Procedure**:
  1. Impose the extreme fault (grid-connection loss + S28 outage).
  2. Solve the islanding division and operation model for a sample wind/PV output period.
  3. Record the island partition (membership of DGs and loads).
- **Metrics**: island count; DG membership per island; number of loads supplied per island
- **Expected outcome**:
  - All DGs and all important (high-weight) loads end up inside islands.
  - The network splits into a small number of self-supplying radial islands.
- **Baselines**: none (feasibility/mechanism demonstration)
- **Dependencies**: none

## E02: Scenario generation and reduction for wind and PV
- **Verifies**: C02
- **Evidence**: evidence/figures/figure2.md, figure3.md (wind), figure4.md, figure5.md (PV)
- **Run**: Not released; per §4.2/§5.1, Latin hypercube sampling + K-means clustering
- **Setup**:
  - Model: Weibull wind-speed distribution (Eq. 40) + turbine curve (Eq. 41); normal PV prediction error (Eq. 42)
  - Hardware: Not specified in paper
  - Dataset: measured wind-speed data from a Hubei Province microgrid project; typical day sampled at 15-min intervals (96 points); JZ818 smart-meter measurements (precision level 1.0)
  - System: sampling scale N = 500; cluster number K = 5; two extreme scenarios appended (Eq. 47)
- **Procedure**:
  1. Fit Weibull parameters k, c from measured wind data; fit PV error distribution.
  2. Latin-hypercube-sample a large ensemble of daily output curves on the typical-day base profile.
  3. K-means-cluster the ensemble to a small representative set; weight each by cluster size (ρ).
  4. Append the max-wind/min-PV and min-wind/max-PV extreme scenarios (Ψcom).
- **Metrics**: ensemble envelope vs. base profile; representativeness of reduced curves; cluster weights
- **Expected outcome**:
  - The reduced set tracks the typical-day shape while spanning the generated ensemble's spread.
  - Optimization over the reduced+extreme set stays tractable per scheduling period.
- **Baselines**: full generated ensemble (visual comparison)
- **Dependencies**: none

## E03: Island 2 rolling operation with wind at node 6
- **Verifies**: C03
- **Evidence**: evidence/figures/figure7.md (voltages), evidence/figures/figure8.md (DG/load/loss)
- **Run**: Not released; §5.2 rolling optimization, five periods analyzed
- **Setup**:
  - Model: scenario-weighted islanding operation MISOCP with rolling horizon
  - Hardware: Not specified in paper
  - Dataset: improved IEEE 33-node, Island 2 nodes (2–7, 22–26); wind DG at node 6
  - System: extreme fault as in E01; ΔT = 15 min; five periods selected for reporting
- **Procedure**:
  1. Run rolling optimization; at each period commit only the next-step schedule.
  2. Record per-period node voltages, wind output, diesel output, island load, line losses.
- **Metrics**: node voltage (pu); DG outputs (MW); island load (MW); line loss (kW); wind share of supply (%)
- **Expected outcome**:
  - All node voltages remain inside the safety band in every period.
  - Diesel output complements wind fluctuation so important loads stay supplied.
- **Baselines**: none
- **Dependencies**: E01, E02

## E04: Island 2 rolling operation with PV at node 6
- **Verifies**: C03
- **Evidence**: evidence/figures/figure9.md (voltages), evidence/figures/figure10.md (DG/load/loss)
- **Run**: Not released; §5.2, same protocol as E03 with PV replacing wind
- **Setup**: as E03 but node 6 hosts photovoltaic power (larger fluctuation across the five periods)
- **Procedure**: as E03.
- **Metrics**: as E03 (PV share of supply instead of wind share)
- **Expected outcome**:
  - Despite larger PV fluctuation, voltages stay in band and loads stay supplied.
  - PV share can reach a higher peak than the wind case without violation.
- **Baselines**: E03 (wind case, qualitative contrast)
- **Dependencies**: E01, E02

## E05: Voltage robustness over 20 random wind scenarios
- **Verifies**: C03
- **Evidence**: evidence/figures/figure11.md (box plots)
- **Run**: Not released; §5.2, 20 randomly generated wind scenarios
- **Setup**:
  - Model: as E03; wind at node 6, Island 2
  - System: 20 random wind-power scenarios for one time period
- **Procedure**:
  1. Generate 20 random wind scenarios from the uncertainty model.
  2. Solve island operation per scenario; collect per-node voltage statistics.
- **Metrics**: per-node voltage distribution (median, quartiles, 9–91% whiskers)
- **Expected outcome**:
  - Every node's voltage across all scenarios stays inside the allowed band; dispersion is narrow.
- **Baselines**: none
- **Dependencies**: E03

## E06: Island 1 operation at different initial storage energy levels
- **Verifies**: C03
- **Evidence**: evidence/figures/figure12.md (50% case), evidence/figures/figure13.md (80% case)
- **Run**: Not released; §5.2, Island 1 with storage DG2
- **Setup**:
  - Model: as E03; Island 1 nodes (10–17, 29–32), energy storage at node 13
  - System: initial storage energy = 50% and 80% of rated capacity; five periods each
- **Procedure**:
  1. Fix the initial state of charge; run rolling island operation for five periods.
  2. Record node voltages, island load, and line losses; repeat for the second SOC level.
- **Metrics**: node voltage (pu); island load (MW); line loss (kW); loss share of total load (%)
- **Expected outcome**:
  - No voltage violation at either initial SOC; losses remain a small fraction of load.
  - The strategy is insensitive to the initial storage energy level within the tested range.
- **Baselines**: the two SOC levels serve as mutual comparison
- **Dependencies**: E01

## E07: Fault recovery with reconstruction — fault at S28 and DG3
- **Verifies**: C04, C06
- **Evidence**: evidence/tables/table3.md, evidence/figures/figure14.md, evidence/figures/figure15.md
- **Run**: Not released; §5.3.1, recovery model (Eqs. 35–39) + reconstruction
- **Setup**:
  - Model: fault recovery MISOCP with network reconstruction; scenario-weighted form
  - System: faulted branch S28 plus DG3 outage; upstream grid restored
- **Procedure**:
  1. Isolate the fault; solve recovery with topology reconstruction enabled.
  2. Compare loss and node-voltage extrema before vs. after reconstruction.
- **Metrics**: active power loss (kW); minimum/maximum node voltage (pu); switch actions
- **Expected outcome**:
  - Reconstruction reduces network loss and raises the minimum node voltage.
  - Downstream DG4 islands via S29 opening; node 28 reconnects via tie switch S37.
- **Baselines**: pre-reconstruction (restored-grid, no reconfiguration) configuration
- **Dependencies**: E01

## E08: Fault recovery with reconstruction — fault at S28 only
- **Verifies**: C04, C06
- **Evidence**: evidence/tables/table4.md, evidence/figures/figure16.md, evidence/figures/figure17.md
- **Run**: Not released; §5.3.2, same protocol as E07 with DG3 healthy
- **Setup**: as E07 but only branch S28 faulted (DG3 in service)
- **Procedure**: as E07.
- **Metrics**: as E07
- **Expected outcome**:
  - Reconstruction again reduces loss and raises minimum voltage.
  - With DG3 available, losses are substantially lower than the S28+DG3 case (C06 contrast).
- **Baselines**: pre-reconstruction configuration; E07 (DG-availability contrast)
- **Dependencies**: E07

## E09: Fault recovery with reconstruction — faults at S9 and S22
- **Verifies**: C04
- **Evidence**: evidence/tables/table5.md, evidence/figures/figure18.md, evidence/figures/figure19.md
- **Run**: Not released; §5.3.3, two simultaneous line faults
- **Setup**: as E07 but branches S9 and S22 faulted; DG2 and DG3 island their downstream areas
- **Procedure**: as E07.
- **Metrics**: as E07
- **Expected outcome**:
  - Two islands form (DG2 supplying nodes 10–16, DG3 supplying nodes 22–24) while the rest
    reconnects; reconstruction reduces loss and raises minimum voltage.
- **Baselines**: pre-reconstruction configuration
- **Dependencies**: E07

## E10: Ablation of the island-history-aware recovery weight (β = α comparison)
- **Verifies**: C05
- **Evidence**: evidence/figures/figure20.md (comparison result) vs evidence/figures/figure16.md (proposed)
- **Run**: Not released; §5.3.4, comparison method with β_{i,k} = α_{i,k}
- **Setup**:
  - Model: recovery model as E08 but load weight reduced to the static island-stage weight
  - System: S28 fault; 20 h isolated operation before grid restoration; wind at node 6; node 28
    experiences outage → supply → outage during islanding
- **Procedure**:
  1. Run 20 h rolling islanding so island membership of the boundary node churns with wind output.
  2. Solve recovery once with the proposed β (Eq. 36) and once with β = α.
  3. Compare which loads are re-energized in each reconstruction result.
- **Metrics**: restored-load set; supply status of the churned node; switch actions
- **Expected outcome**:
  - The proposed weight restores the intermittently supplied node; the static weight leaves it
    unpowered (dead-end variant kept as the paper's baseline contrast).
- **Baselines**: β = α static-weight recovery (the comparison method)
- **Dependencies**: E08

## E11: Semi-physical validation on OPAL-RT + DSP
- **Verifies**: C07
- **Evidence**: evidence/figures/figure21.md (framework), evidence/figures/figure22.md,
  figure23.md, figure24.md (waveforms, periods 1–3)
- **Run**: Not released; §6 hardware-in-the-loop experiment
- **Setup**:
  - Model: proposed strategy implemented on a DSP controller
  - Hardware: OPAL-RT real-time simulator (network environment), DSP islanding/fault-recovery
    controller, oscilloscope for node-voltage observation
  - System: PV at node 6; fault in line S28; node 24 as phase-reference node
- **Procedure**:
  1. Run the distribution network in OPAL-RT; DSP gathers power information via analog/digital I/O.
  2. DSP detects the fault, issues switch signals; network splits into two islands (as Figure 6).
  3. Islands dispatch internal resources per the proposed method; observe node voltages for three
     scheduling periods.
- **Metrics**: node voltage magnitude (pu); phase angle (degrees); frequency (Hz); waveform stability
- **Expected outcome**:
  - The hardware-executed partition matches the simulation partition.
  - Islanded operation is stable: near-nominal frequency, bounded voltage and phase spread, no
    limit violations.
- **Baselines**: simulation partition (Figure 6) as the reference
- **Dependencies**: E01, E04
