# Round 1 Independent Review: Power-Grid Application and Engineering Value

## Reviewer identity and scope

I reviewed the frozen R1 MA-SQLGrid manuscript as a power-system data and utility-software application reviewer. The review covers domain terminology, database representativeness, operational safety, external validity, engineering value of the role decomposition, and the boundary between machine/silver labels and qualified human review. I inspected `paper_applsci.tex`, the 13-page PDF, `R1_ASSEMBLY_AUDIT.md`, the implemented coordination core, the GridDB data card, the RTS-GMLC and SimBench pilot reports, and the candidate human-review packet. I did not edit the manuscript or code and did not consult the other reviewers.

## Recommendation

**Recommendation: major revision.**

The manuscript is unusually explicit about negative results and inherited-versus-new evidence, and its build and artifact retention are strong. However, the title's two central engineering qualifiers---**robust** and **multi-agent**---are not yet validated by a prospective run of the implemented coordinator. The only power-grid primary corpus is a small, development-visible synthetic database whose 200 question--SQL pairs have no documented independent domain review. BIRD usefully tests public cross-database behavior, but it cannot establish power-grid validity. The paper is therefore not ready for submission in its current title-preserving form. The most direct route is a prospectively frozen, budget-matched coordinator experiment plus qualified semantic review of domain data and a stronger executor-safety evaluation.

**Confidence: 4/5.** The evidence boundary is clear enough for a high-confidence application assessment; I did not independently recompute every statistical result and defer inferential details to the methods/statistics reviewer.

## Five most serious issues, ordered by decision impact

### 1. [BLOCKING] The implemented artifact has not demonstrated the title's robust multi-agent claim

- **Severity:** Critical
- **Evidence anchors:** `paper_applsci.tex:15`; `paper_applsci.tex:36--42`; `paper_applsci.tex:274--278`; `original_title_rebuild/ma_sqlgrid_agents.py:240--245`; `original_title_rebuild/RETROSPECTIVE_DIAGNOSTIC_REPORT.md`, “Permitted interpretation”.
- **Finding:** The title presents a robust multi-agent framework, but the manuscript itself states that the inherited GridDB and BIRD experiments are not multi-agent runs, the new Synthesizer only packages externally supplied candidates, and the five-role core has not completed a prospectively frozen generation experiment. The replay reports candidate-pool coverage only. Thus implementation existence is supported, whereas coordination efficacy, robustness gain, and superiority over a budget-matched pipeline are not.
- **Why this blocks advancement:** This is a title--evidence mismatch at the central contribution, not a request for a larger baseline table. The defect remains even though the limitations are candid.
- **Required revision:** Execute the already proposed four-condition, hash-frozen, budget-matched experiment: direct single candidate; staged analyst/cartographer with one candidate; fixed multi-candidate validation/adjudication without counterfactual evidence; and the same pool with a preregistered reference-free state/invariant suite. Hold model snapshot, questions, candidate count, physical calls, decoding and states constant. Report execution correctness, safe-executable rate, abstention/coverage, selective risk, latency, tokens/calls and retained incidents. If this cannot be executed, the title and abstract must be narrowed so that “robust” and “multi-agent” describe only an unevaluated software architecture, not demonstrated behavior.
- **Acceptance test:** A new immutable protocol and run manifest exist; every final prediction traces to a sealed blackboard; no gold field is available before selection; all scheduled calls and failures are retained; the primary coordinator contrasts and uncertainty/multiplicity results are in Results, the evidence ledger, abstract and conclusion with identical denominators.

### 2. [BLOCKING] Power-grid semantic validity is not established for the primary corpus

