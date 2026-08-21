# Figure 1: Optimized scheduling flowchart

- **Source**: Figure 1, Section 3.3 (page 8)
- **Caption**: "Optimized scheduling flowchart."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (vertical sequence of rounded boxes, top to bottom):
  1. "When the load is determined, the scheduling of the output power of various distributed power sources begins."
  2. "Photovoltaic and wind power operate at their maximum output power levels."
  3. "Adjust the operating states of the thermal generator and energy storage devices to ensure that the output of all distributed power sources can meet the system load demand."
  4. "Based on the distributed power source model and the state constraint model, the objective function is constructed."
  5. "The SCMPSO (Stochastic Constrained Multi-Objective Particle Swarm Optimization) algorithm is utilized to solve the related model, and the optimal scheduling strategy is provided."
  6. "Adjust the output power of each distributed power source according to the optimal scheduling strategy, and calculate the optimal operating cost of the entire system."
- **Connections**: single downward arrow between each consecutive box (linear pipeline, no branches).
- **Annotations**: Box 5 expands the SCMPSO acronym as "Stochastic Constrained Multi-Objective Particle Swarm Optimization" — note this differs from the abstract's expansion "second-order oscillatory chaotic mapping particle swarm optimization". Both names denote the same proposed method.
- **What it conveys**: the dispatch merit order (renewables at max first, storage + thermal to fill the gap, then optimize cost via SCMPSO). Mirrored into `logic/solution/formulation.md` (scheduling strategy) and `logic/solution/algorithm.md`.
