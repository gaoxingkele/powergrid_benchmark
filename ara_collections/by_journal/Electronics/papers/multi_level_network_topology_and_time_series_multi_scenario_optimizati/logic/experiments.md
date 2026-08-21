# Experiments

## E01: Single-stage topology optimization, DC-load vs all-AC scenario (13-node)
- **Verifies**: C01, C06
- **Evidence**: evidence/figures/figure7.md
- **Run**: Two-layer optimization model solved by the Pareto-niche binary PSO (SABPSO) described in §4; no released code (see src/environment.md)
- **Setup**:
  - Model: bi-level time-series multi-scenario planning model (§3-4)
  - Hardware: Not specified in paper
  - Dataset: 13-node radial distribution test network with distributed PV/WT and a diesel generator
  - System: Scenario 1 = data center with DC + AC loads, PV, WT; Scenario 2 = same loads but all treated as AC (DC loads superimposed on AC)
- **Procedure**:
  1. Set economic parameters (discount rate, VSC unit cost, line investment, converter efficiency, planning life, conventional output cost)
  2. Optimize topology (bus AC/DC type, line DC conversion, DG type/capacity) minimizing the objective
  3. Compare resulting AC/DC morphology between the two scenarios
- **Metrics**: DC vs AC share of buses/lines in the optimal topology; which buses become DC
- **Expected outcome**:
  - The scenario with real data-center DC loads yields a topology with a substantially larger DC share than the all-AC scenario
  - Buses hosting DC loads / new-energy units are preferentially selected as DC buses
- **Baselines**: Scenario 2 (all-AC) as the comparison against Scenario 1
- **Dependencies**: none

## E02: Multi-stage dynamic topology evolution over rising DC-load penetration (13-node)
- **Verifies**: C01, C02, C06
- **Evidence**: evidence/figures/figure8.md, evidence/tables/table3.md
- **Run**: Same two-layer SABPSO model, re-solved per penetration stage
- **Setup**:
  - Model: bi-level time-series multi-scenario planning model
  - Hardware: Not specified in paper
  - Dataset: 13-node network, initial 0% DC-load penetration, +10% per 15-year planning cycle
  - System: successive planning cycles at 0-80% penetration
- **Procedure**:
  1. Start from the 0%-penetration optimal topology
  2. Increase DC-load penetration one cycle at a time
  3. Re-optimize and record which busbars/lines are retrofit to DC and which new DC lines are built each phase
- **Metrics**: staged busbar/line DC retrofit set; buses retained as AC
- **Expected outcome**:
  - No DC retrofit is optimal below a moderate penetration; DC structure grows monotonically as penetration rises
  - Grid-connection buses and large-capacity AC-generator buses remain AC even at the highest penetration
- **Baselines**: the 0%-penetration all-AC topology
- **Dependencies**: E01

## E03: IEEE33 planning with line DC retrofit/new-build enabled ("consider DC")
- **Verifies**: C03, C05
- **Evidence**: evidence/tables/table5.md, evidence/tables/table6.md, evidence/figures/figure10.md
- **Run**: SABPSO planning over the modified IEEE33 system; no released code
- **Setup**:
  - Model: bi-level time-series multi-scenario planning model
  - Hardware: Not specified in paper
  - Dataset: modified IEEE33 (per-node DC-load proportions from Table 4; five added load points 33-37; DG candidate node set; DG in 60 kVA increments)
  - System: DC line reconstruction and DC new construction allowed
- **Procedure**:
  1. Assign per-node DC-load proportions and add the five data-center load points
  2. Optimize DG type/capacity/location, line DC conversion, and new-line form (AC/DC)
  3. Record DG configuration, DC-modified circuits, new lines, and objective-function values
- **Metrics**: DG placement/capacity; DC-modified and new lines; the five objective cost components; total cost; loss; voltage-stability index
- **Expected outcome**:
  - DC lines and DG concentrate at feeder ends; most DG connects within DC sub-systems
  - New load points with high DC-load share are connected via DC lines
- **Baselines**: compared against E04 (DC-forbidden)
- **Dependencies**: none

