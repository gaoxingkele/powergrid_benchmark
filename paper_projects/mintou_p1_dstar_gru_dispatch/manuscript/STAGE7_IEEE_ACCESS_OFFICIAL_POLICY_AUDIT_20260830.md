# IEEE Access official-policy audit — 2026-08-30

## Authority and scope

This audit uses only current first-party IEEE/IEEE Access pages. It separates initial-submission requirements from post-acceptance final-file requirements and does not treat a local workflow preference as a journal rule.

Primary sources:

- [IEEE Access Submission Guidelines](https://ieeeaccess.ieee.org/authors/submission-guidelines/)
- [IEEE Access Preparing Your Article](https://ieeeaccess.ieee.org/authors/preparing-your-article/)
- [IEEE Access Post Acceptance Guide](https://ieeeaccess.ieee.org/authors/post-acceptance-guide/)
- [IEEE Author Center: Tools for IEEE Authors](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/tools-for-ieee-authors/)

## Requirements mapped to the P1 gates

| Official requirement | P1 implementation | Status before human input |
|---|---|---|
| Required IEEE Access double-column, single-spaced template | `manuscript/journal_submission/paper.tex` uses the dedicated source tree; LaTeX compilation remains mandatory. | PASS at Stage 6; must be re-proved for Stage 7. |
| Source file and PDF are both required and their contents must match; each file must stay below 40 MB | Stage 7 packages exact TeX/PDF source bytes and terminally checks byte/semantic identity. A file-size gate is included in the Stage 7 terminal validator. | BLOCKED until human-complete build. |
| All authors must appear in both source and PDF | Human metadata gate checks the confirmed ordered author list against Markdown, TeX, and packaged TeX; the compiled PDF placeholder scan prevents a placeholder release. | BLOCKED: names/order absent. |
| Submitting author's account must have a public, populated ORCID | Manuscript display remains exactly `ORCID(s): NONE` by author instruction, while `orcid.submitting_account` is independently checksum-validated and requires explicit confirmation that the profile is public and populated. | BLOCKED: account ORCID absent. |
| Short biography required for every author at submission | Human metadata gate requires one confirmed biography per author in manuscript and TeX. | BLOCKED: authors/biographies absent. |
| Author photographs are required in post-acceptance final files | The publication-ready Stage 7 gate rejects bundled sample portraits and requires one real photo per author. This is intentionally stronger than the initial-submission minimum because the requested deliverable is a complete final package. | BLOCKED: real photos absent. |
| AI-generated text must be disclosed in the Acknowledgment; grammar-only assistance has separate guidance | Human ledger requires a confirmed, rendered AI-use statement and acknowledgment. | BLOCKED: author confirmation absent. |
| References must be relevant, accurate, and not retracted | Citation/reference verification remains a mandatory final integrity/Harness gate; finalizer engineering alone cannot prove it. | Must be rerun after final text. |
| No concurrent submission | Human ledger requires explicit concurrent/prior-submission yes/no declarations. | BLOCKED: declaration absent. |
| Select 3–10 accurate keywords in the submission system | Current manuscript carries seven Index Terms; terminal review must confirm extraction and final system entry. | Manuscript count PASS; system entry remains human action. |
| No hard page limit; under 20 pages is strongly recommended | Stage 7 reproducible-build gate accepts only 1–19 pages without an EIC pre-submission exception. | Stage 6 has 9 pages; Stage 7 must be re-counted after biographies. |
| Experiments/statistics must meet a high technical standard; conclusions must be supported; scope, English, and prior work must be adequate | Covered by the accepted Stage 6 scientific record and the required fresh Stage 7 integrity/reviewer/Harness gates. | Stage 6 PASS; final human-complete text still requires re-review. |
| Supplementary code/data may be submitted; a public repository or archival DOI is not stated as mandatory | The ledger now requires an explicit availability mode: `public`, `submission_supplement`, or `not_public`, plus a truthful rendered statement. URL/DOI is mandatory only when `public` is claimed. | BLOCKED: author choice absent. |

## Gate correction made by this audit

The earlier P1 ledger required a public HTTPS repository or archival DOI in every case. The current official submission instructions allow supplementary material and do not make a public repository/DOI an unconditional submission requirement. The gate was therefore corrected to require an explicit, truthful availability decision instead of forcing a public-release claim.

No authorship, ORCID, funding, contribution, conflict, repository, ethics, APC, or submission fact was inferred during this audit.
