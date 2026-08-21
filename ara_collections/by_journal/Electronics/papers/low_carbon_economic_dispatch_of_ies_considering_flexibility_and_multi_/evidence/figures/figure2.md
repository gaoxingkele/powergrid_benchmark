# Figure 2: IES structure diagram

- **Source**: Figure 2, Section 3 (page 7). Located at the top of the page.
- **Caption**: "IES structure diagram."
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Energy carriers (color-coded flows)**: Electric energy (green), Thermal energy (red), Cooling energy (blue).
- **Components (sources, left)**: Wind Turbine, Photovoltaic Power, Power Grid.
- **Components (conversion/storage, middle)**: Electric Vehicles, Storage Battery, Gas Turbine, Heat Storage Tank, Electric Boiler, Electric Chiller, Absorption Chiller.
- **Components (loads, right)**: Electric Load, Thermal Load, Cooling Load.
- **Connections**:
  - Electric bus (green) feeds: Electric Load, Electric Vehicles (bidirectional), Storage Battery (bidirectional), Electric Boiler, Electric Chiller; fed by Wind Turbine, Photovoltaic, Power Grid, Gas Turbine.
  - Thermal bus (red): Gas Turbine and Electric Boiler and Heat Storage Tank (bidirectional) feed Thermal Load and the Absorption Chiller.
  - Cooling bus (blue): Absorption Chiller and Electric Chiller feed Cooling Load.
- **Annotations**: Absorption Chiller converts heat → cooling; Electric Chiller converts electricity → cooling; Gas Turbine is a combined heat-and-power (electric + thermal) unit.
- **What it conveys**: The physical topology and multi-energy coupling (electricity/heat/cooling) of the park-level IES that the dispatch model optimizes. Mirrored into logic/solution/architecture.md.
