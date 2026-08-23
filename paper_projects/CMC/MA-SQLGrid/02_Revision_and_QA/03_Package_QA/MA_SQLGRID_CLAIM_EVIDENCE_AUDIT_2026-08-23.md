# MA-SQLGrid claim--evidence audit

Date: 2026-08-23
Scope: current `01_Manuscript/LaTeX/paper_applsci.tex` and the post-review unified-evaluator artifacts.

| Claim family | Current treatment | Evidence | Verdict |
|---|---|---|---|
| multi-agent advantage | No causal/end-to-end advantage claimed | Historical pool makes zero model calls; roles are traced and deterministic components disclosed | PASS with route-A boundary |
| historical-pool counts | 76 C000, 99 validation, 100 complete, 129 best fixed source | One shape-and-denotation evaluator, 1,620 bounded executions, 1,440 fixed-slot outcomes | PASS |
| 76 versus historical 80 | Same normalized C000 artifacts; evaluator-policy drift | Four empty-result cases Q104/Q107/Q110/Q140 fail the expected-column gate | PASS |
| candidate-order stability | Explicitly reported as unresolved | Exact all 40,320 orders; both selectors range 95--128; 130/180 top ties | PASS as negative diagnostic |
| unique-SQL ambiguity | Duplicate slots disclosed | 154/180 pools contain a duplicate normalized SQL; mean 5.322 unique strings | PASS as post-run diagnostic |
| risk/abstention | No calibrated confidence claim | Strict no-tie covers 50/180 and gets 24 correct; descriptive AURC 0.4826/0.4795 | PASS with non-calibration boundary |
| five-role utilization | Recorded-only/active paths distinguished | Schema Cartographer does not feed historical selector; query features/order and witness eligibility ablations reported | PASS as implementation audit, not causal role efficacy |
| failure semantics | Automated execution/shape/denotation categories only | 1,980 method-item rows; `expert_semantic_adjudication=false` | PASS with expert gate open |
| robustness | Restricted to mutation denial, bounded execution, complete-evidence gating, deterministic failure behavior, and observed order response | 35 portable tests plus frozen ledgers | PASS under stated tested conditions |
| power-grid semantic validity | Not generalized beyond one synthetic case | No untouched external grid database or dual-expert adjudication | PASS as limitation; external gate open |
| BIRD portability | Explicitly non-grid | Eight method cells over 500 Mini-Dev items | PASS with domain boundary |

Residual prohibitions:

- Do not restore 80/100/101 as current evaluator results.
- Do not describe 99/100 as outperforming fixed strategies; Qwen F01 is 129/180.
- Do not select the exact best candidate order after inspecting outcomes.
- Do not present role ablations as an unseen, call-matched end-to-end agent experiment.
- Do not treat execution equality or constructed-state agreement as qualified business-semantic correctness.
