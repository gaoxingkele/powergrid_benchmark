# Experiments

## E01: FDB-variant identification on CEC benchmark suites (Friedman + Wilcoxon)
- **Verifies**: C01, C02, C06
- **Evidence**: evidence/tables/table2.md, table3.md, table4.md, table5.md, table6.md; evidence/figures/figure1.md
- **Run**: src/execution/fdbcoa_obl.py (reconstructed); COA + FDBCOA1/FDBCOA2/FDBCOA3 (Table 1 placements) on CEC2020/CEC2022 benchmark packages [51], [52].
- **Setup**:
  - Model: COA and three FDB variants (FDB injected at different position-update equations)
  - Hardware: not specified for benchmark runs (see environment.md)
  - Dataset: CEC2020 (dims 5,10,15,20,30,50,100) and CEC2022 (dims 10,20) test functions
  - System: termination at maxFEs = 10000×Dim; 51 independent runs; population sizes 30/50/100
- **Procedure**:
  1. Define three FDB placements (FDBCOA1: Eq. 17; FDBCOA2/3: Eq. 19 branches).
  2. Run all four algorithms on each function/dim/pop-size 51 times.
  3. Compute Friedman scores and rank the mean values.
  4. Compute Wilcoxon pairwise +/=/- vs COA per dim and pop size.
- **Metrics**: Friedman mean score and rank; Wilcoxon win/tie/loss counts; aggregate win/draw/loss rates.
- **Expected outcome**:
  - All FDB variants outrank base COA on mean Friedman score.
  - FDBCOA1 attains the best rank; FDBCOA3 the worst among FDB variants.
  - A residual set of ties/losses remains (no universal domination).
- **Baselines**: base COA.
- **Dependencies**: none

## E02: Scalability analysis of the FDB variants (D=20 → D=50)
- **Verifies**: C01, C02, C07
- **Evidence**: evidence/tables/table7.md
- **Run**: src/execution/fdbcoa_obl.py (reconstructed); COA + FDBCOA1/2/3 on F1–F10.
- **Setup**:
  - Model: COA and three FDB variants
  - Dataset: CEC2020 functions F1–F10
  - System: P=100; dimensions D=20 and D=50
- **Procedure**:
  1. Run each algorithm on F1–F10 at D=20 and D=50.
  2. Record mean and standard deviation per function.
  3. Compare the growth of mean and std as dimension increases.
- **Metrics**: per-function Mean and Std of the objective at each dimension.
- **Expected outcome**:
  - Base COA has highest mean but highest variance (unstable).
  - FDBCOA1 keeps the most controlled std as dimension grows (best scalability); FDBCOA3 scales worst.
- **Baselines**: base COA.
- **Dependencies**: E01

## E03: OBL-scheme identification on CEC benchmark suites (Friedman + Wilcoxon)
- **Verifies**: C03, C06
- **Evidence**: evidence/tables/table8.md, table9.md, table10.md, table11.md, table12.md; evidence/figures/figure4.md
- **Run**: src/execution/fdbcoa_obl.py (reconstructed); COA, FDBCOA1, and FDBCOA1-OBL1…OBL8 (eight OBL initial-population schemes).
- **Setup**:
  - Model: 10 algorithms (COA, FDBCOA1, 8 OBL-seeded FDBCOA1 variants)
  - Dataset: CEC2020 (dims 5–100), CEC2022 (dims 10,20)
  - System: maxFEs = 10000×Dim; 51 runs; pop sizes 30/50/100
- **Procedure**:
  1. Seed FDBCOA1's initial population with each of eight OBL schemes (Eqs. 29–38).
  2. Run all 10 algorithms across functions/dims/pop-sizes 51 times.
  3. Compute Friedman ranks and Wilcoxon +/=/- vs COA.
- **Metrics**: Friedman mean score and rank (of 10); Wilcoxon win/tie/loss; aggregate rates.
- **Expected outcome**:
  - Elite OBL (OBL5) attains the best mean Friedman rank.
  - FDBCOA1-without-OBL ranks well below the best OBL variant (mid-pack).
  - OBL-seeded variants generally outperform non-OBL variants.
- **Baselines**: COA, FDBCOA1 (no OBL).
- **Dependencies**: E01

## E04: Scalability analysis of the OBL variants (P=100, D=50)
- **Verifies**: C03
- **Evidence**: evidence/tables/table13.md
- **Run**: src/execution/fdbcoa_obl.py (reconstructed); COA, FDBCOA1, FDBCOA1-OBL1…OBL8 on F1–F10.
- **Setup**:
  - Model: 10 algorithms
  - Dataset: CEC2020 F1–F10
  - System: P=100, D=50
- **Procedure**:
  1. Run all 10 algorithms on F1–F10 at P=100, D=50.
  2. Record mean and std per function.
  3. Assess which variant scales best (average improves, std reasonable).
- **Metrics**: per-function Mean and Std.
- **Expected outcome**: FDBCOA1-OBL5 shows the best scalability (best average across most functions with reasonable std).
- **Baselines**: COA, FDBCOA1.
- **Dependencies**: E03

## E05: Convergence and box-plot analysis of variants
- **Verifies**: C01, C03
- **Evidence**: evidence/figures/figure2.md, figure3.md, figure5.md, figure6.md
- **Run**: src/execution/fdbcoa_obl.py (reconstructed); selected functions from unimodal/basic/hybrid/composition categories.
- **Setup**:
  - Dataset: CEC2020 (P=50) and CEC2022 (P=30/P=100) representative functions
  - System: 51 runs; convergence over fitness-evaluations; box plots of best fitness
