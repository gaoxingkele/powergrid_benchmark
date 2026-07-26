# Claims

Claim system rewritten 2026-07-14 under "Route A" (claim downgrade after the v7 10-seed significance verdict). The method's working name before v7 was `HyG-LoadFormer`; evidence CSVs retain that historical name (rows such as `HyG-LoadFormer (neural)`), which maps to `CSA-LoadNet` in the manuscript. The pre-v7 claim table (C1-C4, stdlib-baseline era) is superseded; its evidence files remain preserved.

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 (main) | `CSA-LoadNet` significantly outperforms the strongest external neural baseline (MLP) on OPSD day-ahead 24h multi-region load forecasting. | Supported, 10 seeds, Mann-Whitney U + Holm, p_holm=0.00853125 | E-real-OPSD v7; `evidence/runs/real_p2_v7_significance_analysis.md`; `evidence/tables/real_p2_v7_significance.csv`; proposed mean MAPE `0.032345` vs MLP `0.03371542` |
| C2 (component) | The cross-series aggregation component contributes significantly: the full model beats the TemporalOnly (no-aggregation) ablation on OPSD 24h. | Supported, 10 seeds, p_holm=0.00109603 | E-real-OPSD v7; proposed mean MAPE `0.032345` vs TemporalOnly `0.03459125` |
| C3 (honest negative finding) | The specific form of the aggregation weights — hyperbolic (Poincare-ball) distance vs Euclidean distance vs equal-weight neighbors vs fixed curvature — is statistically inseparable in all five tested dataset/horizon settings (OPSD 1h/24h, SimBench 1h/24h, Ausgrid 24h). Aggregation itself, not its geometry, is the source of the contribution. | Supported as a negative/inseparability result, 10 seeds, all pairwise p_holm ≈ 1 | E-real v7 significance tables, all five setting blocks in `real_p2_v7_significance_analysis.md` |
| C4 (reproducibility) | The experiment package is reproducible from public data under an identical protocol across v5/v6/v7, with the full evidence chain (including failed versions) preserved. | Supported structurally | `src/powergrid_benchmark/mintou_hyg_neural.py`; `src/powergrid_benchmark/mintou_hyg_significance.py`; `evidence/tables/real_{opsd,simbench}_combined_leaderboard.csv` |

## Non-claims and recorded limitations

- SimBench 1h/24h: statistically inseparable from MLP (1h mean slightly ahead, 24h mean slightly behind, p=0.084). Reported descriptively; no superiority claim.
- Ausgrid hierarchical 24h: `CSA-LoadNet` significantly loses to DLinear (p=0.0044) and is inseparable from MLP/TCN/PatchTST with worse mean trend. Recorded limitation.
- OPSD 1h: significantly loses to MLP (p_holm=0.0348). Recorded limitation.

## Prohibited claims (binding for the manuscript)

1. MUST NOT claim any advantage from hyperbolic geometry, learnable attention geometry, or adaptive curvature (contradicted by C3 evidence). The Poincare embedding may be described only as one weight-parameterization option retained in the implementation.
2. MUST NOT claim short-horizon (1h) advantage (contradicted on OPSD; inseparable on SimBench).
3. MUST NOT claim advantage in hierarchical (Ausgrid-type customer/region/system) scenarios (contradicted, p=0.0044 loss to DLinear).
4. MUST NOT use the "Smart Dispatch" narrative in title, abstract, or claims (dispatch_sensitivity has smoke-only evidence).

Exact numerical manuscript claims must be scoped to the evidence file used. All superiority language must be limited to day-ahead 24h OPSD multi-region forecasting with the 10-seed significance backing above.
