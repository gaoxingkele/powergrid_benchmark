# W4 Formal-Protocol and Five-Seed Acceptance Report

Date: 2026-08-05 (Asia/Shanghai)

## Acceptance decisions

- C2GES five-seed execution and evidence audit: **ACCEPTED**.
- Reliable role-conditioning benefit: **NO-GO**.
- Blanket superiority over BM25: **NO-GO**.
- MA external-database factorial protocol: **ACCEPTED for development use**.
- MA external questions as human-gold or sealed evidence: **NO-GO** until real
  reviewers complete the supplied workflow; development-visible items can never
  be made retroactively sealed.

## C2GES formal evidence

The frozen corpus contains 8000/1500/1500 instances and 745/141/145 underlying
Wikipedia documents. Seeds 2026--2030 each contain oracle-label,
predicted-label, and label-blind runs. Seed 2026 is the frozen W3 run and was not
rerun; seeds 2027--2030 add 12 successful W4 executions.

| Protocol | K=1 | K=3 | K=5 | K=10 |
|---|---:|---:|---:|---:|
| Oracle-label | 0.6705 +/- 0.0050 | 0.4926 +/- 0.0015 | 0.4160 +/- 0.0009 | 0.3563 +/- 0.0001 |
| Predicted-label | 0.6688 +/- 0.0051 | 0.4920 +/- 0.0021 | 0.4150 +/- 0.0007 | 0.3563 +/- 0.0002 |
| Label-blind | 0.6677 +/- 0.0021 | 0.4910 +/- 0.0021 | 0.4154 +/- 0.0006 | 0.3560 +/- 0.0003 |
| BM25 | 0.6994 | 0.4864 | 0.4109 | 0.3530 |

Values are mean +/- sample standard deviation over five training seeds; BM25 is
fixed for the common test set.

At the preregistered K=3 role contrast, predicted-label minus label-blind is
0.00097 with seed t-CI [-0.00165, 0.00359] and hierarchical seed/document CI
[-0.00119, 0.00307]. Oracle-label contrasts also include zero. Role conditioning
therefore fails the primary gate.

All protocols underperform BM25 at K=1 by approximately 0.029--0.032 F1. At K=3,
oracle and predicted-label have small positive hierarchical intervals relative
to BM25, while label-blind narrowly fails the gate. This is budget-dependent
behavior, not broad superiority.

Mean wall time per run is approximately 200--205 seconds and sampled peak RSS is
approximately 1.27--1.28 GiB. All 15 protocol runs succeeded. The evidence audit
passed 176/176 checks and independently verified the frozen corpus, predicted
labels, code, local encoder snapshot, configurations, seeds, protocol identities,
data hashes, and prediction counts.

Freeze manifest SHA-256:
`75b19cc9609bce6014c1b275210bb9399d2a68c41df186003015198f6ada0ceb`.

## MA external protocol

RTS-GMLC contributes 55 and SimBench 36 development-visible automatic
candidates. Each enters a balanced full/compact x no-shape/shape design, giving
91 x 4 = 364 prompt cells. The accepted protocol demonstrates:

- exact registered-reference SQL and answer-field prompt leakage: zero;
- identical per-item database, perturbation ID, perturbation block, and hashes
  across four cells;
- 91/91 registered reference queries safe, read-only, and executable;
- shared Cartesian/hash audit 364/364 passed;
- network/model/paid calls: zero;
- dedicated tests: 7/7 passed.

This is protocol plumbing, not a model-accuracy result.

## Human-review dependency

The blind A/B review packet covers all 91 candidates and includes a third-person
adjudication sheet plus raw agreement/Cohen-kappa calculation. Machine triage
flags 4 high-, 69 medium-, and 18 low-risk records; prominent issues include 44
unit-expression flags, 57 high-template-similarity flags, 22 top-k tie-policy
flags, and 4 empty results. Machine flags prioritize attention but cannot decide
semantic validity.

At this checkpoint, real human review completion is 0 and sealed items are 0.

## Manuscript implications

1. C2GES must abandon role improvement as its primary contribution.
2. Its title should receive the smallest honest change that retains C2GES,
   evidence selection, interpretable reranking, and the power-grid application
   while removing/subordinating a causal-role gain claim.
3. Oracle-label is a conditional upper bound, never an end-to-end result.
4. NERC remains silver/qualitative unless real domain-expert evidence is added.
5. MA may describe cross-schema protocol feasibility, but external accuracy and
   sealed generalization remain unavailable until model execution and real review.

