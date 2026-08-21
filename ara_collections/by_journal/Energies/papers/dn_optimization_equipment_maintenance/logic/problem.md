# Problem Statement

## Observations

**O1: High renewable penetration causes flexibility deficits in distribution networks.**
Traditional distribution networks face challenges such as low flexibility, poor response speed, and operational inefficiency with increasing renewable energy integration [Source: Abstract, Page 1]. The distribution network is most impacted due to its proximity to distributed generation sources such as rooftop PV and local wind farms [Source: Page 1, Introduction].

**O2: Existing flexibility metrics are often static.**
Existing flexibility metrics fail to capture system-wide spatial and temporal constraints [Source: Page 2, line 29]. Flexibility has emerged as a key metric in modern power system design and operation, but current approaches do not adequately account for dynamic conditions.

**O3: Dispatch decisions and network structure are treated independently in existing methods.**
Robust optimization methods typically treat dispatch decisions independently of network structure, limiting their ability to address topological constraints and flexibility allocation simultaneously [Source: Page 2, line 30].

**O4: Equipment maintenance is rarely co-optimized with operational dispatch.**
Existing two-layer optimization studies rarely address coordination with equipment maintenance or dynamic reconfigurability [Source: Page 2, line 30]. This paper claims to contribute to predictive maintenance by identifying optimal switching strategies and branch stress levels [Source: Abstract, Page 1].

**O5: Three schemes show different performance trade-offs.**
Scheme 1 (no flexibility/no interconnection) has the lowest direct operation cost but highest comprehensive cost due to flexibility deficits. Scheme 2 (flexibility without interconnection) reduces flexibility losses but cannot fully leverage cross-grid resources. Scheme 3 (both flexibility and interconnection) achieves the best overall performance [Source: Pages 9-12, Tables 1-2].

**O6: The DRO model outperforms deterministic, stochastic, and robust approaches.**
Under 500 Monte Carlo scenarios, the proposed DRO model achieves the lowest average cost and maximum cost. The deterministic model has the highest costs due to inability to account for uncertainty. The stochastic model lacks robustness in extreme scenarios. The traditional robust model is overly conservative [Source: Pages 13-14, Figures 7-8].

## Gaps

**G1: Lack of unified framework integrating reconfiguration, flexibility, robust dispatch, and maintenance.**
Existing approaches address these aspects separately. No prior work combines network reconfiguration, flexibility assessment, robust scheduling, and equipment maintainability in a single unified framework [Source: Page 2, line 34].

**G2: No branch-level flexibility adequacy metric for guiding reconfiguration.**
Existing flexibility metrics are system-level and static. The paper introduces FBF (Branch Flexibility Adequacy) as a branch-level metric, but its generalizability to other network topologies is unvalidated [Source: Pages 3-4, Equations (1)-(2)].

**G3: Computational scalability for ultra-large systems is unproven.**
The hybrid ACO-FHO-DE metaheuristic may encounter scalability challenges when applied to ultra-large distribution systems or real-time operation scenarios [Source: Page 16, Section 5, Limitations].

## Key Insight

Coordinating grid reconfiguration (topology decisions) with distributionally robust dispatch (operational decisions) through a two-layer feedback loop, quantified by a branch-level flexibility adequacy index, enables simultaneous improvement of economic efficiency, system flexibility, and equipment sustainability. The key mechanism is that topology flexibility and operational dispatch are mutually reinforcing: better topology improves dispatch feasibility, and dispatch feedback identifies topology bottlenecks.

## Assumptions

A1. Historical or forecasted renewable and load profiles are available with sufficient accuracy [Source: Page 15, Section 4].
A2. Grid topology and equipment constraints are known and controllable [Source: Page 15, Section 4].
A3. Centralized coordination and controllability of distributed resources (flexible loads, storage, distributed generation) is achievable [Source: Page 15, Section 4].
A4. Sufficient computational resources exist to solve the dispatch problem offline or in near real-time [Source: Page 15, Section 4].
A5. The Disflow power flow model with convex relaxation (big-M method) provides sufficient accuracy for distribution network analysis [Source: Pages 3-4, Equations (3)-(6)].
A6. Renewable generation uncertainty can be adequately characterized by historical data-based scenario generation and clustering [Source: Page 5, Section 2.2].
