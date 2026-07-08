# Initial Smoke Debug

## Commands Run

```powershell
python source/code/experiment_final/setup.py
pytest -q source/code/evaluator/tests
where.exe pdflatex
```

## Result

- Setup passed.
- Evaluator tests failed: 11 failed, 2 passed.
- `pdflatex` was not found in the current Windows shell.

## Main Error

The tests resolve the dataset path as:

```text
source/code/data/griddb_maintenance_v2_v0_1/questions.jsonl
```

The uploaded package stores the dataset at:

```text
source/data/griddb_maintenance_v2_v0_1/questions.jsonl
```

## Immediate Fix Queue

1. Decide whether to patch test path discovery or add a compatibility data link/copy.
2. Rerun `pytest -q source/code/evaluator/tests`.
3. After tests pass, run the final experiment entrypoint or a bounded smoke subset.
4. Install or configure a LaTeX distribution before local PDF rebuild.
