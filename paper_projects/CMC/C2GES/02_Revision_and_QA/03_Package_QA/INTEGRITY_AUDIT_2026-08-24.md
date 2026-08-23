# C2GES Fresh Integrity Audit

Date: 2026-08-24

Manuscript baseline: `01_Manuscript/LaTeX/paper_applsci.tex`

Scope: citation existence and context, claim-to-artifact consistency, common research-integrity failure modes, and explicit release boundaries.

## Verdict

**PASS_WITH_MANUAL_PORTAL_ATTESTATION.** All 34 active bibliography entries pass identity verification and are cited; all active citation contexts were reviewed and are compatible with the cited work's documented topic or method. Author metadata and conservative declarations have been incorporated from the user-directed 0823 baseline and prior author record. This audit is not expert scientific validation, professional plagiarism clearance, or a substitute for the corresponding author's portal attestations.

## Citation-context coverage

| Context role | Keys reviewed | Outcome and boundary |
|---|---|---|
| Extractive ranking signals and semantic representations | `zhong2020extractive`, `bi2021aredsum`, `liu2021unsupervised`, `mihalcea2004textrank`, `reimers2019sentencebert` | PASS. Used for method-family positioning, not for a superiority claim. |
| Sentence/heterogeneous graph and structural summarization | `siragusa2022sentencegraph`, `onan2024mches`, `hark2025mis`, `wang2020heterogeneous`, `cui2020enhancing`, `jing2021multiplex`, `bugueno2025graphlss` | PASS. The text attributes graph, hypergraph, filtering, or heterogeneous structural mechanisms at family level and explicitly distinguishes C2GES. |
| Technical-artefact and multi-document summarization | `koh2022bugreport`, `zhang2024tomds` | PASS. Used only to motivate discourse-role and source-balance concerns. |
| Causal-language boundary | `feder2022causal`, `du2022ecare` | PASS. Used to deny causal/interventional interpretation of the typed-path score. |
| Grid, fault, alarm, line-loss, maintenance, and relation-extraction work | `xie2022massively`, `hamann2024foundation`, `madabhushi2023survey`, `srinivasan2023artificial`, `ranawaka2024leveraging`, `meng2023gridfield`, `liu2022powerfault`, `li2024lineloss`, `ma2025alarm`, `cao2024coalmaintenance`, `zgg2026bridge`, `dimaggio2025predictivemaintenance`, `li2025moere`, `she2025clear` | PASS with collective-claim boundary. The grouped sentence describes the families collectively; no cited study is presented as evidence for the C2GES result. |
| NERC event-analysis institutional context | `nerc2015qualityreport` | PASS after correction. The citation now supports only NERC quality-report guidance; corpus membership and public-source locators are supported by the rights-safe sampling frame, not inferred from this guidance document. |
| ROUGE definition | `lin2004rouge` | PASS. Used for lexical-overlap metric definition only. |
| Cluster-aware bootstrap sensitivity | `cameron2008bootstrap` | PASS. Used as methodological background; the manuscript labels the resulting intervals as composition sensitivity, not population confidence intervals. |
| Multiplicity control | `holm1979simple` | PASS. Used for the Holm family correction. |

Coverage check: **34/34 unique cited keys; 25/25 citation occurrences; 0 dangling keys; 0 uncited bibliography entries.** Entry-level primary-source URLs, checks, timestamps, and metadata comparisons are recorded in `REFERENCE_EXISTENCE_AUDIT_2026-08-24.json`.

## Claim and data integrity

| Risk | Check | Outcome |
|---|---|---|
| Fabricated or mismatched references | Fresh DOI/publisher/official-record lookup and title/year/author comparison | PASS, 34/34. |
| Citation-key ghosts | TeX-to-BibTeX bidirectional join | PASS, 0 missing and 0 orphan entries. |
| Result fabrication or denominator drift | Public verifier, frozen CSV/JSON evidence, tests, and LaTeX rebuild | PASS for the released technical subset. |
| Selective reporting | Strict path-deletion result, matched-word sensitivity, output-length mismatch, zero-weight development calibration, and non-significant adjusted contrasts remain visible | PASS with limitations retained. |
| HARKing / post-hoc upgrade | Post-run analyses are labelled diagnostic or exploratory; no retrospective result is called preregistered | PASS. |
| Causal or physical-graph overclaim | Manuscript uses `path-deletion term` and explicitly denies physical/causal validity | PASS. |
| Generalization overclaim | One-organization report corpus and absent untouched-series/expert validation are explicit | PASS; external validation remains open. |
| Data leakage | Development/test report boundary, source-page locators, and `test_input_accessed=false` for later calibration are recorded | PASS for recorded workflows; restricted source regeneration is not publicly re-executed. |
| Human/expert validation | No automated or AI-assisted check is relabelled as expert annotation | PASS as a boundary; dual-expert annotation remains open. |
| Rights and redistribution | Raw NERC PDFs and verbatim derivatives are excluded | PASS for current public package. No explicit open-source licence is granted, so code remains all-rights-reserved; third-party permission is required only before broader redistribution. |
| Authorship and declarations | Names, affiliations, ORCID `NONE`, correspondence, CRediT, funding, conflict, and AI disclosure are cross-checked against the designated source records | PASS for package metadata; final portal attestations remain the corresponding author's manual responsibility. |
| Originality/plagiarism | No professional similarity service or publisher database was available | **NOT CERTIFIED**; author/editor similarity screening remains required. |

## Manual actions at journal submission

1. The corresponding author reads the frozen final PDF and confirms the portal metadata.
2. The corresponding author attests no simultaneous submission and final all-author approval in SuSy.
3. Any requested reviewer-only restricted transfer receives a fresh file-level rights and confidentiality check.

## Conditional claim-upgrade gates

These items remain genuinely unperformed, but they do not block submission of the present scope-contracted manuscript because the corresponding strong claims have been removed:

1. Third-party permission before redistributing any material beyond the current rights-safe package.
2. Independent power-system expert structure/source-faithfulness annotation before restoring structure-validity claims.
3. Untouched external report-series evaluation before restoring external-generalization claims.
4. Expert task utility or genuine maintenance-record validation before restoring operational-use claims.
