# MA-SQLGrid order/tie adjudication

Two independently blinded agent reviewers covered all 114 `order_sensitive` questions and all 18 top-k questions without reading model predictions or semantic-outcome diagnostics. Both reviewers found zero questions whose current natural-language request, metadata, schema constraints, and gold `ORDER BY` jointly establish a claim-promoting total-order comparison.

- Reviewer A: 95 `ORDER_METADATA_INCONSISTENT`, 19 `TIE_AMBIGUOUS_HOLD`.
- Reviewer B: 96 `ORDER_METADATA_INCONSISTENT`, 18 `TIE_AMBIGUOUS_HOLD`.
- Hold-set agreement: 114/114.
- Exact classification agreement: 113/114.

The only label difference is Q064. It asks for the latest reading for every asset but does not request output order. Reviewer A emphasized possible co-latest rows; Reviewer B emphasized that sequence-sensitive metadata is unsupported. The adjudicated label is `ORDER_METADATA_INCONSISTENT`, while the formal status remains `HOLD` either way.

Consequently, the claim-promoting automated multi-state suite may use only the 66 questions currently marked order-insensitive. All 180 questions may still be executed and reported diagnostically, but none of the 114 held questions may enter the primary suite denominator. This is an agent technical review, not qualified human power-grid annotation or a human audit of question--SQL correctness.
