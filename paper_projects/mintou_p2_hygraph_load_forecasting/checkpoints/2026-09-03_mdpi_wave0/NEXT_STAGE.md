# P4 Next Stage: Graph/Data and HGCN Feasibility Gate

**Stage status:** `QUEUED_AFTER_P3 / NOT YET RUN`  
**Planned namespace:** `experiments/p2_s4_electronics_hgcn_load_v1/`

## Goal

Determine whether at least one load dataset supports a reproducible, leakage-free graph and whether a genuine Euclidean GCN/HGCN pair can run on the same temporal pipeline.

## Ordered work

1. Inventory local/public multi-node load datasets and their topology/hierarchy mappings, licences, temporal coverage, and missingness.
2. Select one graph type: physical topology, documented hierarchy, or training-window-only functional graph. Never use validation/test values to construct it.
3. Freeze nodes, edges, time split, forecast horizons, covariates, normalization, and missing-data rules.
4. Implement a Euclidean GCN with the shared temporal encoder as the sanity baseline.
5. Implement genuine hyperbolic graph convolution with explicit maps, curvature, aggregation, projection, and numerical tests.
6. Run 3–5-seed pilots against target-self, persistence, DLinear, Euclidean GCN, and existing CSA variants.
7. Only after leakage, numerical stability, and fairness gates pass, freeze the formal rolling-origin experiment.

## Decision outcomes

- **GO:** at least one explainable graph and both GCN/HGCN implementations pass end-to-end tests.
- **CONDITIONAL:** one reliable dataset only or HGCN does not beat Euclidean GCN; write a bounded/negative result without performance hype.
- **NO-GO:** no defensible graph, test leakage, or the implementation remains distance attention rather than graph convolution.

## Author input

A real multi-node load dataset with feeder/bus topology would be the strongest addition. Public SimBench or documented hierarchy data can start the gate if no private data are available.
