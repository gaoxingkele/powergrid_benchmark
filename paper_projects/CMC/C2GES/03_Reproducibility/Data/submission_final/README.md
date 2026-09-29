# C2GES submission evidence locks

Two scientific routes are kept separate.

## Diagnostic route (current)

The current manuscript is a bounded diagnostic study. Run:

```text
python 03_Reproducibility/Code/prospective_v1/diagnostic_submission_readiness.py
```

Its final lock is `DIAGNOSTIC_SUBMISSION_EVIDENCE_LOCK.json`. This route accepts
only explicitly post-access exploratory results and automated error-discovery
labels. It requires the manuscript to disclaim confirmatory superiority,
human validation, semantic construct validity, and operational benefit. The
item-level disposition of the former 42 findings is stored in
`CONFIRMATORY_42_FINDINGS_DISPOSITION.json`.

The authoritative scope resolution is
`CURRENT_SUBMISSION_REQUIREMENTS_RESOLUTION.json`. It distinguishes current
submission requirements from optional future claim upgrades. When that record
states `CURRENT_SUBMISSION_REQUIREMENTS_RESOLVED` and `current_required_open=0`,
the unfinished confirmatory E1/E2 files are not current submission blockers;
they become mandatory only if the title or claims are upgraded. Author portal
attestation remains a manual submission step and is not fabricated by the package.

## Confirmatory route (future)

The confirmatory package remains intentionally incomplete.
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
