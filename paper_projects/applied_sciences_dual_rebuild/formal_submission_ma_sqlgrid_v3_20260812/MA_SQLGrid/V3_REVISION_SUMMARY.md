# MA-SQLGrid 3.0 Revision Summary

Version 3.0 is the second content-narrative revision of the Applied Sciences manuscript. It does not define a new experiment generation or alter the retained numerical evidence.

## Main changes

1. Preserved the title, three research questions, five-role architecture, and the 80/180 -> 100/180 -> 101/180 main result.
2. Recast `robust`, `auditable`, and `multi-agent` once in the Introduction and removed repeated defensive qualifications.
3. Removed revision-process meta-narrative from the Introduction, Methods, and Discussion.
4. Rebuilt Tables 2 and 3 around resource roles, analytical units, endpoints, and research questions. RTS-GMLC/SimBench pilot status now appears as future validation context rather than a main-data audit table.
5. Replaced internal version labels in the main narrative with functional names such as `constructed-state study`, `historical-pool selection study`, and `later executor revision`.
6. Merged the duplicated candidate-coverage paragraphs and moved the full candidate and tie-size distributions to the supplement.
7. Shortened the BIRD predecessor-run account to one traceability sentence.
8. Reworked the Q039 table into readable projection, filter, witness, and reference-result differences; the full SQL remains a supplementary artifact.
9. Removed reverse-order endpoint values from the Abstract and Conclusions while retaining the complete sensitivity results in Results and Discussion.
10. Consolidated the detailed AI-use disclosure in Methods and reduced Acknowledgments to a short responsibility statement.
11. Simplified the Supplementary Materials and Data Availability statements.
12. Corrected the correspondence line so that Liu Bijing's address is not presented as Yang Yong's email. Yang Yong's actual submission email remains an explicit author-completion field.

## Verification outcome

- PDF: 25 A4 pages.
- Figures/tables: 6/11, discovered dynamically from the current TeX.
- Undefined citations/references: 0.
- Overfull boxes: 0.
- In-text citation keys missing from the bibliography: 0.
- Visual inspection: all 25 rendered pages inspected; no clipping, overlap, blank page, or corrupted glyph was found.
- Numerical token comparison confirmed that the core 80/100/101 result and the underlying historical-pool, component, BIRD, and constructed-state denominators remain present.
- Core test suites: 96 tests passed and 1 was skipped across the coordination, executor, GridDB, component, and constructed-state code. The BIRD v1.1 runtime-identity test was not re-certified under the current Python 3.12 / SQLite 3.49.1 environment; the paper correctly identifies the formal runtime as Python 3.10.11 / SQLite 3.40.1.

## Remaining human gate

Before submission, Yang Yong must provide and approve the correspondence email. No substitute address has been inferred.
