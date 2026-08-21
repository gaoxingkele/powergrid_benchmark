# W3 RTS-GMLC Pilot Data Engineering Report

## Outcome

- Source: RTS-GMLC commit `3ece0d3725c844056132393ee252b3083dd4eab4`.
- SQLite tables: **10**; rows: **360,530**.
- Programmatic NL/SQL records: **55**, all explicitly `AUTO_CANDIDATE`.
- Gold SQL execution: **55/55** successful with result hashes.
- Template families: **11**; family overlap across splits: **0**.
- Database SHA-256: `ef1c2c6c36804ddb0bd34375256f65e4e3e6ccdafc69c1a7da9ea21bf5f91047`.

## SQLite row counts

| Table | Rows |
|---|---:|
| `branches` | 120 |
| `buses` | 73 |
| `dispatch_da` | 52,416 |
| `generator_constraints` | 158 |
| `generator_costs` | 158 |
| `generators` | 158 |
| `load_timeseries_da` | 26,352 |
| `renewable_availability_da` | 254,736 |
| `reserve_products` | 7 |
| `reserve_requirements_da` | 26,352 |

## Time-series coverage

- Load, renewable availability, and reserve requirements: 8,784 hourly timestamps from `2020-01-01 00:00:00` through `2020-12-31 23:00:00`.
- PLEXOS allTX dispatch: 336 hourly timestamps from `2020-07-05 00:00:00` through `2020-07-18 23:00:00`, covering 156 of 158 generator identifiers.

## Candidate question design

| Split label | Candidate rows |
|---|---:|
| `candidate_holdout_unsealed` | 15 |
| `candidate_train` | 30 |
| `candidate_validation` | 10 |

Families are assigned wholly to one split label. The holdout is named `candidate_holdout_unsealed` because generation was automatic and no independent human annotation or sealing occurred.

Coverage includes single-table retrieval, joins, aggregation/grouping, time predicates, filters, top-k, generator costs, operating constraints, renewable availability, regional load, reserves, and PLEXOS dispatch.

## License and provenance

The pinned upstream README permits use/copy/distribution subject to retaining the complete data-use notice and crediting DOE/NREL/Alliance. The upstream notice in this commit ends mid-sentence; the exact local text is preserved in `SOURCE_DATA_USE_NOTICE.md`, and redistribution remains subject to legal review.

## Scientific limitations

- Questions are deterministic `AUTO_CANDIDATE` records, not human gold labels and not publication-ready sealed evidence.
- PLEXOS `production_cost_value` retains source values without an independently verified unit.
- Period-based timestamps assume Period 1 maps to 00:00 and have no asserted timezone.
- Human domain review, paraphrase review, ambiguity adjudication, and an independently sealed split remain mandatory before confirmatory experiments.
