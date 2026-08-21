# Technical Concepts

## C01: WGAN-GP (Wasserstein Generative Adversarial Network with Gradient Penalty)
- **Definition**: An improved GAN framework that uses the Wasserstein distance as the optimization objective and incorporates a gradient penalty term to enforce 1-Lipschitz continuity on the discriminator. The gradient penalty term is defined as GP = E[(||∇_x̂ D(x̂)||_2 - 1)^2], where x̂ = εx + (1-ε)G(z) with ε ~ U[0,1].
- **Purpose**: Generates representative wind–solar time-series scenarios that accurately capture uncertainty and correlation of renewable generation, avoiding gradient vanishing and mode collapse problems of traditional GANs.
- **Source**: Section 2, Equations (2)–(4), Figure 1

## C02: E-SOP (Energy Storage-integrated Soft Open Point)
- **Definition**: An integrated flexible interconnection device that incorporates a Battery Energy Storage System (BESS) on the DC side of a Soft Open Point (SOP). The SOP provides controllable bidirectional power flow between feeders for spatial regulation, while the BESS performs temporal energy shifting through charging/discharging.
- **Purpose**: Achieves coordinated spatial power flow regulation and temporal energy balancing within a single device platform, enhancing system spatiotemporal flexibility.
- **Source**: Section 3.3, Figure 2, Equations (12)–(17)

## C03: Source–Network–Storage Coordinated Planning
- **Definition**: A unified expansion planning framework that jointly optimizes the siting and sizing of distributed generation (DG, including wind and PV), E-SOP devices, feeder layout, and substation construction/expansion in ADNs.
- **Purpose**: Overcomes the limitations of traditional separate planning approaches by achieving system-level optimization of generation, network, and storage resources.
- **Source**: Section 3.1, Equation (5), Section 5.3

## C04: SCCR (Successive Convex Cone Relaxation / Successive Contraction of Convex Relaxation)
- **Definition**: An iterative algorithm that solves non-convex ADN planning models by: (1) applying convex relaxation (SOCP) to the non-convex power flow constraints, (2) introducing penalty terms and linear cutting-plane constraints to progressively tighten the feasible region, and (3) iterating until the relaxation gap satisfies the convergence criterion.
- **Purpose**: Provides fast convergence to a high-precision feasible solution, balancing tractability of SOCP with accuracy of the original non-convex model.
- **Source**: Section 4, Equations (28)–(33), Figure 6, Table 3

## C05: Relaxation Gap Metrics
- **Definition**: Quantitative measures of the relaxation error introduced by convexification, defined for branches and SOPs. For branches: g^flow_t = (P_ijt^2 + Q_ijt^2)/(I_ijt^2 × v_it^2) - 1. For SOPs: g^E-SOP_t = (P_AC,ijt^2 + Q_AC,ijt^2)/(A_E-SOP × P_E-SOP_L,ijt) - 1.
- **Purpose**: Quantifies how closely the relaxed solution approximates the original non-convex constraints; the SCCR algorithm drives these gaps toward zero.
- **Source**: Section 4.2, Equations (28)–(29)

## C06: K-medoids Clustering with Silhouette Coefficient
- **Definition**: A clustering algorithm applied to reduce the computational burden of the planning model by extracting representative scenarios from the WGAN-GP-generated wind–solar scenarios. The number of clusters is evaluated using the Silhouette Coefficient (SC) method.
- **Purpose**: Reduces large-scale stochastic scenarios to 4 representative typical scenarios that serve as inputs for the multi-scenario optimization model.
- **Source**: Section 5.2

## C07: Annualized Comprehensive Cost
- **Definition**: The objective function of the planning model, consisting of annualized investment cost and annualized O&M cost. Investment cost includes substations, feeders, DG (wind and PV), BESS, and SOP components, each annualized using a capital recovery factor α = [r(1+r)^T_x] / [(1+r)^T_x - 1]. O&M cost includes equipment maintenance, electricity purchase, and curtailment penalty costs.
- **Purpose**: Provides a life-cycle cost perspective for comparing different planning schemes across multiple scenarios.
- **Source**: Section 3.2, Equations (5)–(11)
