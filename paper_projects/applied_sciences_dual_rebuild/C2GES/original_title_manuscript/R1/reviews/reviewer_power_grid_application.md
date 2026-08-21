# Round 1 Independent Review — Power-Grid Application

## Reviewer identity and scope

Independent domain reviewer with a power-system event-analysis, reliability-report engineering, and operational decision-support perspective. This review evaluates the frozen Round 1 TeX/PDF, assembly audit, protocol-v0.2 outputs, and NERC dataset-construction records. It does not edit the manuscript and does not assess author identity.

## Recommendation

**Major revision.** The negative counterfactual result, deterministic reproduction, and explicit safety disclaimers are valuable. However, the present evidence does not yet support the manuscript's report-level maintenance application. The most serious defect is that the candidate texts are inherited event-focused/agent-audited sentence collections rather than a reproducible segmentation of each complete report body. In 31 of the 40 upstream records the sentence count is exactly 80, and the upstream manifest itself describes some records as “event-focused excerpts.” The formal predictions also retain headers, page markers, table fragments, and mojibake; 11 of 16 five-sentence Full outputs match at least one such contamination pattern. Consequently, current ROUGE values characterize selection from a truncated and noisy excerpt pool, not summarization of complete maintenance reports. The corpus is also a heterogeneous convenience set of NERC disturbance, reliability, storm, recommendation, and assessment documents, not an evaluated sample of utility maintenance reports. The paper is unusually candid about proxy causality and the failed counterfactual component, but it still needs full-document reconstruction, domain-quality validation, and a per-document rights ledger before the application claim is credible.

**Confidence:** 5/5 (based on direct inspection of the frozen manuscript, builder, source and build manifests, prediction ledger, figures, and reproduced aggregate report).

## Five highest-impact issues

### W1. The experiment does not summarize complete report bodies

**Classification:** Blocking  
**Severity:** Major  
**Evidence Anchor:** `dataset: build_nerc_summary_dataset.py lines 114–115 reads source["sentences"] from pre-existing agent_audit_40doc JSON; its manifest describes event-focused excerpts, and 31/40 JSON records contain exactly 80 sentences`  
**Confidence:** 5/5 — direct code and corpus inspection.

The paper states that candidates come from “the segmented body” and repeatedly calls the task report summarization (TeX lines 61–65, 203, and 233). The builder does not segment full PDFs into candidates. It extracts the Executive Summary from each PDF, but candidates are sliced from an already-existing `agent_audit_40doc` record. That upstream asset was created for five-role causal QA and explicitly notes that some annual/reliability documents are event-focused excerpts. The exact 80-sentence ceiling in most records is not disclosed. This is a scope-changing provenance defect, not a minor parsing detail.

**Required modification and acceptance test:** Build a new immutable candidate corpus directly from every complete source PDF using a frozen, tested section/header/table cleaning and sentence segmentation pipeline. Record full-PDF page and sentence counts, retained/excluded regions, sentence-to-page offsets, and truncation status for every document. No unexplained common sentence ceiling is permitted. Run all frozen comparators and both budgets again in new directories. A verifier must reconstruct every candidate row from PDF hash plus code/config alone and confirm that the manuscript consistently says either “full report body” or the narrower actual unit.

### W2. The title population and measured population do not match

**Classification:** Blocking  
**Severity:** Major  
**Evidence Anchor:** `text: paper_applsci.tex line 63, “maintenance reports” denotes intended use while the measured corpus is NERC reliability and disturbance reports`  
**Confidence:** 5/5 — power-grid document-type assessment.

The 40-document source is a convenience collection spanning event reports, annual State of Reliability reports, hurricanes, special assessments, recommendations, and an EMS assessment. It is not a sampling frame for utility maintenance work orders, inspection reports, defect records, or maintenance completion reports. Retaining the original title is an authorial choice, but a limitation paragraph cannot convert a reliability/disturbance benchmark into evidence for maintenance-report performance. Selection by the presence and parser-detectability of an Executive Summary further favors publication-style reports and excludes many operational maintenance genres by design.

**Required modification and acceptance test:** Either (a) add a license-cleared, sealed evaluation set of genuine maintenance reports with a documented genre taxonomy and report-level split, or (b) make every title-adjacent, abstract, contribution, featured-application, discussion, and conclusion claim explicitly about NERC reliability/disturbance report excerpts and present maintenance use only as untested transfer. Provide a document table with year, report genre, event/asset type, length, inclusion reason, split, and exclusion reason. The test set must be checked for genre and time coverage; hash assignment alone is insufficient evidence of representativeness.

