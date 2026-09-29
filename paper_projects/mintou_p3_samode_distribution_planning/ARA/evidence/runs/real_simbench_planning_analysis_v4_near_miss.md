# Real SimBench Planning Analysis - P3 CARS-MODE

Status: public SimBench benchmark-derived planning experiment v1. The experiment uses actual SimBench Load, Line, RES, and Transformer/Switch-adjacent network files to derive subnets and candidate planning actions. It is not a full AC power-flow validation.

- Proposed method: `CARS-MODE`
- Proposed mean hypervolume proxy: `0.56142680`
- Best baseline: `MOEA/D` with `0.55875075`
- Best ablation: `Ablation-NoDiversity` with `0.56708815`
- Relative gain over best baseline: `0.48%`
- Relative gain over best ablation: `-1.00%`
- Current value signal: `needs_compliant_optimization`

## Interpretation Boundary

This is a reproducible public benchmark-derived optimization experiment. It validates candidate generation, objective design, baseline coverage, ablations, and result-table wiring. Manuscript-level electrical claims still require pandapower/AC load-flow checks and repeated scenario variance.

## Compliant Optimization Path

- Add pandapower load-flow feasibility checks when dependencies are available.
- Add rolling/load-growth scenarios and larger subnet samples.
- Keep weak ablations and constraint violations in the evidence tables.
