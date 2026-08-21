# C²GES R2 Staging Evidence Registry

This registry is the source boundary for `MANUSCRIPT_R2_STAGING.md`. It deliberately excludes formal test outputs because none has been authorized or audited at the time of drafting.

| Evidence | Path | SHA-256 / state | Manuscript use |
|---|---|---|---|
| Full-PDF builder | `original_title_rebuild/R2_v0_3/build_full_pdf_dataset.py` | `817518DF...AA38` | Candidate construction |
| Build08 complete dataset | `R2_v0_3/diagnostic_build_08/nerc_full_pdf_benchmark_v0_3.jsonl` | `87F7F754...AA15` | Counts only; not redistributed |
| Build08 development set | `R2_v0_3/diagnostic_build_08/nerc_full_pdf_dev_v0_3.jsonl` | `27CE41D3...7F79` | Development selection |
| Build08 test set | `R2_v0_3/diagnostic_build_08/nerc_full_pdf_test_v0_3.jsonl` | `A9342BD7...D127` | **Not read by staging task** |
| Independent Stage-1 re-audit | `R2_v0_3/INDEPENDENT_STAGE1_REAUDIT_08.md` | `C5E8B61B...D974` | Dataset/audit claims |
| Dev decision | `R2_v0_3/dev_selection_run04/DEV_SELECTION_DECISION.json` | `EEBD0D0A...FE3` | Frozen weights and dev evidence |
| Dev search ledger | `R2_v0_3/dev_selection_run04/dev_search_ledger.jsonl` | `19A3D17C...14B` | 144-grid provenance |
| CF identifiability note | `R2_v0_3/CF_IDENTIFIABILITY_NOTE.md` | Bound in predecessor/successor history | Mathematical interpretation |
| v0.3 pre-test freeze | `R2_v0_3/TEST_FREEZE_MANIFEST_v0_3.json` | `F70387B4...25BAE` | Retained FAIL predecessor only |
| Independent v0.3 pre-test audit | `R2_v0_3/INDEPENDENT_PRETEST_AUDIT_v0_3.md` | `2ADA2B71...DECF` | B1–B5 findings; test not run |
| v0.3.1 repair response | `R2_v0_3/PRETEST_REPAIR_RESPONSE.md` | `6B1D6812...82D9` | Repair claims |
| v0.3.1 dependency lock | `R2_v0_3/OUTPUT_DEPENDENCY_LOCK_v0_3_1.json` | `E36FF278...A10` | Runtime closure |
| v0.3.1 formal config | `R2_v0_3/formal_config_v0_3_1.json` | `C9240352...F14C` | Conditions/statistics |
| v0.3.1 freeze manifest | `R2_v0_3/TEST_FREEZE_MANIFEST_v0_3_1.json` | `DE3205B0...19B5` | Passed pre-test audit |
| v0.3.1 pre-test audit | `R2_v0_3/INDEPENDENT_PRETEST_AUDIT_v0_3_1.md` | `AEE22F61...A048`; PASS | Test content not reviewed; run not executed by auditor |
| v0.3.1 pre-test decision | `R2_v0_3/INDEPENDENT_PRETEST_DECISION_v0_3_1.json` | `5D9C5E9D...A894`; PASS | Exact freeze binding |
| v0.3.1 authorization | `R2_v0_3/FORMAL_TEST_AUTHORIZATION_v0_3_1.json` | `BB9DDE1C...C2C` | Exact run/output authorization |
| Formal run state | `R2_v0_3/formal_runs_v0_3_1/c2ges_v031_formal_20260808/run_state.json` | `COMPLETE` | Numerical outputs quarantined pending post-run audit |

## Prohibited Evidence Substitutions

- v0.1 and v0.2 aggregate results, predictions, figures, and bootstrap intervals are corrective-history artifacts and cannot populate R2 Results.
- The v0.3 predecessor freeze failed independent audit and was never authorized; it cannot be executed or represented as v0.3.1.
- Development results cannot be relabeled as test results.
- An SVG placeholder cannot be represented as empirical evidence.
- LLM output cannot be represented as qualified-expert annotation or adjudication.
- A public URL cannot be represented as redistribution permission.
