# Independent semantic-reliability design audit for MA-SQLGrid

## Decision

**NO-GO for claim-promoting multi-state results in the manuscript at this time.** The two frozen prediction ledgers are complete, unique, hash-consistent with their run manifests, and byte-bound to the canonical-v2 freeze. That input gate passes. The present four in-memory states are deliberately labelled a design diagnostic, however, not a formal experiment: they were created after the predictions existed, leave 20/180 gold denotations unchanged, do not resolve order-tie ambiguity, and reuse an evaluator whose float quantization is not an absolute-tolerance comparison and whose score does not compare output-column meaning.

The diagnostic is still decisive for planning. Under the archived evaluator, the snapshot has 391/720 correct Qwen question--condition pairs and 359/720 correct Granite pairs. Requiring correctness on the snapshot plus four query-blind diagnostic states retains 287 and 271 pairs, respectively. Thus 104/391 (26.6%) Qwen and 88/359 (24.5%) Granite snapshot-correct pairs fail at least one diagnostic state. These are **provisional collision flags**, not publishable corrected accuracies: some failures can arise from question ambiguity or incomplete ordering rules, so independent semantic adjudication must precede promotion.

## Audited scope and immutable inputs

The audit read, but did not alter, the GridDB source, the 180 test records, either prediction ledger, the existing semantic experiment directory, or the manuscript. It created only this audit directory. The machine-readable inventory records SHA-256 hashes for the following authoritative inputs:

- `database.sqlite`: `ba74e84f30c15ecf04bf2b1ffb5d1ccbb978a9e210b69f4676b9bde64e5bbc46`;
- `questions.jsonl`: `a08f302afb47bc2e7c352d20ca69efa0068b74d9ad296c988bc7b27160593a82`;
- frozen Qwen predictions: `53aaf0c9659f6a6b71b66ff64d34ed925664742205d0ca4fd7585d7fe5c9f5e3`;
- frozen Granite predictions: `be433ac853f60ebc8882fdcc7bd01033bca8868fa23b298114b0977476983e3`.

The diagnostic ran with Python SQLite 3.49.1. A formal release must pin and report one SQLite version and compile-option set for state generation and scoring; a result must not silently combine the original-run engine and another engine.

## Prediction-ledger provenance gate

Both ledgers pass all of the checks requested for reuse:

| Check | Qwen | Granite |
|---|---:|---:|
| Rows | 720 | 720 |
| Unique `(question_id, condition)` keys | 720 | 720 |
| Duplicate / missing / unexpected keys | 0 / 0 / 0 | 0 / 0 / 0 |
| Questions x conditions | 180 x 4 | 180 x 4 |
| Successful rows | 720 | 720 |
| Row-level data/code/config hash sets equal run manifest | PASS | PASS |
| Prediction file hash equals canonical-v2 frozen input | PASS | PASS |
| Run-manifest hash equals canonical-v2 frozen input | PASS | PASS |
| Run manifest completed and canonically eligible | PASS | PASS |

The row-level code hash is a run-contract identifier and is not assumed to be a raw file hash. The canonical-v2 `FREEZE_AND_METHOD.json` independently binds the physical run script, database, questions, manifests, prompts, predictions, and scores by file SHA-256. A formal semantic release must copy this two-layer check; row count plus `status=success` is insufficient.

## Gold-SQL risk inventory

The 180 test SQL statements have overlapping feature exposure:

| Risk stratum | Questions | Required state family |
|---|---:|---|
| Filter | 170 | categorical covering array; numeric/date boundary states; text decoys |
| Join | 102 | multiplicity and cross-link decoys with valid foreign keys |
| Aggregation | 59 | exact clones, category rebalancing, threshold-crossing states |
| Order-sensitive / `ORDER BY` | 114 | insertion-order permutation plus intentional tie states |
| Float-valued result | 36 | below/at/above-boundary real values and pairwise tolerance tests |
| Time predicate | 30 | date/time grid around schema-profile extrema and intervals |
| Top-k | 18 | tie-at-cutoff and strict-extreme states with deterministic tie policy |
| Group-by / HAVING | 12 / 2 | group creation, deletion, duplication, threshold crossing |
| Topology traversal / self-join | 11 / 9 | orientation reversal, status toggle, branch/merge motifs |
| Nested query | 6 | witness and counter-witness states for `EXISTS`, `NOT EXISTS`, `NOT IN` |
| Distinct | 3 | duplicates plus new projected values |
| Left join | 2 | parent with no child and parent with multiple children |
| Pattern / scalar function | 2 / 2 | prefix/suffix/case decoys and function boundary strings |
| NULL | 1 | both NULL and non-NULL witnesses under the same other predicates |

