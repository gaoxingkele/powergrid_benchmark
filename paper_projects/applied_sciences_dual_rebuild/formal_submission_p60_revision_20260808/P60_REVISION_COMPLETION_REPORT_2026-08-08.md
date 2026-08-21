# Applied Sciences P60 Revision Completion Report

Date: 2026-08-08 (Asia/Shanghai)

## Scope and provenance

This revision expands and restructures the two original-title manuscripts against the local 20-paper-per-topic Applied Sciences corpus. The preceding formal preview remains unchanged at `formal_submission_preview_20260808`. The P60 revision was made in a separate tree.

Base TeX SHA-256 values before the P60 revision:

- C2GES: `174EF3334C39485D999F0F8DCDA2C493FF6F6250622E36D0132FAF57DF5D44EE`
- MA-SQLGrid: `6CA17FCFCAC69D41B9CB024C27DBB6803B40675618C149CD2DC00AC94D2D0365`

## Final manuscript profile

| Manuscript | Estimated body words | Pages incl. references | Figures | Tables | BibTeX records |
|---|---:|---:|---:|---:|---:|
| C2GES | 8567 | 26 | 6 | 10 | 43 |
| MA-SQLGrid | 9201 | 27 | 6 | 13 | 36 |

### C2GES section profile

| Section | Words | Paragraphs |
|---|---:|---:|
| Introduction | 1032 | 13 |
| Related Work | 1040 | 15 |
| Materials and Methods | 3491 | 50 |
| Results | 1883 | 28 |
| Discussion | 704 | 10 |
| Conclusions | 417 | 5 |

### MA-SQLGrid section profile

| Section | Words | Paragraphs |
|---|---:|---:|
| Introduction | 1116 | 13 |
| Related Work | 1154 | 17 |
| Materials and Methods | 3442 | 45 |
| Results | 1792 | 28 |
| Discussion | 866 | 10 |
| Limitations and Future Work | 416 | 6 |
| Conclusions | 415 | 4 |

## Principal revisions

### C2GES

- Retained the original title and explicitly separated the intended maintenance application from the evaluated NERC proxy population.
- Expanded the literature comparison to graph/hypergraph summarization, technical-document summarization, power-domain knowledge graphs, relation extraction, and maintenance-oriented human evaluation.
- Added research questions, a claim--evidence map, a worked typed-path example, deterministic selection details, audit layers, evidence classes, and a layered linguistic-error taxonomy.
- Expanded the result interpretation for report-level pairing, leakage gates, budget sensitivity, metric validity, output-length fairness, exact sign-flip sensitivity, mechanism activity versus efficacy, and post-unblinding calibration.
- Added an output-length figure and evidence-ladder figure.
- Preserved the unfavorable Full-versus-no-CF result. No counterfactual-component gain, length-controlled superiority, physical causal identification, or operational maintenance effectiveness is claimed.

### MA-SQLGrid

- Retained the original title and defined “multi-agent” as typed software roles and “robust” as the specifically tested execution/evidence mechanisms.
- Expanded comparison with recent Applied Sciences Text-to-SQL, schema-retrieval, domain-adaptation, language-model-team, and energy multi-agent studies.
- Added the admissible/executable/correct distinction, artifact evidence classes, asymmetric information flow, append-only trace semantics, executor threat model, failure policy, adjudication/abstention analysis, witness semantics, and statistical-family interpretation.
- Expanded all major result blocks: GridDB cell interactions, structural-proxy limits, component heterogeneity, multi-state denominators, BIRD call accounting, retained failures, tie multiplicity, order sensitivity, and evidence-class incompatibility.
- Added an offline-selector diagnostic figure and evidence-class map.
- Preserved prior-outcome exposure and the 130/180 top-score tie result. No prospective five-role superiority, qualified grid semantic validity, deployment safety, or universal robustness is claimed.

## Verification

- Both papers compile under the local MDPI `applsci` class using `pdflatex` and `bibtex`.
- Final logs contain zero unresolved citation/reference warnings, zero multiply-defined-label warnings, and zero overfull-box warnings under the applied check.
- Every citation key used in either TeX file has a corresponding BibTeX record.
- First pages and representative results/discussion pages were rasterized and visually inspected; titles, author metadata, line numbers, tables, and new figures render legibly.
- Author affiliations, Yang Yong correspondence, `liubijing@outlook.com`, grant `521300250006`, author-contribution confirmation, repository URLs, and third-party-review-access language are retained.

## Final SHA-256

- C2GES TeX: `C8F946A3AFB66D46D34E2D40F3F461F56FC896D30F7DDA251FAB011E874ED8E4`
- C2GES PDF: `E1507062382307A728212E5C6345D3D2A9D7A7A4BEFE645B5B6E7B6349E45097`
- MA-SQLGrid TeX: `2E1DC27D397D3863B83431049C8A344D72A3EC53BC875DDC7D6180D557CB6412`
- MA-SQLGrid PDF: `C6244CD71FF7D76DBE82427A4F457C2F2B2BB0F280912E9D343FE19465D818DF`

## Remaining submission gates

The manuscripts are structurally complete, but the following declarations must remain truthful at submission:

1. Synchronize, license, tag, archive, and fresh-clone-verify each public repository before replacing the current conditional Data Availability wording.
2. Confirm that the corresponding email is the intended submission contact.
3. Do not relabel machine-silver data or LLM review as qualified human expert adjudication.
4. Do not remove the C2GES negative ablation/length caveat or the MA-SQLGrid prior-outcome/tie-order caveat.
5. Supply restricted editor/reviewer materials only subject to the stated third-party permissions.
