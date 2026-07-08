# Environment

## Runtime

Current host: Windows PowerShell under `C:\aicoding\powergrid_benchmark`.

## Dependencies

Initial smoke run failed because `numpy` is not installed in the active Python environment. The script also imports `rouge_score`.

## External Repositories

None. This was imported from a zip package.

## Commands

```powershell
python source/code/main.py --limit-docs 1 --bootstrap-samples 10 --out-dir debug/c2ges_smoke_run
```
