# Figure 2: Black-Box Hydrogen Tank Cost Function

**Source**: Page 6 of the PDF.

**Visual Description**:
A line plot showing the hydrogen storage tank investment cost (Million USD, y-axis) as a function of hydrogen tank capacity (MWh, x-axis from 0 to 100 MWh).

**Key features of the curve**:
- **Base upward trend**: The cost generally increases with capacity following a power-law (x^0.7) trend, representing economies of scale (sub-linear growth)
- **Sinusoidal oscillation**: A periodic wavy pattern (sine wave) is superimposed on the base cost, creating multiple local minima and maxima
- **Step discontinuity at x=50 MWh**: A visible downward jump at 50 MWh where the bulk-purchase discount (×0.9) is applied
- **Minimum threshold at $1M**: The cost function has a floor at C_min = $1M

**Curve character**: The function is:
- Non-convex (sinusoidal oscillations create alternating convex and concave regions)
- Non-monotonic (the sinusoidal perturbation means larger capacity does not always mean higher cost)
- Discontinuous at x=50 MWh (step discount)
- Non-differentiable at the discount point and at C_min

**Data extraction**: Approximate values along the curve:
- At E_H2 = 10 MWh: cost ≈ $2.5M (near a local maximum)
- At E_H2 = ≈23 MWh: cost ≈ $4.5M (near a local minimum — where optimal solution lands)
- At E_H2 = 50 MWh: cost ≈ $10M (just before discount)
- At E_H2 = 60 MWh: cost ≈ $9M (after discount)
- At E_H2 = 100 MWh: cost ≈ $12M

**Annotations on the figure**:
- "Non-convex / Non-monotonic (sin(x))" — highlighting the sinusoidal character
- "Discontinuous Discount (x>50)" — pointing to the step discount
- "Min Threshold ($1M)" — marking the minimum cost
- "Cost Function (See Eq. 8)" — reference to the equation
