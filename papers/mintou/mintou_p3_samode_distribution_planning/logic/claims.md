# Claims

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 | `CARS-MODE` improves DER/storage planning quality against target-journal-level baselines on the public SimBench DER/storage stress benchmark. | Supported narrowly for proxy benchmark v5 | E-real-SimBench: `0.55322842` vs NSGA-II `0.55071321` |
| C2 | Constraint-aware repair and strategy adaptation contribute beyond the strongest ablation. | Supported narrowly for proxy benchmark v5 | E-real-SimBench: strongest ablation FixedDE `0.55217215` |
| C3 | The method remains feasible or robust under DER/storage stress scenarios. | Partially supported for proxy benchmark v5 | E-real-SimBench: `mean_constraint_violation_rate=0.07036504`; still requires power-flow validation |
| C4 | The experiment package is reproducible from public or benchmark-derived data. | Public benchmark-derived evidence available | E-real-SimBench; `src/code/run_real_simbench_planning.py`; `src/configs/real_simbench_planning_config.json` |

Current public-data evidence supports only a narrow proxy-level positive signal. The next compliant path is to add pandapower/AC power-flow feasibility and scenario variance rather than overstating the SimBench aggregate result.
