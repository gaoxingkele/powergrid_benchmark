# BIRD gold-SQL preflight blocker — resolved by a uniform pinned runtime

**Date:** 2026-08-05  
**Historical decision:** `BLOCK` under SQLite 3.49.1.  
**Current decision:** `PASS` 500/500 under pinned Python 3.10.11 / SQLite 3.40.1; no baseline model execution is yet authorized.

The official 346,207,293-byte archive was hash-bound and safely expanded into a dedicated directory. Both ZIP layers contained no absolute or parent-traversal paths and no Unix symlinks; the extracted tree contains 11 expected SQLite files, 101 files total, no reparse points, and 1,493,445,090 bytes.

The read-only compatibility preflight executed 499 of the 500 official Mini-Dev gold SQL statements under Python SQLite 3.49.1 with a 180-second per-query ceiling. Official question 701 (`codebase_community`) was interrupted. Its published SQL joins `users`, `posts`, and an aggregate subquery for maximum reputation. The local query plan uses a coroutine and remains incomplete after an additional direct 120-second run.

A logically equivalent diagnostic rewrite that moves the maximum-reputation subquery into a scalar `WHERE` predicate completed in 0.272 seconds and returned `0.6644518272425249`. This diagnostic is **not** substituted for the official gold SQL and does not satisfy the 500/500 gate.

The project selected a uniform runtime boundary rather than a one-item rewrite or performance index. The official Python 3.10.11 Windows embeddable archive (8,629,277 bytes; SHA-256 `608619f8619075629c9c69f361352a0da6ed7e62f83a0e19c63e0ea32eb7629d`) supplies SQLite 3.40.1. Under that runtime, the unchanged Q701 query is materialized, completes in approximately 0.254 seconds, and returns `0.6644518272425249`. The complete unchanged 500-item preflight then passed 500/500 in 22.447 seconds. No row was dropped, no SQL was rewritten, and no index or data value was changed.

This resolves only the database/gold compatibility gate. Prompt materialization, evaluator/adaptor pinning, leakage and token-budget audits, code/config hashes, and independent freeze sign-off remain open; formal model generation is still prohibited.

Evidence: `BIRD_GOLD_PREFLIGHT.json`, `preflight_bird_gold.py`, `DATABASE_ARCHIVE_ACQUISITION.json`, and `SQLITE_RUNTIME_COMPATIBILITY.json`.
