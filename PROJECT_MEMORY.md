# Project Memory

This file records durable project decisions so future sessions can recover context quickly.

## Current State

- Repository scaffold created for powergrid plus computer-science benchmark work.
- The benchmark follows an ARA-first layout: every selected paper gets an `ara_artifacts/<paper_id>/` package.
- Engineering reproductions and GitHub integrations live under `paper_projects/<paper_id>/`.
- Imported two uploaded paper workspaces:
  - `2026_c2ges_engineeringletters`
  - `2026_ma_sqlgrid_cmc`
- Created `knowledge_base/` as the global benchmark knowledge base for datasets, tasks, baselines, literature, sources, and update logs.
- Created `data/public_datasets/` as the public dataset cache and metadata area.
- Cached core public benchmark sources:
  - MATPOWER case files
  - pandapower networks/test cases
  - PGLib-OPF
  - RTS-GMLC
  - SimBench
  - Grid2Op datasets index
- Stored metadata-only entries for OPSD, EIA, NREL NSRDB, TAMU test cases, ACN-Data, and a Zenodo large synthetic power-grid ML dataset.
- On 2026-07-07, expanded local public dataset cache:
  - `opsd_time_series` now includes the 60-minute CSV.
  - `psml` repository cached.
  - DGA/PMU candidates cached: `dgann_duval`, `dgadb`, `lbnl_pmu_event_library`, `gridstage`.
  - ENTSO-E and PJM now have local metadata/API-ready paths.
- On 2026-07-08, recovered and downloaded the public source-report layer for C2GES:
  - `data/public_datasets/reliability_reports/c2ges_nerc_reports`
  - 40 official NERC PDFs mapped from C2GES `nerc_*` document IDs.
  - The C2GES sentence-level candidate labels remain missing from the uploaded package.
- On 2026-07-08, created independent `research_wiki/` for methodology evolution, paper idea logic, and per-round research logs.

## Open Decisions

- Select the first benchmark task family: load forecasting, state estimation, optimal power flow, contingency analysis, fault detection, cyber-physical security, or grid operation agents.
- Select canonical grid systems and datasets.
- Decide whether external simulators such as MATPOWER, Grid2Op, PowerModels, or OpenDSS are required for the first batch.
- Decide whether `2026_c2ges_engineeringletters` should reconstruct the missing `verification_pilot` workspace or remain manuscript-only.
- Decide whether `2026_ma_sqlgrid_cmc` should fix evaluator test path discovery in code or add a compatibility data link/copy.
- Decide whether API-token sources should be configured through local environment variables for EIA, NREL NSRDB, ENTSO-E, PJM, and ACN-Data.
- Decide whether OPSD should be downloaded as a full package or as a smaller 60-minute forecasting subset.
- Decide the first subset strategy for the TB-scale Zenodo synthetic power-grid ML dataset.

## Operating Rules

- Do not mix raw evidence and interpretation.
- Preserve failed reproduction attempts in the relevant ARA `trace/` and `evidence/runs/` files.
- Prefer shared config files over hidden script arguments for comparable experiments.
- Keep large data, PDFs, extracted text, and cloned repositories out of git unless explicitly curated.
- Treat `knowledge_base/updates/*` as auditable decision/rationale summaries; do not store hidden chain-of-thought.
- After each interaction, judge whether the work created durable research value. If yes, update `research_wiki/` with audit-friendly summaries:
  - methodology changes
  - paper/source idea extraction
  - data/source/label/evidence gaps
  - next validation hypotheses
- When new papers, articles, datasets, or benchmark ideas are found, extract their core value into `research_wiki/paper_ideas/` or `research_wiki/logs/`.
- Do not write hidden chain-of-thought; use Observation -> Action -> Rationale Summary -> Evidence -> Impact -> Next.
