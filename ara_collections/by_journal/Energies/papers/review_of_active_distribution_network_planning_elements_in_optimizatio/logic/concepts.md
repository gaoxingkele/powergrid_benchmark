# Concepts

## Active Distribution Network (ADN)
An evolution of traditional distribution networks characterized by bidirectional power flows, near real-time control and monitoring, integration of distributed energy resources, flexible loads, and energy storage systems. ADNs actively manage grid constraints using flexibility from DERs, demand response, EVs, and storage rather than relying solely on infrastructure reinforcement.

## Passive Distribution Network
Traditional distribution network with unidirectional power flow, limited manual monitoring and control, minimal flexibility sources, and heavy reliance on infrastructure upgrades ("fit and forget") for voltage and congestion management.

## Planning Horizon
The time span considered in distribution network planning decisions. Classified as short-term (1-4 years, expansion planning for immediate near-term needs), long-term (5-20 years, infrastructure development for future demand), and horizon-year (20+ years, strategic cost-effective infrastructure design).

## CAPEX (Capital Expenditure)
Investment costs associated with acquiring, upgrading, or installing physical assets such as substations, feeders, transformers, and energy storage systems in distribution network planning.

## OPEX (Operational Expenditure)
Ongoing costs for operating and maintaining distribution network assets, including energy losses, maintenance, and operational management.

## TOTEX (Total Expenditure)
The combined total of capital expenditure (CAPEX) and operational expenditure (OPEX).

## Hosting Capacity
The maximum amount of distributed energy resources that can be integrated into a distribution network without causing operational constraint violations, given a fixed budget or within existing infrastructure limits.

## Decision Variables
Elements subject to optimization when expanding, reinforcing, or modernizing the network. Categorized as traditional (substation locations/sizes, feeder locations/sizes, reserve feeders, transformer tap settings) and flexible/active (renewable DG, ESS, EV charging stations, voltage control devices, demand response).

## Optimal Power Flow (OPF)
A mathematical optimization formulation that determines the optimal operating point of a power system while satisfying physical and operational constraints. In planning contexts, OPF formulations include LP, MILP, MINLP, convex relaxations (SOC), and metaheuristic approaches.

## Generative AI (GenAI)
A class of artificial intelligence models that learn the underlying distribution of training data to generate new, synthetic samples. In ADN planning, GenAI models include Generative Adversarial Networks (GANs), diffusion models, Variational Autoencoders (VAEs), flow-based models, and transformer-based large language models.

## GAN-based Models
Generative models that use adversarial training between a generator and discriminator to produce realistic synthetic data. Used in ADN for scenario generation of renewable energy, load, and EV behavior; data augmentation; and cyber-resilience testing.

## Diffusion-based Models
Generative models that learn to reverse a gradual noising process, transforming random noise into coherent data samples through iterative denoising. Effective for uncertainty quantification, extreme event modeling, and resilience analysis in energy systems.

## VAE-based Models
Variational autoencoders that combine deep learning and probabilistic inference, learning to compress and reconstruct data in a lower-dimensional latent space. Used for probabilistic forecasting, scenario synthesis, and voltage stability assessment.

## Flow-based Models
Generative models using sequences of invertible transformations to map simple probability distributions into complex data distributions, enabling exact likelihood computation. Applied to renewable and load scenario generation and probabilistic OPF.

## Transformer-based Models
Models built around self-attention mechanisms that capture long-range dependencies and contextual relationships. In power systems, these include GPT, LLaMA, and specialized models (eGridGPT, PowerPulse) used for planning assistance, data mining, simulation automation, and decision support.

## Uncertainty Modeling Techniques
Methods for representing uncertainty in ADN planning input parameters. Includes probabilistic methods (stochastic/robust optimization), possibilistic (fuzzy) approaches, hybrid probabilistic-possibilistic frameworks, Information Gap Decision Theory, Monte Carlo simulations (sequential, pseudo-sequential, non-sequential), analytical methods, and approximation of probability density functions.

## Mixed-Integer Linear Programming (MILP)
An optimization technique that models both continuous and discrete variables, particularly effective for investment decisions in distribution network planning including asset type selection, capacity decisions, and system upgrades.

## Convex Relaxation
Mathematical approach that relaxes non-convex constraints to convex ones, enabling global optimality guarantees. Second-Order Cone (SOC) relaxations are notable for radial network systems and DER-rich ADN planning.

## Flexible Sources
Assets in active distribution networks that provide operational flexibility, including PV generation with inverter-based voltage regulation, energy storage systems for peak shaving, EV charging stations with V2G capabilities, and demand response programs.

## Vehicle-to-Grid (V2G)
Technology enabling electric vehicles to inject stored energy from their batteries back into the grid, providing flexibility services and supporting grid stability.

## Information Gap Decision Theory (IGDT)
A decision-making framework that explores system performance under increasing uncertainty without requiring probability distributions, valuable for long-term planning under deep uncertainty.
