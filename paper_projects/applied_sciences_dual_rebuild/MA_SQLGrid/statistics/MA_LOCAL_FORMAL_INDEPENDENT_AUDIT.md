# MA-SQLGrid Local Formal Run — Independent Audit

**Decision: PASS — eligible for canonical statistical use.**

## Run boundary

- Eligible input only: `paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\formal_run\qwen25coder7b_q4km_seed20260805_clean_rerun1`.
- Explicitly rejected/quarantined: `formal_run/qwen25coder7b_q4km_seed20260805`; incident status `quarantined_not_eligible_for_claim_promotion`. No artifact inside that directory was read by this audit.
- Clean manifest: `completed`; started 2026-08-05T07:28:51.294625Z, finished 2026-08-05T07:33:48.927872Z.

## Integrity and independent recomputation

- 720 prompts, 720 predictions, and 720 scores; exactly 720 unique database/question/cell identities and a complete 180 × 4 Cartesian product.
- Server accounting: 720 launches, 720 completed timings, 720 unique generation task IDs—one generation per final row.
- Provider/parse/scoring errors: 0/0/0; retries: 0. All predicted SQL passed the independent single-statement read-only SELECT guard.
- Direct SQLite recomputation matched archived execution and answer-shape verdicts for all 720 rows (0 mismatches).
- Configuration, data, code, local-model, prompt-set, prompt/context/response linkage, and freeze hashes all match.
- Gold isolation passed: prompt records contain no gold fields and no prompt/context contains its question's exact gold SQL.

## Recomputed cell results

| Cell | Execution correct/180 | Execution accuracy | Shape correct/180 | Shape accuracy |
|---|---:|---:|---:|---:|
| F00_Full_NoShape | 76 | 0.4222 | 90 | 0.5000 |
| F01_Full_WithShape | 129 | 0.7167 | 174 | 0.9667 |
| F10_Compact_NoShape | 78 | 0.4333 | 79 | 0.4389 |
| F11_Compact_WithShape | 108 | 0.6000 | 173 | 0.9611 |

## Registered paired edge contrasts

Holm adjustment spans the eight registered edge tests (four 2×2 edges × execution/shape). CIs use 20,000 paired cluster bootstrap draws over 70 normalized gold-SQL template clusters.

| Contrast | Metric | Delta | 95% cluster CI | McNemar discordance (base-only/treat-only) | Exact p | Holm p |
|---|---|---:|---|---:|---:|---:|
| shape_at_full | correct_int | +0.2944 | [+0.1318, +0.4902] | 3/56 | 1.18933e-13 | 7.13596e-13 |
| shape_at_full | shape_int | +0.4667 | [+0.2323, +0.6710] | 2/86 | 2.5313e-23 | 1.77191e-22 |
| compact_at_no_shape | correct_int | +0.0111 | [-0.0101, +0.0373] | 1/3 | 0.625 | 1 |
| compact_at_no_shape | shape_int | -0.0611 | [-0.1691, +0.0059] | 14/3 | 0.0127258 | 0.0381775 |
| shape_at_compact | correct_int | +0.1667 | [-0.0405, +0.3869] | 13/43 | 7.33322e-05 | 0.000366661 |
| shape_at_compact | shape_int | +0.5222 | [+0.2970, +0.7165] | 2/96 | 3.06204e-26 | 2.44963e-25 |
| compact_at_with_shape | correct_int | -0.1167 | [-0.2339, -0.0208] | 25/4 | 0.000103716 | 0.000414863 |
| compact_at_with_shape | shape_int | -0.0056 | [-0.0340, +0.0195] | 3/2 | 1 | 1 |

## Factorial effects

Effects are paired per question. Positive context main effect favors compact; positive shape main effect favors hints; interaction is (shape effect under compact) − (shape effect under full).

| Metric | Effect | Estimate | 95% template-cluster CI |
|---|---|---:|---|
| correct_int | context_compact_main | -0.0528 | [-0.1136, +0.0000] |
| correct_int | shape_hint_main | +0.2306 | [+0.0538, +0.4306] |
| correct_int | interaction | -0.1278 | [-0.2449, -0.0339] |
| shape_int | context_compact_main | -0.0333 | [-0.0906, +0.0037] |
| shape_int | shape_hint_main | +0.4944 | [+0.2662, +0.6912] |
| shape_int | interaction | +0.0556 | [-0.0149, +0.1646] |

## Canonical artifacts

- `MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json` — check-level audit evidence and canonical statistics.
- `canonical_recomputed_rows.jsonl` — independently recomputed binary outcomes and provenance hashes.
- `shared_stat_audit_clean.json/.md` — direct output of the shared statistical audit engine.
- `table_cell_summary.csv`, `table_registered_contrasts.csv`, `table_factorial_effects.csv` — canonical tabulations.

- `canonical_artifact_manifest.json` — hashes and byte sizes for every canonical audit output.

This audit establishes integrity and local paired effects for the frozen single-database run. It does not establish cross-database or cross-model generalization.
