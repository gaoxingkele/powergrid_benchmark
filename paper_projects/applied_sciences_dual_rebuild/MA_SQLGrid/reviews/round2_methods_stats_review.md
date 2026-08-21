# MA-SQLGrid Round-2 independent methods/statistics/reproducibility review

**Review date:** 2026-08-05  
**Target:** MDPI *Applied Sciences*, Computing and Artificial Intelligence  
**Material reviewed:** current `paper_applsci.tex`; rebuilt 19-page PDF; `canonical_v2_reanalysis`; Round-1 response/revision report; current BIRD public-baseline audit and 499/500 preflight blocker  
**Decision:** **MAJOR REVISION**

## Independent bottom line

The Round-1 revision repaired the most serious construct error: all four cells and both backbones now use one common projected-column target per question, execution results remain unchanged, and the context and hint factors are described as the bundled interventions that were actually run. I independently recovered all eight cell means from the 1440-row v2 ledger. I also confirmed that the manuscript's factorial estimates and cross-backbone modifiers match the canonical CSV files.

This is not yet acceptable as an Applied Sciences article. The principal remaining problems are (i) inferential promotion of factorial effects that are not members of the stated Holm families and lack a clearly defined sampling population, (ii) absence of an executed public or independently human-validated comparison beyond one small, exposed synthetic database, and (iii) a primary evidence package that cannot yet be independently obtained and re-executed because the GridDB redistribution decision and permanent public archive are unresolved.

## Checks completed independently

- Canonical v2 has 1440 unique rows: 180 questions x 4 cells x 2 backbones.
- Recomputed execution means are Qwen 0.4222/0.7167/0.4333/0.6000 and Granite 0.4278/0.5556/0.4111/0.6000 for F00/F01/F10/F11.
- Recomputed common-target means are Qwen 0.5222/0.9667/0.5889/0.9611 and Granite 0.5222/0.8778/0.5667/0.9222.
- The target is invariant across conditions/backbones. Its column-count distribution is 1:61, 2:31, 3:57, and 4:31 questions.
- The v2 release's 15 tests pass under direct `unittest` execution. The manuscript verifier passes: 26 v2 files, six checked figures, and 17 cited keys.
- The current PDF is 19 pages, 482,206 bytes, SHA-256 `90a887c1fd5675d348a48dc3ce563de7e72c12d3eb8760e4509e2add72261e96`; the log has no overfull boxes, undefined citations/references, or LaTeX errors. Pages 5, 9, 11, and 13 were visually inspected; the principal algorithm, diagrams, tables, and plots are readable.
- The current BIRD statement is accurate: the archive is downloaded, hash-bound, safely extracted, and contains all 11 databases; official gold preflight is BLOCK at 499/500 because Q701 exceeds the 180 s ceiling under SQLite 3.49.1; the item was not dropped or rewritten and zero model calls were made.
- As a dependence sensitivity check, I regrouped questions by the previously defined 39 difficulty-by-SQL-feature families. The core interval directions survived (for example, Qwen execution hint +0.2306, interval approximately [0.0319,0.4680]; execution three-way modifier +0.1889, approximately [0.0100,0.4575]). This is reassuring, but this analysis is not in the v2 release or paper and the 39 groups are not true authoring-template identifiers.

## Major issues

### MA-R2-M01 — Inferential claims are not aligned with the declared hypothesis families

The paper defines factorial main effects and interactions as its central estimands and promotes bootstrap intervals excluding zero for the Qwen execution hint effect, Qwen interaction, Granite and Qwen structural-hint effects, and the execution three-way modifier. However, the stated Holm families contain only four cell edges x two endpoints for each backbone and four cross-backbone cell differences x two endpoints. They do **not** contain the reported main effects, interactions, or backbone-by-effect modifiers. Thus the abstract's three-way statement and Discussion's “nonzero”/“statistically clearer” language receive no family-wise adjustment under the method described.

There is also no defined probability sample of questions. Every cell is deterministically evaluated on the complete, author-constructed, development-visible 180-item set. The cluster bootstrap can quantify sensitivity to question-family composition, but calling its percentile limits confidence intervals requires an explicit hypothetical question-family population and exchangeability assumptions. Finally, “registered” is ambiguous: the common-target endpoint and cluster sign-flip plan were created during the Round-1 reanalysis. Unless a time-stamped plan predating access to these outcomes exists, this should be called a frozen post-review reanalysis, not preregistration.

**Required action:** define the finite-set and any superpopulation estimands; distinguish exact finite-set contrasts from composition-sensitivity intervals; state when every endpoint/family was frozen; and either (a) place the core execution factorial effects/modifiers in an explicit multiplicity family with cluster-valid tests or simultaneous intervals, or (b) label those interval-based claims exploratory and remove family-wise/nonzero promotion. Report raw and adjusted values together and make the abstract follow the corrected hierarchy.

### MA-R2-M02 — Applied validation and competitive evidence remain below the journal's bar

The only canonical accuracy evidence is one synthetic, development-visible database with eight tables, 98 rows, and 180 questions. The two backbones are useful sensitivity runs, but they are not competitive baselines. RTS-GMLC and SimBench pairs are automatic and unadjudicated. The BIRD suite is still a draft, has a 499/500 gold-preflight BLOCK, and has produced no model result. DKASQL is appropriately treated qualitatively, but that does not supply a same-environment baseline.

The narrowed singular title is honest, yet the paper still needs a concrete validation result beyond an exposed internal case study to meet an applied-computing journal's evidential expectation.

