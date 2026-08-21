# MA-SQLGrid Introduction/Related-Work Reference Audit

Audit date: 2026-08-05  
Scope: `INTRO_RELATED_WORK_DRAFT.md` and `references_verified.bib` only  
Policy: metadata must be traceable to a DOI resolver, publisher page, ACL Anthology, NeurIPS Proceedings, OpenReview, arXiv, MDPI, OSTI, or the official dataset article. Search-result snippets were used only to locate primary pages. No unverified bibliographic identity is admitted.

## Audit Summary

- Bibliography entries: **25**.
- Entries with DOI: **21**.
- Entries with a primary archival URL but no DOI used: **4** (`li2023bird`, `lei2025spider2`, `pourreza2023dinsql`, `tan2024tailored`).
- *Applied Sciences* entries: **3** (`bian2025dkasql`, `meng2023gridroberta`, `tang2023provenance`).
- *Applied Sciences* entries cited in the draft: **2** (`bian2025dkasql`, `meng2023gridroberta`). `tang2023provenance` is verified reserve material for the reproducibility/data-provenance section and is intentionally not forced into the Introduction.
- Direct same-journal technical predecessor: **1**, DKASQL.
- Unverified entries admitted: **0**.
- URL-only limitations: CHESS is cited explicitly as an arXiv preprint; BIRD/DIN-SQL use official NeurIPS proceedings URLs; Spider 2.0 uses its ICLR 2025 OpenReview page; the LREC-COLING paper uses its official ACL Anthology page.

## Literature Claim-to-Source Map

