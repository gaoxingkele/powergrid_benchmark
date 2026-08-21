# C2GES Applied Sciences W7 Assembly

This is a new, isolated MDPI *Applied Sciences* manuscript. It does not overwrite the earlier CMC or preliminary Applied Sciences drafts.

## Build

```powershell
.\build.ps1
```

The build first regenerates every empirical number and result table from the frozen W6/W4 CSV/JSON artifacts, verifies source hashes, front-matter boundaries, citations, figures, and prohibited claims, then compiles with the official local MDPI class.

## Submission metadata

The authors, affiliations, correspondence address, CRediT roles, funding grant
521300250006, conflicts statement, ethics wording, acknowledgments, public
project repository, and generative-AI declaration are populated in the current
manuscript. Third-party source materials are provided to editors and reviewers
on reasonable request, subject to the applicable permissions and licenses.

## Evidence boundary

- Canonical quantitative source: `workspace/w6_c2_canonical_v2` only.
- Oracle-label is conditional and not end-to-end.
- Role-conditioning and blanket BM25 superiority are frozen NO-GO claims.
- NERC silver annotations are qualitative/application-design material only.
