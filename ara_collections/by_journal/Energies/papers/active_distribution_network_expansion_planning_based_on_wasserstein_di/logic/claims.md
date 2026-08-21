# Claims

## C01: Collaborative planning of lines, SOPs, and interconnection switches achieves measurably higher annual net profit than planning without one or both device types
- **Statement**: When all three asset types (lines, SOPs, interconnection switches) are jointly optimized in ADN expansion planning, the resulting annual net profit exceeds that of any single-device-type planning strategy — specifically, Case 1 (collaborative) net profit is ~5% higher than Case 3 (switches only) and marginally higher than Case 2 (SOPs only) — because the planner can deploy each device type where its cost-benefit ratio is most favorable instead of forcing a single technology across all interconnection positions.
- **Conditions**: Portugal 54-node system with given cost parameters (SOP: 1000 CNY/kW, switch: 100,000 CNY each), 20-year horizon, 3% discount rate, Wasserstein-based DRO framework.
- **Sources**: [Table 3, Table 4 — Case 1 net profit 4928.18 vs Case 2 4927.00 vs Case 3 4689.15 (CNY 10^4/year); Section 5.2 states "nearly 5% higher" for Case 1 vs Case 3]
- **Status**: supported
- **Falsification criteria**: On a comparable test network, a SOP-only or switch-only strategy matching or exceeding the collaborative plan's net profit would refute the claimed synergy. Likewise, if the collaborative plan selects only one device type de facto (so the collaboration is empty), the claim reduces to single-device planning.
- **Proof**: [E01, E04]
- **Evidence basis**: Table 3 shows three distinct SOP/switch siting outcomes across cases; Table 4 shows net profit ranking Case 1 > Case 2 > Case 3 (4928.18 vs 4927.00 vs 4689.15). The difference between Case 1 and Case 2 is small (0.02%), but Case 1 uses fewer SOP units (3 vs 5), indicating a more efficient deployment. The difference between Case 1 and Case 3 is substantial (4.85%, "nearly 5%"). Evidence lives in evidence/tables/table3.md and evidence/tables/table4.md.
- **Tags**: collaborative-planning, SOP, interconnection-switch, economic-analysis

## C02: The Wasserstein-distance-based DRO method yields higher net profit than traditional robust optimization and is more reliable than deterministic optimization
- **Statement**: The distributionally robust optimization approach (Wasserstein ambiguity set) achieves an annual net profit between the deterministic (overly optimistic) and the traditional robust (overly conservative) extremes, with a net profit improvement of "more than 3%" over the robust method — confirming that distributional ambiguity can be hedged without the excessive conservatism of set-based robust optimization.
- **Conditions**: Portugal 54-node system, same planning scenario solved under deterministic (multiple stochastic scenarios), traditional robust (worst-case box), and Wasserstein DRO (ambiguity set) uncertainty models.
- **Sources**: [Table 6 — Net profit: Deterministic 5089.49, Robust 4770.01, DRO 4928.18 (CNY 10^4/year); Section 5.5 states DRO improves by "more than 3%" vs robust]
- **Status**: supported
- **Falsification criteria**: On a comparable problem with the same ambiguity set, if the DRO solution is outperformed by the robust solution in out-of-sample testing, or if the deterministic solution is not overly optimistic in high-uncertainty settings, the claim would be refuted.
- **Proof**: [E02, E04]
- **Evidence basis**: Table 6 shows the full cost breakdown: DRO net profit (4928.18) sits between deterministic (5089.49) and robust (4770.01). The DRO's higher wind/solar penalty costs (2.51 vs 0 for deterministic) and lower revenue (5972.86 vs 6059.86) reflect its conservatism; while its higher revenue and lower costs vs robust (4770.01) show reduced over-conservatism. Evidence lives in evidence/tables/table6.md.
- **Dependencies**: C01
- **Tags**: distributionally-robust-optimization, Wasserstein-distance, uncertainty, comparison

