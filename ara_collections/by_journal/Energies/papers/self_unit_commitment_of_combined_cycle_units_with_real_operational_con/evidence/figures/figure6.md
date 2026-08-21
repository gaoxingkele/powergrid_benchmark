# Figure 6: CCGT power output vs. initial load for Case II

- **Source**: Figure 6, Section 3.1/3.2 (introduced page 13, discussed in Case II), page 13
- **Caption**: "CCGT power output vs. initial load for Case II."
- **Screenshot**: figure6.png
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: high (values from embedded data table); medium on exact hour-index alignment
- **Object location**: Lower half of page 13; line chart with embedded data table (rows LOAD, GCCT OPM, HEURISTIC MODEL) over hours 1–24.
- **Plot kind**: line
- **Axes**: X = Hours (1–24, linear), Y = MW (0–900, linear)

Values as printed in the data table beneath the chart ("-" = offline / no value). Text: "a warm startup is needed from periods 14 to 18 … increased ramp in period 19 … maximum capacity from periods 20 to 22."

| Hour | LOAD | GCCT OPM (model) | HEURISTIC MODEL |
|------|------|------------------|-----------------|
| 1–13 | - | - | - |
| 14 | - | 50 | - |
| 15 | - | 100 | - |
| 16 | - | 100 | - |
| 17 | - | 150 | 50 |
| 18 | - | 210 | 204 |
| 19 | - | 463 | 351 |
| 20 | 800 | 800 | 800 |
| 21 | 800 | 800 | 800 |
| 22 | 800 | 800 | 800 |
| 23 | 210 | 463 | 417 |
| 24 | 210 | 349 | 392 |

Full value sequences as printed (for fidelity):
- **GCCT OPM**: …, 50, 100, 100, 150, 210, 463, 800, 800, 800, 463, 349
- **HEURISTIC MODEL**: …, 50, 204, 351, 800, 800, 800, 417, 392
- **LOAD**: …, 800, 800, 800, 210, 210

## Trend summary
With all units initially offline (Table 6), the model performs a warm startup ramp over periods ~14–19 (50→100→100→150→210→463), longer than the heuristic's trajectory, reaching maximum capacity (800 MW) for periods 20–22 then ramping down. The heuristic instead applies a faster (hot-startup-like) ramp starting later (…50→204→351→800), which neglects the units' prior thermal state. Neither trajectory tracks the LOAD step exactly; the model's is the physically-followable one.
