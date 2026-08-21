# MA-SQLGrid R3 Visual QA

The exact 20-page PDF with SHA-256
`1D1284C35F691717457A592FF24F48D68C29386B7C6D2ED9E7BCF0D4710BE1C6`
was rendered anew with Poppler `pdftoppm` 25.07.0 at 144 dpi. All 20 page
images were inspected; no R2 render or earlier PDF was reused.

Result: **PASS**. No clipping, overlap, missing glyph, figure truncation,
unresolved reference, or stale release-v3 prospective claim was visible. All
12 tables and four figures were checked. Page 8 has intentional float-related
white space, and the Q039 table on page 15 is compact but legible. The explicit
corresponding-author email placeholder is a manual submission blocker rather
than a rendering defect.

The machine-readable PDF, renderer, page-image hashes, and inspection scope are
recorded in `VISUAL_QA_MANIFEST.json`.
