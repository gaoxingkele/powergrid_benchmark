# Independent Release Audit: MA-SQLGrid Offline Coordination Release v3

**Audit date:** 2026-08-08 (Asia/Shanghai)  
**Auditor role:** independent, read-only release auditor  
**Scope:** `metamorphic_witnesses_v3`, its builder and manifest; the release/core runners; frozen tests; `study_config_v3.json`, `selection_inputs.jsonl`, `freeze_manifest.json`; `run_v3a`, `run_v3b`, and the reproduction records.  
**Overall decision:** **FAIL for the claimed prospective-from-freeze evidence class; PASS for mechanical integrity, deterministic reproduction, and descriptive result traceability.**

## Executive finding

The v3 artifacts are internally coherent. The witness, freeze, and run content hashes recompute; all 21 frozen file records match the current bytes; four database states have distinct hashes; both runs contain the expected 5760 candidate--state attempts; all failures and sealed blackboards are retained; the registered fixed, validation-only, and complete-invariance rules reproduce; run A and run B have identical canonical outputs; and the primary and sensitivity summaries independently recompute.

The release nevertheless fails the stronger **prospectively blinded** claim. The pre-freeze test suite invoked by `offline_coordination_release_v3.py` does not test only outcome-free structure. `tests/test_offline_coordination_release_v3.py` binds `RUN` to `prospective_from_freeze_offline_study_v2/run_v2a` (lines 15--17), opens that prior run's gold-derived `evaluation_ledger.jsonl` (lines 109 and 120), and asserts that the full-versus-validation differences have a positive net effect (lines 123--127). That test file was then frozen and its passing result was incorporated into the v3 freeze. Thus the raw gold JSONL was not opened by the v3 selection runner before sealing, but information derived from the same 180 gold outcomes was deliberately read and tested before the v3 run. Re-running the same selectors on the same evaluation items cannot restore prospectivity.

## Audit matrix

| Requirement | Result | Independently checked evidence |
|---|---:|---|
| Witness builder/manifest/database hashes | PASS | Builder SHA-256 `0d9b5b694037e0483e842a1befe3e63c9b35669e6615df42f1312d77ba959654` agrees in the witness and freeze manifests. T0, M1, M2, and M3 have four distinct SHA-256 values. All recorded database hashes and `PRAGMA integrity_check` values agree. |
| Manifest `created_at_utc` included in content hash | PASS, with limitation | Removing only `manifest_content_sha256` or `freeze_content_sha256` and canonicalizing the remaining object reproduces the stored digest. The timestamps are therefore content-bound statements, not externally attested times. |
| Code and tests frozen | PASS | Release runner, core runner, agent code, executor, builder, four test files, configuration, selection input, source ledgers, schema, databases, witness manifest, and pre-freeze result are among 21 matching frozen files. |
| Pre-freeze tests precede v3 execution | PASS mechanically | Bound test record: `2026-08-08T08:16:00+00:00`, return code 0. Run manifests start at `08:16:09` and `08:16:13` UTC. |
| Pre-freeze tests are outcome-blind | **FAIL (blocking)** | The frozen v3 test reads v2 gold-derived evaluation rows for the same 180 questions and checks the sign of the full-versus-validation effect. |
| Raw gold file excluded from freeze/selection code path | PASS narrowly | The release freeze records the externally supplied path/hash but does not hash, open, or parse the raw `questions.jsonl`. In `run()`, the direct raw-gold read occurs after blackboard, selection, sensitivity, and seal files are written. |
| Selection input contains no gold keys | PASS | Exactly 180 unique rows; every row has exactly `question_id` and `question`. No `gold_sql`, answer shape, order-sensitive flag, required literals, difficulty, feature, table, or column key occurs. |
| No prior same-item gold-derived information available at freeze | **FAIL (blocking)** | The v2 evaluation ledger is opened by the frozen pre-run test. The configuration statement `selection_or_rule_tuning_from_gold: false` is therefore not sufficient evidence of outcome blindness. |
| Shared operation evidence | PASS | Each run has exactly `180 x 8 x 4 = 5760` attempts. Every consecutive four-record candidate block follows T0, M1, M2, M3 database hashes, and every block's SQL hash matches the corresponding frozen candidate in its board. This is one shared evidence collection, not 5760 operations per selector. |
| Fixed-order rule | PASS | All 180 fixed-order decisions select frozen slot `C000` after evidence collection. |
| Validation-only rule and empty CF channel | PASS | All validation decisions contain zero counterfactual passes, zero evaluated states, and incomplete CF coverage for every candidate. Recomputed validation score/eligibility/original-order ties reproduce all 180 choices. |
| Full rule | PASS | Eligibility requires safe executable SQL and complete 3/3 invariant passes; recomputed validation-first ranking and ordinal tie breaking reproduce all 180 choices. No full-condition abstention occurred. |
| Three unique witnesses and invariants | PASS | M1 adds an irrelevant relation, M2 changes indexes/storage, and M3 adds nullable columns. All original named columns and rows independently match T0. Explicit-column M3 queries remain invariant. |
| M3 `SELECT *` exception predeclared | PASS mechanically | The witness manifest states that wildcard projections may fail and are not normalized away. Independent execution confirms explicit projection equivalence and wildcard arity non-equivalence. The important caveat is that the same Q039 effect was already visible in v2 before v3 freeze. |
| Full versus validation difference | PASS descriptively | Q039 is the only selection difference. Validation selects `C000` (`SELECT *`); full selects `C001` (explicit `work_order_id, scheduled_date`). The corresponding correctness values are false and true. |
| Attempts, failures, and seals retained | PASS | Per run: 5760 candidate attempts, including 332 non-executable attempts with nonempty `failure_kind` and `error`; 180 gold-execution attempts; 180 sealed boards with recomputed digests and contiguous message sequence; 540 method evaluation rows; 3240 sensitivity rows. Release-manifest hashes match all retained files. |
| A/B normalized reproduction | PASS | Selection, evaluation, sensitivity evaluation, and summary files are byte-identical. Both reproduction manifests recompute to canonical SHA-256 `71a0dbdbc004d0468ef57f8eb69e4e6caedb3b2482d92bd72bcbc6261e0d7cf2`. |
| Summary independently recomputed | PASS | Fixed order: 80/180; validation-only: 100/180; full: 101/180. Coverage, abstention, invariance, rescue, harm, and all 18 sensitivity cells exactly recompute from ledgers. |
| No LLM calls in v3 | PASS | The execution path reads frozen Qwen/Granite prediction ledgers and local SQLite files. Static inspection finds no LLM or network client in the release, core, agent, or executor path. The result is not new model generation. |

