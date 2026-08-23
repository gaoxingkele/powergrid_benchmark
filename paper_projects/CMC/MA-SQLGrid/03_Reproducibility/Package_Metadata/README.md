# MA-SQLGrid — 2026-08-23 Revision Package

The current release root is `paper_projects/CMC/MA-SQLGrid/`.

- `01_Manuscript/LaTeX/`: MDPI source, verified bibliography, six figures, and lineage records.
- `01_Manuscript/PDF/`: current PDF built from the 0823 LaTeX baseline.
- `01_Manuscript/Supplementary/`: rights-safe historical protocol/numerical subset.
- `02_Revision_and_QA/`: incoming review, detailed plan, route decision, evidence ledger, build reports, and author/external gates.
- `03_Reproducibility/Code/`: framework, executors, analyses, post-review evaluator diagnostics, environment locks, and one public verifier.
- `03_Reproducibility/Data/`: redistribution-safe derived evidence for GridDB, components, constructed states, the historical pool, and BIRD.
- `03_Reproducibility/Figures/`: publication outputs and lineage sources.
- `03_Reproducibility/Package_Metadata/`: rights notice, source map, verifier, release manifest, and checksums.

Run the portable technical check from any working directory:

```text
python paper_projects/CMC/MA-SQLGrid/03_Reproducibility/Code/run_public_verification.py
```

The frozen unified evaluator reports C000 `76/180`, validation-only `99/180`, complete witness `100/180`, and best fixed source Qwen F01 `129/180`. The package deliberately reports `submission_ready=false` until the corresponding email, author approvals, rights, external grid evaluation, and expert-review gates are closed.
