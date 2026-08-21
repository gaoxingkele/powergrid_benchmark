# Concepts

## Combined-Cycle Gas Turbine (CCGT)
- **Notation**: CCGT
- **Definition**: A power plant in which gas turbines drive generators and their hot exhaust is used to raise steam in Heat Recovery Steam Generators (HRSGs) to drive steam turbines, yielding higher overall thermal efficiency than a simple-cycle gas turbine.
- **Boundary conditions**: The coupling between gas and steam stages is mediated by HRSG thermal dynamics; sustained operation depends on maintaining steam quality.
- **Related concepts**: SEUC, HRSG

## Self-Unit Commitment (SEUC)
- **Notation**: SEUC
- **Definition**: A unit-commitment model operated by the plant itself (not the ISO) that, given an ISO dispatch instruction, produces an hourly commitment and dispatch plan the plant can physically follow, respecting its own operational constraints.
- **Boundary conditions**: Designed for hourly dispatch in the Colombian market; assumes an ISO-provided initial dispatch signal as input.
- **Related concepts**: CCGT, MIP, Unit Commitment

## Component representation
- **Notation**: —
- **Definition**: Modelling approach in which each gas turbine and steam turbine is represented as an individual unit with its own commitment and dispatch variables, as opposed to aggregate/mode representations.
- **Boundary conditions**: Requires solving larger MIP problems due to more binary variables; enables per-unit coupling constraints that aggregate models cannot express.
- **Related concepts**: Mode/configuration representation

## Mode / configuration representation
- **Notation**: —
- **Definition**: Modelling approach that represents a CCGT through a set of discrete operating modes (e.g., "2 × 1" for 2 gas + 1 steam) rather than individual unit variables, losing per-unit granularity.
- **Boundary conditions**: More computationally efficient but cannot enforce per-unit constraints like load distribution or minimum gas-hours gating.
- **Related concepts**: Component representation

## Hot / Warm / Cold startup
- **Notation**: t1, t2, t3
- **Definition**: Classification of a steam turbine's thermal state based on how long it has been offline: hot (t ≤ 16 h), warm (16 < t ≤ 30 h), cold (t > 30 h). Each state has a different startup ramp sequence defined in the Colombian grid code (Table 2).
- **Boundary conditions**: The thermal state windows (t1/t2/t3) are plant-specific parameters; the TEBSA plant uses the Colombian grid code thresholds.
- **Related concepts**: Startup ramp blocks, KGC, KMH

## Minimum gas-turbine operating hours (KGC, KMH)
- **Notation**: KGC (cold start), KMH (hot-start window), KGH (hot start)
- **Definition**: The minimum number of consecutive hours gas turbines must be operating before a steam turbine can be started. KGC = 3 h for the cold-start steam turbine window; KMH governs the hot-start steam turbine window (9 h offline triggers cold start).
- **Boundary conditions**: KGC governs cold startup window; KMH = 6 h defines the lookback window for gas-turbine connection history before a steam turbine can start.
- **Related concepts**: Hot/Warm/Cold startup, MUG

## Minimum number of gas units (MUG)
- **Notation**: MUG
- **Definition**: The minimum number of gas turbines that must be online to support a dispatched steam turbine (MUG = 2 for the TEBSA-like 5 × 2 plant).
- **Boundary conditions**: Plant-specific parameter; a combined-cycle unit cannot be dispatched unless at least MUG gas turbines are online.
- **Related concepts**: CCGT, Steam-gas coupling

## Supplementary firing / supplementary fire
- **Notation**: af, PAF
- **Definition**: Additional fuel burned in the HRSG to raise steam temperature and output independently of the gas-turbine exhaust, bounded by a per-unit supplementary fire capacity (PAF = 15 MW).
- **Boundary conditions**: Steam quality assumed maintained when supplementary firing is used; each gas unit has its own PAF cap.
- **Related concepts**: HRSG, Steam-gas coupling

## Load distribution constraint (DSC)
- **Notation**: DSC, vhdr, δ
- **Definition**: An objective-term penalty on the pairwise output difference between any two gas turbines that are both above their technical minimum, designed to drive even loading and reduce steam-rotor thermal stress.
- **Boundary conditions**: Only activates when both gas turbines exceed their technical minimum (δ = 1); may be overridden by ISO requirements for asymmetric output.
- **Related concepts**: Gas turbine, steam-rotor thermal stress

## Steam waste
- **Notation**: gvsc t
- **Definition**: A modelling mechanism that allows excess steam not used by a steam turbine to be vented (wasted) while still accounting for the gas-turbine heat input that produced it; avoids infeasibility when steam output exceeds turbine capacity.
- **Boundary conditions**: Quantity limited by the maximum capacity of an online steam turbine.
- **Related concepts**: HRSG, Steam-gas coupling

## Steam-to-gas output factor (STF)
- **Notation**: STF
- **Definition**: A constant ratio (STF = 0.613 p.u.) relating the additional steam-turbine output achievable from supplementary firing per unit of supplementary fuel; assumed constant.
- **Boundary conditions**: Variable ratios left to future work; assumed constant for model simplification.
- **Related concepts**: Supplementary firing, steam-gas coupling

## Colombian deviation penalty rule
- **Notation**: 5% rule
- **Definition**: Market rule [25] that penalises deviations exceeding 5% between scheduled and actual generation; the paper uses this to quantify the cost of omitted constraints (USD 60,957 / USD 66,093 daily).
- **Boundary conditions**: Only deviations exceeding the 5% band are penalized; penalty rate = PCC (120 USD/MWh).
- **Related concepts**: Deviation penalty, SEUC
