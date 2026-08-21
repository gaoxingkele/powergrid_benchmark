# Round 2 Independent Review: Power-Grid Application and Engineering Safety

## Reviewer identity and scope

I reviewed the frozen MA-SQLGrid R2 source, current 19-page PDF, R2 assembly
and round audits, the R1 power-grid review and response matrix, the SQLite
read-only executor and its tests, and the v3 metamorphic release and independent
release audit. I acted as a power-system data/application and utility-software
safety reviewer. I did not modify the manuscript, code, figures, data, or prior
review records, and I did not consult the other R2 reviewers.

## Recommendation

**Major revision. Conditional approval to enter R3 under the original title,
but not approval for submission.**

R2 is substantially more honest and technically concrete than R1. It now
defines robustness as a vector of tested properties, implements a real
database-level read-only boundary, reports failures, separates BIRD from
power-grid validity, and correctly downgrades v3 to a descriptive analysis
after the independent audit found same-item outcome access. The original title
can remain as the identity of an implemented framework during R3 because the
abstract and conclusion explicitly limit what “robust” means. It is not yet a
fully substantiated empirical title for submission: the five-role framework has
no untouched end-to-end evaluation, GridDB has no qualified semantic review,
and the only full-versus-validation change is an outcome-exposed, constructed
projection case. Several submission gates require real author or qualified
human action and cannot be closed by an AI agent.

**Confidence: 5/5.** The central domain and safety boundaries are stated in the
manuscript and are directly inspectable in the retained code, tests, ledgers,
and independent audit.

## Five most serious issues, ordered by decision impact

### 1. [BLOCKING FOR SUBMISSION] “Robust multi-agent” remains a framework label, not an end-to-end demonstrated system property

- **Severity:** Major
- **Evidence Anchor:** `text: paper_applsci.tex:409 “the system has not completed a new-generation experiment on an evaluation resource whose outcomes were previously inaccessible”`
- **Confidence:** 5/5 — directly stated limitation and audited evidence lineage
- **Finding:** R2 implements five typed roles, but the Analyst and Cartographer
  are deterministic skeletons, the Synthesizer packages external historical
  candidates, and the v3 run evaluates deterministic selection over an existing
  pool. The independent release audit also fails prior-outcome independence.
  Therefore R2 supports an auditable architecture and tested mechanisms, not a
  robust five-agent generation process or a multi-agent performance benefit.
  The manuscript is admirably explicit about this, but the title will still be
  read as an empirical claim unless the limitation is made inseparable from the
  title claim throughout the paper and cover letter.
- **Required revision:** Retain the original title only as a framework name in
  R3. Add a one-sentence operational definition near the first title-method
  claim: in this article, “multi-agent” denotes five typed roles sharing a
  blackboard, while “robust” denotes only the tested SQLite safety, bounded
  execution, complete-evidence, and three-witness invariance mechanisms. Do not
  use “robust framework” as shorthand for accuracy, autonomous collaboration,
  domain validity, or deployment readiness. A stronger empirical title claim
  requires a new untouched, budget-matched end-to-end evaluation under separate
  authorization.
- **Acceptance test:** A search of title, abstract, contributions, captions,
  discussion, conclusion, cover letter, and repository README finds no
  unqualified multi-agent gain, universal robustness, autonomous-agent, or
  deployment claim. The evidence ledger maps every use of “robust” to a tested
  dimension in Table `tab:robustness` or labels it as framework nomenclature.

### 2. [BLOCKING FOR SUBMISSION] Power-grid semantic validity is still unverified, and Q039 exposes the exact problem

- **Severity:** Critical
- **Evidence Anchor:** `dataset: GridDB questions.jsonl Q039 and paper_applsci.tex:371`
- **Confidence:** 5/5 — direct inspection of the question, gold SQL, candidates, and selected trace
- **Finding:** GridDB remains synthetic, development-visible, and without
  independent dual-expert review. Q039 asks, “Show the first scheduled work
  order after June 2024,” but the frozen gold uses
  `scheduled_date > '2024-06-01'` and does not require
  `status = 'scheduled'`. A qualified reviewer could reasonably interpret
  “after June 2024” as after 30 June and “scheduled work order” as a status
  constraint. The sole full-versus-validation improvement therefore shows
  conformity to one frozen projection and date interpretation, not established
  power-grid semantics. Mechanical execution and strict result equality cannot
  adjudicate this ambiguity.
