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

Paths inside historical manifests identify the original workspace layout. The
top-level `FILE_SHA256SUMS.txt` verifies the portable package contents.
