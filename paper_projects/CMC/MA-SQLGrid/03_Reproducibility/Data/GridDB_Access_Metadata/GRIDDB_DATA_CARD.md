# GridDB-Maintenance-v2 v0.1 data card

## Intended use and non-use

GridDB is a small, synthetic, deterministic SQLite case study for controlled Text-to-SQL experiments. It is not operational utility data, does not represent production scale, and cannot alone establish cross-database or field effectiveness.

## Database contents

| Table | Rows | Role |
|---|---:|---|
| `asset_types` | 6 | equipment categories and engineering attributes |
| `assets` | 18 | named assets, type/location links, status and capacity |
| `grid_topology` | 9 | directed asset connections and switch state |
| `locations` | 8 | site, region, coordinates and criticality |
| `maintenance_logs` | 8 | performed actions, timing, notes and parts cost |
| `sensor_readings` | 26 | timestamped values, units and alarm flags |
| `technicians` | 8 | staff specialty, region and active flag |
| `work_orders` | 15 | asset/technician assignments, priority, status and dates |
| **Total** | **98** | **8 tables** |

## Questions, split, and construction

- 200 authored/expanded natural-language–SQL records: 20 development (`Q001`–`Q020`) and 180 test (`Q021`–`Q200`).
- Each record stores question, gold SQL, order sensitivity, requested answer shape, SQL feature tags, involved tables/columns, required literals, difficulty, and split.
- Every reference SQL statement was executed during dataset generation; the frozen verification log reports PASS for all 200.
- `Q081`–`Q200` are deterministic template expansions over the same schema, values, and execution checker. Thus the nominal test split is held out from the formal model run but not an independently authored or development-unexposed benchmark.

## Difficulty and structural coverage

| Partition | Easy | Medium | Hard | Total |
|---|---:|---:|---:|---:|
| Full corpus | 74 | 102 | 24 | 200 |
| Formal test | 66 | 91 | 23 | 180 |

The annotation protocol lists filters, joins, aggregation, grouping/HAVING, date predicates, top-k/order-sensitive requests, NULL checks, scalar SQLite functions, topology joins, parameterized domain values, and executable-but-wrong value traps. The formal test contains 70 normalized-gold-SQL structural clusters after string and numeric literals are replaced. This clustering is an analysis construct, not an authored template identifier. Cluster sizes range from 1 to 19, and 58 clusters are singletons.

Feature-tag counts in the 180-item formal test are overlapping: filter 170, order-by 114, join 102, aggregation 59, floating-point result 36, time predicate 30, top-k 18, group-by 12, topology traversal 11, self-join 9, nested query 6, distinct 3, having 2, pattern 2, scalar function 2, left join 2, and NULL 1. They are not mutually exclusive “question families.” The dataset has no authored family or template-ID field.

## Empty results and result-state dependence

Five of 200 gold queries return zero rows on the frozen snapshot (`Q073`, `Q104`, `Q107`, `Q110`, `Q140`), all in the formal test: 5/180 = 2.78%. Execution equality is measured on this one state and may accept accidentally equivalent SQL; the dataset does not include counterfactual/test-suite database states.

## Exposure and annotation status

- Questions and rule patterns were available during earlier method development.
- The compact selector and composite hint inventory are tailored to recurring GridDB language.
- The formal Qwen and Granite runs are frozen one-pass executions, but this does not make the corpus prospectively sealed.
- No independent dual-expert semantic review of the 200 GridDB question–SQL pairs is documented in the current package.

## Provenance, redistribution, and license

The local annotation protocol states that the schema adapts an earlier project pilot and that deterministic rows/questions were produced by the project build script. The current manuscript review records unresolved GridDB redistribution permission. Consequently:

- hashes and local reproducibility are available;
- public redistribution must remain blocked until the author/license owner records an explicit license or written permission;
- no open-data or public-domain status may be inferred;
- a public archive must either include permission-cleared files or a genuinely lawful regeneration route and precisely list exclusions.
