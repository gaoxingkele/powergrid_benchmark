# Figure 5: Power output by unit for Case I

- **Source**: Figure 5, Section 3.1 (Case I), page 13
- **Caption**: "Power output by unit for Case I."
- **Screenshot**: figure5.png
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: medium (per-unit values from the embedded data table; hour-column alignment of individual entries is partly inferred)
- **Object location**: Upper half of page 13; a stacked bar chart with an embedded per-unit data table (rows ST2, ST1, GT5, GT4, GT3, GT2, GT1, AUX) over hours 1–24.
- **Plot kind**: bar (stacked, per-unit contribution)
- **Axes**: X = Hours (1–24, linear), Y = MW (−100 to 900, linear; AUX is negative auxiliary consumption)

Per-unit values as printed in the embedded data table ("-" = not dispatched). Late-horizon values (periods ~15–24) are the readable dispatched segments.

| Unit | Early periods (1–6, where online) | Late periods (≈15–24 sequence as printed) |
|------|-----------------------------------|--------------------------------------------|
| ST2 | - | 30.00, 100.0, 155.6, 155.6, 155.6, 90.11, 80.00 |
| ST1 | 82.81, 82.81, 80.91 | 80.00, 155.6, 155.6, 155.6, 90.11, 80.00 |
| GT5 | 67.54, 67.54, 66.00, 50.45, 50.45 | 50.45, 50.45, 61.12, 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT4 | - | 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT3 | - | 50.45, 50.45, 61.12, 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT2 | - | 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT1 | 67.54, 67.54, 67.54, 66.00, 50.45 | 50.45, 61.12, 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| AUX | −7.90, −7.90, −7.90, −2.90, −0.90, −0.45 | −0.45, −0.90, −1.35, −3.35, −10.80, −11.25, −11.25, −11.25, −11.25, −11.25 |

## Trend summary
Early in the horizon only GT1, GT5 and ST1 are online (meeting the 210 MW dispatch), matching the Case I initial conditions (Table 5). After the offline window the model brings units on in sequence to reach maximum capacity: gas turbines GT1–GT5 ramp to their 100 MW maximum and both steam turbines ST1, ST2 reach ~155.6 MW during periods 20–22. Auxiliary consumption (AUX, negative) grows in magnitude as more units come online (from ≈−0.45 MW with one unit to ≈−11.25 MW at full plant), consistent with Eq. (18). The stacked decomposition shows the model resolves individual unit contributions — something the aggregate heuristic cannot.
