# MA-SQLGrid Round 3 Independent Domain, Venue, and Visual Review

## Review identity and frozen snapshot

- Review type: independent power-grid application boundary, MDPI *Applied Sciences* fit, narrative, and visual review.
- Manuscript reviewed: `manuscript_applsci/paper_applsci.tex`.
- TeX SHA-256: `2206ADAEC37BA3C89F5177C1D32AB8519967BA1C688C96E134F754769FE29067`.
- PDF reviewed: `manuscript_applsci/build/paper_applsci.pdf`.
- PDF SHA-256: `441494CF65860CB7ECDC25F8638DE2BF12D3A06E066DE4D0B677A4B2383E6C44`.
- PDF extent: 24 A4 pages; 9 figures; 9 tables; 6 numbered main sections; 27 subsections; 23 references.
- Scope of this review: no manuscript edits were made.

## Recommendation

**Major Revision; not submission-ready.**

[Target] MDPI *Applied Sciences*  
[Fit] **Medium, potentially High after external domain validation.** The paper has a concrete engineering interface, complete controlled experiments, reproducible negative results, and an accessible applied narrative. However, the only claim-promoting quantitative database is a synthetic, development-visible 8-table/98-row GridDB instance, while RTS-GMLC and SimBench remain automatic, unadjudicated pilots. This is the main application-over-theory risk for the journal.  
[Contribution type] applied-method / controlled benchmark case study.  
[Main evidence gap] independently human-reviewed power-grid external validation on a sealed or newly authored set.  
[Best-fit Section] Computing and Artificial Intelligence is the clearest methodological route; an Electrical/Electronic Engineering route is defensible only after stronger domain-expert validation. The exact current Section title must be verified before submission.  
[Top rejection risk] weak real-world/external validation relative to the power-grid application framing.  

The title is appropriately bounded and should not be enlarged. “A Controlled Factorial Study ... over a Power-Grid Maintenance Database” accurately signals a one-database study. The abstract and Conclusions are notably conservative: they state the synthetic/development-visible boundary, do not call the automatic external matches accuracy, do not promote the nine null factorial families, and do not claim operational generalization. The present recommendation is driven by evidence maturity and submission completeness, not by exaggerated claims in the title.

## Major issues and required actions

### R3-DV-M01 — Applied power-grid validation remains below the strongest venue-ready level

The paper is methodologically substantial, but its claim-promoting evidence remains entirely within one small synthetic maintenance database. RTS-GMLC and SimBench contribute schema-portability diagnostics, not validated accuracy: zero of 91 candidate pairs has completed the stated two-reviewer human adjudication. The Qwen external run is intentionally excluded, and BIRD is unexecuted. Consequently, the paper currently demonstrates an auditable experimental protocol more strongly than a validated power-grid application.

Required action:

1. Complete independent qualified-domain review and adjudication of the external question–SQL pairs, with units, ties, projection granularity, and acceptable-equivalence rules recorded.
2. Freeze a genuinely sealed or newly authored/rewritten confirmatory subset after prompt repair, then run at least the main declared model–prompt configurations without dropping failures.
3. Report per-dataset denominators, execution failures, accuracy/agreement under the adjudicated contract, and representative grid-domain error classes.
4. If this cannot be completed before submission, keep the present title but further recast the article as a controlled benchmark/methodology case study. Change the Featured Application from “supports” to “is designed to support,” and state that no deployed maintenance workflow or field decision has been validated.

Acceptance condition: either provide claim-promoting, expert-adjudicated external grid evidence, or consistently reduce the application claim to a synthetic protocol demonstration and accept the resulting Medium venue fit.

### R3-DV-M02 — “Two blinded technical reviewers” is ambiguous and can be read as human expert review

The abstract says “Two blinded technical reviewers held all 114 order-sensitive questions.” Section 3.7 later calls this an “agent review” and correctly says it is not qualified human annotation. A reader or editor can nevertheless understand the abstract phrase as independent human peer/domain review. This ambiguity is material because the held-set decision determines the 66-question claim-promoting denominator, and the manuscript's generative-AI declaration is still an unresolved placeholder.

Required action:

1. Identify the reviewer type consistently at first mention and throughout: for example, “two independently prompted AI protocol-review agents” if that is the actual mechanism. Do not use “blinded technical reviewers” alone unless they were human reviewers.
2. Describe what was blinded, the fixed rubric, independence mechanism, disagreement count, adjudicator, and why the decision is a conservative protocol-safety screen rather than semantic ground truth.
3. Put the exact 114/66 classification ledger and rubric in the public supplement.
4. Complete the generative-AI-use declaration with tool/model identity, roles in study design/code/analysis/figures/writing, and named human verification responsibility.
5. Retain the statement that qualified human domain experts must still resolve intended ordering, ties, units, and granularity.