- **Severity:** Critical
- **Evidence anchors:** `paper_applsci.tex:86`; `paper_applsci.tex:270`; `round1_revision_assets/GRIDDB_DATA_CARD.md`, “Exposure and annotation status”; `data/human_review_packet/W4_MA_HUMAN_REVIEW_PACKET_REPORT.md`, “Status and non-substitution boundary”.
- **Finding:** GridDB has only eight tables and 98 rows; 120 of 200 questions are deterministic template expansions; its evaluation partition and rule patterns were visible during development; and no independent dual-expert semantic review of its 200 question--SQL pairs is documented. The external review packet does not repair this gap: it contains 91 machine-generated RTS-GMLC/SimBench candidates and records **zero** human-reviewed and **zero** sealed items. Successful SQL execution proves mechanical consistency, not correct intent, units, tie policy, topology semantics, or usefulness to a utility analyst.
- **Why this blocks advancement:** Without verified domain semantics, the manuscript cannot substantiate the “in Power Grid Databases” application claim beyond a synthetic schema demonstration. This requirement follows the project's own data-card and review-packet promotion gates; it is not an attempt to relabel machine evidence as expert gold.
- **Required revision:** Have two qualified power-system/data reviewers independently assess all primary GridDB items used for the confirmatory domain result, lock their decisions, adjudicate every conflict through a third qualified reviewer, re-execute revised SQL, and freeze new hashes. Record qualifications, coverage, dispositions, disagreement, adjudication, units, ordering/tie handling, empty-result decisions and access history. An LLM may assist triage but must remain machine assistance and must not be called a human or domain expert.
- **Acceptance test:** The package contains two locked independent forms, an adjudication ledger, 100% coverage of the reported domain set, execution/result hashes after revision, and a data card that distinguishes human-reviewed-unsealed from genuinely sealed items. The manuscript reports the actual status and does not infer natural-query representativeness from template expansions.

### 3. [BLOCKING] The read-only claim is a lexical gate, not yet an operational security boundary

- **Severity:** Major
- **Evidence anchors:** `paper_applsci.tex:80`; `paper_applsci.tex:107`; `paper_applsci.tex:264`; `original_title_rebuild/ma_sqlgrid_agents.py:18--22`; `original_title_rebuild/ma_sqlgrid_agents.py:271--325`.
- **Finding:** The Validator checks a leading `SELECT`/`WITH`, comments, semicolons and a forbidden-keyword regex, then calls a supplied executor. The inspected core does not itself enforce SQLite `query_only`, a database authorizer/allowlist, extension disabling, immutable database copies, resource/time/result-size limits, filesystem/process isolation, row/column authorization, or output-data handling. A syntactically read-only query can still exhaust resources, invoke enabled functions, enumerate sensitive records, or return an unsafe volume. The manuscript correctly says read-only is not operational certification, but the Featured Application still presents experimental decision support.
- **Required revision:** Specify and implement the executor trust boundary, not just the SQL-string gate. Add fail-closed tests for nested/recursive CTEs, dangerous functions/extensions, oversized results, long-running queries, malformed Unicode/comments, unauthorized tables/columns, and cancelled execution. Separate “lexically admissible”, “database-enforced read-only”, “resource-bounded”, and “authorized for this user” in both evidence and terminology. Keep human inspection as a final operational gate.
- **Acceptance test:** A documented sandboxed executor uses a disposable/immutable snapshot and database-enforced read-only policy; adversarial tests demonstrate no mutation and bounded termination; the validator trace records timeout, authorization and output-limit failures; the manuscript does not equate lexical safety with operational safety.

### 4. [MAJOR] BIRD does not supply power-grid external validity, while the power-grid external assets remain silver

- **Severity:** Major
- **Evidence anchors:** `paper_applsci.tex:68--70`; `paper_applsci.tex:88`; `paper_applsci.tex:219--221`; `paper_applsci.tex:276`; `data/rts_gmlc_pilot/W3_RTS_GMLC_REPORT.md`, “Scientific limitations”; `data/simbench_pilot/W3_SIMBENCH_REPORT.md`, “Promotion gate and limitations”.
- **Finding:** BIRD Mini-Dev is valuable public benchmarking across 11 databases, but it is not a power-grid corpus and the tested four prompting procedures are not the new coordinator. RTS-GMLC and SimBench provide authentic power-system structures, yet their 55 and 36 NL--SQL pairs are deterministic `AUTO_CANDIDATE` resources with no independent domain review and no sealed test. Therefore BIRD supports software portability to a public benchmark; it does not validate field deployment or transfer to utility databases.
- **Required revision:** Keep BIRD as a general cross-database stress test, label that role explicitly in every relevant table/caption, and add at least two semantically reviewed power-grid relational cases with different schema/workload profiles if a domain-general claim is retained. Do not generate more silver questions merely to increase the denominator. Resolve the RTS-GMLC notice and SimBench ODbL/DbCL redistribution conditions before packaging derived databases.
- **Acceptance test:** Results separate (a) synthetic GridDB development evidence, (b) public non-grid BIRD transfer evidence, and (c) reviewed power-grid external evidence. No conclusion uses BIRD accuracy as evidence of power-grid validity. Every released external asset has a recorded license/status decision.

