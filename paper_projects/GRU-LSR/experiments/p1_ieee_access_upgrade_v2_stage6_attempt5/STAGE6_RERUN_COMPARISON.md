# Stage 6 Frozen Rerun Comparison

Status: **scientific content exact; timing disclosed; no new claim**.

## Identity

- Runner SHA-256: `d4f0e14dd010e4f429e2d61771d781b169a673b73156dac5236113f0e3f34e28` (exact).
- Contract SHA-256: `3d99dc96aeb9ac51974f76e5c0f544083f4dc41a4f5de5998b7b3e7f2ec78878` (exact).
- All four source-file hashes, evaluated-row profile, delivery keys, branch constants, model counts, fixed budgets, selections, completeness fields, and protocol-validity fields are exact.
- The rerun used the same Python/NumPy/PyTorch-CUDA versions, CUDA device, deterministic cuDNN flags, CUBLAS workspace configuration, and four CPU threads.

## Scientific content

- All non-timing fields in all 2,310 result rows and all 240 trajectory rows are exact.
- Seven sealed outputs, including the prediction NPZ, are raw-byte identical. The two non-identical CSVs differ only in their declared runtime fields.
- All 30 paired-effect rows, 36 moving-block rows, 258 cap/k rows, protocol-validity fields, failure ledger, completeness ledger, and prediction arrays are exact.
- All five paper-facing derived tables are exact in canonical scientific CSV bytes when independently rederived from the rerun. The Windows checkout's CRLF rendering is recorded separately from the accepted LF provenance and has no scientific effect.
- The accepted abstract remains the same 236-word narrative under the frozen alphabetic-token rule (`c86963d625f30e7f1c709f0b2ea55a6913c01a51d88835f3053fb42c37f176f6`), and Markdown/TeX text agrees.
- All Stage 7 human placeholders remain: 11 in `MANUSCRIPT.md` and 9 in `journal_submission/paper.tex`.

## Timing and environment disclosure

The total measured runtime changed from 156.5523632 s to 166.1597529 s. Per-row/trajectory runtime fields also changed, as expected for non-scientific wall-clock measurements. Start/completion timestamps, the isolated script path, and absolute command path changed with the new execution location. The recorded execution environment fields are exact.

## Claim boundary

This rerun verifies exact non-timing scientific reproduction under the frozen execution environment. It does not change any result direction, null/adverse finding, comparison family, uncertainty unit, descriptive qualifier, evidence boundary, method claim, discussion statement, or conclusion. It supports no new causal, operational, external-expert, deployment, cross-system, complete-year, policy-transport, operator, safety, physical, or economic claim.
