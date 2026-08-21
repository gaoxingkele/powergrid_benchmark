# x10 Scaled-Database Scale-Robustness Run (deepseek-chat)

Run date: 2026-07-20. Runner: `run_x10_scale.py`. Model: `deepseek-chat`
(`https://api.deepseek.com/v1`), temperature 0, max_tokens 700 — the paper's
validated second generator. The original gpt-5.4-mini/krill endpoint is
unavailable, so this experiment is framed as **scale robustness on the second
generator**, comparing against the same generator's v0.1 run
(`outputs_deepseek_chat/`).

## Setup and provenance

- Database: `data/griddb_maintenance_v2_x10` — 10x rows plus two distractor
  tables (`vegetation_inspections`, `spare_parts_inventory`). Gold SQL
  re-verified before any API call: **200 questions, 0 gold-validation errors**
  (same check as `expand_dataset.py` reported; re-run by the runner's
  GOLD_CHECK gate). Test split: the same 180 questions (Q021-Q200); question
  text and gold SQL are byte-identical to v0.1.
- Contexts/prompts: rebuilt with the **received original builders**
  (`source/smoke/dev_chess_style_pilot.py`, integrated 2026-07-20) pointed at
  the x10 SQLite file via path overrides only; prompt templates imported from
  `main.py`. Fidelity check: on the v0.1 database, the received builders
  reproduce the archived formal-run prompts **byte-for-byte (180/180 for both
  C2 and C4)**.
- C5 uses the original `chess.rank_candidates` / `chess.reference_free_validation`
  and mirrors `main.py`'s candidate/repair flow. 540 primary calls + 13 repair
  calls; **0 provider errors; safe-SQL rate 1.0 in all conditions**.
- Scoring: packaged evaluator against the x10 database (strict), plus
  `analysis/recompute_relaxed_metrics_deepseek_x10.py` (set_exact /
  set_relaxed).

## Headline comparison (deepseek-chat, n=180 per condition)

| condition | v0.1 strict | x10 strict | v0.1 set_exact | x10 set_exact | v0.1 set_relaxed | x10 set_relaxed |
|---|---:|---:|---:|---:|---:|---:|
| C2_FullSchemaValues_Direct | 0.3389 | **0.3333** | 0.3667 | 0.3667 | 0.8500 | 0.8167 |
| C4_MASQLGrid_DomainContext | 0.7000 | **0.5944** | 0.7944 | 0.6944 | 0.7944 | 0.6944 |
| C5_MASQLGrid_DomainContext_Validated | 0.7667 | **0.6500** | 0.8278 | 0.7000 | 0.8278 | 0.7000 |

Token/latency economics (real API usage):

| condition | v0.1 input tok mean | x10 input tok mean | growth | v0.1 output tok | x10 output tok | x10 latency ms mean |
|---|---:|---:|---:|---:|---:|---:|
| C2 | 2011.6 | 3042.6 | **+51%** | 49.9 | 48.6 | 989.7 |
| C4 | 509.3 | 504.0 | **-1% (flat)** | 46.6 | 47.3 | 1115.9 |
| C5 (incl. repair) | 680.5 | 560.5 | -18% | 186.2 | 180.3 | 1834.1 |

Context sizes (builder word-token estimate): C2 full-schema+values context
631 -> 1125 (+78%); C4 compact domain context 174 -> 176 mean (flat, max 261).
C5 repair invocations dropped from 52/180 (v0.1) to 13/180 (x10) — see
anomaly 2 below.

## Verdicts on the key questions

**(a) Does the compact-context advantage (C4 vs C2 strict) survive at 10x
scale with distractor tables? YES, attenuated.** C4-C2 = +26.1 points at x10
(0.5944 vs 0.3333) versus +36.1 points at v0.1 (0.7000 vs 0.3389). The gap
shrinks because C4 loses ~10 points to a specific, fully-diagnosed mechanism
(anomaly 1), while C2 is statistically unchanged. Caveat for the paper: the
C4/C5 builders operate over a hardcoded 8-table catalog (`TABLE_COLUMNS`), so
the two distractor tables are excluded from the compact context *by
construction*, not by learned selection; the distractors stress only C2
(whose prompt includes their DDL).

