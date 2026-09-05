# C2GES submission-final evidence lock

This directory remains intentionally incomplete in the protocol-ready release.
It is populated only after confirmatory E1 and E3 have finished, independent E2
annotation and adjudication are complete, the manuscript has been backfilled
from those measured results, and the final PDF has been rebuilt.

Run the fail-closed readiness gate from the C2GES root:

```text
python 03_Reproducibility/Code/prospective_v1/submission_readiness.py
```

A final release may proceed only when the command exits with code 0 and reports
`status: READY`. Development pilots, placeholder files, hand-edited gate labels,
or a manuscript that still promises future E1--E3 work cannot satisfy the gate.

The final `SUBMISSION_EVIDENCE_LOCK.json` must use this minimal shape:

```json
{
  "status": "SUBMISSION_FINAL",
  "git_commit": "<40-hex commit id>",
  "git_tag": "c2ges-<date>-submission-final-v1",
  "sha256": {
    "01_Manuscript/LaTeX/paper_applsci.tex": "<SHA-256>",
    "01_Manuscript/PDF/<submission-final-pdf>.pdf": "<SHA-256>",
    "02_Revision_and_QA/04_Build_Reports/C2GES_PUBLIC_VERIFICATION.json": "<SHA-256>",
    "03_Reproducibility/Data/prospective_external_v1/EXTERNAL_PROTOCOL_FREEZE.json": "<SHA-256>",
    "03_Reproducibility/Data/component_factorial_v1/FACTORIAL_PROTOCOL.json": "<SHA-256>",
    "<every required E1/E2/E3 result and every additional artifact used by a table, figure, or claim>": "<SHA-256>"
  }
}
```

The lock is an integrity record, not an author attestation and not a substitute
for institutional ethics review, data rights, or scientific interpretation.
