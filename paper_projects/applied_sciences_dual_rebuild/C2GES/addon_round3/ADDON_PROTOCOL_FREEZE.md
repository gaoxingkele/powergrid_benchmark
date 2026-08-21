# C2GES Round-3 add-on protocol freeze

- Frozen at: `2026-08-05T16:50:01+08:00` (Asia/Shanghai), before any Round-3 add-on training, scoring, or outcome inspection.
- Status: post-primary prospective execution from this freeze forward. It is separate from canonical v2 and retrospective exploratory v3 and cannot alter either W6 primary gate.
- Feasibility at freeze: both new architectures instantiate and expose the intended structural constraints; the cached cross-encoder snapshot loads locally on CPU. The machine has 24 logical processors and 68,572,536,832 bytes RAM.

## Unchanged evaluation contract

The add-on uses the existing document-grouped FEVER train/development/test files and unchanged test documents, claims, sentence candidates, exact sentence identifiers, exact-ID macro precision/recall/F1, and `K in {1,3,5,10}`. The data manifest SHA-256 is `ebccec847886e7f8478869ac0e83c3fd2a2e7fdefd244c6868eb97281554b89f`; the test partition SHA-256 remains `fff475583c9603673134614b06d17229f6711f3e55e80ac5412462845bdc63b8`. The primary editorial cell is label-blind `K=3`.

Label-blind is the sole add-on protocol because it is the deployment-valid primary cell and is sufficient for identifying the two architectural questions: removing all floors while retaining the role architecture, and structurally removing the role head and role floor. Repeating oracle/predicted protocols would answer a different role-provenance question already bounded by canonical v2 and would multiply new training without improving these estimands.

## Frozen arms

All and only these arms are reported at every K:

1. `full`: existing five-seed label-blind predictions, original three-channel floors `(0.35, 0.25, 0.05)`.
2. `bm25`: existing deterministic supplied-document BM25.
3. `query_only`: existing deterministic equal lexical/dense query channel.
4. `dense`: existing deterministic frozen MiniLM cosine (`sbert`).
5. `no_local`: existing five-seed full head/mixture with the local channel removed at inference (`no_graph`).
6. `true_no_floor`: **new**, retrained independently for seeds 2026--2030; the role head remains, but all three mixture floors are exactly zero.
7. `true_no_role`: **new**, retrained independently for seeds 2026--2030; the role head has zero parameters, its mixture weight is structurally zero, and the trainable mixture contains query/local channels only with their original floors `(0.35, 0.05)`.
8. `cross_encoder`: **new prospective rerun**, zero-shot `cross-encoder/ms-marco-MiniLM-L-6-v2`, local revision `c5ee24cb16019beea0893ab7796b1df96625c6b8`, CPU, batch size 64, maximum token length 512.

New learned variants reuse the original optimizer and learning contract: seeds 2026--2030, four epochs, Adam, learning rate 0.001, train/development/test limits 8000/1500/1500, training selection K=3, pairwise softplus ranking loss, and development-F1 checkpoint selection. `true_no_floor` retains the 0.5 role-contrast loss; `true_no_role` omits it because the role head is absent. The executable SHA-256 is `473b36c3beabe8dfabdb6ec138fbbf1fce82a1e3a4e85fdb2965890debfa33f8`.

## Cross-encoder scoring and integrity

Each candidate is scored once as the ordered pair `[claim text, candidate sentence text]` with the cached model's scalar relevance logit, no fine-tuning, CPU inference, batch size 64, and truncation/padding performed by the snapshot tokenizer at maximum length 512. For every claim and K, sort by descending score; exact ties retain the original candidate-sentence order (stable sort). The runner SHA-256 is `509220e67a7120e3604206d27582585268b17a11109afbd49f53d78c6d8bede7`. The six-file snapshot contains 91,815,758 bytes; the frozen file-list digest is `f565acfdd6b717b0248d4adcf9addae285f14f5d5841f8dae9089df0733cab88`. File hashes are stored in the companion JSON.

## Estimands, intervals, and multiplicity

The point estimand is claim-weighted macro exact-ID evidence F1. For seeded arms, average the five predictions within claim before arm contrasts. Document-cluster bootstrap intervals resample the 145 underlying test documents with replacement and pool every claim and its complete seed bundle from each sampled document; repeated sampled documents repeat all constituent claims. Use 10,000 percentile draws with RNG seed `20260805 + contrast index`.

The single primary family contains seven K=3 arm-minus-`full` contrasts (`bm25`, `query_only`, `dense`, `no_local`, `true_no_floor`, `true_no_role`, `cross_encoder`). Raw two-sided p-values use 100,000 document-cluster sign-flip draws with RNG seed `20261805 + contrast index`, and Holm adjustment covers all seven. Exact two-sided five-seed sign-flip p-values are additionally reported for `true_no_floor-full` and `true_no_role-full`; with five seeds, their minimum is 0.0625 and they are stability diagnostics rather than a route around the primary family. K=1,5,10 are descriptive sensitivity results and cannot rescue a K=3 claim.

## Runtime boundary

- New learned variants: wall time and sampled peak RSS for the complete CPU process, including model/encoder load, train/dev/test encoding, four-epoch training, checkpoint selection, and all-K test scoring. This is a reproducibility-resource boundary, not online latency.
- Cross-encoder: model load plus complete 1,500-claim test scoring and all-K extraction; training is none.
- Existing arms: retain their recorded historical boundaries and do not infer missing mode-specific latency from a shared full-script measurement.

No cross-arm Pareto or non-dominance claim is permitted because these boundaries differ. A resource table must name each boundary explicitly.

## Integrity and stopping rule

Each new run must use a fresh output directory and retain configuration, checkpoint (where trained), complete prediction ledger, stdout/stderr, resource record, source/data/model hashes, Python/package versions, and success status. Report every frozen arm and contrast regardless of direction. No substitutions, tuning after test inspection, favorable-seed selection, or expansion are permitted. If any architecture cannot run as frozen, report the exact blocker and do not substitute an inference-only legacy mode.
