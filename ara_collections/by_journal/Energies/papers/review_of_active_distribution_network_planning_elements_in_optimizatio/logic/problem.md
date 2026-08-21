# Problem Statement

## Observations

1. Traditional distribution network planning relies on passive "fit and forget" reinforcement strategies, worst-case assumptions, and deterministic models that cannot accommodate high DER penetration and dynamic system behavior.

2. The increasing integration of distributed energy resources (DERs), energy storage systems (ESS), electric vehicles (EVs), and demand response mechanisms creates bidirectional power flows and operational variability that passive planning methods cannot manage.

3. Existing literature on distribution system planning has primarily focused on isolated aspects — such as substation upgrades, feeder reinforcements, or DER integration — without providing a unified planning framework that integrates time horizons, decision variables, and constraints across low- and medium-voltage contexts.

4. Few reviews provide a comprehensive view of the evolving needs and new trends in the application of generative AI to power system planning and operation.

5. Active distribution networks must manage stochastic and dynamic uncertainties arising from variable renewable generation, fluctuating loads, and bidirectional power flows, requiring advanced modeling beyond traditional approaches.

6. The literature lacks holistic frameworks that integrate time horizons, decision variables, and constraints across LV/MV contexts, particularly under high DER penetration and uncertainties such as load forecast errors, EV charging variability, and cyber threats.

7. A systematic review of generative AI model categories (GANs, diffusion models, VAEs, flow-based models, transformers) and their specific applications in ADN planning has not been comprehensively compiled.

## Gaps

- **Gap 1: Missing unified planning framework.** No existing review provides a comprehensive classification of the fundamental optimization elements (horizons, objectives, variables, constraints, uncertainty, OPF formulations) in a single structured framework for ADN planning.

- **Gap 2: Incomplete generative AI application taxonomy for ADNs.** The application of generative AI to distribution network planning is scattered across disparate studies; no systematic categorization exists linking GenAI model families to specific ADN planning tasks.

- **Gap 3: Undefined transition from passive to active planning.** The evolution needs from traditional passive planning to active dynamic optimization are not systematically characterized in the literature, including the specific AC-OPF formulations, asset modeling, and uncertainty techniques required.

- **Gap 4: Emerging asset integration challenges undocumented.** The accelerating integration of data centers, AI factories, renewable energy communities, and fast-charging hubs introduces high-magnitude, fast-ramping events that lie outside traditional grid design parameters, but these challenges are not formally reviewed.

## Key Insight

The transition from passive to active distribution network planning requires a holistic redefinition of all optimization elements: planning horizons must become multi-timescale, objectives must span economic-technical-environmental dimensions, decision variables must incorporate both traditional infrastructure and flexible sources, and uncertainty modeling must move from deterministic worst-case to probabilistic and AI-driven approaches. Generative AI offers a complementary paradigm for scenario generation, uncertainty quantification, and decision support that can bridge the gap between current planning practice and the requirements of future DER-rich networks.

## Assumptions

1. The reviewed literature (104 references identified from ~500 initial records) provides sufficient coverage of the state of the art in ADN planning optimization elements and GenAI applications.

2. The PRISMA-guided systematic search across IEEE Xplore, Scopus, Web of Science, ScienceDirect, and Google Scholar (2020-2025) captures the most relevant recent developments.

3. The classification taxonomies proposed (e.g., planning horizons, objective categories, GenAI model families) are representative of the broader research landscape.