### 5. [MAJOR] The engineering value of individual roles and adjudication weights is untested

- **Severity:** Major
- **Evidence anchors:** `paper_applsci.tex:105--113`; `paper_applsci.tex:225--246`; `paper_applsci.tex:254--260`; `paper_applsci.tex:274`; `original_title_rebuild/ma_sqlgrid_agents.py:365--419`.
- **Finding:** The Analyst and Cartographer are deterministic skeletons, the Synthesizer has no model client, the Counterfactual Critic receives zero reference-free evidence in the replay, and the Adjudicator uses unoptimized 40/40/10/5/5 weights. Candidate availability for 172/180 questions proves interface coverage, not that any role improves correctness, safety, abstention or cost. The current role naming risks making a typed pipeline appear more mature than its evidence.
- **Required revision:** Add role-level ablations and failure-injection tests within the prospective design: analyst/cartographer handoff on/off; validation-only versus validation plus adjudication; critic unavailable versus preregistered evidence; and fixed weight/rule sensitivity. Report when each role changes a decision, rescues an error, causes harm, abstains, or adds latency/calls. Treat weights as a frozen engineering policy unless independently tuned on development-only data.
- **Acceptance test:** Each claimed role has a measurable contract, an exercised failure mode and at least one reported outcome/cost endpoint. Counterfactual contribution is either prospectively measured with reference-free evidence or removed from empirical contribution language. Sensitivity analysis shows whether conclusions depend on arbitrary score weights.

## Claim--evidence audit

| Claim/location | Available evidence | Domain verdict | Required action |
|---|---|---|---|
| Title, `paper_applsci.tex:15`: robust multi-agent framework | Implemented typed roles and unit-tested coordinator; no prospective coordinator run | **Not established as an empirical claim** | Complete Issue 1 or narrow title/claim semantics |
| Featured Application, `paper_applsci.tex:24`: experimental read-only decision support | Lexical SQL guard, execution evidence and abstention; explicit human-inspection warning | **Partially supported; not operationally secured or validated** | Complete Issue 3 and state the user/permission/output boundary |
| Contributions, `paper_applsci.tex:40`: 1440 + 700 + 25,920 + 5000-call integration | Frozen inherited ledgers, audits and matching denominators in assembly audit | **Supported as asset integration** | Add evidence-class tags beside every table/figure; never relabel as coordinator performance |
| Data, `paper_applsci.tex:86`: GridDB counts and construction | Data card supports eight tables, 98 rows, 200 records and visible development exposure | **Counts supported; application representativeness unsupported** | Add expert semantic audit and retain synthetic/unsealed labels |
| BIRD, `paper_applsci.tex:88, 221`: 500 items/11 databases and reported accuracies | Retained v1.1 ledgers and independent re-execution are cited in the local audit | **Supported for this public protocol; not power-grid validity** | Keep as non-grid transfer evidence and report version/runtime prominently |
| Coordination diagram and roles, `paper_applsci.tex:96--109` | Source implements trace, packaging, lexical grounding, validation and critic interfaces | **Supported as software architecture** | Show external candidate provider and executor trust boundary more prominently |
| Retrospective coverage, `paper_applsci.tex:225--246` | Hash-locked replay supports 180/173/172/7/1 and zero reference-free CF evidence | **Supported as diagnostic only** | Retain no-accuracy/no-gain wording |
| Engineering value, `paper_applsci.tex:254`: typed contracts make future comparison falsifiable | Append-only trace and gold isolation support auditability | **Supported for auditability; performance/safety value untested** | Add prospective and adversarial evaluations |
| Silver boundary, `paper_applsci.tex:276, 296` | Pilot reports and review packet explicitly record machine-only status | **Correctly bounded** | Preserve; LLM review cannot be promoted to human-expert review |
| Conclusion, `paper_applsci.tex:284--288` | Accurately distinguishes inherited evidence from unproven coordinator | **Internally honest but in tension with title** | Resolve Issue 1 before submission |

