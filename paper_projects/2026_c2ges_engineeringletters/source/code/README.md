# Code Package for "Causal-Role-Aware Extractive Evidence Selection for Power Grid Reliability Reports" (C²GES)

## Description
This directory contains the experiment runner used for the paper, plus a prepared
harness for learned and LLM baselines (`prepared_baselines/`).

`main.py` is the Executor wrapper for the revised role-selective C²GES protocol.
It delegates ranking logic to the validated pilot scripts and expects an
experiment workspace with the following layout:

```
<workspace>/
  verification_pilot/
    agent_audit_40doc/          # nerc_*.json documents (+ optional manifest.json)
    scripts/
      run_baselines.py          # validated baseline rankers
      run_c2ges.py              # validated C2GES scoring components
  three-pack/
    config.yaml
```

## Project Files
- `main.py` — main experiment runner (all conditions, ablations, CV protocol, bootstrap statistics)
- `prepared_baselines/` — prepared cross-encoder, BGE-reranker, and zero-shot LLM baselines
  (runnable once the workspace above is supplied; see its README)

## How to Run
```
pip install -r requirements.txt
python main.py --workspace /path/to/workspace
# or: export C2GES_WORKSPACE=/path/to/workspace && python main.py
```
If neither is given, `main.py` searches upward from the current directory for the
workspace layout and exits with a clear error if not found.

## Dependencies
Install dependencies with `pip install -r requirements.txt`. The SBERT baseline
additionally downloads a sentence-transformers checkpoint on first run.
