# Prospectively frozen multi-state SQL reliability protocol

## Scope and claim boundary

This experiment is an automated database-state stress test of execution
agreement.  It is **not** a human semantic audit and does not establish that a
gold query correctly formalizes its natural-language question.  The estimand is
the fraction of predictions that agree with the frozen gold SQL on the original
GridDB state but cease to agree on one or more deterministic, schema-valid
perturbation states ("false frozen-state agreements").

## Prospective separation

`freeze` reads only the schema, database, test questions, and this code.  It
must not open either model's prediction file.  It deterministically constructs
the states, validates their integrity, records all SHA-256 hashes, and writes a
freeze lock.  Only `run`, after verifying the lock and state hashes, may load
the 1,440 archived predictions.  No state is added, removed, or adapted after
prediction results are observed.

## States

The original state and six perturbations are evaluated.  Perturbations append
referentially coherent cohorts with remapped primary keys:

1. `P1_exact_clone`: one exact attribute/relationship clone;
2. `P2_attribute_rotation`: non-key attribute tuples rotate within each table;
3. `P3_relation_rewire`: foreign keys rotate among valid referenced rows;
4. `P4_numeric_time_shift`: numeric measurements and ISO dates shift by fixed rules;
5. `P5_combined`: attribute rotation, relationship rewiring, and numeric/time shifts;
6. `P6_two_cohorts`: one exact and one combined cohort.

These are synthetic, deterministic test-suite states.  "Valid" means the
unchanged schema accepts the data, `PRAGMA integrity_check` is `ok`, foreign-key
checking returns no violations, all NOT NULL constraints remain satisfied, and
every gold query executes with its declared projection width.  It does not mean
that every synthetic record has been certified by a power-system operator.

## Execution and denominators

Every one of the 1,440 predictions is executed on all seven states; failures
remain in the denominator.  SQL is restricted to one `SELECT`/`WITH` statement,
opened with SQLite `mode=ro&immutable=1`, guarded by an authorizer, and bounded
by a progress deadline.  Results use the frozen evaluator's multiset comparison
for order-insensitive questions, ordered comparison otherwise, and 1e-6 float
normalization.

Primary outcomes are: original-state agreement count; multi-state suite pass
(agreement on all seven states); false-agreement count among original-state
agreements; and the false-agreement proportion with an exact Clopper--Pearson
95% interval.  State-level failures, backbone/condition strata, SQL feature
strata, execution errors, and complete row-level logs are reported without
post-hoc exclusions.

