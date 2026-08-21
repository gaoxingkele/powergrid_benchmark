# Method and prompt assets

## Algorithm 1: executed MA-SQLGrid factorial pipeline

**Inputs:** natural-language question `q`; read-only SQLite snapshot `D`; DDL `S`; frozen model snapshot `M`; condition `(c,h)` where `c in {FULL, COMPACT}` and `h in {0,1}`; run/configuration identifiers. Gold SQL and gold results are excluded from Steps 1--8.

**Output:** one terminal ledger row containing the raw response, parsed SQL if present, safety/execution status, hashes, timing/token telemetry, and—only after generation—the offline score.

```text
1  Assert that the prompt-path record contains none of
     {gold_sql, gold_result(s), answer(s)}.
2  Introspect/freeze schema metadata: tables, columns, primary keys,
     foreign keys, descriptions, and permitted database values.
3  Build GLOBAL VALUE INVENTORY V:
     for each permitted non-ID categorical/date/text column, select at most
     80 distinct non-null values in sorted order; numeric flags are included
     for domain-context construction but most IDs and continuous measures are excluded.
4  Build FULL CONTEXT PACKAGE P_full:
     complete eight-table DDL || global value dictionary V.
5  Build COMPACT DOMAIN-GROUNDED PACKAGE P_compact(q):
     a. tokenize q after fixed stop-word removal;
     b. exact-match permitted values, then prune known ambiguous matches;
     c. fire frozen corpus-tailored synonym, column-phrase, date/numeric,
        topology, aggregation, and domain-literal rules;
     d. select seed tables/columns; expand the foreign-key graph to at most
        six related tables; retain identifier and connecting FK columns;
     e. serialize selected tables/columns, retained join paths, matched values,
        and normalization/predicate hints.
6  Derive COMPOSITE STRUCTURAL/SQL-OPERATION HINT H(q):
     expected projected-column count, row granularity, ordering need, and
     applicable corpus-tailored instructions for COUNT/AVG/SUM/MIN/MAX,
     GROUP BY/HAVING, exact projections, ordering, or LIMIT.
7  Assemble context C:
     if c=FULL, C=P_full; if c=COMPACT, C=P_compact(q);
     if h=1, append/retain H(q); if h=0, remove H(q).
8  Serialize the common system instruction, condition label, C, stable
     question ID, and q. Hash both prompt and context. Verify that the literal
     gold SQL is absent.
9  Make exactly one deterministic model request for this backbone/run.
10 Parse once: remove an optional Markdown SQL fence, begin at the first
     WITH/SELECT token, collapse whitespace, and retain text through the first
     semicolon (or append one). No candidate ranking or repair is executed.
11 Validate the parsed candidate: require exactly one parsed statement whose
     leading form is SELECT or WITH; reject forbidden write/schema-changing
     tokens. Execute admissible SQL on the frozen database.
12 Write the terminal ledger row with question/cell/model/run IDs; prompt,
     context, response, data, code, and configuration hashes; raw response;
     parsed SQL; status/error; latency; input/output tokens; and retry count.
13 Only after Step 12, compare the executed result with the frozen reference
     result for offline evaluation. The reference never selects or repairs SQL.
```

### Boundary that must accompany Algorithm 1

`extract_sql` retains the first candidate through its first semicolon before the evaluator sees it. Therefore the safety claim is “the parsed candidate passed the single-statement read-only validator,” not “the raw response was proven to contain no later SQL text.” The current formal run is one generation per prompt; the older multi-candidate/ranker/repair pilot is not part of this algorithm.

## Representative four-cell prompt excerpts (Q041)

Common instruction and question in all four records:

```text
Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, or multiple statements.
...
Question ID: Q041
Question: How many alarmed readings does each asset have?
```

F00—full package, no composite hint:

```text
Condition: F00_Full_NoShape
SQLite schema:
[complete DDL for all 8 tables]
Database value dictionary:
[global sorted values from permitted columns, including sensor_readings.alarm_flag: 0, 1]
```

F01—full package with composite hint:

```text
Condition: F01_Full_WithShape
[the same complete DDL and the same global value dictionary as F00]
Question-derived answer-shape hints:
{"column_count": 2, "hints": ["Use COUNT(*) for count questions."],
 "order_required": true, "row_granularity": "multi-row"}
```

F10—compact domain-grounded package, no composite hint:

```text
Condition: F10_Compact_NoShape
SQLite selected context:
Tables and selected columns:
- assets(asset_id, asset_type_id, location_id)
- sensor_readings(reading_id, asset_id, alarm_flag)
[four additional graph-expanded tables are retained]
Join paths:
...
- sensor_readings.asset_id = assets.asset_id
Power-grid domain normalization hints inferred from the question:
- sensor_readings.alarm_flag = 1
```

F11—compact domain-grounded package with composite hint:

```text
Condition: F11_Compact_WithShape
[the same selected schema, join paths, and alarm_flag normalization as F10]
Answer-shape hints inferred from the question text:
- expected column count: 2
- row granularity: multi-row
- deterministic ordering needed: True
- Use COUNT(*) for count questions.
```

These are excerpts from the frozen Qwen prompt ledger; bracketed text only shortens repeated material. Full records remain in `formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1/prompts.jsonl`.

## Factor invariance/difference matrix

| Component | F00 | F01 | F10 | F11 | Status/interpretation |
|---|---|---|---|---|---|
| Question and stable ID | same | same | same | same | invariant within question |
| Database snapshot | same | same | same | same | invariant |
| Common system/safety instruction | same except condition label | same except label | same except label | same except label | invariant substantive instruction |
| Model snapshot, temperature, seed, max output | same within backbone run | same | same | same | invariant within backbone |
| Schema serialization | full 8-table DDL | same full DDL | question-selected columns/tables + FK expansion | same compact selection | differs by context-package factor |
| Value presentation | global value dictionary | same global dictionary | matched values + derived normalization/predicate hints | same compact grounding | **bundled with context factor; not invariant** |
| Handcrafted domain normalization | absent as a dedicated rule block | absent as a dedicated rule block | present when rules fire | present when rules fire | **bundled with context factor** |
| Composite structural/SQL-operation hint | absent | present as JSON block | absent | present as rendered rules | hint factor; serialization form also differs by context package |
| Gold SQL/result visible to prompt builder | no | no | no | no | invariant exclusion |
| Model calls | one | one | one | one | no repair/ranking/repetition |
| Parser and read-only validator | same | same | same | same | invariant |
| Offline result-equality scoring | same | same | same | same | performed after generation |

### Corpus-tailoring disclosure

The compact selector and hint rules were developed with prior exposure to GridDB. They contain explicit patterns for the corpus’s entity names, statuses, units, dates, topology relations, and recurring question forms. For example, they map “alarmed readings” to `sensor_readings.alarm_flag = 1`; translate month wording to half-open date predicates; and emit exact guidance such as `Use COUNT(*)`, `GROUP BY ... HAVING COUNT(*) > 1`, specified projection fields, descending order, and `LIMIT 1`. The experimental estimands are therefore effects of two frozen, GridDB-tailored prompt packages on development-visible questions—not effects of generic schema reduction or generic answer formatting.