Acceptance condition: no wording may imply human semantic validation where only agent-based protocol review occurred.

### R3-DV-M03 — Front matter, artifact availability, and licensing are hard submission blockers

The first page visibly contains author, affiliation, and correspondence placeholders. Pages 23–24 contain unresolved placeholders for author contributions, funding, IRB confirmation, informed consent confirmation, repository DOI/URL, acknowledgments, conflicts of interest, and AI-use disclosure. GridDB redistribution permission is unresolved, and source-specific obligations for derived RTS-GMLC and SimBench artifacts await human review.

Required action:

1. Replace every `W10_FRONT_MATTER` placeholder with author-approved text.
2. Complete CRediT contributions, funding and funder role, conflicts, acknowledgments, corresponding-author details, and AI-use disclosure.
3. Finish the license audit before depositing any raw or derived database artifacts; distinguish redistributable files, reconstruction scripts, and restricted files.
4. Mint and insert a permanent repository DOI/URL, and ensure the Data Availability Statement describes precisely what can be obtained and under which license.
5. Verify that all author identities and affiliations match the submission system.

Acceptance condition: zero unresolved placeholders and a license-cleared, DOI-bound reproducibility package.

### R3-DV-M04 — Interval terminology is not fully consistent with the paper's own estimand boundary

The prose carefully calls bootstrap ranges “composition-sensitivity intervals” and explicitly denies population-confidence interpretation. Several result tables and figures still use abbreviated “95% CI” or “CI low/high” labels, including Tables 3, 4, and 8. In a broad applied venue, many readers will interpret “CI” as a confidence interval despite the caption caveat. Tables 6–7 avoid this problem and should be the model for the other displays.

Required action:

1. Replace every “95% CI,” “CI low,” and “CI high” display label with “95% composition-sensitivity interval,” “composition low,” and “composition high,” or an equally explicit short form defined in each caption.
2. Use “confidence interval” only when a population/sampling interpretation is actually supported.
3. Perform a manuscript-wide terminology search so Abstract, tables, figures, captions, Results, and Discussion use one contract.

Acceptance condition: a reader cannot mistake empirical-composition sensitivity for population uncertainty.

## Minor issues and required actions

### R3-DV-m01 — Figure 6 is readable, but the repeated Holm labels create avoidable crowding

Figure 6 is legible at the current full-page width, colors and zero line are distinguishable, and all nine intervals can be matched to labels. The final “Holm p=1.000” annotation begins immediately after the longest green interval, creating a near-collision; repeating the same value nine times also consumes plot width without adding discrimination.

Action: remove the nine in-panel Holm labels and state once in the caption that all adjusted values are 1.0000, or reserve a separate right-aligned annotation column outside the interval axes. Keep a vector PDF/SVG source and verify grayscale/colour-blind differentiation.

### R3-DV-m02 — Tables 6 and 7 need a self-contained decoding aid

Both tables are sharp and readable, have complete rows, and fit the page without clipping. Table 6 gives exact counts and rates, which is strong. However, readers reaching these tables must remember F00–F11 from Figure 3, and Table 7 does not repeat the eligible denominator or 12-cluster scope.

Action: add a compact caption/footnote such as “Fxy: x=context-package indicator, y=hint indicator; n=66 questions (12 clusters) per cell.” Use an en dash consistently in “Granite–Qwen.”

### R3-DV-m03 — The abstract's new reliability result should identify the reviewer type and define “suite rate” more plainly

The abstract is approximately 204 words and remains within a reasonable MDPI-style length. “Suite rates” is not immediately transparent to a multidisciplinary reader, and the reviewer identity ambiguity arises here first.

Action: replace “suite rates” with “15-state logical-AND execution-agreement rates,” and identify the order screen as agent-based or human-based accurately. Preserve the sentence that it is not a human semantic audit.

### R3-DV-m04 — The Featured Application slightly outruns the demonstrated evidence

The Featured Application is admirably qualified in its second sentence, but “supports auditable natural-language querying” can still read as an implemented operational capability. The experiments show a read-only audited prototype and bounded benchmark behavior, not field workflow validation.

