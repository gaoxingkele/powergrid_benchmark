# W3 SimBench SQLite Pilot Report

## Outcome

The SimBench pilot is a complete, deterministic **data-engineering feasibility artifact** for MA-SQLGrid. It is not a human-gold benchmark and is not a sealed test. All 36 natural-language/SQL pairs carry `AUTO_CANDIDATE`, `human_gold=False`, and `sealed=False`.

Selected network: `1-MV-urban--0-sw` (urban medium-voltage distribution grid with upstream high-voltage connection). This network was selected because one coherent case covers topology, 110/10 kV voltage levels, loads, distributed renewable generation, transformers, lines, and switching assets.

## Source and license audit

| Item | Frozen value |
|---|---|
| Upstream repository | `https://github.com/e2nIEE/simbench` |
| Local repository commit | `c426a1a3fecbe986a868edc2beed56349c37baf7` |
| SimBench package used | 1.6.2 |
| Database license | Open Database License (ODbL) 1.0 |
| Individual database contents | Database Contents License (DbCL) 1.0 |
| SimBench code | BSD 3-Clause |
| Hashed source inputs | 17 network CSV files + `LICENSE` + `AUTHORS` |

The upstream `LICENSE` is copied verbatim to `UPSTREAM_LICENSE.txt`. `source_manifest.json` records the local source path, commit, remote URL, each source file's byte length and SHA-256, and the database/software license distinction. The generated SQLite database is treated as a transformed/derived database. Attribution must be preserved, and ODbL share-alike obligations must be reviewed before public redistribution; this report is not legal advice.

## SQLite contents

| Table | Rows | Purpose |
|---|---:|---|
| `networks` | 1 | Selected case and scenario metadata |
| `voltage_levels` | 2 | Derived 110/10 kV dimension and bus counts |
| `buses` | 144 | Distribution topology nodes and voltage constraints |
| `lines` | 147 | Directed endpoint representation and electrical/length attributes |
| `transformers` | 2 | HV/LV connectivity, ratings and tap metadata |
| `loads` | 139 | Connected load assets, active/reactive power and profiles |
| `generators` | 134 | Distributed renewable generation and profiles |
| `switches` | 305 | Bus-to-element switching topology and open/closed state |

The dictionary contains 82 fields with SQLite type, nullability, primary/foreign-key status, upstream table mapping, and a plain-language definition. SQLite `integrity_check` returns `ok`; `foreign_key_check` returns no violations.

Frozen database SHA-256 after deterministic rebuild:

```text
01d0cd9da3ab15a6dca2709546ddc6acc33b3a3887defef7060caf5b02cf5524
```

## Candidate NL–SQL design

There are 36 deterministic candidates, exactly six in each requested query class:

| Template family | Query class | Split | Count |
|---|---|---|---:|
| `asset_inventory` | single-table | `development_candidate` | 6 |
| `threshold_filter` | filter | `development_candidate` | 6 |
| `asset_aggregation` | aggregate | `evaluation_candidate` | 6 |
| `cross_asset_join` | join | `evaluation_candidate` | 6 |
| `ranked_assets` | top-k | `evaluation_candidate` | 6 |
| `network_topology` | topology | `evaluation_candidate` | 6 |

Splits are assigned at template-family level: no family appears in more than one split. The word `test` is deliberately not used for the current automatic evaluation partition, because this pilot is development-visible and has not been independently authored or reviewed.

Every query is a read-only single `SELECT` or `WITH` statement. Execution records retain column names, complete normalized result rows, row count and SHA-256. Four candidates (`SB-AUTO-008`, `009`, `010`, and `035`) return zero rows and are retained intentionally to cover legitimate empty-answer behavior; they require human review before any benchmark freeze. Across all candidates, stored results contain 100 rows, with at most 15 rows for one question.

## Reproducibility and validation

Build:

```powershell
python build_simbench_pilot.py
```

Validation:

```powershell
python -m unittest -v test_simbench_pilot.py
```

Observed validation result:

```text
Ran 6 tests in 9.933s
OK
```

The tests cover:

1. required artifacts and exact license classes;
2. SQLite integrity, foreign keys, row counts and 110/10 kV coverage;
3. `AUTO_CANDIDATE`/non-human/non-sealed status, six query classes and family-level split isolation;
4. independent re-execution of all 36 SQL statements and exact result-hash agreement;
5. byte length and SHA-256 of every listed artifact;
6. rebuild in a fresh temporary directory with byte-identical schema, questions, results, dictionary, data card and SQLite database.

## Artifact inventory

- `simbench_mv_urban.sqlite`: deterministic derived database.
- `schema.sql`: complete DDL, constraints, foreign keys and indexes.
- `field_dictionary.csv`: 82-field dictionary and source mapping.
- `source_manifest.json`: source, commit, license and per-source-file hashes.
- `UPSTREAM_LICENSE.txt`: verbatim upstream license notice.
- `questions_auto_candidate.csv`: deterministic NL–SQL candidates and family splits.
- `gold_execution_results.jsonl`: executed results and result hashes. Here “gold execution” means execution of the registered reference SQL; it does **not** mean human-gold language annotation.
- `data_card.json`: counts, status and limitations.
- `artifact_hashes.json`: byte length and SHA-256 for every data artifact.
- `build_simbench_pilot.py` and `test_simbench_pilot.py`: build and verification code.

## Promotion gate and limitations

This pilot may support schema/context pipeline testing now. It may enter a paper's quantitative main table only after all of the following:

1. two independent reviewers check natural-language intent against SQL and result semantics;
2. disagreements and empty-result cases are adjudicated with a recorded audit trail;
3. wording is de-templated without changing intent, and duplicate/paraphrase leakage is tested;
4. a new family-isolated split is frozen with content, schema, question and result hashes;
5. the final evaluation set is not used for prompt, repair-rule, threshold or model selection;
6. the derived-database redistribution plan receives an ODbL/DbCL compliance decision;
7. the experiment artifact reaches the project's E4 evidence level.

Current limitations are one network, automatic questions, no independent domain review, no human-authored questions, and no sealed test. Accordingly, no claim of human-gold quality, natural-query representativeness, or cross-network generalization is permitted.
