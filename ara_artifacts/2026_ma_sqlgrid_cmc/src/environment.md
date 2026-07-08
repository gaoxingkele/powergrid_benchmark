# Environment

## Runtime

Current host: Windows PowerShell under `C:\aicoding\powergrid_benchmark`.

## Dependencies

The setup script is self-contained and reports no downloads required. Evaluator tests use Python and SQLite.

## External Repositories

None. This was imported from a zip package.

## Commands

```powershell
python source/code/experiment_final/setup.py
pytest -q source/code/evaluator/tests
```
