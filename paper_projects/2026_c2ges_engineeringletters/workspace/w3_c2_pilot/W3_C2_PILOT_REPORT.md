# W3 C2GES Pilot Report

## Scope and decision

Shared evidence audit: **PASS** (47 checks; 0 failures).
This is a one-seed pilot on the complete document-grouped corpus, not the final five-seed result.
Oracle-label remains conditional evidence selection and is not end-to-end.

## Data and leakage controls

- Instances: 8000 train / 1500 dev / 1500 test; corpus SHA-256 `683694b87a9842e54eb48aad1aaff85f1105e150f10e9e43fa7efe915a36af20`.
- Wikipedia documents: {'train': 745, 'dev': 141, 'test': 145}; exact document overlap: zero.
- Title audit examined 233515 pairs at SequenceMatcher >= 0.92 and trigram Jaccard >= 0.72.
- Exact normalized aliases: 0; reviewed candidates: 1; unreviewed: 0.
- The sole high-similarity candidate was A_Game_of_Thrones versus Game_of_Thrones, manually evidenced as novel versus television series.
- This title screen does not establish absence of redirect, content-level, or semantic near-duplicates.

## Upstream label predictor

| Split | Accuracy | Balanced accuracy | Macro-F1 |
|---|---:|---:|---:|
| train | 0.7741 | 0.7360 | 0.7365 |
| dev | 0.7927 | 0.7591 | 0.7611 |
| test | 0.8000 | 0.7621 | 0.7648 |

Train values are document-grouped OOF predictions; dev/test use a model fitted only on train.

## Selector evidence F1

| Protocol | K=1 | K=3 | K=5 | K=10 |
|---|---:|---:|---:|---:|
| oracle-label | 0.6656 | 0.4910 | 0.4148 | 0.3561 |
| predicted-label | 0.6612 | 0.4897 | 0.4147 | 0.3563 |
| label-blind | 0.6667 | 0.4914 | 0.4151 | 0.3559 |

BM25 test F1 was K=1: 0.6994, K=3: 0.4864, K=5: 0.4109, K=10: 0.3530.
At K=1, BM25 is significantly stronger than each C2GES protocol in the within-run document-cluster bootstrap; K=3 and K=5 differences are not significant. These pilot results do not support a blanket superiority claim.

## Runtime and resources

| Protocol | Wall seconds | Peak RSS GiB | Status |
|---|---:|---:|---|
| oracle-label | 201.58 | 1.259 | success |
| predicted-label | 191.75 | 1.261 | success |
| label-blind | 199.36 | 1.293 | success |

RSS is sampled with psutil over the process tree every 0.2 s; sub-interval peaks and GPU memory are not measured.

## Cross-protocol paired cluster bootstrap

- oracle-label_minus_predicted-label: K=1 delta=0.0043, 95% CI [-0.0040, 0.0139]; K=3 delta=0.0013, 95% CI [-0.0014, 0.0039]; K=5 delta=0.0000, 95% CI [-0.0013, 0.0015]; K=10 delta=-0.0002, 95% CI [-0.0013, 0.0009].
- oracle-label_minus_label-blind: K=1 delta=-0.0011, 95% CI [-0.0091, 0.0071]; K=3 delta=-0.0004, 95% CI [-0.0027, 0.0018]; K=5 delta=-0.0004, 95% CI [-0.0014, 0.0007]; K=10 delta=0.0002, 95% CI [-0.0008, 0.0011].
- predicted-label_minus_label-blind: K=1 delta=-0.0055, 95% CI [-0.0149, 0.0035]; K=3 delta=-0.0017, 95% CI [-0.0047, 0.0012]; K=5 delta=-0.0004, 95% CI [-0.0018, 0.0008]; K=10 delta=0.0004, 95% CI [-0.0003, 0.0013].

## Failures and next gate

- Recorded protocol failures: 0.
- Complete the remaining four seeds before confirmatory claims or canonical manuscript tables.
- Preserve oracle-label only as a conditional upper-bound protocol.
- Retain the title-audit caveat and consider redirect/content fingerprint auditing as an additional robustness check.
