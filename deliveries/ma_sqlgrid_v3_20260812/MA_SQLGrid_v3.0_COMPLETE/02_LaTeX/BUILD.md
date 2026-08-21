# Build Instructions

Run the following commands in the LaTeX source directory:

```text
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
bibtex paper_applsci
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
```

The package contains the MDPI class and bibliography style under `Definitions/`,
the bibliography database, and the six figure PDFs referenced by the manuscript.
The validated version 3.0 output contains 25 A4 pages, six figures, and eleven
tables.
