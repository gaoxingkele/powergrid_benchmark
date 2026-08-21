# MA-SQLGrid Round 1 Independent Methods, Statistics, and Reproducibility Review

**Review date:** 2026-08-05  
**Target:** *Applied Sciences* (Computing and Artificial Intelligence Section)  
**Manuscript reviewed:** `manuscript_applsci/paper_applsci.tex` and the 18-page PDF built 2026-08-05 18:13:58 local time  
**Decision:** **Major revision**  
**Scope:** This is an independent review. The manuscript and canonical result files were not edited.

## Overall assessment

The paper has an unusually strong local provenance chain: the two accepted run directories contain the complete 180-question by four-cell Cartesian design; all 1440 canonical rows are present; the contaminated Qwen directory is appropriately quarantined; model, prompt, data, configuration, and code identities are hash-bound; and two independent audit scripts reproduce all archived execution verdicts. I independently recovered every cell mean, the six within-backbone factorial point estimates, the six Granite-minus-Qwen modifiers, and all eight cross-backbone McNemar/Holm results from the canonical row ledgers. The execution findings are reported conservatively: compact context is not promoted as a gain, the Granite interval caveat is retained, and the external automatic candidates are not called human-gold accuracy.

The current manuscript is nevertheless not ready for submission. The most important defect is not a transcription problem but a measurement problem: `shape_ok` is defined with a different target in hint-absent and hint-present cells. A second construct-validity problem is that the nominal schema-scope factor changes schema scope, value presentation, and domain-normalization hints together. Consequently, the paper's answer-shape estimates and causal labels do not currently match the implemented experiment. In addition, the only canonical applied evaluation is a very small project-authored synthetic database, while the external resources have zero completed human reviews. These issues are repairable through reanalysis, honest relabeling, fuller methods, and a stronger external-validation gate, but they require major revision.

## Independent checks completed

- Read the complete `mdpi-applied-sciences` skill and shared MDPI model; assessed applied value, validation, section fit, reproducibility, mandatory statements, and visual legibility.
- Read the complete TeX source, the latest 18-page PDF, claim ledger, Qwen and Granite independent audits, dual-backbone release manifest and generated tables, external protocol reports, human-review protocol, reference audit, and bibliography.
- Confirmed 720 unique rows per backbone, 180 unique questions, four complete cells, identical question/cell keys, identical prompt/data boundaries, and 70 template clusters.
- Independently recovered execution cell means: Qwen `(0.4222, 0.7167, 0.4333, 0.6000)` and Granite `(0.4278, 0.5556, 0.4111, 0.6000)` in F00/F01/F10/F11 order.
- Independently recovered execution effects `(context, hint, interaction)`: Qwen `(-0.0528, +0.2306, -0.1278)`; Granite `(+0.0139, +0.1583, +0.0611)`; Granite-minus-Qwen modifiers `(+0.0667, -0.0722, +0.1889)`.
- Independently recovered all eight cross-backbone discordant-pair counts, exact p-values, and Holm-adjusted p-values, including F01 execution `35/6`, raw `4.8736e-6`, Holm `3.8989e-5`.
- Ran the canonical dual-release tests: 6/6 passed. Inspected all eight framework/result figure families and their placement in the manuscript PDF.
- Examined cluster-size imbalance: 70 normalized-SQL clusters range from 1 to 19 questions; 58 are singletons. As a reviewer sensitivity check, a coarser 39-family cluster bootstrap (20,000 draws, reviewer seed 4242) preserved the qualitative execution conclusions: Qwen hint CI approximately `[0.031, 0.469]`, Qwen interaction `[-0.257, -0.036]`, Granite-minus-Qwen hint modifier `[-0.135, -0.030]`, and three-way modifier `[0.012, 0.456]`. This is reassuring but is not a substitute for an author-specified sensitivity analysis.
- Citation-key audit: 17 unique cited keys, no missing or duplicate bibliography keys. The bibliography contains eight uncited reserve records, which BibTeX does not print and is harmless.

