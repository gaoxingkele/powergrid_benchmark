# Manuscript artifact status

- `MANUSCRIPT.md` is the current content master for the P2 S4 results-narrative stage.
- `derived_tables/` and the result figures in `figures/` were regenerated deterministically by `figures/make_figures.py` after it verified the accepted rolling-origin manifest and its recorded outputs. `derived_tables/p2_artifact_manifest.json` records the source and output hashes.
- `journal_submission/paper.tex`, `body.generated.md`, `body.generated.tex`, and its figure directory were regenerated or synchronized from the current master.
- `submission_preview/paper.tex` and its figure directory were synchronized to the same current content.
- The existing PDFs were not regenerated because the required `pdflatex` executable is unavailable in this environment. They predate the P2 S4 narrative and must not be used as current manuscript previews.

The failed PDF compilation occurred after Markdown-to-TeX conversion and did not alter experiment outputs. The listed scientific acceptance check passes; the official journal acceptance remains environment-blocked at PDF compilation.
