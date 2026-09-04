# P3 s4 Experiment Protocol

**Status:** `SCAFFOLD_ONLY / DESIGN_NOT_FROZEN / NO_RESULTS`  
**Purpose:** independent parameter/strategy adaptation identification and action-aligned AC planning validation.  
**Protected predecessor:** existing s3 validation scripts and outputs are read-only.

Before any formal run, freeze the four mechanism arms, backward-compatibility tests, planning-action/cost provenance, public networks, load/DER scenarios, AC limits, seed list, baselines, primary metric/reference rules, comparison family, correction method, failure handling, and output schema. A 3–5-seed pilot is only a pipeline gate and must remain separate from confirmatory results.

No numeric result exists in this namespace at Wave 0.

## Stage-3 implementation disposition

The independent adaptation and action interface is specified in
`../../manuscript/reconstruction_v2/METHOD_IMPLEMENTATION_CONTRACT.md` and
implemented in `../../scripts/p3_s03_method_contract.py`. The four arms,
legacy switch mapping, independent random streams, heritable control state,
phenotype/repair rules, evaluation accounting, and AC pass/fail limits have
unit tests.

The action-aligned pilot remains **NO-GO**: legacy `subnet::kind` coordinates
do not uniquely identify buses, lines, transformers, or switches in a public
validation network, and no evidence-backed capacity/cost registry is present.
The machine-readable disposition is `method_implementation_contract.json`.
No optimizer or power-flow result was generated in this stage.
