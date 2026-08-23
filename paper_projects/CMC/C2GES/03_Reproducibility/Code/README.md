# Code map

`core/` preserves the source hierarchy expected by the formal code. Run the distributable regression subset from `core/R2_v0_3/`:

```text
python -m unittest -v test_v03_methods test_v031_repair test_counterfactual_paths
```

The third-party source corpus, verbatim JSONL derivatives, local MiniLM model snapshot, and one-attempt run directories are excluded. Their identities are recorded by the formal manifest and dependency lock.