- **Required revision:** Keep Q039 as a software trace, but explicitly state
  that its temporal and status semantics are unverified and that “correct” means
  equality to the frozen synthetic reference. Before using GridDB as scientific
  evidence of power-grid semantic correctness, two qualified power-system/data
  reviewers must independently review the reporting set, with a predefined
  rubric and third-person conflict adjudication. AI/LLM or author-only review
  may assist triage but cannot be reported as independent expert validation.
- **Acceptance test:** R3 includes a compact Q039 case table with the natural
  language, C000, C001, M3 effect, frozen reference interpretation, and semantic
  ambiguity. No sentence calls Q039 an engineering correctness rescue. For
  submission, locked reviewer forms, qualifications, complete coverage,
  disagreement/adjudication records, revised hashes, and re-execution outputs
  must be present; otherwise GridDB remains explicitly synthetic and
  semantically unverified.

### 3. [MAJOR] The executor is genuinely read-only and bounded in tested ways, but it is not a complete authorization or resource-containment boundary

- **Severity:** Major
- **Evidence Anchor:** `text: paper_applsci.tex:151 “They do not establish user entitlement, data minimization, process isolation, or operational authorization.”`
- **Confidence:** 5/5 — source and adversarial tests inspected
- **Finding:** `mode=ro&immutable=1`, `query_only`, the authorizer, disabled
  extensions, progress callbacks, and the row cap are valuable improvements.
  Tests cover writes, DDL, ATTACH, PRAGMA, metadata, table/column denial,
  recursive work, row overflow, and retained traces. However, the v3 run's
  table/column allowlist is the full parsed schema plus probe columns rather
  than a user-specific entitlement policy. The executor limits rows, opcodes,
  and elapsed progress checks but not result bytes, cell size, output column
  count, or process memory. Its function policy is a small denylist, so one
  expensive allowed scalar function or one enormous value can exceed practical
  resources before a row cap helps. “Column limit” currently means column
  authorization, not a maximum number of returned columns.
- **Required revision:** Separate four controls in prose and traces:
  database-enforced non-mutation, registered schema authorization, resource
  bounding, and real user authorization. Rename “column limit” to “column
  allowlist” wherever appropriate. Add a result-byte/cell-byte and output-column
  budget, prefer an explicit allowed-function policy for operational profiles,
  and add adversarial tests for oversized scalar values and wide projections.
  If process isolation is intentionally out of scope, retain that limitation
  and do not call the executor sandboxed or production-safe.
- **Acceptance test:** Tests demonstrate denial or bounded failure for an
  oversized single-row value, an over-wide projection, unauthorized
  table/column reads, and recursive work; traces identify the distinct failure
  classes. The manuscript states whether the R2 study used a full-schema
  research allowlist or a user-specific policy. No tested executor property is
  equated with organizational authorization.

### 4. [MAJOR] Q039 is a constructed projection-stability witness, not evidence of counterfactual reasoning or broad robustness

- **Severity:** Major
- **Evidence Anchor:** `figure: paper_applsci.tex:371 Q039 trace and Figure fig:offline`
- **Confidence:** 5/5 — selection ledger, witness manifest, and audit agree
- **Finding:** M3 deliberately adds a nullable column to `work_orders`.
  Consequently, `SELECT *` changes arity while an explicit projection does not.
  This is a useful schema-evolution regression rule, but it is designed to
  penalize wildcard projection and it changes only one of 180 decisions. The
  same Q039 effect was already visible in v2 before the v3 freeze. The R2 text
  mostly handles this correctly; the remaining risk is that the 101 versus 100
  count, “Counterfactual Critic” role name, or robustness graphics cause readers
  to infer a general benefit that the study cannot establish.
- **Required revision:** Report the case primarily as a qualitative failure
  trace and place 1/180 beside every graphical or tabular mention of the
  increment. State that M1--M3 are three operator families, not independent
  deployment samples, and that the Q039 rule is both constructed and
  outcome-exposed. Retain the reversed-tie result (117--118/180) next to the
  primary count because it is the strongest evidence about rule dependence.
- **Acceptance test:** A reader can recover from one table/figure caption that
  (i) v3 is descriptive, (ii) Q039 is the sole difference, (iii) M3 was designed
  to expose wildcard arity, (iv) the same-item outcome had entered the frozen
  pre-run test, and (v) reversed order changes the result substantially. No
  “counterfactual gain” or “robustness improvement” wording remains.

### 5. [BLOCKING FOR RELEASE] External-domain and licensing gates remain open

