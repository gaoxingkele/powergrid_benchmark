# Round-2 Independent Review: Applied Sciences Fit and Research Integrity

**Manuscript:** *MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases*  
**Frozen round reviewed:** R2  
**Reviewer role:** Applied Sciences journal-fit and research-integrity reviewer  
**Review date:** 2026-08-08 (Asia/Shanghai)  
**Recommendation:** **Major revision**

## Overall assessment

R2 is substantially more candid and auditable than R1. The manuscript now distinguishes inherited, diagnostic, component, public non-grid, and post-audit descriptive evidence; retains negative results and incidents; reports the failed prior-outcome-independence gate; and limits the v3 result to a deterministic no-generation re-execution. The SQLite executor, complete-evidence gate, blackboard trace, and deterministic reproductions are real implementation contributions. The present paper is therefore reviewable and potentially relevant to the *Applied Sciences* Computing and Artificial Intelligence section.

It is not yet a submission candidate. The title-level combination of **robust**, **multi-agent**, and **power-grid databases** is only partly supported: the integrated roles have not been evaluated in a matched new-generation experiment, the Synthesizer merely packages external candidates, GridDB is synthetic and development-visible, and the authentic grid-derived resources have zero qualified-human semantic reviews. More immediately, the claimed editor/reviewer archive is not synchronized to the frozen R2 manuscript: the existing packages contain a different title and older PDF/source, while one cited visual-QA directory contains an obsolete 18-page draft with the now-disallowed prospective-from-freeze wording. These are blocking integrity and release-control defects, not cosmetic packaging issues.

## Five most serious issues

### 1. The available submission/reviewer packages are not the frozen R2 article (blocking)

The current source and PDF hashes are `17EE387D...EC2E1` and `C4C83B2...EC01`. In contrast, `reviewer_packages/MA_SQLGrid_submission_review_2026-08-08/manuscript/` contains source/PDF hashes `F0CA2BA1...83C8` and `2F368EED...6EF` and the different title *MA-SQLGrid: A Multi-Stage Context-Grounding Framework for Text-to-SQL over Power Grid Maintenance Databases*. The parallel email-delivery package contains the same obsolete manuscript. Its README also says that public project code and license-cleared materials complement the package, whereas R2 correctly states that repository synchronization has not occurred. Thus the R2 Data Availability claim that a manuscript-bound archive “has been prepared” is not presently supported by a matching archive.

**Required R3 action:** quarantine the two old packages from submission use without deleting them; build a new R3 editor/reviewer archive from an explicit allow-list; bind the exact R3 source, PDF, bibliography, used figures/tables, code, tests, evidence manifests, incident index, and restricted/public inventory; and verify every package hash from a clean extraction. The archive README must state its round, title, evidence class, excluded incidents, license restrictions, and repository status.

**Acceptance test:** extracted archive source/PDF hashes equal the final R3 audit; the title is exact; a search finds no alternate-title manuscript; the v3 independent release audit is included; current and packaged manuscript verifiers pass; and the package contains no `.env`, credentials, model weights, unauthorized third-party database, or excluded incident result presented as evidence.

### 2. The title-level “robust multi-agent ... power grid” proposition exceeds the integrated empirical evidence (blocking scientific gap)

The manuscript is admirably explicit that the Analyst and Cartographer are deterministic skeletons, the Synthesizer accepts externally generated SQL, and the v3 selector does not estimate generation, communication, or five-role effects (Sections 3.3, 3.8, 4.7, 5.1, 6, and 7). This candor prevents misreporting but does not itself validate the title. The tested robustness vector establishes selected SQLite safety/resource/evidence-completeness mechanisms and three bounded metamorphic operators. It does not establish broad semantic, distributional, prompt, schema, or deployment robustness. Likewise, the principal domain accuracy resource is one 98-row synthetic, development-visible database; BIRD is explicitly non-grid; and RTS-GMLC/SimBench pairs are machine silver with zero qualified-human reviews.

