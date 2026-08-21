# Figure 2: Scenario generation result of the wind power

**Source**: Figure 2, Section 5.1, page 12
**Location on page**: bottom of page 12
**Caption**: "Scenario generation result of the wind power."
**Screenshot**: figure2.png
**Figure type**: quantitative_plot
**Extraction method**: digitized_estimate
**Reading confidence**: low
**Plot kind**: line (3D surface / waterfall of many scenario curves)
**Axes**: X = Time (×15 min, 0-100 steps = 96-point typical day), Y = Scenario (0-500 index),
Z = Active Power (kW, linear, 0-800)

| Quantity | Value |
|----------|-------|
| Number of generated scenarios | 500 (stated in text) |
| Time resolution | 15 min, 96 points/day |
| Peak active power (visual) | ≈800 kW |

## Trend summary
A dense 3D waterfall of 500 Latin-hypercube-sampled wind-power curves over one typical day. Each
curve follows the base typical-day wind profile with Weibull-derived random perturbations. Envelope
spans roughly 0 to ≈800 kW; the bundle is widest (most uncertain) at mid-day time steps. Individual
curves are unreadable (500 overlaid) — only the ensemble spread is meaningful. This is the input
scenario set later reduced to 5 representatives (Figure 3).
