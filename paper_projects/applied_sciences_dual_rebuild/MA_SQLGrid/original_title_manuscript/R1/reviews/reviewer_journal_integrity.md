# Round 1 Independent Review 3: Applied Sciences Fit, Integrity, and Submission Completeness

Review date: 2026-08-08 (Asia/Shanghai)  
Manuscript: **MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases**  
Frozen source SHA-256: `B68685E184F0E5F3DC9698A5E27908AA1640F0FDA4A9B0CEBCFD79E8BB5E909D`  
Frozen PDF SHA-256: `0B9AB819053D462C5E41D1F365EC9CABD34D80146110DAB30220E1F3031D743F`  
Reviewer role: Applied Sciences fit, publication integrity, and submission completeness. This is a read-only independent review; the reviewer did not modify the manuscript, code, data, or evidence.

## Recommendation

**MAJOR REVISION — not a submission candidate in Round 1.**

The manuscript is unusually candid about negative results, gold isolation, failed-run retention, machine-adjudicated silver resources, and the diagnostic-only status of the replay. The LaTeX/PDF build is clean, the main figures are readable, and the required MDPI back-matter categories are present. These are real strengths.

The central editorial problem is nevertheless decisive: the title promises a **robust multi-agent framework**, but no prospective experiment evaluates the implemented five-role coordination core. The completed accuracy and reliability experiments evaluate inherited single-generation prompting procedures or deterministic selection components, while the only direct coordination-core result is candidate-pool coverage without accuracy. The current manuscript therefore does not yet provide the title-level scientific evidence needed for a regular Applied Sciences research article. A live check of the stated GitHub repository also found that its public README and packaged assets describe an older, differently titled C1--C5/gpt-5.4-mini/deepseek study rather than the frozen Qwen/Granite/BIRD/five-role evidence described here. That mismatch independently blocks a reproducibility claim and submission.

## Five Most Serious Issues

### JI-R1-01 — [blocking] The central multi-agent claim has no prospective outcome

The title (line 15), abstract (line 22), contribution list (line 40), and conclusion (lines 284--288) present MA-SQLGrid as a multi-agent framework. Yet the manuscript explicitly states that the GridDB and BIRD experiments were not multi-agent executions (lines 36 and 140), that the replay is not an accuracy experiment (lines 154--156 and 223--246), and that the five-role core has not completed a prospective generation experiment (line 274). The Synthesizer has no model client and only packages external candidates (line 107). Thus, the evidence validates interfaces and trace sealing, not the behavior or benefit of a multi-agent system.

**Required resolution:** execute the pre-registered, budget-matched prospective comparison described at line 278, or weaken the title and all framework-performance language to an implementation/protocol paper. If the original title must be retained, the experiment is mandatory.

**Acceptance test:** a frozen run must compare at least (i) direct single call, (ii) staged single-candidate handoff, (iii) budget-matched multi-candidate validation/adjudication without counterfactual evidence, and (iv) the full condition with pre-registered reference-free state/invariant evidence. Model snapshot, prompts, data order, decoding, candidate budget, physical call accounting, executor, abstention rule, and evaluator must be frozen. Every condition must report strict execution accuracy, safe/valid SQL rate, abstention/coverage, latency/tokens, paired uncertainty, multiplicity handling, incidents, and immutable prediction traces. The abstract and conclusion must report the result even if null or adverse.

### JI-R1-02 — [blocking] “Robust” is not operationally defined or demonstrated for the proposed framework

The only result called a robustness diagnostic is the inherited constructed-state analysis (lines 208--217). It evaluates old predictions, yields no corrected factorial effect, and is explicitly not human-certified semantic equivalence. It does not test whether the five-role controller is robust to paraphrases, schema perturbations, value shifts, database-state changes, model variation, invalid SQL, or missing evidence. The manuscript itself disclaims a universal robustness claim (line 22) and admits that adjudication weights are not independently optimized (line 274). These caveats are honest but do not supply the positive evidence implied by the title.

