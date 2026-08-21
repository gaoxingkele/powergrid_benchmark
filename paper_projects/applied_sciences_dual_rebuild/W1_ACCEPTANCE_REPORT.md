# W1 Scientific-Protocol Acceptance Report

Date: 2026-08-05 (Asia/Shanghai)

Scope: protocol repair and offline validation for the planned Applied Sciences
rebuilds of MA-SQLGrid and C2GES. This report does **not** promote any old result
to the new manuscripts and does not claim that model experiments are complete.

## Acceptance decision

W1 is accepted for code/protocol readiness. Formal model execution remains a W2+
activity. In particular, MA-SQLGrid still needs configured model endpoints, and
C2GES still needs a leakage-free rebuilt corpus plus an upstream predicted-label
model for the end-to-end protocol.

## MA-SQLGrid

The registered design is a balanced 2 x 2 factorial experiment:

- context scope: full vs. compact;
- answer-shape hints: absent vs. present;
- frozen held-out questions: 180;
- cells: 4;
- required predictions for each model/seed: 720.

The zero-cost full dry run completed successfully and wrote 720 prompts, 180 in
each cell. Gold fields are removed before prompt construction and exact gold-SQL
absence is asserted per prompt.

Key frozen identifiers:

- prompt-set SHA-256: `28009f5b926867e240fd45102a820a37d38dfaa1ba36eb11281e584190491ad5`;
- data SHA-256: `199fcf7cf850eceb94378131a0a9f55fea475dfbd838ac7deb99d02846f8f266`;
- code SHA-256: `8d94dddfbbcaff7505f2deb6aa1daa820d64c174dadedfbb18c24033a3be543b`;
- configuration SHA-256: `62a0b71550bcd54c16c4eef1a79aabfe070bba98d271ede2396128e90363029b`.

Artifact: `w1_validation/ma_factorial_dryrun/manifest.json`.

No prediction or score was fabricated in dry-run mode. Provider failures in
execution mode are represented as explicit failures with null SQL, and any run
containing provider, parse, or scoring failures is marked
`completed_with_failures`. Existing managed artifacts require explicit resume or
overwrite intent.

## C2GES

The rebuilt protocol now preserves the original FEVER Wikipedia identity as
`underlying_document_id`. The default split assigns complete Wikipedia-document
groups deterministically; limits are applied only at document boundaries, so a
page cannot be split or partially truncated by the instance cap.

The old local corpus failed the new leakage audit:

| Pair | Overlap count | Wikipedia documents |
|---|---:|---|
| train vs. dev | 1 | YouTube |
| train vs. test | 3 | Elizabeth_I_of_England; Floyd_Mayweather_Jr.; Linkin_Park |
| dev vs. test | 0 | none |

Decision: all performance numbers derived from that old split are legacy-only
and are ineligible for new primary tables. They may appear solely in an explicitly
labelled reproducibility appendix.

Three machine-readable protocols are available:

- `oracle-label`: conditional evidence selection; `is_end_to_end=false`;
- `predicted-label`: end-to-end, using external predicted roles;
- `label-blind`: end-to-end, exposing no veracity role.

Bootstrap resampling uses the underlying Wikipedia document as the cluster.
Runs record per-instance predictions and candidate scores, configuration, data
hashes, environment/Git state, and leakage audit. Generated results cannot be
silently overwritten; `--overwrite` removes only the known generated files.

## Shared statistics and evidence gates

The shared audit accepts CSV or JSONL and checks the complete condition-by-item
Cartesian product, duplicates, missing values, item-cluster consistency,
cross-condition cluster coverage, and provenance hashes. Only complete unique
pairs enter paired cluster bootstrap. Binary paired outcomes additionally receive
exact McNemar tests, and the resulting family is Holm-adjusted.

Evidence is eligible for a primary table only when all of the following hold:

1. the registered data split and protocol are used;
2. the leakage audit passes;
3. the expected condition-by-item grid is complete;
4. data, code, prompt/configuration, model, and seed provenance are present;
5. failed calls are explicit and are not replaced by placeholder predictions;
6. uncertainty and paired significance are computed at the registered cluster;
7. oracle-label C2GES results are labelled conditional and never end-to-end.

## Verification record

- MA-SQLGrid protocol tests: 4/4 passed.
- C2GES protocol and tiny offline training tests: 10/10 passed.
- Shared statistical-audit tests: 5/5 passed.
- Total: 19/19 passed.
- Modified C2GES scripts passed `py_compile`.
- MA-SQLGrid full dry run completed with status
  `prompts_frozen_not_executed` and `is_full_registered_run=true`.

## Open dependencies for W2

- Execute MA-SQLGrid on preregistered model/seed blocks once model endpoints are
  available; do not mix model versions within a block.
- Rebuild the formal C2GES document-grouped dataset and retain its manifest and
  zero-overlap audit.
- Train an upstream FEVER role predictor without exposing test labels; training
  roles supplied to the selector must be out-of-fold predictions or otherwise
  generated without self-prediction leakage.
- Run the C2GES oracle, predicted-label, and label-blind protocols over the same
  registered split and seed set.
- Route all candidate main-table results through the shared strict audit.

