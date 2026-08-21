# C2GES Applied Sciences compressed submission package

Prepared on 2026-08-09 after the second content-compression revision.

## Manuscript

- Title: *Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES) for Power Grid Maintenance Reports*
- Current PDF length: 25 pages, including 41 references
- `manuscript/`: current MDPI LaTeX source, compiled PDF, bibliography, MDPI definitions, all figure files, figure lineage, and the build script

## Code and data

- `scripts/`: verification and package-building scripts
- `supplementary/transferable/`: rights-safe code snapshots, protocols, result ledgers, non-verbatim metadata, figure inputs, statistical diagnostics, tests, and audit records
- Source NERC PDFs, verbatim derived text, model weights, credentials, and `.env` files are intentionally excluded because they are restricted or unnecessary for editorial verification.

The public code repository is <https://github.com/gaoxingkele/c2ges>.

## Submission checks

Yang Yong is the corresponding author. Before submission, create and verify an independent email account controlled by Yang Yong and replace the temporary correspondence address in `paper_applsci.tex`. Recompile the PDF after that change.

All numerical claims must remain tied to the included frozen or audited ledgers. Machine-assisted labels are not qualified power-grid expert gold.
