# MA-SQLGrid Role-Utilization and Score-Ablation Protocol

Status: frozen before executing the audit script on 2026-08-23. This is a post-review diagnostic analysis of the existing historical pool. It is not a prospective role-removal experiment and makes no model calls.

## Questions

1. Which recorded role outputs are actually consumed downstream by the frozen selector implementation?
2. How do selected slots and unified-evaluator matches change when one observable score component is removed at a time?
3. What deterministic role/message/execution costs are visible in the frozen ledgers?

## Frozen inputs

- Sealed pre-gold blackboards: SHA-256 `2B447A63D47D225E15148E0A75C660DDAFC83E5C50AAA2DDC207D252B9FB6777`.
- Unified fixed-slot outcomes (`canonical_rows_v2.jsonl`): SHA-256 `A290770448219ECB81B01DB61E3A789C4101F5CC38BF342BD34E2931FC7E10F9`.
- Candidate execution attempts: SHA-256 `BD26ABCBFDB4F86BFAC640B06B74C496E0B6571A4521EDAA9EA644393B97EC38`.
- Historical study driver: SHA-256 `31D1EBDA004890DD22935A83DA168A106BDFE50D2CFE423862A80AE73894F8CD`.
- Adjudicator implementation: SHA-256 `EA8105FC3AB6F8F54B59E74B0AD9AC96D5CD1ABB073469C51E9DB5A7066915BE`.

## Code-level utilization definitions

- `consumed`: a field is passed into a computation that can affect eligibility or ranking.
- `recorded_only`: the message is stored in the blackboard but no field from it is passed into the historical selector computation.
- Invocation/message counts do not by themselves establish utilization or benefit.

The audit must distinguish the Query Analyst output used by `validation_for` from the Schema Cartographer output, which is posted to the board but is not passed to candidate generation, validation, the critic, or adjudication in the frozen historical-pool driver.

## Frozen ablations

All ablations retain the same eight fixed candidate slots, original candidate order, stored execution admissibility, and unified shape-and-denotation outcome matrix. They change only one recorded scoring component:

- remove the Query-Analyst-derived terms jointly (`shape`, `order`, and lexical `value_hits`);
- remove `shape` points only;
- remove `order` points only;
- remove lexical `value_hits` only;
- remove the constructed-state eligibility gate from complete-witness selection, which must reduce exactly to the validation-only selector;
- remove Schema Cartographer output, which is expected to be selection-invariant because that output has no downstream consumer in the frozen driver.

The safety and executability gates remain active in every executable selector variant. The audit does not simulate an unsafe system without execution validation.

For each variant report unified correct count, accuracy, changed choices, gains, and losses relative to its stated parent selector. No post-result ablation is elevated to a preferred method.

## Cost accounting

Report observed blackboard message counts by role/kind; 5,760 database execution attempts; failure-kind counts; and total/median/95th-percentile recorded execution time. These are ledger costs on this machine and are not model-token, deployment-latency, energy, or scale estimates.

## Acceptance checks

- 180 unique sealed boards, 22 messages per board, and 1,440 fixed outcomes.
- Reconstructed original validation and complete choices match all sealed decisions.
- Unified original counts reproduce 99 and 100.
- The no-constructed-state complete variant exactly reproduces every validation-only choice.
- Schema-grounding removal changes zero choices.
- No question text or SQL text appears in output tables.
