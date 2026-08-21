# Experiments

## E01 — GMM-Based Renewable Scenario Generation

**Verifies:** C01 (foundational — GMM scenarios characterize DG uncertainty used in priority index computation)

**Evidence:**
- Figure 8 (representative scenarios for wind and solar)
- Figure 9 (scenario probabilities)
- CH index criterion determining K=5 as optimal

**Run:**
- Input: Historical wind speed and solar irradiance data from Zhejiang Province distribution grid
- Parameters: K=5 clusters (determined by CH index maximization), RV-coefficient-based K-means initialization
- Algorithm: GMM with expectation-maximization (Equation 5)

**Setup:**
- Data: Historical time-series of wind and PV output for the case study region
- Preprocessing: None specified beyond the RV-coefficient distance metric
- Software: Python 3.9 with GMM implementation (scikit-learn or custom)

**Procedure:**
1. Initialize GMM parameters using K-means clustering with RV coefficient distance metric
2. Optimize parameters via expectation-maximization to maximize log-likelihood (Equation 5)
3. Evaluate clustering quality using CH(K) index (Equation 7–9)
4. Select optimal K where CH(K) is maximized
5. Assign probability weights to each cluster scenario

**Metrics:**
- CH(K) index (maximized at K=5)
- Visual distinctiveness of scenario clusters (diurnal patterns for PV, multimodal patterns for wind)
- Scenario probability distribution

**Expected outcome:** PV scenarios will exhibit clear diurnal patterns with activity during daylight; wind scenarios will show more complex multimodal patterns with temporal variation across clusters. Five clusters will be identified as optimal.

**Baselines:**
- Standard K-means (without RV coefficient)
- Random initialization GMM

**Dependencies:** O2 (need for uncertainty characterization), G3 (scenario generation limitations in literature)

---

## E02 — Priority Index Construction via Critic Weighting

**Verifies:** C01 — Critic method assigns objective weights to quality indicators I1–I7, producing a priority index that differentiates energy storage demand across nodes and blocks.

**Evidence:**
- Table 2 (quality indicator definitions)
- Weights: I1=0.05, I2=0.19, I3=0.15, I4=0.08, I5=0.18, I6=0.17, I7=0.19
- Figure 10 (matching degree identification per block)
- Figure 14 (node-level and block-level priority indices)

**Run:**
- Input: Quality indicator values (I1–I7) per node, efficiency indicator (matching degree η) per block
- Parameters: 7 quality indicators across b nodes
- Method: Critic objective weighting procedure (Equations 11–14)

**Setup:**
- Data: Annual statistical indicators for reliability, power quality, service quality; 96-point daily load profiles
- Scale: 26+ blocks with multiple nodes each in Zhejiang grid
- Software: Python 3.9

**Procedure:**
1. Perform dimensionless processing on quality indicators using Equation (11) (positive vs. reverse indicator normalization)
2. Compute standard deviation S_d for each indicator (Equation 12)
3. Compute Pearson correlation coefficients r_de between indicators (Equation 13)
4. Calculate information measure M_d = S_d * Σ(1 − r_de) for each indicator
5. Derive objective weights ω_d = M_d / Σ(M_d)
6. Combine with efficiency indicator η per Equation (10) to obtain H_pi per node

**Metrics:**
- Priority index value range across nodes
- Rank ordering of blocks/nodes by H_pi
- Weight distribution: I2 (primary load share) and I7 (complaints) have highest weights (0.19 each)

**Expected outcome:** Nodes in load-dominant blocks (e.g., Blocks 21, 23) and generation-dominant blocks (e.g., Blocks 1, 26) will receive higher priority indices due to matching degree extremes. Primary load share (I2) and customer complaints (I7) will dominate the weighting.

**Baselines:**
- Equal weighting (all ω_d = 1/7)
- Subjective/AHP weighting

**Dependencies:** C01, O3, G1

---

## E03 — Sequential Planning Comparison (Cases 1–3)

**Verifies:** C02, C03 — Sequential priority-index updating yields more balanced spatial DESS distribution with higher economic return compared to global traversal and one-shot priority ranking.

