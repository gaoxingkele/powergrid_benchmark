# Figure 1: Generation of wind and photovoltaic daily curve

- **Source**: Figure 1, Section 3 (DG Output Prediction Model), page 5
- **Caption**: "Generation of wind and photovoltaic daily curve."
- **Screenshot**: figure1.png (diagram mid-page 5, below Equation (5))
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (dashed box titled "Scenery day curve generation"):
  - "Random sampling" block
  - Matrix block `N[u^1 u^2 ... u^24 ; v^1 v^2 ... v^24]` — 24-hour sampled uniform variates for wind (u) and PV (v)
  - Inverse-CDF block `x^i = F_x^{-1}(u^i)`, `y^i = F_y^{-1}(v^i)`
  - Matrix block `N[x^1 x^2 ... x^24 ; y^1 y^2 ... y^24]` — reconstructed 24-hour wind (x) and PV (y) output
- **Connections**: Random sampling → sampled (u,v) matrix → inverse marginal transform → reconstructed (x,y) output matrix (forming the daily curve).
- **Annotations**: 24 columns denote the 24 hours of a typical day; two rows separate wind vs PV.
- **What it conveys**: the copula-based scenario pipeline — draw correlated uniforms via the Frank copula, then invert each variable's marginal CDF (fitted by KDE) to obtain a joint wind–PV 24-hour output scenario. Mirrored in `logic/solution/method.md`.
