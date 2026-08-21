# MA-SQLGrid Round 1 Independent Domain and Venue Review

**Independent decision: MAJOR REVISION — not ready for submission.**

**Applied Sciences fit: Medium in the current form; potentially high after external validation.** The natural destination is the **Computing and Artificial Intelligence** Section. The paper concerns a database/LLM interface evaluated on power-grid-shaped data, not a power-system algorithm validated by load flow, dispatch, protection, or field operation. Routing it to an Energy or Electrical Engineering section would invite the wrong evidentiary expectations.

The strongest parts are unusually candid evidence boundaries, complete paired execution ledgers, independent re-execution of all 1440 canonical predictions, template-cluster uncertainty, retention of negative results, and clean separation of answer-shape conformity from execution correctness. The decisive weakness is application evidence: the only canonical accuracy study uses one synthetic, development-visible GridDB database with unresolved redistribution permission. RTS-GMLC and SimBench remain automatically generated, unreviewed pilots, and the diagnostic run exposes severe schema-grounding failure rather than external validation. This weakness cannot be repaired by expanding prose alone.

This review was read-only. It covered the Applied Sciences skill and shared MDPI model; the current TeX and 18-page PDF (SHA-256 `F16E24591586146A48B195F9937150C4D32984BE9F85CF55BDD11DF1CCBA7B4D`); the ten-paper Applied Sciences corpus; the reference audit; the canonical dual-backbone release; the RTS-GMLC and SimBench data reports; the 91-item human-review protocol; and the external Qwen diagnostic. The closest same-journal precedent, DKA-SQL (DOI `10.3390/app152011121`), was independently checked against the MDPI version-of-record metadata and article content.

## Venue summary

```text
[Target] Applied Sciences (MDPI)
[Fit] Medium — strong auditable computing method, but current power-grid application validation is synthetic and unsealed
[Contribution type] applied-method / reproducible factorial experiment / validation protocol
[Main evidence gap] human-reviewed external database evidence and competitive direct-precedent baselines
[Best-fit Section] Computing and Artificial Intelligence
[Official items to re-check] current Section name/scope / instructions / data policy / APC / Special Issue
[Top rejection risk] weak applied validation relative to DKA-SQL and an application-forward title
[Re-route suggestion] IEEE Access or a database/NLP venue if external grid validation cannot be completed
```

## Major issues

### R1-DV-M01 — The power-grid maintenance application is not yet validated

The title and featured application promise Text-to-SQL over power-grid maintenance databases (`paper_applsci.tex:13,21`). However, the sole canonical accuracy source is GridDB, which the paper itself identifies as one synthetic maintenance-oriented database whose 180-question evaluation partition was exposed during prior development (`paper_applsci.tex:34,86,319`). The two public grid resources are not quantitative external evidence: zero of 91 natural-language/SQL candidates have completed human review, and all remain development-visible (`paper_applsci.tex:36,134–137,329`).

The external diagnostic makes the gap concrete. Qwen produced only 321 executable statements from 364 attempts, with 43 missing/ambiguous-column failures, and only 15 executions matched automatic candidate references; all 15 were SimBench and none were RTS-GMLC. The manuscript correctly refuses to call 15/364 accuracy (`paper_applsci.tex:201,285–287`). That honesty is commendable, but it leaves no observed external engineering effectiveness.

**Required new experiment:** complete two independent qualified reviews and third-person adjudication for all 91 existing candidates, then report them only as a human-reviewed **unsealed** set. Separately create a new access-controlled confirmatory set after schema/prompt repair is frozen: at least 50–100 questions, family-isolated, preferably spanning both RTS-GMLC and more than one SimBench network, with at least 15–20% genuinely human-authored or deeply rewritten questions. Freeze SQL, units, tie rules, result hashes, access logs, and method configuration before a one-pass evaluation of both backbones and all four factorial cells. Report each database separately, the all-attempt denominator, expert agreement/adjudication, and failure taxonomy. Without this experiment, retain the title only by making “synthetic benchmark study” explicit; otherwise the application claim is too strong for Applied Sciences.

### R1-DV-M02 — DKA-SQL is a stronger direct precedent than the present comparison acknowledges

The manuscript correctly cites DKA-SQL and states that MA-SQLGrid is not the first power-grid Text-to-SQL framework (`paper_applsci.tex:59`). The distinction it offers is a paired 2×2 prompt-factor analysis across two quantized backbones. That is a legitimate methodological distinction, but it is not yet a convincing applied advance relative to a same-journal article that evaluated BIRD (1527 validation questions) and ElecSQL (104 expert-authored power-grid supply-chain pairs), multiple 7B/14B/32B and proprietary models, direct/CoT/DIN-SQL/CHASE-SQL comparisons, and extraction/verification ablations.

