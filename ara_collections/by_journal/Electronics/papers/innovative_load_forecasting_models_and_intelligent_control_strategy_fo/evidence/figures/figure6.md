# Figure 6: Load balancing using LSTM

- **Source**: Figure 6, §4.1(b) (page 14, bottom)
- **Caption**: "Load balancing using LSTM."
- **Screenshot**: figure6.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: line
- **Axes**: X = Time (hours, 02:00 → 02:00 next day, linear), Y = Power (KW, linear, range ~50–120)

| Time | Power (KW), red load curve |
|------|----------------------------|
| 02:00 | ≈58 |
| 04:00 | ≈62 |
| 06:00 | ≈75 |
| 08:00 | ≈103 (peak) |
| 10:00 | ≈90 |
| 12:00 | ≈80 |
| 14:00 | ≈70 |
| ~15:00+ | ≈55 |

A horizontal dotted reference line sits at ≈80 KW (the levelling threshold).

## Trend summary
Single load curve rising from an off-peak trough (~58 KW at 02:00) through a morning "Load Balancing" region to a "Peak load Shaving" peak (~103 KW around 08:00), then declining back through a second "Load Balancing" region below the ~80 KW dotted threshold. The annotations ("Load Balancing", "Peak load Shaving") mark where the control keeps the curve near the threshold. Exact values approximate (no data labels). Supports C04 (peak shaving / load levelling under LSTM forecasts).
