# Build

Run from this directory.

Information (current submission target):

```text
pdflatex -interaction=nonstopmode -halt-on-error paper_information.tex
bibtex paper_information
pdflatex -interaction=nonstopmode -halt-on-error paper_information.tex
pdflatex -interaction=nonstopmode -halt-on-error paper_information.tex
```

Applied Sciences (retained diagnostic baseline):

```text
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
bibtex paper_applsci
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
```

