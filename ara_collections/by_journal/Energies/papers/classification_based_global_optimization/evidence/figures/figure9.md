# Figure 9 - IEEE 33-Bus Thermal Capacity Limits Effect

**Source**: Figure 9, Section 5.1.3
**Caption**: IEEE-33 thermal capacity limits effect.
**Screenshot**: figure9.png
**Figure type**: quantitative_plot
**Extraction method**: visual_description
**Reading confidence**: low

- **Plot kind**: bar/combined (bar chart with capacity limit line)
- **Axes**: X = Branch number (1-32, linear), Y = Power flow / capacity (kVA or p.u., linear)

## Visual description
The figure shows branch power flow levels for all 32 distribution branches of the IEEE 33-bus system under the optimized configuration, compared against each branch's thermal capacity limit (shown as a horizontal line or individual markers for each branch). Multiple series likely represent the different hosting factors (30%, 40%, 50%).

## Trend summary
All branches carry power below their respective thermal capacity limits for all hosting factors. The margin between operating power flow and the capacity limit is visible for most branches. Branches near the substation (branches 1-5) typically carry higher power flows but remain below the limit. Higher hosting factors show marginally higher branch loading but still within limits. This validates that the CGO solution respects thermal constraints.
