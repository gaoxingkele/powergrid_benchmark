# Concepts

---

## Concept 1: Strategic Energy Investment Readiness Score

- **Notation**: S_i (baseline), S_i^(p) (persona-specific)
- **Definition**: A composite score representing the relative readiness and attractiveness of a country for strategic energy investment, computed as the weighted sum of normalized criterion values. Higher scores indicate stronger overall readiness across macroeconomic, institutional, energy-security, sustainability, market, and technical-resource dimensions.
- **Formula**: S_i = sum_{j=1}^{m} w_j * r_ij
- **Boundary conditions**: Scores range from 0 to 1 (since normalized values are in [0,1] and weights sum to 1). The score is an ordinal screening indicator, not an absolute measure of investment return or risk.
- **Related concepts**: Persona-specific score (S_i^(p)), normalized performance value (r_ij), criterion weight (w_j)

---

## Concept 2: Secondary-Data Decision Matrix

- **Notation**: X = [x_ij] where i = 1,...,n (countries) and j = 1,...,m (criteria)
- **Definition**: A country-by-criterion matrix populated with observed values from public secondary data sources (World Bank WDI/WGI, OWID/Ember, IRENA, NASA POWER, Eurostat, ENTSO-E, Countryeconomy). Each cell x_ij records the observed value of country i on criterion j.
- **Boundary conditions**: Requires complete data for all country-criterion pairs (18/18 coverage for countries in the sample). Missing values would require imputation or exclusion. Data comparability depends on harmonized international reporting standards.
- **Related concepts**: Normalized decision matrix (R = [r_ij]), benefit/cost classification, normalization

---

## Concept 3: Benefit/Cost Normalization (Min-Max)

- **Notation**: r_ij (normalized value)
- **Definition**: A linear scaling procedure that transforms raw indicator values into a common [0,1] scale while preserving directional consistency. Benefit indicators (higher = better) use r_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j)). Cost indicators (higher = worse) use r_ij = (max(x_j) - x_ij) / (max(x_j) - min(x_j)).
- **Boundary conditions**: Sensitive to outliers (extreme values compress the scale for other observations). Preserves ordinal relationships within each criterion but discards absolute magnitude information. Assumes linear value scaling within each criterion.
- **Related concepts**: Decision matrix X, weighted score S_i, standardization (alternative normalization approach)

---

## Concept 4: Objective Weighting Methods (Entropy, CRITIC, Hybrid)

- **Notation**: w_j^(entropy), w_j^(critic), w_j^(hybrid)
- **Definition**: Data-driven weight determination methods that derive criterion importance from the statistical properties of the normalized decision matrix rather than from subjective expert judgment. Entropy weighting assigns higher weights to criteria with greater information dispersion (more discrimination power). CRITIC (Criteria Importance Through Intercriteria Correlation) considers both criterion variability and conflict (negative correlation with other criteria). The hybrid method averages entropy and CRITIC weights.
- **Boundary conditions**: These weights reflect statistical properties of the data, not necessarily economic importance or stakeholder preferences. Entropy can over-weight scale-related variables (e.g., electricity demand). CRITIC can under-weight criteria that correlate with many others. These limitations motivate using them as sensitivity benchmarks rather than primary weights.
- **Related concepts**: Equal weighting (baseline), causal-evidence weighting (modular extension), LLM-salience weighting (modular extension)

---

## Concept 5: Persona-Based Decision Profile

- **Notation**: W^(p) = (w_1^(p), w_2^(p), ..., w_m^(p))
- **Definition**: A stakeholder-specific weight vector that reflects the relative importance a particular decision-maker type assigns to each readiness dimension. The study defines five personas: public planner, private investor, grid operator, sustainability policymaker, and infrastructure fund. Weights are non-negative and sum to one for each persona.
- **Boundary conditions**: Persona weights are theory-informed approximations, not empirically elicited from real stakeholders. Weights are assigned at the dimension level (6 dimensions) and uniformly distributed within each dimension to individual criteria. Persona stability is tested through +/-10% and +/-20% perturbation analysis.
- **Related concepts**: Baseline equal-weight profile, simulated-agent validation, dimension-level aggregation

---

## Concept 6: Simulated-Agent Validation Laboratory

- **Notation**: n = 500 synthetic agents
- **Definition**: A robustness validation procedure that generates 500 synthetic decision agents by randomly varying the relative importance assigned to the six readiness dimensions around stakeholder-relevant anchors. Each simulated agent produces a country ranking, and the distribution of rankings is compared with the baseline using Spearman correlation, top-k overlap, and maximum rank change metrics.
- **Boundary conditions**: Simulated agents represent hypothetical preference heterogeneity, not observed decision-maker behavior. The procedure tests whether the ranking structure is robust to plausible variations in decision logic, but it does not validate against real-world investment outcomes. Extreme agents (strongly prioritizing a single dimension) can produce larger rank shifts (up to 22 positions).
- **Related concepts**: Persona-based ranking, weight perturbation analysis, conventional sensitivity analysis (weight-only)

---

## Concept 7: Criterion Contribution Decomposition (Explainability)

- **Notation**: C_ij = w_j * r_ij
- **Definition**: A linear decomposition of each country's readiness score into criterion-level contributions, showing how much each individual criterion contributes to the final score. Contributions can be aggregated by dimension to identify which readiness areas drive or constrain a country's overall position.
- **Boundary conditions**: Assumes additive independence among criteria (no interaction effects). The decomposition is exact for weighted sum models but does not capture synergistic or emergent effects. Visualized through arrow diagrams (Figure 4) distinguishing strengthening (positive) and constraining (negative) contributions relative to the criterion mean.
- **Related concepts**: Baseline score S_i, dimension-level aggregation, fairness diagnostics
