# Figure 3: The 5 × 2 CCGT scheme

- **Source**: Figure 3, Section 3 (Results and Discussion), page 11
- **Caption**: "The 5 × 2 CCGT scheme."
- **Screenshot**: figure3.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high
- **Object location**: Bottom of page 11, plant schematic.

## Visual description
- **Components**: Five gas turbines (GT1–GT5), each with its own generator (G) and its own Heat Recovery Steam Generator (HRSG 1–HRSG 5); two steam turbines (ST1, ST2), each with a generator (G). Represents the TEBSA plant configuration (5 gas turbines, 2 steam turbines).
- **Connections / data flow**: Each GT feeds its HRSG (exhaust heat); the five HRSGs feed a common steam collector/header (red piping) that supplies the two steam turbines ST1 and ST2. Control valves (triangular symbols) sit between the collector and each steam turbine.
- **Annotations**: The shared collector is what couples all gas turbines' steam to both steam turbines — the structural reason uneven gas-turbine loading produces uneven steam thermal characteristics at the steam-turbine rotors.
- **What it conveys**: The plant is modelled as individual gas and steam turbine units (not one aggregate CCGT), with steam coupling through a common HRSG collector. Mirrored into `logic/solution/method.md` (plant topology) and motivates the load-distribution constraint (C05).
