# Round 2 Independent Review — Methods and Statistics

## Reviewer scope and independence

Role: independent methods and statistics reviewer for the frozen MA-SQLGrid R2
package. I reviewed `paper_applsci.tex`, `build/paper_applsci.pdf`,
`R2_ASSEMBLY_AUDIT.md`, `ROUND_AUDIT.json`, all three R1 reviews, the R1-to-R2
`REVISION_RESPONSE_MATRIX.md`, the release-v3 configuration and retained
summaries, and `INDEPENDENT_RELEASE_AUDIT_V3.md`. I also inspected the released
executor, counterfactual-coverage code, central tests, and item-level sealed-board
records. I did not edit the manuscript or experimental assets and did not
communicate with the other reviewers.

## Recommendation

**Major revision; not a submission candidate.** R2 materially improves the
engineering evidence and is much more candid than R1. The database-level safety
boundary and fail-closed counterfactual coverage defect are genuinely repaired
in code and tests. The manuscript also correctly downgrades release v3 to a
deterministic no-generation descriptive re-execution after the independent audit
found same-item outcome access in the pre-run test suite. The 80/180, 100/180,
101/180, Q039, 5,760-attempt, 332-failure, and 117--118/180 sensitivity values
are consistent with the retained release summaries.

The central R1 scientific blocking item is nevertheless not closed. No experiment
evaluates contemporaneous five-role generation or estimates a multi-agent
benefit, and the only new selector analysis uses previously evaluated items and
an arbitrary candidate-order tie breaker. An independent recomputation of the
sealed-board scores shows that the highest validation score is tied for 130/180
questions in both validation-only and complete-metamorphic selection; the mean
number of top-scoring candidates is approximately 5.4, and all eight candidates
tie on 79 validation-only questions and 78 full-condition questions. This explains
why reversing candidate order changes 101/180 to 117--118/180. Honest wording
contains this defect but cannot turn the result into evidence for the title-level
multi-agent or robust-performance proposition.

**Confidence: 5/5.** The principal findings are based on source code, frozen
item-level ledgers, exact manuscript locations, and the independent release audit.

## Status of the R1 blocking items

| R1 item | R2 verdict | Basis |
|---|---|---|
| Database-level safety (C03) | **Closed as an engineering implementation claim** | `paper_applsci.tex`, lines 151--153; `sqlite_readonly_executor.py`, lines 126--176; adversarial tests. URI read-only/immutable mode, `query_only`, authorizer denial, extension denial, progress limits, row cap, and retained failures are implemented. This does not establish user authorization or process isolation, which the manuscript correctly disclaims. |
| Incomplete counterfactual coverage (part of C02) | **Closed as a fail-closed software rule** | Manuscript lines 153 and 157; `ma_sqlgrid_agents.py`, lines 382--425; tests at `test_ma_sqlgrid_agents.py`, lines 108--126. Required counterfactual evidence needs complete named-state coverage and the threshold; validation-only receives an empty map. |
| Operational definition of robustness (remainder of C02) | **Partly closed, scientifically still open** | Table 3, manuscript lines 159--177, separates mutation safety, resource boundedness, coverage, metamorphic invariance, and semantic validity. Only three constructed witnesses and historical-pool selection are evaluated; this is not general semantic, model, distributional, or operational robustness. |
| Integrated title-method outcome (C01) | **Not closed** | Manuscript lines 228--234 and 409 explicitly state no new LLM calls, external historical candidates, and no five-role end-to-end estimate. Reclassification is correct, but it is not the required integrated-system experiment. |
| Domain validation (C04/C06) | **Not closed; honestly retained** | Resource Table 1, lines 94--113, records zero qualified reviews for the external power-grid candidates; lines 405--415 restrict external validity. |
| Repository synchronization (C10) | **Not closed; manual release blocker** | Data Availability, line 430, says synchronization/tagging is still required. |

## Five most serious issues

### 1. The experiment still does not evaluate the five-role method named in the title — **blocking**

