# Figure 6: GSOA-Benders Convergence Curve

**Source**: Page 16 of the PDF.

**Visual Description**:
A convergence plot showing the GSOA-Benders optimization progress over time.

- **X-axis**: Time (seconds), from 0 to approximately 36 seconds
- **Y-axis**: Total cost (objective value) — scale not explicitly readable from the PDF text description

**Plot features**:
- **Upper line (red/blue)**: The upper bound (UB_k), representing the best feasible total cost found so far. This line should decrease monotonically or stepwise as better solutions are found.
- **Lower line**: The master problem value (c_LB_k) over the accumulated cut approximation
- The gap between the upper and lower curves narrows as the algorithm progresses
- The curves converge near the end (at t ≈ 36s), indicating the stability gap criterion is met

**Key observations from the paper text**:
- The framework successfully converged within 36s
- The final objective value is −242,940.18 (matching both GSOA-Benders and SFOA-Benders)
- The convergence demonstrates the effectiveness of Benders cuts as a surrogate for the expected operational cost

**Data extraction**: Specific convergence values are not available from the text. The figure serves as a qualitative illustration of stable convergence behavior.
