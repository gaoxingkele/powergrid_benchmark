# Information current-evidence supplement index

Date: 2026-09-13. This is a new index, not a replacement for the historical
S1--S4 snapshot or its checksum manifest. No public release is asserted.

Current manuscript: `../LaTeX/paper_information.tex`.
SHA-256: `05f0365c484c27aa91e8ca699d0ff4b8801a1ba0415e99264ee983b5eb5b3cda`.

Paths below are relative to `Workspace/03_Reproducibility/`.

| Manuscript evidence | Current artifact | Interpretation boundary |
|---|---|---|
| Canonical fixed-source scores | `Data/canonical_v2/canonical_rows_v2.jsonl` | 1440 retained candidate verdicts, not independent deployment samples |
| Unified selector comparison | `Data/evaluator_audit/run_unified_v1b/unified_evaluator_results.json` | 76/99/100/129; supersedes historical row-only evaluation |
| Order sensitivity | `Data/evaluator_audit/order_sensitivity_unified_v1/order_sensitivity_summary.json` | 40320 global orders, not independent experimental replications |
| Role utilization | `Data/role_ablation/unified_v1/role_ablation_summary.json` | Active scoring components, not five independently contributing agents |
| Failure-stage partition | `Data/selection_failure_decomposition/information_r1/selection_failure_decomposition.json` | Post-result exploratory; 360 question-selector rows |
| Partition reproducible entry | `Code/evaluator_audit/run_selection_failure_decomposition.py` | Requires retained boards and canonical verdicts; refuses an existing output |
| Partition tests | `Code/evaluator_audit/test_selection_failure_decomposition.py` | Stage nesting plus all-row agreement with prior tie audit |
| Current technical check | `Package_Metadata/verify_information.py` | Technical validation only; no submission or publication verdict |

The current main comparison reports finite-pool counts. Appendix A retains
historical question-level intervals and tests with their dependence caveat;
moving them does not create cluster-valid or external evidence.

From any working directory, run Python 3.12 with the absolute path to
`Package_Metadata/verify_information.py`. MiKTeX `pdflatex` and `bibtex` must
be on PATH. Default output is stdout; `--report` accepts only a new path
outside this Workspace. `--skip-latex` explicitly produces a partial check.
The legacy `run_public_verification.py` still targets the historical
Applied Sciences manuscript and is not the current-version readiness gate.

## Still open

- Independently unpacked full current-version package and byte-level manifest.
- Current public tag/release referenced from Data Availability.
- Core selection diagnosis replicated across independent candidate pools.
- Author-controlled final manuscript and submission attestations.

This index does not grant redistribution rights or certify semantic validity.