**Required resolution:** define robustness before analysis as a vector of measurable failure surfaces rather than a rhetorical adjective. At minimum, separate safety robustness, execution robustness, semantic/state robustness, schema/context robustness, and abstention reliability. State which dimensions the paper tests and which remain out of scope.

**Acceptance test:** provide a pre-registered robustness table linking each claimed dimension to perturbation set, experimental unit, endpoint, comparator, denominator, uncertainty procedure, correction family, and pass/fail rule. At least one genuinely prospective robustness dimension must directly evaluate the full MA-SQLGrid condition. If that evidence cannot be generated, remove “Robust” from the title and corresponding claims.

### JI-R1-03 — [blocking] The public repository does not presently reproduce this manuscript

The Supplementary Materials and Data Availability statements (lines 290 and 295) claim that public code and license-cleared reproducibility materials are available at `https://github.com/gaoxingkele/ma-sqlgrid`. On 2026-08-08, the live public repository described the working title “A Multi-Stage Context-Grounding Framework for Reliable Text-to-SQL over Power-Grid Maintenance Databases,” an archived C1--C5 experiment, gpt-5.4-mini/deepseek outputs, and an x10 study. It did not present the current Qwen/Granite factorial protocol, BIRD v1.1 ledgers, five-role `ma_sqlgrid_agents.py` implementation, retrospective replay, or the Round-1 manuscript evidence map. This is not a cosmetic version mismatch: a reader following the paper's data statement would reach a materially different experiment package.

**Required resolution:** publish a release/tag that is exactly aligned with this manuscript or change the statements to identify precisely what is public and what exists only in the editor/reviewer packet. Do not overwrite or silently relabel the old repository history.

**Acceptance test:** from a clean clone of the cited tag/commit, an independent checker must (a) find the exact manuscript-facing code and protocols, (b) verify the input/output hashes cited in the evidence ledger, (c) reproduce every table and plotted value without model calls where archived outputs are used, and (d) obtain all declared unit-test passes. The manuscript, Data Availability statement, README, release manifest, repository commit SHA, license inventory, and restricted-file inventory must agree. The editor/reviewer packet must carry its own manifest and SHA-256 list.

### JI-R1-04 — [major] Novelty cannot be assessed against the relevant multi-agent literature

Related Work covers benchmarks, schema linking, prompting, and constrained decoding, but the section “Agentic Decomposition and Auditable Control” (lines 60--64) contains no citation to multi-agent Text-to-SQL, LLM-agent orchestration, blackboard architectures, deterministic adjudication, or abstaining agent systems. DKA-SQL is discussed as a domain precedent, not as the nearest coordination design. Because several “agents” are deterministic roles and the Synthesizer receives externally generated candidates, the paper must explain why this is substantively a multi-agent framework rather than a modular workflow with typed stages.

**Required resolution:** add a verified nearest-work comparison and adopt a precise operational definition of “agent” used in this manuscript. Identify which roles reason, which are deterministic transforms, which call a model, what state each role owns, and what interaction cannot be reduced to a conventional pipeline.

**Acceptance test:** include a cited comparison table covering at least role autonomy, model calls, shared memory/blackboard, candidate generation, validation, counterfactual/state evidence, gold isolation, abstention, and evaluation budget. All entries must be supported by verified primary sources. Revise novelty claims so they state the exact implemented difference, not generic “multi-agent” novelty.

### JI-R1-05 — [major] The power-grid application evidence is too narrow for the title-level application claim

The primary GridDB case study is synthetic, has eight tables and 98 rows, and uses 180 visible-during-development evaluation questions (lines 86 and 270). RTS-GMLC, SimBench, and NERC-derived resources remain machine-adjudicated silver data (lines 68 and 276), while BIRD is a general public benchmark. No qualified power-grid expert has verified intended projections, units, ordering, tie handling, code semantics, or operational relevance. The Featured Application correctly disclaims operational validation, but the scientific value for “Power Grid Databases” still rests chiefly on one small controlled database.

