# Retrospective Offline Coordination Diagnostic

Run date: 2026-08-08  
Status: **diagnostic only; not a new multi-agent generation result**

## Inputs

The read-only replay accepted exactly three hash-locked inputs:

| Input | Rows | SHA-256 |
|---|---:|---|
| Frozen Qwen predictions | 720 | `53aaf0c9659f6a6b71b66ff64d34ed925664742205d0ca4fd7585d7fe5c9f5e3` |
| Frozen Granite predictions | 720 | `be433ac853f60ebc8882fdcc7bd01033bca8868fa23b298114b0977476983e3d` |
| Formal-v5 atomic state scores | 25,920 | `89c0ede848b4487a1edadb2fd771dabaf21a16c8359d7000ad9955c3196968cd` |

No prompt was created and no model/API call was made. The original files were
opened for reading only and were not modified.

## Coverage result

| Coverage gate | Questions |
|---|---:|
| Audited | 180 |
| At least two distinct frozen SQL candidates | 173 |
| At least two safe candidates with consistent frozen T0 execution evidence | 172 |
| Retrospectively adjudicated | 172 |
| Failed closed: only one unique SQL | 7 |
| Failed closed: fewer than two eligible SQL candidates | 1 |
| Reference-free counterfactual evidence available for selection | 0 |

Unique candidate counts ranged from one to eight. The distribution was: 1 (7
questions), 2 (19), 3 (15), 4 (18), 5 (27), 6 (23), 7 (45), and 8 (26).

## Counterfactual boundary

The formal-v5 ledger contains multi-state prediction-versus-gold agreement
fields. Feeding those fields to the Adjudicator would allow evaluation evidence
to choose a candidate. The replay therefore invokes Counterfactual Critic with
an empty reference-free evidence set, records coverage as incomplete, and does
not count any missing state as a pass. Consequently, this replay cannot estimate
a counterfactual coordination benefit.

## Permitted interpretation

The replay demonstrates only that existing frozen predictions provide adequate
candidate diversity for a later prospectively frozen coordination experiment on
172/180 questions, and that the deterministic interfaces can replay them without
new generation. It does **not** show that the selected SQL is more accurate, that
multi-agent coordination improved performance, or that the new framework has
been experimentally validated.

Machine-readable evidence is in:

- `retrospective_diagnostic/diagnostic_rows.jsonl` (180 rows)
- `retrospective_diagnostic/coverage_summary.json`
- `retrospective_diagnostic/manifest.json`

