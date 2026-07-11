from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from powergrid_benchmark.mintou_experiments import MINTOU_ROOT, PAPERS, PaperSpec, run_all


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def table(items: tuple[str, ...]) -> str:
    return "\n".join(f"- {item}" for item in items)


def core_claims(paper: PaperSpec) -> str:
    return f"""# Claims

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 | `{paper.algorithm_name}` improves the target downstream task against target-journal-level baselines. | Planned; smoke-tested only | E-main |
| C2 | The named algorithmic component contributes independently beyond the strongest ablation. | Planned; smoke-tested only | E-ablation |
| C3 | The method remains feasible or robust under stress/scenario experiments. | Planned; smoke-tested only | E-robust |
| C4 | The experiment package is reproducible from public or benchmark-derived data. | Scaffolded | E-repro |

Exact numerical manuscript claims are prohibited until public benchmark runs replace the synthetic smoke benchmark.
"""


def experiments_md(paper: PaperSpec) -> str:
    lines = [
        "# Experiments",
        "",
        "Status: all planned experiment slots are implemented as deterministic synthetic smoke tests. They must be upgraded to full public-benchmark simulations before submission.",
        "",
        "## Main Experiments",
        "",
        "| Experiment ID | Purpose | Evidence | Status |",
        "|---|---|---|---|",
    ]
    for exp in paper.main_experiments:
        lines.append(f"| `{exp}` | Validate `{paper.task}` under `{exp}` scenario. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |")
    lines.extend(
        [
            "",
            "## Ablation Experiments",
            "",
            "| Ablation | Purpose | Evidence | Status |",
            "|---|---|---|---|",
        ]
    )
    for ablation in paper.ablations:
        lines.append(f"| `{ablation}` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |")
    lines.extend(
        [
            "",
            "## Metrics",
            "",
            table(paper.metrics),
        ]
    )
    return "\n".join(lines) + "\n"


