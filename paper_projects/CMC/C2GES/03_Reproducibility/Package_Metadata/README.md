# C2GES — 2026-08-23 Revision Package

The current release root is `paper_projects/CMC/C2GES/`.

- `01_Manuscript/LaTeX/`: MDPI source, verified bibliography, template assets, and six manuscript figures.
- `01_Manuscript/PDF/`: current main and supplementary PDFs built from the 0823 LaTeX baseline.
- `01_Manuscript/Supplementary/`: supplementary LaTeX source.
- `02_Revision_and_QA/`: incoming review, detailed plan, evidence ledger, claim audit, build reports, and external gates.
- `03_Reproducibility/Code/`: frozen core, public tests, sensitivity scripts, environment locks, and one public verifier.
- `03_Reproducibility/Data/`: rights-safe metadata, frozen derived results, and post-review diagnostics.
- `03_Reproducibility/Figures/`: publication outputs and lineage sources.
- `03_Reproducibility/Package_Metadata/`: rights notice and current-layout release manifest/checksums.

Run the technical public verification from any working directory:

```text
python paper_projects/CMC/C2GES/03_Reproducibility/Code/run_public_verification.py
```

The technical verifier does not redistribute or regenerate excluded source PDFs or verbatim extracted text. `submission_ready=false` remains correct until the author, rights, expert-annotation, unseen-series, and operational-validation gates are closed.
