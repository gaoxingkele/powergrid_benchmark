# Public Dataset Archive Cache

This directory stores compressed public dataset cache artifacts for Git synchronization.

Raw dataset directories under `data/public_datasets/` are intentionally ignored by Git.
Each dataset cache is packaged as `.tar.gz`; archives larger than 20 MiB are split into
numbered parts such as:

```text
gridstage.tar.gz.part001
gridstage.tar.gz.part002
...
```

The split files are produced by:

```powershell
python scripts\data_acquisition\archive_public_datasets.py --clean --part-size-mb 20
```

The complete index and source paths are tracked in `archives_manifest.csv`.
