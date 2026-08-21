# C2GES v0.3.1 Corrective History

## Historical preservation

The predecessor `TEST_FREEZE_MANIFEST_v0_3.json` and every file it binds remain
unchanged. Its independent pre-test audit verdict was FAIL, so that freeze is a
retained, non-executable historical incident. No v0.3 formal test was run.
This successor history is a new file because appending to the v0.3-bound
`CORRECTIVE_HISTORY.md` would invalidate the historical closure.

## v0.3.1 changes made before any formal test

1. Replaced `semantic_centroid` with `semantic_mmr` while retaining exactly
   seven conditions. Semantic-MMR uses the same frozen normalized MiniLM
   embeddings for document-centroid relevance and pairwise redundancy. Its
   score is `0.5 * relevance - 0.5 * maximum_selected_cosine`; lambda was fixed
   without test inspection or development optimization.
2. Kept three primary contrasts at two budgets (six ROUGE-L tests) and changed
   the semantic primary baseline to `semantic_mmr`; Holm adjustment remains
   across all six records.
3. Converted all test-file entries to repository-relative paths and made the
   formal verifier iterate over `bound_files`, `code_files`, and `test_files`.
4. Threaded `path_min_edges`, `path_max_edges`, `path_max_paths`, and
   `path_max_expansions` through runner, channel scoring, and typed-path
   enumeration. Synthetic regression tests prove each parameter is operative;
   path and expansion limit violations fail closed.
5. Added an installed recursive output-dependency lock, including transformer,
   tokenization, stemming, numerical, and model-loading dependencies, while
   retaining the semantic-model tree hash and offline-only requirement.
6. Added authorization enforcement. A future authorization must bind the exact
   v0.3.1 freeze SHA-256, an independently generated PASS decision SHA-256, one
   unique run id, and the exact canonical output directory.
7. Added a durable repository-global attempt registry. Atomic directory
   creation reserves the only attempt before test content is decoded. Both
   failed and successful attempts remain registered; any existing reservation,
   including a crash-only placeholder, prevents another physical attempt.
8. The successor freeze remains unauthorized. The test-only JSONL has not been
   parsed or executed during repair or regression testing.

## Unchanged scientific boundaries

- The dataset remains diagnostic build08: 12 development and 15 isolated test
  reports. No development configuration was reselected.
- The selected full-method weights, redundancy penalty, graph distance, and
  typed-path length range remain those selected by development run04.
- The negative development full-minus-no-CF ROUGE-L@5 difference
  (`-0.005665215823945863`) remains unchanged and must be reported verbatim.
- Any future test execution is post-audit corrective/descriptive evidence, not
  fresh confirmatory or outcome-unseen evidence.

