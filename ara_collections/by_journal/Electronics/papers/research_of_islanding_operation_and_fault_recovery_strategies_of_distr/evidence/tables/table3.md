# Table 3 - Minimum and maximum voltage of nodes and power loss before and after network reconfiguration (fault in S28 and DG3)

**Source**: Table 3, Section 5.3.1 (The Fault Occurred in S28 and DG3), page 20
**Location on page**: bottom of page 20, below Figure 15
**Caption**: "Minimum and maximum voltage of nodes and power loss before and after network reconfiguration when the fault occurred in S28 and DG3."
**Screenshot**: table3.png
**Extraction type**: raw_table

| Algorithm Category | Active Power Loss | Minimum Voltage | Maximum Voltage |
|--------------------|-------------------|-----------------|-----------------|
| Before reconstruction | 49.3339 | 1.0683 | 1.1 |
| After GA reconstruction | 43.4675 | 1.0729 | 1.1 |

Notes: Active Power Loss is in kW (paper text: "overall active power loss of the line is
reduced by 5.87 kW"; 49.3339 - 43.4675 = 5.8664 ≈ 5.87 kW). Minimum node voltage increases
by 0.0046 pu (1.0729 - 1.0683). Reduction proportion = 5.8664/49.3339 ≈ 11.9% (one of the
three fault cases). "GA" = genetic algorithm (reconstruction search method).
