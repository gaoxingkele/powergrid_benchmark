# Portability and Reproduction

The current public verifier resolves paths from its own location and can be launched from any working directory. It checks manuscript assets and citations, core derived-data denominators, unified-evaluator counts, exact order sensitivity, normalized unique-SQL diagnostics, role ablations, the automated error taxonomy, BIRD aggregates, 35 public framework/executor tests, and a clean temporary LaTeX build.

```text
python paper_projects/CMC/MA-SQLGrid/03_Reproducibility/Code/run_public_verification.py
```

Use `--skip-latex` for code/data checks only. Use `--submission` to enforce author/external gates; it is expected to return `PENDING_EXTERNAL_GATES` until those gates are genuinely closed.

Raw GridDB SQLite/questions, raw state databases, third-party BIRD databases, and model-generation inputs are excluded under the recorded rights boundaries. Historical build scripts and provenance manifests may retain original source-workspace locations; the portable verifier does not treat those provenance strings as live paths. The BIRD formal generation runtime remains Python 3.10.11/SQLite 3.40.1; the current portable audit runs under the supplied Python 3.12 environment and does not regenerate model outputs.
