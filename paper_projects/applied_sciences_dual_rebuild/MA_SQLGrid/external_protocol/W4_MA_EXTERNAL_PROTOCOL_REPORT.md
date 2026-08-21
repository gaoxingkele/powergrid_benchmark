# W4 MA External-Database Protocol Report

## Outcome

- External development candidates: **91** (RTS-GMLC 55; SimBench 36).
- Registered factorial cells: **364**, four conditions x 91 questions.
- Exact registered-reference SQL leakage into prompts: **0**.
- Symmetric perturbation failures: **0**.
- Reference SQL safe/executable: **91/91** of 91.
- Shared Cartesian/hash audit: **PASS** (364/364).
- Model, network, and paid API calls: **0**.

## Protocol

Each question receives full/no-shape, full/shape, compact/no-shape, and compact/shape prompts. Full and compact schemas are generated from SQLite introspection. Compact selection uses only question tokens and schema metadata. Shape hints are coarse heuristics derived only from natural-language text; stored answer shape and registered SQL are never consulted.

A real low-relevance table is deterministically registered as an additional schema candidate. Its ID and exact block hash are identical in all four cells for the same question. Database, schema, question, source-manifest, perturbation, context, prompt, and code hashes are retained per cell.

## Evaluation interface

The reusable evaluator permits one read-only `SELECT` or `WITH ... SELECT`, rejects write/schema-changing tokens and multiple statements, opens SQLite in read-only/query-only mode, and returns execution status, shape, row count, and canonical result SHA-256. In this dry run it evaluates only the registered automatic reference SQL, not model predictions.

## Evidence boundary

All inputs remain `AUTO_CANDIDATE`, non-human-reviewed, nonsealed development artifacts. Reference SQL execution proves mechanical consistency only. It does not justify benchmark accuracy, natural-language validity, external generalization, or main-table claims. Human review, adjudication, family-isolated sealing, and an untouched evaluation run remain required.

## Redistribution

RTS-GMLC carries an NREL data-use notice whose pinned local text is truncated; SimBench is governed by ODbL/DbCL for database content. Both require a redistribution decision before publishing derived databases.