def build_project(paper: PaperSpec) -> None:
    root = MINTOU_ROOT / paper.directory
    for subdir in [
        "logic/solution",
        "src/code",
        "src/configs",
        "trace",
        "evidence/runs",
        "evidence/tables",
        "evidence/figures",
        "evidence/source",
    ]:
        (root / subdir).mkdir(parents=True, exist_ok=True)

    write_text(
        root / "PAPER.md",
        f"""---
title: "{paper.title}"
tag: "{paper.tag}"
paper_id: "{paper.paper_id}"
status: "project_original_planned"
target_journal: "{paper.target_journal}"
backup_journal: "{paper.backup_journal}"
algorithm: "{paper.algorithm_name}"
---

# {paper.title}

## Algorithm Identity

- Short name: `{paper.algorithm_name}`
- Full name: {paper.algorithm_full_name}
- Tag: `{paper.tag}`
- Target journal: {paper.target_journal}
- Backup journal: {paper.backup_journal}

## Abstract

{paper.abstract}

## Current Engineering Status

The ARA structure, experiment manifest, baseline/ablation matrix, and deterministic synthetic smoke benchmark are implemented. Public benchmark simulation remains required before submission-level numerical claims.
""",
    )

    write_text(
        root / "logic/problem.md",
        f"""# Problem

## Downstream Task

{paper.task}

## Target-Journal Gap

The local comparator ARA collection shows that recent target-journal papers already cover many conventional baselines. This paper must therefore prove the incremental value of `{paper.algorithm_name}` through stronger baseline coverage, ablation isolation, and reproducible public data.

## Datasets

{table(paper.datasets)}
""",
    )
    write_text(root / "logic/claims.md", core_claims(paper))
    write_text(
        root / "logic/concepts.md",
        f"""# Concepts

| Concept | Definition |
|---|---|
| `{paper.algorithm_name}` | {paper.algorithm_full_name}. |
| Downstream task | {paper.task}. |
| Synthetic smoke benchmark v0 | Deterministic benchmark-derived scenario generator used to validate experiment wiring only. |
| Public benchmark run | Future full experiment using the local public dataset pool and task-specific simulators. |
""",
    )
    write_text(root / "logic/experiments.md", experiments_md(paper))
    write_text(
        root / "logic/related_work.md",
        """# Related Work

Comparator evidence source: `papers/literature/target_journal_related/comparison_analysis.md`.

This project is project-original planned work and must remain separate from the external published-paper ARA collection.
""",
    )
    write_text(
        root / "logic/solution/constraints.md",
        """# Constraints

- Do not claim synthetic smoke benchmark numbers as final manuscript results.
- Do not fabricate or manually alter experimental outputs.
- If early results are weak, use compliant optimization only: feature engineering, scenario selection, hyperparameter tuning, baseline audit, and clearer task framing.
- Keep every result table in `evidence/` and every interpretation in `logic/` or analysis markdown.
""",
    )
    write_text(
        root / "logic/solution/method.md",
        f"""# Method

## Main Algorithm

`{paper.algorithm_name}`: {paper.algorithm_full_name}

## Innovation Handles

{table(paper.innovations)}

## Baseline Coverage

{table(tuple(method.name for method in paper.baselines))}

## Ablation Coverage

{table(paper.ablations)}
""",
    )
    write_text(
        root / "src/environment.md",
        """# Environment

Current smoke experiments use Python standard library only.

Run:

```powershell
$env:PYTHONPATH='src'
python -m powergrid_benchmark.mintou_experiments
```

Future public benchmark runs may require pandapower, numpy, scipy, torch, grid2op, or other task-specific dependencies.
""",
    )
    write_text(
        root / "src/code/run_experiments.py",
        f"""from pathlib import Path

from powergrid_benchmark.mintou_experiments import MINTOU_ROOT, paper_by_id, run_paper


if __name__ == "__main__":
    paper = paper_by_id("{paper.paper_id}")
    run_paper(paper, MINTOU_ROOT / paper.directory)
""",
    )
    write_text(
        root / "evidence/README.md",
        """# Evidence

- `evidence/runs/synthetic_smoke_results.csv`: deterministic smoke benchmark outputs.
- `evidence/tables/synthetic_smoke_leaderboard.csv`: method-level aggregate table.
- `evidence/runs/analysis.md`: interpretation boundary and next optimization action.
- `src/configs/experiment_manifest.json`: experiment, baseline, ablation, dataset, and metric manifest.

These files validate the ARA and experiment pipeline. They do not yet constitute final public benchmark results.
""",
    )
    write_text(
        root / "evidence/figures/README.md",
        "# Figures\n\nFigures will be generated after public benchmark result tables are upgraded beyond synthetic smoke tests.\n",
    )
    write_text(
        root / "trace/exploration_tree.yaml",
        f"""version: 1
paper_id: {paper.paper_id}
tag: mintou
nodes:
  - id: root
    type: planning
    status: done
    provenance: ai-executed
    support_level: explicit
    summary: "Create independent ARA project for {paper.algorithm_name}."
    children:
      - experiment_matrix
      - smoke_benchmark
      - public_benchmark_upgrade
  - id: experiment_matrix
    type: decision
    status: done
    provenance: ai-executed
    support_level: explicit
    summary: "Define target-journal-level baselines, ablations, metrics, and datasets."
    children: []
  - id: smoke_benchmark
    type: experiment
    status: done
    provenance: ai-executed
    support_level: explicit
    summary: "Run deterministic synthetic smoke benchmark for pipeline validation."
    children: []
  - id: public_benchmark_upgrade
    type: experiment
    status: planned
    provenance: ai-suggested
    support_level: explicit
    summary: "Replace smoke results with full public benchmark simulations."
    children: []
""",
    )


def write_collection_manifest() -> None:
    rows = []
    for paper in PAPERS:
        rows.append(
            {
                "paper_id": paper.paper_id,
                "tag": paper.tag,
                "directory": paper.directory,
                "title": paper.title,
                "algorithm_name": paper.algorithm_name,
                "algorithm_full_name": paper.algorithm_full_name,
                "target_journal": paper.target_journal,
                "backup_journal": paper.backup_journal,
                "main_experiments": str(len(paper.main_experiments)),
                "ablations": str(len(paper.ablations)),
                "baseline_methods": str(len(paper.baselines)),
            }
        )
    path = MINTOU_ROOT / "manifest.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    write_text(
        MINTOU_ROOT / "README.md",
        """# Mintou Six-Paper ARA Projects

This directory contains six independent project-original ARA engineering packages for the `mintou` paper portfolio.

Current status:

- Six independent ARA directories are scaffolded.
- Each paper has a named academic algorithm, target journal, baselines, ablations, datasets, and metrics.
- Deterministic synthetic smoke benchmark v0 is implemented and run for every paper.
- Public benchmark simulation remains required before final manuscript claims.

See `manifest.csv` for the portfolio index.
""",
    )


def main() -> int:
    for paper in PAPERS:
        build_project(paper)
    write_collection_manifest()
    run_all(MINTOU_ROOT)
    print(f"scaffolded: {len(PAPERS)} projects under {MINTOU_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
