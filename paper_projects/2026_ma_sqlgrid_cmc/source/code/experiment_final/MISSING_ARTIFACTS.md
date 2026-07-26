# Missing artifacts the author must supply for full reproducibility (P0-3)

## Update 2026-07-20: support modules received

The author-supplied smoke modules arrived on 2026-07-20 via
`c2ges_supplement_incoming/collected_artifacts_2026-07-19/MA-SQLGrid/smoke/`
and are now integrated at `source/smoke/` (the location `main.py` inserts on
sys.path via `WORKSPACE/"smoke"`, and the only placement where the modules'
internal `WORKSPACE = parents[1]` data paths resolve):

* `dev_chess_style_pilot.py` — RECEIVED. Original context builders
  (`render_full_schema_values`, `generic_context`, `infer_domain_context`,
  `render_selected_context`, `rank_candidates`, `reference_free_validation`,
  `estimate_tokens`). Verified importable and runnable against a different
  SQLite file (the x10 expansion) via path overrides only.
* `minimal_text2sql_smoke.py` — RECEIVED. Defines the archived-run constants
  `MODEL_NAME="gpt-5.4-mini"`, `PROVIDER="krill"`,
  `BASE_URL="https://api.krill-ai.com/codex/v1"`, `WIRE_API="responses"`
  plus `extract_sql` / `extract_candidate_sql`. The krill endpoint is not
  called by any new run (it is unavailable); new runs use the deepseek
  chat-completions client.
* `dev_superiority_pilot.py`, `dev_ablation_pilot.py`,
  `dev_autocompact_pilot.py` — RECEIVED (supporting pilots).

Still missing:

* `researchclaw.llm.client` (the original LLM client used for the archived
  krill run). A clearly-labeled compatibility stand-in now lives at
  `code/agent_reference/researchclaw/llm/client.py`: it reproduces the
  `LLMClient`/`LLMConfig` interface over the standard OpenAI
  chat-completions wire so `main.py` and the received modules import and can
  drive OpenAI-compatible endpoints, but it deliberately raises on
  `wire_api="responses"` (the proprietary krill wire) rather than guess the
  original wire format. `code/agent_reference/evaluator.py` is a
  path-compatibility re-export of the packaged evaluator for the same
  reason (main.py's sys.path entries do not include `code/evaluator`).
* `build_griddb_maintenance_v2.py` (v0.1 dataset generator) — still missing;
  dataset provenance for v0.1 remains as-archived. The x10 expansion has its
  own generator (`expand_dataset.py`, included).

Verified on 2026-07-20: `import main` succeeds; the x10 scale run
(`run_x10_scale.py`) rebuilt C2/C4/C5 contexts with the received builders.

## Original inventory (2026-07 packaging)

`main.py` (the archived formal-run driver) imports four modules that are NOT
in this release package. The formal run's *outputs* (900 predictions,
scores, traces with full prompts and raw responses) are archived and fully
auditable without them, and the prepared second-model/consistency runners
deliberately avoid these imports by reusing archived prompts. But re-running
`main.py` itself, or regenerating condition contexts for a new database
(e.g. the x10 expansion), requires the originals:

| Missing module / file | Role | Import site |
|---|---|---|
| `dev_chess_style_pilot` | Core MA-SQLGrid implementation: `render_full_schema_values`, `generic_context`, `infer_domain_context`, `render_selected_context`, `rank_candidates`, `reference_free_validation`, `estimate_tokens` — i.e. schema selection, value normalization, answer-shape inference, and the C5 ranker | `main.py` (`import dev_chess_style_pilot as chess`) |
| `minimal_text2sql_smoke` | Model constants (`MODEL_NAME`, `BASE_URL`, `PROVIDER`, `WIRE_API`) and SQL extraction (`extract_sql`, `extract_candidate_sql`) | `main.py` (`import minimal_text2sql_smoke as smoke`) |
| `researchclaw.llm.client` | `LLMClient` / `LLMConfig` OpenAI-compatible wrapper used for the archived run | `main.py` |
| `build_griddb_maintenance_v2.py` (dataset generator) | Script that generated `data/griddb_maintenance_v2_v0_1` (database + questions) | referenced by dataset provenance notes; not imported |

Notes:

* The original hardcoded fallback path
  `/media/lenovo/data2/cja/GridMind/.../ma-sqlgrid-value-grounded-restart`
  has been removed from `main.py`; the workspace is now resolved by
  searching upward for `data/griddb_maintenance_v2_v0_1/database.sqlite` or
  via the `MA_SQLGRID_WORKSPACE` environment variable.
* Partial stand-ins already in this package:
  - `run_second_model.py` reimplements SQL extraction and the C5
    validator/ranker from the published specification (98.8% selection
    agreement with the archived ranker) and reuses archived prompts, so
    second-model and consistency experiments do not need the originals.
  - `analysis/` recomputes all headline and relaxed metrics from archived
    artifacts with only the packaged evaluator.
* Action for the author before submission: drop the four items above into
  the package (suggested layout: `code/experiment_final/agent_reference/`
  for the two pilot modules, `code/researchclaw/` for the client,
  `data/griddb_maintenance_v2_v0_1/build_griddb_maintenance_v2.py` for the
  generator), then verify `python main.py` starts in smoke mode with
  `MA_SQLGRID_RUN_MODE=smoke` and a valid `KRILL_API_KEY`.
