# Figure 10: DG output, load, and network loss in isolated island when photovoltaic power is connected

**Source**: Figure 10, Section 5.2, page 17
**Location on page**: top of page 17 (3-panel: (a) main, (b) local zoom-1, (c) local zoom-2)
**Caption**: "DG output, load, and network loss in isolated island when photovoltaic power is connected."
**Screenshot**: figure10.png
**Figure type**: quantitative_plot
**Extraction method**: exact_from_labels (values from text)
**Reading confidence**: high
**Plot kind**: bar (stacked: photovoltaic + diesel generator; overlaid line = island load; separate panel = network loss)
**Axes**: X = Time (×15 min, periods 1-5), Y = Active Power (MW). Local Zoom-2 Y = network loss (×10^-3 MW)

Values (from text, Section 5.2, Island 2, node 6 = PV):

| Period | Total island load (MW) | PV output (MW) | Diesel output (MW) | Line loss (kW) | PV share |
|--------|------------------------|----------------|--------------------|----------------|---------|
| 1 | 1.58 | 0.12 | 1.4709 | 10.9 | 7.59% |
| 2 | 1.32 | 0.25 | 1.0752 | 5.2 | 18.94% |
| 3 | 1.04 | 0.42 | 0.6226 | 2.6 | 40.38% |
| 4 | 0.96 | 0.02 | 0.9486 | 8.6 | 2.08% |
| 5 | 1.295 | 0.63 | 0.6685 | 3.5 | 48.65% |

## Trend summary
Same island loads as the wind case; PV output is more volatile period-to-period (0.02-0.63 MW), so
diesel swings more (0.62-1.47 MW) to balance. Line losses are larger and more variable than the wind
case (2.6-10.9 kW) because periods with low PV push more power through diesel/lines. Still, load is
fully supplied without voltage-limit violation (see Figure 9).
