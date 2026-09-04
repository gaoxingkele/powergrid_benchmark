# P1 s04 Frozen Runbook

**State:** protocol only; no command below has been executed as a scientific run.

1. Materialize the three permitted source inputs without modifying the legacy
   experiment. Verify source-specific licences, record exact local paths and
   SHA-256 hashes in `data_manifest.json`, and generate the 120-row proxy pool
   with a hashed construction program. Stop if any required provenance or
   licence field remains unresolved.
2. Create the exact environment in `environment.json`. Record the resolved lock
   and its hash. Run a non-paper pilot that checks deterministic replay,
   objective-call counting, seed propagation, output schema, and wall-time
   enforcement. Pilot rows stay under `pilot/` and never enter tuning or formal
   outputs.
3. Verify the Stage-4 `bounds.csv` against the recorded Stage-3 source-artifact
   hash. These conservative analytic bounds were derived without method
   outputs. Hash the Stage-4 subset and bind that hash into every later row.
4. Execute all four frozen tuning grids on the four development-only scenarios
   and ten development seeds. Enforce 3,200 objective calls and 1,800 seconds
   per stochastic run. Publish every cell and apply the frozen median-HV and
   lexicographic tie rule. Lock the selected configurations.
5. Confirm that no development scenario or seed appears in the confirmatory
   schedule. Then execute the seven stochastic methods on the three
   confirmatory scenarios and thirty confirmatory seeds. Execute deterministic
   references once per scenario and label them descriptive.
6. Run the four-level budget scan in `preference_aware_support` for Full TRACE,
   NSGA-II, and R-NSGA-II. Reuse—not rerun—the 1.00-B main cells.
7. Preserve failures under the frozen policy. Do not add seeds, calls, alternate
   package versions, bounds, metrics, or favorable subsets.
8. Analyze all 18 primary comparisons as one Holm family. Write every primary,
   secondary, null, adverse, and failed result before revising manuscript prose.
   Update `planned_vs_executed.json` and a run manifest with artifact hashes.

Formal execution is blocked while `data_manifest.json` has missing hashes or
unverified licences, while the `bounds.csv` hash is unbound, or while the
planned runtime has not passed the pilot gate.
