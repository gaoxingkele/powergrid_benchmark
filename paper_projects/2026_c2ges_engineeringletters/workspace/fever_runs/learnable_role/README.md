# FEVER learnable-role C2GES run

- Date: 2026-08-04
- Data: filtered FEVER evidence-selection (human gold), converted by `source/code/prepare_fever_benchmark.py`
- Train/Dev/Test: 4000 / 800 / 800
- Model: frozen MiniLM + learnable role MLP + mixture floors (0.35/0.25/0.05)
- Test full F1: **0.5066**
- vs no-role: +0.0103, p=0.005
- vs TF-IDF/SBERT/LexCue/query-only: significant (p<0.001)
- vs BM25: not significant (p=0.365)
- Artifacts: `summary.json`, `checkpoint.pt`
