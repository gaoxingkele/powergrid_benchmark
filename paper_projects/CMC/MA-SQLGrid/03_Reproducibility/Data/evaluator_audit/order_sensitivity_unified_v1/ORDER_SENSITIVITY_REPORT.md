# Unified-Evaluator Candidate-Order Audit

This is a post-review descriptive diagnostic. It does not define a preferred policy or a confirmatory comparison.

- Questions: 180; fixed slots per question: 8.
- Exact global candidate orders enumerated: 40,320.
- C000 under the unified evaluator: 76/180.

| Selector | Original | Reverse | Exact min | Median | Mean | Exact max | Top ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| validation_only | 99/180 | 116/180 | 95/180 | 107.0/180 | 109.845/180 | 128/180 | 130/180 |
| complete_witness | 100/180 | 116/180 | 95/180 | 107.0/180 | 109.929/180 | 128/180 | 130/180 |

## Strict no-tie abstention diagnostic

| Selector | Covered | Correct when covered | Covered accuracy | Overall correct yield |
|---|---:|---:|---:|---:|
| validation_only | 50/180 | 24 | 0.4800 | 0.1333 |
| complete_witness | 50/180 | 24 | 0.4800 | 0.1333 |

The permutation range measures how much the frozen evidence leaves to the arbitrary final tie breaker. The risk--coverage table is outcome-aware and descriptive; it requires independent calibration and evaluation before operational use.

## Normalized unique-SQL audit

- Questions with at least one duplicate normalized SQL slot: 154/180.
- Mean unique SQL strings per eight-slot pool: 5.322.
- Descriptive right-step tie-size AURC: validation 0.4826; complete witness 0.4795.
- Deduplication changes the reported tie multiplicity when duplicate slots share one normalized SQL; it does not create a deployable tie rule. No SQL text is emitted.