### W3. ROUGE against Executive Summaries does not establish engineering usefulness, and current outputs contain operationally material noise

**Classification:** Blocking  
**Severity:** Major  
**Evidence Anchor:** `dataset: formal_runs/C2GES_NERC_FORMAL_v0_2_20260808_run01/predictions.jsonl; 11/16 K=5 Full predictions contain at least one inspected header/page-marker/mojibake pattern such as “<Public>”, spaced running titles, or “鈥”`  
**Confidence:** 5/5 — direct output inspection and reliability-report use assessment.

Official Executive Summaries are legitimate reference text, but they are long (reported median 790.5 words), editorially structured, and not independent judgments of what a five- or ten-sentence engineering briefing must contain. ROUGE measures lexical overlap, not whether an extract preserves the initiating contingency, chronology, equipment identity, protection/control response, magnitude, root cause, recommendations, uncertainty, or safety caveats. The actual selected sentences sometimes include running headers, page markers, malformed dashes, table fragments, or broken report titles. Such artifacts can obscure equipment names and relationships and are unacceptable for an engineering navigation aid. Moreover, K=5 Full silver coverage is 0.375 (about 1.875 of five registered roles per report when all five roles are present), so the current diagnostic does not demonstrate preservation of a full causal/operational chain.

**Required modification and acceptance test:** Add deterministic text-quality gates and publish their per-document failure counts; no selected sentence may contain page headers/footers, access markers, encoding corruption, or unparsed table rows unless explicitly labeled as a table extract. Conduct a sealed, blinded evaluation by qualified power-system reviewers on at least coverage of event/cause/response/impact/mitigation, equipment-and-quantity fidelity, chronology, critical-omission risk, and navigation usefulness. Retain individual ratings and disagreements; report agreement and adjudication separately. LLM-only labels may be exploratory but must not be called expert validation. Include representative success and failure cases with source-page anchors.

### W4. The five-role proxy graph is auditable but not validated as a causal event model

**Classification:** Blocking for causal/engineering-effectiveness claims; non-blocking for release as a deterministic textual baseline  
**Severity:** Major  
**Evidence Anchor:** `text: paper_applsci.tex lines 75–79, “Direction follows role semantics rather than narrative order” and edges “have not been validated as physical causal relations”`  
**Confidence:** 5/5 — causal event-analysis and grid-domain reasoning.

The paper correctly disclaims physical causality, but the fixed transition set can still connect unrelated sentences within 12 positions and can orient edges against report chronology. The role inventory merges materially different concepts (for example, propagation with system response, and cause with trigger in the selection reserve groups). Machine-produced silver evidence can break lexical ties and is then evaluated by a silver-coverage diagnostic derived from the same layer. No role confusion matrix, edge-validity sample, temporal-consistency audit, or expert event-chain coverage is available. The strict no-CF method performs at least as well as Full, so the title's “counterfactual” component is implemented but not shown to add value.

**Required modification and acceptance test:** Freeze a role/edge annotation manual that distinguishes report assertions from inferred links. On a sealed document sample, obtain independent domain labels for sentence roles, directed links, temporal order, and “insufficient evidence/no link”; retain disagreement and adjudication. Report role-wise precision/recall, directed-edge precision, invalid cross-event link rate, and whether the selector covers a coherent chain. Rename the diagram node to “typed textual proxy graph” and ensure every causal/counterfactual claim says “proxy-graph” unless supported by this validation. Do not tune a revised CF score on the current test set.

### W5. Public accessibility is documented, but redistribution and derivative-use permissions are not

**Classification:** Blocking for data/package release and submission data statement  
**Severity:** Major  
**Evidence Anchor:** `absence: data/public_datasets/reliability_reports/c2ges_nerc_reports/metadata/c2ges_nerc_report_manifest.json — expected per-document license/copyright/redistribution fields; checked all manifest fields and R1 data-availability text`  
**Confidence:** 4/5 — direct provenance audit; final legal determination remains with the authors/institution.

The source manifest records title, URL, local path, and download status, but no license text, copyright holder, derivative-data permission, or access date. The derived JSONL contains verbatim Executive Summaries and candidate sentences. The manuscript prudently says that source PDFs will not be redistributed where permissions do not allow it, yet it also refers to “license-cleared reproducibility materials” without an auditable rights decision. A public URL is not itself evidence of redistribution permission.

