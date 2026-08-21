# MA-SQLGrid Offline Study v2: Independent Method Audit

## Material Passport

- Audit mode: ARS experiment-agent `validate` (independent, read-only examination of frozen inputs, code, ledgers, and two completed runs)
- Audit date: 2026-08-08 (Asia/Shanghai)
- Audited study: `prospective-from-freeze offline coordination selection study v2`
- Freeze content SHA-256: `31eea8af71ad24be31df91091724d58a160eb230636a093c78e8eabf53b732cb`
- Freeze-manifest file SHA-256: `60479af3f8313046f54e12e1f53b87121da14d86ea727801af9e109197e82425`
- Study-code SHA-256: `31d1ebda004890dd22935a83da168a106bdfe50d2cfe423862a80ae73894f8cd` (matches the freeze manifest)
- Witness-builder SHA-256 observed on disk: `86ecae91365973e350904a7d09ad66b814c2129e87d778c99cf4baec014f8b8d` (not bound by either manifest)
- Verification status: **ANALYZED; deterministic canonical outputs reproduced twice, but the release-level provenance gate fails**
- Overall decision: **FAIL (two blocking provenance/test-freeze defects); numerical and method-behavior checks otherwise PASS**

## Scope and independence

The audit did not modify the study code, input files, witness databases, freeze, or run directories. It did not communicate with the implementation agent. Existing `INDEPENDENT_AUDIT_v2.json` and `INDEPENDENT_REPRODUCTION_CHECK_v2.json` were treated as claims to be checked, not as evidence sufficient by themselves. Counts, hashes, blackboard digests, attempt topology, method differences, and summary values were independently recomputed.

## Verdict by requested issue

