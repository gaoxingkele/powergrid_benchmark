# Figure 2: Time Series Plot

- **Source**: Figure 2, Section 3.1 (p.6)
- **Caption**: "Time series plot."
- **Screenshot**: figure2.png
- **Figure type**: line plot (time series)
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description

A time-series line plot with "Load vs. Datetime" as the chart title. The x-axis represents datetime (January 2022 through December 2022 at 15-min intervals), and the y-axis represents load in megawatts (MW). The plot shows the actual Elia Grid load values as blue markers or a continuous blue line across the full year.

**Axes**:
- X-axis: DateTime (1 Jan 2022 to 31 Dec 2022 / 14 Dec 2022); densely packed due to 15-min sampling (~35,040 data points).
- Y-axis: Load (MW), ranging from approximately 0 MW to approximately 14,000 MW.

**Key visual features**:
- The load exhibits clear seasonal cycles: lower troughs in summer months (July–August), higher peaks in winter months (December–January).
- Within-week periodicity is visible as repeated short-term oscillations (higher weekday loads, lower weekend loads).
- Sudden spikes and dips are visible throughout the series, especially during transition seasons.
- Near-zero outlier readings are visible at scattered points (e.g., ~0 MW dips).

**Note on paper inconsistency**: Figure 2's caption says "Time series plot" and is framed as an actual-vs-predicted comparison in the paper's narrative, but the plotted title reads "Load vs. Datetime" and shows only actual load data points. No prediction trace is visible in this figure.

**Relevant claims/observations**: Supports O3 (load has spikes, non-stationarity, human-driven randomness) and provides visual context for C01 and C03 (hybrid advantage in volatile regimes).
