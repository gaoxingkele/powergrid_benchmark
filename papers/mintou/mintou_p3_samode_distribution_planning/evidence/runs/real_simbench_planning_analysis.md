# Real SimBench Planning Analysis - P3 CARS-MODE

Status: public SimBench DER/storage stress planning experiment v5. The experiment uses actual SimBench Load, Line, RES, and Transformer/Switch-adjacent network files to derive subnets and candidate planning actions. It is not a full AC power-flow validation.

- Proposed method: `CARS-MODE`
- Proposed mean hypervolume proxy: `0.55322842`
- Best baseline: `NSGA-II` with `0.55071321`
- Best ablation: `Ablation-FixedDE` with `0.55217215`
- Relative gain over best baseline: `0.46%`
- Relative gain over best ablation: `0.19%`
- Current value signal: `promising_public_signal`

## Interpretation Boundary

This is a reproducible public benchmark-derived optimization experiment. It validates candidate generation, objective design, baseline coverage, ablations, and result-table wiring. Manuscript-level electrical claims still require pandapower/AC load-flow checks and repeated scenario variance.

## Compliant Optimization Path

- Add pandapower load-flow feasibility checks when dependencies are available.
- Add rolling/load-growth scenarios and larger subnet samples.
- Keep weak ablations and constraint violations in the evidence tables.
