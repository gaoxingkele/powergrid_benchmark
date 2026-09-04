# P1 s4 Experiment Protocol

**Status:** `SCAFFOLD_ONLY / DESIGN_NOT_FROZEN / NO_RESULTS`  
**Purpose:** cost, physical-feasibility, or external validation of the investment proxy; isolated hybrid-component tests.  
**Protected predecessor:** `../p5_s3_matched_sensitivity/` is read-only.

Before any formal run, add immutable machine-readable configuration, environment lock, data-provenance manifest, seed list, baseline budget, primary metric/reference definition, comparison family, correction rule, failure policy, and output schema. Pilot outputs must be stored separately from formal outputs and must never be cited as confirmatory results.

No numeric result exists in this namespace at Wave 0.

## Stage-3 asset gate (2026-09-04)

This gate records usability, not an experiment result. The detailed authority is
`manuscript/reconstruction_v2/METHOD_DATA_IMPLEMENTATION_CONTRACT.md` and its
machine-readable companion.

| Candidate validation layer | Decision | Reason | Permitted scope |
|---|---|---|---|
| Candidate-level cost calibration | `NO_GO` | No source-specific licence/redistribution record, candidate-to-record mapping, or currency/base-year transform is present in this worktree. | Synthetic cost units only; no actual-return or calibrated cost-effectiveness claim. |
| AC/OPF post-validation | `NO_GO` | Portfolio bits select archetype proxies and cannot be mapped to bus, branch, generator, topology, dispatch, or control actions. A stage-local licence manifest is also absent. | Budget-feasible proxy portfolios only; no electrical-feasibility claim. |
| Existing NERC/MTEP16 records | `GO_DESCRIPTIVE_ONLY` | Official URLs support citation and the preserved derived summaries, but redistribution permission for source files is not established. Source reuse, label imbalance, portfolio dependence, and absence of a confirmatory comparison family remain. | Descriptive external consistency only. |

Accordingly, this namespace remains `SCAFFOLD_ONLY / DESIGN_NOT_FROZEN /
NO_RESULTS`. None of these decisions authorizes a pilot or formal run, and none
upgrades claim P1-C08.
