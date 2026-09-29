# AC Scope Decision

No new AC power-flow experiment was executed in this stage. The archived AC
panel evaluates one run-index-0 compromise composition per method in three
planning experiments over four networks and six fixed cases. Those 72 rows per
method are dependent case evaluations, not optimizer-seed replications.

Accordingly, the AC layer remains an **illustrative composition diagnostic**.
The matched table in `ac_common_panel_vs_no_plan.csv` uses the same No-Plan row
as a common reference for each experiment/network/case and reports paired
descriptive changes only. It supplies no p-value, binomial confidence interval,
hierarchical optimizer-seed interval, or method-superiority claim. GDE3, NSDE,
and NSGA-II+Repair were not present in the archived AC panel and are not
silently assigned electrical results.

The optimizer rerun exports a deterministic compromise composition for every
seed in `../optimizer_rerun/all_seed_compromise_compositions.csv`; those plans
were **not** evaluated by AC power flow. A future multi-seed AC study can use
that table but is not evidence for this manuscript stage.
