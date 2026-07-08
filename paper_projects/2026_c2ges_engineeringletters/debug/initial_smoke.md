# Initial Smoke Debug

## Commands Run

```powershell
python source/code/main.py --limit-docs 1 --bootstrap-samples 10 --out-dir debug/c2ges_smoke_run
where.exe pdflatex
```

## Result

- Python smoke failed before experiment startup.
- `pdflatex` was not found in the current Windows shell.

## Error

```text
ModuleNotFoundError: No module named 'numpy'
```

## Immediate Fix Queue

1. Create or activate an isolated Python environment.
2. Install `source/code/requirements.txt` plus missing imports such as `rouge-score`.
3. Check whether the omitted `verification_pilot` workspace exists elsewhere or must be reconstructed.
4. Install or configure a LaTeX distribution before local PDF rebuild.