The full R2 execution is deterministic selection over eight candidates generated
earlier by two backbones and four prompting packages. The Synthesizer only
packages those candidates; no experiment estimates Analyst, Cartographer,
Synthesizer, Validator, and Critic interaction under contemporaneous generation.
The manuscript states this correctly in the abstract, lines 36--42, lines
228--234, and lines 409--423. Therefore, 100/180 and 101/180 are selector outcomes,
not MA-SQLGrid end-to-end outcomes, and the comparison cannot isolate an agent,
role, communication, or generation effect.

This cannot be closed by further caveats while retaining the title as an
empirically validated proposition. It requires an untouched evaluation resource
and a frozen, budget-matched new-generation comparison: direct generation,
staged single-candidate handoffs, equal-pool validation/adjudication without
counterfactual evidence, and the same pool with the registered reference-free
state suite. Model snapshot, prompt, decoding, question order, candidate count,
physical calls, evaluator, failure policy, and abstention rule must be held fixed.

**Acceptance test:** the untouched-set protocol and development-only tests are
frozen before any evaluation outcome is accessed; every generated attempt and
failure is retained; each board is sealed before gold; the integrated condition
is actually executed; independent recomputation reproduces all reported counts,
resource use, and effects.

### 2. Tie order dominates the descriptive selector result — **blocking for selector efficacy; major for descriptive reporting**

The manuscript reports that reversing candidate order changes 101/180 to
117--118/180 (abstract; lines 373 and 395), but it does not quantify why. Direct
recomputation from `run_v3a/blackboards_sealed_before_gold.jsonl` finds top-score
ties on 130/180 questions for both adjudicating selectors. For validation-only,
top-tie multiplicities are 1:50, 2:5, 3:3, 4:4, 5:5, 6:8, 7:26, and 8:79;
for complete metamorphic selection they are 1:50, 2:5, 3:3, 4:4, 5:5, 6:9,
7:26, and 8:78. Thus the mean top-tie set is about 5.4 candidates. Original order
systematically favors the frozen Qwen-first source order; reverse order favors
the opposite end. Neither is a semantic adjudication rule.

The current text appropriately calls this a design risk, but `improved` or
`coordination` can still be misread as selector value. R3 can add the exact tie
multiplicity and selected-origin tables, plus an outcome-descriptive permutation
or random-tie analysis. It may not choose a favorable order after seeing these
outcomes. Establishing selector efficacy requires development-only rule selection
and one untouched evaluation; wording alone cannot do so.

**Acceptance test:** every selector result is accompanied by top-tie multiplicity,
selected source-slot distribution, and order-sensitivity accounting. The default
rule is described as arbitrary on this release. Any future primary rule is chosen
only from development evidence and evaluated once on untouched items.

### 3. Release v3 is downgraded correctly in the paper but not consistently across the release package — **major integrity/reproducibility issue**

The abstract, chronology table, Methods lines 232--234, Discussion lines 391--395,
and `INDEPENDENT_RELEASE_AUDIT_V3.md` correctly classify v3 as descriptive because
the bound pre-run test accessed v2 gold-derived outcomes from the same items.
The dependency is direct: `tests/test_offline_coordination_release_v3.py`, lines
15--17 and 109--127, reads the prior evaluation ledger and checks the observed
full-versus-validation effect.

However, both retained `run_v3a/summary.json` and `run_v3b/summary.json` still
describe the study as “offline prospective selection”; `study_config_v3.json`
still uses `study_label: release-v3 prospective-from-freeze...`,
`selection_or_rule_tuning_from_gold: false`, and a prospective interpretation.
Those historical bytes should remain immutable, but a reader receiving the
archive encounters conflicting evidence-class labels. The 29/29 internal audit
also remains `PASS` and must never be presented without the superseding split
decision.

R3 should add a machine-readable superseding classification record that binds
the hashes of the frozen config, both summaries, internal audit, and independent
release audit; identifies every deprecated prospective field; and declares the
sole permitted descriptive interpretation. The archive README and evidence
ledger must point to this record first. Do not overwrite the frozen v3 files.