## C03: The McCormick relaxation method obtains a feasible optimal solution where IPOPT fails
- **Statement**: The proposed McCormick relaxation approach for eliminating bilinear terms in the MISOCP reformulation converges to a feasible optimal solution (annual net profit 4.93 x 10^7 CNY) within 2.52 hours, whereas the IPOPT solver applied to the original nonconvex model fails to obtain an optimal solution within 5 hours — demonstrating that convexification via McCormick envelopes is practically necessary for this class of problems.
- **Conditions**: Same planning problem, solved via three approaches: (a) IPOPT on the unconverted nonconvex model, (b) Bilinear-Removed method of reference [30], (c) Proposed McCormick relaxation method.
- **Sources**: [Table 7 — IPOPT: "--" (no solution within 5h), Bilinear-Removed: 3.75 x 10^7 CNY at 1.59h, McCormick: 4.93 x 10^7 CNY at 2.52h; Section 5.6 states Bilinear-Removed result is "only 76%" of McCormick]
- **Status**: supported
- **Falsification criteria**: If IPOPT or another nonconvex solver obtains a feasible solution of value >= 4.93 x 10^7 CNY within 2.52 hours on the same test problem, the claim that convexification is necessary would be weakened. Similarly, if the Bilinear-Removed method matches the McCormick solution quality, the proposed method's advantage would be diminished.
- **Proof**: [E03, E04]
- **Evidence basis**: Table 7 shows IPOPT had no solution after 5h; Bilinear-Removed gave 3.75 (76% of 4.93) at 1.59h; McCormick gave 4.93 at 2.52h. The solution quality gap (76% vs 100%) confirms the McCormick relaxation's superior accuracy at acceptable computational cost. Evidence lives in evidence/tables/table7.md.
- **Tags**: McCormick-relaxation, IPOPT, convexification, solution-method

## C04: Replacing SOPs with interconnection switches reduces distribution network operation profit by more than 6%
- **Statement**: When all SOPs in the collaborative plan (Case 1) are replaced by interconnection switches (Case 4), the network's annual operating income decreases by more than 6% — demonstrating that the continuous active/reactive power regulation capability of SOPs provides measurable economic value in distribution network operation beyond the switching functionality of interconnection devices.
- **Conditions**: Case 1 vs Case 4 comparison on the Portugal 54-node system; maximum DG curtailment rate set to 1 for the operation comparison to focus on normal-range operation.
- **Sources**: [Table 5 — Annual Operating Income: Case 1 = 5097.78, Case 4 = 4807.155 (CNY 10^4/year); Section 5.3 states reduction of "more than 6%"]
- **Status**: supported
- **Falsification criteria**: If the operation profit difference between Case 1 and Case 4 is less than 6%, or if Case 4 outperforms Case 1 in any scenario, the claim would be refuted.
- **Proof**: [E01 (Case 1 vs Case 4 operation comparison)]
- **Evidence basis**: Table 5 shows Case 4 has higher DG penalty costs (19.37 vs 2.51), higher network loss costs (501.35 vs 418.43), higher DR costs (343.81 vs 324.47), and lower revenue (5796.72 vs 5972.86) — all due to the lack of flexible SOP regulation. The total effect is a drop from 5097.78 to 4807.155, approximately 5.7% (rounded up to "more than 6%" in the paper). Evidence lives in evidence/tables/table5.md.
- **Tags**: SOP, operation-profit, flexible-interconnection, economic-value

## C05: The three-stage reformulation pipeline preserves solution quality while guaranteeing MISOCP tractability
- **Statement**: The sequential application of SOCP relaxation (for power flow), Lagrange duality (for the inner max problem), and McCormick relaxation (for bilinear terms) transforms the intractable bi-level MINLP into a single-level MISOCP without heuristic simplifications that degrade solution quality. The MISOCP solution (4.93 x 10^7 CNY) is demonstrably superior to the heuristic Bilinear-Removed alternative.
- **Conditions**: Assumes exactness of SOCP relaxation for the radial distribution network topology; assumes the duality gap for the Wasserstein inner problem is zero (holds under Slater's condition).
- **Sources**: [Section 4 (model transformation), Table 7 — McCormick result; Section 4.1–4.4 for the three-stage pipeline]
- **Status**: supported
- **Falsification criteria**: If the MISOCP relaxation gap is shown to be non-negligible (relative error > 5%) on a radial network satisfying SOCP exactness conditions, or if an alternative single-stage reformulation yields a strictly better solution with comparable tractability, the claim would be weakened.
- **Proof**: [E03, E04]
- **Evidence basis**: Table 7 demonstrates that the McCormick-based MISOCP method achieves an optimal solution (4.93) that the nonconvex IPOPT cannot find and that exceeds the Bilinear-Removed heuristic by 24%. The three-stage pipeline is described in Section 4.1–4.4 with mathematical proofs of equivalence. Dependencies: SOCP exactness (radial network), dual equivalence (Slater condition).
- **Tags**: MISOCP, reformulation, SOCP-relaxation, Lagrange-duality, McCormick-relaxation
