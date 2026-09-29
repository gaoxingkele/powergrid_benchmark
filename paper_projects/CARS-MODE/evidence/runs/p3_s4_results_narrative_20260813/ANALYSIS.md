# P3 S4 Configuration-Level Results Narrative

## Analysis status

This stage performs deterministic aggregation and artifact generation only. It runs no optimizer and no AC power flow. The canonical input/output contract is `manifest.json`; every upstream CSV is pinned there by SHA-256.

## Configuration and replication rule

The archive has six distinct deterministic configurations and seven experiment-labelled seed blocks. `pareto_quality` is an independently seeded replication of `base_distribution_planning`. For descriptive base-configuration estimates, their two 30-run blocks are pooled. For cross-configuration summaries, each of the six configurations receives one weight. For inference, the seven upstream seed blocks and their existing within-block Holm families remain separate.

## Configuration-specific effects

Effects are oriented so that positive values favor CARS-MODE.

- Relative to NSGA-II+Repair, sampled-bound/clipped HV favors CARS-MODE in 6/6 configurations.
- Analytic HV at reference 1.05 favors CARS-MODE in 3/6 configurations.
- Common-reference IGD+ favors CARS-MODE in 1/6 configurations.
- Relative to FixedDE, sampled-bound/clipped HV is lower for CARS-MODE in 6/6 configurations.

With equal configuration weight, CARS-MODE versus NSGA-II+Repair is 0.04240014 versus 0.03997622 on sampled-bound/clipped HV, 0.00043464 versus 0.00043530 on analytic HV at reference 1.05, and 0.02218917 versus 0.02117209 on common-reference IGD+. CARS-MODE ranks third, fourth, and fifth, respectively. FixedDE remains nominally ahead of CARS-MODE on all three summaries.

## Decision-value boundary

The archived AC common panel is an illustrative composition diagnostic. For CARS-MODE, 11 matched rows change from infeasible to feasible and 3 change in reverse relative to No-Plan; the median maximum-loading change is -16.97 percentage points. These dependent rows arise from three run-index-0 compositions and do not estimate optimizer-seed physical feasibility. Their supported value is screening: they expose proxy--physics disagreements that require action-aligned power-flow follow-up.

## Generated artifacts

Run `D:\Python\Python314\python.exe scripts/generate_p3_s4_artifacts.py` in this environment, or use an equivalent Python interpreter with pandas plus Windows PowerShell/System.Drawing. The command validates all source hashes, regenerates the declared tables, and renders the declared figures. Runtime columns are retained as rerun-environment provenance only and do not support engineering-value claims.
