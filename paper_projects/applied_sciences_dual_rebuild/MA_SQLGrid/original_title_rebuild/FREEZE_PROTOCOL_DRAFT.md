# Draft Prospective Freeze: MA-ORIGINAL-TITLE-COORD-v0.1

Status: **DRAFT — NOT AUTHORIZED FOR FORMAL EXECUTION**  
Created: 2026-08-08, Asia/Shanghai

## 1. Objective and estimand

Estimate whether explicit, reference-free coordination changes execution accuracy
and robustness relative to matched single-generation and staged baselines, holding
the model snapshot, question set, database snapshot, decoding parameters and total
candidate budget fixed. The principal estimand is the paired change in execution
accuracy per question. Robustness and resource use are secondary estimands.

This draft does not authorize API calls, GPU generation, edits to prior freezes,
or incorporation of results into the manuscript.

## 2. Roles and immutable handoffs

The six roles and their serialized outputs are fixed by
`ma_sqlgrid_agents.py`: Query Analyst, Schema Cartographer, SQL Synthesizer,
Execution and Safety Validator, Counterfactual Critic, and Adjudicator. All role
messages are written to one append-only blackboard and sealed before any gold
evaluation. The audit digest is stored with the terminal record.

Forbidden pre-evaluation fields: `gold_sql`, `gold_result`, `gold_results`,
`answer`, `answers`, evaluator correctness, or any derivative thereof.

## 3. Proposed matched conditions

1. `SINGLE`: one direct SQL candidate, no inter-role coordination.
2. `STAGED`: query/schema context followed by one SQL candidate and validation;
   no alternative candidate and no adjudication.
3. `MULTI_NO_CF`: fixed candidate budget, validation and deterministic
   adjudication; counterfactual evidence withheld.
4. `MULTI_FULL`: the same candidates plus the frozen counterfactual state suite.

The exact candidate count, generation order and call accounting must be filled in
before freezing. Equalize the physical generation-call budget across conditions or
pre-register a separate budget-controlled contrast. Do not claim a coordination
effect from a comparison confounded by candidate count.

## 4. Proposed datasets and units

- Primary domain benchmark: frozen GridDB test questions and SQLite snapshot.
- Public generalization benchmark: BIRD Mini-Dev only if its existing protocol
  permits reuse or a separate new freeze is approved.
- Diagnostic state suites: existing schema-valid semantic reliability states;
  RTS-GMLC/SimBench only under separately specified mappings.
- Unit of inference: question, clustered by database where multiple databases are
  present. Repeated candidates/states are not independent samples.

Exact file paths, SHA-256 values, inclusion/exclusion rules and denominators must
be inserted into the machine-readable lock before authorization.

## 5. Deterministic adjudication

Eligibility requires a safe, executable candidate. Selection order is:

1. validation points (safety, execution, shape, order and capped value hits);
2. counterfactual pass rate when evaluated;
3. number of evaluated counterfactual states;
4. original candidate order.

If no candidate is eligible, the coordinator abstains. Missing counterfactual
evidence is unknown, never a pass. No retry, silent exclusion, manual selection or
gold-guided repair is permitted.

## 6. Outcomes and analysis

Primary: execution accuracy using the frozen official evaluator.  
Secondary: valid SQL rate, unsafe SQL rate, abstention rate, repair rescue/harm if
repair is separately enabled, complete-state pass rate, false frozen-state
agreement rate, latency and input/output tokens.

Planned comparisons are paired at question level. Report absolute paired
differences, clustered/bootstrap 95% confidence intervals and a preselected paired
randomization or McNemar test as appropriate. Apply Holm correction to the fixed
family of secondary pairwise contrasts. Report all denominators and failures.

## 7. Failure and incident policy

- Every attempted call receives a terminal ledger row.
- New failed runs are retained verbatim and excluded only by pre-registered rules.
- No automatic retry beyond the frozen retry limit.
- No continuation, overwrite or deletion of the two existing BIRD incident runs.
- Parser, evaluator or state-suite changes require a new protocol version and hash.

## 8. Required pre-freeze gates

- [ ] Resolve exact dataset/database/model/config hashes.
- [ ] Fix candidate count and matched physical-call budget.
- [ ] Add adapters that consume frozen prompt/candidate records without gold data.
- [ ] Add integration tests against a disposable SQLite fixture.
- [ ] Define the counterfactual state IDs and evidence-field contract.
- [ ] Pre-register primary/secondary contrasts and multiplicity family.
- [ ] Generate a machine-readable manifest containing SHA-256 for every input and
      executable source file.
- [ ] Independent audit confirms zero gold leakage and deterministic replay.
- [ ] Author supplies explicit final-run authorization for the resulting hash.

Until every gate is checked and a final SHA-256 is authorized, only offline unit
tests with synthetic evidence may be run.
