# Real SimBench Planning Analysis - P4 SHIELD-MOEA

Status: public SimBench benchmark-derived planning experiment v1. The experiment uses actual SimBench Load, Line, RES, and Transformer/Switch-adjacent network files to derive subnets and candidate planning actions. It is not a full AC power-flow validation.

- Proposed method: `SHIELD-MOEA`
- Proposed mean hypervolume proxy: `0.79432775`
- Best baseline: `MOEA/D` with `0.77286075`
- Best ablation: `Ablation-NoScenarioScreen` with `0.76928208`
- Relative gain over best baseline: `2.78%`
- Relative gain over best ablation: `3.26%`
- Current value signal: `promising_public_signal`

## Interpretation Boundary

This is a reproducible public benchmark-derived optimization experiment. It validates candidate generation, objective design, baseline coverage, ablations, and result-table wiring. Manuscript-level electrical claims still require pandapower/AC load-flow checks and repeated scenario variance.

## Compliant Optimization Path

- Add pandapower load-flow feasibility checks when dependencies are available.
- Add rolling/load-growth scenarios and larger subnet samples.
- Keep weak ablations and constraint violations in the evidence tables.
