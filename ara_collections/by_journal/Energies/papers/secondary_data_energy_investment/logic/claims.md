# Claims

---

## C01: Secondary-data-driven MCDM enables reproducible country-level readiness ranking

- **Statement**: Public secondary data can be transformed into a comparable, normalized country-level decision matrix that produces reproducible energy investment readiness rankings, reducing dependence on expert-only linguistic scoring in multi-criteria energy investment assessment.
- **Conditions**: Requires (a) access to harmonized public data sources (World Bank WDI/WGI, OWID/Ember, IRENA, NASA POWER, Eurostat), (b) clear benefit/cost classification for each criterion, (c) min-max normalization to 0-1 scale, and (d) documentation of all proxy decisions and source notes.
- **Sources**: Section 3.4.3-3.4.4 (Equations 1-3), Tables S1.2-S1.6 in Supplementary File S1, Table 1 in main text.
- **Status**: Supported by empirical implementation -- a complete 36-country by 18-criterion normalized matrix was constructed and used for all subsequent analyses.
- **Falsification**: Demonstrated if a different team using the same data sources and procedures produces substantially different normalized matrices or baseline rankings (e.g., Spearman < 0.90).
- **Proof**: The paper provides the full raw matrix (Table S1.2), normalized matrix (Table S1.4), normalization equations (2-3), and all source references. Equal-weight baseline ranking (Table 2) shows meaningful cross-country variation.
- **Evidence basis**: Table 1 (criteria dictionary), Table 2 (baseline ranking), Supplementary Tables S1.2-S1.6, normalization equations (2) and (3).
- **Dependencies**: A1 (data comparability), A2 (normalization adequacy), A3 (equal-weight baseline).
- **Tags**: reproducibility, secondary-data, MCDM, normalization

---

## C02: Strategic energy investment readiness is multidimensional and requires integration of six distinct criteria dimensions

- **Statement**: Strategic energy investment readiness across countries cannot be captured by a single technical, financial, or environmental indicator; it requires integrated assessment of macroeconomic feasibility, institutional capacity, energy security, sustainability and decarbonization, market and demand conditions, and technical resource potential.
- **Conditions**: Holds when (a) countries exhibit heterogeneous readiness profiles where different dimensions drive overall scores for different countries, (b) no single dimension explains most of the variance in the aggregate score, and (c) the dimension-level decomposition reveals distinct country typologies.
- **Sources**: Section 4.5 (Figure 3), Section 4.10 (Figure 4), Section 4.11 (Table 7), Section 5.1.
- **Status**: Supported by evidence -- dimension-level profiles (Figure 3) show Norway driven by energy security and sustainability, the US by market scale, Turkiye constrained by institutional/macroeconomic factors. Fairness diagnostics (Table 7) show that the ranking is not purely wealth-driven.
- **Falsification**: Refuted if (a) a single dimension accounts for >80% of score variance across all countries, or (b) the country ranking perfectly correlates (r > 0.95) with a single indicator such as GDP per capita or renewable capacity.
- **Proof**: Figure 3 shows distinct dimension-level profiles across countries. Table 7 shows Pearson correlations of 0.727 with GDP per capita and 0.751 with institutional capacity, which are strong but far from deterministic. Partial-correlation diagnostics (Table S1.13) confirm additional dimensions contribute beyond wealth.
- **Evidence basis**: Figure 3 (dimension profiles), Table 7 (fairness correlations), Figure 4 (contribution profiles), Table S1.13 (partial correlations).
- **Dependencies**: C01 (data matrix enables dimensional decomposition).
- **Tags**: multidimensionality, energy-investment, readiness-profiles, MCDM

---

## C03: Persona-based weighting generates stakeholder-sensitive country prioritizations that differ from the equal-weight baseline

- **Statement**: Different stakeholder personas (public planners, private investors, grid operators, sustainability policymakers, infrastructure funds) produce meaningfully different country prioritization rankings when they apply their characteristic dimension-weighting profiles to the same underlying normalized decision matrix.
- **Conditions**: Requires (a) that each persona weight vector (Table 5) reflects plausible, non-trivial differences in dimension priorities, (b) that weights are non-negative and sum to one, and (c) that the top-5 or top-10 country sets shift measurably across personas.
- **Sources**: Section 3.4.8 (Equations 7-8), Section 4.6 (Tables 5-6), Section 4.7, Table S1.11.
- **Status**: Supported -- Table 6 shows that Denmark leads under the sustainability policymaker, the US improves under private investor and grid operator, and Norway remains top across most personas. Top-5 composition changes across profiles.
- **Falsification**: Refuted if all five persona weight vectors produce the same country ranking (i.e., identical top-5 with no rank changes) or if rank differences are within the margin of noise from the normalization procedure alone.
- **Proof**: Table 5 documents five distinct weight vectors (e.g., sustainability policymaker assigns 0.35 to sustainability vs. 0.05 to macroeconomy; private investor assigns 0.25 to macroeconomy and 0.25 to institutions). Table 6 shows resulting country rankings differ across personas.
- **Evidence basis**: Table 5 (persona weights), Table 6 (persona-specific top-5), Table S1.11 (perturbation sensitivity), Section 4.7 (weight perturbation analysis).
- **Dependencies**: C01 (requires the normalized decision matrix), C02 (multidimensionality enables differential weighting).
- **Tags**: stakeholder-analysis, persona-modeling, decision-support, sensitivity

