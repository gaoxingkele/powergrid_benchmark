# MA-SQLGrid Expansion Runbook (prepared experiments)

All scripts below are runnable as-is but require a live model endpoint
(`KRILL_API_KEY` for the original model, or any OpenAI-compatible key for a
second model). No key is stored in this package. Everything else (dataset,
archived prompts, evaluator, analysis) is self-contained.

Python: 3.10+ (developed and smoke-tested with 3.14). No third-party
packages are required for the runners; `pytest` is needed only for the
evaluator test suite.

## 0. Recomputations that need NO API key (already run)

```bash
python analysis/recompute_relaxed_metrics.py   # strict / order-insensitive / projection-tolerant accuracy
python analysis/recompute_efficiency.py        # real API token, latency, retry statistics
python -m pytest ../evaluator/tests -q         # evaluator unit tests (13 passed)
python expand_dataset.py                       # builds data/griddb_maintenance_v2_x10 (x10 rows + 2 distractor tables)
```

Outputs: `analysis/relaxed_metrics.json`, `analysis/efficiency_stats.json`,
`../../data/griddb_maintenance_v2_x10/`.

## 1. P0-1 Second-generator comparison (needs API key)

Runs C2/C4/C5 on the identical 180 test questions with the identical
archived prompts against a second model, writing `outputs_<model>/` in the
same schema as the formal run.

```bash
# open-source example (any OpenAI-compatible serving endpoint works):
export SECOND_MODEL_API_KEY=...
python run_second_model.py \
    --model Qwen2.5-Coder-32B-Instruct \
    --base-url https://<your-endpoint>/v1 \
    --api-key-env SECOND_MODEL_API_KEY \
    --provider <provider-label>

# different closed-source model example:
export SECOND_MODEL_API_KEY=...
python run_second_model.py \
    --model gpt-4o-mini \
    --base-url https://api.openai.com/v1 \
    --api-key-env SECOND_MODEL_API_KEY \
    --provider openai
```

Then analyze the new run with the same scripts by pointing them at the new
outputs directory (both accept the default `outputs/`; copy or symlink, or run:
`MA_OUT=outputs_<model>` and edit the `OUT_DIR` constant, which is the only
path they read).

Fidelity notes (also in the script docstring):

* C2/C4/C5 prompts are the byte-identical archived prompts from
  `outputs/traces/`, so the second model sees exactly the context the
  original model saw. The missing `dev_chess_style_pilot` module is NOT
  needed for this.
* The C5 validator/ranker/repair loop is reimplemented from the published
  specification (weights in the paper's implementation-details table). On
  the archived C5 candidates it reproduces the archived selection in
  167/169 non-repair cases (98.8%).

Cost estimate: 3 conditions x 180 questions x ~1.2 calls x ~5-6.5k input
tokens = roughly 4M input tokens + ~0.1M output tokens per model.

## 2. P0-6 Temperature-0 repeat-consistency check (needs API key)

```bash
export KRILL_API_KEY=...
python run_consistency_check.py \
    --model gpt-5.4-mini-2026-03-17 \
    --base-url https://api.krill-ai.com/v1 \
    --api-key-env KRILL_API_KEY \
    --conditions C4,C5 --repeats 3
```

Reports per-condition exact-SQL agreement, evaluator-verdict agreement, and
per-repeat execution accuracy in
`outputs_consistency_<model>/consistency_report.json`.

Determinism evidence already available WITHOUT rerunning (recomputed from
the archived 900 predictions): temperature fixed at 0 in the runner
hyperparameters; 898/900 calls succeeded on the first attempt (2 calls used
one retry each: 1 in C1, 1 in C4); zero provider errors in the final
records.

## 3. P1-2 Scaled-dataset run (needs API key)

`expand_dataset.py` (no key needed) builds
`data/griddb_maintenance_v2_x10`: every entity table x10 by deterministic
block replication with convention-preserving new names, plus two distractor
tables (`vegetation_inspections`, `spare_parts_inventory`). Gold SQL
re-validates with zero errors on the scaled database.

Re-running conditions on it requires regenerating the condition contexts
for the new database, which depends on the missing `dev_chess_style_pilot`
module (see MISSING_ARTIFACTS.md). Two options:

* supply the missing module and run `main.py` with
  `MA_SQLGRID_WORKSPACE` pointing at a workspace whose
  `data/griddb_maintenance_v2_v0_1` is replaced by the x10 variant; or
* run C2 only (full schema + values prompt can be rebuilt mechanically from
  the new schema/database without the missing module).

## 4. Evaluator tests (P0-3, fixed)

```bash
python -m pytest ../evaluator/tests -q   # 13 passed
```

The tests previously failed 11/13 because they resolved the dataset
relative to the wrong parent directory; they now search upward for
`data/griddb_maintenance_v2_v0_1`. Hardcoded `/media/lenovo/...` fallback
paths were removed from `main.py`.
