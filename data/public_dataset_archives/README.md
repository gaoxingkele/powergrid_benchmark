# Public Dataset Archives

This directory contains compressed public-dataset cache archives for GitHub synchronization.

The original dataset cache under `data/public_datasets/` remains ignored by git. Large archives are split into 20 MB parts using the naming pattern:

```text
public_datasets_<category>.tar.gz.part001
public_datasets_<category>.tar.gz.part002
...
```

Small categories are stored as a single `.tar.gz` file.

## Restore

To restore a split archive on Windows PowerShell:

```powershell
Get-Content public_datasets_grid_cases.tar.gz.part* -Encoding Byte -ReadCount 0 |
  Set-Content public_datasets_grid_cases.tar.gz -Encoding Byte
tar -xzf public_datasets_grid_cases.tar.gz -C ..\..
```

Repeat for each category. The `manifest.csv` file lists category, source path, file names, and part sizes.
