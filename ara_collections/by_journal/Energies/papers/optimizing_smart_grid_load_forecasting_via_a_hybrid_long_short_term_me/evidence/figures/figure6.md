# Figure 6: Heatmap of Load by Hour and Date

- **Source**: Figure 5 (in-text reference in Section 3.1, p.6)
- **Caption**: Not independently captioned — referenced as a heatmap showing load patterns across hours and dates.
- **Screenshot**: figure6.png
- **Figure type**: 2D heatmap / color-mesh
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description

A 2D heatmap with dates on the x-axis and hours of the day (0–23) on the y-axis, where each cell is colored according to the average or actual load value at that (date, hour) combination.

**Axes**:
- X-axis: Date (January 2022 through December 2022, approximately monthly ticks).
- Y-axis: Hour of day (0 to 24, top to bottom or bottom to top).

**Color mapping**:
- A continuous color scale (typically cool-to-warm, e.g., blue-to-red or viridis colormap) represents load magnitude.
- Low-load cells appear in cool colors (blue); high-load cells appear in warm colors (red/orange).
- The paper's figure uses a heat color map where darker / warmer colors indicate higher load.

**Key visual features**:
- **Vertical stripes** (columns): daily load profiles shift seasonally — winter days show more warm cells (higher load) across most hours; summer days shift cooler.
- **Horizontal bands** (rows by hour): a clear diurnal pattern is visible:
  - Early morning hours (0–5): consistently cool (low demand, off-peak).
  - Morning ramp-up (6–9): transition from cool to warm (increasing demand as经济活动 begins).
  - Daytime plateau (9–17): warm/hot (peak demand hours).
  - Evening decline (18–23): cooling transition back to off-peak.
- Weekends appear as periodic vertical bands with cooler colors (lower demand) compared to adjacent weekdays.
- The near-zero outlier dates appear as isolated cool (dark blue) vertical stripes.

**What it conveys**: The heatmap reveals the daily and weekly periodicity of electricity demand, the seasonal shift in load magnitude, and the stable diurnal pattern across the year. The clear day-night and weekday-weekend contrasts are inputs the model's datetime features (hour, day-of-week, weekday indicator) are designed to capture.

**Relevant observations**: Supports O3 (load has non-stationarity across daily, weekly, and seasonal cycles).
