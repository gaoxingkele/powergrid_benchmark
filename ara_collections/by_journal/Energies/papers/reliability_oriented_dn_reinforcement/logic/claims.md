# Claims

## C01: Integrated Reinforcement-Oriented Reliability Planning Framework
- **Category**: Framework Contribution
- **Claim**: The proposed framework simultaneously optimizes tie line allocation, normally open (NO) switch placement, feeder upgrades, and substation reinforcement while embedding regulatory reliability constraints directly within the investment decision process.
- **Evidence**: Page 3-4, Section 1 (Contributions point 1). The objective function (Equation 7) minimizes total NPV including CENS, CTL, CNOS, and CUPG. Constraints (12)-(13) impose SAIDI and ENS regulatory thresholds. The GA chromosome encoding (Figure 1) represents NO switches, tie line configurations, and infrastructure upgrades in a unified decision vector.
- **Confidence**: High - explicitly stated as contribution and formulized in the mathematical model.

## C02: Hierarchical Contingency Recovery Strategy
- **Category**: Methodological Contribution
- **Claim**: A two-level operational hierarchy performs network reconfiguration for load restoration first, followed by a secondary transition to intentional islanded operation when restoration is infeasible, enhancing load recovery capability while reducing excessive capital investment.
- **Evidence**: Page 3-4, Contributions point 2. Page 11-12, Section 2.2.2 details Success Mode 1 (restoration conditions, Equations 14-18) and Success Mode 2 (islanding requirements, Equation 19). Figure 5 flowcharts the decision process. The reliability indices (Equations 20-33) account for both modes via indicator functions ISR and ISI (Equations 24-26).
- **Confidence**: High - mathematically formulized with explicit success conditions and indicator functions.

## C03: Probabilistic Analytical Reliability Assessment
- **Category**: Methodological Contribution
- **Claim**: An analytical probabilistic reliability model captures load variability, renewable DG intermittency, and component failure uncertainties within a unified optimization framework, avoiding the computational burden of Monte Carlo simulation while maintaining modeling rigor.
- **Evidence**: Page 4-6, Section 2.1. Load modeled with normal distribution (Section 2.1.1). Solar irradiance with beta distribution, wind speed with Weibull distribution (Section 2.1.2). The scenario matrix combines all discretized states (Section 2.1.3). Reliability indices calculated analytically via Equations 20-33 using probability-weighted success conditions.
- **Confidence**: High - detailed probabilistic modeling methodology presented with distribution fitting results.

## C04: Case Study 1 Effectiveness (Dispatchable CDGs Only)
- **Category**: Experimental Result
- **Claim**: For the system with only controllable DGs, 5 tie lines (3, 4, 5, 7, 8) and 4 feeder upgrades are required. The framework achieves ~47% reduction in total ENS across all stages, SAIDI compliance at all buses, and a total NPV of $8,845,220.
- **Evidence**: Page 16-20, Section 3.2.1. Figure 7 shows system after reinforcement. Table 8 lists installed tie lines and upgrades. ENS drops from 92.5 to 48.9 MWh/yr (Stage 1), 103.4 to 54.8 (Stage 2), 106 to 56 (Stage 3) -- Figure 13. Table 9 provides NPV breakdown: CENS=$792,680, CTL=$6,992,000, CNOS=$23,500, CUPG=$1,037,040, Total=$8,845,220. 27 buses (54%) initially violated SAIDI thresholds; all resolved after reinforcement (Figures 9-10).
- **Confidence**: High - specific numbers reported in tables and figures.

## C05: Case Study 2 Effectiveness (CDG + Wind + PV)
- **Category**: Experimental Result
- **Claim**: With renewable DGs included, 4 tie lines (3, 5, 7, 8) and 6 feeder upgrades are required. The framework achieves ~52% reduction in total ENS across all stages, SAIDI compliance at all buses, with a total NPV of $9,140,302. Fewer tie lines are needed due to DG support, but more feeder upgrades increase overall cost.
- **Evidence**: Page 20-24, Section 3.2.2. Figure 16 shows system configuration. Table 10 lists installations. ENS drops from 91.5 to 48.9 MWh/yr (Stage 1), 99.7 to 52.9 (Stage 2), 109.7 to 56 (Stage 3) -- Figure 21. Table 11 provides NPV: CENS=$784,010, CTL=$5,868,000, CNOS=$18,800, CUPG=$2,469,491.9, Total=$9,140,302. Tie line count reduced by one compared to Case 1 (from 5 to 4) due to renewable DG support.
- **Confidence**: High - specific numbers reported in tables and figures.
