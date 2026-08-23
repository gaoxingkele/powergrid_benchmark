# Code map

`core/` preserves the source hierarchy expected by the formal code. Run the distributable regression subset from `core/R2_v0_3/`:

```text
python -m unittest -v test_v03_methods test_v031_repair test_counterfactual_paths
```

For the complete portable verification on Python 3.12, including all public
tests, rights-safe data accounting, and both LaTeX builds, run from this
directory:

```text
python run_public_verification.py
```

Create the environment with `conda env create -f environment-py312.yml`, or
install `requirements-py312.txt` into an existing Python 3.12 environment. The
verifier records restricted-input tests as explicit skips and never reruns the
one-attempt formal test.

The third-party source corpus, verbatim JSONL derivatives, local MiniLM model snapshot, and one-attempt run directories are excluded. Their identities are recorded by the formal manifest and dependency lock.
