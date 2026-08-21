# Figure 2: Diagram of flexible DC distribution system in a B data center

- **Source**: Figure 2, Section 2.2 (page 6)
- **Caption**: "Diagram of flexible DC distribution system in a B data center."
- **Screenshot**: figure2.png
- **Location on page**: Upper half of page 6.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: "10KV DC mains supply" → DC/DC → red 750V DC busbar (left); a green 750V DC busbar (right) with no independent second mains source. Four load converters in the middle: DC/AC, DC/AC → "380/220V AC equipment"; DC/DC, DC/DC → "336/240V DC equipment".
- **Connections**: Single supply path from the left mains; both red and green bus segments feed the middle load buses. No diesel generator branch shown in this variant.
- **Annotations**: Red vs green busbars.
- **What it conveys**: Tier B / Tier II style single-supply-path architecture with N+1 redundancy in UPS/generator equipment (redundancy without full fault tolerance). Multiple single points of failure remain, but UPS failure/maintenance causes essentially no interruption.
