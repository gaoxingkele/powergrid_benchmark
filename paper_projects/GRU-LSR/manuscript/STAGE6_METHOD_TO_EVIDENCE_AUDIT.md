# Stage 6 Method-to-Evidence Audit

Status: **aligned; accepted science preserved; no new claim**.

This audit is an internal release record. Its evidence sources are the frozen
`upgrade_contract.json`, the accepted and Stage-6 rerun manifests and sealed
outputs, the five Stage-3 derived tables, `DEEP_REVISION_EVIDENCE.md`,
`MANUSCRIPT.md`, and `journal_submission/paper.tex`. It does not replace or
expand those sources.

## Narrative and placeholder preservation

The Markdown abstract and TeX abstract remain semantically identical. Under
the accepted rule that counts ASCII alphabetic tokens and retains internal
hyphens as one token, the narrative is exactly 236 words. Its UTF-8 SHA-256 is
`c86963d625f30e7f1c709f0b2ea55a6913c01a51d88835f3053fb42c37f176f6`.
Stage 6 did not rewrite it.

All human-supplied facts remain deferred to Stage 7. The Markdown source still
contains 11 `AUTHOR INPUT REQUIRED` markers and the exact journal TeX contains
9. No author, affiliation, correspondence, funding, contribution, conflict,
AI-disclosure, biography, photograph, public-release URL/DOI, dataset vintage,
or external-review fact was inferred.

## Claim-chain alignment

| Claim layer | Accepted statement | Evidence binding and retained boundary |
|---|---|---|
| Title | Reproducible retrospective curtailment-risk benchmark and fair evaluation of GRU learned-space retrieval on RTS-GMLC | One hashed, truncated 8760-row sequence; proxy target; delivery-row lags; no operational forecast or uniform-superiority claim |
| Contribution | Auditable benchmark, matched retrieval use case, and evidence-ranked reporting | Protocol validity does not depend on a favorable method result; contribution remains bounded to the explicitly verified corpus |
| Method | Fixed proxy, temporal gate, shared training budget, matched retrieval controls, and frozen inference | Runner, contract, four input hashes, budgets, candidates, seeds, estimands, analysis units, families, stopping rule, and statistical decisions are unchanged |
| Experiment | 2310 completed result rows and 240 completed trajectories | Ten algorithmic seeds on one sequence; test targets are reused across seeds and are not independent replicates; architectures are budget matched but not parameter-count matched |
| Primary result | Learned-space attribution is horizon dependent | At 1 h, learned k=8 retrieval is favorable versus raw and randomized controls after within-family Holm adjustment; at 24 h it is adverse versus raw and unresolved versus randomized |
| Negative reference result | Persistence has lower MAE than selected GRU-LSR at the primary cap at both lags | Deterministic descriptive comparison only; no seed-based p-value for Persistence |
| Null/adverse architecture result | Architecture findings are contrast specific | At 1 h GRU is adverse versus LSTM and TCN and favorable versus DLinear after the separate family adjustment; at 24 h GRU is favorable versus DLinear, while its adverse means versus LSTM and TCN are not Holm-resolved; no overall winner is claimed |
| Onset result | Onset-targeted analysis is inapplicable | Zero positive onsets in selection and calibration at every cap/lag; diagnostic exact tests and fallback ties do not cure missing support or prove no effect |
| Dependence sensitivity | Moving-block intervals are conditional and descriptive | One chronological test sequence after seed averaging; excluded from Holm; the 24 h learned-versus-raw intervals include zero at both block lengths and do not override the adverse paired-seed result |
| Cross-cap result | Selected-learned-versus-Persistence ordering crosses | Same-sequence descriptive sensitivity only; no transport claim across policies, years, systems, or caps |
| Discussion | Benchmark value is compatible with mixed, null, and adverse method findings | No causal, decision-impact, operator-usefulness, physical-feasibility, safety, economic, or deployment inference |
| Conclusion | Licensed advance is the manifest-bound benchmark and evidence-ranked evaluation | No global recurrent-method novelty, observed-curtailment accuracy, probabilistic calibration, operational dispatch, external-expert validation, complete-year, or cross-system claim |

## Estimand and comparison qualifications

The primary estimand remains the cap-0.70 mean paired within-seed
treatment-minus-control difference conditional on the ten frozen seeds,
sequence, horizons, selection objective, metric, model budget, retrieval bank,
and contrast. One paired method-seed run remains the analysis unit. The 95%
seed interval remains conditional on training-seed variability; it is not an
interval over hours, blocks, years, systems, policies, operators, or
deployments. Exact sign-flip interpretation continues to require
sign-exchangeability under a no-effect null; the common seeds are not
randomized experimental assignments.

The three comparison families remain separate within each horizon. Cross-cap
comparisons, k=4/16/32 sensitivity, comparisons with deterministic references,
and all onset readouts without pre-test support remain descriptive or
diagnostic as frozen. Combined ablations license only joint conclusions, and
proxy or historical studies retain their source-specific scopes.

## Stage 6 rerun disposition

The isolated attempt-5 rerun used exact runner, contract, and input identities.
Every non-timing scientific field and every paper-facing derived table is
exact. Seven sealed outputs are raw-byte identical; `run_results.csv` and
`trajectory_ledger.csv` differ only in declared runtime fields. The recorded
software/hardware environment is exact. Timestamps, isolated paths, and wall-
clock runtimes are non-scientific and are disclosed in
`STAGE6_RERUN_COMPARISON.json` and `STAGE6_RERUN_COMPARISON.md`.

The rerun supports no manuscript change and no new claim.
