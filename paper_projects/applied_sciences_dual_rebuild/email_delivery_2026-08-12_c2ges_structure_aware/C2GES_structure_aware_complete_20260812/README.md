# C2GES Applied Sciences Complete Package (2026-08-12)

Manuscript title:

**C2GES: Structure-Aware Extractive Summarization of Long Power-System Technical Reports with Typed-Path Graphs**

This clean package contains the current manuscript PDF and MDPI LaTeX source, the six figures used by the paper (including vector sources where available), the formal v0.3.1 algorithm snapshot and regression tests, distributable non-verbatim experimental results, and the supplementary materials.

## Directory map

- `01_Manuscript_PDF/`: submission PDF.
- `02_LaTeX_Source/`: MDPI LaTeX source, bibliography, class resources, and the six figure PDFs referenced by the manuscript.
- `03_Figures/`: publication figures in PDF/SVG/PNG formats and the current figure-lineage note.
- `04_Experiment_Code/`: formal algorithm, runner, tests, development-only calibration, sensitivity analysis, and figure-generation code.
- `05_Experimental_Data/`: rights-safe metadata, aggregate and paired results, output-length diagnostics, page locators, exact sign-flip results, and the predefined formal configuration.
- `06_Supplementary/`: supplementary PDF and LaTeX source.
- `07_Revision_and_QA/`: narrative-revision summary and current visual-QA records.

## Verified release facts

- Main manuscript: 20 A4 pages and 6 figures.
- Supplementary materials: 2 A4 pages.
- Main results: 15 retained test reports, 7 conditions, and sentence budgets K=5 and K=10.
- Formal code lineage: C2GES-NERC-FORMAL-v0.3.1.
- The package preserves the original source hierarchy required by the formal Python imports.

`FILE_SHA256SUMS.txt` records file-level SHA-256 values. `RELEASE_MANIFEST.json` records the release-level validation results.

## Data-rights boundary

The source NERC PDFs and derived sentence-level verbatim corpora are not redistributed because third-party redistribution permission has not been established. The package includes the non-verbatim statistics, report metadata, source URLs, page locators, and code needed for editorial inspection. See `DATA_RIGHTS_NOTICE.md`.

