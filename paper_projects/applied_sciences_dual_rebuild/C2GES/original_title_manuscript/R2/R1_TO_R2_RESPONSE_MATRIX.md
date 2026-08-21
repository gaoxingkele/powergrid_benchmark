# C²GES R1 → R2 response matrix

Status: assembled R2 review draft, 2026-08-08. Scientific results derive only from the independently audited v0.3.1 formal output. “Closed” means both manuscript text and supporting artifact are present; it does not imply that unresolved external-validity or manual submission requirements disappeared.

| ID | R1 concern | R2 response and evidence | Status |
|---|---|---|---|
| M1 | The v0.2 deletion score was algebraically identical to weighted degree. | Retired v0.2 evidence. Defined stage-monotone 2–4-edge path-utility loss under node deletion; tests and a constructive counterexample establish non-identity. See Methods 3.4 and `counterfactual_paths_v031.py`. | Closed for mathematical/software identity; efficacy is negative |
| M2 | Executive Summary leakage and capped excerpts invalidated candidates. | Rebuilt 40 complete PDFs with fail-closed boundaries, no candidate cap, 27 retained reports and 12,924 candidates. Independent audit found zero page overlap, exact match, ≥50-character common substring, and registered pollution hits. | Closed for registered build08 gates |
| M3 | NERC reports do not validate maintenance-work-order performance or physical causality. | Abstract, Introduction, Discussion, and Conclusion explicitly identify the measured population, untested transfer, and proxy-only meaning of causal/counterfactual. | Transparently bounded; title-concordant validation remains open |
| M4 | Primary outcomes and multiplicity family were inconsistent. | Registered ROUGE-L only, three contrasts at two budgets, one six-test Holm family, 10,000 paired report bootstrap samples. | Closed |
| M5 | No development ledger and weak semantic comparator. | Complete 144-configuration ledger; grid 60 selected on 12 reports. Added frozen MiniLM Semantic-MMR with λ=0.5. | Closed |
| M6 | Split and near-duplicate evidence was inadequate. | Report-level disjoint split, page/sentence/substring checks, immutable hashes and independent re-audit. | Closed within registered checks |
| M7 | Figures misrepresented identical channels and lacked paired uncertainty. | Four code-native, hash-bound figures now show the distinct path mechanism, dataset flow, aggregate means, and all 15 paired differences. | Closed |
| M8 | Result tables and PDF layout were incomplete. | All 7×2×4 aggregate metrics and all six registered contrasts are reported. PDF compiled without overfull boxes or undefined references and was inspected page-by-page. | Closed |
| W1 | Corpus consisted of excerpts, not full report bodies. | Full-PDF build with 51–1898 candidates per report; 25 reports exceed 80 candidates. | Closed |
| W2 | Title population mismatched measured population. | Retained exact author-directed title but states NERC technical reports are measured and maintenance records remain untested. | Editorial risk remains |
| W3 | Extraction noise and ROUGE’s engineering limitation were omitted. | Registered pollution gates are reported; zero hits are not treated as semantic cleanliness. ROUGE is explicitly not engineering usefulness, factual sufficiency, or unsafe-omission assessment. | Closed for disclosure |
| W4 | Five-role graph lacked domain validation. | Consistently described as a lexical typed textual proxy graph; no qualified-expert validation or physical-causality claim is made. | Wording closed; expert validation open |
| W5 | Redistribution rights were unclear. | Data Availability fails closed on PDFs/verbatim derivatives and allows editor/reviewer verification only subject to third-party permission. | Closed at manuscript-policy level; permission is human-controlled |
| W6 | Inventory and page-anchored audit were absent. | Dataset audit table, flow figure, frozen manifests, and independent reports are bound in the supplement plan. | Closed |
| W7 | Human review/abstention boundary was absent. | Featured Application and future-validation sections require source-linked qualified review; no AI judgment is called expert validation. | Boundary closed; actual expert study absent |
| J1 | Exact title is broader than evidence. | Maintained by author instruction with repeated transfer limitation. | Unresolved submission risk |
| J2 | “Causal and Counterfactual” lacked a distinct method and validated gain. | Distinct mechanism is implemented; strict ablation is unfavorable at both K values and the negative result appears in Abstract, Results, Discussion, and Conclusion. | Method identity closed; gain not supported |
| J3 | Inspected test population cannot yield confirmatory evidence. | Every claim labels the execution post-audit corrective descriptive and calls for a new sealed holdout. | Closed as evidence classification |
| J4 | Public repository was not synchronized to evidence. | Data Availability explicitly withholds a reproducibility claim until synchronization, tagging, and fresh-clone verification. | Honest disclosure closed; release task open |
| J5 | Corresponding email and detailed AI disclosure were incomplete. | Manual email placeholder and AI-use disclosure are present; exact tool-by-tool provenance remains a pre-submission author task. | Manual blocker remains |
| J6 | Immutable manuscript package was absent. | R2 binds formal output hashes and includes round audit, source, figures, scripts, PDF, and response matrix. | Closed for R2 review package |

## Audited formal findings inserted in R2

- Full ROUGE-L: 0.1060435 (K=5), 0.1276358 (K=10).
- Strict no-CF: 0.1093758 and 0.1309962; Full differences −0.003332 and −0.003360, with both 95% intervals crossing zero.
- Semantic-MMR: 0.0853068 and 0.1132759; TextRank: 0.0806058 and 0.1156068.
- Machine estimator values of 0.0 are reported in prose/table as `p_boot < 0.0002`, with zero smaller-tail draws among 10,000 samples; immutable machine artifacts retain 0.0.
- Independent post-run verdict: PASS; evidence class remains `post_audit_corrective_descriptive_not_fresh_confirmatory`.

## Remaining manual/external gates

1. Provide and verify Yang Yong’s corresponding-author email.
2. Synchronize/tag the public repository and verify the exact release from a fresh clone.
3. Confirm funder-role, CRediT, conflict-of-interest, and detailed tool-by-tool AI disclosure statements.
4. Obtain any third-party permissions required for editor/reviewer transfer.
5. Treat maintenance-domain and qualified-expert validation as future scientific work, not completed R2 evidence.
