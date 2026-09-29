# Real Project Review Analysis - P6 BiLo-NSGA

Status: public RTS-GMLC + SimBench + NERC/C2GES-report-cache benchmark-derived budget-constrained project review experiment v1.

- Proposed method: `BiLo-NSGA`
- Proposed mean hypervolume proxy: `1.57351601`
- Best baseline: `Random Feasible` with `5.36989256`
- Best ablation: `Ablation-ShallowLocalSearch` with `1.77302497`
- Relative gain over best baseline: `-70.70%`
- Relative gain over best ablation: `-11.25%`
- Current value signal: `needs_compliant_optimization`

## Interpretation Boundary

This experiment derives project candidates from public grid case statistics and public reliability-report metadata. It evaluates portfolio optimization, traceability, feasibility, and ranking robustness proxies. It is not a replacement for utility expert labels or a full engineering economic review.

## Compliant Optimization Path

- Add expert-labeled feasibility-review outcomes when available.
- Add AC/pandapower feasibility and cost-calibration checks for selected projects.
- Preserve weak baselines, constraint violations, and failed ablations in evidence tables.
