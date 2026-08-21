# Round-1 Independent Review: Applied Sciences Fit, Integrity, and Submission Completeness

## Review identity and scope

- **Manuscript**: *Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports*
- **Role**: Independent Reviewer 3 — *Applied Sciences* fit, research integrity, and submission completeness
- **Round**: R1
- **Review date**: 2026-08-08 (Asia/Shanghai)
- **Files reviewed**: `paper_applsci.tex`; the 11-page PDF in `build_original_title_run04/`; `ASSEMBLY_AUDIT_R1.md`; `ROUND_AUDIT.json`; the v0.2 freeze manifest, configuration, aggregate metrics, paired-bootstrap output, predictions lineage, and reproduction report; both figure-lineage records; the live public GitHub repository.
- **Independence boundary**: This report was prepared without reading or discussing the other reviewers' reports. No manuscript, code, data, figure, or experiment file was edited.

## Recommendation

**Major revision — not ready for submission and not ready to pass the R1-to-R2 gate.**

**Confidence: 5/5** for journal-fit, claim–evidence, reproducibility-package, disclosure, and submission-completeness findings. I do not independently certify the domain semantics of individual grid events; that belongs to the power-grid reviewer and qualified human annotators.

The manuscript is substantially more honest and auditable than the source concept: it explicitly calls the graph a textual proxy, reports the negative counterfactual ablation, identifies machine labels as silver, supplies exact frozen numbers, and compiles cleanly. The engineering-NLP topic is within the broad scope of *Applied Sciences*. However, the exact title promises maintenance-report validation and a causal/counterfactual enhancement that the current experiment does not establish. The measured corpus is a small set of NERC reliability/disturbance reports, not maintenance reports; the counterfactual channel is unsupported at five sentences and unfavorable at ten; and no expert assessment establishes causal fidelity or engineering usefulness. In addition, the live GitHub repository does not contain the v0.2 method and results described by this manuscript, while the R1 reproducibility manifest is a stale FEVER-era bundle rather than the frozen original-title experiment. These are claim-integrity and reproducibility blockers, not cosmetic shortcomings.

## Five most serious issues, ordered by decision impact

### 1. The exact title is not supported by the evaluated document population

- **Classification**: **Blocking / Critical**
- **Evidence anchors**:
  - `text: paper_applsci.tex:12 "for Power Grid Maintenance Reports"`
  - `text: paper_applsci.tex:63 "the measured corpus is described precisely as public NERC reliability and disturbance reports"`
  - `text: paper_applsci.tex:217 "not utility-internal work orders"`
- **Finding**: The manuscript itself concedes that “maintenance reports” is an intended use rather than the sampled document class. Reliability event analyses, disturbance reviews, storm reports, and lessons-learned documents are related engineering texts, but they are not interchangeable with maintenance work orders, inspection reports, defect records, or preventive/corrective maintenance reports. A limitation paragraph cannot cure a title–population mismatch. Readers, indexers, and editors will reasonably infer that the system was evaluated on maintenance reports.
- **Required revision**: Because the author requires the original title to remain, add a genuinely maintenance-report evaluation set with an explicit source/provenance/license table and a report-level split. If that is impossible, scientific accuracy requires changing the title; retaining the exact title without maintenance data is not acceptable.
- **Acceptance test**: A frozen manifest identifies maintenance-report documents by type and source; the Results contain a separately reported maintenance-report test set; all title/abstract/conclusion statements describe the measured population without redefining “maintenance” as a use case. At least one qualified power-grid reviewer confirms that the included documents are maintenance reports under an explicit operational definition.

### 2. The named causal/counterfactual contribution is not validated as an enhancement

- **Classification**: **Blocking / Critical**
- **Evidence anchors**:
  - `text: paper_applsci.tex:51 "Removing a graph node and its incident edges measures how much registered graph flow depends on that sentence"`
  - `text: paper_applsci.tex:154 "provides no evidence that graph-flow counterfactual sensitivity improves five-sentence overlap"`
  - `text: paper_applsci.tex:205 "cannot be presented as an effective innovation in its current form"`
  - `table: paper_applsci.tex:178-184, Table 2 — Graph without CF is higher than Full on all three reported ROUGE means at K=10`
