# P4 Leakage-Free Graph and Model Implementation Contract

**Stage:** `p4_v2_s03_graph_data_model_implementation_contract`  
**Status:** implementation contract frozen; pilot and formal protocols not frozen; `NO_RESULTS`  
**Protected predecessor:** `../p2_s3_identifiable_v1/` remains unchanged.

This artifact freezes executable semantics without claiming a forecast result. The machine-readable authority is `implementation_contract.json`; `graph_data.py`, `models.py`, and `verify_implementation.py` implement and check it.

## Nodes, Targets, and Graph Provenance

The Ausgrid condition has 17 nodes: 12 source-manifest customer leaves, four deterministic regional sums, and one system sum. A leaf target is its observed load at processed position (t+24); every aggregate target is the contemporaneous sum of its registered descendants. Leaf identity, selection, and regional membership are intentionally not guessed in this stage: a pilot or formal run must supply those fields and their source hash in a frozen data manifest. The 16 child--parent links are an accounting hierarchy, not asserted feeder topology. `hierarchy_graph` accepts only an explicit source-manifest parent map and rejects incomplete, disconnected, or cyclic/non-tree mappings.

The OPSD condition has the ordered country nodes DE, FR, IT, ES, NL, and PL, bound to the six source columns already registered by the accepted predecessor. Each target is that node's observed load at processed position (t+24). Its undirected functional edge rule is frozen as absolute Pearson correlation at least 0.7 with at least 168 pairwise-finite rows. Correlations use only the prefix `[0, train_stop_exclusive)` and are rebuilt within every outer split. These are functional associations, not physical transmission edges.

Both graph constructors return a binary adjacency without self-loops plus provenance containing ordered node IDs, graph rule, source-manifest digest, exclusive training cutoff, thresholds, and an adjacency digest. The functional graph additionally records a digest of the exact training-prefix values used to construct it. Self-loops are added only by the symmetric convolution normalization. Validation/test values, future missingness, future labels, and observed model errors are forbidden graph inputs. Normalization statistics must likewise be fitted on the training prefix and reused unchanged.

The processed-position qualifier is retained: a lead of 24 is not silently called 24 elapsed hours if source rows are missing.

## Matched Euclidean and Hyperbolic Convolution

`EuclideanGCNForecaster` is the adjacency-based sanity baseline. Each layer computes a learned linear transform followed by multiplication with symmetrically normalized adjacency and a ReLU. It contains no attention scores or dense all-pairs replacement for the supplied graph.

`HyperbolicGCNForecaster` uses the Poincare ball with sectional curvature (-c), (c>0). For point (x) and origin-tangent vector (v), the implemented maps are

\[
\exp_0^c(v)=\tanh(\sqrt{c}\lVert v\rVert)\frac{v}{\sqrt{c}\lVert v\rVert},\qquad
\log_0^c(x)=\operatorname{artanh}(\sqrt{c}\lVert x\rVert)\frac{x}{\sqrt{c}\lVert x\rVert}.
\]

One hyperbolic convolution is `log -> linear -> normalized-adjacency aggregation -> tangent ReLU -> exp`. Readout maps the final state back with `log`. The fixed mode uses (c=1); learnable curvature uses (c=\operatorname{softplus}(c_{raw})+10^{-4}). The fixed-zero geometry cell is the Euclidean GCN itself, avoiding a numerically artificial near-zero-curvature HGCN.

The matched pair uses the same ordered graph, shared 168--96--48 temporal encoder, 48-dimensional graph layers, four calendar terms, 100--64--1 head, layer count, data, and eventual training/tuning budget. Only the geometry changes. Learnable curvature adds one scalar, and the executable audit enforces the predeclared parameter-count difference below 10%.

Numerical safeguards are explicit: a positive curvature floor, tangent-norm clipping, projection inside the open-ball radius, clipping of the `atanh` argument, adjacency validation, and immediate failure on non-finite graph states. A formal runner must additionally record numerical failure counts rather than silently retrying them.

## Mandatory Predecessors and Claim Boundary

CSA-LoadNet remains the accepted predecessor and must not be renamed as a GCN or HGCN. Its rolling-origin aggregation comparison remains unresolved. DLinear remains a mandatory strong non-graph predecessor and its existing exact-hierarchy advantage is preserved. Their historical evidence is not a run of the new models.

The implementation check uses synthetic tensors only to verify invariants, gradients, map round trips, parameter matching, and future-perturbation immunity of graph construction. It is not a pilot, dataset experiment, or source of paper metrics. Therefore the manuscript statement that no GCN or HGCN experiment or result is reported remains scientifically necessary.