Five gold queries return zero rows on the snapshot: Q073, Q104, Q107, Q110, and Q140. An empty snapshot is especially collision-prone: many wrong filters, joins, and projections also return empty. Each must become nonempty in at least two pre-frozen, query-independent states before it contributes to a primary suite score.

### Diagnostic mutation sensitivity

Four schema-fixed constructors were run only in memory. Constructors read the schema/base rows but not questions, gold SQL, predictions, scores, or correctness when choosing mutations. All states have zero `PRAGMA foreign_key_check` violations and all 180 gold SQL statements execute.

| State | Operator | Changed gold denotations | Unchanged | Coverage |
|---|---|---:|---:|---:|
| S1 | exact relational-world clone with remapped PK/FK | 133 | 47 | 73.9% |
| S2 | clone with numeric `+0.125` and date/time shifts | 159 | 21 | 88.3% |
| S3 | valid cross-links, reversed topology direction, switched state | 132 | 48 | 73.3% |
| S4 | work-order clone with `completed_date` NULL/non-NULL toggle | 54 | 126 | 30.0% |
| Union | changed in one or more states | 160 | 20 | 88.9% |

The 20 gold denotations unchanged in every diagnostic state are Q039, Q042, Q058, Q073, Q077, Q104, Q107, Q110, Q140, Q148, Q152, Q153, Q154, Q180, Q184, Q186, Q187, Q188, Q192, and Q193. They reveal exactly what the formal design still lacks:

- Q039 needs a date-boundary/top-k state rather than cloning later dates;
- Q042 and Q058 need new categorical projected values, not duplicated old values;
- Q073 and Q077 need isolated-parent and anti-join witness states;
- Q104/Q107/Q110 need relation coverage for currently childless named assets;
- Q140 needs a `load` plus alarm witness;
- Q148/Q152--Q154 and Q180/Q184/Q186--Q188/Q192/Q193 need pairwise categorical covering arrays.

This diagnosis may guide an operator-family revision, but it must not guide candidate-specific row construction. General operators must be justified from schema risk classes, frozen, and then applied uniformly.

## Required formal state suite

### Separation of construction from scoring

Use two executables and two freezes:

1. **Stage A, state generation**, accepts only the immutable base database, schema profile, an operator-policy JSON, and a seed. It must run in a process that has no path or API for `questions.jsonl`, gold SQL, prediction ledgers, scores, or correctness. It writes immutable SQLite files plus a manifest containing input/output hashes, row counts, `integrity_check`, `foreign_key_check`, generator version, SQLite version/compile options, and operator trace.
2. A human/agent not involved in mutation selection signs the state manifest. Failed coverage may add a whole schema-motivated operator family in a versioned refreeze, but no existing unfavorable state may be removed and no row may be tailored to a gold or predicted SQL string.
3. **Stage B, scoring**, first verifies the signed state manifest and the canonical-v2 prediction bindings, then loads questions/gold/predictions. It is forbidden to write or choose states.

Because predictions were already visible when this study was conceived, the GridDB multi-state result remains a **retrospective robustness reanalysis**, even after a clean two-stage implementation. It may become preregistered only for a new sealed database/prediction release.

### Minimum state families