- **Finding**: The paper truthfully shows that the counterfactual channel does not improve the primary metric and may reduce ROUGE-1 at the longer budget. The graph edges are lexical/role-compatible proxies, with no human causal-relation gold, structural causal model, intervention ground truth, or physical-grid validation. Accordingly, “causal” describes an imposed role schema and “counterfactual” describes node deletion; neither is yet an empirically validated source of enhancement. The title and acronym make these the paper's defining novelty, so a negative/unsupported component cannot be left as if it substantiated the named method.
- **Required revision**: Either (a) redesign the CF component using only a frozen development protocol, validate causal-role/edge quality independently, and test the frozen redesign on a genuinely unseen sealed holdout, or (b) reposition the paper as a negative-results/auditable proxy-graph study and reduce all “enhanced” and causal-effect implications. Because the exact title is being retained, option (a) is the viable path for this project.
- **Acceptance test**: The revised paper reports an expert-validated edge/role task and a strict single-factor counterfactual ablation on a sealed holdout not inspected during R1 development. It reports effect sizes and uncertainty on the primary metric. If the CF benefit remains unsupported, the title/abstract/conclusion must not imply that CF improves summarization.

### 3. The experiment is too small and too indirect for the claimed engineering application; the proposed reuse of the observed test set is not confirmatory

- **Classification**: **Blocking / Major**
- **Evidence anchors**:
  - `dataset: corrected NERC benchmark — 28 retained reports, only 16 test reports, described at paper_applsci.tex:65 and 221`
  - `text: paper_applsci.tex:221 "ROUGE does not measure engineering usefulness, factual sufficiency, or causal correctness"`
  - `text: paper_applsci.tex:227 "one-shot evaluation on the unchanged 16-report test set"`
- **Finding**: Sixteen test reports support a bounded pilot, not a strong journal-level application claim. The only external quality target is overlap with official Executive Summaries; there is no expert judgment of causal-chain coverage, factual sufficiency, equipment/entity preservation, actionability, or harmful omission. Moreover, the R1 test outcomes are already known and discussed. A redesigned R2 method evaluated on the same 16 reports cannot become a fresh confirmatory “one-shot” test merely because its code is frozen after development; knowledge of R1 test behavior can influence redesign decisions.
- **Required revision**: Reserve a new sealed holdout, preferably containing actual maintenance reports and multiple document subtypes. Pre-register the development objective and redesign choices before opening that holdout. Add independent qualified-domain evaluation, stronger contemporary extractive baselines, and a leakage/near-duplicate audit between Executive Summaries and candidate bodies.
- **Acceptance test**: The protocol timestamps and hashes the sealed holdout before algorithm redesign; no holdout-derived metric appears in development records; expert evaluation includes a manual, independent blinded ratings, retained disagreements, adjudication, agreement statistics, and uncertainty. The old 16-report set remains explicitly exploratory if reused.

### 4. The public repository and the frozen R1 package do not support the manuscript's current code/data-availability claim

- **Classification**: **Blocking / Critical**
- **Evidence anchors**:
  - `text: paper_applsci.tex:244 "Public code and license-cleared reproducibility materials are available at https://github.com/gaoxingkele/c2ges"`
  - `text: paper_applsci.tex:239 "The reproducibility package contains ... frozen v0.1 and v0.2 configurations ... both completed v0.2 run directories"`
  - `dataset: live GitHub repository HEAD d247219e0f8685186616298a338a475bee1810c4 — checked 2026-08-08; no formal_config_v0.2.json, run_formal_experiment_v0_2.py, C2GES_NERC_FORMAL_v0_2 run, aggregate_metrics.json, paired_bootstrap.json, or NERC Executive Summary benchmark`
  - `dataset: R1/reproducibility/bundle_manifest.json — 11,673 artifacts / 2,196,680,670 bytes, dominated by the older FEVER evidence-selection workspace and lacking the original-title v0.2 formal artifacts`
