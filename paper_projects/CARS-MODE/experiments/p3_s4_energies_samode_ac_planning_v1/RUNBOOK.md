# P3 S04 Frozen Protocol Runbook

**Current disposition:** `DO NOT RUN / NO_RESULTS`.

This runbook records the required order of operations. It is not an executable
runner and does not authorize an experiment while the protocol gate is blocked.

1. Verify all four exact SimBench MV identifiers, versions, licenses, and file
   hashes without consulting method outcomes; update the versioned data record.
2. Supply every actual optimizer coordinate and its unique action binding in
   `action_registry.json`; validate it with `validate_complete_registry`.
3. Freeze storage dispatch, DER reactive-power/power-factor behavior, the N-1
   branch, transformer applicability/limit, and pandapower/runtime versions.
4. The control settings in `config.json` are frozen and may not be tuned. Keep
   tuning seeds 91001--91010 isolated for implementation-only diagnostics;
   never use pilot or confirmatory seeds for selection.
5. Run the method-contract unit tests and deterministic replay. Record source,
   config, data, registry, and environment SHA-256 values.
6. Run only pilot seeds 99001--99003. Audit schemas, paired initialization,
   4,800-row counters, registry coverage, action application, AC failures, and
   leakage. Store the pilot separately with `paper_use=false`.
7. A human-reviewed pilot gate may authorize the formal run only if all cells
   pass. Do not change arms, seeds, budgets, outcomes, references, families, or
   failure rules after viewing pilot performance.
8. Run all seven methods on all six configurations and 30 paired confirmatory
   seeds. Preserve every failed or incomplete cell and update
   `planned_vs_executed.json` without overwriting legacy or pilot artifacts.
9. Select up to five plans per front by the frozen equal-weight normalized-ideal
   rule, apply registered actions to fresh network copies, and evaluate all four
   networks and six cases.
10. Produce the intention-to-run primary analysis, paired effect sizes and
    intervals, three separate Holm families, complete failure ledger, and a
    dedicated negative-results table. Keep joint and proxy/AC scope qualifiers.

Stopping immediately is mandatory if hashes drift, a registry row is missing,
one method exceeds the objective-row ceiling, a paired seed is selectively
lost, or an unresolved engineering policy is encountered. Record the incident;
do not improvise a replacement action, seed, network, reference, or threshold.
