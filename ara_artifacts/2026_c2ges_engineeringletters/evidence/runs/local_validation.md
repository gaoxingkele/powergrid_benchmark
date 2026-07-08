# Local Validation

## Command

```powershell
python source/code/main.py --limit-docs 1 --bootstrap-samples 10 --out-dir debug/c2ges_smoke_run
```

## Environment

Windows PowerShell; active Python does not have required experiment dependencies installed.

## Result

Failed with `ModuleNotFoundError: No module named 'numpy'`.