**Acceptance test:** a clean-package search for `prospective`, `blinded`,
`prespecified`, or `PASS 29/29` either lands in a historical frozen object listed
by the supersession record or in text explicitly rejecting that evidence class.

### 4. Full numeric reporting remains incomplete and the response matrix is internally stale — **major**

R2 adds useful resource, chronology, robustness, BIRD, replay, and offline tables.
The BIRD budget is now clear: B0--B2 use one call/item, B3 uses two, each backbone
uses 2,500 calls, total formal calls are 5,000, and 2,476 incident calls remain
excluded. This closes the principal BIRD accounting criticism, with latency and
token totals honestly marked unavailable.

Nevertheless, R1-C08 asked for complete count/denominator/status tables. GridDB
Table 4 gives proportions only (lines 242--256); the component result remains a
figure and selected prose estimates (lines 275--283); and the eight multi-state
cells remain summarized only by a range (lines 288--293). The release sensitivity
grid has 18 cells but only three distinct outcome values are summarized in prose.
These omissions make negative and null evidence harder to audit than the BIRD
and offline tables.

The R2 `REVISION_RESPONSE_MATRIX.md` also retains “Planned R2” for completed
C02, C03, C05, C08, C11, C12, C16, and C17 rows, while its introductory table
says some of those changes were implemented; it says 21 tests pass whereas the
assembly audit and manuscript say 30. This is not an experiment error, but it
prevents a reliable closure decision.

**Acceptance test:** add complete machine-generated numeric tables for all eight
GridDB cells with counts/180, the component endpoints, all eight 15-state cells,
and all 18 selector sensitivity cells (main text or clearly bound supplement).
Reissue the R2-to-R3 response matrix with one authoritative status and exact
artifact/line verification for every R1 item.

### 5. Power-grid semantic validity and broader robustness remain untested — **blocking for application/robustness claims**

The sole scored domain corpus is a synthetic eight-table, 98-row database whose
180-item evaluation partition was development-visible (lines 86 and 405). The
RTS-GMLC and SimBench question--SQL resources have zero completed qualified-human
reviews and remain machine silver (Table 1; lines 411--415). BIRD is non-grid.
Three metamorphic operators expose useful projection and execution behavior, but
they are constructed operator families, not samples from grid deployment states.

The manuscript now states these limits accurately. That wording closes the risk
of false generalization but not the missing validation. No additional rewriting
can establish intended units, tie handling, projections, code semantics, or
operational relevance. A qualified independent semantic review and an untouched,
structurally distinct power-grid evaluation are required before claiming domain
validity or general robustness.

**Acceptance test:** a frozen rubric and stratified sample are independently
reviewed by qualified power-grid/database experts; qualifications, independent
labels, disagreements, adjudication, exclusions, and agreement are retained.
Separately, a held-out domain database is evaluated under the matched protocol.
Machine or LLM adjudication must remain silver and cannot substitute for this
gate.

## Claim–evidence audit

