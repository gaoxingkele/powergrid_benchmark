# Code Map

- `framework/`: five-role coordination, read-only execution, historical-pool
  selection, witness construction, and replay diagnostics.
- `final_executor/`: later executor revision and its focused regression tests.
- `canonical_v2/`: canonical rescoring and analysis code.
- `inference_hierarchy/`: finite-corpus and composition-sensitivity analysis.
- `component/`: component-effect release builder and tests.
- `constructed_state/`: state construction, scoring, analysis, exact sign
  enumeration, and tests.
- `bird_protocol/`: frozen BIRD v1.1 protocol, run harness, audit scripts, and
  runtime-identity records. Formal execution used Python 3.10.11 and SQLite
  3.40.1; it must not be represented as re-certified under a different runtime.
- `evaluator_audit/`: unified evaluator reconciliation, exact 40,320-order and
  unique-SQL audit, role-utilization diagnostics, and automated error taxonomy.
- `run_public_verification.py`: project-relative entry point for the current
  portable technical verification and clean LaTeX build.

Paths inside historical manifests identify the original workspace layout. The
current checksum list is in `../Package_Metadata/FILE_SHA256SUMS.txt`. Create
the Python 3.12 audit environment from `environment-py312.yml` or install
`requirements-py312.txt`.