At present, MA-SQLGrid compares four prompt cells but no competitive Text-to-SQL system. F00 is a useful internal direct-prompt reference, not a literature-level baseline suite. Consequently the paper can establish that hints affect its two local snapshots, but not that the framework is competitive, improves on a simpler domain pipeline, or offers practical value beyond DKA-SQL.

**Required new experiment:** run fresh, same-environment comparisons on at least one publicly distributable benchmark shared with the literature, preferably a registered BIRD validation subset plus the human-reviewed grid set from R1-DV-M01. Include a plain direct prompt, CoT/decomposition, one schema-selection/retrieval baseline, and one verification/repair baseline; use the released DKA-SQL implementation if it can be reproduced, otherwise implement a clearly labeled DKA-SQL-style comparator and avoid comparing incomparable published point estimates. Hold backbone, quantization, database snapshot, token budget, decoding, and scoring fixed. A compact closest-work table should then distinguish data, knowledge source, modules, models, metrics, and evidence status.

### R1-DV-M03 — The claimed multi-stage framework is only partially experimentally identified

The six-stage pipeline includes schema selection, value grounding, answer-shape guidance, generation, safety validation, and execution (`paper_applsci.tex:38,89`). The factorial experiment changes only schema scope and shape guidance. Value grounding and the validator are held fixed, and neither their isolated benefit nor their interaction with context is tested. The compact selector is described only as deterministic and question-conditioned; the paper does not state its scoring rule, thresholds, fallback policy, selected-table/column recall, token reduction, or join-path coverage (`paper_applsci.tex:96–98`). Thus the manuscript is currently a strong factorial study of two prompt interventions, not evidence for the effectiveness of a full multi-stage framework.

**Required action and experiment:** provide executable pseudocode or an algorithm box for full/compact serialization, value inventory construction, shape-hint derivation, and validation. Report per-question context tokens, selected table/column counts, gold-required schema recall used only offline for analysis, join-path retention, and omission-caused failures. Prospectively add at least `no value grounding` and a validator/candidate-replay comparison on identical raw candidates. If these experiments are not run, remove claims implying demonstrated benefit of every stage and present MA-SQLGrid explicitly as an audit framework for two-factor prompt evaluation.

### R1-DV-M04 — The evaluation contract is too weak to support semantic reliability claims

Strict result equality on one database state is reasonable as a primary automated endpoint, and the manuscript openly notes accidental equivalence (`paper_applsci.tex:158–171,325`). However, a single synthetic database state can reward nonequivalent SQL, while the separate answer-shape score only measures structural conformity. No test-suite databases, query perturbations, or human semantic audit estimate false-positive execution matches. This is particularly important when the paper motivates high-consequence engineering access.

**Required new experiment:** for a preregistered stratified sample of correct and incorrect GridDB predictions, obtain blinded SQL-intent adjudication or use distilled/perturbed database test suites that alter discriminating values while preserving schema. Report the confusion between single-state execution equality and semantic judgment. On external data, require expert review of question, SQL, units, projection, ordering, null behavior, and ties before scoring. The conclusion should use “execution equality on the frozen snapshot” unless stronger semantic evidence is added.

### R1-DV-M05 — Data governance currently blocks reproducibility of the headline experiment

The primary question set has no located redistribution license (`paper_applsci.tex:104–108,331,352`). Hashes prove local identity but do not let a reviewer reproduce the experiment. The local package is excellent, yet no permanent public DOI exists, and the paper cannot currently share its headline raw questions. SimBench has explicit ODbL/DbCL obligations; RTS-GMLC’s preserved notice is incomplete and awaits review. These are material data-availability issues for a journal that requires a Data Availability Statement.

**Required action:** before submission, either obtain written GridDB redistribution permission, replace the primary corpus with an openly distributable benchmark, or publish a regeneration route whose inputs and license genuinely permit independent reconstruction. Deposit the permitted code, prompts, predictions, manifests, data builders, environment lock, audits, and derived artifacts at a permanent DOI/URL. State exact exclusions and source-specific licenses. Do not treat the local workspace or hashes alone as public availability.

### R1-DV-M06 — Applied deployment claims need either controlled resource evidence or narrower wording

The paper discusses operational interfaces and compares two local backbones, but explicitly reports no common efficiency experiment (`paper_applsci.tex:304–314,327`). DKA-SQL makes efficiency part of its contribution, and deployment-oriented Applied Sciences readers will ask whether compact context reduces tokens, latency, or memory even though it does not improve accuracy. The current study cannot answer that question.

**Required experiment if operational/deployment framing is retained:** measure prompt tokens, generated tokens, warm and cold latency, throughput, peak host/accelerator memory, SQL execution time, failure/retry counts, and optionally energy on identical hardware and software boundaries. Report compact/full savings jointly with accuracy, not as a post-hoc Pareto claim. If this study is not run, keep efficiency entirely in Future Work and describe the contribution as accuracy/audit analysis rather than deployment optimization.

