# MA-SQLGrid v5 Post-Score Independent Audit A

## Decision

**PASS_INTEGRATION**

The formal v5 score, frozen analysis, and release manifest are internally consistent and independently reproducible from `atomic_scores.jsonl` plus the frozen inputs. This audit was read-only: it did not run the scorer, modify results, or reuse the released analysis functions to derive its verdict.

## Independent recomputation

- Atomic score rows: **25,920/25,920**, with **25,920 unique** `(backbone, condition, question, state)` keys.
- Corpus: **180 questions**, two backbones, four conditions, and 18 states. Every state contributes exactly **1,440** atomic rows.
- State partition: **15 semantic states** and **3 insertion-order diagnostic states**, disjoint and flag-consistent. Physical diagnostic states never enter the primary suite.
- Primary partition: **66 eligible questions** and **114 order-hold questions**, with zero overlap. This yields **528 primary predictions**, **912 held predictions**, **7,920 primary semantic-state rows**, and **16,416 all-state hold rows**.
- Gold execution: zero failures. No strict agreement is true when tolerant agreement is false.
- T0 snapshot: the **1,440/1,440** atomic outcomes match the canonical-v2 execution labels; mismatches: **0**.
- Suite aggregation: the independently reconstructed **1,440** prediction-level objects exactly equal `formal_v5_analysis/suite_outcomes.jsonl`.
- Frozen inputs: all **35/35** file identities match their frozen byte counts and SHA-256 values.
- Release manifest: all **9/9** artifacts exist and match both recorded bytes and SHA-256. The repository verifier also reports `RELEASE_V3_VERIFY PASS`.

## Primary 15-state suite outcomes

| Backbone | Condition | Pass / 66 | Rate | Strict pass / 66 | Eligible T0 pass / 66 |
|---|---|---:|---:|---:|---:|
| Granite | F00 Full, no shape | 54 | 81.82% | 54 | 62 |
| Granite | F01 Full, shape | 41 | 62.12% | 41 | 47 |
| Granite | F10 Compact, no shape | 51 | 77.27% | 51 | 64 |
| Granite | F11 Compact, shape | 49 | 74.24% | 49 | 62 |
| Qwen | F00 Full, no shape | 49 | 74.24% | 49 | 65 |
| Qwen | F01 Full, shape | 48 | 72.73% | 48 | 64 |
| Qwen | F10 Compact, no shape | 53 | 80.30% | 53 | 64 |
| Qwen | F11 Compact, shape | 43 | 65.15% | 43 | 54 |

The strict and tolerant 15-state pass counts happen to coincide in all eight cells. This is a result, not a change in the frozen comparison policy.

## Contrasts and clustered inference

I independently rebuilt the four-cell effect vectors for each backbone and the Granite-minus-Qwen modifiers, then reran the frozen two-sided cluster sign-flip and cluster bootstrap procedures with the declared deterministic seeds. All nine estimates, interval bounds, raw p-values, and Holm-adjusted p-values reproduce the released CSV to absolute tolerance `1e-15`.

| Family | Contrast | Estimate | Composition-sensitivity interval | Raw p | Holm p |
|---:|---|---:|---:|---:|---:|
| 1 | Qwen hint | -0.0833 | [-0.2476, 0.0606] | 0.7509 | 1.0000 |
| 2 | Qwen compact | -0.0076 | [-0.2500, 0.3976] | 1.0000 | 1.0000 |
| 3 | Qwen interaction | -0.1364 | [-0.4643, 0.1707] | 1.0000 | 1.0000 |
| 4 | Granite hint | -0.1136 | [-0.2532, 0.0000] | 0.5005 | 1.0000 |
| 5 | Granite compact | 0.0379 | [-0.1622, 0.1930] | 1.0000 | 1.0000 |
| 6 | Granite interaction | 0.1667 | [0.0000, 0.4151] | 1.0000 | 1.0000 |
| 7 | Granite-Qwen hint | -0.0303 | [-0.0833, 0.0217] | 0.4980 | 1.0000 |
| 8 | Granite-Qwen compact | 0.0455 | [-0.5526, 0.4464] | 0.6237 | 1.0000 |
| 9 | Granite-Qwen interaction | 0.3030 | [-0.1714, 0.8780] | 1.0000 | 1.0000 |

The settings are **100,000** cluster sign-flip samples, **20,000** cluster-bootstrap samples, and a **9-test Holm family**. The frozen map has 70 clusters over all 180 questions; the eligible 66-question primary subset occupies **12 clusters**, correctly reported by every contrast row. All adjusted p-values are 1.0, so no contrast supports a statistical-significance claim.

## Integration boundaries and nonblocking metadata notes

- Describe the intervals as frozen **composition-sensitivity intervals**, not population confidence intervals.
- The `seed` column in `clustered_contrasts.csv` stores base seed 20260805. Exact reproduction uses family-specific offsets: sign-flip `base + 1000 + i` and bootstrap `base + 10000 + i`, with zero-based family index `i`.
- For eligible rows, `adjudication_class` records execution status (`automatic` or `execution_error_hold`); it is not the denominator authority. Eligibility is defined by `automatic_primary_eligible`, and execution errors remain failures in the declared denominator.
- The 114 order-sensitive questions remain diagnostic holdouts. Do not pool their all-18-state outcomes into the 66-question primary claim.
- The evidence is a retrospective automated multi-state gold-SQL agreement stress test, not a human semantic audit.

## Audited SHA-256 identities

| File | SHA-256 |
|---|---|
| `formal_v5_results/atomic_scores.jsonl` | `89c0ede848b4487a1edadb2fd771dabaf21a16c8359d7000ad9955c3196968cd` |
| `formal_v5_results/RUN_SUMMARY.json` | `b1eb15cc528d8b0a6318fcb0e8ca3513d46e4e9147f06ff2580074f76154c0e1` |
| `PROTOCOL_FREEZE_V5_DRAFT.json` | `cccd903bd7f3309f50fae4a5d7084b1f272b094ef0afd42467287a51b376e898` |
| `canonical_rows_v2.jsonl` | `a290770448219ecb81b01db61e3a789c4101f5cc38bf342bd34e2931fc7e10f9` |
| `formal_v5_analysis/suite_outcomes.jsonl` | `65d37b0801b780ea07b767bfcc46a5c9b7278046a4362ebb0562a69fae5df07b` |
| `formal_v5_analysis/suite_outcomes.csv` | `322bb787184f9798bd8821ec54dc31f6573ca62fb364a703e275ba1020e1dabe` |
| `formal_v5_analysis/clustered_contrasts.csv` | `14c2c3671fb7c31ebe249fb9cdb85d504bb5effea2a166af8c343ab0dfe9f15b` |
| `formal_v5_analysis/ANALYSIS_SUMMARY.json` | `9f060883528da90e79a4e152373b0207df80ffe9b5f6e3e6e2c3f6c7b0414dab` |
| `formal_v5_release/release_manifest.json` | `6eac92a3743b39dceba2b59737d1546397e1e716274b3bc789c60cb13cd2a5df` |

