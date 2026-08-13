# P5 S3 matched-output and sensitivity experiment

This stage-local package consumes the existing public-data candidate builder and
registered P5/P6 project-review implementation without modifying shared source.
The frozen design is in `config.json`. Its three output families are written to
new directories beneath an explicitly supplied output root:

- `matched_compromise/`: the preserved one-compromise-per-run readout, with
  deterministic provenance duplicates collapsed to one unique output;
- `normalization/`: bound vectors, clipping incidence, and hypervolume under the
  reported, unclipped, expanded, analytic, and alternative-reference schemes;
- `sensitivity/`: a one-factor-at-a-time formulation/preference scan around the
  registered TRACE-MOEA setup.

The main experiment uses 30 seeded runs per stochastic method-scenario and one
unique output per deterministic method-scenario. The sensitivity scan also uses
30 seeds per cell. No public-record backtest is promoted beyond descriptive
scope, and the script emits no p-values.

The preserved comparator rows were generated with recorded `pymoo==0.6.2`.
This host cannot rerun that package's `moocore` dependency under a single
compatible Python/CFFI ABI, so no different pymoo version is substituted. New
front-level recomputations cover the shared TRACE engine, its
NoPreferenceRanking MOEA control, and deterministic rules. The stage-local
SciPy compatibility surface supplies only import-time distance/binomial calls;
statistical entry points fail closed. Hypervolume is computed by an isolated
pure-Python Fonseca dimension-sweep helper, and the legacy-reproduction table
checks agreement with preserved custom-engine/deterministic metrics.

The evidence-of-record run is `runs/primary_v4/`; `runs/reproduction_v1/` is
the independent same-seed reproduction, and `runs/VALIDATION.md` records the
artifact comparison. The earlier directories are retained as failed or
superseded pre-result history and must not be used as the final result.

Example in a healthy environment where the repository package and dependencies
are installed:

```powershell
python experiments/p5_s3_matched_sensitivity/run_experiments.py `
  --config experiments/p5_s3_matched_sensitivity/config.json `
  --output-root experiments/p5_s3_matched_sensitivity/runs/new_reproduction
```

Run directories are immutable inputs to later reporting: the script refuses to
write into an existing output root.