**Required R3 action:** preserve the original title only with an explicit title-interpretation paragraph in the Introduction and Conclusion, define “agent” and every robustness dimension operationally, and remove any sentence that invites a general performance interpretation. To close the scientific gap rather than merely disclose it, run a newly authorized, call-matched, outcome-untouched power-grid comparison: direct single candidate; staged question/schema handoff; matched multi-candidate validation/adjudication without CF; and the same pool with preregistered reference-free CF witnesses. Reference SQL and semantic intent must be independently reviewed under a frozen qualified-expert protocol.

**Acceptance test:** either (a) the matched untouched study and independent audit support bounded integrated-system claims, or (b) R3 explicitly labels the paper an architecture/safety study and the editorial cover letter flags that the original title is a framework identity, not an observed multi-agent superiority claim. Route (b) remains scientifically honest but may still be judged insufficient by the editor for the retained title.

### 3. Qualified power-grid semantic validation remains absent (blocking for broad applied value)

Table 1 correctly records zero completed human reviews and zero sealed items for the authentic grid-derived pilots. The manuscript also states that LLM- or author-assisted triage cannot be relabeled as expert gold. Nevertheless, the applied value is presently inferred from authentic schemas and synthetic/development-visible questions rather than demonstrated through independently adjudicated operational semantics. Query correctness in this domain depends on units, codes, temporal bounds, tie handling, topology, aggregation granularity, and authorization context; SQLite result equality alone cannot adjudicate those matters.

**Required R3 action:** complete the frozen two-reviewer-plus-adjudicator protocol for a development-visible descriptive tier and, for claim-promoting evaluation, create or deeply rewrite an outcome-untouched set held by a custodian. Record reviewer qualifications, independence, item-level decisions, disagreements, adjudication, exclusions, inter-rater agreement with uncertainty, reference-SQL re-execution, and license/ethics determination. LLM API review may assist triage but must remain separately labeled machine assistance.

**Acceptance test:** no count is called expert-reviewed without signed/dated records and reviewer qualifications; every revised reference query re-executes; denominators retain disagreements and failures; the manuscript distinguishes human-reviewed-unsealed from untouched/sealed evidence; and the institution documents whether collecting professional annotations requires ethics review or consent.

### 4. The R2 round audit does not bind a valid visual-QA and figure-lineage set (blocking release-control defect)

`R2_ASSEMBLY_AUDIT.md` reports visual inspection of `visual_qa_root` pages, but those images show an obsolete 18-page draft whose page 1 calls v3 a “prospective-from-freeze” study. The frozen current PDF is 19 pages and the newer `r2_descriptive_final_*` images show the corrected descriptive wording. The audit therefore overstates what was visually checked. In addition, `FIGURE_LINEAGE.json` binds only the architecture figure, while the manuscript uses four figures. The R2 directory contains numerous unused legacy figures and tables, increasing accidental-package contamination risk.

**Required R3 action:** render the exact final PDF after its hash is frozen; store a page manifest binding PDF SHA, renderer/version, page count, and image hashes; visually inspect every page or a declared risk-based set plus all figure/table pages; and create lineage records for all used figures. Build the submission package from references parsed from the final TeX, not by copying the whole R2 directory.

**Acceptance test:** visual-QA manifest PDF hash equals `ROUND_AUDIT.json`; page count and every inspected image match; no inspected image contains `prospective-from-freeze` for v3; all four used figures have source/data/code/hash lineage; and the package contains no unreferenced legacy figure/table unless explicitly placed in a labeled supplement.

### 5. Journal-facing narrative, literature support, and declarations remain incomplete (major; several portal blockers)