| Requested check | Verdict | Independent finding |
|---|---:|---|
| Three unique witness SHAs and declared invariants | PASS | T0 and M1/M2/M3 have four distinct SHA-256 values. All three witnesses pass `PRAGMA integrity_check`. M1 adds only the probe relation and preserves every original table/row; M2 adds three indexes plus `VACUUM` and preserves original logical contents; M3 adds one nullable probe column to each of `assets`, `work_orders`, and `sensor_readings`, and every projection over the original named columns remains identical to T0. |
| Query-blind witness definition | PASS for the inspected source; provenance FAIL | The builder accepts only `--base` and `--out` and contains no question, prompt, prediction, score, or gold-file read. However, its code hash is not recorded in the witness manifest or main freeze, so the executed builder cannot be cryptographically tied to the inspected source. |
| Goldless selection view | PASS | `selection_inputs.jsonl` has exactly 180 rows and exactly two fields per row: `question_id` and `question`. No forbidden gold-derived field is present. The two prediction ledgers contain generation metadata and predicted SQL but no gold SQL or correctness fields. |
| Gold opened only after sealing | PASS at code/output level | The first gold-bearing-file read in `run()` occurs after all 180 blackboards, selections, sensitivities, and `pre_gold_seal_manifest.json` are written. The post-seal gold file hash equals `a08f302afb47bc2e7c352d20ca69efa0068b74d9ad296c988bc7b27160593a82`. All 540 evaluation rows declare the post-seal phase. |
| Same 8-candidate x 4-state evidence budget | PASS with a wording limit | For each run, 1,440 candidate slots each have one T0 and three metamorphic executions: 5,760 physical attempts total, 1,440 per state. The fixed-order, validation-only, and full decisions are all made only after this shared evidence collection. This is a **shared precomputed evidence budget**, not 5,760 separately executed attempts for each method and not an estimate of each method's natural runtime cost. |
| Fixed-order really waits for equal evidence | PASS | Source order and the sealed blackboards show that all 32 candidate-state attempts per question are completed before the fixed-order decision is posted. It always selects frozen slot C000 and explicitly ignores the collected ranking evidence. |
| Validation has no counterfactual input | PASS | The validation selector is called with an empty counterfactual mapping. Across 180 sealed decisions in each run, all eight candidates have `counterfactual_total=0`, `counterfactual_passes=0`, and incomplete counterfactual coverage in the validation-only score record. |
| Full-versus-validation difference and one-question source | PASS | The selected candidate differs on exactly one of 180 questions, Q039. Validation selects C000 from `qwen:F00_Full_NoShape` (`SELECT * ...`); full coordination rejects it only on M3 and selects C001 from `qwen:F01_Full_WithShape` (explicit `work_order_id, scheduled_date`). The former is incorrect and the latter correct under the post-seal evaluator. Thus the observed increment is exactly 1/180, not a broad multi-agent gain. |
| Five roles and grounding boundary | PASS with a strong limitation | The offline path records Query Analyst, Schema Cartographer, Execution/Safety Validator, Counterfactual Critic, and Adjudicator; the frozen candidate provider is an external non-agent source. Schema grounding is written to the trace but is not consumed by validation or adjudication. The study therefore does not estimate a five-role end-to-end benefit, a schema-grounding benefit, autonomous deliberation, or new SQL-generation quality. |
| Every attempt, failure, and blackboard retained | PASS, trace-ID improvement advised | Each run contains 5,760 candidate attempts, including all 332 failures (83 per database state), 180 gold-evaluation attempts, and 180 sealed blackboards. Every blackboard digest independently verifies. Attempt order closes exactly against question -> candidate -> T0/M1/M2/M3, using SQL and database hashes. Individual attempt rows do not carry explicit question/candidate/state IDs; their provenance currently depends on order plus hashes. |
| Two independent deterministic repetitions | PASS | Blackboards, pre-gold seal manifests, selections, evaluations, sensitivity selections/evaluations, reproduction manifests, and summaries are byte-identical between run_v2a and run_v2b. Attempt logs differ only in runtime-dependent trace values and have identical counts/outcome topology. |
| Summary recomputation | PASS | Recomputed values exactly match both summaries; see the next section. |
| M3 definition predeclared and reasonable | PASS as a narrow projection-stability witness | The M3 operator and wildcard exception are declared in both the witness manifest and frozen config before the two runs. It is logically valid for explicit-column projections. It must be described as a nullable-schema-extension/projection-stability test, not as general counterfactual robustness. |
| Freeze time and code hashes | **FAIL -- BLOCKING** | The study code, agents, executor, config, inputs, witness states, and witness manifest are content-hashed. But neither manifest contains a signed/content-bound `created_at_utc` (or equivalent freeze time), and the witness-builder code is absent from both hash inventories. Filesystem times show builder 15:48:51, witness manifest 15:49:02, final study-code modification 15:53:00, freeze 15:53:10, run_v2a summary 15:53:19, and run_v2b summary 15:53:36 (Asia/Shanghai), but filesystem metadata is mutable and is not part of the freeze commitment. |
| Added regression tests | **FAIL -- BLOCKING** | The existing 21 tests pass, including the new validation-empty-CF tie-break test and lower-level executor/blackboard tests. There is no v2 orchestration regression test for the gold boundary, 8x4 attempt topology, fixed-order-after-collection behavior, M3 `SELECT *` exception, witness uniqueness/invariants, summary recomputation, or freeze completeness; test files are also not bound in the freeze. |

## Independent result recomputation

| Method | Covered | Abstained | Correct | Accuracy (all 180) | Robust-invariant selections | Rescues vs fixed order | Harms vs fixed order |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fixed order, equal shared evidence | 180 | 0 | 80 | 44.44% | 177 | 0 | 0 |
| Validation rank, no CF | 180 | 0 | 100 | 55.56% | 179 | 22 | 2 |
| Full coordination, complete metamorphic | 180 | 0 | 101 | 56.11% | 180 | 23 | 2 |

Full minus validation is `+1/180 = +0.56` percentage points. Because the methods make different selections on only Q039, this descriptive difference supplies no credible basis for claiming a general accuracy improvement, statistical superiority, or a five-role-system effect.

The sensitivity table also recomputes exactly. Its large dependence on tie direction (101/180 under original order versus 117--118/180 under reverse order) shows that candidate ordering is a material design factor. All 18 prespecified sensitivity cells are reported, so this is not hidden selective reporting; it remains a limitation of the selector.

## M3 and Q039 interpretation

M3 is predeclared and internally coherent: adding nullable columns preserves the denotation of queries that explicitly project only original columns, while `SELECT *` changes output arity and is intentionally non-invariant. Twenty-six frozen candidate slots use wildcard projection, although only wildcards touching the three extended tables are affected.

