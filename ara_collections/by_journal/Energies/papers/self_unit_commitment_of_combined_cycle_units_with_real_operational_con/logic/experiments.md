# Experiments

## E01: Case I — Hot-start feasibility verification
- **Verifies**: C01, C02, C03
- **Evidence**: [figure4.md](evidence/figures/figure4.md) (model-vs-heuristic output), [figure5.md](evidence/figures/figure5.md) (per-unit decomposition), [table5.md](evidence/tables/table5.md) (initial conditions)
- **Run**: SEUC MIP formulation (Eqs. 1–46) solved with Case I initial conditions (Table 5)
- **Setup**:
  - Model: SEUC MIP with 5 gas turbines + 2 steam turbines
  - Plant: TEBSA-like 5 × 2 CCGT, 800 MW max, G = 210 MW min
  - Initial state: GT1 and GT5 online (8 h), ST1 online (8 h), others off (hot-start regime)
  - Solver: Not specified in paper
- **Procedure**:
  1. Solve the SEUC formulation with Case I initial conditions
  2. Compare the resulting output trajectory against the heuristic schedule
  3. Verify per-unit decomposition resolves individual GT and ST contributions
  4. Check that minimum gas-hours (KGC=3 h) gate ST2 startup
- **Expected outcome**: The SEUC dispatch respects all modeled constraints (startup ramps, minimum gas hours, unit-count coupling, load distribution) and produces a physically followable plan; the heuristic schedule deviates beyond the 5% tolerance
- **Baselines**: Heuristic simulation code currently used by TEBSA
- **Dependencies**: none

## E02: Case II — Warm-start feasibility verification with cold ST2
- **Verifies**: C02, C03
- **Evidence**: [figure6.md](evidence/figures/figure6.md) (model-vs-heuristic output), [figure7.md](evidence/figures/figure7.md) (per-unit decomposition with supplementary fire), [table6.md](evidence/tables/table6.md) (initial conditions)
- **Run**: SEUC MIP formulation solved with Case II initial conditions (Table 6, all units off for 8 h)
- **Setup**:
  - Model: SEUC MIP (identical formulation to E01)
  - Initial state: All units offline for 8 h (warm-start regime)
  - Plant: Same 5 × 2 CCGT configuration as Case I
- **Procedure**:
  1. Solve the SEUC formulation with Case II initial conditions
  2. Verify ST2 cold-start gating (KGC = 3 h minimum gas-turbine operation)
  3. Verify supplementary fire contribution to reach maximum capacity
  4. Compare model output against heuristic schedule
- **Expected outcome**: The model selects a warm-start ramp (not hot-start as the heuristic does); ST2 start is delayed until gas turbines have run for at least KGC hours; supplementary fire is used at peak periods
- **Baselines**: Heuristic simulation code
- **Dependencies**: E01

## E03: Economic penalty quantification
- **Verifies**: C06
- **Evidence**: [figure4.md](evidence/figures/figure4.md), [figure6.md](evidence/figures/figure6.md), §3.1, §3.2, Ref [25]
- **Run**: Post-hoc calculation using model-vs-heuristic trajectory differences from E01 and E02
- **Setup**:
  - Penalty rule: Deviations exceeding 5% between scheduled and actual generation are penalized (Colombian market rule [25])
  - Penalty price: PCC = 120 USD/MWh
  - Scope: 24-hour horizon
- **Procedure**:
  1. Compute MW deviation between the heuristic and SEUC trajectories for Case I
  2. Apply the 5% threshold — only deviations exceeding 5% are penalized
  3. Multiply excess deviation by PCC price to obtain daily penalty
  4. Repeat for Case II
- **Expected outcome**: Heuristic-omitted constraints result in daily penalties on the order of tens of thousands of USD — demonstrating that modelling omissions convert directly into monetary costs
- **Baselines**: SEUC model output (treated as the physically followable baseline)
- **Dependencies**: E01, E02

## E04: Load distribution and supplementary fire verification
- **Verifies**: C04, C05
- **Evidence**: [figure5.md](evidence/figures/figure5.md), [figure7.md](evidence/figures/figure7.md), objective function DSC term (Eq. 1), Eqs. (41)–(46)
- **Run**: Analysis of per-unit output decomposition data from E01 and E02
- **Setup**:
  - Data: Per-unit GT and ST output trajectories from SEUC solution
  - Load distribution penalty: DSC term penalizing pairwise GT output differences
  - Supplementary fire: PAF = 15 MW cap per gas unit
- **Procedure**:
  1. Measure pairwise gas-turbine output differences at full-load periods
  2. Verify that both-above-minimum indicator activates DSC penalty in objective
  3. Check that supplementary fire contributes to ST output without raising GT output in Case II peak periods
- **Expected outcome**: Gas-turbine outputs are nearly equal (about 100 MW each) at full load; supplementary fire provides extra steam-turbine output (4.75 MW in Case II) without additional gas generation
- **Baselines**: SEUC model without DSC term
- **Dependencies**: E01, E02