| Claim/location | Evidence checked | Verdict | R3 action |
|---|---|---|---|
| Database-enforced executor, abstract and lines 151--153 | Executor source and adversarial tests | **Supported as a SQLite engineering boundary.** Not support for user authorization, process isolation, or semantic safety. | Retain current caveats; record exact runtime for this v3 study separately from the BIRD 3.10.11/SQLite 3.40.1 runtime. |
| Complete counterfactual coverage fails closed, lines 153, 157, 191--197 | Agent code lines 382--425 and tests | **Supported.** Validation-only has no counterfactual score; required mode makes incomplete evidence ineligible. | Mark R1-C02 software defect closed, while leaving performance/general robustness open. |
| 5,760 attempts and 332 retained failures, abstract and lines 228--234, 352 | v3 summaries and independent release audit | **Supported.** It is one shared `180 x 8 x 4` evidence collection, not 5,760 attempts per selector. | Retain exact wording. |
| 80/180, 100/180, 101/180, Table 7 | Both v3 summaries and evaluation ledgers | **Numerically supported, descriptive only.** | Add paired transition and tie-multiplicity provenance to the table/supplement. |
| Q039 is the only full-vs-validation difference, line 371 | Independent audit and item-level selection/evaluation ledgers | **Supported as a narrow wildcard-projection trace.** | Keep the “not general gain” language. |
| Reverse order gives 117--118/180, lines 373 and 395 | All 18 retained sensitivity cells in both summaries | **Supported, and materially undermines rule-independent efficacy.** | Report all 18 cells and top-tie distribution; do not select the higher rule post hoc. |
| V3 is descriptive rather than prospective, abstract and lines 118, 232--234, 391 | Independent release audit; pre-run test lines 15--17, 109--127 | **Correct in manuscript, inconsistent in frozen release metadata.** | Add hash-bound supersession record and archive-first warning. |
| BIRD uses 5,000 formal calls with unequal calls/method, lines 88, 133, 299--323 | Eight-cell table and frozen protocol lineage | **Supported and adequately bounded as non-grid workflow evidence.** | Preserve 2,476 incidents and do not imply call-matched repair or MA-SQLGrid evaluation. |
| “five-role framework” and “robust” title | Implementation plus all experiments | **Implementation supported; end-to-end benefit and broad robustness not supported.** | Requires new untouched matched experiment and domain review; cannot be closed by prose. |

## Experiment audit

### Required before submission under the retained title

1. **Untouched, budget-matched integrated-system evaluation.** It must compare
   contemporaneous generation conditions and actually execute the submitted
   roles/controller. A rerun of the same 180 items cannot repair prior outcome
   exposure.
2. **Development-only tie-rule selection plus untouched evaluation.** Freeze the
   semantic or calibrated tie rule without evaluation outcomes; report coverage,
   abstention, failures, and selected-source distributions.
3. **Independent power-grid semantic review and a held-out domain resource.**
   LLM/author review may assist triage but cannot be relabeled as independent
   expert evidence.
4. **Independent recomputation.** Rebuild every manuscript table and figure from
   item-level immutable ledgers, including negative and sensitivity results.

### Required for R3 using current assets (no new generation needed)

1. Add the v3 evidence-class supersession record without modifying frozen bytes.
2. Add complete GridDB/component/multi-state/sensitivity tables and a quantitative
   tie diagnostic.
3. Repair the response matrix's stale statuses and test-count conflict.
4. Synchronize version metadata: the current PDF footer still says “Version
   August 5, 2026” although the R2 package and audits are dated August 8.
5. Render and inspect the final R3 PDF anew; older 18-page visual-QA images remain
   beside the current 19-page descriptive renders and should be clearly marked
   historical or excluded from the submission archive.

### Desirable analyses

- Descriptive random-permutation or all-achievable tie analysis on the historical
  pool, with no inferential or confirmatory label.
- Selected-candidate distribution by backbone and prompt cell for every tie rule.
- Failure taxonomy by witness and candidate origin, including the 332 retained
  failures.
- Risk–coverage analysis on a future untouched set once abstention actually
  occurs; the current 0/180 abstention gives no calibration information.

### Unjustified reruns or relabeling

- Do not rerun these 180 questions and call the result prospective, blinded,
  confirmatory, preregistered, or prior-outcome-independent.
- Do not choose reverse order, a weight policy, or an invariance threshold because
  it yields 117--118/180.
- Do not treat the 1/180 Q039 increment as a counterfactual, coordination,
  robustness, or multi-agent gain.
- Do not count 5,760 shared state executions as a per-method natural runtime cost.
- Do not relabel BIRD as power-grid evidence, the inherited prompting workflows
  as MA-SQLGrid, or machine-silver labels as qualified expert gold.

## Statistical reporting assessment

**Rating: Needs Improvement.** Multiplicity handling for the inherited factorial,
component, multi-state, and BIRD families is explicit and appropriately separated.
The v3 analysis is correctly not given confirmatory p-values or population
confidence intervals after its evidence-class failure. Rescue/harm counts expose
paired direction. The remaining problem is completeness: full cell tables and the
tie distribution are absent, and the word “accuracy” should always remain paired
with “finite-corpus descriptive” for v3.

