# Figure 5: Identified 9 n-1 thermal generator contingencies for IEEE RTS

- **Source**: Figure 5, §VI-B (p.181190)
- **Caption**: "Identified 9 n-1 thermal generator contingencies for IEEE RTS."
- **Screenshot**: figure5.png (bottom-left column of the page)
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: high
- **Plot kind**: bar
- **Axes**: X = Contingency Index (Cy), count 1–9, linear; Y = Capacity of generator Out (MW), linear (tick marks at 0, 20, 76, 100, 155, 197, 250, 300, 350, 400)

Each bar is labeled on the plot with its bus; the bar height is the outaged capacity (corroborated by
Table 2 / Table 5).

| Contingency Index (Cy) | Bus label on bar | Capacity out (MW) |
|------------------------|------------------|-------------------|
| 1 | Bus 1 | 20 |
| 2 | Bus 2 | 76 |
| 3 | Bus 7 | 100 |
| 4 | Bus 13 | 197 |
| 5 | Bus 15 | 12 |
| 6 | Bus 18 | 400 |
| 7 | Bus 21 | 400 |
| 8 | Bus 23 | 155 |
| 9 | Bus 23 | 350 |

## Trend summary
Contingencies are indexed by ascending bus number, not by capacity, so the bar heights are non-monotonic:
tallest bars are Cy6/Cy7 (400 MW, buses 18/21) and Cy9 (350 MW, bus 23); shortest is Cy5 (12 MW, bus 15)
and Cy1 (20 MW, bus 1). This mapping of index→bus→capacity underpins the criticality ranking (C02, C07).