**Required modification and acceptance test:** Produce a per-document rights ledger with source URL, access date, rights holder, governing terms/license locator and captured hash, permitted local processing, permitted quotation, permitted redistribution of PDF/text/derived rows, and reviewer-only access conditions. Have the responsible human/institution approve the ledger. The public package must include only assets whose redistribution is affirmatively allowed; otherwise distribute hashes, URLs, code, and non-verbatim metadata, with a controlled editor/reviewer verification procedure. Make the Data Availability Statement match the approved ledger exactly.

## Claim–evidence audit

| Manuscript claim | Location | Evidence verdict | Required action |
|---|---|---|---|
| A benchmark was constructed from 40 public NERC reports, with 28 retained and 12/16 dev/test. | Abstract; lines 63–65 | **Partly supported.** Counts, hashes, and exclusions are traceable. “Public” means accessible URLs; rights are not established. Candidate inputs are pre-existing excerpts rather than reproducibly segmented complete bodies. | Rebuild full candidates and add sampling/rights ledgers. |
| The method summarizes power-grid maintenance reports. | Title; lines 27, 63, 215–217 | **Not supported by the measured population.** The test set contains NERC reliability/disturbance/assessment documents and no demonstrated utility maintenance-report sample. | Add genuine maintenance evaluation or narrow all performance claims to NERC documents. |
| The five roles preserve an event-to-mitigation chain. | Lines 67–79, 109–117 | **Method implemented; engineering validity unverified.** Role evidence is machine silver, fixed transitions are proxy rules, and observed silver coverage is incomplete. | Add sealed expert role/edge/chain evaluation. |
| Full C²GES improves over Lead and TextRank. | Abstract; lines 129–156 | **Supported only for K=5 ROUGE-1 on the current noisy excerpt benchmark.** ROUGE-2/L intervals cross zero; no broad method superiority follows. | Preserve bounded wording and rerun after full-document cleaning. |
| Counterfactual sensitivity is beneficial. | Title/method name versus lines 154–156, 203–211 | **Explicitly not supported.** The manuscript reports this negative result correctly. | Retain the negative result; do not claim component effectiveness. |
| The output is source-traceable decision support. | Featured Application; lines 81–87, 213–217 | **Traceability mechanism is supported; decision-support utility is untested and text quality is currently inadequate.** | Add page anchors, text-quality gates, and blinded domain-use evaluation. |
| Two independent executions are exactly reproducible. | Abstract; lines 191–193 | **Supported for frozen predictions, aggregates, and bootstrap artifacts.** | Preserve hashes; extend reproduction to the full PDF-to-candidate pipeline. |

## Experiment audit

### Required reruns

1. **Full-PDF corpus reconstruction and complete rerun:** regenerate candidates from complete PDF bodies, freeze preprocessing, retain every failed parse, and rerun all seven conditions at both budgets in new immutable directories.
2. **Parser and encoding audit:** inspect every included report for summary boundaries, section boundaries, header/footer removal, tables, hyphenation, encoding, and sentence-to-page alignment. Report failure rates before presenting aggregate accuracy.
3. **Population/genre evaluation:** define the NERC sampling frame and strata. If the title remains unchanged, add a sealed genuine-maintenance test set; otherwise treat maintenance as future transfer.
4. **Domain evaluation:** qualified reviewers must assess engineering completeness, critical omission, chronology, equipment/quantity fidelity, and usefulness. Human adjudication must remain distinct from model-assisted pre-labeling.
5. **Role/edge validation:** evaluate the five role labels and directed proxy edges against sealed independent domain judgments, including “no relation/uncertain.”

### Desirable additions

- Compare token- or word-matched budgets in addition to sentence counts, because sentence length varies markedly in technical reports.
- Add section-aware and long-document extractive comparators, plus an oracle upper-bound diagnostic on the same clean candidates.
- Report per-genre and per-length results with case-level failure analysis rather than only pooled means.
- Evaluate whether selected recommendations retain conditions, responsible entities, quantities, and uncertainty language.

### Unjustified reruns or claims

- More bootstrap samples on the current excerpt/noise-contaminated corpus would not repair construct validity.
- Do not tune the CF formulation, weights, or role transitions on the 16 frozen test reports.
- Do not replace qualified human review with LLM-only “expert” adjudication or relabel silver coverage as causal fidelity.
- Do not infer physical grid causality, operational safety, or autonomous root-cause analysis from ROUGE or proxy-graph flow.

## Figure and table audit

### Figure 1 — implemented architecture

**Verdict:** Legible and unusually transparent about no GNN, no model API, node deletion, and non-gold silver evidence. However, “Typed causal event graph” remains stronger than the validated object. The diagram omits that candidates originate from a pre-existing excerpt/QA asset, omits full-PDF preprocessing and text-quality failures, and does not show the mandatory human review gate.

