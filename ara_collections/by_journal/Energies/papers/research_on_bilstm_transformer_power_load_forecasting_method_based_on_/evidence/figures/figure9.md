# Figure 9

**Source:** `evidence/figures/figure9.png`

**Caption:** Figure 9. Weekly load forecasting curves.

**Figure type:** Quantitative plot

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — weekly load prediction comparison across models.

**Structured Description:**

This figure shows weekly load forecasting curves over a full week (336 time steps at 0.5h resolution), comparing model predictions against actual load values.

**Plot layout:**
- **X-axis:** Time over one week (Monday 00:00 through Sunday 23:30)
- **Y-axis:** Power load value

**Model traces:**
- Actual load curve
- DAF-BT prediction
- Selected baseline model predictions (typically 2-4 baselines for readability)

**Key visual observations:**
- The weekly pattern shows five similar weekday profiles followed by two distinct weekend day profiles
- Weekend days show lower overall load levels and different peak timing (the "weekend effect")
- Transition periods (Friday-to-Saturday and Sunday-to-Monday) are visible as profile changes
- DAF-BT maintains closer tracking during these transition periods compared to baselines
- Error accumulation over the week may be visible for some baseline models (prediction drift)
- DAF-BT shows less drift and maintains consistent tracking quality across all seven days

This figure is part of Experiment E02 (multi-time-scale evaluation), extending the analysis from daily to weekly horizons.
