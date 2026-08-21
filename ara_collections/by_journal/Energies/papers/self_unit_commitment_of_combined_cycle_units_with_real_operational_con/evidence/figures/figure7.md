# Figure 7: Power output by unit for Case II

- **Source**: Figure 7, Section 3.2 (Case II), page 14
- **Caption**: "Power output by unit for Case II."
- **Screenshot**: figure7.png
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: medium (per-unit values from the embedded data table; hour-column alignment partly inferred)
- **Object location**: Lower half of page 14; stacked bar chart with embedded per-unit data table (rows ST2, ST1, GT5, GT4, GT3, GT2, GT1, AUX) over hours 1–24.
- **Plot kind**: bar (stacked, per-unit contribution)
- **Axes**: X = Hours (1–24, linear), Y = MW (−100 to 900, linear; AUX negative)

Per-unit values as printed in the embedded data table for the dispatched periods (≈14–24; earlier periods all "-" since all units start offline).

| Unit | Late periods (≈18–24 sequence as printed) |
|------|--------------------------------------------|
| ST2 | 30.00, 150.08, 155.63, 155.63, 155.63, 90.11, 80.00 |
| ST1 | 30.00, 155.63, 155.63, 155.63, 90.11, 80.00 |
| GT5 | 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT4 | 50.45, 50.45, 50.45, 75.45, 61.12, 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT3 | 61.12, 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT2 | 100.0, 100.0, 100.0, 58.80, 50.00 |
| GT1 | 50.45, 50.45, 75.45, 61.12, 73.43, 100.0, 100.0, 100.0, 58.80, 50.00 |
| AUX | −0.45, −0.90, −0.90, −3.35, −10.80, −11.25, −11.25, −11.25, −11.25, −10.80 |

## Trend summary
Starting from all-offline, the model activates gas turbines GT1–GT5 progressively during the warm startup (periods ~14–19: GT2, GT3, GT4 lead the startup ramp per the text), then brings ST1 and ST2 online, with ST2 starting in cold mode at period 18. All units reach full output (gas turbines at 100 MW, steam turbines at ~155.6 MW) for periods 20–22. To hit maximum capacity, one supplementary fire is used, contributing an additional 4.75 MW to steam output. Auxiliary consumption (AUX, negative) scales with the number of online units, reaching ≈−11.25 MW at full plant.