## Major issues

### MA-R1-M01 — Answer-shape outcome uses a condition-dependent target

The manuscript defines answer-shape correctness as satisfying the requested structural response contract (`paper_applsci.tex`, lines 166--171) and treats the four cell means as a common outcome. The implementation does not do that. `build_contexts` empties `inferred_shape` in F00 and F10 (`applsci_factorial.py`, lines 156--165), while `reference_free_validation` defaults a missing column count to one (`dev_chess_style_pilot.py`, lines 842--855). Thus no-hint predictions are judged against one column regardless of the question, whereas hint-present predictions are judged against the question-derived target. Audit reproduction of this code proves computational fidelity, not construct validity.

I performed a diagnostic rescore using each question's same requested column count in all four cells. The point means become:

| Backbone | F00 | F01 | F10 | F11 | Common-target hint main effect |
|---|---:|---:|---:|---:|---:|
| Qwen | 0.5222 | 0.9667 | 0.5889 | 0.9611 | +0.4083 |
| Granite | 0.5222 | 0.8778 | 0.5667 | 0.9222 | +0.3556 |

The positive direction survives, but the abstract's 0.4944/0.4528 estimates are not estimates of a condition-invariant requested-shape outcome. Recompute this endpoint from the raw predictions with one frozen target per question across all cells, independently audit the new rows and cluster intervals, regenerate all affected tables/figures/text, and define exactly whether the endpoint checks only projected-column count or also row granularity and ordering. If the present evaluator is retained, rename it as a condition-specific validator diagnostic and do not use it for between-cell inference.

### MA-R1-M02 — The nominal schema-scope factor is a bundled context intervention

Equations (2) and the surrounding prose state that schema scope varies while deterministic value grounding is held independent of scope (`paper_applsci.tex`, lines 93--99). The frozen prompts show otherwise. Full cells receive the entire schema plus a global database value dictionary. Compact cells receive selected tables/columns, question-matched values, and additional handcrafted normalization hints such as predicate forms. Therefore F10-minus-F00 and F11-minus-F01 do not isolate schema compactness; they compare two context packages that differ in schema breadth, value breadth, and semantic normalization.

Either (a) relabel the factor everywhere as `full schema + global value dictionary` versus `compact domain-grounded context package`, and interpret all context and interaction effects accordingly, or (b) run a genuinely controlled schema-scope experiment in which value and normalization fields are invariant. The current claims that compactness is the intervention and that both scopes use the same grounding term must be removed or corrected. The title need not change materially, but the abstract, equations, Methods, Results, figure labels, and conclusion must use the implemented estimand.

### MA-R1-M03 — “Answer-shape hint” is a corpus-tailored composite intervention

The intervention includes more than an output shape. The frozen rule set provides exact operator and projection guidance, for example `Use COUNT(*)`, `Project type_name and AVG(capacity_mw)`, exact projection fields, `GROUP BY/HAVING`, and ordering/limit instructions (`infer_answer_shape`, approximately lines 473--648). Its inferred column count matches the stored GridDB answer-shape metadata for all 180 exposed evaluation questions. The manuscript instead describes a generic response contract and says that the intervention “optionally states the requested projection or aggregate form” without disclosing the extensive rule inventory or its development history.

Publish the complete rule specification or a compact pseudocode/table plus frozen code reference; state that it was developed with prior exposure to this corpus; provide representative prompts from all four cells; and rename the factor to a question-derived structural/SQL-operation hint package unless it is reduced to pure output shape and rerun. General claims about reliable answer-shape guidance require a prospectively frozen evaluation on newly authored or otherwise unexposed questions.

### MA-R1-M04 — Applied validation is below the journal's application-evidence bar