- **Finding**: The live repository currently describes a different working title and task: causal-role-conditioned evidence sentence selection over 200 questions. It does not expose the implementation and frozen outputs underlying this manuscript. Separately, `ROUND_AUDIT.json` reports `PASS`, but its file inventory does not freeze the authoritative v0.2 configuration, dataset, code, predictions, aggregate metrics, and bootstrap outputs together with the manuscript. The bundled manifest is stale and not a substitute for the missing original-title package. Thus, the current availability statement is materially misleading.
- **Required revision**: Publish or prepare an editor-accessible, immutable release specific to this manuscript. It must contain the exact v0.2/vNext code, configs, testable data representation or acquisition manifest, exclusions, predictions, statistics, figure-generation scripts, licenses, and hashes. Use a release/tag/commit or DOI and cite that immutable identifier. Regenerate `ROUND_AUDIT.json` and the bundle manifest from the exact round contents; do not include failed builds or unrelated FEVER assets as if they were the domain package.
- **Acceptance test**: From a fresh directory, an auditor can obtain the declared package, verify every hash, run tests, regenerate Tables 1–2 and Figure 2, and match the final PDF numbers. A repository-tree check finds every manuscript-named artifact. The Data Availability Statement distinguishes public code, public derived data, third-party source PDFs, and confidential editor/reviewer materials item by item.

### 5. Mandatory author-side and GenAI disclosures are incomplete or insufficiently specific

- **Classification**: **Blocking for portal upload / Major**
- **Evidence anchors**:
  - `text: paper_applsci.tex:17 "email address to be provided before submission"`
  - `text: paper_applsci.tex:245 "AI-assisted tools were used for drafting, editing, code review, and reproducibility checks"`
  - `text: paper_applsci.tex:69 "machine workflows"`
  - `absence: Acknowledgments and data provenance — expected GenAI tool/provider, model/version, exact purpose, and affected content; checked paper_applsci.tex:67-69, 239-246, ASSEMBLY_AUDIT_R1.md`
- **Finding**: The corresponding-author email is an acknowledged hard placeholder. The AI disclosure is generic and does not identify the tools/models/versions or clearly distinguish their roles in text drafting, code, figures, dataset construction, machine-silver labels, analysis, and interpretation. The local requirements snapshot explicitly requires tool/purpose and author responsibility. Current MDPI guidance also expects a specific disclosure when GenAI was used for text, data, graphics, study design, collection, analysis, or interpretation. The funding-project name and no-funder-role statement also require explicit author confirmation rather than inheritance from an automated rebuild.
- **Required revision**: Obtain author-approved email, CRediT roles, funding agency/project wording, conflict statement, and funder-role statement. Expand the GenAI disclosure into a tool-by-tool record with provider, model/version/date where known, purpose, outputs affected, human verification, and a clear statement that LLM-generated labels are not expert annotation. If version information cannot be recovered, state that limitation rather than inventing it.
- **Acceptance test**: No manual placeholder remains; both authors approve the final PDF and declarations; the disclosure is specific enough for an editor to understand every GenAI role; the data/provenance ledger points from each machine-produced label or figure to its generator and verification status.

## Claim–evidence audit

