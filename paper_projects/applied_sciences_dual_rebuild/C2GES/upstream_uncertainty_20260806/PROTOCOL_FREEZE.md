# C2GES upstream-uncertainty protocol freeze

The five-seed results in the current manuscript reuse one grouped out-of-fold upstream role ledger. Their variation therefore covers downstream training but not alternative upstream folds, refits, or probability estimates. This protocol freezes a complete 5-by-5 upstream--downstream matrix before any new result is generated.

## Design

- Data: the existing document-grouped FEVER conversion, limited to 8,000/1,500/1,500 train/development/test instances.
- Upstream role classifier: the existing TF--IDF/logistic pipeline, with five independent `StratifiedGroupKFold` partitions using seeds 3101--3105. Training predictions are out of fold by source document; development and test predictions come from a model fitted only on the training split.
- Downstream selector: the existing predicted-label C2GES implementation, trained with seeds 2026--2030 for every upstream ledger.
- Matrix: five upstream ledgers by five downstream seeds, for 25 complete selector runs and approximately 1.35 million prediction rows over K=1/3/5/10.
- Primary operating point: K=3. Other cutoffs are sensitivity analyses and cannot replace the primary result.

## Statistical boundary

The analysis will retain every frozen cell and use the source document as the cluster. It will report the grand mean, upstream-ledger means, downstream-seed means, and the variance attributable to upstream, downstream, and residual interaction terms. Document-clustered intervals will retain complete upstream--downstream bundles. The primary comparison family and Holm correction are specified before outcome inspection.

This experiment measures uncertainty on FEVER. It cannot establish power-grid-domain accuracy, expert usefulness, or NERC performance.

## Integrity and stopping

The runner refuses code or data hash drift and refuses an existing formal output root. Every child uses a fresh directory. A failure is retained with its logs and incident record; no seed, model, cutoff, or data item may be substituted. The run is not stopped for an unfavorable direction or lack of statistical significance.
