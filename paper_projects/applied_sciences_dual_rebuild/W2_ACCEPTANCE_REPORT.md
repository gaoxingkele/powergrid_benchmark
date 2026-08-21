# W2 Readiness and Data-Protocol Acceptance Report

Date: 2026-08-05 (Asia/Shanghai)

## Decision

W2 readiness is accepted. The C2GES data/protocol pipeline is released for a
formal five-seed pilot. MA-SQLGrid is released for external-dataset ETL and
sealed-question construction, but not for confirmatory model claims because no
model endpoint is configured and the existing 180-question test has already
been inspected.

No manuscript number was changed. Smoke, diagnostic, and legacy evidence remain
ineligible for primary result tables.

## C2GES release evidence

- Document-grouped FEVER instances: 8000 train / 1500 dev / 1500 test.
- Underlying Wikipedia documents: 745 / 141 / 145.
- Pairwise document overlap: zero for all three split pairs.
- Corpus SHA-256:
  `683694b87a9842e54eb48aad1aaff85f1105e150f10e9e43fa7efe915a36af20`.
- Upstream predictor: word and character TF-IDF with balanced logistic
  regression.
- Training predictions: StratifiedGroupKFold out-of-fold predictions, grouped
  by `underlying_document_id`.
- Dev/test predictions: one model fitted only on the complete training split.
- Protocols exercised: oracle-label, predicted-label, and label-blind.
- Offline protocol tests: 11/11 passed; five relevant scripts compile.

The 240/80/80 upstream smoke produced train OOF/dev/test accuracies of
0.6375/0.6625/0.6250. These values validate the workflow only. Likewise, the
60/20/20 selector smoke and one-seed wrapper output are not scientific results.

Residual risk: exact normalized Wikipedia titles do not detect every alias or
semantic near-duplicate. A title-alias/near-duplicate audit remains registered
before canonical result freezing.

## MA-SQLGrid release evidence

The read-only model audit found no configured common cloud model key/endpoint
pair, local serving command, or matching serving process. It performed zero
network probes and zero paid calls; serialized output contains presence booleans,
not secret values.

Seven local data families were inventoried with per-file hashes:

1. GridDB-Maintenance-v2 v0.1;
2. GridDB-Maintenance-v2 x10;
3. RTS-GMLC;
4. SimBench;
5. MATPOWER cases;
6. pandapower networks;
7. GridSTAGE.

The first two are existing benchmark/robustness data. RTS-GMLC and SimBench are
the primary candidates for new SQL ETL, schema construction, questions, license
review, and a sealed split. MATPOWER, pandapower, and GridSTAGE are secondary
schema-diversity or event-data candidates.

Two new dev-only deterministic diagnostics generated 360 predictions and passed
the paired artifact audit. Their strict accuracies were 0/180 and 2/180; both
reached 36.11% on the projection contract and 100% executable/safe SQL. These are
lower-bound diagnostics, not competitive baselines or manuscript claims.

Old model outputs were re-scored without inference into a separate 1980-row
legacy artifact. They must not be pooled with new predictions. The 2 x 2 design
again produced 720/720 frozen prompt cells and passed the shared audit.

MA W2 tests passed 4/4; factorial tests passed 4/4; shared statistical tests
passed 5/5.

## Unified execution controls

- Registered experiments: 26 total, 13 per paper.
- Evidence levels culminate at E4; only E4 can enter primary tables.
- Both manuscript budgets target approximately 8500 body words and six primary
  sections, derived from the ten-paper sample and explicitly not journal rules.
- Review workflow: 41 tracked checks across three rounds (15/13/13).
- Planning artifact validation: PASS for schemas, IDs, experiment coverage,
  E4 gates, budget sums, corpus linkage, and review-state coverage.

## Next authorized wave

1. Build small RTS-GMLC and SimBench SQLite pilots with field dictionaries,
   source/license manifests, template-family splits, and executable gold SQL.
2. Run the formal C2GES pilot on the full document-disjoint corpus for the three
   protocols, initially one seed; estimate time/memory before the remaining four.
3. Add Wikipedia alias/near-duplicate auditing and refuse canonical freezing if
   a cross-split pair is detected.
4. Do not initiate a paid MA model run until an endpoint/model/key is explicitly
   supplied and a pilot cost is measured.
5. Do not call any GridDB result confirmatory or sealed; it is diagnostic evidence
   because the test items have been repeatedly inspected.