| Manuscript claim | Location | Evidence status | Integrity verdict / required action |
|---|---|---|---|
| The method is for power-grid maintenance reports | Title; Abstract; Featured Application | **Not demonstrated** | Current data are NERC reliability/disturbance reports. Add actual maintenance data or change the title. |
| The graph is “causal” | Abstract; Sections 3.3 and 5.2 | **Mechanistically supported only as a typed textual proxy** | Keep the proxy boundary in every high-visibility claim; add independent edge/role validation before claiming causal fidelity. |
| Node deletion is “counterfactual” | Sections 3.4 and 5.2 | **Implementation verified; causal interpretation not validated** | Prefer “graph-flow node-deletion sensitivity” in technical claims unless a causal estimand and assumptions are supplied. |
| Counterfactual enhancement improves summarization | Title implication; Results and Discussion | **Refuted/unsupported by R1** | The manuscript reports this honestly. The title-level implication still requires redesign plus sealed validation or a title change. |
| 40 source reports, 28 eligible, 12 development, 16 test | Abstract; Section 3.1 | **Supported locally** | Counts and dataset SHA agree with the v0.2 evidence. Add a report-level appendix with IDs, type, year, split, inclusion/exclusion, URL/hash, and license. |
| Seven conditions, two budgets, 224 rows | Abstract; Sections 3.6, 4.4 | **Supported locally** | `16 × 7 × 2 = 224`; both runs have matching core hashes. Preserve exact artifacts in the round package. |
| Full at K=5: 0.2608/0.0934/0.1323 | Abstract; Table 1 | **Supported** | Matches `aggregate_metrics.json`. |
| Full–Lead and Full–TextRank R-1 intervals exclude zero at K=5 | Abstract; Section 4.1 | **Supported but exploratory** | Matches paired-bootstrap output. Keep the multiplicity caveat and do not call it general superiority. |
| Full has no demonstrated CF benefit; K=10 R-1 interval is negative | Abstract; Section 4.2; Conclusions | **Supported** | Matches v0.2. This is the strongest integrity feature of the manuscript but weakens the named innovation. |
| Two executions are byte-identical | Abstract; Section 4.4 | **Supported locally** | Say “two complete executions” rather than implying independent-team validation unless a different analyst performed the second run. |
| Public code/materials are available in the cited GitHub repository | Data Availability | **False as of 2026-08-08 for this manuscript's v0.2 method** | Synchronize and release the exact package before retaining this sentence. |
| Restricted materials can be supplied for editor/reviewer verification | Data Availability | **Promise not yet verified** | Produce and audit the actual editor packet; include a third-party permission/license matrix. |

## Experiment audit

### Required before a submission candidate

1. **Title-concordant domain set**: a frozen test set of actual preventive/corrective maintenance, inspection, defect, or work-order reports, with document-type criteria and permissions.
2. **New sealed holdout**: do not promote the already inspected 16-report set to confirmatory status after R2 redesign.
3. **Qualified human evaluation**: at least two independent domain reviewers plus adjudication for causal role/edge correctness, engineering sufficiency, factuality, equipment/entity preservation, mitigation/action coverage, and harmful omission. Report agreement and denominators. An LLM panel may assist pre-annotation but cannot be called expert adjudication.
4. **Strict CF test**: a single-factor ablation using a development-frozen redesign; report the primary metric and interval first, including a negative result if retained.
5. **Stronger fair comparators**: include at least one modern extractive neural baseline and one strong LLM/extractive selector under identical candidates, budgets, and information access, plus a reference/oracle ceiling. Existing Lead, centroid, TextRank, role-only, and MiniLM centroid are useful but not sufficient to establish current value.
6. **Leakage and representativeness audits**: near-duplicate checking between Executive Summaries and candidate bodies; report subtype/year/source distribution; document exclusions; and sentence-candidate truncation effects.
7. **Multiplicity plan**: predeclare a small confirmatory comparison family or adjust it. Preserve the full exploratory family separately.

### Desirable but not blocking if limitations remain explicit

- Cross-corpus validation across at least two organizations or report genres.
- Per-genre and per-length effects with uncertainty, not only pooled means.
- BERTScore or another semantic metric as secondary evidence, accompanied by human evaluation rather than replacing it.
- Runtime, memory, and failure-mode comparisons for the actual deployed pipeline.
- Error taxonomy and source-linked case studies showing cause/trigger/propagation/impact/mitigation coverage.
- Sensitivity analysis for sentence segmentation and graph-edge distance thresholds, performed only on development data.

### Reruns that would be unjustified or misleading

- Tuning CF weights, graph transitions, budgets, or stopping rules against the already viewed 16-report R1 test results.
- Increasing bootstrap replications while leaving the number/diversity of reports unchanged and presenting that as stronger evidence.
- Replacing qualified domain experts with LLM calls and relabeling their agreement as “expert adjudication.”
- Selecting only the budget or ROUGE metric that favors Full.
- Adding unrelated FEVER evidence-selection results as if they strengthen maintenance-report summarization validity.

