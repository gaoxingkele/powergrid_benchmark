# Problem

## Observations

1. **O01**: Traditional transmission and generation expansion planning (TGEP) does not consider battery energy storage systems (ESS) as an alternative to defer transmission line investments [56,57].
2. **O02**: High penetration of variable renewable energy (VRE) introduces significant variability, limited predictability, and near-zero marginal cost, disrupting deterministic generation scheduling [1].
3. **O03**: Environmental constraints restrict deterministic (dispatchable) generation expansion, increasing reliance on stochastic renewable sources.
4. **O04**: TSO-DSO interconnection can provide upward and downward flexibility services through demand response, distributed generation, and aggregated DERs [19-22].
5. **O05**: Existing literature includes only one study considering DDDRO for contingency-constrained generation reserve optimization in transmission expansion planning [10].
6. **O06**: No studies were found that model ESS at transmission level implementing the virtual power line concept with the aim of postponing or avoiding transmission infrastructure investments.
7. **O07**: The Garver 6-node test system consists of 15 right-of-ways, one isolated node, 760 MW total load, 152 MVAr, and 1140 MW total active power generation [72].
8. **O08**: The IEEE RTS-GMLC test system consists of 104 right-of-ways (36 at 138 kV, 68 at 230 kV), 16 power transformers, and three generation dispatch areas [73].
9. **O09**: Historical data from Spain (ENTSO-E, 01/2015 to 12/2023) with 15-minute interval measurements was used for demand and VRE generation [70].
10. **O10**: Clustering with K-means partitioned the sample space into six data bins to represent net demand scenarios.
11. **O11**: Four net demand stages per day were considered with durations: stage 1 (peak, 0.05/1), stages 2-3 (0.2/1 each), stage 4 (low demand, 0.55/1).
12. **O12**: The DDDRO approach uses two norms (L1 and L∞) to construct the confidence uncertainty set based on historical data [68,69].
13. **O13**: Column and constraint generation (CCG) decomposition is used; CCG converges faster than Benders decomposition [66,67].
14. **O14**: For Garver 6-node, candidate ESS devices have max charge/discharge 50 MW, round-trip efficiency 85%, usable capacity 75 MWh.
15. **O15**: For IEEE RTS-GMLC, the model was parameterized for a three-year expansion plan with 4.5% annual linear growth for demand and VRE.
16. **O16**: Processing time for IEEE RTS-GMLC scenarios was approximately 10 minutes average, up to 30 minutes for scenarios with many integer variables.
17. **O17**: In scenario S2.4, 25% of demand has demand response contracts, and upward/downward flexibility contracted is 30%.

## Gaps

1. **G01**: No existing TGEP model simultaneously incorporates VPL (ESS as transmission deferral), VPP, TSO-DSO flexibility (upward/downward), VRE injection, and demand response within a unified optimization framework.
2. **G02**: The impact of local flexibility services from DSOs on transmission expansion investment timing and cost has not been quantified.
3. **G03**: Existing approaches lack a combined use of DDDRO with duality-free decomposition for TGEP problems with VPL and flexibility.

## Key Insight

The paper proposes a unified optimization model that uses battery energy storage as virtual power lines to defer transmission investments, combined with TSO-DSO flexibility contracting and DDDRO for uncertainty handling, achieving cost reduction and improved transmission utilization.

## Assumptions

1. **A01**: Generation and transmission expansion are co-optimized within a single objective (minimize total cost).
2. **A02**: Two types of demand exist: (1) centralized generation expansion demand, and (2) demand served by virtual power plants (VPP) contracted by consumers.
3. **A03**: Net demand = demand minus VRE injection; the load duration curve is discretized into four average net demand stages.
4. **A04**: Flexibility is categorized as upward (decrease demand / increase distributed generation) and downward (increase demand / decrease distributed generation) from the TSO perspective.
5. **A05**: Virtual power lines operate ESSs in coordination with transmission line load profiles, charging during low-demand stages and discharging during high-demand stages.
6. **A06**: VPPs are aggregated groups of DERs (generators, ESSs, demands) located in multiple transmission network nodes.
7. **A07**: Reserve capacity is contracted from VPPs to handle unforeseen fluctuations.
8. **A08**: The DDDRO ambiguity set covers all possible probability realizations within L1 and L∞ norm tolerances determined by historical data.
9. **A09**: Investment projects with different useful lives are compared using the perpetuity financial model extending useful life to infinity.
10. **A10**: The AC power flow model uses a linearized AC-OPF with second-order cone constraint for apparent power.
11. **A11**: Historical data (9 years, 15-minute intervals) adequately represents the true probability distribution when sample size is large.
