# C²GES R1 → R2 Response Matrix

Status: R2 staging, 2026-08-08. One formal execution is complete, but its numerical evidence is quarantined pending independent post-run audit.  
Decision rule: an item is *closed* only when the manuscript change and its supporting artifact are both present. Test-dependent items remain `EVIDENCE_PENDING_TEST`.

## Methods and Statistics Reviewer

| ID | R1 concern | R2 action | Acceptance evidence | Status |
|---|---|---|---|---|
| M1 | The v0.2 node-deletion score was algebraically identical to weighted degree. | Retired v0.2 quantity. Defined the loss of qualified, stage-monotone 2–4 edge path strength under node deletion. Strict no-CF removes only the CF coefficient. | `R2_v0_3/CF_IDENTIFIABILITY_NOTE.md`; `counterfactual_paths_v031.py`; regression tests; Methods 3.5–3.6. | Closed for mathematical/software identifiability; efficacy pending |
| M2 | Executive Summary text contaminated candidates. | Rebuilt candidates from complete PDFs with fail-closed summary/body boundaries and page/sentence/substring leakage gates. | `diagnostic_build_08`; `INDEPENDENT_STAGE1_REAUDIT_08.md`; Methods 3.2–3.3. | Closed for build08 |
| M3 | NERC data do not validate maintenance-report performance or physical causality. | Kept exact title but added title-adjacent transfer boundary in Abstract, Introduction, Discussion, and Conclusion; graph is called a textual proxy and perturbation is not a causal effect. | Manuscript Abstract; Sections 1, 3.1, 5.2–5.3, 6. | Partly closed; title-concordant external validity remains unresolved |
| M4 | Primary family and outcome emphasis were inconsistent. | Registered ROUGE-L only, three contrasts at two budgets, one six-test Holm family; other analyses exploratory. | `formal_config_v0_3_1.json`; `TEST_FREEZE_MANIFEST_v0_3_1.json`; Methods 3.9. | Closed at design level; `EVIDENCE_PENDING_TEST` |
| M5 | No development-search ledger and weak semantic comparator. | Recorded 144-row dev grid and decision; replaced relevance-only semantic centroid with frozen MiniLM Semantic-MMR (lambda 0.5). | `dev_selection_run04`; `PRETEST_REPAIR_RESPONSE.md`; Methods 3.7–3.8. | Closed at design level |
| M6 | Series and near-duplicate split audit was absent. | Added series-aware grouping, report-level partition checks, and normalized leakage audit before test execution. | `INDEPENDENT_STAGE1_REAUDIT_08.md`; Methods 3.2–3.3. | Closed within registered checks |
| M7 | Architecture falsely separated identical degree/CF channels; result figure lacked paired uncertainty. | Redrew architecture after method redesign; formal-result scaffold requires report-level paired values and intervals. | `figures/fig01_c2ges_algorithm.svg`; `figures/fig04_results_pending.svg`. | Architecture closed; result figure pending |
| M8 | Captions/counts and layout were inaccurate. | Staging tables use exact six-test family and explicit evidence states; final float/page QA deferred to assembled PDF. | Results 4.3–4.4. | Partly closed; PDF QA pending |

## Power-Grid Application Reviewer

| ID | R1 concern | R2 action | Acceptance evidence | Status |
|---|---|---|---|---|
| W1 | Candidates were capped excerpts, not full PDF bodies. | Full-PDF-only build, 12,924 candidates, 51–1,898 per report, no cap or truncation. | Build08 manifest; Stage-1 re-audit; Figure 2. | Closed |
| W2 | Title population mismatched the measured population. | Explicitly states that NERC reliability/disturbance/assessment reports are measured and maintenance work orders are an untested transfer population. | Abstract; Introduction; Discussion 5.2; Conclusion. | Transparently bounded; substantive title-validity blocker remains |
| W3 | Headers, footers, markers, encoding, and table noise were not controlled; ROUGE is not engineering usefulness. | Registered eight deterministic pollution gates and page anchors; manuscript states that zero pattern hits are not a semantic-cleanliness guarantee and ROUGE is not engineering utility. | Stage-1 re-audit; Sections 3.3 and 5.4. | Closed for registered gates; human usefulness unresolved |
| W4 | Five-role graph lacked domain causal validation. | Renamed and consistently bounded as a typed textual proxy graph; no physical-causality claim. | Sections 2.2, 3.4–3.5, 5.3. | Wording closed; expert validation unresolved |
| W5 | Public URLs did not establish redistribution rights. | Added fail-closed rights statement; no source PDF/verbatim text redistribution without permission. | Build08 rights ledger; Sections 3.10 and Data Availability. | Closed at policy level; human permission decision pending |
| W6 | Report inventory, parser-quality audit, and page-anchored cases were absent. | Added dataset/extraction table and figure; supplement plan binds per-report audit. | Results 4.1; Figure 2; Supplementary Materials. | Closed for staging |
| W7 | Human review and abstention boundary were absent. | Figure 1 shows quality gate, abstention, and qualified human review as deployment requirements; no fabricated expert study. | Figure 1; Sections 3.10 and 5.5. | Closed as boundary; actual expert study unresolved |