Action: use “is designed to support” or “demonstrates an auditable prototype for,” and add that a human must inspect SQL and source rows before high-consequence use.

### R3-DV-m05 — Section 4.7's “15 result matches” is easy to remember out of context

The manuscript repeatedly states that 15/364 is not accuracy, which is responsible reporting. The raw match count nevertheless attracts attention while the candidate references remain unadjudicated.

Action: consider moving the exact count and missing-column breakdown to a clearly labeled diagnostic table/supplement, leaving the main text focused on the failure modes and the prohibition against accuracy interpretation. If retained, state “automatic-reference diagnostic matches” every time.

### R3-DV-m06 — The narrative is complete but over-fragmented for a broad applied audience

The six main sections follow a suitable IMRaD-like progression, but 27 subsections produce short transitions and make the evidence hierarchy harder to retain. The Results sequence is logical; Methods contains the greatest density of gates, audits, and protocol distinctions.

Action: consolidate closely related Methods subsections, provide one compact evidence-tier table/graphic (canonical GridDB, retrospective stress test, prospective components, automatic external pilot, frozen-not-run BIRD), and move file-hash/process detail to the supplement while retaining the essential safeguards in the article.

### R3-DV-m07 — Practical beneficiary and decision context should be named more concretely

The Discussion gives good safety guidance but remains generic about who uses the interface and for what bounded decisions.

Action: name plausible beneficiaries—maintenance engineers, asset-data analysts, and query reviewers—and give one non-deployment example workflow (e.g., retrieving inspection/work-order records for review). Explicitly state that the system does not perform protection, dispatch, or autonomous maintenance decisions.

## Visual and structural audit

| Item | Finding | Decision |
|---|---|---|
| PDF integrity | 24 pages; no overfull-box warning in the reviewed build; no visible clipping on inspected pages | Pass |
| First page | Title and abstract fit cleanly; front-matter placeholders are visually prominent | Blocked by R3-DV-M03 |
| Figures 1–3 | Clear architecture/evidence-gate/factorial diagrams; labels readable | Pass |
| Figures 4–5 | Readable; Figure 4 appropriately states point estimates only | Pass with terminology consistency check |
| Table 5 | Dense but readable at full page width | Pass |
| Table 6 | Exact counts/rates clear; no clipping | Pass with F-cell legend addition |
| Table 7 | Nine effects and intervals readable; no clipping | Pass with denominator/cluster footnote |
| Figure 6 | Vector-like, readable labels and intervals; repeated Holm labels crowd right edge | Minor revision |
| Figures 7–9 / Tables 8–9 | Readable; Table 8's “95% CI” label conflicts with prose | Revise terminology |
| Conclusions | Claims remain bounded; external and BIRD limitations are explicit | Pass after reviewer-identity fix |
| Declarations | Multiple unresolved placeholders | Submission blocker |

## Claim-boundary audit

- **Title:** pass; no major title change recommended.
- **Abstract:** mostly pass; fix reviewer identity and replace “suite rates.”
- **Conclusions:** pass in direction and restraint; do not add universal, operational, or cross-database claims.
- **Power-grid boundary:** clearly states no protection/dispatch conclusion implicitly, but an explicit exclusion would help.
- **External validation:** correctly blocked in the current text; still a venue-strength weakness.
- **Human review boundary:** scientifically stated in Methods/Limitations but ambiguous in the abstract; major revision required.
- **BIRD:** correctly described as frozen-not-run and excluded; do not cite it as evidence unless formally launched and integrated under its frozen protocol.

## Required Round 3 revision order

1. Resolve reviewer identity and AI-use disclosure language.
2. Decide whether to complete external expert adjudication/sealed validation or submit as a narrower synthetic methodology case study.
3. Standardize interval terminology manuscript-wide.
4. Implement Figure 6 and Tables 6–7 caption/annotation refinements.
5. Tighten the evidence-tier narrative and practical beneficiary framing.
6. Complete human front matter, licensing, public repository DOI, and all declarations.
7. Recompile and perform final visual QA on pages 1, 15–19, and the declarations/references pages.

## Final decision rule

This review can move from **Major Revision** to **Acceptable after Revision** only when R3-DV-M02, R3-DV-M03, and R3-DV-M04 are fully closed and R3-DV-M01 is either closed with expert-adjudicated external evidence or answered through a consistently narrower synthetic case-study framing accepted by the authors. At present, the scientific claim discipline is strong, but the applied-evidence depth and submission metadata are not yet sufficient for a clean *Applied Sciences* submission.
