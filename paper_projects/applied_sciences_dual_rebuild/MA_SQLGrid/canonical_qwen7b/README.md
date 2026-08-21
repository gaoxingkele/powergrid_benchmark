# MA-SQLGrid Qwen-7B Canonical Release

This directory is an isolated publication-graphics release generated only from the independent formal audit, its canonical recomputed rows, and its three canonical CSV tables.

**Claim boundary:** Qwen2.5-Coder-7B-Instruct Q4_K_M on GridDB only; one model, one database, and one frozen execution seed. Granite second-model robustness is pending. No cross-model or external-database accuracy claim is supported here.

Run:

```powershell
python generate_release.py
python -m unittest -v test_release.py
```

The generator creates six figures in editable SVG, PDF, and 450-dpi PNG formats; five logical tables in CSV and TeX formats; captions; a hash manifest; and a visual-QA record. Do not edit generated numbers by hand.