## Journal and Integrity Reviewer

| ID | R1 concern | R2 action | Acceptance evidence | Status |
|---|---|---|---|---|
| J1 | Exact title is unsupported without maintenance/work-order data. | Retained title per author instruction and disclosed the transfer boundary in all claim-bearing sections. | Abstract; Sections 1, 5.2, 6. | **Unresolved submission risk** |
| J2 | “Causal and Counterfactual” lacked distinct method and validated benefit. | Added non-identical typed path deletion and strict single-channel ablation; retained negative dev effect. | Methods 3.5–3.7; Results 4.2. | Identifiability closed; benefit/expert validity pending |
| J3 | Reused/inspected test population cannot be confirmatory. | Labels future output as post-audit corrective/descriptive throughout; no one-shot confirmatory wording. | Abstract; Sections 3.1, 3.9, 4.4, 5.4. | Closed as evidence classification; confirmation unresolved |
| J4 | Public repository did not reproduce manuscript evidence. | Data Availability states repository is not claimed synchronized until exact tag and fresh-clone verification. | Section 3.10; Data Availability. | Honest disclosure closed; release synchronization pending |
| J5 | Corresponding email and GenAI disclosure incomplete. | Preserved explicit email placeholder and tool-by-tool disclosure placeholder. | Front matter; declarations. | Manual blockers remain |
| J6 | Immutable manuscript-specific package and rights matrix absent. | Staging points to v0.3.1 hashes, rights ledger, dependency lock, and intended supplement; formal result ledger still absent. | Evidence registry; Supplementary Materials. | Partly closed; final package/result hashes pending |
| J7 | Figures were unsuitable and lacked dataset flow/paired uncertainty. | Added four code-native SVG figures: algorithm, dataset flow, protocol, and non-deceptive result scaffold. | `figures/*.svg`; `FIGURE_LINEAGE.json`. | Closed for staging; result population pending |
| J8 | Corrective reconstruction dominated the scientific narrative. | Main text uses conventional IMRaD organization; incident history is summarized only where needed for evidence classification. | Manuscript structure; `CORRECTIVE_HISTORY_v0_3_1.md`. | Closed for staging |

## New v0.3 Pre-Test Audit Findings and Repair

| ID | Independent finding | v0.3.1 repair | Status |
|---|---|---|---|
| B1 | Semantic comparator lacked MMR diversity. | Added frozen Semantic-MMR with MiniLM centroid relevance and pairwise semantic redundancy, lambda 0.5. | Repaired; fresh audit pending |
| B2 | Test-file paths/hashes were outside runtime closure. | Repository-relative paths and runtime verification of bound, code, and test files. | Repaired; fresh audit pending |
| B3 | Registered CF work limits were not threaded through the runner. | Threaded all four path limits and added behavioral tests. | Repaired; fresh audit pending |
| B4 | Transitive output dependencies were unbound. | Added and hash-bound recursive dependency lock. | Repaired; fresh audit pending |
| B5 | One-shot rule was documentary. | Added hash-bound authorization and durable atomic run registry. | Repaired; fresh audit pending |

## Remaining R2 Gates

1. **Completed:** the fresh independent pre-test audit passed the v0.3.1 freeze.
2. **Completed:** exact hash-bound authorization was recorded and one physical formal run completed in the canonical output directory.
3. A fresh agent must audit predictions, aggregate metrics, paired statistics, Holm adjustment, and figure lineage.
4. All `EVIDENCE_PENDING_TEST` tokens must be replaced only by audited values or retained explicitly if the post-run audit fails.
5. The exact repository release must be synchronized/tagged and verified from a fresh clone.
6. Corresponding-author email, CRediT roles, funder name/role, conflicts statement, and GenAI disclosure require author approval.
7. Title-concordant maintenance data and qualified-domain validation remain substantive submission-quality blockers unless the author accepts the stated transfer limitation and the editor considers it sufficient.
