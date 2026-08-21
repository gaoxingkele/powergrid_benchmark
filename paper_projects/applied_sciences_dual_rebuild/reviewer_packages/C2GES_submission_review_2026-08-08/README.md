# C2GES Submission-Version Reviewer Package

Prepared: 2026-08-08 (Asia/Shanghai)

This private package supports editorial and peer-review verification of the
Applied Sciences submission version. It complements the public project-code
repository at <https://github.com/gaoxingkele/c2ges>.

## Included

- the submission-version manuscript source, bibliography, verification scripts,
  generated result fragments, and compiled PDF;
- every hash-bound source named by the manuscript claim/source map, including
  the five-seed, structural-ablation, MiniLM/BGE, and crossed 5-by-5 analysis
  summaries and the BGE prediction ledger;
- the development and frozen NERC machine-silver protocols, label ledgers,
  adjudication outputs, manifests, and statistics used for the annotation-process
  statements in the manuscript; and
- `SHA256SUMS.csv`, which binds every packaged file.

## Deliberately excluded

- API credentials, environment files, model weights, and local caches;
- NERC source PDFs and other downloaded third-party source documents;
- superseded or smoke-run outputs not used by the manuscript; and
- materials whose redistribution is not authorized by the applicable license.

The excluded third-party materials may be inspected through the corresponding
author when permission permits. They must not be redistributed by recipients.
The NERC records in this package are machine-adjudicated silver labels, not
human or domain-expert ground truth.

Corresponding author: Yang Yong. The correspondence email will be supplied by
the author before submission.
