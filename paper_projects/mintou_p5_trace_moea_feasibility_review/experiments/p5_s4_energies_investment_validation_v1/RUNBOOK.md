# P1 s04 Frozen Runbook

**State:** non-paper pilot completed; tuning and formal execution have not
started, and the pilot is not a scientific manuscript result.

1. The three permitted source inputs were snapshotted without modifying the
   legacy experiment. Exact pilot-local paths and SHA-256 hashes are recorded,
   and the 120-row proxy pool was generated with a hashed construction program.
   NERC metadata redistribution remains unresolved, so release/formal work is
   stopped pending human/legal review.
2. The non-paper pilot checked deterministic replay, objective-call counting,
   seed propagation, output schema, budget calculations, metric orientation,
   and wall-time measurement. Pilot rows stay under `pilot/` and never enter
   tuning or formal outputs. The resolved NumPy/SciPy versions do not match the
   frozen environment, so recreate that environment before proceeding.
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

Formal execution remains blocked by the frozen-environment mismatch and the
unresolved NERC metadata redistribution decision. The candidate/source hashes,
objective-call equality, deterministic replay, and `bounds.csv` binding passed
the pilot mechanics gate; this does not convert pilot metrics into evidence.