**Required action:** before acceptance, complete at least one prospectively frozen public comparison with transparent direct/decomposition/schema-selection/repair baselines and no item dropping, and add independently reviewed grid-domain evidence. Resolve BIRD Q701 by a uniform, documented evaluator policy rather than a one-item rewrite. Because BIRD is cross-domain, it does not replace the two-reviewer/adjudication gate and genuinely new sealed grid set if the paper retains an applied power-grid interpretation. If these studies cannot be completed, further reduce the article to an explicitly exploratory methods/case-study contribution and justify why that is sufficient for Applied Sciences.

### MA-R2-M03 — Primary-result reproducibility is still externally blocked

The local evidence chain is unusually complete, but an outside reviewer cannot currently obtain the primary GridDB records/database, rerun the 1440 SQL evaluations, or regenerate the paper from a permanent archive. GridDB redistribution permission is unresolved, the public DOI/URL is a placeholder, and the manuscript's required author/declaration fields are unfinished. Local hashes demonstrate integrity, not accessibility.

**Required action:** complete license review; deposit the legally redistributable database/question corpus, prompt ledgers, predictions, evaluator, v2 analysis, environment lock, and build instructions in a permanent repository; add a DOI/URL and file-level manifest; and demonstrate a clean-room rebuild. If GridDB cannot be redistributed, supply a legally shareable reconstruction generator plus immutable expected outputs sufficient to reproduce every primary result, and state precisely what remains unavailable. No `W10_FRONT_MATTER` marker may remain at submission.

## Minor issues

### MA-R2-m01 — The dependence cluster needs a stronger definition and sensitivity report

The 70 “normalized SQL-template” clusters are produced by lowercasing SQL, replacing quoted strings/numbers, and normalizing whitespace. Of the 70 clusters, 58 are singletons; the remaining 12 contain 122 of 180 questions and range up to 19 items. This is not necessarily the same as authoring-template dependence. Publish the mapping/rule, explain why it captures dependence, and include a coarser sensitivity analysis. The prior 39 difficulty-by-feature grouping is useful but should not be presented as a true authoring family.

### MA-R2-m02 — The common-target outcome is a direct manipulation check

The same `answer_shape.column_count` provenance underlies the composite hint and the projected-column score. The paper is clear that this is not semantic correctness, but it should also state explicitly that the endpoint tests uptake of an instruction that directly supplies the target. Report the target distribution and freeze timing, call it a manipulation/adherence diagnostic, and avoid treating it as independent corroboration of the hint's semantic benefit.

### MA-R2-m03 — Statistical methods need enough detail and citations to reproduce from the article

Add primary references for cluster bootstrap, paired/randomization inference, Holm correction, and McNemar. State percentile-CI construction, question weighting when clusters differ in size, the sign-flip statistic and Monte Carlo plus-one correction, seeds, SQL-normalization rule, and the exact contents of each multiplicity family. Currently these details are recoverable from code but not from the manuscript.

### MA-R2-m04 — The data-resource table has incorrect field types

Table 1 labels columns “Tables” and “Rows” but reports GridDB as “maintenance schema” and “local.” Replace these with 8 and 98. Add a separate provenance/evidence-status column if those textual labels are needed.

### MA-R2-m05 — Rebuild checks do not yet enforce immutable external inputs

`release_manifest.json` seals current v2 outputs, but the v2 generator records current upstream hashes rather than refusing unexpected upstream hashes, and the tests do not compare each live accepted input to a separately frozen expected digest. The generator also writes `VISUAL_QA.json` as pass with a current timestamp; automated generation should not self-certify a manual review. Add an immutable preflight hash contract, dependency/runtime lock, one clean rebuild command, and a separately signed/manual QA record. Update the manuscript README, which still says results are copied from `canonical_dual_backbone` rather than v2.

### MA-R2-m06 — Use “execution equality on the frozen database state” consistently

Section 3.6 opens with “Strict execution correctness,” while the surrounding paper correctly acknowledges accidental equivalence on one state. Use “strict execution equality” throughout, and reserve “correctness” for claims supported by semantic review or discriminating test suites.

### MA-R2-m07 — Synchronize the Round-1 response with the actual revised manuscript

`round1_author_response.md` still says the current manuscript has not yet been edited and gives intended rather than actual insertion locations; it also contains encoding corruption. Update it to the submitted version, current BIRD blocker, actual page/line references, and completed-versus-external-open status. Do not mark public baseline, human review, license, DOI, or author metadata resolved.

## Claim-level assessment

| Claim area | Round-2 assessment |
|---|---|
| Common-target correction | Validly implemented and numerically consistent |
| Context-package construct | Properly relabeled as bundled |
| Composite-hint construct | Properly disclosed as corpus-tailored |
| Cell means/factorial arithmetic | Recomputed and consistent |
| Cluster inference | Improved, but estimand/cluster/multiplicity interpretation remains incomplete |
| Cross-backbone modifier | Arithmetic consistent; inferential promotion is not in the stated Holm family |
| External accuracy | Correctly not claimed |
| BIRD status | Correctly reported as 499/500 BLOCK with zero model calls |
| Applied generalization | Not established |
| Reproducibility | Strong locally; externally blocked by access/license/archive gaps |
| PDF/figures | Build-clean and readable in inspected pages |

## Decision rationale

**Major revision**, not rejection: the executed factorial evidence is internally auditable, the corrected endpoint is coherent as a manipulation diagnostic, numerical reporting is consistent, and the limitations are unusually candid. Acceptance still requires a corrected inferential hierarchy and substantially stronger applied/public validation, plus an externally executable artifact package. These are substantive evidence changes, not editorial polishing.
