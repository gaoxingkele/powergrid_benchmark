# Related Work

## Research Streams Identified

### 1. Wind-PV-Storage Integrated System Planning
Common approach: collaborative configuration of flexibility resources in high-penetration systems.

**Key references and contributions:**
- **Liang et al.** [3]: Three-level structure with bidirectional converters for hybrid AC/DC microgrid clusters
- **Wu et al.** [4]: Cyber-physical integrated planning with spatiotemporal flexible resources and multi-network coupling
- **Liu et al.** [5]: Three-level robust ESS planning accommodating wind power investment uncertainty and coal plant retirements
- **Lu et al.** [6]: Quantitative index system for power system flexibility and collaborative source-grid-load-storage planning
- **Zhu et al.** [7]: Coordinated planning of energy storage and Soft Open Points (SOPs) using multi-timescale flexibility indices
- **Lee et al.** [8]: Integrated planning of generators, transmission lines, and ESS using two-stage Benders decomposition
- **Huo et al.** [9]: Lightweight data-driven planning model for HESS based on production simulation

**Gap identified**: Flexibility resource synergy mechanisms in these approaches are imperfect and do not fully integrate dynamic response characteristics of multi-dimensional resources (source, network, load, storage).

### 2. Hybrid Energy Storage Systems for Power Fluctuation Mitigation
**Key references:**
- **Wang et al.** [10]: Hybrid ESS for wind-PV composite power fluctuations considering complementary characteristics
- **Wang et al.** [11]: MADRL-based power smoothing control for multi-wind turbines and ESS
- **Li et al.** [12]: PCA-based incomplete data equivalence for data-driven ESS dispatch models
- **Erdinc** [13]: Real-time energy management for residential communities with PV and ESS

**Gap identified**: Existing work primarily focuses on wind-storage or PV-storage at farm level; limited attention to large-scale centralized ESS in regional grids with both utility-scale PV and wind.

### 3. VMD-Based Power Decomposition for HESS
**Key references:**
- **Ma et al.** [15]: Double-layer VMD with energy entropy thresholds for mode mixing mitigation
- **Fang et al.** [16]: VMD combined with Wigner-Ville Distribution for net load decomposition
- **Zheng et al.** [17]: VMD for HESS capacity configuration in secondary frequency regulation
- **Tang et al.** [18]: VMD-ST-QF load frequency division strategy
- **Zhou et al.** [19]: IBWO-VMD-TCN for industrial load decomposition and prediction

**Gap identified**: Existing methods exhibit significant subjectivity in selecting key VMD parameters (K, alpha) and overlook the critical step of determining specific power allocation to different storage types after decomposition.

### 4. Metaheuristic Algorithms for Energy Storage Planning
**Key references:**
- **Cheng and De Waele** [27]: Original Weighted Average Algorithm — novel metaheuristic based on weighted average position concept
- **Maheedhar and Deepa** [23]: COOT algorithm
- **Zhang et al.** [25]: Improved PSO for battery-supercapacitor ESS sizing
- **Asija and Choudekar** [26]: Multi-objective hybrid DE-PSO for congestion management

**Gap**: Standard WAA converges to local optima in complex high-dimensional bi-level HESS planning and has insufficient Pareto diversity for multi-objective optimization.

## Positioning of Current Work
The paper positions itself as addressing the identified gaps by:
1. Proposing a bi-level model integrating planning and operation for multi-timescale flexibility
2. Developing PSO-VMD for adaptive, objective-free parameter selection
3. Enhancing WAA with refraction opposition-based learning and dynamic crowding distance
4. Validating on real grid data from Southwest China with five comparative schemes
