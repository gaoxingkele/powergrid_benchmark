# MA-SQLGrid canonical v2 independent reanalysis

**Decision: PASS.** No model was run; the manuscript and prior canonical release were not modified.

## Corrected endpoint

The inferential structural endpoint is deliberately narrow: successful SQLite execution with the number of projected result columns equal to one frozen, project-authored target for that question in every condition. The implemented evidence does not validate row granularity, ordering correctness, or semantic correctness.

## Main correction

- Qwen common-target structural-hint main effect: +0.4083, 95% template-cluster bootstrap CI [+0.2115, +0.6122] (old condition-dependent value +0.4944).
- Granite common-target structural-hint main effect: +0.3556, 95% CI [+0.1352, +0.5793] (old condition-dependent value +0.4528).
- All 1440 execution outcomes are unchanged and independently reproduced from the accepted prediction ledgers.

## Inference

Twenty-thousand cluster bootstrap draws preserve all rows within each of 70 normalized-gold-SQL template clusters. Inferential p-values use 100,000 Monte Carlo sign flips at that same cluster unit. Holm adjustment is applied separately to exactly three documented eight-test families. Question-level McNemar discordances and p-values are retained only as descriptive sensitivity fields.

## Intervention boundary

The context factor is a bundled package, not isolated schema compactness: full schema plus a global value dictionary is compared with selected schema plus question-matched values and handcrafted normalization hints. The hint factor is a corpus-tailored structural/SQL-operation package. Gold tables and columns are used only in the offline selector audit.

## Granite p-value correction

The archived question-level exact McNemar result for Granite structural hints at compact context on execution was raw p=3.1028e-7 and Holm p=1.8617e-6; 1.86e-4 was a transcription error. The v2 release replaces that inferential use with the cluster-aware randomization result in `tables/cluster_randomization_holm_v2.csv`.