No reported statistic supports a bounded recomputation using
`p_from_test_statistic`, GRIM, GRIMMER, or `n_from_df`: the manuscript reports
adjusted p-values and intervals without their underlying test statistic/df form,
while the principal v3 outcomes are finite counts. I therefore found no applicable
bounded arithmetic receipt. Direct count/rate checks of 80/180, 100/180, 101/180,
117/180, and 118/180 are consistent to the displayed precision.

## Figure and table audit

- **Figure 1:** pass. The code-native architecture is legible and correctly exposes
  external candidates, the database executor, complete-state eligibility, the
  deterministic adjudicator, the gold boundary, and external human authorization.
- **Figures 2--4:** acceptable visually, but the numeric evidence should not remain
  plot-only. Bind each to a complete numeric table and evidence-class/run label.
- **Tables 1--3:** scientifically useful. They make development visibility,
  chronology, and robustness scope explicit. Table 2 is dense but legible in the
  inspected PDF.
- **GridDB Table 4:** major reporting omission. Replace proportions with
  `correct/180 (rate)` and bind composition-sensitivity/contrast tables.
- **BIRD table:** pass for core accounting. It clearly reports all eight cells,
  unequal calls/item, counts, intervals, and non-grid status. “Failures” is more
  precisely “final-ledger omissions”; no token/latency estimate should be invented.
- **Offline Table 7:** numerically correct but incomplete without top-tie
  multiplicity and all sensitivity cells. “Complete metamorphic coordination” is
  a rule label, not proof of complete semantic or multi-agent coordination.
- **PDF:** no clipping or overfull box was found in the frozen build; hashes agree
  with `ROUND_AUDIT.json`. Page 19 is almost entirely blank after the publisher
  disclaimer, a minor typesetting inefficiency rather than an integrity defect.

## Reproducibility and ethics findings

### Strengths

- The independent release audit correctly overrides the inadequate 29/29 internal
  audit and preserves the failed evidence-class decision.
- Both v3 runs are byte-identical for canonical selection, evaluation, sensitivity,
  and summary outputs.
- All failures and earlier v1/v2 incidents are retained rather than repaired or
  deleted.
- The manuscript separates BIRD's authorized Python 3.10.11/SQLite 3.40.1 runtime
  from the no-generation offline study conceptually, although v3's recorded Python
  3.12.10/SQLite 3.49.1 runtime should be made explicit in the resource ledger.
- Human review is not fabricated; machine-silver resources remain visibly silver.

### Blocking/manual items

1. The public repository is not yet synchronized and immutably tagged.
2. Yang Yong's correspondence email remains a manual placeholder.
3. Funding-agency identity and funder-role wording remain unconfirmed.
4. Qualified power-grid semantic review has not occurred.
5. Third-party license review and the editor/reviewer restricted bundle require
   author/release-owner confirmation.

## What can and cannot advance to R3

### May advance to R3 as bounded work on existing assets

- database-level safety and fail-closed coverage implementation;
- descriptive v3 counts, Q039 trace, and tie-order warning;
- BIRD budget/resource table and chronology;
- complete-table generation, tie diagnostics, release supersession record,
  response-matrix repair, version-date repair, and fresh PDF/package audit.

### Cannot be closed by another wording pass

- a five-role or autonomous multi-agent performance benefit;
- a general counterfactual or robust-selector gain;
- prior-outcome-independent validation on these same 180 items;
- validity of the current tie rule;
- qualified power-grid semantic correctness, production safety, or external
  generalizability.

Those items require new evidence, not stronger prose. R2 can therefore enter R3
as a review draft whose engineering implementation and descriptive evidence are
auditable. It cannot become a submission candidate under the retained title until
the untouched integrated experiment and qualified domain-validation gates are
satisfied, or until the editor/author formally accepts a manuscript positioned
only as a framework/design-and-diagnostic paper with no performance-validation
claim.
