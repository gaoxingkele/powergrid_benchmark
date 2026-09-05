# P4 Frozen Graph-Geometry Forecasting Protocol

**Stage:** `p4_v2_s04_frozen_experiment_protocol`

**Status:** `FROZEN / NOT_EXECUTED / NO_RESULTS`

**Frozen on:** 2026-09-05 (Asia/Shanghai)

**Machine-readable authority:** `config.json`

**Protected predecessor:** `../p2_s3_identifiable_v1/` is read-only.

This is a prospective protocol, not experiment evidence. It freezes the data,
model, tuning, evaluation, and reporting rules before any pilot or formal P4
graph-geometry forecast is run. Pilot outputs belong only under `pilot/` and
cannot select a configuration or appear in tuning, formal inference, or the
paper. Accepted predecessor results retain their historical scope and are not
imported as observations in this experiment.

## Dataset, Licence, Node, and Target Freeze

The permitted conditions are the Ausgrid solar-home hierarchy (`Hier`) and the
OPSD six-country load record (`Dense`). `data_manifest.json` is authoritative
for node order, source columns, hierarchy membership, edge rules, source hashes,
and licence gates. Raw Ausgrid files and source-specific licence records are not
present in this worktree. The inherited OPSD byte hash is recorded, but its
licence evidence is also absent here. No data are authorized for formal
execution or redistribution until those fields are completed and checked.
Completing a path, hash, or licence field may identify the frozen source; it may
not change the dataset, node map, or task.

For Ausgrid, the ordered nodes are the twelve disclosed customer IDs, four
deterministic regional sums, and one system sum. The sixteen child-parent edges
are an accounting tree, not electrical feeder topology. The leaf list was
selected in the historical workflow using full-record availability and energy;
that limitation is retained. Freezing the list before this experiment prevents
outcome-adaptive reselection but does not make the historical rule train-only.

For OPSD, the ordered nodes are DE, FR, IT, ES, NL, and PL. In each outer split,
an undirected edge exists only when absolute Pearson correlation is at least
0.7 over at least 168 pairwise-finite rows strictly before the training cutoff.
The graph is rebuilt per outer split. Validation/test values, future
missingness, labels, and model errors are forbidden inputs.

Each model predicts one scalar for every node at processed position `t+24` from
the 168 positions ending at `t`. Both datasets use lead 24 only. These are
processed-position semantics, not guaranteed elapsed hours.

## Rolling Origins, Visibility, Normalization, and Covariates

Exact development and formal anchors are frozen in `config.json`. Development
blocks precede and are disjoint from all formal blocks. Every block contains 672
consecutive forecast origins with stride one. Training origins use stride three,
and their targets must end strictly before the block anchor. The last 15% of
eligible training origins by time is an internal checkpoint-validation segment;
it cannot tune model-family hyperparameters.

Per outer block and node, the sample mean and sample standard deviation are
fitted from finite training-prefix load values only and reused unchanged for
validation and test. A zero or non-finite standard deviation fails the cell. No
imputation or interpolation is permitted. Source parsing and row rejection run
before splitting, and their counts and timestamp lists must be retained.

The only covariates are four sequence-phase terms computed from processed target
position: sine and cosine of position modulo 24, and sine and cosine of
`floor(position/24)` modulo 7. No weather, holiday, localized civil-time,
daylight-saving, price, future-load, or externally forecast covariate is used.

Each graph record must contain ordered node IDs, source-manifest SHA-256, graph
kind and rule, exclusive train cutoff, threshold and minimum overlap where
applicable, random-control seed where applicable, self-loop policy, exact
training-value digest for value-derived graphs, edge list, and adjacency SHA-256.
Self-loops are added only during convolution normalization.

## Frozen Methods and Direct Ablations

The final matrix contains ten arms:

| Arm | Graph | Geometry / role | Licensed comparison scope |
|---|---|---|---|
| Persistence | none | last observed value | deterministic naive baseline |
| DLinear | none | decomposed linear model | strong non-graph baseline |
| CSA-LoadNet | none | accepted dense attention implementation, rerun | non-graph baseline; never called GCN/HGCN |
| EuclideanGCN-Real | frozen real graph | Euclidean | matched geometry control |
| HGCN-Fixed1-Real | frozen real graph | Poincare ball, `c=1` | primary HGCN arm |
| HGCN-Learnable-Real | frozen real graph | Poincare ball, learned positive curvature | secondary curvature variant |
| EuclideanGCN-Identity | identity | Euclidean | graph ablation cell |
| HGCN-Fixed1-Identity | identity | Poincare ball, `c=1` | graph/geometry factorial cell |
| EuclideanGCN-Random | fixed random control | Euclidean | graph ablation cell |
| HGCN-Fixed1-Random | fixed random control | Poincare ball, `c=1` | graph/geometry factorial cell |

