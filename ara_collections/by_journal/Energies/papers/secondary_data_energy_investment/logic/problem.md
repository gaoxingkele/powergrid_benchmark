# Research Problem

## Observations

1. Strategic energy investment prioritization is a multidimensional country-level decision problem shaped by energy security, decarbonization pressure, affordability, institutional feasibility, electricity-market stability, technical resource potential, and financing conditions.
2. Countries exhibit uneven readiness profiles: a country may have strong solar or wind potential but weak macroeconomic stability; another may have advanced institutions but limited demand growth; a third may have large market scale but high price volatility and fossil-based electricity dependence.
3. Multiple stakeholder types (public planners, private investors, grid operators, sustainability policymakers, infrastructure funds) have fundamentally different priorities when evaluating country-level energy investment readiness.
4. Many existing MCDM applications in energy depend heavily on expert-derived linguistic scores for both criterion weights and alternative performance values, which can limit reproducibility and cross-country comparability.
5. Variables such as electricity price volatility, renewable electricity share, energy import dependence, carbon intensity, demand growth, solar irradiance, and wind speed can be operationalized through public datasets.

## Gaps

- **G1 (methodological)**: Existing studies on energy transition, fuzzy MCDM, and decision support systems are fragmented. Energy transition studies document emissions, renewable penetration, and investment conditions but do not always transform these into structured, stakeholder-sensitive prioritization models.
- **G2 (reproducibility)**: Many fuzzy MCDM applications rely on expert linguistic scores for both weights and alternative performance, reducing reproducibility and cross-country comparability when measurable secondary data are available.
- **G3 (stakeholder sensitivity)**: A single universal ranking does not reflect stakeholder diversity. Public planners, private investors, grid operators, and sustainability policymakers have different evaluation criteria.
- **G4 (fairness)**: Rankings may inadvertently favor high-income countries, institutionally mature countries, or countries with already developed renewable infrastructure, while resource-rich but financially constrained countries may be penalized.
- **G5 (robustness validation)**: Conventional MCDM robustness analysis is often limited to changing criterion weights and observing rank variation, without capturing the behavioral diversity of decision environments through simulated-agent approaches.
- **G6 (boundary clarity)**: Many AI-assisted and fuzzy DSS studies combine several advanced components without making the empirical status of each component explicit, creating ambiguity about what is actually implemented versus proposed.

## Key Insight

Public secondary data (World Bank, IRENA, NASA POWER, Eurostat, Ember/OWID) can be systematically transformed into a comparable country-level decision matrix through clear indicator selection, benefit/cost classification, normalization, and source documentation. This enables a reproducible, explainable, and stakeholder-sensitive MCDM framework that reduces dependence on expert-only linguistic scoring while maintaining the ability to represent uncertainty through fuzzy extensions when sufficient time-series data are available.

## Assumptions

1. **A1 (data comparability)**: International harmonized data sources (World Bank WDI/WGI, OWID, Ember, IRENA, NASA POWER) provide sufficiently comparable cross-country indicators for strategic screening purposes.
2. **A2 (normalization adequacy)**: Min-max normalization with benefit/cost classification adequately transforms heterogeneous indicators into comparable 0-1 scales without distorting the underlying readiness signal.
3. **A3 (equal-weight baseline)**: Equal weighting provides a neutral and transparent benchmark for baseline readiness scoring before introducing stakeholder-specific or objective weighting schemes.
4. **A4 (latest-year snapshot)**: The latest available cross-sectional data provide a meaningful snapshot of current readiness, accepting that this does not capture long-term transition dynamics.
5. **A5 (country-level granularity)**: Country-level solar irradiance and wind-speed indicators (from representative coordinates) are adequate for strategic screening but not substitutes for project-level resource assessments.
6. **A6 (synthetic agents)**: Simulated-agent validation with synthetic preference profiles provides meaningful robustness evidence even though it does not replace observed decision-maker behavior.