## Experiment audit

### Required before a title-preserving submission candidate

1. **Prospective coordinator comparison:** the four-condition, call-budget-matched design specified under Issue 1, with sealed gold boundary and immutable outputs.
2. **Qualified domain review:** dual independent review and third-person adjudication of the domain question--SQL/result semantics used for primary claims. Report actual reviewer status; no API model may be described as a human expert.
3. **Executor and authorization red team:** adversarial SQL, resource exhaustion, unauthorized relation/column access, output-volume and cancellation tests against an immutable database copy.
4. **Role/mechanism ablation:** separate candidate-count effects from role handoffs, validation, adjudication and counterfactual evidence; report rescue, harm, abstention, latency and physical calls.
5. **External domain validation:** at least two different reviewed power-grid database structures if the paper retains language beyond “one synthetic case study”. BIRD remains a non-grid transfer benchmark.

### Desirable, not blocking by itself

- Report accuracy--coverage or risk--coverage curves for abstention instead of only a binary abstain count.
- Include unit, temporal-window, topology-direction, tie-policy and code-mapping challenge subsets designed or approved by qualified reviewers.
- Add schema drift, renamed-column, missing-value, stale-code-list and permission-view tests that reflect database maintenance conditions.
- Compare deterministic adjudication with first-candidate selection and budget-matched voting under the same candidate pool.
- Report per-query wall time, generation time, validation time, peak result rows and failure reason distribution.

### Reruns that would be unjustified or misleading

- More BIRD calls alone do not validate power-grid semantics or the multi-agent core.
- More LLM-generated RTS-GMLC/SimBench questions do not repair the lack of qualified human review.
- Post-hoc gold scoring of the retrospective replay cannot become a prospective coordinator result.
- Gold-relative formal-v5 state labels must not enter the Critic or Adjudicator.
- DKA-SQL reproduction or head-to-head language is unjustified without its official implementation and matched evaluation boundary.

## Figure and table audit

- **Figure 1 (PDF p. 5; `paper_applsci.tex:98--103`)** is legible and honestly shows external SQL candidates and gold outside the coordination boundary. For R2, show the executor/database as a separate untrusted boundary and distinguish lexical filtering, database-enforced read-only execution, user authorization and offline gold evaluation. The small fine print should remain readable at journal column width; a vector PDF generated from the lineage-bound SVG is preferable to the current PNG derivative.
- **Table 1 and Figure 2 (PDF pp. 7--8; `paper_applsci.tex:164--187`)** match the stated 180-per-cell point estimates. Their captions should explicitly add “Inherited single-generation experiment; not MA-SQLGrid coordination” and identify F00--F11 factors without requiring the reader to search Methods. Point estimates without cell intervals are acceptable only because registered contrasts are described separately; do not imply the cell plot is inferential.
- **Figure 3 (PDF p. 8; `paper_applsci.tex:201--206`)** visually matches the stated component effects. Add the evidence class and backbone denominators to the caption and avoid letting “prospectively frozen” be read as prospective evaluation of the new five-role core.
- **Figure 4 (PDF p. 9; `paper_applsci.tex:212--216`)** makes the null/corrected result visible. Its internal title says “Retrospective multi-state reliability effects”; the caption must continue to say constructed states, 66 order-insensitive questions and no operator-certified robustness. Consider replacing “reliability” with “constructed-state agreement” in the figure itself.
- **Table 2 (PDF p. 10; `paper_applsci.tex:227--244`)** clearly reports coverage and zero counterfactual evidence. It should additionally state that the candidate pool mixes two backbones/four prompt packages and that the 172 adjudications are not deployable outcomes.
- Add an evidence-status column or standardized caption prefix (`Inherited`, `Diagnostic`, `New`) to every quantitative table and figure. This would materially reduce the risk that reviewers attribute inherited results to the multi-agent coordinator.

## Reproducibility, ethics and operational-risk findings

### Positive findings

- The assembly audit records a clean 13-page build with no unresolved citations, references, overflow or fatal errors and provides SHA-256 values for the manuscript, bibliography, PDF and major figures.
- Failed BIRD attempts are retained and excluded rather than overwritten, and the manuscript states the physical incident-call count.
- Gold SQL/results are explicitly outside the pre-selection interfaces, and the replay refuses gold-relative counterfactual evidence.
- The manuscript discloses AI assistance and says machine-generated candidates are not human/domain-expert ground truth.
- The limitations state that GridDB is synthetic, development-visible and not production evidence.

