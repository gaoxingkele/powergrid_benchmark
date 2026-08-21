# Collected Supplement Artifacts

Collected on: 2026-07-19

This directory gathers the local artifacts requested by
`../SUPPLEMENT_REQUEST_2026-07-19.md`.

## C2GES

### Dataset Workspace

Path:

```text
C2GES/verification_pilot/agent_audit_40doc/
```

Source:

```text
paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess/verification_pilot/agent_audit_40doc/
```

Verified contents:

- 40 `nerc_*.json` files
- 2940 sentence records
- 200 causal-role questions
- 608 evidence sentence ID assignments
- `manifest.json`

### Pilot Scripts

Path:

```text
C2GES/verification_pilot/scripts/
```

Source:

```text
paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess/verification_pilot/scripts/
```

Includes:

- `build_pilot_dataset.py`
- `run_baselines.py`
- `run_c2ges.py`

### Three-Pack Config

Path:

```text
C2GES/three-pack/config.yaml
```

Source:

```text
paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess/three-pack/config.yaml
```

### Role-Selective Graph-Gate Executor

Path:

```text
C2GES/post_freeze_revisions/role_selective_graph_gate/
```

Sources:

```text
paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess/post_freeze_revisions/role_selective_graph_gate/code/main.py
paper_workspace/workspaces/c2ges-causal-mechanism-ieeeaccess/post_freeze_revisions/role_selective_graph_gate/experiment_outputs/c2ges_role_selective_graph/
```

Included result files:

- `summary.json`
- `details.jsonl`
- `cv_protocol.json`
- `heldout_predictions.jsonl`
- `metadata.json`
- `results.json`
- `diagnostic_role_masked_details.jsonl`

## MA-SQLGrid

### Smoke Support Modules

Path:

```text
MA-SQLGrid/smoke/
```

Source:

```text
paper_workspace/workspaces/ma-sqlgrid-value-grounded-restart/smoke/
```

Included files:

- `dev_chess_style_pilot.py`
- `dev_superiority_pilot.py`
- `minimal_text2sql_smoke.py`
- `dev_ablation_pilot.py`
- `dev_autocompact_pilot.py`

Note: the current `experiment_final/main.py` imports
`minimal_text2sql_smoke as smoke`; the email's `smoke.py` wording appears to
refer to this module's provider constants (`BASE_URL`, `MODEL_NAME`,
`WIRE_API`).

## Final Paper Refine Zip Packages

Path:

```text
final_paper_refine_zips/
```

Copied files:

- `c2ges-engineeringletters-20260627.zip`
- `ma-sqlgrid-cmc-20260627.zip`
- `c2ges-ma-sqlgrid-workspaces-20260627.zip`

## Optional Figure Upgrade

These files are additional visual upgrade candidates generated after the
required supplement artifact collection. They are not part of the blocking
artifact checklist and were not inserted into the original manuscript PDFs.

### C2GES optional teaser/architecture upgrade

Path:

```text
C2GES/figure_upgrade/
```

Included files:

- `c2ges_teaser_architecture_upgrade.png`
- `c2ges_teaser_architecture_upgrade_prompt.txt`
- `manifest.json`
- `README.md`

The selected C2GES candidate upgrades the paper's teaser / architecture story
around role-conditioned sentence-ID evidence reranking while preserving the
claim boundary: the evaluated output remains selected evidence sentence IDs,
not expert adjudication or a full operational simulation.

### MA-SQLGrid optional teaser/architecture upgrade

Path:

```text
MA-SQLGrid/figure_upgrade/
```

Included files:

- `ma_sqlgrid_teaser_architecture_upgrade.png`
- `ma_sqlgrid_teaser_architecture_upgrade_prompt.txt`
- `manifest.json`
- `README.md`

The selected MA-SQLGrid candidate upgrades the paper's teaser / architecture
story around compact domain-grounded Text-to-SQL and bounded reference-free
validation. The AutoFigure provider timed out twice for this paper, so this
candidate was generated as a deterministic raster fallback from the same
curated method story.
