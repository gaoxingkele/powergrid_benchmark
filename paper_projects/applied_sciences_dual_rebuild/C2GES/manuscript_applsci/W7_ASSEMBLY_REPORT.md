# W7 C2GES Applied Sciences Assembly Report

> Current-status addendum (2026-08-06): this report preserves the historical W7
> assembly snapshot below. The authoritative current manuscript is 22 pages,
> with author names, affiliations and correspondence migrated from the paired
> CMC manuscript. Current build and bundle identities are recorded in
> `../../DETERMINISTIC_BUILD_AUDIT.json` and
> `../reviews/round3_author_metadata_closure.json`.

## Outcome

- New isolated manuscript created; no earlier CMC or preliminary Applied Sciences manuscript was overwritten.
- Frozen title: **C2GES: Interpretable Extractive Evidence Selection for Power Grid Reliability Reports**.
- Official local MDPI `Definitions` reused with the `applsci` class option.
- Three accepted framework figures and five canonical W6 result figures embedded.
- PDF builds successfully through the scripted `pdflatex`/`bibtex` fallback.

## Size

- PDF: 18 A4 pages, 704,100 bytes.
- Extracted PDF text: 8,312 whitespace-delimited words, including references, table text, headers, and declarations.
- Main TeX source: 5,857 whitespace-delimited tokens, including commands and front matter.
- Structure: Introduction; Related Work; Materials and Methods; Results; Discussion; Conclusions; required MDPI declarations.

## Evidence Controls

- All empirical manuscript values and result tables are generated from frozen CSV/JSON artifacts.
- Verifier result: PASS for 11 source hashes, 6 generated TeX fragments, 8 figures, and 23 cited bibliography keys.
- Final LaTeX log audit: no undefined citations/references, overfull boxes, fatal errors, or undefined commands.
- Canonical boundaries retained: role-conditioning primary claim NO-GO; blanket superiority over BM25 NO-GO; oracle conditional and non-end-to-end; NERC silver labels excluded from quantitative claims.

## Required Human Input

All fields marked `W7_FRONT_MATTER` remain submission blockers: author names, affiliations and e-mails, corresponding author, CRediT roles, funding and grant identifiers, conflicts of interest, ethics wording confirmation, acknowledgments, permanent repository DOI/license, and author-approved generative-AI disclosure.

## Build

Run `./build.ps1`. The script regenerates canonical TeX, verifies claim/source integrity, and compiles. `latexmk` is skipped on the current machine because Perl is unavailable; the automatic `pdflatex`/`bibtex` fallback succeeds. MiKTeX prints its local update reminder, which is an environment notice rather than a manuscript error.
