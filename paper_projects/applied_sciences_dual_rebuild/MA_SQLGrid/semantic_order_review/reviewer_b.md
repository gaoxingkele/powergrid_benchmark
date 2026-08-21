# Reviewer B — GridDB order and top-k tie audit

## Independent-review boundary

I reviewed only the Q021–Q200 test records in `questions.jsonl` and the keys and constraints declared in `schema.sql`. I did **not** inspect Reviewer A, model predictions, semantic-diagnostic outcomes, gold-result rows, or state-specific executions. This is an agent technical consistency review of wording, gold SQL, `ORDER BY`, declared constraints, and tie policy; it is not a human power-system-domain validation, operational audit, or model-performance assessment.

Source SHA-256 values:

- `questions.jsonl`: `a08f302afb47bc2e7c352d20ca69efa0068b74d9ad296c988bc7b27160593a82`
- `schema.sql`: `37ce31ee7cdf928b464af77ddb65bd4aa7beb7c3250f2da07e512427fe7980d4`

The complete machine-readable, per-question ledger is `reviewer_b.json`. It contains 114 unique records, every gold `ORDER BY`, a schema-level total-order judgment, the verdict, per-item evidence codes, and the top-k cutoff judgment.

## Decision

**HOLD ordered evaluation as currently annotated.** Coverage and totals validate as follows:

| Check | Result |
|---|---:|
| `order_sensitive=true` test questions reviewed | 114/114 |
| Unique question IDs | 114 |
| Top-k questions reviewed | 18/18 |
| `TOTAL_ORDER_VALID` | 0 |
| `TIE_AMBIGUOUS_HOLD` | 18 |
| `ORDER_METADATA_INCONSISTENT` | 96 |
| Syntactically total under declared constraints | 70 |
| Not guaranteed total under declared constraints | 44 |
| Missing `ORDER BY` extraction | 0 |

I used a deliberately semantic verdict rule: `TOTAL_ORDER_VALID` requires both (i) an order/rank requested by the natural-language question and (ii) a SQL/tie policy that uniquely fixes positions and cutoff membership. A technically deterministic presentation order is not sufficient when the question never requests that order.

## Top-k cutoff findings (18/18)

| IDs | Gold ranking | Verdict and cutoff evidence |
|---|---|---|
| Q039 | `scheduled_date ASC LIMIT 1` | `TIE_AMBIGUOUS_HOLD`: equal earliest dates are possible; no unique secondary key or co-earliest policy. |
| Q051 | `parts_cost DESC LIMIT 1` | `TIE_AMBIGUOUS_HOLD`: equal maximum costs are possible; no unique secondary key or co-maximum policy. |
| Q074 | rounded `avg_capacity_mw DESC LIMIT 1` | `TIE_AMBIGUOUS_HOLD`: equal or rounding-induced maxima are possible; no tie rule. |
| Q117–Q130 | `reading_time DESC LIMIT 1` | `TIE_AMBIGUOUS_HOLD`: the schema permits equal latest timestamps for an asset; no co-latest or secondary-key policy. |
| Q200 | `alarm_count DESC, type_name LIMIT 1` | `TIE_AMBIGUOUS_HOLD`: SQL is technically total, but alphabetical elimination of co-maximal types is a hidden policy not authorized by the question. |

Top-k IDs: Q039, Q051, Q074, Q117, Q118, Q119, Q120, Q121, Q122, Q123, Q124, Q125, Q126, Q127, Q128, Q129, Q130, Q200.

## Non-top-k metadata finding (96/96)

Every remaining `order_sensitive=true` question requests a collection or grouped summary without stating a sorting requirement. Its gold `ORDER BY` is therefore a presentation choice, so each receives `ORDER_METADATA_INCONSISTENT`. These questions should be compared as unordered multisets, or their wording must be revised to request the exact order.

Of all 114 reviewed records, these 70 gold queries are syntactically total under the declared constraints (Q200 remains a semantic cutoff hold): Q023, Q025, Q027, Q030, Q031, Q032, Q035, Q036, Q041, Q042, Q045, Q047, Q053, Q054, Q056, Q058, Q059, Q062, Q066, Q067, Q068, Q070, Q071, Q076, Q077, Q079, Q080, Q099, Q100, Q101, Q102, Q103, Q104, Q105, Q106, Q107, Q108, Q109, Q110, Q111, Q112, Q113, Q114, Q115, Q116, Q155, Q156, Q157, Q158, Q159, Q160, Q161, Q162, Q163, Q164, Q165, Q166, Q167, Q168, Q169, Q170, Q171, Q172, Q173, Q174, Q175, Q176, Q177, Q178, Q200.

These 44 are not guaranteed total under the declared constraints: Q021, Q024, Q026, Q029, Q033, Q034, Q037, Q038, Q039, Q040, Q043, Q046, Q048, Q050, Q051, Q052, Q055, Q060, Q061, Q063, Q064, Q065, Q069, Q073, Q074, Q075, Q117, Q118, Q119, Q120, Q121, Q122, Q123, Q124, Q125, Q126, Q127, Q128, Q129, Q130, Q139, Q140, Q141, Q142.

## Required remediation

1. Relabel the 96 unordered-language records as `order_sensitive=false`, or rewrite each question to state the intended sort keys and directions.
2. Keep all 18 top-k records on hold until ties are handled by returning all co-extrema or by an explicit question-authorized secondary criterion reflected in the gold SQL.
3. For Q074, rank on the unrounded aggregate and round only the displayed value.
4. For Q200, either state the alphabetical tie-break in the question or return every co-maximal asset type.
