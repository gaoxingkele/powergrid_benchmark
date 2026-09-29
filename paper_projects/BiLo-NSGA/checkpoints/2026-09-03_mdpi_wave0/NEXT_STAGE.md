# P2 Next Stage: Applied Sciences Grid-Investment Gate

**Stage status:** `QUEUED_AFTER_P1_P3_P4 / NOT YET RUN`  
**Planned namespace:** `experiments/p6_s4_applsci_grid_investment_v1/`

## Goal

Test non-dominated sorting and bidirectional local search as a normal power-grid investment optimizer without inventing cybersecurity semantics and without suppressing the existing NSGA-II loss.

## Ordered work

1. Freeze the old proxy task as task family A and reconstruct its fairness accounting.
2. Implement one switch per component: NDS-only, forward-only, backward-only, and bidirectional; keep repair separate.
3. Define task family B using traceable grid investment actions, costs, and a reproducible evaluation path.
4. Pilot both families with 3–5 common seeds; audit unique evaluations, constraints, caching, and move semantics.
5. Freeze the formal comparison family, HV/IGD+ definitions, seeds, correction, and failure handling.
6. Run formal experiments and update the register with positive, negative, and unresolved outcomes.

## Decision outcomes

- **GO:** component attribution, two task families, strong baselines, and at least one engineering-validation layer all pass.
- **CONDITIONAL:** only task-dependent value is found; write a boundary/diagnostic study.
- **NO-GO:** bidirectionality cannot be separated, budgets are unfair, or title-method implementation remains inconsistent.

## Explicit non-action

PG-T13 and cybersecurity investment are not part of this stage. The SCN alternative may be resumed only with real intervention semantics and a separate author decision.