- **Severity:** Major
- **Evidence Anchor:** `table: paper_applsci.tex:107--111, Table tab:resources`
- **Confidence:** 5/5 — manuscript, response matrix, and data-availability statement agree
- **Finding:** BIRD is correctly labelled a public non-grid portability
  benchmark, so it cannot validate power-grid semantics. RTS-GMLC and SimBench
  provide authentic engineering structures but their question--SQL pairs have
  zero completed qualified reviews and zero sealed items. The manuscript also
  records unresolved RTS source-use and SimBench ODbL/DbCL redistribution
  review. These assets strengthen transparency and future-study design, but not
  current external power-grid accuracy.
- **Required revision:** Keep the three evidence classes separated in every
  claim and package inventory: synthetic/development-visible GridDB, public
  non-grid BIRD, and authentic-structure machine-silver RTS/SimBench. Do not
  distribute source-dependent derivatives until the responsible author has
  completed a file-level license decision. Restricted editor/reviewer access
  remains subject to third-party permission; a request route is not itself a
  license grant.
- **Acceptance test:** The final archive manifest records origin, derivative
  status, license, redistribution decision, public/restricted location, and
  human-review status for every external asset. The public repository clean
  clone contains no restricted source. BIRD is never cited as power-grid
  validation, and machine-silver data are never called expert gold.

## Claim--evidence audit

| Claim/location | Evidence available in R2 | Power-grid/application verdict | R3 action |
|---|---|---|---|
| Title and abstract: robust multi-agent framework | Five implemented typed roles, blackboard, executor, fail-closed adjudicator; no untouched end-to-end generation study | **Supported as a bounded architecture identity; not as a demonstrated multi-agent gain** | Add the operational title definition and keep all exclusions adjacent |
| Featured Application, line 24 | Read-only research executor and explicit human-inspection warning | **Appropriately cautious** | Preserve; add that authorization must be configured outside the framework |
| Executor boundary, lines 151 and 399 | Source and tests establish non-mutation, schema allowlisting, row/opcode/time controls | **Supported for tested SQLite boundary; incomplete for memory, byte volume, process isolation, and user entitlement** | Complete Issue 3 or narrow resource-bound wording |
| Robustness vector, lines 159--175 | Table separates mutation, resource, evidence coverage, metamorphic invariance, and semantic validity | **Good operational framing** | Add “tested/not tested” status and ensure “column limit” is not confused with output width |
| GridDB, lines 86 and 107 | 8 tables, 98 rows, 200 records; development visibility documented | **Counts supported; natural-query and domain-semantic validity unverified** | Retain synthetic case-study label; require qualified review for promotion |
| Q039, lines 22 and 371 | Complete trace shows wildcard arity failure and explicit projection selection | **Mechanism supported; semantic rescue and general robustness unsupported** | Add the ambiguity/case table and 1/180 boundary |
| BIRD, lines 88, 297--323 | Retained 500-item/11-database audit and unequal calls | **Supported non-grid workflow portability evidence only** | Preserve exact label and unequal-call caveat |
| RTS-GMLC/SimBench, lines 68, 94, 109--110, 411 | Authentic structures; machine-silver question--SQL; 0 reviewed/0 sealed | **No external domain accuracy evidence** | Human review and license decisions remain manual gates |
| Conclusion, lines 419--423 | Matches descriptive v3 and inherited negative results | **Substantively honest** | Keep the final operational definition of “robust” and avoid stronger cover-letter language |

## Experiment audit

### Required before submission under the original title

1. **Untouched end-to-end test:** a prospectively frozen evaluation resource
   whose outcomes have not appeared in development, tests, reports, or earlier
   runs; budget-match the candidate-generation and coordination conditions.
2. **Qualified power-grid semantic review:** dual independent review with
   predefined rubric and third-person adjudication for the domain reporting set.
3. **Executor containment extension:** result-byte/cell-byte/output-width tests
   and an explicit distinction between research-schema allowlisting and user
   authorization.
4. **Q039 semantic adjudication:** independently decide the date boundary,
   status interpretation, projection, ordering, and tie policy; retain the old
   record and any revised record rather than silently overwriting it.
5. **External release review:** resolve RTS-GMLC/SimBench derivative licensing
   and verify the public/restricted package split.

### Required to enter R3, without claiming the manual gates are closed

- Implement the textual and figure/table acceptance tests in Issues 1, 3, and
  4, or explicitly decline them with evidence.
- Keep the independent v3 audit's split decision visible: mechanical and
  descriptive PASS, prior-outcome-independence FAIL.
- Carry Issues 2 and 5 as named manual blockers with owner and evidence needed;
  do not replace qualified review with LLM adjudication.
- Synchronize the response-matrix status cells that still say “Planned R2” even
  where the R2 audit reports implementation complete.

