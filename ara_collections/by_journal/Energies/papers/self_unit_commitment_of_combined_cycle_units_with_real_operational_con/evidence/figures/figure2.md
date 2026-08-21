# Figure 2: Cold and hot steam turbine startup and shutdown condition

- **Source**: Figure 2, Section 2.6 (Steam Turbine Startup), page 9
- **Caption**: "Cold and hot steam turbine startup and shutdown condition." (adopted from ref. [13])
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high
- **Object location**: Lower half of page 9, a state-transition diagram.

## Visual description
- **Components**: Four state boxes — "Off", "Cold startup", "Warm startup", "On".
- **Connections / transitions**:
  - Off → Cold startup, labelled "Downtime > KGC" (a long downtime forces a cold startup).
  - Off → Warm startup, labelled "Downtime < KGH" (a shorter downtime allows a warm/hot startup).
  - Cold startup → On, and Warm startup → On, labelled "Minimum uptime after startup".
  - On → Off, labelled "Minimum downtime after shutdown".
- **Annotations**: Thresholds KGC and KGH gate which startup type (cold vs warm/hot) is entered based on how long the unit has been offline (downtime).
- **What it conveys**: The steam turbine's startup type is determined by its thermal state, which is set by accumulated downtime relative to thresholds KGC/KGH; this state machine is the structural basis of the startup constraints Eqs. (32)–(40). Mirrored into `logic/solution/method.md` (steam-turbine startup logic).
