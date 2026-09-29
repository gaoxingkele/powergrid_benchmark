# Manuscript artifact status

- `MANUSCRIPT.md` is the current content master for the P2 S5 three-round scientific-closure stage.
- `derived_tables/` and the quantitative result figures in `figures/` retain the P2 S4 outputs. Their content inputs did not change in S5. A hash audit matches all 14 recorded sources and all 32 recorded outputs in `derived_tables/p2_artifact_manifest.json`; canonical bytes were restored for result-figure PDFs after Windows checkout conversion, and a project attribute now preserves PDFs as binary files.
- A fresh invocation of `figures/make_figures.py` stopped before any writes because the only available Python 3.14 installation cannot load its Pillow `_imaging` extension. Quantitative figure regeneration is therefore environment-blocked in this stage; the retained figures are supported by their unchanged, hash-matched P2 S4 artifact record, not by a claimed S5 rebuild.
- `journal_submission/paper.tex`, `body.generated.md`, and `body.generated.tex` were regenerated from the current master. `submission_preview/paper.tex` was mechanically synchronized to the same generated source.
- The existing manuscript PDFs were not regenerated because no usable `pdflatex` executable is available in this environment. They predate the P2 S5 source revision and must not be used as current manuscript previews. All 34 retained PDFs pass `pdfinfo` and first-page `pdftotext` parsing without diagnostics, but that structural result does not make the two stale manuscript PDFs current.

The failed source and PDF regeneration attempts did not alter experiment outputs. The scientific acceptance result and the official journal acceptance result are recorded from commands run in this worktree; no unavailable artifact check is treated as passed.
