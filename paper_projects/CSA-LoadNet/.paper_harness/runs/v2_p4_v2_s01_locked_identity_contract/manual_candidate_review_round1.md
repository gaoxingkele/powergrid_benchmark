# P4 Stage-1 Candidate Review — Round 1

## Scope and provenance

- Target: `Electronics`.
- Locked title: `Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting`.
- Initial candidate commit: `15a5d9b7`.
- Review-fix commit: `038faade7b29b02845076639111669c7f9080840`.
- Build-evidence update: `534e528d4db93d8bdcbd529bd2951b805053e731`.
- This review covers the Stage-1 identity and claim contract. It is not an acceptance of the future GCN/HGCN method, unrun experiments, stale PDFs, or the full paper for submission.

## Reviewer verdict on the candidate delta

- Candidate-introduced CRITICAL issues after the review fix: **0**.
- Candidate-introduced MAJOR issues after the review fix: **0**.
- Candidate-introduced MINOR issues after the review fix: **0**.
- Stage quality: **9/10**. Recommendation: accept Stage 1 and continue the planned scientific reconstruction.
- Full-manuscript submission readiness: **not ready**.

## 1. Macro logic and scientific claim control

- The exact locked title and exact author order are present in the Markdown and both TeX sources.
- Zheng Jieyun is locked as first and corresponding author; the shared affiliation and correspondence address match the author-provided record.
- The contract correctly identifies CSA-LoadNet as the existing baseline, not a GCN or HGCN.
- P4-C02 and P4-C03 remain `NOT_SUPPORTED`, P4-C04 remains `UNRESOLVED`, and P4-C06/P4-C07 remain future hypotheses. The review fix changed P4-C06 from a present-tense experimental claim to a prospective protocol statement.
- The DLinear adverse result and the null matched-context comparisons are retained. No GCN/HGCN result is introduced or implied.
- The full manuscript remains CRITICAL for submission until the project implements and evaluates a leakage-free graph construction, a Euclidean GCN sanity baseline, a genuine HGCN, and orthogonal graph-versus-geometry controls.

## 2. Quantitative evidence audit

- `CSA-Poincare-Shared`: mean block-level MAPE `0.0366404835`; WAPE `0.0367754537`.
- `TargetSelfContext-Matched`: mean block-level MAPE `0.0368937083`; WAPE `0.0371092741`.
- Paired MAPE difference: `-0.0002532248`; relative difference `-0.686363%`; interval `[-0.0006688492, 0.0002315019]`; exact p = `0.328125`; Holm p = `0.984375`; 6 of 8 blocks favor CSA.
- The exact-hierarchy comparison remains adverse: DLinear OLS `0.280466` versus CSA OLS `0.289488`, so CSA is `3.22%` higher; reported Holm p = `0.000985`.
- These values support bounded negative/null wording only. They do not support a superiority, GCN, or HGCN claim.

## 3. Writing and grammar review

- The initial candidate unnecessarily requested another identity verification after the user had already supplied the authoritative record; the review fix locks that record and leaves only CRediT/final-author approval as separate human gates.
- The ambiguous abstract phrase `neither difference separates` was replaced consistently with `neither contrast is statistically distinguishable from zero`.
- No new G1–G5 grammar defect remains in the candidate delta.
- The canonical abstract is 212 words against the configured 220-word limit.
- Full-text scan found no Unicode em dash. Existing terms requiring later prose review are `yet` (2 uses) and `yielding` (2 uses). The only `innovative` hit is inside a bibliography title; seven `superior*` hits occur in bounded or negative contexts.

## 4. LaTeX, citations, figures, and PDF status

- Source-level identity is exact in the canonical journal TeX and submission-preview TeX.
- Citation-key accounting is internally closed at 30 cited keys and 30 bibliography items, with no unresolved citation key. Item-level bibliographic and novelty verification remains a Stage-2 gate.
- Downstream LaTeX cleanup remains MAJOR: 39 of 39 citation commands lack the nonbreaking-space convention and 28 of 48 labels contain a hyphen or space.
- Eight raster figures are referenced and all eight have PDF counterparts. Final source should switch to the verified vector versions.
- The checked-in PDFs are stale and retain earlier titles/metadata. An isolated three-pass `pdflatex` build of the canonical source now succeeds as a 25-page A4 PDF with the locked title and author metadata and no undefined citations or references. `latexmk` alone remains unavailable because Perl is missing. The checked-in PDFs are therefore still not candidate evidence and must be regenerated from the final accepted source, replaced, rendered, and visually inspected before submission.

## 5. Reproducibility checks

- Reconstruction-v2 contract: PASS.
- `tests/test_mintou_reconstruction_v2_acceptance.py`: 4/4 PASS.
- Narrative structure: PASS; abstract 212/220 words.
- Manuscript hygiene: PASS.
- `git diff --check`: PASS.
- Isolated canonical-source build: PASS; three `pdflatex` passes, 25 A4 pages, no undefined citations or references. Remaining log findings are layout/style warnings, led by one 18.10 pt overfull box and template `fancyhdr` warnings.
- Candidate worktree after review-fix commit: clean.

## Acceptance recommendation

Accept the Stage-1 identity/claim contract only. This permits Stage 2 to begin after explicit human acceptance. It does not approve the manuscript for submission and does not authorize replacing missing experiments with prose.

## Supplemental compilation/style audit

- Three-pass `pdflatex`: PASS; 25 A4 pages; zero undefined citations/references.
- Build log: one overfull box; maximum approximately 18.10 pt.
- Raw ChkTeX findings: 247 total, comprising 156 before the bibliography and 91 in bibliography formatting. The dominant body signals are dash-length warnings (50), missing nonbreaking citation spaces (39), bracket warnings (25), and intersentence-spacing warnings (17).
- ChkTeX counts are triage signals, not automatically confirmed defects; template macros, mathematics, and literal bibliographic titles require manual adjudication during the final LaTeX pass.
