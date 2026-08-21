# CMC LaTeX delivery — 2026-07-24

Both manuscripts use the official 2026 Tech Science Press class
(`Definitions/tsp.cls`, SHA-256
`0AF34BE19ABB02753E8B29D2B2E4833FAAA49F07FE38BEEB8D105F27462A9145`)
with the `cmc,article,submit,moreauthors,pdftex` options and the official
Vancouver bibliography style.

## MA-SQLGrid

- Main PDF: `MA-SQLGrid/MA-SQLGrid_CMC.pdf` — 20 pages
- Submission source: `MA-SQLGrid/MA-SQLGrid_CMC_LaTeX.zip`
- Supplement: `MA-SQLGrid/MA-SQLGrid_CMC_Supplementary.tex` and `.pdf` — 9 pages
- ZIP SHA-256:
  `F069FBA88FAA34BDCF36EF1576A05FB0C86378D97F6100A1E1AF9333DF53E442`
- PDF SHA-256:
  `31337226A29D50F609FE6D7C356DEB12BE13900E8DC68C6A517700A7CABDBF24`

## C2GES

- Main PDF: `C2GES/C2GES_CMC_20pages.pdf` — 20 pages
- Submission source: `C2GES/C2GES_CMC_LaTeX.zip`
- Supplement: `C2GES/C2GES_CMC_Supplementary.tex` and `.pdf` — 6 pages
- ZIP SHA-256:
  `DAE7748797C06743D7FCA8BDD7AE852CA80FA631899D871365B81425972700D4`
- PDF SHA-256:
  `D274EB194AC7C9AF1D89EA6AC0D0AC41DD06691FBA583AE8BFCAE83B0F478788`

`C2GES_CMC.pdf` is the superseded 26-page file and was open in another
process during delivery refresh, so the final 20-page version is explicitly
named `C2GES_CMC_20pages.pdf`. The ZIP contains the final 20-page source.

## Verification

- Each source ZIP was independently extracted and rebuilt with
  `pdflatex -> bibtex -> pdflatex -> pdflatex`.
- Both rebuilt main manuscripts are exactly 20 pages and compile with zero
  errors, zero undefined citations or references, and zero overfull boxes.
- Both supplements compile with zero errors, zero undefined references, and
  zero overfull boxes.
- Main PDFs are US Letter size and use the official single-column submission
  layout.
- Detailed tables removed from the main text for length control remain in the
  supplementary materials.
- The six mandatory CMC declarations are present in the required order.

## Author action still required

Both manuscripts intentionally retain
`[AUTHOR INPUT REQUIRED: grant number]` in the Funding Statement. Replace this
with the confirmed grant number before submission. The DOI, received/accepted
dates, volume, issue, and article number shown as template placeholders are
assigned by the publisher and should not be filled by the authors.

BibTeX reports non-fatal missing-page warnings for several conference records
whose existing bibliography metadata does not contain page ranges. These do
not affect compilation, numbering, or the generated PDF, but the records may
be enriched before submission if authoritative page ranges are available.
