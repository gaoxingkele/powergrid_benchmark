# Figure 7: Schematic workflow of the hybrid GWO-PSO algorithm
- **Source**: Figure 7, Section 5 (page 22) in the review
- **Caption**: "Schematic workflow of the hybrid GWO-PSO algorithm, detailing the HRES control calculation."
- **Screenshot**: figure7.png (page 22; flowchart in the lower half, below Table 7)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (flowchart; MathWorks watermark bottom-left):
  - **Start** (oval) → "Data" input.
  - **GWO Exploration branch** (left column): "Update SEARCH AGENT Positions based on Alpha, Beta, Delta" → "Update Alpha, Beta, Delta Search Agents" → "Evaluate Fitness of updated population" → decision diamond "GWO Iteration Limit Reached?" (NO loops back — dashed — to updating the search agents; YES exits the branch).
  - **Handoff block** (top centre, with GWO wolf / CPU / PSO icons): "Transfer top GWO solutions as initial PSO particles—Initialize particle velocities."
  - **PSO Exploitation branch** (right column): "Calculate Particle Velocities" → "Update Particle Positions" → "Evaluate Fitness of updated population" → "Update Personal Best (pbest) and Global Best (gbest)" → decision diamond "PSO Iteration Limit reached OR Convergence Threshold met?" (NO loops back — dashed — to updating particle positions; YES proceeds).
  - **Output**: "Output Best Solution (Gbest for HRES control)" → **END** (oval).
- **Connections**: solid arrows for the forward flow; dashed arrows for the two iteration loops and the "PSO Exploitation" handoff label.
- **What it conveys**: the dual-strategy division of labour — GWO's alpha/beta/delta hierarchy performs global exploration until its iteration limit, its top solutions seed the PSO swarm, and PSO's pbest/gbest updates exploit that region to convergence, emitting the final gbest as the HRES control solution (§4.2, ref [63]). This is the mechanism behind C04.
- **Numbering note**: §4.2's running text cites this workflow as "Figure 6", but the printed caption is "Figure 7" (Figure 6 is the DC-coupled HESS diagram). Filed by printed caption.

**Supports claims**: C04