The current abstract is approximately 285 words and reads as an audit chronology rather than a concise applied-science abstract. The article carries seven dense tables/figures across multiple evidence tiers, but the “Agentic Decomposition” subsection has no citation and the compiled paper cites only 13 bibliography keys; the nearest multi-agent/agentic Text-to-SQL comparison is therefore too thin to establish novelty. Tables 1 and 2 use aggressive resizing and small text. Back matter correctly includes “All authors have read and agreed...”, the supplied author order/affiliations, grant number `521300250006`, a third-party-permission clause, and an AI-assistance statement. However, Yang Yong's email is still a placeholder; the funding agency and funder role are unconfirmed; the GitHub repository is unsynchronized; license review is incomplete; and the AI statement does not identify the models/providers and stages used to generate or machine-adjudicate external question--SQL assets.

**Required R3 action:** shorten and restructure the abstract; add only verified primary literature for agentic/multi-agent Text-to-SQL, execution safety, and the closest power-grid precedent; state novelty relative to those methods; improve table legibility; and complete a file-level submission checklist. Expand the AI disclosure to distinguish writing/code assistance, image production, dataset/question generation, machine adjudication, and scientific decisions, with exact tool/model identity where records exist. Do not guess the funding agency or email.

**Acceptance test:** current official *Applied Sciences* instructions are rechecked immediately before submission; abstract and declarations conform to the then-current requirements; all citations are verified and cited; email, funding-agency/funder-role wording, author spelling/order, repository release/tag, and license inventory have written author/release-owner confirmation; and AI-generated or AI-adjudicated artifacts are never described as human gold.

## Claim--evidence audit

| Claim and location | Evidence located | Verdict | R3 requirement |
|---|---|---|---|
| Title, line 15: “A Robust Multi-Agent Framework ... in Power Grid Databases” | Sections 3.3--3.4; Table 3; executor/agent tests; v3 descriptive ledgers | **Partially supported.** Framework mechanisms exist; integrated multi-agent efficacy, general robustness, and broad power-grid validity do not. | Keep the claim explicitly mechanism-bounded; ideally add the matched untouched domain experiment. |
| Abstract, line 22: five-role append-only coordination and fail-closed CF | `ma_sqlgrid_agents.py`, `sqlite_readonly_executor.py`, 30 passing tests, Figure 1 lineage | **Supported as implementation evidence.** | Preserve code/test hashes and distinguish deterministic roles from model-calling agents. |
| Abstract/Sections 3.8 and 4.7: v3 is descriptive, 5760 attempts, 332 failures, 80/100/101, Q039 only | v3 ledgers, dual byte-identical reproduction, `INDEPENDENT_RELEASE_AUDIT_V3.md` | **Supported under the descriptive boundary.** The independent audit explicitly fails prior-outcome independence. | Do not use prospective, confirmatory, preregistered, or unseen-outcome labels for v3. |
| Section 3.6/Figure 3: prospectively frozen component study | `component_canonical_release/INDEPENDENT_AUDIT.md`, SHA `93CC596B...9282`; 700 scored rows | **Boundedly supported for this separate component study**, not for v3 or five-role coordination. | Name the separate release/audit in provenance and retain the audit's non-notarial timing and latency caveats. |
| Section 3.3/5.4: database-enforced read-only and bounded execution | Executor source, adversarial tests, unchanged database hash/failure traces | **Supported for the tested SQLite boundary.** | Never extend to user authorization, process isolation, data minimization, or operational safety. |
| Table 3/Section 4.5: 15-state logical-AND reliability | Formal-v5 25,920 rows; 66-question automated subset; no corrected effects | **Supported as constructed-state diagnostic.** | Prefer “constructed-state agreement/invariance” over unqualified reliability; retain 114-item diagnostic hold. |
| Section 4.6: BIRD results and unequal calls | BIRD v1.1 ledgers/audit; 500 items, 11 databases, 5000 new calls; incidents excluded | **Supported as inherited non-grid workflow portability evidence.** | Do not call it MA-SQLGrid, call-matched repair, or power-grid validation. |
| Table 1/Limitations: authentic grid structures but machine-silver semantics | RTS-GMLC/SimBench manifests and zero qualified reviews | **Supported as resource/provenance statement only.** | No external accuracy or expert-grounded claim until qualified review is complete. |
| Data Availability, line 430: manuscript-bound archive “has been prepared” | Existing reviewer/email packages contain older title, source, and PDF | **Not supported for current R2. Blocking.** | Generate and independently verify a current round-bound archive before retaining this wording. |
| Supplementary, line 425: public repository must be synchronized/tagged | R2 audit lists repository synchronization as manual blocker | **Accurate negative-status statement.** | Record immutable commit/tag/DOI and clean-clone verification before portal upload. |
| AI disclosure, line 431 | Codex assistance stated; machine-generated candidates acknowledged generically | **Incomplete.** | Add exact, stage-specific provenance for LLM-assisted data construction/adjudication and distinguish author scientific decisions. |
| Author/funding metadata, lines 16--20 and 426--432 | Author names/affiliations and grant number supplied; email/agency unresolved | **Partly complete; portal blocking.** | Obtain written confirmations; do not infer missing fields. |

