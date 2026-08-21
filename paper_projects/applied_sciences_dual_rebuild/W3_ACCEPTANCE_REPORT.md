# W3 Pilot Acceptance and Scientific Decision Report

Date: 2026-08-05 (Asia/Shanghai)

## Decision summary

- **MA-SQLGrid data engineering: GO for controlled development experiments.**
  RTS-GMLC and SimBench SQLite pilots are reproducible and executable, but their
  questions remain automatic, unsealed candidates and cannot support
  confirmatory claims.
- **C2GES engineering pipeline: GO for the remaining four seeds.** The complete
  one-seed run passed all artifact checks.
- **C2GES original superiority/role claim: NOT YET SUPPORTED.** At seed 2026,
  BM25 is significantly better at K=1, while oracle, predicted-label, and
  label-blind C2GES are statistically indistinguishable across all evaluated K.
  The final paper must follow the five-seed evidence, including a claim or title
  downgrade if this pattern persists.

No W3 value is promoted to a manuscript primary table at this stage.

## MA-SQLGrid external database pilots

### RTS-GMLC

- 10 tables and 360,530 rows.
- 55 deterministic `AUTO_CANDIDATE` NL-SQL records in 11 template families.
- 55/55 reference SQL statements execute and reproduce their result hashes.
- Template-family overlap across candidate splits: zero.
- Database SHA-256:
  `ef1c2c6c36804ddb0bd34375256f65e4e3e6ccdafc69c1a7da9ea21bf5f91047`.
- Dedicated acceptance tests: 6/6 passed.

The upstream data-use notice is retained exactly. Its local upstream copy ends
mid-sentence, so derived-data redistribution remains a legal-review blocker.

### SimBench

- Official network `1-MV-urban--0-sw` with eight tables.
- Rows: 1 network, 2 voltage levels, 144 buses, 147 lines, 2 transformers,
  139 loads, 134 generators/DER units, and 305 switches (874 total rows).
- 36 deterministic `AUTO_CANDIDATE` NL-SQL records, six in each of six query
  classes; all reference SQL results and hashes are recorded.
- Template-family overlap across candidate splits: zero.
- Database SHA-256:
  `01d0cd9da3ab15a6dca2709546ddc6acc33b3a3887defef7060caf5b02cf5524`.
- Dedicated acceptance tests: 6/6 passed.

Four candidates currently have empty answers and require explicit retain/rewrite
decisions during human semantic review. ODbL/DbCL attribution and share-alike
requirements remain part of the release gate.

### Promotion requirements

Neither pilot is human gold or sealed. Promotion requires independent dual
semantic review, ambiguity adjudication, natural-language de-templating,
unit/field verification, license clearance, and a genuinely unseen split frozen
after method development. Until then, they may be used only for pipeline,
robustness, and diagnostic development.

## C2GES complete-corpus seed-2026 pilot

Dataset: 8000/1500/1500 instances and 745/141/145 underlying Wikipedia
documents; exact cross-split document overlap is zero.

| Protocol | K=1 | K=3 | K=5 | K=10 | Wall time | Peak RSS |
|---|---:|---:|---:|---:|---:|---:|
| Oracle-label | 0.6656 | 0.4910 | 0.4148 | 0.3561 | 201.58 s | 1.259 GiB |
| Predicted-label | 0.6612 | 0.4897 | 0.4147 | 0.3563 | 191.75 s | 1.261 GiB |
| Label-blind | 0.6667 | 0.4914 | 0.4151 | 0.3559 | 199.36 s | 1.293 GiB |
| BM25 | 0.6994 | 0.4864 | 0.4109 | 0.3530 | n/a | n/a |

At K=1, document-cluster bootstrap supports BM25 over every C2GES protocol. At
K=3 and K=5, differences from BM25 are not significant. Every cross-protocol
paired cluster-bootstrap interval includes zero. This rules out a blanket
superiority statement for the pilot and makes the role contribution an explicit
five-seed decision point.

The upstream role predictor reached train-OOF/dev/test accuracy
0.7741/0.7927/0.8000. Oracle-label remains a conditional upper-bound protocol,
not an end-to-end result.

The title screen assessed 233,515 cross-split pairs. It found no normalized exact
alias and one reviewed high-similarity pair, `A_Game_of_Thrones` versus
`Game_of_Thrones`, which refers to the novel and television series respectively.
This screen cannot establish absence of redirect, content, or semantic
near-duplicates.

Shared evidence audit: 47/47 checks passed; no protocol failure was recorded.

## Next gate

1. Complete C2GES seeds 2027-2030 under the identical frozen protocol.
2. Independently aggregate five-seed effects and uncertainty; freeze the role
   contribution decision before manuscript writing.
3. Build a structured human-review packet for all 91 MA candidates, including
   the four empty-answer SimBench items and license/units warnings.
4. Exercise the MA prompt/evaluator pipeline on the two external schemas only as
   development evidence until a sealed, human-reviewed subset exists.