### Unresolved findings

- GridDB redistribution permission remains unresolved in its data card. The Data Availability Statement's “upon reasonable request” route is appropriately conditional on third-party permission, but the editor/reviewer package must list exactly what can and cannot legally be supplied.
- The human-review packet is only a prepared protocol: all 91 RTS-GMLC/SimBench items remain machine candidates with zero completed human reviews and zero sealed items.
- “Institutional Review Board Statement: Not applicable” is consistent with the present package because no human annotation was performed. If qualified reviewers are recruited for research data validation, the authors must document the applicable institutional determination, consent/confidentiality handling and role; this review does not make that determination for them.
- Read-only SQL is not equivalent to user authorization, data minimization or safe operational use. No result from this paper should trigger maintenance, protection, dispatch, switching or asset-management action without authorized source-row inspection and existing utility controls.
- The repository URL and license-cleared availability statement were not network-verified in this offline review; release readiness remains subject to a final public-package check.

## Concrete revision requirements and round-gate tests

### Blocking for R1-to-R2 claim advancement

| ID | Required change | Verification/acceptance test |
|---|---|---|
| PG-B1 | Freeze and run a prospective budget-matched coordinator experiment, or narrow the robust/multi-agent title claim | Protocol hash, complete call ledger, sealed traces, retained failures, registered contrast table, and consistent abstract/conclusion |
| PG-B2 | Complete qualified semantic review of the primary domain set | Two locked independent reviews, third-party adjudication, 100% item coverage, revised-SQL execution hashes, status-aware data card |
| PG-B3 | Strengthen and test the executor security boundary | Immutable database copy, DB-enforced read-only/authorization, resource limits, adversarial tests, explicit failure fields |

### Major revisions

| ID | Required change | Verification/acceptance test |
|---|---|---|
| PG-M1 | Separate BIRD portability from power-grid external validity | Every BIRD claim/caption labels it non-grid; at least two reviewed grid schemas for broader domain claims, or conclusions narrowed |
| PG-M2 | Demonstrate role-level engineering value and weight sensitivity | Prespecified role ablations, rescue/harm/abstain/cost results, no candidate-budget confounding |
| PG-M3 | Add evidence-class labels to all quantitative displays | Each table/figure caption says Inherited/Diagnostic/New and names its run identity/denominator |
| PG-M4 | Close redistribution and reviewer-package inventory | License/status matrix and file-level editor-access manifest agree with Data Availability Statement |

### Minor revisions

| ID | Required change | Verification/acceptance test |
|---|---|---|
| PG-m1 | Replace ambiguous operational uses of “reliability”/“robustness” with the measured endpoint where appropriate | Search audit shows constructed-state agreement is not described as operational certification |
| PG-m2 | Define domain coding, units, timestamps and topology directionality in a compact data dictionary table | Every GridDB field used by reported questions has type/unit/code semantics or an explicit not-applicable value |
| PG-m3 | Add verified literature on utility information models and operational data governance | Citation audit confirms primary/authoritative sources; **[FIELD-NORM UNVERIFIED]** until the authors identify and verify the applicable standards |
| PG-m4 | State the corresponding-author email as an unresolved manual action | Final package remains labelled not ready for portal upload until the placeholder at `paper_applsci.tex:20` is replaced by the authors |

## Questions for the authors

1. Who authored and technically checked the 80 non-template GridDB questions, and what power-system/database qualifications did those checkers have?
2. What database-level mechanism, if any, enforces read-only behavior independently of the regex Validator, and what timeout/result-size/authorization limits apply?
3. What operational user is the intended reader of returned rows---maintenance planner, asset manager, dispatcher, protection engineer, or database analyst---and which decisions are explicitly out of scope?
4. Can the proposed reference-free counterfactual states be defined from schema invariants without consulting gold SQL/results, and how will their domain validity be approved?
5. Will the title-preserving version wait for the prospective coordinator and qualified domain-review gates, or will “robust” be explicitly defined as trace/safety behavior only?

