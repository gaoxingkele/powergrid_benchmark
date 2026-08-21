# Figure 3: GCN structure

- **Source**: Figure 3, §2.2 (page 6, upper half of page)
- **Caption**: "GCN structure."
- **Screenshot**: figure3.png (full-page render of p.6)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - Two green input boxes on the left: *adjacent matrix* (drawn as a small node-edge graph)
    and *Feature Matrix*.
  - A large blue central panel containing multiple copies of the same feature graph, each with a
    different node highlighted in red, labeled "Spatial feature for node 1", "Spatial feature for
    node 2", "…", "Spatial feature for node 8" (ellipsis between node 2 and node 8 indicates the
    intermediate nodes).
  - A small box "σ(·)" (nonlinear activation) after the panel.
  - A yellow *Output* box on the right containing the resulting graph.
- **Connections**: adjacency matrix + feature matrix → (graph convolution) per-node aggregation
  panel → σ(·) → output graph representation.
- **Annotations**: red node in each sub-graph marks the node whose spatial feature is being
  aggregated from its neighbors; 8 nodes total, matching the 8-dimensional meteorological feature
  vectors (§2.2).
- **What it conveys**: the GCN computes, for each of the 8 feature-nodes, a spatial feature by
  aggregating the node with its graph neighbors (per Eq. 1, symmetric-normalized adjacency with
  self-loops), then applies a nonlinear activation to produce the output representation. Structure
  mirrored into `logic/solution/architecture.md` (component 3).