## E04: IEEE33 planning with line DC retrofit/new-build forbidden ("exclude DC")
- **Verifies**: C05
- **Evidence**: evidence/tables/table7.md
- **Run**: SABPSO planning over the modified IEEE33 with the DC-line option removed
- **Setup**:
  - Model: bi-level time-series multi-scenario planning model
  - Hardware: Not specified in paper
  - Dataset: same modified IEEE33 as E03
  - System: no DC power supply permitted in the network (all new lines AC, no line DC conversion)
- **Procedure**:
  1. Re-run the optimization with DC line reconstruction/new-build disabled
  2. Record the DG configuration and new (AC) lines
- **Metrics**: total hosted DG capacity; new-line set
- **Expected outcome**:
  - Total hosted DG capacity is lower than in the DC-enabled plan
- **Baselines**: E03 (DC-enabled)
- **Dependencies**: E03

## E05: Consider-DC vs exclude-DC objective comparison (IEEE33)
- **Verifies**: C04, C08
- **Evidence**: evidence/tables/table8.md, evidence/figures/figure11.md
- **Run**: Post-processing comparison of the E03 and E04 optima
- **Setup**:
  - Model: same planning model, two solved cases
  - Hardware: Not specified in paper
  - Dataset: modified IEEE33
  - System: consider-DC (E03) vs exclude-DC (E04)
- **Procedure**:
  1. Tabulate each objective component for both cases
  2. Compute per-branch annual average voltage-stability index for both
  3. Compare total cost, network loss, and stability
- **Metrics**: per-component and total annual economic cost; annual active-power loss; per-branch and average voltage-stability index
- **Expected outcome**:
  - The DC-enabled plan has lower total economic cost and network loss
  - Per-DG and per-load converter costs collapse when DC is allowed, offset by a DC-line converter cost
  - DC-converted/new-DC branches show zero AC voltage-stability index; hybrid network is more stable than pure-AC
- **Baselines**: exclude-DC case
- **Dependencies**: E03, E04

## E06: Practical-engineering regional DC-interconnection evaluation
- **Verifies**: C09
- **Evidence**: evidence/tables/table9.md
- **Run**: Field data analysis of a regional network (4 substations); no optimization run
- **Setup**:
  - Model: engineering evaluation (load-rate analysis)
  - Hardware: Not specified in paper
  - Dataset: maximum annual load rates of feeder/link line pairs across four substations in a region
  - System: candidate lines for DC interconnection, including lines already using soft-straightening technology
- **Procedure**:
  1. Collect maximum annual load rates of feeder and link line pairs
  2. Identify pairs with poor mutual transfer reliability (unbalanced load rates)
  3. Recommend DC interconnection for those pairs
- **Metrics**: feeder vs link maximum annual load rate per line
- **Expected outcome**:
  - Unbalanced-load-rate feeder pairs are flagged as the DC-interconnection candidates; existing soft-straightened lines support feasibility
- **Baselines**: none
- **Dependencies**: none

## E07: Multi-level topology design-adequacy analysis by reliability tier
- **Verifies**: C07
- **Evidence**: evidence/tables/table1.md, evidence/figures/figure1.md, evidence/figures/figure2.md, evidence/figures/figure3.md, evidence/figures/figure4.md, evidence/figures/figure5.md
- **Run**: Design/architecture analysis (§2); no simulation
- **Setup**:
  - Model: qualitative physical-level topology design
  - Hardware: Not specified in paper
  - Dataset: GB50174 / TIA-942 / Uptime tier standards
  - System: flexible-DC supply architectures for Tier A/B/C data centers
- **Procedure**:
  1. Map GB50174 grades to Uptime/TIA tiers and their power-supply configuration methods
  2. For each tier, design a flexible-DC supply topology (bus count, redundancy, backup)
  3. Check that each design meets its tier's availability requirement
- **Metrics**: supply-path count; equipment redundancy level (2N, N+1, N); presence of hot-standby paths
- **Expected outcome**:
  - Higher reliability tiers require more redundant DC supply architectures (dual bus + hot standby for fault-tolerant tiers, single path + N+1 for redundant, single path for basic)
- **Baselines**: none
- **Dependencies**: none