**Required resolution:** add domain validation without presenting LLM adjudication as human expertise. Prefer a second structurally distinct power-grid relational database and a documented expert semantic audit of a frozen stratified sample. If expert review is infeasible, retain silver labeling and narrow all external-validity language to a synthetic case study.

**Acceptance test:** report database/schema/row/question characteristics for every domain dataset; freeze the sample and annotation protocol; record reviewer qualifications, independent decisions, disagreement and adjudication rules; report inter-reviewer agreement where applicable; and separate human-gold, machine-silver, and diagnostic outcomes in every table. No operational-safety or domain-generalization claim may be made from the current 98-row database alone.

## Claim--Evidence Audit

| Claim/location | Evidence found | Verdict | Required action |
|---|---|---|---|
| Title, line 15: “Robust Multi-Agent Framework” | Five-role code/interface, unit tests, inherited experiments, diagnostic replay; no prospective full-condition outcome | **Unsupported at title strength; blocking** | Satisfy JI-R1-01 and JI-R1-02 or weaken title |
| Abstract, line 22: framework rejects unsafe SQL, abstains, seals trace | Implemented deterministic contracts and code asset are identified in the assembly audit | **Supported as implementation behavior**, not empirical performance | Add test coverage/trace manifest to supplement and avoid benefit language |
| Abstract/results: GridDB, component, BIRD, and multi-state numbers | Frozen inherited audits are identified; denominators and negative results are consistently bounded | **Locally traceable**, subject to full evidence-package audit | Add a compact evidence-lineage table and run IDs in manuscript/supplement |
| Contribution, line 40: integrated 1440/700/25,920/5000 evidence | These experiments do not evaluate the new coordination core | **Accurate lineage but weak contribution alignment** | Separate “framework evidence” from “context/component evidence” visually and rhetorically |
| Lines 96--113: five agents plus deterministic adjudicator | Figure and code describe five roles; Analyst/Cartographer/controller are deterministic and Synthesizer is an external-candidate packager | **Architecture supported; “agent” semantics ambiguous** | Define agency and add nearest-work comparison |
| Line 113: 40/40/10/5/5 scoring weights | Fixed rule exists; line 274 says weights were not independently optimized | **Implemented but scientifically unjustified** | Pre-register rationale and ablate/calibrate without test-set tuning |
| Lines 210--217: constructed-state robustness | 25,920-row inherited ledger; no corrected effect; not human-certified | **Supported only as a diagnostic** | Do not use it as evidence that MA-SQLGrid is robust |
| Lines 225--246: 172/180 replay coverage and zero reference-free CF evidence | Hash-locked retrospective diagnostic report matches the manuscript counts | **Supported as coverage only** | Retain explicit “not accuracy” language |
| Lines 290/295: public reproducibility package contains current assets | Live public repository describes a materially different older study | **Mismatched; blocking** | Satisfy JI-R1-03 |
| Line 292: named funding program/agency | User-supplied record available to this review confirms grant number `521300250006`, but not the exact funding-agency wording | **待作者核实** | Obtain written author confirmation; otherwise state only verified information |
| Line 296: AI use and machine-generated data disclosure | Tool family and purposes are disclosed; author responsibility and non-gold status are stated | **Partially adequate** | Record exact product/model/version or access date, uses in figures/data/study design, and human verification responsibility |

The build resolves all 13 cited keys used by the manuscript, with no undefined citation or cross-reference in the frozen log. This review did **not** independently re-verify every bibliographic record against publishers; a final citation-integrity gate remains required. The uncited agentic-control discussion is a substantive coverage gap, not a LaTeX citation error.

## Experiment Audit

### Required before the title can be retained

