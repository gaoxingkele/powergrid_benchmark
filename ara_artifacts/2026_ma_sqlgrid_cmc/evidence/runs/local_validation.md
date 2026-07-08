# Local Validation

## Command

```powershell
python source/code/experiment_final/setup.py
pytest -q source/code/evaluator/tests
```

## Environment

Windows PowerShell; local SQLite dataset present under `source/data/griddb_maintenance_v2_v0_1`.

## Result

Setup passed. Evaluator tests failed with 11 failures and 2 passes because tests look for `source/code/data/griddb_maintenance_v2_v0_1`.
