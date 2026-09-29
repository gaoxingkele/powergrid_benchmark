# P3 Next Stage: Adaptation Identification and AC Planning Gate

**Stage status:** `QUEUED_AFTER_P1 / NOT YET RUN`  
**Planned namespace:** `experiments/p3_s4_energies_samode_ac_planning_v1/`

## Goal

Separate parameter adaptation from strategy adaptation and demonstrate at least one reproducible planning-action-to-AC-validation loop.

## Ordered work

1. Locate every use of `strategy_adaptive` and document current coupling and backward-compatibility behavior.
2. Introduce independent parameter-adaptation and strategy-adaptation switches without changing legacy results by default.
3. Add unit tests for the four 2×2 mechanism arms and deterministic replay under a fixed seed.
4. Map a minimal set of line/transformer/DER/storage actions to one public network, with cost and model effects.
5. Run a small AC feasibility pilot; record voltage/thermal violations and failed power-flow cases explicitly.
6. Freeze primary reference set/point, IGD+, paired seeds, baselines, scenario aggregation, and correction before formal runs.
7. Run formal cross-network/scenario comparison only after both code and physical gates pass.

## Decision outcomes

- **GO:** four-arm identification and at least one action-aligned AC loop are reproducible.
- **CONDITIONAL:** identification succeeds but engineering validation is one-case only; write a bounded case study.
- **NO-GO:** adaptation remains coupled, metric selection remains post hoc, or decisions cannot map to network changes.

## Author input

Public networks and explicit scenario assumptions can support the pilot. Real candidate actions, costs, load-growth cases, or internal engineering review would improve external validity but are not required to start.
