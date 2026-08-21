# Final Diagnostic Candidate: diagnostic_build_08

Status: **awaiting fresh independent audit**. Development selection and test
evaluation remain prohibited until that audit passes.

## Composition

- Included reports: 27 (12 development, 15 test)
- Candidate sentences: 12,924; no fixed candidate cap
- Source PDFs missing: 0 of 40 manifest entries
- Sentence-level reference overlap at normalized common substring >= 50
  characters: 0
- Reference/candidate page-interval overlap: 0
- Declared extraction pollution instances: 0

`nerc_034_2025_state_of_reliability_report_overview` is the sole conservative
exclusion relative to the retired 28-report build. Its Executive Summary flows
into an unnumbered report-specific section title that the registered general
chapter-heading rule does not recognize. It is recorded as
`missing_executive_summary_end`; no document-specific exception was added.

## SHA-256

- Combined dataset:
  `87F7F7545CE8116E161A88919483B4EEB0ACF7A9C8854981894947C326EDAA15`
- Development dataset:
  `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79`
- Test dataset:
  `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127`
- Builder:
  `817518DF71F16DA05F54E18A5505BD0639201082E5E846142EF74F64F1A1BA38`

## Local verification

- Unit and real-PDF regression tests: 20/20 passed.
- Builder-team structural audit:
  `audits/diagnostic_build_08_structural_audit/diagnostic_audit.json`, status
  `PASS_WITH_ADVISORIES`.
- The advisory is procedural: rights human approval remains pending. It is not
  a license finding and does not authorize redistribution.
- Development role ambiguity audit: 111 positive maximum-score ties, all 111
  abstained (`dominant_role=None`), with zero graph edges incident to an
  ambiguous node.
