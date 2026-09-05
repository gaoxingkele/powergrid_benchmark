# P2 s4 Frozen-Protocol Runbook

## Current gate

**STOP: formal execution is not authorized.** `data_manifest.json` and `environment.json` contain unresolved null fields. This runbook freezes the order and checks; it does not authorize filling missing scientific inputs by inference.

## A. Pre-pilot input gate

1. Inspect each source snapshot. Record its local artifact and SHA-256; the two source digests must differ.
2. Build the RTS branch and SimBench line registries with persistent source-element IDs, family-qualified action IDs, capacity increments, formula inputs, synthetic costs, formula IDs, coefficients, and provenance. Hash each registry.
3. Validate disjoint namespaces, separate generators, finite nonnegative costs, positive budgets, finite objective implementations, and family-specific analytic normalization bounds.
4. Capture and hash the runner, dependency lock, host, thread limits, and power mode in `environment.json`.
5. Confirm that the frozen arms, formal/pilot seeds, caps, HV/IGD+ rules, comparison families, multiplicity, and failure policies match `config.json`. Evidence-bound manifest values may be filled before pilot; these protocol choices may not be changed after formal results are visible.

If any item fails, retain `NO_GO`, add the blocker to `planned_vs_executed.json`, and do not create a formal results directory.

## B. Pilot gate (not paper evidence)

Run all six methods for both families using only the five family-specific pilot seeds. Verify:

- forward and backward switches produce the four declared arms and `backward_only` never invokes substitution;
- identical within-family seed indices and task snapshots reach every method;
- every request, unique cache miss, and cache hit reconciles exactly;
- no run exceeds 3,200 unique evaluations, 6,400 requests, or the declared wall-time behavior;
- violation, repair, feasibility, and cost-to-budget values agree on sampled phenotypes;
- HV empty-front behavior and the 1.05 clipped reference are tested;
- IGD+ reference construction is symmetric across methods and separated by family/instance/protocol;
- deterministic repeated runs match for evaluation counts and front hashes; wall-time variation is recorded, not forced to match; and
- all warnings and failures are reviewed.

Pilot files stay under `pilot/`, carry `paper_use=false`, and are excluded from every formal empirical reference set and inferential table. A signed `pilot/PILOT_GATE.json` is required before formal execution.

## C. Formal execution

Create an immutable output root. For each family and each compute protocol, iterate seed indices 0--29. Rotate method order deterministically by seed index, but keep the family-specific seed value fixed across all six methods. Write one row per attempt immediately and never overwrite it.

An infrastructure failure may be retried once under the identical frozen state; retain both attempts. Do not retry algorithmic failures and do not replace seeds. Stop the study if a hash changes, cross-family cache/action leakage appears, or an unregistered configuration is requested.

Expected formal matrix: `2 families x 2 protocols x 30 seed indices x 6 methods = 720 runs`.

## D. Locked analysis

1. Verify hashes, row keys, seed pairing, cap accounting, and failure classifications.
2. Extract finite feasible non-dominated unique fronts.
3. Compute clipped normalized HV with the family bounds and all-1.05 reference vector.
4. Construct the separate pooled empirical IGD+ reference set for each family/instance/protocol, then compute IGD+ for every run.
5. Apply only the contrasts and separately Holm-corrected families in `config.json`. Use contrast-specific complete paired blocks; report every exclusion. Downgrade according to the frozen failure threshold.
6. Emit feasibility, synthetic-cost, calibrated-cost-nullability, and compute summaries without deployment, ROI, electrical-feasibility, or audit claims.
7. Populate both primary and `NEGATIVE_RESULTS.csv` outputs. Retain negative, null, reversed, and inconclusive findings and the protected historical NSGA-II result.
8. Update `planned_vs_executed.json` from the immutable manifest. Do not retune, change normalization, replace seeds, or add a comparator after viewing results.

## E. Required formal records

The formal package must contain the raw run table, failed-run ledger, front artifacts and hashes, run manifest, configuration/data/environment hashes, primary and negative-result tables, statistical audit, and claim-evidence bindings. Absence of any record is a failed execution gate, not permission to infer its contents.
