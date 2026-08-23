# C2GES build validation — 2026-08-23 revision

Status: **PASS (technical)**; `submission_ready=false` because author/external gates remain open.

- Public entry point: `python 03_Reproducibility/Code/run_public_verification.py`
- Python: 3.12.10.
- Tests: core 29/29; development 10/10 with 1 restricted-input skip; post-run 10/10 with 2 restricted-input skips.
- Data checks: 40 sampling-frame rows, 27 included reports, 15 test reports/10 series, 210 output rows, six report and six series contrasts, 210 matched-word rows, 12,924 embedding candidates, 27 layout-audit reports, two normalized-path contrasts, and equal nine-configuration development budgets for three methods.
- Clean temporary LaTeX build: main 22 pages; supplement 2 pages; zero undefined citation/reference, fatal/error, or overfull findings.
- Technical visual QA: every page rendered and contact sheets inspected; no obvious clipping, overlap, blank/corrupt page, or misplaced figure/table.

Final PDFs:

- `01_Manuscript/PDF/C2GES_Applied_Sciences_2026-08-23.pdf` — SHA-256 `590B816F95D1F902E48D44D5140C6295676E0ADA24C56FF63A3E1AFF605B91E1`.
- `01_Manuscript/PDF/C2GES_Supplementary_2026-08-23.pdf` — SHA-256 `0ADDA6A11B574787E0873B637FD0872DBC38910D6A65AD8092FA41FE5E8F39DB`.

MiKTeX printed its local update reminder; it did not affect any build return code or LaTeX correctness check.
