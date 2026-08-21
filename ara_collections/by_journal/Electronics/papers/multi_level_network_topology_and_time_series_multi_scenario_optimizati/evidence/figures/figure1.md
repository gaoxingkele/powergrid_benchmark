# Figure 1: Diagram of flexible DC distribution system in an A or Tier IV/III data center

- **Source**: Figure 1, Section 2.2 (page 5)
- **Caption**: "Diagram of flexible DC distribution system in an A or Tier IV/III data center."
- **Screenshot**: figure1.png
- **Location on page**: Lower half of page 5.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Two symmetric supply sides. Left side: "10KV DC mains supply" → DC/DC converter → red 750V DC busbar; "10KV diesel generator" → AC/DC converter → same red busbar. Right side: "10KV DC mains supply" → DC/DC converter → green 750V DC busbar. Between the two busbars sit four load converters feeding equipment: DC/AC and DC/AC → "380/220V AC equipment"; DC/DC and DC/DC → "336/240V DC equipment".
- **Connections**: Red-bus lines and green-bus lines both reach the middle load buses (two mutually hot-standby paths). Colors red and green denote the two independent power-supply buses/lines.
- **Annotations**: Red vs green = the two supply buses; 750V DC busbar labels on each side.
- **What it conveys**: Tier IV/A (fault-tolerant) architecture — dual 750V DC buses, each path normally carrying 50% of the load, either able to carry 100% on failure/maintenance.
