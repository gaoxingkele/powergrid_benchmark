# MA-SQLGrid Applied Sciences compressed submission package

Prepared on 2026-08-09 after the second content-compression revision.

## Manuscript

- Title: *MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases*
- Current PDF length: 28 pages, including 35 references
- `manuscript/`: current MDPI LaTeX source, compiled PDF, bibliography, MDPI definitions, all figure files and lineage inputs, and the build script

## Code and data

- `code/`, `tests/`, and `scripts/`: executor, coordination, verification, and regression assets
- `evidence/`: rights-safe result tables, manifests, selector traces, numerical supplements, and reproducibility evidence
- `reviews_round3/` and root audit files: retained review and engineering-boundary records
- Third-party databases, model weights, credentials, `.env` files, and excluded accident runs are intentionally omitted. Public BIRD data remain available from the dataset provider; access to restricted power-system artifacts remains subject to their licenses.

The public code repository is <https://github.com/gaoxingkele/ma-sqlgrid>.

## Submission checks

Yang Yong is the corresponding author. Before submission, create and verify an independent email account controlled by Yang Yong and replace the temporary correspondence address in `paper_applsci.tex`. Recompile the PDF after that change.

The evidence supports bounded software and finite-corpus claims only; it must not be promoted to universal robustness, five-role superiority, or qualified expert validation.
