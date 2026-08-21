# Experiments

---

## E01: Baseline Country Readiness Ranking (Equal-Weight Model)

- **Verifies**: C01 (reproducible secondary-data ranking), C02 (multidimensional readiness)
- **Evidence**: Table 2, Supplementary File S1 Table S1.5
- **Run**: Baseline equal-weight ranking with 36 countries x 18 criteria
- **Setup**: Normalized decision matrix R = [r_ij] with values in [0,1]; equal weights w_j = 1/18 for all j = 1,...,18; scores computed as S_i = sum_j w_j * r_ij; countries ranked by descending S_i.
- **Procedure**: (1) Assemble raw data matrix X from 10+ public data sources (World Bank WDI/WGI, OWID/Ember, IRENA, NASA POWER, Eurostat, ENTSO-E, Countryeconomy); (2) Classify each criterion as benefit or cost; (3) Apply min-max normalization per benefit/cost type; (4) Compute weighted sum with equal weights; (5) Rank countries by score.
- **Metrics**: Baseline readiness score (0-1 scale), rank position, data coverage (18/18 for all 36 countries).
- **Expected outcome**: Meaningful cross-country variation in readiness scores demonstrating unequal readiness; clear separation between top-tier and bottom-tier countries; all countries have full data coverage.

---

## E02: Convergent Validity Against External Benchmarks

- **Verifies**: C01 (index validity), C04 (captures more than wealth)
- **Evidence**: Table 3, Supplementary File S1 Table S1.10
- **Run**: Post-hoc validation against independent investment/transition benchmarks
- **Setup**: Baseline readiness scores correlated with five observable benchmarks: FDI inflows (% GDP), renewable electricity share, renewable installed capacity, electricity carbon intensity, electricity demand/market scale. Also compared qualitatively with Climatescope, RECAI, Climate Change Performance Index, Energy Transition Index.
- **Procedure**: (1) Collect benchmark data from independent sources; (2) Compute Pearson r and Spearman rho between baseline readiness score and each benchmark; (3) Compare direction and strength with expected associations; (4) Qualitatively compare with existing transition/investment indices.
- **Metrics**: Pearson r (p-value), Spearman rho (p-value), direction consistency with expectations.
- **Expected outcome**: Significant positive association with renewable share and capacity; significant negative association with carbon intensity; weaker positive association with FDI and demand (indicating readiness is not merely market-size or capital-flow driven).

---

## E03: Alternative Weighting Sensitivity Analysis

- **Verifies**: C05 (ranking stability under weighting changes)
- **Evidence**: Table 4, Supplementary File S1 Table S1.9
- **Run**: Entropy, CRITIC, and hybrid entropy-CRITIC weighting comparison
- **Setup**: Three objective weighting methods computed from the same normalized 36x18 matrix. Each produces a distinct weight vector. Country scores are recalculated with each weight vector and compared with the equal-weight baseline.
- **Procedure**: (1) Compute entropy weights from normalized matrix (information dispersion); (2) Compute CRITIC weights (variability + inter-criterion conflict); (3) Compute hybrid as arithmetic mean of entropy and CRITIC weights; (4) Recalculate country scores with each weight set; (5) Compare rankings via Spearman correlation, top-5 overlap, top-10 overlap, and identify top-ranked countries.
- **Metrics**: Spearman correlation with baseline, top-5 overlap (/5), top-10 overlap (/10), identity of top-ranked countries.
- **Expected outcome**: CRITIC highly consistent with baseline with very strong rank correlation; entropy more sensitive due to overweighting of high-dispersion criteria (scale-related variables); hybrid intermediate between the two; all methods preserve the broad country ordering with some top-5 and top-10 composition changes.

---

## E04: Persona-Based Stakeholder Ranking

- **Verifies**: C03 (persona sensitivity), C05 (stability under stakeholder variation)
- **Evidence**: Tables 5, 6, Supplementary File S1 Table S1.11
- **Run**: Five stakeholder persona ranking scenarios
- **Setup**: Five theory-informed weight vectors (public planner, private investor, grid operator, sustainability policymaker, infrastructure fund) applied to the same normalized 36x18 matrix. Each persona redistributes weights across the six readiness dimensions.
- **Procedure**: (1) Define dimension weights for each persona (Table 5); (2) Distribute dimension weight equally to constituent criteria within each dimension; (3) Recalculate scores as S_i^(p) = sum_j w_j^(p) * r_ij; (4) Rank countries by persona-specific score; (5) Compare top-5 sets across personas and against baseline.
- **Metrics**: Persona-specific top-5 countries with scores, rank composition overlap across personas, comparison with baseline ranking, stability under +/-10% and +/-20% weight perturbation.
- **Expected outcome**: Norway remains top in most profiles; Denmark leads under sustainability policymaker; US improves under private investor and grid operator; country sets differ across personas confirming stakeholder sensitivity.

---

## E05: Fairness and Distributional Diagnostics

- **Verifies**: C04 (readiness beyond wealth/institutions), C02 (multidimensionality)
- **Evidence**: Table 7, Figure 5, Supplementary File S1 Table S1.13
- **Run**: Fairness check against GDP per capita, institutional capacity, renewable capacity, technical resource potential
- **Setup**: Baseline readiness scores correlated with four distributional factors. Partial-correlation analysis controls for GDP per capita and institutional capacity to test whether non-economic dimensions contribute additional explanatory power.
- **Procedure**: (1) Compute Pearson and Spearman correlations between baseline score and GDP per capita, institutional capacity, renewable installed capacity, technical resource potential; (2) Plot scatter of readiness score vs. GDP per capita (Figure 5); (3) Conduct partial-correlation analysis controlling for GDP and institutions to assess residual contribution of other dimensions.
- **Metrics**: Pearson correlation, Spearman correlation, scatter distribution, partial-correlation coefficients and significance.
- **Expected outcome**: Strong but not deterministic correlations with GDP per capita and institutional capacity (both statistically significant but far from unity); weaker correlations with renewable capacity and technical resource potential; scatter plot shows non-linear distribution with countries above and below the trend line; partial-correlation analysis confirms non-economic dimensions contribute significant additional information beyond wealth and institutions.

---

## E06: Robustness and Simulated-Agent Validation

- **Verifies**: C05 (ranking stability under diverse preferences)
- **Evidence**: Table 8, Supplementary File S1 Table S1.12
- **Run**: Full robustness suite including simulated agents (n=500), persona scenarios, weighting methods, and data treatment variations
- **Setup**: Multiple alternative ranking scenarios generated through (a) four alternative weighting methods, (b) five persona profiles (already computed in E04), (c) persona-weight perturbations at +/-10% and +/-20%, and (d) 500 simulated decision agents with random preference variation around stakeholder-anchored dimension weights.
- **Procedure**: (1) For each scenario/agent, compute alternative country ranking; (2) Compare each alternative ranking with baseline using Spearman rank correlation, top-5 overlap, and largest rank change; (3) Report summary statistics across all simulated agents.
- **Metrics**: Spearman correlation with baseline (range, median), top-5 overlap (median and range), largest rank change (median and maximum).
- **Expected outcome**: Persona scenarios show high rank correlation with baseline and strong top-5 overlap; CRITIC weighting shows the strongest alignment with baseline; entropy weighting is more sensitive but still produces broadly consistent ordering; simulated agents yield a high median rank correlation across 500 heterogeneous preference profiles, although extreme agents (strongly prioritizing a single dimension) can substantially shift some country positions.
