# Information draft build

Revision: 2026-09-13, reconstruction round 3. This is a local rewrite, not a submitted or accepted article.

The entry point is `paper_information.tex`. Keep `paper_applsci.tex` and its historical records unchanged. Required local assets are `Definitions/`, the six referenced PDFs under `figures/`, `references_verified.bib`, and `references_information.bib`.

From this LaTeX directory, run with MiKTeX or a compatible installation on PATH:

```powershell
pdflatex -interaction=batchmode -halt-on-error paper_information.tex
bibtex paper_information
pdflatex -interaction=batchmode -halt-on-error paper_information.tex
pdflatex -interaction=batchmode -halt-on-error paper_information.tex
```

Stop on any nonzero exit code. Rerun LaTeX if the final log still requests reference updates. The verified installation was MiKTeX-pdfTeX 4.23 (MiKTeX 25.12), under `C:/Users/10175/AppData/Local/Programs/MiKTeX/miktex/bin/x64/`.

From the repository root:

```powershell
py -3.12 paper_projects/MA-SQLGrid/Workspace/02_Revision_and_QA/08_Information_Iterations/verify_iteration.py --round 3 --pass-name final
py -3.12 -m unittest discover -s paper_projects/MA-SQLGrid/Workspace/03_Reproducibility/Code/evaluator_audit -p test_selection_failure_decomposition.py -v
py -3.12 paper_projects/MA-SQLGrid/Workspace/02_Revision_and_QA/08_Information_Iterations/render_current.py --round 3 --pass-name final
```

Rendering needs PyMuPDF and Pillow. Rendering refuses an existing output folder; inspect it instead of overwriting earlier evidence. A new revision requires a new versioned QA folder. Rendering must be followed by inspection of every current page; the script itself does not certify visual quality. These commands refresh round-specific checks, not the historical release manifest. Rebuilding can change PDF metadata and its SHA-256; record the new hash and repeat visual QA before freezing another version. The legacy v1 audit assumes unchanged tables and must not be used to certify later versions with new analyses.

Round 3 build: 30 pages; 13 main-text tables plus one historical appendix table, six figures and 39 cited references. The 189-word abstract and artifact-specific verification scope are recorded in `../../02_Revision_and_QA/08_Information_Iterations/round3/final/verification.json`. Consult the round review for visual status; a previous PDF's visual approval does not transfer to a rebuild.

The MDPI `information` journal option is active. Its draft header is template text, not proof of submission. The dummy template DOI is suppressed. Existing historical supplementary data remain unchanged and are not represented as newly generated experiments.
