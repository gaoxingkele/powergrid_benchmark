# C2GES Protocol-Ready Upgrade

Date: 2026-09-05  
Target: MDPI *Applied Sciences*  
Status: `PROTOCOL_READY / EXPERIMENTS_NOT_EXECUTED / NOT_SUBMISSION_READY`

## Baseline identity

- Plan-declared SHA-256: `224BCAC8E903882FB46CD0B5144E29B7726E1937EA81124C8202EDE35E1187E0` (not found in the current repository or available history).
- Active manuscript used for this upgrade: `01_Manuscript/LaTeX/paper_applsci.tex`.
- Pre-upgrade active-manuscript SHA-256: `998917E9AD77B563567A4DDA071680390F9D5B0D390A1E0CC4271E79807FC04B`.
- The active manuscript is later than the plan-declared state and was not rolled back.

## Completed in this version

1. Added a manuscript-level prospective protocol for layout-aware, matched-word, balanced-tuning external-series evaluation.
2. Added clean AB-0--AB-6, RP-00--RP-11, and G-U/G-T component definitions and separated their multiplicity families.
3. Added a blinded two-annotator structural-validity protocol and explicit ethics/exemption gate.
4. Reclassified all current 15-report results as historical/retained-test evidence.
5. Added portable marker-based release discovery and non-mutating/default-temporary verification behavior.

## Still required before submission

- Freeze a rights-cleared unseen external-series inventory and immutable code/configuration revision.
- Complete layout-boundary audit before opening external outcomes.
- Execute E1 and E3 once under the frozen protocol.
- Recruit qualified annotators, obtain the required ethics/exemption determination, and execute E2 independently before adjudication.
- Backfill only measured results into Abstract, Results, Discussion, Conclusions, figures, supplementary tables, and manifests.
- Re-run clean ZIP verification and page-by-page PDF QA.

No prospective or human-validation result is asserted in this upgrade.

## 2026-09-06 implementation checkpoint

- Added a development-only E3 runner implementing all 13 AB/RP/G conditions at
  110 and 260 words with within-condition positive-weight renormalization.
- Corrected the G-U/G-T control so both variants use the same lexical-overlap
  calculation; only the role-transition typing gate differs.
- Completed immutable `run_2`: 12 development reports, 6 series, 312/312 rows
  passed, no budget violations, and all three expected configuration identities
  held at selection level.
- Added a non-mutating run validator and integrated both the prospective unit
  tests and `run_2` integrity check into the public verifier.
- Public verification, including clean temporary LaTeX builds, remains `PASS`.

This checkpoint verifies implementation only. It does not change the manuscript's
`NOT_SUBMISSION_READY` status and no pilot estimate is promoted to a confirmatory
claim.

### Layout and comparator follow-up

- Added layout-builder v2 with typed units, table isolation, deterministic
  source locators, tokenizer lengths, conservative cross-boundary repair, and a
  244-row risk-enriched human-audit frame. Private text remains outside release.
- Verified 3,782 development candidates mechanically; candidate-quality gates
  remain pending two independent human reviewers.
- Identified PacSum from ACL Anthology P19-1628. Because upstream revision
  `67cc8ad370eac160ede997b7c32eb74907728bf8` contains no license file, no upstream
  code was copied. A paper-equation-based PacSum-MiniLM clean-room scorer and
  nine-configuration grid were added and unit-tested.

### Human-validation execution follow-up

- Separated the administrator-only sampling manifest from blinded annotator
  forms; system condition, automated role, confidence, and agreement strata are
  not present in either annotator packet.
- Added `human_validation.py` with three fail-closed stages: packet preparation,
  pre-adjudication agreement/hash freeze, and exact-disagreement adjudication plus
  final analysis.
- Added series-equal bootstrap intervals, role confusion/macro metrics,
  edge/path/faithfulness rates, and explicit claim-gate decisions. Undefined
  kappa values cannot pass a gate.
- Added tests for information leakage, missing labels, changed frozen inputs,
  incomplete adjudication, known kappa values, and successful artifact creation;
  all 18 prospective tests pass.

