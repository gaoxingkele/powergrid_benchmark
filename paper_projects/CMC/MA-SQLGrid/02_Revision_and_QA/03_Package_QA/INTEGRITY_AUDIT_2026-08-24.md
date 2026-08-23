# MA-SQLGrid Fresh Integrity Audit

Date: 2026-08-24

Manuscript baseline: `01_Manuscript/LaTeX/paper_applsci.tex`

Scope: citation existence and context, claim-to-artifact consistency, common research-integrity failure modes, and explicit release boundaries.

## Verdict

**PASS_WITH_MANUAL_PORTAL_ATTESTATION.** All 37 active bibliography entries pass identity verification and are cited; all active citation contexts were reviewed and are compatible with the cited work's documented topic or method. Author metadata and conservative declarations have been incorporated from the user-directed 0823 baseline and prior author record. The route A manuscript is technically coherent, but this audit is not expert scientific validation, professional plagiarism clearance, or a substitute for the corresponding author's portal attestations.

## Citation-context coverage

| Context role | Keys reviewed | Outcome and boundary |
|---|---|---|
| Cross-database and enterprise Text-to-SQL benchmarks | `yu2018spider`, `li2023bird`, `lei2025spider2`, `li2024multisql` | PASS. Used for benchmark scope and workflow complexity, not as direct evidence for GridDB performance. |
| Schema linking, retrieval, and context selection | `wang2020ratsql`, `lei2020reexamining`, `liu2022semantic`, `bozdemir2026schema`, `liu2025solidsql`, `hao2025genlink`, `wang2025linkalign`, `safdarian2026schemagraphsql`, `nahid2026bidirectional` | PASS. Used to describe recall--distraction and schema-grounding mechanisms at family level. |
| Constrained decoding, prompting, decomposition, repair, probing, and dialect support | `scholak2021picard`, `nan2023enhancing`, `sun2023sqlprompt`, `pourreza2023dinsql`, `talaei2024chess`, `mao2024dartsql`, `xie2024deasql`, `luo2024ptdsql`, `zhai2025executionfeedback`, `xie2026sdesql`, `zhang2025exesql` | PASS. Used for stage/method positioning; no cross-paper numerical comparison is inferred. |
| Multi-role or multi-agent Text-to-SQL | `lee2025team`, `wang2025macsql`, `shao2025qcmasql`, `xia2025r3` | PASS. Supports role coordination, routing, tools, and consensus positioning; the manuscript separately defines its own five stable interfaces. |
| Semantic evaluation across database states | `zhong2020semantic` | PASS. Used for the distilled-test-suite concept only. |
| Power-system benchmark structures | `barrows2020rts`, `meinecke2020simbench` | PASS with transformation boundary. These sources support reproducible engineering structures; the relational conversion is proposed future work, not attributed as an existing result in those papers. |
| Power-grid and adjacent Text-to-SQL positioning | `bian2025dkasql`, `li2024rgisql`, `zhou2025zeroshot` | PASS. Used for domain-adaptation, relational-graph, and prompt-strategy positioning. |
| Finite-set inference and multiplicity | `cameron2008bootstrap`, `canay2017randomization`, `holm1979simple` | PASS. The manuscript explicitly treats clusters as dependence proxies and intervals as corpus-composition sensitivity. The Canay DOI was corrected to `10.3982/ECTA13081`. |

Coverage check: **37/37 unique cited keys; 21/21 citation occurrences; 0 dangling keys; 0 uncited bibliography entries.** Entry-level source URLs, checks, timestamps, documented overrides, and metadata comparisons are recorded in `REFERENCE_EXISTENCE_AUDIT_2026-08-24.json`.

## Claim and data integrity

| Risk | Check | Outcome |
|---|---|---|
| Fabricated or mismatched references | Fresh DOI/publisher/official-proceedings lookup and title/year/author comparison | PASS, 37/37. |
| Citation-key ghosts | TeX-to-BibTeX bidirectional join | PASS, 0 missing and 0 orphan entries. |
| Historical-evaluator mixing | Unified evaluator retains C000 `76/180`, validation-only `99/180`, complete-witness `100/180`, and Qwen F01 `129/180`; old `80/100/101` is historical only | PASS. |
| Result or denominator fabrication | Public verifier checks canonical, constructed-state, historical-pool, order, error-taxonomy, and BIRD row counts | PASS for the released technical subset. |
| Selective reporting | Best fixed source, ties, order sensitivity, rescue/harm, Q039, abstention, and failure taxonomy remain visible | PASS. |
| HARKing / post-hoc upgrade | Historical-pool analyses are labelled retrospective/descriptive; route A removes prospective end-to-end advantage claims | PASS. |
| Causal/system overclaim | Five-role interfaces are not presented as a learned causal treatment or proven end-to-end gain | PASS. |
| External generalization | BIRD portability is distinguished from grid-domain semantic validity; RTS-GMLC/SimBench remain future resources | PASS with external-study boundary. |
| Data leakage | Protocol histories, fixed pools, constructed-state prediction blindness, and runtime identities are recorded | PASS for recorded workflows; independent external reruns remain desirable. |
| Human/expert validation | AI-assisted review is not relabelled as power-system/database expert adjudication | PASS as a boundary; external expert review remains open. |
| Rights and redistribution | Raw GridDB/BIRD databases and restricted source-dependent assets are excluded | PASS for current public package. No explicit open-source licence is granted, so code remains all-rights-reserved; restricted-access transfer still requires file-level permission. |
| Authorship and declarations | Names, affiliations, ORCID `NONE`, correspondence, CRediT, funding, conflict, and AI disclosure are cross-checked against the designated source records | PASS for package metadata; final portal attestations remain the corresponding author's manual responsibility. |
| Originality/plagiarism | No professional similarity service or publisher database was available | **NOT CERTIFIED**; author/editor similarity screening remains required. |

## Manual actions at journal submission

1. The corresponding author reads the frozen final PDF and confirms the portal metadata and cover letter.
2. The corresponding author attests no simultaneous submission and final all-author approval in SuSy.
3. Suggested/opposed reviewer fields are completed only if required and only with real conflict checks; the repository does not fabricate names.
4. Any requested reviewer-only restricted transfer receives a fresh file-level rights and confidentiality check.

Independent expert review, untouched external grid evaluation, and a budget-matched prospective end-to-end study remain claim-upgrade requirements only if the authors later choose route B/C.
