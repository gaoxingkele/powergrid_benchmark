# Figure 16: Comparison of algorithm iterations

- **Source**: Figure 16, Section 4.3 (page 20). Figure in the lower portion of the page.
- **Caption**: "Comparison of algorithm iterations."
- **Screenshot**: figure16.png
- **Figure type**: quantitative_plot
- **Extraction method**: exact_from_labels
- **Reading confidence**: high
- **Plot kind**: line (three convergence curves)
- **Axes**: X = Iterations (0–200, linear), Y = Degree of approximation to ideal solution (≈0.3–1.0, linear; TOPSIS relative closeness)

Three series: Improved PSO (black), DBO (blue), PSO (red). Convergence points stated verbatim in §4.3 text.

| Algorithm | Iterations at convergence | Proximity to ideal solution at convergence |
|-----------|---------------------------|--------------------------------------------|
| PSO | 100 | 0.80 |
| DBO | 73 | 0.82 |
| Improved PSO (IPSO) | 46 | 0.86 |

## Trend summary
All three curves rise from ≈0.35–0.4 and plateau. Improved PSO converges fastest (46 iterations) and to the highest closeness (0.86); DBO next (73 iter, 0.82); PSO slowest (100 iter, 0.80). Text derives: vs PSO, IPSO reduced iterations-to-convergence by 54.0% ((100−46)/100) and improved closeness by 7.5% ((0.86−0.80)/0.80). Values are stated exactly in text (not read off pixels).

**Note**: The Abstract reports the iteration reduction as 52.0%, whereas §4.3/§5 report 54.0%; the 54.0% figure is consistent with the stated 100→46 iterations. Recorded as a source inconsistency.
