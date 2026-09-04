# P4 s4 Experiment Protocol

**Status:** `IMPLEMENTATION_CONTRACT_FROZEN / PILOT_AND_FORMAL_NOT_FROZEN / NO_RESULTS`
**Purpose:** leakage-free graph/data feasibility, Euclidean GCN sanity baseline, and genuine HGCN comparison.  
**Protected predecessor:** `../p2_s3_identifiable_v1/` is read-only.

The Stage-3 node/target, edge-provenance, visibility, matched-model, manifold, curvature, map, aggregation, and numerical-safeguard semantics are frozen in `implementation_contract.json` and `DATA_MODEL_IMPLEMENTATION_CONTRACT.md`. Their executable definitions are `graph_data.py` and `models.py`; `verify_implementation.py` is an invariant check using synthetic tensors, not an experiment.

Before any formal run, freeze dataset licence/provenance, node/edge mapping, train-only graph construction, rolling splits, horizons, normalization, covariates, shared temporal encoder, model/tuning budget, seed list, statistical unit, correction rule, numerical-failure policy, and output schema. Pilot outputs must be isolated from formal outputs.

This scaffold does not convert the existing CSA attention model into a GCN/HGCN and contains no result.
