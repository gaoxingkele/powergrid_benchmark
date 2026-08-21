# Table 8: Ranking Stability Under Persona, Weighting, Data-Treatment, and Simulated-Agent Scenarios

- **Source**: Energies 2026, 19, 3243, page 23
- **Caption**: Ranking stability under persona, weighting, data-treatment, and simulated-agent scenarios.
- **Screenshot**: `table8.png`
- **Extraction type**: raw_table
- **Data table**:

| Scenario/Persona | Spearman Correlation with Baseline | Top-5 Overlap | Largest Rank Change | Interpretation |
|-----------------|-----------------------------------|--------------|-------------------|----------------|
| Public planner | 0.958 | 4/5 | 8 | Highly stable; stronger emphasis on energy security and sustainability produces only limited top-rank change. |
| Private investor | 0.942 | 4/5 | 8 | Stable overall; market size, macroeconomic feasibility, and institutions slightly reshape the upper ranking. |
| Grid operator | 0.962 | 4/5 | 9 | Highly stable; demand conditions and system-security priorities affect some mid-ranked countries. |
| Sustainability policymaker | 0.938 | 4/5 | 8 | Stable but more sensitive to renewable, carbon, and technical-resource dimensions. |
| Infrastructure fund | 0.977 | 4/5 | 5 | Most stable persona scenario; balanced long-term investment priorities closely follow the baseline. |
| Entropy weighting | 0.892 | 3/5 | 13 | More sensitive; criteria with greater dispersion, especially scale-related indicators, influence the ranking. |
| CRITIC weighting | 0.986 | 5/5 | 4 | Very strong alignment; variability and inter-criterion conflict preserve the baseline top group. |
| Simulated agents, n=500 | 0.932 median | 4/5 median | 10 median; 22 max | Robust under heterogeneous preferences, although extreme agents can substantially shift some country positions. |
