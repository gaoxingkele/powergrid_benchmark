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

Create GitHub-friendly dataset archives:

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
