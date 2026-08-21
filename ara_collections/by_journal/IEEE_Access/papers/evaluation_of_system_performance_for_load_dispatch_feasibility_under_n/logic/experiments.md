# Experiments

Directional plans only; exact numbers live in `evidence/`. Experiments and claims are many-to-many.

## E01: Base Case DA UC cost benchmark (no contingency)
- **Verifies**: C01
- **Evidence**: evidence/tables/table4.md, evidence/figures/figure6.md
- **Run**: DP-based DA UC solved in MATLAB on the original IEEE RTS at forecasted load, 10% CM, no generator outage (§VII-A1).
- **Setup**:
  - Model: Day-ahead unit commitment, thermal generators only
  - Hardware: Not specified in paper
  - Dataset: 24-bus, 26-generator IEEE Reliability Test System (data in Table 2, Table 3; demand in Fig. 6)
  - System: Dynamic Programming optimizer, all constraints (Eq. 1–8)
- **Procedure**:
  1. Assemble generator data and forecasted 24-hour demand.
  2. Solve DA UC by DP with 10% spinning reserve, no contingencies.
  3. Record cumulative hourly UC cost across the 24 hours.
- **Metrics**: Cumulative DA UC cost ($) per hour and total.
- **Expected outcome**:
  - Produces a finite baseline cost with the system running smoothly (no infeasibility).
  - This baseline is the reference for cost comparison in Cases 1 and 2.
- **Baselines**: This is the baseline itself.
- **Dependencies**: none

## E02: Case 1 — N-1 generator contingency DA UC at 10% SR, criticality/robustness ranking
- **Verifies**: C01, C02, C03, C06, C07
- **Evidence**: evidence/tables/table5.md, evidence/tables/table6.md, evidence/figures/figure5.md, evidence/figures/figure7.md, evidence/figures/figure8.md
- **Run**: DP-based DA UC re-solved for each of the nine single-generator outages with CM = 10% SR (§IV-B Case 1, §VII-A2).
- **Setup**:
  - Model: DA UC under single-generator outage
  - Hardware: Not specified in paper
  - Dataset: IEEE RTS; nine contingencies indexed by ascending bus number (Fig. 5)
  - System: DP optimizer, 10% spinning reserve (CM 310.5 MW)
- **Procedure**:
  1. Simulate outage of one generator at a time.
  2. Re-run DA UC with constraints and 10% CM; compile cost per contingency.
  3. Compute percentage cost rise vs Base Case; classify stable vs critical contingencies; identify robust vs weak buses; rank weak buses by percentage rise (robust buses in reverse).
- **Metrics**: DA UC cost ($) per contingency, percentage cost variation (%), contingency rank.
- **Expected outcome**:
  - Largest-capacity outages (400 MW, buses 18/21) give the largest cost rise and top criticality rank; smallest give ~0% or slight decrease.
  - A subset of outages are cost-neutral/reducing (robust buses).
  - Supply-demand balance is maintained for all outages at this reserve.
- **Baselines**: Base Case cost (E01).
- **Dependencies**: E01

## E03: Post-outage available-capacity vs peak-demand feasibility check
- **Verifies**: C04, C06
- **Evidence**: evidence/tables/table7.md, evidence/tables/table8.md
- **Run**: Compilation of Capacity Outage Probability Tables (COPT) giving total capacity available after each single-unit outage per case (§VII-B1).
- **Setup**:
  - Model: Capacity-adequacy screening
  - Hardware: Not specified in paper
  - Dataset: IEEE RTS generator capacities; reserve settings 10%/8%/5%/0%
  - System: Post-outage available capacity = pre-outage dispatchable capacity − lost unit
- **Procedure**:
  1. For each contingency and each reserve level, compute total capacity available after generator outage.
  2. Compare against the peak forecasted demand.
  3. Flag contingencies whose post-outage capacity falls below demand.
- **Metrics**: Total capacity available after outage (MW); probability of generation unavailability.
- **Expected outcome**:
  - Only large-unit outages at specific buses drop below peak demand at higher reserve; reducing reserve raises available capacity for all.
- **Baselines**: Peak demand reference.
- **Dependencies**: E01, E02

