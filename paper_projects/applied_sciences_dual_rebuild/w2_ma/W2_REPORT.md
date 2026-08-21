# W2 MA-SQLGrid Zero-Cost Audit

## Outcome

- Configured model environment variables (non-empty): **0** of 14 audited names.
- Local model/runtime commands available: **0** of 6; matching process present: **False**.
- Network probes and paid model calls: **0**.
- Dataset entries inventoried: **7**.
- New deterministic result rows: **360**; paired artifact audit: **PASS**.
- Legacy prediction rows rescored without inference: **1980**.
- Factorial dry-run: **720** cells; shared statistical audit: **PASS**.

## New deterministic baselines

These are explicitly diagnostic, non-confirmatory lower bounds. Generation uses only the 20-question development partition and database lexicons; test gold SQL is used only after prediction for scoring.

| Method | N | Strict execution | Projection contract | Executable | Safe |
|---|---:|---:|---:|---:|---:|
| `DEV_1NN_LITERAL_TRANSFER` | 180 | 0.0111 | 0.3611 | 1.0000 | 1.0000 |
| `DEV_1NN_SQL_COPY` | 180 | 0.0000 | 0.3611 | 1.0000 | 1.0000 |

## Dataset readiness

| Dataset | Present | Files | Size (MB) | Intended role | SQL benchmark readiness | License status |
|---|---|---:|---:|---|---|---|
| `griddb-maintenance-v2-v0.1` | True | 6 | 0.2 | primary in-domain Text-to-SQL benchmark | ready_existing_200_questions_180_test | BLOCKER_missing_explicit_license |
| `griddb-maintenance-v2-x10` | True | 6 | 0.2 | scale and distractor robustness only | ready_existing_queries_but_factorial_symmetry_must_be_enforced | BLOCKER_parent_license_unresolved |
| `rts-gmlc` | True | 206 | 209.4 | external transmission/operations database candidate | source_present_requires_SQL_ETL_questions_and_sealed_split | present_review_notice_before_redistribution |
| `simbench` | True | 165 | 386.1 | external distribution asset/topology database candidate | source_present_requires_SQL_ETL_questions_and_sealed_split | present_attribution_and_share_alike_review_required |
| `matpower-cases` | True | 97 | 74.8 | auxiliary standard-grid schema diversity | case_files_present_requires_parser_SQL_ETL_and_questions | present_review_before_redistribution |
| `pandapower-networks` | True | 87 | 26.2 | auxiliary network-schema diversity | network_files_present_requires_SQL_ETL_and_questions | present |
| `gridstage` | True | 105 | 101.2 | optional fault/PMU extension; lower Text-to-SQL priority | source_present_but_MATLAB_dependent_and_requires_SQL_ETL | present_review_before_redistribution |

## Evidence separation

- `new_deterministic_*` contains newly generated zero-cost predictions.
- `legacy_rescored_*` contains old model outputs evaluated by the current evaluator; no new inference occurred.
- `factorial_*` proves design completeness only and contains no model predictions or accuracy claims.
- None of these artifacts changes manuscript values. The confirmatory 2x2 execution remains pending an explicitly supplied endpoint/model/key.

## Blocking items carried forward

1. No usable configured endpoint or local model runtime was found in this process environment.
2. GridDB-Maintenance-v2 lacks an explicit dataset license in its local dataset directory.
3. RTS-GMLC and SimBench are source datasets, not yet frozen SQL/NL-to-SQL benchmarks.
4. Existing GridDB test questions have already been inspected; a new sealed external split is required for confirmatory claims.
