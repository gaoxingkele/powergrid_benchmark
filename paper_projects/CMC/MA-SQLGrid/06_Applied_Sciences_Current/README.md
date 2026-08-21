# MA-SQLGrid Applied Sciences Source

- Main source: `paper_applsci.tex`
- Built PDF: `paper_applsci.pdf`
- Bibliography: `references_applsci.bib`
- Experiment protocol: `EXPERIMENT_PLAN.md`
- Formal 2x2 prompt manifest:
  `../../../2026_ma_sqlgrid_cmc/source/code/applsci_factorial/manifest.json`

Build with `pdflatex`, `bibtex`, then two further `pdflatex` passes. Replace all
`AUTHOR INPUT REQUIRED` and placeholder author emails before submission. Do not
report the 2x2 experiment as completed until `applsci_factorial.py --execute`
produces predictions and scores.
