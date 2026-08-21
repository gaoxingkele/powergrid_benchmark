# Constraints and Known Limitations

## Boundary Conditions

1. **Geographic scope**: Results apply to the 36-country sample (EU-27, UK, Norway, Switzerland, Turkiye, US, Canada, Japan, South Korea, Australia). Findings do not generalize to developing economies, African nations, Latin American countries, or non-OECD Asia without additional validation and data comparability checks.

2. **Temporal scope**: The empirical application is based on the latest available cross-sectional data (circa 2024-2025), capturing a snapshot rather than long-term transition dynamics. The baseline does not incorporate time trends, panel effects, or trajectory analysis.

3. **Decision level**: The framework is designed as an early-stage country-level screening tool, not as a substitute for project-level feasibility analysis, financial appraisal, site-specific technical assessment, or investment due diligence.

4. **Data availability**: The framework requires access to harmonized international datasets for all country-criterion pairs. Countries with missing data on key indicators (e.g., electricity price volatility) are excluded from the sample. The 36-country sample was chosen partly because these countries provide relatively strong access to comparable secondary data.

5. **Model scope**: The framework implements secondary-data matrix construction, baseline scoring, objective weighting sensitivity, persona-based ranking, explainability decomposition, fairness diagnostics, external validation, and simulated-agent robustness. Fuzzy intervals, causal-evidence weighting, and LLM-salience weighting are treated as modular extensions (not fully activated in the empirical baseline).

## Assumptions (from problem.md)

- **A1 (data comparability)**: International harmonized data sources provide sufficiently comparable indicators for strategic screening.
- **A2 (normalization adequacy)**: Min-max normalization with benefit/cost classification preserves the readiness signal.
- **A3 (equal-weight baseline)**: Equal weighting is a neutral benchmark.
- **A4 (latest-year snapshot)**: Cross-sectional data provide a meaningful current readiness snapshot.
- **A5 (country-level granularity)**: Country-level resource indicators are adequate for screening (not for project assessment).
- **A6 (synthetic agents)**: Simulated preferences provide valid robustness evidence.

## Known Limitations (from paper Section 6)

1. **Cross-sectional data limitation**: The empirical application is mainly based on the latest available cross-sectional data, limiting the ability to capture long-term transition dynamics and temporal changes in readiness.

2. **Data comparability constraints**: Public secondary data may contain comparability limitations related to national reporting practices, electricity-market definitions, and differences between wholesale and retail price data. Normalization cannot fully eliminate differences in national reporting systems.

3. **Proxy indicator constraints**: Solar irradiance and wind-speed indicators are used as country-level screening variables (from representative coordinates) and should not be interpreted as substitutes for project-level resource assessments. Electricity price volatility is a proxy indicator based on available country-level data.

4. **LLM scope limitation**: The LLM-assisted component is limited to criterion discovery and documentation support; it does not determine the final scoring, weighting, or ranking. The LLM is not used as an autonomous decision maker.

5. **Simulated-agent limitation**: Simulated-agent validation is based on synthetic preference profiles rather than observed decision-maker behavior or empirically elicited stakeholder weights. It demonstrates robustness to hypothetical heterogeneity but does not validate against real-world investment decisions.

6. **Persona weights**: Persona weight vectors are theory-informed approximations, not empirically derived from surveys or interviews with actual stakeholders. Persona stability is partially tested through perturbation analysis (+/-10%, +/-20%).

7. **External validation**: Post-hoc validation against observable benchmarks provides convergent validity evidence but does not constitute causal prediction or independent outcome validation. Comparison benchmarks may share conceptual overlap with the readiness criteria.

8. **Expert judgment not eliminated**: The framework reduces but does not eliminate the role of expert judgment. Criterion selection, benefit/cost classification, normalization choices, persona weight design, and validation benchmark selection all involve researcher decisions.