The primary database is a project-authored synthetic SQLite benchmark with only eight tables and 98 total data rows (table sizes 6, 18, 9, 8, 8, 26, 8, and 15), yet Table 1 reports its table field as “maintenance schema” and its row field as “local”. The 180 evaluation questions were previously exposed during development. RTS-GMLC and SimBench broaden the schema plumbing but have zero human-reviewed question--SQL pairs and no canonical accuracy. This is honest in the prose, but it leaves no validated result beyond an idealized, tiny database. That is a substantial desk/reviewer risk for *Applied Sciences*, whose central standard is concrete application with validation beyond an idealized setting.

At minimum, report the full GridDB schema/table sizes, question construction and template distribution, authorship/annotation and verification procedure, difficulty distribution, and exposure status. Before submission, complete real dual review and adjudication of an external set and run a frozen no-drop evaluation; preferably use newly authored/deeply rewritten sealed questions. If this cannot be completed, narrow the application and title wording to a controlled synthetic case study and remove operationally suggestive language. External automatic-reference matches must remain diagnostic.

### MA-R1-M05 — McNemar inference ignores the dependence that motivated cluster bootstrap

The manuscript correctly recognizes shared-template dependence and uses a template-cluster bootstrap. Exact McNemar tests are nevertheless calculated over 180 question pairs as though those pairs were independent, then treated as inferential support after Holm adjustment. Holm addresses multiplicity, not within-template dependence. This is especially problematic where a cluster interval crosses zero but McNemar rejects, because the latter is the anti-conservative summary under the paper's own dependence model.

Use cluster-aware randomization/permutation, a cluster-robust model, or a hierarchical bootstrap test for inferential p-values; alternatively report McNemar discordances and p-values as question-level descriptive sensitivity only and make cluster intervals the sole inferential criterion. Define three Holm families explicitly: eight Qwen factorial edges, eight Granite factorial edges, and eight cross-backbone cell-by-metric contrasts. Do not write “supported under both summaries” until both summaries respect the registered dependence unit.

### MA-R1-M06 — Direct DKASQL positioning is too thin for novelty and baseline adequacy

The manuscript correctly admits DKASQL as the direct same-journal power-grid text-to-SQL predecessor, but gives only a short conceptual distinction and no systematic comparison. MA-SQLGrid is not evaluated against DKASQL, a reproduced domain system, a standard text-to-SQL baseline, or even a clearly defined direct-prompt baseline outside its own four prompt packages. The current contribution is therefore primarily an audit/factorial study, not a demonstrated system improvement.

Add a same-journal technical-comparator table covering task, domain corpus, knowledge adaptation, generation/verification stages, models, evaluation, external validity, and open evidence. Explain why a numerical DKASQL comparison is or is not technically possible. If no common benchmark comparison is feasible, make the novelty explicitly methodological (paired causal decomposition, evidence ledger, negative results) and avoid presenting the framework as performance-superior. A reproducible standard direct-schema baseline on the same GridDB would materially strengthen the applied result.

### MA-R1-M07 — Methods are not self-contained enough to reproduce the interventions

The paper supplies model and run hashes but omits the exact compact-selection rules, answer-hint rules, value-dictionary construction, scoring implementation, prompt length manipulation check, SQLite/Python/runtime versions, and hardware. It also describes row granularity and ordering as parts of the structural contract although the canonical `shape_ok` is only a column-count check. The prompt word-count manipulation is substantial (reviewer check: full/no-hint 631 words for every question; compact/no-hint mean 150.3, range 121--197) and should be reported.

Add algorithm/pseudocode and representative prompt fragments, a factor-invariance audit table, common outcome definitions, context/token-length distributions, database/runtime/hardware details, full immutable artifact identifiers, and exact commands. Separate reproducibility of archived outputs from validity of the estimands. Add appropriate statistical references for cluster bootstrap, McNemar, and Holm.

### MA-R1-M08 — The architecture figures depict unevaluated or inaccurate workflow elements

Figure 1 includes a repair pass even though the formal factorial run makes one generation per prompt and the paper explicitly says validator-repair benefit is pending. Figure 3 says “Models × repetitions” although each backbone has one deterministic generation per prompt. These diagrams therefore do not faithfully depict the executed experiment. At manuscript page scale, the internal text of Figures 1--3 is too small to read; the result plots are acceptable but also text-dense.

