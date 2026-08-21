# MA-SQLGrid Round-1 Revision Response Matrix

Status date: 2026-08-08 (Asia/Shanghai)  
Scope: consolidated response plan for the three independent R1 reviews. This
record is added to the frozen R1 package as the required review-to-revision
handoff; the R1 manuscript, PDF, evidence, code, and reviews remain unchanged.

## Decision key

- **Blocking / major / minor** records reviewer severity after consolidation.
- **Feasible** means the R2 work can be completed from frozen local assets
  without model generation or external authorization.
- **Manual** requires an author, qualified human reviewer, funder, repository
  owner, or corresponding author.
- **New authorization** would require new LLM calls, new private-data access, or
  another action outside the present offline-study authorization. No such
  action is planned for R2.

| ID | Consolidated reviewer comment | Severity | Route | R2 decision and change | Verification / acceptance test | R2 status |
|---|---|---:|---|---|---|---|
| R1-C01 | The title method has no frozen system-level outcome; inherited GridDB/BIRD runs and the diagnostic replay are not five-role generation experiments. | Blocking | Feasible, bounded | Run a prospective-from-freeze **offline coordination-selection study** over the pre-existing eight candidates per question. Compare first candidate, validation-only/no-CF, and complete-invariance coordination under an equal frozen candidate budget. Describe it as historical-candidate offline selection, never new multi-agent generation. | Configuration and input manifest hashed before outcome access; 180 sealed blackboards; gold loaded only after sealing; two independent recomputations; all rows/failures retained. | Planned R2 |
| R1-C02 | Robustness is not operationalized; the Critic has no reference-free evidence and incomplete evidence can outrank complete evidence. | Blocking | Feasible | Define measured robustness as database-enforced read-only execution plus invariance under three logically equivalent insertion permutations. Make CF-required adjudication fail closed on incomplete coverage and jointly report accuracy, coverage/abstention, and robust-invariance. | Regression test proves 1/1 incomplete evidence cannot beat 10/11 complete evidence; every full-condition candidate has all required states or is ineligible; denominators include failures. | Planned R2 |
| R1-C03 | The lexical Validator is not an executor-level safety boundary. | Blocking | Feasible | Add a database-level SQLite executor using URI `mode=ro`, `PRAGMA query_only`, disabled extensions, an authorizer, time/opcode and row limits, optional table/column authorization, and append-only failure traces. | Adversarial tests cover writes, DDL, ATTACH, PRAGMA, multi-statements, dangerous functions, recursive resource exhaustion, row overflow, unauthorized tables/columns, and executor exceptions; source database hash remains unchanged. | Planned R2 |
| R1-C04 | GridDB is synthetic, development-visible, small, and lacks qualified dual-expert semantic adjudication; this prevents confirmatory/domain-general claims. | Blocking | Manual | Do not fabricate expert review or promote machine/LLM review. Keep GridDB as development-visible synthetic case-study evidence and the new offline study as a finite historical-pool analysis. Retain prepared review packet as incomplete. | Resource/timeline table says `0` completed qualified reviews unless human forms are supplied; abstract/conclusion make no confirmatory, production, or domain-general claim. | Manual blocker retained |
| R1-C05 | BIRD is non-grid, uses unequal calls across inherited workflows, and does not evaluate MA-SQLGrid. | Major | Feasible | Add a complete BIRD resource/results table with calls, counts, denominators, failures, and evidence status. Label BIRD a public **non-grid** portability benchmark and the old comparison workflow efficacy with unequal physical calls. | All eight model-method cells reconcile with retained ledgers; captions and conclusions never use BIRD as power-grid validity evidence. | Planned R2 |
| R1-C06 | A held-out or second reviewed power-grid resource is needed for broad power-grid validity. | Major | Manual | Inventory GridDB, RTS-GMLC, and SimBench separately. Keep RTS-GMLC/SimBench as machine-generated silver and do not claim reviewed external validation. A future qualified-review study remains required for broader validity. | Resource table includes schema/row/question counts, evidence class, license/status, visibility, and review status; no silver-to-gold relabeling. | Manual/future blocker |
| R1-C07 | Role value, fixed weights, tie rules, and coverage thresholds are untested. | Major | Feasible | Pre-freeze first-candidate, validation-only, and full complete-invariance selectors; add prespecified role/rule, weight, and invariant-pass-threshold sensitivity without choosing a rule from final outcomes. Report rescue/harm and abstention. | Sensitivity grid is present in the freeze configuration; default rule precedes evaluation; every result is retained including null/adverse results. | Planned R2 |
| R1-C08 | Statistical reporting omits counts, intervals/status, resource accounting, and full cell tables. | Major | Feasible | Add complete GridDB/BIRD/state/offline-selection tables with counts and denominators; use finite-corpus or descriptive labels where population inference is unsupported. | Each quantitative manuscript claim maps to a retained JSON/CSV row; automated audit recomputes tables; no post-review analysis is called preregistered. | Planned R2 |
| R1-C09 | Evidence chronology is blurred among prospective freeze, post-review reanalysis, retrospective diagnostic, and inherited evidence. | Major | Feasible | Add a study chronology and evidence-lineage table recording data visibility, intervention/rule freeze, outcome access, evidence class, and what each study can establish. | Search audit finds no unsupported `preregistered`, `confirmatory`, or `prospective generation` wording. | Planned R2 |
| R1-C10 | Public repository content is not synchronized with the manuscript package. | Blocking | Manual | Change Data Availability to: manuscript-bound archive prepared for editor/reviewer; public repository must be synchronized and tagged before submission. Retain the repository URL without claiming present synchronization. | Clean-clone/tag check and public release hash are required before portal upload; R2 remains not portal-ready until then. | Manual blocker retained |
| R1-C11 | Nearest multi-agent/agentic Text-to-SQL literature and the operational definition of “agent” are insufficient. | Major | Feasible + citation verification | Define each role as model-calling or deterministic, identify shared blackboard state and external candidate boundary, and add only locally verified primary-source comparisons. Unsupported literature cells remain `待核实` rather than invented. | Citation audit verifies every new bibliographic record and comparison-cell source. | Planned / verification gate |
| R1-C12 | Figures/tables need evidence-class labels and an explicit executor/gold boundary; generated imagery is inappropriate for the scientific architecture. | Major | Feasible | Revise the code-native vector framework diagram; add executor, authorization, fail-closed coverage, and offline-gold boundaries. Prefix quantitative captions with Inherited/Diagnostic/New-offline. Add BIRD and evidence-lineage tables. | Vector/source provenance retained; PDF visual audit checks label size, clipping, mixed percent/proportion scales, captions, and table legibility. | Planned R2 |
| R1-C13 | Corresponding-author email is missing. | Minor / submission blocking | Manual | Preserve a conspicuous email placeholder and mark the package not ready for portal upload. | Yang Yong supplies and verifies the email; no placeholder remains in the portal package. | Manual blocker retained |
| R1-C14 | Funding-agency wording and no-funder-role statement are not author-confirmed. | Minor / submission blocking | Manual | Retain grant `521300250006`; mark exact agency name and funder-role sentence for author confirmation instead of inferring them from affiliations. | Written author confirmation is recorded before submission. | Manual blocker retained |
| R1-C15 | Restricted-data governance, external-asset licenses, and editor/reviewer inventory must be explicit. | Major | Feasible + manual release check | Add file-level public/restricted/license status to the manuscript-bound archive inventory; do not upload third-party-restricted assets. State that restricted materials may be requested from the corresponding author subject to third-party permission. | Archive manifest and Data Availability agree; release owner confirms no restricted asset was pushed publicly. | Planned / manual release check |
| R1-C16 | AI assistance/provenance and exact tool uses need clearer disclosure. | Minor | Feasible + author confirmation | State that AI tools assisted drafting/code/figure preparation and that authors verified outputs; identify actual tools used in provenance records. Do not claim GPTImg2/Gemini figures if none enter the paper. | Figure/data/code provenance and disclosure agree; authors confirm final wording. | Planned / manual confirmation |
| R1-C17 | Version metadata, abstract length, captions, terminology, and backbone interpretation need cleanup. | Minor | Feasible | Synchronize R2 date; shorten abstract while retaining evidence boundaries; call two backbones sensitivity analyses rather than independent replications; replace unbounded reliability/robustness wording with measured endpoints. | Build/search/visual audit and title--abstract--results--conclusion consistency check pass. | Planned R2 |

## Explicitly declined or deferred requests

1. **No LLM-generated “expert” adjudication.** It cannot satisfy the required
   qualified-human dual review and third-person adjudication gate.
2. **No new model calls in R2.** The offline study consumes only the eight
   candidates already frozen for each of 180 questions; therefore it cannot
   estimate the effect of new candidate generation or autonomous dialogue.
3. **No post-hoc relabeling.** The retrospective replay, formal-v5 gold-relative
   labels, and machine-silver datasets remain diagnostic/silver evidence.
4. **No incident modification.** Existing BIRD incident runs remain retained,
   excluded, and unchanged.
5. **No broad power-grid generalization.** That claim remains deferred until
   qualified human review and independently held domain evidence exist.

## Round-2 gate

R2 may advance to independent review only after C01--C03 and C05--C09 have
machine-verifiable artifacts, manuscript/table/figure values reconcile with
those artifacts, and C04/C06/C10/C13--C16 remain visibly listed as unresolved
manual or release gates rather than being silently treated as completed.
