# MA-SQLGrid Round-1 revision assets

This directory is an isolated authoring package prepared from the executed code and frozen artifacts. It does **not** modify the manuscript, `canonical_dual_backbone/`, or any v2 reanalysis directory.

## Contents

- `METHOD_AND_PROMPT_ASSETS.md`: self-contained Algorithm 1, four-cell prompt excerpts, and the factor audit matrix.
- `GRIDDB_DATA_CARD.md`: GridDB construction, contents, question structure, exposure, and licensing boundary.
- `DKASQL_COMPARATOR.md`: closest-work table with no imported performance numbers.
- `ROUND1_BLOCKERS_AND_EXPERIMENT_SPECS.md`: human blockers and immediately executable experiment specifications.
- `FACT_PROVENANCE.md`: code/artifact locations supporting every material statement.
- `generate_framework_figures.py`: deterministic generator for the three revised framework diagrams.
- `figures/`: SVG, PDF, and 450 dpi PNG exports.
- `qa/page_scale_preview.pdf` and `VISUAL_QA.md`: page-width visual-QA record.

## Required terminology

The executed first factor is a **context-package factor**, not an isolated schema-length factor:

- full package = all eight-table DDL plus the global permitted value dictionary;
- compact package = question-conditioned selected tables/columns and join paths plus matched values and handcrafted domain-normalization rules.

The second factor is a **question-derived composite structural/SQL-operation hint**, not a pure answer-format hint. It can specify projected-column count, row granularity, ordering, aggregation, grouping/HAVING, projection fields, or LIMIT behavior.

The canonical formal path makes one model call per question/cell/backbone. It parses one SQL candidate and validates/executes it; it does not perform candidate generation, ranking, or repair.

