# Concepts

## 1. Grid-Based Distribution Network
A networked layout of smart grid forming autonomous unit groups through topology reconfiguration, enabling hierarchical utilization and dynamic allocation of regional energy. Each grid group has relatively independent operational characteristics but interconnected influences requiring collaborative optimization.

## 2. Three-Dimensional Objective System
The paper constructs three primary objectives:
- **Investment Cost (Fm)**: Includes capital costs of DG (wind, PV), energy storage, and distribution network construction, plus operation and maintenance costs
- **Expected Grid Energy Shortage (Em)**: Quantifies power supply reliability based on failure probabilities of lines, storage devices, and islanding/system states
- **Network Loss (Floss)**: Active power losses calculated from branch admittance, node voltages, and phase angles

## 3. Improved NSGA-II Algorithm
The standard NSGA-II enhanced with:
- **Hybrid-integer encoding**: Mixed discrete (siting) and continuous (sizing) variable representation
- **Feasibility-priority constraint handling**: Binary feasibility indicator (delta_feas) for DER deployment eligibility
- **Fuzzy membership decision-making**: Compromise solution selection via weighted membership aggregation
- **Adaptive crossover and mutation rates**: Dynamic parameter adjustment

## 4. Dispatchable vs. Non-Dispatchable EVs
- **Non-dispatchable EVs**: Operate solely as charging loads; daily energy demand follows normal distribution based on driving distance
- **Dispatchable EVs**: Can both charge and discharge, functioning like energy storage devices with SOC limits, power limits, and availability windows

## 5. Energy Storage Model
Mathematical model for ES and dispatchable EVs using energy balance equations with charge/discharge loss coefficient (eta), SOC constraints (SOCmin to SOCmax), and charging/discharging power limits.

## 6. Distributed Generation Models
- **Wind turbine (WT)**: Piecewise output function of wind speed with cut-in, cut-out, and rated speeds
- **Photovoltaic (PV)**: Output proportional to irradiance with temperature correction via power temperature coefficient

## 7. Power-Supply Schemes
Four comparative schemes:
- **Scheme 1**: DG connected directly to grid (no ES)
- **Scheme 2**: Power solely from ES and dispatchable EVs
- **Scheme 3**: Em prioritized (weight vector [0.3, 0.4, 0.3])
- **Scheme 4**: Multi-objective coordinated optimization via Pareto-front analysis

## 8. Feasibility Constraint in DER Siting
Practical constraints for DER deployment: spatial availability, short-circuit capacity limits of switchgear, and grid connection feasibility. Formalized via binary indicator delta_feas_i for each candidate node.

## 9. Sensitivity Analysis
Two types:
- **Post-evaluation sensitivity**: Fixed optimal configuration, varying operating points (irradiance, wind speed, ES strategy)
- **Re-optimization sensitivity**: Changing ES access location (trunk/end/mid) and re-optimizing planning variables

## 10. Fuzzy Membership Function
Method for selecting the optimal compromise solution from the Pareto set by calculating membership values (u^k_i) for each solution across all objectives, then aggregating with equal weights.