Remove or visibly mark the repair loop as future/not evaluated, replace “repetitions” with the actual one-run-per-backbone design, simplify the three framework figures, enlarge internal labels, and repeat manual page-scale visual QA after rebuilding the PDF.

### MA-R1-M09 — Submission-critical declarations and artifact access are incomplete

Author names, affiliations, corresponding author, CRediT roles, funding, conflicts, acknowledgments, AI-use declaration, public repository URL/DOI, and author confirmations remain placeholders. GridDB redistribution permission is unresolved. These are explicit MDPI submission requirements or material data-availability obligations.

Resolve every `W10_FRONT_MATTER` placeholder, complete license review, deposit the permitted reproducibility package at a permanent public location, and state precisely which raw records cannot be redistributed and how qualified reviewers can verify them. This is an external human/author blocker and must not be fabricated.

## Minor issues

### MA-R1-m01 — One adjusted p-value is transcribed incorrectly

`paper_applsci.tex` line 240 and PDF page 12 report Granite `shape_at_compact` execution Holm p as `1.86e-4`; `granite_registered_contrasts.csv` gives `1.861682221715455e-6`. Correct the prose from the canonical table after resolving MA-R1-M05.

### MA-R1-m02 — Avoid dichotomous “nonzero” and “reject equality” wording

Prefer “the 95% interval excluded zero” and “the paired distributions differed under the stated test” to “nonzero modifier” or “reject equality”. An interval is not proof of a population parameter being nonzero, and failure to reject is not evidence of equality.

### MA-R1-m03 — Table 1 mixes numeric and textual fields

The columns `Tables` and `Rows` contain `maintenance schema` and `local` for GridDB. Replace them with the actual counts (8 tables, 98 rows) and add construction/review/exposure/license columns so all rows have comparable meanings.

### MA-R1-m04 — Title and featured application need a singular evidence boundary

The title says “databases” while canonical accuracy comes from one synthetic maintenance database; the external databases are noncanonical pilots and are not maintenance databases. Consider the small change “over a Power-Grid Maintenance Database” or add “A Controlled Factorial Study” to prevent plural external-validation inference. The featured-application sentence should remain explicitly non-operational.

### MA-R1-m05 — Reference audit is not synchronized with the assembled manuscript

The audit says two of three *Applied Sciences* entries are cited and treats Tang et al. as reserve, but the assembled manuscript cites all three. Update the final reference audit and add the statistical-method references. The bibliography itself has no missing citation keys.

### MA-R1-m06 — Release visual QA status is internally inconsistent

`visual_qa.json` says automated pass with manual review pending, while the manuscript uses the figures as final. Record an actual manual page-scale decision and any remediations. Do not use automated DPI/editable-text checks as a substitute for legibility.

## Required revision gates

1. Recompute and independently audit a condition-invariant structural outcome; rebuild every affected artifact and claim.
2. Correctly relabel or rerun the bundled context factor and composite hint factor.
3. Replace question-level McNemar inference with cluster-aware inference or explicitly demote it to descriptive sensitivity.
4. Fully disclose GridDB construction, size, templates, and exposure; complete meaningful human external validation or sharply narrow the applied claim.
5. Expand DKASQL/standard-baseline positioning and make novelty methodological unless a performance comparison is added.
6. Make Methods self-contained, repair the framework figures, correct the p-value transcription, and complete all MDPI declarations and public-artifact fields.

## Decision rationale

**Major revision**, rather than reject, because the complete execution ledgers and conservative execution claims provide a credible foundation, and my independent calculations reproduce the central execution point estimates. The paper becomes potentially publishable if the authors correct the outcome measurement, acknowledge the bundled interventions, and raise the applied-validation evidence. Without those changes, the abstract's strongest shape result is not an estimate of a common outcome and the nominal schema-scope causal interpretation is unsupported.