**(b) Does C5 validation still add gain? YES.** +5.6 points strict over C4
(0.6500 vs 0.5944), versus +6.7 points at v0.1. The gain persists but is
slightly smaller, partly because the truncated value inventory (anomaly 1)
yields fewer normalized value hints, weakening both the ranker's value-hit
signal and the repair trigger (13 repairs vs 52 at v0.1).

**(c) Token economics at scale: as predicted.** The C2 full-schema+values
prompt grew +51% in real API input tokens (2012 -> 3043) at 10x rows + 2
distractor tables and will keep growing with DB size (value dictionary +
schema DDL). The C4 compact context stayed flat (509 -> 504, ~6x cheaper than
C2 at x10). Honesty caveat: part of C4's boundedness comes from the same
`LIMIT 80` value-inventory cap that causes anomaly 1 — it is bounded partly
at the cost of value recall, not by a scalable retrieval index.

**(d) Does the projection-tolerant pattern persist? YES.** C2's failures
remain overwhelmingly projection/shape errors (99/120 errors are
shape_mismatch): strict 0.3333 -> set_relaxed 0.8167, so under
projection-tolerant scoring C2 again overtakes C4/C5 (0.8167 vs
0.6944/0.7000), exactly the v0.1 pattern (0.85 vs 0.7944/0.8278). C4/C5 gain
from order-insensitivity (set_exact) but nothing further from projection
tolerance (set_relaxed = set_exact), also as at v0.1.

## Anomalies (honest accounting)

1. **The C4/C5 drop is a value-inventory truncation artifact, precisely
   localized.** The builder's `value_inventory` uses
   `SELECT DISTINCT <col> ... ORDER BY <col> LIMIT 80`. At v0.1 all 18 asset
   names fit; at x10 there are 180 distinct `asset_name` values and the
   alphabetical top-80 ends at "LN-611", so all RL-*/SB-*/TX-* names —
   including the TX-001..TX-004 literals referenced by test questions — fall
   out of the inventory. Those questions lose their "Exact database values
   matched from the question" lines and normalization hints. Attribution:
   149/180 C4 prompts are byte-identical between v0.1 and x10, and on those
   the x10 run scores 101/149 vs 102/149 for the v0.1 predictions re-scored
   on the x10 DB (no scale effect). The **entire** drop sits in the 31
   changed-prompt questions: 23/31 -> 6/31. Implication for the paper: the
   domain-context *idea* survives scale; the pilot's fixed-cap alphabetical
   value scan does not, and would need a scalable value index (as in
   CHESS-style keyword/LSH retrieval) beyond ~80 distinct values per column.
2. **Fewer C5 repairs at x10 (13 vs 52)** — a downstream symptom of anomaly
   1: fewer inferred value hints means fewer `missing_value_hints` triggers.
3. **Small-database coincidental correctness is negligible**: re-scoring the
   v0.1 deepseek predictions on the x10 database moves C4 only 0.7000 ->
   0.6944 and leaves C5 at 0.7667, so v0.1 numbers were not inflated by
   accidental denotation matches on tiny tables.
4. **Cosmetic**: this run extracts SQL with the original `smoke.extract_sql`
   (collapses whitespace), while the v0.1 deepseek run used
   `run_second_model.extract_sql` (preserves newlines); raw string diffs
   between the runs are therefore not meaningful. After whitespace
   normalization, 137/149 same-prompt C4 predictions are identical,
   consistent with the packaged temperature-0 repeat-consistency report
   (82% exact-SQL agreement).

## Artifacts

- `predictions.jsonl`, `scores.jsonl`, `contexts.jsonl` (domain contexts),
  `results.json`, `traces/` (540 trace files, full prompts + raw responses;
  repair prompts/responses embedded in the C5 traces)
- Relaxed metrics: `../analysis/relaxed_metrics_deepseek_x10.json`
- Runner: `../run_x10_scale.py` (gold-validation gate + context rebuild +
  deepseek client reusing `run_second_model.ChatClient`)