## E04: LOLP reliability estimation across reserve levels
- **Verifies**: C04, C08
- **Evidence**: evidence/tables/table9.md, evidence/tables/table10.md
- **Run**: Hourly LOLP computed from the COPT for each hour and aggregated over 24 hours, for Case 1 and Case 2(a),(b),(c) (§VII-B2).
- **Setup**:
  - Model: Probabilistic reliability via LOLP
  - Hardware: Not specified in paper
  - Dataset: IEEE RTS hourly forecasted demand; per-capacity FR/MTTF (Table 3)
  - System: LOLP (Eq. 11–14) under single-unit-outage assumption
- **Procedure**:
  1. For each hour, evaluate probability that demand exceeds post-outage available generation.
  2. Aggregate hourly LOLP over 24 hours per case.
  3. Compare overall LOLP against LOLP_max = 0.05.
- **Metrics**: Hourly LOLP_t; overall 24-hour LOLP.
- **Expected outcome**:
  - Overall LOLP decreases monotonically as reserve is reduced from 10% to 0%; reaches zero at 0% reserve (full capacity dispatchable).
- **Baselines**: LOLP_max threshold.
- **Dependencies**: E03

## E05: Operating-margin evaluation and feasibility signal
- **Verifies**: C01, C04, C05, C08
- **Evidence**: evidence/tables/table11.md
- **Run**: Operating margin computed as LOLP_max − LOLP for each case (§VII-C, Eq. 15).
- **Setup**:
  - Model: Operating-margin metric
  - Hardware: Not specified in paper
  - Dataset: Aggregated LOLP per case (E04)
  - System: Fixed LOLP_max = 0.05
- **Procedure**:
  1. Take overall LOLP for each case.
  2. Subtract from LOLP_max to obtain operating margin.
  3. Interpret sign: non-positive → at-limit/infeasible; positive → headroom.
- **Metrics**: Operating margin $M_{da}^o$ (dimensionless probability).
- **Expected outcome**:
  - Margin rises as reserve is reduced; the highest-reserve case yields a non-positive/at-limit margin, lower-reserve cases yield positive margins.
- **Baselines**: Zero-margin threshold.
- **Dependencies**: E04

## E06: Case 2 — reserve sweep and cross-case invariance of criticality/robustness
- **Verifies**: C01, C05, C07
- **Evidence**: evidence/tables/table6.md, evidence/tables/table12.md, evidence/tables/table13.md, evidence/figures/figure9.md, evidence/figures/figure10.md
- **Run**: DA UC re-solved for each contingency at 8%, 5%, and 0% CM (Case 2a/2b/2c), with performance parameters assembled (§IV-B Case 2, §VII).
- **Setup**:
  - Model: DA UC under single-generator outage at reduced reserves
  - Hardware: Not specified in paper
  - Dataset: IEEE RTS; nine contingencies
  - System: DP optimizer at CM 248/155/0 MW
- **Procedure**:
  1. Repeat E02's per-contingency DA UC at each reduced reserve.
  2. Recompute percentage cost variation and contingency ranking.
  3. Compare critical/weak and stable/robust identities across cases.
- **Metrics**: DA UC cost ($) and percentage variation per contingency per reserve; criticality/robustness sets.
- **Expected outcome**:
  - Costs for 8%/5% CM match Case 1; 0% CM differs (lower for most contingencies).
  - Critical contingencies and weak buses (and stable/robust) remain the same across reserve levels, with a minor extension at 0% CM.
- **Baselines**: Case 1 results (E02).
- **Dependencies**: E02, E04

## E07: Integrated system-performance and feasibility assessment
- **Verifies**: C01
- **Evidence**: evidence/tables/table12.md, evidence/tables/table13.md
- **Run**: Assembly of criticality, robustness, reliability, and operating margin into a joint assessment of DA-UC performance and real-time dispatch feasibility with corrective actions (§VII-D, §VIII).
- **Setup**:
  - Model: Multi-metric decision assessment
  - Hardware: Not specified in paper
  - Dataset: Outputs of E02–E06
  - System: Qualitative + quantitative synthesis across four metrics
- **Procedure**:
  1. Collate the four performance parameters per case.
  2. Judge dispatch feasibility and withstanding capability per case.
  3. Recommend corrective actions (e.g., alternate generation at critical buses).
- **Metrics**: Composite qualitative ratings (feasibility, withstanding capability) plus the underlying quantitative metrics.
- **Expected outcome**:
  - The multi-metric view distinguishes cases that are cheap-but-fragile from cases with headroom, in a way cost alone does not.
- **Baselines**: Cost-only comparison.
- **Dependencies**: E02, E04, E05, E06
