# Powergrid Benchmark

This workspace is for engineering benchmark studies at the intersection of power systems and computer science. The primary sources are journal and conference papers, with each selected paper represented as an Agent-Native Research Artifact (ARA). GitHub repositories are treated as upstream evidence and reproducibility inputs.

## Directory Map

```text
powergrid_benchmark/
  ara_artifacts/          One ARA package per paper or benchmark case.
  configs/                Shared dataset, system, model, metric, split, and experiment configs.
  data/                   Local data area. Keep large/raw/generated data out of git.
  docs/                   Benchmark design notes, literature notes, reports, and theory.
  env/                    Environment notes and reproducibility manifests.
  experiments/            Runnable experiment definitions and result summaries.
  external_repos/         Cloned upstream GitHub repositories, one repo per directory.
  knowledge_base/         Global dataset, task, baseline, literature, and update wiki.
  notebooks/              Exploratory notebooks.
  paper/                  Optional paper draft or benchmark survey manuscript.
  paper_projects/         One engineering reproduction project per selected paper.
  papers/                 PDFs, metadata, BibTeX, and extracted text.
  scripts/                Utility scripts for acquisition, preprocessing, runs, and validation.
  src/                    Shared benchmark code.
  tests/                  Tests for shared benchmark utilities and repository contracts.
  research_wiki/          Methodology evolution, paper idea logic, and research logs.
```

## Workflow

1. Register candidate papers in `papers/metadata/paper_registry.csv`.
2. Store PDFs under `papers/raw/` and extracted text under `papers/extracted_text/`.
3. Create one ARA package from `ara_artifacts/_template/` for every paper promoted into the benchmark.
4. Create one engineering project from `paper_projects/_template/` when implementation or reproduction work starts.
5. Clone official or strong community GitHub repositories into `external_repos/owner__repo`.
6. Describe datasets, grid systems, splits, models, metrics, and experiments under `configs/`.
7. Run reproducible experiments into `experiments/runs/` and summarize stable findings in `docs/reports/`.

## Global Knowledge Base

The shared benchmark foundation lives under `knowledge_base/`.

- Dataset registry: `knowledge_base/datasets/public_dataset_registry.md`
- Task taxonomy: `knowledge_base/tasks/task_taxonomy.md`
- Baseline matrix: `knowledge_base/algorithms/baseline_matrix.md`
- Recent literature map: `knowledge_base/literature/recent_2024_2026_literature_map.md`
- Update protocol: `knowledge_base/wiki/how_to_update.md`

Public dataset caches and metadata live under `data/public_datasets/`. Use:

```powershell
python scripts/data_acquisition/audit_public_datasets.py
python scripts/data_acquisition/download_public_datasets.py
```

## Research Wiki

The independent research wiki lives under `research_wiki/`. It records methodology evolution, paper-idea extraction, evidence gaps, and audit-friendly thinking summaries.

Use the structured logger when a work round adds research value:

```powershell
python scripts/wiki/log_research_event.py --title "event title" --observation "..." --action "..." --rationale "..." --evidence "..." --impact "..." --next "..."
```

The wiki does not store hidden chain-of-thought. It stores decision paths, rationale summaries, and method evolution.

## Naming Convention

Use stable paper IDs:

```text
YYYY_short_title_first_author
```

Examples:

```text
2024_grid_gnn_fault_li
2025_power_load_transformer_wang
```

Use stable GitHub repo IDs:

```text
owner__repo
```

Example:

```text
lanl-ansi__grid-network-toolkit
```

## ARA Contract

Each benchmarked paper should have a package shaped like:

```text
ara_artifacts/YYYY_short_title_author/
  PAPER.md
  logic/
    problem.md
    claims.md
    concepts.md
    experiments.md
    related_work.md
    solution/
      constraints.md
      method.md
  src/
    environment.md
    configs/
  trace/
    exploration_tree.yaml
  evidence/
    README.md
    source/
    tables/
    figures/
    runs/
```

Claims must point to experiment IDs or evidence files. Raw evidence belongs in `evidence/`; interpretation belongs in `logic/`.
