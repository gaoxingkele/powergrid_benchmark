# Concepts

## Classification-based Global Optimization (CGO)
- **Notation**: CGO
- **Definition**: A deterministic optimization methodology that pre-classifies network buses by voltage sensitivity, active power demand, and reactive power demand before performing a global search for optimal DG, CB, and EVCS placement and sizing. The classification restricts the search space to high-load branches, eliminating the randomness and parameter sensitivity of stochastic metaheuristics.
- **Boundary conditions**: Applicable to radial distribution networks with known topological data and load profiles. Not applicable when load data are unavailable or network topology is unknown. The deterministic nature requires fixed, known inputs; uncertainty in load or generation is not inherently handled.
- **Related concepts**: Hosting Factor, Classification-Based Bus Selection, Global Multi-Objective Function

## Hosting Factor (HF)
- **Notation**: HF or EV_HF
- **Definition**: The ratio of EV charging load to total system load, expressed as a percentage. In this study, EV_HF values of 30%, 40%, and 50% are investigated, representing the share of total network load attributed to EV charging stations. The total EVCS load is split between two candidate stations.
- **Boundary conditions**: Applies to distribution network planning scenarios. Values of 30-50% represent high EV penetration scenarios. The hosting factor determines the total EVCS capacity to be allocated: at HF = 30%, total EVCS load = 0.3 x total system load.
- **Related concepts**: Electric Vehicle Charging Station (EVCS), Total Load Demand

## Voltage Deviation Index (VDI)
- **Notation**: VDI
- **Definition**: A scalar index quantifying the total voltage deviation across all N network buses from the nominal value, calculated as VDI = sum from i=1 to N of (1 - Vi)^2, where Vi is the voltage at bus i in p.u. Constraint: 0.95 <= Vi <= 1.05 for all buses.
- **Boundary conditions**: Lower VDI indicates a flatter voltage profile closer to nominal. Used as an optimization objective (minimized via weight W2 in the global function).
- **Related concepts**: Voltage Profile, Global Multi-Objective Function

## Classification-Based Bus Selection
- **Notation**: —
- **Definition**: A pre-optimization screening process that ranks distribution branches according to active power demand (for DG and EVCS placement) and reactive power demand (for CB placement), then restricts the optimization search to only the highest-demand branches rather than the full set of network buses.
- **Boundary conditions**: Requires known load values at each bus. Assumes that heavily loaded branches are the most beneficial locations for resource placement. Risk of misclassification is considered negligible when load data are known.
- **Related concepts**: CGO, Branch Ranking, Active Power Demand, Reactive Power Demand

## Thermal Capacity Limit
- **Notation**: Sij,max
- **Definition**: The maximum apparent power that can flow through a distribution branch connecting buses i and j without exceeding its thermal rating. Constraint: |Sij| <= Sij,max for all branches, where Sij = Vi x Iij*.
- **Boundary conditions**: Enforced as an operational constraint in the optimization. Varies per branch based on conductor type and installation conditions. The proposed CGO verifies that all optimized solutions satisfy this constraint.
- **Related concepts**: Power Flow, Branch Loading, Line Current

## Global Multi-Objective Function
- **Notation**: Ft
- **Definition**: The weighted composite objective function minimized by the CGO framework. Ft = min[W1(PLoss + QLoss) + W2 x VDI - W3 x CSaved Energy Loss + W4 x (1/delta QCO2)]. Weights: W1 = 0.4, W2 = 0.25, W3 = 0.1, W4 = 0.25, selected via sensitivity analysis to balance losses, voltage, economics, and emissions.
- **Boundary conditions**: Weight values were tuned for the specific networks under study. Different network characteristics or priorities may require re-tuning. The function assumes equal or comparable importance of the four objective components.
- **Related concepts**: VDI, PLoss, QLoss, CSaved Energy Loss, delta QCO2

## Payback Period
- **Notation**: Payback
- **Definition**: The time (in years) required for the annual cost savings from reduced energy losses to recover the total capital investment in DGs and CBs. Computed as Payback = (CDG + CCB) / CSaved Energy Loss, where CDG sums DG capital costs and CCB sums CB capital costs.
- **Boundary conditions**: Operating and maintenance costs are not included. Time-of-use electricity pricing effects are not considered. Only the peak-load-based annual energy loss saving is used for the denominator.
- **Related concepts**: CSaved Energy Loss, CDG, CCB

## CO2 Emission Reduction Factor
- **Notation**: fCO2
- **Definition**: The mass of CO2 emissions avoided per unit of electrical energy not supplied from the substation (kg CO2/kWh). The study reports typical values: Coal = 0.95, Oil = 0.75, Natural Gas = 0.45, Grid average = 0.5-0.9 kg CO2/kWh. The annual emission reduction is delta QCO2 = fCO2 x delta Eslack.
- **Boundary conditions**: The emission factor depends on the energy mix of the specific grid. The study uses a grid-average value. The calculation assumes that reduced substation energy directly maps to reduced generation-side emissions.
- **Related concepts**: delta QCO2, delta Eslack, Global Multi-Objective Function
