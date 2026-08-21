# Current-Release Audit Correction — 2026-08-11

## Finding

The reported inconsistency was real. The current `MA_SQLGrid/paper_applsci.pdf` contains 28 pages and six manuscript figures, whereas the superseded Visual QA described a 20-page/four-figure manuscript. Intermediate reports also described 27-, 30-, or 31-page builds. Those records must not be used for the 2026-08-09 reference-revision release.

The directory also contained copied analysis scripts whose relative paths were bound to their previous workspace locations. In particular, one path ascended four parents and then appended `paper_projects/...` again, while another resolved an experiment directory relative to its new `figures` location. Both failed after relocation.

## Canonical current release

| Paper | PDF pages | Figures used | PDF SHA-256 | Visual QA |
|---|---:|---:|---|---|
| C2GES | 25 | 6 | `CD1B9D0B3684A1BE4C985450A239D2E68607D874AECF7144653344245F8E4F36` | PASS, 25/25 pages inspected |
| MA-SQLGrid | 28 | 6 | `DF19B83D9F1695EDD59909FACDE26295FC8D787775CF166CEAFD5E898EC5539F` | PASS, 28/28 pages inspected |

`CURRENT_RELEASE_MANIFEST.json` is the machine-readable authority for these counts and hashes. Each paper's `VISUAL_QA_MANIFEST.json` binds the page render set and inspection result to the corresponding PDF hash. Each `figures/FIGURE_LINEAGE.json` now contains six entries, matching the six `figure` environments in the active TeX source.

## Corrections made

1. The two active TeX sources and PDFs were designated as the only canonical current manuscripts in `VERSION_BOUNDARY.md`.
2. Superseded root reports, intermediate page-check images, four-figure lineage files, unused architecture renders, and the two workspace-bound MA-SQLGrid scripts were moved without deletion to `_archive_pre_current_audit/`.
3. Portable figure-generation entry points were added or repaired. Active scripts resolve data and outputs from `Path(__file__).resolve()` and local packaged lineage sources rather than from the shell working directory or a former repository depth.
4. Both manuscripts and all six figures per paper were rebuilt. The final LaTeX logs contain no fatal errors, undefined references, or undefined citations.
5. All 53 PDF pages were rendered at 144 dpi and inspected. No blank page, page-edge clipping, missing figure, detached caption, table overflow, or truncated reference block was detected.
6. The active scripts passed Python bytecode compilation, and a search of active Python files found none of the broken legacy path patterns.

## Reproduction and provenance rule

Run the entry points listed in `VERSION_BOUNDARY.md`; they are independent of the caller's current working directory. Files under `_archive_pre_current_audit/` are recoverable provenance only. They may not be cited, packaged, or used to characterize the current PDFs.

Visual QA certifies rendering and layout consistency only. It does not, by itself, certify scientific validity, experimental completeness, or language correctness.
