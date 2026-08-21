# Table 4 - Minimum and maximum voltage of nodes and power loss before and after network reconfiguration (fault in S28)

**Source**: Table 4, Section 5.3.2 (The Fault Occurred in S28), page 21
**Location on page**: bottom of page 21, below Figure 17
**Caption**: "Minimum and maximum voltage of nodes and power loss before and after network reconfiguration when the fault occurred in S28."
**Screenshot**: table4.png
**Extraction type**: raw_table

| Algorithm Category | Active power Loss | Minimum Voltage | Maximum Voltage |
|--------------------|-------------------|-----------------|-----------------|
| Before reconstruction | 22.2987 | 0.9736 | 1.1 |
| After GA reconstruction | 19.2725 | 0.9824 | 1.1 |

Notes: Active Power Loss in kW (paper text: "overall active power loss of the line is
reduced by 3.03 kW"; 22.2987 - 19.2725 = 3.0262 ≈ 3.03 kW). Minimum node voltage increases
by 0.0088 pu (0.9824 - 0.9736). Reduction proportion = 3.0262/22.2987 ≈ 13.6%. Compared to
the S28+DG3 case, integrating (healthy) DG3 significantly reduces losses and raises minimum
voltage.