## Blocking issue

### B1. Same-item outcome information entered the pre-freeze regression gate

The problematic dependency is direct and frozen:

1. `offline_coordination_release_v3.py` calls the full test directory before writing the freeze manifest.
2. `test_offline_coordination_release_v3.py` points to the prior v2 run and witness directories rather than a synthetic structural fixture or the not-yet-run v3 release.
3. The test parses v2 `evaluation_ledger.jsonl`, whose `correct` fields were computed from the same raw gold resource later used by v3.
4. The test derives the full-versus-validation selection differences and asserts that their correctness difference has positive net sum.
5. V3 subsequently reproduces the already observed sole Q039 improvement.

This does **not** invalidate the bytes, the deterministic algorithm, the 80/100/101 descriptive counts, the 5760-operation ledger, or the post-seal ordering inside each v3 execution. It invalidates the stronger statements that the v3 selector outcome was unseen, that the 180-item evaluation was prospective, or that its rules/sensitivity were prespecified relative to these outcomes.

The existing `INDEPENDENT_AUDIT_V3.json` decision `PASS` (29/29) is therefore incomplete for release-level scientific provenance: it checks that pre-freeze tests passed but does not detect that those tests open prior gold-derived outcomes from the same items.

## Required remediation

For the present 180-item release, no rerun can erase the prior outcome visibility. The honest repair is textual and classificatory:

1. Relabel v3 as a **deterministic no-generation re-execution / descriptive offline selection analysis over a historical candidate pool and previously evaluated items**.
2. Remove `prospective-from-freeze`, `prospectively blinded`, `unseen gold outcomes`, `prespecified sensitivity`, and statements that the rules were not exposed to these 180 outcomes.
3. Retain the precise within-run statement that the **raw gold file was opened only after all 180 v3 blackboards were sealed**.
4. Report 80/100/101 and Q039 as descriptive traceable results, not confirmatory evidence of a counterfactual, coordination, robustness, or multi-agent gain.
5. Replace references to a release audit “PASS 29/29” with this split decision.

To obtain genuinely prospective evidence, create a new release on an untouched evaluation resource or on a split whose evaluation outcomes have never appeared in tests, reports, or development. Freeze the rule/code/tests against synthetic or development-only fixtures; ensure pre-run tests never open same-evaluation gold-derived artifacts; then run the untouched set once, retain incidents, and independently reproduce it. A v4 rerun of these same 180 questions would still be retrospective.

## Manuscript claim boundary

### Required limiting sentence

> Release v3 is a deterministic, no-generation re-execution over a historical candidate pool and 180 previously evaluated items; although its execution path opened the raw gold file only after all v3 blackboards were sealed, the frozen pre-run regression suite had accessed gold-derived v2 outcomes for the same items. Accordingly, the 80/180, 100/180, and 101/180 results are descriptive, and the sole Q039 wildcard-projection change is not evidence of a general counterfactual, robustness, coordination, or multi-agent gain.

### Statements that remain supportable

- The v3 execution path made no LLM calls.
- Both selectors used the same shared 5760 candidate--state execution records.
- All 180 v3 boards were sealed before that execution path directly loaded raw gold.
- Run A and run B reproduce the same canonical selections, evaluations, sensitivity results, and summary.
- Complete-invariance selection differs from validation-only only on Q039 and enforces 180/180 selected-query invariance under the three registered witnesses.

### Statements not supportable from this release

- The 180-item result is prospective, prospectively blinded, confirmatory, or preregistered relative to outcome access.
- The v3 rules or sensitivity family were demonstrably chosen without exposure to these 180 outcomes.
- The 1/180 increment establishes a counterfactual, robust, multi-agent, or general coordination benefit.
- The study evaluates new model generation, agent communication benefit, deployment safety, or an autonomous multi-agent system.

## Final decision

**FAIL** as a prospective-from-freeze scientific release because the bound pre-freeze gate reads and tests prior gold-derived outcomes from the same evaluation items. **PASS** as a hash-bound, complete, deterministic, no-generation descriptive re-execution whose ledgers and reported counts are independently reproducible under the narrow claim boundary above.
