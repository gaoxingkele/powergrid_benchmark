# Mintou Experiment Strength Gates

## Observation

The six mintou manuscripts have executable ARA directories and public benchmark-derived evidence, but several claims are still too narrow for target-journal submission if presented as strong operational results.

## Decision

Manage the six manuscripts with explicit experiment-strength gates:

- Dataset sufficiency
- Baseline sufficiency
- Ablation coverage
- Robustness evidence
- Engineering or label-validity boundaries

## Rationale Summary

The portfolio should improve through stronger evidence rather than cosmetic rewriting. Dispatch and planning papers need feasibility or load-flow evidence before strong engineering claims. Forecasting papers must keep horizon-specific claims. Feasibility-review papers must separate public proxy construction from expert-labeled review outcomes.

## Evidence

- `papers/mintou/submission_assets/experiment_strength_upgrade_plan.md`
- `papers/mintou/submission_assets/remaining_validation_gaps.md`
- Six ARA paper directories under `papers/mintou/`

## Rules

- Dispatch and planning claims require OPF, load-flow, contingency, or feasibility evidence before strong operational wording.
- Strong 24h forecasting results do not imply 1h superiority.
- Proxy labels are not expert labels.
- Data optimization means public-data expansion, calibrated scenarios, stratified reporting, and transparent claim scoping.
- Weak, mixed, or failed runs remain part of the ARA trace.

## Next Check

Execute upgrades in priority order:

1. P2 neural baseline decision for short-horizon claims.
2. P4 contingency and feasibility validation.
3. P6 dependency-aware portfolio labels and seed variance.
4. P1 OPF/Grid2Op feasibility.
5. P3 AC load-flow and DER-hosting variance.
6. P5 expert or rule-audited review labels.
