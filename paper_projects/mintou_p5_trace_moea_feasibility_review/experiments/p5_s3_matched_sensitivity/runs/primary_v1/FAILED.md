## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run
- Verification Status: UNVERIFIED
- Version Label: p5_s3_primary_v1_failed

## Failed pre-run attempt

The process stopped before candidate construction and before any optimizer or
metric execution. The isolated harness checkout does not include the public-data
cache at the shared module's checkout-relative path, producing a
`FileNotFoundError` for RTS-GMLC `gen.csv`.

The documented read-only cache binding was added to `config.json` as a path-only
prespecification amendment. No scientific parameter or observed result was
available when that amendment was made. This directory is retained as a failed
attempt and is not used as evidence.
