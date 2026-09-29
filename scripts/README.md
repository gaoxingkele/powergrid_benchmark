# Scripts

Utility scripts for repository maintenance, data acquisition, preprocessing, experiment runs, and validation.

Run the scaffold check with:

```powershell
python scripts/validate_scaffold.py
```

Audit public dataset cache:

```powershell
python scripts/data_acquisition/audit_public_datasets.py
```

Refresh default public dataset sources:

```powershell
python scripts/data_acquisition/download_public_datasets.py
```

Download Zenodo extension datasets via **aria2 + local proxy** (recommended; proven stable):

```powershell
python scripts/data_acquisition/download_zenodo_aria2.py
python scripts/data_acquisition/download_zenodo_aria2.py --only vce_rare_power finland_afrr_weather
```

Flags used: `--all-proxy=http://127.0.0.1:17890 --split=16 --max-connection-per-server=16 --continue=true --file-allocation=none`.

Fetch a specific metadata-only source:

```powershell
python scripts/data_acquisition/download_public_datasets.py --dataset large_synthetic_power_grid_ml_zenodo --include-large
```

Create knowledge-base update files for a new work round:

```powershell
python scripts/knowledge_base/new_update_round.py
```

Refresh the C2GES/NERC report PDF cache:

```powershell
python scripts/data_acquisition/download_c2ges_nerc_reports.py
```

Create GitHub-friendly dataset archives. The default part size is 20 MB:

```powershell
python scripts/data_acquisition/archive_public_datasets.py --clean
```

Restore archived datasets:

```powershell
python scripts/data_acquisition/restore_public_dataset_archives.py
```

Append a research-wiki event:

```powershell
python scripts/wiki/log_research_event.py --title "event title" --observation "..." --action "..." --rationale "..." --evidence "..." --impact "..." --next "..."
```

Run the read-only MDPI Applied Sciences pre-submission audit:

```powershell
python scripts/papers/applsci_preflight.py paper_projects/CMC/C2GES --baseline-ref 840dcce5 --run-project-verifier
```

The former string-replacement converter is retained only as a disabled historical record. See `docs/paper_workflows/APPLIED_SCIENCES_PRE_SUBMISSION_WORKFLOW.md`.