## Figure, table, and layout audit

### What passes

- The final PDF is 11 A4 pages and contains no fully blank page.
- No unresolved citation, cross-reference, fatal LaTeX error, multiply defined label, or overfull box was found in the final Run-04 log.
- Figures 1 and 2 are legible when zoomed, captions state important limitations, and every figure/table is called from the text.
- Figure 2 values match the frozen aggregate JSON and its lineage record.
- Tables 1 and 2 use consistent denominators and clearly state that bold indicates observed maxima only.

### Required or major improvements

- Figure 1 is included from `fig_c2ges_implemented_architecture_r1_qa2.png`, a QA-named raster derivative, while the native SVG exists. Convert the SVG to submission-safe vector PDF/EPS and cite that artifact; do not ship a draft/QA filename as the canonical figure.
- Figure 2 plots only means although paired uncertainty is central to the paper. Add a compact forest plot for the predeclared Full-minus-baseline contrasts and the strict CF contrast; retain the current grouped bars only if they add information.
- Add a dataset-flow diagram/table showing 40 screened, 12 excluded by reason, 28 retained, 12 development, and 16 test. This is more valuable than carrying unused FEVER-era framework figures in the directory.
- The architecture figure's smallest explanatory text is borderline at printed full-page scale. Minimum final font size should be checked in the vector export.

### Minor layout issues

- Page 11 has substantial unused lower-page space but is not a blank page; this is acceptable and does not warrant content padding.
- The template footer says “Version August 5, 2026” although the round is dated August 8. Regenerate from the current template metadata.
- Remove failed/literal `$outputDir` builds and obsolete figures from the submission ZIP, while preserving them in an internal accident archive with an exclusion manifest.

## Reproducibility and data/license audit

| Item | R1 status | Required disposition |
|---|---|---|
| Frozen v0.2 config and hashes | Exists outside R1 | Copy/reference through an immutable round manifest and verify paths from a fresh directory. |
| Predictions, aggregates, bootstrap output | Exists locally; two core-hash matches | Include in the editor/reviewer package and repository release where licensing permits. |
| R1 `ROUND_AUDIT.json` | Mechanically `PASS` | Regenerate with the authoritative experiment artifacts; the current PASS is too narrow to satisfy the three-round protocol. |
| `bundle_manifest.json` | Stale FEVER-oriented 2.2 GB workspace inventory | Replace with a manuscript-specific minimal manifest; unrelated assets obscure rather than improve reproducibility. |
| Public GitHub | Public, MIT code license, HEAD `d247219e...` | Does not contain this manuscript's method/results. Create a tagged release and update README/title/task. |
| NERC source and derived-text rights | Source URLs/hashes exist; redistribution boundary asserted | Provide a per-artifact rights matrix. Do not apply the repository's MIT license to third-party text by implication. |
| Local MiniLM model | Revision and tree hash recorded | Give acquisition instructions and upstream license; do not redistribute model weights without checking that license. |
| Figures | Lineage exists | Canonicalize source-to-vector conversion and include all generation scripts in the released package. |

## Authorship, ethics, and submission-completeness audit

