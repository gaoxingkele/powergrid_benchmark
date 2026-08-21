# MA-SQLGrid Dual-Backbone Canonical Release

This release compares the independently audited Qwen2.5-Coder-7B Q4_K_M and Granite-3.3-8B Q4_K_M runs on the same 180 GridDB questions and four factorial cells.

The scope is deliberately bounded: two quantized instruction backbones on one database. It is not evidence of general model-family robustness, external-database accuracy, human-reviewed external validity, or comparative efficiency.

```powershell
python generate_release.py
python -m unittest -v test_release.py
```

All numbers are generated from audited `statistics/` and `statistics_granite/` artifacts. Never transcribe values into generated tables by hand.