**Evidence:**
- Table 5 (storage planning results for each case)
- Table 6 (system-level electrical performance comparison)
- Figure 14 (priority indices per iteration)
- Figure 15 (demand indicator profiles of selected nodes)

**Run:**
- Input: Priority indices, generalized load curves, GMM scenarios, equipment parameters (Table 4)
- Parameters: Budget constraint equivalent to ~3 DESS units, discount rate 0.05, DESS lifetime 12 years
- Solver: Gurobi v11.0 with multi-objective weighted-sum normalization

**Setup:**
- Platform: Python 3.9 + Gurobi 11.0
- Hardware: Not specified (standard workstation)
- Cases: Case 1 (global traversal), Case 2 (one-shot priority), Case 3 (sequential priority)

**Procedure:**
1. Case 1: Solve optimization for all possible node combinations; select combination with best composite objective
2. Case 2: Compute priority indices once for all nodes; select top 3 nodes; solve optimization for their capacities
3. Case 3: Iteratively: (a) select highest-H_pi node, (b) solve optimization for that node, (c) update generalized load and priority indices, (d) repeat until budget reached
4. In all cases, optimize four objectives: lifecycle cost (F1), economic benefit (F2), curtailment rate (F3), peak-valley difference (F4)
5. Apply weighted-sum method after normalizing each objective relative to base-case values

**Metrics:**
- DESS location and capacity per case
- Average primary load share
- Maintenance cost and economic benefit
- Peak-to-valley difference reduction, frequency violation rate, voltage deviation
- Spatial concentration (number of distinct blocks served)

**Expected outcome:** Case 1 will yield scattered nodes with lowest economic benefit; Case 2 will concentrate nodes within few blocks (especially Block 21); Case 3 will distribute nodes across more blocks with highest economic benefit and balanced demand indicator profiles.

**Baselines:** Case 1 and Case 2 serve as baselines for Case 3.

**Dependencies:** C02, C03, G4, E01, E02

---

## E04 — Multi-Dimensional Resilience Evaluation

**Verifies:** C04, C05 — Priority-index-based sequential planning achieves superior node-level, block-level, and grid-level resilience metrics compared to baseline methods.

**Evidence:**
- Figure 16 (comparison of evaluation indicators across cases)
- Formulas (31)–(37) for each indicator
- Quantitative results: O1 +25% (Case 2 vs. Case 1), O2 +102%, L1 +82%, L2 +70%, G1 +25%, G2 +324%

**Run:**
- Input: DESS configurations from Cases 1–3, original network topology and operational data
- Parameters: Evaluation formulas (31)–(37)
- Scale: Node, block, and grid levels

**Setup:**
- Data: Physical distribution network, feeder topology, operational data
- Method: Post-processing evaluation using the proposed indicator formulas

**Procedure:**
1. Compute node-level indicators O1 (node optimization potential), O2 (economic efficiency ratio), O3 (renewable integration improvement) per Equations (31)–(33)
2. Compute block-level indicators L1 (matching rate improvement) and L2 (quality demand improvement) per Equations (34)–(35)
3. Compute grid-level indicators G1 (high-quality demand improvement) and G2 (matching degree discreteness improvement) per Equations (36)–(37)
4. Compare all indicators across Case 1, Case 2, and Case 3

**Metrics:**
- O1: Node optimization potential (target: higher → better source-load balance at nodes)
- O2: Economic efficiency ratio (higher → better cost-benefit, >1 means revenue exceeds cost)
- O3: Renewable integration improvement from baseline (higher → better utilization)
- L1: Block matching improvement (higher → better block-level source-load balance)
- L2: Block quality demand satisfaction improvement (higher → better power quality)
- G1: Grid quality demand improvement (higher → better system-wide quality)
- G2: Grid matching degree uniformity (higher → more equitable distribution across grid)

**Expected outcome:** Case 3 > Case 2 > Case 1 for all seven metrics. The gap will be largest for G2 (grid uniformity) and O2 (economic efficiency), reflecting the key benefit of sequential updating.

**Baselines:** Case 1 (global traversal) and Case 2 (one-shot priority ranking).

**Dependencies:** C04, C05, E03