1. The budget-matched four-condition prospective coordination experiment specified under JI-R1-01.
2. A prospectively defined robustness evaluation directly involving the full framework, with a declared primary dimension and multiplicity family.
3. An ablation of the deterministic adjudicator: first candidate, validation-only, fixed weighted selector, and counterfactual/state-aware selector under the same candidate pool and no gold access.
4. Resource accounting by condition: physical model calls, generated candidates, input/output tokens, wall time, execution calls, failures, abstentions, and GPU/runtime configuration.
5. A second power-grid schema or a qualified-expert semantic audit sufficient to bound the synthetic case study's domain validity.

### Desirable

- An abstention calibration/risk-coverage analysis and failure taxonomy.
- A learned or strong schema-linking baseline alongside the lexical Cartographer.
- A clean-clone independent reproduction of tables/figures and prospective scores.
- Sensitivity analysis for the 40/40/10/5/5 adjudication weights, performed without tuning on the final evaluation partition.
- A BIRD result table with all four methods, both backbones, denominators, valid-SQL/abstention rates, and corrected comparisons; the current prose-only presentation is difficult to audit.

### Unjustified and prohibited

- Post-hoc gold scoring of the 172 replay selections as if it were a prospective coordination result.
- Relabeling inherited single-generation runs as MA-SQLGrid outcomes.
- Using formal-v5 gold-relative state labels inside the Critic or Adjudicator.
- Treating LLM agreement, machine adjudication, or author review as independent power-grid expert gold.
- Re-running a frozen null-result experiment merely to seek significance, deleting failed calls, or merging incident calls into a new denominator.
- Claiming a DKA-SQL reproduction or head-to-head comparison without its official implementation and matched protocol.

## Figure and Table Audit

| Object | Finding | Severity / action |
|---|---|---|
| Figure 1, PDF p. 5 | The code-native architecture is visually clean and honestly marks external candidates, deterministic adjudication, and gold outside the boundary. Small internal labels approach the lower limit for print reading. | **Minor:** enlarge internal type and add an explicit “implemented/diagnostic; not prospectively evaluated” panel note or caption sentence. |
| Figure 2, PDF p. 8 | Cell estimates are legible and explicitly identify the absence of cell-level error bars. Numeric labels are percentages (e.g., 71.7) while the vertical scale is a 0--1 proportion, which is a mixed convention. | **Minor:** use either proportions everywhere or append percent signs; label the experiment “Inherited GridDB factorial.” |
| Figure 3, PDF p. 8 | Zero line and intervals are readable, but the caption does not state eligible denominators per contrast and “Prospectively frozen” could be mistaken for a prospective MA-SQLGrid evaluation. | **Major:** identify this as the inherited component study, give denominators or a table pointer, and prevent framework attribution. |
| Figure 4, PDF p. 9 | The plot is readable and the caption says constructed-state diagnostic. Its title/caption should also say “inherited predictions,” since it does not evaluate the new framework. | **Major:** add evidence class/run identity and keep robustness scope bounded. |
| Table 1, source lines 164--178 | Clear cell table, but no intervals and no inline evidence/run identifiers. | **Minor:** add evidence class and artifact/run reference; point to registered contrasts. |
| Table 2, PDF p. 10 | Clear, compact, and appropriately says counts are not accuracy. | **Pass**, with a manifest/run identifier desirable. |
| Missing synthesis objects | No table maps each headline result to dataset, condition, generation budget, evidence class, and whether it evaluates the five-role framework. BIRD is prose-only. | **Major:** add an evidence-lineage table and a BIRD results table. |

No clipping, overlap, unresolved label, or visibly broken graphic was found in the inspected 13-page PDF. The framework diagram should remain code-native/vector for label fidelity; generative image synthesis is neither necessary nor preferable for this scientific block diagram.

## Reproducibility, Ethics, and Submission Completeness

### Positive findings

