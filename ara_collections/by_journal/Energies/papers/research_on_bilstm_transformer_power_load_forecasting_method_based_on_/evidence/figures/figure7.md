# Figure 7

**Source:** `evidence/figures/figure7.png`

**Caption:** Figure 7. Daily load forecasting curves.

**Figure type:** Quantitative plot

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — daily load prediction comparison across models.

**Structured Description:**

This figure shows daily load forecasting curves comparing model predictions against actual load values at the daily time scale (48 time steps for a 24-hour period at 0.5h resolution).

**Plot layout:**
- **X-axis:** Time of day (00:00 to 23:30)
- **Y-axis:** Power load value

**Model traces:**
- Actual load curve
- Multiple baseline model predictions
- DAF-BT prediction
- Usually 4-6 models are shown per panel for readability

**Key visual observations:**
- The daily load shape typically shows: low overnight demand, morning ramp-up (6:00-9:00), daytime plateau, evening peak (17:00-21:00), and nighttime decline
- The weekend effect may be visible if weekday vs. weekend days are compared
- DAF-BT tracks the morning ramp and evening peak more accurately than baselines
- The model shows less overshoot at peak points and less undershoot at valley points

This figure is part of Experiment E02 (multi-time-scale evaluation) alongside Figure 8 (quantitative errors for daily load).
