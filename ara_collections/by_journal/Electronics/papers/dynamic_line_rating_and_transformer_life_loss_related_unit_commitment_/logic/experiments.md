# Experiments

## E01: DLR vs SLR transmission-capacity utilization under an extreme high-temperature typical day
- **Verifies**: C01, C03
- **Evidence**: evidence/figures/figure5.md, evidence/figures/figure4.md, evidence/tables/table2.md
- **Run**: UC optimization solved in Gurobi 12.0.1 (see src/environment.md); DLR ampacity per the
  formulation in logic/solution/formulation.md (Eqs. 1-10). No source code released by the paper.
- **Setup**:
  - Model: Mixed-integer UC on IEEE 39-bus, 10 thermal units, wind (DFIG) at buses 17 and 21
  - Hardware: 24-core Intel i9-13900, 16 GB RAM
  - Dataset: Day-ahead temperature/load/wind forecasts for a region in southwest China; 24 h horizon
    at 1 h steps; five regional temperature zones
  - System: Conventional static-thermal-stability UC vs temperature-dependent DLR-constrained UC
- **Procedure**:
  1. Build steady-state conductor temperature model (Eqs. 8-9) and derive Imax/Pmax(Ta) (Eq. 10).
  2. Solve conventional UC with static line limits.
  3. Solve UC with the temperature-dependent capacity constraint (Eq. 31).
  4. Compare transmission-capacity utilization in high-temperature regions and interface flows.
- **Metrics**: Transmission-capacity utilization improvement (%); interface power flow vs limit (MW)
- **Expected outcome**:
  - DLR exposes additional usable capacity in hot regions relative to SLR
  - Critical interface flows remain within limits under the DLR-constrained dispatch
- **Baselines**: Conventional (static thermal stability) UC
- **Dependencies**: none

## E02: Transformer hot-spot temperature and life-loss cost, aging-aware vs conventional
- **Verifies**: C02
- **Evidence**: evidence/figures/figure6.md, evidence/tables/table2.md
- **Run**: Same UC solve with vs without the transformer life-loss cost term; hot-spot/life-loss per
  logic/solution/formulation.md (Eqs. 11-21). No source code released by the paper.
- **Setup**:
  - Model: TL-TF UC (with life-loss cost) vs conventional UC
  - Hardware: as E01
  - Dataset: as E01; OA/ONAN transformer parameters (FT=1.4, n=0.9, m=0.8, θQC=22 C, ∆θTM-R=56.3 C)
  - System: 24 h dispatch, hot-spot computed from load ratio and ambient temperature
- **Procedure**:
  1. Compute hot-spot temperature trajectory for both models across the 24 h horizon.
  2. Evaluate transformer life-loss cost (Eqs. 20-22) for both.
  3. Compare hot-spot profiles against the 98 C IEC bound and compare loss costs.
- **Metrics**: Average transformer hot-spot temperature (C) over time; transformer loss cost
  (10^4 CNY)
- **Expected outcome**:
  - Conventional model exceeds 98 C and rises with ambient temperature; TL-TF stays near 98 C
  - TL-TF transformer loss cost is lower than conventional
- **Baselines**: Conventional UC
- **Dependencies**: E01

## E03: Total operating cost and dispatch reallocation, TL-TF vs conventional
- **Verifies**: C03
- **Evidence**: evidence/tables/table2.md, evidence/figures/figure4.md
- **Run**: Full UC objective (Eq. 22) solved for both models.
- **Setup**:
  - Model: TL-TF UC vs conventional UC
  - Hardware: as E01
  - Dataset: as E01; wind-curtailment penalty 500 CNY/(MW·h)
  - System: composite objective (generation, start-up/shutdown, transformer loss, wind curtailment)
- **Procedure**:
  1. Solve both models over the typical day.
  2. Compare per-unit output stacks (Figure 4a vs 4b), focusing on hot-region Unit 2.
  3. Tabulate generation, start-up/shutdown, wind-curtailment, transformer-loss, and total costs.
- **Metrics**: Cost components and total cost (10^4 CNY); wind curtailment reduction (MW); wind
  curtailment reduction (%)
- **Expected outcome**:
  - TL-TF suppresses hot-region economic unit output and shifts it to cooler/spare units
  - TL-TF lowers total operating cost and wind curtailment vs conventional
- **Baselines**: Conventional UC
- **Dependencies**: E01, E02

## E04: Temperature-scaling sensitivity of transformer life-loss cost
- **Verifies**: C04
- **Evidence**: evidence/tables/table4.md
- **Run**: Repeated UC solves with all regional temperature curves scaled by λ.
- **Setup**:
  - Model: TL-TF UC and conventional UC
  - Hardware: as E01
  - Dataset: Figure 2 temperature curves multiplied by λ ∈ {0.9, 1.0, 1.1, 1.2}, all other
    parameters fixed
  - System: 24 h dispatch per scenario
- **Procedure**:
  1. For each λ, scale all regional temperature curves.
  2. Solve conventional and TL-TF models; record transformer life-loss cost.
  3. Compute the cost-reduction ratio of TL-TF vs conventional per λ.
- **Metrics**: Transformer life-loss cost per model (10^4 CNY); cost-reduction ratio (%)
- **Expected outcome**:
  - Life-loss cost rises with λ in both models
  - TL-TF cost-reduction ratio increases with λ (benefit widens as it gets hotter)
- **Baselines**: Conventional UC
- **Dependencies**: E02

## E05: Sensitivity to wind-curtailment penalty and transformer investment cost
- **Verifies**: C05
- **Evidence**: evidence/tables/table3.md
- **Run**: UC solves sweeping penalty coefficient and transformer investment cost.
- **Setup**:
  - Model: TL-TF UC
  - Hardware: as E01
  - Dataset: penalty ∈ {100, 300, 500, 1000} CNY/(MW·h) at investment 230; investment ∈ {190, 230,
    260} (10^4 CNY) at penalty 500
  - System: 24 h dispatch per setting
- **Procedure**:
  1. Sweep the wind-curtailment penalty at fixed investment; record cost components and total cost.
  2. Sweep transformer investment cost at fixed penalty; record transformer loss and total cost.
  3. Characterize the total-cost trend vs penalty and the life-loss-cost trend vs investment.
- **Metrics**: Cost components and total cost (10^4 CNY)
- **Expected outcome**:
  - Total cost is U-shaped in the penalty coefficient (interior minimum near mid-range)
  - Both higher and lower investment cost raise life-loss cost relative to the standard value
- **Baselines**: Base-case setting (penalty 500, investment 230)
- **Dependencies**: E03
