# W7 C2GES Citation and Compliance Audit

**Decision: NOT READY FOR ASSEMBLY/SUBMISSION.** This is a read-only audit; no TeX or Bib file was changed.

The old bibliography has 48 entries and 14 cited keys. The rebuilt W5/W6 drafts contain **zero scholarly citations**. The old abstract is 169 words and passes the requested 200-word ceiling, but no rebuilt final abstract exists. There are 7 submission blockers.

## Immediate blockers

- **Current title truthful to frozen role result:** Old title says Causal-Role-Aware, but W6 freezes the primary role-conditioning claim as NO-GO.
- **Current numerical claims:** Old abstract/results use superseded 4000/800/800 and single-run positive role claims; final text must use frozen W6/W7 evidence only.
- **Author Contributions:** Declaration exists, but initials L.B. do not match displayed author name Bijing Liu (normally B.L.); authors must correct/confirm.
- **Funding:** Funding statement contains [AUTHOR INPUT REQUIRED].
- **Data Availability:** Contains local workspace paths and requires a permanent public repository URL.
- **Author contact metadata:** Two affiliation emails remain author-email-required@example.com placeholders.
- **Citation coverage in rebuilt drafts:** W5 citations=0, W6 citations=0; artifact CLAIM comments are not scholarly citations.

## Reusable local Bib keys

- **benchmark and evidence selection:** `thorne2018fever`, `liao2023muser`, `yadav2020unsupervised`, `liang2020hammer`
- **query focused and extractive selection:** `zhong2021qmsum`, `vig2022exploring`, `zhong2020extractive`, `bi2021aredsum`, `joshi2022ranksuman`
- **graph and local structure:** `wang2020heterogeneous`, `jing2021multiplex`, `cui2020enhancing`, `liu2021unsupervised`, `zhao2023multigranularity`
- **role and causal relation context:** `feder2022causal`, `du2022ecare`, `wang2024documentlevel`, `zhang2023causal`
- **reranking context:** `qin2024pairwise`, `zhuang2024setwise`, `ren2025selfcalibrated`
- **power grid context:** `xie2022massively`, `srinivasan2023artificial`, `rajkumar2023cyber`, `madabhushi2023survey`, `ramirezmeyers2021different`
- **preprint only use with status label:** `hamann2024foundation`, `sotudeh2024rank`, `liu2023rank`

These are candidate keys, not an instruction to cite every item. Three currently cited/background entries remain preprint-only and require publication-status review.

## Bibliography integrity

- Exact DOI duplicates: 0; exact normalized-title duplicates: 0.
- Structured `doi` fields: 0/48; DOI strings recoverable from `note`: 37.
- Preprint-only entries requiring status review: 11.

- **BIB-DOI-FIELD (major):** No entry uses a structured doi field; 37 DOI strings are embedded in note/href. Move verified DOI strings into doi fields and let the final MDPI bibliography style format links. Keys: all DOI-bearing entries.
- **BIB-ARXIV-MACRO (major):** 11 entries encode arXiv identifiers with the manuscript-specific \adot macro and have no DOI. Before reuse, verify publication status; otherwise retain explicit preprint status and use portable eprint/archivePrefix fields. Keys: `hamann2024foundation`, `kcman2023causal`, `liang2020hammer`, `liu2023queryutterance`, `liu2023rank`, `mao2023bipartite`, `sotudeh2023qontsum`, `sotudeh2024rank`, `wright2025unstructured`, `yadav2020unsupervised`, `yu2023improving`.
- **BIB-RAJKUMAR-PAGES (major):** Journal pages are absent; DOI record resolves to IEEE Access 11, 103154-103176. Add verified page range 103154--103176. Keys: `rajkumar2023cyber`.
- **BIB-BELWAL-INCOMPLETE (major):** Volume, issue and pages are absent, and online-first year versus issue year needs resolution. Refresh the complete record through DOI 10.1007/s12652-020-02591-x before reuse. Keys: `belwal2020graphbased`.
- **BIB-RAMIREZ-INCOMPLETE (major):** Volume and article number are absent; the DOI publication page identifies Progress in Energy 3, 033001. Add volume 3 and article number 033001 after author review. Keys: `ramirezmeyers2021different`.
- **BIB-AHMAD-AUTHORS (critical):** Local author names (Nadeem Ahmad; Chen Zhang; Umme Sehar) conflict with the publisher record (Nouman Ahmad; Changsheng Zhang; Uroosa Sehar). Do not reuse until the authors are corrected from the publisher BibTeX. Keys: `ahmad2026mitigating`.
- **BIB-STALE-COMMENT (minor):** The Bib header still says 'References for CMC submission' although the file is in the Applied Sciences tree. Replace the stale provenance comment when the final Bib is assembled.

## Related-work coverage required

