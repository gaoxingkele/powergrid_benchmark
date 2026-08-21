# Figure 7: Load balancing using GRU

- **Source**: Figure 7, §4.2(b) (page 16)
- **Caption**: "Load balancing using GRU."
- **Screenshot**: figure7.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line
- **Axes**: X = Time (hours, 02:00 → 02:00 next day, linear), Y = Power (KW, linear, range ~50–120)

| Time | Power (KW), blue load curve |
|------|-----------------------------|
| 02:00 | ≈58 |
| 04:00 | ≈62 |
| 06:00 | ≈90 (peak) |
| 08:00 | ≈88 |
| 10:00 | ≈82 |
| 12:00 | ≈65 |
| 14:00 | ≈62 |
| ~15:00+ | ≈64 |

A horizontal dotted reference line sits at ≈80 KW (the levelling threshold).

## Trend summary
GRU version of the load-balancing curve: rises from ~58 KW off-peak through "Load Balancing" to a "Peak load Shaving" peak (~90 KW around 06:00), then drops below the ~80 KW dotted threshold into a second "Load Balancing" region. Shape mirrors Figure 6 (LSTM) but with a lower/earlier peak as drawn. Values approximate (no data labels). Supports C04.
