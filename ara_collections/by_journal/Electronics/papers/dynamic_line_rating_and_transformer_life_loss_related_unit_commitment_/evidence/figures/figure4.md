# Figure 4: Comparison of unit output results under the extreme high-temperature typical day scenario

- **Source**: Figure 4 (panels a and b), §5 (Case Study), page 12 (upper half of page)
- **Caption**: "Comparison of unit output results under the extreme high-temperature typical day
  scenario. (a) Output results of conventional unit commitment method; (b) output results of the
  TL-TF method."
- **Screenshot**: figure4.png
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: low
- **Plot kind**: stacked bar (two panels, one per model)
- **Axes**: X = Time (h, 1–24, linear), Y = Power (MW, 0–7000, linear); stacked series = units
  G1–G10 (legend colors)

## Panel structure
- **Panel (a)** conventional UC (static thermal stability, no line-capacity limit, no transformer
  life loss): stacked hourly unit outputs G1–G10 summing to total generation, peaking at ≈6500–7000
  MW near hours 12–14.
- **Panel (b)** TL-TF method (temperature-dependent capacity + transformer life loss): same stacked
  layout; total generation profile is similar in shape but the per-unit composition differs — the
  low-cost hot-region unit (Unit 2 / G2, in Area 3) carries visibly less of the mid-day peak and
  cooler-region/spare units carry more, relative to panel (a).

## Trend summary
Both panels track the load profile of Figure 3 (mid-day peak ≈7000 MW, evening secondary bump). The
qualitative point (stated in §5 text, not readable as exact stack values): under the conventional
model the economically-cheap Units 1 and 2 are dispatched at higher loads; under TL-TF the high
temperature in Area 3 reduces line capacity and prices transformer aging, so Unit 2's output is
suppressed and lower-temperature / spare-capacity units increase output to compensate. Exact
per-unit stack heights are not reliably readable (dense 10-way stack); the composition shift
between (a) and (b) is the robust evidence. Supports C03.
