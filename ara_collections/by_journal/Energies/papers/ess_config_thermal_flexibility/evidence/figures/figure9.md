# Figure 9: Scaled Value of Fitness for Different Algorithms

**Source**: Figure 9, Section 6.2, Energies 2025, 18, 2527
**Caption**: "Scaled value of fitness for different algorithms."
**Screenshot**: figure9.png
**Figure type**: quantitative_plot
**Extraction method**: digitized_estimate
**Reading confidence**: low

## Visual description
A line plot showing scaled fitness values vs. iteration count for four algorithms:

**Legend**:
- Method 1 (M1): POA-GWO-CSO (proposed) — highest curve
- Method 2 (M2): Standalone POA (without improvement)
- Method 3 (M3): Standalone GWO (without improvement)
- Method 4 (M4): POA-GWO without CSO improvement

## Axes
- X = Number of iterations, 0–500, scale: linear
- Y = Fitness value (scaled/normalized), 0–1.0, scale: linear

## Trend summary
- **M1 (POA-GWO-CSO)**: Achieves the highest fitness value across the entire iteration range. Converges quickly — reaches high fitness within the first ~100 iterations and continues to rise steadily.
- **M2 (standalone POA)**: Shows the lowest convergence rate and lowest final fitness value among all methods.
- **M3 (standalone GWO)**: Performs better than M2 but still significantly below M1.
- **M4 (POA-GWO without CSO)**: Falls between M3 and M1, confirming that the CSO crossover operators contribute additional search capability beyond the GWO leader integration alone.
- **Ranking**: M1 > M4 > M3 > M2 (by final fitness value).

## Text-derived context
From Section 6.2: "the fitness function value of method 1 (i.e., using the POA-GWO-CSO algorithm) was significantly higher than in the other schemes for the same number of iterations"; "the algorithm could obtain better fitness values in fewer iterations, which indicates that it can find a solution that satisfies the multi-objective optimization at a faster speed."