**Required change:** Rename the block “Typed textual proxy graph”; add the actual source lineage (PDF → full-body parser/cleaner → sentence/page IDs), show machine-silver provenance as an optional input, and add an explicit output-quality/human-review gate. Acceptance requires that every displayed dependency match executable code and the frozen lineage record.

### Figure 2 — ROUGE by budget

**Verdict:** Values and labels are legible, and the caption correctly calls them descriptive means. It visually suppresses uncertainty and gives three overlap metrics equal prominence even though ROUGE-L is registered primary.

**Required change:** Add a separate paired-effect/interval panel for the primary metric or a forest plot of Full-minus-comparator intervals. Visually identify that Centroid leads observed ROUGE-L and strict no-CF leads observed ROUGE-1 at both budgets. Do not add error bars that are not derived from the retained report-level artifacts.

### Tables

**Verdict:** Tables 1–2 match the aggregate report, but the paper lacks the tables needed to judge the engineering population and parsing quality.

**Required change:** Add (i) a report inventory/genre/split/exclusion table, (ii) a preprocessing quality table with full-PDF and retained candidate counts plus contamination flags, (iii) role/edge validation results when available, and (iv) at least two page-anchored output cases, including one failure. Bold maxima must remain descriptive and not imply significance.

## Reproducibility audit

### Strengths

- Frozen v0.2 configuration, hash checks, immutable output directories, and retained failed builds are strong practices.
- Run 01 and Run 02 have byte-identical prediction, aggregate, and bootstrap hashes.
- The strict counterfactual ablation is genuinely single-channel and the negative result is reported.
- The architecture figure states the implemented boundaries instead of depicting an absent GNN or generator.

### Blocking gaps

- The PDF-to-candidate transformation is not end-to-end: the builder depends on pre-existing `agent_audit_40doc` JSON and cannot recreate its sentence list from the PDF source manifest.
- The upstream JSON provenance includes agent rewriting/verification and event-focused excerpt selection, but the manuscript describes candidates as the segmented report body.
- The public DOI/archive and final repository/license review are incomplete, as the assembly audit acknowledges.
- Reproducing identical outputs reproduces the same truncation and extraction noise; it does not validate the benchmark construct.

## Ethics, licensing, and operational-safety audit

- **Machine annotation:** Correctly disclosed as silver and not expert gold. Keep machine assistance, human qualification, independent ratings, and adjudication as separate provenance layers.
- **Copyright/licensing:** Not closed. Source accessibility and local processing are documented, but derived-text redistribution authority is not. This blocks a public data release and requires human/institutional review.
- **Operational safety:** The manuscript correctly says the system is navigation support, not autonomous root-cause analysis. This boundary should be operationalized with a mandatory source-page link, abstention/rejection path, quality flag, and human sign-off in any prototype.
- **Confidentiality:** No confidential utility work orders are in the current corpus. Any future maintenance-record experiment needs a separate data-use, redaction, access-control, and sealed-evaluation protocol.

## Minor issues

1. TeX line 65 reports the test reference range as 279–2298 words, while the build manifest includes longer development references; explicitly label every range as test-only and provide all-split statistics.
2. “Root cause” should not be assigned when a report states only a contributing condition, observed response, or unresolved cause; the annotation manual must allow “unknown/not established.”
3. “Propagation or response” conflates system evolution with corrective/protection response. Report both separately in expert validation even if the implementation retains a merged score.
4. The auxiliary FEVER paragraph is not evidence of power-grid engineering value and distracts from the primary domain validation gap; retain it only as a clearly separated software/ranking audit.
5. The corresponding-author email placeholder and permanent archive identifier remain manual pre-submission blockers, as already recorded in the assembly audit.

## Round-1 acceptance checklist

- [ ] Complete PDF bodies, not capped QA excerpts, are deterministically reconstructed and independently verified.
- [ ] All selected text passes frozen header/footer/table/encoding quality gates.
- [ ] Corpus genre, date, length, inclusion, exclusion, and split distributions are published.
- [ ] Maintenance-report scope is either directly tested or consistently labeled as untested transfer.
- [ ] Qualified domain reviewers validate roles, edges, chain coverage, critical omissions, and navigation usefulness on a sealed set.
- [ ] Current test reports are not used to tune the counterfactual component.
- [ ] A per-document rights ledger is approved and the public/reviewer packages follow it.
- [ ] Figures expose actual PDF-to-output lineage and the proxy/human-review boundaries.
- [ ] All revised numerical claims trace to new immutable run artifacts and an independent reproduction.

