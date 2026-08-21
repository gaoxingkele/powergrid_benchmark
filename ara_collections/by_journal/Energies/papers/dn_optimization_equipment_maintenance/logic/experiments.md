# Experiments

## E01: Three-Scheme Comparison of Flexibility and Grid Interconnection

**Verifies:** C01 (flexibility-grid interconnection synergy), C03 (hybrid algorithm effectiveness), C04 (predictive maintenance via branch flexibility)

**Evidence:** evidence/tables/table1.md (Grid indicator results), evidence/tables/table2.md (Optimization results under different schemes)

**Run:** Simulation on modified CPS62-node system (3 interconnected grids, 62 nodes, 18 pages)

**Setup:**
- System: CPS62-node benchmark derived from real-world medium-voltage grid in China. Three interconnected grids (Grid 1, 2, 3) with tie-lines. PV at nodes 14, 35, 49. Wind at nodes 6, 26, 55. ESS at nodes 8, 31, 50. Base voltage 12.66 kV, power reference 1 MVA. Branch capacity limit 1 MW. GT output capped at 0.3 MW, ESS capacity 0.9 MWh.
- Three scheme conditions:
  - Scheme 1: No flexibility index, no grid interconnection (traditional cost-only optimization)
  - Scheme 2: Flexibility index included, no grid interconnection
  - Scheme 3: Both flexibility index and grid interconnection included
- Upper-layer objectives: FBF (branch flexibility adequacy) and C_loss (network loss cost)
- Lower-layer: DRO with comprehensive norm ambiguity set
- Solver: Hybrid ACO-FHO-DE with Tent chaos initialization

**Procedure:**
1. Configure CPS62 system with three sub-grids, renewable generators, ESS, and flexible loads.
2. Run Scheme 1: single-layer cost optimization without flexibility or interconnection.
3. Run Scheme 2: upper-layer optimization with FBF, lower-layer DRO, but no tie-line activation.
4. Run Scheme 3: full two-layer optimization with FBF and tie-line activation.
5. Record flexibility deficits, curtailed renewable energy, branch flexibility adequacy for each sub-grid.
6. Record operation cost breakdown: source-side, load-side, flexibility deficit, comprehensive cost.

**Metrics:**
- Grid flexibility deficit (unitless, 0-1 range)
- Grid branch flexibility adequacy (unitless, 0-1 range)
- Curtailed wind-solar energy (kWh)
- Operation cost components (CNY 10,000)
- Comprehensive cost (CNY 10,000) = total operation cost + flexibility deficit cost

**Expected Outcome (directional, no exact numbers):**
Scheme 3 is expected to have the lowest flexibility deficits and comprehensive cost, despite potentially higher operation cost than Scheme 1, demonstrating that flexibility-interconnection synergy reduces overall system cost. Scheme 2 should improve flexibility over Scheme 1 but to a lesser extent than Scheme 3. Grids with high renewable penetration (Grid 1, Grid 2) should benefit more from interconnection than Grid 3.

**Baselines:** Scheme 1 (no flexibility, no interconnection — traditional approach), Scheme 2 (flexibility without interconnection)

**Dependencies:** CPS62 test system configuration, hybrid ACO-FHO-DE solver

---

## E02: Monte Carlo Comparative Analysis of Uncertainty-Handling Methods

**Verifies:** C02 (DRO outperforms deterministic/stochastic/robust), C03 (hybrid algorithm), C05 (two-layer architecture tractability)

**Evidence:** evidence/figures/figure7.md (Monte Carlo statistical comparison bar chart), evidence/figures/figure8.md (Cost comparison under typical scenarios)

**Run:** Monte Carlo simulation with 500 scenarios on CPS62 system

**Setup:**
- 500 synthetic wind-solar-load scenarios generated using Latin Hypercube Sampling based on historical data distributions.
- Scenarios clustered to select K representative scenarios.
- Four optimization models compared:
  - Deterministic: forecasts as point values, no uncertainty modeling
  - Stochastic programming: multiple scenarios with assigned probabilities
  - Traditional robust optimization: worst-case protection
  - Proposed DRO: comprehensive norm ambiguity set (joint 1-norm and infinity-norm)
- Three typical scenarios selected for detailed analysis:
  - (a) High wind-solar generation + peak load
  - (b) Medium wind-solar output + flat load
  - (c) Low renewable generation + valley load

**Procedure:**
1. Generate 500 uncertainty scenarios using Latin Hypercube Sampling from historical wind, PV, and load data.
2. Cluster scenarios into K representative scenarios with initial probabilities p^0_k.
3. Construct DRO ambiguity set with confidence bounds theta_1, theta_inf.
4. Solve each of the four models for all 500 scenarios.
5. Record total operation cost for each model-scenario combination.
6. Compute average cost and maximum (worst-case) cost across all scenarios.
7. Compare cost distributions under three typical scenario categories.

**Metrics:**
- Average total operation cost across 500 scenarios (CNY 10,000)
- Maximum total operation cost (worst-case scenario, CNY 10,000)
- Cost distribution shape under different uncertainty conditions

**Expected Outcome (directional, no exact numbers):**
The deterministic model is expected to show the highest average and maximum cost. The stochastic model should achieve lower average cost than robust but higher worst-case cost. The traditional robust model should have lower worst-case cost than stochastic but higher average cost due to conservatism. The proposed DRO model should achieve the lowest or near-lowest on both metrics, representing the best trade-off between robustness and economic efficiency.

**Baselines:** Deterministic optimization, stochastic programming, traditional robust optimization

**Dependencies:** E01 system configuration, Latin Hypercube Sampling implementation

---

## E03: Grid Interconnection Impact on Sub-Grid Resource Balancing

**Verifies:** C01 (flexibility-interconnection synergy), C04 (branch stress maintenance)

**Evidence:** evidence/figures/figure6.md (grid interconnection topology after optimization), evidence/tables/table1.md (per-grid indicators)

**Run:** Comparative analysis of sub-grid indicators across interconnection states

**Setup:**
- Same CPS62 system as E01.
- Focus on comparing pre-interconnection (Schemes 1, 2) vs. post-interconnection states (Scheme 3).
- Per-grid metrics: curtailed wind-solar energy, flexibility deficit, branch flexibility adequacy.
- Branch switching states tracked to evaluate load redistribution.

**Procedure:**
1. Record per-grid metrics for Schemes 1, 2, and 3 from E01 results.
2. Analyze the distribution of flexibility deficits and curtailment across Grids 1, 2, 3.
3. Identify how interconnection (tie-line activation) redistributes power flows.
4. Compare branch flexibility adequacy changes per grid to assess stress redistribution.

**Metrics:**
- Per-grid curtailed wind-solar energy (kWh)
- Per-grid flexibility deficit (unitless)
- Per-grid branch flexibility adequacy (unitless)
- Inter-grid imbalance ratio

**Expected Outcome (directional, no exact numbers):**
Grids with high renewable penetration (Grids 1, 2) are expected to show the largest improvement from interconnection. Grid 3, with lower renewable penetration, should show smaller changes. Under Scheme 3, the flexibility adequacy values across grids should converge toward more balanced levels compared to Schemes 1 and 2. The redistribution of branch loading through interconnection should reduce the peak stress on heavily loaded branches.

**Baselines:** Pre-interconnection states (Schemes 1 and 2)

**Dependencies:** E01 results, CPS62 system topology
