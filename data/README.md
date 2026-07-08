# Data

```text
data/
  raw/        Original data and simulator exports. Usually not committed.
  interim/    Intermediate transformed files. Usually not committed.
  processed/  Benchmark-ready datasets. Usually not committed.
  metadata/   Small registries and schemas that are safe to commit.
  public_datasets/ Public benchmark caches, metadata pages, and manifests.
```

Record dataset contracts under `configs/datasets/` and large-file acquisition steps in `docs/benchmark_design/data_pipeline.md`.

The global public dataset registry is maintained at `knowledge_base/datasets/public_dataset_registry.md`.
