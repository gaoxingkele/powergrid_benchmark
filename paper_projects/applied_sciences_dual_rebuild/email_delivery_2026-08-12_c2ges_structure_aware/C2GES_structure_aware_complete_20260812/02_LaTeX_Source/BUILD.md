# LaTeX build

Run from this directory with MiKTeX or TeX Live:

```text
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
bibtex paper_applsci
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
```

The manuscript uses the bundled MDPI class and bibliography files in `Definitions/`. All six referenced figure PDFs are included under `figures/`.

