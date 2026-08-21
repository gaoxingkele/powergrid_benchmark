# Experiments

## E01: AHP weight derivation and consistency verification
- **Verifies**: C01
- **Evidence**: evidence/tables/table1.md, evidence/tables/table2.md, evidence/tables/table3.md
- **Run**: Analytical AHP procedure (§2.2); pairwise matrix construction + column-sum normalization + row-mean weight extraction + consistency check. No external code artifact; computed by the authors.
- **Setup**:
  - Model: AHP multi-criteria weighting over the five criticality indices
  - Hardware: n/a (analytical)
  - Dataset: expert pairwise comparison judgments (Santy scale)
  - System: objective/criteria/alternative hierarchy
- **Procedure**:
  1. Elicit pairwise importance of the five indices using the Santy 1–9 scale (Table 1).
  2. Assemble the 5×5 comparison matrix (Table 2).
  3. Normalize columns, average rows to obtain criterion weights (Table 3).
  4. Compute the consistency ratio and compare against the acceptance threshold.
- **Metrics**: Criterion weights (dimensionless); consistency ratio (dimensionless).
- **Expected outcome**:
  - The load-level criterion receives the largest weight; the low-voltage-grid-influence (10 kV line count) criterion receives the smallest.
  - Consistency ratio falls well below the acceptance threshold, validating the judgments.
- **Baselines**: none (weighting internal to the method).
- **Dependencies**: none

## E02: Criticality scoring of the six new 110 kV substations
- **Verifies**: C01
- **Evidence**: evidence/tables/table4.md, evidence/tables/table5.md
- **Run**: Apply Eqs. 1–7 to the 2020 baseline configuration (§4.2); indices computed from topology/load, sum-normalized, combined with E01 weights.
- **Setup**:
  - Model: composite importance score (Eq. 6) with sum normalization (Eq. 7)
  - Hardware: n/a (analytical)
  - Dataset: 2020 baseline regional grid — six new 110 kV substations, their served load, 10 kV feeder counts/lengths, coverage
  - System: 220/110/10 kV regional network
- **Procedure**:
  1. Compute the five raw indices per substation (Table 4).
  2. Sum-normalize each index across the six substations (Eq. 7).
  3. Weight and sum to produce each substation's importance score (Table 5).
  4. Rank substations; select highest- and lowest-scored for downstream delay analysis.
- **Metrics**: Per-substation raw indices (MW, count, km); composite importance score (dimensionless).
- **Expected outcome**:
  - Scores separate the six substations into higher- and lower-criticality; the highest-load / high-density substation ranks top and a low-connectivity, low-density one ranks bottom.
- **Baselines**: none.
- **Dependencies**: E01

## E03: Baseline multi-voltage grid evolution simulation (on-schedule plan)
- **Verifies**: C04
- **Evidence**: evidence/figures/figure3.md, evidence/figures/figure4.md, evidence/tables/table6.md
- **Run**: Genetic-algorithm-solved evolution model (Eqs. 8–25); all six substations commissioned on schedule; rolling optimization for 2025 and 2035 from the 2020 topology.
- **Setup**:
  - Model: multi-voltage evolution model, GA solver (max gen 200, pop 800, crossover 0.5, mutation 0.5)
  - Hardware: Not specified in paper
  - Dataset: regional grid — 220 equivalent load nodes; 2020 base demand; 2025/2035 load forecasts; discount rate 8%
  - System: co-planned 220/110/10 kV network; loading factor 75%, 10 kV feeder 552 A, 110 kV line 718 A limits
- **Procedure**:
  1. Initialize with the 2020 network topology (Figure 4a,b).
  2. Roll the evolution forward to 2025 then 2035, minimizing per-horizon total cost subject to all constraints.
  3. Record per-layer construction/operating cost by year as the baseline (Table 6, "Original planning program").
- **Metrics**: Per-layer and converted-total construction+operating cost per horizon (million CNY).
- **Expected outcome**:
  - A feasible on-schedule expansion trajectory whose per-layer costs serve as the reference for differencing delay scenarios.
- **Baselines**: this run *is* the baseline for E04/E05.
- **Dependencies**: none

## E04: Paired delay experiment — high-criticality (No. 1) vs low-criticality (No. 6)
- **Verifies**: C03, C04, C05
- **Evidence**: evidence/figures/figure5.md, evidence/figures/figure6.md, evidence/tables/table6.md
- **Run**: Re-run the evolution model with commissioning of substation No. 1 (then No. 6) postponed from 2020 to 2025; difference against the E03 baseline.
- **Setup**:
  - Model / Hardware / System: as E03
  - Dataset: same regional grid; delay applied to one substation at a time
- **Procedure**:
  1. Postpone substation No. 1's commissioning to 2025; run evolution to 2025 and 2035 (Figure 5).
  2. Repeat with substation No. 6 postponed (Figure 6).
  3. Discount annual investments (8%) to the initial year; tabulate per-layer costs and total incremental cost vs baseline (Table 6).
  4. Compare which voltage layer absorbs the incremental cost and how it evolves over horizons.
- **Metrics**: Per-layer cost by year; total incremental cost relative to baseline (%).
- **Expected outcome**:
  - Delaying the high-criticality substation yields a larger incremental cost than delaying the low-criticality one.
  - The incremental cost concentrates in the 10 kV layer and persists to 2035; the high-density-area delay drives more feeder construction than the low-density-area delay.
- **Baselines**: E03 on-schedule plan.
- **Dependencies**: E02, E03

## E05: Six-substation individual-deferral sweep and score–cost regression
- **Verifies**: C02, C03
- **Evidence**: evidence/tables/table7.md, evidence/figures/figure7.md
- **Run**: Defer each of the six substations individually by one horizon; collect total cost to 2035 and incremental cost; regress incremental cost on importance score.
- **Setup**:
  - Model / Hardware / System: as E03
  - Dataset: six delay scenarios (one per substation) + baseline
- **Procedure**:
  1. For each substation, postpone its commissioning to the next horizon and run the evolution model to 2035.
  2. Record total cumulative cost and incremental cost vs baseline (Table 7).
  3. Pair each substation's E02 importance score with its incremental cost; fit a linear regression (Figure 7).
  4. Assess the strength/direction of the score–cost relationship.
- **Metrics**: Total cost to 2035 (million CNY); incremental cost (%); importance score (dimensionless); regression fit.
- **Expected outcome**:
  - A strong positive, approximately linear association between importance score and incremental cost, cross-validating the static score against the dynamic simulation.
- **Baselines**: E03 on-schedule plan.
- **Dependencies**: E02, E03
