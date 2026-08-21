# Figure 5: Selling (a) and buying (b) bid time-varying factors boxplots

- **Source**: Figure 5, Section 3, p. 13
- **Caption**: "Selling (a) and buying (b) bid time-varying factors boxplots."
- **Screenshot**: figure5.png (lower half of page 13)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: box
- **Axes**: (a) Y = Time varying factors, 1–9 (linear); (b) Y = Time varying factors, 0.0–2.0 (linear). X categories are per-service ratio factors.

The factors are obtained by averaging the hourly ratio between ASM bid prices of each service and DAM step prices from Italian market data [41]. Panel (a) = selling bids (factors > 1); panel (b) = buying bids (factors mainly < 1). Values approximate — median (box center) and whisker/outlier extent read visually.

Panel (a) selling: R^u_{1,t} (UR step1), R^u_{2,t} (UR step2), R^u_{3,t} (UR step3), R^su_t (SU), R^{sr_u}_t (upward SR):
| Series | Median ≈ | Box (IQR) ≈ | Outliers up to ≈ |
|--------|----------|-------------|-------------------|
| R^u_1 | ≈1.5 | 1.3–1.8 | ≈4 |
| R^u_2 | ≈1.8 | 1.4–2.3 | ≈6.5 |
| R^u_3 | ≈2.3 | 1.7–3.0 | ≈8+ |
| R^su | ≈1.5 | 1.3–1.8 | ≈4 |
| R^{sr_u} | ≈1.8 | 1.5–2.3 | ≈5 |

Panel (b) buying: R^d_{1,t}, R^d_{2,t}, R^d_{3,t} (DR steps), R^sd_t (SD), R^{sr_d}_t (downward SR):
| Series | Median ≈ | Box (IQR) ≈ |
|--------|----------|-------------|
| R^d_1 | ≈0.55 | 0.45–0.65 |
| R^d_2 | ≈0.50 | 0.4–0.6 |
| R^d_3 | ≈0.45 | 0.35–0.55 |
| R^sd | ≈0.38 | 0.3–0.45 |
| R^{sr_d} | ≈0.45 | 0.4–0.5 |

## Trend summary
Selling factors (UR, SU, USR) are all > 1 and increase with the UR step index (later UR steps carry larger factors, with heavy upper-tail outliers), making ASM upward power increasingly profitable. Buying factors (DR, SD, DSR) are all < 1 (mostly 0.35–0.65), so buying-back bids are cheaper than the DAM marginal price, ensuring TSO revenue. Consistent with text (Section 3). Assigned per unit with a Gaussian variation, 99.7% CI set at 10% of the value.
