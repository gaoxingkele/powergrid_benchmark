# Evidence Index

## Tables

| ID | Title | Source | Claims | Description |
|----|-------|--------|--------|-------------|
| Table 1 | A brief description of the literature | Section 1.3, p.4 | — | Comparative table of literature related to DESS planning methods, showing network scale, node priority evaluation, planning strategy, objectives, uncertainty modeling, and system-level evaluation for each reference. |
| Table 2 | System of quality demand indicators | Section 3.1.2, p.9 | C01 | Defines 7 quality indicators: I1 (supply reliability expectation), I2 (primary load share), I3 (value of loss per unit shortage), I4 (frequency nonconformance rate), I5 (voltage deviation), I6 (peak-to-valley difference), I7 (customer complaints). |
| Table 3 | Result generation process summary | Section 4.3, p.20 | C01, C02, C03, C04, C05 | Maps each analysis stage (demand evaluation, priority evaluation, DESS planning, electrical evaluation, case comparison) to its inputs, method/tool, outputs, and related paper sections. |
| Table 4 | Equipment Parameters of Each DESS | Section 4.3, p.21 | C02, C03 | DESS cost parameters: unit capacity cost (2000 CNY/kW), unit power cost (600 CNY/kW), annual O&M costs, charge/discharge efficiency (0.95), SOC limits (0.9, 0.2), service life (12 years). |
| Table 5 | Corresponding storage planning results for each case | Section 4.3, p.21 | C02, C03 | Comparison of 3 planning cases: average primary load share, maintenance cost, economic benefit, configured nodes and capacities, belonging block. Case 3 achieves highest economic benefit with balanced spatial distribution. |
| Table 6 | System-level electrical performance comparison at energy storage nodes before and after DESS planning | Section 4.3, p.22 | C02, C03 | Peak-to-valley difference (%), frequency violation rate (%), voltage deviation (%) for DESS nodes across Cases 1–3 before and after planning. |

## Figures

| ID | Title | Source | Claims | Description |
|----|-------|--------|--------|-------------|
| Figure 1 | Overall framework of the proposed DESS planning and resilience evaluation method | Section 1.3, p.5 | C01, C03, C04, C05 | Three-stage methodology: historical wind/PV and load data → priority index model (quality + efficiency indicators) → multi-objective optimization → node–block–grid evaluation. |
| Figure 2 | DESS-based resilience enhancement planning framework for distribution networks | Section 2, p.6 | C01, C03 | Internal structure of the planning framework: objective functions, decision variables, and the sequential planning mechanism across grid, block, and node dimensions. |
| Figure 3 | Block diagram illustrating the proposed overall evaluation framework | Section 2, p.6 | C01, C04 | Step-by-step illustration of the priority evaluation and decision-guidance process. |
| Figure 4 | Hierarchical structure of DESS methods and indicators for grid resilience | Section 3, p.7 | C01 | Target layer (grid resilience), method layer (emergency backup, frequency/voltage regulation, peak shaving, economic dispatch), and indicator layer (efficiency and quality indicators). |
| Figure 5 | Generalized load curve characteristic diagram | Section 3.1.1, p.8 | C04 | Conceptual illustration of the generalized load curve combining conventional load, demand response, and energy storage. |
| Figure 6 | Grid block distribution schematic | Section 3.4.1, p.13 | C04 | Spatial layout of the 26+ grid blocks in the Zhejiang case study with block type labeling. |
| Figure 7 | Load typical daily output curve | Section 3.4.1, p.13 | C01 | Typical 96-point daily load profiles for different load types (residential, industrial, commercial, etc.). |
| Figure 8 | Representative scenarios of wind and solar power output | Section 3.4.2, p.14 | E01 | GMM-extracted typical output scenarios: (a) PV — clear diurnal patterns, (b) wind — complex multimodal fluctuation patterns. |
| Figure 9 | Probability of typical power output scenarios | Section 3.4.2, p.14 | E01 | Probability distribution across the 5 GMM clusters for both PV and wind scenarios. |
| Figure 10 | Identification of matches and types of blocks of the grid | Section 3.4.4, p.15 | C01, C04 | Source-load matching degree (η) per block, identifying load-dominant (Blocks 21, 23) and generation-dominant (Blocks 1, 26) blocks. |
| Figure 11 | Planning process diagram | Section 4.1, p.16 | C02 | Flowchart of the sequential planning process: GMM scenario extraction → priority index ranking → sequential DESS siting/sizing → budget constraint check → iteration. |
| Figure 12 | Schematic Diagram of DESS | Section 4.3, p.19 | C02 | System architecture diagram showing wind and PV generation units, energy storage system, and electrical interconnections. |
| Figure 13 | Result-oriented process flow diagram | Section 4.3, p.20 | C03, C04 | Logical connection between priority index evaluation, sequential siting/sizing, and assessment of system-level electrical performance. |
| Figure 14 | Priority indices obtained from each node iteration | Section 4.3, p.21 | C01, C02 | Node-level and block-level priority indices: (a) per-node H_pi values, (b) per-block aggregated priority. Shows which nodes were selected across iterations. |
| Figure 15 | Demand indicator chart for selected nodes in each case | Section 4.3, p.23 | C02, C03 | Indicator profiles for selected DESS nodes: Case 1 shows larger variation (weaker demand correspondence), Cases 2 and 3 align better with actual demand intensity. |
| Figure 16 | Comparison of evaluation indicators across cases | Section 5, p.25 | C03, C04, C05 | Bar/radar chart comparing O1, O2, O3, L1, L2, G1, G2 for Cases 1–3. Case 3 leads in all metrics, especially G2 (+324%) and O2 (+102%). |
