# Figure 8: Impact of control strategy

- **Source**: Figure 8, §4.3 (page 16, bottom)
- **Caption**: "Impact of control strategy."
- **Screenshot**: figure8.png
- **Figure type**: quantitative_plot (mixed — two side-by-side panels)
- **Extraction method**: digitized_estimate (with exact anchor values from §4.3 text)
- **Reading confidence**: medium
- **Plot kind**: line (two panels, each with markers)

### Panel A — Peak Load Reduction
- **Axes**: X = Time (Months, ~1–12, linear), Y = Load (MW, linear, ~95–165)
- **Series**: "Before Control Strategy" (blue), "After Control Strategy" (orange)

| Time (Months) | Before (MW) | After (MW) |
|---------------|-------------|------------|
| 2 | ≈100 | ≈95 |
| 4 | ≈112 | ≈105 |
| 6 | ≈130 | ≈112 |
| 8 | ≈135 | ≈120 |
| 10 | ≈150 | ≈128 |
| 12 | ≈160 | ≈140 |

### Panel B — Grid Stability Improvement (Voltage Fluctuation)
- **Axes**: X = Time (Months, ~1–12, linear), Y = Voltage Fluctuation (%, linear, ~3–7.5)
- **Series**: "Before Control Strategy" (blue), "After Control Strategy" (orange)

| Time (Months) | Before (%) | After (%) |
|---------------|-----------|-----------|
| 2 | ≈4 | ≈3 |
| 4 | ≈5 | ≈3.8 |
| 6 | ≈6 | ≈4 |
| 8 | ≈6 | ≈4.3 |
| 10 | ≈7 | ≈4.8 |
| 12 | ≈7.5 | ≈5 |

## Verbatim source text (§4.3, page 16)
- "the strategy achieving an average reduction of 10% across various time periods"
- "in the month of July, the peak load decreased from 160 MW to 140 MW after applying the control strategy"
- "Before the implementation of the control strategy, voltage fluctuations ranged from 4% to 7.5%. After the strategy was applied, fluctuations were reduced to a range of 3% to 5%"
- Conclusions (page 19): "resulting in a reduction of up to 15% in operational costs and an enhancement of approximately 20% in grid stability by mitigating voltage fluctuations"

## Trend summary
Both panels: the "After Control Strategy" curve sits below "Before" at every month. Panel A shows peak load rising over the year but held ~10–20 MW lower after control (endpoint 160→140 MW, matching the §4.3 July example and the stated ~10% average reduction). Panel B shows voltage fluctuation narrowing from a 4–7.5% band (before) to a 3–5% band (after) — exact bounds stated in §4.3. Supports C04. Anchor values (160→140 MW; 4–7.5%→3–5%) are exact from text; per-month points are estimated (≈).
