# Portability and Reproduction

Earlier internal experiment scripts were written against the full project tree
and therefore retain source-workspace paths. Moving those scripts alone would
make their historical relative paths invalid. Version 3.0 does not claim that a
rights-safe email attachment can reproduce restricted raw-data acquisition or
formal model generation without the omitted inputs.

This package resolves the portability issue in three ways:

1. Code and derived data are separated but mapped by study name.
2. `verify_package.py` uses only package-relative paths and performs a read-only
   validation of hashes, manuscript assets, key denominators, 80/100/101, BIRD
   aggregate cells, and the portable framework/executor unit tests.
3. Historical source scripts are retained for methodological inspection. To
   rerun an experiment from its raw inputs, restore the repository layout and
   obtain the excluded data under the applicable licence, then use the recorded
   protocol and runtime.

Run the portable check from any directory with:

```text
python path/to/MA_SQLGrid_v3.0_COMPLETE/verify_package.py
```

The BIRD formal run additionally requires the recorded Python 3.10.11 and
SQLite 3.40.1 runtime. The portable check does not regenerate model outputs.
