# Taxonomy: Classification of MOOPF Techniques in Power Systems

## Overview

This review paper presents a multi-dimensional taxonomy of multi-objective optimal power flow (MOOPF) techniques. The taxonomy is organized along three primary axes: temporal evolution, methodological approach, and application domain.

---

## Axis 1: Chronological Evolution of Optimization Techniques

### 1.1 Traditional Period (pre-1980s to early 1990s)
- **Methods**: Linear Programming (LP), Nonlinear Programming (NLP), Mixed-Integer Programming (MIP), Quadratic Programming (QP), Newton's method
- **Characteristics**: Deterministic, mathematically rigorous, exact solutions
- **Strengths**: Fast convergence for convex problems, high numerical stability
- **Limitations**: Local minima propensity, poor scalability to large/complex systems

### 1.2 Metaheuristics and AI Period (1990s to late 2000s)
- **Methods**: Genetic Algorithms (GA), Particle Swarm Optimization (PSO), Ant Colony Optimization (ACO)
- **Characteristics**: Nature-inspired, stochastic, population-based
- **Strengths**: Handle non-linearity, non-convexity, discrete variables; avoid local optima
- **Limitations**: Slower convergence, no optimality guarantee

### 1.3 Modern Hybrid and Advanced Period (2010s to present)
- **Methods**: Hybrid deterministic-stochastic approaches, robust optimization, stochastic programming, AI/ML-based methods
- **Characteristics**: Emphasis on resilience, real-time flexibility, uncertainty handling
- **Strengths**: Balance of precision and exploration, adaptability to change
- **Focus**: Managing high variability from RES integration and smart grid technologies

---

## Axis 2: Methodological Classification

### 2.1 Classical (Deterministic/Exact) Methods
- Explicit mathematical models
- Single optimal solution per run
- Fast for small, convex systems
- Limited complexity handling
- Rigid constraint enforcement (CFD = 0)

### 2.2 Intelligent (Stochastic/Non-Exact) Methods
- **2.2.1 Simple Heuristics**: Constructive/local search, domain-specific
- **2.2.2 Metaheuristics**:
  - *Evolutionary Algorithms*: GA, NSGA-II, DE, NSGA, NSGSA
  - *Swarm Intelligence*: PSO, MOPSO, IMOPSO, ACO, ABC, GWO, WOA, ALO, HHO, SSOA, GTO, MRFO, POA, SHO
  - *Physics-based*: GSA, SMA, EO, MOSAO, MOTEO
  - *Human-based*: Imperialist Competitive Algorithm, TLBO
  - *Multi-objective frameworks*: MOEA/D, KnEA, MOGA, MODE, MOWDO, MOSGA
- **2.2.3 AI-based Methods**:
  - Artificial Neural Networks (ANN)
  - Deep Learning (SELM, DRL, DDPG, MG-ASTGCN)
  - Reinforcement Learning for sequential decision-making

### 2.3 Hybrid Methods
- Combination of deterministic + stochastic approaches
- Integration of multiple metaheuristics (e.g., PSO + DE, BA + GEWA)
- Two-stage frameworks (Pareto front generation + decision-maker preference)

---

## Axis 3: Preference Articulation in MOO

### 3.1 A Priori Methods
- Preferences expressed before optimization
- Techniques: Weighted sum, epsilon-constraint, goal programming, Lexicographic Goal Programming

### 3.2 A Posteriori Methods
- Pareto front generated first, then decision-maker selects
- Techniques: NSGA-II, MOPSO, MOEA/D, SPEA2, KnEA

### 3.3 No Preference Methods
- No explicit preference articulation

### 3.4 Multi-Objective Evolutionary Algorithms (MOEAs)
- Population-based Pareto optimization
- Dominance ranking, crowding distance, decomposition strategies

### 3.5 Data-Driven Methods
- Neural networks, reinforcement learning
- Learn complex relationships between objectives and decision criteria

---

## Axis 4: Application Domain Taxonomy

### 4.1 Economic Dispatch / Optimal Power Flow
- Minimizing generation cost
- Multi-objective cost-emission dispatch
- Security-constrained OPF

### 4.2 Network Reconfiguration
- Topology optimization for loss minimization
- Voltage profile improvement

### 4.3 Power Distribution Planning
- Optimal DG placement and sizing
- Reactive power planning (RPP/ORPD)

### 4.4 Operational Planning with RES Integration
- Hybrid renewable energy system design
- Stochastic OPF with wind/solar uncertainty
- Microgrid energy management

### 4.5 Emerging Applications
- Demand response coordination
- Electric vehicle integration
- FACTS device optimization (TCSC, UPFC, IPFC)
- Energy storage system planning
- Multi-energy system optimization
