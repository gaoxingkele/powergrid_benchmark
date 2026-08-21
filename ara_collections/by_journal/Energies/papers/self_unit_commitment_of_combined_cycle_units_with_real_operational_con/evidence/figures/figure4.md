# Figure 4: CCGT power output vs. initial load for Case I

- **Source**: Figure 4, Section 3.1 (Case I), page 12
- **Caption**: "CCGT power output vs. initial load for Case I."
- **Screenshot**: figure4.png
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: high (values from the data table printed beneath the chart); medium on exact hour-index alignment of ramp onset
- **Object location**: Bottom of page 12; a line chart with an embedded data table (rows LOAD, GCCT OPM, HEURISTIC MODEL) over hours 1–24.
- **Plot kind**: line
- **Axes**: X = Hours (1–24, linear), Y = MW (0–900, linear)

Values transcribed from the data table printed under the chart ("-" = no value / offline). Hour alignment of the ramp segments is inferred from the value order and the text ("shutdown ramp in period 5 … offline until period 15 … ramps up in period 19 … maximum from periods 20 to 22").

| Hour | LOAD | GCCT OPM (model) | HEURISTIC MODEL |
|------|------|------------------|-----------------|
| 1 | 210 | 210 | 210 |
| 2 | 210 | 210 | 210 |
| 3 | 210 | 210 | 210 |
| 4 | 210 | 210 | 210 |
| 5 | - | 100 | 50 |
| 6 | - | 50 | - |
| 7–14 | - | - | - |
| 15 | - | 50 | 50 |
| 16 | - | 100 | 204 |
| 17 | - | 150 | 351 |
| 18 | - | 210 | (ramping) |
| 19 | - | 463 | (ramping) |
| 20 | 800 | 800 | 800 |
| 21 | 800 | 800 | 800 |
| 22 | 800 | 800 | 800 |
| 23 | 210 | 463 | 417 |
| 24 | 210 | 399 | 392 |

Full value sequences as printed (for fidelity):
- **GCCT OPM**: 210, 210, 210, 210, 100, 50, …, 50, 100, 150, 210, 463, 800, 800, 800, 463, 399
- **HEURISTIC MODEL**: 210, 210, 210, 210, 50, …, 50, 204, 351, 800, 800, 800, 417, 392
- **LOAD**: 210, 210, 210, 210, …, 800, 800, 800, 210, 210

## Trend summary
The model output (GCCT OPM, red dashed) initially follows the load at 210 MW, then executes a shutdown ramp (100→50→offline) around period 5, stays offline through ~period 15, and executes a graduated hot startup ramp (50→100→150→210→463) reaching maximum capacity (800 MW) for periods 20–22 before ramping down. It cannot instantaneously track the step change in LOAD (from offline to 800 MW) because of the ramp constraints. The heuristic model reaches the 800 MW plateau on a different (steeper) trajectory (…50→204→351→800), diverging from what the plant can physically follow. The initial dispatch (LOAD) is a step profile that neither trajectory can match exactly — the source of the deviation penalty.
