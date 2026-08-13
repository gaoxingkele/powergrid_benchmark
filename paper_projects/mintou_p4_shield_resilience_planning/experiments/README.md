# P4 Stage-3 Boundary Experiment

`p4_s3_boundary_predeclared.json` fixes the matrix before execution. The local
runner freezes the 18 SimBench subnet statistics sufficient for the reconciled
p4 candidate equations and then writes new run-level evidence without changing
the shared p3/p4 planning code or any historical archive.

The matrix varies one factor at a time: budget factor, scenario count (with
`K=|S|/4`), and the selected-action term in the survivability proxy. It runs
SHIELD-MOEA, NSGA-II with final-population repair, GA-only, DE-only, and
fixed-worst-K controls for 30 independent method-specific seeds per setting.
Every raw front is scored three ways: the primary clipped fixed-bound HV at
reference 1.1, an unclipped audit at 1.1, and clipped HV at the predeclared
alternative reference 1.2.

The runner refuses to overwrite outputs. Verify the completed package with:

```powershell
python experiments/p4_boundary_experiments.py verify
```

The manifest under `evidence/manifests/` records hashes and environment details.
