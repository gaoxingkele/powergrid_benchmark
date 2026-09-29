# Round 3 consultation review — partial completion

2026-09-13. Same-agent review, not independent peer review or an editorial verdict.

Current source SHA: `05f0365c484c27aa91e8ca699d0ff4b8801a1ba0415e99264ee983b5eb5b3cda`.
Current retained PDF SHA: `7d7c3a5c1d7a14ff9a17fb7e032c9a8fa8a92b566c9cee4011c915b8fb657876`.

## Verified improvements

1. Main historical-pool table now gives counts, differences and rescue/harm;
   the full original numerical rows survive in Appendix A, Table A1. Method
   text explicitly states why question-level tests do not protect against
   shared-SQL-structure dependence. This closes the presentation mismatch,
   not the external-validity gap.
2. All 30 pages were inspected through contact sheets before the final
   appendix-counter correction. Final pages 6, 14, 15, 18, 27 and 28 were
   inspected at higher resolution. Only pages 14, 15, 27 and 28 changed in
   the final PNG comparison; all four have been inspected. No clipping or
   overlap found within this visual scope. This is not a line-by-line
   semantic or citation-truth certification.
3. New `verify_information.py` selects the Information manuscript, reads
   both declared bibliographies, validates labels/figure files, checks
   retained data and the 360-row partition, and builds in a temporary folder.
   It does not reuse legacy author/readiness conclusions or overwrite the
   historical report. No report is written unless explicitly requested.
4. Python 3.12.10 run: framework 21 tests PASS, executor 14 PASS, partition
   3 PASS. Clean pdflatex/bibtex/pdflatex/pdflatex build PASS, 30 pages;
   39 cited keys, 6 figures, 14 table environments including Appendix A.
   Source SHA remained unchanged. Temporary PDF hash differs because the
   build is not byte-reproducible across timestamps; it is not substituted
   for the retained PDF identity.
5. New supplement index distinguishes current evidence from historical
   S1--S4 and maps main claims to actual paths.

## Remaining findings

- Major: core selection diagnosis remains a single development-visible
  synthetic database case; BIRD generation experiments do not close it.
- Major: current complete independently unpacked package, manifest and public
  release binding remain unfinished. The old verifier targets another paper
  version and its `submission_ready` value cannot certify this manuscript.
- Major: basic propositions organize diagnosis but do not themselves establish
  a novel general theory. Contribution sufficiency remains an author/editor
  judgment requiring more than software tests.
- Author gate: no new author approval or editorial acceptance was obtained.

Round 3 has substantive revision and review evidence, but its planned complete
release validation is still open. Do not count this as a fully closed third
round or label the manuscript publication-ready.
