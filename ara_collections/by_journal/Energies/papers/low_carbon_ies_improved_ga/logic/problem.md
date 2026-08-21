# Problem Specification

## Observations

### O1: Growing urgency of low-carbon integrated energy systems
- **Statement**: Global climate change and energy security challenges have made the pursuit of low-carbon integrated energy systems (IESs) increasingly important. China has proposed the "dual-carbon" goal: peak carbon emissions by 2030 and achieve carbon neutrality by 2060.
- **Evidence**: Section 1 (Introduction), first paragraph
- **Implication**: Effective optimization methods for low-carbon IES operation are needed to meet these policy targets.

### O2: IES optimization is a complex multi-objective problem
- **Statement**: IES scheduling typically involves multiple objective functions (operating cost, carbon emissions), multiple decision variables (power generation, gas consumption, storage operation), and multiple constraints (power balance, heat balance, equipment limits). Tiered pricing mechanisms for electricity, natural gas, and carbon emissions make the optimization even more complex.
- **Evidence**: Sections 1, 2.2.1-2.2.3
- **Implication**: Traditional single-objective optimization methods cannot adequately handle the competing objectives and complex constraints.

### O3: Heuristic algorithms for IES optimization face constraint-handling challenges
- **Statement**: Most heuristic algorithms handle equality constraints (power and heat balance) using penalty functions, treating them as soft constraints. This may lead to solutions that violate equality constraints, causing imbalances between supply and demand of electrical and thermal energy.
- **Evidence**: Section 1, last paragraph before Section 2; Section 4.5 discusses the penalty function approach used by MPSO and MABC
- **Implication**: A constraint-handling approach that strictly enforces equality constraints is needed for practical IES operation.

### O4: Existing studies do not fully account for tiered pricing structures
- **Statement**: Most current studies do not account for the tiered structures of energy prices and carbon emission prices found in real-world applications.
- **Evidence**: Section 1, final paragraph
- **Implication**: IES optimization models must incorporate tiered electricity, natural gas, and carbon emission pricing mechanisms to reflect real-world operational conditions.

## Gaps

### G1: Standard GA mutation and crossover methods lack sufficient exploration capability
- **Statement**: Traditional GA crossover (e.g., single-point, uniform) and mutation (e.g., uniform random) operations often lead to premature convergence or loss of superior genetic material, limiting their effectiveness for multi-objective IES optimization.
- **Caused by**: O2, O3
- **Existing attempts**: NSGA-II with dynamic crowding distance (Ref. [12]) and other MOEA approaches; standard penalty function methods (Ref. [16])
- **Why they fail**: Standard crossover does not preserve parental genetic structure; uniform mutation can be either too aggressive or too conservative; penalty functions treat constraints as soft objectives rather than hard requirements.

### G2: Trade-off between economic and environmental objectives is not systematically optimized
- **Statement**: IES operation requires balancing operating costs and carbon emissions, but existing approaches often either treat carbon costs as part of operating costs (single-objective) or fail to maintain solution diversity across the Pareto front.
- **Caused by**: O2, O3
- **Existing attempts**: Ref. [10] considered energy efficiency and total cost; Ref. [12] used NSGA-II for rural IESs
- **Why they fail**: These approaches do not simultaneously address constraint handling, genetic diversity preservation, and Pareto front diversity maintenance.

## Key Insight
- **Insight**: By combining cyclic crossover (which preserves parental genetic structure while avoiding duplicate gene combinations) with polynomial mutation (which provides adaptive mutation amplitude based on fitness), and embedding a constraint-prioritizing selection mechanism within the NSGA-II fast non-dominated sorting framework, the IGA can simultaneously achieve low constraint violations, explore the Pareto front effectively, and produce superior trade-off solutions between cost and emissions.
- **Derived from**: O3, G1, G2
- **Enables**: A day-ahead scheduling optimization method that produces feasible (constraint-satisfying) solutions with verified performance across multiple IES operational scenarios.

## Assumptions
- A1: Tiered pricing structures (electricity, natural gas, carbon emissions) follow a 120% surcharge for consumption above threshold, and three-tier carbon pricing, as specified.
- A2: Renewable generation (PV, wind) output is known/predictable for day-ahead scheduling.
- A3: Electricity, heat, and gas loads are known for the scheduling horizon.
- A4: The CHP unit operates with fixed efficiency ηCHP = 0.9 and the WHU with ηWHU = 0.6.
- A5: The ESS initial and final state of charge are both 50% (SOCBE_1 = SOCBE_24 = 50%).
- A6: Operating cost and carbon emission minimization are equally weighted (w1 = w2 = 1) in the final Pareto solution selection.
