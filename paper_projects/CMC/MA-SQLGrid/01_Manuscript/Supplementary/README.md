# MA-SQLGrid Supplementary Verification Set

This directory is a manuscript-bound, rights-safe subset of the retained
MA-SQLGrid evidence. It separates implementation tests, version chronology,
numerical evidence, and rights information from the scientific narrative.

- `S1_software/`: executor test report and independent executor audit.
- `S2_protocols/`: supersession records, historical-pool retrospective
  manifest, and independent release-v3 audit.
- `S3_numerical/`: complete R3 numerical tables in Markdown and JSON.
- `S4_rights/`: item-level rights and redistribution inventory.
- S5 release verification is stored one directory above in the current Visual
  QA files, revision ledger, and release manifest.

The files in S1--S4 preserve the historical v3 evidence snapshot. Their
SHA-256 values are recorded in `SUPPLEMENT_MANIFEST.json`. Current post-review
unified-evaluator, order, role-ablation, and automated error-taxonomy records
are under `03_Reproducibility/Data/` and supersede the historical row-only
counts for the current manuscript.

The supplement must not be read as evidence that later executor hardening
generated the historical row-only 80/100/101 values. Under the current frozen
shape-and-denotation evaluator the corresponding counts are 76/99/100, and the
best fixed source is 129/180. Restricted third-party source records are
intentionally absent.
