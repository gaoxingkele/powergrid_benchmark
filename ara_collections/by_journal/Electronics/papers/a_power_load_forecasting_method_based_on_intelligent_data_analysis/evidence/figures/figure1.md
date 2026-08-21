# Figure 1: Flowchart of the EMD Algorithm

- **Source**: Figure 1, §3.1 (p.5)
- **Caption**: "Flowchart of the EMD Algorithm."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high
- **Location on page**: mid-to-lower page, below Eq. 3.

## Visual description
- **Components (top→bottom)**: Begin → "Time series x(t)" → "Determine the local maxima and local
  minima of x(t)" → "Fitting the upper envelope to the lower envelope" → "Calculate the average
  value of the envelope m(t)" → "h(t)=x(t)−m(t)" → decision "h(t) Whether the IMF condition is
  satisfied" → "r(t)=x(t)−h(t)" → decision "Meet the stopping conditions" → End.
- **Connections / loops**:
  - From "h(t) Whether the IMF condition is satisfied": **No** → "x(t)=h(t)" → loops back up to
    "Determine the local maxima and local minima"; **Yes** → "r(t)=x(t)−h(t)".
  - From "Meet the stopping conditions": **No** → "x(t)=r(t)" → loops back to the maxima/minima step;
    **Yes** → End.
- **Annotations**: Two nested loops — the inner sifting loop (IMF condition) and the outer residual
  loop (stopping condition).
- **What it conveys**: The iterative sifting procedure of EMD: repeatedly extract IMFs by envelope
  averaging until the IMF condition holds, then peel off residuals until the stopping condition is
  met. Mirrored into logic/solution/method.md (Stage 1a, EMD).