| Claim ID | Bounded claim used in the draft | Primary evidence | Audit decision |
|---|---|---|---|
| LIT-01 | Text-to-SQL maps natural-language requests to SQL and requires treatment of question, schema, and grounding information. | [VLDB Journal survey](https://doi.org/10.1007/s00778-022-00776-8); [Spider](https://doi.org/10.18653/v1/D18-1425) | Verified; general task description only. |
| LIT-02 | Benchmarks evolved from cross-domain schemas to large databases and enterprise workflows. | [Spider](https://doi.org/10.18653/v1/D18-1425); [BIRD](https://proceedings.neurips.cc/paper_files/paper/2023/hash/83fc8fab1710363050bbd1d4b8cc0021-Abstract-Datasets_and_Benchmarks.html); [Spider 2.0](https://openreview.net/forum?id=XmProj9cPs) | Verified; no leaderboard comparison imported. |
| LIT-03 | RTS-GMLC and SimBench are reproducible power-system resources, not native human-gold text-to-SQL corpora. | [RTS update](https://doi.org/10.1109/TPWRS.2019.2925557); [SimBench](https://doi.org/10.3390/en13123290) | Verified. The “not native text-to-SQL corpora” statement follows from their published task/data definitions, not an absence-of-evidence novelty claim. |
| LIT-04 | Power-grid NLP has used domain-sensitive representations; relation extraction is distinct from SQL generation. | [Meng et al.](https://doi.org/10.3390/app131911074) | Verified; treated as application-adjacent, never as a text-to-SQL baseline. |
| LIT-05 | Schema linking/selection and schema graphs are established control mechanisms. | [RAT-SQL](https://doi.org/10.18653/v1/2020.acl-main.677); [Lei et al.](https://doi.org/10.18653/v1/2020.emnlp-main.564); [IESQL](https://doi.org/10.1145/3534678.3539294); [SchemaGraphSQL](https://doi.org/10.18653/v1/2026.findings-eacl.134); [CHESS](https://doi.org/10.48550/arXiv.2405.16755) | Verified. Draft does not claim all methods improve every setting. |
| LIT-06 | Prompt decomposition, tailored schema prompts, and consistency selection have been studied. | [DIN-SQL](https://proceedings.neurips.cc/paper_files/paper/2023/hash/72223cc66f63ca1aa59edaec1b3670e6-Abstract-Conference.html); [Nan et al.](https://doi.org/10.18653/v1/2023.findings-emnlp.996); [SQLPrompt](https://doi.org/10.18653/v1/2023.findings-emnlp.39); [Tan et al.](https://aclanthology.org/2024.lrec-main.539/) | Verified. |
| LIT-07 | Output-form compliance and semantic execution are different outcomes. | [Semantic test suites](https://doi.org/10.18653/v1/2020.emnlp-main.29); [SQLPrompt](https://doi.org/10.18653/v1/2023.findings-emnlp.39) | Verified as a methodological distinction; MA-SQLGrid's quantitative separation is supported by local claim MA-C12, not by these citations. |
| LIT-08 | Structural and execution metrics can disagree; realistic and perturbed evaluations reveal robustness gaps. | [Semantic test suites](https://doi.org/10.18653/v1/2020.emnlp-main.29); [KaggleDBQA](https://doi.org/10.18653/v1/2021.acl-long.176); [synonym robustness](https://doi.org/10.18653/v1/2021.acl-long.195) | Verified. |
| LIT-09 | Constrained decoding, correction, candidate consistency, and execution-guided refinement intervene at different stages. | [PICARD](https://doi.org/10.18653/v1/2021.emnlp-main.779); [error correction](https://doi.org/10.18653/v1/2023.acl-short.117); [SQLPrompt](https://doi.org/10.18653/v1/2023.findings-emnlp.39); [DART-SQL](https://doi.org/10.18653/v1/2024.findings-acl.120) | Verified. The impossibility of guaranteeing intent from reference-free execution is framed as a logical boundary, not an empirical claim about these papers. |
| LIT-10 | DKASQL is a direct same-journal, domain-specific, power-grid Text-to-SQL predecessor with extraction/generation/verification and BIRD/ElecSQL evaluation. | [DKASQL](https://doi.org/10.3390/app152011121) | Verified from the MDPI version of record. Novelty wording was narrowed accordingly. |

## Entry-Level Metadata Audit

| Bib key | Type/status | DOI or primary URL | Verified facts used |
|---|---|---|---|
| `katsogiannis2023survey` | Journal article | https://doi.org/10.1007/s00778-022-00776-8 | Title, authors, journal, volume/pages. |
| `yu2018spider` | EMNLP paper | https://aclanthology.org/D18-1425/ | Title, author order, venue, pages, DOI. |
| `wang2020ratsql` | ACL paper | https://aclanthology.org/2020.acl-main.677/ | Title, authors, venue, pages, DOI. |
| `lei2020reexamining` | EMNLP paper | https://aclanthology.org/2020.emnlp-main.564/ | Title, authors, DOI. |
| `liu2022semantic` | ACM KDD paper | https://doi.org/10.1145/3534678.3539294 | Title, authors, DOI. |
| `zhong2020semantic` | EMNLP paper | https://aclanthology.org/2020.emnlp-main.29/ | Title, authors, venue, pages, DOI. |
| `gan2021robustness` | ACL paper | https://aclanthology.org/2021.acl-long.195/ | Title, authors, DOI. |
| `lee2021kaggledbqa` | ACL paper | https://aclanthology.org/2021.acl-long.176/ | Title, authors, DOI. |
| `li2023bird` | NeurIPS Datasets and Benchmarks | https://proceedings.neurips.cc/paper_files/paper/2023/hash/83fc8fab1710363050bbd1d4b8cc0021-Abstract-Datasets_and_Benchmarks.html | Title, full author list, venue/year; no DOI asserted. |
| `lei2025spider2` | ICLR 2025 paper | https://openreview.net/forum?id=XmProj9cPs | Title, full author list, ICLR 2025 publication; no DOI asserted. |
| `nan2023enhancing` | Findings EMNLP | https://doi.org/10.18653/v1/2023.findings-emnlp.996 | Title, authors, DOI. |
| `sun2023sqlprompt` | Findings EMNLP | https://aclanthology.org/2023.findings-emnlp.39/ | Title, authors, venue, pages, DOI. |
| `pourreza2023dinsql` | NeurIPS paper | https://proceedings.neurips.cc/paper_files/paper/2023/hash/72223cc66f63ca1aa59edaec1b3670e6-Abstract-Conference.html | Title, authors, venue/year; no DOI asserted. |
| `talaei2024chess` | arXiv preprint | https://doi.org/10.48550/arXiv.2405.16755 | Title, authors, identifier. No archival venue is claimed. |
| `tan2024tailored` | LREC-COLING paper | https://aclanthology.org/2024.lrec-main.539/ | Title, authors, venue, pages. Anthology exposes no DOI, so none is asserted. |
| `mao2024dartsql` | Findings ACL | https://aclanthology.org/2024.findings-acl.120/ | Title, authors, venue, pages, DOI. |
| `scholak2021picard` | EMNLP paper | https://aclanthology.org/2021.emnlp-main.779/ | Title, authors, venue, pages, DOI. |
| `chen2023texttosql` | ACL short paper | https://aclanthology.org/2023.acl-short.117/ | Title, authors, venue, pages, DOI. |
| `safdarian2026schemagraphsql` | Findings EACL | https://aclanthology.org/2026.findings-eacl.134/ | Title, authors, venue, pages, DOI. |
| `xie2026sdesql` | ACL long paper | https://aclanthology.org/2026.acl-long.116/ | Title, authors, venue, pages, DOI. |
| `bian2025dkasql` | *Applied Sciences* article | https://doi.org/10.3390/app152011121 | Title, authors, volume/issue/article, method/datasets. |
| `meng2023gridroberta` | *Applied Sciences* article | https://doi.org/10.3390/app131911074 | Title, authors, volume/issue/article, grid relation-extraction task. |
| `tang2023provenance` | *Applied Sciences* article | https://doi.org/10.3390/app13010064 | Title, authors, volume/issue/article. Verified reserve item. |
| `barrows2020rts` | IEEE journal article | https://doi.org/10.1109/TPWRS.2019.2925557 and https://www.osti.gov/biblio/1545004 | Title, full author list, journal, volume/issue/pages, DOI. |
| `meinecke2020simbench` | *Energies* article | https://doi.org/10.3390/en13123290 | Title, authors, volume/issue/article, benchmark scope. |

## Ten-Paper Applied Sciences Sample: Technical versus Structural Use

The local corpus is `papers/literature/applied_sciences_power_ai_10/`. All ten official PDFs and JATS XML files are present. Its medians (24 pages, 7098 body words, five primary sections, 26 numbered equations, nine figures, five tables) are descriptive comparators, not journal requirements.

| Local ID / DOI | Topic | Permitted use for MA-SQLGrid | Technical-precedent decision |
|---|---|---|---|
| `13-11074` / [10.3390/app131911074](https://doi.org/10.3390/app131911074) | Grid relation extraction | Cite for domain-sensitive power-grid NLP and use as an application-framing example. | **Adjacent only**; not text-to-SQL. |
| `13-12690` / [10.3390/app132312690](https://doi.org/10.3390/app132312690) | DNN voltage control | Study organization, applied-value statement, data/setup/result flow. | **Structural only**. |
| `14-06486` / [10.3390/app14156486](https://doi.org/10.3390/app14156486) | Transmission/storage planning | Case-study and engineering-discussion organization. | **Structural only**. |
| `14-10368` / [10.3390/app142210368](https://doi.org/10.3390/app142210368) | Typhoon emergency dispatch | Scenario/evidence narration. | **Structural only**. |
| `14-11797` / [10.3390/app142411797](https://doi.org/10.3390/app142411797) | Active distribution optimization | Methods-to-case-study organization. | **Structural only**. |
| `15-02435` / [10.3390/app15052435](https://doi.org/10.3390/app15052435) | Multi-attention load forecasting | Multi-dataset result organization and limitations style. | **Structural only**. |
| `15-04498` / [10.3390/app15084498](https://doi.org/10.3390/app15084498) | GNN/LP unit commitment | Applied AI framing and hybrid-system diagram style. | **Structural only**. |
| `15-07003` / [10.3390/app15137003](https://doi.org/10.3390/app15137003) | GCN-Transformer load forecasting | Dense results/ablation presentation. | **Structural only**. |
| `16-00466` / [10.3390/app16010466](https://doi.org/10.3390/app16010466) | Graph-Mamba wind forecasting | Recent AI-paper section balance and visual evidence density. | **Structural only**. |
| `16-04476` / [10.3390/app16094476](https://doi.org/10.3390/app16094476) | Wind-farm frequency regulation | Engineering-benefit discussion and limitation placement. | **Structural only**. |

**Critical addition outside the ten-paper sample:** [DKASQL](https://doi.org/10.3390/app152011121) is the closest same-journal technical predecessor and must be cited. The ten-paper corpus was built for structure/statistics and is not an exhaustive novelty search.

## Items Not Admitted or Requiring Caution

1. The older project bibliography contains numerous 2025--2026 arXiv entries. They were not imported merely for recency; only sources needed for a bounded paragraph were retained.
2. The local `applied_sciences_power_grid_recent` registry leaves DOI cells blank for `applsci-14-01077`, `applsci-15-08656`, and `applsci-16-06581`. These papers are not used in this support draft, so their incomplete registry metadata cannot propagate into the bibliography.
3. CHESS has a verified arXiv identity, but no archival venue was verified in this audit. It must remain labelled a preprint unless the final assembler verifies a later version of record.
4. BIRD, DIN-SQL, Spider 2.0, and the LREC-COLING tailored-prompting paper have verified primary proceedings pages; this audit does not invent DOI fields where the primary page does not expose one.
5. The old `quamar2022natural` entry duplicated an author name and was excluded rather than silently repaired without a fresh publisher-level metadata audit.
6. Applied Sciences sample statistics are not evidence of technical novelty, acceptance probability, or mandatory manuscript length.

## Local Evidence Cross-Check for Present-Study Statements

| Study statement in draft | Claim status | Canonical/local source |
|---|---|---|
| Complete paired (2\times2) design, 180 questions, 720 rows/backbone, 1440 total | `MA-C10`, `MA-C15` | `../canonical_dual_backbone/release_manifest.json`; `../canonical_dual_backbone/tables/table01_dual_cell_accuracy.csv` |
| Shape-hint execution direction replicates with Granite CI nuance; answer-shape intervals exclude zero | `MA-C13` | `../canonical_dual_backbone/tables/table04_shape_effect_replication.csv` |
| Effect magnitude and context interaction are backbone-sensitive | `MA-C14` | `../canonical_dual_backbone/tables/table03_backbone_effect_modifiers.csv` |
| Independent positive compact-context claim rejected | `MA-C03`, `E4-NO-GO` | `../canonical_dual_backbone/tables/table02_backbone_factorial_effects.csv` |
| External RTS-GMLC/SimBench plumbing only; no human-gold accuracy | `MA-C02`, `MA-C05`, `MA-C06` | `../external_protocol/W4_MA_EXTERNAL_PROTOCOL_REPORT.md`; `../data/human_review_packet/W4_MA_HUMAN_REVIEW_PACKET_REPORT.md` |
| Efficiency and validator-repair claims remain pending | `MA-C08`, `MA-C09` | `../../CLAIM_LEDGER.md` |

These local statements do not acquire credibility from external citations; they must be verified by the manuscript's canonical claim/source checker during assembly.