- **T0 snapshot:** the unmodified database.
- **T1 insertion permutation:** logically identical databases inserted in at least three fixed permutations. This diagnoses reliance on unspecified row order; it does not count as independent semantic evidence.
- **T2 relational multiplicity:** exact, valid PK/FK-remapped clones to expose missing `DISTINCT`, fan-out joins, and aggregate errors.
- **T3 categorical covering array:** query-blind pairwise combinations for categorical columns within a table (priority x status, region x criticality, type x alarm, etc.), using the database-derived domain plus a fixed sentinel value.
- **T4 numeric/date boundaries:** schema-profile min, max, midpoint, and fixed epsilon-offset values; include deliberate ties and values on both sides of derived grid boundaries. Do not extract constants from SQL.
- **T5 NULL witnesses:** NULL and non-NULL `completed_date` rows matched on all other work-order attributes.
- **T6 relationship witnesses/counter-witnesses:** parent without child, parent with one/many children, permuted valid FKs, and cross-region/type assignments.
- **T7 topology motifs:** reversed edge, open/closed status, branch, merge, length-two path, and disconnected asset, all FK-valid.
- **T8 string decoys:** fixed case, prefix, suffix, whitespace, and punctuation transforms for text domains, without inspecting `LIKE` or equality predicates.
- **T9 anti-join and empty-break coverage:** isolated active technician, alarming asset without open order, and child rows for every asset. These are general relationship states, not repairs for named questions.

For every state, execute `PRAGMA integrity_check`, `PRAGMA foreign_key_check`, enforce `PRAGMA foreign_keys=ON`, and retain a complete insert/update trace. The original evaluator opens SQLite with foreign keys off; the state generator must not inherit that default.

## Result-comparison contract

The original evaluator is internally consistent in three important respects: unordered results are duplicate-preserving multisets (`Counter`), ordered results are compared as sequences, and NULL is mapped to a distinct sentinel. It also treats integer `1` and float `1.0` as equal, which is reasonable for SQLite numeric affinity.

Four fixes/decisions are mandatory before formal use:

1. **Ordering:** preserve sequence comparison only after adjudicating all 114 order-sensitive questions. Every top-k gold SQL must define a total order at the cutoff or the natural-language item must explicitly accept all ties. Add deterministic secondary keys where semantically justified. Run insertion-permutation states. A query without a semantically complete order is BLOCK, not automatically wrong.
2. **Floats:** replace `round(value/tol)*tol` binning. It can declare `0.49e-6` and `0.51e-6` unequal although their difference is below the stated `1e-6` tolerance. Use finite-number checks and pairwise `isclose` with predeclared absolute and relative tolerances. For unordered rows containing floats, use exact grouping on non-float fields followed by deterministic bipartite matching, retaining duplicate multiplicity.
3. **Columns:** the current scorer checks column count but not names or semantic provenance. Keep denotation equality as the primary semantic criterion only if the review protocol explicitly says headers are irrelevant. Otherwise compare normalized output labels against `answer_shape.columns`. At minimum, report header agreement as a diagnostic and manually audit same-valued wrong-column cases.
4. **Resource safety:** enforce one read-only statement, SQLite authorizer restrictions, progress/step timeout, row/byte caps, and deterministic failure categories. Record query errors separately from semantic mismatches; never coerce error-on-one-state into ordinary zero.

Do not sort ordered results after execution. Do not turn unordered results into sets; duplicates are semantic. Compare gold and candidate afresh on each state, rather than comparing a candidate state result to the snapshot gold.

## Minimal statistical report

The finite 180-question corpus is the estimand; avoid population-confidence language. Report, for each backbone x condition:

- `n=180`, state count, and all input/state/evaluator hashes;
- snapshot correct, suite correct (correct on every eligible state), and collision flags among snapshot-correct items, with exact numerators/denominators;
- per-state correct counts and per-state gold-denotation changed/unchanged counts;
- coverage by join, aggregation, order, top-k, NULL, float, empty-snapshot, and difficulty strata;
- paired suite-accuracy contrasts for the frozen 2x2 conditions, with the existing normalized-SQL cluster definitions, cluster sign-flip/randomization inference, and one predeclared multiplicity family; label intervals as composition-sensitivity intervals;
- backbone differences as modifiers, not independent replications, unless the same direction survives the frozen family;
- an adjudication flow table: automatic pass, automatic fail, ambiguous-order hold, execution-error hold, and human-resolved cases;
- sensitivity results under strict exact numeric comparison and the predeclared tolerance comparator.

