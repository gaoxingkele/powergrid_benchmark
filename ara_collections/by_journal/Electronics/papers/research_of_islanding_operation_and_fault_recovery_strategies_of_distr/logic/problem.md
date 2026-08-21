# Problem Specification

## Observations

### O1: DG integration adds complexity and uncertainty to fault handling
- **Statement**: Wind and photovoltaic DGs are increasingly connected to distribution networks; they
  raise structural/power-flow complexity and carry significant output uncertainty (randomness,
  intermittency, volatility).
- **Evidence**: §1 Introduction; uncertainty models Eqs. (40)-(42).
- **Implication**: Fault handling must explicitly account for stochastic DG output, not just
  pre-fault deterministic data.

### O2: Fault handling has two coupled stages
- **Statement**: Distribution-network fault handling splits into (i) the island division & operation
  stage (superior grid cannot supply — form islands around DGs to feed important loads) and (ii) the
  fault recovery stage (superior grid restored — reconnect lost load, possibly via reconstruction).
- **Evidence**: §1 (pages 1-2).
- **Implication**: A node's supply status in stage (i) affects its priority and satisfaction in stage
  (ii); the two stages are correlated.

### O3: Troubleshooting (fault-clearing) time is not fixed
- **Statement**: The autonomous operation time of a distribution island is uncertain — a fault may be
  fixed within a short span (<24 h) or persist far longer (>24 h).
- **Evidence**: §1 (page 3).
- **Implication**: Islanding/operation plans built on predicted data over a FIXED horizon (e.g. 24 h)
  may be suboptimal; a rolling, feedback-corrected scheme is preferable.

### O4: Voltage stays in band at high new-energy penetration
- **Statement**: In the case study, island node voltage stays in [1.0811, 1.1] pu across periods even
  when wind/PV output share reaches 34.09% (wind) and 48.65% (PV); over 20 random wind scenarios all
  node voltages remain within [1.08, 1.1] pu.
- **Evidence**: Figures 7, 9, 11; §5.2 text; Abstract.
- **Implication**: The proposed uncertainty-aware islanding operation keeps voltages safe under
  substantial renewable variability.

### O5: Network reconstruction reduces losses and raises minimum voltage in every tested fault
- **Statement**: Across three fault cases, GA-based reconstruction reduces line active-power loss by
  ≈11.9% / 13.6% / 14.2% and raises the minimum node voltage by 0.0046 / 0.0088 / 0.0046 pu.
- **Evidence**: Tables 3, 4, 5; Figures 15, 17, 19.
- **Implication**: Reconstruction during recovery improves economy and stability; DG availability
  (e.g. healthy DG3) materially affects the gains.

## Gaps

### G1: Islanding and fault recovery treated as separate, uncorrelated problems
- **Statement**: Existing research handles island operation and fault recovery independently,
  neglecting their correlation; the effect of island-scheme changes and no-power periods on user
  electricity satisfaction during recovery is ignored.
- **Caused by**: O2.
- **Existing attempts**: Reference [19] melds islanding with reconstruction; references [7-9] optimize
  island division alone; references [22-25] address recovery/reconstruction alone.
- **Why they fail**: They do not propagate a load's island-stage supply history into its
  recovery-stage weight, so loads that suffered intermittent supply can end up with poor satisfaction.

### G2: Fixed-horizon plans do not fit uncertain troubleshooting time
- **Statement**: Models relying on pre-fault data and a fixed future window cannot adapt when the
  fault-clearing time is variable.
- **Caused by**: O1, O3.
- **Existing attempts**: 24-h look-ahead islanding/operation plans; reference [14] introduced rolling
  optimization for real-time island operation.
- **Why they fail**: Long-horizon renewable prediction is inaccurate; a fixed horizon wastes the
  higher accuracy of short-term prediction.

### G3: DG output uncertainty not embedded in the island/recovery optimization
- **Statement**: Deterministic islanding/recovery models under-represent wind/PV randomness, risking
  voltage/flow violations under real fluctuation.
- **Caused by**: O1.
- **Existing attempts**: References [10,11,15] consider DG uncertainty for supply-capacity or
  resilience.
- **Why they fail**: Not integrated with a rolling islanding+recovery formulation solved as a tractable
  convex program.

## Key Insight
- **Insight**: Couple the two stages through a recovery-stage load weight β_{i,k} (Eq. 36) that adds,
  to the island-stage weight α_{i,k}, penalty terms for (a) changes in a node's island-membership over
  time and (b) periods with no supply — and drive both stages by a short-horizon ROLLING optimization
  with feedback correction, all cast as a scenario-weighted second-order cone program so wind/PV
  uncertainty is handled tractably.
- **Derived from**: O2, O3, O1.
- **Enables**: A single strategy that maximizes important-load supply and user satisfaction across the
  islanding->recovery lifecycle while respecting voltage/flow limits under renewable uncertainty.

## Assumptions
- A1: Island topology is radial; radiality/switch constraints (Eqs. 3-12) hold.
- A2: SOC relaxation of the branch-flow model is accurate for the radial network.
- A3: Wind speed follows a Weibull distribution; PV prediction error follows a normal distribution.
- A4: Scheduling interval ΔT = 15 min; short-term DG prediction is more accurate than long-term.
- A5: Energy storage returns to its initial state of charge at the end of the scheduling horizon
  (Eq. 34).
- A6: Test system = improved IEEE 33-node network with 4 DGs (Table 1); solved with CPLEX 12.10.
