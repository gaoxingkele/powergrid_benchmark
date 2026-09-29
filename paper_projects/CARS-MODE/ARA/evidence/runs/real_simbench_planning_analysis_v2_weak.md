# Real SimBench Planning Analysis - P3 CARS-MODE

Status: public SimBench benchmark-derived planning experiment v1. The experiment uses actual SimBench Load, Line, RES, and Transformer/Switch-adjacent network files to derive subnets and candidate planning actions. It is not a full AC power-flow validation.

- Proposed method: `CARS-MODE`
- Proposed mean hypervolume proxy: `0.44676559`
- Best baseline: `Standard DE` with `0.51681058`
- Best ablation: `Ablation-NoDER` with `0.59425328`
- Relative gain over best baseline: `-13.55%`
- Relative gain over best ablation: `-24.82%`
- Current value signal: `needs_compliant_optimization`

## Interpretation Boundary

This is a reproducible public benchmark-derived optimization experiment. It validates candidate generation, objective design, baseline coverage, ablations, and result-table wiring. Manuscript-level electrical claims still require pandapower/AC load-flow checks and repeated scenario variance.

## Compliant Optimization Path

- Add pandapower load-flow feasibility checks when dependencies are available.
- Add rolling/load-growth scenarios and larger subnet samples.
- Keep weak ablations and constraint violations in the evidence tables.
