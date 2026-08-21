# W4 C2GES Five-Seed Report

## Decision

- Role-conditioning primary claim: **NO-GO**.
- Blanket superiority over BM25: **NO-GO**.
- Seed 2026 is the frozen W3 run and was not rerun; seeds 2027-2030 are new W4 runs.
- Evidence/failure audit: **PASS** (176 checks, 0 failures).

## Five-seed evidence F1 (mean +/- sample SD)

| Protocol | K=1 | K=3 | K=5 | K=10 |
|---|---:|---:|---:|---:|
| oracle-label | 0.6705 +/- 0.0050 | 0.4926 +/- 0.0015 | 0.4160 +/- 0.0009 | 0.3563 +/- 0.0001 |
| predicted-label | 0.6688 +/- 0.0051 | 0.4920 +/- 0.0021 | 0.4150 +/- 0.0007 | 0.3563 +/- 0.0002 |
| label-blind | 0.6677 +/- 0.0021 | 0.4910 +/- 0.0021 | 0.4154 +/- 0.0006 | 0.3560 +/- 0.0003 |
| BM25 (fixed) | 0.6994 | 0.4864 | 0.4109 | 0.3530 |

## Primary role effect at K=3

- predicted-label_minus_label-blind: mean delta 0.00097; seed t-CI [-0.00165, 0.00359]; hierarchical CI [-0.00119, 0.00307]; gate=NO-GO.
- oracle-label_minus_label-blind: mean delta 0.00157; seed t-CI [-0.00167, 0.00482]; hierarchical CI [-0.00093, 0.00440]; gate=NO-GO.
- oracle-label_minus_predicted-label: mean delta 0.00060; seed t-CI [-0.00117, 0.00237]; hierarchical CI [-0.00121, 0.00228]; gate=NO-GO.

## Relative to BM25

- oracle-label: K=1: delta=-0.0289, hierarchical CI [-0.0435, -0.0141], gate=NO-GO; K=3: delta=0.0062, hierarchical CI [0.0017, 0.0109], gate=GO; K=5: delta=0.0051, hierarchical CI [0.0021, 0.0082], gate=GO; K=10: delta=0.0033, hierarchical CI [0.0022, 0.0045], gate=GO.
- predicted-label: K=1: delta=-0.0306, hierarchical CI [-0.0465, -0.0157], gate=NO-GO; K=3: delta=0.0056, hierarchical CI [0.0008, 0.0107], gate=GO; K=5: delta=0.0041, hierarchical CI [0.0012, 0.0071], gate=GO; K=10: delta=0.0033, hierarchical CI [0.0022, 0.0044], gate=GO.
- label-blind: K=1: delta=-0.0317, hierarchical CI [-0.0456, -0.0173], gate=NO-GO; K=3: delta=0.0046, hierarchical CI [-0.0000, 0.0092], gate=NO-GO; K=5: delta=0.0045, hierarchical CI [0.0015, 0.0075], gate=GO; K=10: delta=0.0031, hierarchical CI [0.0019, 0.0042], gate=GO.

## Runtime and failures

| Protocol | Mean wall s | Mean peak RSS GiB | Successful runs |
|---|---:|---:|---:|
| oracle-label | 200.40 | 1.280 | 5/5 |
| predicted-label | 204.99 | 1.270 | 5/5 |
| label-blind | 200.40 | 1.274 | 5/5 |

No subprocess failure was recorded. RSS is a 0.2-second psutil process-tree sample and may miss shorter spikes.

## Claim guidance

Do not claim a reliable role-conditioning gain if the primary role gate is NO-GO; frame results around budget-dependent retrieval behavior and transparent cost/accuracy trade-offs.
The five training seeds are a small algorithmic-repeat sample; seed-level t intervals and the hierarchical seed/document bootstrap are both reported. Exact sign-flip p-values are retained in the JSON/CSV rather than treated as adequately powered with n=5.