## Minor issues

### R1-DV-m01 — Manuscript size is acceptable, but methods are under-explained relative to visual density

The compiled article is 18 pages, approximately 5000 body words, six primary sections, seven displayed equation environments, eight figures, six tables, three framework diagrams, and five result figures. The local ten-paper sample has medians of 24 pages, 7098 body words, five sections, 26 equations, nine figures, five tables, two framework diagrams, and 8.5 result visuals/tables. These are descriptive comparators, not quotas. The current paper is inside the sample’s lower page quartile and near its minimum word count, while its figure/table counts are already adequate. Do not pad equations or add redundant graphics; spend any added length on reproducible selector details, dataset characterization, baselines, and external cases.

### R1-DV-m02 — GridDB needs a real data card in the manuscript

Table 1 reports “maintenance schema” and “local” where the other resources report numeric table and row counts (`paper_applsci.tex:120–132`). Add table count, row count, fields, asset/entity types, question-family distribution, complexity distribution, empty-result frequency, source/authoring provenance, synthetic-generation procedure, and duplicate/template statistics. Explain how the 70 normalized SQL-template clusters were derived.

### R1-DV-m03 — Framework figures are not legible at journal page scale

Figures 1–3 use strong colors and hatching, but internal labels are too small in the compiled PDF, particularly pages 5, 7, and 8. The canonical release’s `visual_qa.json` also says manual visual review is pending. Increase label size, shorten node text, reduce decorative hatching, and ensure grayscale/color-vision accessibility. Results Figures 4–8 are substantially clearer.

### R1-DV-m04 — The abstract’s “nonzero three-way modifier” should be quantitative

The abstract gives numeric within-backbone effects but describes the key cross-backbone interaction only as “nonzero” (`paper_applsci.tex:19`). Report the estimate and 95% interval, and say explicitly that it describes only the two tested snapshots. This is more informative and avoids binary significance language.

### R1-DV-m05 — Bibliography and venue copyediting remain necessary

The reference audit is strong and admits no unverified identity. However, the rendered bibliography contains phrases such as “In Proceedings of the Proceedings of…”, and capitalization alternates among Text2SQL, Text-to-SQL, and text-to-SQL. Normalize venue fields, task naming, model names, and en dashes. Do not add same-journal citations solely to imitate the corpus; retain only technically relevant sources.

### R1-DV-m06 — Front matter is an absolute submission blocker

Author names, affiliations, correspondence, CRediT contributions, funding, conflicts, acknowledgments, repository DOI, and the final AI-use declaration remain `W10_FRONT_MATTER` placeholders (`paper_applsci.tex:14–17,347–357`). These require real author approval and must never be inferred by an agent. The scientific review can continue locally, but the PDF is not submission-ready while these placeholders are visible.

## What is already strong enough

1. The 2×2 paired design is complete for both backbones, and all 1440 predictions were directly re-executed.
2. The clean Qwen rerun is separated from the contaminated 857-generation directory; Granite is independently audited.
3. Negative results are retained: compact context has no independent positive execution effect, and execution interactions are backbone-sensitive.
4. Answer-shape conformity is not presented as semantic correctness.
5. The 91 external candidates are correctly labeled automatic, unreviewed, unsealed, and noncanonical.
6. The abstract is approximately 195 words and the 18-page, six-section structure is compatible with the ten-paper sample.
7. The reference audit identifies DKA-SQL as the direct technical predecessor instead of claiming first-in-domain novelty.

## Minimum scientifically defensible revision package

The following are not interchangeable writing options; Items 1–3 require new evidence.

1. **External engineering validation:** dual expert review/adjudication of the 91 visible candidates plus a genuinely new sealed 50–100-question set and a single frozen two-backbone evaluation.
2. **Competitive comparison:** fresh direct/CoT/schema-selection/verification baselines on a public shared benchmark and the reviewed grid set, with a reproducible DKA-SQL comparison where feasible.
3. **Framework identification:** selector coverage/token diagnostics plus value-grounding and validator/candidate-replay ablations, or explicit narrowing of framework efficacy claims.
4. **Semantic robustness:** perturbed-database or blinded expert audit of execution-match validity.
5. **Public reproducibility:** license resolution and a permanent repository DOI with exact exclusions.
6. **Submission completion:** readable framework diagrams and author-approved declarations.

## Recommendation

Do not submit this version. After R1-DV-M01 and R1-DV-M02 are completed, the paper could become a credible Applied Sciences Computing and Artificial Intelligence article: its paired design and audit trail would then complement, rather than merely sit beside, DKA-SQL’s broader performance study. If external human review and a new sealed set cannot be obtained, the honest fallback is to narrow the title to a synthetic factorial benchmark study and consider a database/NLP methods venue; prose expansion alone will not make the current evidence an applied power-grid validation.
