# MA-SQLGrid Narrative Revision (2026-08-12)

This release is a narrative restructuring of the current MA-SQLGrid Applied
Sciences manuscript.  It was created from the 2026-08-09 reference release
(`paper_applsci.tex` SHA-256
`AFB06156782467C495E36964FEB541FC6C0C061D8AA8C795DD924D27C7000D99`).
The reference release and all frozen experiment directories remain unchanged.

## Authority

- Working manuscript: `MA_SQLGrid/paper_applsci.tex`
- Compiled PDF: `MA_SQLGrid/paper_applsci.pdf`
- Supplementary guide: `MA_SQLGrid/SUPPLEMENTARY_MATERIALS.md`
- Revision ledger: `REVISION_LEDGER.md`
- Visual QA: `MA_SQLGrid/VISUAL_QA_MANIFEST.json` and
  `MA_SQLGrid/VISUAL_QA_REPORT.md`

This release changes the title and research narrative but does not introduce a
new experiment, dataset, baseline, or result.  All quantitative claims must
remain traceable to the evidence used by the 2026-08-09 reference release.

## Build

Run from `MA_SQLGrid/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
bibtex paper_applsci
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
pdflatex -interaction=nonstopmode -halt-on-error paper_applsci.tex
```

Generate a new Visual QA only after the final build:

```powershell
python audit_ma_visual_qa.py
```

The audit script refuses to overwrite an existing `visual_qa` directory or QA
manifest.  Move the previous QA into a separately named archive before an
intentional rebuild; never delete a QA record that has been used for delivery.

