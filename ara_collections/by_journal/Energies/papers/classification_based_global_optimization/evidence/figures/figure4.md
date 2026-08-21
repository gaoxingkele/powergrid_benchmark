# Figure 4 - Unified Planning Pseudocode

**Source**: Figure 4, Section 2.3
**Caption**: Unified planning pseudocode.
**Screenshot**: figure4.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: medium

## Visual description
- **Components**:
  - Start block: "Start"
  - Input block: "Read network data (load data, bus data, line data)"
  - Power flow base case block
  - Classification blocks (active and reactive power)
  - Three sequential sub-processes: EVCS placement -> DGs placement -> CBs placement
  - Final evaluation block with power flow and all performance metrics
  - Output block: optimal configuration with all parameters
- **Connections**: Linear flow: Start -> Read data -> Run base case PF -> Classify branches (active PF for EVCS/DG, reactive PF for CB) -> Place EVCSs -> Place DGs -> Place CBs -> Run final PF with all components -> Output results. Each placement sub-process contains its own iterative tuning loop.
- **Annotations**: The unified flowchart shows the sequential ordering: EVCS first (the stressor), then DGs (active power), then CBs (reactive power). All three converge into a single final evaluation.
- **What it conveys**: The complete CGO methodology is a three-stage sequential process within a deterministic, classification-guided search framework.
