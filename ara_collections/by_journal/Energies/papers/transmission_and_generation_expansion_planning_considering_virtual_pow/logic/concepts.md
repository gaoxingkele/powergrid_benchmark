# Concepts

## C01: Virtual Power Line (VPL)
A concept where battery energy storage systems deployed at transmission network nodes operate in coordination with the load profile of transmission lines to defer or avoid investments in new physical transmission lines. ESSs charge during low-demand stages and discharge during high-demand stages, implementing peak shaving behavior.

## C02: Virtual Power Plant (VPP)
Aggregated groups of distributed energy resources (DERs), represented as generators, ESSs, and demands, located in multiple transmission network nodes. Each has a variable power output divided in stages. VPPs provide aggregated energy and power capacity to transmission nodes and reserve capacity for system reliability.

## C03: Upward Flexibility
From the TSO perspective, the ability of DSOs and VPPs to decrease their electricity demand or increase the injection of distributed generation when there is a shortage of electricity supply in the transmission network.

## C04: Downward Flexibility
From the TSO perspective, the ability of DSOs and VPPs to increase their electricity demand or decrease injection of distributed generation when there is an excess of electricity supply in the transmission network.

## C05: Net Demand
Demand for electricity minus the contribution from VRE injection. Used as the basis for the load duration curve and demand stage modeling.

## C06: Load Duration Curve / Net Demand Stages
The relationship between cumulative load (net demand) and the percentage of time for which that load occurs. Discretized into four average net demand levels (S1, S2, S3, S4), each with associated duration and depth (p.u. relative to average).

## C07: Data-Driven Distributionally Robust Optimization (DDDRO)
An optimization approach that uses historical data to construct an ambiguity set of probability distributions, then optimizes for the worst-case distribution within that set. Uses two norms (L1 and L∞) to bound the confidence uncertainty set.

## C08: Column and Constraint Generation (CCG)
A decomposition method for solving two-stage robust optimization problems. Iteratively adds columns (recourse variables) and constraints. Proven to converge faster than Benders decomposition for certain problem classes [66,67].

## C09: Duality-Free Decomposition
A method to transform bi-level (max-min) problems into independent subproblems without computing dual information [60,61]. Exploits the disjoint feasible regions between uncertainty variables and operational variables.

## C10: Ambiguity Set
The set of all possible probability distributions considered in DDDRO. Constructed using L1 and L∞ norm tolerances (δ1, δ∞) based on historical data confidence levels (α1, α2). The set shrinks as more historical data becomes available.

## C11: Locational Marginal Price (LMP)
Nodal pricing method used to allocate transmission costs among users. Represents the marginal cost of supplying the next increment of load at a specific bus, reflecting generation marginal cost and congestion.

## C12: TSO-DSO Interface
The interconnection point between transmission system operator (TSO) and distribution system operator (DSO) networks, through which flexibility services (upward/downward), demand response, and DER injection can be coordinated.

## C13: Demand Response Flexibility Band
The fraction of demand response contracted capacity that can be activated. Modeled as `dBand_RSP` parameter limiting `dP_FxU_RSP` and `dP_FxD_RSP` decision variables.

## C14: Perpetuity Financial Model
Procedure used to make investment projects with different useful lives comparable. Extends useful life to infinity and determines the present value of the infinite series of installments at a defined discount rate [59].