| Topic | Local coverage | Status |
|---|---|---|
| FEVER benchmark, evidence annotations and conversion boundary | `thorne2018fever` | available |
| sentence-level evidence retrieval/fact verification | `thorne2018fever`, `liao2023muser`, `yadav2020unsupervised`, `liang2020hammer` | available |
| query-focused and extractive sentence selection | `zhong2021qmsum`, `vig2022exploring`, `zhong2020extractive`, `bi2021aredsum`, `joshi2022ranksuman` | available |
| graph/local-chain sentence interactions | `wang2020heterogeneous`, `jing2021multiplex`, `cui2020enhancing`, `liu2021unsupervised`, `zhao2023multigranularity` | available |
| role/causal relation extraction background | `feder2022causal`, `du2022ecare`, `wang2024documentlevel`, `zhang2023causal` | available_but_avoid_claiming_causal_gain |
| power-grid text analytics and report-review motivation | `xie2022massively`, `srinivasan2023artificial`, `rajkumar2023cyber`, `madabhushi2023survey`, `ramirezmeyers2021different` | partial; add locally verified Applied Sciences grid-NLP paper |
| BM25 definition and implementation | none | missing_verified_reference |
| Sentence-BERT/MiniLM encoder | none | missing_verified_reference |
| cross-encoder and BGE rerankers | none | missing_verified_references |
| grouped OOF/cross-fitting | none | missing_verified_method_reference |
| cluster/hierarchical bootstrap, sign-flip and Holm | none | missing_verified_statistical_references |
| official NERC reports and usage/provenance | none | missing_official_source_entries |

## Claim--citation gaps

| Location | Claim needing support | Required source | Priority |
|---|---|---|---|
| W5 2.2 | FEVER construction, human evidence and task scope | thorne2018fever | critical |
| W5 2.3 | grouped out-of-fold/train-only role prediction | verified grouped OOF/cross-fitting reference | major |
| W5 3.2 | frozen MiniLM/SBERT query representation | canonical Sentence-BERT and MiniLM/model reference | critical |
| W5 3.4 | local-chain/structural consistency motivation | wang2020heterogeneous; jing2021multiplex | major |
| W5 3.5 | pairwise ranking objective | verified learning-to-rank reference | major |
| W5 4.1 | BM25, cross-encoder and BGE comparator definitions | verified BM25; verified cross-encoder; verified BGE | critical |
| W5 4.3 | paired seed inference, hierarchical bootstrap and multiplicity control | verified cluster bootstrap; verified Holm | critical |
| W5 2.4 / W6 6.5 | NERC source and silver-label provenance | official NERC report/source entries | critical |
| W6 6.1/6.3 | mechanistic interpretation of BM25 top-1 versus deeper-list behaviour | BM25/IR literature or retain explicitly as hypothesis | major |
| Final Introduction/Related Work | Applied Sciences fit and closest power-grid NLP precedent | proposed local key meng2023gridfield; xie2022massively | critical |

Artifact/claim-ledger comments support internal numerical provenance, but they do not replace citations for datasets, algorithms, prior methods, or domain context.

## Ten-paper Applied Sciences corpus

Only the grid-field relation-extraction paper is a direct C2GES related-work candidate. The emergency-dispatch paper is optional application context. The other eight are venue/style comparators and should not be cited merely because they appeared in the target journal.

