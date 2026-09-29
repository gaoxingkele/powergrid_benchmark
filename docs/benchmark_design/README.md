# Benchmark Design

This directory stores stable design decisions for the shared benchmark.

Active files:

- `grid_tracking_targets.md`: **电网 Benchmark 跟踪目标**（PG-T01…T24）— 论文/GitHub/数据集检索与本地缓存对照（与三地申报脱钩）。
- `config_schema.md`: required fields for experiment configs.

Recommended files to add as the benchmark matures:

- `task_taxonomy.md`: task families, inputs, outputs, and comparability rules.
- `data_pipeline.md`: ingestion, cleaning, simulation, and leakage checks.
- `system_registry.md`: grid systems and simulator assumptions.
- `reproduction_protocol.md`: hardware, seeds, result acceptance, and failure logging.