### Desirable, not required for the present descriptive paper

- Add a schema-drift suite involving renamed columns, permission views,
  retired code values, null propagation, and temporal-window ambiguity.
- Report risk--coverage curves once a prospective run produces meaningful
  abstention rather than 0/180 abstentions.
- Add operator-reviewed challenge subsets for topology direction, units,
  status-code semantics, time zones, ties, and empty results.

### Unjustified reruns

- Another run of the same 180 GridDB items cannot restore prior-outcome
  independence and must not be described as prospective or confirmatory.
- More LLM-generated “expert” labels cannot close qualified-human review.
- More machine-silver RTS/SimBench questions do not improve semantic validity
  until review and licensing gates are resolved.
- Repeating the same v3 selectors with more random seeds is not meaningful for
  a deterministic release; the retained byte-identical reproductions suffice.

## Figure and table audit

- The R2 architecture figure is strong: it visibly shows external candidates,
  five typed roles, the SQLite validator, complete state coverage, append-only
  blackboard, deterministic adjudicator, and post-seal gold boundary. The note
  that user authorization is outside the software boundary must remain.
- The architecture figure should avoid implying that “authorized schema view”
  was a utility-user entitlement in v3; caption it as the registered full-schema
  research allowlist unless a real user policy is supplied.
- The Q039 result needs a compact case table or inset because the aggregate
  101/180 versus 100/180 presentation hides that the entire difference is one
  designed wildcard-projection event.
- Resource and chronology tables correctly separate BIRD, GridDB, and silver
  power-grid assets. Keep “0 human-reviewed; 0 sealed” and license status visible
  rather than moving them only to supplementary material.
- The current PDF compiles without unresolved references or clipping according
  to `ROUND_AUDIT.json`. The template footer still displays “Version August 5,
  2026” while the round audit is dated August 8; synchronize this metadata in R3.

## Reproducibility audit

R2 passes the reproducibility gate for the claims it now makes. The source,
PDF, bibliography, code, figure, freeze, and audit hashes are recorded; 30 tests
pass; both v3 reproductions are byte-identical; all 5760 attempts and 332
failures per run are retained. The independent audit's evidence-class failure
is correctly incorporated into the current abstract, results, discussion, and
round audit. The main remaining reproducibility defect is release governance:
the GitHub repository is not yet asserted to match the manuscript-bound archive
and no immutable public tag/DOI is recorded. That is a repository-owner action,
not a reviewer-agent action.

## Ethics, governance, and engineering-safety audit

No human-subject or animal study is reported, so the stated IRB non-applicability
is consistent with the current machine-only experiments. The paper correctly
states that generated SQL and returned rows require authorized human inspection
before consequential use and that LLM assistance is not expert ground truth.
No reviewer agent may fabricate expert forms, qualifications, funder identity,
author consent, repository release, or third-party permission. If qualified
experts later review data and their judgments become scientific evidence, the
authors must prospectively define reviewer qualifications, rubric, independence,
adjudication, agreement reporting, exclusions, access handling, and retention.

## Manual blockers that an AI agent cannot close

1. Yang Yong's actual corresponding-author email and all-author verification of
   spelling, order, affiliations, and final manuscript.
2. Qualified power-grid/database expert review and genuine human adjudication;
   an LLM API cannot substitute for this status.
3. Exact funding-agency name and funder-role confirmation for grant
   `521300250006`.
4. Repository-owner synchronization, clean-clone verification, immutable tag or
   release, and public archive/DOI decision.
5. File-level third-party license and redistribution decisions for RTS-GMLC,
   SimBench, and any restricted source-dependent derivative; provision to an
   editor/reviewer is still subject to permission.
6. Author approval of the AI-assistance disclosure, data-availability wording,
   and final risk statements.
7. Authorization and genuinely untouched data for any new confirmatory
   end-to-end run. Reusing the same 180 items cannot satisfy this gate.

## R3 acceptance conditions

The manuscript may advance to R3 with the original title when: (a) “robust” and
“multi-agent” are operationally bounded everywhere; (b) Q039 is presented as an
ambiguous, descriptive projection trace rather than a semantic rescue; (c) the
executor terminology and result-size tests distinguish non-mutation,
allowlisting, bounding, and user authorization; (d) figure/table captions expose
the 1/180 and outcome-exposure boundaries; (e) the response matrix and PDF date
are synchronized; and (f) every unresolved human/license/release action remains
visibly open. R3 cannot become a submission candidate until the qualified-human,
author, repository, funding, correspondence, and licensing blockers above are
closed with real records.