The real-graph Euclidean/HGCN pair has the same ordered data, adjacency,
168--96--48 temporal encoder, four covariates, prediction head, layer count,
hidden width, optimizer, batches, epochs, and tuning budget. Only geometry
changes; learned curvature adds one scalar and the parameter-count difference
must remain below 10%. Fixed-zero geometry is represented by the Euclidean GCN,
not a near-zero-curvature approximation.

Graph-only contrasts hold geometry fixed at `c=1` and compare real with identity
and random graphs. The geometry-only contrast holds the real graph fixed and
compares fixed-curvature HGCN with Euclidean GCN. The difference-in-differences
contrast compares that geometry effect between real and identity graphs. It is
a joint interaction contrast and cannot allocate an effect to one layer. Random
graphs use the frozen graph seed and match the real graph's undirected edge
count; an Ausgrid random graph must also be a connected tree. These are controls,
not alternative physical networks.

## Tuning Budget and Final-Test Separation

Persistence has no tuned parameter. DLinear, CSA-LoadNet, EuclideanGCN-Real,
HGCN-Fixed1-Real, and HGCN-Learnable-Real each receive exactly eight candidate
configurations per dataset, evaluated on the same three development blocks and
three development seeds: 72 runs per family per dataset and 720 tuning runs in
total. Candidate grids are explicit in `config.json`. Selection minimizes
median development-block WAPE after averaging the three seeds within each block;
ties use the lexicographically smallest configuration ID. Every tuning row and
selection decision must be released.

Identity and random arms inherit the selected setting of their same-geometry
real-graph arm and are not retuned. All neural and linear fits run 20 complete
epochs, use the frozen batch size and optimizer budget, and restore the lowest
internal-validation MSE checkpoint. No early termination, test-driven restart,
or extra candidate is allowed.

Formal evaluation then uses all eight later blocks and paired seeds
`{11,23,47,59,71}`. No development seed or block occurs in the formal schedule.
Formal test targets are unavailable to configuration and checkpoint selection.
There are 720 trainable formal runs plus 16 deterministic persistence block
outputs. A pilot may only confirm feasibility or trigger no-go; it cannot alter
grids or select settings.

## Outcomes, Analysis Unit, and Comparison Family

The primary outcome is block-level WAPE. For Ausgrid it is the equal-weight mean
of leaf-, region-, and root-pooled WAPE; for OPSD it is WAPE pooled over the six
nodes. MAE, RMSE, MAPE, and sMAPE are secondary/descriptive, with percentage-
metric denominator limitations retained. Point forecasts have no probabilistic
calibration target: coverage, interval width, CRPS, ECE, and reliability claims
are `NOT_APPLICABLE`, not zero. Mean signed error is descriptive bias and is not
called calibration.

Efficiency outcomes are parameter count, completed epochs, training seconds,
inference seconds for a 672-origin block, peak host memory, and peak CUDA memory
when used. They are machine-specific. Numerical outcomes include non-finite
loss/gradient/state counts, projection and tangent-clipping counts, curvature
range, failed cells, and the retry ledger.

The outer unit is the rolling-origin block. Seeds are averaged within each
method--dataset--block before inference. Fourteen frozen two-sided primary
contrasts (seven per dataset) form one family: fixed-curvature HGCN versus the
matched Euclidean GCN, identity graph, random graph, DLinear, persistence, and
CSA, plus the real-versus-identity geometry difference-in-differences. Exact
paired sign-flip tests over eight block differences receive one Holm correction
at familywise alpha 0.05. Report mean paired difference, raw and adjusted
p-values, wins/ties/losses, and a pointwise 95% percentile interval from 20,000
deterministic block resamples. No equivalence margin is defined; non-significance
is not equivalence or evidence of no advantage. Learnable-curvature, secondary-
metric, efficiency, and stability comparisons are descriptive and cannot rescue
a failed primary claim.

## Failure and Negative-Result Policy

An infrastructure failure before data or model execution may be rerun once with
the identical cell and environment after its cause is logged. Algorithm
exceptions, non-finite quantities, timeouts, resource exhaustion after model
start, and numerical safeguards firing to failure remain observed outcomes:
retain the row, do not replace the seed, and do not impute. Any missing member
of a paired primary contrast makes it incomplete; do not run a favorable
complete-case test.

All null, adverse, unstable, failed, and resource-limited outcomes are reported.
No dataset subset, seed subset, secondary metric, learned-curvature variant, or
historical result may replace a failed primary contrast. Combined ablations
support joint conclusions only. A favorable hierarchy result remains conditional
on this constructed accounting hierarchy; the dense graph remains nonphysical.
No result can establish deployment value, physical topology validity, general
forecasting superiority, or state of the art.

## Execution Gate

`planned_vs_executed.json` intentionally states `NOT_EXECUTED`. Formal work is
blocked until source identities and licences are verified, raw and processed
hashes are recorded, anchors are resolved against frozen sources, a runner emits
the required schema, the runtime passes a non-paper pilot, and the resource
budget is accepted. An amendment after outcomes become visible invalidates
confirmatory status. No result claim may be added until the separate evidence
stage verifies the formal manifest.