### Prospective-wording search conclusion

The current R2 TeX does **not** relabel the failed v3 release as prospective. Its remaining “prospectively frozen” wording at Figure 3 refers to the separately audited 700-call component release. However, obsolete `visual_qa_root` images still contain prospective-from-freeze v3 wording. Those images must be excluded from any current audit or package and retained only as clearly labeled history.

## Experiment audit

### Required to support the retained title at a strong scientific level

1. A newly authorized, call-matched, contemporaneous four-condition integrated-system experiment on a genuinely untouched power-grid evaluation set.
2. Two qualified independent semantic reviewers plus a qualified adjudicator under a frozen rubric; item-level retained decisions, disagreement and agreement statistics, and reference-SQL re-execution.
3. Pre-run tests restricted to synthetic/development fixtures; no same-evaluation gold-derived row may enter tests, thresholds, rule selection, or reports.
4. Complete reporting of accuracy, valid execution, coverage/abstention, rescue/harm, failures, tokens/calls, and latency only under a controlled timing protocol; clustered inference and multiplicity family fixed before evaluation.
5. Independent recomputation and a package-level release audit from clean extraction.

### Desirable but optional

- Risk--coverage calibration and abstention thresholds chosen on development-only data.
- Error taxonomy by join, filter, aggregation, unit/code, ordering/tie, and authorization failure.
- A second authentic grid schema after qualified review, treated as external transfer rather than pooled with BIRD.
- Controlled efficiency analysis with exclusive-GPU/process/thermal attestation.
- A code-native plot showing 80/100/101 together with the 117--118 reversed-order sensitivity, so the negative order-dependence result is visually prominent.

### Unjustified or scientifically improper reruns

- Rerunning v3 on the same 180 items to claim restored prospectivity, preregistration, or outcome blindness.
- Choosing the favorable reversed-tie 117--118/180 result after outcome access and promoting it as the primary rule.
- Using LLM API “experts” as substitutes for qualified independent human semantic reviewers.
- Dropping failed attempts, excluded incidents, ambiguous items, or harmed cases from denominators.
- Increasing candidate calls only for MA-SQLGrid while calling the comparison budget-matched.
- Treating BIRD, automatic GridDB states, or machine-silver RTS-GMLC/SimBench pairs as power-grid expert gold.

## Figure and table audit

### Strengths

- Figure 1 is code-native, directly tied to the implemented boundary, and explicitly shows externally supplied candidates, the executor, complete-evidence gate, gold isolation, and authorization limits.
- Result captions generally state evidence class and avoid turning diagnostics into confirmatory results.
- Tables retain denominators, failures, unequal call budgets, negative results, and abstention/coverage.

### Required corrections