1. [A Combined Semantic Dependency and Lexical Embedding RoBERTa Model for Grid Field Relational Extraction](https://doi.org/10.3390/app131911074) — direct; Closest local Applied Sciences precedent for power-grid NLP/relation extraction; create a verified Bib entry such as meng2023gridfield.
2. [Deep Neural Network-Based Autonomous Voltage Control for Power Distribution Networks with DGs and EVs](https://doi.org/10.3390/app132312690) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.
3. [Multi-Stage Coordinated Planning for Transmission and Energy Storage Considering Large-Scale Renewable Energy Integration](https://doi.org/10.3390/app14156486) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.
4. [Emergency Dispatch Strategy Considering Spatiotemporal Evolution of Power Grid Failures Under Typhoon Conditions](https://doi.org/10.3390/app142210368) — contextual; Optional power-grid failure/emergency context only; it does not support evidence-retrieval claims.
5. [Optimization of Active Distribution Network Operation with SOP Considering Reverse Power Flow](https://doi.org/10.3390/app142411797) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.
6. [Power Grid Load Forecasting Using a CNN-LSTM Network Based on a Multi-Modal Attention Mechanism](https://doi.org/10.3390/app15052435) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.
7. [Stable Variable Fixation for Accelerated Unit Commitment via Graph Neural Network and Linear Programming Hybrid Learning](https://doi.org/10.3390/app15084498) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.
8. [Short-Term Power Load Forecasting Using an Improved Model Integrating GCN and Transformer](https://doi.org/10.3390/app15137003) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.
9. [A Dual-Decomposition Graph-Mamba-Transformer Framework for Ultra-Short-Term Wind Power Forecasting](https://doi.org/10.3390/app16010466) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.
10. [Coordinated Optimization of Wind Farm Control Parameters for Primary Frequency Regulation Based on Fatigue Load Prediction](https://doi.org/10.3390/app16094476) — venue_style_only; Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it.

## MDPI and scientific-disclosure checks

| Item | Status | Evidence/action |
|---|---|---|
| MDPI Applied Sciences article class | **pass** | documentclass[applsci,article,submit,moreauthors] |
| Abstract <= 200 words | **pass_old_only** | Old abstract: 169 words; rebuilt final abstract is not yet written. |
| Section fit | **open** | Old source has 7 top-level sections; corpus median is 5 and registered C2GES plan is 6. Merge final draft to the six-section plan. |
| Current title truthful to frozen role result | **blocker** | Old title says Causal-Role-Aware, but W6 freezes the primary role-conditioning claim as NO-GO. |
| Current numerical claims | **blocker** | Old abstract/results use superseded 4000/800/800 and single-run positive role claims; final text must use frozen W6/W7 evidence only. |
| Oracle disclosure | **pass_in_new_drafts** | W5/W6 explicitly label oracle-label conditional, end_to_end=false, and prohibit deployable interpretation. |
| NERC provenance disclosure | **pass_in_new_drafts** | W5/W6 state agent-generated/verified silver, qualitative-only, not human gold or quantitative domain proof. |
| AI-use disclosure | **open** | Old Acknowledgments discloses LLM drafting/editing and author responsibility; final version should retain it and identify tool/purpose per the submission-time policy. |
| Author Contributions | **blocker** | Declaration exists, but initials L.B. do not match displayed author name Bijing Liu (normally B.L.); authors must correct/confirm. |
| Funding | **blocker** | Funding statement contains [AUTHOR INPUT REQUIRED]. |
| IRB and Informed Consent | **author_confirmation** | Both statements exist and say not applicable; authors/institution must confirm applicability for reuse of public benchmark/report material. |
| Data Availability | **blocker** | Contains local workspace paths and requires a permanent public repository URL. |
| Conflicts of Interest and funder role | **pass_text_present** | Both conflict declaration and funder non-involvement language are present. |
| Author contact metadata | **blocker** | Two affiliation emails remain author-email-required@example.com placeholders. |
| Citation coverage in rebuilt drafts | **blocker** | W5 citations=0, W6 citations=0; artifact CLAIM comments are not scholarly citations. |
| Final declarations present in rebuilt assembly | **open** | W5/W6 are staging drafts and contain no final declaration block; migrate only verified declarations during assembly. |

### Required final structure

Use the registered six-section plan: Introduction; Related Work; Data and Task; Proposed C2GES Method; Experiments, Results and Discussion; Conclusions. Merge standalone Reproducibility and Limitations material into the relevant method/experiment section. The 10-paper corpus median is five top-level sections; six remains a reasonable task-driven target, not a journal rule.

### Protocol and disclosure wording to preserve

- Oracle-label is a conditional diagnostic using human FEVER veracity and must state `end_to_end=false`.
- Predicted-label is end-to-end only within document-conditioned role prediction plus sentence selection; it is not open-corpus fact verification.
- NERC material is agent-generated/verified silver and qualitative-only, not expert gold or quantitative domain proof.
- Retain an AI-use declaration identifying drafting/editing assistance, author verification and responsibility; confirm exact tool and purpose at submission.

## Metadata verification URLs

- Rajkumar IEEE Access metadata: https://doi.org/10.1109/ACCESS.2023.3317695
- Belwal Springer metadata: https://doi.org/10.1007/s12652-020-02591-x
- Ramirez-Meyers IOP metadata: https://doi.org/10.1088/2516-1083/abf636
- Ahmad CMC publisher metadata: https://www.techscience.com/cmc/v87n1/66046/html
- Borovcak CMC publisher metadata: https://www.techscience.com/cmc/v88n2/67604

## Ordered remediation

1. Replace the old title and all superseded 4000/800/800 single-run claims.
2. Build the missing Introduction/Related Work with verified citations, then insert citations into W5/W6 claim locations.
3. Acquire and verify BM25, Sentence-BERT/MiniLM, cross-encoder/BGE, grouped-OOF, bootstrap/Holm and official NERC source references.
4. Repair Bib DOI fields and critical author/incomplete-record issues; do not copy all 48 entries blindly.
5. Assemble to the registered six-section structure and write a <=200-word abstract from frozen results.
6. Resolve author emails, funding grant, CRediT initials, permanent repository/data DOI, IRB confirmation and AI-tool disclosure before submission.

Machine-readable entry-level findings, source hashes and the complete 1060-cell statistics provenance boundary are kept outside the manuscript; this audit does not modify the paper.
