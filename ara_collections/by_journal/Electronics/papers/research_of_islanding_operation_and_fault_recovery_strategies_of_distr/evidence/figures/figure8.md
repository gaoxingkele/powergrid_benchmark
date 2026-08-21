# Figure 8: DG output, load, and network loss in isolated island when wind power is connected

**Source**: Figure 8, Section 5.2, page 16
**Location on page**: top-middle of page 16 (3-panel: (a) main, (b) local zoom-1, (c) local zoom-2)
**Caption**: "DG output, load, and network loss in isolated island when wind power is connected."
**Screenshot**: figure8.png
**Figure type**: quantitative_plot
**Extraction method**: exact_from_labels (values from text)
**Reading confidence**: high
**Plot kind**: bar (stacked: wind power + diesel generator; overlaid line = island load; separate panel = network loss)
**Axes**: X = Time (×15 min, periods 1-5), Y = Active Power (MW). Local Zoom-2 Y = network loss (×10^-3 MW)

Values (from text, Section 5.2, Island 2, node 6 = wind):

| Period | Total island load (MW) | Wind output (MW) | Diesel output (MW) | Line loss (kW) | Wind share |
|--------|------------------------|------------------|--------------------|----------------|-----------|
| 1 | 1.58 | 0.5 | 1.0849 | 4.9 | 31.65% |
| 2 | 1.32 | 0.45 | 0.873 | 3 | 34.09% |
| 3 | 1.04 | 0.3 | 0.7434 | 3.4 | 28.85% |
| 4 | 0.96 | 0.25 | 0.7144 | 4.4 | 26.04% |
| 5 | 1.295 | 0.43 | 0.8693 | 4.3 | 33.21% |

## Trend summary
Wind + diesel stack sums to island load + losses each period. Diesel fills the deficit as wind output
falls, so total generation tracks the descending-then-rising load (1.58->0.96->1.295 MW). Network loss
is tiny (3-4.9 kW, panel c, order 10^-3 MW). Demonstrates the island balances important-load supply
across periods using dispatchable diesel to absorb wind variability.
