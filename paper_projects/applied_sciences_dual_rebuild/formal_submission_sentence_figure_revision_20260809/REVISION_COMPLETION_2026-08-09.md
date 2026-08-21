# Sentence and Figure Revision Completion Record

Date: 2026-08-09 (Asia/Shanghai)

## Scope

This revision was created in a new directory and does not overwrite the preceding three-round-review version. No experimental observations, registered outcomes, or statistical estimates were altered in this pass.

## C2GES

- Rewrote the abstract to state the problem, method, experimental evidence, negative ablation result, and scope directly.
- Replaced manuscript-process and title-concordance language with research-facing statements.
- Split overloaded sentences in the method, reproducibility, discussion, conclusion, supplementary-material, and data-availability sections.
- Preserved the registered negative counterfactual-channel ablation and removed any implication that this component improved predictive accuracy.
- Added a two-panel native-vector framework figure covering the end-to-end selector and the path-deletion mechanism.
- Final PDF: 27 A4 pages; framework figure on page 7.

## MA-SQLGrid

- Replaced manuscript-process language with direct methodological and evidentiary statements.
- Standardized the terminology around named-state evidence and removed ambiguous historical labels.
- Split overloaded release, manifest, experiment-design, conclusion, supplementary-material, and data-availability sentences.
- Added a two-panel native-vector figure covering five-role coordination, the append-only trace, candidate gates, evidence scoring, the sealing boundary, and offline gold evaluation.
- Final PDF: 30 A4 pages; framework figure on page 10.

## Figure Reproducibility

- Both figures are produced from `figure_sources/generate_dual_panel_frameworks.py`.
- Editable SVG and publication PDF versions are stored with each manuscript.
- The publication PDFs contain no raster-image objects and use no hatch or diagonal-grid pattern.

## Build Verification

- Both manuscripts completed the `pdflatex -> bibtex -> pdflatex -> pdflatex` build sequence.
- No fatal TeX errors, undefined citations, or undefined cross-references were found in the final logs.
- The rendered figure pages were visually inspected for clipping, overlap, boundary violations, and caption consistency.