- The manuscript explicitly preserves two failed BIRD incidents and excludes them from scores.
- Gold SQL/results are excluded from pre-evaluation roles and the replay refuses gold-relative counterfactual evidence.
- Machine-adjudicated RTS-GMLC, SimBench, and NERC assets are not called expert gold.
- Human inspection and the non-operational safety boundary are stated prominently.
- Author names and affiliations match the supplied original-title information; Yang Yong is marked corresponding author.
- CRediT-style contributions and “All authors have read and agreed to the published version of the manuscript” are present.
- IRB, informed consent, conflicts, funding, data availability, acknowledgments, and supplementary statements are present.
- The third-party restriction language correctly conditions access on permission and applicable licenses.
- Generative-AI assistance is disclosed and the authors accept responsibility.

### Blocking/manual findings

1. **Corresponding-author email:** line 20 is intentionally a placeholder. This is allowed during drafting but blocks portal upload. Acceptance test: the author supplies and verifies the email; the final package must remain labelled “not ready for portal upload” until then.
2. **Funding identity:** only grant number `521300250006` is confirmed in the supplied instruction. The exact “Science and Technology Project of NARI Group Corporation…” wording and the line-297 no-funder-role declaration require explicit author confirmation. Do not infer the agency from affiliation.
3. **Repository/package synchronization:** resolve JI-R1-03. The current ROUND_AUDIT establishes local file integrity, not public reproducibility.
4. **Restricted-data governance:** include a file-level license/restriction inventory, permitted reviewer access route, retention/deletion rule, and confirmation that no restricted data or model weights were pushed publicly.
5. **AI disclosure:** identify exact tools/models or stable product descriptors, purposes, and whether any manuscript figures, constructed questions, labels, analysis text, or code were generated or transformed. State the authors' verification process. If no GPTImg2/Gemini-generated figure is used, say so in the provenance record rather than implying it.
6. **Abstract length:** the abstract is approximately 288 whitespace-delimited words and visually fills most of page 1. The local requirements snapshot does not freeze a word limit, so this is **待核实**, but it should be checked against the current Applied Sciences instructions and shortened to the permitted limit without deleting negative-result boundaries.
7. **Version metadata:** the PDF footer says “Version August 5, 2026,” whereas the frozen review is dated August 8. Synchronize version metadata before the next round.

## Round-1 Acceptance Conditions

The journal/integrity reviewer will consider this report resolved only when all of the following are documented in the Round-2 response matrix:

- [ ] JI-R1-01: a frozen prospective full-framework experiment is completed and independently recomputed, or the title/claims are weakened.
- [ ] JI-R1-02: robustness is operationally defined and directly tested, or “Robust” is removed.
- [ ] JI-R1-03: the cited public release and editor/reviewer packet match the manuscript and pass a clean-clone reproduction/hash audit.
- [ ] JI-R1-04: verified multi-agent/agentic Text-to-SQL nearest work and an operational agent definition are added.
- [ ] JI-R1-05: power-grid external validity is strengthened with a second schema and/or qualified expert semantic audit, with gold/silver/diagnostic labels preserved.
- [ ] Every headline number is mapped to an immutable artifact and an evidence class; figure/table values match those artifacts.
- [ ] Abstract, Results, Discussion, and Conclusions make no stronger claim than the prospective evidence.
- [ ] Funding agency wording and funder-role statement are explicitly confirmed by the authors.
- [ ] Yang Yong's verified email is inserted before portal upload; until then, the package is labelled not portal-ready.
- [ ] The AI-use statement and figure/data provenance identify exact tools, purposes, and author verification.
- [ ] Restricted and public artifacts have a license/restriction inventory and no unauthorized upload occurred.
- [ ] A final citation audit verifies every cited bibliographic record and claim context; the build remains free of undefined citations/references and fatal layout defects.

## Decision Rationale

The manuscript has a credible integrity posture and an unusually good record of negative and diagnostic evidence. Its current limitation is not a missing disclaimer; the disclaimers are already clear. The limitation is that the evidence does not test the system named in the title. That gap cannot be solved by prose alone while retaining “Robust Multi-Agent Framework.” A genuinely prospective, budget-matched coordination/robustness experiment, plus synchronization of the public evidence package, is the minimum path to a defensible Round-2 manuscript.
