# Constraints

## Data Constraints

Claims are local to `GridDB-Maintenance-v2 v0.1`; no Spider/BIRD-style external benchmark claim is supported by the uploaded package.

## Simulator Constraints

No power-system simulator is involved. The benchmark uses a local SQLite maintenance database.

## Compute Constraints

The manuscript reports an NVIDIA RTX A6000 with 49140 MB VRAM for the local run.

## Reproducibility Constraints

Evaluator tests currently resolve dataset paths to `source/code/data/...`, but the package stores data under `source/data/...`.
