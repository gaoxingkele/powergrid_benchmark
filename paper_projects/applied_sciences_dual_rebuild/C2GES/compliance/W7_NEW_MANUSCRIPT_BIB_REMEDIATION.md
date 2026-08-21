# W7 New C2GES Manuscript: Cited-Only Bibliography Remediation

## Scope and Result

This remediation covers only the 23 keys cited by the new C2GES manuscript before the audit, plus five primary sources added because the methods and application-provenance statements required them. Uncited entries in the inherited `references_applsci.bib` were not bulk-edited. The manuscript now uses the isolated, cited-only file `manuscript_applsci/references_cited_verified.bib`.

Result: all cited DOI-bearing entries use a structured `doi` field; the two arXiv-only papers use structured `archivePrefix`, `eprint`, and official arXiv URLs; official NERC claims cite NERC pages directly. The new bibliography contains no legacy DOI-in-`note` fields.

## Audit of the Original 23 Cited Keys

| Key | Authoritative record | Remediation |
|---|---|---|
| `thorne2018fever` | [ACL Anthology / DOI](https://aclanthology.org/N18-1074/) | Added publisher, pages 809--819, structured DOI and official URL. |
| `zhong2021qmsum` | [ACL Anthology / DOI](https://aclanthology.org/2021.naacl-main.472/) | Added publisher, pages 5905--5921, DOI and URL. |
| `vig2022exploring` | [ACL Anthology / DOI](https://aclanthology.org/2022.findings-naacl.109/) | Added publisher, pages 1455--1468, DOI and URL. |
| `zhong2020extractive` | [ACL Anthology / DOI](https://aclanthology.org/2020.acl-main.552/) | Added publisher, pages 6197--6208, DOI and URL. |
| `xie2022massively` | [IEEE DOI record](https://doi.org/10.1109/JPROC.2022.3175070) | Retained citation key for compatibility; confirmed print year 2023, volume/issue/pages, and structured DOI. |
| `hamann2024foundation` | [official arXiv record](https://arxiv.org/abs/2407.09434) | Replaced pseudo-journal formatting with `@misc`, eprint, archive prefix, class, and official URL; no DOI invented. |
| `bi2021aredsum` | [ACL Anthology / DOI](https://aclanthology.org/2021.eacl-main.22/) | Added Main Volume title, publisher, pages 281--291, DOI and URL. |
| `liu2021unsupervised` | [ACM DOI record](https://doi.org/10.1145/3404835.3463111) | Added publisher, pages 2313--2317, DOI and URL. |
| `liao2023muser` | [ACM DOI record](https://doi.org/10.1145/3580305.3599873) | Added publisher, pages 4461--4472, DOI and URL. |
| `liang2020hammer` | [official arXiv record](https://arxiv.org/abs/2009.10791) | Replaced pseudo-journal formatting with `@misc`, eprint, archive prefix, class, and official URL; no DOI invented. |
| `robertson2009probabilistic` | [publisher DOI record](https://doi.org/10.1561/1500000019) | Confirmed journal, volume, issue and pages; retained structured DOI and added resolver URL. |
| `reimers2019sentencebert` | [ACL Anthology / DOI](https://aclanthology.org/D19-1410/) | Added ACL publisher and URL; retained authoritative ACL/PDF pages 3982--3992. |
| `wang2020heterogeneous` | [ACL Anthology / DOI](https://aclanthology.org/2020.acl-main.553/) | Added publisher, pages 6209--6219, DOI and URL. |
| `cui2020enhancing` | [ACL Anthology / DOI](https://aclanthology.org/2020.coling-main.468/) | Added publisher, pages 5360--5371, DOI and URL. |
| `jing2021multiplex` | [ACL Anthology / DOI](https://aclanthology.org/2021.emnlp-main.11/) | Added publisher, pages 133--139, DOI and URL. |
| `qin2024pairwise` | [ACL Anthology / DOI](https://aclanthology.org/2024.findings-naacl.97/) | Confirmed pages, added publisher, DOI and official URL. |
| `zhuang2024setwise` | [ACM DOI record](https://doi.org/10.1145/3626772.3657813) | Added publisher and pages 38--47; structured DOI and URL. |
| `ren2025selfcalibrated` | [ACM DOI record](https://doi.org/10.1145/3696410.3714658) | Confirmed proceedings and pages; structured DOI and URL. |
| `madabhushi2023survey` | [Springer DOI record](https://doi.org/10.1007/s10207-023-00720-z) | Expanded journal title and added structured DOI/URL. |
| `srinivasan2023artificial` | [MDPI publisher page](https://www.mdpi.com/1996-1073/16/14/5383) | Confirmed article number, volume/issue, DOI and publisher URL. |
| `ranawaka2024leveraging` | [MDPI publisher page](https://www.mdpi.com/1996-1073/17/21/5342) | Confirmed article number, volume/issue, DOI and publisher URL. |
| `feder2022causal` | [MIT Press DOI record](https://doi.org/10.1162/tacl_a_00511) | Expanded journal title; confirmed pages and added structured DOI/URL. |
| `du2022ecare` | [ACL Anthology / DOI](https://aclanthology.org/2022.acl-long.33/) | Added publisher, pages 432--446, DOI and URL. |

DOI-bearing records were also checked through the Crossref Works API. The isolated bibliography uses publisher/ACL metadata where the publisher record is more precise than the Crossref deposit.

## Primary Method References Added

- Holm multiple-testing correction: Sture Holm, *A Simple Sequentially Rejective Multiple Test Procedure*, verified through [JSTOR](https://www.jstor.org/stable/4615733), DOI `10.2307/4615733`.
- Cluster-aware bootstrap inference: Cameron, Gelbach, and Miller, *Bootstrap-Based Improvements for Inference with Clustered Errors*, [MIT Press DOI](https://doi.org/10.1162/rest.90.3.414).
- Cross-fitting: Chernozhukov et al., *Double/Debiased Machine Learning for Treatment and Structural Parameters*, verified through the [Oxford Academic publisher page](https://academic.oup.com/ectj/article/21/1/C1/5056401), DOI `10.1111/ectj.12097`. The manuscript explicitly says that its document grouping is an adaptation of the general cross-fitting principle; it does not attribute `StratifiedGroupKFold` itself to this paper.

The corresponding TeX changes are limited to the sentences that already described Holm correction, document-cluster resampling, and grouped out-of-fold role prediction.

## Official NERC Provenance Added

- [NERC Event Analysis, Reliability Assessment, and Performance Analysis](https://www.nerc.com/programs/reliability-assessment--performance-analysis), the official program page identifying the event-analysis and lessons-learned context.
- [NERC, *Attributes of a Quality Event Analysis Report*](https://www.nerc.com/globalassets/programs/event-analysis/ero-event-analysis-process-documents/attributes_of_a_quality_event_analysis_report_20150211.pdf), the official report describing causal sequences, corrective actions, conclusions/recommendations, and report-quality elements.

These citations support only the provenance and intended review workflow. They do not change the frozen boundary that local NERC annotations are agent-produced silver and cannot support quantitative domain claims.

## Contradictions and Resolutions

1. Crossref currently reports Sentence-BERT pages 3980--3990, while the ACL Anthology record and its authoritative PDF citation report 3982--3992. The bibliography uses ACL's 3982--3992 and records this discrepancy here.
2. `xie2022massively` contains 2022 in the stable citation key because its DOI was registered/available in 2022, but the journal issue is 2023. The record now reports the correct print year 2023 without renaming the key and breaking existing citations.
3. `hamann2024foundation` and `liang2020hammer` have no verified DOI. They are represented as arXiv eprints rather than being assigned inferred or unofficial DOI values.

## Verification and Build

- Claim/source verifier: PASS for 11 canonical source hashes, 6 generated fragments, 8 figures, and 28 cited keys.
- Bibliography verifier now requires every cited entry to contain either a structured DOI or a verified official arXiv/NERC URL, and rejects legacy DOI-in-note formatting.
- PDF rebuild: PASS, 19 A4 pages.
- Final LaTeX log: no undefined citations, undefined references, undefined commands, fatal errors, or overfull boxes.

## Unresolved Submission Items

- The permanent public artifact repository/DOI and license review remain `W7_FRONT_MATTER` requirements.
- NERC site URLs may change as the organization migrates pages; an archived access copy or submission-date URL check is recommended.
- Copyright and redistribution terms for extracted NERC report text remain a data-governance question, not a bibliography defect.
- Author-approved names, contributions, funding, conflicts, ethics wording, and AI-use disclosure remain unchanged placeholders.
