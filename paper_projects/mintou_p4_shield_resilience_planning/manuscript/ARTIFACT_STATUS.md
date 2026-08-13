# Artifact Status

- `MANUSCRIPT.md` is the canonical manuscript source for this stage.
- `EQUATION_IMPLEMENTATION_CONTRACT.md` records the equation--configuration--code mapping and the scopes that must be preserved when regenerating derived artifacts.
- `../experiments/p4_s3_boundary_predeclared.json` and `../experiments/p4_boundary_experiments.py` control the new p4-only boundary study. The frozen source profile, 1050 complete run rows, bounds, summaries, gaps, and immutable manifest are under `../evidence/`; `python experiments/p4_boundary_experiments.py verify` checks their hashes and within-setting bound sharing.
- No shared p3/p4 planning source was changed. The boundary NSGA-II+Repair execution uses the installed pymoo 0.4.1 API and is explicitly supplementary to the historical main archive.
- `journal_submission/paper.tex` is regenerated from the canonical manuscript by the official preview builder. The checked-in `journal_submission/paper.pdf` predates this revision and is not a current rendering because no LaTeX engine is available in this worktree environment.
- The figure-generation source is corrected and copied into `journal_submission/figures/`. The checked-in PNG files were not regenerated because the available Python/Matplotlib installation fails during import; captions in the canonical manuscript explicitly qualify the retained legacy panel labels.
- `submission_preview/` is a legacy pre-stage preview and is not a controlling manuscript or evidence source.
