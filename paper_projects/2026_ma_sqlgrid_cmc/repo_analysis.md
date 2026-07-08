# Repository Analysis

## Repository

This is an uploaded Paper Refine workspace, not an external GitHub repository.
The original zip contained an embedded `.git`; it was intentionally excluded from the benchmark-managed copy.

## License

Not specified in provided sources.

## Environment

- Experiment setup: `source/code/experiment_final/setup.py`
- Evaluator package: `source/code/evaluator/`
- Dataset: `source/data/griddb_maintenance_v2_v0_1/`
- Local `pdflatex` was not found in the current Windows environment.

## Data Dependencies

The package includes the local SQLite dataset:

- `source/data/griddb_maintenance_v2_v0_1/database.sqlite`
- `source/data/griddb_maintenance_v2_v0_1/questions.jsonl`
- `source/data/griddb_maintenance_v2_v0_1/schema.sql`
- `source/data/griddb_maintenance_v2_v0_1/splits.json`

## Entrypoints

- Manuscript: `source/manuscript/paper.tex`
- Setup: `python source/code/experiment_final/setup.py`
- Evaluator tests: `pytest -q source/code/evaluator/tests`
- Final experiment code: `source/code/experiment_final/main.py`

## Reusable Components

- Final manuscript and verified bibliography.
- GridDB-Maintenance-v2 v0.1 dataset.
- Evaluator and experiment code.
- Main result, ablation, validator, and mechanism diagnostic evidence.
- Harness approval records.

## Integration Notes

The evaluator tests currently expect data under `source/code/data/...`, while the imported package stores data under `source/data/...`. This is a packaging-path issue to repair before using the tests as a quality gate.

## Reproducibility Risks

- Path mismatch in evaluator tests.
- Protocol-B formal result is a single deterministic pass, not multi-seed inference.
- Claims are local to GridDB-Maintenance-v2 v0.1 and should not be generalized to Spider/BIRD-style external benchmarks without new experiments.