- **Authors/affiliations**: Liu Bijing and Yang Yong, both affiliations, and Yang Yong as corresponding author are rendered consistently. The email placeholder blocks portal upload.
- **CRediT**: Roles and the “All authors have read and agreed…” sentence are present. Both authors must confirm that the listed roles reflect actual contributions, especially software, validation, data curation, and funding acquisition.
- **Funding**: Grant `521300250006` is present. The full project/agency name and the no-role-of-funder claim require author/institution confirmation.
- **IRB/consent**: “Not applicable” is reasonable for public documents and the non-human experiment. Any future expert annotation study must separately determine whether institutional review/consent is required for the human participants and record that determination before recruitment.
- **Conflicts**: A declaration is present but still requires author sign-off.
- **AI/LLM disclosure**: Insufficiently specific; see Blocking Issue 5. It must cover machine-silver labels as data construction, not only writing/code review.
- **Data availability**: The requested third-party-permission wording is present, but current repository/package reality does not support the statement. Availability must be described artifact by artifact.
- **Citations**: The 21 rendered references are cited and resolve in the final build. The bibliography is credible and relevant at a broad level, but the paper lacks a direct maintenance-report summarization comparison and should not use general grid-AI surveys as a substitute for task-specific prior art. Any claim that no directly comparable work exists must be supported by a documented search, not asserted from absence.
- **Meta-reconstruction language**: Lines 31 and 65 narrate unsupported claims in the old concept and a failed build. Preserve the provenance in the audit/supplement, but rewrite the article itself as a conventional research report. Readers do not need the history of an unsubmitted source draft to understand the method.

## Decision register

### Blocking items

1. Title–dataset mismatch.
2. No validated benefit or causal fidelity for the defining causal/counterfactual enhancement.
3. No new sealed, title-concordant holdout or qualified expert evaluation.
4. Public repository and frozen package do not contain the current manuscript's evidence.
5. Corresponding email and specific GenAI/provenance disclosures are incomplete.

### Major items

- Stronger contemporary baselines and a declared confirmatory comparison family.
- Replace the proposed reuse of the observed R1 test set with a new sealed holdout or label all follow-on tests exploratory.
- Manuscript-specific data/license matrix and editor verification packet.
- Remove reconstruction-process narration from the scientific body.
- Add uncertainty-focused and dataset-flow visualizations.

### Minor items

- Use canonical vector figure files and remove `qa2` from submission filenames.
- Update the template version date.
- Clean the submission ZIP of failed builds and unrelated figures, retaining a separate immutable internal accident archive.
- Standardize “counterfactual sensitivity” to “graph-flow node-deletion sensitivity” wherever no causal estimand is intended.

## R1-to-R2 acceptance conditions

R2 should not be frozen until all of the following are demonstrably true:

1. A response matrix assigns every blocking item an owner, concrete artifact, and verification command.
2. The exact-title strategy is resolved with actual maintenance-report data; otherwise the title decision is reopened.
3. The R2 method-development protocol is frozen before a new sealed holdout is accessed.
4. Human domain-evaluation protocol, annotator qualifications, consent/ethics determination, manual, disagreement retention, and adjudication are documented before labeling.
5. The public or confidential-review repository contains the exact current code/data/results, and a fresh clone/package reproduces all manuscript tables and figures.
6. The Data Availability, AI disclosure, funding, CRediT, conflict, and correspondence fields are author-approved and factually complete.
7. A regenerated audit hashes the manuscript, PDF, bibliography, every used figure/table source, frozen data/config/code, predictions, and statistical outputs together. It must exclude obsolete/failed runs from the evidentiary set while retaining them in a separately labelled accident archive.

## External verification note

External checks were performed on **2026-08-08 (Asia/Shanghai)** and were limited to the journal policy and the author-provided repository:

- [MDPI Layout Style Guide](https://www.mdpi.com/authors/layout): confirms the expected front matter, research-article structure, figures/tables, Author Contributions, Funding, Data Availability, ethics statements, conflicts, and references. Direct page retrieval returned HTTP 429 during this review; the search-indexed official page and the frozen local requirements snapshot dated 2026-08-08 were used for the policy checklist.
- [Applied Sciences journal and scope](https://www.mdpi.com/journal/applsci) and [Aims & Scope](https://www.mdpi.com/journal/applsci/about): the engineering/NLP application is in broad scope, but scope fit does not cure title/evidence mismatch.
- [C2GES public GitHub repository](https://github.com/gaoxingkele/c2ges): public `main` HEAD was `d247219e0f8685186616298a338a475bee1810c4`, last pushed 2026-07-20 UTC. Its visible README and recursive tree describe the earlier evidence-selection package and do not contain the original-title v0.2 formal experiment named in the manuscript.

No unpublished manuscript text, private corpus, or private experimental artifact was uploaded to an external model or service during this review.
