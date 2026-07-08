# MA-SQLGrid Submission Package

Package date: 2026-06-27

This package contains the refrozen MA-SQLGrid paper artifacts after bounded submission polish.

## Main Files

- `manuscript/paper.pdf` -- final rendered IEEE Access manuscript PDF.
- `manuscript/paper.tex` -- final LaTeX source used to build the PDF.
- `manuscript/references_verified.bib` -- bibliography containing exactly the 45 keys cited by `paper.tex`.
- `manuscript/references_full.bib` -- full Stage 22 bibliography pool.
- `manuscript/paper_final_verified.md` -- Markdown companion regenerated from the current TeX.

## Supporting Material

- `assets/charts/` -- figure assets used by the paper.
- `data/griddb_maintenance_v2_v0_1/` -- GridDB-Maintenance-v2 v0.1 dataset package.
- `code/experiment_final/` -- canonical experiment code, outputs, traces, and result files.
- `code/evaluator/` -- local semantic evaluator.
- `evidence/` -- main results, component ablation, validator diagnostics, mechanism diagnostics, and Stage 14 analysis artifacts.
- `verification/` -- citation/finalization reports, recent-reference check, and workspace progress snapshot.
- `harness_approvals/` -- Paper-Harness decisions for bounded polish and final text/PDF approval.

## Final Harness Status

- `run_20260626-234417`: `REOPEN_FOR_BOUNDED_SUBMISSION_POLISH`
- `run_20260626-235834`: `paper_text_quality APPROVE`
- `run_20260627-000428`: `paper_pdf_quality APPROVE`

No external Spider/BIRD-style benchmark expansion or experiment rerun is included in this package. Claims remain local to the fixed `GridDB-Maintenance-v2 v0.1` protocol and archived run artifacts.