The sole full-versus-validation difference is therefore a highly specific projection case. On Q039, both candidates have identical validation points. C000 passes M1/M2 but fails M3 because `SELECT *` exposes the new nullable column; C001 explicitly projects the two requested fields and passes all three witnesses. This supports a narrow statement about projection-stability filtering. It does not demonstrate resistance to arbitrary database shifts or counterfactual semantic reasoning.

## Blocking defects and required correction

1. **Bind construction provenance.** Create a new release/freeze (do not edit or overwrite v2) in which the witness manifest records the exact builder path, bytes, SHA-256, schema version, and content-bound `created_at_utc`. The main freeze must include the builder itself and the complete witness manifest.
2. **Bind freeze chronology.** Add a content-bound `created_at_utc` with timezone to the new freeze and each run manifest. A timestamp added retroactively to the existing v2 is not acceptable; make a new freeze first and then execute two fresh no-overwrite offline repetitions.
3. **Add and freeze central regression tests before the new freeze.** At minimum test: unique/distinct witness hashes; logical M1/M2/M3 invariants; M3 explicit projection passes and `SELECT *` on an extended table fails; selection rows contain only question fields; gold loader cannot be reached before 180 seals; each question produces eight candidates x four states before any decision; validation receives no CF evidence; Q039 selection change is derived from M3; independent summary recomputation. Include the test-code hashes and test command/result in the release manifest.

Recommended but non-blocking: add explicit `question_id`, `candidate_id`, and `state_id` to every attempt row so audit closure does not rely on append order. Also rename v2 artifacts whose `schema_version` still ends in `v1` to avoid release-version ambiguity.

## Statistical/methodological fallacy scan

Coverage: **11/11 checked**.

| Fallacy | Finding |
|---|---|
| Simpson's paradox | Not assessable from the aggregate summary; no subgroup-effect claim should be made. |
| Ecological fallacy | Not applicable to the question-level accuracy claim. |
| Berkson's paradox | No detected within the fixed 180-question ledger; external generalization beyond this frozen subset remains unsupported. |
| Collider bias | No covariate-adjusted causal model is used. |
| Base-rate neglect | Not a diagnostic-classification analysis. |
| Regression to the mean | No pre/post extreme-group design. |
| Survivorship bias | All frozen 180 questions and all eight slots are retained; no failed candidate or question is dropped. |
| Look-elsewhere effect | All 18 prespecified sensitivity cells are retained. Do not select the reverse-order 65.0--65.6% cells as the primary result post hoc. |
| Garden of forking paths | Reduced by the pre-run config, but the lack of a content-bound freeze timestamp and frozen central tests weakens the confirmatory claim. |
| Correlation implies causation | The offline paired selector comparison cannot establish a general causal benefit of a multi-agent framework. |
| Reverse causality | Not applicable; there is no observational directional model. |

## Wording that may enter the manuscript after the blocking freeze defects are corrected

> We conducted a deterministic prospective-from-freeze offline selection study over a historical pool of eight SQL candidates per question. All selectors shared the same precomputed evidence collection of eight candidates across one reference and three query-blind metamorphic SQLite states; no new model calls were made.

> The validation-only selector did not receive counterfactual evidence. The complete-metamorphic selector differed from validation-only on one of 180 questions, increasing exact execution correctness from 100/180 (55.56%) to 101/180 (56.11%). This one-question descriptive increment arose from a predeclared nullable-schema-extension test that rejected a wildcard projection and retained an explicit-column projection; it should not be interpreted as statistical superiority or a general five-role gain.

> The five recorded deterministic roles provide an auditable coordination trace, but schema grounding was trace-only and candidate SQL was imported from frozen historical generation runs. Accordingly, this experiment does not estimate end-to-end autonomous-agent performance, schema-grounding benefit, or new-generation quality.

> M1--M3 test invariance under an irrelevant relation, physical index/rebuild changes, and nullable-column extension, respectively. These operators provide bounded metamorphic evidence and do not represent arbitrary deployment shifts.

## Final decision

**FAIL for release/freeze acceptance; PASS for the recomputed numerical ledger and the six repaired method behaviors.** The manuscript may use the limited numerical statements only after a fresh non-overwriting freeze binds the builder, timestamps, and central tests, followed by two fresh matching offline repetitions. Until then, the existing v2 should remain an audit-preserved diagnostic artifact rather than the final frozen experiment release.
