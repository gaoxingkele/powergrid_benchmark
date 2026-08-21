# Shared experiment statistics and artifact audit

`stat_audit.py` is the common acceptance gate for MA-SQLGrid and C2GES
instance-level result files. It accepts UTF-8 CSV or JSONL and produces both a
machine-readable JSON report and a reviewer-friendly Markdown report.

It checks:

- required columns and non-empty values;
- uniqueness of `condition × item` identities;
- the complete `condition × item` Cartesian product;
- one stable cluster assignment per item and equal cluster coverage;
- hexadecimal provenance hashes and their invariance across conditions;
- paired cluster-bootstrap confidence intervals;
- exact McNemar tests for binary metrics;
- Holm family-wise multiplicity correction over all applicable comparisons.

Only unique complete pairs enter statistical comparisons. A strict audit defect
returns exit code 2, so the command can be used as a pipeline gate.

## MA-SQLGrid example

```powershell
python stat_audit.py results.csv `
  --condition-field condition `
  --item-fields question_id `
  --cluster-field question_id `
  --metrics strict_execution_correct,set_execution_correct,shape_correct `
  --conditions Full+Shape,Full+NoShape,Compact+Shape,Compact+NoShape `
  --required-fields run_id,model,seed,database_id,prediction `
  --hash-fields input_hash,schema_hash `
  --json-out audit/ma_stats.json `
  --markdown-out audit/ma_stats.md
```

If multiple seeds are stored in one file, include the seed in the paired
identity: `--item-fields question_id,model,seed`. A coarser cluster such as
`database_id` can be chosen when the scientific design requires database-level
rather than question-level resampling.

## C2GES example

```powershell
python stat_audit.py results.jsonl `
  --condition-field method `
  --item-fields instance_id,seed `
  --cluster-field document_id `
  --metrics evidence_hit,recall_at_5 `
  --conditions BM25,C2GES `
  --required-fields run_id,split,query_id,prediction `
  --hash-fields input_hash,corpus_hash `
  --json-out audit/c2ges_stats.json `
  --markdown-out audit/c2ges_stats.md
```

Hash options are intended for input/provenance hashes that must remain identical
for the same paired item across methods. Output hashes, which naturally differ
by method, should be retained in the artifact but not passed to `--hash-fields`.

## Tests

From this directory:

```powershell
python -m unittest -v test_stat_audit.py
```

The synthetic tests cover a passing paired design, dirty Cartesian products,
duplicate identities, cluster mismatch, malformed/inconsistent hashes, Holm
adjustment, JSONL input, and end-to-end CLI report generation.
