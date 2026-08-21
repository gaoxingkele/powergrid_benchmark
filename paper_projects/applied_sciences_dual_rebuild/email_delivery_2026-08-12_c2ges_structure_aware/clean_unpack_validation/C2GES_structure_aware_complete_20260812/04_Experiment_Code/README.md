# Experiment code

The formal algorithm snapshot retains the source hierarchy expected by the code:

```text
original_title_rebuild/
  c2ges_offline.py
  run_formal_experiment.py
  R2_v0_3/
    run_test_v0_3_1.py
    v03_methods.py
    v031_methods.py
    counterfactual_paths.py
    counterfactual_paths_v031.py
    tests and configuration files
```

Run the rights-safe regression subset from `original_title_rebuild/R2_v0_3/`:

```text
python -m unittest -v test_v03_methods test_v031_repair test_counterfactual_paths
```

The original third-party PDF corpus, verbatim JSONL derivatives, the local MiniLM model snapshot, and historical one-attempt run directories are not included in this distributable package. The exact model revision and dependency identity are recorded in `TEST_FREEZE_MANIFEST_v0_3_1.json` and `OUTPUT_DEPENDENCY_LOCK_v0_3_1.json`.

Development-only calibration and exact sign-flip sensitivity code are provided in their own subdirectories. Figure generators are under `figure_generation/`.

