# Figure 6: Hourly Forecasted load demand of IEEE RTS

- **Source**: Figure 6, §VI-B (p.181191)
- **Caption**: "Hourly Forecasted load demand of IEEE RTS [9]."
- **Screenshot**: figure6.png (top-left column of the page)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium (peak value stated exactly in text; other points read off the curve)
- **Plot kind**: line
- **Axes**: X = Time (hour), 0–24, linear; Y = Forecasted Load Demand (MW), 1600–2800, linear

The paper states the peak exactly: "The expected highest demand on the next day will be 2670 MW at the
11th hour." The tabulated hourly demand values also appear in Table 9 / Table 10 (D_f^t column) and are
authoritative; this figure visualizes them.

| Hour | Forecasted load (MW) — from Table 9/10 |
|------|-----------------------------------------|
| 1 | 1700 |
| 5 | 1750 |
| 8 | 2430 |
| 11 | 2670 (peak) |
| 15 | 2620 |
| 20 | 2550 |
| 24 | 1840 |

## Trend summary
Demand rises from ~1700 MW in the early hours to a peak of 2670 MW at hour 11, holds a high plateau
(~2500–2650 MW) through the afternoon/evening, then drops sharply to ~1840 MW by hour 24. The peak
(2670 MW) sits just below the 2795 MW dispatchable capacity (10% SR), which is why large-unit outages
create non-zero LOLP (supports C06, C08).