- **Procedure**:
  1. Log function-error value vs number of fitness evaluations per algorithm.
  2. Aggregate best fitness across 51 cycles into box plots.
  3. Compare curves/box positions across variants.
- **Metrics**: function-error convergence trajectory; distribution (best/median/worst) of best fitness.
- **Expected outcome**: FDB and OBL variants reduce function error below base COA / FDBCOA1; the best variant (FDBCOA1 for FDB stage; OBL5 for OBL stage) has the lowest error/box.
- **Baselines**: COA, FDBCOA1.
- **Dependencies**: E01, E03

## E06: Static TNEP on Garver 6-bus (with/without generation resizing)
- **Verifies**: C04, C08
- **Evidence**: evidence/tables/table14.md, table15.md; evidence/figures/figure8.md, figure9.md, figure10.md
- **Run**: FDBCOA1-OBL5 on Garver 6-bus; DC flow via MATPOWER 6.0; data from ref [58].
- **Setup**:
  - Model: FDBCOA1-OBL5
  - System: Garver 6-bus, 760 MW consumption, 215 MW production (+545 MW sixth-bus unit); slack = bus 1; max parallel lines = 4; 9 params (fixed) / 11 params (resizing)
  - Penalty: ω₁,λ₁,λ₂,λ₃ = 10^5, 10^6, 10^7, 10^5
- **Procedure**:
  1. Solve STNEP without generation resizing (Case 1), 51 runs.
  2. Solve STNEP with generation resizing (Case 2), 51 runs.
  3. Compare best/worst/average cost and line additions vs SS, GAPSO, PLPSO, DEA.
- **Metrics**: total investment cost (US$); line additions; convergence iteration.
- **Expected outcome**: reaches the documented optimal (lower with resizing than without); matches best literature results.
- **Baselines**: SS [7], GAPSO [2], PLPSO [25], DEA [58].
- **Dependencies**: E03, E04

## E07: Static TNEP on IEEE 25-bus (with/without generation resizing)
- **Verifies**: C04, C08
- **Evidence**: evidence/tables/table16.md, table17.md; evidence/figures/figure11.md, figure12.md, figure13.md
- **Run**: FDBCOA1-OBL5 on IEEE 25-bus; DC flow via MATPOWER 6.0; data from refs [58], [64].
- **Setup**:
  - Model: FDBCOA1-OBL5
  - System: IEEE 25-bus, 2750 MW demand, 36 candidate line paths; max parallel lines = 4; 36 params (fixed) / 46 params (resizing)
  - Penalty: ω₁,λ₁,λ₂,λ₃ = 10^8, 10^9, 10^9, 10^7
- **Procedure**:
  1. Solve STNEP without resizing (Case 1), 51 runs.
  2. Solve STNEP with resizing (Case 2), 51 runs.
  3. Compare cost/line additions vs GBMO, MOX, CGA, DEA.
- **Metrics**: total investment cost (US$); line additions; convergence iteration.
- **Expected outcome**: competitive/lowest cost; resizing yields far lower cost than fixed generation.
- **Baselines**: GBMO [65], MOX [66], CGA [67], DEA [58].
- **Dependencies**: E03, E04

## E08: Dynamic multistage TNEP on Colombian 93-bus
- **Verifies**: C04
- **Evidence**: evidence/tables/table18.md, table19.md; evidence/figures/figure14.md, figure15.md
- **Run**: FDBCOA1-OBL5 on Colombian 93-bus; 3 planning stages; DC flow via MATPOWER 6.0; data from ref [58].
- **Setup**:
  - Model: FDBCOA1-OBL5
  - System: Colombian 93-bus, 14559 MW active demand, 155 candidate lines; max parallel lines = 4; 155 params; base year 2002; I=10%
  - Stages: P1 (2002–2005), P2 (2005–2009), P3 (2009–2012)
  - Penalty: ω₁,λ₁,λ₂,λ₃ = 10^9, 5×10^8, 5×10^8, 5×10^6
- **Procedure**:
  1. Solve DTNEP per stage, 51 runs each.
  2. Discount each stage's investment to base year (Eq. 10) and sum.
  3. Compare total cost and load shedding vs HGA, DEA, CGA, EGA.
- **Metrics**: per-stage and total discounted investment cost (US$); load shedding (MW); convergence iteration.
- **Expected outcome**: low total cost, ranks near the top (second to HGA), with 0.00 MW load shedding.
- **Baselines**: HGA [68], DEA [58], CGA [67], EGA [23].
- **Dependencies**: E03, E04

## E09: Stability analysis on all TNEP case studies (SR%, MIT, MST)
- **Verifies**: C05
- **Evidence**: evidence/tables/table20.md, table21.md
- **Run**: COA, FDBCOA1, FDBCOA1-OBL5, GA, PSO on seven TNEP case studies.
- **Setup**:
  - Model: 5 algorithms (COA, FDBCOA1, FDBCOA1-OBL5, GA, PSO)
  - System: seven case studies (Garver ±resizing, IEEE-25 ±resizing, Colombian P1/P2/P3)
  - Runs: 30 independent runs per case study
- **Procedure**:
  1. For each algorithm/case study, run 30 times.
  2. Record whether each run reaches a feasible solution.
  3. Compute SR% (Eq. 39), MIT (Eq. 40), MST (Eq. 41); also min/mean/max/median/std of cost.
- **Metrics**: SR% (feasibility rate), MIT (iterations), MST (time); cost distribution statistics.
- **Expected outcome**: FDBCOA1-OBL5 has the highest mean SR% (feasible in all/most cases), far above COA/FDBCOA1/GA/PSO which are often near-zero.
- **Baselines**: COA, FDBCOA1, GA, PSO.
- **Dependencies**: E06, E07, E08