1. Recreate visual QA from the exact final PDF; the current audit's `visual_qa_root` evidence is stale.
2. Bind lineage for all four used figures, not only Figure 1. Each record must name input tables/JSON, generating code, source hash, rendered hash, and caption claim boundary.
3. Exclude or explicitly label the many unreferenced legacy figures/tables in R2 so they cannot enter a submission package accidentally.
4. Reformat Tables 1 and 2 to avoid very small resized text; split, rotate, or move file-level details to supplementary material.
5. Reduce the nearly empty final page if possible after reference/back-matter layout is frozen; this is a presentation issue, not a scientific defect.

## Reproducibility, ethics, and declarations

### Positive findings

- The v3 independent audit reports the prior-outcome exposure rather than concealing it.
- V1/v2 and BIRD incidents are retained and excluded explicitly.
- All v3 attempts and failures are retained; two canonical reproductions are identical.
- The paper states that generated SQL requires authorized human inspection and is not operational control evidence.
- Author Contributions includes “All authors have read and agreed to the published version of the manuscript.”
- Data Availability contains the requested third-party-license/corresponding-author route and does not claim that GitHub is already synchronized.

### Open integrity and ethics gates

- The current editor/reviewer archive claim is premature because no matching archive exists.
- Qualified-human semantic annotation is absent. If introduced, obtain and report the appropriate institutional ethics/consent determination before data collection; “Not applicable” cannot simply be carried forward without review.
- The corresponding-author email, exact funding agency, funder role, repository release, and license inventory require human confirmation.
- AI disclosure must cover scientific-asset generation/adjudication, not only drafting, editing, code review, and figure preparation.
- Current official journal instructions, including the preferred AI disclosure location and abstract constraints, remain to be rechecked immediately before submission.

## Concrete R3 revision and acceptance checklist

| Priority | Revision | Acceptance evidence |
|---|---|---|
| P0 | Replace stale submission/reviewer/email packages with a round-bound archive; preserve old artifacts as labeled history only. | Clean-extraction verifier; exact R3 source/PDF hashes; allow-list inventory; restricted-file scan; no alternate title. |
| P0 | Correct the round audit and visual provenance. | PDF-bound page-render manifest; current 19-page or final page count; all used figures have lineage; no stale prospective-v3 screenshot cited as current. |
| P0 | Decide how the retained title is scientifically supported. | New matched untouched domain study, or explicit architecture-only positioning plus a visible unresolved title-evidence gate in the cover letter/final audit. |
| P0 | Preserve v3's descriptive evidence class. | Search gate: no v3 occurrence of `prospective-from-freeze`, `confirmatory`, `preregistered`, or unseen outcomes; audit split decision quoted accurately. |
| P1 | Complete qualified domain review if domain-validity claims are desired. | Frozen protocol, qualifications, decisions, adjudication, agreement, ethics determination, re-execution, immutable hashes. |
| P1 | Improve journal narrative and novelty positioning. | Shorter structured abstract; verified agentic/multi-agent Text-to-SQL comparison; explicit contribution-to-evidence map; no uncited novelty claim. |
| P1 | Complete declarations and release governance. | Yang Yong email; author/order/affiliation confirmation; funding agency and role; repository tag/commit; license inventory; stage-specific AI disclosure. |
| P2 | Improve dense tables and final-page economy. | Visual inspection of exact final PDF confirms readable labels at normal zoom and no clipping/collision. |

## Decision rationale

The paper should advance to R3 because the R2 scientific boundary is unusually honest and the implementation/reproducibility contributions are tangible. It should not be marked minor revision or submission-ready because two independent blocking classes remain: (1) the retained title's integrated multi-agent/power-grid robustness proposition lacks matched expert-grounded evidence, and (2) the available submission package and visual audit do not correspond to the frozen R2 manuscript. R3 can close the release-control, narrative, figure, and declaration defects without inventing data. The stronger application claim can be closed only with newly authorized untouched data and qualified human adjudication; another rerun of the same 180 items cannot close it.
