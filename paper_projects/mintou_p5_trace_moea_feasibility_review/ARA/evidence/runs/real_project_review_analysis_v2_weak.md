# Real Project Review Analysis - P5 TRACE-MOEA

Status: public RTS-GMLC + SimBench + NERC/C2GES-report-cache benchmark-derived traceable feasibility review experiment v1.

- Proposed method: `TRACE-MOEA`
- Proposed mean hypervolume proxy: `1.81532648`
- Best baseline: `Random Feasible` with `2.97835093`
- Best ablation: `Ablation-SingleObjective` with `1.86515119`
- Relative gain over best baseline: `-39.05%`
- Relative gain over best ablation: `-2.67%`
- Current value signal: `needs_compliant_optimization`

## Interpretation Boundary

This experiment derives project candidates from public grid case statistics and public reliability-report metadata. It evaluates portfolio optimization, traceability, feasibility, and ranking robustness proxies. It is not a replacement for utility expert labels or a full engineering economic review.

## Compliant Optimization Path

- Add expert-labeled feasibility-review outcomes when available.
- Add AC/pandapower feasibility and cost-calibration checks for selected projects.
- Preserve weak baselines, constraint violations, and failed ablations in evidence tables.
