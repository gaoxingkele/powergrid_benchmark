# Prospective BGE Expansion Protocol Freeze

Frozen: 2026-08-06 Asia/Shanghai, before any formal BGE output existed.

## Scope

This is a new prospective baseline family independent of the completed Round-3 add-on. It evaluates the locally cached `BAAI/bge-reranker-base` snapshot on the existing document-grouped FEVER test partition. It neither changes the Round-3 seven-comparison family nor uses the agent-labelled NERC pilot.

## Fixed inputs

- Test data: 1,500 human-gold FEVER claim/document instances in 145 underlying Wikipedia-document clusters.
- Model: `BAAI/bge-reranker-base`, Hugging Face revision `2cfc18c9415c912f9d8155881c133215df768a70`, six cached files, 1,134,374,819 logical bytes.
- BGE input: ordered `[claim, candidate sentence]` pairs; no FEVER label or gold evidence is exposed to the model.
- Reference methods: five-seed C2GES full, deterministic BM25, and the already prospective MiniLM cross-encoder.

All file identities are recorded in `PROTOCOL_FREEZE.json`.

## Execution contract

- One deterministic zero-shot BGE run; no fine-tuning and no outcome-dependent retry.
- CPU execution, batch size 32, maximum sequence length 512, seed 20260806.
- Stable descending score order; original sentence order breaks exact ties.
- Evidence budgets: K = 1, 3, 5, and 10.
- Every claim must produce all four rows. A failure aborts the run rather than silently dropping a claim.
- Formal outputs are written only under `formal_run/` and never overwrite an existing directory.

## Endpoints and estimands

- Primary endpoint: exact sentence-ID evidence F1 at K=3.
- Secondary descriptive endpoints: evidence precision and recall at K=3, evidence F1 at K=1/5/10, wall time, and sampled peak resident memory.
- C2GES is averaged over its complete five-seed bundle at the claim level. BM25, MiniLM, and BGE are deterministic single-run methods.
- All point estimates are claim weighted. Documents are the resampling and randomization clusters.

## Frozen primary family

The sign convention is BGE minus comparator. Exactly three K=3 comparisons form the new family:

1. BGE minus C2GES full;
2. BGE minus BM25;
3. BGE minus MiniLM cross-encoder.

For each contrast:

- a 10,000-draw document-cluster bootstrap gives a composition-sensitivity 95% percentile interval, resampling documents with replacement and pooling all claims in sampled clusters;
- a two-sided 100,000-sample document-cluster sign-flip test evaluates the sharp zero-effect reference;
- Holm correction controls the three-comparison family at alpha 0.05.

Bootstrap seeds are `20270806 + family_index`; sign-flip seeds are `20260806 + family_index`, using zero-based family indices. No claim will be promoted unless the Holm-adjusted p-value is below 0.05. Intervals are not described as population confidence intervals.

## Required outputs and gates

- Immutable predictions ledger, resource record, provenance with model/code/data hashes.
- Cell and contrast CSV, TeX table, SVG/PDF/PNG budget and forest figures.
- Results summary, recursive artifact manifest, and an independent validator that recomputes all cells, intervals, randomization p-values, and Holm values from the frozen inputs.
- Integration is allowed only if there are exactly 6,000 unique `(qid,K)` BGE rows, 1,500 claims at every K, 145 document clusters, zero model/run failures, exact input hashes, and a passing independent validation report.

## Claim boundary

This experiment establishes only a human-gold FEVER zero-shot BGE comparison under the frozen local snapshot. It is not NERC or deployed power-grid validation, not a BGE fine-tuning study, and not evidence that any method generalizes beyond the two tested corpora.