No human was recruited and no annotation outcome was generated. E2 remains an
external evidence gate, not a completed experiment.

The manuscript was synchronized with this implementation: it now distinguishes
200 boundary judgments from 200 role judgments, documents the SHA-256 stage lock
and exact-disagreement rule, names the controlled comparator as PacSum-MiniLM,
and cites its verified ACL 2019 method paper. Active manuscript SHA-256 after
this synchronization is
`7591320D3463BD98C5FC951C53A896DAFAF482B8656854228357C54869A53E4C`.

The synchronized PDF compiled to 24 pages and passed a complete Poppler-rendered
visual review; the PDF SHA-256 is
`CF2BA0BE1DD26CF0C2E56C484E58A985927F0E46BD418A10AAAE95D20535371B`.

### Portable release verification follow-up

- Staged a test archive from the exact 225-file checksum allowlist rather than
  recursively packaging the worktree.
- Confirmed that the extracted release contains no `.git` entry and excludes
  archive, build-intermediate, bytecode, rendered-QA, restricted-source, and
  verbatim-derived material.
- In the clean extracted directory, Python 3.12.10 completed all seven public
  verification commands with zero failures and three documented restricted-
  input skips; clean LaTeX builds produced 24 main-text pages and two supplement
  pages.
- Manifest validation passed before and after execution with zero missing,
  mismatch, or unlisted files; checksum-list and release-manifest bytes were
  unchanged.

Release repair R1 is closed for this snapshot. Scientific gates E1, E2, and the
confirmatory E3 run remain open.

### Integrity and figure-lineage follow-up

- Verified the current 35-entry bibliography with a 34-entry cached audit plus
  an official ACL Anthology identity/method check for the new PacSum citation;
  no dangling, orphan, or ghost reference was found.
- Restored the rights-safe independent post-run audit to the release tree and
  removed Figure 6's hard-coded scientific values. The generator now reads and
  validates the historical audit and the development calibration decision.
- Expanded machine-readable figure lineage from 3/6 to 6/6 figures. Twenty-nine
  registered input, script, and output hashes match, and all six manuscript PDF
  figures are byte-identical to their reproducibility counterparts.
- Rebuilt the 24-page manuscript. Citation/figure/reference validation passed;
  the log contains no undefined reference, undefined citation, or overfull box.
  The rebuilt PDF SHA-256 is
  `B827ABDE60E19CF47130A5CD18802882125262F72F7CF663556B1FAD38A1B0C0`.
- Added explicit integrity and figure/table audit records. Their verdict is
  `PASS_FOR_PROTOCOL_SNAPSHOT / FAIL_FOR_SUBMISSION_FINALIZATION` because E1,
  E2, and confirmatory E3 remain unexecuted.
- Rebuilt the updated 231-file public ZIP and re-ran the manifest and public
  verifier from a `.git`-free extracted root. Both checks passed before and
  after execution with zero missing, mismatched, or unlisted files, and the
  checksum list and manifest remained byte-stable.

### Live venue and immutable-release follow-up

- Rechecked the current official Applied Sciences scope, Computing and
  Artificial Intelligence Section, abstract/data/GenAI rules, and APC page.
  The venue fit is medium in the present evidence state and becomes strong only
  after E1--E3 support the application and structure claims.
- Replaced the stale `cmc-2026-08-24-v3` Data Availability target with the
  version-specific protocol tag `c2ges-2026-09-06-protocol-ready-v1`. This tag
  must remain distinct from the later submission-final tag.
- Added a live-requirements matrix and a severity-calibrated pre-submission
  review. Two scientific CRITICAL findings remain: E1/E2/E3 are unexecuted, and
  the title's structure-aware claim remains conditional on E2/E3.
- Removed two AI-tone uses of “reveal” and corrected the PacSum BibTeX
  `booktitle` so the MDPI style no longer renders “Proceedings of the
  Proceedings of”. The resulting 24-page PDF SHA-256 is
  `4CE48AD0BB3E608E125F1A8496A3D224B36812D74AA095744E798C5A85BB6BB7`.
