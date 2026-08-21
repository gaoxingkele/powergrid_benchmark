# CMC revised delivery — 2026-07-24

## C2GES

- Main PDF: `C2GES/C2GES_CMC_simexpert75_18pages.pdf` — 18 pages.
- Submission source: `C2GES/C2GES_CMC_LaTeX_simexpert75.zip`.
- Supplement: `C2GES/C2GES_CMC_Supplementary_simexpert75.tex` and `.pdf` — 7 pages.
- Annotation and dataset package: `C2GES/C2GES_SimulatedExpert75_Artifacts.zip`.
- SHA-256: PDF `743A84CC94ADE85F21FBED72CD75719D18DF2BFE276D552A9060A7E434E56051`; LaTeX ZIP `DCAC9220A19828AD4E63A9FE089C3285E6CDDF8D07C75BFF1CC31CA4E41009FD`; artifact ZIP `BD4D419410FD13DFF6E5456CDFA2EB04034371A857EFCE6CF3FD185C0972FEF9`.

The revised paper uses two explicit label views:

1. A mixed-provenance 200-question view containing 75 AI simulated-expert-adjudicated labels and 125 retained agent-candidate labels.
2. A fully replaced 75-question sensitivity subset containing only the new simulated-expert-adjudicated labels.

The three annotators were separate OpenAI Codex (GPT-5-based) instances operating on a blind packet. They are AI simulated-expert perspectives, not human experts or human-gold annotation. The manuscript, supplement, dataset fields, and reports disclose this limitation.

## MA-SQLGrid

- Main PDF: `MA-SQLGrid/MA-SQLGrid_CMC_revised_20pages.pdf` — 20 pages.
- Submission source: `MA-SQLGrid/MA-SQLGrid_CMC_LaTeX_revised.zip`.
- Supplement: `MA-SQLGrid/MA-SQLGrid_CMC_Supplementary_revised.pdf` — 9 pages.
- SHA-256: PDF `C04C1A24D2910E0EC90C22481B7A38A086F53CFDD8613A365A6C6E295AE8BE0F`; LaTeX ZIP `49DE18BD0B1D4CDFA0D2C135362793F50EDBA8B417EA90C514100FEFCC27240A`.

The revised manuscript now states that the original-generator validation increment is not significant, the projection-tolerant metric reverses the compact/full ordering, the tenfold test is asymmetric, and the missing full context-by-shape factorial prevents a compactness-only causal interpretation.

## Verification

- Official Tech Science Press CMC class and bibliography style retained.
- Both main manuscripts rebuilt with `pdflatex -> bibtex -> pdflatex -> pdflatex`.
- Both supplements rebuilt with two `pdflatex` passes.
- Zero compilation errors, undefined citations, or undefined references.
- Main-manuscript page counts: 18 and 20.
- Supplement page counts: 7 and 9.

## Author action required

Both manuscripts still contain `[AUTHOR INPUT REQUIRED: grant number]`. Replace it with the verified funding grant number before submission. Publisher metadata placeholders should remain for editorial assignment.
