# Clean-Unpack Validation Incidents

This register preserves all validation attempts; none was overwritten or used selectively.

- The first extraction attempt under `packages/clean_unpack_validation_01` stopped before verification because the nested target exceeded the Windows path-length limit. The partial directory is retained locally and is excluded from the editor package.
- The first complete short-path run at `.c2ges_clean_unpack_01` reproduced the source set, calibration checks, figures, citations, compilation, text, page count, and rendered pages. It was conservatively recorded as failed because the raw PDF SHA-256 differed across absolute build paths.
- The fresh short-path run at `.c2ges_clean_unpack_02` used the documented acceptance rule for path-dependent PDF identifiers: raw-hash equality when available, otherwise identical byte length, extracted text, and all 14 rendered page pixels. It passed every required check. Its authoritative machine-readable record is `CLEAN_UNPACK_RECEIPT.json`.

The raw-PDF-hash exception is limited to reproducible path-dependent PDF metadata. It does not permit differences in manuscript text, page count, rendered content, figures, tables, or cited references.
