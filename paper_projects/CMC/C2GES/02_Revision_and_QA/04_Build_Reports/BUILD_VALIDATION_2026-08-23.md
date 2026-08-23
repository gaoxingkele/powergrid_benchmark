# C2GES build validation — 2026-08-24 candidate from the 2026-08-23 revision

Status: **PASS (technical)**; `submission_ready=false` because author/external gates remain open.

- Public entry point: `python 03_Reproducibility/Code/run_public_verification.py`
- Python: 3.12.10.
- Tests: core 29/29; development 10/10 with 1 restricted-input skip; post-run 10/10 with 2 restricted-input skips.
- Data checks: 40 sampling-frame rows, 27 included reports, 15 test reports/10 series, 210 output rows, six report and six series contrasts, 210 matched-word rows, 12,924 embedding candidates, 27 layout-audit reports, two normalized-path contrasts, and equal nine-configuration development budgets for three methods.
- Clean temporary LaTeX build: main 22 pages; supplement 2 pages; zero undefined citation/reference, fatal/error, or overfull findings.
- Technical visual QA: every page rendered and contact sheets inspected; no obvious clipping, overlap, blank/corrupt page, or misplaced figure/table.

Final PDFs:

- `01_Manuscript/PDF/C2GES_Applied_Sciences_2026-08-24.pdf` — SHA-256 `6FCDD4278BFF0EC89F39AE3DBD713A6FB0DE9691F913197BB2D11DB2F7E5C9A9`.
- `01_Manuscript/PDF/C2GES_Supplementary_2026-08-24.pdf` — SHA-256 `AB2FB14C388F2A28C58892760F70D85E2914E13B1C8CB5EF38332C1A35F037B1`.

MiKTeX printed its local update reminder; it did not affect any build return code or LaTeX correctness check.
