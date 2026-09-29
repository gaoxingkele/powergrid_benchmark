# Real Project Review Analysis - P6 BiLo-NSGA

Status: public RTS-GMLC + SimBench + NERC/C2GES-report-cache benchmark-derived budget-constrained project review experiment v1.

- Proposed method: `BiLo-NSGA`
- Proposed mean hypervolume proxy: `1.70989680`
- Best baseline: `AHP-TOPSIS` with `1.64612807`
- Best ablation: `Ablation-ShallowLocalSearch` with `1.65100922`
- Relative gain over best baseline: `3.87%`
- Relative gain over best ablation: `3.57%`
- Current value signal: `promising_public_signal`

## Interpretation Boundary

This experiment derives project candidates from public grid case statistics and public reliability-report metadata. It evaluates portfolio optimization, traceability, feasibility, and ranking robustness proxies. It is not a replacement for utility expert labels or a full engineering economic review.

## Compliant Optimization Path

- Add expert-labeled feasibility-review outcomes when available.
- Add AC/pandapower feasibility and cost-calibration checks for selected projects.
- Preserve weak baselines, constraint violations, and failed ablations in evidence tables.