---

## C04: The readiness index captures multidimensional investment readiness beyond wealth and institutional maturity

- **Statement**: The proposed readiness index does not simply reproduce economic capacity (GDP per capita) or institutional quality; it captures additional energy-system, sustainability, market, and resource-potential dimensions that contribute to overall readiness beyond what wealth or governance alone would predict.
- **Conditions**: Valid if (a) the correlation between readiness score and GDP per capita is statistically significant but not near-perfect (r < 0.90), (b) countries with similar GDP per capita show different readiness scores, (c) partial-correlation analysis shows that non-economic dimensions contribute significant additional variance.
- **Sources**: Section 4.11 (Table 7, Figure 5), Table S1.13 (partial-correlation diagnostics), Section 5.1.
- **Status**: Supported -- GDP per capita correlates at Pearson r = 0.727 with baseline score (strong but not deterministic). Figure 5 shows scatter with non-linear distribution. Partial-correlation analysis shows energy security, sustainability, market, and technical-resource dimensions contribute beyond wealth.
- **Falsification**: Refuted if (a) Pearson r between readiness score and GDP per capita exceeds 0.95, (b) partial-correlation analysis shows no significant variance explained by non-economic dimensions after controlling for GDP and institutions, or (c) the ranking perfectly mirrors an existing wealth-based index.
- **Proof**: Table 7 reports Pearson r = 0.727 (GDP) and 0.751 (institutional capacity). Table 7 also shows weaker correlations with renewable capacity (0.323) and technical potential (0.441), confirming the model captures more than just existing infrastructure. Partial-correlation diagnostics (Table S1.13) show non-economic dimensions provide additional information.
- **Evidence basis**: Table 7, Figure 5, Table S1.13.
- **Dependencies**: C02 (multidimensional claim is prerequisite for this fairness check).
- **Tags**: fairness, distributional-analysis, partial-correlation, validity

---

## C05: The baseline ranking shows broad stability under multiple weighting, perturbation, and simulated-agent scenarios

- **Statement**: The equal-weight baseline ranking of country energy investment readiness remains broadly stable under entropy, CRITIC, hybrid entropy-CRITIC weighting, persona-weight perturbations (+/-10%, +/-20%), outlier treatment, and simulated-agent preference heterogeneity (n=500), with median Spearman correlation of 0.932 across simulated agents.
- **Conditions**: Requires (a) that alternative weighting methods are derived from the same normalized matrix, (b) that simulated agents are generated from stakeholder-relevant anchors with plausible variation ranges, and (c) that stability is measured through Spearman rank correlation, top-k overlap, and largest rank change metrics.
- **Sources**: Section 4.4 (Table 4), Section 4.7, Section 4.12 (Table 8), Tables S1.9, S1.11, S1.12.
- **Status**: Supported -- CRITIC weighting shows Spearman = 0.986 with baseline; entropy shows 0.892; personas range from 0.938 to 0.977; simulated agents median = 0.932 (Table 8). Top-5 overlap is 4/5 for most scenarios.
- **Falsification**: Refuted if any objectively reasonable weighting scheme or simulated-agent profile produces a Spearman correlation < 0.70 with the baseline, or if the top-5 overlap for multiple scenarios drops to 0/5.
- **Proof**: Table 8 summarizes all stability scenarios: Spearman correlations range from 0.892 (entropy) to 0.986 (CRITIC), with persona scenarios from 0.938 to 0.977. Simulated agents (n=500) yield median Spearman = 0.932. Top-5 overlap is 4/5 or 5/5 for most scenarios.
- **Evidence basis**: Table 4 (weighting comparison), Table 8 (full stability summary), Tables S1.9, S1.11, S1.12.
- **Dependencies**: C01 (requires the normalized matrix for re-weighting), C03 (persona scenarios inform perturbation ranges).
- **Tags**: robustness, sensitivity-analysis, simulated-agents, validation