Do not p-hack over states, seeds, tolerance values, or subsets. The primary suite operator is logical AND across predeclared eligible states. Per-state scores are diagnostics, not opportunities to select the most favorable state.

## Go/no-go gates for a claim-promoting release

| Gate | Requirement | Current |
|---|---|---|
| G1 input identity | 720 unique expected keys per backbone; run hashes and canonical freeze all match | **PASS** |
| G2 generator blindness | Stage-A executable cannot access questions/gold/predictions/scores; signed pre-score freeze | **BLOCK** |
| G3 state reproducibility | state DB hashes, operator traces, pinned SQLite/compile options, deterministic rerun | **BLOCK** |
| G4 database validity | FK on; integrity/FK checks zero; all gold execute in every state | diagnostic PASS; formal **BLOCK** |
| G5 semantic coverage | all 180 have predeclared relevance coverage; all five empty results broken; every risk stratum covered; changed/unchanged counts reported | **BLOCK** (160/180 changed; five empty remain empty) |
| G6 ordering | 114 order-sensitive and 18 top-k items independently adjudicated; total-order/tie policy frozen | **BLOCK** |
| G7 comparison semantics | multiset/sequence/NULL tests pass; float comparator fixed; column-label policy frozen | **BLOCK** |
| G8 no adaptation | no state/candidate removal or mutation selected after viewing scores; version history retained | **BLOCK** |
| G9 statistics | finite-corpus estimand, paired clustered contrasts, multiplicity family, all strata and holds reported | **BLOCK** |
| G10 release audit | independent rerun reproduces every row; manifest and tests cover ledgers, states, scores, tables, and figures | **BLOCK** |

Promotion rule: all gates must pass. If G5 cannot reach full coverage without question-specific adaptation, report the covered subset only as a predeclared secondary analysis and retain the snapshot metric as the limited primary result. Do not describe the current four-state diagnostic counts as corrected accuracy.

## Independent release checklist

- [ ] Recompute SHA-256 for database, questions, evaluator, both manifests, both predictions, and canonical freeze.
- [ ] Verify exactly 180 x 4 unique keys in each ledger, no duplicates/missing/unexpected keys, all `status=success`.
- [ ] Verify row-level data/code/config fields are singleton sets and equal the corresponding run-manifest values.
- [ ] Verify both prediction and manifest physical hashes equal canonical-v2 accepted inputs.
- [ ] Inspect Stage A imports/CLI and filesystem trace; prove it cannot read question, gold, prediction, or score artifacts.
- [ ] Regenerate states twice in clean directories and compare byte or canonical logical hashes.
- [ ] Check `integrity_check`, `foreign_key_check`, table counts, schema hash, and mutation trace for every state.
- [ ] Execute all 180 gold queries in every state; report errors and changed/unchanged denotations by state and union.
- [ ] Confirm all five snapshot-empty queries become nonempty in at least two general-purpose states.
- [ ] Independently review 114 ordering labels and 18 top-k tie rules before scoring predictions.
- [ ] Unit-test ordered sequence, unordered multiset with duplicates, NULL, numeric affinity, float boundary, and wrong-column/same-value cases.
- [ ] Score both ledgers without changing states; persist one row per backbone x condition x question x state.
- [ ] Recompute suite AND aggregation from atomic rows; no use of cached snapshot scores.
- [ ] Recompute paired clustered statistics and multiplicity corrections from atomic suite rows.
- [ ] Verify every paper table/figure cell traces to a hashed analysis row and carries the retrospective/finite-corpus limitation.

## Applied Sciences assessment

[Target] Applied Sciences (MDPI)  
[Fit] Medium until semantic and external validation gates close; the applied power-grid framing is relevant, but one-state execution equality is too weak for the claimed reliability contribution.  
[Contribution type] applied-method with benchmark validation  
[Main evidence gap] query-independent multi-state semantic validation plus independent order/tie adjudication  
[Best-fit Section] Computing and Artificial Intelligence, with an electrical-power application framing  
[Top rejection risk] weak validation caused by snapshot collisions and synthetic-corpus tailoring

