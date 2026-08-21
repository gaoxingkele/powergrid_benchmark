# C²GES R2 Staging

This directory is a manuscript-preparation area only. It does not modify the R1 manuscript, the build08 dataset, the development run, the v0.3 FAIL freeze, or the v0.3.1 successor freeze.

## Current state

- The manuscript has a complete *Applied Sciences*-style section skeleton and evidence-bounded prose.
- Figures 1–3 are code-native SVG schematics backed by frozen design/audit artifacts.
- Figure 4 is an explicit `EVIDENCE_PENDING_TEST` scaffold and contains no data marks.
- Formal result tables contain only `EVIDENCE_PENDING_TEST` tokens.
- The v0.3.1 pre-test audit passed and one authorized formal execution completed after the initial staging draft. Numerical outputs remain quarantined until independent post-run audit.
- This staging task did not read the test JSONL or the prediction ledger.

## Assembly rule

Do not replace any pending token until a fresh independent result audit validates the completed formal output. If that audit fails, preserve the run and its audit finding, revise the manuscript as a methods/data paper or stop submission, and do not import R1 results.
